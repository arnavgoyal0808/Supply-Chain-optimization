# 🏥 Service Monitoring & Health Check Guide

## 🎯 Quick Service Check Commands

### **Option 1: Comprehensive Check (Recommended)**
```bash
./check_all_services.sh
```
**What it does:**
- ✅ Checks all prerequisites (Docker, files, etc.)
- ✅ Validates all containers are running
- ✅ Tests network connectivity on all ports
- ✅ Verifies API endpoints are responding
- ✅ Tests MQTT broker functionality
- ✅ Confirms data flow between components
- ✅ Analyzes logs for errors
- ✅ Provides detailed troubleshooting advice

### **Option 2: Detailed Health Check**
```bash
./health_check.sh
```
**What it does:**
- 🔍 Comprehensive system health analysis
- 📊 Service status with colored output
- 🌐 Port connectivity testing
- 📡 MQTT functionality verification
- 💡 Specific troubleshooting recommendations

### **Option 3: Python Service Validator**
```bash
python3 validate_services.py
```
**What it does:**
- 🐍 Python-based comprehensive validation
- 📋 Structured service testing
- 🔗 API endpoint functionality testing
- 📊 Data flow verification
- 📈 Success rate calculation

### **Option 4: Continuous Monitoring**
```bash
./monitor_system.sh
```
**What it does:**
- 📊 Real-time system monitoring (updates every 30 seconds)
- 🐳 Container status tracking
- 💻 Resource usage monitoring
- 📡 Live data flow checking
- 📋 Recent log activity display

## 🚀 Quick Start Verification

After starting your system, run this sequence:

```bash
# 1. Start the system
./setup_and_run.sh

# 2. Wait 30 seconds for services to initialize
sleep 30

# 3. Run comprehensive check
./check_all_services.sh

# 4. If all good, open dashboard
open http://localhost:3000
```

## 📊 What Each Service Should Show

### **✅ Healthy System Indicators**

#### MQTT Broker (Mosquitto)
```bash
docker-compose logs mosquitto
# Should show: "mosquitto version X.X.X starting"
# Should show: "Opening ipv4 listen socket on port 1883"
```

#### IoT Simulator
```bash
docker-compose logs iot-simulator
# Should show: "Connected to MQTT broker"
# Should show: "Truck 1: {'truck_id': 1, 'lat': 34.xxxx, ...}"
# Should show: Regular truck data updates every 2 seconds
```

#### Edge Agent
```bash
docker-compose logs edge-agent
# Should show: "TensorFlow Lite model loaded successfully"
# Should show: "Connected to MQTT broker"
# Should show: "Truck X: Hold/Produce/Ship (Inventory: XX, Distance: XX.XXkm)"
```

#### Dashboard
```bash
docker-compose logs dashboard
# Should show: "serve: Running on port 3000"
# Should show: No error messages
```

### **🌐 API Endpoint Tests**

```bash
# Health check - should return {"status": "healthy"}
curl http://localhost:8080/api/health

# Truck data - should return array of truck objects
curl http://localhost:8080/api/trucks

# Actions - should return array of RL decisions
curl http://localhost:8080/api/actions

# Dashboard - should return HTML content
curl http://localhost:3000
```

### **📡 MQTT Message Testing**

```bash
# Subscribe to all truck messages
docker exec -it mqtt-broker mosquitto_sub -h localhost -t "trucks/+/data"

# Should see messages like:
# {"truck_id": 1, "lat": 34.0522, "lng": -118.2437, "inventory": 45, "timestamp": 1699123456}
```

## 🚨 Common Issues & Solutions

### **Issue: Containers not starting**
```bash
# Check Docker daemon
sudo systemctl status docker

# Check port conflicts
lsof -i :3000 :8080 :1883 :9001

# Rebuild containers
docker-compose down && docker-compose up --build -d
```

### **Issue: No truck data**
```bash
# Restart IoT simulator
docker-compose restart iot-simulator

# Check MQTT broker
docker exec -it mqtt-broker mosquitto_pub -h localhost -t test -m "hello"
```

### **Issue: RL agent not making decisions**
```bash
# Check if model exists
ls -la edge_agent/models/

# Create demo model if missing
cd edge_agent && python3 create_demo_model.py && cd ..

# Restart edge agent
docker-compose restart edge-agent
```

### **Issue: Dashboard not loading**
```bash
# Check if port 3000 is free
lsof -i :3000

# Check dashboard logs
docker-compose logs dashboard

# Rebuild dashboard
docker-compose up --build dashboard -d
```

## 📈 Performance Monitoring

### **Resource Usage**
```bash
# Check container resource usage
docker stats

# Check system resources
htop  # or top
```

### **Data Flow Rates**
```bash
# Count messages per minute
docker exec -it mqtt-broker mosquitto_sub -h localhost -t "trucks/+/data" | pv -l -i 10

# Monitor API response times
time curl http://localhost:8080/api/trucks
```

## 🎯 Success Criteria

Your system is **fully operational** when:

✅ **All containers show "Up" status**  
✅ **Dashboard loads at http://localhost:3000**  
✅ **Map shows 3 moving trucks**  
✅ **Action log shows RL decisions**  
✅ **Status panel shows "Connected"**  
✅ **No errors in container logs**  
✅ **API endpoints return valid JSON**  
✅ **MQTT messages flow continuously**  

## 🔧 Advanced Debugging

### **Deep Log Analysis**
```bash
# Search for specific errors
docker-compose logs | grep -i "error\|exception\|failed"

# Monitor logs in real-time
docker-compose logs -f --tail=100

# Export logs for analysis
docker-compose logs > system_logs.txt
```

### **Network Debugging**
```bash
# Check internal Docker network
docker network ls
docker network inspect supply-chain-rl_default

# Test inter-container connectivity
docker exec edge-agent ping mosquitto
```

### **Database/State Debugging**
```bash
# Check MQTT broker state
docker exec -it mqtt-broker mosquitto_sub -h localhost -t '$SYS/#'

# Check edge agent internal state
curl http://localhost:8080/api/health | jq
```

---

**Use these tools to ensure your Supply Chain RL system is running perfectly! 🚀**
