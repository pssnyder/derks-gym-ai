#!/bin/bash
# Derk's Gym AI Web Dashboard Setup and Launch Script

echo "🤖 Derk's Gym AI Web Dashboard Setup"
echo "======================================"

# Check if we're in the correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the main project directory"
    exit 1
fi

# Install Flask for the web dashboard
echo "📦 Installing Flask for web dashboard..."
venv/Scripts/pip.exe install flask==2.3.3 jinja2==3.1.2 werkzeug==2.3.7

if [ $? -eq 0 ]; then
    echo "✅ Flask installed successfully!"
else
    echo "❌ Failed to install Flask"
    exit 1
fi

# Check if the web dashboard files exist
if [ ! -f "web_dashboard/app.py" ]; then
    echo "❌ Error: Web dashboard files not found"
    exit 1
fi

echo ""
echo "🎯 Web Dashboard Features:"
echo "  📊 Derkling Profiles & Teams"
echo "  🤝 Fighter Bonds & Compatibility"
echo "  🔥 Project Number Eleven (Special)"
echo "  📈 Battle Metrics & Performance"
echo ""

echo "🚀 Starting web dashboard..."
echo "   Dashboard URL: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

# Change to web dashboard directory and start Flask
cd web_dashboard
FLASK_APP=app.py FLASK_DEBUG=true ../venv/Scripts/python.exe -m flask run --host=0.0.0.0 --port=5000
