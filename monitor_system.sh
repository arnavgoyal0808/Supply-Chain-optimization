#!/bin/bash

echo "📊 Supply Chain RL System Monitor"
echo "================================="
echo "Press Ctrl+C to stop monitoring"
echo ""

# Function to get timestamp
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Function to check service health
check_service_health() {
    local service=$1
    local port=$2
    local endpoint=$3
    
    if curl -s --connect-timeout 3 "$endpoint" >/dev/null 2>&1; then
        echo "✅ $(timestamp) - $service (port $port) is healthy"
        return 0
    else
        echo "❌ $(timestamp) - $service (port $port) is not responding"
        return 1
    fi
}

# Function to check container status
check_containers() {
    echo "🐳 Container Status at $(timestamp):"
    if command -v docker-compose >/dev/null 2>&1; then
        docker-compose ps 2>/dev/null | grep -E "(mosquitto|iot-simulator|edge-agent|dashboard)" | while read line; do
            if echo "$line" | grep -q "Up"; then
                service=$(echo "$line" | awk '{print $1}')
                echo "   ✅ $service is running"
            else
                service=$(echo "$line" | awk '{print $1}')
                echo "   ❌ $service has issues"
            fi
        done
    else
        echo "   ⚠️  Docker Compose not available"
    fi
}

# Function to check data flow
check_data_flow() {
    echo "📡 Data Flow Check at $(timestamp):"
    
    # Check truck count
    if truck_data=$(curl -s --connect-timeout 3 "http://localhost:8080/api/trucks" 2>/dev/null); then
        truck_count=$(echo "$truck_data" | grep -o '"truck_id"' | wc -l)
        echo "   📍 Active trucks: $truck_count"
    else
        echo "   ❌ Cannot fetch truck data"
    fi
    
    # Check action count
    if action_data=$(curl -s --connect-timeout 3 "http://localhost:8080/api/actions" 2>/dev/null); then
        action_count=$(echo "$action_data" | grep -o '"action"' | wc -l)
        echo "   🤖 Recent actions: $action_count"
    else
        echo "   ❌ Cannot fetch action data"
    fi
}

# Function to show resource usage
show_resource_usage() {
    echo "💻 Resource Usage at $(timestamp):"
    if command -v docker >/dev/null 2>&1; then
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null | head -5
    else
        echo "   ⚠️  Docker not available for resource monitoring"
    fi
}

# Main monitoring loop
monitor_interval=30  # seconds

while true; do
    clear
    echo "📊 Supply Chain RL System Monitor - $(timestamp)"
    echo "=================================================="
    echo ""
    
    # Check container status
    check_containers
    echo ""
    
    # Check service endpoints
    echo "🌐 Service Health:"
    check_service_health "Dashboard" "3000" "http://localhost:3000"
    check_service_health "Edge Agent" "8080" "http://localhost:8080/api/health"
    check_service_health "MQTT Broker" "1883" "http://localhost:1883"
    echo ""
    
    # Check data flow
    check_data_flow
    echo ""
    
    # Show resource usage
    show_resource_usage
    echo ""
    
    # Show recent logs (last 5 lines from each service)
    echo "📋 Recent Activity:"
    if command -v docker-compose >/dev/null 2>&1; then
        echo "   Edge Agent (last 3 lines):"
        docker-compose logs --tail=3 edge-agent 2>/dev/null | sed 's/^/      /'
        echo ""
        echo "   IoT Simulator (last 3 lines):"
        docker-compose logs --tail=3 iot-simulator 2>/dev/null | sed 's/^/      /'
    else
        echo "   ⚠️  Cannot access logs - Docker Compose not available"
    fi
    
    echo ""
    echo "🔄 Next update in $monitor_interval seconds... (Ctrl+C to stop)"
    
    # Wait for next update
    sleep $monitor_interval
done
