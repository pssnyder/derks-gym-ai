"""
Basic Environment Test
======================

Test the most basic DerkEnv functionality to isolate the issue.
"""

import numpy as np
from gym_derk.envs import DerkEnv

def test_basic_environment():
    """Test the most basic environment functionality"""
    print("🔍 BASIC DERKING ENVIRONMENT TEST")
    print("=" * 40)
    
    print("🌍 Creating basic environment...")
    try:
        # Create the simplest possible environment
        env = DerkEnv(
            n_arenas=1,
            turbo_mode=True,
            # No custom team configs - use defaults
        )
        print("✅ Environment created successfully")
        print(f"   Action space: {env.action_space}")
        print(f"   Number of agents: {env.n_agents}")
    except Exception as e:
        print(f"❌ Environment creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🔄 Testing environment reset...")
    try:
        observation_n = env.reset()
        
        if observation_n is None:
            print("❌ Environment reset returned None")
            env.close()
            return False
        
        print(f"✅ Environment reset successful")
        print(f"   Observations type: {type(observation_n)}")
        print(f"   Observations length: {len(observation_n)}")
        if len(observation_n) > 0:
            print(f"   First observation shape: {np.array(observation_n[0]).shape}")
        
    except Exception as e:
        print(f"❌ Environment reset failed: {e}")
        import traceback
        traceback.print_exc()
        env.close()
        return False
    
    print("\n🎮 Testing random actions...")
    try:
        # Test with random actions for a few steps
        for step in range(5):
            # Generate random actions for all agents
            actions = []
            for i in range(env.n_agents):
                action = env.action_space.sample()
                actions.append(action)
            
            # Step the environment
            observation_n, reward_n, done_n, info = env.step(np.array(actions))
            
            print(f"   Step {step}: rewards = {np.sum(reward_n):.3f}, done = {any(done_n)}")
            
            if all(done_n):
                print(f"   Episode ended early at step {step}")
                break
                
    except Exception as e:
        print(f"❌ Environment step failed: {e}")
        import traceback
        traceback.print_exc()
        env.close()
        return False
    
    print("\n🏁 Closing environment...")
    try:
        env.close()
        print("✅ Environment closed successfully")
    except Exception as e:
        print(f"❌ Environment close failed: {e}")
    
    print("\n✅ Basic environment test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_basic_environment()
    if success:
        print("\n🎉 Environment is working! Ready for brain testing.")
    else:
        print("\n💥 Environment has issues. Need to investigate further.")
