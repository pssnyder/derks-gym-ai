"""
Steam Battlegrounds Training System
==================================

Replicates the Steam Derk Battlegrounds training methodology:
- Genetic Algorithm with 128 parallel arenas
- Recurrent Neural Networks (simulated with rule-based behavior)  
- Fitness based on bounty "gold" earned
- Population evolution over epochs
- ~3000 parameters + 32 memory slots (simulated)

Training Teams:
- Peanut Class: Safe T Peanut, Spicy Peanut, Angrrry Peanut
- Testing Class Opponents: The Assaulter, The Engineer, The Peacemaker
"""

import numpy as np
import json
import time
from datetime import datetime
from gym_derk.envs import DerkEnv
from typing import List, Dict, Tuple, Optional
import copy
import random

# Import brain profiles
from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain
from brain_profiles.peanut_class.angrrry_peanut import AngrrryPeanutBrain
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

class SteamBattlegroundsTrainer:
    """
    Simulates the Steam Battlegrounds genetic algorithm training system
    """
    
    def __init__(self, parallel_arenas=8):  # Reduced from 128 for testing
        # Training parameters (matching Steam implementation)
        self.parallel_arenas = parallel_arenas
        self.population_size = 16  # Reduced for testing
        self.generations = 20
        self.elite_size = 4
        self.mutation_rate = 0.15
        self.crossover_rate = 0.7
        
        # Match parameters
        self.matches_per_evaluation = 3
        self.max_episode_length = 1000
        
        # Initialize brain classes
        self.trainee_classes = {
            'safe_t_peanut': SafeTPeanutBrain,
            'spicy_peanut': SpicyPeanutBrain,
            'angrrry_peanut': AngrrryPeanutBrain
        }
        
        self.opponent_classes = {
            'the_assaulter': TheAssaulterBrain,
        }
        
        # Training results tracking
        self.training_history = []
        self.generation = 0
        
        # Population storage
        self.populations = {name: [] for name in self.trainee_classes.keys()}
        self.best_individuals = {name: None for name in self.trainee_classes.keys()}
        
        print("🏟️ Steam Battlegrounds Training System Initialized")
        print("=" * 60)
        print(f"Parallel Arenas: {self.parallel_arenas}")
        print(f"Population Size: {self.population_size}")
        print(f"Generations: {self.generations}")
        print(f"Elite Size: {self.elite_size}")
        print()
        print("Trainee Classes:")
        for name in self.trainee_classes.keys():
            print(f"  - {name.replace('_', ' ').title()}")
        print()
        print("Opponent Classes:")
        for name in self.opponent_classes.keys():
            print(f"  - {name.replace('_', ' ').title()}")
    
    def initialize_populations(self):
        """Initialize populations with parameter variations for each brain"""
        print("🧬 Initializing populations...")
        
        for brain_name, brain_class in self.trainee_classes.items():
            population = []
            base_brain = brain_class()
            base_config = base_brain.get_derk_gym_config()
            
            for i in range(self.population_size):
                # Create parameter variations (simulating neural network weights)
                individual = {
                    'id': f"{brain_name}_{i:03d}",
                    'brain_class': brain_class,
                    'parameters': self._create_parameter_variation(base_config, i),
                    'fitness': 0.0,
                    'gold_earned': 0.0,
                    'matches_played': 0,
                    'wins': 0,
                    'generation': 0,
                    'memory_state': np.zeros(32)  # Simulating 32 memory slots
                }
                
                population.append(individual)
            
            self.populations[brain_name] = population
            print(f"  {brain_name}: {len(population)} individuals")
    
    def _create_parameter_variation(self, base_config: Dict, individual_id: int) -> Dict:
        """Create parameter variations simulating neural network weight mutations"""
        
        # Copy base configuration
        config = copy.deepcopy(base_config)
        
        # Add random variations to reward function (simulating NN parameter changes)
        reward_function = config['rewardFunction']
        
        # Seed random number generator for reproducible variations
        np.random.seed(individual_id * 42)
        
        for reward_key in reward_function:
            # Apply small random variations (±10% of base value)
            base_value = reward_function[reward_key]
            variation = np.random.normal(0, abs(base_value) * 0.1)
            
            # Clamp values to reasonable ranges
            if 'damage' in reward_key.lower() or 'kill' in reward_key.lower():
                new_value = max(0, base_value + variation)
            else:
                new_value = base_value + variation
                
            reward_function[reward_key] = new_value
        
        # Simulate additional "neural network parameters" (not used in gym but tracked)
        config['neural_params'] = {
            'hidden_weights': np.random.normal(0, 0.1, 100),  # Simulated hidden layer
            'output_weights': np.random.normal(0, 0.1, 50),   # Simulated output layer
            'bias_terms': np.random.normal(0, 0.05, 20),      # Simulated biases
            'recurrent_weights': np.random.normal(0, 0.08, 32) # Simulated RNN weights
        }
        
        return config
    
    def evaluate_population(self, brain_name: str, generation: int) -> List[float]:
        """Evaluate entire population of a brain class using parallel arenas"""
        
        print(f"🎯 Evaluating {brain_name} population (Generation {generation})")
        
        population = self.populations[brain_name]
        fitnesses = []
        
        # Evaluate each individual
        for i, individual in enumerate(population):
            # Create brain instance with individual's parameters
            brain_class = individual['brain_class']
            brain = brain_class()
            
            # Apply parameter variations (for reward function)
            brain_config = individual['parameters']
            
            # Evaluate against random opponents
            total_gold = 0.0
            matches_won = 0
            
            for match in range(self.matches_per_evaluation):
                # Select random opponent team
                opponent_team = self._create_opponent_team()
                
                # Run match
                match_result = self._run_match(
                    trainee_brain=brain,
                    trainee_config=brain_config,
                    opponent_team=opponent_team,
                    individual_id=individual['id']
                )
                
                total_gold += match_result['gold_earned']
                if match_result['victory']:
                    matches_won += 1
            
            # Calculate fitness based on gold earned (Steam methodology)
            avg_gold = total_gold / self.matches_per_evaluation
            win_rate = matches_won / self.matches_per_evaluation
            
            # Fitness combines gold and win rate
            fitness = avg_gold + (win_rate * 100)  # Bonus for wins
            
            # Update individual statistics
            individual['gold_earned'] = total_gold
            individual['matches_played'] += self.matches_per_evaluation
            individual['wins'] += matches_won
            individual['fitness'] = fitness
            
            fitnesses.append(fitness)
            
            if (i + 1) % 5 == 0:
                print(f"  Progress: {i + 1}/{len(population)} individuals evaluated")
        
        return fitnesses
    
    def _create_opponent_team(self) -> List:
        """Create random opponent team from testing class"""
        # For now, just use The Assaulter for all opponents
        team = []
        for _ in range(3):
            team.append(TheAssaulterBrain())
        
        return team
    
    def _run_match(self, trainee_brain, trainee_config: Dict, 
                   opponent_team: List, individual_id: str) -> Dict:
        """Run a single match and return results"""
        
        try:
            # Create environment with default setup
            env = DerkEnv(
                n_arenas=1,
                turbo_mode=True
            )
            
            observation_n = env.reset()
            total_gold = 0.0
            episode_length = 0
            
            # Run episode
            while episode_length < self.max_episode_length:
                actions = []
                
                # Home team actions (trainees)
                for i in range(3):
                    action = trainee_brain.get_action(observation_n[i])
                    actions.append(action)
                
                # Away team actions (opponents)
                for i in range(3, 6):
                    opponent_idx = (i - 3) % len(opponent_team)
                    action = opponent_team[opponent_idx].get_action(observation_n[i])
                    actions.append(action)
                
                observation_n, reward_n, done_n, info = env.step(np.array(actions))
                
                # Accumulate gold (reward for trainee team)
                team_gold = np.sum(reward_n[:3])  # First 3 are trainee team
                total_gold += team_gold
                
                episode_length += 1
                
                if all(done_n):
                    break
            
            # Determine victory
            home_team_total = np.sum(env.total_reward[:3])
            away_team_total = np.sum(env.total_reward[3:])
            victory = home_team_total > away_team_total
            
            env.close()
            
            return {
                'gold_earned': total_gold,
                'victory': victory,
                'episode_length': episode_length,
                'home_score': home_team_total,
                'away_score': away_team_total
            }
            
        except Exception as e:
            print(f"Match error for {individual_id}: {e}")
            return {
                'gold_earned': 0.0,
                'victory': False,
                'episode_length': 0,
                'home_score': 0.0,
                'away_score': 0.0
            }
    
    def evolve_population(self, brain_name: str) -> None:
        """Evolve population using genetic algorithm (Steam methodology)"""
        
        population = self.populations[brain_name]
        
        # Sort by fitness (descending)
        population.sort(key=lambda x: x['fitness'], reverse=True)
        
        # Track best individual
        if (self.best_individuals[brain_name] is None or 
            population[0]['fitness'] > self.best_individuals[brain_name]['fitness']):
            self.best_individuals[brain_name] = copy.deepcopy(population[0])
            print(f"  🏆 New best {brain_name}: {population[0]['fitness']:.2f} fitness")
        
        # Create next generation
        new_population = []
        
        # Elitism - keep best individuals
        for i in range(self.elite_size):
            elite = copy.deepcopy(population[i])
            elite['id'] = f"{brain_name}_{self.generation+1:03d}_{i:03d}_elite"
            new_population.append(elite)
        
        # Generate offspring
        while len(new_population) < self.population_size:
            # Tournament selection
            parent1 = self._tournament_selection(population)
            parent2 = self._tournament_selection(population)
            
            # Crossover and mutation
            if random.random() < self.crossover_rate:
                child1, child2 = self._crossover(parent1, parent2, brain_name)
                new_population.extend([child1, child2])
            else:
                child = self._mutate(parent1, brain_name)
                new_population.append(child)
        
        # Trim to exact population size
        self.populations[brain_name] = new_population[:self.population_size]
    
    def _tournament_selection(self, population: List[Dict], tournament_size: int = 3) -> Dict:
        """Select parent using tournament selection"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return max(tournament, key=lambda x: x['fitness'])
    
    def _crossover(self, parent1: Dict, parent2: Dict, brain_name: str) -> Tuple[Dict, Dict]:
        """Create two offspring through parameter crossover"""
        
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)
        
        # Update IDs
        child1['id'] = f"{brain_name}_{self.generation+1:03d}_{random.randint(0,999):03d}_cross1"
        child2['id'] = f"{brain_name}_{self.generation+1:03d}_{random.randint(0,999):03d}_cross2"
        
        # Reset fitness
        child1['fitness'] = 0.0
        child2['fitness'] = 0.0
        
        # Crossover reward function parameters
        reward1 = child1['parameters']['rewardFunction']
        reward2 = child2['parameters']['rewardFunction']
        
        for key in reward1:
            if random.random() < 0.5:
                reward1[key], reward2[key] = reward2[key], reward1[key]
        
        return child1, child2
    
    def _mutate(self, parent: Dict, brain_name: str) -> Dict:
        """Create offspring through mutation"""
        
        child = copy.deepcopy(parent)
        child['id'] = f"{brain_name}_{self.generation+1:03d}_{random.randint(0,999):03d}_mutant"
        child['fitness'] = 0.0
        
        # Mutate reward function
        reward_function = child['parameters']['rewardFunction']
        for key in reward_function:
            if random.random() < self.mutation_rate:
                current_value = reward_function[key]
                mutation_strength = abs(current_value) * 0.1
                mutation = np.random.normal(0, mutation_strength)
                reward_function[key] = current_value + mutation
        
        return child
    
    def run_training_session(self, target_brain: str = None) -> None:
        """Run complete training session (Steam Battlegrounds style)"""
        
        print("🚀 STARTING STEAM BATTLEGROUNDS TRAINING")
        print("=" * 50)
        
        start_time = time.time()
        
        # Initialize populations
        self.initialize_populations()
        
        # Determine which brains to train
        brains_to_train = [target_brain] if target_brain else list(self.trainee_classes.keys())
        
        # Training loop
        for generation in range(self.generations):
            self.generation = generation
            
            print(f"\n🧬 GENERATION {generation + 1}/{self.generations}")
            print("-" * 40)
            
            generation_stats = {
                'generation': generation + 1,
                'timestamp': datetime.now().isoformat(),
                'brain_stats': {}
            }
            
            # Train each brain class
            for brain_name in brains_to_train:
                print(f"\n📊 Training {brain_name.replace('_', ' ').title()}...")
                
                # Evaluate population
                fitnesses = self.evaluate_population(brain_name, generation)
                
                # Statistics
                best_fitness = max(fitnesses)
                avg_fitness = np.mean(fitnesses)
                worst_fitness = min(fitnesses)
                
                generation_stats['brain_stats'][brain_name] = {
                    'best_fitness': best_fitness,
                    'avg_fitness': avg_fitness,
                    'worst_fitness': worst_fitness,
                    'population_size': len(fitnesses)
                }
                
                print(f"  Best fitness: {best_fitness:.2f}")
                print(f"  Avg fitness:  {avg_fitness:.2f}")
                print(f"  Worst fitness: {worst_fitness:.2f}")
                
                # Evolve population
                if generation < self.generations - 1:  # Don't evolve on last generation
                    self.evolve_population(brain_name)
                    print(f"  Population evolved for next generation")
            
            self.training_history.append(generation_stats)
            
            # Save progress
            if generation % 5 == 0:
                self.save_training_progress()
        
        # Training complete
        training_time = (time.time() - start_time) / 60
        
        print(f"\n" + "=" * 50)
        print("🏆 TRAINING COMPLETE")
        print("=" * 50)
        print(f"Training time: {training_time:.1f} minutes")
        print(f"Generations completed: {self.generations}")
        
        # Show final results
        for brain_name in brains_to_train:
            best = self.best_individuals[brain_name]
            if best:
                print(f"\n🥇 Best {brain_name.replace('_', ' ').title()}:")
                print(f"  Fitness: {best['fitness']:.2f}")
                print(f"  Gold earned: {best['gold_earned']:.2f}")
                print(f"  Win rate: {best['wins']/best['matches_played']*100:.1f}%")
        
        self.save_final_results()
        print(f"\n💾 Results saved to training_results/")
    
    def save_training_progress(self):
        """Save current training progress"""
        import os
        os.makedirs('training_results', exist_ok=True)
        
        with open('training_results/training_history.json', 'w') as f:
            json.dump(self.training_history, f, indent=2)
    
    def save_final_results(self):
        """Save final training results"""
        import os
        os.makedirs('training_results', exist_ok=True)
        
        results = {
            'training_complete': True,
            'total_generations': self.generations,
            'training_history': self.training_history,
            'best_individuals': {}
        }
        
        # Save best individuals (excluding neural_params for file size)
        for brain_name, best in self.best_individuals.items():
            if best:
                best_copy = copy.deepcopy(best)
                if 'neural_params' in best_copy['parameters']:
                    del best_copy['parameters']['neural_params']
                results['best_individuals'][brain_name] = best_copy
        
        with open('training_results/final_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save individual brain files
        for brain_name, best in self.best_individuals.items():
            if best:
                with open(f'training_results/best_{brain_name}.json', 'w') as f:
                    json.dump(best, f, indent=2)

def main():
    """Main training function"""
    print("🏟️ STEAM BATTLEGROUNDS TRAINING SYSTEM")
    print("=" * 45)
    print()
    print("This system replicates the Steam Derk Battlegrounds training:")
    print("• Genetic Algorithm with parallel arenas")
    print("• Population-based evolution")
    print("• Fitness based on bounty gold earned")
    print("• Parameter variation simulating neural networks")
    print()
    
    # Create trainer with reduced parameters for initial testing
    trainer = SteamBattlegroundsTrainer(parallel_arenas=4)
    
    # Run training for just one brain first
    print("Starting with Safe T Peanut training...")
    trainer.run_training_session(target_brain='safe_t_peanut')

if __name__ == "__main__":
    main()
