#!/usr/bin/env python3
"""
Quick demo script to showcase the process monitoring application.
This script demonstrates the capabilities without requiring user interaction.
"""

import subprocess
import time
import sys
import requests
import json

WORKERS = [
    {'name': 'worker1', 'port': 8001},
    {'name': 'worker2', 'port': 8002},
    {'name': 'worker3', 'port': 8003},
]

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def start_workers():
    """Start all worker processes."""
    print_header("Starting Worker Processes")
    processes = []
    for worker in WORKERS:
        cmd = [
            sys.executable,
            'worker_process.py',
            '--name', worker['name'],
            '--port', str(worker['port'])
        ]
        print(f"  Starting {worker['name']} on port {worker['port']}...")
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        processes.append(proc)
        time.sleep(0.5)
    
    print(f"  ✓ All {len(processes)} workers started!")
    return processes

def check_health():
    """Check health of all workers."""
    print_header("Worker Health Status")
    for worker in WORKERS:
        try:
            response = requests.get(f"http://localhost:{worker['port']}/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                failures = [k for k, v in data['failures'].items() if v]
                status = "✓ HEALTHY" if not failures else f"⚠ FAILURES: {', '.join(failures)}"
                print(f"  {worker['name']:10} | {status:40} | PID: {data['pid']}")
            else:
                print(f"  {worker['name']:10} | ✗ HTTP {response.status_code}")
        except Exception as e:
            print(f"  {worker['name']:10} | ✗ NO RESPONSE")

def inject_failure(worker_name, failure_type):
    """Inject a failure into a worker."""
    worker = next((w for w in WORKERS if w['name'] == worker_name), None)
    if worker:
        try:
            url = f"http://localhost:{worker['port']}/inject-failure"
            payload = {'type': failure_type}
            response = requests.post(url, json=payload, timeout=2)
            if response.status_code == 200:
                print(f"  ✓ Injected '{failure_type}' into {worker_name}")
                return True
        except Exception as e:
            print(f"  ✗ Error: {e}")
    return False

def run_demo(processes):
    """Run the demo scenario."""
    try:
        print_header("Demo Application Ready")
        print("  Waiting for workers to initialize...")
        time.sleep(3)
        
        # Initial health check
        check_health()
        
        # Scenario 1: CPU spike in worker1
        print_header("Scenario 1: CPU Spike in worker1")
        inject_failure('worker1', 'cpu_spike')
        time.sleep(2)
        check_health()
        
        # Scenario 2: Memory leak in worker2
        print_header("Scenario 2: Memory Leak in worker2")
        inject_failure('worker2', 'memory_leak')
        time.sleep(2)
        check_health()
        
        # Scenario 3: I/O heavy in worker3
        print_header("Scenario 3: I/O Heavy Load in worker3")
        inject_failure('worker3', 'io_heavy')
        time.sleep(2)
        check_health()
        
        print_header("Demo Complete")
        print("  All failure scenarios demonstrated!")
        print("\n  In a real monitoring setup, you would see:")
        print("    • worker1: High CPU usage in process.cpu.utilization metrics")
        print("    • worker2: Increasing memory in process.memory.usage metrics")
        print("    • worker3: High I/O in process.disk.io metrics")
        print("\n  Monitor these processes with:")
        print("    • Azure Monitor Agent + OpenTelemetry Collector")
        print("    • View metrics in Azure Monitor / Application Insights")
        print("    • Use the Kusto queries in azure-monitor-queries.md")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    finally:
        print_header("Cleanup")
        print("  Stopping all worker processes...")
        for proc in processes:
            if proc.poll() is None:
                proc.terminate()
        time.sleep(1)
        for proc in processes:
            if proc.poll() is None:
                proc.kill()
        print("  ✓ All workers stopped.")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  PROCESS MONITORING DEMO APPLICATION")
    print("  Showcasing per-process monitoring with Azure Monitor")
    print("="*70)
    
    processes = start_workers()
    run_demo(processes)
    
    print("\n" + "="*70)
    print("  Thank you for trying the demo!")
    print("  For more information, see README.md and SETUP_GUIDE.md")
    print("="*70 + "\n")
