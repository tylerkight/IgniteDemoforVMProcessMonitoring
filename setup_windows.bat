@echo off
REM Windows setup script for Azure Monitor Process Monitoring Demo
REM Creates batch files that will show up as .exe processes

echo Setting up Azure Monitor Process Monitoring Demo for Windows...
echo ===============================================================

REM Create batch files that launch Python scripts with .exe names
echo @echo off > BackupDataWarehouse.exe.bat
echo py BackupDataWarehouse.py %%* >> BackupDataWarehouse.exe.bat

echo @echo off > WebServiceMonitor.exe.bat  
echo py WebServiceMonitor.py %%* >> WebServiceMonitor.exe.bat

echo.
echo ✓ Created Windows batch files:
echo   BackupDataWarehouse.exe.bat
echo   WebServiceMonitor.exe.bat
echo.
echo Setup complete! You can now test locally:
echo   BackupDataWarehouse.exe.bat                (normal mode)
echo   BackupDataWarehouse.exe.bat --memory-leak  (memory leak mode)
echo   WebServiceMonitor.exe.bat                  (normal mode)  
echo   WebServiceMonitor.exe.bat --cpu-spike      (CPU spike mode)
echo   python demo_controller.py                  (interactive menu)
echo.
echo Note: On Linux VM, the setup.sh script will create proper .exe symlinks