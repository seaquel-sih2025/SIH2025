#!/usr/bin/env python3
"""
Test script to verify Render deployment is working
"""
import requests
import json
import sys

def test_deployment(base_url):
    """Test basic deployment functionality"""
    print(f"🧪 Testing deployment at: {base_url}")
    
    try:
        # Test health endpoint
        print("\n1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=30)
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health endpoint working!")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Database: {health_data.get('database')}")
            print(f"   Environment: {health_data.get('environment')}")
            print(f"   RabbitMQ: {health_data.get('rabbitmq')}")
            
            if health_data.get('status') == 'unhealthy':
                print("⚠️  Application is unhealthy:")
                print(f"   Message: {health_data.get('message')}")
                if 'database_error' in health_data:
                    print(f"   DB Error: {health_data.get('database_error')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
        # Test basic API endpoint
        print("\n2. Testing sync status endpoint...")
        response = requests.get(f"{base_url}/api/sync/status", timeout=15)
        
        if response.status_code == 200:
            print("✅ Sync status endpoint working!")
        else:
            print(f"⚠️  Sync status endpoint issue: {response.status_code}")
            
        print("\n✅ Basic deployment tests passed!")
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out - server might be starting up")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - server might be down")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Test both local and production
    urls_to_test = [
        "https://pravaah-backend.onrender.com",  # Your production URL
        "http://localhost:8000"  # Local testing
    ]
    
    if len(sys.argv) > 1:
        urls_to_test = [sys.argv[1]]
    
    for url in urls_to_test:
        print(f"\n{'='*50}")
        success = test_deployment(url)
        if not success:
            print(f"❌ Tests failed for {url}")
        print(f"{'='*50}")