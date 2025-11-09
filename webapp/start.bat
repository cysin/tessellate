@echo off
REM Startup script for Tessellate Web Application (Windows)

echo ==========================================
echo 🎯 Tessellate Web Application Startup
echo ==========================================

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Start the application
echo.
echo ==========================================
echo 🚀 Starting Tessellate Web Server
echo ==========================================
echo.
echo 📍 Web Interface: http://localhost:5000
echo 📍 API Health: http://localhost:5000/api/health
echo 📍 Example Data: http://localhost:5000/api/example
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
