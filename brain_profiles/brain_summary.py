"""
Derkling Brain Profiles Summary
=============================

This file provides an overview of all the extracted and converted derkling brains
from your Steam game configuration into Derk Gym RL environment.

COMPLETED BRAIN PROFILES:
========================

PEANUT CLASS:
-------------
1. Spicy Peanut - Aggressive duo fighter
   - File: brain_profiles/peanut_class/spicy_peanut.py
   - Strategy: Aggressive engagement, duo coordination, balanced risk
   - Bonded pair: Safe T Peanut

2. Nightrider Peanut - Kill-focused balanced fighter  
   - File: brain_profiles/peanut_class/nightrider_peanut.py
   - Strategy: Kill priority, balanced approach, moderate aggression
   - Bounties: Equal kills (90 each), high territory (90), balanced damage

3. Angrrry Peanut - Hyper-aggressive berserker
   - File: brain_profiles/peanut_class/angrrry_peanut.py
   - Strategy: Maximum aggression, kill obsessed, territory domination
   - Bounties: Maximum kills (200 each), territory (100), minimal damage concern

4. Poonut - Conservative support fighter
   - File: brain_profiles/peanut_class/poonut.py
   - Strategy: Damage-focused, extremely defensive, peanut gang support
   - Bounties: High damage (90 each), low kills (10), extreme damage avoidance

5. Safe T Peanut - Defensive team fighter
   - File: brain_profiles/peanut_class/safe_t_peanut.py
   - Strategy: Conservative team fighter, survivability, statue protection
   - Bonded pair: Spicy Peanut

LONE WOLF CLASS:
---------------
6. Clint Eastwood - Lone wolf ranged fighter
   - File: brain_profiles/lone_wolf_class/clint_eastwood.py
   - Strategy: Solo operations, ranged combat, damage-over-kills
   - Bounties: High damage focus (80-81), territory control (70), high damage avoidance

TESTING CLASS:
--------------
7. The Assaulter - Pure aggression assault fighter
   - File: brain_profiles/testing_class/the_assaulter.py
   - Strategy: Kill-focused assault, territory domination, high aggression
   - Bounties: Equal high kills (100 each), moderate damage, acceptable risk

8. The Engineer - Defensive support specialist
   - File: brain_profiles/testing_class/the_engineer.py
   - Strategy: Statue-focused defense, team support, selective engagement
   - Bounties: Highest statue kills (110), moderate unit kills (60), conservative

9. The Peacemaker - Balanced control specialist
   - File: brain_profiles/testing_class/the_peacemaker.py
   - Strategy: Balanced approach, team coordination, equal priorities
   - Bounties: Equal balanced kills (75 each), moderate territory, team focus

SPECIAL CLASS:
--------------
10. Frank - Special operations specialist
   - File: brain_profiles/special/frank.py
   - Strategy: Damage-focused operations, territory infiltration, high survivability
   - Bounties: High damage focus (68-70), low kills (30-40), territory control

11. Number Eleven - Genetic algorithm evolution derkling
   - File: brain_profiles/special/number_eleven.py
   - Strategy: Dynamic reward function evolution through genetic algorithms
   - Bounties: Self-optimizing through GA (starts at all zeros)

STILL TO CREATE:
===============
None - All profiles complete including GA evolution system!

BRAIN COMPATIBILITY MATRIX:
==========================

Peanut Class (All Compatible):
- Spicy Peanut ↔ Safe T Peanut (bonded pair)
- Nightrider Peanut ↔ Angrrry Peanut ↔ Poonut
- Strategy: Gang coordination, role specialization within team

Lone Wolf Class:
- Clint Eastwood: Solo operations, minimal team interaction

Testing Class:
- The Assaulter, The Engineer, The Peacemaker: Experimental combinations

Special Class:
- Frank: Unique operations, specialized role

USAGE INSTRUCTIONS:
==================

1. Individual Testing:
   ```python
   from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain
   brain = SpicyPeanutBrain()
   results = test_spicy_peanut()
   ```

2. Team Composition:
   ```python
   # Peanut Gang Team
   team = [SpicyPeanutBrain(), NightriderPeanutBrain(), AngrrryPeanutBrain()]
   
   # Mixed Specialist Team  
   team = [ClintEastwoodBrain(), TheEngineerBrain(), FrankBrain()]
   ```

3. Configuration Export:
   ```python
   brain = SpicyPeanutBrain()
   config = brain.get_derk_gym_config()
   # Use config in Derk Gym environment setup
   ```

STRATEGIC NOTES:
===============

High Aggression Brains:
- Angrrry Peanut (1.0 aggression, 200 kill bounties)
- The Assaulter (1.0 aggression, 100 kill bounties)  
- Spicy Peanut (0.8 aggression, 50 kill bounties)

Defensive/Support Brains:
- Poonut (0.3 aggression, 90 damage focus, -100 damage penalty)
- The Engineer (0.4 aggression, 110 statue focus, team support)
- The Peacemaker (0.6 aggression, balanced approach)

Specialist Operations:
- Clint Eastwood (lone wolf, ranged specialist)
- Frank (special ops, territory infiltration)

Team Players:
- All Peanut Class (0.8-0.95 team focus)
- The Engineer (0.9 team focus)
- The Peacemaker (0.8 team focus)

Each brain file includes:
- Complete bounty configuration from Steam screenshots
- Behavioral trait analysis
- Strategic decision-making logic
- Derk Gym environment configuration
- Individual test harness
- Compatibility information
"""

def list_all_brains():
    """List all available brain profiles"""
    brains = {
        "peanut_class": [
            "Spicy Peanut - Aggressive duo fighter",
            "Safe T Peanut - Defensive team fighter",
            "Nightrider Peanut - Kill-focused balanced fighter", 
            "Angrrry Peanut - Hyper-aggressive berserker",
            "Poonut - Conservative support fighter"
        ],
        "lone_wolf_class": [
            "Clint Eastwood - Lone wolf ranged fighter"
        ],
        "testing_class": [
            "The Assaulter - Pure aggression assault fighter",
            "The Engineer - Defensive support specialist", 
            "The Peacemaker - Balanced control specialist"
        ],
        "special": [
            "Frank - Special operations specialist",
            "Number Eleven - Genetic algorithm evolution derkling"
        ]
    }
    
    print("🧠 AVAILABLE DERKLING BRAIN PROFILES")
    print("=" * 37)
    
    total_brains = 0
    for class_name, brain_list in brains.items():
        print(f"\n{class_name.upper().replace('_', ' ')}:")
        print("-" * (len(class_name) + 1))
        for brain in brain_list:
            print(f"  • {brain}")
            total_brains += 1
    
    print(f"\nTotal Profiles Created: {total_brains}")
    print("\nEach profile includes:")
    print("  • Extracted Steam bounty configuration")  
    print("  • Behavioral trait analysis")
    print("  • Strategic decision-making logic")
    print("  • Derk Gym environment setup")
    print("  • Individual test harness")
    
    return brains

if __name__ == "__main__":
    list_all_brains()
