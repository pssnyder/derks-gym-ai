"""
The Peacemaker - Balanced Support/Control (Testing Class)
======================================================
Class: Testing Class Derkling  
Role: Balanced support and control specialist
Compatible: Unknown (testing classification)

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class ThePeacemakerBrain:
    """
    The Peacemaker - Balanced control and support
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 35 per hitpoint
    - Damage enemy unit: 45 per hitpoint
    - Kill enemy statue: 75 points
    - Kill enemy unit: 75 points  
    - Stay in enemy territory: 45 every 5 seconds
    - Damage taken: -35 per hitpoint
    - Friendly fire: -50 per hitpoint
    - Take fall damage: -90 per hitpoint
    - Manual bonus: -1000 points
    - Tie: -10 points
    - Time scaling: 0%
    
    Strategy: Balanced approach, equal kill/statue focus, territory control
    """
    
    def __init__(self):
        self.name = "The Peacemaker"
        self.brain_class = "testing"
        self.role = "balanced_control"
        self.compatible_with = "unknown"
        
        # Behavioral traits
        self.aggression = 0.6           # Moderate aggression
        self.team_focus = 0.8           # High team coordination
        self.risk_tolerance = 0.5       # Balanced risk management
        self.territory_preference = "balanced"  # Moderate territory bonus
        self.balance_focus = 1.0        # Equal kill and statue priorities
        
        # Equipment (likely versatile/balanced loadout)
        self.preferred_equipment = {
            "arms": "Pistol",      # Balanced ranged weapon
            "tail": "Unknown",     # Possibly utility
            "misc": "Unknown"      # Possibly balanced support
        }
        
    def get_action(self, observation):
        """
        The Peacemaker decision making - balanced control
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
        
        return self._peacemaker_strategy(
            self_hp, closest_enemy, enemy_statue_distance, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _peacemaker_strategy(self, hp, closest_enemy, statue_distance,
                           has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        The Peacemaker's balanced control strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_damaged = health_ratio < 0.6  # Moderate threshold
        
        # BALANCED CONTROL STRATEGY
        
        # 1. Team coordination assessment
        team_support_needed = False
        if len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            furthest_friend = max([d for d in friend_distances if d > 0] or [0])
            team_spread = furthest_friend - closest_friend
            
            if team_spread > 30 or closest_friend > 35:
                team_support_needed = True
                
        # 2. Balanced target prioritization (equal 75 point bonuses)
        enemy_priority = False
        statue_priority = False
        
        if closest_enemy < 35 and (not is_damaged or health_ratio > 0.4):
            enemy_priority = True
        if statue_distance < 40 and closest_enemy > 20:
            statue_priority = True
            
        # Choose based on tactical situation
        if enemy_priority and statue_priority:
            # Both available - choose based on team needs
            if team_support_needed:
                enemy_priority = True  # Support team with enemy focus
            else:
                statue_priority = True  # Push objective
                
        # 3. Enemy engagement (balanced approach)
        if enemy_priority:
            if closest_enemy > 20:
                # Advance with team coordination
                move_x = 0.6
                chase_focus = 0.7
                focus_target = 5
                
                # Coordinate with team
                if len(friend_distances) > 0:
                    closest_friend = min([d for d in friend_distances if d > 0] or [999])
                    if closest_friend < 15:
                        # Good team coordination - synchronized attack
                        chase_focus = 0.8
                        
            elif closest_enemy <= 20:
                # Engage at medium range
                focus_target = 5
                chase_focus = 0.5  # Moderate chase
                
                if has_ranged and closest_enemy > 8:
                    cast_slot = 2  # Ranged engagement
                elif has_melee and closest_enemy < 12:
                    cast_slot = 1  # Melee when close
                    
        # 4. Statue objective (balanced with enemy focus)
        elif statue_priority:
            if statue_distance > 25:
                # Advance on statue with team
                move_x = 0.5
                focus_target = 4
                
                # Ensure team support
                if len(friend_distances) > 0:
                    closest_friend = min([d for d in friend_distances if d > 0] or [999])
                    if closest_friend > 25:
                        # Wait for team support
                        move_x = 0.3
                        
            else:
                # Attack statue while monitoring threats
                focus_target = 4
                if has_ranged:
                    cast_slot = 2
                elif has_melee:
                    cast_slot = 1
                    
                # Stay alert for enemy interference
                if closest_enemy < 25:
                    # Enemy approaching - consider switching focus
                    focus_target = 5
                    
        # 5. Territory control (45 point bonus)
        elif closest_enemy > 40 and statue_distance > 45:
            # Push territory with team
            move_x = 0.6
            
            # Maintain team cohesion
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend > 20:
                    move_x = 0.4  # Slower advance to stay together
                    
        # 6. Team support positioning
        if team_support_needed and not (enemy_priority or statue_priority):
            # Move to support team
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend > 25:
                    move_x = 0.7  # Move to support
                elif closest_friend < 8:
                    move_x = -0.2  # Create space
                    rotate = 0.1  # Adjust position
                    
        # 7. Health management (moderate damage penalty)
        if is_damaged:
            if closest_enemy < 20:
                # Create distance while maintaining team position
                move_x = -0.4
                
                # Continue to provide support fire if possible
                if has_ranged and closest_enemy < 35:
                    cast_slot = 2
                    focus_target = 5
                    chase_focus = 0.2  # Limited chase when damaged
                    
        # 8. Weapon optimization
        if has_ranged and closest_enemy < 35:
            cast_slot = 2  # Primary weapon choice
        elif has_melee and closest_enemy < 10 and health_ratio > 0.5:
            cast_slot = 1  # Melee when safe and close
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["Pistol", None, None],  # Balanced ranged weapon
            "rewardFunction": {
                "damageEnemyStatue": 0.35,       # Moderate statue damage
                "damageEnemyUnit": 0.45,         # Higher unit damage focus
                "killEnemyStatue": 0.75,         # Balanced kill priority
                "killEnemyUnit": 0.75,           # Balanced kill priority
                "timeSpentAwayTerritory": 0.45,  # Moderate territory bonus
                "damageTaken": -0.35,            # Moderate damage penalty
                "friendlyFire": -0.5,            # Friendly fire penalty
                "fallDamageTaken": -0.9,         # Avoid fall damage
                "teamSpirit": 0.8,               # High team coordination
                "timeScaling": 0.0               # No time pressure
            },
            "primaryColor": "#9370DB",           # Medium purple (balance/wisdom)
            "secondaryColor": "#F0F8FF"          # Alice blue (peace/calm)
        }

def test_the_peacemaker():
    """Test The Peacemaker brain"""
    print("☮️ TESTING THE PEACEMAKER BRAIN")
    print("=" * 33)
    
    brain = ThePeacemakerBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # The Peacemaker
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
    print(f"\n☮️ The Peacemaker Average Reward: {avg_reward:.2f}")
    print("Strategy: Balanced control, team coordination, equal priorities")
    
    return results

if __name__ == "__main__":
    test_the_peacemaker()
