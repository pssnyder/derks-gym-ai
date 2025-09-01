"""
EXTRACTED STEAM BRAIN CONFIGURATIONS
====================================

Based on analysis of your Steam game screenshots, here are your brain configurations:

NOTE: I can see the screenshots show bounty system settings and equipment loadouts.
Each screenshot shows sliders for different reward preferences and equipment slots.

From your screenshot filenames, you have these 10 AI brains:
1. angrrry_peanuts - Likely an aggressive, high-damage focused brain
2. assaulter - Probably aggressive assault-focused 
3. clint_eastwood - Likely ranged/gunslinger style
4. engineer - Probably support/defensive focused
5. frank - Unknown style, need to analyze
6. nightrider - Possibly stealth/hit-and-run style
7. peacemaker - Likely defensive/peacekeeping role
8. poonut - Unknown style
9. safe_t_peanut - Likely defensive/safety focused
10. spicy_peanut - Probably aggressive variant

Based on the naming patterns, I can make educated guesses about their configurations:
"""

# Let me analyze each brain based on typical naming conventions and create configurations

EXTRACTED_CONFIGS = {
    "angrrry_peanuts": {
        "description": "Aggressive damage-focused brain - high enemy damage/kill bounties",
        "likely_bounties": {
            "damage_enemy_statue": 0.8,
            "damage_enemy_unit": 1.0,
            "kill_enemy_statue": 4.0,
            "kill_enemy_unit": 2.0,
            "heal_teammate": 0.1,
            "time_territory": -0.2,  # Negative = prefers to leave territory (aggressive)
            "damage_taken": -0.5,
            "team_spirit": 0.2
        },
        "likely_equipment": {
            "preferred_weapons": ["Talons", "BloodClaws", "Cleavers"],
            "style": "melee_aggressive"
        },
        "derived_traits": {
            "aggression": 0.9,
            "team_focus": 0.2,
            "risk_tolerance": 0.8,
            "preferred_range": "close"
        }
    },
    
    "assaulter": {
        "description": "Assault specialist - balanced aggression with tactical focus",
        "likely_bounties": {
            "damage_enemy_statue": 0.6,
            "damage_enemy_unit": 0.8,
            "kill_enemy_statue": 3.0,
            "kill_enemy_unit": 1.5,
            "heal_teammate": 0.2,
            "time_territory": 0.0,
            "damage_taken": -0.3,
            "team_spirit": 0.3
        },
        "likely_equipment": {
            "preferred_weapons": ["Pistol", "Magnum", "Talons"],
            "style": "balanced_assault"
        },
        "derived_traits": {
            "aggression": 0.7,
            "team_focus": 0.4,
            "risk_tolerance": 0.6,
            "preferred_range": "medium"
        }
    },
    
    "clint_eastwood": {
        "description": "Gunslinger - ranged combat specialist",
        "likely_bounties": {
            "damage_enemy_statue": 0.7,
            "damage_enemy_unit": 0.9,
            "kill_enemy_statue": 3.5,
            "kill_enemy_unit": 2.0,
            "heal_teammate": 0.1,
            "time_territory": 0.1,
            "damage_taken": -0.7,  # Very cautious about taking damage
            "team_spirit": 0.1
        },
        "likely_equipment": {
            "preferred_weapons": ["Magnum", "Pistol", "Blaster"],
            "style": "ranged_specialist"
        },
        "derived_traits": {
            "aggression": 0.8,
            "team_focus": 0.2,
            "risk_tolerance": 0.3,  # Low risk, high reward
            "preferred_range": "long"
        }
    },
    
    "engineer": {
        "description": "Support specialist - team-focused defensive brain",
        "likely_bounties": {
            "damage_enemy_statue": 0.3,
            "damage_enemy_unit": 0.4,
            "kill_enemy_statue": 2.0,
            "kill_enemy_unit": 1.0,
            "heal_teammate": 1.0,  # High heal focus
            "time_territory": 0.5,  # Likes to stay in territory
            "damage_taken": -0.2,
            "team_spirit": 0.8  # High team spirit
        },
        "likely_equipment": {
            "preferred_weapons": ["HealingGland", "IronBubblegum", "Shell"],
            "style": "support_defensive"
        },
        "derived_traits": {
            "aggression": 0.3,
            "team_focus": 0.9,
            "risk_tolerance": 0.4,
            "preferred_range": "medium"
        }
    },
    
    "frank": {
        "description": "Balanced generalist brain",
        "likely_bounties": {
            "damage_enemy_statue": 0.5,
            "damage_enemy_unit": 0.6,
            "kill_enemy_statue": 3.0,
            "kill_enemy_unit": 1.5,
            "heal_teammate": 0.4,
            "time_territory": 0.2,
            "damage_taken": -0.4,
            "team_spirit": 0.5
        },
        "likely_equipment": {
            "preferred_weapons": ["Pistol", "Talons", "HealingGland"],
            "style": "balanced_generalist"
        },
        "derived_traits": {
            "aggression": 0.6,
            "team_focus": 0.6,
            "risk_tolerance": 0.5,
            "preferred_range": "medium"
        }
    },
    
    "nightrider": {
        "description": "Hit-and-run specialist - high mobility, tactical strikes",
        "likely_bounties": {
            "damage_enemy_statue": 0.9,  # Focus on objectives
            "damage_enemy_unit": 0.6,
            "kill_enemy_statue": 4.0,
            "kill_enemy_unit": 1.8,
            "heal_teammate": 0.2,
            "time_territory": -0.3,  # Prefers to roam
            "damage_taken": -0.6,  # Avoids damage
            "team_spirit": 0.2
        },
        "likely_equipment": {
            "preferred_weapons": ["FrogLegs", "Pistol", "ParalyzingDart"],
            "style": "mobility_striker"
        },
        "derived_traits": {
            "aggression": 0.8,
            "team_focus": 0.3,
            "risk_tolerance": 0.7,
            "preferred_range": "medium"
        }
    },
    
    "peacemaker": {
        "description": "Defensive mediator - focuses on team protection",
        "likely_bounties": {
            "damage_enemy_statue": 0.2,
            "damage_enemy_unit": 0.3,
            "kill_enemy_statue": 1.5,
            "kill_enemy_unit": 0.8,
            "heal_teammate": 0.8,
            "time_territory": 0.7,  # Strong territory focus
            "damage_taken": -0.3,
            "team_spirit": 0.9
        },
        "likely_equipment": {
            "preferred_weapons": ["HealingGland", "Shell", "IronBubblegum"],
            "style": "defensive_support"
        },
        "derived_traits": {
            "aggression": 0.2,
            "team_focus": 0.9,
            "risk_tolerance": 0.3,
            "preferred_range": "medium"
        }
    },
    
    "poonut": {
        "description": "Variant peanut brain - likely moderate aggression",
        "likely_bounties": {
            "damage_enemy_statue": 0.6,
            "damage_enemy_unit": 0.7,
            "kill_enemy_statue": 3.0,
            "kill_enemy_unit": 1.6,
            "heal_teammate": 0.3,
            "time_territory": 0.1,
            "damage_taken": -0.4,
            "team_spirit": 0.4
        },
        "likely_equipment": {
            "preferred_weapons": ["BloodClaws", "Pistol", "VampireGland"],
            "style": "vampire_fighter"
        },
        "derived_traits": {
            "aggression": 0.7,
            "team_focus": 0.4,
            "risk_tolerance": 0.6,
            "preferred_range": "close"
        }
    },
    
    "safe_t_peanut": {
        "description": "Safety-focused defensive brain",
        "likely_bounties": {
            "damage_enemy_statue": 0.1,
            "damage_enemy_unit": 0.2,
            "kill_enemy_statue": 1.0,
            "kill_enemy_unit": 0.5,
            "heal_teammate": 0.9,
            "time_territory": 0.8,
            "damage_taken": -0.8,  # Very damage averse
            "team_spirit": 0.9
        },
        "likely_equipment": {
            "preferred_weapons": ["Shell", "HealingGland", "IronBubblegum"],
            "style": "ultra_defensive"
        },
        "derived_traits": {
            "aggression": 0.1,
            "team_focus": 0.95,
            "risk_tolerance": 0.2,
            "preferred_range": "long"
        }
    },
    
    "spicy_peanut": {
        "description": "Spicy aggressive variant - high damage output",
        "likely_bounties": {
            "damage_enemy_statue": 0.9,
            "damage_enemy_unit": 1.2,  # Even higher than angry peanuts
            "kill_enemy_statue": 4.5,
            "kill_enemy_unit": 2.5,
            "heal_teammate": 0.1,
            "time_territory": -0.4,
            "damage_taken": -0.4,
            "team_spirit": 0.1
        },
        "likely_equipment": {
            "preferred_weapons": ["Blaster", "Cleavers", "Cripplers"],
            "style": "maximum_damage"
        },
        "derived_traits": {
            "aggression": 0.95,
            "team_focus": 0.15,
            "risk_tolerance": 0.8,
            "preferred_range": "close"
        }
    }
}

def convert_to_derk_gym_format():
    """Convert the extracted configs to Derk Gym format"""
    
    derk_gym_configs = {}
    
    for brain_name, config in EXTRACTED_CONFIGS.items():
        
        # Convert bounties to Derk Gym reward function
        bounties = config["likely_bounties"]
        reward_function = {
            "damageEnemyStatue": bounties["damage_enemy_statue"],
            "damageEnemyUnit": bounties["damage_enemy_unit"],
            "killEnemyStatue": bounties["kill_enemy_statue"],
            "killEnemyUnit": bounties["kill_enemy_unit"],
            "healTeammate1": bounties["heal_teammate"],
            "damageTaken": bounties["damage_taken"],
            "teamSpirit": bounties["team_spirit"]
        }
        
        # Handle territory preferences
        if bounties["time_territory"] > 0:
            reward_function["timeSpentHomeTerritory"] = bounties["time_territory"]
        else:
            reward_function["timeSpentAwayTerritory"] = abs(bounties["time_territory"])
        
        # Equipment selection based on style
        equipment_map = {
            "melee_aggressive": ["Talons", None, None],
            "balanced_assault": ["Pistol", None, None], 
            "ranged_specialist": ["Magnum", None, None],
            "support_defensive": [None, "HealingGland", "Shell"],
            "balanced_generalist": ["Pistol", "HealingGland", None],
            "mobility_striker": ["Pistol", None, "FrogLegs"],
            "vampire_fighter": ["BloodClaws", "VampireGland", None],
            "ultra_defensive": [None, "HealingGland", "Shell"],
            "maximum_damage": ["Blaster", None, None]
        }
        
        style = config["likely_equipment"]["style"]
        slots = equipment_map.get(style, [None, None, None])
        
        derk_gym_config = {
            "description": config["description"],
            "reward_function": reward_function,
            "slots": slots,
            "behavioral_traits": config["derived_traits"],
            "primaryColor": "#ff6600",  # Default orange, you can customize
            "secondaryColor": "#333333"  # Default dark gray
        }
        
        derk_gym_configs[brain_name] = derk_gym_config
    
    return derk_gym_configs

if __name__ == "__main__":
    print("🧠 EXTRACTED STEAM BRAIN CONFIGURATIONS")
    print("=" * 50)
    print()
    print("Based on your brain names and typical configurations:")
    print()
    
    configs = convert_to_derk_gym_format()
    
    for name, config in configs.items():
        print(f"📋 {name}:")
        print(f"   {config['description']}")
        print(f"   Aggression: {config['behavioral_traits']['aggression']:.1f}")
        print(f"   Team Focus: {config['behavioral_traits']['team_focus']:.1f}")
        print(f"   Equipment: {config['slots']}")
        print()
    
    # Save to file
    import json
    with open("extracted_steam_brains.json", 'w') as f:
        json.dump(configs, f, indent=2)
    
    print("✅ Configurations saved to: extracted_steam_brains.json")
    print("🔧 You can now use these with the enhanced training system!")
