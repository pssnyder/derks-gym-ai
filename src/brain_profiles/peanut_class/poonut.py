"""
Poonut - Conservative Support Fighter (Peanut Class)
=================================================
Class: Peanut Class Derkling  
Role: Conservative support fighter
Compatible: Spicy Peanut, Nightrider Peanut, Angrrry Peanut

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class PoonutBrain:
    """
    Poonut - The conservative peanut
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 90 per hitpoint
    - Damage enemy unit: 90 per hitpoint
    - Kill enemy statue: 10 points
    - Kill enemy unit: 10 points  
    - Stay in enemy territory: 80 every 5 seconds
    - Damage taken: -100 per hitpoint
    - Friendly fire: -50 per hitpoint
    - Take fall damage: -90 per hitpoint
    - Manual bonus: -1000 points
    - Tie: -10 points
    - Time scaling: 0%
    
    Strategy: Damage-focused, extremely defensive, territory control, peanut support
    """
    
    def __init__(self):
        self.name = "Poonut"
        self.brain_class = "peanut"
        self.role = "conservative_support"
        self.compatible_with = ["Spicy Peanut", "Nightrider Peanut", "Angrrry Peanut"]
        
        # Behavioral traits
        self.aggression = 0.3           # Low aggression
        self.team_focus = 0.95          # Very high peanut gang support
        self.risk_tolerance = 0.1       # Extremely low risk (highest damage penalty)
        self.territory_preference = "controlled"  # High territory bonus but careful
        self.damage_focus = 1.0         # Extreme damage-over-kills focus
        
        # Equipment (likely defensive/ranged support)
        self.preferred_equipment = {
            "arms": "Blaster",     # Safe ranged weapon
            "tail": "Unknown",     # Possibly defensive
            "misc": "Unknown"      # Possibly utility/support
        }
        
    def get_action(self, observation):
        """
        Poonut decision making - conservative peanut support
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
        
        # Peanut gang support positioning
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
        
        return self._poonut_strategy(
            self_hp, closest_enemy, enemy_statue_distance, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _poonut_strategy(self, hp, closest_enemy, statue_distance,
                        has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Poonut's conservative support strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_damaged = health_ratio < 0.8   # Conservative threshold
        is_critical = health_ratio < 0.5  # Very conservative critical threshold
        
        # CONSERVATIVE PEANUT SUPPORT STRATEGY
        
        # 1. Peanut gang support analysis
        peanut_gang_needs_help = False
        safe_support_position = True
        
        if len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            furthest_friend = max([d for d in friend_distances if d > 0] or [0])
            
            # Determine if gang needs support
            if closest_friend > 40 or furthest_friend > 50:
                peanut_gang_needs_help = True
                
            # Check if current position is safe for support
            if closest_enemy < 25:
                safe_support_position = False
                
        # 2. Safe damage dealing (90 point damage bonuses)
        if statue_distance < 40 and closest_enemy > 30 and not is_damaged:
            # Safe statue damage opportunity
            if statue_distance > 25:
                # Cautious approach with escape route
                move_x = 0.3
                focus_target = 4
                
                # Ensure peanut gang is nearby for support
                if len(friend_distances) > 0:
                    closest_friend = min([d for d in friend_distances if d > 0] or [999])
                    if closest_friend < 25:
                        # Gang is close - safer to engage
                        if has_ranged:
                            cast_slot = 2
                            
            else:
                # Close range statue damage - very careful
                if safe_support_position:
                    focus_target = 4
                    if has_ranged:
                        cast_slot = 2  # Ranged damage from safety
                        
        # 3. Enemy damage (only when very safe)
        elif closest_enemy < 35 and closest_enemy > 20 and not is_damaged:
            # Safe range for enemy damage
            if safe_support_position:
                focus_target = 5
                chase_focus = 0.1  # Minimal chase - safety first
                
                if has_ranged:
                    cast_slot = 2  # Safe ranged damage
                    
        # 4. Peanut gang support positioning
        if peanut_gang_needs_help and not is_critical:
            # Move to support gang, but safely
            if closest_enemy > 25:
                move_x = 0.4  # Cautious movement to support
                
                # Provide covering fire while moving
                if has_ranged and closest_enemy < 40:
                    cast_slot = 2
                    focus_target = 5
                    
        elif len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            
            if closest_friend < 12:
                # Too close - create space for effective support
                move_x = -0.2
                rotate = 0.1
                
            elif closest_friend > 25 and closest_enemy > 30:
                # Move closer to gang for support
                move_x = 0.3
                
        # 5. Territory control (80 point bonus - but safely)
        elif closest_enemy > 40 and statue_distance > 45 and not is_damaged:
            # Safe territory advancement
            move_x = 0.4
            
            # Stay with peanut gang for safety
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend > 30:
                    # Gang is too far - slower advance
                    move_x = 0.2
                    
        # 6. Defensive positioning (extremely high damage penalty)
        if is_damaged or closest_enemy < 20:
            # Retreat to safe distance
            if closest_enemy < 25:
                move_x = -0.6  # Retreat quickly
                
                # Clear focus to avoid pursuit
                if is_critical:
                    focus_target = 0
                    
            # Move toward peanut gang for protection
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend > 20:
                    move_x = max(move_x, -0.3)  # Move toward gang but still retreating
                    
        # 7. Emergency support fire
        if not is_critical and has_ranged:
            # Provide support fire when safe
            if closest_enemy < 35 and closest_enemy > 15:
                cast_slot = 2
                focus_target = 5
                chase_focus = 0.05  # Minimal chase for safety
                
        # 8. Weapon preference - heavily favor ranged
        if has_ranged and closest_enemy < 40:
            cast_slot = 2  # Always prefer ranged for safety
        elif has_melee and closest_enemy < 8 and health_ratio > 0.8:
            # Only melee when very healthy and very close
            cast_slot = 1
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["Blaster", None, None],  # Safe ranged weapon
            "rewardFunction": {
                "damageEnemyStatue": 0.9,        # High damage focus
                "damageEnemyUnit": 0.9,          # High damage focus
                "killEnemyStatue": 0.1,          # Very low kill priority
                "killEnemyUnit": 0.1,            # Very low kill priority
                "timeSpentAwayTerritory": 0.8,   # High territory bonus
                "damageTaken": -1.0,             # Maximum damage avoidance
                "friendlyFire": -0.5,            # Friendly fire penalty
                "fallDamageTaken": -0.9,         # Avoid fall damage
                "teamSpirit": 0.95,              # Maximum peanut gang support
                "timeScaling": 0.0               # No time pressure
            },
            "primaryColor": "#DEB887",           # Burlywood (nutty/conservative)
            "secondaryColor": "#8FBC8F"          # Dark sea green (cautious)
        }

def test_poonut():
    """Test Poonut brain"""
    print("🥜 TESTING POONUT BRAIN")
    print("=" * 23)
    
    brain = PoonutBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # Poonut
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
    print(f"\n🥜 Poonut Average Reward: {avg_reward:.2f}")
    print("Strategy: Conservative support, damage-focused, peanut gang coordination")
    
    return results

if __name__ == "__main__":
    test_poonut()
