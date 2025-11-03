# Process Monitoring Demo Application - Project Summary

## 🎯 Project Objective

Build a basic application that demonstrates per-process monitoring capabilities using Azure Monitor Agent with OpenTelemetry Collector. The application allows users to showcase how process-level metrics can identify which specific process is causing failures in a multi-process environment.

## ✅ Implementation Complete

All requirements from the problem statement have been successfully implemented.

### Requirements Met

1. ✅ **2-3 Processes Running Side-by-Side** 
   - Implemented 3 independent worker processes
   - All running in a single VM environment
   - Each process has unique PID and HTTP endpoint

2. ✅ **Initialize Failures for Processes**
   - CPU spike injection
   - Memory leak injection
   - I/O heavy load injection
   - Process crash injection
   - HTTP API for failure control

3. ✅ **OpenTelemetry Collector Compatibility**
   - Configuration for Host Metrics Receiver
   - Process-level metric collection (process.cpu.*, process.memory.*, process.disk.*)
   - Azure Monitor Agent integration ready

4. ✅ **Visual Identification of Problem Processes**
   - Health status dashboard
   - Kusto queries for Azure Monitor
   - Clear differentiation between healthy/unhealthy processes

5. ✅ **Demo-Ready Application**
   - Interactive mode for live demos
   - Automated quick demo mode
   - Comprehensive documentation
   - Example outputs and visualization guides

## 📦 Deliverables

### Core Application (3 Python Scripts)

1. **worker_process.py** (199 lines)
   - Independent worker process
   - Simulates normal workload
   - Injects configurable failures
   - HTTP endpoints: /health, /status, /inject-failure, /clear-failures

2. **manager.py** (199 lines)
   - Orchestrates 3 worker processes
   - Interactive CLI interface
   - Real-time health monitoring
   - Failure injection control

3. **quick_demo.py** (132 lines)
   - Automated demonstration mode
   - Runs through all scenarios
   - Self-contained and non-interactive
   - Perfect for presentations

### Testing & Validation

4. **test_demo.sh** (72 lines)
   - Automated test suite
   - Validates all endpoints
   - Tests all failure types
   - Returns success/failure status

### Documentation (5 Files, ~1,650 lines)

5. **README.md** (233 lines)
   - Project overview
   - Quick start guide
   - Usage instructions
   - Architecture diagram
   - Demo scenarios

6. **SETUP_GUIDE.md** (372 lines)
   - VM preparation steps
   - OpenTelemetry Collector installation
   - Azure Monitor configuration
   - Systemd service setup
   - Troubleshooting guide

7. **azure-monitor-queries.md** (257 lines)
   - 15+ Kusto queries
   - Failure detection queries
   - Alert rule examples
   - Dashboard queries
   - Visualization examples

8. **EXAMPLE_OUTPUTS.md** (277 lines)
   - Application output examples
   - Azure Monitor query results
   - Dashboard mockups
   - API response examples
   - Demo presentation timeline

9. **otel-collector-config.yaml** (94 lines)
   - Complete OpenTelemetry Collector configuration
   - Host Metrics Receiver setup
   - Azure Monitor exporter configuration
   - Process filtering examples

### Configuration

10. **requirements.txt**
    - Single dependency: requests>=2.25.0
    - Minimal external dependencies

11. **.gitignore**
    - Python artifacts
    - Virtual environments
    - Temporary files
    - IDE files

## 🔧 Technical Implementation

### Architecture

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

### Failure Types Implemented

| Type | Effect | Metrics Impacted |
|------|--------|------------------|
| cpu_spike | High CPU usage | process.cpu.utilization, process.cpu.time |
| memory_leak | Continuous memory allocation | process.memory.usage, process.memory.virtual |
| io_heavy | Intensive file I/O | process.disk.io, process.disk.operations |
| crash | Process termination | Process disappears from metrics |

### HTTP API Endpoints

Each worker exposes:
- `GET /health` - Health status with failure state
- `GET /status` - Worker info and PID
- `POST /inject-failure` - Inject failure type
- `POST /clear-failures` - Clear all failures

## 🧪 Testing & Validation

### Automated Tests
- ✅ Worker process startup
- ✅ Health endpoint responses
- ✅ Failure injection (all 4 types)
- ✅ Status checking
- ✅ Failure clearing
- ✅ Multi-worker scenarios

### Code Quality
- ✅ Code review passed (2 minor issues addressed)
- ✅ CodeQL security scan: 0 vulnerabilities
- ✅ All functionality tested
- ✅ Documentation verified

## 📊 Demo Scenarios

### Scenario 1: CPU Spike Detection
1. Start application
2. Inject CPU spike into worker1
3. Monitor process.cpu.utilization
4. Observe worker1 at 85%+ while others at ~12%

### Scenario 2: Memory Leak Detection
1. Inject memory leak into worker2
2. Monitor process.memory.usage over time
3. Observe continuous memory growth in worker2

### Scenario 3: I/O Bottleneck
1. Inject I/O heavy load into worker3
2. Monitor process.disk.io
3. Observe high disk activity in worker3

### Scenario 4: Multiple Concurrent Failures
1. Inject different failures into each worker
2. Compare metrics side-by-side
3. Demonstrate clear identification of each issue

## 🚀 Usage

### Quick Start (< 5 minutes)

```bash
# Clone repository
git clone https://github.com/tylerkight/IgniteDemoforVMProcessMonitoring.git
cd IgniteDemoforVMProcessMonitoring

# Install dependencies
pip install requests

# Run automated demo
python3 quick_demo.py
```

### Interactive Demo

```bash
# Start interactive manager
python3 manager.py

# Use CLI commands
Command> health
Command> inject worker1 cpu_spike
Command> inject worker2 memory_leak
Command> health
Command> quit
```

## 📈 Metrics Collection

The application is designed to be monitored by OpenTelemetry Collector's Host Metrics Receiver, which collects:

- `process.cpu.time` - CPU time used by process
- `process.cpu.utilization` - CPU usage percentage
- `process.memory.usage` - Physical memory used
- `process.memory.virtual` - Virtual memory used
- `process.disk.io` - Disk I/O bytes
- `process.disk.operations` - Disk operation count
- `process.threads` - Thread count

## 🎓 Learning Outcomes

Users of this demo will learn:
1. How to monitor multiple processes on a single VM
2. How to identify problematic processes using metrics
3. How OpenTelemetry Collector captures process metrics
4. How to query and visualize metrics in Azure Monitor
5. How to set up alerts for process-level issues

## 🔍 Use Cases

This demo is applicable to:
- Microservices running on same VM
- Multiple worker processes (job queues, batch processing)
- Multi-tenant applications
- Service mesh monitoring
- Container-less deployments
- Legacy application monitoring

## 📝 Documentation Quality

All documentation includes:
- Clear step-by-step instructions
- Code examples
- Troubleshooting sections
- Visual examples
- Real-world use cases

## 🎯 Success Criteria - All Met

✅ Application runs 2-3 processes simultaneously  
✅ Failure injection works for all types  
✅ Compatible with Azure Monitor Agent + OpenTelemetry  
✅ Provides visual identification of problem processes  
✅ Serves as effective demo for new users  
✅ Comprehensive documentation provided  
✅ Zero security vulnerabilities  
✅ Production-ready code quality  

## 🏆 Project Status

**STATUS: COMPLETE AND READY FOR USE**

The application is fully functional, tested, documented, and ready to be deployed for demonstrations of per-process monitoring with Azure Monitor.

---

**Repository:** tylerkight/IgniteDemoforVMProcessMonitoring  
**Branch:** copilot/add-process-monitoring-demo  
**Files Changed:** 11 files  
**Total Lines:** ~2,300 lines (code + docs)  
**Commits:** 4 commits  
**Last Updated:** 2025-11-03
