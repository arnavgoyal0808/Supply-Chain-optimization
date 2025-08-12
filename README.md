# 🚛🤖 Supply Chain RL Optimization Engine

<div align="center">

![Supply Chain RL](https://img.shields.io/badge/Supply%20Chain-RL%20Optimization-blue?style=for-the-badge&logo=truck)
![Live Demo](https://img.shields.io/badge/Demo-Live%20Animations-red?style=for-the-badge&logo=play-circle)
![Cost](https://img.shields.io/badge/Cost-%240-green?style=for-the-badge&logo=dollar-sign)

**Zero-cost supply chain optimization with live RL decisions and real-time animations**

[🚀 Quick Start](#-quick-start) • [🎬 Live Demo](#-live-demo) • [📖 Docs](docs/ARCHITECTURE.md)

</div>

## 🎬 **Live Demo**

```bash
# Interactive HTML visualization
open docs/live_architecture.html

# Terminal monitoring
./live_demo.sh

# Dashboard with moving trucks
open http://localhost:3000
```

**Features**: Moving trucks, flowing MQTT messages, real-time RL decisions (<50ms), animated metrics

## 🚀 **Quick Start**

```bash
git clone https://github.com/arnavgoyal0808/Supply-Chain-optimization.git
cd Supply-Chain-optimization
./setup_and_run.sh
```

## 🏗️ **Architecture**

```
🚛 IoT Trucks → 📡 MQTT → 🤖 RL Agent → 📊 Dashboard
```

**Components**: 3 GPS trucks, Mosquitto MQTT, TensorFlow Lite edge inference, React.js dashboard

## 🧠 **RL Environment**

- **State**: `[inventory, demand, capacity, distance]`
- **Actions**: Hold (0), Produce (1), Ship (2)  
- **Algorithm**: PPO with TensorFlow Lite edge inference

## 🔧 **Monitoring**

```bash
./check_all_services.sh    # Health check
./live_demo.sh             # Real-time monitoring
./monitor_system.sh        # Continuous monitoring
```

## 📱 **Training**

**Google Colab**: Open `rl_trainer/Supply_Chain_RL_Training.ipynb`  
**Local**: `cd rl_trainer && python train.py --timesteps 50000`

## 🌐 **API Endpoints**

- `GET /api/health` - System status
- `GET /api/trucks` - Current truck positions  
- `GET /api/actions` - Recent RL decisions

## 💰 **Zero Cost Stack**

Google Colab (training) + Docker (local) + Mosquitto (MQTT) + React.js (UI) = **$0**

## 🚨 **Troubleshooting**

| Issue | Fix |
|-------|-----|
| Dashboard not loading | `lsof -i :3000` |
| No truck data | `docker-compose restart iot-simulator` |
| RL agent not working | `ls edge_agent/models/` |

## 📚 **Documentation**

- [🏗️ Architecture](docs/ARCHITECTURE.md) - Technical details
- [🎬 Live Features](docs/LIVE_ARCHITECTURE.md) - Animated diagrams
- [🔧 Setup Guide](SETUP.md) - Installation steps

## 📄 **License**

MIT License - Use freely for commercial and personal projects.

---

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/arnavgoyal0808/Supply-Chain-optimization?style=social)](https://github.com/arnavgoyal0808/Supply-Chain-optimization/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/arnavgoyal0808/Supply-Chain-optimization?style=social)](https://github.com/arnavgoyal0808/Supply-Chain-optimization/network/members)

**🚛 Built for the supply chain optimization community 🤖**

</div>
