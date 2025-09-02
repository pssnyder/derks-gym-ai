"""
Simplified Efficient Steam Trainer
=================================

A working version with persistent environment to eliminate UI flickering.
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

class SimplifiedSteamTrainer:
    """
    Simplified but efficient trainer with persistent environment
    """
    
    def __init__(self, n_arenas=4):
        self.n_arenas = n_arenas
        self.population_size = 8  # Small for testing
        self.generations = 10
        self.matches_per_individual = 3
        
        # Persistent environment
        self.env = None
        
        # Population
        self.population = []
        self.best_individual = None
        self.training_history = []
        
        print(f"🏟️ Simplified Steam Trainer ({n_arenas} arenas)")
    
    def initialize_environment(self):
        """Initialize persistent environment once"""
        print("🌍 Creating persistent environment...")
        
        try:
            # Create environment with basic settings first
            self.env = DerkEnv(
                n_arenas=self.n_arenas,
                turbo_mode=True
            )
            
            # Store team configurations for later use
            safe_t_brain = SafeTPeanutBrain()
            assaulter_brain = TheAssaulterBrain()
            
            self.safe_t_config = safe_t_brain.get_derk_gym_config()
            self.assaulter_config = assaulter_brain.get_derk_gym_config()
            
            print(f"🛠️ Team configurations loaded:")
            print(f"   Safe T Peanut - Equipment: {self.safe_t_config['slots']}")
            print(f"   The Assaulter - Equipment: {self.assaulter_config['slots']}")
            
            print(f"✅ Environment created with {self.n_arenas} arenas")
            return True
        except Exception as e:
            print(f"❌ Environment creation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def initialize_population(self):
        """Create initial population"""
        print("🧬 Creating population...")
        
        base_brain = SafeTPeanutBrain()
        base_config = base_brain.get_derk_gym_config()
        
        for i in range(self.population_size):
            # Create variations
            config = copy.deepcopy(base_config)
            
            # Mutate reward function
            np.random.seed(i * 42)
            for key in config['rewardFunction']:
                base_value = config['rewardFunction'][key]
                variation = np.random.normal(0, abs(base_value) * 0.1)
                config['rewardFunction'][key] = base_value + variation
            
            individual = {
                'id': f"safe_t_{i:03d}",
                'config': config,
                'brain': SafeTPeanutBrain(),
                'fitness': 0.0,
                'total_reward': 0.0,
                'matches_played': 0
            }
            
            self.population.append(individual)
        
        print(f"  Created {len(self.population)} individuals")
    
    def evaluate_individual(self, individual):
        """Evaluate a single individual using persistent environment"""
        total_reward = 0.0
        
        for match in range(self.matches_per_individual):
            try:
                # Reset environment (reuses existing environment)
                observation_n = self.env.reset()
                
                episode_reward = 0.0
                episode_length = 0
                
                # Create opponent team
                opponents = [TheAssaulterBrain() for _ in range(3)]
                
                # Run episode
                while episode_length < 1000:  # Longer episodes for meaningful interactions
                    actions = []
                    
                    # Home team (trainee) - first 3 agents
                    for i in range(3):
                        action = individual['brain'].get_action(observation_n[i])
                        actions.append(action)
                        
                        # Debug output for first few steps
                        if episode_length < 5:
                            move_x, rotate, chase_focus, cast_slot, focus_target = action
                            print(f"      Agent {i}: move={move_x:.2f}, chase={chase_focus:.2f}, cast={cast_slot}, target={focus_target}")
                    
                    # Away team (opponents) - next 3 agents
                    for i in range(3):
                        action = opponents[i].get_action(observation_n[i + 3])
                        actions.append(action)
                    
                    # Step environment
                    observation_n, reward_n, done_n, info = self.env.step(np.array(actions))
                    
                    # Accumulate reward for trainee team
                    team_reward = np.sum(reward_n[:3])
                    episode_reward += team_reward
                    
                    # Debug output for first few steps and when rewards are earned
                    if episode_length < 5 or np.any(np.abs(reward_n) > 0.1):
                        print(f"      Step {episode_length}: Home rewards: {reward_n[:3]}, Away rewards: {reward_n[3:]}")
                    
                    episode_length += 1
                    
                    if all(done_n):
                        break
                
                total_reward += episode_reward
                
            except Exception as e:
                print(f"  Match error for {individual['id']}: {e}")
                # Continue with 0 reward for this match
        
        # Update individual stats
        individual['total_reward'] = total_reward
        individual['matches_played'] = self.matches_per_individual
        individual['fitness'] = total_reward / self.matches_per_individual
        
        return individual['fitness']
    
    def evaluate_population(self):
        """Evaluate entire population"""
        print("🎯 Evaluating population...")
        
        for i, individual in enumerate(self.population):
            fitness = self.evaluate_individual(individual)
            print(f"  Individual {i+1}/{len(self.population)}: {fitness:.2f}")
        
        # Sort by fitness
        self.population.sort(key=lambda x: x['fitness'], reverse=True)
        
        # Track best
        if self.best_individual is None or self.population[0]['fitness'] > self.best_individual['fitness']:
            self.best_individual = copy.deepcopy(self.population[0])
            print(f"  🏆 New best: {self.population[0]['fitness']:.2f}")
    
    def evolve_population(self):
        """Simple evolution - keep best half, mutate to create new half"""
        print("🧬 Evolving population...")
        
        # Keep best half
        elite_size = self.population_size // 2
        new_population = copy.deepcopy(self.population[:elite_size])
        
        # Create new individuals by mutating elites
        for i in range(elite_size):
            parent = random.choice(new_population)
            child = copy.deepcopy(parent)
            child['id'] = f"safe_t_{len(new_population):03d}_gen"
            child['brain'] = SafeTPeanutBrain()  # New brain instance
            child['fitness'] = 0.0
            child['total_reward'] = 0.0
            child['matches_played'] = 0
            
            # Mutate reward function
            for key in child['config']['rewardFunction']:
                if random.random() < 0.3:  # 30% mutation rate
                    current_value = child['config']['rewardFunction'][key]
                    mutation = np.random.normal(0, abs(current_value) * 0.15)
                    child['config']['rewardFunction'][key] = current_value + mutation
            
            new_population.append(child)
        
        self.population = new_population
        print(f"  Population evolved: {elite_size} elites + {elite_size} offspring")
    
    def run_training(self):
        """Run complete training session"""
        print("🚀 STARTING SIMPLIFIED STEAM TRAINING")
        print("=" * 40)
        
        start_time = time.time()
        
        # Initialize
        if not self.initialize_environment():
            return
        
        self.initialize_population()
        
        try:
            # Training loop
            for generation in range(self.generations):
                print(f"\\n🧬 GENERATION {generation + 1}/{self.generations}")
                print("-" * 25)
                
                # Evaluate
                self.evaluate_population()
                
                # Stats
                fitnesses = [ind['fitness'] for ind in self.population]
                best_fitness = max(fitnesses)
                avg_fitness = np.mean(fitnesses)
                
                print(f"  Best fitness: {best_fitness:.2f}")
                print(f"  Avg fitness:  {avg_fitness:.2f}")
                
                # Save stats
                generation_stats = {
                    'generation': generation + 1,
                    'best_fitness': best_fitness,
                    'avg_fitness': avg_fitness,
                    'timestamp': datetime.now().isoformat()
                }
                self.training_history.append(generation_stats)
                
                # Evolve (except last generation)
                if generation < self.generations - 1:
                    self.evolve_population()
        
        finally:
            # Clean up
            if self.env:
                self.env.close()
                print("\\n🏁 Environment closed cleanly")
        
        # Results
        training_time = (time.time() - start_time) / 60
        
        print(f"\\n" + "=" * 40)
        print("🏆 TRAINING COMPLETE")
        print("=" * 40)
        print(f"Training time: {training_time:.1f} minutes")
        
        if self.best_individual:
            print(f"\\n🥇 Best Safe T Peanut:")
            print(f"  Fitness: {self.best_individual['fitness']:.2f}")
            print(f"  Avg reward per match: {self.best_individual['fitness']:.2f}")
        
        # Save results
        self.save_results()
    
    def save_results(self):
        """Save training results"""
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
                'fitness': self.best_individual['fitness'],
                'config': self.best_individual['config']
            } if self.best_individual else None
        }
        
        # Convert all numpy types to JSON-serializable types
        results = make_serializable(results)
        
        with open('training_results/simplified_training.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("💾 Results saved to training_results/simplified_training.json")

def main():
    """Main function"""
    print("🏟️ SIMPLIFIED STEAM TRAINER")
    print("=" * 30)
    print()
    print("Key features:")
    print("• Single persistent environment (no flickering)")
    print("• Efficient evaluation without create/destroy cycles")
    print("• Simple genetic algorithm")
    print("• Fast training suitable for testing")
    print()
    
    # Create and run trainer
    trainer = SimplifiedSteamTrainer(n_arenas=2)  # Start small
    trainer.run_training()

if __name__ == "__main__":
    main()
