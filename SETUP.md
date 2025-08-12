# Setup Instructions

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start

```bash
git clone https://github.com/arnavgoyal0808/Supply-Chain-optimization.git
cd Supply-Chain-optimization
./setup_and_run.sh
```

## Manual Setup

```bash
# Create demo model
cd edge_agent && python3 create_demo_model.py && cd ..

# Start services
docker-compose up --build -d

# Check status
docker-compose ps
```

## Access Points

- Dashboard: http://localhost:3000
- Edge Agent: http://localhost:8080/api/health
- MQTT Broker: localhost:1883

## Troubleshooting

```bash
# View logs
docker-compose logs -f

# Restart service
docker-compose restart edge-agent

# Rebuild
docker-compose down && docker-compose up --build -d
```
