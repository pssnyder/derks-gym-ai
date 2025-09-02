"""
Nightrider Peanut - Correct Steam Configuration
=============================================

Updated with actual Steam game bounty values from screenshot.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class NightriderPeanutBrain:
    """
    Nightrider Peanut - Correct Steam Configuration
    
    Actual Steam Game Bounties (from screenshot):
    - Damage enemy statue: 50 per hitpoint
    - Damage enemy unit: 100 per hitpoint
    - Kill enemy statue: 90 points
    - Kill enemy unit: 1000 points
    - Damage taken: -20 per hitpoint
    - Heal enemy: -90 per hitpoint
    - Take fall damage: -100 per hitpoint
    - Manual bonus: 1000 points
    - Victory: 100 points
    - Loss: -100 points
    - Time scaling: 0%
    
    Strategy: Extremely kill-focused (1000 point bounty), low damage penalties
    """
    
    def __init__(self):
        self.name = "Nightrider Peanut"
        self.brain_class = "peanut" 
        self.role = "kill_focused_fighter"
        self.compatible_with = "all_peanut_class"
        
        # Behavioral traits - MAXIMUM kill focus due to 1000 point bounty
        self.aggression = 0.95          # Extremely high due to huge kill reward
        self.team_focus = 0.15          # Low team support - individual hunter
        self.risk_tolerance = 0.85      # Lower damage penalty allows risk-taking
        self.territory_preference = "aggressive"
        self.kill_focus = 1.0           # Maximum kill priority
        
        # Equipment preferences (will be set properly when team configs work)
        self.preferred_equipment = {
            "arms": "Magnum",          # Ranged for safer kills
            "tail": "HealingTail",     # Sustain for longer hunts
            "misc": "FocusingOrb"      # Accuracy for securing kills
        }
        
    def get_action(self, observation):
        """
        Nightrider decision making - hunt for 1000-point kills
        """
        obs = observation
        
        # Key observations
        self_hp = obs[ObservationKeys.Hitpoints.value]
        has_focus = obs[ObservationKeys.HasFocus.value]
        focus_hp = obs[ObservationKeys.FocusHitpoints.value] if has_focus else 0
        
        # Enemy analysis - prioritize kills above all else
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
        
        # Team positioning (minimal - focus on individual kills)
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
        
        return self._kill_hunter_strategy(
            self_hp, closest_enemy, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _kill_hunter_strategy(self, hp, closest_enemy, has_focus, focus_hp,
                            friend_distances, has_ranged, has_melee):
        """
        Kill-focused hunter strategy - 1000 points per kill!
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        
        # KILL HUNTER STRATEGY (1000 point bounty!)
        
        # 1. PRIORITY: Finish low-health enemies (maximum reward)
        if has_focus and focus_hp < 50:
            chase_focus = 1.0       # Full commitment to secure kill
            move_x = 0.9            # Aggressive pursuit
            
            if closest_enemy < 15 and has_melee:
                cast_slot = 1       # Melee for guaranteed kill
            elif has_ranged:
                cast_slot = 2       # Ranged to secure kill safely
                
        # 2. Hunt for kill opportunities
        elif closest_enemy < 45:
            chase_focus = 0.9
            focus_target = 5        # Target nearest enemy
            
            # Optimal positioning for kills
            if closest_enemy > 25:
                move_x = 0.8        # Close gap aggressively
            elif closest_enemy < 12:
                move_x = -0.1       # Back off for optimal range
                
            # Weapon selection for maximum kill potential
            if closest_enemy < 15 and has_melee:
                cast_slot = 1       # Melee for high damage
            elif closest_enemy < 35 and has_ranged:
                cast_slot = 2       # Ranged for safety
                
        # 3. Minimal team coordination (individual hunter)
        elif len(friend_distances) > 0:
            avg_friend_distance = np.mean([d for d in friend_distances if d > 0] or [30])
            
            # Only coordinate if it leads to kills
            if avg_friend_distance > 40:
                chase_focus = 0.2   # Minimal team movement
                focus_target = 2
                
        # 4. Health management (higher risk tolerance due to low damage penalty)
        if health_ratio < 0.3:      # Only retreat when low
            if closest_enemy < 25:
                move_x = -0.3       # Tactical retreat
                focus_target = 2
            else:
                # Still hunt for kills even when hurt (low damage penalty)
                if has_ranged and closest_enemy < 40:
                    cast_slot = 2
                    chase_focus = 0.5
                    
        # 5. Active hunting when no immediate targets
        if closest_enemy > 50:
            move_x = 0.6            # Actively search for enemies
            rotate = 0.2            # Scan for kill opportunities
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return correct Steam game configuration"""
        return {
            "slots": ["Magnum", "HealingTail", "FocusingOrb"],
            "rewardFunction": {
                "damageEnemyStatue": 0.5,       # 50 per hitpoint
                "damageEnemyUnit": 1.0,         # 100 per hitpoint
                "killEnemyStatue": 0.9,         # 90 points
                "killEnemyUnit": 10.0,          # 1000 points (HUGE!)
                "damageTaken": -0.2,            # -20 per hitpoint
                "healEnemy": -0.9,              # -90 per hitpoint
                "fallDamageTaken": -1.0,        # -100 per hitpoint
                "teamSpirit": 0.0,              # Individual hunter
                "timeScaling": 0.0              # 0% time scaling
            },
            "primaryColor": "#4B0082",          # Indigo
            "secondaryColor": "#000000"         # Black
        }

def test_nightrider():
    """Test correct Nightrider configuration"""
    print("🌙 NIGHTRIDER PEANUT - CORRECT STEAM CONFIG")
    print("=" * 45)
    
    brain = NightriderPeanutBrain()
    config = brain.get_derk_gym_config()
    
    print(f"Equipment: {config['slots']}")
    print(f"Strategy: Kill hunter (1000 point bounty!)")
    print(f"Kill enemy unit: {config['rewardFunction']['killEnemyUnit']} (1000 in Steam)")
    print(f"Damage taken: {config['rewardFunction']['damageTaken']} (-20 in Steam)")
    
    return brain

if __name__ == "__main__":
    test_nightrider()
