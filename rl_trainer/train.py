#!/usr/bin/env python3
"""
Supply Chain RL Training Script
Run this in Google Colab for free GPU training
"""

import argparse
import os
import numpy as np
import tensorflow as tf
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from supply_chain_env import SupplyChainEnv

def train_model(timesteps=10000):
    """Train PPO agent on supply chain environment"""
    
    # Create vectorized environment
    env = make_vec_env(SupplyChainEnv, n_envs=4)
    
    # Initialize PPO agent
    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
        tensorboard_log="./tensorboard_logs/"
    )
    
    print(f"Training PPO agent for {timesteps} timesteps...")
    model.learn(total_timesteps=timesteps)
    
    # Save the trained model
    model.save("supply_chain_ppo")
    print("Model saved as 'supply_chain_ppo'")
    
    return model

def convert_to_tflite(model_path="supply_chain_ppo"):
    """Convert trained model to TensorFlow Lite for edge deployment"""
    
    # Load the trained model
    model = PPO.load(model_path)
    
    # Create a dummy environment to get observation shape
    env = SupplyChainEnv()
    obs_shape = env.observation_space.shape
    
    # Extract the policy network
    policy = model.policy
    
    # Create a TensorFlow function for inference
    @tf.function
    def inference_func(observations):
        # Convert to tensor
        obs_tensor = tf.convert_to_tensor(observations, dtype=tf.float32)
        
        # Get action probabilities
        actions, _, _ = policy(obs_tensor)
        return actions
    
    # Create concrete function with input signature
    concrete_func = inference_func.get_concrete_function(
        tf.TensorSpec(shape=[None] + list(obs_shape), dtype=tf.float32)
    )
    
    # Convert to TensorFlow Lite
    converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()
    
    # Save the TFLite model
    os.makedirs("../edge_agent/models", exist_ok=True)
    with open("../edge_agent/models/supply_chain_model.tflite", "wb") as f:
        f.write(tflite_model)
    
    print("Model converted to TensorFlow Lite and saved to ../edge_agent/models/")
    
    return tflite_model

def test_model(model_path="supply_chain_ppo", episodes=5):
    """Test the trained model"""
    
    model = PPO.load(model_path)
    env = SupplyChainEnv()
    
    for episode in range(episodes):
        obs, _ = env.reset()
        total_reward = 0
        
        print(f"\nEpisode {episode + 1}:")
        
        for step in range(50):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            
            action_names = ["Hold", "Produce", "Ship"]
            print(f"Step {step + 1}: Action={action_names[action]}, Reward={reward:.2f}")
            
            if terminated or truncated:
                break
        
        print(f"Total Reward: {total_reward:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Supply Chain RL Agent")
    parser.add_argument("--timesteps", type=int, default=10000, 
                       help="Number of training timesteps")
    parser.add_argument("--test", action="store_true", 
                       help="Test the trained model")
    parser.add_argument("--convert", action="store_true", 
                       help="Convert model to TensorFlow Lite")
    
    args = parser.parse_args()
    
    if args.test:
        test_model()
    elif args.convert:
        convert_to_tflite()
    else:
        model = train_model(args.timesteps)
        
        # Automatically convert to TFLite after training
        print("\nConverting to TensorFlow Lite...")
        convert_to_tflite()
        
        # Test the model
        print("\nTesting trained model...")
        test_model()
