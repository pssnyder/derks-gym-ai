"""
The Assaulter Player for Derk Starter Kit
========================================

Adapted from The Assaulter brain profile for use with the
starter kit's DerkPlayer architecture.
"""

import numpy as np

class DerkPlayer:
    """
    The Assaulter team player for starter kit
    """

    def __init__(self, n_agents, action_space):
        """
        Parameters:
         - n_agents: TOTAL number of agents being controlled (= #arenas * #agents per arena)
        """
        self.n_agents = n_agents
        self.action_space = action_space
        self.name = "The Assaulter"
        
        # Behavioral traits from Steam analysis
        self.aggression = 1.0           # Maximum aggression
        self.team_focus = 0.6           # Moderate team coordination
        self.risk_tolerance = 0.8       # High risk tolerance
        self.territory_preference = "aggressive"  # Enemy territory focus
        
        print(f"⚔️ The Assaulter Player initialized for {n_agents} agents")
        print(f"   Strategy: Pure aggressive assault, territory domination")
        print(f"   Aggression: {self.aggression}, Team Focus: {self.team_focus}")

    def get_derk_gym_config(self):
        """Return Derk Gym configuration for The Assaulter"""
        return {
            "slots": ["Talons", "Cripplers", "Shell"],  # Melee assault, crippling attacks, defense
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

    def signal_env_reset(self, obs):
        """
        env.reset() was called
        """
        print(f"⚔️ Environment reset - The Assaulter ready for combat!")

    def take_action(self, env_step_ret):
        """
        The Assaulter action logic adapted for starter kit
        
        Parameters:
         - env_step_ret: whatever env.step() returned (obs_n, rew_n, done_n, info_n)

        Returns: action for each agent for each arena
        """
        obs_n, rew_n, done_n, info_n = env_step_ret
        
        actions = []
        
        for i in range(self.n_agents):
            obs = obs_n[i] if i < len(obs_n) else obs_n[0]
            action = self._get_assaulter_action(obs)
            actions.append(action)
        
        return actions
    
    def _get_assaulter_action(self, observation):
        """
        The Assaulter decision making - pure aggressive assault
        
        Parse observation to extract:
        - Health status
        - Enemy positions
        - Team positions  
        - Equipment status
        """
        
        # Parse observation (64-dimensional vector)
        try:
            self_hp = observation[0] * 100  # Convert normalized to 0-100
            
            # Enemy analysis
            enemy_distances = []
            for j in range(1, 4):  # Approximate enemy distance indices
                if j < len(observation):
                    dist = observation[j] * 50  # Scale to game units
                    if dist > 0:
                        enemy_distances.append(dist)
            
            closest_enemy = min(enemy_distances) if enemy_distances else 999
            
            # Statue distance (approximate)
            enemy_statue_dist = observation[7] * 50 if len(observation) > 7 else 999
            
            # Team coordination
            friend_distances = []
            for j in range(4, 6):  # Approximate friend distance indices
                if j < len(observation):
                    dist = observation[j] * 50
                    if dist > 0:
                        friend_distances.append(dist)
            
            # Equipment status
            has_weapon = len(observation) > 10 and observation[10] > 0.5
            
        except (IndexError, ValueError):
            # Fallback values
            self_hp = 100
            closest_enemy = 50
            enemy_statue_dist = 999
            friend_distances = []
            has_weapon = True
        
        return self._assaulter_strategy(self_hp, closest_enemy, enemy_statue_dist, 
                                      friend_distances, has_weapon)
    
    def _assaulter_strategy(self, hp, closest_enemy, statue_distance, 
                          friend_distances, has_weapon):
        """
        The Assaulter's pure aggression strategy
        
        Returns tuple: (MoveX, Rotate, ChaseFocus, CastingSlot, ChangeFocus)
        """
        
        health_ratio = hp / 100.0
        is_critical_health = health_ratio < 0.25
        
        # Default aggressive stance
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        # PURE ASSAULT STRATEGY
        
        # 1. PRIORITY: Enemy elimination 
        if closest_enemy < 60 and not is_critical_health:
            if closest_enemy > 30:
                # Charge at enemy
                move_x = 1.0  # Full speed assault
                chase_focus = 1.0
                focus_target = 5  # Focus closest enemy
                
            elif closest_enemy > 15:
                # Combat range - full assault
                move_x = 0.7
                chase_focus = 1.0
                focus_target = 5
                
                # Use weapon aggressively
                if has_weapon:
                    cast_slot = 1  # Primary assault ability
                    
            else:
                # Close quarters - finish them
                chase_focus = 1.0
                focus_target = 5
                
                if has_weapon:
                    cast_slot = 1  # Melee finish
                else:
                    move_x = 0.5  # Stay in close combat
                    
        # 2. Statue assault (secondary priority)
        elif statue_distance < 80 and not is_critical_health:
            if statue_distance > 40:
                # Advance on statue
                move_x = 0.8
                focus_target = 4  # Focus enemy statue
                
            else:
                # Assault the statue
                focus_target = 4
                if has_weapon:
                    cast_slot = 1  # Attack statue
                    
        # 3. Territory domination / search and destroy
        elif closest_enemy > 60:
            # Push deep into enemy territory
            move_x = 0.9
            rotate = 0.2  # Scan for targets
            
            # Team coordination for group assault
            if friend_distances:
                avg_friend_dist = np.mean(friend_distances)
                if avg_friend_dist > 40:
                    # Team spread out - maintain aggressive advance
                    move_x = 0.8
                elif avg_friend_dist < 15:
                    # Team bunched up - spread out for better assault
                    move_x = 0.6
                    rotate = 0.3
                    
        # 4. Team assault coordination
        if friend_distances and not is_critical_health:
            closest_friend = min(friend_distances)
            if closest_friend < 20 and closest_enemy < 40:
                # Perfect for coordinated assault
                move_x = 1.0
                chase_focus = 1.0
                focus_target = 5
                
                if has_weapon:
                    cast_slot = 1
                    
        # 5. Combat retreat (only when critical)
        if is_critical_health:
            if closest_enemy < 30:
                # Tactical withdrawal
                move_x = -0.5
                focus_target = 1  # Focus on home statue
                
                # But still fight if cornered
                if closest_enemy < 15 and has_weapon:
                    cast_slot = 1
                    focus_target = 5
            else:
                # Maintain pressure even when hurt
                if has_weapon and closest_enemy < 50:
                    cast_slot = 1
                    focus_target = 5
                    chase_focus = 0.4
                    
        # 6. Maximum aggression when healthy
        if health_ratio > 0.7:
            if closest_enemy < 50:
                chase_focus = min(1.0, chase_focus + 0.3)
                move_x = min(1.0, move_x + 0.2)
                
        # 7. Weapon usage - prefer aggressive engagement
        if has_weapon and closest_enemy < 40:
            cast_slot = max(1, cast_slot)  # Always use weapon when enemies in range
            
        # Ensure values are in valid ranges
        move_x = np.clip(move_x, -1.0, 1.0)
        rotate = np.clip(rotate, -1.0, 1.0)
        chase_focus = np.clip(chase_focus, 0.0, 1.0)
        cast_slot = int(np.clip(cast_slot, 0, 3))
        focus_target = int(np.clip(focus_target, 0, 7))
        
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
