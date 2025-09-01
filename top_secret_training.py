"""
Top Secret Training Program - Integrated GA Training System
==========================================================

This orchestrates the complete training program where your 10 existing
Steam brain profiles train normally for 1000 matches each, while Number
Eleven evolves its reward function through genetic algorithms in parallel.

Features:
- Multithreaded training for maximum PC utilization
- Normal Derk Gym functionality preserved for existing brains
- Number Eleven runs GA evolution in background
- Comprehensive performance tracking and analysis
- Results export for Steam integration
"""

import threading
import multiprocessing as mp
import time
import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import queue
import os

from gym_derk.envs import DerkEnv
from brain_profiles.special.number_eleven import NumberElevenBrain

@dataclass
class TrainingResult:
    """Results from a training session"""
    brain_name: str
    matches_completed: int
    win_rate: float
    avg_reward: float
    training_time: float
    final_config: Dict
    match_history: List[float]

@dataclass
class GAEvolutionResult:
    """Results from Number Eleven's GA evolution"""
    generation: int
    best_fitness: float
    avg_fitness: float
    best_reward_function: Dict
    evolution_time: float

class TopSecretTraining:
    """
    Main orchestrator for the Top Secret Training Program
    
    Manages parallel training of all 11 derklings:
    - 10 existing Steam brains (normal training)
    - 1 Number Eleven (GA evolution)
    """
    
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or min(mp.cpu_count(), 8)
        self.training_results = {}
        self.ga_results = []
        self.eleven = NumberElevenBrain()
        
        # Training parameters
        self.matches_per_brain = 1000
        self.ga_generations = 20
        self.matches_per_ga_evaluation = 50
        
        # Performance tracking
        self.start_time = None
        self.training_active = False
        
        print(f"🔬 Top Secret Training Program Initialized")
        print(f"   Max Workers: {self.max_workers}")
        print(f"   Training Target: {self.matches_per_brain} matches per brain")
        print(f"   GA Evolution: {self.ga_generations} generations")
    
    def load_steam_brains(self) -> List:
        """Load all existing Steam brain profiles"""
        brains = []
        brain_modules = [
            ("brain_profiles.peanut_class.spicy_peanut", "SpicyPeanutBrain"),
            ("brain_profiles.peanut_class.safe_t_peanut", "SafeTPeanutBrain"),
            ("brain_profiles.peanut_class.nightrider_peanut", "NightriderPeanutBrain"),
            ("brain_profiles.peanut_class.angrrry_peanut", "AngrrryPeanutBrain"),
            ("brain_profiles.peanut_class.poonut", "PoonutBrain"),
            ("brain_profiles.lone_wolf_class.clint_eastwood", "ClintEastwoodBrain"),
            ("brain_profiles.testing_class.the_assaulter", "TheAssaulterBrain"),
            ("brain_profiles.testing_class.the_engineer", "TheEngineerBrain"),
            ("brain_profiles.testing_class.the_peacemaker", "ThePeacemakerBrain"),
            ("brain_profiles.special.frank", "FrankBrain")
        ]
        
        for module_path, class_name in brain_modules:
            try:
                module = __import__(module_path, fromlist=[class_name])
                brain_class = getattr(module, class_name)
                brain = brain_class()
                brains.append(brain)
                print(f"✅ Loaded: {brain.name}")
            except Exception as e:
                print(f"❌ Failed to load {class_name}: {e}")
        
        print(f"🧠 Successfully loaded {len(brains)} Steam brains")
        return brains
    
    def train_single_brain(self, brain, brain_index: int, opponent_brains: List) -> TrainingResult:
        """Train a single brain for the specified number of matches"""
        print(f"🚀 Starting training: {brain.name} (Worker {brain_index})")
        
        start_time = time.time()
        wins = 0
        total_reward = 0.0
        match_history = []
        
        try:
            for match in range(self.matches_per_brain):
                # Select random opponent
                opponent = np.random.choice(opponent_brains)
                
                # Run match
                result = self._run_training_match(brain, opponent)
                
                if result['winner'] == 'brain':
                    wins += 1
                
                total_reward += result['brain_reward']
                match_history.append(result['brain_reward'])
                
                # Progress update every 100 matches
                if (match + 1) % 100 == 0:
                    current_wr = wins / (match + 1)
                    print(f"   {brain.name}: {match + 1}/{self.matches_per_brain} - WR: {current_wr:.3f}")
        
        except Exception as e:
            print(f"❌ Training error for {brain.name}: {e}")
            return TrainingResult(
                brain_name=brain.name,
                matches_completed=0,
                win_rate=0.0,
                avg_reward=0.0,
                training_time=time.time() - start_time,
                final_config={},
                match_history=[]
            )
        
        training_time = time.time() - start_time
        win_rate = wins / self.matches_per_brain
        avg_reward = total_reward / self.matches_per_brain
        
        result = TrainingResult(
            brain_name=brain.name,
            matches_completed=self.matches_per_brain,
            win_rate=win_rate,
            avg_reward=avg_reward,
            training_time=training_time,
            final_config=brain.get_derk_gym_config() if hasattr(brain, 'get_derk_gym_config') else {},
            match_history=match_history
        )
        
        print(f"✅ Completed: {brain.name} - WR: {win_rate:.3f}, Avg Reward: {avg_reward:.2f}, Time: {training_time:.1f}s")
        return result
    
    def _run_training_match(self, brain, opponent) -> Dict:
        """Run a single training match between brain and opponent"""
        try:
            env = DerkEnv(n_arenas=1, turbo_mode=True)
            observation_n = env.reset()
            
            for step in range(1000):
                actions = []
                
                for i in range(env.n_agents):
                    if i == 0:  # Primary brain
                        action = brain.get_action(observation_n[i])
                    else:  # Opponent
                        action = opponent.get_action(observation_n[i])
                    actions.append(action)
                
                observation_n, reward_n, done_n, info = env.step(np.array(actions))
                
                if all(done_n):
                    brain_reward = env.total_reward[0]
                    opponent_reward = max(env.total_reward[1:])
                    
                    env.close()
                    return {
                        'winner': 'brain' if brain_reward > opponent_reward else 'opponent',
                        'brain_reward': brain_reward,
                        'opponent_reward': opponent_reward
                    }
            
            env.close()
            return {'winner': 'draw', 'brain_reward': 0.0, 'opponent_reward': 0.0}
            
        except Exception as e:
            print(f"Match error: {e}")
            return {'winner': 'error', 'brain_reward': 0.0, 'opponent_reward': 0.0}
    
    def evolve_number_eleven(self, opponent_brains: List) -> List[GAEvolutionResult]:
        """Run Number Eleven's genetic algorithm evolution"""
        print(f"🧬 Starting Number Eleven GA Evolution")
        print(f"   Target Generations: {self.ga_generations}")
        
        evolution_results = []
        
        for generation in range(self.ga_generations):
            start_time = time.time()
            
            # Evolve generation
            self.eleven.evolve_generation(opponent_brains)
            
            evolution_time = time.time() - start_time
            
            # Record results
            fitnesses = [c.fitness for c in self.eleven.population]
            result = GAEvolutionResult(
                generation=generation,
                best_fitness=max(fitnesses),
                avg_fitness=float(np.mean(fitnesses)),
                best_reward_function=self.eleven.best_chromosome.to_derk_config() if self.eleven.best_chromosome else {},
                evolution_time=evolution_time
            )
            
            evolution_results.append(result)
            
            print(f"🧬 Gen {generation}: Best={result.best_fitness:.3f}, Avg={result.avg_fitness:.3f}, Time={evolution_time:.1f}s")
        
        print(f"✅ Number Eleven evolution complete!")
        return evolution_results
    
    def run_top_secret_training(self) -> Dict:
        """Execute the complete Top Secret Training program"""
        print("\n" + "🔬" * 20)
        print("TOP SECRET TRAINING PROGRAM - INITIATED")
        print("🔬" * 20)
        
        self.start_time = time.time()
        self.training_active = True
        
        # Load all Steam brains
        steam_brains = self.load_steam_brains()
        if len(steam_brains) < 10:
            print(f"⚠️ Warning: Only loaded {len(steam_brains)}/10 expected brains")
        
        # Create opponent pool (all brains including Number Eleven)
        all_brains = steam_brains + [self.eleven]
        
        print(f"\n🚀 PHASE 1: PARALLEL TRAINING INITIATION")
        print(f"   Training {len(steam_brains)} Steam brains")
        print(f"   Each brain: {self.matches_per_brain} matches")
        print(f"   Using {self.max_workers} parallel workers")
        
        # Start parallel training for Steam brains
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit training jobs for Steam brains
            training_futures = []
            for i, brain in enumerate(steam_brains):
                future = executor.submit(self.train_single_brain, brain, i, all_brains)
                training_futures.append((brain.name, future))
            
            # Also start Number Eleven evolution in parallel
            ga_future = executor.submit(self.evolve_number_eleven, steam_brains)
            
            print(f"✅ All training jobs submitted")
            
            # Collect Steam brain results
            for brain_name, future in training_futures:
                try:
                    result = future.result()
                    self.training_results[brain_name] = result
                except Exception as e:
                    print(f"❌ Training failed for {brain_name}: {e}")
            
            # Collect Number Eleven GA results
            try:
                self.ga_results = ga_future.result()
            except Exception as e:
                print(f"❌ GA Evolution failed: {e}")
        
        total_time = time.time() - self.start_time
        self.training_active = False
        
        print(f"\n🎉 TOP SECRET TRAINING COMPLETE!")
        print(f"   Total Time: {total_time:.1f} seconds")
        print(f"   Steam Brains Trained: {len(self.training_results)}")
        print(f"   GA Generations: {len(self.ga_results)}")
        
        # Generate comprehensive results
        return self._generate_final_report()
    
    def _generate_final_report(self) -> Dict:
        """Generate comprehensive training report"""
        report = {
            "training_summary": {
                "total_time": time.time() - (self.start_time or 0),
                "steam_brains_trained": len(self.training_results),
                "ga_generations_completed": len(self.ga_results),
                "matches_per_brain": self.matches_per_brain,
                "max_workers_used": self.max_workers
            },
            "steam_brain_results": {},
            "number_eleven_evolution": {},
            "rankings": {},
            "best_strategies": {}
        }
        
        # Steam brain results
        for brain_name, result in self.training_results.items():
            report["steam_brain_results"][brain_name] = {
                "win_rate": result.win_rate,
                "avg_reward": result.avg_reward,
                "training_time": result.training_time,
                "matches_completed": result.matches_completed
            }
        
        # Number Eleven evolution
        if self.ga_results:
            report["number_eleven_evolution"] = {
                "generations": len(self.ga_results),
                "final_fitness": self.ga_results[-1].best_fitness,
                "best_reward_function": self.ga_results[-1].best_reward_function,
                "evolution_history": [
                    {
                        "generation": r.generation,
                        "best_fitness": r.best_fitness,
                        "avg_fitness": r.avg_fitness
                    } for r in self.ga_results
                ]
            }
        
        # Rankings
        if self.training_results:
            sorted_brains = sorted(
                self.training_results.items(),
                key=lambda x: x[1].win_rate,
                reverse=True
            )
            
            report["rankings"] = {
                "by_win_rate": [(name, result.win_rate) for name, result in sorted_brains],
                "by_avg_reward": sorted([
                    (name, result.avg_reward) for name, result in self.training_results.items()
                ], key=lambda x: x[1], reverse=True)
            }
        
        return report
    
    def save_results(self, filepath: str = "top_secret_training_results.json"):
        """Save complete training results"""
        report = self._generate_final_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"💾 Results saved to {filepath}")
        
        # Also save Number Eleven's evolution data
        if hasattr(self.eleven, 'save_evolution_data'):
            self.eleven.save_evolution_data("number_eleven_final.json")
            print(f"💾 Number Eleven data saved to number_eleven_final.json")

def run_top_secret_program():
    """Main entry point for Top Secret Training"""
    print("🔬 INITIALIZING TOP SECRET TRAINING PROGRAM")
    print("=" * 45)
    
    # Create training orchestrator
    trainer = TopSecretTraining(max_workers=8)  # Adjust based on your PC
    
    # Run complete training program
    results = trainer.run_top_secret_training()
    
    # Save results
    trainer.save_results()
    
    # Print summary
    print(f"\n📊 TRAINING SUMMARY:")
    print(f"   Steam Brains: {results['training_summary']['steam_brains_trained']}")
    print(f"   GA Generations: {results['training_summary']['ga_generations_completed']}")
    print(f"   Total Time: {results['training_summary']['total_time']:.1f}s")
    
    if "rankings" in results and "by_win_rate" in results["rankings"]:
        print(f"\n🏆 WIN RATE RANKINGS:")
        for i, (name, wr) in enumerate(results["rankings"]["by_win_rate"][:5]):
            print(f"   {i+1}. {name}: {wr:.3f}")
    
    if "number_eleven_evolution" in results:
        final_fitness = results["number_eleven_evolution"]["final_fitness"]
        print(f"\n🧬 Number Eleven Final Fitness: {final_fitness:.3f}")
    
    return results

if __name__ == "__main__":
    run_top_secret_program()
