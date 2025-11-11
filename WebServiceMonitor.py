#!/usr/bin/env python3
"""
WebServiceMonitor.exe - Secondary demo process for Azure Monitor demonstration
Simulates a web service monitoring tool with controllable CPU behavior
"""
import sys
import time
import os
import signal
import math
from datetime import datetime

class WebServiceMonitor:
    def __init__(self):
        self.running = True
        self.cpu_spike_mode = False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
        print(f"[{datetime.now()}] WebServiceMonitor.exe starting (PID: {os.getpid()})")
    
    def shutdown(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n[{datetime.now()}] WebServiceMonitor.exe shutting down gracefully...")
        self.running = False
        sys.exit(0)
    
    def normal_monitoring(self):
        """Simulate normal web service monitoring"""
        print(f"[{datetime.now()}] Monitoring web services... All systems normal")
        
        # Light CPU work - simulate checking services
        result = 0
        for i in range(100000):  # Light computation
            result += i * 2
        
        time.sleep(3)
    
    def cpu_spike_operation(self):
        """Simulate high CPU usage - intensive computation"""
        print(f"[{datetime.now()}] *** CPU SPIKE DETECTED *** Processing intensive workload!")
        
        # Heavy CPU computation - designed for sustained high CPU usage
        result = 0
        for i in range(10000000):  # 10 million iterations for high CPU
            result += i * i * i % 997  # Expensive calculation
            result += math.sqrt(i) * math.sin(i)  # More expensive operations
            
            # Every 100k iterations, do even more work
            if i % 100000 == 0:
                temp = [x ** 3 for x in range(1000)]
                result += sum(temp) % 1000
        
        print(f"[{datetime.now()}] High CPU workload completed (result: {result % 10000})")
        
        # Very short pause to maintain sustained ~50% CPU
        time.sleep(0.1)
    
    def run(self):
        """Main execution loop"""
        iteration = 0
        
        while self.running:
            iteration += 1
            
            try:
                if self.cpu_spike_mode:
                    self.cpu_spike_operation()
                else:
                    self.normal_monitoring()
                    
            except KeyboardInterrupt:
                self.shutdown(None, None)
            except Exception as e:
                print(f"[{datetime.now()}] Error: {e}")
                time.sleep(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--cpu-spike":
        print("Starting WebServiceMonitor.exe in CPU SPIKE mode")
        monitor = WebServiceMonitor()
        monitor.cpu_spike_mode = True
        monitor.run()
    else:
        print("Starting WebServiceMonitor.exe in NORMAL mode")
        monitor = WebServiceMonitor()
        monitor.run()

if __name__ == "__main__":
    main()