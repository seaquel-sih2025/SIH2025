#!/usr/bin/env python3
"""
Minimal FastAPI app for Render free tier - Memory optimized startup
Disables heavy features to reduce memory usage under 512MB
"""

import os
import sys
import gc

# Force minimal memory usage from startup
gc.set_threshold(100, 5, 5)  # Aggressive garbage collection

# Set environment to minimal mode
os.environ["MINIMAL_MODE"] = "true"
os.environ["DISABLE_WORKERS"] = "true"
os.environ["DISABLE_SQLITE"] = "true"

def minimal_startup():
    """Start FastAPI with minimal memory footprint"""
    try:
        # Import only what we need
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from app.api.api import api_router
        
        # Create minimal app
        app = FastAPI(
            title="Pravaah API - Minimal",
            description="Memory-optimized API for Render free tier",
            version="0.1.0"
        )
        
        # Minimal CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Simplified for memory
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Include API routes
        app.include_router(api_router, prefix="/api/v1")
        
        @app.get("/health")
        async def health_check():
            return {"status": "ok", "mode": "minimal"}
        
        print("✅ Minimal FastAPI app created")
        return app
        
    except Exception as e:
        print(f"❌ Failed to create minimal app: {e}")
        sys.exit(1)

# Create app instance
app = minimal_startup()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "minimal_app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000")),
        log_level="error"
    )