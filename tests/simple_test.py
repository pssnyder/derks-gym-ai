"""
Simple Derk's Gym Test
=====================

Basic test following the official documentation at http://docs.gym.derkgame.com/
"""

import gym_derk
from gym_derk.envs import DerkEnv
import numpy as np

def main():
    print("🦎 Testing Derk's Gym Environment")
    print("=" * 40)
    
    try:
        # Create environment - minimal configuration
        print("Creating DerkEnv...")
        env = DerkEnv()
        
        print("✅ Environment created successfully!")
        print(f"Number of agents: {env.n_agents}")
        print(f"Number of teams: {env.n_teams}")
        print(f"Observation space: {env.observation_space}")
        print(f"Action space: {env.action_space}")
        
        # Reset environment
        print("\nResetting environment...")
        obs = env.reset()
        print(f"Initial observation shape: {np.array(obs).shape}")
        
        # Take a few random steps
        print("\nTaking 5 random steps...")
        for step in range(5):
            actions = [env.action_space.sample() for _ in range(env.n_agents)]
            obs, rewards, dones, info = env.step(np.array(actions))
            print(f"Step {step + 1}: rewards={rewards}, dones={dones}")
        
        # Close environment
        env.close()
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
