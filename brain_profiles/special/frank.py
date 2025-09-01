"""
Frank - Special Operations (Special Class)
========================================
Class: Special Class Derkling  
Role: Special operations and tactical specialist
Compatible: Unique classification

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class FrankBrain:
    """
    Frank - The special operations specialist
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 68 per hitpoint
    - Damage enemy unit: 70 per hitpoint
    - Kill enemy statue: 30 points
    - Kill enemy unit: 40 points  
    - Stay in enemy territory: 60 every 5 seconds
    - Damage taken: -62 per hitpoint
    - Friendly fire: -50 per hitpoint
    - Take fall damage: -90 per hitpoint
    - Manual bonus: -1000 points
    - Tie: -10 points
    - Time scaling: 0%
    
    Strategy: Damage-focused operations, territory infiltration, high survivability
    """
    
    def __init__(self):
        self.name = "Frank"
        self.brain_class = "special"
        self.role = "special_operations"
        self.compatible_with = "unique"
        
        # Behavioral traits
        self.aggression = 0.8           # High aggression for operations
        self.team_focus = 0.3           # Low team focus - special ops
        self.risk_tolerance = 0.4       # Moderate-low due to high damage penalty
        self.territory_preference = "infiltration"  # High enemy territory bonus
        self.damage_focus = 1.0         # Strong damage-over-kills focus
        
        # Equipment (likely specialized loadout)
        self.preferred_equipment = {
            "arms": "Magnum",      # High-damage precision weapon
            "tail": "Unknown",     # Possibly stealth/mobility
            "misc": "Unknown"      # Possibly tactical gear
        }
        
    def get_action(self, observation):
        """
        Frank decision making - special operations tactics
        """
        obs = observation
        
        # Key observations
        self_hp = obs[ObservationKeys.Hitpoints.value]
        has_focus = obs[ObservationKeys.HasFocus.value]
        focus_hp = obs[ObservationKeys.FocusHitpoints.value] if has_focus else 0
        
        # Enemy analysis
        enemy_distances = [
            obs[ObservationKeys.Enemy1Distance.value],
            obs[ObservationKeys.Enemy2Distance.value], 
            obs[ObservationKeys.Enemy3Distance.value]
        ]
        closest_enemy = min([d for d in enemy_distances if d > 0] or [999])
        
        # Statue targeting
        enemy_statue_distance = obs[ObservationKeys.EnemyStatueDistance.value]
        
        # Team positioning (minimal coordination)
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value],
            obs[ObservationKeys.Friend2Distance.value]
        ]
        
        # Weapon analysis
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
        
        return self._frank_strategy(
            self_hp, closest_enemy, enemy_statue_distance, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _frank_strategy(self, hp, closest_enemy, statue_distance,
                       has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Frank's special operations strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_compromised = health_ratio < 0.5  # Higher threshold due to high damage penalty
        
        # SPECIAL OPERATIONS STRATEGY
        
        # 1. Territory infiltration (60 point bonus - very high)
        in_enemy_territory = closest_enemy < 50 or statue_distance < 60
        
        if not in_enemy_territory and not is_compromised:
            # Infiltrate enemy territory
            move_x = 0.7
            rotate = 0.05  # Tactical scanning
            
            # Avoid team clustering for stealth
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend < 20:
                    # Too close to team - break away for independent operation
                    move_x = 0.5
                    rotate = -0.1
                    
        # 2. High-value damage targeting (68/70 damage bonuses)
        elif statue_distance < 45 and closest_enemy > 25:
            # Optimal statue damage opportunity
            if statue_distance > 30:
                # Approach with tactical precision
                move_x = 0.5
                focus_target = 4  # Focus enemy statue
                
                # Check for overwatch opportunity
                if has_ranged:
                    cast_slot = 2  # Ranged damage
                    
            else:
                # Close-range statue operation
                focus_target = 4
                if has_ranged and statue_distance > 15:
                    cast_slot = 2  # Precision ranged damage
                elif has_melee and statue_distance < 20:
                    cast_slot = 1  # Close operations
                    
        # 3. Tactical enemy engagement (damage priority over kills)
        elif closest_enemy < 35 and not is_compromised:
            if closest_enemy > 20:
                # Optimal engagement range
                focus_target = 5
                chase_focus = 0.5  # Moderate pursuit
                
                if has_ranged:
                    cast_slot = 2  # Precision damage
                    
                # Tactical positioning
                move_x = 0.3
                
            elif closest_enemy <= 20:
                # Close engagement - prioritize damage over kills
                focus_target = 5
                
                if has_ranged and closest_enemy > 10:
                    cast_slot = 2  # Close-range precision
                    chase_focus = 0.3  # Limited chase for damage
                elif has_melee and closest_enemy < 12:
                    cast_slot = 1  # Melee damage application
                    
        # 4. Evasion and repositioning (high damage penalty management)
        elif closest_enemy < 25 and is_compromised:
            # Tactical withdrawal
            move_x = -0.6
            
            # Continue damage application during withdrawal
            if has_ranged and closest_enemy < 35:
                cast_slot = 2
                focus_target = 5
                
            # Break contact if heavily damaged
            if health_ratio < 0.3:
                focus_target = 0  # Clear focus to break contact
                
        # 5. Overwatch position (when no immediate targets)
        elif closest_enemy > 40 and statue_distance > 50:
            # Move to tactical advantage position
            move_x = 0.4
            rotate = 0.1  # Scan for opportunities
            
            # Maintain distance from team for independent ops
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend < 25:
                    # Maintain operational independence
                    move_x = 0.3
                    rotate = 0.05
                    
        # 6. Health threshold management
        if is_compromised:
            # Damage mitigation priority
            if closest_enemy < 30:
                # Create tactical distance
                move_x = -0.5
                
                # Maintain suppressive fire if possible
                if has_ranged and closest_enemy < 40:
                    cast_slot = 2
                    focus_target = 5
                    chase_focus = 0.1  # Minimal pursuit when damaged
                    
        # 7. Weapon specialization
        if has_ranged and closest_enemy < 40:
            # Prefer ranged for damage application
            cast_slot = 2
        elif has_melee and closest_enemy < 10 and health_ratio > 0.6:
            # Melee only when healthy and very close
            cast_slot = 1
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["Magnum", None, None],  # Precision weapon specialist
            "rewardFunction": {
                "damageEnemyStatue": 0.68,       # High statue damage focus
                "damageEnemyUnit": 0.7,          # High unit damage focus
                "killEnemyStatue": 0.3,          # Low kill priority
                "killEnemyUnit": 0.4,            # Low kill priority
                "timeSpentAwayTerritory": 0.6,   # High territory infiltration
                "damageTaken": -0.62,            # High damage avoidance
                "friendlyFire": -0.5,            # Friendly fire penalty
                "fallDamageTaken": -0.9,         # Avoid fall damage
                "teamSpirit": 0.3,               # Low team coordination (special ops)
                "timeScaling": 0.0               # No time pressure
            },
            "primaryColor": "#556B2F",           # Dark olive green (special ops)
            "secondaryColor": "#2F2F2F"          # Dark gray (stealth)
        }

def test_frank():
    """Test Frank brain"""
    print("🎯 TESTING FRANK BRAIN")
    print("=" * 22)
    
    brain = FrankBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # Frank
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
    print(f"\n🎯 Frank Average Reward: {avg_reward:.2f}")
    print("Strategy: Special operations, damage-focused, territory infiltration")
    
    return results

if __name__ == "__main__":
    test_frank()
