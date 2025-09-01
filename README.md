# Derk's Gym AI - Steam Brain Migration

This repository contains the complete migration of custom AI "brains" from the Steam version of Dr.K's game into the Derk Gym reinforcement learning environment.

## 📁 Repository Structure

```
derks-gym-ai/
├── brain_profiles/           # 🧠 Main brain implementations
│   ├── peanut_class/        # Team-oriented fighters
│   │   ├── spicy_peanut.py
│   │   ├── safe_t_peanut.py
│   │   ├── nightrider_peanut.py
│   │   ├── angrrry_peanut.py
│   │   └── poonut.py
│   ├── lone_wolf_class/     # Solo specialists
│   │   └── clint_eastwood.py
│   ├── testing_class/       # Experimental builds
│   │   ├── the_assaulter.py
│   │   ├── the_engineer.py
│   │   └── the_peacemaker.py
│   ├── special/             # Unique operations
│   │   └── frank.py
│   └── brain_summary.py     # Complete overview
├── data/                    # 📊 Configuration data
│   ├── extracted_steam_brains.json
│   └── my_steam_brains.json
├── reference_config_imgs/   # 📸 Original Steam screenshots
├── migration_tools/         # 🔧 Migration utilities
├── archived_files/          # 📦 Old versions
├── requirements.txt         # 📋 Dependencies
├── train-derk.py           # 🚀 Main training script
└── .gitignore              # 🚫 Git exclusions
```

## 🧠 Available Brain Profiles (10 Total)

### 🥜 Peanut Class - Team Players
- **Spicy Peanut** - Aggressive duo fighter (bonded with Safe T Peanut)
- **Safe T Peanut** - Defensive team fighter (bonded with Spicy Peanut)
- **Nightrider Peanut** - Kill-focused balanced fighter
- **Angrrry Peanut** - Hyper-aggressive berserker (200pt kills)
- **Poonut** - Conservative support fighter (ultra-defensive)

### 🤠 Lone Wolf Class - Solo Specialists
- **Clint Eastwood** - Ranged combat specialist

### 🧪 Testing Class - Experimental
- **The Assaulter** - Pure aggression fighter
- **The Engineer** - Defensive support specialist
- **The Peacemaker** - Balanced control specialist

### 🎯 Special Class - Unique Operations
- **Frank** - Special operations and infiltration

## 🚀 Quick Start

### Test Individual Brain
```python
from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain

brain = SpicyPeanutBrain()
results = test_spicy_peanut()  # Built-in test function
```

### Create Team Composition
```python
# Peanut Gang Team
from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain
from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
from brain_profiles.peanut_class.angrrry_peanut import AngrrryPeanutBrain

team = [SpicyPeanutBrain(), SafeTPeanutBrain(), AngrrryPeanutBrain()]
```

### Export Configuration for Derk Gym
```python
brain = SpicyPeanutBrain()
config = brain.get_derk_gym_config()
# Use config in DerkEnv setup
```

## 📊 Brain Characteristics

| Brain | Aggression | Team Focus | Risk Tolerance | Primary Strategy |
|-------|------------|------------|----------------|------------------|
| Angrrry Peanut | 1.0 | 0.8 | 0.9 | Kill everything |
| The Assaulter | 1.0 | 0.6 | 0.8 | Pure assault |
| Frank | 0.8 | 0.3 | 0.4 | Special ops |
| Spicy Peanut | 0.8 | 0.8 | 0.6 | Duo fighter |
| Nightrider Peanut | 0.7 | 0.7 | 0.6 | Balanced killer |
| Clint Eastwood | 0.7 | 0.05 | 0.2 | Lone gunslinger |
| The Peacemaker | 0.6 | 0.8 | 0.5 | Balanced control |
| Safe T Peanut | 0.59 | 0.9 | 0.6 | Team defense |
| The Engineer | 0.4 | 0.9 | 0.3 | Support specialist |
| Poonut | 0.3 | 0.95 | 0.1 | Ultra-defensive |

## 🎯 Strategic Combinations

### **The Peanut Gang** (Full Team)
- Spicy Peanut + Safe T Peanut (bonded pair)
- Angrrry Peanut (berserker)
- Poonut (support)

### **Balanced Assault** 
- The Assaulter (frontline)
- The Engineer (support)
- The Peacemaker (control)

### **Special Operations**
- Frank (infiltration)
- Clint Eastwood (overwatch)
- The Engineer (support)

## 📝 Each Brain Profile Includes

- ✅ **Extracted Steam Configuration** - Complete bounty values from screenshots
- ✅ **Behavioral Trait Analysis** - Aggression, team focus, risk tolerance
- ✅ **Strategic Decision Logic** - Complete AI decision-making algorithms
- ✅ **Equipment Preferences** - Recommended weapon loadouts
- ✅ **Derk Gym Configuration** - Ready-to-use environment setup
- ✅ **Individual Test Harness** - Built-in testing capability
- ✅ **Compatibility Matrix** - Team composition guidance

## 🔧 Development Notes

- All brains are rule-based implementations that can be used immediately
- Each brain file is self-contained and testable
- Original Steam configurations preserved in `reference_config_imgs/`
- Migration tools available in `migration_tools/` for future use
- Archived versions in `archived_files/` for reference

## 🎮 Next Steps

1. **Test Individual Brains** - Run built-in test functions
2. **Create Team Compositions** - Mix and match compatible brains
3. **Train RL Agents** - Use rule-based brains as training baselines
4. **Optimize Strategies** - Tune behavioral parameters
5. **Add New Brains** - Use migration tools for future Steam exports

Your Steam brains are now fully operational in Derk Gym! 🎉
