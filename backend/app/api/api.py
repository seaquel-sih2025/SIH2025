from fastapi import APIRouter

from app.api.endpoints import reports, auth, verifications, feed
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(verifications.router, prefix="/verifications", tags=["Verifications"])
api_router.include_router(feed.router, prefix="/feed", tags=["Feed"])

