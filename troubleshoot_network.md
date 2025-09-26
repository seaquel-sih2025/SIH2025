# Network Error Troubleshooting Guide

## Quick Diagnosis Steps

### 1. Check if Backend is Running
```bash
# Navigate to backend directory
cd backend

# Check if server is running
curl http://localhost:8000/
# Should return: {"status":"active","message":"Welcome to the Pravaah API!"}

# Check health endpoint
curl http://localhost:8000/health
# Should return database and API status
```

### 2. Check Frontend Configuration
```bash
# Navigate to frontend directory
cd frontend/web_app

# Check if .env file exists and has correct API URL
cat .env
# Should contain: VITE_API_BASE_URL="http://127.0.0.1:8000"
```

### 3. Common Network Error Fixes

#### Fix 1: Backend Not Running
```bash
cd backend
# Install dependencies if needed
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Fix 2: Database Connection Issues
```bash
cd backend
# Run database setup
python create_tables.py fresh
# Or just migrations
python create_tables.py migrate
```

#### Fix 3: Environment Variables Missing
Create `backend/.env` file with:
```env
DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/pravaah_db"
SYNC_DATABASE_URL="postgresql://postgres:password@localhost/pravaah_db"
SECRET_KEY="your-secret-key-here"
RABBITMQ_URL="amqp://guest:guest@localhost/"
BACKEND_URL="http://localhost:8000"
GEMINI_API_KEY="your-gemini-key"
WEATHERAPI_KEY="your-weather-key"
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_S3_BUCKET_NAME=""
AWS_S3_REGION=""
FIREBASE_PROJECT_ID=""
FIREBASE_AUTH_URI=""
FIREBASE_TOKEN_URI=""
```

#### Fix 4: CORS Issues
The backend already has CORS configured to allow all origins. If still having issues, try:
```bash
# Start backend with specific host
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### Fix 5: Port Conflicts
```bash
# Check if port 8000 is in use
netstat -an | findstr :8000

# If in use, kill the process or use different port
uvicorn app.main:app --reload --port 8001
# Then update frontend .env: VITE_API_BASE_URL="http://127.0.0.1:8001"
```

### 4. Test API Endpoints
```bash
# Test registration endpoint
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "phone": "+1234567890",
    "password": "testpassword",
    "role": "citizen"
  }'

# Test login endpoint
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword"
```

### 5. Browser Developer Tools
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try to register/login
4. Check for failed requests
5. Look at request/response details

### 6. Frontend Debugging
Add this to your browser console to test API connection:
```javascript
// Test API connection
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log('API Health:', data))
  .catch(error => console.error('API Error:', error));
```

## Error Messages and Solutions

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Network Error" | Backend not running | Start backend server |
| "ECONNREFUSED" | Wrong port or host | Check backend URL in .env |
| "CORS error" | Cross-origin issue | Verify CORS configuration |
| "500 Internal Server Error" | Database/backend issue | Check backend logs and database |
| "404 Not Found" | Wrong API endpoint | Verify API routes |

## Complete Reset Process
If all else fails, try this complete reset:

```bash
# 1. Stop all servers
# Ctrl+C in all terminal windows

# 2. Backend reset
cd backend
python create_tables.py fresh
uvicorn app.main:app --reload

# 3. Frontend reset (in new terminal)
cd frontend/web_app
npm install
npm run dev

# 4. Test in browser
# Go to http://localhost:5173
# Try to register a new account
```
