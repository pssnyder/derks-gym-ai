"""
The Assaulter - Assault Fighter (Testing Class)
=============================================
Class: Testing Class Derkling  
Role: Aggressive assault fighter
Compatible: Unknown (testing classification)

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class TheAssaulterBrain:
    """
    The Assaulter - Pure aggression incarnate
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 54 per hitpoint
    - Damage enemy unit: 55 per hitpoint
    - Kill enemy statue: 100 points
    - Kill enemy unit: 100 points  
    - Stay in enemy territory: 30 every 5 seconds
    - Damage taken: -22 per hitpoint
    - Friendly fire: -50 per hitpoint
    - Take fall damage: -90 per hitpoint
    - Manual bonus: -1000 points
    - Tie: -10 points
    - Time scaling: 0%
    
    Strategy: Kill-focused assault, high aggression, territory domination
    """
    
    def __init__(self):
        self.name = "The Assaulter"
        self.brain_class = "testing"
        self.role = "assault_fighter"
        self.compatible_with = "unknown"
        
        # Behavioral traits
        self.aggression = 1.0           # Maximum aggression
        self.team_focus = 0.6           # Moderate team coordination for assaults
        self.risk_tolerance = 0.8       # High risk tolerance for kills
        self.territory_preference = "aggressive"  # Enemy territory focus
        self.kill_focus = 1.0           # Equal kill and damage bounties = kill priority
        
        # Equipment (likely melee-focused assault)
        self.preferred_equipment = {
            "arms": "Talons",      # High-damage melee
            "tail": "Unknown",     # Possibly mobility
            "misc": "Unknown"      # Possibly defensive
        }
        
    def get_action(self, observation):
        """
        The Assaulter decision making - pure aggressive assault
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
        
        # Team coordination
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
        
        return self._assaulter_strategy(
            self_hp, closest_enemy, enemy_statue_distance, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _assaulter_strategy(self, hp, closest_enemy, statue_distance,
                          has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        The Assaulter's pure aggression strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_critical_health = health_ratio < 0.25  # Only retreat when critical
        
        # PURE ASSAULT STRATEGY
        
        # 1. PRIORITY: Enemy elimination (100 point kills)
        if closest_enemy < 50 and not is_critical_health:
            if closest_enemy > 20:
                # Charge at enemy
                move_x = 1.0
                chase_focus = 1.0
                focus_target = 5  # Focus closest enemy
                
                # Coordinate with team for group assault
                if len(friend_distances) > 0:
                    closest_friend = min([d for d in friend_distances if d > 0] or [999])
                    if closest_friend < 20:
                        # Team is close - synchronized attack
                        chase_focus = 1.0
                        
            elif closest_enemy <= 20:
                # In assault range - all-out attack
                chase_focus = 1.0
                focus_target = 5
                
                if has_melee and closest_enemy < 8:
                    # Melee range - use melee for maximum damage
                    cast_slot = 1
                elif has_ranged and closest_enemy < 15:
                    # Close ranged - finish them
                    cast_slot = 2
                else:
                    # Rush in for melee kill
                    move_x = 1.0
                    
        # 2. Statue assault (if no enemies or after clearing enemies)
        elif statue_distance < 60 and not is_critical_health:
            if statue_distance > 25:
                # Charge the statue
                move_x = 0.8
                focus_target = 4  # Focus enemy statue
                
                # Look for supporting fire opportunities
                if has_ranged and statue_distance < 40:
                    cast_slot = 2
                    
            else:
                # Assault the statue directly
                focus_target = 4
                if has_melee:
                    cast_slot = 1  # Melee the statue
                elif has_ranged:
                    cast_slot = 2  # Ranged assault
                    
        # 3. Territory domination (30 point bonus for enemy territory)
        elif closest_enemy > 50:
            # Push into enemy territory aggressively
            move_x = 0.9
            rotate = 0.1  # Scan for targets
            
            # Stay in formation with team for group assault
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend > 25:
                    # Team is spread - move to support
                    move_x = 0.7
                    
        # 4. Team assault coordination
        if len(friend_distances) > 0 and not is_critical_health:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            if closest_friend < 15 and closest_enemy < 30:
                # Perfect for group assault
                move_x = 1.0
                chase_focus = 1.0
                focus_target = 5
                
        # 5. Emergency retreat (only when critical health)
        if is_critical_health:
            if closest_enemy < 25:
                # Tactical retreat to friendly territory
                move_x = -0.6
                focus_target = 0  # Clear focus to avoid pursuit
            else:
                # Safe distance - continue assault but cautiously
                if has_ranged and closest_enemy < 40:
                    cast_slot = 2
                    focus_target = 5
                    chase_focus = 0.3  # Limited chase when hurt
                    
        # 6. Weapon preference - prefer melee for kills
        if has_melee and closest_enemy < 10:
            cast_slot = 1  # Melee for maximum kill potential
        elif has_ranged and closest_enemy < 30:
            cast_slot = 2  # Ranged to soften up
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["Talons", None, None],  # Melee assault specialist
            "rewardFunction": {
                "damageEnemyStatue": 0.54,       # Moderate statue damage
                "damageEnemyUnit": 0.55,         # Moderate unit damage
                "killEnemyStatue": 1.0,          # High kill priority
                "killEnemyUnit": 1.0,            # High kill priority
                "timeSpentAwayTerritory": 0.3,   # Enemy territory bonus
                "damageTaken": -0.22,            # Acceptable damage for kills
                "friendlyFire": -0.5,            # Friendly fire penalty
                "fallDamageTaken": -0.9,         # Avoid fall damage
                "teamSpirit": 0.6,               # Team coordination for assaults
                "timeScaling": 0.0               # No time pressure
            },
            "primaryColor": "#DC143C",           # Crimson red (assault/aggression)
            "secondaryColor": "#000000"          # Black (intimidation)
        }

def test_the_assaulter():
    """Test The Assaulter brain"""
    print("⚔️ TESTING THE ASSAULTER BRAIN")
    print("=" * 31)
    
    brain = TheAssaulterBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # The Assaulter
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
    print(f"\n⚔️ The Assaulter Average Reward: {avg_reward:.2f}")
    print("Strategy: Pure aggressive assault, kill-focused, territory domination")
    
    return results

if __name__ == "__main__":
    test_the_assaulter()
