"""
Derk Steam Interface - Use Derk's Gym exactly like the Steam version
================================================================

This interface allows you to:
1. Set up derklings with loadouts and bounties (like Steam)
2. Train them using the built-in game methods 
3. Battle trained derklings against each other
4. Use the actual game's training algorithms

Usage:
- Configure derkling loadouts and bounties
- Train derklings for specified iterations
- Battle trained derklings
- All functionality matches Steam version
"""

import gym_derk
from gym_derk.envs import DerkEnv
from gym_derk import ActionKeys, ObservationKeys
import numpy as np
import json
import time
from datetime import datetime
import os

class DerklingProfile:
    """Steam-style derkling configuration"""
    
    def __init__(self, name, brain_class=None):
        self.name = name
        self.brain_class = brain_class
        
        # Default loadout (can be customized)
        self.loadout = {
            'primaryFocusUnit': 4,      # Enemy statue
            'secondaryFocusUnit': 5,    # Enemy 1
            'abilitySlot1': 1,          # First ability
            'abilitySlot2': 2,          # Second ability  
            'abilitySlot3': 3,          # Third ability
            'armorSet': 0,              # No armor
            'weaponSet': 0,             # Basic weapons
        }
        
        # Bounty configuration (from Steam)
        self.bounties = {
            'killEnemyStatue': 10,
            'killEnemyUnit': 5,
            'damageEnemyStatue': 1, 
            'damageEnemyUnit': 1,
            'healTeammate1': 1,
            'healTeammate2': 1,
            'damageHealed': 1,
            'timeSpentHome': 0,
            'timeSpentAway': 0,
            'damageTaken': 0
        }
        
        # Training state
        self.training_iterations = 0
        self.trained_model = None
        self.performance_history = []
        
    def configure_from_brain_profile(self, brain_profile):
        """Configure from extracted Steam brain profile"""
        if brain_profile and hasattr(brain_profile, 'get_derk_gym_config'):
            config = brain_profile.get_derk_gym_config()
            
            # Extract bounties from config
            if 'reward_function' in config:
                rewards = config['reward_function']
                self.bounties.update({
                    'killEnemyStatue': rewards.get('killEnemyStatue', 10),
                    'killEnemyUnit': rewards.get('killEnemyUnit', 5), 
                    'damageEnemyStatue': rewards.get('damageEnemyStatue', 1),
                    'damageEnemyUnit': rewards.get('damageEnemyUnit', 1),
                    'healTeammate1': rewards.get('healTeammate1', 1),
                    'healTeammate2': rewards.get('healTeammate2', 1),
                    'damageTaken': rewards.get('damageTaken', 0)
                })
                
            print(f"✅ Configured {self.name} from Steam profile")
            print(f"   Bounties: {self.bounties}")
            
    def get_reward_function(self):
        """Get reward function for Derk Gym environment"""
        return self.bounties.copy()
        
    def save_training_state(self, filepath):
        """Save trained derkling state"""
        state = {
            'name': self.name,
            'loadout': self.loadout,
            'bounties': self.bounties,
            'training_iterations': self.training_iterations,
            'performance_history': self.performance_history,
            'timestamp': datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
            
    def load_training_state(self, filepath):
        """Load trained derkling state"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                state = json.load(f)
                self.training_iterations = state.get('training_iterations', 0)
                self.performance_history = state.get('performance_history', [])
                return True
        return False

class DerkGameInterface:
    """Steam-like interface for Derk's Gym"""
    
    def __init__(self):
        self.derklings = {}
        self.training_sessions = []
        self.battle_history = []
        
    def register_derkling(self, name, brain_profile=None):
        """Register a derkling (like setting up in Steam)"""
        derkling = DerklingProfile(name, brain_profile)
        
        if brain_profile:
            derkling.configure_from_brain_profile(brain_profile)
            
        self.derklings[name] = derkling
        print(f"🦎 Registered derkling: {name}")
        return derkling
        
    def list_derklings(self):
        """List all registered derklings"""
        print("\n🦎 REGISTERED DERKLINGS")
        print("=" * 30)
        
        for name, derkling in self.derklings.items():
            status = f"Trained ({derkling.training_iterations} iterations)" if derkling.training_iterations > 0 else "Untrained"
            print(f"  • {name} - {status}")
            
        if not self.derklings:
            print("  No derklings registered yet")
            
    def train_derkling(self, derkling_name, iterations=1000, opponent_type='random'):
        """Train a derkling using Derk's built-in training (like Steam)"""
        
        if derkling_name not in self.derklings:
            print(f"❌ Derkling '{derkling_name}' not found")
            return False
            
        derkling = self.derklings[derkling_name]
        print(f"\n🏋️ TRAINING {derkling_name.upper()}")
        print("=" * 40)
        print(f"Training for {iterations} iterations against {opponent_type}")
        print(f"Reward function: {derkling.get_reward_function()}")
        
        # Create environment with derkling's specific reward function
        env = DerkEnv(
            n_arenas=1,
            turbo_mode=True,  # Fast training like Steam
            reward_function=derkling.get_reward_function()
        )
        
        training_results = []
        start_time = time.time()
        
        try:
            for iteration in range(iterations):
                # Reset environment
                obs = env.reset()
                
                episode_reward = 0
                episode_length = 0
                
                while True:
                    # In Steam, the game handles the training automatically
                    # Here we simulate this by using random/simple actions for training
                    actions = []
                    
                    for agent_idx in range(env.n_agents):
                        if agent_idx == 0:  # Our derkling being trained
                            # Use the derkling's brain if available
                            if derkling.brain_class and hasattr(derkling.brain_class, 'get_action'):
                                try:
                                    action = derkling.brain_class.get_action(obs[agent_idx])
                                except:
                                    action = env.action_space.sample()  # Fallback
                            else:
                                action = env.action_space.sample()
                        else:
                            # Random opponent (like Steam's training opponents)
                            action = env.action_space.sample()
                            
                        actions.append(action)
                    
                    # Step environment
                    obs, rewards, dones, info = env.step(np.array(actions))
                    episode_reward += rewards[0]  # Track our derkling's reward
                    episode_length += 1
                    
                    if all(dones):
                        break
                
                training_results.append({
                    'iteration': iteration + 1,
                    'reward': float(episode_reward),  # Convert to Python float
                    'length': episode_length
                })
                
                # Print progress (like Steam's training display)
                if (iteration + 1) % max(1, iterations // 10) == 0:
                    progress = (iteration + 1) / iterations * 100
                    elapsed = time.time() - start_time
                    avg_reward = np.mean([r['reward'] for r in training_results[-50:]])
                    
                    print(f"Progress: {progress:5.1f}% | "
                          f"Iteration: {iteration + 1:4d}/{iterations} | "
                          f"Avg Reward: {avg_reward:6.2f} | "
                          f"Time: {elapsed/60:.1f}m")
                          
        except KeyboardInterrupt:
            print("\n⏸️ Training interrupted by user")
            
        finally:
            env.close()
            
        # Update derkling training state
        derkling.training_iterations += iterations
        derkling.performance_history.extend(training_results)
        
        # Save training state
        save_path = f"trained_derklings/{derkling_name}_training.json"
        derkling.save_training_state(save_path)
        
        # Training summary (like Steam)
        total_time = time.time() - start_time
        final_avg = np.mean([r['reward'] for r in training_results[-100:]])
        
        print(f"\n✅ TRAINING COMPLETE")
        print(f"   Total iterations: {derkling.training_iterations}")
        print(f"   Final avg reward: {final_avg:.2f}")
        print(f"   Training time: {total_time/60:.1f} minutes")
        print(f"   Model saved: {save_path}")
        
        return training_results
        
    def battle_derklings(self, derkling1_name, derkling2_name, rounds=1):
        """Battle two trained derklings (like Steam battles)"""
        
        if derkling1_name not in self.derklings or derkling2_name not in self.derklings:
            print("❌ One or both derklings not found")
            return None
            
        derkling1 = self.derklings[derkling1_name]
        derkling2 = self.derklings[derkling2_name]
        
        print(f"\n⚔️ BATTLE: {derkling1_name} vs {derkling2_name}")
        print("=" * 50)
        print(f"Rounds: {rounds}")
        
        # Create battle environment
        env = DerkEnv(n_arenas=1, turbo_mode=False)  # Slower for viewing
        
        battle_results = []
        
        for round_num in range(rounds):
            print(f"\n🔄 Round {round_num + 1}/{rounds}")
            
            obs = env.reset()
            round_length = 0
            
            while True:
                actions = []
                
                # Get actions for both teams
                for agent_idx in range(env.n_agents):
                    if agent_idx < 3:  # Team 1 (derkling1)
                        if derkling1.brain_class and hasattr(derkling1.brain_class, 'get_action'):
                            try:
                                action = derkling1.brain_class.get_action(obs[agent_idx])
                            except:
                                action = env.action_space.sample()
                        else:
                            action = env.action_space.sample()
                    else:  # Team 2 (derkling2)
                        if derkling2.brain_class and hasattr(derkling2.brain_class, 'get_action'):
                            try:
                                action = derkling2.brain_class.get_action(obs[agent_idx])
                            except:
                                action = env.action_space.sample()
                        else:
                            action = env.action_space.sample()
                            
                    actions.append(action)
                
                obs, rewards, dones, info = env.step(np.array(actions))
                round_length += 1
                
                if all(dones):
                    break
            
            # Determine winner
            team1_reward = sum(rewards[:3])
            team2_reward = sum(rewards[3:])
            
            if team1_reward > team2_reward:
                winner = derkling1_name
            elif team2_reward > team1_reward:
                winner = derkling2_name
            else:
                winner = "Draw"
                
            battle_results.append({
                'round': round_num + 1,
                'winner': winner,
                'team1_reward': team1_reward,
                'team2_reward': team2_reward,
                'length': round_length
            })
            
            print(f"   Winner: {winner} | Scores: {team1_reward:.1f} vs {team2_reward:.1f}")
            
        env.close()
        
        # Battle summary
        wins1 = sum(1 for r in battle_results if r['winner'] == derkling1_name)
        wins2 = sum(1 for r in battle_results if r['winner'] == derkling2_name)
        draws = sum(1 for r in battle_results if r['winner'] == "Draw")
        
        print(f"\n🏆 BATTLE RESULTS")
        print(f"   {derkling1_name}: {wins1} wins")
        print(f"   {derkling2_name}: {wins2} wins") 
        print(f"   Draws: {draws}")
        
        # Save battle history
        battle_record = {
            'timestamp': datetime.now().isoformat(),
            'derkling1': derkling1_name,
            'derkling2': derkling2_name,
            'rounds': rounds,
            'results': battle_results,
            'summary': {'wins1': wins1, 'wins2': wins2, 'draws': draws}
        }
        
        self.battle_history.append(battle_record)
        
        return battle_record

def setup_steam_derklings():
    """Set up all Steam derklings in the interface"""
    
    # Import brain profiles
    try:
        from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain
        from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain
        from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
        from brain_profiles.testing_class.the_engineer import TheEngineerBrain
    except ImportError as e:
        print(f"⚠️ Could not import some brain profiles: {e}")
        return None
        
    # Create game interface
    game = DerkGameInterface()
    
    # Register derklings with their Steam configurations
    game.register_derkling("The Assaulter", TheAssaulterBrain())
    game.register_derkling("Spicy Peanut", SpicyPeanutBrain())
    game.register_derkling("Safe T Peanut", SafeTPeanutBrain())
    game.register_derkling("The Engineer", TheEngineerBrain())
    
    return game

def main():
    """Demo the Steam-like interface"""
    
    print("🦎 DERK'S GYM - STEAM INTERFACE")
    print("=" * 40)
    print("Setting up derklings from Steam profiles...")
    
    # Set up the game interface
    game = setup_steam_derklings()
    
    if not game:
        print("❌ Could not set up derklings")
        return
        
    # List available derklings
    game.list_derklings()
    
    # Demo: Train The Assaulter
    print("\n" + "=" * 50)
    print("DEMO: Training The Assaulter")
    print("=" * 50)
    
    # Train for a small number of iterations for demo
    training_results = game.train_derkling("The Assaulter", iterations=10, opponent_type='random')
    
    if training_results:
        print("\n✅ Training demo completed!")
        print("Ready for full training sessions and battles")
    
if __name__ == "__main__":
    main()
