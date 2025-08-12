#!/usr/bin/env python3
"""
Validate that all required files are present for the supply chain RL system
"""

import os
import sys

def check_file(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists and report status"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} (MISSING)")
        return False

def main():
    print("🔍 Validating Supply Chain RL System Setup...\n")
    
    all_good = True
    
    # Core files
    files_to_check = [
        ("docker-compose.yml", "Docker Compose configuration"),
        ("README.md", "Main documentation"),
        ("SETUP.md", "Setup instructions"),
        ("start.sh", "Startup script"),
        ("test_system.sh", "Test script"),
        (".gitignore", "Git ignore file"),
    ]
    
    # RL Trainer files
    rl_files = [
        ("rl_trainer/supply_chain_env.py", "RL Environment"),
        ("rl_trainer/train.py", "Training script"),
        ("rl_trainer/requirements.txt", "RL dependencies"),
        ("rl_trainer/Supply_Chain_RL_Training.ipynb", "Colab notebook"),
    ]
    
    # IoT Simulator files
    iot_files = [
        ("iot_simulator/truck_simulator.py", "Truck simulator"),
        ("iot_simulator/requirements.txt", "IoT dependencies"),
        ("iot_simulator/Dockerfile", "IoT Docker config"),
    ]
    
    # Edge Agent files
    edge_files = [
        ("edge_agent/edge_inference.py", "Edge inference agent"),
        ("edge_agent/create_demo_model.py", "Demo model creator"),
        ("edge_agent/requirements.txt", "Edge dependencies"),
        ("edge_agent/Dockerfile", "Edge Docker config"),
    ]
    
    # Dashboard files
    dashboard_files = [
        ("dashboard/package.json", "React package config"),
        ("dashboard/Dockerfile", "Dashboard Docker config"),
        ("dashboard/src/App.js", "Main React app"),
        ("dashboard/src/components/TruckMap.js", "Map component"),
        ("dashboard/src/components/ActionLog.js", "Action log component"),
        ("dashboard/src/components/StatusPanel.js", "Status panel component"),
        ("dashboard/public/index.html", "HTML template"),
    ]
    
    # MQTT config
    mqtt_files = [
        ("mosquitto/config/mosquitto.conf", "MQTT broker config"),
    ]
    
    # Check all files
    print("📋 Core Files:")
    for filepath, desc in files_to_check:
        all_good &= check_file(filepath, desc)
    
    print("\n🧠 RL Trainer:")
    for filepath, desc in rl_files:
        all_good &= check_file(filepath, desc)
    
    print("\n📡 IoT Simulator:")
    for filepath, desc in iot_files:
        all_good &= check_file(filepath, desc)
    
    print("\n🤖 Edge Agent:")
    for filepath, desc in edge_files:
        all_good &= check_file(filepath, desc)
    
    print("\n📊 Dashboard:")
    for filepath, desc in dashboard_files:
        all_good &= check_file(filepath, desc)
    
    print("\n📨 MQTT Config:")
    for filepath, desc in mqtt_files:
        all_good &= check_file(filepath, desc)
    
    # Check directories
    print("\n📁 Directories:")
    dirs_to_check = [
        ("rl_trainer", "RL training directory"),
        ("iot_simulator", "IoT simulator directory"),
        ("edge_agent", "Edge agent directory"),
        ("dashboard", "Dashboard directory"),
        ("dashboard/src", "Dashboard source"),
        ("dashboard/src/components", "React components"),
        ("mosquitto", "MQTT directory"),
        ("mosquitto/config", "MQTT config directory"),
    ]
    
    for dirpath, desc in dirs_to_check:
        all_good &= check_directory(dirpath, desc)
    
    # Final result
    print("\n" + "="*50)
    if all_good:
        print("🎉 All files present! System is ready to deploy.")
        print("\n📋 Next steps:")
        print("1. Run: ./test_system.sh")
        print("2. Open: http://localhost:3000")
        print("3. Train model in Google Colab")
        return 0
    else:
        print("❌ Some files are missing. Please check the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
