#!/usr/bin/env python3
"""
Create a simple demo TensorFlow Lite model for immediate testing
This creates a basic model that makes reasonable supply chain decisions
"""

import tensorflow as tf
import numpy as np
import os

def create_demo_model():
    """Create a simple neural network for supply chain decisions"""
    
    # Define a simple model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(4,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax')  # 3 actions: hold, produce, ship
    ])
    
    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    
    # Generate some dummy training data with reasonable logic
    # State: [inventory, demand, capacity, distance]
    X_train = []
    y_train = []
    
    for _ in range(1000):
        inventory = np.random.randint(0, 100)
        demand = np.random.randint(10, 50)
        capacity = np.random.randint(30, 70)
        distance = np.random.randint(50, 300)
        
        state = [inventory, demand, capacity, distance]
        
        # Simple rule-based logic for training data
        if inventory < demand:
            action = 1  # Produce
        elif inventory >= demand and distance < 150:
            action = 2  # Ship
        else:
            action = 0  # Hold
        
        X_train.append(state)
        y_train.append(action)
    
    X_train = np.array(X_train, dtype=np.float32)
    y_train = np.array(y_train, dtype=np.int32)
    
    # Train the model
    print("Training demo model...")
    model.fit(X_train, y_train, epochs=50, verbose=0)
    
    # Convert to TensorFlow Lite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    with open('models/supply_chain_model.tflite', 'wb') as f:
        f.write(tflite_model)
    
    print(f"Demo TensorFlow Lite model created: {len(tflite_model)} bytes")
    print("Model saved to models/supply_chain_model.tflite")
    
    return tflite_model

if __name__ == "__main__":
    create_demo_model()
