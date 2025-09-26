#!/bin/bash

echo "Starting Pravaah Development Environment..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js 16+ and try again"
    exit 1
fi

echo "✅ Python and Node.js are available"
echo

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Start backend
echo "🚀 Starting Backend Server..."
cd "$SCRIPT_DIR/backend"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Backend .env file not found"
    echo "Creating .env from .env.example..."
    cp ".env.example" ".env"
    echo
    echo "❗ IMPORTANT: Please edit backend/.env with your database credentials"
    echo "Then run this script again"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Start backend in background
echo "Starting FastAPI server on http://localhost:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Test backend connection
echo "Testing backend connection..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
    echo "Check the backend process for errors"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo

# Start frontend
echo "🎨 Starting Frontend..."
cd "$SCRIPT_DIR/frontend/web_app"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    echo 'VITE_API_BASE_URL="http://127.0.0.1:8000"' > .env
fi

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start frontend
echo "Starting Vite dev server on http://localhost:5173"
npm run dev &
FRONTEND_PID=$!

echo
echo "🎉 Development environment started!"
echo
echo "📋 Services:"
echo "  - Backend API: http://localhost:8000"
echo "  - Frontend:    http://localhost:5173"
echo "  - API Docs:    http://localhost:8000/docs"
echo
echo "🔧 Troubleshooting:"
echo "  - Run 'python test_api.py' to check backend connectivity"
echo "  - Check browser console for frontend errors"
echo "  - Ensure PostgreSQL is running for database features"
echo
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
