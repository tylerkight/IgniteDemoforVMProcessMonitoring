# Process Monitoring Demo Application

A demo application for showcasing per-process monitoring using Azure Monitor Agent with OpenTelemetry Collector. This application runs multiple worker processes side-by-side in a single VM and allows you to inject various failure modes to demonstrate how process-level metrics can identify problematic processes.

## 📋 Overview

This demo application consists of:
- **3 Worker Processes**: Independent processes running concurrently
- **Failure Injection**: Ability to inject CPU spikes, memory leaks, I/O issues, or crashes
- **Health Monitoring**: HTTP endpoints for health checks and status
- **Interactive Control**: CLI interface to manage and trigger failures

## 🎯 Use Case

This demo is designed to showcase **per-process monitoring** scenarios where:
- Multiple services/processes run on the same VM
- One process may misbehave (high CPU, memory leak, crashes)
- You need to identify which specific process is causing problems
- OpenTelemetry Collector with Host Metrics Receiver collects process.* metrics
- Metrics are visualized in Azure Monitor or Grafana

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- `requests` library for HTTP operations

### Installation

1. Clone the repository:
```bash
git clone https://github.com/tylerkight/IgniteDemoforVMProcessMonitoring.git
cd IgniteDemoforVMProcessMonitoring
```

2. Install Python dependencies:
```bash
pip install requests
```

3. Start the demo application:
```bash
python3 manager.py
```

### Basic Usage

Once started, the application runs in interactive mode:

```bash
# Check health of all workers
Command> health

# Inject a CPU spike into worker1
Command> inject worker1 cpu_spike

# Inject a memory leak into worker2
Command> inject worker2 memory_leak

# Clear all failures from worker1
Command> clear worker1

# Check health again to see the effects
Command> health

# Exit the application
Command> quit
```

## 🔧 Available Failure Types

| Failure Type | Description | Observable Metrics |
|--------------|-------------|-------------------|
| `cpu_spike` | Causes high CPU usage | process.cpu.utilization, process.cpu.time |
| `memory_leak` | Continuously allocates memory | process.memory.usage, process.memory.virtual |
| `io_heavy` | Performs intensive I/O operations | process.disk.io, process.disk.operations |
| `crash` | Terminates the process | Process disappears from metrics |

## 📊 Setting Up OpenTelemetry Collector

To monitor these processes with Azure Monitor Agent and OpenTelemetry Collector:

### 1. Install Azure Monitor Agent

Follow the [Azure Monitor Agent installation guide](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-install) for your VM.

### 2. Configure OpenTelemetry Collector

Create a configuration file for the OpenTelemetry Collector with the Host Metrics Receiver:

```yaml
# otel-config.yaml
receivers:
  hostmetrics:
    collection_interval: 10s
    scrapers:
      process:
        include:
          names: ["python3", "python"]
        metrics:
          process.cpu.time:
            enabled: true
          process.cpu.utilization:
            enabled: true
          process.memory.usage:
            enabled: true
          process.memory.virtual:
            enabled: true
          process.memory.physical:
            enabled: true
          process.disk.io:
            enabled: true

processors:
  batch:
    timeout: 10s

exporters:
  azuremonitor:
    connection_string: "YOUR_APPLICATION_INSIGHTS_CONNECTION_STRING"

service:
  pipelines:
    metrics:
      receivers: [hostmetrics]
      processors: [batch]
      exporters: [azuremonitor]
```

### 3. Query Metrics in Azure Monitor

Once the collector is running, you can query process metrics in Azure Monitor:

```kusto
// Find processes with high CPU usage
customMetrics
| where name == "process.cpu.utilization"
| summarize avg(value) by tostring(customDimensions.process_command)
| order by avg_value desc

// Find processes with increasing memory usage
customMetrics
| where name == "process.memory.usage"
| summarize avg(value) by bin(timestamp, 1m), tostring(customDimensions.process_command)
| render timechart
```

## 🎬 Demo Scenarios

### Scenario 1: CPU Spike Detection

1. Start the application and verify all workers are healthy
2. Inject a CPU spike: `inject worker1 cpu_spike`
3. Monitor process.cpu.utilization metrics
4. Observe that worker1's CPU usage spikes significantly
5. Clear the failure: `clear worker1`

### Scenario 2: Memory Leak Detection

1. Start the application
2. Inject a memory leak: `inject worker2 memory_leak`
3. Monitor process.memory.usage metrics over time
4. Observe that worker2's memory continuously increases
5. Clear the failure or let it run to see OOM behavior

### Scenario 3: Process Crash

1. Start the application
2. Inject a crash: `inject worker3 crash`
3. Monitor process metrics
4. Observe that worker3 disappears from metrics
5. The manager will report the process has stopped

### Scenario 4: Multiple Concurrent Failures

1. Start the application
2. Inject different failures into different workers:
   - `inject worker1 cpu_spike`
   - `inject worker2 memory_leak`
   - `inject worker3 io_heavy`
3. Observe distinct metric patterns for each worker
4. Demonstrate how per-process metrics identify each issue

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              manager.py                          │
│  (Orchestrator & Interactive Control)           │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ worker1  │ │ worker2  │ │ worker3  │
│ Port:8001│ │ Port:8002│ │ Port:8003│
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

- [Azure Monitor Agent Documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/agents-overview)
- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
- [Host Metrics Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver)
- [Azure Monitor OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)