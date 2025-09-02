"""
Updated The Assaulter - Complete Melee Mobility Build
===================================================

Fixed configuration with full equipment loadout and balanced bounties.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class TheAssaulterBrain:
    """
    The Assaulter - Complete melee mobility build (UPDATED)
    
    Improved Configuration:
    - Equipment: Talons (melee), IronTail (defense), HasteOrb (mobility)
    - Balanced bounties with territory focus
    - Aggressive assault with mobility strategy
    """
    
    def __init__(self):
        self.name = "The Assaulter"
        self.brain_class = "testing"
        self.role = "melee_assault"
        self.compatible_with = "unknown"
        
        # Behavioral traits - Mobile assault
        self.aggression = 0.9           # High aggression
        self.team_focus = 0.4           # Balanced team coordination
        self.risk_tolerance = 0.7       # High but not reckless
        self.territory_preference = "aggressive"
        self.kill_focus = 0.8           # High kill focus
        
        # Equipment - Complete melee mobility build
        self.preferred_equipment = {
            "arms": "Talons",          # High-damage melee
            "tail": "IronTail",        # Defensive boost
            "misc": "HasteOrb"         # Mobility for gap closing
        }
        
    def get_action(self, observation):
        """
        The Assaulter decision making - mobile melee assault
        """
        obs = observation
        
        # Key observations
        self_hp = obs[ObservationKeys.Hitpoints.value] * 100
        has_focus = obs[ObservationKeys.HasFocus.value] > 0.5
        focus_hp = obs[ObservationKeys.FocusHitpoints.value] * 100 if has_focus else 0
        
        # Enemy analysis
        enemy_distances = [
            obs[ObservationKeys.Enemy1Distance.value] * 50,
            obs[ObservationKeys.Enemy2Distance.value] * 50, 
            obs[ObservationKeys.Enemy3Distance.value] * 50
        ]
        closest_enemy = min([d for d in enemy_distances if d > 0] or [999])
        
        # Statue analysis
        enemy_statue_distance = obs[ObservationKeys.EnemyStatueDistance.value] * 50
        
        # Team coordination
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value] * 50,
            obs[ObservationKeys.Friend2Distance.value] * 50
        ]
        
        # Weapon status
        has_melee = any([
            obs[ObservationKeys.HasTalons.value],
            obs[ObservationKeys.HasBloodClaws.value],
            obs[ObservationKeys.HasCleavers.value]
        ])
        has_ranged = any([
            obs[ObservationKeys.HasPistol.value],
            obs[ObservationKeys.HasMagnum.value]
        ])
        
        return self._mobile_assault_strategy(
            self_hp, closest_enemy, enemy_statue_distance, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _mobile_assault_strategy(self, hp, closest_enemy, statue_distance,
                               has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Mobile assault strategy with improved positioning
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_low_health = health_ratio < 0.3
        
        # MOBILE ASSAULT STRATEGY
        
        # 1. Priority target elimination
        if closest_enemy < 40 and not is_low_health:
            if closest_enemy > 15:
                # Gap closing phase - use mobility
                move_x = 0.9
                chase_focus = 0.9
                focus_target = 5
                
                # Use ranged to soften while closing
                if has_ranged and closest_enemy < 30:
                    cast_slot = 2
                    
            elif closest_enemy <= 15:
                # Melee engagement range
                chase_focus = 1.0
                focus_target = 5
                
                if has_melee and closest_enemy < 8:
                    cast_slot = 1  # Melee attack
                    move_x = 0.2   # Controlled aggression
                else:
                    move_x = 0.6   # Close for melee
                    
        # 2. Finish low-health targets
        if has_focus and focus_hp < 40:
            chase_focus = 1.0
            if closest_enemy < 20:
                if has_melee:
                    cast_slot = 1
                elif has_ranged:
                    cast_slot = 2
            else:
                move_x = 0.8  # Rush to finish
                
        # 3. Statue assault when no high-priority targets
        elif statue_distance < 50 and not is_low_health:
            if statue_distance > 20:
                move_x = 0.7
                focus_target = 4  # Focus statue
            else:
                focus_target = 4
                if has_melee:
                    cast_slot = 1
                    
        # 4. Team coordination for group assaults
        if len(friend_distances) > 0 and not is_low_health:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            
            if closest_friend < 20 and closest_enemy < 30:
                # Team is close and enemies nearby - coordinated assault
                move_x = 0.8
                chase_focus = 0.8
                focus_target = 5
                
            elif closest_friend > 35:
                # Too far from team - regroup
                move_x = 0.5
                focus_target = 2
                
        # 5. Territory control (bonus for enemy territory)
        if closest_enemy > 40 and not is_low_health:
            # Push into enemy territory for bonus
            move_x = 0.7
            rotate = 0.1  # Scan for targets
            
        # 6. Health management
        if is_low_health:
            if closest_enemy < 20:
                # Tactical retreat
                move_x = -0.5
                focus_target = 0
            else:
                # Look for safe opportunities
                if has_ranged and closest_enemy < 35:
                    cast_slot = 2
                    chase_focus = 0.3
                    
        # 7. Mobility usage (HasteOrb gives speed boost)
        if closest_enemy < 25 and closest_enemy > 10:
            # Use mobility to control engagement range
            if health_ratio > 0.5:
                move_x = min(move_x + 0.2, 1.0)  # Boost movement
                
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return improved Derk Gym configuration"""
        return {
            "slots": ["Talons", "IronTail", "HasteOrb"],
            "rewardFunction": {
                "damageEnemyStatue": 0.6,       # Good statue damage
                "damageEnemyUnit": 0.8,         # Good unit damage
                "killEnemyStatue": 2.0,         # Balanced kills
                "killEnemyUnit": 2.5,           # Slightly higher unit kills
                "timeSpentAwayTerritory": 0.8,  # High territory bonus
                "damageTaken": -0.25,           # Acceptable damage for assault
                "friendlyFire": -0.8,           # Higher friendly fire penalty
                "fallDamageTaken": -1.0,        # Avoid fall damage
                "healEnemy": -0.5,              # Added heal enemy penalty
                "teamSpirit": 0.4,              # Balanced team spirit
                "timeScaling": 0.0              # No time pressure
            },
            "primaryColor": "#DC143C",          # Crimson red
            "secondaryColor": "#000000"         # Black
        }

def test_assaulter():
    """Test updated Assaulter brain"""
    print("⚔️ TESTING UPDATED THE ASSAULTER")
    print("=" * 35)
    
    brain = TheAssaulterBrain()
    config = brain.get_derk_gym_config()
    
    print(f"Equipment: {config['slots']}")
    print(f"Strategy: Mobile melee assault")
    print(f"Territory bonus: {config['rewardFunction']['timeSpentAwayTerritory']}")
    print(f"Team spirit: {config['rewardFunction']['teamSpirit']}")
    
    return brain

if __name__ == "__main__":
    test_assaulter()
