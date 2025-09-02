"""
Updated Nightrider Peanut - Balanced Ranged Fighter
=================================================

Fixed configuration with proper equipment and balanced bounties.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class NightriderPeanutBrain:
    """
    Nightrider Peanut - Balanced ranged fighter (UPDATED)
    
    Improved Configuration:
    - Equipment: Magnum (ranged), HealingTail (sustain), FocusingOrb (accuracy)
    - Balanced bounties (reduced from extracted values)
    - Ranged hit-and-run strategy
    """
    
    def __init__(self):
        self.name = "Nightrider Peanut"
        self.brain_class = "peanut" 
        self.role = "ranged_fighter"
        self.compatible_with = "all_peanut_class"
        
        # Behavioral traits - Balanced ranged fighter
        self.aggression = 0.7           # Moderate aggression
        self.team_focus = 0.2           # Slightly individualistic
        self.risk_tolerance = 0.6       # Ranged allows safer play
        self.territory_preference = "defensive"
        self.kill_focus = 0.8           # High but not maximum
        
        # Equipment - Ranged specialist build
        self.preferred_equipment = {
            "arms": "Magnum",          # High-damage ranged weapon
            "tail": "HealingTail",     # Sustain for longer fights
            "misc": "FocusingOrb"      # Accuracy bonus for ranged
        }
        
    def get_action(self, observation):
        """
        Nightrider decision making - ranged hit-and-run tactics
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
        else:
            closest_enemy = 999
        
        # Team positioning
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value],
            obs[ObservationKeys.Friend2Distance.value]
        ]
        
        # Weapon status
        has_ranged = any([
            obs[ObservationKeys.HasMagnum.value],
            obs[ObservationKeys.HasPistol.value],
            obs[ObservationKeys.HasBlaster.value]
        ])
        has_melee = any([
            obs[ObservationKeys.HasTalons.value],
            obs[ObservationKeys.HasBloodClaws.value]
        ])
        
        return self._ranged_fighter_strategy(
            self_hp, closest_enemy, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _ranged_fighter_strategy(self, hp, closest_enemy, has_focus, focus_hp,
                               friend_distances, has_ranged, has_melee):
        """
        Ranged hit-and-run strategy with proper spacing
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        optimal_range = 25  # Optimal range for Magnum
        
        # RANGED FIGHTER STRATEGY
        
        # 1. Optimal range maintenance
        if closest_enemy < 40:
            if closest_enemy > optimal_range + 5:
                # Too far - close gap
                move_x = 0.5
                chase_focus = 0.7
                focus_target = 5
            elif closest_enemy < optimal_range - 5:
                # Too close - back off while shooting
                move_x = -0.4
                chase_focus = 0.3
                focus_target = 5
            else:
                # Perfect range - maintain distance and shoot
                chase_focus = 0.8
                focus_target = 5
                
            # Use ranged weapons when available
            if has_ranged:
                cast_slot = 2  # Ranged weapon
            elif closest_enemy < 12 and has_melee:
                cast_slot = 1  # Emergency melee
                
        # 2. Finish low-health targets
        if has_focus and focus_hp < 30:
            chase_focus = 1.0
            if closest_enemy < 15:
                move_x = 0.3  # Controlled approach
            if has_ranged:
                cast_slot = 2
                
        # 3. Team coordination
        if len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            if closest_friend > 40:
                # Too far from team - reposition
                move_x = 0.3
                focus_target = 2
            elif closest_friend < 8:
                # Too close - spread out for better firing lanes
                move_x = 0.2
                
        # 4. Health management
        if health_ratio < 0.4:
            # Low health - play more defensively
            if closest_enemy < 20:
                move_x = -0.6  # Retreat
                focus_target = 2  # Toward friendlies
            # Use healing if available
            if health_ratio < 0.25:
                cast_slot = 3  # Healing ability
                
        # 5. Positioning and movement
        if closest_enemy > 50:
            # No immediate threats - reposition strategically
            move_x = 0.3
            rotate = 0.1
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return improved Derk Gym configuration"""
        return {
            "slots": ["Magnum", "HealingTail", "FocusingOrb"],
            "rewardFunction": {
                "damageEnemyStatue": 0.5,       # Moderate statue damage
                "damageEnemyUnit": 1.0,         # Good unit damage
                "killEnemyStatue": 2.0,         # Reduced from 9.0
                "killEnemyUnit": 3.0,           # Reduced from 10.0
                "damageTaken": -0.3,            # Slightly higher penalty
                "healEnemy": -0.5,              # Penalty for healing enemies
                "fallDamageTaken": -1.0,        # Avoid fall damage
                "teamSpirit": 0.2,              # Slightly more team-oriented
                "timeScaling": 0.0              # No time pressure
            },
            "primaryColor": "#4B0082",          # Indigo
            "secondaryColor": "#000000"         # Black
        }

def test_nightrider():
    """Test updated Nightrider Peanut brain"""
    print("🌙 TESTING UPDATED NIGHTRIDER PEANUT")
    print("=" * 40)
    
    brain = NightriderPeanutBrain()
    config = brain.get_derk_gym_config()
    
    print(f"Equipment: {config['slots']}")
    print(f"Strategy: Ranged hit-and-run fighter")
    print(f"Kill bounty: {config['rewardFunction']['killEnemyUnit']} (reduced from 10.0)")
    print(f"Team spirit: {config['rewardFunction']['teamSpirit']}")
    
    return brain

if __name__ == "__main__":
    test_nightrider()
