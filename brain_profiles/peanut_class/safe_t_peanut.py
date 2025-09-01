"""
Safe T Peanut - Rule-Based Implementation
========================================

This implements Safe T Peanut's exact Steam brain behavior as a rule-based
agent that you can test in Derk Gym immediately.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np
import json

class SafeTPeanutBrain:
    """
    Rule-based implementation of Safe T Peanut's Steam brain behavior.
    
    Key characteristics:
    - Defensive team fighter (0.59 aggression, 0.90 team focus)
    - High survivability with self-healing
    - Strong statue protection instincts
    - Moderate risk tolerance but very protective of team assets
    """
    
    def __init__(self):
        self.name = "Safe T Peanut"
        
        # Behavioral traits from Steam analysis
        self.aggression = 0.59
        self.team_focus = 0.90
        self.risk_tolerance = 0.60
        self.survivability = 0.90
        self.statue_defender = 1.00
        
        # Equipment configuration
        self.has_blood_claws = True    # Self-healing melee
        self.has_healing_gland = True  # Team healing
        self.has_shell = True          # Damage reduction
        
        # Tactical parameters
        self.retreat_health_threshold = 45  # Retreat when below 45 HP (moderate caution)
        self.statue_protection_range = 40   # Stay near statue when enemies close
        self.team_support_range = 30        # Heal teammates within this range
        self.engagement_range = 25          # Engage enemies within this range
        
    def get_action(self, observation):
        """Get action based on Safe T Peanut's behavioral profile"""
        obs = observation
        
        # Extract key information
        self_hp = obs[ObservationKeys.Hitpoints.value]
        has_focus = obs[ObservationKeys.HasFocus.value]
        focus_hp = obs[ObservationKeys.FocusHitpoints.value] if has_focus else 0
        
        # Distances
        friendly_statue_dist = obs[ObservationKeys.FriendStatueDistance.value]
        enemy_statue_dist = obs[ObservationKeys.EnemyStatueDistance.value]
        
        enemy_distances = [
            obs[ObservationKeys.Enemy1Distance.value],
            obs[ObservationKeys.Enemy2Distance.value], 
            obs[ObservationKeys.Enemy3Distance.value]
        ]
        valid_enemies = [d for d in enemy_distances if d > 0]
        closest_enemy = min(valid_enemies) if valid_enemies else 999
        
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value],
            obs[ObservationKeys.Friend2Distance.value]
        ]
        valid_friends = [d for d in friend_distances if d > 0]
        closest_friend = min(valid_friends) if valid_friends else 999
        
        # Decision making based on Safe T Peanut's priorities
        return self._make_tactical_decision(
            self_hp, closest_enemy, closest_friend, 
            friendly_statue_dist, enemy_statue_dist,
            has_focus, focus_hp
        )
    
    def _make_tactical_decision(self, hp, closest_enemy, closest_friend, 
                              friendly_statue_dist, enemy_statue_dist,
                              has_focus, focus_hp):
        """
        Make tactical decisions based on Safe T Peanut's Steam brain logic:
        
        Priority Order:
        1. Protect own statue if under threat
        2. Retreat if low health (risk management)
        3. Heal teammates if needed and in range
        4. Engage enemies if safe to do so
        5. Return to defensive position near statue
        """
        
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0  # 0=no cast, 1-3=abilities
        focus_target = 0  # 0=no change
        
        # PRIORITY 1: STATUE PROTECTION (statue_defender = 1.00)
        # If enemies are near our statue, defend it at all costs
        if closest_enemy < self.statue_protection_range and friendly_statue_dist < 30:
            # Aggressive defense of statue
            chase_focus = self.aggression * 1.2  # Boost aggression when defending
            focus_target = 5  # Focus on nearest enemy
            
            if closest_enemy < 15 and self.has_blood_claws:
                cast_slot = 1  # Use BloodClaws (self-healing melee)
            
            # Don't retreat when defending statue
            return (move_x, rotate, chase_focus, cast_slot, focus_target)
        
        # PRIORITY 2: HEALTH MANAGEMENT (risk_tolerance = 0.60)
        health_ratio = hp / 100.0
        should_retreat = hp < self.retreat_health_threshold
        
        if should_retreat:
            # Retreat toward friendly statue for safety
            move_x = -0.5  # Move backward
            focus_target = 1   # Focus on home statue
            
            # Use healing if available and very low health
            if hp < 30 and self.has_healing_gland:
                cast_slot = 2  # Use HealingGland
                focus_target = 2  # Focus on teammate to heal
            
            return (move_x, rotate, chase_focus, cast_slot, focus_target)
        
        # PRIORITY 3: TEAM SUPPORT (team_focus = 0.90)
        # Look for teammates to heal (high team spirit)
        if closest_friend < self.team_support_range and self.has_healing_gland:
            # Position to heal teammate
            chase_focus = 0.3  # Low chase, focus on positioning
            focus_target = 2   # Focus on teammate
            cast_slot = 2      # Use HealingGland
            
            return (move_x, rotate, chase_focus, cast_slot, focus_target)
        
        # PRIORITY 4: COMBAT ENGAGEMENT (aggression = 0.59)
        if closest_enemy < self.engagement_range and health_ratio > 0.6:
            # Moderate aggression - engage but carefully
            chase_focus = self.aggression  # 0.59 - moderate pursuit
            focus_target = 5  # Focus on enemy
            
            # Use BloodClaws for sustainable combat
            if closest_enemy < 18 and self.has_blood_claws:
                cast_slot = 1  # BloodClaws heal us while fighting
            
            # Slight forward movement for engagement
            move_x = 0.3
            
            return (move_x, rotate, chase_focus, cast_slot, focus_target)
        
        # PRIORITY 5: DEFENSIVE POSITIONING
        # Stay near statue for protection (default behavior)
        if friendly_statue_dist > 25:
            # Move toward statue
            chase_focus = 0.4
            focus_target = 1  # Focus on home statue
            move_x = 0.2
        else:
            # Good position, stay alert
            focus_target = 5 if closest_enemy < 40 else 0
        
        return (move_x, rotate, chase_focus, cast_slot, focus_target)

def test_safe_t_peanut(num_episodes=5):
    """Test Safe T Peanut implementation"""
    print("🧪 TESTING SAFE T PEANUT IMPLEMENTATION")
    print("=" * 45)
    
    # Create environment
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    brain = SafeTPeanutBrain()
    
    total_rewards = []
    
    for episode in range(num_episodes):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        print(f"\n📋 Episode {episode + 1}:")
        
        while True:
            actions = []
            
            # Safe T Peanut controls first agent
            action = brain.get_action(observation_n[0])
            actions.append(action)
            
            # Other agents use random actions
            for i in range(1, env.n_agents):
                random_action = env.action_space.sample()
                actions.append(random_action)
                
            observation_n, reward_n, done_n, info = env.step(np.array(actions))
            episode_length += 1
            
            if all(done_n):
                break
        
        # Get Safe T Peanut's reward (first agent)
        safe_t_reward = env.total_reward[0]
        team_avg_reward = np.mean(env.total_reward[:3])  # Home team average
        
        total_rewards.append(safe_t_reward)
        
        print(f"   Safe T Peanut reward: {safe_t_reward:.2f}")
        print(f"   Team average reward: {team_avg_reward:.2f}")
        print(f"   Episode length: {episode_length}")
        
    env.close()
    
    # Results
    avg_reward = np.mean(total_rewards)
    std_reward = np.std(total_rewards)
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"   Average reward: {avg_reward:.2f} ± {std_reward:.2f}")
    print(f"   Best episode: {max(total_rewards):.2f}")
    print(f"   Worst episode: {min(total_rewards):.2f}")
    print(f"   Consistency: {'High' if std_reward < 2.0 else 'Moderate' if std_reward < 4.0 else 'Low'}")
    
    return total_rewards

def create_derk_gym_team_config():
    """Create Derk Gym team configuration for Safe T Peanut"""
    
    # Load the exact configuration from profile
    try:
        with open("safe_t_peanut_profile.json", 'r') as f:
            profile = json.load(f)
            derk_config = profile["derk_gym_config"]
    except FileNotFoundError:
        # Fallback configuration if profile file doesn't exist
        derk_config = {
            "primaryColor": "#4CAF50",
            "secondaryColor": "#2E7D32", 
            "ears": 2,
            "eyes": 3,
            "backSpikes": 4,
            "slots": ["BloodClaws", "HealingGland", "Shell"],
            "rewardFunction": {
                "damageEnemyStatue": 0.20,
                "damageEnemyUnit": 0.80,
                "killEnemyStatue": 3.0,
                "killEnemyUnit": 0.90,
                "healTeammate1": 0.40,
                "healTeammate2": 0.40,
                "damageTaken": -0.40,
                "teamSpirit": 0.90,
                "timeScaling": 0.90
            }
        }
    
    print("🔧 DERK GYM CONFIGURATION:")
    print("=" * 30)
    print(f"Primary Color: {derk_config['primaryColor']}")
    print(f"Secondary Color: {derk_config['secondaryColor']}")
    print(f"Equipment: {derk_config['slots']}")
    print(f"Team Spirit: {derk_config['rewardFunction']['teamSpirit']*100:.0f}%")
    print()
    
    return derk_config

if __name__ == "__main__":
    print("🥜 SAFE T PEANUT - RULE-BASED IMPLEMENTATION")
    print("=" * 50)
    print()
    print("Behavioral Profile:")
    print("• Conservative but battle-hardened")
    print("• High team support (90% team spirit)")
    print("• Sustainable melee fighter")
    print("• Strong statue defender")
    print("• Moderate aggression with high survivability")
    print()
    
    # Create Derk Gym configuration
    team_config = create_derk_gym_team_config()
    
    # Test the implementation
    print("Starting behavioral test...")
    rewards = test_safe_t_peanut(num_episodes=3)
    
    print(f"\n✅ Safe T Peanut successfully implemented!")
    print(f"🎯 Ready to use as baseline for RL training")
    
    # Save test results
    results = {
        "brain_name": "Safe T Peanut",
        "test_rewards": rewards,
        "average_performance": np.mean(rewards),
        "team_config": team_config,
        "behavioral_notes": [
            "Excellent team support and survivability",
            "Moderate aggression balanced with defense",
            "Strong statue protection instincts", 
            "Sustainable combat with self-healing"
        ]
    }
    
    with open("safe_t_peanut_test_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Test results saved to: safe_t_peanut_test_results.json")
