"""
Quick Steam Brain Migration Solution
===================================

This is a standalone solution you can run right now to start migrating
your Steam game strategies to Derk Gym.
"""

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
import numpy as np
import json
import os
from datetime import datetime

class SteamBrainRecreator:
    """Recreate your Steam game strategies as rule-based agents"""
    
    def __init__(self):
        self.strategies_file = "my_steam_brains.json"
        self.load_or_create_config()
    
    def load_or_create_config(self):
        """Load existing config or create a template"""
        if os.path.exists(self.strategies_file):
            with open(self.strategies_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Create a template with examples you can modify
            self.config = {
                "created": datetime.now().isoformat(),
                "instructions": "Modify the strategies below to match your Steam game brains",
                "strategies": {
                    "My_Aggressive_Brain": {
                        "description": "Replace this with your aggressive Steam brain behavior",
                        "aggression": 0.9,
                        "team_focus": 0.3,
                        "risk_tolerance": 0.8,
                        "preferred_range": "close",
                        "weapon_preference": "melee",
                        "retreat_health": 20,
                        "target_priority": "nearest_enemy"
                    },
                    "My_Defensive_Brain": {
                        "description": "Replace this with your defensive Steam brain behavior", 
                        "aggression": 0.3,
                        "team_focus": 0.8,
                        "risk_tolerance": 0.2,
                        "preferred_range": "medium",
                        "weapon_preference": "ranged",
                        "retreat_health": 50,
                        "target_priority": "protect_team"
                    },
                    "My_Support_Brain": {
                        "description": "Replace this with your support Steam brain behavior",
                        "aggression": 0.4,
                        "team_focus": 0.9, 
                        "risk_tolerance": 0.3,
                        "preferred_range": "medium",
                        "weapon_preference": "balanced",
                        "retreat_health": 40,
                        "target_priority": "support_teammates"
                    }
                }
            }
            self.save_config()
            print(f"Created template config file: {self.strategies_file}")
            print("Edit this file to match your Steam brain behaviors, then run again!")
    
    def save_config(self):
        """Save configuration"""
        with open(self.strategies_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_brain_from_config(self, brain_name):
        """Create a rule-based brain from config"""
        if brain_name not in self.config["strategies"]:
            print(f"Brain '{brain_name}' not found in config")
            return None
        
        config = self.config["strategies"][brain_name]
        return ConfigurableBrain(brain_name, config)
    
    def test_all_brains(self, episodes_per_brain=5):
        """Test all configured brains"""
        print("🧠 Testing Your Steam Brain Recreations")
        print("=" * 45)
        
        results = {}
        
        for brain_name in self.config["strategies"]:
            print(f"\nTesting: {brain_name}")
            brain = self.create_brain_from_config(brain_name)
            if brain:
                rewards = self.test_brain(brain, episodes_per_brain)
                avg_reward = np.mean(rewards)
                results[brain_name] = avg_reward
                print(f"Average reward: {avg_reward:.2f}")
        
        # Summary
        print(f"\n📊 RESULTS SUMMARY")
        print("=" * 30)
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        for brain_name, reward in sorted_results:
            print(f"{brain_name:20}: {reward:6.2f}")
        
        return results
    
    def test_brain(self, brain, num_episodes):
        """Test a single brain"""
        env = DerkEnv(n_arenas=1, turbo_mode=True)
        rewards = []
        
        for episode in range(num_episodes):
            observation_n = env.reset()
            
            while True:
                actions = []
                for i in range(env.n_agents):
                    action = brain.get_action(observation_n[i])
                    actions.append(action)
                    
                observation_n, reward_n, done_n, info = env.step(np.array(actions))
                
                if all(done_n):
                    break
            
            rewards.append(np.mean(env.total_reward))
        
        env.close()
        return rewards
    
    def interactive_brain_creator(self):
        """Interactive tool to create/modify brain configs"""
        print("🎮 Interactive Steam Brain Creator")
        print("=" * 40)
        
        brain_name = input("Brain name: ").strip()
        
        config = {
            "description": input("Description of this brain's behavior: "),
            "aggression": float(input("Aggression level (0.1-1.0): ") or "0.5"),
            "team_focus": float(input("Team focus (0.1-1.0): ") or "0.5"), 
            "risk_tolerance": float(input("Risk tolerance (0.1-1.0): ") or "0.5"),
            "preferred_range": input("Preferred range (close/medium/long): ") or "medium",
            "weapon_preference": input("Weapon preference (melee/ranged/balanced): ") or "balanced",
            "retreat_health": int(input("Retreat when health below: ") or "30"),
            "target_priority": input("Target priority (nearest_enemy/weakest_enemy/protect_team): ") or "nearest_enemy"
        }
        
        self.config["strategies"][brain_name] = config
        self.save_config()
        print(f"Brain '{brain_name}' saved!")
        
        # Test it
        test = input("Test this brain now? (y/n): ").lower()
        if test == 'y':
            brain = self.create_brain_from_config(brain_name)
            rewards = self.test_brain(brain, 3)
            print(f"Average reward: {np.mean(rewards):.2f}")

class ConfigurableBrain:
    """A configurable rule-based brain that matches your Steam game strategies"""
    
    def __init__(self, name, config):
        self.name = name
        self.config = config
    
    def get_action(self, observation):
        """Get action based on configured strategy"""
        obs = observation
        
        # Extract key information
        self_hp = obs[ObservationKeys.Hitpoints.value]
        
        # Enemy information
        enemy_distances = [
            obs[ObservationKeys.Enemy1Distance.value],
            obs[ObservationKeys.Enemy2Distance.value], 
            obs[ObservationKeys.Enemy3Distance.value]
        ]
        valid_enemies = [d for d in enemy_distances if d > 0]
        closest_enemy = min(valid_enemies) if valid_enemies else 999
        
        # Team information
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
        
        # Apply configured strategy
        return self._apply_strategy(
            self_hp, closest_enemy, friend_distances, has_ranged, has_melee
        )
    
    def _apply_strategy(self, hp, closest_enemy, friend_distances, has_ranged, has_melee):
        """Apply the configured strategy"""
        config = self.config
        
        # Base action values
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        # Health-based decisions
        should_retreat = hp < config["retreat_health"]
        
        if should_retreat:
            # Retreat behavior
            move_x = -0.6
            focus_target = 2  # Focus on teammate
            return (move_x, rotate, chase_focus, cast_slot, focus_target)
        
        # Engagement range decisions
        preferred_range = config["preferred_range"]
        if preferred_range == "close":
            engage_distance = 25
        elif preferred_range == "long":
            engage_distance = 45
        else:  # medium
            engage_distance = 35
        
        # Target priority
        if config["target_priority"] == "nearest_enemy" and closest_enemy < engage_distance:
            chase_focus = config["aggression"]
            focus_target = 5  # Focus on enemy
            
        elif config["target_priority"] == "protect_team":
            avg_friend_distance = np.mean([d for d in friend_distances if d > 0] or [0])
            if avg_friend_distance > 25:
                chase_focus = config["team_focus"] * 0.7
                focus_target = 2  # Move toward teammate
            elif closest_enemy < 30:
                chase_focus = config["aggression"] * 0.8
                focus_target = 5
        
        # Weapon usage based on preference and availability
        weapon_pref = config["weapon_preference"]
        
        if closest_enemy < engage_distance:
            if weapon_pref == "melee" and has_melee and closest_enemy < 20:
                cast_slot = 1
            elif weapon_pref == "ranged" and has_ranged and closest_enemy > 15:
                cast_slot = 2
            elif weapon_pref == "balanced":
                if closest_enemy < 15 and has_melee:
                    cast_slot = 1
                elif closest_enemy > 15 and has_ranged:
                    cast_slot = 2
        
        # Risk tolerance affects positioning
        if config["risk_tolerance"] < 0.4 and closest_enemy < 20:
            move_x = -0.3  # More cautious positioning
        elif config["risk_tolerance"] > 0.7:
            move_x = 0.4   # More aggressive positioning
        
        return (move_x, rotate, chase_focus, cast_slot, focus_target)

def main():
    """Main function for Steam brain migration"""
    print("🎮 Steam to Derk Gym Brain Migration Tool")
    print("=" * 45)
    
    recreator = SteamBrainRecreator()
    
    while True:
        print("\nOptions:")
        print("1. Edit brain configurations")
        print("2. Create new brain interactively")
        print("3. Test all configured brains")
        print("4. Test specific brain")
        print("5. Show current configurations")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            print(f"Edit the file: {recreator.strategies_file}")
            print("Then run option 3 to test your changes.")
            
        elif choice == "2":
            recreator.interactive_brain_creator()
            
        elif choice == "3":
            recreator.test_all_brains()
            
        elif choice == "4":
            print("Available brains:", list(recreator.config["strategies"].keys()))
            brain_name = input("Enter brain name: ").strip()
            brain = recreator.create_brain_from_config(brain_name)
            if brain:
                rewards = recreator.test_brain(brain, 5)
                print(f"Results: {rewards}")
                print(f"Average: {np.mean(rewards):.2f}")
        
        elif choice == "5":
            print("\nCurrent Brain Configurations:")
            print("=" * 40)
            for name, config in recreator.config["strategies"].items():
                print(f"\n{name}:")
                print(f"  Description: {config['description']}")
                print(f"  Aggression: {config['aggression']}")
                print(f"  Team Focus: {config['team_focus']}")
                print(f"  Weapon Pref: {config['weapon_preference']}")
                
        elif choice == "6":
            print("Migration tool closed.")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
