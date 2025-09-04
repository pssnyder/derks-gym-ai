"""
Number Eleven Neural Network Architecture
========================================

GRU-based recurrent neural network for self-learning derkling AI.
This network processes sequential game states and learns optimal strategies
through self-play without human bias.

Architecture inspired by AlphaZero but adapted for real-time action games.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class NetworkConfig:
    """Configuration for Number Eleven's neural network"""
    # Input dimensions
    raw_observation_dim: int = 64  # Based on gym_derk.ObservationKeys
    objective_metrics_dim: int = 7  # Health percentages, points, survival, progress
    
    # Hidden dimensions
    embedding_dim: int = 128
    gru_hidden_dim: int = 256
    gru_num_layers: int = 2
    
    # Output dimensions
    action_dim: int = 5  # MoveX, Rotate, ChaseFocus, CastingSlot, ChangeFocus
    value_output_dim: int = 1  # Position evaluation
    
    # Network parameters
    dropout_rate: float = 0.1
    learning_rate: float = 0.001
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'


class NumberElevenNetwork(nn.Module):
    """
    GRU-based neural network for Number Eleven.
    
    Architecture:
    1. Embedding layer for raw observations
    2. Objective metrics processing
    3. GRU for sequential learning
    4. Dual heads: action policy + position evaluation
    """
    
    def __init__(self, config: NetworkConfig):
        super(NumberElevenNetwork, self).__init__()
        self.config = config
        
        # Input processing layers
        self.raw_observation_embedding = nn.Sequential(
            nn.Linear(config.raw_observation_dim, config.embedding_dim),
            nn.ReLU(),
            nn.Dropout(config.dropout_rate),
            nn.Linear(config.embedding_dim, config.embedding_dim),
            nn.ReLU()
        )
        
        self.objective_metrics_embedding = nn.Sequential(
            nn.Linear(config.objective_metrics_dim, config.embedding_dim // 2),
            nn.ReLU(),
            nn.Linear(config.embedding_dim // 2, config.embedding_dim // 2),
            nn.ReLU()
        )
        
        # Combined input dimension
        combined_input_dim = config.embedding_dim + config.embedding_dim // 2
        
        # GRU for sequential processing
        self.gru = nn.GRU(
            input_size=combined_input_dim,
            hidden_size=config.gru_hidden_dim,
            num_layers=config.gru_num_layers,
            batch_first=True,
            dropout=config.dropout_rate if config.gru_num_layers > 1 else 0
        )
        
        # Action policy head (what to do)
        self.action_head = nn.Sequential(
            nn.Linear(config.gru_hidden_dim, config.gru_hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout_rate),
            nn.Linear(config.gru_hidden_dim // 2, config.action_dim)
        )
        
        # Value head (position evaluation)
        self.value_head = nn.Sequential(
            nn.Linear(config.gru_hidden_dim, config.gru_hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(config.dropout_rate),
            nn.Linear(config.gru_hidden_dim // 2, config.value_output_dim),
            nn.Tanh()  # Output between -1 and 1 for position evaluation
        )
        
        # Initialize weights
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize network weights using Xavier initialization"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.GRU):
                for name, param in module.named_parameters():
                    if 'weight' in name:
                        nn.init.xavier_uniform_(param)
                    elif 'bias' in name:
                        nn.init.zeros_(param)
    
    def forward(self, raw_observations: torch.Tensor, 
                objective_metrics: torch.Tensor,
                hidden_state: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Forward pass through the network.
        
        Args:
            raw_observations: (batch_size, seq_len, raw_obs_dim) Raw sensor data
            objective_metrics: (batch_size, seq_len, obj_metrics_dim) Health/score metrics
            hidden_state: Optional previous GRU hidden state
            
        Returns:
            action_logits: (batch_size, seq_len, action_dim) Action probabilities
            value_estimates: (batch_size, seq_len, 1) Position evaluations
            new_hidden_state: Updated GRU hidden state
        """
        batch_size, seq_len = raw_observations.shape[:2]
        
        # Process raw observations
        raw_embedded = self.raw_observation_embedding(raw_observations)
        
        # Process objective metrics
        obj_embedded = self.objective_metrics_embedding(objective_metrics)
        
        # Combine inputs
        combined_input = torch.cat([raw_embedded, obj_embedded], dim=-1)
        
        # GRU processing for sequential learning
        gru_output, new_hidden_state = self.gru(combined_input, hidden_state)
        
        # Generate action policy
        action_logits = self.action_head(gru_output)
        
        # Generate position evaluation
        value_estimates = self.value_head(gru_output)
        
        return action_logits, value_estimates, new_hidden_state
    
    def get_action_and_value(self, raw_obs: np.ndarray, 
                           obj_metrics: np.ndarray,
                           hidden_state: Optional[torch.Tensor] = None,
                           deterministic: bool = False) -> Tuple[np.ndarray, float, torch.Tensor]:
        """
        Get action and value estimate for a single step.
        
        Args:
            raw_obs: Raw observation array
            obj_metrics: Objective metrics array
            hidden_state: Previous hidden state
            deterministic: If True, use greedy action selection
            
        Returns:
            action: Selected action array
            value: Position evaluation
            new_hidden_state: Updated hidden state
        """
        self.eval()
        with torch.no_grad():
            # Convert to tensors and add batch/sequence dimensions
            raw_obs_tensor = torch.FloatTensor(raw_obs).unsqueeze(0).unsqueeze(0).to(self.config.device)
            obj_metrics_tensor = torch.FloatTensor(obj_metrics).unsqueeze(0).unsqueeze(0).to(self.config.device)
            
            # Forward pass
            action_logits, value_estimate, new_hidden_state = self.forward(
                raw_obs_tensor, obj_metrics_tensor, hidden_state
            )
            
            # Convert action logits to actual actions
            action_logits = action_logits.squeeze(0).squeeze(0)  # Remove batch and sequence dims
            value = value_estimate.squeeze().item()
            
            # Convert logits to actions based on action space
            action = self._logits_to_action(action_logits, deterministic)
            
        return action, value, new_hidden_state
    
    def _logits_to_action(self, action_logits: torch.Tensor, deterministic: bool = False) -> np.ndarray:
        """
        Convert network logits to actual game actions.
        
        Action format for gym_derk:
        [MoveX, Rotate, ChaseFocus, CastingSlot, ChangeFocus]
        """
        if deterministic:
            # Greedy action selection
            move_x = torch.tanh(action_logits[0]).item()
            rotate = torch.tanh(action_logits[1]).item()
            chase_focus = torch.sigmoid(action_logits[2]).item()
            
            # Discrete actions
            casting_slot = torch.argmax(action_logits[3:6]).item()  # 0-2 for slots, but 0 means no cast
            focus_target = torch.argmax(action_logits[6:13]).item()  # 0-6 for focus targets
            
        else:
            # Stochastic action selection for exploration
            move_x = torch.tanh(action_logits[0] + torch.randn(1) * 0.1).item()
            rotate = torch.tanh(action_logits[1] + torch.randn(1) * 0.1).item()
            chase_focus = torch.sigmoid(action_logits[2] + torch.randn(1) * 0.1).item()
            
            # Sample discrete actions
            cast_probs = F.softmax(action_logits[3:6], dim=0)
            casting_slot = torch.multinomial(cast_probs, 1).item()
            
            focus_probs = F.softmax(action_logits[6:13], dim=0)
            focus_target = torch.multinomial(focus_probs, 1).item()
        
        # Convert to gym_derk action format
        action = np.array([
            np.clip(move_x, -1.0, 1.0),      # MoveX
            np.clip(rotate, -1.0, 1.0),     # Rotate
            np.clip(chase_focus, 0.0, 1.0), # ChaseFocus
            casting_slot,                    # CastingSlot (0=no cast, 1-3=cast slot)
            focus_target                     # ChangeFocus (0=keep, 1-7=targets)
        ], dtype=np.float32)
        
        return action
    
    def clone(self) -> 'NumberElevenNetwork':
        """Create a copy of this network"""
        new_network = NumberElevenNetwork(self.config)
        new_network.load_state_dict(self.state_dict())
        return new_network
    
    def save(self, filepath: str):
        """Save network state"""
        torch.save({
            'model_state_dict': self.state_dict(),
            'config': self.config
        }, filepath)
    
    @classmethod
    def load(cls, filepath: str) -> 'NumberElevenNetwork':
        """Load network from file"""
        checkpoint = torch.load(filepath)
        network = cls(checkpoint['config'])
        network.load_state_dict(checkpoint['model_state_dict'])
        return network


class NumberElevenTrainer:
    """Training utilities for Number Eleven"""
    
    def __init__(self, network: NumberElevenNetwork, config: NetworkConfig):
        self.network = network
        self.config = config
        self.optimizer = torch.optim.Adam(network.parameters(), lr=config.learning_rate)
        self.action_criterion = nn.MSELoss()
        self.value_criterion = nn.MSELoss()
    
    def compute_loss(self, action_logits: torch.Tensor, value_estimates: torch.Tensor,
                    target_actions: torch.Tensor, target_values: torch.Tensor) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Compute training loss.
        
        Args:
            action_logits: Network action outputs
            value_estimates: Network value outputs  
            target_actions: Target action values
            target_values: Target value estimates
            
        Returns:
            total_loss: Combined loss for backpropagation
            loss_info: Dictionary with individual loss components
        """
        # Action loss
        action_loss = self.action_criterion(action_logits, target_actions)
        
        # Value loss
        value_loss = self.value_criterion(value_estimates, target_values)
        
        # Combined loss
        total_loss = action_loss + value_loss
        
        loss_info = {
            'total_loss': total_loss.item(),
            'action_loss': action_loss.item(),
            'value_loss': value_loss.item()
        }
        
        return total_loss, loss_info
    
    def train_step(self, batch_data: Dict[str, torch.Tensor]) -> Dict[str, float]:
        """
        Perform one training step.
        
        Args:
            batch_data: Dictionary containing training batch
            
        Returns:
            loss_info: Training metrics
        """
        self.network.train()
        self.optimizer.zero_grad()
        
        # Forward pass
        action_logits, value_estimates, _ = self.network(
            batch_data['raw_observations'],
            batch_data['objective_metrics']
        )
        
        # Compute loss
        total_loss, loss_info = self.compute_loss(
            action_logits, value_estimates,
            batch_data['target_actions'], batch_data['target_values']
        )
        
        # Backward pass
        total_loss.backward()
        
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.network.parameters(), max_norm=1.0)
        
        self.optimizer.step()
        
        return loss_info


def main():
    """Test the neural network architecture"""
    print("🤖 Number Eleven Neural Network Test")
    print("=" * 40)
    
    # Create network configuration
    config = NetworkConfig()
    print(f"🧠 Network Config:")
    print(f"   Raw observation dim: {config.raw_observation_dim}")
    print(f"   Objective metrics dim: {config.objective_metrics_dim}")
    print(f"   GRU hidden dim: {config.gru_hidden_dim}")
    print(f"   Device: {config.device}")
    
    # Create network
    network = NumberElevenNetwork(config).to(config.device)
    total_params = sum(p.numel() for p in network.parameters())
    print(f"🔢 Total parameters: {total_params:,}")
    
    # Test forward pass
    batch_size, seq_len = 2, 10
    raw_obs = torch.randn(batch_size, seq_len, config.raw_observation_dim).to(config.device)
    obj_metrics = torch.randn(batch_size, seq_len, config.objective_metrics_dim).to(config.device)
    
    print(f"\n🧪 Testing forward pass...")
    print(f"   Input shapes: raw_obs{raw_obs.shape}, obj_metrics{obj_metrics.shape}")
    
    action_logits, value_estimates, hidden_state = network(raw_obs, obj_metrics)
    
    print(f"✅ Forward pass successful!")
    print(f"   Action logits shape: {action_logits.shape}")
    print(f"   Value estimates shape: {value_estimates.shape}")
    print(f"   Hidden state shape: {hidden_state.shape}")
    
    # Test single action generation
    print(f"\n🎮 Testing action generation...")
    single_raw_obs = np.random.randn(config.raw_observation_dim)
    single_obj_metrics = np.random.randn(config.objective_metrics_dim)
    
    action, value, new_hidden = network.get_action_and_value(
        single_raw_obs, single_obj_metrics, deterministic=True
    )
    
    print(f"✅ Action generation successful!")
    print(f"   Action: {action}")
    print(f"   Value estimate: {value:.3f}")
    print(f"   New hidden state shape: {new_hidden.shape}")
    
    # Test trainer
    print(f"\n🏋️ Testing trainer...")
    trainer = NumberElevenTrainer(network, config)
    
    # Create dummy batch
    batch_data = {
        'raw_observations': raw_obs,
        'objective_metrics': obj_metrics,
        'target_actions': torch.randn(batch_size, seq_len, config.action_dim).to(config.device),
        'target_values': torch.randn(batch_size, seq_len, 1).to(config.device)
    }
    
    loss_info = trainer.train_step(batch_data)
    print(f"✅ Training step successful!")
    print(f"   Total loss: {loss_info['total_loss']:.4f}")
    print(f"   Action loss: {loss_info['action_loss']:.4f}")
    print(f"   Value loss: {loss_info['value_loss']:.4f}")
    
    print(f"\n🎯 Number Eleven neural network is ready for self-play training!")


if __name__ == "__main__":
    main()
