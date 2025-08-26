#!/usr/bin/env python
"""
Simplified Supply Chain Optimization Demo
This script simulates the key components of the system without Docker
"""

import os
import time
import random
import json
import threading
import http.server
import socketserver
import webbrowser
from datetime import datetime

# Global variables
truck_data = []
rl_actions = []
system_running = True

# Simulate truck data
def generate_truck_data():
    global truck_data
    truck_ids = ["Truck-A", "Truck-B", "Truck-C"]
    
    while system_running:
        new_data = []
        for truck_id in truck_ids:
            # Simulate truck movement
            lat = 34.0 + random.uniform(-0.1, 0.1)
            lng = -118.2 + random.uniform(-0.1, 0.1)
            
            # Simulate inventory and other metrics
            inventory = random.randint(10, 90)
            fuel = random.randint(30, 100)
            
            new_data.append({
                "id": truck_id,
                "lat": lat,
                "lng": lng,
                "inventory": inventory,
                "fuel": fuel,
                "timestamp": datetime.now().isoformat()
            })
        
        truck_data = new_data
        time.sleep(2)  # Update every 2 seconds

# Simulate RL agent decisions
def simulate_rl_agent():
    global rl_actions, truck_data
    
    actions = ["Hold", "Produce", "Ship"]
    
    while system_running:
        if truck_data:
            for truck in truck_data:
                # Simple rule-based logic
                inventory = truck.get("inventory", 50)
                
                if inventory < 30:
                    action = "Produce"
                elif inventory > 70:
                    action = "Ship"
                else:
                    action = "Hold"
                
                # Record the action
                rl_actions.append({
                    "truck_id": truck["id"],
                    "action": action,
                    "inventory": inventory,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Keep only the last 20 actions
                if len(rl_actions) > 20:
                    rl_actions = rl_actions[-20:]
        
        time.sleep(3)  # Make decisions every 3 seconds

# Create a simple HTTP server for API endpoints
class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/trucks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(truck_data).encode())
        
        elif self.path == '/api/actions':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(rl_actions).encode())
        
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            health_data = {
                "status": "healthy",
                "components": {
                    "truck_simulator": "running",
                    "rl_agent": "running",
                    "api_server": "running"
                }
            }
            self.wfile.write(json.dumps(health_data).encode())
        
        elif self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Simple dashboard HTML
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Supply Chain Optimization Dashboard</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
                    .card { background-color: white; border-radius: 5px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    .truck-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
                    .truck-card { background-color: white; border-radius: 5px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    .truck-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
                    .truck-id { font-weight: bold; font-size: 18px; }
                    .truck-action { padding: 5px 10px; border-radius: 15px; font-size: 14px; }
                    .action-hold { background-color: #f1c40f; color: #000; }
                    .action-produce { background-color: #2ecc71; color: #fff; }
                    .action-ship { background-color: #3498db; color: #fff; }
                    .metric { margin: 10px 0; }
                    .metric-label { font-size: 12px; color: #7f8c8d; }
                    .metric-value { font-size: 16px; font-weight: bold; }
                    .progress-bar { height: 8px; background-color: #ecf0f1; border-radius: 4px; margin-top: 5px; }
                    .progress-fill { height: 100%; border-radius: 4px; }
                    .inventory-fill { background-color: #3498db; }
                    .fuel-fill { background-color: #e74c3c; }
                    .actions-table { width: 100%; border-collapse: collapse; }
                    .actions-table th, .actions-table td { padding: 10px; text-align: left; border-bottom: 1px solid #ecf0f1; }
                    .actions-table th { background-color: #f9f9f9; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚛 Supply Chain Optimization Dashboard</h1>
                        <p>Real-time truck monitoring and RL-based decision making</p>
                    </div>
                    
                    <div class="card">
                        <h2>System Status</h2>
                        <div id="system-status">Loading...</div>
                    </div>
                    
                    <div class="card">
                        <h2>Truck Fleet</h2>
                        <div id="truck-grid" class="truck-grid">Loading trucks...</div>
                    </div>
                    
                    <div class="card">
                        <h2>Recent RL Actions</h2>
                        <div id="actions-log">
                            <table class="actions-table">
                                <thead>
                                    <tr>
                                        <th>Truck</th>
                                        <th>Action</th>
                                        <th>Inventory</th>
                                        <th>Time</th>
                                    </tr>
                                </thead>
                                <tbody id="actions-tbody">
                                    <tr>
                                        <td colspan="4">Loading actions...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                
                <script>
                    // Fetch truck data
                    function fetchTrucks() {
                        fetch('/api/trucks')
                            .then(response => response.json())
                            .then(data => {
                                const truckGrid = document.getElementById('truck-grid');
                                truckGrid.innerHTML = '';
                                
                                data.forEach(truck => {
                                    const truckCard = document.createElement('div');
                                    truckCard.className = 'truck-card';
                                    
                                    // Get the latest action for this truck
                                    let actionClass = 'action-hold';
                                    let actionText = 'Hold';
                                    
                                    truckCard.innerHTML = `
                                        <div class="truck-header">
                                            <div class="truck-id">${truck.id}</div>
                                            <div class="truck-action ${actionClass}">${actionText}</div>
                                        </div>
                                        <div class="metric">
                                            <div class="metric-label">Inventory Level</div>
                                            <div class="metric-value">${truck.inventory}%</div>
                                            <div class="progress-bar">
                                                <div class="progress-fill inventory-fill" style="width: ${truck.inventory}%"></div>
                                            </div>
                                        </div>
                                        <div class="metric">
                                            <div class="metric-label">Fuel Level</div>
                                            <div class="metric-value">${truck.fuel}%</div>
                                            <div class="progress-bar">
                                                <div class="progress-fill fuel-fill" style="width: ${truck.fuel}%"></div>
                                            </div>
                                        </div>
                                        <div class="metric">
                                            <div class="metric-label">Location</div>
                                            <div class="metric-value">Lat: ${truck.lat.toFixed(4)}, Lng: ${truck.lng.toFixed(4)}</div>
                                        </div>
                                    `;
                                    
                                    truckGrid.appendChild(truckCard);
                                });
                            })
                            .catch(error => {
                                console.error('Error fetching truck data:', error);
                                document.getElementById('truck-grid').innerHTML = 'Error loading truck data.';
                            });
                    }
                    
                    // Fetch RL actions
                    function fetchActions() {
                        fetch('/api/actions')
                            .then(response => response.json())
                            .then(data => {
                                const actionsTbody = document.getElementById('actions-tbody');
                                actionsTbody.innerHTML = '';
                                
                                // Sort by timestamp descending
                                data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                                
                                data.forEach(action => {
                                    const row = document.createElement('tr');
                                    const time = new Date(action.timestamp);
                                    const timeStr = time.toLocaleTimeString();
                                    
                                    row.innerHTML = `
                                        <td>${action.truck_id}</td>
                                        <td>${action.action}</td>
                                        <td>${action.inventory}%</td>
                                        <td>${timeStr}</td>
                                    `;
                                    
                                    actionsTbody.appendChild(row);
                                });
                                
                                if (data.length === 0) {
                                    actionsTbody.innerHTML = '<tr><td colspan="4">No actions recorded yet.</td></tr>';
                                }
                            })
                            .catch(error => {
                                console.error('Error fetching actions:', error);
                                document.getElementById('actions-tbody').innerHTML = 
                                    '<tr><td colspan="4">Error loading actions.</td></tr>';
                            });
                    }
                    
                    // Fetch system health
                    function fetchHealth() {
                        fetch('/api/health')
                            .then(response => response.json())
                            .then(data => {
                                const statusDiv = document.getElementById('system-status');
                                statusDiv.innerHTML = `
                                    <div style="color: ${data.status === 'healthy' ? 'green' : 'red'}; font-weight: bold;">
                                        System Status: ${data.status.toUpperCase()}
                                    </div>
                                    <div style="margin-top: 10px;">
                                        <div>Truck Simulator: ${data.components.truck_simulator}</div>
                                        <div>RL Agent: ${data.components.rl_agent}</div>
                                        <div>API Server: ${data.components.api_server}</div>
                                    </div>
                                `;
                            })
                            .catch(error => {
                                console.error('Error fetching health data:', error);
                                document.getElementById('system-status').innerHTML = 'Error loading system status.';
                            });
                    }
                    
                    // Update data periodically
                    setInterval(fetchTrucks, 2000);
                    setInterval(fetchActions, 3000);
                    setInterval(fetchHealth, 5000);
                    
                    // Initial fetch
                    fetchTrucks();
                    fetchActions();
                    fetchHealth();
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        else:
            self.send_error(404, "Not Found")

def run_api_server():
    port = 8000
    handler = APIHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"API server running at http://localhost:{port}")
        while system_running:
            httpd.handle_request()

def main():
    global system_running
    
    print("🚛 Starting Supply Chain Optimization Demo")
    print("==========================================")
    
    # Create threads for each component
    truck_thread = threading.Thread(target=generate_truck_data)
    rl_thread = threading.Thread(target=simulate_rl_agent)
    api_thread = threading.Thread(target=run_api_server)
    
    # Start all threads
    truck_thread.daemon = True
    rl_thread.daemon = True
    api_thread.daemon = True
    
    truck_thread.start()
    print("✅ Truck simulator started")
    
    rl_thread.start()
    print("✅ RL agent started")
    
    api_thread.start()
    print("✅ API server started")
    
    # Open browser
    webbrowser.open('http://localhost:8000')
    print("✅ Opening dashboard in browser")
    
    try:
        print("\n📊 Dashboard is running at http://localhost:8000")
        print("Press Ctrl+C to stop the demo")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping the demo...")
        system_running = False
        time.sleep(2)  # Give threads time to clean up
        print("👋 Demo stopped")

if __name__ == "__main__":
    main()