#!/usr/bin/env python3
"""
API server for AI Extension to receive data from backend worker
"""

import json
import asyncio
from flask import Flask, request, jsonify
from main import run_pipeline_with_params

app = Flask(__name__)

@app.route('/process_report', methods=['POST'])
def process_report():
    """
    API endpoint to receive report data from backend worker
    """
    try:
        data = request.get_json()
        
        # Extract required fields
        report_id = data.get('report_id')
        hazard_type = data.get('hazard_type')
        location = data.get('location')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not all([report_id, hazard_type, location]):
            return jsonify({
                'error': 'Missing required fields: report_id, hazard_type, location'
            }), 400
        
        print(f"🤖 AI Extension received report {report_id}: {hazard_type} in {location}")
        
        # Run the AI pipeline with the provided parameters
        try:
            # Run the pipeline asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            result = run_pipeline_with_params(
                hazard_type=hazard_type,
                location=location,
                latitude=latitude,
                longitude=longitude,
                limit=20
            )
            
            print(f"✅ AI Extension processed report {report_id} successfully")
            
            return jsonify({
                'status': 'success',
                'report_id': report_id,
                'processed_tweets': len(result) if result else 0,
                'message': f'Processed {hazard_type} reports for {location}'
            })
            
        except Exception as e:
            print(f"❌ Error processing report {report_id}: {e}")
            return jsonify({
                'status': 'error',
                'report_id': report_id,
                'error': str(e)
            }), 500
            
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Extension API'
    })

@app.route('/status', methods=['GET'])
def status():
    """Status endpoint with service information"""
    return jsonify({
        'status': 'running',
        'service': 'AI Extension API',
        'version': '1.0.0',
        'endpoints': [
            'POST /process_report - Process report data from backend',
            'GET /health - Health check',
            'GET /status - Service status'
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting AI Extension API Server...")
    print("📡 Listening for reports from backend worker...")
    app.run(host='0.0.0.0', port=8001, debug=True)
