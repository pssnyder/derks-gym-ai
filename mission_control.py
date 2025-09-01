"""
Top Secret Training - Mission Control
====================================

This is your command center for the Top Secret Training program.
Choose your mission and deploy your derklings!
"""

import sys
import os
import time

def main_menu():
    """Display main mission menu"""
    print("\n" + "🔬" * 50)
    print("TOP SECRET TRAINING - MISSION CONTROL")
    print("🔬" * 50)
    
    print("\n🎯 AVAILABLE MISSIONS:")
    print("   1. 🧬 Quick Demo - Test Number Eleven (5 minutes)")
    print("   2. 🚀 Full Training - All 11 derklings (2-3 hours)")
    print("   3. 🧠 Brain Test - Verify all profiles work")
    print("   4. 📊 Integration Guide - Understand the system")
    print("   5. 🎮 Brain Summary - View all 11 derkling profiles")
    print("   6. ❌ Abort Mission")
    
    choice = input("\n🎯 Select mission (1-6): ").strip()
    return choice

def run_quick_demo():
    """Execute quick demonstration"""
    print("\n🧬 INITIATING QUICK DEMO MISSION")
    print("=" * 34)
    print("Testing Number Eleven genetic algorithm system...")
    print("Estimated time: 5 minutes")
    
    confirm = input("Deploy? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            import demo_top_secret
            print("🚀 Mission launched!")
        except Exception as e:
            print(f"❌ Mission failed: {e}")
    else:
        print("Mission aborted.")

def run_full_training():
    """Execute full training program"""
    print("\n🚀 INITIATING FULL TRAINING MISSION")
    print("=" * 37)
    print("Training all 11 derklings for 1000 matches each")
    print("Number Eleven will evolve through 20 GA generations")
    print("Estimated time: 2-3 hours on powerful PC")
    print("\n⚠️  WARNING: This is resource intensive!")
    
    confirm = input("Deploy full training? (y/n): ").strip().lower()
    if confirm == 'y':
        try:
            import top_secret_training
            print("🚀 Full mission launched!")
            top_secret_training.run_top_secret_program()
        except Exception as e:
            print(f"❌ Mission failed: {e}")
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
    print("🔬 Welcome to Top Secret Training Mission Control")
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            run_quick_demo()
        elif choice == '2':
            run_full_training()
        elif choice == '3':
            test_brains()
        elif choice == '4':
            show_integration_guide()
        elif choice == '5':
            show_brain_summary()
        elif choice == '6':
            print("\n🎯 Mission Control shutting down...")
            print("Your derklings await your return! 🎮")
            break
        else:
            print("❌ Invalid mission code. Try again.")
        
        input("\nPress Enter to return to Mission Control...")

if __name__ == "__main__":
    main()
