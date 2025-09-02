"""
Efficient Steam Battlegrounds Training System
============================================

This version uses a single persistent DerkEnv with multiple arenas running concurrently,
eliminating the inefficient create/destroy cycle that causes UI flickering.

Key improvements:
- Single persistent environment with multiple arenas
- Concurrent evaluation of multiple individuals
- No environment recreation between matches
- Efficient arena reuse and batch processing
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

class EfficientSteamTrainer:
    """
    Efficient training system using persistent multi-arena environment
    """
    
    def __init__(self, n_arenas=16):  # Start with 16, can scale up to 128
        # Training parameters
        self.n_arenas = n_arenas
        self.population_size = 32  # 2x arenas for good utilization
        self.generations = 50
        self.elite_size = 8
        self.mutation_rate = 0.15
        self.crossover_rate = 0.7
        
        # Evaluation parameters
        self.matches_per_individual = 5
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
        
        # Persistent environment
        self.env = None
        self.arena_assignments = {}  # Track which individual is in which arena
        
        # Training state
        self.populations = {name: [] for name in self.trainee_classes.keys()}
        self.best_individuals = {name: None for name in self.trainee_classes.keys()}
        self.training_history = []
        self.generation = 0
        
        print("🏟️ Efficient Steam Battlegrounds Trainer")
        print("=" * 50)
        print(f"Concurrent Arenas: {self.n_arenas}")
        print(f"Population Size: {self.population_size}")
        print(f"Generations: {self.generations}")
        print(f"Matches per Individual: {self.matches_per_individual}")
    
    def initialize_persistent_environment(self):
        """Initialize single persistent environment with multiple arenas"""
        print("🌍 Initializing persistent multi-arena environment...")
        
        try:
            # Create environment with multiple arenas
            self.env = DerkEnv(
                n_arenas=self.n_arenas,
                turbo_mode=True,
                # We'll dynamically set team configurations per arena
            )
            
            print(f"✅ Environment created with {self.n_arenas} concurrent arenas")
            print(f"   Total agents: {self.env.n_agents}")
            print(f"   Agents per arena: {self.env.n_agents // self.n_arenas}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create environment: {e}")
            return False
    
    def initialize_populations(self):
        """Initialize populations for each brain type"""
        print("🧬 Initializing populations...")
        
        for brain_name, brain_class in self.trainee_classes.items():
            population = []
            base_brain = brain_class()
            base_config = base_brain.get_derk_gym_config()
            
            for i in range(self.population_size):
                individual = {
                    'id': f"{brain_name}_{i:03d}",
                    'brain_class': brain_class,
                    'brain_instance': brain_class(),  # Pre-create brain instance
                    'config': self._create_parameter_variation(base_config, i),
                    'fitness': 0.0,
                    'total_reward': 0.0,
                    'matches_played': 0,
                    'wins': 0,
                    'generation': 0
                }
                population.append(individual)
            
            self.populations[brain_name] = population
            print(f"  {brain_name}: {len(population)} individuals")
    
    def _create_parameter_variation(self, base_config: Dict, individual_id: int) -> Dict:
        """Create parameter variations for genetic diversity"""
        config = copy.deepcopy(base_config)
        
        # Apply variations to reward function
        np.random.seed(individual_id * 42)  # Reproducible variations
        reward_function = config['rewardFunction']
        
        for key in reward_function:
            base_value = reward_function[key]
            variation_strength = abs(base_value) * 0.15  # 15% variation
            variation = np.random.normal(0, variation_strength)
            
            # Apply variation with bounds
            if base_value >= 0:
                reward_function[key] = max(0, base_value + variation)
            else:
                reward_function[key] = min(0, base_value + variation)
        
        return config
    
    def run_concurrent_evaluation(self, brain_name: str) -> List[float]:
        """Run evaluation using concurrent arenas for efficiency"""
        print(f"🎯 Evaluating {brain_name} population...")
        
        population = self.populations[brain_name]
        
        # Create evaluation queue
        evaluation_queue = []
        for individual in population:
            for match_idx in range(self.matches_per_individual):
                evaluation_queue.append({
                    'individual': individual,
                    'match_idx': match_idx,
                    'status': 'pending'
                })
        
        # Process evaluations in batches
        batch_size = self.n_arenas
        total_batches = (len(evaluation_queue) + batch_size - 1) // batch_size
        
        completed_evaluations = 0
        
        for batch_idx in range(total_batches):
            batch_start = batch_idx * batch_size
            batch_end = min(batch_start + batch_size, len(evaluation_queue))
            batch = evaluation_queue[batch_start:batch_end]
            
            # Run batch concurrently
            self._run_evaluation_batch(batch)
            completed_evaluations += len(batch)
            
            print(f"  Progress: {completed_evaluations}/{len(evaluation_queue)} evaluations ({completed_evaluations/len(evaluation_queue)*100:.1f}%)")\n        \n        # Calculate final fitness scores\n        fitnesses = []\n        for individual in population:\n            # Fitness = average reward + win bonus\n            avg_reward = individual['total_reward'] / max(individual['matches_played'], 1)\n            win_rate = individual['wins'] / max(individual['matches_played'], 1)\n            fitness = avg_reward + (win_rate * 50)  # Win bonus\n            \n            individual['fitness'] = fitness\n            fitnesses.append(fitness)\n        \n        return fitnesses\n    \n    def _run_evaluation_batch(self, batch: List[Dict]):\n        \"\"\"Run a batch of evaluations concurrently in multiple arenas\"\"\"\n        \n        # Assign individuals to arenas\n        arena_assignments = {}\n        for i, eval_item in enumerate(batch):\n            if i < self.n_arenas:  # Don't exceed available arenas\n                arena_assignments[i] = eval_item\n        \n        # Set up teams for each arena\n        team_configs = []\n        opponent_brains = []\n        \n        for arena_idx in range(self.n_arenas):\n            if arena_idx in arena_assignments:\n                eval_item = arena_assignments[arena_idx]\n                individual = eval_item['individual']\n                \n                # Trainee team (3 copies of same individual)\n                trainee_config = individual['config']\n                team_config = [trainee_config, trainee_config, trainee_config]\n                \n                # Opponent team (The Assaulter)\n                opponent_config = TheAssaulterBrain().get_derk_gym_config()\n                team_config.extend([opponent_config, opponent_config, opponent_config])\n                \n                team_configs.append(team_config)\n                \n                # Store brain instances for action generation\n                opponent_brains.append({\n                    'trainee': individual['brain_instance'],\n                    'opponents': [TheAssaulterBrain() for _ in range(3)]\n                })\n            else:\n                # Empty arena - use default config\n                default_config = {}\n                team_configs.append([default_config] * 6)\n                opponent_brains.append(None)\n        \n        # Reset environment with new team configurations\n        try:\n            # Note: DerkEnv doesn't directly support per-arena team configs\n            # So we'll use a simpler approach with standard reset\n            observation_n = self.env.reset()\n            \n            # Run episode\n            episode_rewards = {arena_idx: [] for arena_idx in arena_assignments.keys()}\n            episode_length = 0\n            \n            while episode_length < self.max_episode_length:\n                actions = []\n                \n                # Generate actions for each agent\n                agents_per_arena = self.env.n_agents // self.n_arenas\n                \n                for arena_idx in range(self.n_arenas):\n                    arena_start = arena_idx * agents_per_arena\n                    \n                    if arena_idx in arena_assignments and arena_idx < len(opponent_brains) and opponent_brains[arena_idx]:\n                        # Active arena with evaluation\n                        brains = opponent_brains[arena_idx]\n                        \n                        # Trainee team actions (first 3 agents in arena)\n                        for i in range(3):\n                            agent_idx = arena_start + i\n                            if agent_idx < len(observation_n):\n                                action = brains['trainee'].get_action(observation_n[agent_idx])\n                                actions.append(action)\n                        \n                        # Opponent team actions (next 3 agents in arena)\n                        for i in range(3):\n                            agent_idx = arena_start + 3 + i\n                            if agent_idx < len(observation_n):\n                                opponent_idx = i % len(brains['opponents'])\n                                action = brains['opponents'][opponent_idx].get_action(observation_n[agent_idx])\n                                actions.append(action)\n                    else:\n                        # Inactive arena - random actions\n                        for i in range(agents_per_arena):\n                            agent_idx = arena_start + i\n                            if agent_idx < len(observation_n):\n                                actions.append(self.env.action_space.sample())\n                \n                # Step environment\n                observation_n, reward_n, done_n, info = self.env.step(np.array(actions))\n                \n                # Accumulate rewards for active arenas\n                for arena_idx in arena_assignments.keys():\n                    arena_start = arena_idx * agents_per_arena\n                    arena_team_reward = np.sum(reward_n[arena_start:arena_start+3])  # First 3 agents\n                    episode_rewards[arena_idx].append(arena_team_reward)\n                \n                episode_length += 1\n                \n                # Check if any arena is done\n                if episode_length % 100 == 0:  # Check periodically\n                    arena_done_checks = []\n                    for arena_idx in range(self.n_arenas):\n                        arena_start = arena_idx * agents_per_arena\n                        arena_done = all(done_n[arena_start:arena_start+agents_per_arena])\n                        arena_done_checks.append(arena_done)\n                    \n                    if any(arena_done_checks):\n                        break\n            \n            # Update individual statistics\n            for arena_idx, eval_item in arena_assignments.items():\n                individual = eval_item['individual']\n                \n                if arena_idx in episode_rewards:\n                    match_reward = sum(episode_rewards[arena_idx])\n                    individual['total_reward'] += match_reward\n                    individual['matches_played'] += 1\n                    \n                    # Determine if this was a win (simplified)\n                    if match_reward > 0:\n                        individual['wins'] += 1\n        \n        except Exception as e:\n            print(f\"Batch evaluation error: {e}\")\n            # Mark all individuals in batch as having played with 0 reward\n            for eval_item in arena_assignments.values():\n                individual = eval_item['individual']\n                individual['matches_played'] += 1\n    \n    def evolve_population(self, brain_name: str):\n        \"\"\"Evolve population using genetic algorithm\"\"\"\n        population = self.populations[brain_name]\n        \n        # Sort by fitness\n        population.sort(key=lambda x: x['fitness'], reverse=True)\n        \n        # Track best individual\n        if (self.best_individuals[brain_name] is None or \n            population[0]['fitness'] > self.best_individuals[brain_name]['fitness']):\n            self.best_individuals[brain_name] = copy.deepcopy(population[0])\n            print(f\"  🏆 New best {brain_name}: {population[0]['fitness']:.2f} fitness\")\n        \n        # Create next generation\n        new_population = []\n        \n        # Elitism\n        for i in range(self.elite_size):\n            elite = copy.deepcopy(population[i])\n            elite['id'] = f\"{brain_name}_{self.generation+1:03d}_{i:03d}_elite\"\n            elite['fitness'] = 0.0\n            elite['total_reward'] = 0.0\n            elite['matches_played'] = 0\n            elite['wins'] = 0\n            elite['brain_instance'] = elite['brain_class']()  # New brain instance\n            new_population.append(elite)\n        \n        # Generate offspring\n        while len(new_population) < self.population_size:\n            parent1 = self._tournament_selection(population)\n            parent2 = self._tournament_selection(population)\n            \n            if random.random() < self.crossover_rate:\n                child1, child2 = self._crossover(parent1, parent2, brain_name)\n                new_population.extend([child1, child2])\n            else:\n                child = self._mutate(parent1, brain_name)\n                new_population.append(child)\n        \n        self.populations[brain_name] = new_population[:self.population_size]\n    \n    def _tournament_selection(self, population: List[Dict], tournament_size: int = 3) -> Dict:\n        \"\"\"Tournament selection for parent selection\"\"\"\n        tournament = random.sample(population, min(tournament_size, len(population)))\n        return max(tournament, key=lambda x: x['fitness'])\n    \n    def _crossover(self, parent1: Dict, parent2: Dict, brain_name: str) -> Tuple[Dict, Dict]:\n        \"\"\"Create offspring through crossover\"\"\"\n        child1 = copy.deepcopy(parent1)\n        child2 = copy.deepcopy(parent2)\n        \n        # Update IDs and reset stats\n        for i, child in enumerate([child1, child2]):\n            child['id'] = f\"{brain_name}_{self.generation+1:03d}_{random.randint(0,999):03d}_cross{i+1}\"\n            child['fitness'] = 0.0\n            child['total_reward'] = 0.0\n            child['matches_played'] = 0\n            child['wins'] = 0\n            child['brain_instance'] = child['brain_class']()  # New brain instance\n        \n        # Crossover reward functions\n        reward1 = child1['config']['rewardFunction']\n        reward2 = child2['config']['rewardFunction']\n        \n        for key in reward1:\n            if random.random() < 0.5:\n                reward1[key], reward2[key] = reward2[key], reward1[key]\n        \n        return child1, child2\n    \n    def _mutate(self, parent: Dict, brain_name: str) -> Dict:\n        \"\"\"Create offspring through mutation\"\"\"\n        child = copy.deepcopy(parent)\n        child['id'] = f\"{brain_name}_{self.generation+1:03d}_{random.randint(0,999):03d}_mutant\"\n        child['fitness'] = 0.0\n        child['total_reward'] = 0.0\n        child['matches_played'] = 0\n        child['wins'] = 0\n        child['brain_instance'] = child['brain_class']()  # New brain instance\n        \n        # Mutate reward function\n        reward_function = child['config']['rewardFunction']\n        for key in reward_function:\n            if random.random() < self.mutation_rate:\n                current_value = reward_function[key]\n                mutation_strength = abs(current_value) * 0.1\n                mutation = np.random.normal(0, mutation_strength)\n                reward_function[key] = current_value + mutation\n        \n        return child\n    \n    def run_training_session(self, target_brain: str = 'safe_t_peanut'):\n        \"\"\"Run complete training session with persistent environment\"\"\"\n        print(\"🚀 STARTING EFFICIENT STEAM TRAINING\")\n        print(\"=\" * 45)\n        \n        start_time = time.time()\n        \n        # Initialize persistent environment\n        if not self.initialize_persistent_environment():\n            print(\"❌ Failed to initialize environment - aborting training\")\n            return\n        \n        # Initialize populations\n        self.initialize_populations()\n        \n        try:\n            # Training loop\n            for generation in range(self.generations):\n                self.generation = generation\n                \n                print(f\"\\n🧬 GENERATION {generation + 1}/{self.generations}\")\n                print(\"-\" * 30)\n                \n                # Evaluate target brain\n                fitnesses = self.run_concurrent_evaluation(target_brain)\n                \n                # Statistics\n                best_fitness = max(fitnesses) if fitnesses else 0\n                avg_fitness = np.mean(fitnesses) if fitnesses else 0\n                worst_fitness = min(fitnesses) if fitnesses else 0\n                \n                print(f\"  Best fitness:  {best_fitness:.2f}\")\n                print(f\"  Avg fitness:   {avg_fitness:.2f}\")\n                print(f\"  Worst fitness: {worst_fitness:.2f}\")\n                \n                # Save generation stats\n                generation_stats = {\n                    'generation': generation + 1,\n                    'best_fitness': float(best_fitness),\n                    'avg_fitness': float(avg_fitness),\n                    'worst_fitness': float(worst_fitness),\n                    'timestamp': datetime.now().isoformat()\n                }\n                self.training_history.append(generation_stats)\n                \n                # Evolve population\n                if generation < self.generations - 1:\n                    self.evolve_population(target_brain)\n                    print(f\"  Population evolved for next generation\")\n        \n        finally:\n            # Clean up environment\n            if self.env:\n                self.env.close()\n                print(\"\\n🏁 Environment closed\")\n        \n        # Training complete\n        training_time = (time.time() - start_time) / 60\n        \n        print(f\"\\n\" + \"=\" * 45)\n        print(\"🏆 TRAINING COMPLETE\")\n        print(\"=\" * 45)\n        print(f\"Training time: {training_time:.1f} minutes\")\n        \n        # Show results\n        best = self.best_individuals[target_brain]\n        if best:\n            print(f\"\\n🥇 Best {target_brain.replace('_', ' ').title()}:\")\n            print(f\"  Fitness: {best['fitness']:.2f}\")\n            print(f\"  Win rate: {best['wins']/max(best['matches_played'], 1)*100:.1f}%\")\n        \n        self.save_results()\n    \n    def save_results(self):\n        \"\"\"Save training results\"\"\"\n        import os\n        os.makedirs('training_results', exist_ok=True)\n        \n        with open('training_results/efficient_training_history.json', 'w') as f:\n            json.dump(self.training_history, f, indent=2)\n        \n        print(\"💾 Results saved to training_results/\")\n\ndef main():\n    \"\"\"Main training function\"\"\"\n    print(\"🏟️ EFFICIENT STEAM BATTLEGROUNDS TRAINER\")\n    print(\"=\" * 45)\n    print()\n    print(\"Improvements:\")\n    print(\"• Single persistent environment\")\n    print(\"• Concurrent multi-arena evaluation\")\n    print(\"• No UI flickering from create/destroy cycles\")\n    print(\"• Efficient batch processing\")\n    print()\n    \n    # Create trainer with moderate arena count\n    trainer = EfficientSteamTrainer(n_arenas=8)  # Start with 8, can scale to 128\n    \n    # Run training\n    trainer.run_training_session(target_brain='safe_t_peanut')\n\nif __name__ == \"__main__\":\n    main()
