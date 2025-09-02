"""
Angrrry Peanut - Hyper-Aggressive Fighter (Peanut Class)
=====================================================
Class: Peanut Class Derkling  
Role: Hyper-aggressive fighter
Compatible: Spicy Peanut, Nightrider Peanut, Poonut

EXTRACTED STEAM CONFIGURATION:
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np

class AngrrryPeanutBrain:
    """
    Angrrry Peanut - The rage-fueled berserker
    
    Steam Game Bounties (extracted from screenshot):
    - Damage enemy statue: 10 per hitpoint
    - Damage enemy unit: 10 per hitpoint
    - Kill enemy statue: 200 points
    - Kill enemy unit: 200 points  
    - Stay in enemy territory: 100 every 5 seconds
    - Damage taken: -10 per hitpoint
    - Friendly fire: -50 per hitpoint
    - Take fall damage: -90 per hitpoint
    - Manual bonus: -1000 points
    - Tie: -10 points
    - Time scaling: 0%
    
    Strategy: Maximum aggression, kill-focused, territory domination, minimal damage concern
    """
    
    def __init__(self):
        self.name = "Angrrry Peanut"
        self.brain_class = "peanut"
        self.role = "hyper_aggressive"
        self.compatible_with = ["Spicy Peanut", "Nightrider Peanut", "Poonut"]
        
        # Behavioral traits
        self.aggression = 1.0           # Maximum aggression
        self.team_focus = 0.8           # High team coordination for peanut gang
        self.risk_tolerance = 0.9       # Very high risk tolerance (low damage penalty)
        self.territory_preference = "ultra_aggressive"  # Highest territory bonus (100)
        self.kill_obsession = 1.0       # Extremely high kill focus (200 points each)
        
        # Equipment (likely maximum damage setup)
        self.preferred_equipment = {
            "arms": "BloodClaws",  # Maximum damage melee
            "tail": "Unknown",     # Possibly mobility for gap closing
            "misc": "Unknown"      # Possibly offensive enhancement
        }
        
    def get_action(self, observation):
        """
        Angrrry Peanut decision making - pure berserker mode
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
        
        # Peanut gang coordination
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
        
        return self._angrrry_peanut_strategy(
            self_hp, closest_enemy, enemy_statue_distance, has_focus, focus_hp,
            friend_distances, has_ranged, has_melee
        )
    
    def _angrrry_peanut_strategy(self, hp, closest_enemy, statue_distance,
                               has_focus, focus_hp, friend_distances, has_ranged, has_melee):
        """
        Angrrry Peanut's berserker strategy
        """
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        health_ratio = hp / 100.0
        # Only retreat when near death (very low damage penalty)
        is_near_death = health_ratio < 0.15
        
        # BERSERKER STRATEGY - KILL EVERYTHING
        
        # 1. HIGHEST PRIORITY: Enemy kills (200 points each!)
        if closest_enemy < 60 and not is_near_death:
            # CHARGE! Maximum aggression
            move_x = 1.0
            chase_focus = 1.0
            focus_target = 5  # Always focus closest enemy
            
            # Peanut gang coordination - attack together
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend < 25:
                    # Peanut gang is together - SWARM ATTACK!
                    move_x = 1.0
                    chase_focus = 1.0
                    
            # Weapon selection - prefer melee for kills
            if closest_enemy < 8 and has_melee:
                cast_slot = 1  # MELEE KILL!
            elif closest_enemy < 20 and has_ranged:
                cast_slot = 2  # Soften them up
            elif closest_enemy > 20:
                # Still charging - use ranged while advancing
                if has_ranged:
                    cast_slot = 2
                    
        # 2. Statue kills (200 points - also high priority)
        elif statue_distance < 50 and closest_enemy > 30:
            # Charge the statue when no enemies nearby
            move_x = 1.0
            focus_target = 4  # Focus enemy statue
            
            # Coordinate statue assault with peanut gang
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend < 20:
                    # Gang attack on statue
                    if has_melee and statue_distance < 12:
                        cast_slot = 1  # Melee the statue
                    elif has_ranged:
                        cast_slot = 2  # Ranged assault
                        
        # 3. Territory domination (100 points - highest territory bonus!)
        elif closest_enemy > 40 and statue_distance > 40:
            # INVADE enemy territory with extreme prejudice
            move_x = 1.0
            rotate = 0.1  # Scan for victims
            
            # Keep peanut gang together for invasion
            if len(friend_distances) > 0:
                closest_friend = min([d for d in friend_distances if d > 0] or [999])
                if closest_friend > 30:
                    # Gang is scattered - regroup for invasion
                    move_x = 0.8
                elif closest_friend < 10:
                    # Too close - spread out for better coverage
                    move_x = 0.9
                    rotate = 0.05
                    
        # 4. Peanut gang tactics
        if len(friend_distances) > 0:
            closest_friend = min([d for d in friend_distances if d > 0] or [999])
            
            # Maintain peanut pack cohesion
            if closest_friend > 35 and closest_enemy > 25:
                # Gang is too spread - regroup
                move_x = 0.7
                
            elif closest_friend < 8 and closest_enemy < 20:
                # Too clustered for attack - spread for flanking
                move_x = 1.0
                rotate = 0.1
                
        # 5. Near-death behavior (only when absolutely necessary)
        if is_near_death:
            if closest_enemy < 15:
                # Final berserker charge - go down fighting!
                move_x = 1.0
                chase_focus = 1.0
                focus_target = 5
                
                if has_melee and closest_enemy < 8:
                    cast_slot = 1  # DIE FIGHTING!
                elif has_ranged:
                    cast_slot = 2  # Rage fire
                    
            else:
                # Look for weak targets to take down
                if closest_enemy < 30:
                    move_x = 0.8
                    focus_target = 5
                    if has_ranged:
                        cast_slot = 2
                        
        # 6. Weapon optimization for maximum killing
        if has_melee and closest_enemy < 10:
            cast_slot = 1  # MELEE KILL PRIORITY
        elif has_ranged and closest_enemy < 30:
            cast_slot = 2  # Ranged to close gap
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def get_derk_gym_config(self):
        """Return Derk Gym configuration for this brain"""
        return {
            "slots": ["BloodClaws", None, None],  # Maximum damage melee
            "rewardFunction": {
                "damageEnemyStatue": 0.1,        # Very low damage focus
                "damageEnemyUnit": 0.1,          # Very low damage focus
                "killEnemyStatue": 2.0,          # MAXIMUM kill priority
                "killEnemyUnit": 2.0,            # MAXIMUM kill priority
                "timeSpentAwayTerritory": 1.0,   # Maximum territory aggression
                "damageTaken": -0.1,             # Minimal damage concern
                "friendlyFire": -0.5,            # Friendly fire penalty
                "fallDamageTaken": -0.9,         # Avoid fall damage
                "teamSpirit": 0.8,               # High peanut gang coordination
                "timeScaling": 0.0               # No time pressure
            },
            "primaryColor": "#8B0000",           # Dark red (rage/blood)
            "secondaryColor": "#FF4500"          # Orange red (fury)
        }

def test_angrrry_peanut():
    """Test Angrrry Peanut brain"""
    print("😡 TESTING ANGRRRY PEANUT BRAIN")
    print("=" * 33)
    
    brain = AngrrryPeanutBrain()
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    results = []
    
    for episode in range(5):
        observation_n = env.reset()
        episode_reward = 0
        episode_length = 0
        
        while True:
            actions = []
            for i in range(env.n_agents):
                if i == 0:  # Angrrry Peanut
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
    print(f"\n😡 Angrrry Peanut Average Reward: {avg_reward:.2f}")
    print("Strategy: Berserker mode, maximum kills, territory domination")
    
    return results

if __name__ == "__main__":
    test_angrrry_peanut()
