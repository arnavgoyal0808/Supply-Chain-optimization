#!/bin/bash

echo "🚀 Starting Supply Chain RL Optimization Engine..."

# Create necessary directories
mkdir -p mosquitto/data mosquitto/log
mkdir -p edge_agent/models

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

echo "📦 Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 10

echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Supply Chain RL Engine is starting up!"
echo ""
echo "📊 Dashboard: http://localhost:3000"
echo "🤖 Edge Agent API: http://localhost:8080"
echo "📡 MQTT Broker: localhost:1883"
echo ""
echo "📝 To train the RL model, run in Google Colab:"
echo "   !git clone <your-repo>"
echo "   !cd supply-chain-rl/rl_trainer && python train.py --timesteps 10000"
echo ""
echo "🛑 To stop: docker-compose down"
echo "📋 To view logs: docker-compose logs -f"
