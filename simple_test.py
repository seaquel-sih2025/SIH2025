import json

# Simple test payload for citizen registration
test_payload = {
    "email": "test_citizen@example.com",
    "full_name": "Test Citizen",
    "phone": "1234567890", 
    "password": "testpassword123",
    "role": "citizen"
}

print("Test registration payload:")
print(json.dumps(test_payload, indent=2))

# Test official registration payload
test_official = {
    "email": "test_official@example.com",
    "full_name": "Test Official",
    "phone": "1234567891",
    "password": "testpassword123", 
    "role": "official"
}

print("\nTest official registration payload:")
print(json.dumps(test_official, indent=2))

# Test analyst registration payload
test_analyst = {
    "email": "test_analyst@example.com",
    "full_name": "Test Analyst", 
    "phone": "1234567892",
    "password": "testpassword123",
    "role": "analyst"
}

print("\nTest analyst registration payload:")
print(json.dumps(test_analyst, indent=2))

print("\nTo test these, use:")
print("curl -X POST \"http://127.0.0.1:8000/api/auth/register\" \\")
print("     -H \"Content-Type: application/json\" \\")
print("     -d '" + json.dumps(test_payload) + "'")