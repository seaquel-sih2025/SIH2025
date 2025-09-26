# Update your backend/app/api/endpoints/peer_verifications.py

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, text
from typing import List, Optional
import uuid
from datetime import datetime
from pydantic import BaseModel

from app.db.session import get_db
from app.db.models import User, Report, PeerVerification, SafetyZone
from app.api.dependencies import get_current_user

router = APIRouter()

class PeerVerificationRequest(BaseModel):
    report_id: uuid.UUID
    action: str  # 'verify', 'reject', 'safe', 'not_safe'
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy: Optional[float] = None

@router.post("/submit", summary="Submit peer verification with location")
async def submit_peer_verification(
    request: PeerVerificationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit a peer verification response with optional location data."""
    
    # Check if report exists
    report = await db.get(Report, request.report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Check if user already verified this report
    existing = await db.execute(
        select(PeerVerification).where(
            PeerVerification.report_id == request.report_id,
            PeerVerification.verifier_user_id == current_user.id
        )
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="You have already responded to this report")
    
    # Validate location for safety responses
    if request.action in ['safe', 'not_safe']:
        if not request.latitude or not request.longitude:
            raise HTTPException(
                status_code=400, 
                detail="Location is required for safety responses"
            )
    
    # Create peer verification record
    verification = PeerVerification(
        report_id=request.report_id,
        verifier_user_id=current_user.id,
        verification_type=request.action
    )
    db.add(verification)
    
    safety_zone_created = False
    
    # Handle safety zone creation for 'safe' and 'not_safe' responses
    if request.action in ['safe', 'not_safe'] and request.latitude and request.longitude:
        zone_type = 'safe_green' if request.action == 'safe' else 'unsafe_purple'
        
        # Create PostGIS point from user's location
        user_location_wkt = f'SRID=4326;POINT({request.longitude} {request.latitude})'
        
        safety_zone = SafetyZone(
            user_id=current_user.id,
            report_id=request.report_id,
            zone_type=zone_type,
            location=user_location_wkt,
            radius_meters=1000  # 1km radius
        )
        db.add(safety_zone)
        safety_zone_created = True
    
    # Update confidence score if it's a verify/reject action
    confidence_updated = False
    if request.action in ['verify', 'reject']:
        # Get all peer verifications for this report (including the new one we're adding)
        all_verifications = await db.execute(
            select(PeerVerification).where(
                PeerVerification.report_id == request.report_id,
                PeerVerification.verification_type.in_(['verify', 'reject'])
            )
        )
        peer_verifs = list(all_verifications.scalars().all())
        
        # Add the current verification to the count
        if request.action in ['verify', 'reject']:
            peer_verifs.append(verification)
        
        # Calculate peer confidence boost
        verify_count = sum(1 for v in peer_verifs if v.verification_type == 'verify')
        reject_count = sum(1 for v in peer_verifs if v.verification_type == 'reject')
        total_responses = verify_count + reject_count
        
        if total_responses > 0:
            peer_confidence = verify_count / total_responses
            # Add peer confidence to the existing score (weighted)
            current_score = report.final_confidence_score or 0.0
            
            # Give peer verification increasing weight based on number of responses
            peer_weight = min(0.4, 0.1 + (total_responses * 0.05))  # Max 40% weight
            
            updated_score = (current_score * (1 - peer_weight)) + (peer_confidence * peer_weight)
            report.final_confidence_score = min(1.0, updated_score)
            confidence_updated = True
            
            # Update status based on new confidence
            if report.final_confidence_score >= 0.8:
                report.status = "verified"
            elif report.final_confidence_score <= 0.3:
                report.status = "rejected"
    
    await db.commit()
    
    # Prepare response message
    response_messages = []
    if request.action == 'verify':
        response_messages.append("Report verified successfully")
    elif request.action == 'reject':
        response_messages.append("Report rejected successfully")
    elif request.action == 'safe':
        response_messages.append("Safety status recorded - you're marked as safe")
        if safety_zone_created:
            response_messages.append("Safe zone created around your location")
    elif request.action == 'not_safe':
        response_messages.append("Safety status recorded - alert zone created")
        if safety_zone_created:
            response_messages.append("Alert zone created around your location")
    
    if confidence_updated:
        response_messages.append(f"Report confidence updated to {report.final_confidence_score:.2f}")
    
    return {
        "message": ". ".join(response_messages),
        "report_id": request.report_id,
        "action": request.action,
        "updated_confidence": report.final_confidence_score,
        "safety_zone_created": safety_zone_created,
        "location_captured": bool(request.latitude and request.longitude)
    }

@router.get("/safety-zones/{report_id}", summary="Get safety zones for a specific report")
async def get_safety_zones_for_report(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get safety zones for a specific report to display on the map."""
    
    # Query safety zones with user information
    query = text("""
        SELECT sz.id, sz.zone_type, sz.radius_meters, sz.created_at,
               ST_X(sz.location) as longitude, ST_Y(sz.location) as latitude,
               u.full_name
        FROM safety_zones sz
        JOIN users u ON sz.user_id = u.id
        WHERE sz.report_id = :report_id
        ORDER BY sz.created_at DESC
    """)
    
    result = await db.execute(query, {"report_id": report_id})
    zones = result.fetchall()
    
    zone_data = []
    for zone in zones:
        zone_data.append({
            "id": str(zone.id),
            "zone_type": zone.zone_type,
            "latitude": zone.latitude,
            "longitude": zone.longitude,
            "radius_meters": zone.radius_meters,
            "user_name": zone.full_name,
            "created_at": zone.created_at.isoformat() if zone.created_at else None,
            "color": "#22c55e" if zone.zone_type == "safe_green" else "#a855f7"  # Green for safe, purple for unsafe
        })
    
    return {
        "report_id": report_id,
        "zones": zone_data,
        "total_zones": len(zone_data)
    }

@router.get("/my-verifications", summary="Get current user's peer verifications")
async def get_my_verifications(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get the current user's peer verification history."""
    
    query = text("""
        SELECT pv.report_id, pv.verification_type, pv.created_at,
               r.user_hazard_type, r.user_description,
               ST_X(r.user_location) as report_longitude, 
               ST_Y(r.user_location) as report_latitude
        FROM peer_verifications pv
        JOIN reports r ON pv.report_id = r.id
        WHERE pv.verifier_user_id = :user_id
        ORDER BY pv.created_at DESC
        LIMIT :limit
    """)
    
    result = await db.execute(query, {"user_id": current_user.id, "limit": limit})
    verifications = result.fetchall()
    
    verification_data = []
    for verification in verifications:
        verification_data.append({
            "report_id": str(verification.report_id),
            "action": verification.verification_type,
            "hazard_type": verification.user_hazard_type,
            "description": verification.user_description,
            "report_location": {
                "latitude": verification.report_latitude,
                "longitude": verification.report_longitude
            },
            "created_at": verification.created_at.isoformat() if verification.created_at else None
        })
    
    return {
        "verifications": verification_data,
        "total": len(verification_data)
    }