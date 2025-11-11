#!/usr/bin/env python3
"""
BackupDataWarehouse.exe - Primary demo process for Azure Monitor demonstration
Simulates a data warehouse backup service with controllable memory behavior
"""
import sys
import time
import os
import gc
import signal
from datetime import datetime

class BackupDataWarehouse:
    def __init__(self):
        self.memory_ballast = []
        self.running = True
        self.memory_leak_mode = False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
        print(f"[{datetime.now()}] BackupDataWarehouse.exe starting (PID: {os.getpid()})")
    
    def shutdown(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n[{datetime.now()}] BackupDataWarehouse.exe shutting down gracefully...")
        self.running = False
        sys.exit(0)
    
    def normal_operation(self):
        """Simulate normal backup operations"""
        print(f"[{datetime.now()}] Performing normal backup operations...")
        
        # Simulate some work
        time.sleep(2)
        
        # Light memory usage for normal operations
        temp_data = ["backup_chunk_" + str(i) for i in range(1000)]
        del temp_data
        gc.collect()
    
    def memory_leak_operation(self):
        """Simulate runaway memory leak - RAPID memory consumption"""
        print(f"[{datetime.now()}] *** MEMORY LEAK DETECTED *** Consuming memory rapidly!")
        
        # Allocate 500MB of memory per iteration
        chunk_size = 100 * 1024 * 1024  # 100MB
        
        # Create 5 chunks = 500MB per call
        for i in range(5):
            # Create large string and large data structures
            large_data = "X" * chunk_size
            large_dict = {f"leak_{len(self.memory_ballast)}_{i}": large_data}
            self.memory_ballast.append(large_dict)
        
        total_mb = len(self.memory_ballast) * 100
        print(f"[{datetime.now()}] CRITICAL: Memory consumption now {total_mb}MB and growing!")
        
        # Sleep only 0.5 seconds for RAPID memory growth
        time.sleep(0.5)
    
    def run(self):
        """Main execution loop"""
        iteration = 0
        
        while self.running:
            iteration += 1
            
            try:
                if self.memory_leak_mode:
                    self.memory_leak_operation()
                else:
                    self.normal_operation()
                    
            except KeyboardInterrupt:
                self.shutdown(None, None)
            except Exception as e:
                print(f"[{datetime.now()}] Error: {e}")
                time.sleep(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--memory-leak":
        print("Starting BackupDataWarehouse.exe in MEMORY LEAK mode")
        warehouse = BackupDataWarehouse()
        warehouse.memory_leak_mode = True
        warehouse.run()
    else:
        print("Starting BackupDataWarehouse.exe in NORMAL mode")
        warehouse = BackupDataWarehouse()
        warehouse.run()

if __name__ == "__main__":
    main()