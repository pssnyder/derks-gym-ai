"""
Steam Brain to Derk Gym Migration Tool
====================================

This tool helps you systematically migrate your successful strategies 
from the Steam version to the RL environment.
"""

import json
import os
from datetime import datetime

class BrainMigrationTool:
    """Tool to help migrate strategies from Steam game to Derk Gym"""
    
    def __init__(self):
        self.strategies_file = "steam_strategies.json"
        self.load_strategies()
    
    def load_strategies(self):
        """Load existing strategy documentation"""
        if os.path.exists(self.strategies_file):
            with open(self.strategies_file, 'r') as f:
                self.strategies = json.load(f)
        else:
            self.strategies = {
                "created": datetime.now().isoformat(),
                "strategies": {}
            }
    
    def save_strategies(self):
        """Save strategy documentation"""
        self.strategies["last_updated"] = datetime.now().isoformat()
        with open(self.strategies_file, 'w') as f:
            json.dump(self.strategies, f, indent=2)
    
    def document_steam_brain(self, brain_name):
        """Interactive tool to document a Steam game brain"""
        print(f"\n🧠 Documenting Steam Brain: {brain_name}")
        print("=" * 50)
        
        strategy = {
            "name": brain_name,
            "documented_date": datetime.now().isoformat(),
            "combat": {},
            "team_coordination": {},
            "map_control": {},
            "equipment": {},
            "personality": {}
        }
        
        # Combat Strategy
        print("\n📋 COMBAT STRATEGY")
        print("Describe how this brain handled combat:")
        
        strategy["combat"]["target_priority"] = input("Target priority (enemies/statue/support teammates): ")
        strategy["combat"]["engagement_range"] = input("Preferred engagement range (close/medium/long): ")
        strategy["combat"]["retreat_condition"] = input("When did it retreat? (low health/outnumbered/never): ")
        strategy["combat"]["aggression_level"] = input("Aggression level (1-10): ")
        
        # Team Coordination
        print("\n🤝 TEAM COORDINATION")
        strategy["team_coordination"]["formation"] = input("Formation preference (tight group/spread out/flexible): ")
        strategy["team_coordination"]["support_behavior"] = input("How did it support teammates? ")
        strategy["team_coordination"]["role"] = input("Primary role (tank/damage/support/balanced): ")
        
        # Map Control
        print("\n🗺️ MAP CONTROL")
        strategy["map_control"]["territory_focus"] = input("Territory control style (defensive/aggressive/balanced): ")
        strategy["map_control"]["base_behavior"] = input("Base behavior (always defend/sometimes attack/always attack): ")
        
        # Equipment
        print("\n⚔️ EQUIPMENT PREFERENCES")
        strategy["equipment"]["weapon_preference"] = input("Weapon preference (melee/ranged/balanced): ")
        strategy["equipment"]["favorite_weapons"] = input("Favorite specific weapons (comma separated): ").split(',')
        strategy["equipment"]["ability_usage"] = input("How did it use abilities? ")
        
        # Personality Traits
        print("\n🎭 PERSONALITY TRAITS")
        strategy["personality"]["risk_tolerance"] = input("Risk tolerance (cautious/moderate/reckless): ")
        strategy["personality"]["decision_speed"] = input("Decision making (quick/calculated/slow): ")
        strategy["personality"]["adaptability"] = input("Adaptability (rigid/flexible/very adaptive): ")
        
        # Success Metrics
        print("\n📊 SUCCESS METRICS")
        strategy["success"] = {
            "win_rate": input("Approximate win rate (%): "),
            "best_scenarios": input("What scenarios did it excel in? "),
            "weaknesses": input("What were its main weaknesses? "),
            "notes": input("Additional notes: ")
        }
        
        self.strategies["strategies"][brain_name] = strategy
        self.save_strategies()
        
        print(f"\n✅ Brain '{brain_name}' documented successfully!")
        return strategy
    
    def list_documented_brains(self):
        """List all documented brains"""
        if not self.strategies["strategies"]:
            print("No brains documented yet. Use document_steam_brain() to add one.")
            return
        
        print("\n🧠 DOCUMENTED BRAINS")
        print("=" * 30)
        for name, strategy in self.strategies["strategies"].items():
            print(f"• {name} - {strategy['team_coordination']['role']} ({strategy['combat']['aggression_level']}/10 aggression)")
    
    def generate_rule_based_code(self, brain_name):
        """Generate rule-based code for a documented brain"""
        if brain_name not in self.strategies["strategies"]:
            print(f"Brain '{brain_name}' not found. Document it first.")
            return None
        
        strategy = self.strategies["strategies"][brain_name]
        
        # Generate code based on documented strategy
        code = f'''
class {brain_name.replace(" ", "")}Brain(RuleBasedBrain):
    """
    Recreated from Steam game brain: {brain_name}
    Role: {strategy["team_coordination"]["role"]}
    Aggression: {strategy["combat"]["aggression_level"]}/10
    """
    
    def __init__(self):
        # Personality traits derived from Steam brain documentation
        traits = {{
            'aggression': {float(strategy["combat"]["aggression_level"]) / 10.0},
            'team_focus': {self._role_to_team_focus(strategy["team_coordination"]["role"])},
            'risk_tolerance': {self._risk_to_float(strategy["personality"]["risk_tolerance"])},
            'weapon_preference': '{strategy["equipment"]["weapon_preference"]}'
        }}
        super().__init__("{brain_name}", traits)
    
    def _make_strategic_decision(self, hp, closest_enemy, has_focus, focus_hp, 
                               has_ranged, has_melee, friend_distances):
        """
        Strategy based on documented Steam brain behavior:
        - Target Priority: {strategy["combat"]["target_priority"]}
        - Engagement Range: {strategy["combat"]["engagement_range"]}
        - Formation: {strategy["team_coordination"]["formation"]}
        """
        
        health_ratio = hp / 100.0
        move_x = 0.0
        rotate = 0.0
        chase_focus = 0.0
        cast_slot = 0
        focus_target = 0
        
        # Implement combat strategy: {strategy["combat"]["target_priority"]}
        {self._generate_combat_logic(strategy)}
        
        # Implement team coordination: {strategy["team_coordination"]["formation"]}
        {self._generate_team_logic(strategy)}
        
        # Implement equipment preferences: {strategy["equipment"]["weapon_preference"]}
        {self._generate_equipment_logic(strategy)}
        
        return (move_x, rotate, chase_focus, cast_slot, focus_target)
'''
        
        # Save generated code
        filename = f"{brain_name.replace(' ', '_').lower()}_brain.py"
        with open(filename, 'w') as f:
            f.write(code)
        
        print(f"Generated code saved to: {filename}")
        return code
    
    def _role_to_team_focus(self, role):
        """Convert role to team focus value"""
        role_map = {
            "tank": 0.8,
            "support": 0.9,
            "damage": 0.4,
            "balanced": 0.6
        }
        return role_map.get(role.lower(), 0.6)
    
    def _risk_to_float(self, risk):
        """Convert risk tolerance to float"""
        risk_map = {
            "cautious": 0.2,
            "moderate": 0.5,
            "reckless": 0.9
        }
        return risk_map.get(risk.lower(), 0.5)
    
    def _generate_combat_logic(self, strategy):
        """Generate combat logic based on strategy"""
        aggression = float(strategy["combat"]["aggression_level"]) / 10.0
        
        if aggression > 0.7:
            return '''
        # High aggression - always engage when enemies are near
        if closest_enemy < 40:
            chase_focus = 1.0
            focus_target = 5  # Focus on nearest enemy
            if closest_enemy < 20 and has_melee:
                cast_slot = 1
            elif has_ranged:
                cast_slot = 2'''
        elif aggression < 0.4:
            return '''
        # Low aggression - defensive positioning
        if closest_enemy < 25:
            move_x = -0.3  # Retreat slightly
            if has_ranged and closest_enemy > 15:
                cast_slot = 2
            focus_target = 2  # Focus on teammate for support'''
        else:
            return '''
        # Moderate aggression - tactical engagement
        if closest_enemy < 30 and health_ratio > 0.4:
            chase_focus = 0.7
            focus_target = 5
            if has_melee and closest_enemy < 15:
                cast_slot = 1'''
    
    def _generate_team_logic(self, strategy):
        """Generate team coordination logic"""
        formation = strategy["team_coordination"]["formation"].lower()
        
        if "tight" in formation:
            return '''
        # Tight formation - stay close to team
        avg_friend_distance = np.mean([d for d in friend_distances if d > 0] or [0])
        if avg_friend_distance > 20:
            chase_focus = 0.5
            focus_target = 2  # Move toward teammate'''
        elif "spread" in formation:
            return '''
        # Spread formation - maintain distance from team
        avg_friend_distance = np.mean([d for d in friend_distances if d > 0] or [0])
        if avg_friend_distance < 10:
            move_x = -0.2  # Create some distance'''
        else:
            return '''
        # Flexible formation - adapt based on situation
        avg_friend_distance = np.mean([d for d in friend_distances if d > 0] or [0])
        if avg_friend_distance > 30:
            focus_target = 2  # Too far, move closer
        elif avg_friend_distance < 8:
            move_x = 0.1   # Too close, spread out slightly'''
    
    def _generate_equipment_logic(self, strategy):
        """Generate equipment usage logic"""
        weapon_pref = strategy["equipment"]["weapon_preference"].lower()
        
        if weapon_pref == "melee":
            return '''
        # Melee preference - get close for melee attacks
        if has_melee and closest_enemy < 25:
            chase_focus = 0.8
            cast_slot = 1'''
        elif weapon_pref == "ranged":
            return '''
        # Ranged preference - maintain distance
        if has_ranged and closest_enemy < 35:
            if closest_enemy > 15:
                cast_slot = 2
            else:
                move_x = -0.4  # Back away if too close'''
        else:
            return '''
        # Balanced approach - use best weapon for situation
        if closest_enemy < 15 and has_melee:
            cast_slot = 1
        elif closest_enemy < 35 and has_ranged:
            cast_slot = 2'''

def main():
    """Main migration workflow"""
    tool = BrainMigrationTool()
    
    print("🎮 Steam Brain to Derk Gym Migration Tool")
    print("=" * 45)
    
    while True:
        print("\nOptions:")
        print("1. Document a Steam brain")
        print("2. List documented brains") 
        print("3. Generate code for a brain")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            brain_name = input("Enter brain name: ").strip()
            tool.document_steam_brain(brain_name)
            
        elif choice == "2":
            tool.list_documented_brains()
            
        elif choice == "3":
            tool.list_documented_brains()
            brain_name = input("Enter brain name to generate code for: ").strip()
            tool.generate_rule_based_code(brain_name)
            
        elif choice == "4":
            print("Migration tool closed.")
            break
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
