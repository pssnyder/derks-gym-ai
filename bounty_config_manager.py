"""
Bounty Configuration Manager
===========================

Tool to check, verify, and update derkling bounty configurations and loadouts.
"""

import json
import sys
import os
from typing import Dict, Any

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.brain_profiles.peanut_class.nightrider_peanut import NightriderPeanutBrain
from src.brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

class BountyConfigManager:
    """Manage and validate derkling bounty configurations"""
    
    def __init__(self):
        self.derk_gym_rewards = {
            # Standard Derk's Gym reward function parameters
            "damageEnemyStatue": "Reward for damaging enemy statue (per hitpoint)",
            "damageEnemyUnit": "Reward for damaging enemy units (per hitpoint)", 
            "killEnemyStatue": "Reward for killing enemy statue",
            "killEnemyUnit": "Reward for killing enemy units",
            "damageTaken": "Penalty for taking damage (negative value)",
            "healEnemy": "Penalty for healing enemies (negative value)",
            "fallDamageTaken": "Penalty for fall damage (negative value)",
            "friendlyFire": "Penalty for friendly fire damage (negative value)",
            "timeSpentAwayTerritory": "Bonus for staying in enemy territory",
            "teamSpirit": "Team collaboration bonus/penalty",
            "timeScaling": "Time-based scaling factor"
        }
        
        self.equipment_slots = {
            "arms": ["Talons", "BloodClaws", "Cleavers", "Cripplers", "Pistol", "Magnum", "Blaster"],
            "tail": ["IronTail", "HealingTail", "VampireTail"],
            "misc": ["FocusingOrb", "VitalityOrb", "HasteOrb", "ShieldOrb", "AmmoPouch"]
        }
    
    def analyze_current_configs(self):
        """Analyze current brain configurations"""
        print("🔍 BOUNTY CONFIGURATION ANALYSIS")
        print("=" * 45)
        
        # Load brain instances
        nightrider = NightriderPeanutBrain()
        assaulter = TheAssaulterBrain()
        
        # Display configurations
        self._display_brain_config("Nightrider Peanut", nightrider)
        print()
        self._display_brain_config("The Assaulter", assaulter)
        
        # Analyze differences
        print("\n🔬 CONFIGURATION COMPARISON")
        print("=" * 30)
        self._compare_configs(nightrider, assaulter)
        
        # Identify potential issues
        print("\n⚠️ POTENTIAL ISSUES")
        print("=" * 20)
        self._identify_issues(nightrider, assaulter)
    
    def _display_brain_config(self, name, brain):
        """Display a brain's configuration in detail"""
        config = brain.get_derk_gym_config()
        
        print(f"🧠 {name}")
        print("-" * (len(name) + 3))
        
        # Equipment
        print(f"Equipment:")
        for i, slot in enumerate(config['slots']):
            slot_name = ["Arms", "Tail", "Misc"][i]
            print(f"  {slot_name}: {slot}")
        
        # Colors
        print(f"Colors: {config['primaryColor']} / {config['secondaryColor']}")
        
        # Reward function
        print(f"Bounties:")
        for key, value in config['rewardFunction'].items():
            description = self.derk_gym_rewards.get(key, "Unknown reward type")
            print(f"  {key}: {value:6.2f} - {description}")
    
    def _compare_configs(self, brain1, brain2):
        """Compare two brain configurations"""
        config1 = brain1.get_derk_gym_config()
        config2 = brain2.get_derk_gym_config()
        
        print(f"Equipment Comparison:")
        for i, (slot1, slot2) in enumerate(zip(config1['slots'], config2['slots'])):
            slot_name = ["Arms", "Tail", "Misc"][i]
            print(f"  {slot_name}: {brain1.name} = {slot1}, {brain2.name} = {slot2}")
        
        print(f"\nBounty Differences:")
        all_keys = set(config1['rewardFunction'].keys()) | set(config2['rewardFunction'].keys())
        
        for key in sorted(all_keys):
            val1 = config1['rewardFunction'].get(key, 0)
            val2 = config2['rewardFunction'].get(key, 0)
            diff = abs(val1 - val2)
            
            if diff > 0.01:  # Significant difference
                print(f"  {key}:")
                print(f"    {brain1.name}: {val1:6.2f}")
                print(f"    {brain2.name}: {val2:6.2f}")
                print(f"    Difference: {diff:6.2f}")
    
    def _identify_issues(self, nightrider, assaulter):
        """Identify potential configuration issues"""
        config_nr = nightrider.get_derk_gym_config()
        config_as = assaulter.get_derk_gym_config()
        
        issues = []
        
        # Check for unknown equipment
        for brain_name, config in [("Nightrider", config_nr), ("Assaulter", config_as)]:
            for i, slot in enumerate(config['slots']):
                if slot == "Unknown" or slot is None:
                    slot_name = ["Arms", "Tail", "Misc"][i]
                    issues.append(f"{brain_name} has unknown {slot_name} equipment")
        
        # Check for zero rewards
        for brain_name, config in [("Nightrider", config_nr), ("Assaulter", config_as)]:
            zero_rewards = [k for k, v in config['rewardFunction'].items() if v == 0]
            if zero_rewards:
                issues.append(f"{brain_name} has zero rewards for: {', '.join(zero_rewards)}")
        
        # Check for very high values (potential extraction errors)
        for brain_name, config in [("Nightrider", config_nr), ("Assaulter", config_as)]:
            high_rewards = [f"{k}={v}" for k, v in config['rewardFunction'].items() if abs(v) > 5]
            if high_rewards:
                issues.append(f"{brain_name} has very high bounties: {', '.join(high_rewards)}")
        
        # Check for missing common rewards
        common_rewards = ["killEnemyUnit", "damageEnemyUnit", "damageTaken"]
        for brain_name, config in [("Nightrider", config_nr), ("Assaulter", config_as)]:
            missing = [k for k in common_rewards if k not in config['rewardFunction']]
            if missing:
                issues.append(f"{brain_name} missing common rewards: {', '.join(missing)}")
        
        if issues:
            for issue in issues:
                print(f"  ⚠️ {issue}")
        else:
            print(f"  ✅ No obvious issues detected")
    
    def suggest_improvements(self):
        """Suggest configuration improvements"""
        print(f"\n💡 IMPROVEMENT SUGGESTIONS")
        print("=" * 30)
        
        print("1. Nightrider Peanut Issues:")
        print("   • Equipment shows 'Unknown' - needs proper loadout")
        print("   • Very high killEnemyUnit (10.0) may be extraction error")
        print("   • Consider reducing to 2.0-3.0 for balance")
        print("   • Missing timeSpentAwayTerritory (mobility bonus)")
        
        print("\n2. The Assaulter Issues:")
        print("   • Only has Talons equipped - consider tail/misc items")
        print("   • Missing healEnemy penalty")
        print("   • timeSpentAwayTerritory seems low (0.3)")
        print("   • Consider adding mobility equipment")
        
        print("\n3. General Recommendations:")
        print("   • Test with more balanced bounty values (0.1-2.0 range)")
        print("   • Add equipment for strategic diversity")
        print("   • Ensure both have similar reward function coverage")
        print("   • Consider team spirit balance (0.1 vs 0.6 is very different)")
    
    def create_config_templates(self):
        """Create improved configuration templates"""
        print(f"\n📝 IMPROVED CONFIGURATION TEMPLATES")
        print("=" * 40)
        
        # Nightrider improved config
        nightrider_improved = {
            "name": "Nightrider Peanut (Improved)",
            "slots": ["Magnum", "HealingTail", "FocusingOrb"],  # Balanced ranged fighter
            "rewardFunction": {
                "damageEnemyStatue": 0.5,
                "damageEnemyUnit": 1.0,
                "killEnemyStatue": 2.0,
                "killEnemyUnit": 3.0,           # Reduced from 10.0
                "damageTaken": -0.3,
                "healEnemy": -0.5,
                "fallDamageTaken": -1.0,
                "teamSpirit": 0.2,              # Slightly more team-oriented
                "timeScaling": 0.0
            },
            "primaryColor": "#4B0082",
            "secondaryColor": "#000000"
        }
        
        # Assaulter improved config  
        assaulter_improved = {
            "name": "The Assaulter (Improved)",
            "slots": ["Talons", "IronTail", "HasteOrb"],       # Melee mobility build
            "rewardFunction": {
                "damageEnemyStatue": 0.6,
                "damageEnemyUnit": 0.8,
                "killEnemyStatue": 2.0,
                "killEnemyUnit": 2.5,
                "timeSpentAwayTerritory": 0.8,  # Increased territory bonus
                "damageTaken": -0.25,
                "friendlyFire": -0.8,
                "fallDamageTaken": -1.0,
                "healEnemy": -0.5,              # Added penalty
                "teamSpirit": 0.4,              # Balanced team spirit
                "timeScaling": 0.0
            },
            "primaryColor": "#DC143C", 
            "secondaryColor": "#000000"
        }
        
        print("🌙 Nightrider Peanut (Improved):")
        self._print_config_template(nightrider_improved)
        
        print("\n⚔️ The Assaulter (Improved):")
        self._print_config_template(assaulter_improved)
        
        # Save templates
        self._save_config_templates(nightrider_improved, assaulter_improved)
    
    def _print_config_template(self, config):
        """Print a configuration template"""
        print(f"Equipment: {config['slots']}")
        print(f"Colors: {config['primaryColor']} / {config['secondaryColor']}")
        print("Bounties:")
        for key, value in config['rewardFunction'].items():
            print(f"  {key}: {value}")
    
    def _save_config_templates(self, nightrider_config, assaulter_config):
        """Save configuration templates to file"""
        templates = {
            "nightrider_improved": nightrider_config,
            "assaulter_improved": assaulter_config,
            "timestamp": "2025-09-01",
            "notes": "Improved configurations based on analysis"
        }
        
        filename = "src/config_templates.json"
        try:
            with open(filename, 'w') as f:
                json.dump(templates, f, indent=2)
            print(f"\n💾 Configuration templates saved to: {filename}")
        except Exception as e:
            print(f"⚠️ Failed to save templates: {e}")
    
    def interactive_config_editor(self):
        """Interactive configuration editor"""
        print(f"\n🛠️ INTERACTIVE CONFIGURATION EDITOR")
        print("=" * 40)
        print("This feature would allow you to:")
        print("• Edit equipment loadouts")
        print("• Adjust bounty values") 
        print("• Test different color schemes")
        print("• Preview changes before applying")
        print("• Generate updated brain files")
        print("\nWould you like me to implement this feature?")

def main():
    """Main function"""
    manager = BountyConfigManager()
    
    # Run analysis
    manager.analyze_current_configs()
    manager.suggest_improvements()
    manager.create_config_templates()
    manager.interactive_config_editor()
    
    print(f"\n✅ Bounty configuration analysis complete!")
    print(f"🎯 Next steps: Update brain files with improved configurations")

if __name__ == "__main__":
    main()
