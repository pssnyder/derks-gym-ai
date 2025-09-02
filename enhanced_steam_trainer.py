"""
Enhanced Steam Trainer with Better Environment Setup
==================================================

Based on insights from the starter kit, this version properly configures
teams and ensures visible derkling movement and interactions.
"""

import numpy as np
import json
import time
from datetime import datetime
from gym_derk.envs import DerkEnv
import copy
import random

# Import brain profiles
from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

class EnhancedSteamTrainer:
    """
    Enhanced trainer with proper team configuration and visible derkling actions
    """
    
    def __init__(self, n_arenas=2):
        self.n_arenas = n_arenas
        self.population_size = 4  # Smaller for detailed debugging
        self.generations = 5
        self.matches_per_individual = 2
        
        # Persistent environment
        self.env = None
        
        # Population
        self.population = []
        self.best_individual = None
        self.training_history = []
        
        print(f"🏟️ Enhanced Steam Trainer ({n_arenas} arenas)")
        print("=" * 50)
        print("Key improvements:")
        print("• Proper team configuration with brain profiles")
        print("• Longer episodes for meaningful interactions")
        print("• Enhanced action debugging")
        print("• Reward function validation")
        print()
    
    def initialize_environment(self):
        """Initialize environment with proper team configurations"""
        print("🌍 Creating environment with team configurations...")
        
        try:
            # Get team configurations
            safe_t_brain = SafeTPeanutBrain()
            assaulter_brain = TheAssaulterBrain()
            
            self.safe_t_config = safe_t_brain.get_derk_gym_config()
            self.assaulter_config = assaulter_brain.get_derk_gym_config()
            
            print(f"🛠️ Team configurations:")
            print(f"   Safe T Peanut:")
            print(f"     Equipment: {self.safe_t_config['slots']}")
            print(f"     Team Spirit: {self.safe_t_config['rewardFunction']['teamSpirit']}")
            print(f"     Aggression indicators: damage rewards vs healing rewards")
            
            print(f"   The Assaulter:")
            print(f"     Equipment: {self.assaulter_config['slots']}")
            print(f"     Team Spirit: {self.assaulter_config['rewardFunction']['teamSpirit']}")
            
            # Create team configurations for environment
            home_team = [self.safe_t_config, self.safe_t_config, self.safe_t_config]
            away_team = [self.assaulter_config, self.assaulter_config, self.assaulter_config]
            
            # Create environment with team configurations
            self.env = DerkEnv(
                n_arenas=self.n_arenas,
                turbo_mode=True,
                home_team=home_team,
                away_team=away_team
            )
            
            print(f"✅ Environment created with {self.n_arenas} arenas and team configs")
            return True
            
        except Exception as e:
            print(f"❌ Team configuration failed, trying basic environment: {e}")
            
            # Fallback to basic environment
            try:
                self.env = DerkEnv(
                    n_arenas=self.n_arenas,
                    turbo_mode=True
                )
                print(f"✅ Basic environment created (fallback)")
                return True
            except Exception as e2:
                print(f"❌ Environment creation completely failed: {e2}")
                return False
    
    def initialize_population(self):
        """Create initial population with diverse configurations"""
        print("🧬 Creating population...")
        
        base_brain = SafeTPeanutBrain()
        base_config = base_brain.get_derk_gym_config()
        
        for i in range(self.population_size):
            # Create variations in behavioral parameters
            config = copy.deepcopy(base_config)
            
            # Create behavioral variations
            if i == 0:
                # Pure Safe T Peanut
                pass
            elif i == 1:
                # More aggressive version
                config['rewardFunction']['damageEnemyUnit'] *= 1.5
                config['rewardFunction']['killEnemyUnit'] *= 1.3
            elif i == 2:
                # More defensive version
                config['rewardFunction']['healTeammate1'] *= 2.0
                config['rewardFunction']['healTeammate2'] *= 2.0
                config['rewardFunction']['damageTaken'] *= 1.5  # More penalty for taking damage
            else:
                # Random variation
                np.random.seed(i * 42)
                for key in config['rewardFunction']:
                    base_value = config['rewardFunction'][key]
                    variation = np.random.normal(0, abs(base_value) * 0.15)
                    config['rewardFunction'][key] = base_value + variation
            
            individual = {
                'id': f"safe_t_{i:03d}",
                'config': config,
                'brain': SafeTPeanutBrain(),
                'fitness': 0.0,
                'total_reward': 0.0,
                'matches_played': 0,
                'behavioral_type': ['Pure', 'Aggressive', 'Defensive', 'Random'][i] if i < 4 else 'Random'
            }
            
            self.population.append(individual)
        
        print(f"  Created {len(self.population)} individuals:")
        for ind in self.population:
            print(f"    {ind['id']}: {ind['behavioral_type']}")
    
    def evaluate_individual(self, individual):
        """Evaluate individual with enhanced debugging"""
        total_reward = 0.0
        print(f"    🎯 Evaluating {individual['id']} ({individual['behavioral_type']})")
        
        for match in range(self.matches_per_individual):
            try:
                # Reset environment
                observation_n = self.env.reset()
                
                episode_reward = 0.0
                episode_length = 0
                max_episode_length = 1000  # Long enough for meaningful interactions
                
                # Create opponent team
                opponents = [TheAssaulterBrain() for _ in range(3)]
                
                print(f"      Match {match+1}: Starting episode...")
                
                # Run episode
                while episode_length < max_episode_length:
                    actions = []
                    
                    # Home team (Safe T Peanut variants) - first 3 agents
                    for i in range(3):
                        action = individual['brain'].get_action(observation_n[i])
                        actions.append(action)
                        
                        # Debug first few actions to ensure movement
                        if episode_length < 3:
                            move_x, rotate, chase_focus, cast_slot, focus_target = action
                            print(f"        Agent {i}: move={move_x:.2f}, rotate={rotate:.2f}, chase={chase_focus:.2f}, cast={cast_slot}, target={focus_target}")
                    
                    # Away team (The Assaulter) - next 3 agents  
                    for i in range(3):
                        action = opponents[i].get_action(observation_n[i + 3])
                        actions.append(action)
                        
                        # Debug opponent actions too
                        if episode_length < 3:
                            move_x, rotate, chase_focus, cast_slot, focus_target = action
                            print(f"        Opponent {i}: move={move_x:.2f}, rotate={rotate:.2f}, chase={chase_focus:.2f}, cast={cast_slot}, target={focus_target}")
                    
                    # Step environment
                    observation_n, reward_n, done_n, info = self.env.step(np.array(actions))
                    
                    # Accumulate rewards
                    team_reward = np.sum(reward_n[:3])
                    episode_reward += team_reward
                    
                    # Enhanced reward debugging
                    if episode_length < 10 or np.any(np.abs(reward_n) > 0.01):
                        print(f"        Step {episode_length}: Home={reward_n[:3].round(3)}, Away={reward_n[3:].round(3)}, Sum={team_reward:.3f}")
                    
                    episode_length += 1
                    
                    if all(done_n):
                        print(f"      Episode ended at step {episode_length}")
                        break
                
                total_reward += episode_reward
                print(f"      Match {match+1} reward: {episode_reward:.3f} (length: {episode_length})")
                
            except Exception as e:
                print(f"      ❌ Match {match+1} failed: {e}")
                continue
        
        # Calculate fitness
        average_reward = total_reward / self.matches_per_individual
        individual['fitness'] = average_reward
        individual['total_reward'] = total_reward
        individual['matches_played'] = self.matches_per_individual
        
        print(f"    🏆 {individual['id']} final fitness: {average_reward:.3f}")
        return average_reward
    
    def evolve_population(self):
        """Simple evolution with elitism"""
        print("🧬 Evolving population...")
        
        # Sort by fitness
        self.population.sort(key=lambda x: x['fitness'], reverse=True)
        
        # Keep top half as elites
        elite_count = self.population_size // 2
        elites = self.population[:elite_count]
        
        # Create offspring from elites
        offspring = []
        for i in range(elite_count):
            parent = elites[i % len(elites)]
            
            # Create child with mutations
            child_config = copy.deepcopy(parent['config'])
            
            # Mutate reward function
            for key in child_config['rewardFunction']:
                if np.random.random() < 0.3:  # 30% mutation chance
                    base_value = child_config['rewardFunction'][key] 
                    mutation = np.random.normal(0, abs(base_value) * 0.1)
                    child_config['rewardFunction'][key] = base_value + mutation
            
            child = {
                'id': f"{parent['id']}_gen",
                'config': child_config,
                'brain': SafeTPeanutBrain(),
                'fitness': 0.0,
                'total_reward': 0.0,
                'matches_played': 0,
                'behavioral_type': f"{parent['behavioral_type']}_mut"
            }
            
            offspring.append(child)
        
        # Replace population
        self.population = elites + offspring
        
        print(f"  Population evolved: {len(elites)} elites + {len(offspring)} offspring")
    
    def run_generation(self, generation):
        """Run a single generation"""
        print(f"\n🧬 GENERATION {generation}/{self.generations}")
        print("-" * 25)
        
        # Evaluate all individuals
        print("🎯 Evaluating population...")
        for i, individual in enumerate(self.population):
            print(f"  Individual {i+1}/{len(self.population)}:")
            fitness = self.evaluate_individual(individual)
        
        # Track best individual
        best_current = max(self.population, key=lambda x: x['fitness'])
        if self.best_individual is None or best_current['fitness'] > self.best_individual['fitness']:
            self.best_individual = copy.deepcopy(best_current)
            print(f"  🏆 New best: {best_current['fitness']:.3f}")
        
        # Print generation stats
        fitnesses = [ind['fitness'] for ind in self.population]
        avg_fitness = np.mean(fitnesses)
        
        print(f"  Best fitness: {max(fitnesses):.3f}")
        print(f"  Avg fitness:  {avg_fitness:.3f}")
        print(f"  Fitness range: {min(fitnesses):.3f} to {max(fitnesses):.3f}")
        
        # Evolution
        if generation < self.generations:
            self.evolve_population()
        
        # Store stats
        generation_stats = {
            'generation': generation,
            'best_fitness': max(fitnesses),
            'avg_fitness': avg_fitness,
            'min_fitness': min(fitnesses),
            'best_individual': best_current['id']
        }
        self.training_history.append(generation_stats)
    
    def run_training(self):
        """Run complete training process"""
        print("🚀 STARTING ENHANCED STEAM TRAINING")
        print("=" * 40)
        
        start_time = time.time()
        
        # Initialize
        if not self.initialize_environment():
            print("❌ Environment initialization failed!")
            return
        
        self.initialize_population()
        
        # Train
        for generation in range(1, self.generations + 1):
            self.run_generation(generation)
        
        # Cleanup
        if self.env:
            self.env.close()
            print(f"\n🏁 Environment closed cleanly")
        
        # Results
        training_time = (time.time() - start_time) / 60
        print(f"\n" + "=" * 40)
        print(f"🏆 TRAINING COMPLETE")
        print("=" * 40)
        print(f"Training time: {training_time:.1f} minutes")
        
        if self.best_individual:
            print(f"\n🥇 Best Safe T Peanut Variant:")
            print(f"  ID: {self.best_individual['id']}")
            print(f"  Type: {self.best_individual['behavioral_type']}")
            print(f"  Fitness: {self.best_individual['fitness']:.3f}")
            print(f"  Total reward: {self.best_individual['total_reward']:.3f}")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save training results with proper JSON serialization"""
        import os
        os.makedirs('training_results', exist_ok=True)
        
        def convert_numpy(obj):
            """Convert numpy types to Python native types for JSON serialization"""
            if hasattr(obj, 'tolist'):
                return obj.tolist()
            elif hasattr(obj, 'item'):  # numpy scalar
                return obj.item()
            elif str(type(obj)).startswith("<class 'numpy.float"):
                return float(obj)
            elif str(type(obj)).startswith("<class 'numpy.int"):
                return int(obj)
            return obj
        
        def make_serializable(data):
            """Recursively convert numpy types in nested data structures"""
            if isinstance(data, dict):
                return {k: make_serializable(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [make_serializable(item) for item in data]
            else:
                return convert_numpy(data)
        
        results = {
            'training_complete': True,
            'generations': self.generations,
            'population_size': self.population_size,
            'training_history': self.training_history,
            'best_individual': {
                'id': self.best_individual['id'],
                'behavioral_type': self.best_individual['behavioral_type'],
                'fitness': self.best_individual['fitness'],
                'total_reward': self.best_individual['total_reward'],
                'config': self.best_individual['config']
            } if self.best_individual else None,
            'final_population': [
                {
                    'id': ind['id'],
                    'behavioral_type': ind['behavioral_type'],
                    'fitness': ind['fitness'],
                    'total_reward': ind['total_reward']
                }
                for ind in self.population
            ]
        }
        
        # Convert all numpy types to JSON-serializable types
        results = make_serializable(results)
        
        with open('training_results/enhanced_training.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("💾 Results saved to training_results/enhanced_training.json")

def main():
    """Main function"""
    print("🏟️ ENHANCED STEAM TRAINER")
    print("=" * 30)
    print()
    print("Enhanced features:")
    print("• Team configuration with brain profiles")
    print("• Detailed action and reward debugging")
    print("• Longer episodes for meaningful combat")
    print("• Behavioral variations in population")
    print("• Persistent environment for efficiency")
    print()
    
    trainer = EnhancedSteamTrainer(n_arenas=2)
    trainer.run_training()

if __name__ == "__main__":
    main()
