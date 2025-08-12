# 🏗️ Supply Chain RL System Architecture

## 🎯 System Overview

The Supply Chain Optimization Engine is a comprehensive system that combines **Reinforcement Learning**, **IoT simulation**, and **Edge Computing** to optimize supply chain operations in real-time.

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SUPPLY CHAIN RL OPTIMIZATION ENGINE                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   IoT LAYER     │    │  COMMUNICATION  │    │   AI/ML LAYER   │             │
│  │                 │    │     LAYER       │    │                 │             │
│  │  📍 Truck 1     │────│                 │────│  🤖 RL Agent    │             │
│  │  📍 Truck 2     │────│   MQTT Broker   │────│  (PPO Model)    │             │
│  │  📍 Truck 3     │────│   (Mosquitto)   │────│  TFLite Edge    │             │
│  │                 │    │                 │    │                 │             │
│  │  GPS + Inventory│    │  Message Queue  │    │  Decision Engine│             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│           │                       │                       │                     │
│           │                       │                       │                     │
│           └───────────────────────┼───────────────────────┘                     │
│                                   │                                             │
│                                   ▼                                             │
│                    ┌─────────────────────────────────┐                         │
│                    │        PRESENTATION LAYER       │                         │
│                    │                                 │                         │
│                    │  📊 Real-time Dashboard         │                         │
│                    │  🗺️  Interactive Map            │                         │
│                    │  📋 Action Log                  │                         │
│                    │  📈 Status Monitoring           │                         │
│                    │                                 │                         │
│                    │  (React.js + Leaflet.js)       │                         │
│                    └─────────────────────────────────┘                         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │────▶│             │────▶│             │────▶│             │
│ IoT Trucks  │     │ MQTT Broker │     │ Edge Agent  │     │ Dashboard   │
│             │◀────│             │◀────│             │◀────│             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│GPS Tracking │     │Message Queue│     │RL Inference │     │Live Updates │
│Inventory    │     │Topic Routing│     │Action Pred. │     │Map Visual   │
│Telemetry    │     │Load Balance │     │Model Serving│     │Action Log   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

## 🧩 Component Architecture

### 1. **IoT Simulation Layer**
```
┌─────────────────────────────────────────────────────────────┐
│                    IoT Simulator                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🚛 Truck 1 (Downtown LA)     🚛 Truck 2 (Pasadena)       │
│  ├─ GPS: 34.0522, -118.2437   ├─ GPS: 34.1478, -118.1445  │
│  ├─ Inventory: 0-100 units    ├─ Inventory: 0-100 units   │
│  ├─ Speed: Random walk        ├─ Speed: Random walk       │
│  └─ Update: Every 2 seconds   └─ Update: Every 2 seconds  │
│                                                             │
│  🚛 Truck 3 (LAX Area)                                     │
│  ├─ GPS: 33.9425, -118.4081                               │
│  ├─ Inventory: 0-100 units                                │
│  ├─ Speed: Random walk                                     │
│  └─ Update: Every 2 seconds                               │
│                                                             │
│  📡 MQTT Publisher                                          │
│  ├─ Topic: trucks/{truck_id}/data                         │
│  ├─ Format: JSON                                           │
│  └─ QoS: 0 (Fire and forget)                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. **Communication Layer**
```
┌─────────────────────────────────────────────────────────────┐
│                   MQTT Broker (Mosquitto)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📨 Message Routing                                         │
│  ├─ Port 1883: MQTT Protocol                              │
│  ├─ Port 9001: WebSocket (Dashboard)                      │
│  ├─ Topics: trucks/+/data                                 │
│  └─ Persistence: Enabled                                   │
│                                                             │
│  🔄 Message Flow                                            │
│  ├─ Publishers: 3 IoT Trucks                              │
│  ├─ Subscribers: Edge Agent, Dashboard                     │
│  ├─ Message Rate: ~6 messages/second                      │
│  └─ Message Size: ~150 bytes each                         │
│                                                             │
│  ⚡ Performance                                             │
│  ├─ Latency: <10ms                                        │
│  ├─ Throughput: 1000+ msg/sec                             │
│  └─ Memory: ~50MB                                          │
└─────────────────────────────────────────────────────────────┘
```

### 3. **AI/ML Edge Computing Layer**
```
┌─────────────────────────────────────────────────────────────┐
│                    Edge Inference Agent                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🧠 RL Model (TensorFlow Lite)                             │
│  ├─ Algorithm: PPO (Proximal Policy Optimization)         │
│  ├─ State Space: [inventory, demand, capacity, distance]   │
│  ├─ Action Space: [Hold, Produce, Ship]                   │
│  ├─ Model Size: ~2MB                                       │
│  └─ Inference Time: <50ms                                  │
│                                                             │
│  📊 Decision Engine                                         │
│  ├─ Input: Real-time truck data                           │
│  ├─ Processing: Feature extraction                         │
│  ├─ Output: Optimized actions                             │
│  └─ Logging: All decisions tracked                        │
│                                                             │
│  🌐 REST API Server                                         │
│  ├─ Port 8080: HTTP API                                   │
│  ├─ Endpoints: /health, /trucks, /actions                 │
│  ├─ Format: JSON responses                                 │
│  └─ CORS: Enabled for dashboard                           │
│                                                             │
│  📡 MQTT Subscriber                                         │
│  ├─ Topics: trucks/+/data                                 │
│  ├─ Processing: Real-time inference                       │
│  └─ Actions: Immediate decision making                     │
└─────────────────────────────────────────────────────────────┘
```

### 4. **Presentation Layer**
```
┌─────────────────────────────────────────────────────────────┐
│                   React.js Dashboard                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🗺️ Interactive Map (Leaflet.js)                           │
│  ├─ Base Layer: OpenStreetMap                             │
│  ├─ Markers: 3 Truck locations + Warehouse                │
│  ├─ Updates: Real-time via WebSocket                      │
│  ├─ Popups: Truck details on click                        │
│  └─ Zoom: Los Angeles area focus                          │
│                                                             │
│  📋 Action Log Component                                    │
│  ├─ Display: Recent RL decisions                          │
│  ├─ Columns: Time, Truck, Action, Inventory, Distance     │
│  ├─ Updates: Every 5 seconds via API                      │
│  ├─ Sorting: Most recent first                            │
│  └─ Color Coding: Hold/Produce/Ship actions               │
│                                                             │
│  📊 Status Panel                                            │
│  ├─ MQTT Connection: Connected/Disconnected               │
│  ├─ Active Trucks: Live count                             │
│  ├─ RL Actions: Total decisions made                      │
│  └─ System Health: Overall status                         │
│                                                             │
│  🔌 Connectivity                                            │
│  ├─ MQTT: WebSocket on port 9001                          │
│  ├─ API: HTTP requests to port 8080                       │
│  ├─ Updates: Real-time data streaming                     │
│  └─ Fallback: Polling if WebSocket fails                  │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Message Flow Sequence

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Truck   │    │  MQTT   │    │  Edge   │    │Dashboard│
│Simulator│    │ Broker  │    │ Agent   │    │         │
└────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
     │              │              │              │
     │ 1. GPS Data  │              │              │
     ├─────────────▶│              │              │
     │              │ 2. Route Msg │              │
     │              ├─────────────▶│              │
     │              │              │ 3. RL Infer │
     │              │              ├──────────────┤
     │              │              │ 4. Decision  │
     │              │              │◀─────────────┤
     │              │              │ 5. Log Action│
     │              │              ├─────────────▶│
     │              │ 6. WebSocket │              │
     │              ├─────────────────────────────▶│
     │              │              │ 7. API Call  │
     │              │              │◀─────────────┤
     │              │              │ 8. Response  │
     │              │              ├─────────────▶│
     │              │              │              │
```

## 🏭 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Stack                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🐳 Container 1: mosquitto                                 │
│  ├─ Image: eclipse-mosquitto:2.0                          │
│  ├─ Ports: 1883 (MQTT), 9001 (WebSocket)                 │
│  ├─ Volumes: config, data, logs                           │
│  └─ Network: supply-chain-rl_default                      │
│                                                             │
│  🐳 Container 2: iot-simulator                             │
│  ├─ Build: ./iot_simulator                                │
│  ├─ Depends: mosquitto                                     │
│  ├─ Environment: MQTT_BROKER=mosquitto                     │
│  └─ Restart: unless-stopped                               │
│                                                             │
│  🐳 Container 3: edge-agent                                │
│  ├─ Build: ./edge_agent                                   │
│  ├─ Ports: 8080 (HTTP API)                               │
│  ├─ Volumes: ./edge_agent/models:/app/models             │
│  ├─ Depends: mosquitto                                     │
│  └─ Environment: MQTT_BROKER=mosquitto                     │
│                                                             │
│  🐳 Container 4: dashboard                                 │
│  ├─ Build: ./dashboard                                    │
│  ├─ Ports: 3000 (HTTP)                                   │
│  ├─ Depends: mosquitto, edge-agent                        │
│  └─ Environment: REACT_APP_MQTT_BROKER=ws://localhost:9001│
│                                                             │
│  🌐 Network: Bridge Network                                │
│  ├─ Internal DNS: Service discovery                       │
│  ├─ Port Mapping: Host to container                       │
│  └─ Isolation: Container-to-container communication       │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Technology Stack

### **Backend Technologies**
- **Python 3.9+**: Core programming language
- **TensorFlow Lite**: Edge AI inference
- **stable-baselines3**: RL training framework
- **Gymnasium**: RL environment framework
- **Flask**: REST API server
- **Paho MQTT**: MQTT client library

### **Frontend Technologies**
- **React.js 18**: User interface framework
- **Leaflet.js**: Interactive mapping
- **MQTT.js**: WebSocket MQTT client
- **CSS3**: Styling and animations

### **Infrastructure**
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Mosquitto**: MQTT message broker
- **Nginx**: Reverse proxy (optional)

### **Development Tools**
- **Google Colab**: Free GPU training
- **Jupyter Notebooks**: Interactive development
- **Git**: Version control
- **GitHub**: Code repository

## 🔧 System Requirements

### **Minimum Requirements**
- **CPU**: 2 cores, 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 2 GB free space
- **Network**: Internet connection for initial setup
- **OS**: Linux, macOS, or Windows with Docker

### **Recommended Requirements**
- **CPU**: 4 cores, 2.5 GHz
- **RAM**: 8 GB
- **Storage**: 5 GB free space
- **Network**: Stable internet connection
- **OS**: Ubuntu 20.04+ or macOS 12+

## 🚀 Performance Characteristics

### **Latency**
- **MQTT Message Delivery**: <10ms
- **RL Inference Time**: <50ms
- **API Response Time**: <100ms
- **Dashboard Update**: <200ms

### **Throughput**
- **MQTT Messages**: 1000+ msg/sec
- **RL Decisions**: 20+ decisions/sec
- **API Requests**: 100+ req/sec
- **Concurrent Users**: 50+ users

### **Scalability**
- **Horizontal**: Add more truck simulators
- **Vertical**: Increase container resources
- **Geographic**: Multi-region deployment
- **Load**: Auto-scaling with Kubernetes

## 🔒 Security Architecture

### **Network Security**
- **Container Isolation**: Docker network segmentation
- **Port Exposure**: Minimal external ports
- **MQTT Security**: Optional TLS encryption
- **API Security**: CORS configuration

### **Data Security**
- **No Sensitive Data**: Simulated data only
- **Local Processing**: No cloud data transfer
- **Ephemeral Storage**: No persistent sensitive data
- **Access Control**: Container-level isolation

## 📈 Monitoring & Observability

### **Health Checks**
- **Container Health**: Docker health checks
- **Service Health**: Custom health endpoints
- **Network Health**: Port connectivity tests
- **Application Health**: API response validation

### **Logging**
- **Structured Logs**: JSON format
- **Log Aggregation**: Docker Compose logs
- **Log Levels**: DEBUG, INFO, WARN, ERROR
- **Log Rotation**: Automatic cleanup

### **Metrics**
- **System Metrics**: CPU, Memory, Network
- **Application Metrics**: Message rates, latency
- **Business Metrics**: Decision accuracy, efficiency
- **Custom Dashboards**: Real-time monitoring

---

**This architecture provides a robust, scalable, and maintainable foundation for supply chain optimization using modern AI/ML and IoT technologies! 🚀**
