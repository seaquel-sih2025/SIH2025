import requests
import json

def test_registration():
    """Test user registration for different roles"""
    base_url = "http://127.0.0.1:8001"
    
    test_users = [
        {
            "email": "official@pravaah.in",
            "full_name": "Official User",
            "phone": "1234567890",
            "password": "securePassword123",
            "role": "official"
        },
        {
            "email": "analyst@pravaah.in", 
            "full_name": "Analyst User",
            "phone": "1234567891",
            "password": "securePassword123",
            "role": "analyst"
        },
        {
            "email": "authority@pravaah.in",
            "full_name": "Authority User", 
            "phone": "1234567892",
            "password": "securePassword123",
            "role": "authority"
        }
    ]
    
    for user_data in test_users:
        print(f"\nTesting registration for {user_data['role']}: {user_data['email']}")
        
        try:
            response = requests.post(
                f"{base_url}/api/auth/register",
                json=user_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 201:
                print(f"✅ SUCCESS: {user_data['role']} registration successful")
            elif response.status_code == 400 and "already exists" in response.text:
                print(f"⚠️  INFO: User {user_data['email']} already exists")
            else:
                print(f"❌ FAILED: {user_data['role']} registration failed")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ CONNECTION ERROR: {e}")
            
    print("\n" + "="*50)
    print("Registration test completed!")

if __name__ == "__main__":
    test_registration()