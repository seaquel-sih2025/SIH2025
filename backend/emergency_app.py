#!/usr/bin/env python3
"""
Ultra minimal FastAPI for Render free tier - EMERGENCY memory mode
"""

import os
import gc

# Extreme memory optimization
gc.set_threshold(50, 2, 2)

# Minimal FastAPI app
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Pravaah API - Emergency Mode")

@app.get("/")
async def root():
    return {"message": "Pravaah API - Emergency minimal mode", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "ok", "mode": "emergency"}

@app.get("/api/v1/health")
async def api_health():
    return {"status": "ok", "api": "minimal"}

if __name__ == "__main__":
    import uvicorn
    
    # Ultra minimal uvicorn config
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "10000")),
        log_level="critical",
        access_log=False,
        workers=1
    )