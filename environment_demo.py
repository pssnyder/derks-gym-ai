"""
Derk Gym Environment Demo - Understanding Through Examples
=========================================================

This demonstrates core Derk Gym concepts using your actual Steam brains
so you can see how the environment works in practice.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np
import json

def demonstrate_observation_space():
    """Show what information each derkling receives"""
    print("🔍 OBSERVATION SPACE DEMONSTRATION")
    print("=" * 38)
    
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    observation_n = env.reset()
    
    # Look at what one derkling observes
    obs = observation_n[0]
    
    print("Each derkling receives this information every frame:")
    print(f"• Self Health: {obs[ObservationKeys.Hitpoints.value]:.1f}")
    print(f"• Has Focus: {bool(obs[ObservationKeys.HasFocus.value])}")
    
    print(f"\n🎯 Enemy Information:")
    print(f"• Enemy 1 Distance: {obs[ObservationKeys.Enemy1Distance.value]:.1f}")
    print(f"• Enemy 2 Distance: {obs[ObservationKeys.Enemy2Distance.value]:.1f}")
    print(f"• Enemy 3 Distance: {obs[ObservationKeys.Enemy3Distance.value]:.1f}")
    
    print(f"\n🤝 Team Information:")
    print(f"• Friend 1 Distance: {obs[ObservationKeys.Friend1Distance.value]:.1f}")
    print(f"• Friend 2 Distance: {obs[ObservationKeys.Friend2Distance.value]:.1f}")
    
    print(f"\n🏛️ Objectives:")
    print(f"• Enemy Statue Distance: {obs[ObservationKeys.EnemyStatueDistance.value]:.1f}")
    
    print(f"\n⚔️ Equipment Status:")
    print(f"• Has Talons: {bool(obs[ObservationKeys.HasTalons.value])}")
    print(f"• Has Pistol: {bool(obs[ObservationKeys.HasPistol.value])}")
    print(f"• Has Magnum: {bool(obs[ObservationKeys.HasMagnum.value])}")
    
    print(f"\n💡 WHY THIS MATTERS:")
    print(f"   Limited information = Strategic decisions")
    print(f"   Derklings can't see everything at once")
    print(f"   Must balance attention between threats and objectives")
    
    env.close()

def demonstrate_action_space():
    """Show what actions each derkling can take"""
    print("\n🎮 ACTION SPACE DEMONSTRATION")
    print("=" * 33)
    
    print("Each derkling controls 5 continuous values:")
    print("• move_x: -1.0 to 1.0 (backward to forward)")
    print("• rotate: -1.0 to 1.0 (left to right)")  
    print("• chase_focus: 0.0 to 1.0 (how aggressively to chase target)")
    print("• cast_slot: 0, 1, or 2 (which ability/weapon to use)")
    print("• focus_target: 0-5 (what to focus on)")
    
    print(f"\n🎯 Focus Targets:")
    print(f"   0 = No focus (defensive)")
    print(f"   1 = Friend 1")
    print(f"   2 = Friend 2") 
    print(f"   3 = Enemy 1")
    print(f"   4 = Enemy Statue")
    print(f"   5 = Closest Enemy")
    
    print(f"\n⚔️ Cast Slots:")
    print(f"   0 = No action")
    print(f"   1 = Melee weapon (Talons, BloodClaws, etc.)")
    print(f"   2 = Ranged weapon (Pistol, Magnum, Blaster)")
    
    print(f"\n💡 WHY THIS MATTERS:")
    print(f"   Simple controls allow complex emergent behavior")
    print(f"   Your Steam brains already use this action space")
    print(f"   RL agents can discover frame-perfect timing")

def demonstrate_reward_functions():
    """Show how different reward functions create different strategies"""
    print("\n🏆 REWARD FUNCTION DEMONSTRATION")
    print("=" * 36)
    
    # Example reward configurations from your Steam brains
    reward_examples = {
        "Angrrry Peanut (Berserker)": {
            "killEnemyUnit": 2.0,        # 200 points - MAXIMUM
            "killEnemyStatue": 2.0,      # 200 points - MAXIMUM  
            "damageEnemyUnit": 0.1,      # 10 points - minimal
            "damageTaken": -0.1,         # -10 points - don't care
            "strategy": "Pure aggression - kills everything"
        },
        "Poonut (Ultra-Defensive)": {
            "damageEnemyUnit": 0.9,      # 90 points - damage focus
            "killEnemyUnit": 0.1,        # 10 points - low kills
            "damageTaken": -1.0,         # -100 points - AVOID DAMAGE
            "teamSpirit": 0.95,          # High team support
            "strategy": "Damage dealing but extreme safety"
        },
        "The Engineer (Support)": {
            "killEnemyStatue": 1.1,      # 110 points - statue priority
            "killEnemyUnit": 0.6,        # 60 points - moderate
            "teamSpirit": 0.9,           # High team focus
            "damageTaken": -0.5,         # Moderate damage avoidance
            "strategy": "Team support with statue focus"
        },
        "Clint Eastwood (Lone Wolf)": {
            "damageEnemyUnit": 0.81,     # 81 points - damage focus
            "timeSpentAwayTerritory": 0.7, # 70 points - territory
            "teamSpirit": 0.0,           # No team interaction
            "damageTaken": -0.77,        # High damage avoidance
            "strategy": "Solo operations, ranged damage"
        }
    }
    
    for brain, config in reward_examples.items():
        print(f"\n🧠 {brain}:")
        strategy = config.pop('strategy')
        for reward, value in config.items():
            if value > 0:
                print(f"   ✅ {reward}: +{value}")
            else:
                print(f"   ❌ {reward}: {value}")
        print(f"   🎯 Result: {strategy}")
    
    print(f"\n💡 WHY THIS MATTERS:")
    print(f"   Reward function IS the strategy")
    print(f"   Change rewards = Change behavior")
    print(f"   RL agents optimize rewards perfectly")
    print(f"   Your Steam bounties already define clear strategies")

def demonstrate_training_concepts():
    """Explain training methodologies with your brains as examples"""
    print("\n🚀 TRAINING METHODOLOGY DEMONSTRATION")
    print("=" * 41)
    
    training_examples = {
        "Self-Play with Angrrry Peanut": {
            "concept": "Agent plays against copies of itself",
            "example": "Angrrry Peanut vs Angrrry Peanut",
            "evolution": [
                "Gen 1: Basic charging and attacking",
                "Gen 10: Learns to dodge while attacking", 
                "Gen 50: Discovers optimal engagement ranges",
                "Gen 100: Masters timing and positioning",
                "Gen 500: Frame-perfect micro-management"
            ],
            "why": "Each generation must counter the previous generation's tactics"
        },
        "Population Training with Peanut Gang": {
            "concept": "Multiple diverse agents train together", 
            "example": "Spicy + Safe T + Angrrry + Poonut all learning",
            "specialization": [
                "Spicy learns to coordinate with Safe T",
                "Safe T learns when to be aggressive for Spicy",
                "Angrrry learns to use others as distractions",
                "Poonut learns optimal support positioning"
            ],
            "why": "Prevents overfitting to one opponent style"
        },
        "Transfer Learning from Steam Brains": {
            "concept": "Use existing agents as teachers",
            "example": "RL agent starts by copying Clint Eastwood", 
            "progression": [
                "Phase 1: Learn to mimic Clint's behavior",
                "Phase 2: Improve on Clint's weaknesses", 
                "Phase 3: Discover new strategies",
                "Phase 4: Become better than original"
            ],
            "why": "Faster learning than starting from scratch"
        }
    }
    
    for method, details in training_examples.items():
        print(f"\n🎯 {method}:")
        print(f"   Concept: {details['concept']}")
        print(f"   Example: {details['example']}")
        
        if 'evolution' in details:
            print(f"   Evolution:")
            for stage in details['evolution']:
                print(f"     • {stage}")
        elif 'specialization' in details:
            print(f"   Specialization:")
            for spec in details['specialization']:
                print(f"     • {spec}")
        elif 'progression' in details:
            print(f"   Progression:")
            for stage in details['progression']:
                print(f"     • {stage}")
                
        print(f"   Why: {details['why']}")
    
    print(f"\n💡 YOUR STRATEGIC OPPORTUNITIES:")
    print(f"   • Evolve your favorite brains beyond their current limits")
    print(f"   • Discover optimal team compositions")  
    print(f"   • Create counters to your own strategies")
    print(f"   • Find strategies you never thought possible")

def demonstrate_practical_applications():
    """Show specific ways to leverage your Steam brains"""
    print("\n🎮 PRACTICAL APPLICATIONS FOR YOUR BRAINS")
    print("=" * 43)
    
    applications = {
        "Immediate Experiments": [
            "🥊 Steam Brain Tournament - Which brain is strongest?",
            "🤝 Peanut Gang Optimization - Perfect the team chemistry",
            "⚔️ Rock-Paper-Scissors Discovery - Which counters which?",
            "📊 Performance Analysis - Measure actual vs perceived strength"
        ],
        "Evolution Projects": [
            "🧬 Hybrid Angrrry - Keep the aggression, add intelligence",
            "🛡️ Adaptive Poonut - Learn when safety hurts the team", 
            "🎯 Super Clint - Lone wolf with perfect aim",
            "🔧 Meta Engineer - Support that adapts to team needs"
        ],
        "Discovery Missions": [
            "🔍 Anti-Peanut Specialist - Train counters to your gang",
            "🌟 Novel Strategy Hunter - Find tactics you can't program",
            "🎭 Personality Switcher - Agent that changes brain personalities",
            "🧠 Perfect Team - Discover optimal 3-derkling composition"
        ],
        "Advanced Research": [
            "📈 Meta-Learning - Agents that learn how to learn faster",
            "🎨 Strategy Artistry - Beautiful, impractical but effective tactics", 
            "🏆 Tournament Evolution - Evolving specifically to win competitions",
            "🔬 Behavioral Analysis - Understanding why strategies work"
        ]
    }
    
    for category, items in applications.items():
        print(f"\n🎯 {category}:")
        for item in items:
            print(f"   {item}")
    
    print(f"\n🚀 GETTING STARTED RECOMMENDATION:")
    print(f"   1. Start with a Steam Brain Tournament")
    print(f"   2. Pick your favorite brain for evolution")
    print(f"   3. Train an RL agent to beat your best brain")
    print(f"   4. Discover what 'perfect' versions look like!")

def main():
    """Run the complete demonstration"""
    print("🎮 DERK GYM ENVIRONMENT - WHAT & WHY DEMONSTRATION")
    print("=" * 54)
    print("Understanding the environment through your Steam brains...")
    
    demonstrate_observation_space()
    demonstrate_action_space() 
    demonstrate_reward_functions()
    demonstrate_training_concepts()
    demonstrate_practical_applications()
    
    print(f"\n🎉 CONCLUSION:")
    print(f"Your Steam brains are perfect for Derk Gym because they represent")
    print(f"proven strategies with clear behavioral patterns. RL can evolve these")
    print(f"foundations into strategies beyond human design limitations!")
    
    print(f"\n💡 The real question: Which experiment sounds most fun? 🎯")

if __name__ == "__main__":
    main()
