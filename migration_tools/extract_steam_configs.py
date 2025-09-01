"""
Steam Brain Configuration Extractor
===================================

This tool helps you manually extract configuration data from your Steam game
screenshots and convert them to Derk Gym configurations.

Based on your screenshots, I can see you have these brains:
1. angrrry_peanuts
2. assaulter  
3. clint_eastwood
4. engineer
5. frank
6. nightrider
7. peacemaker
8. poonut
9. safe_t_peanut
10. spicy_peanut

Each screenshot shows:
- Bounty system settings (reward preferences)
- Equipment loadouts (weapons and attachments)
- Behavior configurations
"""

import json
import os
from datetime import datetime

class SteamConfigExtractor:
    """Extract Steam brain configurations from screenshots"""
    
    def __init__(self):
        self.configs = {}
        self.screenshots = [
            "angrrry_peanuts",
            "assaulter", 
            "clint_eastwood",
            "engineer",
            "frank", 
            "nightrider",
            "peacemaker",
            "poonut",
            "safe_t_peanut",
            "spicy_peanut"
        ]
    
    def manual_extraction_guide(self):
        """Guide for manually extracting data from screenshots"""
        print("📸 STEAM BRAIN SCREENSHOT ANALYSIS GUIDE")
        print("=" * 50)
        print()
        print("For each screenshot, look for and record:")
        print()
        print("🏆 BOUNTY SYSTEM (Reward Preferences):")
        print("- Damage Enemy Statue: [value]")
        print("- Damage Enemy Unit: [value]") 
        print("- Kill Enemy Statue: [value]")
        print("- Kill Enemy Unit: [value]")
        print("- Heal Teammate: [value]")
        print("- Time Spent in Territory: [value]")
        print("- Damage Taken: [value] (usually negative)")
        print("- Team Spirit: [0.0-1.0]")
        print()
        print("⚔️ EQUIPMENT LOADOUT:")
        print("- Arms Slot: [weapon name or None]")
        print("- Tail Slot: [attachment name or None]") 
        print("- Misc Slot: [misc item name or None]")
        print()
        print("🎭 VISUAL APPEARANCE:")
        print("- Primary Color: [hex color like #ff0000]")
        print("- Secondary Color: [hex color]")
        print("- Ears: [1-4]")
        print("- Eyes: [1-5]")
        print("- Spikes: [1-7]")
        print()
    
    def interactive_extraction(self):
        """Interactive tool to extract configs from screenshots"""
        print("🔍 INTERACTIVE CONFIG EXTRACTION")
        print("=" * 40)
        print("I'll guide you through each brain configuration.")
        print("Look at the corresponding screenshot for each brain.")
        print()
        
        for brain_name in self.screenshots:
            print(f"\n📸 Analyzing: {brain_name}_bounties.JPG")
            print("=" * 50)
            print(f"Please look at the screenshot: {brain_name}_bounties.JPG")
            print()
            
            config = self.extract_single_config(brain_name)
            self.configs[brain_name] = config
            
            continue_prompt = input("\nContinue to next brain? (y/n): ").lower()
            if continue_prompt != 'y':
                break
        
        self.save_extracted_configs()
        return self.configs
    
    def extract_single_config(self, brain_name):
        """Extract configuration for a single brain"""
        config = {
            "name": brain_name,
            "extracted_date": datetime.now().isoformat(),
            "bounty_system": {},
            "equipment": {},
            "appearance": {},
            "derived_traits": {}
        }
        
        print("🏆 BOUNTY SYSTEM VALUES:")
        print("Look for the bounty/reward sliders in the screenshot")
        
        bounties = [
            ("damage_enemy_statue", "Damage Enemy Statue"),
            ("damage_enemy_unit", "Damage Enemy Unit"), 
            ("kill_enemy_statue", "Kill Enemy Statue"),
            ("kill_enemy_unit", "Kill Enemy Unit"),
            ("heal_teammate", "Heal Teammate"),
            ("time_territory", "Time in Territory"),
            ("damage_taken", "Damage Taken (usually negative)"),
            ("team_spirit", "Team Spirit (0.0-1.0)")
        ]
        
        for key, description in bounties:
            value = input(f"{description}: ").strip()
            if value:
                try:
                    config["bounty_system"][key] = float(value)
                except ValueError:
                    config["bounty_system"][key] = value
        
        print("\n⚔️ EQUIPMENT LOADOUT:")
        equipment_slots = [
            ("arms", "Arms Slot (weapon)"),
            ("tail", "Tail Slot (attachment)"),
            ("misc", "Misc Slot (special item)")
        ]
        
        for key, description in equipment_slots:
            value = input(f"{description}: ").strip()
            config["equipment"][key] = value if value else "None"
        
        print("\n🎭 APPEARANCE:")
        appearance_items = [
            ("primary_color", "Primary Color (hex like #ff0000)"),
            ("secondary_color", "Secondary Color"), 
            ("ears", "Ears (1-4)"),
            ("eyes", "Eyes (1-5)"),
            ("spikes", "Back Spikes (1-7)")
        ]
        
        for key, description in appearance_items:
            value = input(f"{description}: ").strip()
            if value:
                config["appearance"][key] = value
        
        # Derive behavioral traits from bounty system
        config["derived_traits"] = self.derive_traits_from_bounties(config["bounty_system"])
        
        return config
    
    def derive_traits_from_bounties(self, bounties):
        """Derive behavioral traits from bounty system settings"""
        traits = {}
        
        # Calculate aggression from kill/damage bounties
        enemy_damage = bounties.get("damage_enemy_unit", 0)
        enemy_kills = bounties.get("kill_enemy_unit", 0)
        statue_damage = bounties.get("damage_enemy_statue", 0)
        
        aggression_score = (enemy_damage + enemy_kills + statue_damage) / 3.0
        traits["aggression"] = min(max(aggression_score / 2.0, 0.1), 1.0)  # Normalize to 0.1-1.0
        
        # Calculate team focus from heal bounties and team spirit
        heal_bonus = bounties.get("heal_teammate", 0)
        team_spirit = bounties.get("team_spirit", 0)
        
        team_focus = (heal_bonus * 2 + team_spirit) / 2.0
        traits["team_focus"] = min(max(team_focus, 0.1), 1.0)
        
        # Calculate risk tolerance from damage taken penalty
        damage_penalty = abs(bounties.get("damage_taken", 0))
        if damage_penalty > 0:
            # Higher penalty = lower risk tolerance
            traits["risk_tolerance"] = max(0.1, 1.0 - (damage_penalty / 2.0))
        else:
            traits["risk_tolerance"] = 0.7  # Default
        
        # Territory behavior
        territory_bonus = bounties.get("time_territory", 0)
        if territory_bonus > 0:
            traits["territorial"] = True
            traits["preferred_range"] = "medium"  # Stay in territory
        else:
            traits["territorial"] = False
            traits["preferred_range"] = "close"   # More aggressive
        
        return traits
    
    def equipment_to_derk_gym(self, equipment):
        """Convert Steam equipment to Derk Gym format"""
        # Mapping from Steam names to Derk Gym names
        weapon_mapping = {
            "talons": "Talons",
            "blood claws": "BloodClaws", 
            "cleavers": "Cleavers",
            "cripplers": "Cripplers",
            "pistol": "Pistol",
            "magnum": "Magnum",
            "blaster": "Blaster",
            "healing gland": "HealingGland",
            "vampire gland": "VampireGland",
            "paralyzing dart": "ParalyzingDart",
            "frog legs": "FrogLegs",
            "iron bubblegum": "IronBubblegum",
            "helium bubblegum": "HeliumBubblegum",
            "shell": "Shell",
            "trombone": "Trombone"
        }
        
        derk_equipment = []
        
        # Arms slot (index 0)
        arms = equipment.get("arms", "").lower()
        derk_equipment.append(weapon_mapping.get(arms, None))
        
        # Tail slot (index 1) 
        tail = equipment.get("tail", "").lower()
        derk_equipment.append(weapon_mapping.get(tail, None))
        
        # Misc slot (index 2)
        misc = equipment.get("misc", "").lower()
        derk_equipment.append(weapon_mapping.get(misc, None))
        
        return derk_equipment
    
    def bounties_to_reward_function(self, bounties):
        """Convert Steam bounties to Derk Gym reward function"""
        # Map Steam bounty names to Derk Gym reward function keys
        reward_function = {}
        
        mapping = {
            "damage_enemy_statue": "damageEnemyStatue",
            "damage_enemy_unit": "damageEnemyUnit",
            "kill_enemy_statue": "killEnemyStatue", 
            "kill_enemy_unit": "killEnemyUnit",
            "heal_teammate": "healTeammate1",  # Use teammate1 as primary
            "damage_taken": "damageTaken",
            "team_spirit": "teamSpirit"
        }
        
        for steam_key, derk_key in mapping.items():
            if steam_key in bounties:
                reward_function[derk_key] = bounties[steam_key]
        
        # Handle territory time - map to appropriate Derk Gym keys
        if "time_territory" in bounties:
            territory_value = bounties["time_territory"]
            if territory_value > 0:
                reward_function["timeSpentHomeTerritory"] = territory_value
            else:
                reward_function["timeSpentAwayTerritory"] = abs(territory_value)
        
        return reward_function
    
    def save_extracted_configs(self):
        """Save extracted configurations"""
        filename = "extracted_steam_configs.json"
        
        # Convert to Derk Gym compatible format
        derk_gym_configs = {}
        
        for brain_name, config in self.configs.items():
            derk_config = {
                "name": brain_name,
                "description": f"Extracted from Steam brain: {brain_name}",
                "reward_function": self.bounties_to_reward_function(config["bounty_system"]),
                "equipment_slots": self.equipment_to_derk_gym(config["equipment"]),
                "appearance": config["appearance"],
                "behavioral_traits": config["derived_traits"],
                "original_bounties": config["bounty_system"]
            }
            derk_gym_configs[brain_name] = derk_config
        
        # Save both original and converted formats
        with open("original_steam_configs.json", 'w') as f:
            json.dump(self.configs, f, indent=2)
        
        with open(filename, 'w') as f:
            json.dump(derk_gym_configs, f, indent=2)
        
        print(f"\n✅ Configurations saved to:")
        print(f"   - original_steam_configs.json (raw extraction)")
        print(f"   - {filename} (Derk Gym compatible)")
        
        return derk_gym_configs
    
    def quick_analysis_template(self):
        """Create a quick analysis template for all brains"""
        template = {
            "instructions": "Fill in the values from your screenshots",
            "brains": {}
        }
        
        for brain_name in self.screenshots:
            template["brains"][brain_name] = {
                "bounty_system": {
                    "damage_enemy_statue": "VALUE_FROM_SCREENSHOT",
                    "damage_enemy_unit": "VALUE_FROM_SCREENSHOT",
                    "kill_enemy_statue": "VALUE_FROM_SCREENSHOT", 
                    "kill_enemy_unit": "VALUE_FROM_SCREENSHOT",
                    "heal_teammate": "VALUE_FROM_SCREENSHOT",
                    "time_territory": "VALUE_FROM_SCREENSHOT",
                    "damage_taken": "VALUE_FROM_SCREENSHOT",
                    "team_spirit": "VALUE_FROM_SCREENSHOT"
                },
                "equipment": {
                    "arms": "WEAPON_FROM_SCREENSHOT",
                    "tail": "ATTACHMENT_FROM_SCREENSHOT", 
                    "misc": "ITEM_FROM_SCREENSHOT"
                },
                "appearance": {
                    "primary_color": "COLOR_FROM_SCREENSHOT",
                    "secondary_color": "COLOR_FROM_SCREENSHOT"
                }
            }
        
        with open("steam_extraction_template.json", 'w') as f:
            json.dump(template, f, indent=2)
        
        print("Created steam_extraction_template.json")
        print("You can fill this in manually if you prefer!")

def main():
    extractor = SteamConfigExtractor()
    
    print("🎮 STEAM BRAIN CONFIGURATION EXTRACTOR")
    print("=" * 45)
    print("You have 10 brain configurations to extract:")
    for i, name in enumerate(extractor.screenshots, 1):
        print(f"{i:2d}. {name}")
    print()
    
    while True:
        print("Options:")
        print("1. Show extraction guide")
        print("2. Interactive extraction (guided)")
        print("3. Create template file for manual entry")
        print("4. Load and convert existing template")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == "1":
            extractor.manual_extraction_guide()
            
        elif choice == "2":
            extractor.interactive_extraction()
            
        elif choice == "3":
            extractor.quick_analysis_template()
            
        elif choice == "4":
            if os.path.exists("steam_extraction_template.json"):
                print("Loading template...")
                # You can implement template loading here
                print("Template loading not yet implemented - use option 2 for now")
            else:
                print("No template file found. Create one with option 3 first.")
                
        elif choice == "5":
            break
            
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
