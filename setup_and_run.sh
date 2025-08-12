#!/bin/bash

echo "🚀 Supply Chain RL - Setup and Run Script"
echo "=========================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Docker installation
echo "🔍 Checking Docker installation..."
if command_exists docker; then
    echo "✅ Docker is installed: $(docker --version)"
else
    echo "❌ Docker is not installed!"
    echo "📥 Please install Docker first:"
    echo "   - Ubuntu/Debian: sudo apt install docker.io"
    echo "   - macOS: brew install docker"
    echo "   - Windows: Download Docker Desktop"
    exit 1
fi

# Check Docker Compose
echo "🔍 Checking Docker Compose..."
if command_exists docker-compose; then
    echo "✅ Docker Compose is installed: $(docker-compose --version)"
elif docker compose version >/dev/null 2>&1; then
    echo "✅ Docker Compose (plugin) is available"
    alias docker-compose='docker compose'
else
    echo "❌ Docker Compose is not installed!"
    echo "📥 Please install Docker Compose"
    exit 1
fi

# Check if Docker daemon is running
echo "🔍 Checking Docker daemon..."
if docker info >/dev/null 2>&1; then
    echo "✅ Docker daemon is running"
else
    echo "❌ Docker daemon is not running!"
    echo "🔧 Please start Docker:"
    echo "   - Linux: sudo systemctl start docker"
    echo "   - macOS/Windows: Start Docker Desktop"
    exit 1
fi

# Check Python for demo model creation
echo "🔍 Checking Python..."
if command_exists python3; then
    echo "✅ Python3 is available: $(python3 --version)"
elif command_exists python; then
    echo "✅ Python is available: $(python --version)"
    alias python3='python'
else
    echo "⚠️  Python not found, but continuing (Docker will handle it)"
fi

echo ""
echo "🎯 All prerequisites met! Starting the system..."
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p mosquitto/data mosquitto/log edge_agent/models

# Create demo model
echo "🤖 Creating demo TensorFlow Lite model..."
cd edge_agent
if command_exists python3; then
    python3 create_demo_model.py
elif command_exists python; then
    python create_demo_model.py
else
    echo "⚠️  Skipping demo model creation (will use random actions)"
fi
cd ..

# Start the system
echo "🚀 Starting all services with Docker Compose..."
docker-compose up --build -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 15

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 System should be running!"
echo ""
echo "🌐 Access Points:"
echo "   📊 Dashboard: http://localhost:3000"
echo "   🤖 Edge Agent: http://localhost:8080/api/health"
echo "   📡 MQTT Broker: localhost:1883"
echo ""
echo "🔍 Quick Tests:"
echo "   curl http://localhost:8080/api/health"
echo "   curl http://localhost:3000"
echo ""
echo "📋 Useful Commands:"
echo "   docker-compose logs -f          # View all logs"
echo "   docker-compose ps               # Check status"
echo "   docker-compose down             # Stop system"
echo "   docker-compose restart edge-agent  # Restart component"
echo ""
echo "🎯 Next: Open http://localhost:3000 in your browser!"
