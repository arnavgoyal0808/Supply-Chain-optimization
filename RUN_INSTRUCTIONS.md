# 🚀 How to Run the Supply Chain RL Project

## Method 1: Automated Setup (Easiest)

```bash
# 1. Navigate to project directory
cd /q/bin/supply-chain-rl

# 2. Run the automated test (creates demo model + starts everything)
./test_system.sh

# 3. Open dashboard in browser
open http://localhost:3000
```

## Method 2: Manual Step-by-Step

### Step 1: Create Demo Model
```bash
cd edge_agent
python3 create_demo_model.py
cd ..
```

### Step 2: Start All Services
```bash
docker-compose up --build -d
```

### Step 3: Verify Services
```bash
docker-compose ps
```

### Step 4: Access Dashboard
Open your browser to: **http://localhost:3000**

## Method 3: Individual Service Testing

### Start MQTT Broker Only
```bash
docker-compose up mosquitto -d
```

### Start IoT Simulator Only
```bash
docker-compose up iot-simulator -d
```

### Start Edge Agent Only
```bash
docker-compose up edge-agent -d
```

### Start Dashboard Only
```bash
docker-compose up dashboard -d
```

## What You Should See

### 1. Dashboard (http://localhost:3000)
- Interactive map of Los Angeles
- 3 moving truck markers
- Real-time action log showing RL decisions
- Status panel showing connection info

### 2. Truck Data (MQTT Messages)
```bash
# Monitor truck messages
docker exec -it mqtt-broker mosquitto_sub -h localhost -t "trucks/+/data"
```

### 3. RL Actions (API)
```bash
# Check RL agent decisions
curl http://localhost:8080/api/actions
```

## Troubleshooting

### Docker Issues
```bash
# Check Docker status
docker --version
docker-compose --version

# Restart Docker service (Linux)
sudo systemctl restart docker

# View container logs
docker-compose logs -f
```

### Port Conflicts
```bash
# Check what's using ports
lsof -i :3000  # Dashboard
lsof -i :8080  # Edge Agent
lsof -i :1883  # MQTT Broker
```

### Services Not Starting
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# Check individual service logs
docker-compose logs mosquitto
docker-compose logs iot-simulator
docker-compose logs edge-agent
docker-compose logs dashboard
```

### No Truck Data
```bash
# Restart IoT simulator
docker-compose restart iot-simulator

# Check MQTT broker
docker exec -it mqtt-broker mosquitto_pub -h localhost -t test -m "hello"
```

## Advanced Usage

### Train Custom RL Model
1. Open `rl_trainer/Supply_Chain_RL_Training.ipynb` in Google Colab
2. Run all cells to train PPO agent
3. Download the `.tflite` model
4. Replace `edge_agent/models/supply_chain_model.tflite`
5. Restart edge agent: `docker-compose restart edge-agent`

### Monitor System Performance
```bash
# View all logs in real-time
docker-compose logs -f

# Check resource usage
docker stats

# View MQTT messages
docker exec -it mqtt-broker mosquitto_sub -h localhost -t "#"
```

### Stop the System
```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Remove all containers and images
docker-compose down --rmi all
```

## Expected Behavior

1. **3 trucks** moving around Los Angeles map
2. **Real-time updates** every 2 seconds
3. **RL actions** appearing in the action log (Hold/Produce/Ship)
4. **Status indicators** showing green for connected services
5. **Smooth animations** on the map

## Success Indicators

✅ Dashboard loads at http://localhost:3000  
✅ Map shows Los Angeles with 3 moving trucks  
✅ Action log shows RL decisions  
✅ Status panel shows "Connected" for MQTT  
✅ No error messages in docker-compose logs  

## Next Steps

Once running successfully:
1. **Explore the Dashboard**: Click on truck markers, watch actions
2. **Train Better Model**: Use the Google Colab notebook
3. **Customize**: Add more trucks, modify RL environment
4. **Scale**: Deploy to cloud for production use
