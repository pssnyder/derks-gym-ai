"""
Training Control Tower
=====================

Advanced training control system for managing multiple concurrent 
training sessions, monitoring progress, and controlling experiments.

This replaces the Steam game's limitation of one training at a time.
"""

import threading
import time
import json
import os
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional
import queue

from team_training_testing import TeamTrainingSession

@dataclass
class TrainingSession:
    """Represents a training session"""
    id: str
    name: str
    session_type: str
    status: str  # 'queued', 'running', 'completed', 'failed', 'paused'
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    progress: float = 0.0
    current_iteration: int = 0
    total_iterations: int = 1000
    results: Optional[Dict] = None
    thread: Optional[threading.Thread] = None

class TrainingControlTower:
    """
    Central control system for managing multiple training sessions
    
    Features:
    - Run multiple training sessions concurrently
    - Monitor progress of all sessions
    - Queue training requests
    - Advanced experiment management
    - Mission control for genetic algorithms and other experiments
    """
    
    def __init__(self, max_concurrent_sessions=3):
        self.max_concurrent_sessions = max_concurrent_sessions
        self.sessions: Dict[str, TrainingSession] = {}
        self.session_queue = queue.Queue()
        self.running_sessions: Dict[str, TrainingSession] = {}
        self.completed_sessions: Dict[str, TrainingSession] = {}
        
        # Control tower status
        self.is_running = False
        self.control_thread = None
        
        # Create directories
        os.makedirs('control_tower_logs', exist_ok=True)
        os.makedirs('training_sessions', exist_ok=True)
        
        print("🏗️ TRAINING CONTROL TOWER INITIALIZED")
        print(f"   Max concurrent sessions: {max_concurrent_sessions}")
        print(f"   Ready to manage multiple training operations")
        
    def start_control_tower(self):
        """Start the control tower management system"""
        if self.is_running:
            print("⚠️ Control Tower already running")
            return
            
        self.is_running = True
        self.control_thread = threading.Thread(target=self._control_loop, daemon=True)
        self.control_thread.start()
        
        print("🚀 CONTROL TOWER ONLINE")
        print("   Monitoring training queue and managing sessions")
        
    def stop_control_tower(self):
        """Stop the control tower management system"""
        self.is_running = False
        
        # Wait for running sessions to complete or force stop
        for session_id, session in self.running_sessions.items():
            print(f"⏸️ Stopping session: {session.name}")
            session.status = 'paused'
            
        if self.control_thread:
            self.control_thread.join(timeout=5.0)
            
        print("🛑 CONTROL TOWER OFFLINE")
        
    def queue_training_session(self, name: str, session_type: str, 
                             config: Optional[Dict] = None, priority: bool = False):
        """Queue a new training session"""
        
        session_id = f"{session_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = TrainingSession(
            id=session_id,
            name=name,
            session_type=session_type,
            status='queued',
            total_iterations=config.get('iterations', 1000) if config else 1000
        )
        
        self.sessions[session_id] = session
        
        if priority:
            # Add to front of queue
            temp_queue = queue.Queue()
            temp_queue.put(session)
            while not self.session_queue.empty():
                temp_queue.put(self.session_queue.get())
            self.session_queue = temp_queue
        else:
            self.session_queue.put(session)
            
        print(f"📋 QUEUED: {name} ({session_type})")
        print(f"   Session ID: {session_id}")
        print(f"   Queue position: {self.session_queue.qsize()}")
        
        return session_id
        
    def _control_loop(self):
        """Main control loop for managing sessions"""
        while self.is_running:
            try:
                # Check if we can start new sessions
                if (len(self.running_sessions) < self.max_concurrent_sessions and 
                    not self.session_queue.empty()):
                    
                    session = self.session_queue.get_nowait()
                    self._start_session(session)
                    
                # Monitor running sessions
                self._monitor_running_sessions()
                
                # Brief pause to prevent excessive CPU usage
                time.sleep(1.0)
                
            except queue.Empty:
                time.sleep(2.0)
            except Exception as e:
                print(f"❌ Control Tower error: {e}")
                time.sleep(5.0)
                
    def _start_session(self, session: TrainingSession):
        """Start a training session"""
        session.status = 'running'
        session.start_time = datetime.now()
        
        print(f"🏁 STARTING: {session.name}")
        print(f"   Type: {session.session_type}")
        print(f"   Target iterations: {session.total_iterations}")
        
        # Create and start training thread based on session type
        if session.session_type == 'testing_team':
            session.thread = threading.Thread(
                target=self._run_testing_team_training,
                args=(session,),
                daemon=True
            )
        elif session.session_type == 'peanut_team':
            session.thread = threading.Thread(
                target=self._run_peanut_team_training,
                args=(session,),
                daemon=True
            )
        elif session.session_type == 'genetic_algorithm':
            session.thread = threading.Thread(
                target=self._run_genetic_algorithm,
                args=(session,),
                daemon=True
            )
        else:
            print(f"❌ Unknown session type: {session.session_type}")
            session.status = 'failed'
            return
            
        session.thread.start()
        self.running_sessions[session.id] = session
        
    def _run_testing_team_training(self, session: TrainingSession):
        """Run testing team training session"""
        try:
            trainer = TeamTrainingSession()
            
            if not trainer.team_derklings:
                session.status = 'failed'
                session.results = {'error': 'Could not initialize testing team'}
                return
                
            print(f"🦎 Training Testing Team: {session.name}")
            
            # Run training with progress callback
            results = trainer.train_testing_team(iterations=session.total_iterations)
            
            session.results = results
            session.status = 'completed'
            session.end_time = datetime.now()
            
            print(f"✅ COMPLETED: {session.name}")
            
        except Exception as e:
            session.status = 'failed'
            session.results = {'error': str(e)}
            print(f"❌ FAILED: {session.name} - {e}")
            
    def _run_peanut_team_training(self, session: TrainingSession):
        """Run peanut team training session"""
        try:
            # TODO: Implement peanut team training
            print(f"🥜 Training Peanut Team: {session.name}")
            
            # Placeholder for now
            time.sleep(10)  # Simulate training
            
            session.results = {'placeholder': 'Peanut team training not implemented yet'}
            session.status = 'completed'
            session.end_time = datetime.now()
            
        except Exception as e:
            session.status = 'failed'
            session.results = {'error': str(e)}
            
    def _run_genetic_algorithm(self, session: TrainingSession):
        """Run genetic algorithm experiment"""
        try:
            # TODO: Implement genetic algorithm training
            print(f"🧬 Running Genetic Algorithm: {session.name}")
            
            # Placeholder for now
            time.sleep(15)  # Simulate GA training
            
            session.results = {'placeholder': 'Genetic algorithm not implemented yet'}
            session.status = 'completed'
            session.end_time = datetime.now()
            
        except Exception as e:
            session.status = 'failed'
            session.results = {'error': str(e)}
            
    def _monitor_running_sessions(self):
        """Monitor and update running sessions"""
        completed_sessions = []
        
        for session_id, session in self.running_sessions.items():
            if session.status in ['completed', 'failed']:
                completed_sessions.append(session_id)
                self.completed_sessions[session_id] = session
                
                # Save session results
                self._save_session_results(session)
                
        # Remove completed sessions from running list
        for session_id in completed_sessions:
            del self.running_sessions[session_id]
            
    def _save_session_results(self, session: TrainingSession):
        """Save session results to file"""
        try:
            session_data = {
                'id': session.id,
                'name': session.name,
                'session_type': session.session_type,
                'status': session.status,
                'start_time': session.start_time.isoformat() if session.start_time else None,
                'end_time': session.end_time.isoformat() if session.end_time else None,
                'total_iterations': session.total_iterations,
                'results': session.results
            }
            
            filepath = f'training_sessions/{session.id}_results.json'
            with open(filepath, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            print(f"💾 Saved results: {filepath}")
            
        except Exception as e:
            print(f"❌ Could not save session results: {e}")
            
    def get_status_report(self):
        """Get comprehensive status report"""
        report = {
            'control_tower_status': 'online' if self.is_running else 'offline',
            'queue_size': self.session_queue.qsize(),
            'running_sessions': len(self.running_sessions),
            'completed_sessions': len(self.completed_sessions),
            'max_concurrent': self.max_concurrent_sessions,
            'sessions': {}
        }
        
        # Add details for all sessions
        for session_id, session in self.sessions.items():
            duration = None
            if session.start_time:
                end_time = session.end_time or datetime.now()
                duration = (end_time - session.start_time).total_seconds()
                
            report['sessions'][session_id] = {
                'name': session.name,
                'type': session.session_type,
                'status': session.status,
                'progress': session.progress,
                'duration_seconds': duration
            }
            
        return report
        
    def print_status_dashboard(self):
        """Print a nice status dashboard"""
        report = self.get_status_report()
        
        print("\n" + "=" * 60)
        print("🏗️ TRAINING CONTROL TOWER DASHBOARD")
        print("=" * 60)
        print(f"Status: {report['control_tower_status'].upper()}")
        print(f"Queue: {report['queue_size']} waiting")
        print(f"Running: {report['running_sessions']}/{report['max_concurrent']} sessions")
        print(f"Completed: {report['completed_sessions']} sessions")
        
        if report['running_sessions'] > 0:
            print(f"\n🏃 RUNNING SESSIONS:")
            for session_id, session in report['sessions'].items():
                if session['status'] == 'running':
                    duration = session['duration_seconds'] or 0
                    print(f"   • {session['name']} - {duration/60:.1f}m")
                    
        if report['queue_size'] > 0:
            print(f"\n📋 QUEUED SESSIONS:")
            # Note: Can't easily show queued sessions without modifying queue
            print(f"   {report['queue_size']} sessions waiting...")
            
        print("=" * 60)

def main():
    """Demo the Control Tower system"""
    
    print("🏗️ TRAINING CONTROL TOWER DEMO")
    print("=" * 50)
    
    # Create control tower
    tower = TrainingControlTower(max_concurrent_sessions=2)
    
    # Start the control tower
    tower.start_control_tower()
    
    # Queue some training sessions
    print("\n📋 QUEUEING TRAINING SESSIONS...")
    
    # Queue testing team training
    session1 = tower.queue_training_session(
        name="Testing Team Alpha",
        session_type="testing_team",
        config={'iterations': 100}  # Short demo
    )
    
    # Queue another testing team session
    session2 = tower.queue_training_session(
        name="Testing Team Beta", 
        session_type="testing_team",
        config={'iterations': 50}  # Even shorter
    )
    
    # Monitor for a while
    try:
        for i in range(30):  # Monitor for ~30 seconds
            time.sleep(1)
            
            if i % 10 == 0:  # Print dashboard every 10 seconds
                tower.print_status_dashboard()
                
            # Check if all sessions completed
            if (len(tower.running_sessions) == 0 and 
                tower.session_queue.empty()):
                print("\n✅ All sessions completed!")
                break
                
    except KeyboardInterrupt:
        print("\n⏸️ Demo interrupted")
        
    finally:
        tower.stop_control_tower()
        tower.print_status_dashboard()
        print("\n🏁 Demo complete!")

if __name__ == "__main__":
    main()
