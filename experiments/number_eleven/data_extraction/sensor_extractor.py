"""
Number Eleven Data Extraction
=============================

Comprehensive data extraction from Derk environment for objective AI training.
This module extracts all available sensor data and game state information
without applying any human bias or interpretation.

Based on gym-derk ObservationKeys from: http://docs.gym.derkgame.com/
"""

import numpy as np
import json
import time
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys, TeamStatsKeys


@dataclass
class ObjectiveMetrics:
    """Objective reward signals - the only labeled data we provide"""
    own_health_percent: float  # 0-100, higher is better
    own_tower_health_percent: float  # 0-100, higher is better  
    enemy_health_percent: float  # 0-100, lower is better
    enemy_tower_health_percent: float  # 0-100, lower is better
    points_scored: float  # Current game points, higher is better
    is_alive: bool  # Critical survival indicator
    game_progress: float  # 0-1, how far through the game


@dataclass  
class RawSensorData:
    """Raw environmental data with no good/bad labels"""
    # Position and movement
    position: Tuple[float, float, float]  # x, y, z coordinates
    velocity: Tuple[float, float, float]  # movement vector
    rotation: float  # facing direction
    
    # Distances (no interpretation of whether close/far is good)
    distance_to_enemies: List[float]  # distance to each enemy
    distance_to_teammates: List[float]  # distance to each teammate
    distance_to_own_tower: float
    distance_to_enemy_tower: float
    distance_to_nearest_cliff: float  # if available
    
    # Environmental status
    is_falling: bool
    is_on_ground: bool
    height_above_ground: float
    
    # Weapon/ability states
    weapon_cooldowns: List[float]  # time until each weapon ready
    ability_states: List[bool]  # which abilities are available
    
    # Teammate information (for dynamic cooperation)
    teammate_positions: List[Tuple[float, float, float]]
    teammate_healths: List[float]
    teammate_alive_status: List[bool]
    
    # Enemy information
    enemy_positions: List[Tuple[float, float, float]]
    enemy_healths: List[float]  # if visible
    enemy_alive_status: List[bool]
    
    # Raw observation vector (everything else)
    raw_observation: np.ndarray  # Full unprocessed observation


@dataclass
class GameState:
    """Complete game state for Number Eleven"""
    agent_id: int
    step_number: int
    timestamp: float
    
    # The only interpreted data - objective metrics
    objectives: ObjectiveMetrics
    
    # Raw sensor data - no interpretation
    sensors: RawSensorData
    
    # Previous action taken (for learning sequences)
    previous_action: Optional[int]


class NumberElevenDataExtractor:
    """Extracts comprehensive data for Number Eleven's training"""
    
    def __init__(self):
        self.game_history: List[GameState] = []
        self.current_episode_data: List[GameState] = []
    
    def extract_game_state(self, observation: np.ndarray, agent_id: int, 
                          step_number: int, previous_action: Optional[int] = None,
                          reward: float = 0.0, info: Optional[Dict] = None) -> GameState:
        """
        Extract complete game state from environment observation.
        
        This is where we separate objective metrics from raw sensor data.
        Only health percentages and scores get labeled as good/bad.
        Everything else is raw data for the AI to interpret.
        """
        
        # Parse the observation array (this will need to be adjusted based on 
        # the actual structure of gym_derk observations)
        obs = observation
        
        # Extract objective metrics (the only labeled data)
        objectives = self._extract_objective_metrics(obs, reward, info or {})
        
        # Extract raw sensor data (no interpretation)
        sensors = self._extract_raw_sensors(obs, info or {})
        
        # Create complete game state
        game_state = GameState(
            agent_id=agent_id,
            step_number=step_number,
            timestamp=time.time(),
            objectives=objectives,
            sensors=sensors,
            previous_action=previous_action
        )
        
        # Store for analysis
        self.current_episode_data.append(game_state)
        
        return game_state
    
    def _extract_objective_metrics(self, obs: np.ndarray, reward: float, 
                                 info: Optional[Dict]) -> ObjectiveMetrics:
        """Extract the objective metrics that define success/failure"""
        
        # Extract health data using actual ObservationKeys
        own_health = obs[ObservationKeys.Hitpoints.value] if len(obs) > ObservationKeys.Hitpoints.value else 1.0
        
        # Get focus target health if available
        focus_health = obs[ObservationKeys.FocusHitpoints.value] if len(obs) > ObservationKeys.FocusHitpoints.value else 1.0
        
        # For tower/statue health, we'll need to use team stats if available
        # For now, use placeholder values - we'll extract from team_stats in actual implementation
        own_tower_health = 1.0  # Will extract from team stats
        enemy_tower_health = 1.0  # Will extract from team stats
        enemy_health = 1.0  # Will calculate from enemy distance/focus data
        
        # Scoring information - use reward as continuous evaluation
        points_scored = reward  # This is our continuous fitness signal
        
        # Survival status
        is_alive = own_health > 0
        
        # Game progress (estimate based on info or use default)
        game_progress = self._calculate_game_progress(info or {})
        
        return ObjectiveMetrics(
            own_health_percent=own_health * 100,
            own_tower_health_percent=own_tower_health * 100,
            enemy_health_percent=enemy_health * 100,
            enemy_tower_health_percent=enemy_tower_health * 100,
            points_scored=points_scored,
            is_alive=is_alive,
            game_progress=game_progress
        )
    
    def _extract_raw_sensors(self, obs: np.ndarray, info: Optional[Dict]) -> RawSensorData:
        """Extract all raw sensor data without interpretation using actual ObservationKeys"""
        
        # Position and spatial awareness using actual observation indices
        position_lr = obs[ObservationKeys.PositionLeftRight.value] if len(obs) > ObservationKeys.PositionLeftRight.value else 0.0
        position_ud = obs[ObservationKeys.PositionUpDown.value] if len(obs) > ObservationKeys.PositionUpDown.value else 0.0
        position = (position_lr, position_ud, 0.0)  # 2D game, so z=0
        
        # Height information (for cliff detection)
        height_front1 = obs[ObservationKeys.HeightFront1.value] if len(obs) > ObservationKeys.HeightFront1.value else 0.0
        height_front5 = obs[ObservationKeys.HeightFront5.value] if len(obs) > ObservationKeys.HeightFront5.value else 0.0
        height_back2 = obs[ObservationKeys.HeightBack2.value] if len(obs) > ObservationKeys.HeightBack2.value else 0.0
        
        # Movement state
        is_stuck = obs[ObservationKeys.Stuck.value] if len(obs) > ObservationKeys.Stuck.value else False
        velocity = (0.0, 0.0, 0.0)  # Not directly available, but we can calculate from position changes
        rotation = 0.0  # Not directly available in observations
        
        # Distance calculations using actual observation data
        friend_statue_distance = obs[ObservationKeys.FriendStatueDistance.value] if len(obs) > ObservationKeys.FriendStatueDistance.value else 0.0
        enemy_statue_distance = obs[ObservationKeys.EnemyStatueDistance.value] if len(obs) > ObservationKeys.EnemyStatueDistance.value else 0.0
        
        friend1_distance = obs[ObservationKeys.Friend1Distance.value] if len(obs) > ObservationKeys.Friend1Distance.value else 0.0
        friend2_distance = obs[ObservationKeys.Friend2Distance.value] if len(obs) > ObservationKeys.Friend2Distance.value else 0.0
        
        enemy1_distance = obs[ObservationKeys.Enemy1Distance.value] if len(obs) > ObservationKeys.Enemy1Distance.value else 0.0
        enemy2_distance = obs[ObservationKeys.Enemy2Distance.value] if len(obs) > ObservationKeys.Enemy2Distance.value else 0.0
        enemy3_distance = obs[ObservationKeys.Enemy3Distance.value] if len(obs) > ObservationKeys.Enemy3Distance.value else 0.0
        
        # Angle information for spatial awareness
        friend_statue_angle = obs[ObservationKeys.FriendStatueAngle.value] if len(obs) > ObservationKeys.FriendStatueAngle.value else 0.0
        enemy_statue_angle = obs[ObservationKeys.EnemyStatueAngle.value] if len(obs) > ObservationKeys.EnemyStatueAngle.value else 0.0
        
        # Weapon and ability states
        ability0_ready = obs[ObservationKeys.Ability0Ready.value] if len(obs) > ObservationKeys.Ability0Ready.value else False
        ability1_ready = obs[ObservationKeys.Ability1Ready.value] if len(obs) > ObservationKeys.Ability1Ready.value else False
        ability2_ready = obs[ObservationKeys.Ability2Ready.value] if len(obs) > ObservationKeys.Ability2Ready.value else False
        
        # Focus target information (what we're currently targeting)
        has_focus = obs[ObservationKeys.HasFocus.value] if len(obs) > ObservationKeys.HasFocus.value else False
        focus_relative_rotation = obs[ObservationKeys.FocusRelativeRotation.value] if len(obs) > ObservationKeys.FocusRelativeRotation.value else 0.0
        focus_facing_us = obs[ObservationKeys.FocusFacingUs.value] if len(obs) > ObservationKeys.FocusFacingUs.value else False
        focus_focusing_back = obs[ObservationKeys.FocusFocusingBack.value] if len(obs) > ObservationKeys.FocusFocusingBack.value else False
        focus_hitpoints = obs[ObservationKeys.FocusHitpoints.value] if len(obs) > ObservationKeys.FocusHitpoints.value else 0.0
        focus_dazed = obs[ObservationKeys.FocusDazed.value] if len(obs) > ObservationKeys.FocusDazed.value else False
        focus_crippled = obs[ObservationKeys.FocusCrippled.value] if len(obs) > ObservationKeys.FocusCrippled.value else False
        
        # Equipment information (what we have equipped)
        equipment_states = {
            'has_talons': obs[ObservationKeys.HasTalons.value] if len(obs) > ObservationKeys.HasTalons.value else False,
            'has_blood_claws': obs[ObservationKeys.HasBloodClaws.value] if len(obs) > ObservationKeys.HasBloodClaws.value else False,
            'has_cleavers': obs[ObservationKeys.HasCleavers.value] if len(obs) > ObservationKeys.HasCleavers.value else False,
            'has_pistol': obs[ObservationKeys.HasPistol.value] if len(obs) > ObservationKeys.HasPistol.value else False,
            'has_magnum': obs[ObservationKeys.HasMagnum.value] if len(obs) > ObservationKeys.HasMagnum.value else False,
            'has_blaster': obs[ObservationKeys.HasBlaster.value] if len(obs) > ObservationKeys.HasBlaster.value else False,
            'has_healing_gland': obs[ObservationKeys.HasHealingGland.value] if len(obs) > ObservationKeys.HasHealingGland.value else False,
            'has_vampire_gland': obs[ObservationKeys.HasVampireGland.value] if len(obs) > ObservationKeys.HasVampireGland.value else False,
            'has_frog_legs': obs[ObservationKeys.HasFrogLegs.value] if len(obs) > ObservationKeys.HasFrogLegs.value else False,
            'has_shell': obs[ObservationKeys.HasShell.value] if len(obs) > ObservationKeys.HasShell.value else False,
            'has_trombone': obs[ObservationKeys.HasTrombone.value] if len(obs) > ObservationKeys.HasTrombone.value else False,
        }
        
        focus_equipment_states = {
            'focus_has_talons': obs[ObservationKeys.FocusHasTalons.value] if len(obs) > ObservationKeys.FocusHasTalons.value else False,
            'focus_has_blood_claws': obs[ObservationKeys.FocusHasBloodClaws.value] if len(obs) > ObservationKeys.FocusHasBloodClaws.value else False,
            'focus_has_cleavers': obs[ObservationKeys.FocusHasCleavers.value] if len(obs) > ObservationKeys.FocusHasCleavers.value else False,
        }
        
        return RawSensorData(
            position=position,
            velocity=velocity,
            rotation=rotation,
            distance_to_enemies=[enemy1_distance, enemy2_distance, enemy3_distance],
            distance_to_teammates=[friend1_distance, friend2_distance],
            distance_to_own_tower=friend_statue_distance,
            distance_to_enemy_tower=enemy_statue_distance,
            distance_to_nearest_cliff=min(height_front1, height_front5, height_back2),
            is_falling=False,  # Not directly available
            is_on_ground=not is_stuck,  # Approximation
            height_above_ground=max(height_front1, height_front5, height_back2),
            weapon_cooldowns=[1.0 - ability0_ready, 1.0 - ability1_ready, 1.0 - ability2_ready],
            ability_states=[ability0_ready, ability1_ready, ability2_ready],
            teammate_positions=[(0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],  # Not directly available
            teammate_healths=[1.0, 1.0],  # Not directly available
            teammate_alive_status=[True, True],  # Not directly available
            enemy_positions=[(0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)],  # Not directly available
            enemy_healths=[focus_hitpoints if has_focus else 1.0, 1.0, 1.0],  # Only focus target known
            enemy_alive_status=[True, True, True],  # Assume alive unless known otherwise
            raw_observation=obs
        )
    
    # Helper methods for data extraction
    def _safe_extract(self, obs: np.ndarray, key: str, default: Any) -> Any:
        """Safely extract data with fallback to default"""
        # This will be implemented once we understand the observation structure
        # For now, return defaults
        return default
    
    def _safe_extract_vector(self, obs: np.ndarray, key: str, 
                           default: Tuple) -> Tuple:
        """Safely extract vector data"""
        return default
    
    def _calculate_enemy_distances(self, obs: np.ndarray) -> List[float]:
        """Calculate distances to all enemies"""
        # Placeholder - implement based on observation structure
        return [10.0, 15.0, 20.0]  # Example distances
    
    def _calculate_teammate_distances(self, obs: np.ndarray) -> List[float]:
        """Calculate distances to all teammates"""
        return [5.0, 8.0]  # Example distances
    
    def _calculate_tower_distance(self, obs: np.ndarray, tower_type: str) -> float:
        """Calculate distance to tower"""
        return 25.0  # Example distance
    
    def _calculate_cliff_distance(self, obs: np.ndarray) -> float:
        """Calculate distance to nearest cliff/edge"""
        return 50.0  # Example distance
    
    def _extract_weapon_cooldowns(self, obs: np.ndarray) -> List[float]:
        """Extract weapon cooldown timers"""
        return [0.0, 2.5, 1.0]  # Example cooldowns
    
    def _extract_ability_states(self, obs: np.ndarray) -> List[bool]:
        """Extract ability availability states"""
        return [True, False, True]  # Example states
    
    def _extract_teammate_positions(self, obs: np.ndarray) -> List[Tuple[float, float, float]]:
        """Extract all teammate positions"""
        return [(10.0, 5.0, 0.0), (15.0, 8.0, 0.0)]  # Example positions
    
    def _extract_teammate_healths(self, obs: np.ndarray) -> List[float]:
        """Extract teammate health percentages"""
        return [0.8, 0.6]  # Example healths
    
    def _extract_teammate_status(self, obs: np.ndarray) -> List[bool]:
        """Extract teammate alive/dead status"""
        return [True, True]  # Example status
    
    def _extract_enemy_positions(self, obs: np.ndarray) -> List[Tuple[float, float, float]]:
        """Extract enemy positions if visible"""
        return [(30.0, 20.0, 0.0), (35.0, 25.0, 0.0), (40.0, 30.0, 0.0)]
    
    def _extract_enemy_healths(self, obs: np.ndarray) -> List[float]:
        """Extract enemy health if visible"""
        return [0.9, 0.7, 0.5]  # Example healths
    
    def _extract_enemy_status(self, obs: np.ndarray) -> List[bool]:
        """Extract enemy alive/dead status"""
        return [True, True, False]  # Example status
    
    def _calculate_game_progress(self, info: Optional[Dict]) -> float:
        """Calculate how far through the game we are (0-1)"""
        # This could be based on time, score, or other game state
        return 0.5  # Example progress
    
    def start_new_episode(self):
        """Start tracking a new episode"""
        if self.current_episode_data:
            self.game_history.extend(self.current_episode_data)
        self.current_episode_data = []
    
    def get_episode_data(self) -> List[GameState]:
        """Get current episode data"""
        return self.current_episode_data.copy()
    
    def save_episode_data(self, filename: str):
        """Save episode data to file for analysis"""
        episode_data = {
            'episode_length': len(self.current_episode_data),
            'states': [asdict(state) for state in self.current_episode_data]
        }
        
        with open(filename, 'w') as f:
            json.dump(episode_data, f, indent=2, default=str)
    
    def analyze_observation_structure(self, env: DerkEnv):
        """
        Analyze the actual structure of gym_derk observations
        to properly map data extraction methods.
        """
        print("🔍 Analyzing Derk Environment Observation Structure")
        print("=" * 55)
        
        # Reset environment to get sample observations
        obs_n = env.reset()
        
        if obs_n is not None and len(obs_n) > 0:
            sample_obs = obs_n[0]
            print(f"📊 Observation shape: {sample_obs.shape}")
            print(f"📊 Observation type: {type(sample_obs)}")
            print(f"📊 Value range: [{sample_obs.min():.3f}, {sample_obs.max():.3f}]")
            
            # Print first few values to understand structure
            print(f"📊 First 20 values: {sample_obs[:20]}")
            
            # This is where we'll map the observation indices to actual data
            print("\n🎯 Observation mapping needed:")
            print("   - Identify health indices")
            print("   - Identify position indices") 
            print("   - Identify distance indices")
            print("   - Identify weapon/ability indices")
            print("   - Identify teammate/enemy indices")
            
        else:
            print("❌ Could not get sample observations")
        
        return obs_n


def main():
    """Test the data extraction system"""
    print("🤖 Number Eleven Data Extraction Test")
    print("=" * 40)
    
    # Create extractor
    extractor = NumberElevenDataExtractor()
    
    # Create environment to analyze structure
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    
    try:
        # Analyze observation structure
        obs_n = extractor.analyze_observation_structure(env)
        
        if obs_n is not None:
            # Test data extraction
            print("\n🧪 Testing data extraction...")
            
            sample_obs = obs_n[0]
            game_state = extractor.extract_game_state(
                observation=sample_obs,
                agent_id=0,
                step_number=1,
                previous_action=None,
                reward=0.0,
                info={}
            )
            
            print(f"✅ Successfully extracted game state:")
            print(f"   🎯 Objectives: Health={game_state.objectives.own_health_percent:.1f}%")
            print(f"   📡 Sensors: Position={game_state.sensors.position}")
            print(f"   📡 Raw observation size: {len(game_state.sensors.raw_observation)}")
            
            # Save sample data
            extractor.save_episode_data("sample_number_eleven_data.json")
            print(f"💾 Sample data saved to: sample_number_eleven_data.json")
        
    finally:
        env.close()
        print(f"🏁 Environment closed")


if __name__ == "__main__":
    import time
    main()
