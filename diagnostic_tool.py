"""
Detailed Action & Observation Diagnostic
=======================================

Deep dive into what the brains are actually seeing and doing.
"""

import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys
from src.brain_profiles.peanut_class.nightrider_peanut_updated import NightriderPeanutBrain
from src.brain_profiles.testing_class.the_assaulter_updated import TheAssaulterBrain

class DetailedDiagnostic:
    """Detailed diagnostic of brain behavior"""
    
    def __init__(self):
        self.nightrider = NightriderPeanutBrain()
        self.assaulter = TheAssaulterBrain()
        self.env = None
        
    def diagnose_observations(self):
        """Analyze what the brains are seeing"""
        print("🔍 OBSERVATION ANALYSIS")
        print("=" * 25)
        
        self.env = DerkEnv(n_arenas=1, turbo_mode=True)
        observation_n = self.env.reset()
        
        print(f"Total agents: {len(observation_n)}")
        print(f"Observation shape: {np.array(observation_n[0]).shape}")
        
        # Analyze first agent (Nightrider)
        print(f"\n🌙 Nightrider Agent 0 Observations:")
        self._analyze_single_observation(observation_n[0], "Nightrider")
        
        # Analyze fourth agent (Assaulter)  
        print(f"\n⚔️ Assaulter Agent 3 Observations:")
        self._analyze_single_observation(observation_n[3], "Assaulter")
        
        self.env.close()
    
    def _analyze_single_observation(self, obs, brain_name):
        """Analyze a single agent's observations"""
        print(f"Health: {obs[ObservationKeys.Hitpoints.value]:.3f}")
        print(f"Has Focus: {obs[ObservationKeys.HasFocus.value]:.3f}")
        
        # Enemy distances
        enemy_dists = [
            obs[ObservationKeys.Enemy1Distance.value],
            obs[ObservationKeys.Enemy2Distance.value],
            obs[ObservationKeys.Enemy3Distance.value]
        ]
        print(f"Enemy distances: {[f'{d:.3f}' for d in enemy_dists]}")
        
        # Friend distances
        friend_dists = [
            obs[ObservationKeys.Friend1Distance.value],
            obs[ObservationKeys.Friend2Distance.value]
        ]
        print(f"Friend distances: {[f'{d:.3f}' for d in friend_dists]}")
        
        # Weapons
        weapons = {
            "Talons": obs[ObservationKeys.HasTalons.value],
            "Magnum": obs[ObservationKeys.HasMagnum.value],
            "Pistol": obs[ObservationKeys.HasPistol.value],
            "BloodClaws": obs[ObservationKeys.HasBloodClaws.value],
            "Blaster": obs[ObservationKeys.HasBlaster.value]
        }
        active_weapons = [k for k, v in weapons.items() if v > 0.5]
        print(f"Active weapons: {active_weapons}")
        
        # Statue distance
        statue_dist = obs[ObservationKeys.EnemyStatueDistance.value]
        print(f"Enemy statue distance: {statue_dist:.3f}")
    
    def diagnose_actions(self):
        """Analyze what actions the brains are generating"""
        print(f"\n🎮 ACTION ANALYSIS")
        print("=" * 20)
        
        self.env = DerkEnv(n_arenas=1, turbo_mode=True)
        observation_n = self.env.reset()
        
        # Test multiple steps to see action patterns
        for step in range(10):
            print(f"\nStep {step}:")
            
            # Nightrider actions
            nightrider_actions = []
            for i in range(3):
                action = self.nightrider.get_action(observation_n[i])
                nightrider_actions.append(action)
                if i == 0:  # Just show first agent
                    print(f"  🌙 Nightrider: move={action[0]:.2f}, rotate={action[1]:.2f}, chase={action[2]:.2f}, cast={action[3]}, focus={action[4]}")
            
            # Assaulter actions
            assaulter_actions = []
            for i in range(3, 6):
                action = self.assaulter.get_action(observation_n[i])
                assaulter_actions.append(action)
                if i == 3:  # Just show first agent
                    print(f"  ⚔️ Assaulter: move={action[0]:.2f}, rotate={action[1]:.2f}, chase={action[2]:.2f}, cast={action[3]}, focus={action[4]}")
            
            # Combine all actions
            all_actions = nightrider_actions + assaulter_actions
            
            # Step environment
            observation_n, reward_n, done_n, info = self.env.step(np.array(all_actions))
            
            # Show rewards
            home_reward = np.sum(reward_n[:3])
            away_reward = np.sum(reward_n[3:])
            if home_reward != 0 or away_reward != 0:
                print(f"  💰 Rewards: Home={home_reward:.2f}, Away={away_reward:.2f}")
            
            if any(done_n):
                print(f"  Episode ended at step {step}")
                break
                
        self.env.close()
    
    def diagnose_weapon_availability(self):
        """Check if weapons are actually available to agents"""
        print(f"\n🗡️ WEAPON AVAILABILITY ANALYSIS")
        print("=" * 35)
        
        self.env = DerkEnv(n_arenas=1, turbo_mode=True)
        observation_n = self.env.reset()
        
        # Check all agents for weapon availability
        for i, obs in enumerate(observation_n):
            team = "Home" if i < 3 else "Away"
            agent_num = i if i < 3 else i - 3
            
            weapons = {
                "Talons": obs[ObservationKeys.HasTalons.value],
                "Magnum": obs[ObservationKeys.HasMagnum.value],
                "Pistol": obs[ObservationKeys.HasPistol.value],
                "BloodClaws": obs[ObservationKeys.HasBloodClaws.value],
                "Blaster": obs[ObservationKeys.HasBlaster.value],
                "Cleavers": obs[ObservationKeys.HasCleavers.value],
                "Cripplers": obs[ObservationKeys.HasCripplers.value]
            }
            
            active_weapons = [(k, v) for k, v in weapons.items() if v > 0.1]
            print(f"{team} Agent {agent_num}: {active_weapons}")
            
        self.env.close()
    
    def diagnose_reward_scaling(self):
        """Check if reward scaling is working correctly"""
        print(f"\n💰 REWARD SCALING ANALYSIS")
        print("=" * 30)
        
        # Test reward calculations
        nightrider_config = self.nightrider.get_derk_gym_config()
        assaulter_config = self.assaulter.get_derk_gym_config()
        
        print("🌙 Nightrider Reward Function:")
        for key, value in nightrider_config['rewardFunction'].items():
            print(f"  {key}: {value}")
            
        print("\n⚔️ Assaulter Reward Function:")
        for key, value in assaulter_config['rewardFunction'].items():
            print(f"  {key}: {value}")
            
        # Test a sample reward calculation
        print(f"\nSample reward calculations:")
        print(f"If Nightrider kills an enemy unit:")
        print(f"  Base reward * custom multiplier = ? * {nightrider_config['rewardFunction']['killEnemyUnit']}")
        print(f"If Assaulter kills an enemy unit:")
        print(f"  Base reward * custom multiplier = ? * {assaulter_config['rewardFunction']['killEnemyUnit']}")
    
    def run_full_diagnostic(self):
        """Run complete diagnostic suite"""
        print("🔧 FULL BRAIN DIAGNOSTIC SUITE")
        print("=" * 35)
        
        self.diagnose_observations()
        self.diagnose_weapon_availability() 
        self.diagnose_actions()
        self.diagnose_reward_scaling()
        
        print(f"\n🎯 DIAGNOSTIC SUMMARY")
        print("=" * 22)
        print("Key questions to investigate:")
        print("1. Are weapons actually equipped in the basic environment?")
        print("2. Are the custom reward functions being applied correctly?")
        print("3. Are the brain actions actually causing combat?")
        print("4. Is the environment giving any base rewards to modify?")

def main():
    """Main diagnostic function"""
    diagnostic = DetailedDiagnostic()
    diagnostic.run_full_diagnostic()

if __name__ == "__main__":
    main()
