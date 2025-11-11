# Azure Monitor Process Monitoring Demo# Process Monitoring Demo Application



A simple, focused demonstration of **per-process monitoring** using Azure Monitor Agent with OpenTelemetry Collector for the Microsoft Ignite conference.A demo application showcasing **per-process monitoring** using Azure Monitor Agent with OpenTelemetry Collector. This application demonstrates how to monitor multiple worker processes on a single VM and identify performance issues using Azure Monitor's process-level performance counters.



## 🎯 Demo Overview## 📋 Overview



This demo showcases Azure Monitor's ability to collect and analyze **process-level performance counters** on Linux VMs, perfect for identifying which specific processes are consuming resources.This optimized demo application features:

- **3 Independent Worker Processes**: Each with distinct process names (`demo-worker1`, `demo-worker2`, `demo-worker3`)

**What you'll demonstrate:**- **Sustained Failure Injection**: CPU spikes (50%+ utilization), memory leaks, I/O stress, and crashes

- Two distinct processes: `BackupDataWarehouse.exe` and `WebServiceMonitor.exe`- **Perfect Process Identification**: Uses `setproctitle` for clear process naming in metrics

- Controllable resource consumption (memory leak and CPU spike)- **Interactive Management**: Enhanced CLI with emoji-based status reporting

- Process-level metrics collection via Azure Monitor Agent- **Azure Monitor Integration**: Leverages performance counter collection via Data Collection Rules

- PromQL queries to identify problematic processes

## 🎯 Use Case

## 🖥️ VM Requirements

This demo showcases **Azure Monitor performance counter collection** for process monitoring scenarios where:

- **OS**: Linux Ubuntu 24.04

- **vCPUs**: 2- Multiple services/processes run on the same VM

- **Memory**: 8 GiB RAM- One process may consume excessive CPU, memory, or I/O resources

- **Disk**: 30 GiB Premium SSD LRS (P4, 120 IOPS, 25 MBps)- You need to identify which specific process is causing performance issues

- **Azure Monitor Agent**: Installed with OpenTelemetry Collector- Azure Monitor Agent automatically collects process-level performance counters via OpenTelemetry

- Performance counters are analyzed using PromQL queries in Azure Monitor

## 🚀 Quick Setup (5 minutes)

**Perfect for demonstrating:**

### 1. Clone and Setup- Process identification using distinct process names (`demo-worker1`, `demo-worker2`, `demo-worker3`)

```bash- Sustained resource consumption patterns (50%+ CPU utilization)

git clone https://github.com/tylerkight/IgniteDemoforVMProcessMonitoring.git- Real-time performance monitoring and alerting scenarios

cd IgniteDemoforVMProcessMonitoring

chmod +x setup.sh## 🚀 Quick Start

./setup.sh

```### Prerequisites



### 2. Verify Setup- **Azure VM** with Azure Monitor Agent installed

```bash- **Python 3.8+** with virtual environment support

ls -la *.exe- **Data Collection Rule (DCR)** configured for performance counter collection

# Should show:

# BackupDataWarehouse.exe -> BackupDataWarehouse.py### Installation

# WebServiceMonitor.exe -> WebServiceMonitor.py

```1. **Clone the repository:**



## 🎬 Demo Scenarios```bash

git clone https://github.com/tylerkight/IgniteDemoforVMProcessMonitoring.git

### Scenario 1: Memory Leak Detectioncd IgniteDemoforVMProcessMonitoring

```

**Objective**: Show how to identify which process is consuming excessive memory

2. **Set up Python environment:**

1. **Start the interactive demo**:

   ```bash```bash

   python3 demo_controller.pypython3 -m venv venv

   ```source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

2. **Launch processes in normal mode**:```

   - Choose option `1`: Start BackupDataWarehouse.exe (Normal)

   - Choose option `3`: Start WebServiceMonitor.exe (Normal)3. **Start the optimized demo:**



3. **Verify normal baseline**:### Start the Enhanced Demo

   ```bash

   # In another terminal```bash

   ps aux | grep -E "(BackupDataWarehouse|WebServiceMonitor)"python3 manager_improved.py

   # Should show both processes running normally```

   ```

This provides full control with clear status reporting and Windows compatibility.

4. **Trigger memory leak**:

   - Choose option `2`: Start BackupDataWarehouse.exe (Memory Leak)### Basic Usage

   - Watch the terminal output showing rapid memory consumption

**Interactive Mode:**

5. **Monitor in Azure Monitor**:

   - Use PromQL queries to see memory spike for `BackupDataWarehouse.exe`Once started, the application runs in interactive mode:

   - Show normal memory usage for `WebServiceMonitor.exe`

```bash

### Scenario 2: CPU Spike Identification# Check health of all workers

Command> health

**Objective**: Show how to identify which process is consuming excessive CPU

# Inject a CPU spike into worker1

1. **Start with normal processes**:Command> inject worker1 cpu_spike

   - BackupDataWarehouse.exe (Normal)

   - WebServiceMonitor.exe (Normal)# Inject a memory leak into worker2

Command> inject worker2 memory_leak

2. **Trigger CPU spike**:

   - Choose option `4`: Start WebServiceMonitor.exe (CPU Spike)# Clear all failures from worker1

   - Watch terminal output showing intensive computationCommand> clear worker1



3. **Monitor in Azure Monitor**:# Check health again to see the effects

   - Use PromQL queries to see CPU spike for `WebServiceMonitor.exe`Command> health

   - Show normal CPU usage for `BackupDataWarehouse.exe`

# Exit the application

## 📊 Expected Azure Monitor ResultsCommand> quit

```

### Process Identification

Your PromQL queries should show these distinct processes:**Advanced Usage:**

- `process.command`: `BackupDataWarehouse.exe`

- `process.command`: `WebServiceMonitor.exe`Each worker can also be run independently for focused testing:



### Memory Leak Pattern (BackupDataWarehouse.exe)```bash

- **Normal**: ~50-100MB baseline# Run a single worker directly 

- **Memory Leak**: Rapid growth to 1GB+ within 30 secondspython3 worker1_improved.py worker1 8001

```

### CPU Spike Pattern (WebServiceMonitor.exe)

- **Normal**: ~5-15% CPU usageThis allows for targeted failure injection and individual process monitoring.

- **CPU Spike**: Sustained 40-60% CPU usage

## 🔧 Available Failure Types

## 🛠️ Manual Operations

| Failure Type | Description | Observable Metrics |

### Start Individual Processes|--------------|-------------|-------------------|

```bash| `cpu_spike` | Causes high CPU usage | process.cpu.utilization, process.cpu.time |

# Normal operations| `memory_leak` | Continuously allocates memory | process.memory.usage, process.memory.virtual |

./BackupDataWarehouse.exe &| `io_heavy` | Performs intensive I/O operations | process.disk.io, process.disk.operations |

./WebServiceMonitor.exe &| `crash` | Terminates the process | Process disappears from metrics |



# Problem scenarios## 📊 Azure Monitor Setup

./BackupDataWarehouse.exe --memory-leak &

./WebServiceMonitor.exe --cpu-spike &### 1. Understanding Performance Counters

```

This demo leverages **Azure Monitor's performance counter collection** to gather process-level metrics. Performance counters provide detailed insights into system and process behavior.

### Check Process Status

```bash📖 **Learn more**: [Performance counters and OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/metrics-opentelemetry-guest)

ps aux | grep -E "(BackupDataWarehouse|WebServiceMonitor)"

htop  # Visual process monitoring### 2. Configure Data Collection Rule (DCR)

```

Use Azure Monitor's Data Collection Rules to automatically set up performance counter collection:

### Stop Processes

```bash📖 **Step-by-step guide**: [Collect performance counters with Data Collection Rules](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection-performance?tabs=OpenTelemetry)

pkill -f BackupDataWarehouse

pkill -f WebServiceMonitor**Key benefits of the DCR approach:**

```- Automatically installs the latest Azure Monitor Agent

- Bundles and configures OpenTelemetry Collector

## 🎯 Demo Flow for Ignite- Enables process-level performance counter collection

- No manual OTel configuration required

### 5-Minute Demo Script

### 3. Optimized PromQL Queries

1. **Setup (30 seconds)**:

   - SSH into VMOnce performance counter collection is active, use these **tested and verified** PromQL queries:

   - `cd IgniteDemoforVMProcessMonitoring`

   - `python3 demo_controller.py`#### **Primary Query - Process Identification by Name**

```promql

2. **Baseline (1 minute)**:100 * max by ("process.command") ({"process.cpu.utilization", 

   - Start both processes in normal mode"process.executable.name"="python3", "process.owner"="azureuser"})

   - Show Azure Monitor dashboard with normal metrics```

   - Point out process.command identification**Expected results:**

- `demo-worker1`: 5-15% (normal operation)

3. **Memory Demo (2 minutes)**:- `demo-worker2`: **50%+** (during CPU spike)

   - Trigger BackupDataWarehouse.exe memory leak- `demo-worker3`: 5-15% (normal operation)

   - Show rapid memory growth in Azure Monitor

   - Highlight how you can identify the specific problematic process#### **Alternative Query - Process Identification by PID**

```promql

4. **CPU Demo (1.5 minutes)**:100 * max by ("process.pid", "process.command") ({"process.cpu.utilization", 

   - Trigger WebServiceMonitor.exe CPU spike"process.executable.name"="python3", "process.owner"="azureuser"})

   - Show CPU spike in Azure Monitor```

   - Demonstrate process-level filtering in PromQL

#### **Memory Usage Monitoring**

5. **Wrap-up (30 seconds)**:```promql

   - Stop all processesmax by ("process.command") ({"process.memory.usage", 

   - Summarize the value of per-process monitoring"process.executable.name"="python3", "process.owner"="azureuser"})

```

## 🔧 Troubleshooting

#### **Process Count Verification**

### Processes Not Showing in Azure Monitor```promql

- Verify Azure Monitor Agent is running: `systemctl status azuremonitoragent`count by ("process.command") ({"process.cpu.utilization", 

- Check OpenTelemetry Collector configuration"process.executable.name"="python3", "process.owner"="azureuser"})

- Ensure Data Collection Rules are configured for performance counters```

Should return `3` when all workers are running.

### High Resource Usage

- Stop runaway processes: `pkill -f BackupDataWarehouse; pkill -f WebServiceMonitor`## 🎬 Demo Scenarios

- Check available memory: `free -h`

- Monitor disk space: `df -h`### Scenario 1: Sustained CPU Spike Detection



### Permission Issues1. **Start the optimized demo**: `python3 manager_improved.py`

- Ensure scripts are executable: `chmod +x *.py *.sh`2. **Verify all workers healthy**: Look for `✅ Normal operation` messages from all 3 workers

- Check symbolic links: `ls -la *.exe`3. **Inject CPU spike**: `inject worker2 cpu_spike`

4. **Monitor with PromQL**: Use the primary query above to see `demo-worker2` spike to 50%+

## 📈 Success Metrics5. **Clear the failure**: `clear worker2` and observe CPU return to normal



After running the demo, you should be able to demonstrate:**What you'll see:**

- ✅ Clear process identification in Azure Monitor- `demo-worker1`: Consistent 5-15% CPU (normal)

- ✅ Dramatic memory spike attribution to specific process- `demo-worker2`: **Sustained 50%+ CPU** (problem process)

- ✅ CPU spike attribution to specific process  - `demo-worker3`: Consistent 5-15% CPU (normal)

- ✅ Ability to filter and query by process.command

- ✅ Real-time process monitoring capabilities### Scenario 2: Memory Leak Pattern



This demo effectively showcases the value of Azure Monitor's process-level monitoring for identifying and troubleshooting resource consumption issues in production environments.1. **Inject memory leak**: `inject worker3 memory_leak`
2. **Monitor memory growth**: Watch terminal for "🧠 Allocated 10MB" messages
3. **Query memory metrics**: Use memory PromQL query to see increasing usage
4. **Demonstrate alerting**: Set up alerts for memory growth patterns

### Scenario 3: Process Identification

1. **Start all workers** and verify distinct process names appear in metrics
2. **Use process.command dimension** to distinguish between workers
3. **Demonstrate filtering** by process owner (`azureuser`) vs system processes
4. **Show process lifecycle** - start, spike, recover, stop

### Scenario 4: Real-World Troubleshooting

Perfect for demonstrating how to identify "which Python process is causing issues":

1. **Multiple Python processes** running on same VM
2. **One misbehaving process** consuming excessive resources  
3. **Clear identification** using process names and PromQL queries
4. **Actionable insights** for remediation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│          manager_improved.py                    │
│  (Orchestrator & Interactive Control)           │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│worker1_  │ │worker2_  │ │worker3_  │
│improved  │ │improved  │ │improved  │
│Port:8001 │ │Port:8002 │ │Port:8003 │
└──────────┘ └──────────┘ └──────────┘
     │            │            │
     └────────────┴────────────┘
                  │
                  ▼
     ┌─────────────────────────┐
     │  OpenTelemetry Collector│
     │  (Host Metrics Receiver)│
     └────────────┬────────────┘
                  │
                  ▼
          ┌──────────────┐
          │ Azure Monitor│
          └──────────────┘
```

## 🔍 Worker Process Details

Each worker process:
- Runs independently with its own PID
- Exposes HTTP endpoints on different ports (8001, 8002, 8003)
- Can be monitored individually via process metrics
- Accepts failure injection commands
- Performs normal work when no failures are active

### HTTP Endpoints

Each worker exposes:
- `GET /health` - Returns health status and current failures
- `GET /status` - Returns worker name, PID, and failure state
- `POST /inject-failure` - Injects a specific failure type
- `POST /clear-failures` - Clears all active failures

## 📝 Troubleshooting

### Workers Not Starting

- Ensure Python 3.7+ is installed: `python3 --version`
- Check if ports 8001-8003 are available: `netstat -tuln | grep 800`
- Verify you have the `requests` library: `pip install requests`

### Health Checks Failing

- Wait a few seconds after starting for workers to initialize
- Check if worker processes are running: `ps aux | grep worker_process`
- Verify no firewall blocking localhost connections

### Metrics Not Appearing

- Verify OpenTelemetry Collector is running and configured correctly
- Check that the collector is monitoring Python processes
- Ensure the Azure Monitor connection string is valid
- Review collector logs for any errors

## 🤝 Contributing

This is a demo application for educational purposes. Feel free to:
- Add more worker processes
- Implement additional failure modes
- Enhance the monitoring capabilities
- Improve the documentation

## 📄 License

This project is provided as-is for demonstration purposes.

## 🔗 Related Resources

### **Essential Reading**
- [📊 Performance counters and OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-monitor/metrics/metrics-opentelemetry-guest) - Understanding what performance counters are and how they work
- [⚙️ Collect performance counters with Data Collection Rules](https://learn.microsoft.com/en-us/azure/azure-monitor/vm/data-collection-performance?tabs=OpenTelemetry) - Step-by-step DCR setup guide

### **Additional Resources**
- [Azure Monitor Agent Overview](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/agents-overview)
- [Azure Monitor Agent Installation](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-install)
- [OpenTelemetry in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)
- [Data Collection Rules](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-collection-rule-overview)