"""
Quick Setup and Migration Guide
===============================
"""

print("""
🎮 STEAM TO DERK GYM BRAIN MIGRATION GUIDE
==========================================

Unfortunately, you cannot directly extract and import "brains" from the Steam 
version of Dr.K's game into Derk Gym because they use completely different systems.

HOWEVER, you CAN recreate your successful strategies! Here's how:

📋 STEP 1: Document Your Steam Strategies
-----------------------------------------
Think about your best performing "brains" from Steam and answer:
• How aggressive were they? (1-10)
• Did they prefer melee or ranged combat?
• Did they stick with the team or go solo?
• When did they retreat vs fight?
• What was their target priority?

📁 STEP 2: Use the Migration Tool
---------------------------------
Run: python steam_brain_migrator.py

This tool will:
• Create a config file for your strategies
• Let you test different approaches
• Help you fine-tune the behaviors

🚀 STEP 3: Train RL Agents
--------------------------
Once you have working rule-based versions of your Steam brains:
• Use them as starting points for RL training
• The RL agents will learn and improve upon your strategies
• You'll end up with better-than-Steam performance!

💡 EXAMPLE WORKFLOW:
-------------------
1. "My Steam brain was very aggressive, always charged enemies with melee weapons"
   → Configure: aggression=0.9, weapon_preference="melee", preferred_range="close"

2. "My defensive brain stayed back, protected teammates, used ranged weapons"  
   → Configure: aggression=0.3, team_focus=0.8, weapon_preference="ranged"

3. Test these configurations against each other
4. Use the best ones as starting points for RL training

🎯 WHAT YOU'LL ACHIEVE:
----------------------
• Recreate your Steam game strategies in Derk Gym
• Improve them through machine learning
• Have AI agents that play like your best Steam brains, but better!

Ready to start? Run: python steam_brain_migrator.py
""")

# Quick test to make sure everything is working
if __name__ == "__main__":
    try:
        from gym_derk.envs import DerkEnv
        print("✅ Derk Gym is properly installed!")
        
        # Test basic functionality
        env = DerkEnv(n_arenas=1)
        obs = env.reset()
        env.close()
        print("✅ Environment test successful!")
        
        print("\n🚀 You're ready to start migrating your Steam brains!")
        print("Run: python steam_brain_migrator.py")
        
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("Please install gym-derk: pip install gym-derk")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
        print("There might be an issue with your setup, but the migration tool should still work.")
