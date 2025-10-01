from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.api import api_router
from app.core.config import settings
import os
import asyncio
from app.services.rabbitmq_service import rabbitmq_service
from app.services.connectivity_service import connectivity_service
from app.services.sync_service import sync_service
from app.db.sqlite_setup import init_sqlite_db

app = FastAPI(
    title="Pravaah API",
    description="API for crowdsourced ocean hazard reporting and social media analytics.",
    version="0.1.0"
)

# Get environment - default to production for safety
environment = os.getenv("ENVIRONMENT", "production")

# Configure CORS based on environment
if environment == "development":
    # Local development - allow all origins temporarily for debugging
    allowed_origins = ["*"]
else:
    # Production - always explicit origins
    allowed_origins = []
    
    # Add frontend URL from environment variable (primary)
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        # Clean the URL (remove trailing slash)
        frontend_url = frontend_url.rstrip('/')
        allowed_origins.append(frontend_url)
    
    # Fallback to default Render URL if FRONTEND_URL not set
    if not allowed_origins:
        allowed_origins.append("https://pravaah-frontend.onrender.com")
    
    # Add Vercel deployment URLs if present
    vercel_url = os.getenv("VERCEL_URL")
    if vercel_url:
        allowed_origins.append(f"https://{vercel_url}")
    
    # Add any additional production origins
    additional_origins = os.getenv("ADDITIONAL_CORS_ORIGINS")
    if additional_origins:
        origins_list = [origin.strip() for origin in additional_origins.split(",")]
        allowed_origins.extend(origins_list)
    # Production - always explicit origins
    allowed_origins = []
    
    # Add frontend URL from environment variable (primary)
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        # Clean the URL (remove trailing slash)
        frontend_url = frontend_url.rstrip('/')
        allowed_origins.append(frontend_url)
    
    # Fallback to default Render URL if FRONTEND_URL not set
    if not allowed_origins:
        allowed_origins.append("https://pravaah-frontend.onrender.com")
    
    # Add Vercel deployment URLs if present
    vercel_url = os.getenv("VERCEL_URL")
    if vercel_url:
        allowed_origins.append(f"https://{vercel_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False if "*" in allowed_origins else True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Add debugging middleware for CORS issues (development only)
if environment == "development":
    @app.middleware("http")
    async def cors_debug_middleware(request: Request, call_next):
        origin = request.headers.get("origin")
        if origin:
            print(f"🔍 Request from origin: {origin}")
            if origin not in allowed_origins and "*" not in allowed_origins:
                print(f"⚠️  Origin {origin} not in allowed origins: {allowed_origins}")
        
        response = await call_next(request)
        return response

@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print(f"🚀 Starting Pravaah API")
    print(f"Environment: {environment}")
    print(f"CORS allowed origins: {allowed_origins}")
    print("=" * 60)
    
    # CRITICAL: Create database tables if they don't exist
    try:
        from app.db.session import engine
        from app.db.base import Base
        print("Creating/verifying database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✓ Database tables created/verified successfully.")
    except Exception as e:
        print(f"✗ CRITICAL: Database table creation failed: {e}")
        print("Application may not function correctly without database tables!")
        # Don't raise - let app start so you can debug via health endpoint
    
    # Initialize SQLite database for offline sync
    try:
        await asyncio.wait_for(init_sqlite_db(), timeout=10.0)
        print("✓ SQLite database initialized successfully.")
    except asyncio.TimeoutError:
        print("✗ SQLite initialization timed out")
    except Exception as e:
        print(f"✗ SQLite initialization failed: {e}")
    
    # Try to connect to RabbitMQ with timeout (optional in production)
    try:
        await asyncio.wait_for(rabbitmq_service.connect(), timeout=5.0)
        print("✓ Successfully connected to RabbitMQ.")
    except asyncio.TimeoutError:
        print("⚠ RabbitMQ connection timed out (running without message queue)")
    except Exception as e:
        print(f"⚠ RabbitMQ connection failed (running without message queue): {e}")
    
    # Start connectivity monitoring (non-blocking)
    try:
        await asyncio.wait_for(connectivity_service.start_monitoring(), timeout=5.0)
        print("✓ Connectivity monitoring started.")
    except asyncio.TimeoutError:
        print("⚠ Connectivity monitoring timed out")
    except Exception as e:
        print(f"⚠ Connectivity monitoring failed: {e}")
    
    # Start sync service (non-blocking)
    try:
        await asyncio.wait_for(sync_service.start_sync_service(), timeout=5.0)
        print("✓ Sync service started.")
    except asyncio.TimeoutError:
        print("⚠ Sync service timed out")
    except Exception as e:
        print(f"⚠ Sync service failed: {e}")
    
    # Note: Safety circle cleanup moved to separate endpoint to avoid startup errors
    # You can manually trigger cleanup via DELETE /api/safety-circles/expired
    
    print("=" * 60)
    print("✅ Pravaah API startup complete!")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Pravaah API...")
    
    # Stop sync services
    try:
        await sync_service.stop_sync_service()
        print("✓ Sync service stopped.")
    except Exception as e:
        print(f"✗ Error stopping sync service: {e}")
    
    try:
        await connectivity_service.stop_monitoring()
        print("✓ Connectivity monitoring stopped.")
    except Exception as e:
        print(f"✗ Error stopping connectivity monitoring: {e}")
    
    # Close RabbitMQ connection
    try:
        await rabbitmq_service.close()
        print("✓ RabbitMQ connection closed.")
    except Exception as e:
        print(f"✗ Error closing RabbitMQ: {e}")
    
    print("Pravaah API shutdown complete.")

app.include_router(api_router, prefix="/api")

# Create uploads directories if they don't exist
os.makedirs("uploads/profile_pictures", exist_ok=True)
os.makedirs("uploads/media", exist_ok=True)

# Mount static files for serving uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/", tags=["Root"])
def read_root():
    return {
        "status": "active", 
        "message": "Welcome to the Pravaah API!",
        "version": "0.1.0",
        "environment": environment,
        "cors_origins": allowed_origins
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint to verify API and database connectivity"""
    health_status = {
        "status": "healthy",
        "api": "running",
        "environment": environment,
        "cors_origins": allowed_origins,
    }
    
    # Test database connection
    try:
        from app.db.session import engine
        from sqlalchemy import text
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
        health_status["database"] = "connected"
        
        # Check if tables exist
        try:
            async with engine.begin() as conn:
                result = await conn.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.scalar()
                health_status["users_table"] = "exists"
                health_status["user_count"] = user_count
        except Exception as e:
            health_status["users_table"] = "missing"
            health_status["tables_error"] = str(e)
            
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["database"] = "disconnected"
        health_status["database_error"] = str(e)
    
    # Check RabbitMQ status
    try:
        if rabbitmq_service.is_connected():
            health_status["rabbitmq"] = "connected"
        else:
            health_status["rabbitmq"] = "disconnected"
    except:
        health_status["rabbitmq"] = "unavailable"
    
    # Overall status
    if health_status.get("database") == "disconnected":
        health_status["status"] = "unhealthy"
        health_status["message"] = "Database connection failed"
    elif health_status.get("users_table") == "missing":
        health_status["status"] = "unhealthy"
        health_status["message"] = "Database tables missing - run migrations"
    else:
        health_status["message"] = "All systems operational"
    
    return health_status