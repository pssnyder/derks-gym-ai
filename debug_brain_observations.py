"""
Debug Brain Observations
=======================

Check what observations the Safe T Peanut brain is receiving to understand
why it's making specific decisions.
"""

import numpy as np
from gym_derk.envs import DerkEnv
from gym_derk import ObservationKeys
from brain_profiles.peanut_class.safe_t_peanut import SafeTPeanutBrain

def debug_brain_observations():
    """Debug what observations the brain is receiving"""
    print("🔍 DEBUGGING BRAIN OBSERVATIONS")
    print("=" * 40)
    
    # Create environment
    env = DerkEnv(n_arenas=1, turbo_mode=True)
    observation_n = env.reset()
    
    # Create brain
    brain = SafeTPeanutBrain()
    
    print(f"🧬 Safe T Peanut Brain Parameters:")
    print(f"   statue_protection_range: {brain.statue_protection_range}")
    print(f"   engagement_range: {brain.engagement_range}")
    print(f"   team_support_range: {brain.team_support_range}")
    print(f"   retreat_health_threshold: {brain.retreat_health_threshold}")
    print(f"   aggression: {brain.aggression}")
    
    # Check first agent's observations
    obs = observation_n[0]
    
    print(f"\n📊 Agent 0 Observations:")
    print(f"   Observation length: {len(obs)}")
    
    # Extract key values
    hp = obs[ObservationKeys.Hitpoints.value]
    has_focus = obs[ObservationKeys.HasFocus.value]
    focus_hp = obs[ObservationKeys.FocusHitpoints.value] if has_focus else 0
    
    friendly_statue_dist = obs[ObservationKeys.FriendStatueDistance.value]
    enemy_statue_dist = obs[ObservationKeys.EnemyStatueDistance.value]
    
    enemy_distances = [
        obs[ObservationKeys.Enemy1Distance.value],
        obs[ObservationKeys.Enemy2Distance.value], 
        obs[ObservationKeys.Enemy3Distance.value]
    ]
    valid_enemies = [d for d in enemy_distances if d > 0]
    closest_enemy = min(valid_enemies) if valid_enemies else 999
    
    friend_distances = [
        obs[ObservationKeys.Friend1Distance.value],
        obs[ObservationKeys.Friend2Distance.value]
    ]
    valid_friends = [d for d in friend_distances if d > 0]
    closest_friend = min(valid_friends) if valid_friends else 999
    
    print(f"\n🏥 Health Status:")
    print(f"   HP: {hp}")
    print(f"   Has focus: {has_focus}")
    print(f"   Focus HP: {focus_hp}")
    
    print(f"\n🏛️ Statue Distances:")
    print(f"   Friendly statue: {friendly_statue_dist}")
    print(f"   Enemy statue: {enemy_statue_dist}")
    
    print(f"\n👥 Entity Distances:")
    print(f"   Enemy distances: {enemy_distances}")
    print(f"   Valid enemies: {valid_enemies}")
    print(f"   Closest enemy: {closest_enemy}")
    print(f"   Friend distances: {friend_distances}")
    print(f"   Valid friends: {valid_friends}")
    print(f"   Closest friend: {closest_friend}")
    
    # Test brain decision making
    print(f"\n🧠 Brain Decision Analysis:")
    
    # Manually check each priority condition
    print(f"\n   PRIORITY 1 - STATUE PROTECTION:")
    statue_threat = closest_enemy < brain.statue_protection_range and friendly_statue_dist < 30
    print(f"     closest_enemy < statue_protection_range: {closest_enemy} < {brain.statue_protection_range} = {closest_enemy < brain.statue_protection_range}")
    print(f"     friendly_statue_dist < 30: {friendly_statue_dist} < 30 = {friendly_statue_dist < 30}")
    print(f"     Both conditions met: {statue_threat}")
    
    print(f"\n   PRIORITY 2 - HEALTH MANAGEMENT:")
    should_retreat = hp < brain.retreat_health_threshold
    print(f"     hp < retreat_threshold: {hp} < {brain.retreat_health_threshold} = {should_retreat}")
    
    print(f"\n   PRIORITY 3 - TEAM SUPPORT:")
    team_support = closest_friend < brain.team_support_range and brain.has_healing_gland
    print(f"     closest_friend < support_range: {closest_friend} < {brain.team_support_range} = {closest_friend < brain.team_support_range}")
    print(f"     has_healing_gland: {brain.has_healing_gland}")
    print(f"     Both conditions met: {team_support}")
    
    print(f"\n   PRIORITY 4 - COMBAT ENGAGEMENT:")
    health_ratio = hp / 100.0
    can_engage = closest_enemy < brain.engagement_range and health_ratio > 0.6
    print(f"     closest_enemy < engagement_range: {closest_enemy} < {brain.engagement_range} = {closest_enemy < brain.engagement_range}")
    print(f"     health_ratio > 0.6: {health_ratio} > 0.6 = {health_ratio > 0.6}")
    print(f"     Both conditions met: {can_engage}")
    
    print(f"\n   PRIORITY 5 - DEFENSIVE POSITIONING:")
    needs_repositioning = friendly_statue_dist > 25
    print(f"     friendly_statue_dist > 25: {friendly_statue_dist} > 25 = {needs_repositioning}")
    
    # Get actual action
    action = brain.get_action(obs)
    move_x, rotate, chase_focus, cast_slot, focus_target = action
    
    print(f"\n⚡ Final Action:")
    print(f"     move_x: {move_x}")
    print(f"     rotate: {rotate}")
    print(f"     chase_focus: {chase_focus}")
    print(f"     cast_slot: {cast_slot}")
    print(f"     focus_target: {focus_target}")
    
    # Test if actions have any effect after a few steps
    print(f"\n🎮 Testing Action Effects:")
    
    # Create actions for all agents
    actions = []
    for i in range(6):
        if i < 3:
            # Home team uses Safe T Peanut
            agent_action = brain.get_action(observation_n[i])
        else:
            # Away team uses random actions
            agent_action = env.action_space.sample()
        actions.append(agent_action)
    
    # Run a few steps
    for step in range(5):
        new_obs, rewards, dones, info = env.step(np.array(actions))
        
        # Check if positions or states changed
        new_hp = new_obs[0][ObservationKeys.Hitpoints.value]
        new_friendly_dist = new_obs[0][ObservationKeys.FriendStatueDistance.value]
        new_enemy_dist = new_obs[0][ObservationKeys.EnemyStatueDistance.value]
        
        print(f"   Step {step}: HP {hp}->{new_hp}, Friend statue {friendly_statue_dist:.1f}->{new_friendly_dist:.1f}, Rewards: {rewards[:3]}")
        
        # Update for next iteration
        observation_n = new_obs
        hp = new_hp
        friendly_statue_dist = new_friendly_dist
        
        if all(dones):
            break
    
    env.close()

if __name__ == "__main__":
    debug_brain_observations()
