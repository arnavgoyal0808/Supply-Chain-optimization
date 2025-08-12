#!/usr/bin/env python3
"""
IoT Truck Simulator
Publishes GPS and inventory data for 3 trucks to MQTT broker
"""

import json
import time
import random
import os
import paho.mqtt.client as mqtt
import numpy as np
from threading import Thread

class TruckSimulator:
    def __init__(self, truck_id, initial_lat, initial_lng, mqtt_client):
        self.truck_id = truck_id
        self.lat = initial_lat
        self.lng = initial_lng
        self.inventory = random.randint(20, 80)
        self.mqtt_client = mqtt_client
        self.running = True
        
        # Movement parameters
        self.speed = 0.001  # degrees per update
        self.direction = random.uniform(0, 2 * np.pi)
        
    def update_position(self):
        """Simulate truck movement"""
        # Random walk with some momentum
        self.direction += random.uniform(-0.3, 0.3)
        
        # Move truck
        self.lat += self.speed * np.cos(self.direction)
        self.lng += self.speed * np.sin(self.direction)
        
        # Keep within reasonable bounds (Los Angeles area)
        self.lat = max(33.7, min(34.3, self.lat))
        self.lng = max(-118.7, min(-117.9, self.lng))
        
        # Simulate inventory changes
        if random.random() < 0.1:  # 10% chance of inventory change
            self.inventory += random.randint(-5, 5)
            self.inventory = max(0, min(100, self.inventory))
    
    def publish_data(self):
        """Publish truck data to MQTT"""
        data = {
            "truck_id": self.truck_id,
            "lat": round(self.lat, 6),
            "lng": round(self.lng, 6),
            "inventory": self.inventory,
            "timestamp": int(time.time())
        }
        
        topic = f"trucks/{self.truck_id}/data"
        self.mqtt_client.publish(topic, json.dumps(data))
        print(f"Truck {self.truck_id}: {data}")
    
    def run(self):
        """Main simulation loop"""
        while self.running:
            self.update_position()
            self.publish_data()
            time.sleep(2)  # Update every 2 seconds

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect to MQTT broker: {rc}")

def main():
    # MQTT configuration
    mqtt_broker = os.getenv('MQTT_BROKER', 'localhost')
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    
    # Create MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    
    # Connect to broker
    print(f"Connecting to MQTT broker at {mqtt_broker}:{mqtt_port}")
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()
    
    # Wait for connection
    time.sleep(2)
    
    # Create 3 truck simulators with different starting positions
    trucks = [
        TruckSimulator(1, 34.0522, -118.2437, client),  # Downtown LA
        TruckSimulator(2, 34.1478, -118.1445, client),  # Pasadena
        TruckSimulator(3, 33.9425, -118.4081, client),  # LAX area
    ]
    
    # Start truck simulation threads
    threads = []
    for truck in trucks:
        thread = Thread(target=truck.run)
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    print("Started 3 truck simulators. Publishing data every 2 seconds...")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down truck simulators...")
        for truck in trucks:
            truck.running = False
        
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
