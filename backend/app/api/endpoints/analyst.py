from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func, text
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
import json
import csv
import io

from app.models.pydantic_models import UserRead
from app.db.models import User, Report, ReportStatus, HazardType, Verification
from app.db.session import get_db
from app.api.dependencies import get_current_analyst
from pydantic import BaseModel

router = APIRouter()

# Pydantic models for Analyst endpoints
class QueryFilters(BaseModel):
    event_types: Optional[List[HazardType]] = None
    keywords: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[ReportStatus] = None
    min_confidence: Optional[float] = None
    max_confidence: Optional[float] = None

class QueryResponse(BaseModel):
    reports: List[Dict[str, Any]]
    total_count: int
    filters_applied: QueryFilters

class LagAnalysisData(BaseModel):
    date: str
    avg_verification_time_minutes: float
    report_count: int
    hazard_type: str

class TrendData(BaseModel):
    keyword: str
    frequency: int
    sentiment_score: float
    time_period: str

class ReliabilityScore(BaseModel):
    user_id: UUID
    user_name: str
    total_reports: int
    verified_reports: int
    reliability_percentage: float
    avg_confidence_score: float

@router.post("/query", response_model=QueryResponse)
async def custom_data_query(
    filters: QueryFilters,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_analyst),
    db: AsyncSession = Depends(get_db)
):
    """Custom data query builder with filters."""
    
    # Build the query based on filters
    query = select(Report)
    conditions = []
    
    if filters.event_types:
        conditions.append(Report.user_hazard_type.in_(filters.event_types))
    
    if filters.start_date:
        conditions.append(Report.created_at >= filters.start_date)
    
    if filters.end_date:
        conditions.append(Report.created_at <= filters.end_date)
    
    if filters.status:
        conditions.append(Report.status == filters.status)
    
    if filters.min_confidence is not None:
        conditions.append(Report.final_confidence_score >= filters.min_confidence)
    
    if filters.max_confidence is not None:
        conditions.append(Report.final_confidence_score <= filters.max_confidence)
    
    if filters.keywords:
        # Search in description for keywords
        keyword_conditions = []
        for keyword in filters.keywords:
            keyword_conditions.append(Report.user_description.ilike(f"%{keyword}%"))
        conditions.append(func.or_(*keyword_conditions))
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total_count = count_result.scalar()
    
    # Apply pagination
    query = query.offset(offset).limit(limit).order_by(Report.created_at.desc())
    
    result = await db.execute(query)
    reports = result.scalars().all()
    
    # Convert to dict format
    reports_data = []
    for report in reports:
        # Get user info
        user_query = select(User).where(User.id == report.user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalars().first()
        
        reports_data.append({
            "id": str(report.id),
            "user_id": str(report.user_id),
            "user_name": user.full_name if user else "Unknown",
            "hazard_type": report.user_hazard_type.value,
            "description": report.user_description,
            "city": report.user_city,
            "confidence_score": report.final_confidence_score,
            "status": report.status.value,
            "created_at": report.created_at.isoformat(),
            "location": {
                "latitude": None,  # TODO: Extract from Geography field
                "longitude": None  # TODO: Extract from Geography field
            }
        })
    
    return QueryResponse(
        reports=reports_data,
        total_count=total_count,
        filters_applied=filters
    )

@router.get("/lag-analysis", response_model=List[LagAnalysisData])
async def get_lag_analysis(
    days_back: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_analyst),
    db: AsyncSession = Depends(get_db)
):
    """Report-to-warning lag analysis dashboard data."""
    
    # TODO: Implement proper lag analysis
    # This would require tracking when reports are created vs when warnings are issued
    # For now, return mock data
    
    mock_data = []
    for i in range(days_back):
        date = datetime.now() - timedelta(days=i)
        for hazard_type in ["Tsunami", "High Waves / Swell", "Storm Surge"]:
            mock_data.append(LagAnalysisData(
                date=date.strftime("%Y-%m-%d"),
                avg_verification_time_minutes=float(30 + (i % 60)),
                report_count=max(1, 10 - (i % 8)),
                hazard_type=hazard_type
            ))
    
    return mock_data

@router.get("/nlp-trends", response_model=List[TrendData])
async def get_nlp_trends(
    days_back: int = Query(7, ge=1, le=90),
    current_user: User = Depends(get_current_analyst),
    db: AsyncSession = Depends(get_db)
):
    """Trending keywords & sentiment timeline from NLP analysis."""
    
    # TODO: Implement proper NLP trend analysis from verification data
    # This would analyze the result_data from Verification table where source = 'nlp_pipeline'
    
    mock_trends = [
        TrendData(
            keyword="tsunami",
            frequency=25,
            sentiment_score=8.5,  # High urgency/panic
            time_period="last_7_days"
        ),
        TrendData(
            keyword="flooding",
            frequency=18,
            sentiment_score=6.2,
            time_period="last_7_days"
        ),
        TrendData(
            keyword="evacuation",
            frequency=12,
            sentiment_score=7.8,
            time_period="last_7_days"
        )
    ]
    
    return mock_trends

@router.get("/reliability-scores", response_model=List[ReliabilityScore])
async def get_reliability_scores(
    limit: int = Query(50, ge=1, le=200),
    min_reports: int = Query(5, ge=1, le=50),
    current_user: User = Depends(get_current_analyst),
    db: AsyncSession = Depends(get_db)
):
    """Citizen reliability scorecard based on verification history."""
    
    # Query to get user reliability stats
    query = text("""
        SELECT 
            u.id as user_id,
            u.full_name as user_name,
            COUNT(r.id) as total_reports,
            COUNT(CASE WHEN r.status = 'verified' THEN 1 END) as verified_reports,
            ROUND(
                (COUNT(CASE WHEN r.status = 'verified' THEN 1 END)::float / COUNT(r.id) * 100), 2
            ) as reliability_percentage,
            ROUND(AVG(r.final_confidence_score), 2) as avg_confidence_score
        FROM users u
        JOIN reports r ON u.id = r.user_id
        WHERE u.role = 'citizen'
        GROUP BY u.id, u.full_name
        HAVING COUNT(r.id) >= :min_reports
        ORDER BY reliability_percentage DESC, total_reports DESC
        LIMIT :limit
    """)
    
    result = await db.execute(query, {"min_reports": min_reports, "limit": limit})
    rows = result.fetchall()
    
    reliability_scores = []
    for row in rows:
        reliability_scores.append(ReliabilityScore(
            user_id=row.user_id,
            user_name=row.user_name,
            total_reports=row.total_reports,
            verified_reports=row.verified_reports,
            reliability_percentage=float(row.reliability_percentage),
            avg_confidence_score=float(row.avg_confidence_score or 0)
        ))
    
    return reliability_scores

@router.get("/export")
async def export_data(
    format: str = Query("csv", regex="^(csv|json)$"),
    filters: Optional[str] = Query(None),  # JSON string of QueryFilters
    current_user: User = Depends(get_current_analyst),
    db: AsyncSession = Depends(get_db)
):
    """Downloadable CSV/JSON with validated dataset."""
    
    # Parse filters if provided
    query_filters = QueryFilters()
    if filters:
        try:
            filter_dict = json.loads(filters)
            query_filters = QueryFilters(**filter_dict)
        except (json.JSONDecodeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filters format"
            )
    
    # Get data using the same logic as custom_data_query
    query = select(Report)
    conditions = []
    
    if query_filters.event_types:
        conditions.append(Report.user_hazard_type.in_(query_filters.event_types))
    
    if query_filters.start_date:
        conditions.append(Report.created_at >= query_filters.start_date)
    
    if query_filters.end_date:
        conditions.append(Report.created_at <= query_filters.end_date)
    
    if query_filters.status:
        conditions.append(Report.status == query_filters.status)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(Report.created_at.desc()).limit(10000)  # Limit for performance
    
    result = await db.execute(query)
    reports = result.scalars().all()
    
    # Prepare data
    export_data = []
    for report in reports:
        # Get user info
        user_query = select(User).where(User.id == report.user_id)
        user_result = await db.execute(user_query)
        user = user_result.scalars().first()
        
        export_data.append({
            "report_id": str(report.id),
            "user_id": str(report.user_id),
            "user_name": user.full_name if user else "Unknown",
            "hazard_type": report.user_hazard_type.value,
            "description": report.user_description or "",
            "city": report.user_city or "",
            "confidence_score": report.final_confidence_score,
            "status": report.status.value,
            "created_at": report.created_at.isoformat()
        })
    
    if format == "csv":
        # Create CSV
        output = io.StringIO()
        if export_data:
            writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
            writer.writeheader()
            writer.writerows(export_data)
        
        output.seek(0)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=reports_export.csv"}
        )
    
    else:  # JSON format
        json_output = json.dumps(export_data, indent=2)
        
        return StreamingResponse(
            io.BytesIO(json_output.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=reports_export.json"}
        )
