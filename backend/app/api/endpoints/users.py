from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
import uuid
import os
from typing import List

from app.models.pydantic_models import UserRead, UserUpdate
from app.db.models import User, Report
from app.db.session import get_db
from app.api.dependencies import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserRead)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile information"""
    return current_user

@router.put("/profile", response_model=UserRead)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's profile information"""
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user

@router.post("/profile/picture")
async def upload_profile_picture(
    profile_picture: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upload profile picture"""
    # Validate file type
    if not profile_picture.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads/profile_pictures"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = profile_picture.filename.split('.')[-1]
    filename = f"{current_user.id}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await profile_picture.read()
        buffer.write(content)
    
    # Update user profile picture URL - use full URL for frontend
    profile_picture_url = f"/uploads/profile_pictures/{filename}"
    current_user.profile_picture = profile_picture_url
    
    await db.commit()
    await db.refresh(current_user)
    
    return {"profile_picture": profile_picture_url}

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user statistics"""
    # Get total reports
    total_reports_query = select(func.count(Report.id)).where(Report.user_id == current_user.id)
    total_reports_result = await db.execute(total_reports_query)
    total_reports = total_reports_result.scalar() or 0
    
    # Get verified reports
    verified_reports_query = select(func.count(Report.id)).where(
        Report.user_id == current_user.id,
        Report.status == "verified"
    )
    verified_reports_result = await db.execute(verified_reports_query)
    verified_reports = verified_reports_result.scalar() or 0
    
    # Calculate safety rating (simplified - based on verification rate)
    safety_rating = 0.0
    if total_reports > 0:
        safety_rating = min(5.0, (verified_reports / total_reports) * 5.0)
    
    # Mock data for other stats (replace with real calculations later)
    stats = {
        "total_reports": total_reports,
        "verified_reports": verified_reports,
        "safety_rating": round(safety_rating, 1),
        "community_helps": 0,  # TODO: Implement community helps tracking
        "forum_views": 0,      # TODO: Implement forum views tracking
        "badges_earned": 0,    # TODO: Implement badges system
        "monthly_reports": 0,  # TODO: Implement monthly stats
        "monthly_forum_posts": 0,
        "monthly_helps": 0,
        "monthly_points": 0
    }
    
    return stats

@router.get("/activity")
async def get_user_activity(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's recent activity"""
    # Get recent reports
    reports_query = select(Report).where(
        Report.user_id == current_user.id
    ).order_by(Report.created_at.desc()).limit(limit)
    
    reports_result = await db.execute(reports_query)
    reports = reports_result.scalars().all()
    
    activities = []
    for report in reports:
        activities.append({
            "id": str(report.id),
            "type": "submitted",
            "title": f"Submitted {report.user_hazard_type.value} report",
            "created_at": report.created_at,
            "description": report.user_description
        })
    
    return activities

@router.get("/reports")
async def get_user_reports(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's reports"""
    reports_query = select(Report).where(
        Report.user_id == current_user.id
    ).order_by(Report.created_at.desc()).limit(limit)
    
    reports_result = await db.execute(reports_query)
    reports = reports_result.scalars().all()
    
    return reports

@router.get("/badges")
async def get_user_badges(
    current_user: User = Depends(get_current_user)
):
    """Get user's badges (mock data for now)"""
    # TODO: Implement badges system
    return []

@router.get("/rewards")
async def get_user_rewards(
    current_user: User = Depends(get_current_user)
):
    """Get user's rewards (mock data for now)"""
    # TODO: Implement rewards system
    return []
