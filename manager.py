#!/usr/bin/env python3
"""
Main orchestrator script that manages multiple worker processes.
This script starts and monitors worker processes that can be used for
demonstrating per-process monitoring with OpenTelemetry Collector.
"""

import subprocess
import time
import sys
import signal
import requests
import json
from typing import List, Dict

# Worker configuration
WORKERS = [
    {'name': 'worker1', 'port': 8001},
    {'name': 'worker2', 'port': 8002},
    {'name': 'worker3', 'port': 8003},
]


class WorkerManager:
    """Manages multiple worker processes."""
    
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.running = True
        
    def start_workers(self):
        """Start all worker processes."""
        print("Starting worker processes...")
        for worker in WORKERS:
            cmd = [
                sys.executable,
                'worker_process.py',
                '--name', worker['name'],
                '--port', str(worker['port'])
            ]
            print(f"Starting {worker['name']} on port {worker['port']}...")
            proc = subprocess.Popen(cmd)
            self.processes.append(proc)
            time.sleep(0.5)
        
        print(f"\nAll {len(self.processes)} workers started!\n")
        
    def stop_workers(self):
        """Stop all worker processes gracefully."""
        print("\nStopping worker processes...")
        for proc in self.processes:
            if proc.poll() is None:  # Still running
                proc.terminate()
        
        # Wait for graceful shutdown
        time.sleep(2)
        
        # Force kill if still running
        for proc in self.processes:
            if proc.poll() is None:
                proc.kill()
        
        print("All workers stopped.")
        
    def check_health(self):
        """Check health of all workers."""
        print("\n" + "="*60)
        print("WORKER HEALTH STATUS")
        print("="*60)
        for worker in WORKERS:
            try:
                response = requests.get(f"http://localhost:{worker['port']}/health", timeout=2)
                if response.status_code == 200:
                    data = response.json()
                    status = "✓ HEALTHY" if data['status'] == 'healthy' else "✗ UNHEALTHY"
                    print(f"{worker['name']:10} [{status:12}] PID: {data['pid']}")
                    if any(data['failures'].values()):
                        active_failures = [k for k, v in data['failures'].items() if v]
                        print(f"           └─ Active failures: {', '.join(active_failures)}")
                else:
                    print(f"{worker['name']:10} [✗ ERROR     ] HTTP {response.status_code}")
            except requests.RequestException as e:
                print(f"{worker['name']:10} [✗ NO RESPONSE] {str(e)[:40]}")
        print("="*60 + "\n")
        
    def inject_failure(self, worker_name: str, failure_type: str):
        """Inject a failure into a specific worker."""
        worker = next((w for w in WORKERS if w['name'] == worker_name), None)
        if not worker:
            print(f"Error: Worker '{worker_name}' not found!")
            return False
            
        try:
            url = f"http://localhost:{worker['port']}/inject-failure"
            payload = {'type': failure_type}
            response = requests.post(url, json=payload, timeout=2)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Successfully injected '{failure_type}' into {worker_name}")
                return True
            else:
                print(f"✗ Failed to inject failure: HTTP {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"✗ Error communicating with worker: {e}")
            return False
            
    def clear_failures(self, worker_name: str):
        """Clear all failures from a specific worker."""
        worker = next((w for w in WORKERS if w['name'] == worker_name), None)
        if not worker:
            print(f"Error: Worker '{worker_name}' not found!")
            return False
            
        try:
            url = f"http://localhost:{worker['port']}/clear-failures"
            response = requests.post(url, timeout=2)
            
            if response.status_code == 200:
                print(f"✓ Cleared all failures from {worker_name}")
                return True
            else:
                print(f"✗ Failed to clear failures: HTTP {response.status_code}")
                return False
        except requests.RequestException as e:
            print(f"✗ Error communicating with worker: {e}")
            return False
    
    def monitor_processes(self):
        """Monitor worker processes and report status."""
        while self.running:
            # Check if any processes have died
            for i, proc in enumerate(self.processes):
                if proc.poll() is not None:
                    worker_name = WORKERS[i]['name']
                    print(f"\n⚠ WARNING: {worker_name} (PID {proc.pid}) has stopped!")
            
            time.sleep(5)
    
    def interactive_mode(self):
        """Run in interactive mode with menu."""
        print("\n" + "="*60)
        print("PROCESS MONITORING DEMO - INTERACTIVE MODE")
        print("="*60)
        print("\nAvailable commands:")
        print("  health              - Check health of all workers")
        print("  inject <worker> <type> - Inject failure into worker")
        print("                       Types: cpu_spike, memory_leak, crash, io_heavy")
        print("  clear <worker>      - Clear all failures from worker")
        print("  quit                - Stop all workers and exit")
        print("\nExamples:")
        print("  inject worker1 cpu_spike")
        print("  inject worker2 memory_leak")
        print("  clear worker1")
        print("="*60 + "\n")
        
        try:
            while self.running:
                try:
                    cmd = input("\nCommand> ").strip().split()
                    if not cmd:
                        continue
                    
                    if cmd[0] == 'health':
                        self.check_health()
                    elif cmd[0] == 'inject' and len(cmd) == 3:
                        self.inject_failure(cmd[1], cmd[2])
                    elif cmd[0] == 'clear' and len(cmd) == 2:
                        self.clear_failures(cmd[1])
                    elif cmd[0] == 'quit':
                        self.running = False
                        break
                    else:
                        print("Invalid command. Type 'health', 'inject <worker> <type>', 'clear <worker>', or 'quit'")
                except EOFError:
                    print("\nEOF detected, exiting...")
                    self.running = False
                    break
        except KeyboardInterrupt:
            print("\nInterrupted, exiting...")
            self.running = False


def main():
    """Main entry point."""
    manager = WorkerManager()
    
    # Setup signal handlers
    def signal_handler(sig, frame):
        print("\nReceived shutdown signal...")
        manager.running = False
        manager.stop_workers()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start workers
    manager.start_workers()
    
    # Wait for workers to be ready
    print("Waiting for workers to be ready...")
    time.sleep(3)
    
    # Check initial health
    manager.check_health()
    
    # Run interactive mode
    manager.interactive_mode()
    
    # Cleanup
    manager.stop_workers()


if __name__ == '__main__':
    main()
