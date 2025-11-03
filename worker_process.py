#!/usr/bin/env python3
"""
Worker process that simulates various workloads and can inject failures.
This process is designed to be monitored by OpenTelemetry Collector with Host Metrics Receiver.
"""

import argparse
import time
import sys
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import random

# Global state for failure injection
failure_state = {
    'cpu_spike': False,
    'memory_leak': False,
    'crash': False,
    'io_heavy': False
}

memory_ballast = []


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP handler for health checks and failure injection."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def do_GET(self):
        """Handle GET requests for health check."""
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'failures': failure_state,
                'pid': os.getpid(),
                'name': worker_name
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'worker_name': worker_name,
                'pid': os.getpid(),
                'failure_state': failure_state
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for failure injection."""
        if self.path == '/inject-failure':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode())
                failure_type = data.get('type', '')
                
                if failure_type in failure_state:
                    failure_state[failure_type] = True
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'success': True,
                        'message': f'Injected {failure_type} failure',
                        'worker': worker_name
                    }
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'message': 'Invalid failure type'}
                    self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'message': str(e)}
                self.wfile.write(json.dumps(response).encode())
        elif self.path == '/clear-failures':
            failure_state['cpu_spike'] = False
            failure_state['memory_leak'] = False
            failure_state['io_heavy'] = False
            failure_state['crash'] = False
            memory_ballast.clear()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': True, 'message': 'Cleared all failures'}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()


def cpu_intensive_work():
    """Perform CPU-intensive calculations."""
    result = 0
    for i in range(1000000):
        result += i * i % 997
    return result


def memory_leak_work():
    """Simulate memory leak by allocating memory."""
    # Allocate 10MB at a time
    chunk_size = 10 * 1024 * 1024
    memory_ballast.append(bytearray(chunk_size))


def io_intensive_work():
    """Perform I/O-intensive operations."""
    temp_file = f'/tmp/worker_{worker_name}_io.tmp'
    try:
        with open(temp_file, 'w') as f:
            for i in range(1000):
                f.write(f'Line {i}: {"x" * 100}\n')
        with open(temp_file, 'r') as f:
            _ = f.read()
        os.remove(temp_file)
    except Exception as e:
        print(f"I/O error: {e}", file=sys.stderr)


def normal_work():
    """Simulate normal workload."""
    # Light CPU usage
    for _ in range(100):
        _ = random.random() * random.random()
    time.sleep(0.1)


def run_http_server(port):
    """Run HTTP server for health checks and failure injection."""
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"[{worker_name}] Health server listening on port {port}")
    server.serve_forever()


def main_worker_loop():
    """Main worker loop that performs work and handles failure injection."""
    print(f"[{worker_name}] Worker started with PID {os.getpid()}")
    iteration = 0
    
    while True:
        iteration += 1
        
        # Check for crash failure
        if failure_state['crash']:
            print(f"[{worker_name}] CRASH FAILURE INJECTED - Exiting!")
            sys.exit(1)
        
        # Perform work based on failure state
        if failure_state['cpu_spike']:
            print(f"[{worker_name}] CPU spike active (iteration {iteration})")
            # Do intensive CPU work
            for _ in range(10):
                cpu_intensive_work()
        elif failure_state['memory_leak']:
            print(f"[{worker_name}] Memory leak active (iteration {iteration})")
            memory_leak_work()
            time.sleep(0.5)
        elif failure_state['io_heavy']:
            print(f"[{worker_name}] I/O heavy load active (iteration {iteration})")
            io_intensive_work()
        else:
            # Normal operation
            if iteration % 10 == 0:
                print(f"[{worker_name}] Normal operation (iteration {iteration})")
            normal_work()


worker_name = None


def main():
    """Main entry point."""
    global worker_name
    
    parser = argparse.ArgumentParser(description='Worker process for monitoring demo')
    parser.add_argument('--name', required=True, help='Worker name (e.g., worker1)')
    parser.add_argument('--port', type=int, required=True, help='HTTP port for health checks')
    args = parser.parse_args()
    
    worker_name = args.name
    
    # Start HTTP server in background thread
    http_thread = Thread(target=run_http_server, args=(args.port,), daemon=True)
    http_thread.start()
    
    # Give server time to start
    time.sleep(1)
    
    # Run main worker loop
    try:
        main_worker_loop()
    except KeyboardInterrupt:
        print(f"\n[{worker_name}] Shutting down gracefully...")
        sys.exit(0)


if __name__ == '__main__':
    main()
