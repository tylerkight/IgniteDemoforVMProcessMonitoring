# CPU Spike Tool

Simple Python tool to generate massive CPU load on a VM for performance testing.

## Quick Start

1. **Install dependency:**
   ```bash
   sudo apt install python3-setproctitle
   ```

2. **Run CPU spike:**
   ```bash
   python3 cpu_spike.py
   ```

3. **Stop with Ctrl+C**

## What it does

- Creates massive CPU load (sustained high usage)  
- Process appears as "backupdatawarehouse.exe" (not python3)
- Runs until you stop it with Ctrl+C
- Perfect for Azure Monitor testing

## Monitoring

```bash
# Check process name
ps aux | grep backup

# Monitor CPU usage  
top -p $(pgrep -f cpu_spike)
```

That's it! Simple and focused.