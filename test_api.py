#!/usr/bin/env python3
"""
Quick API test script to verify backend is working correctly
Run this to diagnose network issues
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        data = response.json()
        print(f"✅ Health endpoint: {response.status_code} - {data}")
        return data.get('status') == 'healthy'
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False

def test_registration():
    """Test user registration"""
    try:
        test_user = {
            "email": "test@example.com",
            "full_name": "Test User",
            "phone": "+1234567890",
            "password": "testpassword123",
            "role": "citizen"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=test_user)
        
        if response.status_code == 201:
            print(f"✅ Registration successful: {response.status_code}")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print(f"✅ Registration endpoint working (user already exists)")
            return True
        else:
            print(f"⚠️  Registration response: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        return False

def test_login():
    """Test user login"""
    try:
        login_data = {
            "username": "test@example.com",
            "password": "testpassword123"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/auth/login", 
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "access_token" in data:
                print(f"✅ Login successful: Got access token")
                return True
            else:
                print(f"⚠️  Login response missing token: {data}")
                return False
        else:
            print(f"⚠️  Login response: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def main():
    print("🔍 Testing Pravaah API endpoints...\n")
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("User Registration", test_registration),
        ("User Login", test_login)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    elif passed >= 2:
        print("⚠️  Some tests failed, but basic connectivity is working.")
        print("   Check the specific error messages above.")
    else:
        print("❌ Most tests failed. Backend may not be running.")
        print("   Try: uvicorn app.main:app --reload")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
