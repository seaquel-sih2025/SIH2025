@echo off
echo Starting Pravaah Backend...
cd /d "C:\Users\athar\OneDrive\Desktop\SIH2025\backend"

:restart
echo.
echo ================================
echo Starting backend server...
echo ================================
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

echo.
echo Backend stopped. Restarting in 3 seconds...
timeout /t 3 /nobreak > nul
goto restart