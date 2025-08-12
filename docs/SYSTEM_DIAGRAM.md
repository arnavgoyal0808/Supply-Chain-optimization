# 🎨 Supply Chain RL System - Visual Architecture

## 🏗️ Complete System Architecture Diagram

```
                    SUPPLY CHAIN RL OPTIMIZATION ENGINE
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                               ║
    ║  ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐ ║
    ║  │   🚛 IoT LAYER  │         │ 📡 COMMUNICATION│         │  🤖 AI/ML LAYER │ ║
    ║  │                 │         │      LAYER      │         │                 │ ║
    ║  │  ┌───────────┐  │         │                 │         │  ┌───────────┐  │ ║
    ║  │  │ Truck 1   │──┼─────────│   MQTT Broker   │─────────┼──│ RL Agent  │  │ ║
    ║  │  │ GPS+Inv   │  │         │   (Mosquitto)   │         │  │ (PPO)     │  │ ║
    ║  │  └───────────┘  │         │                 │         │  └───────────┘  │ ║
    ║  │  ┌───────────┐  │         │  ┌───────────┐  │         │  ┌───────────┐  │ ║
    ║  │  │ Truck 2   │──┼─────────│  │ Message   │  │─────────┼──│ TFLite    │  │ ║
    ║  │  │ GPS+Inv   │  │         │  │ Queue     │  │         │  │ Inference │  │ ║
    ║  │  └───────────┘  │         │  └───────────┘  │         │  └───────────┘  │ ║
    ║  │  ┌───────────┐  │         │  ┌───────────┐  │         │  ┌───────────┐  │ ║
    ║  │  │ Truck 3   │──┼─────────│  │ WebSocket │  │─────────┼──│ Decision  │  │ ║
    ║  │  │ GPS+Inv   │  │         │  │ Support   │  │         │  │ Engine    │  │ ║
    ║  │  └───────────┘  │         │  └───────────┘  │         │  └───────────┘  │ ║
    ║  └─────────────────┘         └─────────────────┘         └─────────────────┘ ║
    ║           │                           │                           │           ║
    ║           │                           │                           │           ║
    ║           └───────────────────────────┼───────────────────────────┘           ║
    ║                                       │                                       ║
    ║                                       ▼                                       ║
    ║                        ┌─────────────────────────────────┐                   ║
    ║                        │      📊 PRESENTATION LAYER      │                   ║
    ║                        │                                 │                   ║
    ║                        │  ┌─────────────────────────────┐│                   ║
    ║                        │  │    🗺️ Interactive Map       ││                   ║
    ║                        │  │   (Leaflet.js + React)     ││                   ║
    ║                        │  └─────────────────────────────┘│                   ║
    ║                        │  ┌─────────────────────────────┐│                   ║
    ║                        │  │    📋 Real-time Action Log  ││                   ║
    ║                        │  │   (RL Decision History)    ││                   ║
    ║                        │  └─────────────────────────────┘│                   ║
    ║                        │  ┌─────────────────────────────┐│                   ║
    ║                        │  │    📈 Status Dashboard      ││                   ║
    ║                        │  │   (System Health Monitor)  ││                   ║
    ║                        │  └─────────────────────────────┘│                   ║
    ║                        └─────────────────────────────────┘                   ║
    ║                                                                               ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 🔄 Data Flow Visualization

```
    IoT Trucks                MQTT Broker              Edge Agent               Dashboard
    ┌─────────┐              ┌─────────────┐           ┌─────────────┐          ┌─────────┐
    │ 🚛      │              │             │           │             │          │ 📊      │
    │ Truck 1 │─────────────▶│   Message   │──────────▶│ RL Model    │─────────▶│ Live    │
    │ GPS+Inv │   MQTT       │   Routing   │   MQTT    │ Inference   │   API    │ Map     │
    └─────────┘   Publish    │             │ Subscribe │             │ Calls    └─────────┘
    ┌─────────┐              │             │           │             │          ┌─────────┐
    │ 🚛      │              │ Port 1883   │           │ TensorFlow  │          │ 📋      │
    │ Truck 2 │─────────────▶│ Port 9001   │──────────▶│ Lite        │─────────▶│ Action  │
    │ GPS+Inv │   Every      │ (WebSocket) │   Real    │ Model       │   JSON   │ Log     │
    └─────────┘   2 seconds  │             │   Time    │             │ Response └─────────┘
    ┌─────────┐              │             │           │             │          ┌─────────┐
    │ 🚛      │              │ Mosquitto   │           │ Decision:   │          │ 📈      │
    │ Truck 3 │─────────────▶│ Broker      │──────────▶│ Hold/       │─────────▶│ Status  │
    │ GPS+Inv │   JSON       │             │   Topic   │ Produce/    │   HTTP   │ Panel   │
    └─────────┘   Messages   └─────────────┘   Filter  │ Ship        │   REST   └─────────┘
                                                        └─────────────┘
```

## 🐳 Docker Container Architecture

```
                            DOCKER COMPOSE ORCHESTRATION
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                               ║
    ║  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐           ║
    ║  │ 📨 mosquitto    │    │ 🚛 iot-simulator│    │ 🤖 edge-agent   │           ║
    ║  │                 │    │                 │    │                 │           ║
    ║  │ Port: 1883      │◀───│ MQTT Publisher  │    │ MQTT Subscriber │           ║
    ║  │ Port: 9001      │    │                 │    │ Port: 8080      │           ║
    ║  │                 │    │ 3 Truck Sims   │    │                 │           ║
    ║  │ eclipse-        │    │                 │    │ TFLite Model    │           ║
    ║  │ mosquitto:2.0   │    │ Python 3.9      │    │ Flask API       │           ║
    ║  │                 │    │                 │    │ Python 3.9      │           ║
    ║  └─────────────────┘    └─────────────────┘    └─────────────────┘           ║
    ║           │                       │                       │                  ║
    ║           └───────────────────────┼───────────────────────┘                  ║
    ║                                   │                                          ║
    ║                                   ▼                                          ║
    ║                        ┌─────────────────┐                                  ║
    ║                        │ 📊 dashboard    │                                  ║
    ║                        │                 │                                  ║
    ║                        │ Port: 3000      │                                  ║
    ║                        │                 │                                  ║
    ║                        │ React.js App    │                                  ║
    ║                        │ Leaflet Maps    │                                  ║
    ║                        │ MQTT WebSocket  │                                  ║
    ║                        │ Node.js 18      │                                  ║
    ║                        │                 │                                  ║
    ║                        └─────────────────┘                                  ║
    ║                                                                               ║
    ║  Network: supply-chain-rl_default (Bridge)                                   ║
    ║  DNS: Automatic service discovery                                             ║
    ║  Volumes: Persistent storage for MQTT data and ML models                     ║
    ║                                                                               ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 🧠 RL Agent Decision Flow

```
                            REINFORCEMENT LEARNING PIPELINE
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │  📡 MQTT Input          🧠 RL Processing           📤 Action Output         │
    │  ┌─────────────┐       ┌─────────────────┐        ┌─────────────┐          │
    │  │ Truck Data  │       │                 │        │ Decision    │          │
    │  │             │       │  State Vector   │        │             │          │
    │  │ truck_id: 1 │──────▶│  [inventory,    │───────▶│ Action: 0   │          │
    │  │ lat: 34.05  │       │   demand,       │        │ (Hold)      │          │
    │  │ lng: -118.2 │       │   capacity,     │        │             │          │
    │  │ inventory:50│       │   distance]     │        │ Action: 1   │          │
    │  │ timestamp   │       │                 │        │ (Produce)   │          │
    │  └─────────────┘       │  TensorFlow     │        │             │          │
    │         │               │  Lite Model     │        │ Action: 2   │          │
    │         │               │                 │        │ (Ship)      │          │
    │         ▼               │  Input: 4D      │        │             │          │
    │  ┌─────────────┐       │  Hidden: 32     │        └─────────────┘          │
    │  │ Feature     │       │  Hidden: 16     │               │                 │
    │  │ Extraction  │──────▶│  Output: 3      │               │                 │
    │  │             │       │                 │               ▼                 │
    │  │ Normalize   │       │  Activation:    │        ┌─────────────┐          │
    │  │ Calculate   │       │  ReLU + Softmax │        │ Action Log  │          │
    │  │ Distance    │       │                 │        │             │          │
    │  │ Estimate    │       │  Inference:     │        │ Store in    │          │
    │  │ Demand      │       │  < 50ms         │        │ Database    │          │
    │  └─────────────┘       └─────────────────┘        │ Send to     │          │
    │                                                    │ Dashboard   │          │
    │                                                    └─────────────┘          │
    └─────────────────────────────────────────────────────────────────────────────┘
```

## 🌐 Network Communication Diagram

```
                            NETWORK COMMUNICATION FLOW
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │  External Access                    Docker Network                          │
    │  ┌─────────────┐                   ┌─────────────────────────────────────┐  │
    │  │ 🌐 Browser  │                   │                                     │  │
    │  │             │                   │  ┌─────────────┐  ┌─────────────┐   │  │
    │  │ localhost:  │──── HTTP ────────▶│  │ dashboard   │  │ edge-agent  │   │  │
    │  │ 3000        │                   │  │ :3000       │  │ :8080       │   │  │
    │  │             │                   │  └─────────────┘  └─────────────┘   │  │
    │  └─────────────┘                   │         │               │          │  │
    │                                    │         │               │          │  │
    │  ┌─────────────┐                   │         ▼               ▼          │  │
    │  │ 📱 MQTT     │                   │  ┌─────────────────────────────────┐│  │
    │  │ Client      │──── WebSocket ───▶│  │         mosquitto               ││  │
    │  │             │     :9001         │  │         :1883 (MQTT)            ││  │
    │  │ localhost:  │                   │  │         :9001 (WebSocket)       ││  │
    │  │ 9001        │                   │  └─────────────────────────────────┘│  │
    │  └─────────────┘                   │                   │                 │  │
    │                                    │                   │                 │  │
    │  ┌─────────────┐                   │                   ▼                 │  │
    │  │ 🔧 API      │                   │         ┌─────────────┐             │  │
    │  │ Client      │──── HTTP ────────▶│         │iot-simulator│             │  │
    │  │             │     :8080         │         │             │             │  │
    │  │ localhost:  │                   │         │ 3 Trucks    │             │  │
    │  │ 8080        │                   │         │ Publishing  │             │  │
    │  └─────────────┘                   │         └─────────────┘             │  │
    │                                    │                                     │  │
    │                                    └─────────────────────────────────────┘  │
    │                                                                             │
    │  Port Mappings:                                                             │
    │  • 3000:3000  → Dashboard (React.js)                                       │
    │  • 8080:8080  → Edge Agent API (Flask)                                     │
    │  • 1883:1883  → MQTT Broker (Mosquitto)                                    │
    │  • 9001:9001  → MQTT WebSocket (Mosquitto)                                 │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Real-time Dashboard Layout

```
                            DASHBOARD USER INTERFACE
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                    Supply Chain RL Dashboard                                 ║
    ╠═══════════════════════════════════════════════════════════════════════════════╣
    ║  📊 Status: Connected | 🚛 Trucks: 3 | 🤖 Actions: 127 | ⏰ 14:32:15        ║
    ╠═══════════════════════════════════════════════════════════════════════════════╣
    ║                                                                               ║
    ║  ┌─────────────────────────────────────┐  ┌─────────────────────────────────┐ ║
    ║  │           🗺️ LIVE MAP                │  │      📋 ACTION LOG              │ ║
    ║  │                                     │  │                                 │ ║
    ║  │  🏢 Warehouse (Downtown LA)         │  │ Time    | Truck | Action | Inv  │ ║
    ║  │                                     │  │---------|------|--------|------│ ║
    ║  │     🚛 Truck 1 (Moving NE)         │  │ 14:32:15| T1   | Ship   | 45   │ ║
    ║  │        Inventory: 45 units          │  │ 14:32:13| T3   | Produce| 67   │ ║
    ║  │        Status: Shipping             │  │ 14:32:11| T2   | Hold   | 23   │ ║
    ║  │                                     │  │ 14:32:09| T1   | Produce| 50   │ ║
    ║  │  🚛 Truck 2 (Moving SW)            │  │ 14:32:07| T3   | Ship   | 72   │ ║
    ║  │     Inventory: 23 units             │  │ 14:32:05| T2   | Ship   | 28   │ ║
    ║  │     Status: Holding                 │  │ 14:32:03| T1   | Hold   | 45   │ ║
    ║  │                                     │  │ 14:32:01| T3   | Produce| 77   │ ║
    ║  │        🚛 Truck 3 (Moving N)       │  │ 14:31:59| T2   | Produce| 33   │ ║
    ║  │           Inventory: 67 units       │  │ 14:31:57| T1   | Ship   | 50   │ ║
    ║  │           Status: Producing         │  │                                 │ ║
    ║  │                                     │  │ 📊 Action Summary:              │ ║
    ║  │  📍 Real-time GPS tracking          │  │ • Hold: 42 (33%)                │ ║
    ║  │  🔄 Updates every 2 seconds         │  │ • Produce: 45 (35%)             │ ║
    ║  │  🎯 Click markers for details       │  │ • Ship: 40 (32%)                │ ║
    ║  │                                     │  │                                 │ ║
    ║  └─────────────────────────────────────┘  └─────────────────────────────────┘ ║
    ║                                                                               ║
    ║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
    ║  │                        📈 SYSTEM METRICS                                │ ║
    ║  │                                                                         │ ║
    ║  │  🔄 Message Rate: 6 msg/sec  |  ⚡ Latency: 45ms  |  💾 Memory: 234MB  │ ║
    ║  │  📡 MQTT Status: ✅ Connected |  🤖 RL Model: ✅ Loaded | 🌐 API: ✅ OK │ ║
    ║  │                                                                         │ ║
    ║  └─────────────────────────────────────────────────────────────────────────┘ ║
    ║                                                                               ║
    ╚═══════════════════════════════════════════════════════════════════════════════╝
```

## 🔄 Development Workflow

```
                            DEVELOPMENT & DEPLOYMENT PIPELINE
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │  🧑‍💻 Development        🏗️ Build & Test         🚀 Deployment              │
    │  ┌─────────────┐       ┌─────────────────┐      ┌─────────────────┐        │
    │  │             │       │                 │      │                 │        │
    │  │ 1. Code     │──────▶│ 4. Docker       │─────▶│ 7. Production   │        │
    │  │    Changes  │       │    Build        │      │    Deploy       │        │
    │  │             │       │                 │      │                 │        │
    │  │ 2. Local    │──────▶│ 5. Integration  │─────▶│ 8. Health       │        │
    │  │    Testing  │       │    Testing      │      │    Monitoring   │        │
    │  │             │       │                 │      │                 │        │
    │  │ 3. Git      │──────▶│ 6. Performance  │─────▶│ 9. Auto         │        │
    │  │    Commit   │       │    Validation   │      │    Scaling      │        │
    │  │             │       │                 │      │                 │        │
    │  └─────────────┘       └─────────────────┘      └─────────────────┘        │
    │                                                                             │
    │  Tools Used:                                                                │
    │  • VS Code / PyCharm    • Docker Compose      • Docker Swarm               │
    │  • Git / GitHub         • pytest              • Kubernetes                 │
    │  • Python venv          • GitHub Actions      • Prometheus                 │
    │  • Node.js / npm        • SonarQube           • Grafana                    │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘
```

---

**These visual diagrams provide a comprehensive understanding of the system architecture, data flow, and component interactions! 🎨🏗️**
