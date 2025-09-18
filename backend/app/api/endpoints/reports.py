from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends, Header
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from uuid import uuid4
import uuid

from app.db.models import User, HazardType, Report, Media
from app.db.session import get_db
from app.models.pydantic_models import ReportSubmitResponse
from app.services.rabbitmq_service import rabbitmq_service
from app.services.s3_service import s3_service
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/submit", response_model=ReportSubmitResponse, status_code=202, summary="Submit a new Hazard Report")
async def submit_hazard_report(
    latitude: float = Header(..., description="Auto-detected latitude from device GPS"),
    longitude: float = Header(..., description="Auto-detected longitude from device GPS"),
    user_hazard_type: HazardType = Form(..., description="The type of hazard observed"),
    user_description: Optional[str] = Form(None, description="A description of the hazard"),
    media_files: List[UploadFile] = File([], description="Optional list of image, video, or audio files"),
    current_user: User = Depends(get_current_user)
):
    report_id = uuid4()

    media_payloads = []
    for file in media_files:
        content_type = file.content_type
        if content_type.startswith("image/"): media_type = "image"
        elif content_type.startswith("video/"): media_type = "video"
        elif content_type.startswith("audio/"): media_type = "audio"
        else: continue
            
        # Call the S3 service to upload the file and get a REAL URL
        real_file_url = s3_service.upload_file(file, media_type, report_id)
        
        # We only add the file to the message if the upload was successful
        if real_file_url:
            media_payloads.append({
                "file_url": real_file_url,
                "media_type": media_type
            })
    
    message_body = {
        "report_id": str(report_id),
        "user_id": str(current_user.id),
        "report_data": {
            "user_hazard_type": user_hazard_type.value,
            "user_description": user_description,
            "latitude": latitude,
            "longitude": longitude
        },
        "media_files": media_payloads # This now contains REAL S3 URLs
    }

    try:
        await rabbitmq_service.publish_message("report_processing_queue", message_body)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not queue report for processing.")

    return {"message": "Hazard report has been accepted for processing.", "report_id": report_id}


@router.get("/hotspots", summary="List report hotspots with coordinates and confidence")
async def list_hotspots(db: AsyncSession = Depends(get_db)):
    """Return an array of hotspots with latitude, longitude, and final_confidence_score.
    If score is null, default to 0.0. Only includes reports that have a location.
    """
    # Extract WKT and parse without requiring Shapely
    result = await db.execute(
        select(
            Report.id,
            Report.final_confidence_score,
            Report.status,
            Report.user_hazard_type,
            Report.created_at,
            func.ST_AsText(Report.user_location)
        )
    )
    rows = result.all()

    hotspots: List[dict] = []
    for (rid, conf, status, hazard, created_at, wkt) in rows:
        if not wkt:
            continue
        # Normalize values
        conf_val = float(conf or 0.0)
        status_str = status.value if hasattr(status, 'value') else str(status)
        # Reject only when confidence below threshold (0.35)
        if conf_val < 0.35:
            continue
        # WKT format: 'POINT(lon lat)'
        try:
            coords = wkt.strip().replace("POINT(", "").replace(")", "").split()
            if len(coords) != 2:
                continue
            lng = float(coords[0])
            lat = float(coords[1])
        except Exception:
            continue
        hotspots.append({
            "report_id": str(rid),
            "latitude": lat,
            "longitude": lng,
            "confidence": conf_val,
            "status": status_str,
            "hazard_type": hazard.value if hasattr(hazard, 'value') else str(hazard),
            "created_at": created_at.isoformat() if created_at else None
        })

    return {"items": hotspots, "count": len(hotspots)}


@router.get("/recent", summary="List recent reports with basic info")
async def list_recent_reports(limit: int = 9, db: AsyncSession = Depends(get_db)):
    """Return most recent reports with minimal fields for the dashboard.
    Includes: id, hazard_type, status, created_at, user_description, user_city, thumbnail_url.
    """
    # Clamp limit to a reasonable range
    safe_limit = max(1, min(limit, 24))

    result = await db.execute(
        select(Report).order_by(Report.created_at.desc()).limit(safe_limit)
    )
    reports = result.scalars().all()

    items: List[dict] = []
    for r in reports:
        thumb_url = None
        try:
            # Fetch one media file (first by created_at) for thumbnail if available
            m_res = await db.execute(
                select(Media.file_url).where(Media.report_id == r.id).order_by(Media.created_at.asc()).limit(1)
            )
            mrow = m_res.first()
            if mrow:
                thumb_url = mrow[0]
        except Exception:
            thumb_url = None

        items.append({
            "id": str(r.id),
            "hazard_type": r.user_hazard_type.value if hasattr(r.user_hazard_type, 'value') else str(r.user_hazard_type),
            "status": r.status.value if hasattr(r.status, 'value') else str(r.status),
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "user_description": r.user_description,
            "user_city": r.user_city,
            "thumbnail_url": thumb_url,
        })

    return {"items": items, "count": len(items)}