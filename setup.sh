#!/bin/bash
"""
Setup script for Azure Monitor Process Monitoring Demo
Creates executable symbolic links with .exe names for Linux process monitoring
"""

echo "Setting up Azure Monitor Process Monitoring Demo..."
echo "================================================="

# Make Python scripts executable
chmod +x BackupDataWarehouse.py
chmod +x WebServiceMonitor.py  
chmod +x demo_controller.py

# Create symbolic links with .exe names for process identification
ln -sf BackupDataWarehouse.py BackupDataWarehouse.exe
ln -sf WebServiceMonitor.py WebServiceMonitor.exe

echo "✓ Made Python scripts executable"
echo "✓ Created symbolic links:"
echo "  BackupDataWarehouse.exe -> BackupDataWarehouse.py"
echo "  WebServiceMonitor.exe -> WebServiceMonitor.py"
echo ""
echo "Setup complete! You can now run:"
echo "  ./BackupDataWarehouse.exe                (normal mode)"
echo "  ./BackupDataWarehouse.exe --memory-leak  (memory leak mode)"
echo "  ./WebServiceMonitor.exe                  (normal mode)"
echo "  ./WebServiceMonitor.exe --cpu-spike      (CPU spike mode)"
echo "  python3 demo_controller.py               (interactive menu)"
echo ""
echo "For Azure Monitor, these will appear as separate processes:"
echo "  - process.command: BackupDataWarehouse.exe"
echo "  - process.command: WebServiceMonitor.exe"