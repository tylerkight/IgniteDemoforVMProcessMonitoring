#!/usr/bin/env python3
"""
CPU Spike Tool - Creates massive CPU load while appearing as "backupdatawarehouse.exe"
Simple command line tool for VM performance testing
"""
import math
import time
import signal
import sys
import os

try:
    import setproctitle
    setproctitle.setproctitle("backupdatawarehouse.exe")
    print("✓ Process name set to 'backupdatawarehouse.exe'")
except ImportError:
    print("WARNING: setproctitle not available - process will show as 'python3'")
    print("Install with: sudo apt install python3-setproctitle")

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n🛑 Stopping CPU spike...")
    running = False
    sys.exit(0)

def cpu_spike():
    """Generate massive CPU load with intensive calculations"""
    global running
    iteration = 0
    
    print("🔥 Starting massive CPU spike!")
    print("💡 Press Ctrl+C to stop")
    print("📊 Monitor with: ps aux | grep backup")
    print("📈 Monitor CPU with: top -p $(pgrep -f cpu_spike)")
    print("-" * 50)
    
    while running:
        iteration += 1
        result = 0
        
        # Intensive CPU computation - 10 million operations per iteration
        for i in range(10000000):
            result += i * i * i % 997        # Expensive cubic calculation
            result += int(math.sqrt(abs(i))) # Square root 
            result += int(math.sin(i) * 1000) # Trigonometry
            
            # Extra expensive work every 100k iterations
            if i % 100000 == 0:
                temp = [x ** 3 for x in range(1000)]  # List comprehension with cubing
                result += sum(temp) % 10000
        
        print(f"🔥 CPU spike iteration {iteration} completed (result: {result % 100000})")
        
        # Very brief pause to allow Ctrl+C handling
        time.sleep(0.01)

def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("🚀 BackupDataWarehouse.exe CPU Spike Tool")
    print("=" * 60)
    print(f"📍 Process ID: {os.getpid()}")
    
    # Start the CPU spike
    cpu_spike()

if __name__ == "__main__":
    main()