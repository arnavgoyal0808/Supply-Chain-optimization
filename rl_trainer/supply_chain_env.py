import gymnasium as gym
from gymnasium import spaces
import numpy as np

class SupplyChainEnv(gym.Env):
    """
    Supply Chain Environment with 3 actions: hold/produce/ship
    
    State: [inventory_level, demand_forecast, truck_capacity, distance_to_warehouse]
    Actions: 0=hold, 1=produce, 2=ship
    """
    
    def __init__(self):
        super(SupplyChainEnv, self).__init__()
        
        # Action space: 0=hold, 1=produce, 2=ship
        self.action_space = spaces.Discrete(3)
        
        # Observation space: [inventory, demand, capacity, distance]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0]), 
            high=np.array([1000, 100, 100, 500]), 
            dtype=np.float32
        )
        
        self.reset()
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Initialize state
        self.inventory = np.random.randint(20, 80)
        self.demand = np.random.randint(10, 50)
        self.truck_capacity = np.random.randint(30, 70)
        self.distance = np.random.randint(50, 300)
        self.step_count = 0
        
        return self._get_obs(), {}
    
    def step(self, action):
        self.step_count += 1
        
        # Execute action
        reward = 0
        if action == 0:  # Hold
            reward = -1  # Small penalty for holding
        elif action == 1:  # Produce
            production = min(20, 100 - self.inventory)
            self.inventory += production
            reward = production * 0.5 - 5  # Production cost
        elif action == 2:  # Ship
            if self.inventory >= self.demand:
                shipped = min(self.demand, self.truck_capacity)
                self.inventory -= shipped
                reward = shipped * 2 - self.distance * 0.01  # Revenue minus transport cost
            else:
                reward = -10  # Penalty for insufficient inventory
        
        # Update environment
        self.demand = max(5, self.demand + np.random.randint(-5, 6))
        self.distance = max(10, self.distance + np.random.randint(-20, 21))
        
        # Check termination
        terminated = self.step_count >= 100
        truncated = False
        
        return self._get_obs(), reward, terminated, truncated, {}
    
    def _get_obs(self):
        return np.array([
            self.inventory, 
            self.demand, 
            self.truck_capacity, 
            self.distance
        ], dtype=np.float32)
    
    def render(self):
        print(f"Inventory: {self.inventory}, Demand: {self.demand}, "
              f"Capacity: {self.truck_capacity}, Distance: {self.distance}")
