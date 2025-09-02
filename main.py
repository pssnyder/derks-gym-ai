"""
Derk's Gym AI - Steam Battle Arena
==================================

A Steam-style persistent derkling training and battle system.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.steam_battle_arena import WorkingSteamBattleArena
from src.brain_profiles.peanut_class.nightrider_peanut import NightriderPeanutBrain
from src.brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

def main():
    """Main entry point for the Steam Battle Arena"""
    print("🌙 DERK'S GYM AI - STEAM BATTLE ARENA")
    print("=====================================")
    print("Steam-style persistent derkling training system")
    print()
    
    # Create battle arena with our brain classes
    arena = WorkingSteamBattleArena(NightriderPeanutBrain, TheAssaulterBrain)
    
    # Run battle with extended episodes for better combat
    results = arena.run_battle(max_episodes=5, max_steps_per_episode=1000)
    
    print(f"\n✅ Battle complete!")
    print(f"🎯 Ready for iterative training and strategy refinement")

if __name__ == "__main__":
    main()
