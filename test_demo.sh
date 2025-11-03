#!/bin/bash
# Test script for the process monitoring demo application

set -e

echo "=== Process Monitoring Demo Test ==="
echo ""

# Start workers in background
echo "Starting worker processes..."
python3 worker_process.py --name worker1 --port 8001 > /tmp/worker1.log 2>&1 &
W1_PID=$!
python3 worker_process.py --name worker2 --port 8002 > /tmp/worker2.log 2>&1 &
W2_PID=$!
python3 worker_process.py --name worker3 --port 8003 > /tmp/worker3.log 2>&1 &
W3_PID=$!

echo "Workers started: PID $W1_PID, $W2_PID, $W3_PID"
echo "Waiting for workers to initialize..."
sleep 5

# Cleanup function
cleanup() {
    echo ""
    echo "Cleaning up workers..."
    kill $W1_PID $W2_PID $W3_PID 2>/dev/null || true
    sleep 1
    pkill -9 -f worker_process 2>/dev/null || true
}

trap cleanup EXIT

# Test 1: Health checks
echo ""
echo "=== Test 1: Health Checks ==="
for port in 8001 8002 8003; do
    echo "Testing worker on port $port..."
    curl -sf http://localhost:$port/health || echo "FAILED"
done

# Test 2: Inject CPU spike
echo ""
echo "=== Test 2: Inject CPU Spike into worker1 ==="
curl -sf -X POST http://localhost:8001/inject-failure \
    -H "Content-Type: application/json" \
    -d '{"type":"cpu_spike"}' | python3 -m json.tool

sleep 2

# Check status
echo ""
echo "Worker1 status after CPU spike:"
curl -sf http://localhost:8001/status | python3 -m json.tool

# Test 3: Inject memory leak
echo ""
echo "=== Test 3: Inject Memory Leak into worker2 ==="
curl -sf -X POST http://localhost:8002/inject-failure \
    -H "Content-Type: application/json" \
    -d '{"type":"memory_leak"}' | python3 -m json.tool

sleep 2

# Check status
echo ""
echo "Worker2 status after memory leak:"
curl -sf http://localhost:8002/status | python3 -m json.tool

# Test 4: Clear failures
echo ""
echo "=== Test 4: Clear Failures from worker1 ==="
curl -sf -X POST http://localhost:8001/clear-failures | python3 -m json.tool

sleep 1

echo ""
echo "Worker1 status after clearing:"
curl -sf http://localhost:8001/status | python3 -m json.tool

echo ""
echo "=== All Tests Passed! ==="
