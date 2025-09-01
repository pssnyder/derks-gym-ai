"""
Number Eleven - Dynamic Genetic Algorithm Derkling
=================================================

This implements the "Top Secret Training" program where Number Eleven
starts with zero rewards/penalties and evolves its own optimal reward
function through genetic algorithms while training against your existing
Steam brain profiles.

The GA continuously optimizes reward/penalty values based on win rates,
creating a self-improving derkling that discovers novel strategies.
"""

import numpy as np
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json
import time
from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys

@dataclass
class RewardGene:
    """Single reward/penalty gene in the GA chromosome"""
    name: str
    value: float
    min_val: float = -2.0
    max_val: float = 2.0
    mutation_rate: float = 0.1
    mutation_strength: float = 0.2

@dataclass
class GAChromosome:
    """Complete reward function chromosome for Number Eleven"""
    genes: Dict[str, RewardGene]
    fitness: float = 0.0
    win_rate: float = 0.0
    games_played: int = 0
    generation: int = 0
    
    def to_derk_config(self) -> Dict:
        """Convert chromosome to Derk Gym reward configuration"""
        return {gene.name: gene.value for gene in self.genes.values()}

class NumberElevenBrain:
    """
    Number Eleven - The Genetic Algorithm Derkling
    
    This derkling starts with all rewards/penalties at 0 and evolves
    its own optimal reward function through genetic algorithms.
    """
    
    def __init__(self):
        self.name = "Number Eleven"
        self.brain_class = "genetic_algorithm"
        self.role = "adaptive_evolution"
        self.compatible_with = "all_brains"
        
        # GA Parameters
        self.population_size = 20
        self.mutation_rate = 0.15
        self.crossover_rate = 0.7
        self.elite_size = 4
        self.generation = 0
        
        # Training parameters
        self.matches_per_evaluation = 50
        self.current_chromosome = None
        self.population = []
        self.best_chromosome = None
        self.training_history = []
        
        # Initialize base reward genes
        self.reward_genes_template = {
            "damageEnemyStatue": RewardGene("damageEnemyStatue", 0.0, 0.0, 2.0),
            "damageEnemyUnit": RewardGene("damageEnemyUnit", 0.0, 0.0, 2.0),
            "killEnemyStatue": RewardGene("killEnemyStatue", 0.0, 0.0, 3.0),
            "killEnemyUnit": RewardGene("killEnemyUnit", 0.0, 0.0, 3.0),
            "timeSpentAwayTerritory": RewardGene("timeSpentAwayTerritory", 0.0, 0.0, 1.5),
            "damageTaken": RewardGene("damageTaken", 0.0, -2.0, 0.0),
            "friendlyFire": RewardGene("friendlyFire", 0.0, -2.0, 0.0),
            "fallDamageTaken": RewardGene("fallDamageTaken", 0.0, -2.0, 0.0),
            "teamSpirit": RewardGene("teamSpirit", 0.0, 0.0, 1.0),
            "timeScaling": RewardGene("timeScaling", 0.0, 0.0, 0.5)
        }
        
        # Initialize first generation
        self.initialize_population()
        
    def initialize_population(self):
        """Create initial random population"""
        self.population = []
        
        for i in range(self.population_size):
            chromosome = GAChromosome(
                genes={},
                generation=self.generation
            )
            
            # Create random genes for this chromosome
            for gene_name, template in self.reward_genes_template.items():
                chromosome.genes[gene_name] = RewardGene(
                    name=gene_name,
                    value=random.uniform(template.min_val, template.max_val),
                    min_val=template.min_val,
                    max_val=template.max_val,
                    mutation_rate=template.mutation_rate,
                    mutation_strength=template.mutation_strength
                )
            
            self.population.append(chromosome)
        
        # Start with first chromosome
        self.current_chromosome = self.population[0]
        
    def get_action(self, observation):
        """
        Number Eleven uses a simple rule-based approach
        The GA optimizes the reward function, not the decision logic
        """
        obs = observation
        
        # Simple aggressive strategy - GA will tune rewards to modify behavior
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        # Basic observations
        self_hp = obs[ObservationKeys.Hitpoints.value]
        closest_enemy_dist = min([
            obs[ObservationKeys.Enemy1Distance.value],
            obs[ObservationKeys.Enemy2Distance.value],
            obs[ObservationKeys.Enemy3Distance.value]
        ])
        statue_dist = obs[ObservationKeys.EnemyStatueDistance.value]
        
        health_ratio = self_hp / 100.0
        
        # Simple decision logic - GA will shape this through rewards
        if closest_enemy_dist < 0.4 and health_ratio > 0.3:
            # Engage enemies
            move_x = 0.6
            chase_focus = 0.7
            focus_target = 5
            cast_slot = 1 if closest_enemy_dist < 0.2 else 2
            
        elif statue_dist < 0.6 and closest_enemy_dist > 0.4:
            # Attack statue
            move_x = 0.4
            focus_target = 4
            cast_slot = 2
            
        elif health_ratio < 0.4:
            # Retreat when low health
            move_x = -0.5
            focus_target = 0
            
        else:
            # Explore/advance
            move_x = 0.3
            rotate = 0.1
            
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
    
    def evaluate_chromosome(self, chromosome: GAChromosome, opponent_brains: List, matches: int = 50) -> float:
        """
        Evaluate a chromosome by running matches against opponent brains
        Returns win rate as fitness
        """
        wins = 0
        total_matches = 0
        
        for _ in range(matches):
            # Randomly select opponent brain
            opponent = random.choice(opponent_brains)
            
            # Run match
            result = self._run_match(chromosome, opponent)
            if result == "win":
                wins += 1
            total_matches += 1
        
        win_rate = wins / total_matches if total_matches > 0 else 0.0
        chromosome.fitness = win_rate
        chromosome.win_rate = win_rate
        chromosome.games_played += total_matches
        
        return win_rate
    
    def _run_match(self, chromosome: GAChromosome, opponent_brain) -> str:
        """Run a single match between Number Eleven and opponent"""
        try:
            # Create environment with Number Eleven's current reward function
            env = DerkEnv(
                n_arenas=1,
                turbo_mode=True,
                reward_function=chromosome.to_derk_config()
            )
            
            observation_n = env.reset()
            
            for step in range(1000):  # Max steps per match
                actions = []
                
                for i in range(env.n_agents):
                    if i == 0:  # Number Eleven
                        action = self.get_action(observation_n[i])
                    else:  # Opponent brain
                        action = opponent_brain.get_action(observation_n[i])
                    actions.append(action)
                
                observation_n, reward_n, done_n, info = env.step(np.array(actions))
                
                if all(done_n):
                    # Determine winner based on total reward
                    eleven_reward = env.total_reward[0]
                    opponent_reward = max(env.total_reward[1:])
                    
                    env.close()
                    return "win" if eleven_reward > opponent_reward else "loss"
            
            env.close()
            return "draw"  # Timeout
            
        except Exception as e:
            print(f"Match error: {e}")
            return "loss"
    
    def mutate_chromosome(self, chromosome: GAChromosome) -> GAChromosome:
        """Apply mutation to a chromosome"""
        new_chromosome = GAChromosome(
            genes={},
            generation=self.generation + 1
        )
        
        for gene_name, gene in chromosome.genes.items():
            new_gene = RewardGene(
                name=gene.name,
                value=gene.value,
                min_val=gene.min_val,
                max_val=gene.max_val,
                mutation_rate=gene.mutation_rate,
                mutation_strength=gene.mutation_strength
            )
            
            # Apply mutation
            if random.random() < gene.mutation_rate:
                mutation = random.gauss(0, gene.mutation_strength)
                new_gene.value = np.clip(
                    gene.value + mutation,
                    gene.min_val,
                    gene.max_val
                )
            
            new_chromosome.genes[gene_name] = new_gene
        
        return new_chromosome
    
    def crossover_chromosomes(self, parent1: GAChromosome, parent2: GAChromosome) -> Tuple[GAChromosome, GAChromosome]:
        """Create two offspring through crossover"""
        child1 = GAChromosome(genes={}, generation=self.generation + 1)
        child2 = GAChromosome(genes={}, generation=self.generation + 1)
        
        for gene_name in parent1.genes:
            if random.random() < 0.5:
                child1.genes[gene_name] = parent1.genes[gene_name]
                child2.genes[gene_name] = parent2.genes[gene_name]
            else:
                child1.genes[gene_name] = parent2.genes[gene_name] 
                child2.genes[gene_name] = parent1.genes[gene_name]
        
        return child1, child2
    
    def evolve_generation(self, opponent_brains: List):
        """Evolve to next generation through GA operations"""
        print(f"🧬 Number Eleven - Evolving Generation {self.generation}")
        
        # Evaluate all chromosomes
        for i, chromosome in enumerate(self.population):
            fitness = self.evaluate_chromosome(chromosome, opponent_brains, self.matches_per_evaluation)
            print(f"   Chromosome {i:2d}: Fitness = {fitness:.3f}")
        
        # Sort by fitness (descending)
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Track best chromosome
        if self.best_chromosome is None or self.population[0].fitness > self.best_chromosome.fitness:
            self.best_chromosome = self.population[0]
            print(f"🏆 New best chromosome! Fitness: {self.best_chromosome.fitness:.3f}")
        
        # Create next generation
        new_population = []
        
        # Elitism - keep best chromosomes
        for i in range(self.elite_size):
            new_population.append(self.population[i])
        
        # Generate offspring
        while len(new_population) < self.population_size:
            # Tournament selection
            parent1 = self._tournament_selection()
            parent2 = self._tournament_selection()
            
            if random.random() < self.crossover_rate:
                child1, child2 = self.crossover_chromosomes(parent1, parent2)
                new_population.extend([child1, child2])
            else:
                new_population.extend([
                    self.mutate_chromosome(parent1),
                    self.mutate_chromosome(parent2)
                ])
        
        # Trim to population size
        self.population = new_population[:self.population_size]
        self.generation += 1
        
        # Update current chromosome to best
        self.current_chromosome = self.population[0]
        
        # Log generation stats
        self._log_generation_stats()
    
    def _tournament_selection(self, tournament_size: int = 3) -> GAChromosome:
        """Select parent through tournament selection"""
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        return max(tournament, key=lambda x: x.fitness)
    
    def _log_generation_stats(self):
        """Log statistics for current generation"""
        fitnesses = [c.fitness for c in self.population]
        stats = {
            "generation": self.generation - 1,
            "best_fitness": max(fitnesses),
            "avg_fitness": np.mean(fitnesses),
            "worst_fitness": min(fitnesses),
            "timestamp": time.time()
        }
        
        self.training_history.append(stats)
        
        print(f"Generation {stats['generation']} Stats:")
        print(f"  Best:  {stats['best_fitness']:.3f}")
        print(f"  Avg:   {stats['avg_fitness']:.3f}")
        print(f"  Worst: {stats['worst_fitness']:.3f}")
    
    def get_current_derk_config(self) -> Dict:
        """Get current reward configuration for Derk Gym"""
        if self.current_chromosome:
            return {
                "slots": ["Talons", "Pistol", None],  # Balanced loadout
                "rewardFunction": self.current_chromosome.to_derk_config(),
                "primaryColor": "#00FF00",    # Bright green (evolution)
                "secondaryColor": "#000000"   # Black (unknown)
            }
        else:
            return {
                "slots": ["Talons", "Pistol", None],
                "rewardFunction": {k: 0.0 for k in self.reward_genes_template.keys()},
                "primaryColor": "#888888",    # Gray (starting)
                "secondaryColor": "#000000"
            }
    
    def save_evolution_data(self, filepath: str):
        """Save evolution history and best chromosome"""
        data = {
            "generation": self.generation,
            "training_history": self.training_history,
            "best_chromosome": {
                "fitness": self.best_chromosome.fitness,
                "win_rate": self.best_chromosome.win_rate,
                "games_played": self.best_chromosome.games_played,
                "reward_function": self.best_chromosome.to_derk_config()
            } if self.best_chromosome else None,
            "current_chromosome": {
                "fitness": self.current_chromosome.fitness,
                "reward_function": self.current_chromosome.to_derk_config()
            } if self.current_chromosome else None
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

def test_number_eleven():
    """Test Number Eleven's genetic algorithm system"""
    print("🧬 TESTING NUMBER ELEVEN - GENETIC ALGORITHM DERKLING")
    print("=" * 55)
    
    # Import some existing brains as opponents
    try:
        from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain
        from brain_profiles.peanut_class.angrrry_peanut import AngrrryPeanutBrain
        opponent_brains = [SpicyPeanutBrain(), AngrrryPeanutBrain()]
    except ImportError:
        print("Creating simple test opponents...")
        opponent_brains = [NumberElevenBrain() for _ in range(2)]  # Self-play for testing
    
    # Create Number Eleven
    eleven = NumberElevenBrain()
    
    print(f"Initial Population Size: {len(eleven.population)}")
    print(f"Starting with all rewards at 0.0")
    
    # Run a few generations
    for generation in range(3):
        print(f"\n🧬 GENERATION {generation + 1}")
        print("-" * 20)
        eleven.evolve_generation(opponent_brains)
        
        if eleven.best_chromosome:
            print(f"Best reward function so far:")
            config = eleven.best_chromosome.to_derk_config()
            for reward, value in config.items():
                if abs(value) > 0.01:  # Only show non-zero values
                    print(f"  {reward}: {value:.3f}")
    
    # Save results
    eleven.save_evolution_data("number_eleven_evolution.json")
    print(f"\n💾 Evolution data saved to number_eleven_evolution.json")
    
    return eleven

if __name__ == "__main__":
    test_number_eleven()
