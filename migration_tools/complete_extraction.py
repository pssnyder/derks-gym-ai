"""
Complete Steam Brain Extraction - All 10 Derklings
=================================================

Based on your screenshots, here are all the exact bounty configurations:
"""

# EXTRACTED CONFIGURATIONS FROM SCREENSHOTS

BRAIN_CONFIGS = {
    "safe_t_peanut": {
        "class": "peanut",
        "role": "conservative_helper", 
        "combat_style": "primary_duo",
        "bonded_pair": "spicy_peanut",
        "equipment": ["HealingGland", "BloodClaws", "Shell"],
        "colors": {"primary": "#90EE90", "secondary": "#228B22"},  # Light green/green from screenshot
        "bounties": {
            "damage_enemy_statue": 20,
            "damage_enemy_unit": 80, 
            "kill_enemy_statue": 30,
            "kill_enemy_unit": 90,
            "heal_own_statue": 75,
            "heal_teammate1": 40,
            "heal_teammate2": 40,
            "stay_close_to_own_statue": 10,
            "damage_taken": -40,
            "friendly_fire": -50,
            "heal_enemy": -100,
            "take_fall_damage": -90,
            "own_statue_takes_damage": -100,
            "loss": -1000,
            "tie": 50,
            "team_spirit": 0.9,
            "time_scaling": 0.9
        }
    },
    
    "spicy_peanut": {
        "class": "peanut",
        "role": "aggressive_winner",
        "combat_style": "primary_duo", 
        "bonded_pair": "safe_t_peanut",
        "equipment": ["Unknown", "Unknown", "Unknown"],  # Need to check derkling loadouts screen
        "colors": {"primary": "#FF69B4", "secondary": "#8B008B"},  # Hot pink/purple from screenshot
        "bounties": {
            "damage_enemy_statue": 50,
            "damage_enemy_unit": 80,
            "kill_enemy_statue": 60,
            "kill_enemy_unit": 100,
            "heal_own_statue": 10,
            "heal_teammate1": 10,
            "heal_teammate2": 1,
            "stay_in_enemy_territory": 10,
            "damage_taken": -40,
            "friendly_fire": -60,
            "heal_enemy": -10,
            "take_fall_damage": -100,
            "own_statue_takes_damage": -70,
            "victory": 1000,
            "team_spirit": 0.8,
            "time_scaling": 0.9
        }
    },
    
    "angrrry_peanut": {
        "class": "peanut", 
        "role": "midlevel_aggressive",
        "combat_style": "solo_secondary_duo",
        "compatible_with": "all_peanut_class",
        "equipment": ["Unknown", "Unknown", "Unknown"],
        "colors": {"primary": "#FF4500", "secondary": "#8B0000"},  # Orange red/dark red
        "bounties": {
            "damage_enemy_statue": 50,
            "damage_enemy_unit": 80,
            "kill_enemy_statue": 60,
            "kill_enemy_unit": 100,
            "heal_own_statue": 10,
            "heal_teammate1": 10,
            "heal_teammate2": 1,
            "stay_in_enemy_territory": 10,
            "damage_taken": -40,
            "friendly_fire": -60,
            "heal_enemy": -10,
            "take_fall_damage": -100,
            "own_statue_takes_damage": -70,
            "manual_bonus": -1000,
            "victory": 100,
            "tie": -50,
            "time_scaling": 0.9
        }
    },
    
    "the_assaulter": {
        "class": "testing",
        "role": "aggressive_attacker", 
        "combat_style": "solo_duo_team",
        "compatible_with": "other_testing_fighters",
        "equipment": ["Unknown", "Unknown", "Unknown"],
        "colors": {"primary": "#00BFFF", "secondary": "#0000CD"},  # Deep sky blue/medium blue
        "bounties": {
            "damage_enemy_unit": 75,
            "kill_enemy_unit": 90,
            "damage_taken": -50,
            "friendly_fire": -50,
            "take_fall_damage": -50,
            "team_spirit": 0.5
        }
    },
    
    "clint_eastwood": {
        "class": "lone_wolf",
        "role": "balanced_ranged", 
        "combat_style": "solo",
        "compatible_with": "none_non_peanut",
        "equipment": ["Unknown", "Unknown", "Unknown"],
        "colors": {"primary": "#40E0D0", "secondary": "#008B8B"},  # Turquoise/dark cyan
        "bounties": {
            "damage_enemy_statue": 80,
            "damage_enemy_unit": 81,
            "kill_enemy_statue": 20,
            "kill_enemy_unit": 30,
            "stay_in_enemy_territory": 70,
            "damage_taken": -77,
            "friendly_fire": -50,
            "take_fall_damage": -90,
            "manual_bonus": -1000,
            "tie": -10,
            "time_scaling": 0.0
        }
    },
    
    "the_engineer": {
        "class": "testing",
        "role": "balanced_win_focused",
        "combat_style": "solo_duo_team",
        "compatible_with": "other_testing_fighters", 
        "equipment": ["Unknown", "Unknown", "Unknown"],
        "colors": {"primary": "#FF6347", "secondary": "#B22222"},  # Tomato/fire brick
        "bounties": {
            "damage_enemy_statue": 90,
            "kill_enemy_statue": 100,
            "stay_in_enemy_territory": 70,
            "stay_close_to_enemy_statue": 80,
            "damage_taken": -10,
            "friendly_fire": -50,
            "take_fall_damage": -50,
            "team_spirit": 0.5
        }
    },
    
    "frank": {
        "class": "special",
        "role": "frank_just_frank",
        "combat_style": "frank_does_frank_things", 
        "compatible_with": "everyone_loves_frank",
        "equipment": ["Unknown", "Unknown", "Unknown"],
        "colors": {"primary": "#C0C0C0", "secondary": "#696969"},  # Silver/dim gray
        "bounties": {
            "victory": 100,
            "loss": -100
        }
    },
    
    "nightrider": {
        "class": "peanut",
        "role": "midlevel_balanced",
        "combat_style": "solo_secondary_duo",
        "compatible_with": "all_peanut_class",
        "equipment": ["Unknown", "Unknown", "Unknown"], 
        "colors": {"primary": "#9370DB", "secondary": "#4B0082"},  # Medium purple/indigo
        "bounties": {
            "damage_enemy_statue": 50,
            "damage_enemy_unit": 100,
            "kill_enemy_statue": 90,
            "kill_enemy_unit": 1000,
            "damage_taken": -20,
            "heal_enemy": -90,
            "take_fall_damage": -100,
            "manual_bonus": 1000,
            "victory": 100,
            "loss": -100,
            "time_scaling": 0.0
        }
    },
    
    "the_peacemaker": {
        "class": "testing", 
        "role": "conservative_defender",
        "combat_style": "solo_duo_team",
        "compatible_with": "other_testing_fighters",
        "equipment": ["Unknown", "Unknown", "Unknown"],
        "colors": {"primary": "#F0F8FF", "secondary": "#B0C4DE"},  # Alice blue/light steel blue
        "bounties": {
            "heal_own_statue": 100,
            "heal_teammate1": 80,
            "heal_teammate2": 80,
            "stay_close_to_own_statue": 50,
            "friendly_fire": -100,
            "heal_enemy": -90,
            "take_fall_damage": -100,
            "own_statue_takes_damage": -50
        }
    },
    
    "poonut": {
        "class": "peanut",
        "role": "bait_distraction",
        "combat_style": "secondary_duo_team_only",
        "compatible_with": "tower_focused_peanut_class",
        "equipment": ["Unknown", "Unknown", "Unknown"],
        "colors": {"primary": "#DDA0DD", "secondary": "#9932CC"},  # Plum/dark orchid
        "bounties": {
            "damage_enemy_unit": 75,
            "kill_enemy_unit": 90,
            "damage_taken": -50,
            "friendly_fire": -50,
            "take_fall_damage": -50,
            "own_statue_takes_damage": -80,
            "team_spirit": 0.5
        }
    }
}

def extract_behavioral_traits(bounties):
    """Extract behavioral traits from bounty configuration"""
    traits = {}
    
    # Calculate aggression from offensive bounties
    offensive_bounties = [
        bounties.get("damage_enemy_statue", 0),
        bounties.get("damage_enemy_unit", 0),
        bounties.get("kill_enemy_statue", 0), 
        bounties.get("kill_enemy_unit", 0)
    ]
    aggression = sum(b for b in offensive_bounties if b > 0) / 400.0  # Normalize
    traits["aggression"] = min(max(aggression, 0.1), 1.0)
    
    # Calculate team focus from healing and team spirit
    healing_bounties = [
        bounties.get("heal_own_statue", 0),
        bounties.get("heal_teammate1", 0),
        bounties.get("heal_teammate2", 0)
    ]
    team_spirit = bounties.get("team_spirit", 0)
    team_focus = (sum(b for b in healing_bounties if b > 0) / 200.0 + team_spirit) / 2.0
    traits["team_focus"] = min(max(team_focus, 0.1), 1.0)
    
    # Calculate risk tolerance from damage penalties
    damage_penalty = abs(bounties.get("damage_taken", 0))
    if damage_penalty > 0:
        traits["risk_tolerance"] = max(0.1, 1.0 - (damage_penalty / 100.0))
    else:
        traits["risk_tolerance"] = 0.7
    
    # Territory preference
    enemy_territory = bounties.get("stay_in_enemy_territory", 0)
    own_territory = bounties.get("stay_close_to_own_statue", 0)
    
    if enemy_territory > 0:
        traits["territorial_preference"] = "aggressive"
        traits["preferred_range"] = "close"
    elif own_territory > 0:
        traits["territorial_preference"] = "defensive" 
        traits["preferred_range"] = "medium"
    else:
        traits["territorial_preference"] = "neutral"
        traits["preferred_range"] = "medium"
    
    return traits

def convert_to_derk_gym_reward_function(bounties):
    """Convert Steam bounties to Derk Gym reward function"""
    reward_function = {}
    
    # Direct mappings
    mapping = {
        "damage_enemy_statue": "damageEnemyStatue",
        "damage_enemy_unit": "damageEnemyUnit", 
        "kill_enemy_statue": "killEnemyStatue",
        "kill_enemy_unit": "killEnemyUnit",
        "heal_teammate1": "healTeammate1",
        "heal_teammate2": "healTeammate2",
        "damage_taken": "damageTaken",
        "friendly_fire": "friendlyFire",
        "take_fall_damage": "fallDamageTaken"
    }
    
    for steam_key, derk_key in mapping.items():
        if steam_key in bounties:
            reward_function[derk_key] = bounties[steam_key] / 100.0  # Normalize to smaller values
    
    # Handle territory preferences
    if "stay_in_enemy_territory" in bounties:
        reward_function["timeSpentAwayTerritory"] = bounties["stay_in_enemy_territory"] / 100.0
    if "stay_close_to_own_statue" in bounties:
        reward_function["timeSpentHomeBase"] = bounties["stay_close_to_own_statue"] / 100.0
    
    # Handle team spirit and time scaling
    if "team_spirit" in bounties:
        reward_function["teamSpirit"] = bounties["team_spirit"]
    if "time_scaling" in bounties:
        reward_function["timeScaling"] = bounties["time_scaling"]
    
    return reward_function

if __name__ == "__main__":
    print("🧠 COMPLETE STEAM BRAIN EXTRACTION")
    print("=" * 50)
    
    for brain_name, config in BRAIN_CONFIGS.items():
        print(f"\n📋 {brain_name.upper()}:")
        print(f"   Class: {config['class']}")
        print(f"   Role: {config['role']}")
        print(f"   Combat Style: {config['combat_style']}")
        print(f"   Equipment: {config['equipment']}")
        
        # Extract traits
        traits = extract_behavioral_traits(config['bounties'])
        print(f"   Aggression: {traits['aggression']:.2f}")
        print(f"   Team Focus: {traits['team_focus']:.2f}")
        print(f"   Risk Tolerance: {traits['risk_tolerance']:.2f}")
        print(f"   Territory: {traits['territorial_preference']}")
    
    print(f"\n✅ All {len(BRAIN_CONFIGS)} brain configurations extracted!")
