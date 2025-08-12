#!/bin/bash

echo "🧪 Testing Supply Chain RL System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    exit 1
fi

echo "✅ Docker is running"

# Create demo model first
echo "📱 Creating demo TensorFlow Lite model..."
cd edge_agent
python3 create_demo_model.py
cd ..

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Test MQTT broker
echo "📡 Testing MQTT broker..."
if docker exec mqtt-broker mosquitto_pub -h localhost -t test -m "test" > /dev/null 2>&1; then
    echo "✅ MQTT broker is working"
else
    echo "❌ MQTT broker test failed"
fi

# Test edge agent API
echo "🤖 Testing edge agent API..."
if curl -s http://localhost:8080/api/health > /dev/null; then
    echo "✅ Edge agent API is responding"
else
    echo "❌ Edge agent API test failed"
fi

# Test dashboard
echo "📊 Testing dashboard..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Dashboard is accessible"
else
    echo "❌ Dashboard test failed"
fi

echo ""
echo "🎉 System test completed!"
echo ""
echo "📋 Service Status:"
docker-compose ps

echo ""
echo "🌐 Access Points:"
echo "  Dashboard: http://localhost:3000"
echo "  Edge Agent: http://localhost:8080/api/health"
echo "  MQTT Broker: localhost:1883"
echo ""
echo "📝 Next Steps:"
echo "  1. Open http://localhost:3000 to see the dashboard"
echo "  2. Watch trucks move and RL actions in real-time"
echo "  3. Train a better model in Google Colab using the notebook"
echo ""
echo "🛑 To stop: docker-compose down"
