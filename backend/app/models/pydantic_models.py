from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

from app.db.models import UserRole, HazardType

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str | None = None

class UserCreate(UserBase):
    password: str
    role: UserRole

class UserRead(UserBase):
    id: UUID
    role: UserRole
    is_active: bool
    bio: str | None = None
    location: str | None = None
    profile_picture: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    bio: str | None = None
    location: str | None = None
    profile_picture: str | None = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ReportCreate(BaseModel):
    user_hazard_type: HazardType
    user_description: str | None = None
    latitude: float
    longitude: float

class ReportSubmitResponse(BaseModel):
    message: str
    report_id: UUID

class VerificationCreate(BaseModel):
    """
    A generic model for submitting verification results from any source.
    """
    report_id: UUID
    result_data: dict = Field(..., example={"condition": "Rain", "temp_celsius": 25.5})




# Add these classes to your existing backend/app/models/pydantic_models.py file

from typing import List, Dict, Any

class PeerNotificationCreate(BaseModel):
    report_id: UUID
    latitude: float
    longitude: float
    hazard_type: str
    notification_type: str = "new_report_alert"
    message: str
    priority: str = "normal"

class PeerNotificationResponse(BaseModel):
    message: str
    report_id: UUID
    notifications_sent: int
    recipient_details: List[Dict[str, Any]]


# Add to backend/app/models/pydantic_models.py

class SafetyStatusUpdate(BaseModel):
    report_id: UUID
    is_safe: bool
    latitude: float
    longitude: float
    message: str = None

class SafetyZoneResponse(BaseModel):
    zone_id: str
    zone_type: str  # "safe" or "danger"
    latitude: float
    longitude: float
    user_count: int
    created_at: datetime
    
class MapZone(BaseModel):
    id: str
    type: str  # "safe", "danger", "hazard"
    latitude: float
    longitude: float
    radius: float
    color: str  # hex color for map display
    opacity: float
    created_at: datetime
    report_id: UUID = None