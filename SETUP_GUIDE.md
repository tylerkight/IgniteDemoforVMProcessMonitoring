# Setup and Deployment Guide

This guide provides step-by-step instructions for setting up the Process Monitoring Demo application on a VM with Azure Monitor Agent and OpenTelemetry Collector.

## Table of Contents
1. [VM Preparation](#vm-preparation)
2. [Application Setup](#application-setup)
3. [OpenTelemetry Collector Setup](#opentelemetry-collector-setup)
4. [Azure Monitor Configuration](#azure-monitor-configuration)
5. [Running the Demo](#running-the-demo)
6. [Verification](#verification)

## VM Preparation

### System Requirements
- Operating System: Linux (Ubuntu 20.04+ recommended) or Windows Server
- Python: 3.7 or higher
- RAM: 2GB minimum (4GB recommended)
- CPU: 2 cores minimum
- Network: Outbound HTTPS access to Azure

### Install Prerequisites

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
```

#### On RHEL/CentOS:
```bash
sudo yum install -y python3 python3-pip git
```

#### On Windows:
1. Download and install Python 3.7+ from python.org
2. Install Git for Windows
3. Add Python to PATH

## Application Setup

### 1. Clone the Repository

```bash
# Clone the demo application
git clone https://github.com/tylerkight/IgniteDemoforVMProcessMonitoring.git
cd IgniteDemoforVMProcessMonitoring
```

### 2. Install Python Dependencies

```bash
# Install required Python packages
pip3 install -r requirements.txt
```

### 3. Verify Installation

```bash
# Check Python version
python3 --version

# Test worker process help
python3 worker_process.py --help

# Verify manager script exists
python3 -c "import os; assert os.path.exists('manager.py')"
```

## OpenTelemetry Collector Setup

### 1. Install OpenTelemetry Collector

#### Using Azure Monitor Agent (Recommended):

Follow the official documentation:
https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-install

The Azure Monitor Agent includes OpenTelemetry Collector capabilities.

#### Standalone Installation (Alternative):

```bash
# Download OpenTelemetry Collector Contrib (includes hostmetrics receiver)
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.88.0/otelcol-contrib_0.88.0_linux_amd64.tar.gz

# Extract
tar -xzf otelcol-contrib_0.88.0_linux_amd64.tar.gz

# Move to system location
sudo mv otelcol-contrib /usr/local/bin/
```

### 2. Configure OpenTelemetry Collector

```bash
# Copy the sample configuration
cp otel-collector-config.yaml /etc/otelcol/config.yaml

# Edit the configuration to add your Application Insights connection string
sudo nano /etc/otelcol/config.yaml
```

Update the connection string:
```yaml
exporters:
  azuremonitor:
    connection_string: "InstrumentationKey=YOUR-KEY-HERE;IngestionEndpoint=https://YOUR-REGION.in.applicationinsights.azure.com/"
```

### 3. Set Environment Variable (Alternative)

```bash
# Set the connection string as an environment variable
export APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=YOUR-KEY-HERE;..."
```

### 4. Create Systemd Service (Linux)

```bash
# Create service file
sudo cat > /etc/systemd/system/otelcol.service << 'EOF'
[Unit]
Description=OpenTelemetry Collector
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/otelcol-contrib --config=/etc/otelcol/config.yaml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable otelcol
sudo systemctl start otelcol

# Check status
sudo systemctl status otelcol
```

## Azure Monitor Configuration

### 1. Create Application Insights Resource

```bash
# Using Azure CLI
az monitor app-insights component create \
  --app process-monitoring-demo \
  --location eastus \
  --resource-group your-resource-group \
  --application-type web

# Get the connection string
az monitor app-insights component show \
  --app process-monitoring-demo \
  --resource-group your-resource-group \
  --query connectionString -o tsv
```

### 2. Configure Data Collection

The OpenTelemetry Collector will automatically send metrics to Application Insights using the connection string.

### 3. Verify Data Flow

```bash
# Check OpenTelemetry Collector logs
sudo journalctl -u otelcol -f

# Or if running standalone
tail -f /var/log/otelcol.log
```

## Running the Demo

### 1. Start the Demo Application

#### Option A: Foreground (for testing)
```bash
python3 manager.py
```

#### Option B: Background (for demos)
```bash
# Start in background
nohup python3 manager.py > demo-app.log 2>&1 &

# Check if running
ps aux | grep manager.py
```

#### Option C: Systemd Service (production-like)
```bash
# Create service file
sudo cat > /etc/systemd/system/process-demo.service << 'EOF'
[Unit]
Description=Process Monitoring Demo Application
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/IgniteDemoforVMProcessMonitoring
ExecStart=/usr/bin/python3 manager.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable process-demo
sudo systemctl start process-demo
```

### 2. Verify Workers are Running

```bash
# Check for worker processes
ps aux | grep worker_process

# Test health endpoints
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### 3. Interact with the Application

If running in foreground, use the interactive commands:
```bash
Command> health
Command> inject worker1 cpu_spike
Command> inject worker2 memory_leak
```

If running in background, use curl:
```bash
# Inject CPU spike into worker1
curl -X POST http://localhost:8001/inject-failure \
  -H "Content-Type: application/json" \
  -d '{"type":"cpu_spike"}'

# Inject memory leak into worker2
curl -X POST http://localhost:8002/inject-failure \
  -H "Content-Type: application/json" \
  -d '{"type":"memory_leak"}'

# Clear failures
curl -X POST http://localhost:8001/clear-failures
```

## Verification

### 1. Verify Process Metrics Collection

Wait 1-2 minutes after starting the application, then check Azure Monitor:

```bash
# Using Azure CLI
az monitor app-insights metrics show \
  --app process-monitoring-demo \
  --resource-group your-resource-group \
  --metrics "customMetrics/process.cpu.utilization"
```

Or navigate to Application Insights in Azure Portal:
- Go to Application Insights > Logs
- Run query: `customMetrics | where name startswith "process."`

### 2. Verify Failure Injection

1. Inject a CPU spike:
   ```bash
   curl -X POST http://localhost:8001/inject-failure \
     -H "Content-Type: application/json" \
     -d '{"type":"cpu_spike"}'
   ```

2. Wait 1-2 minutes

3. Query Azure Monitor:
   ```kusto
   customMetrics
   | where name == "process.cpu.utilization"
   | where timestamp > ago(5m)
   | summarize avg(value) by tostring(customDimensions.process_command)
   ```

4. You should see increased CPU usage for the affected worker

## Troubleshooting

### Application Issues

**Workers not starting:**
```bash
# Check Python installation
python3 --version

# Check for port conflicts
netstat -tuln | grep -E '8001|8002|8003'

# Run in foreground to see errors
python3 manager.py
```

**Health checks failing:**
```bash
# Check if workers are running
ps aux | grep worker_process

# Check worker logs
# (If using systemd)
sudo journalctl -u process-demo -f
```

### OpenTelemetry Collector Issues

**Collector not starting:**
```bash
# Check configuration syntax
/usr/local/bin/otelcol-contrib --config=/etc/otelcol/config.yaml --dry-run

# Check logs
sudo journalctl -u otelcol -n 50
```

**No metrics in Azure:**
```bash
# Verify connection string
echo $APPLICATIONINSIGHTS_CONNECTION_STRING

# Check network connectivity
curl https://dc.services.visualstudio.com/v2/track

# Enable debug logging in config.yaml
exporters:
  logging:
    verbosity: detailed
```

**Metrics not showing up:**
```bash
# Verify process names in collector config match actual process names
ps aux | grep python

# Check that Python processes are included in the collector config
# The config should include "python3" or "python" in the include list
```

### Azure Monitor Issues

**Connection string errors:**
- Verify the connection string format
- Check that the Application Insights resource exists
- Ensure the VM has outbound HTTPS access

**No data appearing:**
- Wait 2-5 minutes for initial data ingestion
- Check Application Insights ingestion endpoint health
- Verify the collector is sending data (check logs)

## Demo Presentation Tips

1. **Setup Before Demo:**
   - Start application 5-10 minutes before demo
   - Verify metrics are flowing to Azure Monitor
   - Prepare Azure Monitor queries in advance
   - Open Application Insights dashboard

2. **Demo Flow:**
   - Show normal operation (all workers healthy)
   - Inject failure into one worker
   - Wait 1-2 minutes for metrics to reflect
   - Show Azure Monitor graphs highlighting the problem
   - Clear failure and show recovery

3. **Key Points to Highlight:**
   - Multiple processes running on same VM
   - Per-process metrics visibility
   - Quick identification of problematic process
   - No application code changes needed
   - Standard OpenTelemetry approach

## Additional Resources

- [Azure Monitor Documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/)
- [OpenTelemetry Collector Documentation](https://opentelemetry.io/docs/collector/)
- [Host Metrics Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver)
- [Application Insights Overview](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)

## Support

For issues or questions about this demo:
1. Check the troubleshooting section above
2. Review OpenTelemetry Collector logs
3. Verify Azure Monitor configuration
4. Open an issue in the GitHub repository
