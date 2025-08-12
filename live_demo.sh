#!/bin/bash

echo "🎬 Starting Live Supply Chain RL Demo"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_live() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to show animated header
show_header() {
    clear
    print_live $CYAN "╔═══════════════════════════════════════════════════════════════════════════════╗"
    print_live $CYAN "║                    🎬 LIVE SUPPLY CHAIN RL SYSTEM 🎬                         ║"
    print_live $CYAN "╠═══════════════════════════════════════════════════════════════════════════════╣"
    print_live $GREEN "║  🚛 IoT Trucks → 📡 MQTT Broker → 🤖 Edge Agent → 📊 Dashboard              ║"
    print_live $CYAN "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
}

# Function to show live truck data
show_truck_data() {
    print_live $YELLOW "🚛 LIVE TRUCK DATA:"
    print_live $YELLOW "==================="
    
    if command -v curl >/dev/null 2>&1; then
        truck_data=$(curl -s --connect-timeout 3 "http://localhost:8080/api/trucks" 2>/dev/null)
        if [ $? -eq 0 ] && [ -n "$truck_data" ]; then
            echo "$truck_data" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for truck_id, truck_info in data.items():
        lat = truck_info.get('lat', 'N/A')
        lng = truck_info.get('lng', 'N/A')
        inv = truck_info.get('inventory', 'N/A')
        print(f'  🚛 Truck {truck_id}: GPS({lat:.4f}, {lng:.4f}) | 📦 Inventory: {inv} units')
except:
    print('  ⚠️  Truck data not available')
" 2>/dev/null || print_live $RED "  ❌ Cannot parse truck data"
        else
            print_live $RED "  ❌ Cannot fetch truck data from API"
        fi
    else
        print_live $RED "  ❌ curl not available"
    fi
    echo ""
}

# Function to show live actions
show_live_actions() {
    print_live $BLUE "🤖 LIVE RL ACTIONS:"
    print_live $BLUE "==================="
    
    if command -v curl >/dev/null 2>&1; then
        action_data=$(curl -s --connect-timeout 3 "http://localhost:8080/api/actions" 2>/dev/null)
        if [ $? -eq 0 ] && [ -n "$action_data" ]; then
            echo "$action_data" | python3 -c "
import sys, json
from datetime import datetime
try:
    data = json.load(sys.stdin)
    if isinstance(data, list) and len(data) > 0:
        # Show last 5 actions
        for action in data[-5:]:
            truck_id = action.get('truck_id', 'N/A')
            action_name = action.get('action', 'N/A')
            inventory = action.get('inventory', 'N/A')
            timestamp = action.get('timestamp', 0)
            try:
                time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
            except:
                time_str = 'N/A'
            
            action_emoji = {'Hold': '🔄', 'Produce': '💫', 'Ship': '⚡'}.get(action_name, '🎯')
            print(f'  {time_str} | Truck {truck_id} | {action_emoji} {action_name} | 📦 {inventory}')
    else:
        print('  ⚠️  No actions recorded yet')
except Exception as e:
    print(f'  ⚠️  Cannot parse action data: {e}')
" 2>/dev/null || print_live $RED "  ❌ Cannot parse action data"
        else
            print_live $RED "  ❌ Cannot fetch action data from API"
        fi
    else
        print_live $RED "  ❌ curl not available"
    fi
    echo ""
}

# Function to show system metrics
show_system_metrics() {
    print_live $PURPLE "📊 SYSTEM METRICS:"
    print_live $PURPLE "=================="
    
    # Container status
    if command -v docker-compose >/dev/null 2>&1; then
        running_containers=$(docker-compose ps 2>/dev/null | grep "Up" | wc -l)
        total_containers=$(docker-compose ps 2>/dev/null | grep -v "Name\|----" | grep -v "^$" | wc -l)
        print_live $GREEN "  🐳 Containers: $running_containers/$total_containers running"
    else
        print_live $RED "  ❌ Docker Compose not available"
    fi
    
    # Port checks
    ports=("3000:Dashboard" "8080:Edge Agent" "1883:MQTT Broker")
    for port_info in "${ports[@]}"; do
        port="${port_info%%:*}"
        service="${port_info##*:}"
        
        if nc -z localhost "$port" 2>/dev/null; then
            print_live $GREEN "  ✅ $service (port $port): Active"
        else
            print_live $RED "  ❌ $service (port $port): Inactive"
        fi
    done
    
    # API health check
    if command -v curl >/dev/null 2>&1; then
        health_response=$(curl -s --connect-timeout 3 "http://localhost:8080/api/health" 2>/dev/null)
        if echo "$health_response" | grep -q "healthy"; then
            print_live $GREEN "  ✅ Edge Agent API: Healthy"
        else
            print_live $RED "  ❌ Edge Agent API: Unhealthy"
        fi
    fi
    
    echo ""
}

# Function to show live MQTT messages
show_mqtt_activity() {
    print_live $CYAN "📡 MQTT ACTIVITY (Last 5 seconds):"
    print_live $CYAN "=================================="
    
    if command -v docker >/dev/null 2>&1; then
        # Try to capture MQTT messages for 5 seconds
        timeout 5 docker exec mqtt-broker mosquitto_sub -h localhost -t "trucks/+/data" 2>/dev/null | while read -r line; do
            if [ -n "$line" ]; then
                echo "$line" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    truck_id = data.get('truck_id', 'N/A')
    lat = data.get('lat', 'N/A')
    lng = data.get('lng', 'N/A')
    inv = data.get('inventory', 'N/A')
    print(f'  📨 Truck {truck_id}: GPS({lat:.4f}, {lng:.4f}) Inv:{inv}')
except:
    print(f'  📨 Raw: {sys.stdin.read().strip()[:50]}...')
" 2>/dev/null || echo "  📨 $line"
            fi
        done &
        
        # Wait a bit for messages
        sleep 2
        
        # Kill the background process
        jobs -p | xargs -r kill 2>/dev/null
    else
        print_live $RED "  ❌ Docker not available for MQTT monitoring"
    fi
    
    echo ""
}

# Function to show access information
show_access_info() {
    print_live $GREEN "🌐 ACCESS POINTS:"
    print_live $GREEN "================"
    print_live $GREEN "  📊 Dashboard:    http://localhost:3000"
    print_live $GREEN "  🤖 Edge Agent:   http://localhost:8080/api/health"
    print_live $GREEN "  📡 MQTT Broker:  localhost:1883"
    print_live $GREEN "  🎬 Live Demo:    file://$(pwd)/docs/live_architecture.html"
    echo ""
}

# Main demo loop
main_demo() {
    echo "🎬 Starting live demo... Press Ctrl+C to stop"
    echo ""
    
    # Open the HTML visualization if possible
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "docs/live_architecture.html" 2>/dev/null &
    elif command -v open >/dev/null 2>&1; then
        open "docs/live_architecture.html" 2>/dev/null &
    fi
    
    while true; do
        show_header
        show_truck_data
        show_live_actions
        show_system_metrics
        show_mqtt_activity
        show_access_info
        
        print_live $YELLOW "🔄 Refreshing in 10 seconds... (Ctrl+C to stop)"
        sleep 10
    done
}

# Check if system is running
check_system() {
    if ! nc -z localhost 8080 2>/dev/null; then
        print_live $RED "❌ System not running! Please start with:"
        print_live $YELLOW "   ./setup_and_run.sh"
        exit 1
    fi
}

# Trap Ctrl+C
trap 'echo -e "\n\n🛑 Live demo stopped. Thanks for watching!"; exit 0' INT

# Start the demo
check_system
main_demo
