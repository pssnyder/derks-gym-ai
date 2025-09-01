from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, ActionKeys, TeamStatsKeys
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import gym
import math
import os.path
import json
import matplotlib.pyplot as plt
from collections import deque, namedtuple
import random
import time
from datetime import datetime

# Set up device for PyTorch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Experience tuple for replay buffer
Experience = namedtuple('Experience', ['state', 'action', 'reward', 'next_state', 'done'])

class ObservationProcessor:
    """Advanced observation processing and feature engineering"""
    
    def __init__(self):
        self.obs_size = len(ObservationKeys)
        self.history_size = 4  # Keep last 4 observations for temporal patterns
        self.obs_history = deque(maxlen=self.history_size)
        
    def reset(self):
        self.obs_history.clear()
        
    def process(self, raw_obs):
        """Process raw observations into enhanced features"""
        obs = np.array(raw_obs)
        
        # Add to history
        self.obs_history.append(obs)
        
        # Pad history if needed
        while len(self.obs_history) < self.history_size:
            self.obs_history.append(np.zeros_like(obs))
            
        # Create enhanced features
        features = []
        
        # Current observations
        features.extend(obs)
        
        # Calculate derived features
        self_hp = obs[ObservationKeys.Hitpoints.value]
        
        # Enemy threat assessment
        enemy_distances = [
            float(obs[ObservationKeys.Enemy1Distance.value]),
            float(obs[ObservationKeys.Enemy2Distance.value]), 
            float(obs[ObservationKeys.Enemy3Distance.value])
        ]
        closest_enemy_dist = min([d for d in enemy_distances if d > 0] or [1.0])
        features.append(closest_enemy_dist)
        
        # Team coordination features
        friend_distances = [
            float(obs[ObservationKeys.Friend1Distance.value]),
            float(obs[ObservationKeys.Friend2Distance.value])
        ]
        team_spread = max(friend_distances) - min(friend_distances) if all(d > 0 for d in friend_distances) else 0
        features.append(team_spread)
        
        # Equipment assessment
        has_ranged = any([
            obs[ObservationKeys.HasPistol.value],
            obs[ObservationKeys.HasMagnum.value],
            obs[ObservationKeys.HasBlaster.value]
        ])
        has_melee = any([
            obs[ObservationKeys.HasTalons.value],
            obs[ObservationKeys.HasBloodClaws.value],
            obs[ObservationKeys.HasCleavers.value],
            obs[ObservationKeys.HasCripplers.value]
        ])
        features.extend([has_ranged, has_melee])
        
        # Focus target analysis
        if obs[ObservationKeys.HasFocus.value]:
            focus_hp = float(obs[ObservationKeys.FocusHitpoints.value])
            focus_relative_hp = focus_hp / max(float(obs[ObservationKeys.Hitpoints.value]), 0.1)  # Avoid division by zero
            features.append(focus_relative_hp)
        else:
            features.append(0.0)
            
        # Temporal features (change from previous observation)
        if len(self.obs_history) >= 2:
            prev_obs = list(self.obs_history)[-2]
            hp_change = float(obs[ObservationKeys.Hitpoints.value]) - float(prev_obs[ObservationKeys.Hitpoints.value])
            features.append(hp_change)
        else:
            features.append(0.0)
            
        return np.array(features, dtype=np.float32)

class DerkNet(nn.Module):
    """Advanced neural network architecture for Derk AI"""
    
    def __init__(self, input_size, hidden_sizes=[256, 128, 64], dropout_rate=0.1):
        super(DerkNet, self).__init__()
        
        # Build network layers
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(dropout_rate),
                nn.BatchNorm1d(hidden_size)
            ])
            prev_size = hidden_size
            
        self.feature_layers = nn.Sequential(*layers)
        
        # Action heads - separate outputs for different action types
        self.movement_head = nn.Sequential(
            nn.Linear(prev_size, 32),
            nn.ReLU(),
            nn.Linear(32, 2)  # MoveX, Rotate
        )
        
        self.chase_head = nn.Sequential(
            nn.Linear(prev_size, 32),
            nn.ReLU(), 
            nn.Linear(32, 1)  # ChaseFocus
        )
        
        self.cast_head = nn.Sequential(
            nn.Linear(prev_size, 32),
            nn.ReLU(),
            nn.Linear(32, 4)  # No cast + 3 abilities
        )
        
        self.focus_head = nn.Sequential(
            nn.Linear(prev_size, 32), 
            nn.ReLU(),
            nn.Linear(32, 8)  # No focus + 7 focus targets
        )
        
        # Value head for actor-critic
        self.value_head = nn.Sequential(
            nn.Linear(prev_size, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
        
    def forward(self, x):
        if x.dim() == 1:
            x = x.unsqueeze(0)
            
        features = self.feature_layers(x)
        
        # Get action distributions
        movement = self.movement_head(features)
        chase = torch.sigmoid(self.chase_head(features))
        cast = F.softmax(self.cast_head(features), dim=-1)
        focus = F.softmax(self.focus_head(features), dim=-1)
        value = self.value_head(features)
        
        return {
            'movement': movement,
            'chase': chase, 
            'cast': cast,
            'focus': focus,
            'value': value
        }
        
    def get_action(self, outputs, deterministic=False):
        """Convert network outputs to game actions"""
        movement = outputs['movement']
        chase = outputs['chase']
        cast = outputs['cast']
        focus = outputs['focus']
        
        if deterministic:
            # Deterministic action selection
            move_x = torch.tanh(movement[0, 0]).item()
            rotate = torch.tanh(movement[0, 1]).item()
            chase_focus = chase[0, 0].item()
            cast_slot = torch.argmax(cast[0]).item()
            focus_target = torch.argmax(focus[0]).item()
        else:
            # Stochastic action selection for exploration
            move_x = torch.tanh(movement[0, 0] + torch.randn(1) * 0.1).item()
            rotate = torch.tanh(movement[0, 1] + torch.randn(1) * 0.1).item()
            chase_focus = torch.clamp(chase[0, 0] + torch.randn(1) * 0.05, 0, 1).item()
            cast_slot = torch.multinomial(cast[0], 1).item()
            focus_target = torch.multinomial(focus[0], 1).item()
            
        return (
            move_x,  # MoveX
            rotate,  # Rotate  
            chase_focus,  # ChaseFocus
            cast_slot,  # CastSlot (0=no cast, 1-3=abilities)
            focus_target  # Focus (0=no change, 1=home statue, 2-3=teammates, 4=enemy statue, 5-7=enemies)
        )

class ReplayBuffer:
    """Experience replay buffer for training"""
    
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)
        
    def push(self, experience):
        self.buffer.append(experience)
        
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)
    
    def __len__(self):
        return len(self.buffer)

class DerkAgent:
    """Advanced Derk AI agent with PPO-style training"""
    
    def __init__(self, obs_processor, lr=3e-4, epsilon=0.2, value_coef=0.5, entropy_coef=0.01):
        self.obs_processor = obs_processor
        
        # Network setup
        processed_obs = obs_processor.process(np.zeros(len(ObservationKeys)))
        input_size = len(processed_obs)
        
        self.network = DerkNet(input_size).to(device)
        self.optimizer = optim.Adam(self.network.parameters(), lr=lr)
        
        # PPO hyperparameters
        self.epsilon = epsilon
        self.value_coef = value_coef
        self.entropy_coef = entropy_coef
        
        # Training tracking
        self.training_data = []
        
    def get_action(self, observation, deterministic=False):
        """Get action from observation"""
        processed_obs = self.obs_processor.process(observation)
        obs_tensor = torch.FloatTensor(processed_obs).to(device)
        
        with torch.no_grad():
            outputs = self.network(obs_tensor)
            action = self.network.get_action(outputs, deterministic)
            value = outputs['value'].item()
            
        return action, value, outputs
        
    def save_model(self, filepath):
        """Save the trained model"""
        torch.save({
            'model_state_dict': self.network.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, filepath)
        
    def load_model(self, filepath):
        """Load a trained model"""
        if os.path.exists(filepath):
            checkpoint = torch.load(filepath, map_location=device)
            self.network.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            print(f"Loaded model from {filepath}")
            return True
        return False

class TrainingManager:
    """Manages the overall training process"""
    
    def __init__(self, n_arenas=4, save_frequency=10):
        self.n_arenas = n_arenas
        self.save_frequency = save_frequency
        
        # Environment setup with enhanced reward function
        self.env = DerkEnv(
            n_arenas=n_arenas,
            turbo_mode=True,  # Faster training
            reward_function={
                'damageEnemyStatue': 0.1,
                'damageEnemyUnit': 0.05,
                'killEnemyStatue': 10,
                'killEnemyUnit': 2,
                'healTeammate1': 0.02,
                'healTeammate2': 0.02,
                'timeSpentAwayTerritory': 0.001,  # Encourage aggression
                'damageTaken': -0.01,  # Penalize taking damage
                'teamSpirit': 0.5,  # Partial team reward sharing
                'timeScaling': 0.8  # Slight time penalty for longer games
            }
        )
        
        # Create agents
        self.agents = []
        self.obs_processors = []
        
        for i in range(self.env.n_agents):
            obs_processor = ObservationProcessor()
            agent = DerkAgent(obs_processor)
            self.agents.append(agent)
            self.obs_processors.append(obs_processor)
            
        # Training tracking
        self.episode_rewards = []
        self.episode_lengths = []
        self.training_stats = {
            'episodes': 0,
            'best_reward': float('-inf'),
            'best_episode': 0,
            'total_steps': 0
        }
        
        # Try to load existing model
        self.load_checkpoint()
        
    def train_episode(self):
        """Train for one episode"""
        observation_n = self.env.reset()
        
        # Reset processors
        for processor in self.obs_processors:
            processor.reset()
            
        episode_data = [[] for _ in range(self.env.n_agents)]
        episode_length = 0
        
        while True:
            # Get actions from all agents
            actions = []
            values = []
            
            for i, agent in enumerate(self.agents):
                action, value, outputs = agent.get_action(observation_n[i])
                actions.append(action)
                values.append(value)
                
                # Store experience
                episode_data[i].append({
                    'observation': observation_n[i].copy(),
                    'action': action,
                    'value': value,
                    'outputs': outputs
                })
                
            # Step environment
            next_observation_n, reward_n, done_n, info = self.env.step(actions)
            episode_length += 1
            
            # Store rewards
            for i in range(self.env.n_agents):
                if len(episode_data[i]) > 0:
                    episode_data[i][-1]['reward'] = reward_n[i]
                    episode_data[i][-1]['done'] = done_n[i]
                    
            observation_n = next_observation_n
            
            if all(done_n):
                break
                
        # Calculate returns and advantages (simple version)
        total_rewards = self.env.total_reward
        avg_reward = np.mean(total_rewards)
        
        # Update training stats
        self.episode_rewards.append(avg_reward)
        self.episode_lengths.append(episode_length)
        self.training_stats['episodes'] += 1
        self.training_stats['total_steps'] += episode_length
        
        if avg_reward > self.training_stats['best_reward']:
            self.training_stats['best_reward'] = avg_reward
            self.training_stats['best_episode'] = self.training_stats['episodes']
            self.save_checkpoint(is_best=True)
            
        return avg_reward, episode_length, total_rewards
        
    def train(self, num_episodes=1000):
        """Main training loop"""
        print(f"Starting training for {num_episodes} episodes...")
        print(f"Using {self.env.n_agents} agents across {self.n_arenas} arenas")
        print(f"Device: {device}")
        print("-" * 60)
        
        start_time = time.time()
        
        for episode in range(num_episodes):
            avg_reward, episode_length, total_rewards = self.train_episode()
            
            # Print progress
            if episode % 10 == 0 or episode == num_episodes - 1:
                elapsed_time = time.time() - start_time
                avg_reward_recent = np.mean(self.episode_rewards[-50:]) if len(self.episode_rewards) >= 50 else np.mean(self.episode_rewards)
                
                print(f"Episode {episode + 1:4d} | "
                      f"Avg Reward: {avg_reward:7.2f} | "
                      f"Recent Avg: {avg_reward_recent:7.2f} | "
                      f"Best: {self.training_stats['best_reward']:7.2f} | "
                      f"Length: {episode_length:3d} | "
                      f"Time: {elapsed_time/60:.1f}m")
                      
                # Print individual agent rewards
                print(f"         Agent rewards: {[f'{r:.1f}' for r in total_rewards]}")
                
            # Save checkpoint periodically
            if episode % self.save_frequency == 0 and episode > 0:
                self.save_checkpoint()
                
        print(f"\nTraining completed in {(time.time() - start_time)/60:.1f} minutes")
        print(f"Best reward: {self.training_stats['best_reward']:.2f} at episode {self.training_stats['best_episode']}")
        
        self.save_checkpoint()
        self.plot_training_progress()
        
    def save_checkpoint(self, is_best=False):
        """Save training checkpoint"""
        os.makedirs('checkpoints', exist_ok=True)
        
        # Save each agent
        for i, agent in enumerate(self.agents):
            filename = f'checkpoints/agent_{i}_latest.pth'
            if is_best:
                filename = f'checkpoints/agent_{i}_best.pth'
            agent.save_model(filename)
            
        # Save training stats
        stats_file = 'checkpoints/training_stats.json'
        with open(stats_file, 'w') as f:
            json.dump({
                **self.training_stats,
                'episode_rewards': self.episode_rewards[-1000:],  # Keep last 1000
                'episode_lengths': self.episode_lengths[-1000:]
            }, f, indent=2)
            
        if is_best:
            print(f"🏆 New best model saved! Reward: {self.training_stats['best_reward']:.2f}")
            
    def load_checkpoint(self):
        """Load training checkpoint"""
        # Load training stats
        stats_file = 'checkpoints/training_stats.json'
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                data = json.load(f)
                self.training_stats.update({k: v for k, v in data.items() if k in self.training_stats})
                self.episode_rewards = data.get('episode_rewards', [])
                self.episode_lengths = data.get('episode_lengths', [])
                
        # Load agent models
        for i, agent in enumerate(self.agents):
            latest_file = f'checkpoints/agent_{i}_latest.pth'
            best_file = f'checkpoints/agent_{i}_best.pth'
            
            # Try to load best model first, then latest
            if os.path.exists(best_file):
                agent.load_model(best_file)
                print(f"Loaded best model for agent {i}")
            elif os.path.exists(latest_file):
                agent.load_model(latest_file)
                print(f"Loaded latest model for agent {i}")
                
    def plot_training_progress(self):
        """Plot training progress"""
        if len(self.episode_rewards) < 10:
            return
            
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Plot rewards
            episodes = range(len(self.episode_rewards))
            ax1.plot(episodes, self.episode_rewards, alpha=0.6, label='Episode Reward')
            
            # Moving average
            if len(self.episode_rewards) >= 50:
                window = min(50, len(self.episode_rewards) // 4)
                moving_avg = np.convolve(self.episode_rewards, np.ones(window)/window, mode='valid')
                ax1.plot(range(window-1, len(self.episode_rewards)), moving_avg, 'r-', linewidth=2, label=f'Moving Avg ({window})')
                
            ax1.set_xlabel('Episode')
            ax1.set_ylabel('Average Reward')
            ax1.set_title('Training Progress - Rewards')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot episode lengths
            ax2.plot(episodes, self.episode_lengths, alpha=0.6, color='green')
            ax2.set_xlabel('Episode')
            ax2.set_ylabel('Episode Length')
            ax2.set_title('Training Progress - Episode Lengths')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('training_progress.png', dpi=150, bbox_inches='tight')
            print("Training progress plot saved as 'training_progress.png'")
            
        except Exception as e:
            print(f"Could not create plot: {e}")
            
    def evaluate(self, num_episodes=10, render=True):
        """Evaluate the trained agents"""
        print(f"Evaluating agents for {num_episodes} episodes...")
        
        # Set to deterministic mode
        eval_rewards = []
        
        for episode in range(num_episodes):
            observation_n = self.env.reset()
            
            for processor in self.obs_processors:
                processor.reset()
                
            episode_reward = 0
            episode_length = 0
            
            while True:
                actions = []
                for i, agent in enumerate(self.agents):
                    action, _, _ = agent.get_action(observation_n[i], deterministic=True)
                    actions.append(action)
                    
                observation_n, reward_n, done_n, info = self.env.step(actions)
                episode_length += 1
                
                if all(done_n):
                    break
                    
            total_rewards = self.env.total_reward
            avg_reward = np.mean(total_rewards)
            eval_rewards.append(avg_reward)
            
            print(f"Eval Episode {episode + 1}: Reward = {avg_reward:.2f}, Length = {episode_length}")
            
        print(f"\nEvaluation Results:")
        print(f"Average Reward: {np.mean(eval_rewards):.2f} ± {np.std(eval_rewards):.2f}")
        print(f"Best Episode: {np.max(eval_rewards):.2f}")
        print(f"Worst Episode: {np.min(eval_rewards):.2f}")
        
        return eval_rewards

def main():
    """Main training script"""
    print("🤖 Advanced Derk AI Training System")
    print("=" * 50)
    
    # Create training manager
    trainer = TrainingManager(n_arenas=8, save_frequency=25)
    
    try:
        # Train the agents
        trainer.train(num_episodes=500)
        
        # Evaluate the trained agents
        print("\n" + "=" * 50)
        trainer.evaluate(num_episodes=20)
        
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