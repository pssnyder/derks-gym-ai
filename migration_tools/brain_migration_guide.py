"""
Brain Migration Guide: Recreating Steam Game Strategies in Derk Gym
==================================================================

Since you can't directly import brains from the Steam game, this guide helps you
recreate your successful strategies in the RL environment.

Step 1: Document Your Steam Game Strategies
------------------------------------------
For each of your successful "brains" from Steam, document:

1. **Combat Strategies**:
   - How did they prioritize targets?
   - When did they engage vs retreat?
   - How did they use different weapons?

2. **Team Coordination**:
   - Did they stick together or spread out?
   - How did they support teammates?
   - Did they have specific roles (tank, damage, support)?

3. **Map Control**:
   - Did they focus on territory control?
   - How aggressive were they toward enemy base?
   - Did they defend or attack more?

4. **Equipment Preferences**:
   - Which weapon combinations worked best?
   - Did they prefer ranged or melee?
   - How did they use special abilities?

Step 2: Implement Strategies as Rule-Based Behaviors
---------------------------------------------------
Before training with RL, implement your strategies as rule-based agents.
This gives you a baseline to improve upon.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np
import math

class RuleBasedBrain:
    """
    A rule-based implementation of a strategy from your Steam game brains.
    This serves as a starting point for RL training.
    """
    
    def __init__(self, strategy_name="Aggressive", personality_traits=None):
        self.strategy_name = strategy_name
        self.traits = personality_traits or {
            'aggression': 0.7,      # 0-1: How aggressive toward enemies
            'team_focus': 0.5,      # 0-1: How much to prioritize team support
            'risk_tolerance': 0.6,   # 0-1: Willingness to take risks
            'weapon_preference': 'balanced',  # 'ranged', 'melee', 'balanced'
        }
        
    def get_action(self, observation):
        """
        Convert your Steam game strategy into actions for Derk Gym.
        Modify this based on your successful brain behaviors.
        """
        obs = observation
        
        # Extract key information
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
        
        # Team distances
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
        
        # Decision making based on your strategy
        action = self._make_strategic_decision(
            self_hp, closest_enemy, has_focus, focus_hp,
            has_ranged, has_melee, friend_distances
        )
        
        return action
    
    def _make_strategic_decision(self, hp, closest_enemy, has_focus, focus_hp, 
                               has_ranged, has_melee, friend_distances):
        """
        Implement your brain's decision-making logic here.
        This is where you recreate your successful Steam strategies.
        """
        
        # Example strategy - modify based on your successful brains:
        
        # 1. Health-based decisions
        health_ratio = hp / 100.0
        is_low_health = health_ratio < 0.3
        
        # 2. Targeting decisions
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0  # 0=no cast, 1-3=abilities
        focus_target = 0  # 0=no change
        
        if self.strategy_name == "Aggressive":
            # Aggressive strategy: Always push forward, focus nearest enemy
            if closest_enemy < 50 and not is_low_health:
                chase_focus = 1.0  # Chase the focused target
                focus_target = 5   # Focus on enemy 1 (adjust based on which is closest)
                
                # Use abilities aggressively
                if has_melee and closest_enemy < 20:
                    cast_slot = 1  # Use first ability when close
                elif has_ranged and closest_enemy < 40:
                    cast_slot = 2  # Use ranged ability
                    
            elif is_low_health:
                # Retreat when low health
                move_x = -0.5  # Move backward
                focus_target = 2   # Focus on teammate for potential healing
                
        elif self.strategy_name == "Defensive":
            # Defensive strategy: Stay near team, protect base
            avg_friend_distance = np.mean([d for d in friend_distances if d > 0] or [0])
            
            if avg_friend_distance > 30:
                # Too far from team, move closer
                chase_focus = 0.5
                focus_target = 2  # Focus on teammate
            elif closest_enemy < 25:
                # Enemy is close, engage defensively
                move_x = 0.2  # Slight forward movement
                rotate = 0.1  # Slight rotation for positioning
                cast_slot = 1 if has_melee else 2
                
        elif self.strategy_name == "Support":
            # Support strategy: Focus on team healing and assistance
            focus_target = 2  # Usually focus on teammates
            
            # Look for teammates who need healing
            # (You'd need to implement teammate health detection)
            
            if closest_enemy < 30:
                # Stay at medium range, use ranged attacks
                move_x = -0.2  # Stay back slightly
                if has_ranged:
                    cast_slot = 2
                    
        # Add your other successful strategies here...
        
        return (move_x, rotate, chase_focus, cast_slot, focus_target)

class StrategyLibrary:
    """
    Collection of different strategies you can recreate from your Steam brains.
    """
    
    @staticmethod
    def create_aggressive_brain():
        return RuleBasedBrain("Aggressive", {
            'aggression': 0.9,
            'team_focus': 0.3,
            'risk_tolerance': 0.8,
            'weapon_preference': 'melee'
        })
    
    @staticmethod
    def create_defensive_brain():
        return RuleBasedBrain("Defensive", {
            'aggression': 0.3,
            'team_focus': 0.8,
            'risk_tolerance': 0.2,
            'weapon_preference': 'ranged'
        })
    
    @staticmethod
    def create_support_brain():
        return RuleBasedBrain("Support", {
            'aggression': 0.4,
            'team_focus': 0.9,
            'risk_tolerance': 0.3,
            'weapon_preference': 'balanced'
        })
    
    @staticmethod
    def create_balanced_brain():
        return RuleBasedBrain("Balanced", {
            'aggression': 0.6,
            'team_focus': 0.6,
            'risk_tolerance': 0.5,
            'weapon_preference': 'balanced'
        })

def test_strategy(brain, num_episodes=5):
    """
    Test a rule-based strategy to see how well it performs.
    Use this to validate your recreated strategies.
    """
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    total_rewards = []
    
    for episode in range(num_episodes):
        observation_n = env.reset()
        episode_reward = 0
        
        while True:
            # Get actions from your brain for all agents
            actions = []
            for i in range(env.n_agents):
                action = brain.get_action(observation_n[i])
                actions.append(action)
                
            observation_n, reward_n, done_n, info = env.step(np.array(actions))
            
            if all(done_n):
                episode_reward = np.mean(env.total_reward)
                break
                
        total_rewards.append(episode_reward)
        print(f"Episode {episode + 1}: Reward = {episode_reward:.2f}")
    
    avg_reward = np.mean(total_rewards)
    print(f"\nAverage reward for {brain.strategy_name} strategy: {avg_reward:.2f}")
    
    env.close()
    return avg_reward

if __name__ == "__main__":
    print("Testing different strategies recreated from Steam game...")
    
    # Test each strategy
    strategies = [
        StrategyLibrary.create_aggressive_brain(),
        StrategyLibrary.create_defensive_brain(),
        StrategyLibrary.create_support_brain(),
        StrategyLibrary.create_balanced_brain()
    ]
    
    for brain in strategies:
        print(f"\n{'='*50}")
        print(f"Testing {brain.strategy_name} Strategy")
        print(f"{'='*50}")
        test_strategy(brain, num_episodes=3)
