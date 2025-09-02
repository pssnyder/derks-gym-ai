"""
Custom Derk Battle Runner
========================

Modified version of the starter kit that uses our custom brain configurations
for persistent derkling equipment, colors, and reward functions.
"""

from argparse import ArgumentParser
import importlib

import asyncio
from gym_derk import DerkSession, DerkAgentServer, DerkAppInstance


async def run_player(env: DerkSession, DerkPlayerClass):
    """
    Runs a DerkPlayer
    """
    player = DerkPlayerClass(env.n_agents, env.action_space)
    obs = await env.reset()
    player.signal_env_reset(obs)
    ordi = await env.step()

    while not env.done:
        actions = player.take_action(ordi)
        ordi = await env.step(actions)


async def main(p1, p2, n, turbo):
    """
    Runs the game in n arenas between p1 and p2 using their custom configurations
    """
    print("🏟️ CUSTOM DERK BATTLE")
    print("=" * 30)
    
    # Create player instances to get their configurations
    temp_p1 = p1(3, None)  # Temporary instance to get config
    temp_p2 = p2(3, None)  # Temporary instance to get config
    
    # Get team configurations if available
    p1_config = None
    p2_config = None
    p1_reward_func = None
    p2_reward_func = None
    
    if hasattr(temp_p1, 'get_derk_gym_config'):
        p1_config = temp_p1.get_derk_gym_config()
        p1_reward_func = p1_config.get('rewardFunction')
        print(f"🏠 Home Team ({temp_p1.name}):")
        print(f"   Equipment: {p1_config.get('slots', 'Default')}")
        print(f"   Colors: {p1_config.get('primaryColor', 'Default')} / {p1_config.get('secondaryColor', 'Default')}")
        print(f"   Team Spirit: {p1_reward_func.get('teamSpirit', 0.5) if p1_reward_func else 'Default'}")
    
    if hasattr(temp_p2, 'get_derk_gym_config'):
        p2_config = temp_p2.get_derk_gym_config()
        p2_reward_func = p2_config.get('rewardFunction')
        print(f"🏃 Away Team ({temp_p2.name}):")
        print(f"   Equipment: {p2_config.get('slots', 'Default')}")
        print(f"   Colors: {p2_config.get('primaryColor', 'Default')} / {p2_config.get('secondaryColor', 'Default')}")
        print(f"   Team Spirit: {p2_reward_func.get('teamSpirit', 0.5) if p2_reward_func else 'Default'}")
    
    # Use custom reward function if available, otherwise use balanced defaults
    if p1_reward_func:
        reward_function = p1_reward_func
        print(f"\n🎯 Using {temp_p1.name} reward function")
    elif p2_reward_func:
        reward_function = p2_reward_func
        print(f"\n🎯 Using {temp_p2.name} reward function")
    else:
        reward_function = {
            "damageEnemyStatue": 4,
            "damageEnemyUnit": 2,
            "killEnemyStatue": 4,
            "killEnemyUnit": 2,
            "healFriendlyStatue": 1,
            "healTeammate1": 2,
            "healTeammate2": 2,
            "damageTaken": -1,
            "friendlyFire": -1,
            "healEnemy": -1,
            "fallDamageTaken": -10,
            "victory": 100,
            "loss": -100,
            "tie": 0,
            "teamSpirit": 0.5,
            "timeScaling": 0.8,
        }
        print(f"\n🎯 Using default reward function")
    
    print()
    
    # Create agent servers
    agent_p1 = DerkAgentServer(run_player, args={"DerkPlayerClass": p1}, port=9788)
    agent_p2 = DerkAgentServer(run_player, args={"DerkPlayerClass": p2}, port=9789)

    await agent_p1.start()
    await agent_p2.start()

    app = DerkAppInstance()
    await app.start()

    # Set up team configurations for persistent equipment/colors
    session_config = {
        "n_arenas": n,
        "turbo_mode": turbo,
        "agent_hosts": [
            {"uri": agent_p1.uri, "regions": [{"sides": "home"}]},
            {"uri": agent_p2.uri, "regions": [{"sides": "away"}]},
        ],
        "reward_function": reward_function,
    }
    
    # Add team configurations if available
    if p1_config or p2_config:
        home_team = []
        away_team = []
        
        # Build home team config (3 agents)
        for i in range(3):
            if p1_config:
                agent_config = {
                    "primaryColor": p1_config.get("primaryColor", "#4CAF50"),
                    "secondaryColor": p1_config.get("secondaryColor", "#2E7D32"),
                    "slots": p1_config.get("slots", [None, None, None])
                }
            else:
                agent_config = {}
            home_team.append(agent_config)
        
        # Build away team config (3 agents)
        for i in range(3):
            if p2_config:
                agent_config = {
                    "primaryColor": p2_config.get("primaryColor", "#DC143C"),
                    "secondaryColor": p2_config.get("secondaryColor", "#000000"),
                    "slots": p2_config.get("slots", [None, None, None])
                }
            else:
                agent_config = {}
            away_team.append(agent_config)
        
        session_config["home_team"] = home_team
        session_config["away_team"] = away_team
        
        print("🔧 Team configurations applied for persistent equipment and colors")

    await app.run_session(**session_config)
    await app.print_team_stats()


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument(
        "-p1",
        help="Path to player1 module relative to agent. Defaults to `bot`",
        type=str,
        default="bot",
    )
    p.add_argument(
        "-p2",
        help="Path to player2 module relative to agent. Defaults to `bot`",
        type=str,
        default="bot",
    )
    p.add_argument(
        "-n",
        help="Number of arenas to run, Defaults to 2",
        type=int,
        default=2,
    )
    p.add_argument(
        "--fast",
        help="To enable turbo mode or not. Defaults to False",
        action="store_true",
    )

    args = p.parse_args()
    player1 = importlib.import_module(f"agent.{args.p1}").DerkPlayer
    player2 = importlib.import_module(f"agent.{args.p2}").DerkPlayer

    asyncio.get_event_loop().run_until_complete(
        main(player1, player2, args.n, args.fast)
    )
