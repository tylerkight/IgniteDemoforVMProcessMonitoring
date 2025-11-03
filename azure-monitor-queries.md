# Azure Monitor Kusto Queries for Process Monitoring Demo

This file contains example Kusto queries to analyze the process metrics collected from the demo application.

## Basic Queries

### 1. List All Monitored Processes
```kusto
customMetrics
| where name startswith "process."
| summarize by tostring(customDimensions.process_command)
| order by process_command asc
```

### 2. Current CPU Utilization by Process
```kusto
customMetrics
| where name == "process.cpu.utilization"
| where timestamp > ago(5m)
| summarize avg(value) by tostring(customDimensions.process_command)
| order by avg_value desc
```

### 3. Memory Usage Over Time
```kusto
customMetrics
| where name == "process.memory.usage"
| where timestamp > ago(30m)
| extend processName = tostring(customDimensions.process_command)
| summarize avg(value) by bin(timestamp, 1m), processName
| render timechart
```

## Failure Detection Queries

### 4. Detect High CPU Usage (CPU Spike)
```kusto
customMetrics
| where name == "process.cpu.utilization"
| where timestamp > ago(15m)
| extend processName = tostring(customDimensions.process_command)
| summarize avg_cpu = avg(value), max_cpu = max(value) by processName
| where avg_cpu > 50 or max_cpu > 80
| order by avg_cpu desc
```

### 5. Detect Memory Leaks (Continuously Increasing Memory)
```kusto
customMetrics
| where name == "process.memory.usage"
| where timestamp > ago(30m)
| extend processName = tostring(customDimensions.process_command)
| summarize 
    initial_memory = min(value),
    final_memory = max(value),
    avg_memory = avg(value)
    by processName
| extend memory_increase = final_memory - initial_memory
| extend increase_percent = (memory_increase / initial_memory) * 100
| where increase_percent > 50
| order by memory_increase desc
```

### 6. Detect Process Crashes (Process Disappearance)
```kusto
let TimeWindow = 30m;
let RecentProcesses = customMetrics
    | where name startswith "process."
    | where timestamp > ago(TimeWindow)
    | extend processName = tostring(customDimensions.process_command)
    | summarize last_seen = max(timestamp) by processName;
let CurrentTime = now();
RecentProcesses
| extend minutes_since_last_seen = datetime_diff('minute', CurrentTime, last_seen)
| where minutes_since_last_seen > 5
| project processName, last_seen, minutes_since_last_seen
| order by minutes_since_last_seen desc
```

### 7. Compare Process Metrics Side-by-Side
```kusto
customMetrics
| where name in ("process.cpu.utilization", "process.memory.usage", "process.disk.io")
| where timestamp > ago(15m)
| extend processName = tostring(customDimensions.process_command)
| summarize avg(value) by name, processName
| evaluate pivot(name, avg_value)
| order by processName asc
```

## Advanced Analysis

### 8. Identify Anomalous Behavior
```kusto
customMetrics
| where name == "process.cpu.utilization"
| where timestamp > ago(1h)
| extend processName = tostring(customDimensions.process_command)
| summarize 
    avg_cpu = avg(value),
    stddev_cpu = stdev(value),
    max_cpu = max(value)
    by bin(timestamp, 5m), processName
| extend 
    upper_threshold = avg_cpu + (2 * stddev_cpu),
    is_anomaly = max_cpu > (avg_cpu + (2 * stddev_cpu))
| where is_anomaly
| project timestamp, processName, avg_cpu, max_cpu, upper_threshold
```

### 9. Resource Usage Heatmap
```kusto
customMetrics
| where name in ("process.cpu.utilization", "process.memory.usage")
| where timestamp > ago(1h)
| extend processName = tostring(customDimensions.process_command)
| summarize value = avg(value) by bin(timestamp, 1m), processName, name
| render timechart
```

### 10. Process Health Score
```kusto
let cpu_weight = 0.4;
let memory_weight = 0.4;
let io_weight = 0.2;
customMetrics
| where name in ("process.cpu.utilization", "process.memory.usage", "process.disk.io")
| where timestamp > ago(10m)
| extend processName = tostring(customDimensions.process_command)
| summarize avg(value) by name, processName
| evaluate pivot(name)
| extend health_score = 
    (coalesce(process_cpu_utilization, 0) * cpu_weight) +
    (coalesce(process_memory_usage, 0) / 1024 / 1024 / 10 * memory_weight) +
    (coalesce(process_disk_io, 0) / 1024 / 1024 * io_weight)
| project processName, health_score, process_cpu_utilization, process_memory_usage, process_disk_io
| order by health_score desc
```

## Alert Rules

### 11. Alert: High CPU Usage
```kusto
// Use this query for alert rules
customMetrics
| where name == "process.cpu.utilization"
| where timestamp > ago(5m)
| extend processName = tostring(customDimensions.process_command)
| summarize avg_cpu = avg(value) by processName
| where avg_cpu > 75
```

### 12. Alert: Memory Leak Detected
```kusto
// Use this query for alert rules
customMetrics
| where name == "process.memory.usage"
| where timestamp > ago(15m)
| extend processName = tostring(customDimensions.process_command)
| summarize 
    start_memory = min(value),
    end_memory = max(value)
    by processName
| extend growth_mb = (end_memory - start_memory) / 1024 / 1024
| where growth_mb > 100
```

### 13. Alert: Process Not Responding
```kusto
// Use this query for alert rules
let TimeWindow = 10m;
customMetrics
| where name startswith "process."
| where timestamp > ago(TimeWindow)
| extend processName = tostring(customDimensions.process_command)
| summarize last_seen = max(timestamp) by processName
| extend minutes_since = datetime_diff('minute', now(), last_seen)
| where minutes_since > 5
```

## Visualization Queries

### 14. Real-time Dashboard: Process Overview
```kusto
customMetrics
| where name in ("process.cpu.utilization", "process.memory.usage")
| where timestamp > ago(5m)
| extend processName = tostring(customDimensions.process_command)
| extend metric_type = case(
    name == "process.cpu.utilization", "CPU %",
    name == "process.memory.usage", "Memory (MB)",
    "Other"
)
| extend display_value = case(
    name == "process.memory.usage", value / 1024 / 1024,
    value
)
| summarize current_value = avg(display_value) by processName, metric_type
| order by processName, metric_type
```

### 15. Trend Analysis: Last Hour
```kusto
customMetrics
| where name == "process.cpu.utilization"
| where timestamp > ago(1h)
| extend processName = tostring(customDimensions.process_command)
| summarize avg(value) by bin(timestamp, 2m), processName
| render timechart with (title="CPU Usage Trend - Last Hour")
```

## Usage Tips

1. **Time Ranges**: Adjust `ago()` values based on your demo duration
2. **Thresholds**: Modify threshold values (e.g., CPU > 75%) based on your demo scenario
3. **Process Names**: The queries use `process_command` which will contain "python3 worker_process.py"
4. **Custom Dimensions**: Azure Monitor stores process metadata in customDimensions
5. **Rendering**: Use `| render timechart` or `| render columnchart` for visualizations

## Creating Workbooks

Combine multiple queries into an Azure Monitor Workbook:
1. Create a new Workbook in Azure Monitor
2. Add query tiles using the queries above
3. Set appropriate time ranges and auto-refresh
4. Share with your audience for live monitoring during the demo
