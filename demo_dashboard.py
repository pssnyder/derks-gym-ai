"""
Quick Web Dashboard Demo
========================

Launch the web dashboard and show key features.
"""

import sys
import os
import webbrowser
import time
from threading import Timer

# Add paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'web_dashboard'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def launch_dashboard():
    """Launch the web dashboard and open browser"""
    print("🤖 DERK'S GYM AI WEB DASHBOARD")
    print("=" * 35)
    print()
    
    try:
        from web_dashboard.app import app
        
        # Test that data loads correctly
        with app.test_client() as client:
            response = client.get('/api/derklings')
            derklings = response.get_json() if response.status_code == 200 else {}
            
            response = client.get('/api/teams')
            teams = response.get_json() if response.status_code == 200 else {}
            
        print(f"📊 Dashboard Features:")
        print(f"   - {len(derklings)} Derkling Profiles")
        print(f"   - {len(teams)} Active Teams")
        print(f"   - Fighter Bonds & Compatibility")
        print(f"   - Project Number Eleven (Special)")
        print(f"   - Battle Metrics & Analytics")
        print()
        
        print("🚀 Starting web server...")
        print("   URL: http://localhost:5000")
        print("   Press Ctrl+C to stop")
        print()
        
        # Open browser after a short delay
        Timer(2.0, lambda: webbrowser.open('http://localhost:5000')).start()
        
        # Start Flask app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please ensure Flask is installed: pip install flask")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    launch_dashboard()
