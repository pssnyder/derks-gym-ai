"""
Clint Eastwood - Lone Wolf Ranged Fighter
========================================
Class: Lone Wolf Class Derkling  
Role: Balanced ranged fighter, solo fighter
Compatible: None (non-compatible with peanut class)

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class ClintEastwoodBrain:
    """
    Clint Eastwood - The lone gunslinger
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 80 per hitpoint
    - Damage enemy unit: 81 per hitpoint
    - Kill enemy statue: 20 points
    - Kill enemy unit: 30 points  
    - Stay in enemy territory: 70 every 5 seconds
    - Damage taken: -77 per hitpoint
    - Friendly fire: -50 per hitpoint
    - Take fall damage: -90 per hitpoint
    - Manual bonus: -1000 points
    - Tie: -10 points
    - Time scaling: 0%
    
    Strategy: Damage-over-kills focus, high damage avoidance, territory control
    """
    
    def __init__(self):
        self.name = "Clint Eastwood"
        self.brain_class = "lone_wolf"
        self.role = "balanced_ranged"
        self.compatible_with = "none"
        
        # Behavioral traits
        self.aggression = 0.70          # Moderate-high damage focus
        self.team_focus = 0.05          # Lone wolf - minimal team interaction
        self.risk_tolerance = 0.20      # Very low due to high damage penalty
        self.territory_preference = "aggressive"  # Enemy territory bonus
        self.damage_focus = 1.0         # Prefers damage over kills
        
        # Equipment (likely ranged specialist)
        self.preferred_equipment = {
            "arms": "Magnum",      # High-damage ranged weapon
            "tail": "Unknown",     # Possibly support/utility
            "misc": "Unknown"      # Possibly mobility or defense
        }
        
    def get_action(self, observation):
        """
        Clint Eastwood decision making - lone wolf ranged combat
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
        
        # Team distances (but lone wolf avoids close cooperation)
        friend_distances = [
            obs[ObservationKeys.Friend1Distance.value],
            obs[ObservationKeys.Friend2Distance.value]
        ]
        
        # Weapon focus - prioritize ranged
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
        
        return self._clint_eastwood_strategy(
            self_hp, closest_enemy, enemy_statue_distance, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _clint_eastwood_strategy(self, hp, closest_enemy, statue_distance,
                               has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Clint Eastwood's lone wolf ranged strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_low_health = health_ratio < 0.4  # More conservative due to high damage penalty
        
        # LONE WOLF RANGED STRATEGY
        
        # 1. Maintain optimal range - avoid close combat
        if closest_enemy < 30:
            if closest_enemy < 15:
                # Too close - retreat and shoot
                move_x = -0.6
                if has_ranged:
                    cast_slot = 2
                    focus_target = 5
            elif closest_enemy < 25:
                # Good range for ranged combat
                move_x = -0.2  # Slight retreat to maintain distance
                if has_ranged:
                    cast_slot = 2
                    focus_target = 5
                    chase_focus = 0.3  # Minimal chase, stay at range
                    
        # 2. Statue damage focus (high damage bounty, low kill bounty)
        elif statue_distance < 45 and health_ratio > 0.5:
            # Approach statue cautiously for damage
            if statue_distance > 30:
                move_x = 0.4
                focus_target = 4  # Focus enemy statue
            else:
                # In range - focus on dealing sustained damage
                if has_ranged:
                    cast_slot = 2
                    focus_target = 4
                # Don't chase - maintain safe distance
                
        # 3. Territory control (enemy territory bonus)
        elif closest_enemy > 40 and statue_distance > 50:
            # Move into enemy territory but carefully
            move_x = 0.3
            rotate = 0.1  # Scan for threats
            
        # 4. Lone wolf positioning - avoid clustering with team
        if len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            if closest_friend < 15:
                # Too close to team - maintain independence
                move_x = 0.2
                rotate = -0.2  # Turn away from team
                
        # 5. Health management (very conservative due to -77 damage penalty)
        if is_low_health:
            if closest_enemy < 35:
                # Retreat to safe distance
                move_x = -0.8
                focus_target = 0  # Clear focus to avoid pursuit
            else:
                # Safe distance - continue ranged attacks
                if has_ranged and closest_enemy < 50:
                    cast_slot = 2
                    focus_target = 5
                    
        # 6. Weapon preference - strongly favor ranged
        if not has_ranged and has_melee and closest_enemy < 12:
            # Only use melee as last resort when very close
            cast_slot = 1
        elif has_ranged and closest_enemy < 40:
            # Prefer ranged whenever possible
            cast_slot = 2
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["Magnum", None, None],  # Ranged specialist
            "rewardFunction": {
                "damageEnemyStatue": 0.8,    # High statue damage focus
                "damageEnemyUnit": 0.81,     # Slightly higher unit damage
                "killEnemyStatue": 0.2,      # Low kill focus
                "killEnemyUnit": 0.3,        # Low kill focus
                "timeSpentAwayTerritory": 0.7, # Enemy territory bonus
                "damageTaken": -0.77,        # High damage avoidance
                "friendlyFire": -0.5,        # Friendly fire penalty
                "fallDamageTaken": -0.9,     # Avoid fall damage
                "teamSpirit": 0.0,           # No team spirit (lone wolf)
                "timeScaling": 0.0           # No time pressure
            },
            "primaryColor": "#8B4513",       # Saddle brown (western theme)
            "secondaryColor": "#2F4F4F"      # Dark slate gray
        }

def test_clint_eastwood():
    """Test Clint Eastwood brain"""
    print("🤠 TESTING CLINT EASTWOOD BRAIN")
    print("=" * 38)
    
    brain = ClintEastwoodBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # Clint Eastwood
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
    print(f"\n🤠 Clint Eastwood Average Reward: {avg_reward:.2f}")
    print("Strategy: Lone wolf ranged combat, damage-over-kills, territory control")
    
    return results

if __name__ == "__main__":
    test_clint_eastwood()
