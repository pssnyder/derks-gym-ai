"""
Nightrider Peanut Player for Derk Starter Kit
============================================

Adapted from the Nightrider Peanut brain profile for use with the
starter kit's DerkPlayer architecture.
"""

import numpy as np

class DerkPlayer:
    """
    Nightrider Peanut team player for starter kit
    """

    def __init__(self, n_agents, action_space):
        """
        Parameters:
         - n_agents: TOTAL number of agents being controlled (= #arenas * #agents per arena)
        """
        self.n_agents = n_agents
        self.action_space = action_space
        self.name = "Nightrider Peanut"
        
        # Behavioral traits from Steam analysis
        self.aggression = 0.95          # Extremely high due to 1000 kill bounty
        self.team_focus = 0.15          # Low team support
        self.risk_tolerance = 0.85      # Higher risk tolerance
        self.kill_focus = 1.0           # Maximum kill focus
        
        print(f"🌙 Nightrider Peanut Player initialized for {n_agents} agents")
        print(f"   Strategy: Maximum kill focus, hunt priority")
        print(f"   Aggression: {self.aggression}, Risk Tolerance: {self.risk_tolerance}")

    def get_derk_gym_config(self):
        """Return Derk Gym configuration for Nightrider Peanut"""
        return {
            "slots": ["Talons", "IronButt", "VampireGland"],  # High-damage melee, defense, sustain
            "rewardFunction": {
                "damageEnemyStatue": 0.5,    # Moderate statue damage
                "damageEnemyUnit": 1.0,      # High unit damage
                "killEnemyStatue": 9.0,      # Very high statue kills
                "killEnemyUnit": 10.0,       # MAXIMUM unit kill reward!
                "damageTaken": -0.2,         # Low damage penalty (high risk tolerance)
                "healEnemy": -0.9,           # Penalty for healing enemies
                "fallDamageTaken": -1.0,     # Avoid fall damage
                "teamSpirit": 0.15,          # Low team spirit (solo hunter)
                "timeScaling": 0.0           # No time pressure
            },
            "primaryColor": "#4B0082",       # Indigo (nightrider theme)
            "secondaryColor": "#000000"      # Black
        }

    def signal_env_reset(self, obs):
        """
        env.reset() was called
        """
        print(f"🌙 Environment reset - Nightrider ready to hunt!")

    def take_action(self, env_step_ret):
        """
        Nightrider Peanut action logic adapted for starter kit
        
        Parameters:
         - env_step_ret: whatever env.step() returned (obs_n, rew_n, done_n, info_n)

        Returns: action for each agent for each arena
        """
        obs_n, rew_n, done_n, info_n = env_step_ret
        
        actions = []
        
        for i in range(self.n_agents):
            obs = obs_n[i] if i < len(obs_n) else obs_n[0]
            action = self._get_nightrider_action(obs)
            actions.append(action)
        
        return actions
    
    def _get_nightrider_action(self, observation):
        """
        Nightrider decision making - hunt and eliminate enemies
        
        From observation keys we can extract:
        - Hitpoints (self health)
        - Enemy distances  
        - Friend distances
        - Statue distances
        - Equipment status
        """
        
        # Parse observation (64-dimensional vector)
        # Key indices based on Derk Gym documentation
        try:
            self_hp = observation[0] * 100  # Convert normalized to 0-100
            
            # Enemy analysis - look for closest threats
            enemy_distances = []
            for j in range(1, 4):  # Approximate enemy distance indices
                if j < len(observation):
                    dist = observation[j] * 50  # Scale to game units
                    if dist > 0:
                        enemy_distances.append(dist)
            
            closest_enemy = min(enemy_distances) if enemy_distances else 999
            
            # Basic equipment check (approximate indices)
            has_weapon = len(observation) > 10 and observation[10] > 0.5
            
        except (IndexError, ValueError):
            # Fallback if observation parsing fails
            self_hp = 100
            closest_enemy = 50
            has_weapon = True
        
        return self._nightrider_hunt_strategy(self_hp, closest_enemy, has_weapon)
    
    def _nightrider_hunt_strategy(self, hp, closest_enemy, has_weapon):
        """
        Nightrider's hunt-focused strategy - prioritize kills above all
        
        Returns tuple: (MoveX, Rotate, ChaseFocus, CastingSlot, ChangeFocus)
        """
        
        health_ratio = hp / 100.0
        
        # Default action
        move_x = 0.0
        rotate = 0.0  
        chase_focus = 0.0
        cast_slot = 0  # 0 = don't cast, 1-3 = cast abilities
        focus_target = 0  # 0 = keep current, 1 = home statue, 2-3 = teammates, 4 = enemy statue, 5-7 = enemies
        
        # KILL-FOCUSED STRATEGY (1000 point bounty!)
        
        if closest_enemy < 50:
            # Enemy in range - begin hunt
            if closest_enemy > 25:
                # Close the gap aggressively
                move_x = 0.8
                chase_focus = 0.9
                focus_target = 5  # Focus on nearest enemy
                
            elif closest_enemy > 15:
                # Optimal combat range
                move_x = 0.5
                chase_focus = 1.0  # Full commitment
                focus_target = 5
                
                # Use weapon if available
                if has_weapon:
                    cast_slot = 1  # Use primary ability
                    
            else:
                # Close combat - finish the kill
                chase_focus = 1.0
                focus_target = 5
                
                if has_weapon:
                    cast_slot = 1  # Melee/close range attack
                else:
                    move_x = 0.3  # Stay close for basic attacks
                    
        elif closest_enemy < 100:
            # Medium range - hunt mode
            move_x = 0.6
            rotate = 0.2  # Scan for better targets
            chase_focus = 0.7
            focus_target = 5
            
        else:
            # No immediate targets - roam aggressively
            move_x = 0.5
            rotate = 0.3  # Active scanning
            chase_focus = 0.0
            
        # Health management (higher risk tolerance)
        if health_ratio < 0.3:
            # Still aggressive but more cautious
            if closest_enemy < 20:
                move_x = max(0.0, move_x - 0.3)  # Reduce forward movement
                
                # But still fight if weapon available
                if has_weapon and closest_enemy < 30:
                    cast_slot = 1
                    focus_target = 5
            
        elif health_ratio < 0.6:
            # Moderate caution - maintain aggression
            chase_focus = max(0.5, chase_focus)
            
        # Max aggression when healthy
        if health_ratio > 0.7 and closest_enemy < 40:
            chase_focus = min(1.0, chase_focus + 0.2)
            move_x = min(1.0, move_x + 0.2)
        
        # Ensure values are in valid ranges
        move_x = np.clip(move_x, -1.0, 1.0)
        rotate = np.clip(rotate, -1.0, 1.0)
        chase_focus = np.clip(chase_focus, 0.0, 1.0)
        cast_slot = int(np.clip(cast_slot, 0, 3))
        focus_target = int(np.clip(focus_target, 0, 7))
        
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
