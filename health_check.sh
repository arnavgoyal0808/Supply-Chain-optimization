#!/bin/bash

echo "🏥 Supply Chain RL System Health Check"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ "$2" = "OK" ]; then
        echo -e "${GREEN}✅ $1${NC}"
    elif [ "$2" = "WARNING" ]; then
        echo -e "${YELLOW}⚠️  $1${NC}"
    else
        echo -e "${RED}❌ $1${NC}"
    fi
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "🔍 PREREQUISITE CHECKS"
echo "----------------------"

# Check Docker
if command_exists docker; then
    if docker info >/dev/null 2>&1; then
        print_status "Docker is installed and running" "OK"
        DOCKER_VERSION=$(docker --version)
        echo "   Version: $DOCKER_VERSION"
    else
        print_status "Docker is installed but not running" "ERROR"
        echo "   💡 Start Docker: sudo systemctl start docker (Linux) or Docker Desktop (Mac/Windows)"
    fi
else
    print_status "Docker is not installed" "ERROR"
    echo "   💡 Install: sudo apt install docker.io (Ubuntu) or download Docker Desktop"
fi

# Check Docker Compose
if command_exists docker-compose; then
    print_status "Docker Compose is available" "OK"
    COMPOSE_VERSION=$(docker-compose --version)
    echo "   Version: $COMPOSE_VERSION"
elif docker compose version >/dev/null 2>&1; then
    print_status "Docker Compose (plugin) is available" "OK"
else
    print_status "Docker Compose is not available" "ERROR"
fi

# Check Python
if command_exists python3; then
    print_status "Python3 is available" "OK"
    PYTHON_VERSION=$(python3 --version)
    echo "   Version: $PYTHON_VERSION"
elif command_exists python; then
    print_status "Python is available" "OK"
    PYTHON_VERSION=$(python --version)
    echo "   Version: $PYTHON_VERSION"
else
    print_status "Python is not available" "WARNING"
    echo "   💡 Needed for demo model creation"
fi

echo ""
echo "📁 FILE STRUCTURE CHECKS"
echo "------------------------"

# Check critical files
files_to_check=(
    "docker-compose.yml:Docker Compose configuration"
    "edge_agent/edge_inference.py:Edge Agent main script"
    "edge_agent/create_demo_model.py:Demo model creator"
    "iot_simulator/truck_simulator.py:IoT truck simulator"
    "dashboard/src/App.js:Dashboard main component"
    "mosquitto/config/mosquitto.conf:MQTT broker config"
)

for item in "${files_to_check[@]}"; do
    file="${item%%:*}"
    desc="${item##*:}"
    if [ -f "$file" ]; then
        print_status "$desc exists" "OK"
    else
        print_status "$desc missing: $file" "ERROR"
    fi
done

echo ""
echo "🐳 DOCKER SERVICES CHECK"
echo "------------------------"

if command_exists docker && docker info >/dev/null 2>&1; then
    # Check if containers are running
    if docker-compose ps >/dev/null 2>&1; then
        echo "📊 Container Status:"
        docker-compose ps
        
        echo ""
        echo "🔍 Service Health:"
        
        # Check each service
        services=("mosquitto" "iot-simulator" "edge-agent" "dashboard")
        
        for service in "${services[@]}"; do
            if docker-compose ps | grep -q "$service.*Up"; then
                print_status "$service container is running" "OK"
            else
                print_status "$service container is not running" "ERROR"
            fi
        done
        
        echo ""
        echo "🌐 CONNECTIVITY CHECKS"
        echo "----------------------"
        
        # Check ports
        ports=("3000:Dashboard" "8080:Edge Agent API" "1883:MQTT Broker" "9001:MQTT WebSocket")
        
        for port_info in "${ports[@]}"; do
            port="${port_info%%:*}"
            service="${port_info##*:}"
            
            if curl -s --connect-timeout 3 "http://localhost:$port" >/dev/null 2>&1; then
                print_status "$service (port $port) is responding" "OK"
            elif nc -z localhost "$port" 2>/dev/null; then
                print_status "$service (port $port) is listening" "OK"
            else
                print_status "$service (port $port) is not accessible" "ERROR"
            fi
        done
        
        echo ""
        echo "📡 MQTT BROKER TEST"
        echo "------------------"
        
        # Test MQTT broker
        if docker exec mqtt-broker mosquitto_pub -h localhost -t "test/health" -m "health_check" >/dev/null 2>&1; then
            print_status "MQTT broker accepts messages" "OK"
        else
            print_status "MQTT broker test failed" "ERROR"
        fi
        
        echo ""
        echo "🤖 API ENDPOINTS TEST"
        echo "--------------------"
        
        # Test Edge Agent API
        if curl -s "http://localhost:8080/api/health" | grep -q "healthy"; then
            print_status "Edge Agent API is healthy" "OK"
        else
            print_status "Edge Agent API health check failed" "ERROR"
        fi
        
        # Test if trucks data is available
        if curl -s "http://localhost:8080/api/trucks" | grep -q "truck_id"; then
            print_status "Truck data is available" "OK"
        else
            print_status "No truck data available" "WARNING"
            echo "   💡 Trucks might still be starting up"
        fi
        
        # Test if actions are being generated
        if curl -s "http://localhost:8080/api/actions" | grep -q "action"; then
            print_status "RL actions are being generated" "OK"
        else
            print_status "No RL actions detected" "WARNING"
            echo "   💡 Actions appear after trucks start sending data"
        fi
        
        echo ""
        echo "📋 CONTAINER LOGS SUMMARY"
        echo "-------------------------"
        
        # Check for errors in logs
        for service in "${services[@]}"; do
            error_count=$(docker-compose logs --tail=50 "$service" 2>/dev/null | grep -i "error\|exception\|failed" | wc -l)
            if [ "$error_count" -eq 0 ]; then
                print_status "$service: No errors in recent logs" "OK"
            else
                print_status "$service: $error_count errors found in logs" "ERROR"
                echo "   💡 Check with: docker-compose logs $service"
            fi
        done
        
    else
        print_status "No Docker Compose services found" "ERROR"
        echo "   💡 Run: docker-compose up -d"
    fi
else
    print_status "Cannot check Docker services - Docker not available" "ERROR"
fi

echo ""
echo "🎯 SYSTEM RECOMMENDATIONS"
echo "-------------------------"

if command_exists docker && docker info >/dev/null 2>&1; then
    if docker-compose ps | grep -q "Up"; then
        echo -e "${GREEN}🎉 System appears to be running!${NC}"
        echo ""
        echo "📱 Access Points:"
        echo "   🌐 Dashboard: http://localhost:3000"
        echo "   🤖 Edge Agent: http://localhost:8080/api/health"
        echo "   📊 Truck Data: http://localhost:8080/api/trucks"
        echo "   📋 Actions: http://localhost:8080/api/actions"
        echo ""
        echo "🔍 Monitoring Commands:"
        echo "   docker-compose logs -f                    # All logs"
        echo "   docker-compose logs -f edge-agent         # RL decisions"
        echo "   docker-compose logs -f iot-simulator      # Truck data"
        echo "   curl http://localhost:8080/api/health     # Health check"
    else
        echo -e "${YELLOW}⚠️  System needs to be started${NC}"
        echo ""
        echo "🚀 Start Commands:"
        echo "   ./setup_and_run.sh                       # Automated setup"
        echo "   docker-compose up --build -d             # Manual start"
    fi
else
    echo -e "${RED}❌ Docker needs to be installed and started${NC}"
    echo ""
    echo "📥 Installation:"
    echo "   Ubuntu/Debian: sudo apt install docker.io docker-compose"
    echo "   macOS: brew install docker docker-compose"
    echo "   Windows: Download Docker Desktop"
fi

echo ""
echo "🏥 Health check completed!"
echo "=========================="
