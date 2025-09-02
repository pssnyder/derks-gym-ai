"""
Angrrry (The Assaulter) - Correct Steam Configuration
===================================================

Updated with actual Steam game bounty values from screenshot.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class AngrrryBrain:
    """
    Angrrry (The Assaulter) - Correct Steam Configuration
    
    Actual Steam Game Bounties (from screenshot):
    - Damage enemy statue: 50 per hitpoint
    - Damage enemy unit: 80 per hitpoint
    - Kill enemy statue: 60 points
    - Kill enemy unit: 100 points
    - Heal own statue: 10 per hitpoint
    - Heal teammate 1: 10 per hitpoint
    - Heal teammate 2: 1 per hitpoint
    - Stay in enemy territory: 10 every 5 seconds
    - Damage taken: -40 per hitpoint
    - Friendly fire: -60 per hitpoint
    - Heal enemy: -10 per hitpoint
    - Take fall damage: -100 per hitpoint
    - Own statue takes damage: -70 per hitpoint
    - Manual bonus: -1000 points
    - Victory: 100 points
    - Tie: -50 points
    - Time scaling: 90%
    
    Strategy: Balanced fighter with team support, territory control focus
    """
    
    def __init__(self):
        self.name = "Angrrry"
        self.brain_class = "testing"
        self.role = "balanced_assault"
        self.compatible_with = "unknown"
        
        # Behavioral traits - Balanced with team support
        self.aggression = 0.8           # High but not maximum
        self.team_focus = 0.7           # High team support (healing bonuses)
        self.risk_tolerance = 0.6       # Higher damage penalty = more cautious
        self.territory_preference = "aggressive"  # Territory bonus focus
        self.kill_focus = 0.7           # Moderate kill focus
        
        # Equipment - Assault with support capabilities
        self.preferred_equipment = {
            "arms": "Talons",          # Melee assault
            "tail": "HealingTail",     # Team healing support
            "misc": "HasteOrb"         # Mobility for territory control
        }
        
    def get_action(self, observation):
        """
        Angrrry decision making - balanced assault with team support
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
        
        # Statue analysis (for healing and territory)
        enemy_statue_distance = obs[ObservationKeys.EnemyStatueDistance.value] * 50
        # Note: OwnStatueDistance may not be available, using friend statue as proxy
        friend_statue_distance = obs[ObservationKeys.FriendStatueDistance.value] * 50
        
        # Team coordination (important for healing bonuses)
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value] * 50,
            obs[ObservationKeys.Friend2Distance.value] * 50
        ]
        
        # Weapon status
        has_melee = any([
            obs[ObservationKeys.HasTalons.value],
            obs[ObservationKeys.HasBloodClaws.value]
        ])
        has_ranged = any([
            obs[ObservationKeys.HasPistol.value],
            obs[ObservationKeys.HasMagnum.value]
        ])
        
        return self._balanced_assault_strategy(
            self_hp, closest_enemy, enemy_statue_distance, friend_statue_distance,
            has_focus, focus_hp, friend_distances, has_ranged, has_melee
        )
    
    def _balanced_assault_strategy(self, hp, closest_enemy, enemy_statue_dist, friend_statue_dist,
                                 has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Balanced assault strategy with team support and territory control
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_low_health = health_ratio < 0.4  # More cautious due to -40 damage penalty
        
        # BALANCED ASSAULT STRATEGY
        
        # 1. Team support priority (healing bonuses)
        if len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            
            if closest_friend < 15 and health_ratio > 0.6:
                # Close to teammate and healthy - provide support
                focus_target = 2  # Focus on teammate
                if has_melee:  # Assume healing capability
                    cast_slot = 3  # Healing ability
                    
        # 2. Kill opportunities (100 point bounty)
        if closest_enemy < 35 and not is_low_health:
            if closest_enemy > 15:
                # Approach for kill
                move_x = 0.7
                chase_focus = 0.8
                focus_target = 5
                
                # Use ranged to soften while closing
                if has_ranged and closest_enemy < 25:
                    cast_slot = 2
                    
            elif closest_enemy <= 15:
                # Melee engagement
                chase_focus = 0.9
                focus_target = 5
                
                if has_melee and closest_enemy < 8:
                    cast_slot = 1  # Melee attack
                else:
                    move_x = 0.5   # Close for melee
                    
        # 3. Territory control (10 points every 5 seconds)
        elif closest_enemy > 35 and not is_low_health:
            # Push into enemy territory for bonus
            move_x = 0.6
            rotate = 0.1
            
            # Stay near team for coordination
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend > 25:
                    move_x = 0.4  # Move toward team
                    
        # 4. Statue protection (-70 per hitpoint if own statue damaged)
        if friend_statue_dist < 30 and closest_enemy < 40:
            # Prioritize statue defense
            focus_target = 3  # Focus friend statue area
            move_x = -0.2     # Move toward friend statue
            
            if has_ranged and closest_enemy < 30:
                cast_slot = 2  # Ranged defense
                
        # 5. Health management (higher damage penalty = more cautious)
        if is_low_health:
            if closest_enemy < 25:
                # Retreat toward team/statue
                move_x = -0.6
                focus_target = 2 if len(friend_distances) > 0 else 3
            else:
                # Look for safe support opportunities
                if len(friend_distances) > 0:
                    closest_friend = min([d for d in friend_distances if d > 0] or [999])
                    if closest_friend < 20:
                        cast_slot = 3  # Heal teammate or self
                        
        # 6. Avoid friendly fire (-60 per hitpoint penalty)
        if len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            if closest_friend < 10 and closest_enemy < 15:
                # Too close to teammate near enemy - be careful
                move_x = 0.2  # Create space
                chase_focus = 0.5  # Reduced aggression
                
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return correct Steam game configuration"""
        return {
            "slots": ["Talons", "HealingTail", "HasteOrb"],
            "rewardFunction": {
                "damageEnemyStatue": 0.5,       # 50 per hitpoint
                "damageEnemyUnit": 0.8,         # 80 per hitpoint
                "killEnemyStatue": 0.6,         # 60 points
                "killEnemyUnit": 1.0,           # 100 points
                "healOwnStatue": 0.1,           # 10 per hitpoint
                "healTeammate1": 0.1,           # 10 per hitpoint
                "healTeammate2": 0.01,          # 1 per hitpoint
                "timeSpentAwayTerritory": 0.1,  # 10 every 5 seconds
                "damageTaken": -0.4,            # -40 per hitpoint
                "friendlyFire": -0.6,           # -60 per hitpoint
                "healEnemy": -0.1,              # -10 per hitpoint
                "fallDamageTaken": -1.0,        # -100 per hitpoint
                "ownStatueTakesDamage": -0.7,   # -70 per hitpoint
                "teamSpirit": 0.7,              # High team focus
                "timeScaling": 0.9              # 90% time scaling
            },
            "primaryColor": "#DC143C",          # Crimson red
            "secondaryColor": "#000000"         # Black
        }

def test_angrrry():
    """Test correct Angrrry configuration"""
    print("😡 ANGRRRY - CORRECT STEAM CONFIG")
    print("=" * 35)
    
    brain = AngrrryBrain()
    config = brain.get_derk_gym_config()
    
    print(f"Equipment: {config['slots']}")
    print(f"Strategy: Balanced assault with team support")
    print(f"Kill enemy unit: {config['rewardFunction']['killEnemyUnit']} (100 in Steam)")
    print(f"Damage taken: {config['rewardFunction']['damageTaken']} (-40 in Steam)")
    print(f"Friendly fire: {config['rewardFunction']['friendlyFire']} (-60 in Steam)")
    print(f"Team spirit: {config['rewardFunction']['teamSpirit']} (high team focus)")
    
    return brain

if __name__ == "__main__":
    test_angrrry()
