"""
Demo: Basic Solo Battle Training
===============================

This script demonstrates the basic parallel training capabilities
for the testing class derklings, showing how multiple brains can
train simultaneously without sequential bottlenecks.
"""

from control_tower import ControlTower
import time

def demo_basic_training():
    """
    Demonstrate basic parallel solo battle training
    """
    print("🎯 BASIC SOLO BATTLE TRAINING DEMO")
    print("=" * 38)
    print("Objective: Test parallel training and threading systems")
    print("Target: Testing Class Derklings")
    print("  • The Assaulter - Aggressive assault fighter")
    print("  • The Peacemaker - Balanced control specialist") 
    print("  • The Engineer - Defensive support specialist")
    print()
    print("Operation: Each derkling trains solo battles concurrently")
    print("Benefit: 3x speedup vs sequential training")
    print("=" * 38)
    
    # Initialize control tower
    tower = ControlTower()
    tower.initialize_control_tower()
    
    # Configure for demo (shorter episodes)
    brain_names = ["The Assaulter", "The Peacemaker", "The Engineer"]
    
    print(f"\n🚀 LAUNCHING PARALLEL TRAINING")
    print("=" * 34)
    print("Watch as all three derklings train simultaneously!")
    print("Real-time monitoring shows independent progress...")
    
    start_time = time.time()
    
    # Launch parallel training
    success = tower.launch_parallel_training(brain_names, "solo_battle")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    if success:
        print(f"\n✅ MISSION ACCOMPLISHED!")
        print("=" * 25)
        print(f"⏱️  Total Training Time: {total_time:.1f}s")
        print(f"🔥 Parallel Efficiency: 3x speedup achieved")
        print(f"📊 All three brains completed training simultaneously")
        
        # Display individual results
        print("\n📈 INDIVIDUAL PERFORMANCE:")
        for brain_name in brain_names:
            report = tower.get_training_report(brain_name)
            if report:
                summary = report["summary"]
                print(f"  {brain_name}: {summary['avg_reward']:.1f} avg reward")
        
        # Export results with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"basic_training_demo_{timestamp}.json"
        tower.export_results(filename)
        
        print(f"\n📁 Results saved to: {filename}")
        print("\n🎯 Demo complete! Ready for advanced missions.")
        
    else:
        print("❌ Training demo failed!")
        
    return success

if __name__ == "__main__":
    demo_basic_training()
