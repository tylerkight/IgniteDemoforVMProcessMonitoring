#!/usr/bin/env python3
"""
Demo Controller for Azure Monitor Process Monitoring
Simple interface to demonstrate process-level monitoring capabilities
"""
import subprocess
import sys
import time
import os
import signal
import platform
from datetime import datetime

class DemoController:
    def __init__(self):
        self.processes = {}
        
        print("="*60)
        print("AZURE MONITOR PROCESS MONITORING DEMO")
        print("="*60)
        print(f"Demo started at: {datetime.now()}")
        print()
    
    def start_process(self, script_name, mode=None):
        """Start a demo process"""
        # Use .bat files on Windows for testing, .exe symlinks on Linux
        if platform.system() == "Windows":
            if script_name == "BackupDataWarehouse.py":
                cmd = ["BackupDataWarehouse.exe.bat"]
            elif script_name == "WebServiceMonitor.py":
                cmd = ["WebServiceMonitor.exe.bat"]
            else:
                cmd = [sys.executable, script_name]
        else:
            # Linux - use the .exe symlinks
            if script_name == "BackupDataWarehouse.py":
                cmd = ["./BackupDataWarehouse.exe"]
            elif script_name == "WebServiceMonitor.py":
                cmd = ["./WebServiceMonitor.exe"]
            else:
                cmd = [sys.executable, script_name]
        
        if mode:
            cmd.append(f"--{mode}")
        
        try:
            process = subprocess.Popen(cmd)
            self.processes[script_name] = process
            mode_text = f" in {mode.upper()} mode" if mode else " in NORMAL mode"
            executable = cmd[0] if platform.system() == "Windows" else script_name
            print(f"✓ Started {executable}{mode_text} (PID: {process.pid})")
            return True
        except Exception as e:
            print(f"✗ Failed to start {script_name}: {e}")
            return False
    
    def stop_process(self, script_name):
        """Stop a demo process"""
        if script_name in self.processes:
            process = self.processes[script_name]
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✓ Stopped {script_name}")
                del self.processes[script_name]
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                print(f"✓ Force killed {script_name}")
                del self.processes[script_name]
            except Exception as e:
                print(f"✗ Error stopping {script_name}: {e}")
    
    def stop_all(self):
        """Stop all demo processes"""
        print("\nStopping all demo processes...")
        for script_name in list(self.processes.keys()):
            self.stop_process(script_name)
    
    def show_status(self):
        """Show current process status"""
        print("\nCurrent Process Status:")
        print("-" * 40)
        
        if not self.processes:
            print("No demo processes running")
            return
        
        for script_name, process in self.processes.items():
            status = "Running" if process.poll() is None else "Stopped"
            print(f"{script_name}: {status} (PID: {process.pid})")
    
    def interactive_menu(self):
        """Interactive menu for demo control"""
        while True:
            print("\n" + "="*60)
            print("DEMO CONTROL MENU")
            print("="*60)
            print("1. Start BackupDataWarehouse.exe (Normal)")
            print("2. Start BackupDataWarehouse.exe (Memory Leak)")
            print("3. Start WebServiceMonitor.exe (Normal)")
            print("4. Start WebServiceMonitor.exe (CPU Spike)")
            print("5. Stop BackupDataWarehouse.exe")
            print("6. Stop WebServiceMonitor.exe")
            print("7. Show Process Status")
            print("8. Stop All and Exit")
            print()
            
            try:
                choice = input("Enter your choice (1-8): ").strip()
                
                if choice == "1":
                    self.stop_process("BackupDataWarehouse.py")
                    self.start_process("BackupDataWarehouse.py")
                elif choice == "2":
                    self.stop_process("BackupDataWarehouse.py")
                    self.start_process("BackupDataWarehouse.py", "memory-leak")
                elif choice == "3":
                    self.stop_process("WebServiceMonitor.py")
                    self.start_process("WebServiceMonitor.py")
                elif choice == "4":
                    self.stop_process("WebServiceMonitor.py")
                    self.start_process("WebServiceMonitor.py", "cpu-spike")
                elif choice == "5":
                    self.stop_process("BackupDataWarehouse.py")
                elif choice == "6":
                    self.stop_process("WebServiceMonitor.py")
                elif choice == "7":
                    self.show_status()
                elif choice == "8":
                    self.stop_all()
                    break
                else:
                    print("Invalid choice. Please enter 1-8.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                self.stop_all()
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    controller = DemoController()
    
    try:
        controller.interactive_menu()
    finally:
        controller.stop_all()
        print(f"\nDemo ended at: {datetime.now()}")

if __name__ == "__main__":
    main()