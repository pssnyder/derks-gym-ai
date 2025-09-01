"""
The Engineer - Support/Defense Specialist (Testing Class)
======================================================
Class: Testing Class Derkling  
Role: Support and defensive specialist
Compatible: Unknown (testing classification)

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class TheEngineerBrain:
    """
    The Engineer - Defensive support specialist
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 20 per hitpoint
    - Damage enemy unit: 25 per hitpoint
    - Kill enemy statue: 110 points
    - Kill enemy unit: 60 points  
    - Stay in enemy territory: 20 every 5 seconds
    - Damage taken: -50 per hitpoint
    - Friendly fire: -50 per hitpoint
    - Take fall damage: -90 per hitpoint
    - Manual bonus: -1000 points
    - Tie: -10 points
    - Time scaling: 0%
    
    Strategy: Statue-focused defense, selective engagement, support role
    """
    
    def __init__(self):
        self.name = "The Engineer"
        self.brain_class = "testing"
        self.role = "support_defense"
        self.compatible_with = "unknown"
        
        # Behavioral traits
        self.aggression = 0.4           # Low-moderate aggression
        self.team_focus = 0.9           # High team support focus
        self.risk_tolerance = 0.3       # Conservative due to damage penalty
        self.territory_preference = "defensive"  # Low territory bonus
        self.structure_focus = 1.0      # High statue kill bonus (110 vs 60)
        
        # Equipment (likely defensive/support tools)
        self.preferred_equipment = {
            "arms": "Blaster",     # Defensive ranged weapon
            "tail": "Unknown",     # Possibly utility/support
            "misc": "Unknown"      # Possibly defensive
        }
        
    def get_action(self, observation):
        """
        The Engineer decision making - defensive support
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
        
        # Statue analysis (both friendly and enemy)
        enemy_statue_distance = obs[ObservationKeys.EnemyStatueDistance.value]
        # Note: FriendlyStatueDistance might not be available, using approximation
        friendly_statue_distance = 30.0  # Assume default friendly statue distance
        
        # Team positioning
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
        
        return self._engineer_strategy(
            self_hp, closest_enemy, enemy_statue_distance, friendly_statue_distance,
            has_focus, focus_hp, friend_distances, has_ranged, has_melee
        )
    
    def _engineer_strategy(self, hp, closest_enemy, enemy_statue_distance, 
                         friendly_statue_distance, has_focus, focus_hp, 
                         friend_distances, has_ranged, has_melee):
        """
        The Engineer's defensive support strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        is_damaged = health_ratio < 0.7  # Conservative threshold
        
        # DEFENSIVE SUPPORT STRATEGY
        
        # 1. PRIORITY: Friendly statue defense
        if friendly_statue_distance < 40 and closest_enemy < 35:
            # Enemies near our statue - defensive position
            if closest_enemy > 20:
                # Position between enemy and statue
                move_x = -0.3  # Move toward statue
                if has_ranged:
                    cast_slot = 2
                    focus_target = 5  # Focus closest threat
                    
            else:
                # Enemy too close to statue - defensive engagement
                focus_target = 5
                if has_ranged and closest_enemy > 8:
                    cast_slot = 2  # Ranged defense
                elif has_melee and closest_enemy < 10:
                    cast_slot = 1  # Melee last resort
                    
        # 2. Enemy statue targeting (110 point bonus - highest priority)
        elif enemy_statue_distance < 50 and closest_enemy > 25 and not is_damaged:
            # Safe approach to enemy statue
            if enemy_statue_distance > 30:
                move_x = 0.4  # Cautious advance
                focus_target = 4  # Focus enemy statue
                
                # Support team advance
                if len(friend_distances) > 0:
                    closest_friend = min([d for d in friend_distances if d > 0] or [999])
                    if closest_friend > 20:
                        # Team is ahead - provide covering fire
                        if has_ranged:
                            cast_slot = 2
                            
            else:
                # In range of statue - focused assault
                focus_target = 4
                if has_ranged:
                    cast_slot = 2  # Ranged statue damage
                elif has_melee:
                    cast_slot = 1  # Melee if necessary
                    
        # 3. Team support positioning
        elif len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            
            if closest_friend > 30:
                # Team is too far - move to support
                move_x = 0.5
                
            elif closest_friend < 10:
                # Too close - maintain spacing for effective support
                move_x = -0.2
                rotate = 0.1  # Adjust angle for support
                
            # Provide covering fire for team
            if closest_enemy < 40 and has_ranged:
                cast_slot = 2
                focus_target = 5
                chase_focus = 0.2  # Limited chase - stay in support role
                
        # 4. Selective enemy engagement (only when advantageous)
        elif closest_enemy < 30 and not is_damaged:
            # Engage only with clear advantage
            if closest_enemy > 15:
                # Optimal range for support fire
                if has_ranged:
                    cast_slot = 2
                    focus_target = 5
                    chase_focus = 0.1  # Minimal chase
                    
            else:
                # Too close - create distance
                move_x = -0.4
                if has_ranged:
                    cast_slot = 2  # Fighting withdrawal
                    
        # 5. Health management (conservative due to -50 damage penalty)
        if is_damaged:
            if closest_enemy < 25:
                # Retreat to safe position
                move_x = -0.6
                
                # Move toward friendly statue for protection
                if friendly_statue_distance > 20:
                    move_x = -0.4  # Toward statue
                    
            else:
                # Safe distance - provide long-range support
                if has_ranged and closest_enemy < 45:
                    cast_slot = 2
                    focus_target = 5
                    
        # 6. Weapon optimization for support role
        if has_ranged and closest_enemy < 40:
            # Prefer ranged for support role
            cast_slot = 2
        elif has_melee and closest_enemy < 8 and health_ratio > 0.5:
            # Only melee when healthy and very close
            cast_slot = 1
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["Blaster", None, None],  # Defensive ranged weapon
            "rewardFunction": {
                "damageEnemyStatue": 0.2,        # Low statue damage focus
                "damageEnemyUnit": 0.25,         # Low unit damage focus
                "killEnemyStatue": 1.1,          # High statue kill priority
                "killEnemyUnit": 0.6,            # Moderate unit kill
                "timeSpentAwayTerritory": 0.2,   # Low territory bonus
                "damageTaken": -0.5,             # Moderate damage avoidance
                "friendlyFire": -0.5,            # Friendly fire penalty
                "fallDamageTaken": -0.9,         # Avoid fall damage
                "teamSpirit": 0.9,               # High team support
                "timeScaling": 0.0               # No time pressure
            },
            "primaryColor": "#4169E1",           # Royal blue (support/reliability)
            "secondaryColor": "#FFD700"          # Gold (engineering/precision)
        }

def test_the_engineer():
    """Test The Engineer brain"""
    print("🔧 TESTING THE ENGINEER BRAIN")
    print("=" * 30)
    
    brain = TheEngineerBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # The Engineer
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
    print(f"\n🔧 The Engineer Average Reward: {avg_reward:.2f}")
    print("Strategy: Defensive support, statue-focused, team coordination")
    
    return results

if __name__ == "__main__":
    test_the_engineer()
