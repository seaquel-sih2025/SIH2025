#!/usr/bin/env python3
"""
Test script to create a sample report via the API
"""
import requests
import json

# API endpoints
BASE_URL = "https://pravaah-backend-9w97.onrender.com"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
SUBMIT_URL = f"{BASE_URL}/api/reports/submit"

def test_create_report():
    """Create a test report to verify the system is working"""
    
    # Test credentials (replace with your actual test user)
    login_data = {
        "email": "test@example.com",  # Replace with your test user email
        "password": "testpassword123"  # Replace with your test user password
    }
    
    print("🔐 Attempting to login...")
    
    # Login to get access token
    try:
        login_response = requests.post(LOGIN_URL, json=login_data)
        print(f"Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            access_token = login_result.get("access_token")
            print("✅ Login successful!")
            
            # Create test report
            headers = {
                "Authorization": f"Bearer {access_token}",
                "latitude": "19.0760",  # Mumbai coordinates
                "longitude": "72.8777",
                "Content-Type": "application/json"
            }
            
            report_data = {
                "user_hazard_type": "flood",
                "user_description": "Test flood report - water level rising near coastal area"
            }
            
            print("📝 Creating test report...")
            report_response = requests.post(SUBMIT_URL, headers=headers, json=report_data)
            print(f"Report creation status: {report_response.status_code}")
            
            if report_response.status_code in [200, 202]:
                result = report_response.json()
                print("✅ Test report created successfully!")
                print(f"Report ID: {result.get('report_id')}")
                
                # Test the recent reports endpoint
                print("\n📊 Checking recent reports...")
                recent_reports_response = requests.get(f"{BASE_URL}/api/reports/recent?limit=5")
                if recent_reports_response.status_code == 200:
                    recent_data = recent_reports_response.json()
                    print(f"Recent reports count: {recent_data.get('count', 0)}")
                    if recent_data.get('items'):
                        print("✅ Reports are now showing in the API!")
                    else:
                        print("⚠️  No reports returned yet - might need to wait for processing")
                else:
                    print(f"❌ Error fetching recent reports: {recent_reports_response.status_code}")
            else:
                print(f"❌ Failed to create report: {report_response.text}")
        else:
            print(f"❌ Login failed: {login_response.text}")
            print("\n💡 You may need to:")
            print("1. Register a new user account first")
            print("2. Update the credentials in this script")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_create_report()