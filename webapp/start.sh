#!/bin/bash
# Startup script for Tessellate Web Application (Linux/Mac)

echo "=========================================="
echo "🎯 Tessellate Web Application Startup"
echo "=========================================="

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Start the application
echo ""
echo "=========================================="
echo "🚀 Starting Tessellate Web Server"
echo "=========================================="
echo ""
echo "📍 Web Interface: http://localhost:5000"
echo "📍 API Health: http://localhost:5000/api/health"
echo "📍 Example Data: http://localhost:5000/api/example"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
