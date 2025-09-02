# Derk's Gym AI - Steam Battle Arena

A Steam-style persistent derkling training and battle system for Derk's Gym.

## Project Structure

```
derks-gym-ai/
├── main.py                 # Main entry point
├── src/                    # Source code
│   ├── steam_battle_arena.py     # Core battle arena
│   └── brain_profiles/           # AI brain implementations
│       ├── peanut_class/
│       │   └── nightrider_peanut.py
│       └── testing_class/
│           └── the_assaulter.py
├── tests/                  # Test files
├── experiments/            # Experimental/archived code
├── results/               # Battle results and training data
├── docs/                  # Documentation
├── venv/                  # Virtual environment
└── requirements.txt       # Dependencies
```

## Features

- **Persistent Configurations**: Derklings maintain their equipment and colors throughout training
- **Custom Reward Functions**: Each brain type uses its own fitness function
- **Steam-Style Training**: Continuous improvement through iterative battles
- **Battle Analytics**: Detailed performance tracking and comparison

## Quick Start

1. Activate virtual environment:
   ```bash
   venv/Scripts/activate  # Windows
   ```

2. Run a battle:
   ```bash
   python main.py
   ```

## Current Status

✅ **Working**:
- Basic environment creation and management
- Brain integration and action generation
- Episode completion and battle tracking
- Custom configuration display

🔍 **Investigating**:
- Zero reward issue (derklings may not be engaging in combat)
- Reward function tuning for meaningful feedback
- Episode length optimization for better battles

## Brain Configurations

### Nightrider Peanut
- Equipment: Unknown, Unknown, Unknown
- Colors: Purple (#4B0082) / Black (#000000)
- Team Spirit: 0.1 (individualistic)

### The Assaulter
- Equipment: Talons, None, None
- Colors: Crimson (#DC143C) / Black (#000000)  
- Team Spirit: 0.6 (team-oriented)

## Next Steps

1. Investigate zero rewards and improve combat engagement
2. Tune reward functions for meaningful feedback
3. Extend training system for continuous improvement
4. Add more brain types and strategies
