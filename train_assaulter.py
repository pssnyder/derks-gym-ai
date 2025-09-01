"""
Simple Assaulter Training
========================

Basic training script for The Assaulter brain.
Uses the existing brain logic, just runs it for many episodes to collect performance data.
"""

import numpy as np
import time
import json
from datetime import datetime
from gym_derk.envs import DerkEnv

# Import The Assaulter brain
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

def train_assaulter(episodes=1000):
    """Train The Assaulter for specified episodes"""
    print("⚔️ THE ASSAULTER TRAINING")
    print("=" * 25)
    print(f"Episodes: {episodes}")
    print("=" * 25)
    
    # Initialize
    brain = TheAssaulterBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    print(f"Brain: {brain.name}")
    print(f"Agents in arena: {env.n_agents}")
    print(f"Starting training...\n")
    
    results = []
    start_time = time.time()
    
    for episode in range(episodes):
        # Reset environment
        obs_n = env.reset()
        total_reward = 0
        steps = 0
        
        while True:
            actions = []
            
            # The Assaulter controls agent 0, others are random
            for i in range(env.n_agents):
                if i == 0:
                    action = brain.get_action(obs_n[i])
                else:
                    action = env.action_space.sample()
                actions.append(action)
            
            # Step
            obs_n, rewards, dones, info = env.step(np.array(actions))
            steps += 1
            
            if all(dones):
                total_reward = env.total_reward[0]  # The Assaulter's reward
                break
        
        results.append({
            "episode": episode + 1,
            "reward": total_reward,
            "steps": steps
        })
        
        # Progress every 100 episodes
        if (episode + 1) % 100 == 0:
            recent_avg = np.mean([r["reward"] for r in results[-100:]])
            elapsed = time.time() - start_time
            print(f"Episode {episode + 1:4d} | Reward: {total_reward:6.1f} | Avg100: {recent_avg:6.1f} | Time: {elapsed:5.1f}s")
    
    env.close()
    
    # Results
    total_time = time.time() - start_time
    rewards = [r["reward"] for r in results]
    avg_reward = np.mean(rewards)
    best_reward = max(rewards)
    
    print(f"\n" + "=" * 40)
    print("TRAINING COMPLETE")
    print("=" * 40)
    print(f"Episodes: {episodes}")
    print(f"Time: {total_time:.1f}s ({total_time/60:.1f} min)")
    print(f"Average Reward: {avg_reward:.2f}")
    print(f"Best Reward: {best_reward:.2f}")
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"assaulter_results_{timestamp}.json"
    
    data = {
        "brain": brain.name,
        "episodes": episodes,
        "total_time": total_time,
        "avg_reward": avg_reward,
        "best_reward": best_reward,
        "results": results
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Results saved: {filename}")
    print("⚔️ Training complete!")
    
    return data

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        episodes = int(sys.argv[1])
    else:
        episodes = 1000
    
    print("The Assaulter Training")
    print(f"Will train for {episodes} episodes")
    
    confirm = input("Continue? (y/n): ")
    if confirm.lower() == 'y':
        train_assaulter(episodes)
    else:
        print("Cancelled.")
