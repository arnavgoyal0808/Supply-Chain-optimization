#!/usr/bin/env python3
"""
Edge Inference Agent
Subscribes to MQTT truck data and makes RL-based decisions using TensorFlow Lite
"""

import json
import os
import time
import numpy as np
import paho.mqtt.client as mqtt
import tensorflow as tf
from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread, Lock
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EdgeInferenceAgent:
    def __init__(self):
        self.model_path = "/app/models/supply_chain_model.tflite"
        self.interpreter = None
        self.mqtt_client = None
        self.actions_log = []
        self.actions_lock = Lock()
        self.truck_data = {}
        
        # Action mapping
        self.action_names = {0: "Hold", 1: "Produce", 2: "Ship"}
        
        # Load TensorFlow Lite model
        self.load_model()
        
        # Setup MQTT
        self.setup_mqtt()
        
        # Setup Flask API
        self.setup_flask()
    
    def load_model(self):
        """Load TensorFlow Lite model"""
        if os.path.exists(self.model_path):
            try:
                self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
                self.interpreter.allocate_tensors()
                
                # Get input and output details
                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()
                
                logger.info("TensorFlow Lite model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load TFLite model: {e}")
                self.interpreter = None
        else:
            logger.warning(f"Model file not found: {self.model_path}")
            logger.info("Using random action selection as fallback")
    
    def predict_action(self, observation):
        """Predict action using TensorFlow Lite model"""
        if self.interpreter is None:
            # Fallback to random action if model not available
            return np.random.randint(0, 3)
        
        try:
            # Prepare input
            input_data = np.array([observation], dtype=np.float32)
            
            # Set input tensor
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            
            # Run inference
            self.interpreter.invoke()
            
            # Get output
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Return predicted action
            return int(np.argmax(output_data[0]))
            
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return np.random.randint(0, 3)
    
    def process_truck_data(self, truck_data):
        """Process truck data and generate action recommendation"""
        try:
            # Extract features for RL model
            # State: [inventory_level, demand_forecast, truck_capacity, distance_to_warehouse]
            inventory = truck_data.get('inventory', 50)
            demand = np.random.randint(10, 50)  # Simulated demand forecast
            capacity = 60  # Assumed truck capacity
            
            # Calculate distance to warehouse (assuming warehouse at downtown LA)
            warehouse_lat, warehouse_lng = 34.0522, -118.2437
            truck_lat, truck_lng = truck_data.get('lat', 34.0), truck_data.get('lng', -118.0)
            
            # Simple distance calculation (in km, approximated)
            distance = np.sqrt((truck_lat - warehouse_lat)**2 + (truck_lng - warehouse_lng)**2) * 111
            
            # Create observation
            observation = [inventory, demand, capacity, distance]
            
            # Predict action
            action = self.predict_action(observation)
            action_name = self.action_names[action]
            
            # Create action log entry
            action_entry = {
                'truck_id': truck_data.get('truck_id'),
                'timestamp': int(time.time()),
                'action': action_name,
                'inventory': inventory,
                'distance': round(distance, 2),
                'lat': truck_data.get('lat'),
                'lng': truck_data.get('lng')
            }
            
            # Add to actions log
            with self.actions_lock:
                self.actions_log.append(action_entry)
                # Keep only last 100 actions
                if len(self.actions_log) > 100:
                    self.actions_log.pop(0)
            
            logger.info(f"Truck {truck_data.get('truck_id')}: {action_name} "
                       f"(Inventory: {inventory}, Distance: {distance:.2f}km)")
            
            return action_entry
            
        except Exception as e:
            logger.error(f"Error processing truck data: {e}")
            return None
    
    def setup_mqtt(self):
        """Setup MQTT client and callbacks"""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.info("Connected to MQTT broker")
                client.subscribe("trucks/+/data")
            else:
                logger.error(f"Failed to connect to MQTT broker: {rc}")
        
        def on_message(client, userdata, msg):
            try:
                # Parse truck data
                truck_data = json.loads(msg.payload.decode())
                
                # Store truck data
                truck_id = truck_data.get('truck_id')
                self.truck_data[truck_id] = truck_data
                
                # Process data and generate action
                self.process_truck_data(truck_data)
                
            except Exception as e:
                logger.error(f"Error processing MQTT message: {e}")
        
        # Create MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = on_connect
        self.mqtt_client.on_message = on_message
        
        # Connect to broker
        mqtt_broker = os.getenv('MQTT_BROKER', 'localhost')
        mqtt_port = int(os.getenv('MQTT_PORT', 1883))
        
        logger.info(f"Connecting to MQTT broker at {mqtt_broker}:{mqtt_port}")
        self.mqtt_client.connect(mqtt_broker, mqtt_port, 60)
        self.mqtt_client.loop_start()
    
    def setup_flask(self):
        """Setup Flask API for dashboard communication"""
        self.app = Flask(__name__)
        CORS(self.app)
        
        @self.app.route('/api/actions', methods=['GET'])
        def get_actions():
            """Get recent actions log"""
            with self.actions_lock:
                return jsonify(self.actions_log[-50:])  # Return last 50 actions
        
        @self.app.route('/api/trucks', methods=['GET'])
        def get_trucks():
            """Get current truck data"""
            return jsonify(self.truck_data)
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'model_loaded': self.interpreter is not None,
                'mqtt_connected': self.mqtt_client.is_connected() if self.mqtt_client else False
            })
    
    def run(self):
        """Start the Flask API server"""
        self.app.run(host='0.0.0.0', port=8080, debug=False)

def main():
    agent = EdgeInferenceAgent()
    
    # Start Flask server in main thread
    logger.info("Starting Edge Inference Agent on port 8080...")
    agent.run()

if __name__ == "__main__":
    main()
