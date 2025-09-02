"""
Derk's Gym AI Web Dashboard
==========================

Flask web application for visualizing derkling teams, relationships, and battle metrics.
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import sys
from datetime import datetime

# Add src to path for imports
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src'))

app = Flask(__name__)

# Initialize brain classes as None
NightriderPeanutBrain = None
AngrrryBrain = None
SafeTPeanutBrain = None
SpicyPeanutBrain = None
PoonutBrain = None
TheAssaulterBrain = None
TheEngineerBrain = None
ThePeacemakerBrain = None
ClintEastwoodBrain = None
FrankBrain = None

# Import brain classes for data extraction
try:
    from brain_profiles.peanut_class.nightrider_peanut_correct import NightriderPeanutBrain
    from brain_profiles.testing_class.angrrry_correct import AngrrryBrain
    from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain
    from brain_profiles.peanut_class.spicy_peanut import SpicyPeanutBrain
    from brain_profiles.peanut_class.poonut import PoonutBrain
    from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain
    from brain_profiles.testing_class.the_engineer import TheEngineerBrain
    from brain_profiles.testing_class.the_peacemaker import ThePeacemakerBrain
    from brain_profiles.lone_wolf_class.clint_eastwood import ClintEastwoodBrain
    from brain_profiles.special.frank import FrankBrain
    print("✅ Successfully imported all brain classes")
except ImportError as e:
    print(f"Warning: Could not import some brain classes: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    # Create fallback mock data
    print("Using fallback mock data for demonstration")

def get_derkling_data():
    """Extract data from all brain classes"""
    derklings = {}
    
    # Define brain classes and their metadata
    brain_classes = {
        'nightrider': {
            'class': NightriderPeanutBrain,
            'team': 'peanuts',
            'role': 'Solo Hunter',
            'specialty': 'High-value target elimination, solo or team capable'
        },
        'angrrry': {
            'class': AngrrryBrain,
            'team': 'peanuts',
            'role': 'Versatile Fighter',
            'specialty': 'Solo or team combat, balanced assault approach'
        },
        'safe_t': {
            'class': SafeTPeanutBrain,
            'team': 'peanuts',
            'role': 'Defensive Support',
            'specialty': 'Statue protection, bonds with Spicy for balance'
        },
        'spicy': {
            'class': SpicyPeanutBrain,
            'team': 'peanuts',
            'role': 'Aggressive Fighter',
            'specialty': 'High-risk combat, bonds with Safe T for balance'
        },
        'poonut': {
            'class': PoonutBrain,
            'team': 'peanuts',
            'role': 'Decoy Fighter',
            'specialty': 'Distraction tactics for 3v3 with Safe T and Spicy'
        },
        'the_assaulter': {
            'class': TheAssaulterBrain,
            'team': 'testing',
            'role': 'Pure Assault',
            'specialty': 'Enemy elimination focus strategy'
        },
        'the_engineer': {
            'class': TheEngineerBrain,
            'team': 'testing',
            'role': 'Territory Control',
            'specialty': 'Statue damage and positioning strategy'
        },
        'the_peacemaker': {
            'class': ThePeacemakerBrain,
            'team': 'testing',
            'role': 'Support Control',
            'specialty': 'Team healing and balance strategy'
        },
        'clint_eastwood': {
            'class': ClintEastwoodBrain,
            'team': 'lone_wolf',
            'role': 'Lone Wolf',
            'specialty': 'Independent combat specialist'
        },
        'frank': {
            'class': FrankBrain,
            'team': 'special',
            'role': 'Minimalist',
            'specialty': 'Victory-focused strategy'
        }
    }
    
    for name, info in brain_classes.items():
        try:
            if info['class'] is None:
                # Create fallback data if brain class not available
                derklings[name] = create_fallback_derkling_data(name, info)
                continue
                
            brain = info['class']()
            config = brain.get_derk_gym_config()
            
            derklings[name] = {
                'name': brain.name,
                'display_name': getattr(brain, 'display_name', brain.name),
                'team': info['team'],
                'role': info['role'],
                'specialty': info['specialty'],
                'equipment': config['slots'],
                'bounties': config['rewardFunction'],
                'colors': {
                    'primary': config['primaryColor'],
                    'secondary': config['secondaryColor']
                },
                'team_spirit': config['rewardFunction'].get('teamSpirit', 0.5),
                'time_scaling': config['rewardFunction'].get('timeScaling', 0.0)
            }
        except Exception as e:
            print(f"Error loading {name}: {e}")
            derklings[name] = create_fallback_derkling_data(name, info)
    
    return derklings

def create_fallback_derkling_data(name, info):
    """Create fallback data when brain class is not available"""
    team_colors = {
        'peanuts': {'primary': '#8B4513', 'secondary': '#D2B48C'},
        'testing': {'primary': '#4169E1', 'secondary': '#FFD700'},
        'special': {'primary': '#8B0000', 'secondary': '#FF6347'},
        'lone_wolf': {'primary': '#2F4F4F', 'secondary': '#778899'}
    }
    
    return {
        'name': name.replace('_', ' ').title(),
        'display_name': name.replace('_', ' ').title(),
        'team': info['team'],
        'role': info['role'],
        'specialty': info['specialty'],
        'equipment': {
            'primary': 'Unknown',
            'secondary': 'Unknown',
            'tail': 'Unknown',
            'misc': 'Unknown'
        },
        'bounties': {
            'killEnemyUnit': 100,
            'killEnemyStatue': 50,
            'damageEnemyUnit': 2,
            'healTeammate1': 10,
            'victory': 100,
            'teamSpirit': 0.5,
            'timeScaling': 0.0
        },
        'colors': team_colors.get(info['team'], {'primary': '#666666', 'secondary': '#999999'}),
        'team_spirit': 0.5,
        'time_scaling': 0.0
    }

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/derklings')
def api_derklings():
    """API endpoint for derkling data"""
    return jsonify(get_derkling_data())

@app.route('/api/teams')
def api_teams():
    """API endpoint for team organization"""
    derklings = get_derkling_data()
    teams = {}
    
    for name, data in derklings.items():
        team = data['team']
        if team not in teams:
            teams[team] = []
        teams[team].append({
            'name': name,
            'display_name': data['display_name'],
            'role': data['role'],
            'colors': data['colors']
        })
    
    return jsonify(teams)

@app.route('/api/relationships')
def api_relationships():
    """API endpoint for derkling relationships and compatibility"""
    # Updated relationships based on user specifications
    relationships = {
        'peanuts': {
            'core_team': ['safe_t', 'spicy', 'poonut'],  # 3v3 core with decoy
            'bonds': {
                'safe_t': ['spicy'],           # Bonded pair - balance each other
                'spicy': ['safe_t'],           # Bonded pair - balance each other
                'nightrider': ['angrrry'],     # Similar fighters, solo/team capable
                'angrrry': ['nightrider'],     # Similar fighters, solo/team capable
                'poonut': ['safe_t', 'spicy'] # Decoy works with bonded pair
            },
            'strategies': {
                'balanced_3v3': ['safe_t', 'spicy', 'poonut'],        # Core 3v3 with decoy
                'solo_hunters': ['nightrider', 'angrrry'],            # Flexible solo/team
                'defensive': ['safe_t', 'poonut', 'nightrider'],      # Protection focus
                'aggressive': ['spicy', 'angrrry', 'nightrider'],     # Assault focus
                'full_team': ['safe_t', 'spicy', 'nightrider', 'angrrry', 'poonut']  # All peanuts
            }
        },
        'testing': {
            'core_team': ['the_assaulter', 'the_engineer', 'the_peacemaker'],
            'bonds': {
                'the_assaulter': ['the_engineer'],    # Assault + Territory
                'the_engineer': ['the_peacemaker'],   # Territory + Support
                'the_peacemaker': ['the_assaulter']   # Support + Assault
            },
            'strategies': {
                'aggressive': ['the_assaulter', 'the_engineer', 'the_peacemaker'],
                'control': ['the_engineer', 'the_peacemaker', 'the_assaulter'],
                'support': ['the_peacemaker', 'the_assaulter', 'the_engineer']
            }
        },
        'lone_wolf': {
            'core_team': ['clint_eastwood'],
            'bonds': {},  # Lone wolves don't have bonds
            'strategies': {
                'independent': ['clint_eastwood']
            }
        },
        'special_ops': {
            'core_team': ['frank', 'number_eleven'],  # Frank AND Number Eleven
            'bonds': {
                'frank': ['number_eleven'],      # Special operations synergy
                'number_eleven': ['frank']       # Experimental + Minimalist
            },
            'strategies': {
                'experimental': ['number_eleven', 'frank'],     # Cutting edge tactics
                'minimalist': ['frank', 'number_eleven'],       # Victory-focused
                'classified': ['number_eleven']                 # Solo experimental
            },
            'experimental': ['number_eleven']  # When implemented
        }
    }
    
    return jsonify(relationships)

@app.route('/api/battle_history')
def api_battle_history():
    """API endpoint for battle results"""
    # Load battle results from JSON files
    results = []
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    
    if os.path.exists(results_dir):
        for filename in os.listdir(results_dir):
            if filename.endswith('.json') and 'battle_results' in filename:
                try:
                    with open(os.path.join(results_dir, filename), 'r') as f:
                        battle_data = json.load(f)
                        results.append(battle_data)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    return jsonify(results)

@app.route('/derkling/<name>')
def derkling_profile(name):
    """Individual derkling profile page"""
    derklings = get_derkling_data()
    if name not in derklings:
        return "Derkling not found", 404
    
    return render_template('derkling_profile.html', 
                         derkling=derklings[name], 
                         name=name)

@app.route('/teams')
def teams_page():
    """Teams overview page"""
    return render_template('teams.html')

@app.route('/number_eleven')
def number_eleven_page():
    """Special Project Number Eleven page"""
    return render_template('number_eleven.html')

@app.route('/battles')
def battles_page():
    """Battle metrics and history page"""
    return render_template('battles.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
