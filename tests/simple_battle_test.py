"""
Simple Derkling Battle Test
===========================

A minimal test to verify our brain configurations work with DerkEnv.
"""

import numpy as np
from gym_derk.envs import DerkEnv
from brain_profiles.peanut_class.nightrider_peanut import NightriderPeanutBrain
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

def test_simple_battle():
    """Test a simple battle between our brains"""
    print("🔍 SIMPLE DERKLING BATTLE TEST")
    print("=" * 35)
    
    # Create brain instances
    nightrider = NightriderPeanutBrain()
    assaulter = TheAssaulterBrain()
    
    print(f"🌙 Home: {nightrider.name}")
    print(f"⚔️ Away: {assaulter.name}")
    
    # Create basic environment first
    print("\n🌍 Creating environment...")
    try:
        env = DerkEnv(n_arenas=1, turbo_mode=True)
        print("✅ Environment created successfully")
        print(f"   Number of agents: {env.n_agents}")
        print(f"   Action space: {env.action_space}")
    except Exception as e:
        print(f"❌ Environment creation failed: {e}")
        return
    
    # Test environment reset
    print("\n🔄 Testing environment reset...")
    try:
        observation_n = env.reset()
        if observation_n is not None:
            print(f"✅ Environment reset successful")
            print(f"   Observations shape: {np.array(observation_n).shape}")
            print(f"   First obs length: {len(observation_n[0])}")
        else:
            print("❌ Environment reset returned None")
            env.close()
            return
    except Exception as e:
        print(f"❌ Environment reset failed: {e}")
        env.close()
        return
    
    # Test brain actions
    print("\n🧠 Testing brain actions...")
    try:
        # Test Nightrider
        nightrider_action = nightrider.get_action(observation_n[0])
        print(f"✅ Nightrider action: {nightrider_action}")
        
        # Test Assaulter  
        assaulter_action = assaulter.get_action(observation_n[0])
        print(f"✅ Assaulter action: {assaulter_action}")
    except Exception as e:
        print(f"❌ Brain action test failed: {e}")
        env.close()
        return
    
    # Run a short episode
    print(f"\n⚔️ Running short battle (50 steps)...")
    episode_rewards = {'nightrider': 0, 'assaulter': 0}
    
    try:
        for step in range(50):
            actions = []
            
            # Home team (Nightrider) - first 3 agents
            for i in range(3):
                action = nightrider.get_action(observation_n[i])
                actions.append(action)
            
            # Away team (Assaulter) - next 3 agents
            for i in range(3, 6):
                action = assaulter.get_action(observation_n[i])
                actions.append(action)
            
            # Step environment
            observation_n, reward_n, done_n, info = env.step(np.array(actions))
            
            # Track rewards
            home_reward = np.sum(reward_n[:3])
            away_reward = np.sum(reward_n[3:])
            
            episode_rewards['nightrider'] += home_reward
            episode_rewards['assaulter'] += away_reward
            
            # Print step info for first few steps and when rewards are earned
            if step < 5 or abs(home_reward) > 0.01 or abs(away_reward) > 0.01:
                print(f"  Step {step:2d}: Nightrider={home_reward:6.3f}, Assaulter={away_reward:6.3f}")
            
            if all(done_n):
                print(f"  Episode ended at step {step}")
                break
                
    except Exception as e:
        print(f"❌ Episode execution failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Close environment
    env.close()
    print(f"\n🏁 Environment closed")
    
    # Results
    print(f"\n📊 BATTLE RESULTS:")
    print(f"   🌙 Nightrider total reward: {episode_rewards['nightrider']:.3f}")
    print(f"   ⚔️ Assaulter total reward: {episode_rewards['assaulter']:.3f}")
    
    if episode_rewards['nightrider'] > episode_rewards['assaulter']:
        print(f"   🏆 Winner: Nightrider Peanut!")
    elif episode_rewards['assaulter'] > episode_rewards['nightrider']:
        print(f"   🏆 Winner: The Assaulter!")
    else:
        print(f"   🤝 Tie!")
        
    print(f"\n✅ Basic battle test complete!")
    return episode_rewards

def test_brain_configs():
    """Test that brain configurations are working"""
    print(f"\n🔧 TESTING BRAIN CONFIGURATIONS")
    print("=" * 35)
    
    # Create brain instances
    nightrider = NightriderPeanutBrain()
    assaulter = TheAssaulterBrain()
    
    # Test Nightrider config
    print(f"🌙 Nightrider Peanut Config:")
    try:
        config = nightrider.get_derk_gym_config()
        print(f"   ✅ Equipment: {config['slots']}")
        print(f"   ✅ Colors: {config['primaryColor']} / {config['secondaryColor']}")
        print(f"   ✅ Kill reward: {config['rewardFunction']['killEnemyUnit']}")
        print(f"   ✅ Team spirit: {config['rewardFunction']['teamSpirit']}")
    except Exception as e:
        print(f"   ❌ Config failed: {e}")
    
    # Test Assaulter config  
    print(f"\n⚔️ The Assaulter Config:")
    try:
        config = assaulter.get_derk_gym_config()
        print(f"   ✅ Equipment: {config['slots']}")
        print(f"   ✅ Colors: {config['primaryColor']} / {config['secondaryColor']}")
        print(f"   ✅ Kill reward: {config['rewardFunction']['killEnemyUnit']}")
        print(f"   ✅ Team spirit: {config['rewardFunction']['teamSpirit']}")
    except Exception as e:
        print(f"   ❌ Config failed: {e}")

if __name__ == "__main__":
    test_brain_configs()
    test_simple_battle()
