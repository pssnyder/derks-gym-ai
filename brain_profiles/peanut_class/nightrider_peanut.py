"""
Nightrider Peanut - Midlevel Balanced Fighter  
============================================
Class: Peanut Class Derkling
Role: Midlevel attacking and balanced, solo/secondary duo fighter
Compatible: All peanut class fighters

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class NightriderPeanutBrain:
    """
    Nightrider Peanut - Balanced midlevel fighter
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 50 per hitpoint
    - Damage enemy unit: 100 per hitpoint  
    - Kill enemy statue: 90 points
    - Kill enemy unit: 1000 points (!!)
    - Damage taken: -20 per hitpoint
    - Heal enemy: -90 per hitpoint
    - Take fall damage: -100 per hitpoint
    - Manual bonus: 1000 points
    - Victory: 100 points
    - Loss: -100 points
    - Time scaling: 0%
    
    Strategy: EXTREMELY unit-kill focused, lower damage penalties
    """
    
    def __init__(self):
        self.name = "Nightrider Peanut"
        self.brain_class = "peanut" 
        self.role = "midlevel_balanced"
        self.compatible_with = "all_peanut_class"
        
        # Behavioral traits - VERY kill focused
        self.aggression = 0.95          # Extremely high due to 1000 kill bounty
        self.team_focus = 0.15          # Low team support
        self.risk_tolerance = 0.85      # Lower damage penalty = higher risk tolerance
        self.territory_preference = "neutral"
        self.kill_focus = 1.0           # Maximum kill focus
        
        # Equipment (to be confirmed)
        self.preferred_equipment = {
            "arms": "Unknown",     # Likely high-damage weapon
            "tail": "Unknown",     # Combat enhancement
            "misc": "Unknown"      # Mobility for hit-and-run
        }
        
    def get_action(self, observation):
        """
        Nightrider decision making - hunt and eliminate enemies
        """
        obs = observation
        
        # Key observations
        self_hp = obs[ObservationKeys.Hitpoints.value]
        has_focus = obs[ObservationKeys.HasFocus.value]
        focus_hp = obs[ObservationKeys.FocusHitpoints.value] if has_focus else 0
        
        # Enemy analysis for targeting
        enemy_distances = [
            obs[ObservationKeys.Enemy1Distance.value],
            obs[ObservationKeys.Enemy2Distance.value], 
            obs[ObservationKeys.Enemy3Distance.value]
        ]
        valid_enemies = [d for d in enemy_distances if d > 0]
        
        if valid_enemies:
            closest_enemy = min(valid_enemies)
            # Find weakest/most isolated enemy if possible
            target_priority = self._analyze_enemy_threats(obs)
        else:
            closest_enemy = 999
            target_priority = "nearest"
        
        # Team positioning (compatible with all peanuts)
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value],
            obs[ObservationKeys.Friend2Distance.value]
        ]
        
        # Weapon loadout
        has_ranged = any([
            obs[ObservationKeys.HasPistol.value],
            obs[ObservationKeys.HasMagnum.value],
            obs[ObservationKeys.HasBlaster.value]
        ])
        has_melee = any([
            obs[ObservationKeys.HasTalons.value],
            obs[ObservationKeys.HasBloodClaws.value],
            obs[ObservationKeys.HasCleavers.value],
            obs[ObservationKeys.HasCripplers.value]
        ])
        
        return self._nightrider_hunt_strategy(
            self_hp, closest_enemy, target_priority, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _analyze_enemy_threats(self, obs):
        """Analyze which enemy to prioritize for maximum kill potential"""
        # Check if focused enemy is low health
        if obs[ObservationKeys.HasFocus.value]:
            focus_hp = obs[ObservationKeys.FocusHitpoints.value]
            if focus_hp < 50:  # Low health target
                return "finish_focus"
        
        # Default to nearest for now (could be enhanced with more analysis)
        return "nearest"
    
    def _nightrider_hunt_strategy(self, hp, closest_enemy, target_priority, 
                                has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Nightrider's hunt-focused strategy - prioritize kills above all
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        
        # KILL-FOCUSED STRATEGY (1000 point bounty!)
        
        # 1. Finish low-health targets (highest priority)
        if has_focus and focus_hp < 40:
            chase_focus = 1.0       # Full commitment to kill
            move_x = 0.8            # Aggressive approach
            
            # Use most effective weapon for finishing
            if closest_enemy < 15 and has_melee:
                cast_slot = 1       # Melee for close kills
            elif has_ranged:
                cast_slot = 2       # Ranged to secure kill
                
        # 2. Hunt for vulnerable enemies
        elif closest_enemy < 40:
            chase_focus = 0.9
            focus_target = 5        # Target nearest enemy
            
            # Tactical positioning for kills
            if closest_enemy > 25:
                move_x = 0.6        # Close gap
            elif closest_enemy < 10:
                move_x = -0.2       # Back off slightly for optimal range
                
            # Weapon selection for maximum lethality
            if closest_enemy < 18 and has_melee:
                cast_slot = 1
            elif closest_enemy < 35 and has_ranged:
                cast_slot = 2
                
        # 3. Positioning with other peanut fighters
        elif len(friend_distances) > 0:
            avg_friend_distance = np.mean([d for d in friend_distances if d > 0] or [30])
            
            # Maintain good formation with other peanuts
            if avg_friend_distance > 35:
                chase_focus = 0.3
                focus_target = 2    # Move toward team
            elif avg_friend_distance < 8:
                move_x = 0.2        # Create maneuvering space
                
        # 4. Health management (higher risk tolerance due to lower damage penalty)
        if health_ratio < 0.25:     # Only retreat when very low
            if closest_enemy < 20:
                move_x = -0.4
                focus_target = 2
            else:
                # Still look for kill opportunities even when hurt
                if has_ranged and closest_enemy < 40:
                    cast_slot = 2
                    
        # 5. Roaming/hunting behavior when no immediate targets
        if closest_enemy > 50:
            move_x = 0.4            # Keep moving to find targets
            rotate = 0.1            # Scan for enemies
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": list(self.preferred_equipment.values()),
            "rewardFunction": {
                "damageEnemyStatue": 0.5,    # Moderate statue damage
                "damageEnemyUnit": 1.0,      # High unit damage
                "killEnemyStatue": 9.0,      # Very high statue kills
                "killEnemyUnit": 10.0,       # MAXIMUM unit kill reward!
                "damageTaken": -0.2,         # Low damage penalty
                "healEnemy": -0.9,           # Penalty for healing enemies
                "fallDamageTaken": -1.0,     # Avoid fall damage
                "teamSpirit": 0.1,           # Low team spirit (solo fighter)
                "timeScaling": 0.0           # No time pressure
            },
            "primaryColor": "#4B0082",       # Indigo (nightrider theme)
            "secondaryColor": "#000000"      # Black
        }

def test_nightrider():
    """Test Nightrider Peanut brain"""
    print("🌙 TESTING NIGHTRIDER PEANUT BRAIN")
    print("=" * 40)
    
    brain = NightriderPeanutBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        kills = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # Nightrider
                    action = brain.get_action(observation_n[i])
                else:       # Random actions for others
                    action = env.action_space.sample()
                actions.append(action)
                
            observation_n, reward_n, done_n, info = env.step(np.array(actions))
            episode_length += 1
            
            if all(done_n):
                episode_reward = env.total_reward[0]
                break
        
        results.append(episode_reward)
        print(f"Episode {episode + 1}: Reward = {episode_reward:.2f}, Length = {episode_length}")
    
    env.close()
    
    avg_reward = np.mean(results)
    print(f"\n🌙 Nightrider Average Reward: {avg_reward:.2f}")
    print("Strategy: Maximum kill focus, hunt priority, compatible with all peanuts")
    
    return results

if __name__ == "__main__":
    test_nightrider()
