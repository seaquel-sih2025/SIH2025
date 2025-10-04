import requests
import json
import time

def test_registration():
    """Test registration endpoint directly"""
    
    # Test with a unique email to avoid conflicts
    test_email = f"test_{int(time.time())}@example.com"
    
    url = "http://127.0.0.1:8000/api/auth/register"
    
    payload = {
        "email": test_email,
        "password": "testpass123",
        "full_name": "Test User",
        "phone": "1234567890",
        "role": "citizen"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Testing registration for: {test_email}")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        # Set a reasonable timeout
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        else:
            print(f"❌ Registration failed with status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out!")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the backend running?")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing registration endpoint...")
    success = test_registration()
    
    if success:
        print("\n🎉 Registration test passed!")
    else:
        print("\n💥 Registration test failed!")