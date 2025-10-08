#!/usr/bin/env python3
"""
ABSOLUTE MINIMAL HTTP server for Render free tier - Under 100MB memory
Uses only Python standard library - NO external dependencies
"""

import os
import gc
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# Force minimal memory
gc.set_threshold(10, 2, 2)

class MinimalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "message": "Pravaah API - Absolute minimal mode", 
                    "status": "ok",
                    "memory": "under 100MB"
                }
                self.wfile.write(json.dumps(response).encode())
                
            elif self.path == '/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "ok", "mode": "absolute-minimal"}
                self.wfile.write(json.dumps(response).encode())
                
            elif self.path == '/api/v1/health':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "ok", "api": "minimal", "dependencies": "zero"}
                self.wfile.write(json.dumps(response).encode())
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Not found", "mode": "minimal"}
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": str(e), "mode": "minimal"}
            self.wfile.write(json.dumps(response).encode())
    
    def log_message(self, format, *args):
        """Disable request logging to save memory"""
        pass

def run_server():
    """Run the minimal HTTP server"""
    port = int(os.getenv('PORT', '10000'))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, MinimalHandler)
    
    print(f"✅ Absolute minimal server running on port {port}")
    print(f"✅ Memory usage: Minimal (Python stdlib only)")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    # Ultra aggressive cleanup
    gc.collect()
    run_server()