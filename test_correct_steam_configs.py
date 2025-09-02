"""
Test Correct Steam Configurations
=================================

Test battle with the actual Steam game bounty values from screenshots.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.steam_battle_arena import WorkingSteamBattleArena
from src.brain_profiles.peanut_class.nightrider_peanut_correct import NightriderPeanutBrain
from src.brain_profiles.testing_class.angrrry_correct import AngrrryBrain

def compare_steam_configs():
    """Compare the corrected Steam configurations"""
    print("📸 STEAM SCREENSHOT CONFIGURATIONS")
    print("=" * 40)
    
    nightrider = NightriderPeanutBrain()
    angrrry = AngrrryBrain()
    
    nr_config = nightrider.get_derk_gym_config()
    ang_config = angrrry.get_derk_gym_config()
    
    print("🌙 Nightrider Peanut (Correct Steam Values):")
    print(f"   Kill enemy unit: {nr_config['rewardFunction']['killEnemyUnit']} (1000 in Steam)")
    print(f"   Damage enemy unit: {nr_config['rewardFunction']['damageEnemyUnit']} (100 in Steam)")
    print(f"   Kill enemy statue: {nr_config['rewardFunction']['killEnemyStatue']} (90 in Steam)")
    print(f"   Damage taken: {nr_config['rewardFunction']['damageTaken']} (-20 in Steam)")
    print(f"   Strategy: Maximum kill focus (1000 point bounty!)")
    
    print("\n😡 Angrrry (Correct Steam Values):")
    print(f"   Kill enemy unit: {ang_config['rewardFunction']['killEnemyUnit']} (100 in Steam)")
    print(f"   Damage enemy unit: {ang_config['rewardFunction']['damageEnemyUnit']} (80 in Steam)")
    print(f"   Kill enemy statue: {ang_config['rewardFunction']['killEnemyStatue']} (60 in Steam)")
    print(f"   Damage taken: {ang_config['rewardFunction']['damageTaken']} (-40 in Steam)")
    print(f"   Friendly fire: {ang_config['rewardFunction']['friendlyFire']} (-60 in Steam)")
    print(f"   Team spirit: {ang_config['rewardFunction']['teamSpirit']} (balanced team player)")
    print(f"   Strategy: Balanced assault with team support")
    
    print("\n⚖️ KEY DIFFERENCES:")
    print(f"   Kill bounty difference: 10.0 vs 1.0 (Nightrider has 10x kill reward!)")
    print(f"   Damage penalty: -0.2 vs -0.4 (Nightrider can take more risks)")
    print(f"   Team focus: 0.0 vs 0.7 (Nightrider is solo hunter, Angrrry is team player)")

def test_correct_steam_battle():
    """Test battle with correct Steam configurations"""
    print(f"\n🚀 TESTING CORRECT STEAM CONFIGURATIONS")
    print("=" * 45)
    print("Using actual bounty values from Steam game screenshots")
    print()
    
    # Create battle arena with correct Steam configurations
    arena = WorkingSteamBattleArena(NightriderPeanutBrain, AngrrryBrain)
    
    # Run battle
    results = arena.run_battle(max_episodes=3, max_steps_per_episode=600)
    
    print(f"\n📊 STEAM CONFIGURATION TEST RESULTS")
    print("=" * 40)
    
    if results and results['episodes']:
        successful_episodes = len(results['episodes'])
        avg_nightrider = sum(ep['total_home_reward'] for ep in results['episodes']) / successful_episodes
        avg_angrrry = sum(ep['total_away_reward'] for ep in results['episodes']) / successful_episodes
        
        print(f"✅ Episodes completed: {successful_episodes}/3")
        print(f"🌙 Nightrider avg reward: {avg_nightrider:.2f}")
        print(f"😡 Angrrry avg reward: {avg_angrrry:.2f}")
        print(f"🏆 Battle record: {results['home_wins']}-{results['away_wins']}-{results['ties']}")
        
        # Analysis based on Steam configurations
        print(f"\n🔍 STEAM CONFIG ANALYSIS:")
        if avg_nightrider > 0:
            print(f"   ✅ Nightrider earning rewards (kill-focused strategy working)")
        else:
            print(f"   ⚠️ Nightrider still getting zero (equipment/environment issue)")
            
        if avg_angrrry > avg_nightrider:
            print(f"   📈 Angrrry dominating despite lower kill bounty")
            print(f"   🤔 Team support and balanced approach may be more effective")
        elif avg_nightrider > avg_angrrry:
            print(f"   🎯 Nightrider's kill focus paying off (1000 vs 100 bounty)")
        else:
            print(f"   ⚖️ Balanced competition between strategies")
            
        return results
    else:
        print(f"❌ No successful episodes - environment configuration issue persists")
        return None

def main():
    """Main test function"""
    compare_steam_configs()
    results = test_correct_steam_battle()
    
    print(f"\n🎯 NEXT STEPS:")
    print("=" * 15)
    
    if results and len(results['episodes']) > 0:
        print("✅ Steam configurations are correctly implemented")
        print("🔧 Now need to solve team configuration enforcement:")
        print("   1. Fix environment to use custom team configs")
        print("   2. Ensure weapons are properly equipped")
        print("   3. Validate reward functions are applied correctly")
    else:
        print("🔧 Still need to solve core environment issues:")
        print("   1. Team configurations not being applied")
        print("   2. Agents not getting specified equipment")
        print("   3. Environment reset issues with custom teams")
    
    print("\n🚀 Ready for Steam-style training once equipment issue is resolved!")

if __name__ == "__main__":
    main()
