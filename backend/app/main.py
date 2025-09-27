from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.api import api_router
from app.core.config import settings
from app.services.rabbitmq_service import rabbitmq_service
from app.services.connectivity_service import connectivity_service
from app.services.sync_service import sync_service
from app.db.sqlite_setup import init_sqlite_db
import os

app = FastAPI(
    title="Pravaah API",
    description="API for crowdsourced ocean hazard reporting and social media analytics.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Initialize SQLite database for offline sync
    await init_sqlite_db()
    
    # Connect to RabbitMQ
    await rabbitmq_service.connect()
    
    # Start connectivity monitoring
    await connectivity_service.start_monitoring()
    
    # Start sync service
    await sync_service.start_sync_service()
    
    print("Successfully connected to RabbitMQ.")
    print("Pravaah API startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    # Stop sync services
    await sync_service.stop_sync_service()
    await connectivity_service.stop_monitoring()
    
    # Close RabbitMQ connection
    await rabbitmq_service.close()
    
    print("RabbitMQ connection closed.")
    print("Pravaah API shutdown complete.")

app.include_router(api_router, prefix="/api")

# Create uploads directories if they don't exist
os.makedirs("uploads/profile_pictures", exist_ok=True)
os.makedirs("uploads/media", exist_ok=True)

# Mount static files for serving uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "active", "message": "Welcome to the Pravaah API!"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify API and database connectivity"""
    try:
        from app.db.session import engine
        from sqlalchemy import text
        # Test database connection
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected",
            "api": "running",
            "message": "All systems operational"
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "database": "disconnected",
            "api": "running",
            "error": str(e)
        }