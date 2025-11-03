# Example Output and Monitoring Views

This document shows example outputs from the demo application and what you would see in Azure Monitor.

## Application Output Examples

### 1. Quick Demo Output

```
======================================================================
  PROCESS MONITORING DEMO APPLICATION
  Showcasing per-process monitoring with Azure Monitor
======================================================================

======================================================================
  Starting Worker Processes
======================================================================
  Starting worker1 on port 8001...
  Starting worker2 on port 8002...
  Starting worker3 on port 8003...
  ✓ All 3 workers started!

======================================================================
  Worker Health Status
======================================================================
  worker1    | ✓ HEALTHY                                | PID: 1234
  worker2    | ✓ HEALTHY                                | PID: 1235
  worker3    | ✓ HEALTHY                                | PID: 1236

======================================================================
  Scenario 1: CPU Spike in worker1
======================================================================
  ✓ Injected 'cpu_spike' into worker1

======================================================================
  Worker Health Status
======================================================================
  worker1    | ⚠ FAILURES: cpu_spike                    | PID: 1234
  worker2    | ✓ HEALTHY                                | PID: 1235
  worker3    | ✓ HEALTHY                                | PID: 1236
```

### 2. Interactive Manager Output

```
============================================================
PROCESS MONITORING DEMO - INTERACTIVE MODE
============================================================

Available commands:
  health              - Check health of all workers
  inject <worker> <type> - Inject failure into worker
  clear <worker>      - Clear all failures from worker
  quit                - Stop all workers and exit
============================================================

Command> health

============================================================
WORKER HEALTH STATUS
============================================================
worker1    [✓ HEALTHY   ] PID: 5432
worker2    [✓ HEALTHY   ] PID: 5433
worker3    [✓ HEALTHY   ] PID: 5434
============================================================

Command> inject worker1 cpu_spike
✓ Successfully injected 'cpu_spike' into worker1

Command> health

============================================================
WORKER HEALTH STATUS
============================================================
worker1    [✓ HEALTHY   ] PID: 5432
           └─ Active failures: cpu_spike
worker2    [✓ HEALTHY   ] PID: 5433
worker3    [✓ HEALTHY   ] PID: 5434
============================================================
```

## Azure Monitor Views

### 3. Process CPU Utilization Query Result

```kusto
customMetrics
| where name == "process.cpu.utilization"
| where timestamp > ago(5m)
| summarize avg(value) by tostring(customDimensions.process_command)
```

**Results:**
| process_command              | avg_value |
|------------------------------|-----------|
| python3 worker_process.py    | 85.4%     | ← worker1 (CPU spike)
| python3 worker_process.py    | 12.3%     | ← worker2 (normal)
| python3 worker_process.py    | 11.8%     | ← worker3 (normal)

### 4. Process Memory Usage Over Time

```kusto
customMetrics
| where name == "process.memory.usage"
| where timestamp > ago(15m)
| summarize avg(value) by bin(timestamp, 1m), tostring(customDimensions.process_pid)
```

**Chart Output:**
```
Memory (MB)
  500 |                                           ●●●●●●
  400 |                                   ●●●●●●●
  300 |                           ●●●●●●●              worker2 (memory leak)
  200 |                   ●●●●●●●
  100 | ══════════════════                        worker1, worker3 (normal)
    0 |_________________________________________________
      0m    2m    4m    6m    8m   10m   12m   14m
```

### 5. Side-by-Side Process Comparison

```kusto
customMetrics
| where name in ("process.cpu.utilization", "process.memory.usage")
| where timestamp > ago(5m)
| extend processName = tostring(customDimensions.process_pid)
| summarize avg(value) by name, processName
| evaluate pivot(name)
```

**Results:**
| PID  | Worker  | CPU %  | Memory (MB) | Status      |
|------|---------|--------|-------------|-------------|
| 1234 | worker1 | 89.2   | 145         | CPU spike   |
| 1235 | worker2 | 12.1   | 387         | Memory leak |
| 1236 | worker3 | 11.5   | 142         | Normal      |

### 6. Azure Monitor Workbook View

```
┌─────────────────────────────────────────────────────────────┐
│  Process Monitoring Dashboard                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📊 CPU Utilization by Process (Last 15 minutes)            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ worker1 ████████████████████████████████ 85%          │  │
│  │ worker2 ████ 12%                                       │  │
│  │ worker3 ███ 11%                                        │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  💾 Memory Usage Trend                                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 400MB ┤                              ╭─── worker2      │  │
│  │ 300MB ┤                      ╭───────╯                 │  │
│  │ 200MB ┤              ╭───────╯                         │  │
│  │ 100MB ┼──────────────────────────────── worker1,3      │  │
│  │   0MB ┴────────────────────────────────────────────    │  │
│  │       0m    5m    10m   15m                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ⚠️  Active Alerts                                           │
│  • worker1: High CPU usage detected (85%)                   │
│  • worker2: Memory leak pattern detected (growth: 250MB)   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## REST API Examples

### 7. Health Check Response

```bash
$ curl http://localhost:8001/health
```

```json
{
  "status": "healthy",
  "failures": {
    "cpu_spike": false,
    "memory_leak": false,
    "crash": false,
    "io_heavy": false
  },
  "pid": 5432,
  "name": "worker1"
}
```

### 8. Failure Injection

```bash
$ curl -X POST http://localhost:8001/inject-failure \
  -H "Content-Type: application/json" \
  -d '{"type":"cpu_spike"}'
```

```json
{
  "success": true,
  "message": "Injected cpu_spike failure",
  "worker": "worker1"
}
```

### 9. Status After Failure

```bash
$ curl http://localhost:8001/status
```

```json
{
  "worker_name": "worker1",
  "pid": 5432,
  "failure_state": {
    "cpu_spike": true,
    "memory_leak": false,
    "crash": false,
    "io_heavy": false
  }
}
```

## Demo Presentation Timeline

### Typical 10-Minute Demo Flow

**Minute 0-2: Setup**
- Start demo: `python3 quick_demo.py` or `python3 manager.py`
- Show all workers are healthy
- Explain the architecture (3 processes, 1 VM)

**Minute 2-4: Scenario 1 - CPU Spike**
- Inject CPU spike into worker1
- Show Azure Monitor query for CPU utilization
- Point out worker1's high CPU vs others

**Minute 4-6: Scenario 2 - Memory Leak**
- Inject memory leak into worker2
- Show memory usage trend over time
- Highlight increasing memory pattern

**Minute 6-8: Scenario 3 - I/O Heavy**
- Inject I/O heavy load into worker3
- Show disk I/O metrics
- Compare all three workers side-by-side

**Minute 8-10: Summary**
- Show comprehensive dashboard view
- Explain how OpenTelemetry Collector captured metrics
- Discuss practical use cases
- Answer questions

## Key Talking Points

1. **Per-Process Visibility**
   - "Notice how we can distinguish between three Python processes on the same VM"
   - "Each process has unique PID that we track in metrics"

2. **Failure Detection**
   - "worker1 shows 85% CPU while others are at 12% - clear anomaly"
   - "worker2's memory grows from 150MB to 400MB in 10 minutes"

3. **No Code Changes**
   - "Application doesn't need any instrumentation"
   - "OpenTelemetry Collector's Host Metrics Receiver does all the work"

4. **Azure Integration**
   - "Metrics flow automatically to Application Insights"
   - "Use standard Kusto queries to analyze"
   - "Create alerts on specific process behaviors"

5. **Real-World Applications**
   - Microservices running on same VM
   - Multiple worker processes
   - Background job processors
   - Multi-tenant applications
