"""
Debug Brain Actions
==================

Check what actions our brains are producing and if they're valid for Derk Gym.
"""

import numpy as np
from gym_derk.envs import DerkEnv
from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

def debug_brain_actions():
    """Debug brain action outputs"""
    print("🔍 DEBUGGING BRAIN ACTIONS")
    print("=" * 40)
    
    # Create environment to get valid observations
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    observation_n = env.reset()
    
    print(f"Environment created with {len(observation_n)} agents")
    print(f"Observation shape: {observation_n[0].shape}")
    print(f"Action space: {env.action_space}")
    
    # Test Safe T Peanut
    print(f"\n🥜 Testing Safe T Peanut:")
    safe_t = SafeTPeanutBrain()
    
    try:
        action = safe_t.get_action(observation_n[0])
        print(f"✅ Safe T action: {action}")
        print(f"   Type: {type(action)}")
        print(f"   Length: {len(action) if hasattr(action, '__len__') else 'N/A'}")
        
        # Check if action is valid
        if isinstance(action, (tuple, list)) and len(action) == 5:
            move_x, rotate, chase_focus, cast_slot, focus_target = action
            print(f"   move_x: {move_x}")
            print(f"   rotate: {rotate}")
            print(f"   chase_focus: {chase_focus}")
            print(f"   cast_slot: {cast_slot}")
            print(f"   focus_target: {focus_target}")
        else:
            print(f"   ❌ Invalid action format!")
            
    except Exception as e:
        print(f"❌ Safe T error: {e}")
    
    # Test The Assaulter
    print(f"\n⚔️ Testing The Assaulter:")
    assaulter = TheAssaulterBrain()
    
    try:
        action = assaulter.get_action(observation_n[0])
        print(f"✅ Assaulter action: {action}")
        print(f"   Type: {type(action)}")
        print(f"   Length: {len(action) if hasattr(action, '__len__') else 'N/A'}")
        
        # Check if action is valid
        if isinstance(action, (tuple, list)) and len(action) == 5:
            move_x, rotate, chase_focus, cast_slot, focus_target = action
            print(f"   move_x: {move_x}")
            print(f"   rotate: {rotate}")
            print(f"   chase_focus: {chase_focus}")
            print(f"   cast_slot: {cast_slot}")
            print(f"   focus_target: {focus_target}")
        else:
            print(f"   ❌ Invalid action format!")
            
    except Exception as e:
        print(f"❌ Assaulter error: {e}")
    
    # Test one environment step with brain actions
    print(f"\n🎮 Testing environment step with brain actions:")
    
    try:
        actions = []
        
        # First 3 agents use Safe T Peanut
        for i in range(3):
            action = safe_t.get_action(observation_n[i])
            actions.append(action)
        
        # Last 3 agents use The Assaulter
        for i in range(3, 6):
            action = assaulter.get_action(observation_n[i])
            actions.append(action)
        
        print(f"Created {len(actions)} actions")
        
        # Convert to numpy array as expected by environment
        actions_array = np.array(actions)
        print(f"Actions array shape: {actions_array.shape}")
        
        # Step environment
        new_obs, rewards, dones, info = env.step(actions_array)
        
        print(f"✅ Environment step successful!")
        print(f"   Rewards: {rewards}")
        print(f"   Dones: {dones}")
        print(f"   New obs shape: {new_obs[0].shape}")
        
    except Exception as e:
        print(f"❌ Environment step error: {e}")
        import traceback
        traceback.print_exc()
    
    env.close()
    print(f"\n🏁 Environment closed")

def test_action_validation():
    """Test specific action formats"""
    print(f"\n🧪 TESTING ACTION FORMATS")
    print("=" * 30)
    
    # Create environment
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    observation_n = env.reset()
    
    # Test different action formats
    test_actions = [
        (0.0, 0.0, 0.0, 0, 0),           # All zeros
        (0.5, 0.2, 0.7, 1, 5),           # Valid ranges
        (1.0, 1.0, 1.0, 3, 7),           # Max values
        (-1.0, -1.0, 0.0, 0, 0),         # Negative values
    ]
    
    for i, test_action in enumerate(test_actions):
        print(f"\nTesting action {i+1}: {test_action}")
        
        try:
            # Create action array for all agents
            actions = [test_action] * 6
            actions_array = np.array(actions)
            
            # Step environment
            new_obs, rewards, dones, info = env.step(actions_array)
            print(f"✅ Success! Rewards: {rewards[:3]} vs {rewards[3:]}")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    env.close()

if __name__ == "__main__":
    debug_brain_actions()
    test_action_validation()
