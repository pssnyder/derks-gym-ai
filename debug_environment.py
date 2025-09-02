"""
Debug Environment Setup
======================

Check if environment is configured correctly for our brain teams.
"""

import numpy as np
from gym_derk.envs import DerkEnv
from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

def debug_environment_setup():
    """Debug environment configuration and team setup"""
    print("🔍 DEBUGGING ENVIRONMENT SETUP")
    print("=" * 40)
    
    # Get team configurations from brains
    safe_t = SafeTPeanutBrain()
    assaulter = TheAssaulterBrain()
    
    safe_t_config = safe_t.get_derk_gym_config()
    assaulter_config = assaulter.get_derk_gym_config()
    
    print("🥜 Safe T Peanut config:")
    print(f"   Slots: {safe_t_config['slots']}")
    print(f"   Reward function keys: {list(safe_t_config['rewardFunction'].keys())}")
    print(f"   Team spirit: {safe_t_config['rewardFunction']['teamSpirit']}")
    
    print("\n⚔️ The Assaulter config:")
    print(f"   Slots: {assaulter_config['slots']}")
    print(f"   Reward function keys: {list(assaulter_config['rewardFunction'].keys())}")
    print(f"   Team spirit: {assaulter_config['rewardFunction']['teamSpirit']}")
    
    # Create environment with team configurations
    print(f"\n🏟️ Creating environment with team configs...")
    
    # Build team configs for environment
    team_config = [
        [safe_t_config, safe_t_config, safe_t_config],  # Home team (3x Safe T)
        [assaulter_config, assaulter_config, assaulter_config]  # Away team (3x Assaulter)
    ]
    
    try:
        env = DerkEnv(
            n_arenas=1,
            turbo_mode=True,
            teams=team_config
        )
        
        print("✅ Environment created successfully with team configs")
        
        # Reset and run a few steps
        observation_n = env.reset()
        print(f"   Observation shape: {observation_n[0].shape}")
        
        # Run a longer test episode
        episode_rewards = []
        total_rewards = [0.0] * 6
        
        for step in range(50):  # Run 50 steps
            actions = []
            
            # Home team actions (Safe T Peanut)
            for i in range(3):
                action = safe_t.get_action(observation_n[i])
                actions.append(action)
            
            # Away team actions (The Assaulter)
            for i in range(3, 6):
                action = assaulter.get_action(observation_n[i])
                actions.append(action)
            
            # Step environment
            observation_n, rewards, dones, info = env.step(np.array(actions))
            
            # Accumulate rewards
            for i in range(6):
                total_rewards[i] += rewards[i]
            
            episode_rewards.append(rewards.copy())
            
            # Print step info every 10 steps
            if step % 10 == 0:
                print(f"   Step {step}: Home team rewards: {rewards[:3]}, Away team rewards: {rewards[3:]}")
            
            if all(dones):
                print(f"   Episode ended at step {step}")
                break
        
        print(f"\n📊 Final Results:")
        print(f"   Home team total rewards: {total_rewards[:3]}")
        print(f"   Away team total rewards: {total_rewards[3:]}")
        print(f"   Episode length: {len(episode_rewards)}")
        
        # Check if any meaningful rewards were earned
        if any(abs(r) > 0.1 for r in total_rewards):
            print("✅ Agents are earning meaningful rewards!")
        else:
            print("❌ All rewards are near zero - possible configuration issue")
        
        env.close()
        
    except Exception as e:
        print(f"❌ Environment creation failed: {e}")
        import traceback
        traceback.print_exc()

def debug_minimal_test():
    """Run minimal test without team configs"""
    print(f"\n🧪 MINIMAL TEST (Default Environment)")
    print("=" * 40)
    
    # Create default environment
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    observation_n = env.reset()
    
    safe_t = SafeTPeanutBrain()
    
    total_rewards = [0.0] * 6
    
    # Run 30 steps with just Safe T actions
    for step in range(30):
        actions = []
        
        # All agents use Safe T actions
        for i in range(6):
            action = safe_t.get_action(observation_n[i])
            actions.append(action)
        
        observation_n, rewards, dones, info = env.step(np.array(actions))
        
        for i in range(6):
            total_rewards[i] += rewards[i]
        
        if step % 10 == 0:
            print(f"   Step {step}: Rewards: {rewards}")
        
        if all(dones):
            break
    
    print(f"\n📊 Minimal Test Results:")
    print(f"   Total rewards: {total_rewards}")
    
    env.close()

if __name__ == "__main__":
    debug_environment_setup()
    debug_minimal_test()
