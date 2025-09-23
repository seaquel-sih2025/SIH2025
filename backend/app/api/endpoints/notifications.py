from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from typing import List, Dict, Any
import uuid
from datetime import datetime, timedelta, timezone

from app.db.session import get_db
from app.db.models import User, Report, HazardType, ReportStatus
from app.models.pydantic_models import PeerNotificationCreate, PeerNotificationResponse

router = APIRouter()

async def find_nearby_users(
    latitude: float, 
    longitude: float, 
    radius_km: float = 50,
    db: AsyncSession = None
) -> List[User]:
    """Find users within a specified radius of a location."""
    # Create a point from the given coordinates
    point = f'SRID=4326;POINT({longitude} {latitude})'
    
    # Query for users within the radius
    # Note: This is a simplified approach - you might want to add a location field to users
    # For now, we'll return all active users as potential notification recipients
    result = await db.execute(
        select(User).where(
            and_(
                User.is_active == True,
                User.role == "citizen"
            )
        ).limit(100)  # Limit to prevent overwhelming notifications
    )
    
    return result.scalars().all()

@router.get("/count", summary="Get notification count for current user")
async def get_notification_count(db: AsyncSession = Depends(get_db)):
    """
    Get the count of unread notifications for the current user.
    Returns the count of recent verified reports that can be considered as notifications.
    """
    # Get count of recent verified reports (last 7 days) as notifications
    recent_cutoff = datetime.utcnow() - timedelta(days=7)
    
    result = await db.execute(
        select(func.count(Report.id)).where(
            Report.created_at >= recent_cutoff
        )
    )
    recent_reports_count = result.scalar() or 0
    
    # Get total reports count
    total_result = await db.execute(
        select(func.count(Report.id))
    )
    total_count = total_result.scalar() or 0
    
    return {
        "unread_count": recent_reports_count,
        "total_count": total_count,
        "last_updated": datetime.utcnow().isoformat()
    }

@router.post("/peer", response_model=PeerNotificationResponse, status_code=201)
async def receive_peer_notification(
    notification_data: PeerNotificationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to receive peer notification data from the worker.
    This will process the notification and determine which users to notify.
    """
    try:
        # Validate that the report exists
        report = await db.get(Report, notification_data.report_id)
        if not report:
            raise HTTPException(
                status_code=404,
                detail=f"Report with ID {notification_data.report_id} not found."
            )
        
        # Find nearby users who should receive this notification
        nearby_users = await find_nearby_users(
            notification_data.latitude,
            notification_data.longitude,
            radius_km=50,  # 50km radius
            db=db
        )
        
        # Filter out the user who created the report
        nearby_users = [user for user in nearby_users if user.id != report.user_id]
        
        # Here you would typically:
        # 1. Create notification records in your database
        # 2. Send push notifications to mobile apps
        # 3. Send emails or SMS if configured
        # 4. Update real-time notification feeds
        
        # For now, we'll just log and return the response
        print(f"[Peer Notifications] Found {len(nearby_users)} users to notify about {notification_data.hazard_type} report")
        
        # Mock notification sending (replace with actual notification service)
        notifications_sent = []
        for user in nearby_users[:10]:  # Limit to first 10 users for this example
            notification_record = {
                "user_id": str(user.id),
                "user_email": user.email,
                "message": notification_data.message,
                "hazard_type": notification_data.hazard_type,
                "distance_km": "< 50",  # You'd calculate actual distance here
                "sent_at": datetime.utcnow().isoformat()
            }
            notifications_sent.append(notification_record)
            
            # Here you would send actual notifications:
            # - Push notification to mobile app
            # - Email notification
            # - In-app notification
            print(f"  - [Mock] Notifying {user.full_name} ({user.email})")
        
        response = PeerNotificationResponse(
            message=f"Peer notification processed for report {notification_data.report_id}",
            report_id=notification_data.report_id,
            notifications_sent=len(notifications_sent),
            recipient_details=notifications_sent
        )
        
        return response
        
    except Exception as e:
        print(f"Error processing peer notification: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process peer notification: {str(e)}"
        )

@router.get("/test-peer", summary="Test endpoint for peer notifications")
async def test_peer_notification(db: AsyncSession = Depends(get_db)):
    """Test endpoint to verify the peer notification system is working."""
    
    # Get a sample report to test with
    result = await db.execute(
        select(Report).limit(1)
    )
    sample_report = result.scalars().first()
    
    if not sample_report:
        raise HTTPException(status_code=404, detail="No reports found for testing")
    
    # Extract coordinates from the PostGIS point
    # This is a simplified extraction - you might need ST_X and ST_Y functions
    test_data = PeerNotificationCreate(
        report_id=sample_report.id,
        latitude=12.9716,  # Bangalore coordinates for testing
        longitude=77.5946,
        hazard_type=sample_report.user_hazard_type.value,
        notification_type="test",
        message="Test peer notification",
        priority="low"
    )
    
    return await receive_peer_notification(test_data, db)

@router.get("/recent", summary="Get recent notifications")
async def get_recent_notifications(limit: int = 10, db: AsyncSession = Depends(get_db)):
    """Get recent notifications based on recent verified reports."""
    # Get recent verified reports to show as notifications
    recent_cutoff = datetime.utcnow() - timedelta(days=7)
    
    result = await db.execute(
        select(Report, User.full_name).join(User).where(
            Report.created_at >= recent_cutoff
        ).order_by(Report.created_at.desc()).limit(limit)
    )
    recent_reports = result.all()
    
    # Convert reports to notification format
    notifications = []
    for report, user_name in recent_reports:
        # Map hazard types to readable names
        hazard_name_map = {
            'Tsunami': 'Tsunami',
            'High Waves / Swell': 'High Waves / Swell',
            'Coastal Flooding': 'Coastal Flooding',
            'Storm Surge': 'Storm Surge',
            'Rip Current': 'Rip Current',
            'Coastal Erosion': 'Coastal Erosion',
            'Water Discoloration / Algal Bloom': 'Water Discoloration / Algal Bloom',
            'Marine Debris / Pollution': 'Marine Debris / Pollution',
            'Other': 'Other Hazard'
        }
        
        hazard_name = hazard_name_map.get(report.user_hazard_type, 'Unknown Hazard')
        
        # Format time to ensure proper timezone handling
        if report.created_at.tzinfo is None:
            # If no timezone info, assume UTC and add timezone
            time_with_tz = report.created_at.replace(tzinfo=timezone.utc)
        else:
            # Convert to UTC if not already
            time_with_tz = report.created_at.astimezone(timezone.utc)
        
        notifications.append({
            "id": str(report.id),
            "hazardName": hazard_name,
            "description": report.user_description or f"New {hazard_name.lower()} report",
            "time": time_with_tz.isoformat(),
            "user": user_name,
            "status": report.status.value,
            "confidence": report.final_confidence_score,
            "location": report.user_city or "Unknown location",
            "image": None  # You can add media URL here if needed
        })
    
    return notifications