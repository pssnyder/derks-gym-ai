"""
Reward Investigation Tool
========================

Analyze and improve the reward system for better training feedback.
"""

import numpy as np
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gym_derk.envs import DerkEnv
from src.brain_profiles.peanut_class.nightrider_peanut import NightriderPeanutBrain
from src.brain_profiles.testing_class.the_assaulter import TheAssaulterBrain

class RewardInvestigator:
    """Investigate reward patterns and improve feedback"""
    
    def __init__(self):
        self.env = None
        self.home_brain = NightriderPeanutBrain()
        self.away_brain = TheAssaulterBrain()
        
    def detailed_episode_analysis(self):
        """Run a detailed analysis of what's happening in battles"""
        print("🔍 DETAILED REWARD ANALYSIS")
        print("=" * 40)
        
        # Create environment
        self.env = DerkEnv(n_arenas=1, turbo_mode=True)
        observation_n = self.env.reset()
        
        print(f"Environment created with {len(observation_n)} agents")
        print(f"Observation shape: {np.array(observation_n[0]).shape}")
        
        # Analyze a single episode in detail
        episode_rewards = []
        step_details = []
        
        for step in range(200):  # Extended episode for more data
            actions = []
            
            # Generate actions
            for i in range(3):  # Home team
                action = self.home_brain.get_action(observation_n[i])
                actions.append(action)
            
            for i in range(3, 6):  # Away team
                action = self.away_brain.get_action(observation_n[i])
                actions.append(action)
            
            # Step environment
            observation_n, reward_n, done_n, info = self.env.step(np.array(actions))
            
            # Analyze rewards
            home_rewards = reward_n[:3]
            away_rewards = reward_n[3:]
            
            step_data = {
                'step': step,
                'home_rewards': home_rewards.tolist(),
                'away_rewards': away_rewards.tolist(),
                'home_total': float(np.sum(home_rewards)),
                'away_total': float(np.sum(away_rewards)),
                'any_rewards': bool(np.any(reward_n != 0)),
                'done': bool(any(done_n))
            }
            
            step_details.append(step_data)
            episode_rewards.append(reward_n.copy())
            
            # Print interesting steps
            if step_data['any_rewards'] or step < 5 or step % 50 == 0:
                print(f"Step {step:3d}: Home={step_data['home_total']:6.2f} {home_rewards}, Away={step_data['away_total']:6.2f} {away_rewards}")
            
            if any(done_n):
                print(f"Episode ended at step {step}")
                break
        
        self.env.close()
        
        # Analyze patterns
        self.analyze_reward_patterns(step_details)
        return step_details
    
    def analyze_reward_patterns(self, step_details):
        """Analyze patterns in the reward data"""
        print(f"\n📊 REWARD PATTERN ANALYSIS")
        print("=" * 30)
        
        # Find when rewards first appear
        first_home_reward = next((s['step'] for s in step_details if s['home_total'] != 0), None)
        first_away_reward = next((s['step'] for s in step_details if s['away_total'] != 0), None)
        
        print(f"First home reward at step: {first_home_reward}")
        print(f"First away reward at step: {first_away_reward}")
        
        # Count reward events
        home_reward_steps = [s for s in step_details if s['home_total'] != 0]
        away_reward_steps = [s for s in step_details if s['away_total'] != 0]
        
        print(f"Home reward events: {len(home_reward_steps)}")
        print(f"Away reward events: {len(away_reward_steps)}")
        
        if home_reward_steps:
            home_rewards = [s['home_total'] for s in home_reward_steps]
            print(f"Home reward range: {min(home_rewards):.2f} to {max(home_rewards):.2f}")
            print(f"Home avg reward per event: {np.mean(home_rewards):.2f}")
        
        if away_reward_steps:
            away_rewards = [s['away_total'] for s in away_reward_steps]
            print(f"Away reward range: {min(away_rewards):.2f} to {max(away_rewards):.2f}")
            print(f"Away avg reward per event: {np.mean(away_rewards):.2f}")
        
        # Total rewards
        total_home = sum(s['home_total'] for s in step_details)
        total_away = sum(s['away_total'] for s in step_details)
        
        print(f"\nTotal episode rewards:")
        print(f"  Home: {total_home:.2f}")
        print(f"  Away: {total_away:.2f}")
    
    def test_brain_actions(self):
        """Test what actions our brains are generating"""
        print(f"\n🧠 BRAIN ACTION ANALYSIS")
        print("=" * 30)
        
        # Create a sample observation
        self.env = DerkEnv(n_arenas=1, turbo_mode=True)
        observation_n = self.env.reset()
        
        # Test Nightrider actions
        print(f"🌙 Nightrider Peanut Actions:")
        for i in range(3):
            obs = observation_n[i]
            action = self.home_brain.get_action(obs)
            print(f"  Agent {i}: {action}")
        
        # Test Assaulter actions  
        print(f"\n⚔️ The Assaulter Actions:")
        for i in range(3, 6):
            obs = observation_n[i]
            action = self.away_brain.get_action(obs)
            print(f"  Agent {i}: {action}")
        
        self.env.close()
    
    def suggest_improvements(self):
        """Suggest improvements based on analysis"""
        print(f"\n💡 IMPROVEMENT SUGGESTIONS")
        print("=" * 35)
        
        print("1. Reward Function Tuning:")
        print("   - Increase frequency of positive rewards")
        print("   - Add movement/exploration bonuses")
        print("   - Scale team spirit effects")
        
        print("\n2. Environment Settings:")
        print("   - Try different arena configurations")
        print("   - Adjust episode length")
        print("   - Test with different team sizes")
        
        print("\n3. Brain Strategy Analysis:")
        print("   - Nightrider may be too defensive")
        print("   - Assaulter aggression is working")
        print("   - Consider hybrid strategies")

def main():
    """Run the reward investigation"""
    investigator = RewardInvestigator()
    
    # Run tests
    investigator.test_brain_actions()
    investigator.detailed_episode_analysis()
    investigator.suggest_improvements()
    
    print(f"\n✅ Investigation complete!")

if __name__ == "__main__":
    main()
