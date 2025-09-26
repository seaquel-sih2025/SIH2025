from fastapi import APIRouter

from app.api.endpoints import reports, auth, verifications, feed, users, notifications, safety_circles

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/user", tags=["User"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(verifications.router, prefix="/verifications", tags=["Verifications"])
api_router.include_router(feed.router, prefix="/feed", tags=["Feed"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(safety_circles.router, prefix="/safety-circles", tags=["Safety Circles"])