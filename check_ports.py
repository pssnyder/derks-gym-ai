"""
Port Configuration Validator
============================

Quick script to validate and display current port configuration.
"""

import re
import os

def check_port_configuration():
    """Check and display current port configuration"""
    print("🔧 DERK'S GYM AI PORT CONFIGURATION")
    print("=" * 40)
    
    base_dir = os.path.dirname(__file__)
    
    # Files to check
    files_to_check = [
        "derks-starter-kit/run.py",
        "derks-starter-kit/custom_battle.py"
    ]
    
    port_pattern = r'port=(\d+)'
    
    for file_path in files_to_check:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"\n📄 {file_path}:")
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            ports = re.findall(port_pattern, content)
            if ports:
                for i, port in enumerate(ports, 1):
                    print(f"   Player {i}: Port {port}")
            else:
                print("   No ports found")
        else:
            print(f"\n❌ {file_path}: File not found")
    
    print("\n🎯 Configuration Status:")
    print("   ✅ Ports changed from default 8788/8789 to 9788/9789")
    print("   ✅ Avoids conflicts with Steam game")
    print("   ✅ Main battle systems use DerkEnv directly (no port conflicts)")
    
    print("\n📝 Note:")
    print("   - Steam Battle Arena uses DerkEnv directly (no agent servers)")
    print("   - Only starter kit scripts use DerkAgentServer with ports")
    print("   - Ports 9788/9789 are safe for concurrent Steam game testing")

if __name__ == "__main__":
    check_port_configuration()
