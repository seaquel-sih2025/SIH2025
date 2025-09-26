@echo off
echo Starting Pravaah Development Environment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

echo ✅ Python and Node.js are available
echo.

REM Start backend
echo 🚀 Starting Backend Server...
cd /d "%~dp0backend"

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  Backend .env file not found
    echo Creating .env from .env.example...
    copy ".env.example" ".env"
    echo.
    echo ❗ IMPORTANT: Please edit backend/.env with your database credentials
    echo Then run this script again
    pause
    exit /b 1
)

REM Install Python dependencies if needed
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Start backend in background
echo Starting FastAPI server on http://localhost:8000
start "Pravaah Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Test backend connection
echo Testing backend connection...
curl -s http://localhost:8000/ >nul
if errorlevel 1 (
    echo ❌ Backend failed to start
    echo Check the backend terminal for errors
    pause
    exit /b 1
)

echo ✅ Backend is running
echo.

REM Start frontend
echo 🎨 Starting Frontend...
cd /d "%~dp0frontend\web_app"

REM Check if .env exists
if not exist ".env" (
    echo Creating frontend .env file...
    echo VITE_API_BASE_URL="http://127.0.0.1:8000" > .env
)

REM Install Node dependencies if needed
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

REM Start frontend
echo Starting Vite dev server on http://localhost:5173
start "Pravaah Frontend" cmd /k "npm run dev"

echo.
echo 🎉 Development environment started!
echo.
echo 📋 Services:
echo   - Backend API: http://localhost:8000
echo   - Frontend:    http://localhost:5173
echo   - API Docs:    http://localhost:8000/docs
echo.
echo 🔧 Troubleshooting:
echo   - Run test_api.py to check backend connectivity
echo   - Check browser console for frontend errors
echo   - Ensure PostgreSQL is running for database features
echo.
pause
