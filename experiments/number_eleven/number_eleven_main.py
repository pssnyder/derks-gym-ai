"""
Number Eleven Main Launch Script
===============================

Main entry point for Number Eleven self-learning derkling AI.
This script provides a command-line interface for all Number Eleven operations.

Usage:
    python number_eleven_main.py [command] [options]

Commands:
    analyze-data    - Analyze gym-derk observation structure
    test-network    - Test neural network architecture
    train          - Start self-play training
    evaluate       - Evaluate against existing brains
    battle         - Single battle against specific opponent
    dashboard      - Launch training dashboard (future)

Examples:
    python number_eleven_main.py analyze-data
    python number_eleven_main.py train --generations 100
    python number_eleven_main.py evaluate --games-per-opponent 5
    python number_eleven_main.py battle --opponent "The Assaulter"
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(Path(__file__).parent))

# Number Eleven imports
try:
    from data_extraction.sensor_extractor import NumberElevenDataExtractor
    from neural_network.number_eleven_network import NumberElevenNetwork, NetworkConfig
    from training.self_play_trainer import NumberElevenSelfPlayTrainer, TrainingConfig
    from evaluation.number_eleven_evaluator import NumberElevenEvaluator
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("Running in limited mode - some features may not be available")


def analyze_data():
    """Analyze gym-derk observation structure"""
    print("🔍 Number Eleven: Data Structure Analysis")
    print("=" * 45)
    
    try:
        from gym_derk.envs import DerkEnv
        
        extractor = NumberElevenDataExtractor()
        env = DerkEnv(n_arenas=1, turbo_mode=True)
        
        print("📊 Analyzing gym-derk observation structure...")
        obs_n = extractor.analyze_observation_structure(env)
        
        if obs_n is not None:
            print("✅ Analysis complete! Check output above for observation mapping.")
        else:
            print("❌ Failed to get observations from environment")
        
        env.close()
        
    except ImportError:
        print("⚠️ gym-derk not installed. Install with: pip install gym-derk")
    except Exception as e:
        print(f"❌ Analysis failed: {e}")


def test_network():
    """Test neural network architecture"""
    print("🧠 Number Eleven: Neural Network Test")
    print("=" * 40)
    
    try:
        # Test network creation and forward pass
        config = NetworkConfig()
        print(f"Creating network with config:")
        print(f"  Raw observation dim: {config.raw_observation_dim}")
        print(f"  Hidden dim: {config.gru_hidden_dim}")
        print(f"  Device: {config.device}")
        
        network = NumberElevenNetwork(config)
        total_params = sum(p.numel() for p in network.parameters() if hasattr(p, 'numel'))
        print(f"  Total parameters: {total_params if total_params else 'N/A (PyTorch not available)'}")
        
        print("✅ Neural network architecture is ready!")
        
    except ImportError as e:
        print(f"⚠️ PyTorch not installed. Install with: pip install torch")
        print(f"   Error: {e}")
    except Exception as e:
        print(f"❌ Network test failed: {e}")


def train(args):
    """Start self-play training"""
    print("🚀 Number Eleven: Self-Play Training")
    print("=" * 40)
    
    try:
        # Create training configuration
        config = TrainingConfig()
        
        # Apply command line arguments
        if args.generations:
            config.max_generations = args.generations
        if args.episodes:
            config.episodes_per_generation = args.episodes
        if args.mutation_rate:
            config.mutation_rate = args.mutation_rate
        
        print(f"Training configuration:")
        print(f"  Max generations: {config.max_generations}")
        print(f"  Episodes per generation: {config.episodes_per_generation}")
        print(f"  Mutation rate: {config.mutation_rate}")
        
        # Create trainer and start training
        trainer = NumberElevenSelfPlayTrainer(config)
        trainer.run_training()
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()


def evaluate(args):
    """Evaluate against existing brains"""
    print("⚔️ Number Eleven: Evaluation Tournament")
    print("=" * 42)
    
    try:
        # Load network if specified
        network_path = args.network if args.network else None
        
        # Create evaluator
        evaluator = NumberElevenEvaluator(network_path)
        
        # Run evaluation
        games_per_opponent = args.games_per_opponent if args.games_per_opponent else 3
        results = evaluator.evaluate_against_all_opponents(games_per_opponent)
        
        # Print summary
        evaluator.print_strategic_evolution_summary()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"experiments/number_eleven/evaluation/evaluation_{timestamp}.json"
        evaluator.save_evaluation_results(save_path)
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()


def battle(args):
    """Single battle against specific opponent"""
    print(f"⚔️ Number Eleven vs {args.opponent}")
    print("=" * 40)
    
    try:
        # Load network if specified
        network_path = args.network if args.network else None
        evaluator = NumberElevenEvaluator(network_path)
        
        # Find opponent
        opponent_name = args.opponent
        if opponent_name not in evaluator.opponent_brain_classes:
            print(f"❌ Unknown opponent: {opponent_name}")
            print(f"Available opponents: {list(evaluator.opponent_brain_classes.keys())}")
            return
        
        # Create mock opponent for testing
        class MockOpponent:
            def __init__(self, name):
                self.__name__ = name
        
        mock_opponent = MockOpponent(evaluator.opponent_brain_classes[opponent_name])
        
        # Run battle
        num_games = args.games if args.games else 5
        result = evaluator.battle_against_brain(mock_opponent, num_games)
        
        print(f"\n🏆 Battle Results:")
        print(f"   Win Rate: {result.win_rate:.2%}")
        print(f"   Games Won: {result.number_eleven_wins}/{result.total_games}")
        print(f"   Average Fitness: {result.average_fitness:.2f}")
        
    except Exception as e:
        print(f"❌ Battle failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Number Eleven: Self-Learning Derkling AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python number_eleven_main.py analyze-data
  python number_eleven_main.py test-network
  python number_eleven_main.py train --generations 100
  python number_eleven_main.py evaluate --games-per-opponent 5
  python number_eleven_main.py battle --opponent "The Assaulter" --games 3
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze data command
    subparsers.add_parser('analyze-data', help='Analyze gym-derk observation structure')
    
    # Test network command
    subparsers.add_parser('test-network', help='Test neural network architecture')
    
    # Training command
    train_parser = subparsers.add_parser('train', help='Start self-play training')
    train_parser.add_argument('--generations', type=int, help='Maximum generations to train')
    train_parser.add_argument('--episodes', type=int, help='Episodes per generation')
    train_parser.add_argument('--mutation-rate', type=float, help='Mutation rate for evolution')
    
    # Evaluation command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate against existing brains')
    eval_parser.add_argument('--network', type=str, help='Path to trained network file')
    eval_parser.add_argument('--games-per-opponent', type=int, help='Games to play against each opponent')
    
    # Battle command
    battle_parser = subparsers.add_parser('battle', help='Single battle against specific opponent')
    battle_parser.add_argument('--opponent', type=str, required=True, help='Opponent brain name')
    battle_parser.add_argument('--network', type=str, help='Path to trained network file')
    battle_parser.add_argument('--games', type=int, help='Number of games to play')
    
    args = parser.parse_args()
    
    # Show header
    print("🤖 Number Eleven: Self-Learning Derkling AI")
    print("=" * 43)
    print("Objective: Discover optimal strategies without human bias")
    print("Method: Self-play with pure objective optimization")
    print()
    
    # Execute command
    if args.command == 'analyze-data':
        analyze_data()
    elif args.command == 'test-network':
        test_network()
    elif args.command == 'train':
        train(args)
    elif args.command == 'evaluate':
        evaluate(args)
    elif args.command == 'battle':
        battle(args)
    else:
        parser.print_help()
        print("\n💡 Start with 'analyze-data' to understand the observation structure")
        print("💡 Then 'test-network' to verify the neural architecture")
        print("💡 Finally 'train' to begin self-play learning!")


if __name__ == "__main__":
    main()
