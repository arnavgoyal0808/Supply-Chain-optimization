# Setup Instructions

## Prerequisites

- Docker and Docker Compose installed
- Git
- Google Colab account (for RL training)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd supply-chain-rl
   ```

2. **Start the system:**
   ```bash
   ./start.sh
   ```

3. **Access the dashboard:**
   - Open http://localhost:3000 in your browser
   - You should see 3 trucks moving on the map
   - Actions will appear in the log as the RL agent makes decisions

## Training the RL Model

### Option 1: Use Demo Model (Immediate Testing)
```bash
cd edge_agent
python create_demo_model.py
docker-compose restart edge-agent
```

### Option 2: Train with PPO in Google Colab
1. Open `rl_trainer/Supply_Chain_RL_Training.ipynb` in Google Colab
2. Run all cells to train the PPO agent
3. Download the generated `supply_chain_model.tflite`
4. Place it in `edge_agent/models/`
5. Restart the edge agent: `docker-compose restart edge-agent`

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   IoT Trucks    │───▶│  MQTT Broker    │───▶│   Edge Agent    │
│  (Simulator)    │    │  (Mosquitto)    │    │  (TFLite RL)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   Dashboard     │
                                               │  (React.js)     │
                                               └─────────────────┘
```

## Components

### 1. RL Trainer (`/rl_trainer/`)
- **Environment**: Custom Gymnasium environment simulating supply chain
- **Agent**: PPO from stable-baselines3
- **Export**: TensorFlow Lite model for edge deployment

### 2. IoT Simulator (`/iot_simulator/`)
- Simulates 3 trucks publishing GPS and inventory data
- MQTT topics: `trucks/{truck_id}/data`
- Data format: `{"truck_id": 1, "lat": 34.05, "lng": -118.24, "inventory": 50}`

### 3. Edge Agent (`/edge_agent/`)
- Subscribes to MQTT truck data
- Runs TensorFlow Lite inference
- Makes RL-based decisions (Hold/Produce/Ship)
- Provides REST API for dashboard

### 4. Dashboard (`/dashboard/`)
- Real-time map showing truck locations (Leaflet.js)
- Action log table showing RL decisions
- MQTT WebSocket connection for live updates

## Troubleshooting

### Services not starting
```bash
docker-compose logs -f
```

### MQTT connection issues
```bash
# Test MQTT broker
docker exec -it mqtt-broker mosquitto_pub -h localhost -t test -m "hello"
```

### Dashboard not loading
- Check if port 3000 is available
- Verify MQTT WebSocket on port 9001

### No RL actions appearing
- Ensure TensorFlow Lite model exists in `edge_agent/models/`
- Check edge agent logs: `docker-compose logs edge-agent`

## Development

### Adding new actions
1. Modify `rl_trainer/supply_chain_env.py` action space
2. Update `edge_agent/edge_inference.py` action mapping
3. Retrain the model

### Customizing truck behavior
- Edit `iot_simulator/truck_simulator.py`
- Adjust movement patterns, inventory changes, etc.

### Dashboard modifications
- React components in `dashboard/src/components/`
- Styling in `dashboard/src/App.css`

## Zero-Cost Deployment

This system uses only free tools:
- ✅ Google Colab (free GPU training)
- ✅ Docker (local containers)
- ✅ Mosquitto MQTT (open source)
- ✅ React.js (open source)
- ✅ TensorFlow Lite (open source)
- ✅ GitHub (free hosting)

Total cost: **$0** 💰
