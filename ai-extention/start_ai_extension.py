#!/usr/bin/env python3
"""
Startup script for AI Extension
Runs both the API server and can optionally run the main pipeline
"""

import sys
import argparse
import subprocess
import threading
import time
import os

def run_api_server():
    """Run the API server in a separate thread"""
    print("🚀 Starting AI Extension API Server...")
    try:
        from api_server import app
        app.run(host='0.0.0.0', port=8001, debug=False)
    except Exception as e:
        print(f"❌ Error starting API server: {e}")

def run_main_pipeline():
    """Run the main pipeline once"""
    print("🤖 Running AI Extension Pipeline...")
    try:
        from main import run_pipeline
        output = run_pipeline(limit=20)
        print("✅ Pipeline completed successfully")
        return output
    except Exception as e:
        print(f"❌ Error running pipeline: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="AI Extension Startup Script")
    parser.add_argument("--mode", choices=["api", "pipeline", "both"], default="api",
                       help="Mode to run: api (API server only), pipeline (run once), both (API + pipeline)")
    parser.add_argument("--hazard-type", default="storm", help="Hazard type for pipeline mode")
    parser.add_argument("--location", default="Mumbai", help="Location for pipeline mode")
    parser.add_argument("--limit", type=int, default=20, help="Number of tweets to process")
    
    args = parser.parse_args()
    
    print("🤖 AI Extension Starting...")
    print(f"📋 Mode: {args.mode}")
    
    if args.mode == "api":
        print("🌐 Starting API server only...")
        run_api_server()
        
    elif args.mode == "pipeline":
        print("🔄 Running pipeline once...")
        from main import run_pipeline_with_params
        output = run_pipeline_with_params(
            hazard_type=args.hazard_type,
            location=args.location,
            limit=args.limit
        )
        print("✅ Pipeline completed")
        
    elif args.mode == "both":
        print("🌐 Starting API server and running pipeline...")
        
        # Start API server in background thread
        api_thread = threading.Thread(target=run_api_server, daemon=True)
        api_thread.start()
        
        # Wait a moment for API server to start
        time.sleep(2)
        
        # Run pipeline
        from main import run_pipeline_with_params
        output = run_pipeline_with_params(
            hazard_type=args.hazard_type,
            location=args.location,
            limit=args.limit
        )
        
        print("✅ Pipeline completed, API server running in background")
        print("🌐 API server available at http://localhost:8001")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")

if __name__ == "__main__":
    main()
