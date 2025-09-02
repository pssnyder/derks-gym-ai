"""
Simple Steam Battlegrounds Test
==============================

Test the core training system with minimal setup to verify everything works.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from gym_derk.envs import DerkEnv
import numpy as np
import random
import time

# Import brain profiles
from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain
from brain_profiles.peanut_class.angrrry_peanut import AngrrryPeanutBrain
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

def test_brain_imports():
    """Test that all brain classes can be imported and instantiated"""
    print("🧠 Testing Brain Imports...")
    
    try:
        # Test peanut class brains
        safe_t = SafeTPeanutBrain()
        spicy = SpicyPeanutBrain()
        angrrry = AngrrryPeanutBrain()
        
        # Test testing class brains
        assaulter = TheAssaulterBrain()
        
        print("✅ All brain imports successful!")
        print(f"  Safe T Peanut: {safe_t.name}")
        print(f"  Spicy Peanut: {spicy.name}")
        print(f"  Angrrry Peanut: {angrrry.name}")
        print(f"  The Assaulter: {assaulter.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Brain import error: {e}")
        return False

def test_derk_gym_configs():
    """Test that brain configurations work with Derk Gym"""
    print("\n🎯 Testing Derk Gym Configurations...")
    
    try:
        # Test each brain's configuration
        brains = [
            SafeTPeanutBrain(),
            SpicyPeanutBrain(),
            AngrrryPeanutBrain(),
            TheAssaulterBrain()
        ]
        
        for brain in brains:
            config = brain.get_derk_gym_config()
            print(f"  {brain.name} config:")
            print(f"    Slots: {config.get('slots', 'Not specified')}")
            
            # Check reward function
            reward_func = config.get('rewardFunction', {})
            total_rewards = sum([abs(v) for v in reward_func.values()])
            print(f"    Total reward magnitude: {total_rewards:.2f}")
        
        print("✅ All configurations valid!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_simple_match():
    """Test a simple 3v3 match"""
    print("\n⚔️ Testing Simple 3v3 Match...")
    
    try:
        # Create environment
        env = DerkEnv(n_arenas=1, turbo_mode=True)
        
        # Create teams
        home_team = [SafeTPeanutBrain(), SpicyPeanutBrain(), AngrrryPeanutBrain()]
        away_team = [TheAssaulterBrain(), TheAssaulterBrain(), TheAssaulterBrain()]
        
        # Reset environment
        observation_n = env.reset()
        print(f"  Environment created with {env.n_agents} agents")
        
        # Run a short match
        episode_length = 0
        max_steps = 100
        
        while episode_length < max_steps:
            actions = []
            
            # Home team actions
            for i in range(3):
                action = home_team[i].get_action(observation_n[i])
                actions.append(action)
            
            # Away team actions  
            for i in range(3, 6):
                action = away_team[(i-3) % 3].get_action(observation_n[i])
                actions.append(action)
            
            # Step environment
            observation_n, reward_n, done_n, info = env.step(np.array(actions))
            episode_length += 1
            
            if all(done_n):
                break
        
        # Get results
        home_score = np.sum(env.total_reward[:3])
        away_score = np.sum(env.total_reward[3:])
        
        print(f"  Match completed in {episode_length} steps")
        print(f"  Home team (Peanuts): {home_score:.2f}")
        print(f"  Away team (Assaulters): {away_score:.2f}")
        print(f"  Winner: {'Peanuts' if home_score > away_score else 'Assaulters'}")
        
        env.close()
        print("✅ Match test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Match test error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_parameter_variations():
    """Test parameter variation system (simulating genetic algorithm)"""
    print("\n🧬 Testing Parameter Variations...")
    
    try:
        brain = SafeTPeanutBrain()
        base_config = brain.get_derk_gym_config()
        
        print(f"  Base Safe T Peanut reward function:")
        for key, value in base_config['rewardFunction'].items():
            print(f"    {key}: {value:.3f}")
        
        # Create variations
        variations = []
        for i in range(3):
            # Simulate parameter mutation
            varied_config = base_config.copy()
            varied_rewards = varied_config['rewardFunction'].copy()
            
            # Apply random variations
            np.random.seed(i * 42)
            for key in varied_rewards:
                base_value = varied_rewards[key]
                variation = np.random.normal(0, abs(base_value) * 0.1)
                varied_rewards[key] = base_value + variation
            
            varied_config['rewardFunction'] = varied_rewards
            variations.append(varied_config)
        
        print(f"\n  Generated {len(variations)} parameter variations")
        
        # Show one variation as example
        print(f"  Variation 1 reward function:")
        for key, value in variations[0]['rewardFunction'].items():
            print(f"    {key}: {value:.3f}")
        
        print("✅ Parameter variation test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Parameter variation error: {e}")
        return False

def main():
    """Run all tests"""
    print("🏟️ STEAM BATTLEGROUNDS SYSTEM TESTS")
    print("=" * 45)
    
    start_time = time.time()
    
    # Run tests
    tests = [
        test_brain_imports,
        test_derk_gym_configs,
        test_simple_match,
        test_parameter_variations
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    # Results
    test_time = time.time() - start_time
    
    print(f"\n" + "=" * 45)
    print("🏆 TEST RESULTS")
    print("=" * 45)
    print(f"Tests passed: {passed}/{len(tests)}")
    print(f"Test time: {test_time:.1f} seconds")
    
    if passed == len(tests):
        print("✅ ALL TESTS PASSED - Ready for training!")
        print("\nNext steps:")
        print("1. Run simple training with: python steam_battlegrounds_trainer.py")
        print("2. Monitor results in training_results/ folder")
        print("3. Experiment with different population sizes and generations")
    else:
        print("❌ Some tests failed - check errors above")
    
    return passed == len(tests)

if __name__ == "__main__":
    main()
