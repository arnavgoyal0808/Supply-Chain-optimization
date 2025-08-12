#!/bin/bash

echo "🔍 Supply Chain RL - Complete Service Check"
echo "==========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0

# Function to run a check
run_check() {
    local description="$1"
    local command="$2"
    local expected_output="$3"
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    echo -n "Checking $description... "
    
    if eval "$command" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        return 1
    fi
}

# Function to run a check with output
run_check_with_output() {
    local description="$1"
    local command="$2"
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    echo "Checking $description..."
    
    if output=$(eval "$command" 2>&1); then
        echo -e "${GREEN}✅ PASS${NC}"
        echo "$output" | sed 's/^/   /'
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "$output" | sed 's/^/   /' | head -3
        return 1
    fi
}

echo "🔧 PREREQUISITE CHECKS"
echo "----------------------"

run_check "Docker installation" "docker --version"
run_check "Docker daemon running" "docker info"
run_check "Docker Compose available" "docker-compose --version || docker compose version"

echo ""
echo "📁 FILE STRUCTURE CHECKS"
echo "------------------------"

run_check "Docker Compose config" "test -f docker-compose.yml"
run_check "Edge Agent script" "test -f edge_agent/edge_inference.py"
run_check "IoT Simulator script" "test -f iot_simulator/truck_simulator.py"
run_check "Dashboard app" "test -f dashboard/src/App.js"
run_check "MQTT config" "test -f mosquitto/config/mosquitto.conf"

echo ""
echo "🐳 CONTAINER STATUS CHECKS"
echo "--------------------------"

if docker info >/dev/null 2>&1; then
    run_check_with_output "Container status" "docker-compose ps"
    
    # Individual container checks
    run_check "MQTT Broker container" "docker-compose ps | grep mosquitto | grep -q Up"
    run_check "IoT Simulator container" "docker-compose ps | grep iot-simulator | grep -q Up"
    run_check "Edge Agent container" "docker-compose ps | grep edge-agent | grep -q Up"
    run_check "Dashboard container" "docker-compose ps | grep dashboard | grep -q Up"
else
    echo -e "${RED}❌ Cannot check containers - Docker not available${NC}"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 5))
fi

echo ""
echo "🌐 NETWORK CONNECTIVITY CHECKS"
echo "------------------------------"

run_check "Dashboard port (3000)" "nc -z localhost 3000"
run_check "Edge Agent port (8080)" "nc -z localhost 8080"
run_check "MQTT Broker port (1883)" "nc -z localhost 1883"
run_check "MQTT WebSocket port (9001)" "nc -z localhost 9001"

echo ""
echo "🔗 API ENDPOINT CHECKS"
echo "----------------------"

run_check "Dashboard HTTP response" "curl -s --connect-timeout 5 http://localhost:3000"
run_check "Edge Agent health endpoint" "curl -s --connect-timeout 5 http://localhost:8080/api/health | grep -q healthy"
run_check "Truck data endpoint" "curl -s --connect-timeout 5 http://localhost:8080/api/trucks"
run_check "Actions endpoint" "curl -s --connect-timeout 5 http://localhost:8080/api/actions"

echo ""
echo "📡 MQTT FUNCTIONALITY CHECKS"
echo "----------------------------"

if docker info >/dev/null 2>&1 && docker-compose ps | grep -q mosquitto; then
    run_check "MQTT publish test" "docker exec mqtt-broker mosquitto_pub -h localhost -t test/check -m 'test'"
    run_check "MQTT subscribe test" "timeout 3 docker exec mqtt-broker mosquitto_sub -h localhost -t test/check -C 1"
else
    echo -e "${YELLOW}⚠️  Skipping MQTT tests - broker not available${NC}"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 2))
fi

echo ""
echo "📊 DATA FLOW CHECKS"
echo "-------------------"

# Check if truck data is flowing
if truck_response=$(curl -s --connect-timeout 5 "http://localhost:8080/api/trucks" 2>/dev/null); then
    truck_count=$(echo "$truck_response" | grep -o '"truck_id"' | wc -l)
    if [ "$truck_count" -gt 0 ]; then
        echo -e "Truck data flow... ${GREEN}✅ PASS${NC} ($truck_count trucks active)"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "Truck data flow... ${RED}❌ FAIL${NC} (no trucks detected)"
    fi
else
    echo -e "Truck data flow... ${RED}❌ FAIL${NC} (cannot connect to API)"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# Check if RL actions are being generated
if action_response=$(curl -s --connect-timeout 5 "http://localhost:8080/api/actions" 2>/dev/null); then
    action_count=$(echo "$action_response" | grep -o '"action"' | wc -l)
    if [ "$action_count" -gt 0 ]; then
        echo -e "RL action generation... ${GREEN}✅ PASS${NC} ($action_count actions recorded)"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "RL action generation... ${YELLOW}⚠️  PENDING${NC} (no actions yet - may need time)"
    fi
else
    echo -e "RL action generation... ${RED}❌ FAIL${NC} (cannot connect to API)"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

echo ""
echo "📋 LOG ANALYSIS"
echo "---------------"

if docker info >/dev/null 2>&1; then
    # Check for errors in logs
    services=("mosquitto" "iot-simulator" "edge-agent" "dashboard")
    
    for service in "${services[@]}"; do
        if docker-compose ps | grep -q "$service"; then
            error_count=$(docker-compose logs --tail=20 "$service" 2>/dev/null | grep -i "error\|exception\|failed" | wc -l)
            if [ "$error_count" -eq 0 ]; then
                echo -e "$service logs... ${GREEN}✅ CLEAN${NC} (no errors)"
                PASSED_CHECKS=$((PASSED_CHECKS + 1))
            else
                echo -e "$service logs... ${YELLOW}⚠️  $error_count ERRORS${NC}"
            fi
        else
            echo -e "$service logs... ${RED}❌ CONTAINER NOT FOUND${NC}"
        fi
        TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    done
else
    echo -e "${RED}❌ Cannot analyze logs - Docker not available${NC}"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 4))
fi

echo ""
echo "=" * 50
echo "🎯 FINAL RESULTS"
echo "=" * 50

percentage=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

if [ "$percentage" -ge 90 ]; then
    echo -e "${GREEN}🎉 EXCELLENT: $PASSED_CHECKS/$TOTAL_CHECKS checks passed ($percentage%)${NC}"
    echo ""
    echo "✨ System is fully operational!"
    echo ""
    echo "🌐 Access your dashboard: http://localhost:3000"
    echo "🤖 API health check: http://localhost:8080/api/health"
    
elif [ "$percentage" -ge 70 ]; then
    echo -e "${YELLOW}⚠️  GOOD: $PASSED_CHECKS/$TOTAL_CHECKS checks passed ($percentage%)${NC}"
    echo ""
    echo "System is mostly working but may have minor issues."
    
elif [ "$percentage" -ge 50 ]; then
    echo -e "${YELLOW}⚠️  PARTIAL: $PASSED_CHECKS/$TOTAL_CHECKS checks passed ($percentage%)${NC}"
    echo ""
    echo "System has some functionality but needs attention."
    
else
    echo -e "${RED}❌ CRITICAL: $PASSED_CHECKS/$TOTAL_CHECKS checks passed ($percentage%)${NC}"
    echo ""
    echo "System has major issues and may not be functional."
fi

echo ""
echo "🔧 TROUBLESHOOTING COMMANDS:"
echo "   docker-compose logs -f              # View all logs"
echo "   docker-compose ps                   # Check container status"
echo "   docker-compose restart edge-agent   # Restart specific service"
echo "   ./monitor_system.sh                 # Continuous monitoring"
echo "   ./health_check.sh                   # Detailed health check"

echo ""
echo "📊 MONITORING COMMANDS:"
echo "   curl http://localhost:8080/api/health    # Edge agent health"
echo "   curl http://localhost:8080/api/trucks    # Current truck data"
echo "   curl http://localhost:8080/api/actions   # Recent RL actions"

exit $((TOTAL_CHECKS - PASSED_CHECKS))
