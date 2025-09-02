"""
Quick Environment Test
=====================

Test basic DerkEnv creation and see what parameters it accepts.
"""

from gym_derk.envs import DerkEnv

def test_derk_env_params():
    """Test DerkEnv creation with different parameters"""
    print("🔍 TESTING DERK ENV PARAMETERS")
    print("=" * 35)
    
    # Test 1: Basic environment
    print("Test 1: Basic DerkEnv")
    try:
        env = DerkEnv()
        print(f"✅ Success with defaults")
        print(f"   n_agents: {env.n_agents}")
        print(f"   action_space: {env.action_space}")
        env.close()
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 2: With arenas and turbo
    print("\nTest 2: DerkEnv with n_arenas=1, turbo_mode=True")
    try:
        env = DerkEnv(n_arenas=1, turbo_mode=True)
        print(f"✅ Success")
        env.close()
    except Exception as e:
        print(f"❌ Failed: {e}")
    
    # Test 3: Check DerkEnv constructor
    print("\nTest 3: DerkEnv constructor signature")
    import inspect
    sig = inspect.signature(DerkEnv.__init__)
    print(f"DerkEnv.__init__ parameters: {list(sig.parameters.keys())}")

if __name__ == "__main__":
    test_derk_env_params()
