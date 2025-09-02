@echo off
REM Derk's Gym AI Web Dashboard Setup and Launch Script for Windows

echo 🤖 Derk's Gym AI Web Dashboard Setup
echo ======================================

REM Check if we're in the correct directory
if not exist "requirements.txt" (
    echo ❌ Error: Please run this script from the main project directory
    exit /b 1
)

REM Install Flask for the web dashboard
echo 📦 Installing Flask for web dashboard...
venv\Scripts\pip.exe install flask==2.3.3 jinja2==3.1.2 werkzeug==2.3.7

if %errorlevel% neq 0 (
    echo ❌ Failed to install Flask
    exit /b 1
)

echo ✅ Flask installed successfully!

REM Check if the web dashboard files exist
if not exist "web_dashboard\app.py" (
    echo ❌ Error: Web dashboard files not found
    exit /b 1
)

echo.
echo 🎯 Web Dashboard Features:
echo   📊 Derkling Profiles ^& Teams
echo   🤝 Fighter Bonds ^& Compatibility
echo   🔥 Project Number Eleven (Special)
echo   📈 Battle Metrics ^& Performance
echo.

echo 🚀 Starting web dashboard...
echo    Dashboard URL: http://localhost:5000
echo    Press Ctrl+C to stop the server
echo.

REM Change to web dashboard directory and start Flask
cd web_dashboard
set FLASK_APP=app.py
set FLASK_DEBUG=true
..\venv\Scripts\python.exe -m flask run --host=0.0.0.0 --port=5000
