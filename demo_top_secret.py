"""
Top Secret Training - Quick Demo
===============================

This demonstrates the Number Eleven genetic algorithm system with a
smaller scale test to verify everything works before running the full
1000-match training program.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain_profiles.special.number_eleven import NumberElevenBrain
from top_secret_training import TopSecretTraining

def quick_demo():
    """Run a quick demonstration of the Top Secret Training system"""
    print("🔬 TOP SECRET TRAINING - QUICK DEMO")
    print("=" * 37)
    
    print("Testing Number Eleven genetic algorithm...")
    
    # Create Number Eleven
    eleven = NumberElevenBrain()
    
    # Create a simplified training setup
    trainer = TopSecretTraining(max_workers=2)
    trainer.matches_per_brain = 10  # Reduced for demo
    trainer.ga_generations = 3      # Reduced for demo
    trainer.matches_per_ga_evaluation = 5  # Reduced for demo
    
    print(f"Demo Parameters:")
    print(f"  Matches per brain: {trainer.matches_per_brain}")
    print(f"  GA generations: {trainer.ga_generations}")
    print(f"  Matches per GA eval: {trainer.matches_per_ga_evaluation}")
    
    # Load a few brains for testing
    try:
        steam_brains = trainer.load_steam_brains()[:3]  # Just first 3 for demo
        print(f"Loaded {len(steam_brains)} brains for demo")
        
        if len(steam_brains) == 0:
            print("No brains loaded, creating dummy opponents...")
            steam_brains = [NumberElevenBrain() for _ in range(2)]
        
    except Exception as e:
        print(f"Error loading brains: {e}")
        print("Creating dummy opponents...")
        steam_brains = [NumberElevenBrain() for _ in range(2)]
    
    # Test Number Eleven evolution
    print(f"\n🧬 Testing Number Eleven evolution...")
    
    try:
        # Show initial state
        print(f"Initial population size: {len(eleven.population)}")
        print(f"Initial reward function (should be mostly zeros):")
        initial_config = eleven.get_current_derk_config()["rewardFunction"]
        for reward, value in initial_config.items():
            if abs(value) > 0.01:
                print(f"  {reward}: {value:.3f}")
            else:
                print(f"  {reward}: 0.000")
        
        # Run a few GA generations
        print(f"\n🧬 Running {trainer.ga_generations} GA generations...")
        evolution_results = trainer.evolve_number_eleven(steam_brains)
        
        # Show final state
        print(f"\nFinal best reward function:")
        if eleven.best_chromosome:
            final_config = eleven.best_chromosome.to_derk_config()
            for reward, value in final_config.items():
                if abs(value) > 0.01:
                    print(f"  {reward}: {value:.3f}")
        
        print(f"\n✅ Evolution test complete!")
        print(f"Best fitness achieved: {evolution_results[-1].best_fitness:.3f}")
        
    except Exception as e:
        print(f"❌ Evolution test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎉 Quick demo complete!")
    print(f"\nTo run full training program:")
    print(f"  python top_secret_training.py")

def test_brain_loading():
    """Test loading of individual brain profiles"""
    print("🧠 TESTING BRAIN LOADING")
    print("=" * 25)
    
    brain_tests = [
        ("brain_profiles.peanut_class.spicy_peanut", "SpicyPeanutBrain"),
        ("brain_profiles.peanut_class.angrrry_peanut", "AngrrryPeanutBrain"),
        ("brain_profiles.special.number_eleven", "NumberElevenBrain")
    ]
    
    for module_path, class_name in brain_tests:
        try:
            module = __import__(module_path, fromlist=[class_name])
            brain_class = getattr(module, class_name)
            brain = brain_class()
            
            print(f"✅ {brain.name}")
            print(f"   Class: {brain.brain_class}")
            print(f"   Role: {brain.role}")
            
            # Test get_action method
            dummy_obs = [0.0] * 50  # Dummy observation
            action = brain.get_action(dummy_obs)
            print(f"   Action test: {action[:2]}... ✅")
            
        except Exception as e:
            print(f"❌ {class_name}: {e}")

if __name__ == "__main__":
    test_brain_loading()
    print()
    quick_demo()
