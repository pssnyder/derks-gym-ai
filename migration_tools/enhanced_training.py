"""
Enhanced Training System with Brain Migration Support
===================================================

This enhanced version of your training system includes support for migrating
strategies from your Steam game brains.
"""

import os
import sys
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from datetime import datetime

# Import your existing components
from train-derk import ObservationProcessor, DerkNet, DerkAgent, TrainingManager
from migration_tool import BrainMigrationTool
from brain_migration_guide import RuleBasedBrain, StrategyLibrary

class HybridTrainingManager(TrainingManager):
    """
    Enhanced training manager that can use rule-based brains as starting points
    for RL training, effectively migrating your Steam game strategies.
    """
    
    def __init__(self, n_arenas=4, save_frequency=10, use_steam_strategies=True):
        super().__init__(n_arenas, save_frequency)
        
        self.use_steam_strategies = use_steam_strategies
        self.migration_tool = BrainMigrationTool()
        self.rule_based_brains = []
        
        if use_steam_strategies:
            self.setup_steam_brain_integration()
    
    def setup_steam_brain_integration(self):
        """Set up integration with documented Steam brains"""
        print("🔄 Setting up Steam brain integration...")
        
        # Load any documented strategies
        documented_brains = list(self.migration_tool.strategies.get("strategies", {}).keys())
        
        if documented_brains:
            print(f"Found {len(documented_brains)} documented Steam brains:")
            for brain in documented_brains:
                print(f"  • {brain}")
            
            # Create rule-based versions
            self.create_rule_based_agents(documented_brains)
        else:
            print("No documented Steam brains found.")
            print("Use migration_tool.py to document your Steam strategies first.")
            
            # Use default strategies as examples
            self.create_default_strategy_agents()
    
    def create_rule_based_agents(self, brain_names):
        """Create rule-based agents from documented Steam brains"""
        self.rule_based_brains = []
        
        for brain_name in brain_names:
            strategy_data = self.migration_tool.strategies["strategies"][brain_name]
            brain = self.create_steam_brain_agent(brain_name, strategy_data)
            self.rule_based_brains.append(brain)
            
        print(f"Created {len(self.rule_based_brains)} rule-based agents from Steam brains")
    
    def create_default_strategy_agents(self):
        """Create default strategy agents as examples"""
        self.rule_based_brains = [
            StrategyLibrary.create_aggressive_brain(),
            StrategyLibrary.create_defensive_brain(),
            StrategyLibrary.create_support_brain()
        ]
        print("Created 3 default strategy agents")
    
    def create_steam_brain_agent(self, brain_name, strategy_data):
        """Create a rule-based agent from Steam brain documentation"""
        
        # Convert documented traits to numeric values
        aggression = float(strategy_data["combat"]["aggression_level"]) / 10.0
        
        role = strategy_data["team_coordination"]["role"].lower()
        team_focus_map = {"tank": 0.8, "support": 0.9, "damage": 0.4, "balanced": 0.6}
        team_focus = team_focus_map.get(role, 0.6)
        
        risk = strategy_data["personality"]["risk_tolerance"].lower()
        risk_map = {"cautious": 0.2, "moderate": 0.5, "reckless": 0.9}
        risk_tolerance = risk_map.get(risk, 0.5)
        
        weapon_pref = strategy_data["equipment"]["weapon_preference"]
        
        traits = {
            'aggression': aggression,
            'team_focus': team_focus,
            'risk_tolerance': risk_tolerance,
            'weapon_preference': weapon_pref
        }
        
        return RuleBasedBrain(brain_name, traits)
    
    def train_with_steam_brain_bootstrap(self, episodes_bootstrap=100, episodes_rl=400):
        """
        Two-phase training:
        1. Bootstrap with rule-based Steam brain behaviors
        2. Continue with full RL training
        """
        
        print("🚀 Starting Steam Brain Bootstrap Training")
        print("=" * 50)
        print(f"Phase 1: Bootstrap with rule-based behaviors ({episodes_bootstrap} episodes)")
        print(f"Phase 2: Full RL training ({episodes_rl} episodes)")
        print()
        
        # Phase 1: Bootstrap training
        if self.rule_based_brains and episodes_bootstrap > 0:
            self.bootstrap_phase(episodes_bootstrap)
        
        # Phase 2: Normal RL training
        print(f"\n🧠 Starting RL Training Phase ({episodes_rl} episodes)")
        print("=" * 50)
        self.train(episodes_rl)
        
        # Evaluate final performance
        print(f"\n📊 Final Evaluation")
        print("=" * 30)
        self.evaluate(num_episodes=20)
    
    def bootstrap_phase(self, num_episodes):
        """Bootstrap training using rule-based Steam brain behaviors"""
        print("Phase 1: Learning from Steam brain behaviors...")
        
        # Use rule-based brains to generate training data
        bootstrap_experiences = []
        
        for episode in range(num_episodes):
            if episode % 20 == 0:
                print(f"Bootstrap episode {episode + 1}/{num_episodes}")
            
            observation_n = self.env.reset()
            
            # Reset processors
            for processor in self.obs_processors:
                processor.reset()
            
            episode_experiences = []
            episode_length = 0
            
            while True:
                # Get actions from rule-based brains
                rule_actions = []
                processed_observations = []
                
                for i, (agent, rule_brain) in enumerate(zip(self.agents, self.rule_based_brains)):
                    if i < len(self.rule_based_brains):
                        # Use rule-based brain
                        rule_action = rule_brain.get_action(observation_n[i])
                        rule_actions.append(rule_action)
                        
                        # Also get processed observation for RL agent
                        processed_obs = self.obs_processors[i].process(observation_n[i])
                        processed_observations.append(processed_obs)
                    else:
                        # Use RL agent for remaining agents
                        action, value, outputs = agent.get_action(observation_n[i])
                        rule_actions.append(action)
                        processed_observations.append(
                            self.obs_processors[i].process(observation_n[i])
                        )
                
                # Step environment
                next_observation_n, reward_n, done_n, info = self.env.step(rule_actions)
                episode_length += 1
                
                # Store experiences for imitation learning
                for i in range(min(len(self.rule_based_brains), len(self.agents))):
                    experience = {
                        'observation': processed_observations[i],
                        'action': rule_actions[i],
                        'reward': reward_n[i],
                        'done': done_n[i]
                    }
                    episode_experiences.append((i, experience))
                
                observation_n = next_observation_n
                
                if all(done_n):
                    break
            
            # Train RL agents on rule-based behaviors (imitation learning)
            self.imitation_learning_update(episode_experiences)
            
            if episode % 25 == 0:
                avg_reward = np.mean(self.env.total_reward)
                print(f"  Bootstrap reward: {avg_reward:.2f}")
        
        print("Bootstrap phase completed! RL agents now initialized with Steam brain behaviors.")
    
    def imitation_learning_update(self, episode_experiences):
        """Update RL agents to imitate rule-based behaviors"""
        
        for agent_id, experience in episode_experiences:
            if agent_id >= len(self.agents):
                continue
                
            agent = self.agents[agent_id]
            obs = experience['observation']
            target_action = experience['action']
            
            # Convert observation to tensor
            obs_tensor = torch.FloatTensor(obs).unsqueeze(0).to(agent.network.device)
            
            # Get network outputs
            outputs = agent.network(obs_tensor)
            
            # Create target tensors for imitation
            target_move_x = torch.FloatTensor([target_action[0]]).to(agent.network.device)
            target_rotate = torch.FloatTensor([target_action[1]]).to(agent.network.device)
            target_chase = torch.FloatTensor([target_action[2]]).to(agent.network.device)
            target_cast = torch.LongTensor([target_action[3]]).to(agent.network.device)
            target_focus = torch.LongTensor([target_action[4]]).to(agent.network.device)
            
            # Compute imitation losses
            movement_loss = F.mse_loss(
                torch.tanh(outputs['movement'][0, :2]), 
                torch.stack([target_move_x, target_rotate])
            )
            
            chase_loss = F.mse_loss(outputs['chase'][0, 0], target_chase)
            
            cast_loss = F.cross_entropy(
                outputs['cast'][0:1], 
                target_cast
            )
            
            focus_loss = F.cross_entropy(
                outputs['focus'][0:1], 
                target_focus
            )
            
            # Total loss
            total_loss = movement_loss + chase_loss + cast_loss + focus_loss
            
            # Update network
            agent.optimizer.zero_grad()
            total_loss.backward()
            agent.optimizer.step()
    
    def compare_with_steam_brains(self, num_episodes=10):
        """Compare trained RL agents with original rule-based Steam brains"""
        print("🔬 Comparing RL agents with Steam brain strategies...")
        
        # Test rule-based brains
        rule_rewards = []
        for i, rule_brain in enumerate(self.rule_based_brains):
            print(f"\nTesting rule-based brain: {rule_brain.strategy_name}")
            rewards = self.test_single_strategy(rule_brain, num_episodes)
            rule_rewards.append(np.mean(rewards))
            print(f"Average reward: {np.mean(rewards):.2f}")
        
        # Test RL agents
        print(f"\nTesting trained RL agents...")
        rl_rewards = self.evaluate(num_episodes, render=False)
        
        # Comparison
        print(f"\n📊 PERFORMANCE COMPARISON")
        print("=" * 40)
        for i, (rule_reward, brain) in enumerate(zip(rule_rewards, self.rule_based_brains)):
            improvement = np.mean(rl_rewards) - rule_reward
            improvement_pct = (improvement / abs(rule_reward)) * 100 if rule_reward != 0 else 0
            
            print(f"{brain.strategy_name:15}: {rule_reward:6.2f} -> {np.mean(rl_rewards):6.2f} "
                  f"({improvement:+.2f}, {improvement_pct:+.1f}%)")
        
        return rule_rewards, rl_rewards
    
    def test_single_strategy(self, brain, num_episodes):
        """Test a single rule-based strategy"""
        rewards = []
        
        for episode in range(num_episodes):
            observation_n = self.env.reset()
            
            while True:
                actions = []
                for i in range(self.env.n_agents):
                    if i == 0:  # Use the specific brain for first agent
                        action = brain.get_action(observation_n[i])
                    else:  # Use random actions for others
                        action = self.env.action_space.sample()
                    actions.append(action)
                    
                observation_n, reward_n, done_n, info = self.env.step(np.array(actions))
                
                if all(done_n):
                    break
            
            rewards.append(self.env.total_reward[0])  # First agent's reward
        
        return rewards

def main():
    """Main function with Steam brain integration"""
    print("🎮 Enhanced Derk AI Training with Steam Brain Migration")
    print("=" * 60)
    
    # Check if user has documented any Steam brains
    migration_tool = BrainMigrationTool()
    documented_brains = list(migration_tool.strategies.get("strategies", {}).keys())
    
    if not documented_brains:
        print("⚠️  No Steam brains documented yet!")
        print("To get the most out of this system:")
        print("1. Run 'python migration_tool.py' to document your Steam strategies")
        print("2. Then run this script again")
        print()
        
        choice = input("Continue with default strategies? (y/n): ").lower()
        if choice != 'y':
            print("Please document your Steam brains first using migration_tool.py")
            return
    
    # Create enhanced training manager
    trainer = HybridTrainingManager(
        n_arenas=6,
        save_frequency=25,
        use_steam_strategies=True
    )
    
    try:
        # Train with Steam brain bootstrap
        trainer.train_with_steam_brain_bootstrap(
            episodes_bootstrap=150,  # Learn from Steam brains
            episodes_rl=350         # Continue with RL
        )
        
        # Compare performance
        print("\n" + "=" * 60)
        trainer.compare_with_steam_brains(num_episodes=15)
        
    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
        trainer.save_checkpoint()
        
    except Exception as e:
        print(f"\nTraining error: {e}")
        trainer.save_checkpoint()
        
    finally:
        trainer.env.close()
        print("Environment closed")

if __name__ == "__main__":
    main()
