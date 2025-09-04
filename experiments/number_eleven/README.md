# Number Eleven: Self-Learning Derkling AI

## Project Overview
Number Eleven is a revolutionary self-learning AI derkling that discovers optimal strategies through self-play, similar to AlphaZero. Unlike other derklings that are trained with human-designed reward functions and biases, Number Eleven learns purely from objective game metrics and raw sensor data.

## Core Philosophy: Unbiased Discovery

### What Makes Number Eleven Different
- **No Human Bias**: No predetermined strategies or subjective "good" behaviors
- **Objective Metrics Only**: Health percentages and scores as primary fitness signals
- **Raw Sensor Data**: All environmental data provided without interpretation
- **Self-Discovery**: AI determines its own strategies for winning and survival
- **Contempt for Draws**: Designed to push for decisive victories, not stalemates

### Reward vs Fitness Function
Drawing from chess engine concepts, Number Eleven uses:

**Objective Fitness Function** (like chess position evaluation):
- Own health percentage (0-100%) - higher is better
- Own tower health (0-100%) - higher is better  
- Enemy health percentage (0-100%) - lower is better
- Enemy tower health (0-100%) - lower is better
- Points scored during battle - continuous evaluation signal
- Survival status - critical for learning
- Victory/defeat/draw outcomes with contempt for ties

**Raw Sensor Data** (no good/bad labels):
- Position coordinates and movement vectors
- Distances to enemies, teammates, towers, cliffs
- Weapon/ability states and cooldowns
- Environmental hazards and status
- All 64 observation dimensions from gym-derk

## Architecture

### Neural Network: GRU-Based Sequential Learning
```
Input Layer:
├── Raw Observations (64 dims) → Embedding (128)
├── Objective Metrics (7 dims) → Embedding (64)  
└── Combined → (192 dims)

Sequential Processing:
└── GRU Layers (256 hidden, 2 layers) → Context Understanding

Output Heads:
├── Action Policy (5 actions) → What to do
└── Value Estimation (1 value) → Position evaluation
```

### Training Method: Self-Play Evolution
```
Generation Loop:
1. Champion Network (current best)
2. Create Challenger (mutated champion)
3. Self-Play Games (champion vs challenger)
4. Objective Fitness Evaluation
5. Tournament (challenger vs champion)
6. Evolution (best becomes new champion)
```

## Project Structure

```
experiments/number_eleven/
├── README.md                    # This file
├── data_extraction/            # Game state and sensor data extraction
│   └── sensor_extractor.py     # Comprehensive data extraction from gym-derk
├── neural_network/             # GRU-based AI architecture  
│   └── number_eleven_network.py # Network, training, and action generation
├── training/                   # Self-play training pipeline
│   └── self_play_trainer.py    # AlphaZero-style self-play system
├── evaluation/                 # Performance testing and analysis
│   └── number_eleven_evaluator.py # Tournament testing vs existing brains
└── experiments/               # Training runs and results
```

## Key Features

### 1. Comprehensive Data Extraction (`sensor_extractor.py`)
- Maps all 64 gym-derk observation dimensions to meaningful data
- Separates objective metrics from raw sensor data
- Handles teammate and enemy information for dynamic cooperation
- Extracts equipment states, distances, and environmental conditions

### 2. Advanced Neural Architecture (`number_eleven_network.py`)
- GRU-based recurrent processing for sequential game understanding
- Dual-head output: action policy + position evaluation
- Proper action space mapping for gym-derk format
- Deterministic and stochastic action generation modes

### 3. Self-Play Training System (`self_play_trainer.py`)
- Champion vs challenger tournament system
- Mutation-based evolution for strategy discovery
- Experience replay buffer for learning efficiency
- Objective fitness calculation without human bias
- Contempt for draws to encourage decisive play

### 4. Evaluation & Analysis (`number_eleven_evaluator.py`)
- Tournament testing against all existing derkling brains
- Strategic insight generation and evolution tracking
- Performance analysis and adaptation pattern detection
- Brain adapter for compatibility with existing battle systems

## Installation & Setup

### Prerequisites
```bash
# Core dependencies
pip install torch numpy gym-derk

# Optional for visualization
pip install matplotlib seaborn
```

### Quick Start
```python
# 1. Data extraction test
cd data_extraction
python sensor_extractor.py

# 2. Neural network test  
cd neural_network
python number_eleven_network.py

# 3. Self-play training
cd training
python self_play_trainer.py

# 4. Evaluation tournament
cd evaluation
python number_eleven_evaluator.py
```

## Training Philosophy: Pure Discovery

### What Number Eleven Learns
Number Eleven discovers strategies through pure optimization without human guidance:

**Objective Goals** (the only labeled signals):
- Maximize own health and tower health
- Minimize enemy health and tower health  
- Maximize points scored
- Achieve victory, avoid defeat, despise draws

**Strategic Discovery** (emerges naturally):
- When to attack vs defend
- How to use teammates effectively
- Equipment and ability optimization
- Positioning and movement patterns
- Risk vs reward calculations

### What Makes It Powerful
1. **No Human Limitations**: Not constrained by human strategic assumptions
2. **Adaptive Learning**: Evolves strategies based on what actually works
3. **Objective Optimization**: Optimizes for measurable game outcomes
4. **Continuous Evolution**: Always improving through self-competition

## Usage Examples

### Training a New Number Eleven
```python
from training.self_play_trainer import NumberElevenSelfPlayTrainer, TrainingConfig

# Configure training
config = TrainingConfig()
config.episodes_per_generation = 100
config.max_generations = 500
config.mutation_rate = 0.05

# Start training
trainer = NumberElevenSelfPlayTrainer(config)
trainer.run_training()
```

### Evaluating Against Existing Brains
```python
from evaluation.number_eleven_evaluator import NumberElevenEvaluator

# Load trained network and evaluate
evaluator = NumberElevenEvaluator("champion_network.pth")
results = evaluator.evaluate_against_all_opponents(games_per_opponent=10)
evaluator.print_strategic_evolution_summary()
```

### Using Number Eleven in Battles
```python
from evaluation.number_eleven_evaluator import NumberElevenBrain
from neural_network.number_eleven_network import NumberElevenNetwork

# Load network and create brain
network = NumberElevenNetwork.load("champion_network.pth")
brain = NumberElevenBrain(network, data_extractor)

# Use in existing battle systems
action = brain.get_action(observation)
```

## Expected Evolution Patterns

### Early Training (Generations 1-50)
- Random exploration and basic survival learning
- Discovery of fundamental game mechanics
- Learning to use weapons and abilities

### Mid Training (Generations 50-200)
- Strategic pattern recognition
- Teammate cooperation or competition strategies
- Opponent-specific adaptation

### Advanced Training (Generations 200+)
- Sophisticated meta-strategies
- Complex positioning and timing
- Potential discovery of novel tactics humans haven't considered

## Monitoring Progress

### Key Metrics to Watch
- **Win Rate Progression**: Should increase over generations
- **Average Fitness**: Objective evaluation of game performance
- **Strategic Diversity**: Different behaviors against different opponents
- **Game Length Trends**: May indicate aggressive vs defensive learning

### Evaluation Insights
The evaluation system generates strategic insights such as:
- "Excels against aggressive opponents - learned defensive positioning"
- "Strong breakthrough tactics against defensive play"
- "High fitness suggests robust strategy discovery"

## Theoretical Implications

Number Eleven represents a fascinating experiment in:

1. **Unbiased Strategy Discovery**: What strategies emerge without human preconceptions?
2. **Objective Optimization**: How effectively can AI optimize for measurable outcomes?
3. **Emergent Cooperation**: Will it learn to help or exploit teammates?
4. **Meta-Learning**: Can it adapt its strategy based on opponent patterns?

## Future Enhancements

### Planned Features
- [ ] Integration with full gym-derk environment
- [ ] Advanced mutation strategies (genetic algorithms)
- [ ] Multi-agent team learning
- [ ] Strategy visualization and interpretation tools
- [ ] Real-time adaptation during battles

### Research Directions
- [ ] Comparison with human-designed strategies
- [ ] Analysis of emergent tactical patterns
- [ ] Transfer learning to other game environments
- [ ] Explainable AI for strategy interpretation

## Contributing

Number Eleven is designed for experimentation and extension:

1. **Data Extraction**: Add new sensor modalities or improve state representation
2. **Neural Architecture**: Experiment with different network designs
3. **Training Methods**: Implement new self-play or evolution strategies
4. **Evaluation**: Create new tournament formats or analysis tools

## Philosophy: Let the AI Discover

> "The best way to discover what strategies actually work is to let an unbiased AI figure it out through pure optimization of objective outcomes. Number Eleven doesn't know what 'should' work - it only knows what does work."

Number Eleven embodies the principle that intelligence can emerge from the intersection of:
- Clear objective functions
- Rich environmental data  
- Powerful learning algorithms
- Unlimited exploration time

The question isn't what we think the AI should learn - it's what the AI will discover that we never thought of.

---

**Status**: 🚧 In Development - Core architecture complete, full gym-derk integration in progress

**Next Milestone**: Complete integration with gym-derk environment for real battles against existing derkling brains.
