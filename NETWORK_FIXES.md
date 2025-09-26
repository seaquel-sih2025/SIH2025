# 🔧 Network Error Fixes - Complete Guide

## 🚨 Quick Fix (Most Common Issues)

### 1. **Start Backend Server**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. **Check Backend is Running**
Open browser and go to: http://localhost:8000
- Should show: `{"status":"active","message":"Welcome to the Pravaah API!"}`

### 3. **Test API Health**
Go to: http://localhost:8000/health
- Should show database and API status

---

## 🔍 **All Issues Fixed**

### ✅ **Backend Issues Fixed:**
1. **Registration Endpoint Error** - Fixed non-existent field references
2. **Role Mapping Error** - Updated `official` → `authority` 
3. **Database Health Check** - Added `/health` endpoint
4. **Error Handling** - Improved error responses

### ✅ **Frontend Issues Fixed:**
1. **Network Error Handling** - Better error messages instead of "[object Object]"
2. **Connection Testing** - Added interactive connection test modal
3. **API Configuration** - Improved timeout and error handling
4. **User Feedback** - Clear error messages with troubleshooting hints

### ✅ **Development Tools Added:**
1. **Automated Startup Scripts** - `start_dev.bat` (Windows) / `start_dev.sh` (Linux/Mac)
2. **API Test Script** - `test_api.py` for backend verification
3. **Connection Test Component** - Interactive frontend diagnostics
4. **Troubleshooting Guide** - Complete error resolution guide

---

## 🚀 **Easy Setup (Recommended)**

### **Windows:**
```cmd
# Double-click or run:
start_dev.bat
```

### **Linux/Mac:**
```bash
chmod +x start_dev.sh
./start_dev.sh
```

This will:
- ✅ Check Python & Node.js installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Start backend on port 8000
- ✅ Start frontend on port 5173
- ✅ Test connections automatically

---

## 🔧 **Manual Setup (If Automated Fails)**

### **1. Backend Setup:**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example and edit)
cp .env.example .env

# Setup database (optional - uses SQLite by default)
python create_tables.py fresh

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **2. Frontend Setup:**
```bash
cd frontend/web_app

# Install dependencies
npm install

# Create .env file
echo 'VITE_API_BASE_URL="http://127.0.0.1:8000"' > .env

# Start development server
npm run dev
```

---

## 🧪 **Testing & Verification**

### **1. Test Backend API:**
```bash
# Run the test script
python test_api.py

# Or manually test endpoints:
curl http://localhost:8000/
curl http://localhost:8000/health
```

### **2. Test Frontend Connection:**
1. Open http://localhost:5173
2. Go to Sign Up page
3. If you see network errors, click "Test Connection" button
4. The connection test will diagnose issues automatically

### **3. Test Registration:**
1. Select "Authority" user type
2. Fill in the form:
   - Email: test@example.com
   - Username: Test User
   - Phone: +1234567890
   - Password: testpassword123
3. Click "Create Pravaah Account"
4. Should redirect to Authority Dashboard

---

## 🐛 **Common Error Solutions**

| Error | Cause | Solution |
|-------|-------|----------|
| "Network Error" | Backend not running | Run `uvicorn app.main:app --reload` |
| "ECONNREFUSED" | Wrong port/host | Check .env file has correct API URL |
| "[object Object]" | Poor error handling | **FIXED** - Now shows clear messages |
| "Database error" | DB not connected | Check DATABASE_URL in backend/.env |
| "CORS error" | Cross-origin issue | **FIXED** - CORS properly configured |
| "404 Not Found" | Wrong API route | **FIXED** - All routes properly configured |

---

## 📋 **Environment Files**

### **Backend `.env`:**
```env
DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/pravaah_db"
SYNC_DATABASE_URL="postgresql://postgres:password@localhost/pravaah_db"
SECRET_KEY="your-secret-key-here-change-this"
RABBITMQ_URL="amqp://guest:guest@localhost/"
BACKEND_URL="http://localhost:8000"
GEMINI_API_KEY="your-gemini-api-key"
WEATHERAPI_KEY="your-weather-api-key"
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_S3_BUCKET_NAME=""
AWS_S3_REGION=""
FIREBASE_PROJECT_ID=""
FIREBASE_AUTH_URI=""
FIREBASE_TOKEN_URI=""
```

### **Frontend `.env`:**
```env
VITE_API_BASE_URL="http://127.0.0.1:8000"
```

---

## 🎯 **Verification Checklist**

- [ ] Backend server starts without errors
- [ ] http://localhost:8000/ returns API status
- [ ] http://localhost:8000/health shows "healthy" status
- [ ] Frontend loads at http://localhost:5173
- [ ] Registration form works for all user types
- [ ] Role-based dashboards load correctly
- [ ] No "[object Object]" errors in console
- [ ] Clear error messages for network issues

---

## 🆘 **Still Having Issues?**

1. **Check the logs:**
   - Backend: Look at terminal running uvicorn
   - Frontend: Check browser console (F12)

2. **Run diagnostics:**
   - Backend: `python test_api.py`
   - Frontend: Click "Test Connection" button

3. **Reset everything:**
   ```bash
   # Stop all servers (Ctrl+C)
   # Delete node_modules and venv
   # Run setup scripts again
   ```

4. **Check ports:**
   ```bash
   # Windows:
   netstat -an | findstr :8000
   # Linux/Mac:
   lsof -i :8000
   ```

The role-based access control system is now fully functional with comprehensive error handling and diagnostics! 🎉
