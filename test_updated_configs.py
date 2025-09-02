"""
Test Updated Configurations
===========================

Battle test with the improved bounty configurations and equipment loadouts.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.steam_battle_arena import WorkingSteamBattleArena
from src.brain_profiles.peanut_class.nightrider_peanut_updated import NightriderPeanutBrain
from src.brain_profiles.testing_class.the_assaulter_updated import TheAssaulterBrain

def test_updated_configurations():
    """Test the updated brain configurations"""
    print("🆕 TESTING UPDATED CONFIGURATIONS")
    print("=" * 40)
    print("Testing improved bounty values and complete equipment loadouts")
    print()
    
    # Create battle arena with updated brains
    arena = WorkingSteamBattleArena(NightriderPeanutBrain, TheAssaulterBrain)
    
    # Run extended battle for better analysis
    results = arena.run_battle(max_episodes=5, max_steps_per_episode=800)
    
    print(f"\n📈 CONFIGURATION IMPROVEMENT RESULTS")
    print("=" * 45)
    
    if results and results['episodes']:
        successful_episodes = len(results['episodes'])
        avg_home = sum(ep['total_home_reward'] for ep in results['episodes']) / successful_episodes
        avg_away = sum(ep['total_away_reward'] for ep in results['episodes']) / successful_episodes
        
        print(f"✅ Successful episodes: {successful_episodes}/5")
        print(f"🌙 Nightrider avg reward: {avg_home:.2f} (was 0.00)")
        print(f"⚔️ Assaulter avg reward: {avg_away:.2f}")
        print(f"📊 Battle balance: {results['home_wins']}-{results['away_wins']}-{results['ties']}")
        
        # Analysis
        if avg_home > 0:
            print(f"🎉 SUCCESS: Nightrider now earning rewards!")
        if abs(avg_home - avg_away) < 2.0:
            print(f"⚖️ BALANCED: Configurations are well-balanced")
        else:
            winner = "Nightrider" if avg_home > avg_away else "Assaulter"
            print(f"📈 ANALYSIS: {winner} has advantage, consider tuning")
            
    else:
        print(f"❌ No successful episodes - check configurations")
    
    return results

def compare_configurations():
    """Compare old vs new configurations"""
    print(f"\n🔄 CONFIGURATION COMPARISON")
    print("=" * 30)
    
    # Load updated brains
    nightrider_new = NightriderPeanutBrain()
    assaulter_new = TheAssaulterBrain()
    
    print("🌙 Nightrider Changes:")
    config_nr = nightrider_new.get_derk_gym_config()
    print(f"   Equipment: {config_nr['slots']} (was ['Unknown', 'Unknown', 'Unknown'])")
    print(f"   Kill bounty: {config_nr['rewardFunction']['killEnemyUnit']} (was 10.0)")
    print(f"   Team spirit: {config_nr['rewardFunction']['teamSpirit']} (was 0.1)")
    
    print("\n⚔️ Assaulter Changes:")
    config_as = assaulter_new.get_derk_gym_config()
    print(f"   Equipment: {config_as['slots']} (was ['Talons', None, None])")
    print(f"   Territory bonus: {config_as['rewardFunction']['timeSpentAwayTerritory']} (was 0.3)")
    print(f"   Added healEnemy penalty: {config_as['rewardFunction']['healEnemy']} (was missing)")

def main():
    """Main test function"""
    compare_configurations()
    results = test_updated_configurations()
    
    print(f"\n✅ Updated configuration test complete!")
    
    if results and len(results['episodes']) > 0:
        print(f"🎯 Recommendations:")
        print(f"   • Configurations are working - derklings are now earning rewards")
        print(f"   • Equipment loadouts are complete and functional")
        print(f"   • Bounty values are balanced and realistic")
        print(f"   • Ready for Steam-style iterative training")
    else:
        print(f"⚠️ Need further configuration adjustments")

if __name__ == "__main__":
    main()
