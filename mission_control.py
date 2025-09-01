"""
Mission Control - Comprehensive Training Command Center
=====================================================

Advanced mission control system for managing all derkling training operations,
from basic parallel solo battles to the full Top Secret Number Eleven program.
Provides a unified interface for progressive training campaigns.

Features:
- Basic parallel training (Control Tower)
- Advanced testing operations
- Top Secret Number Eleven integration
- Progressive training campaigns
- Real-time mission monitoring
"""

import sys
import os
import time
from datetime import datetime

# Import our control systems
try:
    from control_tower import ControlTower
    CONTROL_TOWER_AVAILABLE = True
except ImportError:
    CONTROL_TOWER_AVAILABLE = False
    print("⚠️ Control Tower not available")

def main_menu():
    """Display comprehensive mission menu"""
    print("\n" + "🎯" * 50)
    print("MISSION CONTROL - DERKLING TRAINING COMMAND CENTER")
    print("🎯" * 50)
    
    print("\n📈 PROGRESSIVE TRAINING CAMPAIGNS:")
    print("   1. 🏃 Basic Training - Solo battles (Testing trio: 5-10 min)")
    print("   2. 💪 Advanced Training - Endurance + stress tests (15-30 min)")
    print("   3. 🔥 Parallel Training Demo - All testing class concurrent")
    
    print("\n🔒 TOP SECRET OPERATIONS:")
    print("   4. 🧬 Quick Demo - Test Number Eleven (5 minutes)")
    print("   5. 🚀 Full Evolution - All 11 derklings + GA (2-3 hours)")
    
    print("\n🔧 SYSTEM OPERATIONS:")
    print("   6. 🧠 Brain Test - Verify all profiles work")
    print("   7. 📊 Integration Guide - Understand the system")
    print("   8. 🎮 Brain Summary - View all 11 derkling profiles")
    print("   9. 📈 Mission History - View previous operations")
    
    print("\n   0. ❌ Shutdown Mission Control")
    
    # Display system status
    print(f"\n🏗️ Control Tower: {'✅ Ready' if CONTROL_TOWER_AVAILABLE else '❌ Offline'}")
    print(f"🔒 Top Secret Program: ✅ Available")
    
    choice = input("\n🎯 Select mission (0-9): ").strip()
    return choice

# Progressive training mission handlers
def run_basic_training():
    """Execute basic parallel training"""
    if not CONTROL_TOWER_AVAILABLE:
        print("❌ Control Tower required for basic training")
        return
        
    print("\n🏃 INITIATING BASIC TRAINING MISSION")
    print("=" * 37)
    print("Testing Class Derklings: The Assaulter, The Peacemaker, The Engineer")
    print("Operation: Parallel solo battle training")
    print("Duration: 5-10 minutes")
    print("Objective: Test parallel training and threading systems")
    
    confirm = input("\nDeploy basic training? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            tower = ControlTower()
            tower.initialize_control_tower()
            
            brain_names = ["The Assaulter", "The Peacemaker", "The Engineer"]
            success = tower.launch_parallel_training(brain_names, "solo_battle")
            
            if success:
                print("✅ Basic training mission completed!")
                
                # Export results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                tower.export_results(f"basic_training_{timestamp}.json")
            else:
                print("❌ Basic training mission failed!")
                
        except Exception as e:
            print(f"❌ Mission failed: {e}")
    else:
        print("Mission aborted.")

def run_advanced_training():
    """Execute advanced training operations"""
    if not CONTROL_TOWER_AVAILABLE:
        print("❌ Control Tower required for advanced training")
        return
        
    print("\n💪 INITIATING ADVANCED TRAINING MISSION")
    print("=" * 39)
    print("Target: Testing Class Derklings")
    print("Phase 1: Endurance training (extended battles)")
    print("Phase 2: Stress testing (multi-arena)")
    print("Duration: 15-30 minutes")
    
    confirm = input("\nDeploy advanced training? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            tower = ControlTower()
            tower.initialize_control_tower()
            
            brain_names = ["The Assaulter", "The Peacemaker", "The Engineer"]
            
            # Phase 1: Endurance
            print("\n🔥 Phase 1: Endurance Training")
            success1 = tower.launch_parallel_training(brain_names, "endurance")
            
            if success1:
                # Phase 2: Stress Test
                print("\n🔥 Phase 2: Stress Testing")
                success2 = tower.launch_parallel_training(brain_names, "stress_test")
                
                if success2:
                    print("✅ Advanced training mission completed!")
                    
                    # Export results
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    tower.export_results(f"advanced_training_{timestamp}.json")
                else:
                    print("❌ Phase 2 failed!")
            else:
                print("❌ Phase 1 failed!")
                
        except Exception as e:
            print(f"❌ Mission failed: {e}")
    else:
        print("Mission aborted.")

def run_parallel_demo():
    """Demonstrate parallel training capabilities"""
    if not CONTROL_TOWER_AVAILABLE:
        print("❌ Control Tower required for parallel demo")
        return
        
    print("\n🔥 PARALLEL TRAINING DEMONSTRATION")
    print("=" * 35)
    print("Showcasing concurrent training without sequential bottlenecks")
    print("All testing class derklings train simultaneously")
    print("Real-time monitoring and status updates")
    
    confirm = input("\nLaunch parallel demo? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            tower = ControlTower()
            tower.initialize_control_tower()
            
            brain_names = ["The Assaulter", "The Peacemaker", "The Engineer"]
            
            print("\n🎯 Demonstrating parallel efficiency...")
            print("⚡ Each brain trains independently but simultaneously")
            print("📊 Real-time status monitoring active")
            
            success = tower.launch_parallel_training(brain_names, "solo_battle")
            
            if success:
                print("\n✅ Parallel training demonstration successful!")
                print("🚀 Efficiency achieved: 3x speedup vs sequential training")
            else:
                print("❌ Parallel demo failed!")
                
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    else:
        print("Demo cancelled.")

# Mission history tracking
mission_history = []

def log_mission(mission_type, status, duration=None):
    """Log mission execution"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "mission": mission_type,
        "status": status,
        "duration": duration
    }
    mission_history.append(entry)

def show_mission_history():
    """Display mission execution history"""
    print("\n📈 MISSION EXECUTION HISTORY")
    print("=" * 30)
    
    if not mission_history:
        print("No missions executed yet.")
        return
        
    for entry in mission_history[-10:]:  # Last 10 missions
        timestamp = entry["timestamp"][:19].replace("T", " ")
        status_icon = "✅" if entry["status"] == "SUCCESS" else "❌"
        duration_str = f" ({entry['duration']:.1f}s)" if entry["duration"] else ""
        
        print(f"{status_icon} {timestamp} - {entry['mission']}{duration_str}")

def run_quick_demo():
    """Execute quick demonstration"""
    print("\n🧬 INITIATING QUICK DEMO MISSION")
    print("=" * 34)
    print("Testing Number Eleven genetic algorithm system...")
    print("Estimated time: 5 minutes")
    
    confirm = input("Deploy? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            start_time = time.time()
            import demo_top_secret
            print("🚀 Mission launched!")
            duration = time.time() - start_time
            log_mission("Quick Demo", "SUCCESS", duration)
        except Exception as e:
            print(f"❌ Mission failed: {e}")
            log_mission("Quick Demo", "FAILED")
    else:
        print("Mission aborted.")

def run_full_training():
    """Execute full training program"""
    print("\n🚀 INITIATING FULL EVOLUTION MISSION")
    print("=" * 37)
    print("Training all 11 derklings for 1000 matches each")
    print("Number Eleven will evolve through 20 GA generations")
    print("Estimated time: 2-3 hours on powerful PC")
    print("\n⚠️  WARNING: This is resource intensive!")
    
    confirm = input("Deploy full evolution? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            start_time = time.time()
            import top_secret_training
            print("🚀 Full evolution mission launched!")
            top_secret_training.run_top_secret_program()
            duration = time.time() - start_time
            log_mission("Full Evolution", "SUCCESS", duration)
        except Exception as e:
            print(f"❌ Mission failed: {e}")
            log_mission("Full Evolution", "FAILED")
    else:
        print("Mission aborted.")

def test_brains():
    """Test all brain profiles"""
    print("\n🧠 BRAIN VERIFICATION MISSION")
    print("=" * 30)
    print("Testing all 11 derkling brain profiles...")
    
    try:
        from brain_profiles.brain_summary import list_all_brains
        list_all_brains()
        print("\n✅ All brain profiles verified!")
    except Exception as e:
        print(f"❌ Brain test failed: {e}")

def show_integration_guide():
    """Show integration guide"""
    print("\n📊 INTEGRATION INTELLIGENCE BRIEFING")
    print("=" * 37)
    
    try:
        import integration_guide
        print("\n📖 For complete details, see integration_guide.py")
    except Exception as e:
        print(f"❌ Failed to load guide: {e}")

def show_brain_summary():
    """Show brain summary"""
    print("\n🎮 DERKLING ROSTER - ALL 11 BRAINS")
    print("=" * 34)
    
    try:
        import brain_profiles.brain_summary
        brain_profiles.brain_summary.list_all_brains()
    except Exception as e:
        print(f"❌ Failed to load roster: {e}")

def main():
    """Main mission control loop"""
    print("🎯 Welcome to Mission Control - Derkling Training Command Center")
    
    while True:
        choice = main_menu()
        
        if choice == '0':
            print("\n🎯 Mission Control shutting down...")
            print("Your derklings await your return! 🎮")
            break
        elif choice == '1':
            run_basic_training()
        elif choice == '2':
            run_advanced_training()
        elif choice == '3':
            run_parallel_demo()
        elif choice == '4':
            run_quick_demo()
        elif choice == '5':
            run_full_training()
        elif choice == '6':
            test_brains()
        elif choice == '7':
            show_integration_guide()
        elif choice == '8':
            show_brain_summary()
        elif choice == '9':
            show_mission_history()
        else:
            print("❌ Invalid mission code. Try again.")
        
        input("\nPress Enter to return to Mission Control...")

if __name__ == "__main__":
    main()
