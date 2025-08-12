# System Architecture

## Overview

Supply Chain RL system with real-time IoT simulation, MQTT communication, edge AI inference, and live dashboard.

## Components

### 1. IoT Layer
- **3 Truck Simulators**: GPS + inventory data
- **MQTT Publisher**: JSON messages every 2 seconds
- **Data Format**: `{"truck_id": 1, "lat": 34.05, "lng": -118.24, "inventory": 50}`

### 2. Communication Layer  
- **Mosquitto MQTT Broker**: Message routing
- **Ports**: 1883 (MQTT), 9001 (WebSocket)
- **Topics**: `trucks/{truck_id}/data`

### 3. Edge AI Layer
- **TensorFlow Lite Model**: PPO agent inference
- **Decision Engine**: Hold/Produce/Ship actions
- **REST API**: Flask server on port 8080
- **Inference Time**: <50ms

### 4. Dashboard Layer
- **React.js**: Interactive UI
- **Leaflet.js**: Real-time map
- **WebSocket**: Live MQTT connection
- **Port**: 3000

## Data Flow

```
Trucks → MQTT → Edge Agent → Dashboard
  2s      <10ms     <50ms      <200ms
```

## Deployment

**Docker Compose** orchestrates all services with automatic service discovery and health checks.

## Performance

- **Latency**: End-to-end <300ms
- **Throughput**: 1.5 msg/sec, 90 decisions/min
- **Resources**: ~2GB RAM, ~1GB storage
