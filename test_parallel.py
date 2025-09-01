"""
Quick test of parallel training system
"""

from control_tower import ControlTower

def test_parallel_training():
    print("🧪 QUICK PARALLEL TRAINING TEST")
    print("=" * 35)
    
    try:
        tower = ControlTower()
        tower.initialize_control_tower()
        
        brain_names = ["The Assaulter", "The Peacemaker", "The Engineer"]
        print(f"🎯 Testing parallel training with: {brain_names}")
        
        # Add a quick test configuration
        tower.training_configs["quick_test"] = {
            "episodes": 3,
            "arena_count": 1,
            "turbo_mode": True,
            "description": "Quick parallel training test"
        }
        
        success = tower.launch_parallel_training(brain_names, "quick_test")
        
        if success:
            print("✅ Parallel training test successful!")
            tower.export_results("parallel_test_results.json")
        else:
            print("❌ Parallel training test failed!")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_parallel_training()
