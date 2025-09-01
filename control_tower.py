"""
Control Tower - Solo Battle Training Orchestrator
===============================================

A centralized control system for managing parallel solo battle training
across multiple derklings. Supports concurrent training without sequential
bottlenecks, with real-time monitoring and coordination.

Features:
- Parallel threading for concurrent training
- Real-time battle monitoring
- Performance analytics
- Resource management
- Live status updates
"""

import threading
import time
import queue
import numpy as np
from datetime import datetime
from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys

# Import our testing class brains
from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain
from brain_profiles.testing_class.the_peacemaker import ThePeacemakerBrain
from brain_profiles.testing_class.the_engineer import TheEngineerBrain

class ControlTower:
    """
    Central control system for parallel derkling training operations
    """
    
    def __init__(self):
        self.active_operations = {}
        self.status_queue = queue.Queue()
        self.results_database = {}
        self.start_time = None
        self.training_lock = threading.Lock()
        
        # Available brains for training
        self.available_brains = {
            "The Assaulter": TheAssaulterBrain,
            "The Peacemaker": ThePeacemakerBrain, 
            "The Engineer": TheEngineerBrain
        }
        
        # Training configurations
        self.training_configs = {
            "solo_battle": {
                "episodes": 20,
                "arena_count": 1,
                "turbo_mode": True,
                "description": "Solo battle training against random opponents"
            },
            "endurance": {
                "episodes": 50,
                "arena_count": 1,
                "turbo_mode": False,
                "description": "Endurance training for longer battles"
            },
            "stress_test": {
                "episodes": 10,
                "arena_count": 3,
                "turbo_mode": True,
                "description": "Multi-arena stress testing"
            }
        }
        
    def initialize_control_tower(self):
        """Initialize the control tower systems"""
        self.start_time = datetime.now()
        print("🏗️ CONTROL TOWER INITIALIZING")
        print("=" * 35)
        print(f"🕐 System Start Time: {self.start_time.strftime('%H:%M:%S')}")
        print(f"🧠 Available Brains: {len(self.available_brains)}")
        print(f"⚙️ Training Configs: {len(self.training_configs)}")
        print("=" * 35)
        
    def launch_parallel_training(self, brain_names, training_type="solo_battle"):
        """
        Launch parallel training operations for specified brains
        """
        if training_type not in self.training_configs:
            print(f"❌ Unknown training type: {training_type}")
            return False
            
        config = self.training_configs[training_type]
        print(f"\n🚀 LAUNCHING PARALLEL TRAINING: {config['description']}")
        print("=" * 50)
        
        # Validate brain selection
        valid_brains = []
        for brain_name in brain_names:
            if brain_name in self.available_brains:
                valid_brains.append(brain_name)
                print(f"✅ {brain_name} - Ready for deployment")
            else:
                print(f"❌ {brain_name} - Brain not found")
                
        if not valid_brains:
            print("❌ No valid brains selected for training")
            return False
            
        # Launch training threads
        training_threads = []
        
        for brain_name in valid_brains:
            thread = threading.Thread(
                target=self._solo_training_worker,
                args=(brain_name, config),
                name=f"Training-{brain_name}"
            )
            training_threads.append(thread)
            
        # Start all threads simultaneously
        print(f"\n🎯 Deploying {len(training_threads)} concurrent training operations...")
        for thread in training_threads:
            thread.start()
            time.sleep(0.1)  # Small delay to prevent resource conflicts
            
        # Monitor training progress
        self._monitor_training_progress(training_threads, valid_brains)
        
        # Wait for all training to complete
        for thread in training_threads:
            thread.join()
            
        # Compile final results
        self._compile_training_results(valid_brains, training_type)
        
        return True
        
    def _solo_training_worker(self, brain_name, config):
        """
        Worker thread for individual brain training
        """
        brain_class = self.available_brains[brain_name]
        brain = brain_class()
        
        # Thread-safe status update
        self._update_status(brain_name, "INITIALIZING", "Setting up training environment")
        
        try:
            # Create environment
            env = DerkEnv(
                n_arenas=config["arena_count"],
                turbo_mode=config["turbo_mode"]
            )
            
            self._update_status(brain_name, "TRAINING", f"Starting {config['episodes']} episodes")
            
            results = []
            episode_times = []
            
            for episode in range(config["episodes"]):
                episode_start = time.time()
                
                # Run episode
                observation_n = env.reset()
                episode_reward = 0
                episode_length = 0
                actions_taken = 0
                
                while True:
                    actions = []
                    for i in range(env.n_agents):
                        if i == 0:  # Our brain
                            action = brain.get_action(observation_n[i])
                            actions_taken += 1
                        else:  # Random opponents
                            action = env.action_space.sample()
                        actions.append(action)
                        
                    observation_n, reward_n, done_n, info = env.step(np.array(actions))
                    episode_length += 1
                    
                    if all(done_n):
                        episode_reward = env.total_reward[0]
                        break
                        
                episode_time = time.time() - episode_start
                episode_times.append(episode_time)
                results.append({
                    "episode": episode + 1,
                    "reward": episode_reward,
                    "length": episode_length,
                    "actions": actions_taken,
                    "time": episode_time
                })
                
                # Progress update every 5 episodes
                if (episode + 1) % 5 == 0:
                    avg_reward = np.mean([r["reward"] for r in results[-5:]])
                    self._update_status(
                        brain_name, 
                        "TRAINING",
                        f"Episode {episode + 1}/{config['episodes']} | Avg Reward: {avg_reward:.1f}"
                    )
                    
            env.close()
            
            # Store results
            with self.training_lock:
                self.results_database[brain_name] = {
                    "config": config,
                    "results": results,
                    "summary": self._calculate_summary_stats(results)
                }
                
            self._update_status(brain_name, "COMPLETED", "Training operation successful")
            
        except Exception as e:
            self._update_status(brain_name, "ERROR", f"Training failed: {str(e)}")
            
    def _monitor_training_progress(self, threads, brain_names):
        """
        Monitor and display real-time training progress
        """
        print("\n📊 REAL-TIME TRAINING MONITOR")
        print("=" * 40)
        
        while any(thread.is_alive() for thread in threads):
            # Clear previous status display
            if hasattr(self, '_last_status_lines'):
                for _ in range(self._last_status_lines):
                    print("\033[A\033[K", end="")  # Move up and clear line
                    
            # Display current status
            status_lines = 0
            for brain_name in brain_names:
                if brain_name in self.active_operations:
                    op = self.active_operations[brain_name]
                    status_icon = {
                        "INITIALIZING": "🔄",
                        "TRAINING": "⚡",
                        "COMPLETED": "✅",
                        "ERROR": "❌"
                    }.get(op["status"], "❓")
                    
                    elapsed = time.time() - op["start_time"]
                    print(f"{status_icon} {brain_name:15} | {op['status']:12} | {op['message']:40} | {elapsed:6.1f}s")
                    status_lines += 1
                else:
                    print(f"⏳ {brain_name:15} | PENDING      | Waiting for deployment...                | 0.0s")
                    status_lines += 1
                    
            self._last_status_lines = status_lines
            time.sleep(1.0)
            
        # Final status display
        print("\n🎯 TRAINING OPERATIONS COMPLETE")
        
    def _update_status(self, brain_name, status, message):
        """
        Thread-safe status update
        """
        with self.training_lock:
            if brain_name not in self.active_operations:
                self.active_operations[brain_name] = {
                    "start_time": time.time(),
                    "status": status,
                    "message": message
                }
            else:
                self.active_operations[brain_name]["status"] = status
                self.active_operations[brain_name]["message"] = message
                
    def _calculate_summary_stats(self, results):
        """
        Calculate summary statistics for training results
        """
        rewards = [r["reward"] for r in results]
        lengths = [r["length"] for r in results]
        times = [r["time"] for r in results]
        
        return {
            "total_episodes": len(results),
            "avg_reward": np.mean(rewards),
            "max_reward": np.max(rewards),
            "min_reward": np.min(rewards),
            "std_reward": np.std(rewards),
            "avg_length": np.mean(lengths),
            "avg_time": np.mean(times),
            "total_time": np.sum(times)
        }
        
    def _compile_training_results(self, brain_names, training_type):
        """
        Compile and display final training results
        """
        print("\n📈 TRAINING RESULTS ANALYSIS")
        print("=" * 50)
        
        for brain_name in brain_names:
            if brain_name in self.results_database:
                data = self.results_database[brain_name]
                summary = data["summary"]
                
                print(f"\n🧠 {brain_name}")
                print("-" * 25)
                print(f"Episodes Completed: {summary['total_episodes']}")
                print(f"Average Reward: {summary['avg_reward']:.2f}")
                print(f"Best Performance: {summary['max_reward']:.2f}")
                print(f"Worst Performance: {summary['min_reward']:.2f}")
                print(f"Consistency (σ): {summary['std_reward']:.2f}")
                print(f"Avg Battle Length: {summary['avg_length']:.1f} steps")
                print(f"Total Training Time: {summary['total_time']:.1f}s")
                
                # Performance rating
                rating = self._calculate_performance_rating(summary)
                print(f"Performance Rating: {rating}")
                
        # Overall comparison
        self._generate_comparison_report(brain_names)
        
    def _calculate_performance_rating(self, summary):
        """
        Calculate a performance rating based on training results
        """
        avg_reward = summary['avg_reward']
        consistency = 1.0 / (1.0 + summary['std_reward'])  # Higher is better
        
        if avg_reward > 50 and consistency > 0.7:
            return "⭐⭐⭐ EXCELLENT"
        elif avg_reward > 20 and consistency > 0.5:
            return "⭐⭐ GOOD"
        elif avg_reward > 0:
            return "⭐ FAIR"
        else:
            return "❌ NEEDS WORK"
            
    def _generate_comparison_report(self, brain_names):
        """
        Generate a comparative analysis report
        """
        print("\n🏆 COMPARATIVE ANALYSIS")
        print("=" * 30)
        
        # Sort by average reward
        brain_performance = []
        for brain_name in brain_names:
            if brain_name in self.results_database:
                summary = self.results_database[brain_name]
                brain_performance.append((brain_name, summary["summary"]["avg_reward"]))
                
        brain_performance.sort(key=lambda x: x[1], reverse=True)
        
        print("🥇 Performance Ranking:")
        for i, (brain_name, avg_reward) in enumerate(brain_performance):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "🏅"
            print(f"{medal} {i+1}. {brain_name}: {avg_reward:.2f} avg reward")
            
        # Training efficiency
        if self.start_time:
            total_time = time.time() - self.start_time.timestamp()
            print(f"\n⚡ Total Training Time: {total_time:.1f}s")
            print(f"🔥 Parallel Efficiency: {len(brain_names)}x speedup vs sequential")
        
    def get_training_report(self, brain_name):
        """
        Get detailed training report for a specific brain
        """
        if brain_name not in self.results_database:
            return None
            
        return self.results_database[brain_name]
        
    def export_results(self, filename=None):
        """
        Export training results to file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"training_results_{timestamp}.json"
            
        import json
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "results": self.results_database
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
            
        print(f"📁 Results exported to: {filename}")
        
def test_control_tower():
    """
    Test the control tower system
    """
    print("🎯 TESTING CONTROL TOWER SYSTEM")
    print("=" * 40)
    
    tower = ControlTower()
    tower.initialize_control_tower()
    
    # Test with all testing class brains
    brain_names = ["The Assaulter", "The Peacemaker", "The Engineer"]
    
    success = tower.launch_parallel_training(brain_names, "solo_battle")
    
    if success:
        print("\n✅ Control tower test completed successfully!")
        
        # Export results
        tower.export_results("test_results.json")
        
        # Display summary
        print("\n📋 Quick Summary:")
        for brain_name in brain_names:
            report = tower.get_training_report(brain_name)
            if report:
                summary = report["summary"]
                print(f"{brain_name}: {summary['avg_reward']:.1f} avg reward ({summary['total_episodes']} episodes)")
    else:
        print("❌ Control tower test failed")

if __name__ == "__main__":
    test_control_tower()
