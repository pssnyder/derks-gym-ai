"""
Spicy Peanut - Aggressive Winner
===============================
Class: Peanut Class Derkling
Role: Aggressive and win focused, primary duo fighter
Bonded Pair: Safe T Peanut (forms the core fighting duo)

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class SpicyPeanutBrain:
    """
    Spicy Peanut - The aggressive half of the primary duo
    
    Steam Game Bounties (extracted from screenshot):
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
    - Victory: 1000 points
    - Team spirit: 80%
    - Time scaling: 90%
    
    Strategy: High aggression, enemy territory focus, victory-oriented
    Equipment: [Need to check derkling loadouts screen]
    """
    
    def __init__(self):
        self.name = "Spicy Peanut"
        self.brain_class = "peanut"
        self.role = "aggressive_winner"
        self.bonded_pair = "Safe T Peanut"
        
        # Behavioral traits derived from Steam bounties
        self.aggression = 0.85          # High damage/kill focus
        self.team_focus = 0.40          # Some team support but victory focused
        self.risk_tolerance = 0.75      # Willing to take risks for wins
        self.territory_preference = "aggressive"  # Bonus for enemy territory
        self.victory_focus = 1.0        # Huge victory bonus
        
        # Equipment (to be confirmed from loadouts screen)
        self.preferred_equipment = {
            "arms": "Unknown",     # High damage weapon likely
            "tail": "Unknown",     # Combat enhancement likely  
            "misc": "Unknown"      # Mobility or damage boost likely
        }
        
    def get_action(self, observation):
        """
        Spicy Peanut decision making - aggressive, victory-focused
        """
        obs = observation
        
        # Key observations
        self_hp = obs[ObservationKeys.Hitpoints.value]
        has_focus = obs[ObservationKeys.HasFocus.value]
        focus_hp = obs[ObservationKeys.FocusHitpoints.value] if has_focus else 0
        
        # Enemy distances
        enemy_distances = [
            obs[ObservationKeys.Enemy1Distance.value],
            obs[ObservationKeys.Enemy2Distance.value], 
            obs[ObservationKeys.Enemy3Distance.value]
        ]
        closest_enemy = min([d for d in enemy_distances if d > 0] or [999])
        
        # Enemy statue distance
        enemy_statue_distance = obs[ObservationKeys.EnemyStatueDistance.value]
        
        # Team coordination with Safe T Peanut
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value],
            obs[ObservationKeys.Friend2Distance.value]
        ]
        
        # Weapon availability
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
        
        return self._spicy_peanut_strategy(
            self_hp, closest_enemy, enemy_statue_distance, 
            has_focus, focus_hp, friend_distances, has_ranged, has_melee
        )
    
    def _spicy_peanut_strategy(self, hp, closest_enemy, statue_distance, 
                             has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Spicy Peanut's aggressive, victory-focused strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_low_health = health_ratio < 0.3
        
        # AGGRESSIVE PRIORITY SYSTEM
        
        # 1. Victory focus - prioritize enemy statue when possible
        if statue_distance < 40 and health_ratio > 0.4:
            chase_focus = 0.9
            focus_target = 4  # Focus enemy statue
            move_x = 0.6      # Push forward aggressively
            
            # Use abilities on statue
            if statue_distance < 25:
                if has_melee:
                    cast_slot = 1
                elif has_ranged:
                    cast_slot = 2
                    
        # 2. Enemy unit elimination when statue not accessible
        elif closest_enemy < 35 and not is_low_health:
            chase_focus = 0.8
            focus_target = 5  # Focus nearest enemy
            
            # Aggressive positioning
            if closest_enemy > 20:
                move_x = 0.5  # Close the gap
            
            # Combat abilities
            if closest_enemy < 20 and has_melee:
                cast_slot = 1
            elif closest_enemy < 30 and has_ranged:
                cast_slot = 2
                
        # 3. Coordinate with Safe T Peanut (bonded pair tactics)
        elif len(friend_distances) > 0:
            safe_t_distance = min([d for d in friend_distances if d > 0] or [999])
            
            # Stay reasonably close to bonded pair
            if safe_t_distance > 30:
                chase_focus = 0.4
                focus_target = 2  # Move toward teammate
            elif safe_t_distance < 10:
                move_x = 0.2   # Give some space for maneuvering
                
        # 4. Retreat/regroup when low health (but still aggressive)
        if is_low_health:
            # Less retreat than defensive units - risk tolerance
            if closest_enemy < 15:
                move_x = -0.3  # Tactical withdrawal
                focus_target = 2  # Focus on teammate for support
            else:
                # Continue fighting at range if possible
                if has_ranged and closest_enemy < 35:
                    cast_slot = 2
                    
        # 5. Territory control - stay in enemy territory when possible
        # (This is harder to detect in observations, but influences positioning)
        if closest_enemy > 40 and statue_distance > 50:
            move_x = 0.3  # Push toward enemy territory
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["Talons", "Pistol", None],
            "rewardFunction": {
                "damageEnemyStatue": 0.5,    # High statue damage priority
                "damageEnemyUnit": 0.8,      # High unit damage
                "killEnemyStatue": 6.0,      # Very high statue kill reward  
                "killEnemyUnit": 1.0,        # Good unit kill reward
                "healTeammate1": 0.1,        # Some team support
                "healTeammate2": 0.01,       # Minimal secondary support
                "timeSpentAwayTerritory": 0.1, # Enemy territory bonus
                "damageTaken": -0.4,         # Damage penalty
                "friendlyFire": -0.6,        # Heavy friendly fire penalty
                "teamSpirit": 0.8,           # High team spirit
                "timeScaling": 0.9           # Time pressure
            },
            "primaryColor": "#FF1493",       # Deep pink (spicy!)
            "secondaryColor": "#8B0000"      # Dark red
        }

def test_spicy_peanut():
    """Test Spicy Peanut brain"""
    print("🌶️ TESTING SPICY PEANUT BRAIN")
    print("=" * 35)
    
    brain = SpicyPeanutBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # Spicy Peanut
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
    print(f"\n🌶️ Spicy Peanut Average Reward: {avg_reward:.2f}")
    print("Strategy: Aggressive statue focus, victory-oriented, bonds with Safe T Peanut")
    
    return results

if __name__ == "__main__":
    test_spicy_peanut()
