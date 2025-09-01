"""
Team Training Interface - Testing Class Derklings
=================================================

Train The Assaulter, The Engineer, and The Peacemaker as a team
against themselves to develop team coordination and strategies.

This matches the Steam experience but with team-based training.
"""

from derk_steam_interface import DerkGameInterface
import numpy as np
import time
from datetime import datetime
import os
import json

class TeamTrainingSession:
    """Train a team of 3 derklings against themselves"""
    
    def __init__(self):
        self.game = DerkGameInterface()
        
        # Import the testing class brain profiles
        try:
            from brain_profiles.testing_class.the_assaulter import TheAssaulterBrain
            from brain_profiles.testing_class.the_engineer import TheEngineerBrain
            from brain_profiles.testing_class.the_peacemaker import ThePeacemakerBrain
            
            # Register the testing team
            self.assaulter = self.game.register_derkling("The Assaulter", TheAssaulterBrain())
            self.engineer = self.game.register_derkling("The Engineer", TheEngineerBrain())
            self.peacemaker = self.game.register_derkling("The Peacemaker", ThePeacemakerBrain())
            
            self.team_derklings = [
                ("The Assaulter", TheAssaulterBrain()),
                ("The Engineer", TheEngineerBrain()), 
                ("The Peacemaker", ThePeacemakerBrain())
            ]
            
            print("✅ Testing Class Team Assembled:")
            print("   🗡️  The Assaulter - Pure aggression assault fighter")
            print("   🛡️  The Engineer - Defensive support specialist")
            print("   ⚖️  The Peacemaker - Balanced control specialist")
            
        except ImportError as e:
            print(f"❌ Could not import testing class profiles: {e}")
            self.team_derklings = None
            
    def train_testing_team(self, iterations=1000):
        """Train the testing team against themselves"""
        
        if not self.team_derklings:
            print("❌ Testing team not available")
            return None
            
        print(f"\n🏋️ TRAINING TESTING CLASS TEAM")
        print("=" * 50)
        print(f"Team vs Team training for {iterations} iterations")
        print("Each derkling will learn their role within the team!")
        
        # Create environment - this will be 3v3 by default
        from gym_derk.envs import DerkEnv
        
        # Combine reward functions from all team members
        combined_rewards = self._combine_team_rewards()
        
        env = DerkEnv(
            n_arenas=1,
            turbo_mode=True,  # Fast training like Steam
            reward_function=combined_rewards
        )
        
        print(f"Environment: {env.n_agents} agents (3v3 team training)")
        print(f"Combined team reward function: {combined_rewards}")
        
        training_results = []
        start_time = time.time()
        
        try:
            for iteration in range(iterations):
                # Reset environment
                obs = env.reset()
                
                team_rewards = [0, 0, 0, 0, 0, 0]  # Track each agent's reward
                episode_length = 0
                
                while True:
                    actions = []
                    
                    # Team 1 (positions 0, 1, 2) - our training team
                    for agent_idx in range(3):
                        derkling_name, brain_class = self.team_derklings[agent_idx]
                        
                        if hasattr(brain_class, 'get_action'):
                            try:
                                action = brain_class.get_action(obs[agent_idx])
                            except:
                                action = env.action_space.sample()  # Fallback
                        else:
                            action = env.action_space.sample()
                            
                        actions.append(action)
                    
                    # Team 2 (positions 3, 4, 5) - copy of our team (self-play)
                    for agent_idx in range(3, 6):
                        team_idx = agent_idx - 3  # Map to team 1 indices
                        derkling_name, brain_class = self.team_derklings[team_idx]
                        
                        if hasattr(brain_class, 'get_action'):
                            try:
                                action = brain_class.get_action(obs[agent_idx])
                            except:
                                action = env.action_space.sample()  # Fallback
                        else:
                            action = env.action_space.sample()
                            
                        actions.append(action)
                    
                    # Step environment
                    obs, rewards, dones, info = env.step(np.array(actions))
                    
                    # Accumulate rewards for each agent
                    for i in range(6):
                        team_rewards[i] += rewards[i]
                    
                    episode_length += 1
                    
                    if all(dones):
                        break
                
                # Calculate team performance
                team1_total = sum(team_rewards[:3])  # Our training team
                team2_total = sum(team_rewards[3:])  # Mirror team
                
                training_results.append({
                    'iteration': iteration + 1,
                    'team1_reward': float(team1_total),
                    'team2_reward': float(team2_total),
                    'individual_rewards': [float(r) for r in team_rewards],
                    'length': episode_length,
                    'winner': 'Team1' if team1_total > team2_total else 'Team2' if team2_total > team1_total else 'Draw'
                })
                
                # Print progress
                if (iteration + 1) % max(1, iterations // 20) == 0:
                    progress = (iteration + 1) / iterations * 100
                    elapsed = time.time() - start_time
                    
                    # Recent team performance
                    recent_results = training_results[-50:] if len(training_results) >= 50 else training_results
                    avg_team1 = np.mean([r['team1_reward'] for r in recent_results])
                    avg_team2 = np.mean([r['team2_reward'] for r in recent_results])
                    
                    # Win statistics
                    recent_wins = [r['winner'] for r in recent_results]
                    team1_wins = recent_wins.count('Team1')
                    team2_wins = recent_wins.count('Team2')
                    draws = recent_wins.count('Draw')
                    
                    print(f"Progress: {progress:5.1f}% | "
                          f"Iteration: {iteration + 1:4d}/{iterations} | "
                          f"Team1: {avg_team1:6.2f} | Team2: {avg_team2:6.2f} | "
                          f"W/L/D: {team1_wins}/{team2_wins}/{draws} | "
                          f"Time: {elapsed/60:.1f}m")
                          
        except KeyboardInterrupt:
            print("\n⏸️ Training interrupted by user")
            
        finally:
            env.close()
            
        # Save training results
        self._save_team_training_results(training_results)
        
        # Training summary
        total_time = time.time() - start_time
        final_results = training_results[-100:] if len(training_results) >= 100 else training_results
        
        final_team1_avg = np.mean([r['team1_reward'] for r in final_results])
        final_team2_avg = np.mean([r['team2_reward'] for r in final_results])
        
        final_wins = [r['winner'] for r in final_results]
        final_team1_wins = final_wins.count('Team1')
        final_team2_wins = final_wins.count('Team2')
        final_draws = final_wins.count('Draw')
        
        print(f"\n✅ TESTING TEAM TRAINING COMPLETE")
        print(f"   Total iterations: {len(training_results)}")
        print(f"   Training time: {total_time/60:.1f} minutes")
        print(f"   Final Team1 avg reward: {final_team1_avg:.2f}")
        print(f"   Final Team2 avg reward: {final_team2_avg:.2f}")
        print(f"   Final W/L/D record: {final_team1_wins}/{final_team2_wins}/{final_draws}")
        
        print(f"\n🎯 TEAM ROLES DEVELOPED:")
        print(f"   🗡️  The Assaulter learned aggressive assault tactics")
        print(f"   🛡️  The Engineer learned defensive support strategies") 
        print(f"   ⚖️  The Peacemaker learned balanced team coordination")
        
        return training_results
        
    def _combine_team_rewards(self):
        """Combine reward functions from all team members"""
        combined = {}
        
        if not self.team_derklings:
            # Default reward function if team not available
            return {
                'killEnemyStatue': 20,
                'killEnemyUnit': 10,
                'damageEnemyStatue': 2,
                'damageEnemyUnit': 1,
                'teamSpirit': 0.3
            }
        
        # Get each derkling's reward preferences
        for name, brain in self.team_derklings:
            if hasattr(brain, 'get_derk_gym_config'):
                config = brain.get_derk_gym_config()
                if 'reward_function' in config:
                    rewards = config['reward_function']
                    
                    # Combine rewards (taking maximum values to encourage all behaviors)
                    for key, value in rewards.items():
                        if key in combined:
                            combined[key] = max(combined[key], value)
                        else:
                            combined[key] = value
        
        # Add team coordination bonuses
        combined.update({
            'teamSpirit': 0.3,  # Reward team coordination
            'killEnemyStatue': max(combined.get('killEnemyStatue', 10), 20),  # High statue reward
            'killEnemyUnit': max(combined.get('killEnemyUnit', 5), 10),  # Good unit kill reward
        })
        
        return combined
        
    def _save_team_training_results(self, results):
        """Save team training results"""
        os.makedirs('team_training_results', exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f'team_training_results/testing_team_{timestamp}.json'
        
        training_data = {
            'team': ['The Assaulter', 'The Engineer', 'The Peacemaker'],
            'timestamp': datetime.now().isoformat(),
            'total_iterations': len(results),
            'results': results,
            'summary': self._analyze_team_performance(results)
        }
        
        with open(filepath, 'w') as f:
            json.dump(training_data, f, indent=2)
            
        print(f"📊 Training data saved: {filepath}")
        
    def _analyze_team_performance(self, results):
        """Analyze team training performance"""
        if not results:
            return {}
            
        team1_rewards = [r['team1_reward'] for r in results]
        team2_rewards = [r['team2_reward'] for r in results]
        winners = [r['winner'] for r in results]
        
        # Individual agent analysis
        individual_performance = {}
        for i in range(6):
            agent_rewards = [r['individual_rewards'][i] for r in results]
            agent_name = f"Team{'1' if i < 3 else '2'}_Agent{i % 3}"
            individual_performance[agent_name] = {
                'avg_reward': float(np.mean(agent_rewards)),
                'max_reward': float(np.max(agent_rewards)),
                'min_reward': float(np.min(agent_rewards))
            }
        
        return {
            'team1_avg_reward': float(np.mean(team1_rewards)),
            'team2_avg_reward': float(np.mean(team2_rewards)),
            'team1_wins': winners.count('Team1'),
            'team2_wins': winners.count('Team2'),
            'draws': winners.count('Draw'),
            'avg_episode_length': float(np.mean([r['length'] for r in results])),
            'individual_performance': individual_performance
        }

def main():
    """Train the testing class team"""
    
    print("🦎 TESTING CLASS TEAM TRAINING")
    print("=" * 40)
    
    # Create team training session
    trainer = TeamTrainingSession()
    
    if not trainer.team_derklings:
        print("❌ Could not set up testing team")
        return
        
    print("\nStarting team vs team training...")
    print("This will develop each derkling's role within the team!")
    
    # Train for 1000 iterations
    results = trainer.train_testing_team(iterations=1000)
    
    if results:
        print(f"\n🏆 TRAINING SESSION COMPLETE!")
        print(f"The testing team is now trained and ready for battles!")
        print(f"\nNext: Set up battles against other teams or create Control Tower")

if __name__ == "__main__":
    main()
