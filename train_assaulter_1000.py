"""
Quick Training Session for The Assaulter
=======================================

Train The Assaulter for 1000 iterations using Steam-like interface
"""

from derk_steam_interface import setup_steam_derklings

def main():
    print("🦎 TRAINING THE ASSAULTER - 1000 ITERATIONS")
    print("=" * 50)
    
    # Set up the Steam interface
    game = setup_steam_derklings()
    
    if not game:
        print("❌ Could not set up derklings")
        return
    
    print("Training The Assaulter with his Steam configuration...")
    print("This will create a strong baseline derkling to battle against!")
    
    # Train The Assaulter for 1000 iterations
    results = game.train_derkling("The Assaulter", iterations=1000, opponent_type='random')
    
    if results:
        print(f"\n✅ THE ASSAULTER TRAINING COMPLETE!")
        print(f"Total training iterations: 1000")
        print(f"Ready to battle other derklings!")
        
        # Show final performance
        final_rewards = [r['reward'] for r in results[-100:]]  # Last 100 episodes
        avg_performance = sum(final_rewards) / len(final_rewards)
        print(f"Final average performance: {avg_performance:.2f}")
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. Train other derklings (Spicy Peanut, Engineer, etc.)")
        print(f"2. Battle trained derklings against each other")
        print(f"3. Set up Control Tower for concurrent training")
        print(f"4. Implement advanced training experiments")

if __name__ == "__main__":
    main()
