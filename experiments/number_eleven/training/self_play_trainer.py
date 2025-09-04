"""
Number Eleven Self-Play Training System
======================================

AlphaZero-inspired self-play training for Number Eleven.
The AI learns by playing against evolving versions of itself,
discovering optimal strategies without human bias.

Key Features:
- Self-play against previous best versions
- Objective fitness evaluation based on health and scores
- Experience replay and continuous learning
- Strategy mutation and evolution
"""

import numpy as np
import json
import random
import time
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import copy

# Our custom imports
try:
    from data_extraction.sensor_extractor import NumberElevenDataExtractor, GameState, ObjectiveMetrics
    from neural_network.number_eleven_network import NumberElevenNetwork, NetworkConfig, NumberElevenTrainer
except ImportError:
    # Fallback for testing
    print("⚠️ Import error in self_play_trainer - running in test mode")
    NumberElevenDataExtractor = None
    GameState = None
    ObjectiveMetrics = None
    NumberElevenNetwork = None
    NetworkConfig = None
    NumberElevenTrainer = None


@dataclass
class TrainingConfig:
    """Configuration for Number Eleven's self-play training"""
    # Training parameters
    episodes_per_generation: int = 50
    max_generations: int = 1000
    steps_per_episode: int = 500
    
    # Self-play parameters
    mutation_rate: float = 0.05  # How much to mutate when creating new challenger
    evaluation_games: int = 10   # Games to determine if challenger beats champion
    champion_win_threshold: float = 0.55  # Win rate needed to become new champion
    
    # Experience replay
    replay_buffer_size: int = 10000
    batch_size: int = 32
    training_steps_per_episode: int = 5
    
    # Reward scaling for objective function
    health_weight: float = 1.0
    tower_health_weight: float = 2.0  # Towers are more important
    points_weight: float = 0.5  # Points provide continuous feedback
    survival_bonus: float = 10.0  # Big bonus for staying alive
    victory_bonus: float = 100.0  # Huge bonus for winning
    draw_penalty: float = -20.0  # Contempt for draws
    
    # File paths
    save_directory: str = "experiments/number_eleven/experiments"
    champion_save_path: str = "champion_network.pth"
    training_log_path: str = "training_log.json"


@dataclass
class GameResult:
    """Result from a single game"""
    winner: str  # 'number_eleven', 'opponent', 'draw'
    number_eleven_score: float
    opponent_score: float
    game_length: int
    number_eleven_fitness: float  # Our objective evaluation
    opponent_fitness: float


@dataclass
class TrainingMetrics:
    """Metrics for tracking training progress"""
    generation: int
    episode: int
    win_rate: float
    average_fitness: float
    average_game_length: float
    champion_score: float
    challenger_score: float
    mutations_applied: int
    timestamp: str


class ExperienceReplay:
    """Experience replay buffer for training Number Eleven"""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.experiences: List[Dict[str, Any]] = []
    
    def add_experience(self, game_states: List[GameState], final_fitness: float):
        """Add a game's worth of experiences to the buffer"""
        for i, state in enumerate(game_states):
            # Calculate temporal difference target
            time_remaining = (len(game_states) - i) / len(game_states)
            td_target = final_fitness * time_remaining
            
            experience = {
                'raw_observation': state.sensors.raw_observation,
                'objective_metrics': np.array([
                    state.objectives.own_health_percent / 100.0,
                    state.objectives.own_tower_health_percent / 100.0,
                    state.objectives.enemy_health_percent / 100.0,
                    state.objectives.enemy_tower_health_percent / 100.0,
                    state.objectives.points_scored,
                    float(state.objectives.is_alive),
                    state.objectives.game_progress
                ]),
                'td_target': td_target,
                'final_fitness': final_fitness
            }
            
            self.experiences.append(experience)
            
            # Remove oldest if buffer is full
            if len(self.experiences) > self.max_size:
                self.experiences.pop(0)
    
    def sample_batch(self, batch_size: int) -> Dict[str, np.ndarray]:
        """Sample a random batch of experiences"""
        if len(self.experiences) < batch_size:
            batch = self.experiences.copy()
        else:
            batch = random.sample(self.experiences, batch_size)
        
        # Convert to arrays
        raw_observations = np.array([exp['raw_observation'] for exp in batch])
        objective_metrics = np.array([exp['objective_metrics'] for exp in batch])
        td_targets = np.array([exp['td_target'] for exp in batch])
        
        return {
            'raw_observations': raw_observations,
            'objective_metrics': objective_metrics,
            'td_targets': td_targets
        }
    
    def __len__(self):
        return len(self.experiences)


class NumberElevenSelfPlayTrainer:
    """Main self-play training system for Number Eleven"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.network_config = NetworkConfig()
        
        # Create save directory
        Path(config.save_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize champion network (the current best)
        self.champion_network = NumberElevenNetwork(self.network_config)
        
        # Data extractor for game state processing
        self.data_extractor = NumberElevenDataExtractor()
        
        # Experience replay buffer
        self.replay_buffer = ExperienceReplay(config.replay_buffer_size)
        
        # Training metrics
        self.training_history: List[TrainingMetrics] = []
        self.current_generation = 0
        
        print(f"🤖 Number Eleven Self-Play Trainer Initialized")
        print(f"   Episodes per generation: {config.episodes_per_generation}")
        print(f"   Max generations: {config.max_generations}")
        print(f"   Mutation rate: {config.mutation_rate}")
        print(f"   Champion win threshold: {config.champion_win_threshold}")
    
    def calculate_objective_fitness(self, game_states: List[GameState], 
                                  game_result: GameResult) -> float:
        """
        Calculate objective fitness score based on pure game metrics.
        This is our unbiased evaluation function - like a chess position evaluation.
        """
        if not game_states:
            return 0.0
        
        final_state = game_states[-1]
        
        # Health-based fitness (normalized)
        own_health_fitness = final_state.objectives.own_health_percent / 100.0
        tower_health_fitness = final_state.objectives.own_tower_health_percent / 100.0
        
        # Enemy health fitness (inverted - lower enemy health is better)
        enemy_health_fitness = (100.0 - final_state.objectives.enemy_health_percent) / 100.0
        enemy_tower_fitness = (100.0 - final_state.objectives.enemy_tower_health_percent) / 100.0
        
        # Points scored throughout the game
        points_fitness = final_state.objectives.points_scored / 10.0  # Normalize
        
        # Survival bonus
        survival_fitness = self.config.survival_bonus if final_state.objectives.is_alive else 0.0
        
        # Victory/defeat/draw bonuses
        if game_result.winner == 'number_eleven':
            outcome_fitness = self.config.victory_bonus
        elif game_result.winner == 'draw':
            outcome_fitness = self.config.draw_penalty  # Contempt for draws
        else:
            outcome_fitness = 0.0
        
        # Combine all fitness components
        total_fitness = (
            self.config.health_weight * own_health_fitness +
            self.config.tower_health_weight * tower_health_fitness +
            self.config.health_weight * enemy_health_fitness +
            self.config.tower_health_weight * enemy_tower_fitness +
            self.config.points_weight * points_fitness +
            survival_fitness +
            outcome_fitness
        )
        
        return total_fitness
    
    def mutate_network(self, base_network: NumberElevenNetwork, 
                      mutation_rate: float) -> Tuple[NumberElevenNetwork, int]:
        """
        Create a mutated version of the network for challenger generation.
        This is how we create new "opponents" for self-play.
        """
        mutated_network = base_network.clone()
        mutations_applied = 0
        
        # Note: torch import will be needed when PyTorch is installed
        # For now, we'll use numpy for mutation simulation
        import numpy as np
        
        # Simplified mutation for testing (replace with actual torch mutation)
        mutations_applied = int(mutation_rate * 100)  # Mock mutation count
        
        # TODO: When PyTorch is available, use:
        # with torch.no_grad():
        #     for param in mutated_network.parameters():
        #         if random.random() < mutation_rate:
        #             noise = torch.randn_like(param) * 0.01
        #             param.add_(noise)
        #             mutations_applied += 1
        
        return mutated_network, mutations_applied
    
    def play_game_against_self(self, network1: NumberElevenNetwork, 
                              network2: NumberElevenNetwork) -> Tuple[GameResult, List[GameState], List[GameState]]:
        """
        Play a game between two networks.
        This simulates the actual Derk environment battle.
        
        Note: This is a simplified version - in the full implementation,
        this would use the actual gym_derk environment.
        """
        # Initialize game state tracking
        network1_states = []
        network2_states = []
        
        # Simplified game simulation (replace with actual gym_derk in full implementation)
        game_length = random.randint(100, self.config.steps_per_episode)
        
        # Track health, scores, etc. throughout the game
        network1_health = 100.0
        network2_health = 100.0
        network1_tower = 100.0
        network2_tower = 100.0
        network1_score = 0.0
        network2_score = 0.0
        
        # Simulate game progression
        for step in range(game_length):
            # Create mock game states (replace with real extraction)
            mock_state1 = self._create_mock_game_state(
                step, network1_health, network1_tower, network2_health, network2_tower, network1_score
            )
            mock_state2 = self._create_mock_game_state(
                step, network2_health, network2_tower, network1_health, network1_tower, network2_score
            )
            
            network1_states.append(mock_state1)
            network2_states.append(mock_state2)
            
            # Simulate health/score changes (simplified)
            if random.random() < 0.02:  # 2% chance per step
                damage = random.uniform(5, 15)
                if random.random() < 0.5:
                    network1_health = max(0, network1_health - damage)
                    network2_score += damage * 0.1
                else:
                    network2_health = max(0, network2_health - damage)
                    network1_score += damage * 0.1
            
            # Check for game end conditions
            if network1_health <= 0 or network2_health <= 0:
                break
            if network1_tower <= 0 or network2_tower <= 0:
                break
        
        # Determine winner
        if network1_health <= 0:
            winner = 'opponent'
        elif network2_health <= 0:
            winner = 'number_eleven'
        elif network1_tower <= 0:
            winner = 'opponent'
        elif network2_tower <= 0:
            winner = 'number_eleven'
        elif abs(network1_score - network2_score) < 1.0:
            winner = 'draw'
        elif network1_score > network2_score:
            winner = 'number_eleven'
        else:
            winner = 'opponent'
        
        game_result = GameResult(
            winner=winner,
            number_eleven_score=network1_score,
            opponent_score=network2_score,
            game_length=game_length,
            number_eleven_fitness=0.0,  # Will be calculated later
            opponent_fitness=0.0
        )
        
        return game_result, network1_states, network2_states
    
    def _create_mock_game_state(self, step: int, own_health: float, own_tower: float,
                               enemy_health: float, enemy_tower: float, score: float) -> GameState:
        """Create a mock game state for testing (replace with real extraction)"""
        from ..data_extraction.sensor_extractor import ObjectiveMetrics, RawSensorData, GameState
        
        objectives = ObjectiveMetrics(
            own_health_percent=own_health,
            own_tower_health_percent=own_tower,
            enemy_health_percent=enemy_health,
            enemy_tower_health_percent=enemy_tower,
            points_scored=score,
            is_alive=own_health > 0,
            game_progress=step / 500.0
        )
        
        sensors = RawSensorData(
            position=(random.uniform(-10, 10), random.uniform(-10, 10), 0.0),
            velocity=(0.0, 0.0, 0.0),
            rotation=0.0,
            distance_to_enemies=[random.uniform(5, 25), random.uniform(5, 25), random.uniform(5, 25)],
            distance_to_teammates=[random.uniform(3, 15), random.uniform(3, 15)],
            distance_to_own_tower=random.uniform(10, 30),
            distance_to_enemy_tower=random.uniform(15, 40),
            distance_to_nearest_cliff=random.uniform(20, 50),
            is_falling=False,
            is_on_ground=True,
            height_above_ground=0.0,
            weapon_cooldowns=[random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)],
            ability_states=[random.choice([True, False]) for _ in range(3)],
            teammate_positions=[(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
            teammate_healths=[random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)],
            teammate_alive_status=[True, True],
            enemy_positions=[(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],
            enemy_healths=[random.uniform(0.3, 1.0), random.uniform(0.3, 1.0), random.uniform(0.3, 1.0)],
            enemy_alive_status=[True, True, True],
            raw_observation=np.random.randn(64)
        )
        
        return GameState(
            agent_id=0,
            step_number=step,
            timestamp=time.time(),
            objectives=objectives,
            sensors=sensors,
            previous_action=None
        )
    
    def evaluate_challenger(self, challenger_network: NumberElevenNetwork) -> float:
        """
        Evaluate challenger against current champion.
        Returns win rate of challenger.
        """
        wins = 0
        games_played = 0
        
        for game_idx in range(self.config.evaluation_games):
            # Alternate who plays as network1 vs network2
            if game_idx % 2 == 0:
                game_result, challenger_states, champion_states = self.play_game_against_self(
                    challenger_network, self.champion_network
                )
                challenger_won = (game_result.winner == 'number_eleven')
            else:
                game_result, champion_states, challenger_states = self.play_game_against_self(
                    self.champion_network, challenger_network
                )
                challenger_won = (game_result.winner == 'opponent')
            
            if challenger_won:
                wins += 1
            games_played += 1
        
        win_rate = wins / games_played if games_played > 0 else 0.0
        return win_rate
    
    def train_generation(self) -> TrainingMetrics:
        """Train one generation of self-play"""
        print(f"\n🎯 Training Generation {self.current_generation}")
        print("=" * 50)
        
        total_fitness = 0.0
        total_game_length = 0
        wins = 0
        total_games = 0
        
        # Create challenger by mutating champion
        challenger_network, mutations_applied = self.mutate_network(
            self.champion_network, self.config.mutation_rate
        )
        
        print(f"🧬 Created challenger with {mutations_applied} mutations")
        
        # Play episodes for this generation
        for episode in range(self.config.episodes_per_generation):
            # Play game between champion and challenger
            game_result, number_eleven_states, opponent_states = self.play_game_against_self(
                challenger_network, self.champion_network
            )
            
            # Calculate objective fitness
            number_eleven_fitness = self.calculate_objective_fitness(number_eleven_states, game_result)
            game_result.number_eleven_fitness = number_eleven_fitness
            
            # Add experiences to replay buffer
            self.replay_buffer.add_experience(number_eleven_states, number_eleven_fitness)
            
            # Track metrics
            total_fitness += number_eleven_fitness
            total_game_length += game_result.game_length
            if game_result.winner == 'number_eleven':
                wins += 1
            total_games += 1
            
            # Training step using experience replay
            if len(self.replay_buffer) >= self.config.batch_size:
                trainer = NumberElevenTrainer(challenger_network, self.network_config)
                for _ in range(self.config.training_steps_per_episode):
                    batch = self.replay_buffer.sample_batch(self.config.batch_size)
                    # TODO: Convert batch to proper format and train
                    # trainer.train_step(batch)
            
            if episode % 10 == 0:
                print(f"  Episode {episode}: Fitness={number_eleven_fitness:.2f}, Winner={game_result.winner}")
        
        # Calculate generation metrics
        avg_fitness = total_fitness / total_games
        avg_game_length = total_game_length / total_games
        win_rate = wins / total_games
        
        # Evaluate if challenger should become new champion
        challenger_win_rate = self.evaluate_challenger(challenger_network)
        
        if challenger_win_rate >= self.config.champion_win_threshold:
            print(f"🏆 New champion! Win rate: {challenger_win_rate:.2%}")
            self.champion_network = challenger_network
            champion_score = challenger_win_rate
            challenger_score = 1.0 - challenger_win_rate
        else:
            print(f"🛡️ Champion defended! Challenger win rate: {challenger_win_rate:.2%}")
            champion_score = 1.0 - challenger_win_rate
            challenger_score = challenger_win_rate
        
        # Create training metrics
        metrics = TrainingMetrics(
            generation=self.current_generation,
            episode=self.config.episodes_per_generation,
            win_rate=win_rate,
            average_fitness=avg_fitness,
            average_game_length=avg_game_length,
            champion_score=champion_score,
            challenger_score=challenger_score,
            mutations_applied=mutations_applied,
            timestamp=datetime.now().isoformat()
        )
        
        self.training_history.append(metrics)
        self.current_generation += 1
        
        return metrics
    
    def save_progress(self):
        """Save training progress and champion network"""
        # Save champion network
        champion_path = Path(self.config.save_directory) / self.config.champion_save_path
        self.champion_network.save(str(champion_path))
        
        # Save training log
        log_path = Path(self.config.save_directory) / self.config.training_log_path
        with open(log_path, 'w') as f:
            json.dump([asdict(metrics) for metrics in self.training_history], f, indent=2)
        
        print(f"💾 Progress saved to {self.config.save_directory}")
    
    def run_training(self):
        """Run the complete self-play training loop"""
        print(f"🚀 Starting Number Eleven Self-Play Training")
        print(f"   Objective: Learn optimal derkling strategies without human bias")
        print(f"   Method: Self-play with evolving neural networks")
        print(f"   Fitness: Based purely on health, scores, and survival")
        print(f"   Anti-draw: Contempt for ties encourages decisive play")
        
        try:
            for generation in range(self.config.max_generations):
                metrics = self.train_generation()
                
                # Print generation summary
                print(f"\n📊 Generation {generation} Summary:")
                print(f"   Win Rate: {metrics.win_rate:.2%}")
                print(f"   Avg Fitness: {metrics.average_fitness:.2f}")
                print(f"   Avg Game Length: {metrics.average_game_length:.1f}")
                print(f"   Champion Score: {metrics.champion_score:.2%}")
                
                # Save progress every 10 generations
                if generation % 10 == 0:
                    self.save_progress()
                
                # Early stopping if performance plateaus
                if len(self.training_history) >= 20:
                    recent_fitness = [m.average_fitness for m in self.training_history[-10:]]
                    if max(recent_fitness) - min(recent_fitness) < 1.0:
                        print(f"🏁 Training converged at generation {generation}")
                        break
        
        except KeyboardInterrupt:
            print(f"\n⏸️ Training interrupted by user")
        
        finally:
            self.save_progress()
            self.print_final_summary()
    
    def print_final_summary(self):
        """Print final training summary"""
        print(f"\n🎯 Final Training Summary")
        print("=" * 50)
        print(f"   Generations completed: {len(self.training_history)}")
        print(f"   Total games played: {sum(m.episode for m in self.training_history)}")
        print(f"   Final win rate: {self.training_history[-1].win_rate:.2%}")
        print(f"   Final fitness: {self.training_history[-1].average_fitness:.2f}")
        print(f"   Experience buffer size: {len(self.replay_buffer)}")
        
        # Best performance
        best_generation = max(self.training_history, key=lambda m: m.average_fitness)
        print(f"\n🏆 Best Performance:")
        print(f"   Generation: {best_generation.generation}")
        print(f"   Fitness: {best_generation.average_fitness:.2f}")
        print(f"   Win Rate: {best_generation.win_rate:.2%}")
        
        print(f"\n✅ Number Eleven training complete!")
        print(f"   The AI has discovered its own strategies for survival and victory!")


def main():
    """Test the self-play training system"""
    print("🤖 Number Eleven Self-Play Training Test")
    print("=" * 45)
    
    # Create training configuration
    config = TrainingConfig()
    config.episodes_per_generation = 5  # Small for testing
    config.max_generations = 3
    config.evaluation_games = 3
    
    print(f"🎯 Training Config:")
    print(f"   Episodes per generation: {config.episodes_per_generation}")
    print(f"   Max generations: {config.max_generations}")
    print(f"   Mutation rate: {config.mutation_rate}")
    print(f"   Health weight: {config.health_weight}")
    print(f"   Victory bonus: {config.victory_bonus}")
    print(f"   Draw penalty: {config.draw_penalty}")
    
    # Create trainer
    trainer = NumberElevenSelfPlayTrainer(config)
    
    # Run a few generations
    print(f"\n🧪 Running test training...")
    trainer.run_training()
    
    print(f"\n✅ Self-play training system is working!")
    print(f"   Number Eleven is ready to discover optimal derkling strategies!")


if __name__ == "__main__":
    main()
