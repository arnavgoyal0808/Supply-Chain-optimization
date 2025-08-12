#!/usr/bin/env python3
"""
Comprehensive service validation for Supply Chain RL system
Checks all components for proper functionality
"""

import json
import time
import subprocess
import requests
import socket
from pathlib import Path

class ServiceValidator:
    def __init__(self):
        self.results = {}
        self.errors = []
        self.warnings = []
        
    def print_status(self, message, status="INFO"):
        colors = {
            "OK": "\033[92m✅",
            "ERROR": "\033[91m❌", 
            "WARNING": "\033[93m⚠️",
            "INFO": "\033[94mℹ️"
        }
        reset = "\033[0m"
        print(f"{colors.get(status, colors['INFO'])} {message}{reset}")
        
    def check_file_structure(self):
        """Validate all required files exist"""
        self.print_status("Checking file structure...", "INFO")
        
        required_files = [
            "docker-compose.yml",
            "edge_agent/edge_inference.py",
            "edge_agent/create_demo_model.py", 
            "iot_simulator/truck_simulator.py",
            "dashboard/src/App.js",
            "mosquitto/config/mosquitto.conf"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
                
        if not missing_files:
            self.print_status("All required files present", "OK")
            return True
        else:
            for file in missing_files:
                self.print_status(f"Missing file: {file}", "ERROR")
            return False
    
    def check_docker_status(self):
        """Check if Docker is available and running"""
        self.print_status("Checking Docker status...", "INFO")
        
        try:
            # Check if docker command exists
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                self.print_status("Docker not installed", "ERROR")
                return False
                
            # Check if Docker daemon is running
            result = subprocess.run(['docker', 'info'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                self.print_status("Docker daemon not running", "ERROR")
                return False
                
            self.print_status("Docker is available and running", "OK")
            return True
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.print_status("Docker not available", "ERROR")
            return False
    
    def check_docker_compose_services(self):
        """Check Docker Compose services status"""
        self.print_status("Checking Docker Compose services...", "INFO")
        
        try:
            # Get service status
            result = subprocess.run(['docker-compose', 'ps'], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                self.print_status("Docker Compose not available or no services", "ERROR")
                return False
            
            # Parse output to check service status
            lines = result.stdout.strip().split('\n')
            services = ['mosquitto', 'iot-simulator', 'edge-agent', 'dashboard']
            
            running_services = []
            for line in lines:
                for service in services:
                    if service in line and 'Up' in line:
                        running_services.append(service)
                        
            for service in services:
                if service in running_services:
                    self.print_status(f"{service} container is running", "OK")
                else:
                    self.print_status(f"{service} container not running", "ERROR")
            
            return len(running_services) == len(services)
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.print_status("Cannot check Docker Compose services", "ERROR")
            return False
    
    def check_port_connectivity(self):
        """Check if required ports are accessible"""
        self.print_status("Checking port connectivity...", "INFO")
        
        ports = {
            3000: "Dashboard",
            8080: "Edge Agent API", 
            1883: "MQTT Broker",
            9001: "MQTT WebSocket"
        }
        
        accessible_ports = 0
        for port, service in ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                self.print_status(f"{service} (port {port}) is accessible", "OK")
                accessible_ports += 1
            else:
                self.print_status(f"{service} (port {port}) not accessible", "ERROR")
        
        return accessible_ports == len(ports)
    
    def check_api_endpoints(self):
        """Test API endpoints for functionality"""
        self.print_status("Testing API endpoints...", "INFO")
        
        endpoints = {
            "http://localhost:8080/api/health": "Edge Agent Health",
            "http://localhost:8080/api/trucks": "Truck Data",
            "http://localhost:8080/api/actions": "RL Actions"
        }
        
        working_endpoints = 0
        for url, description in endpoints.items():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.print_status(f"{description} API working", "OK")
                    working_endpoints += 1
                else:
                    self.print_status(f"{description} API returned {response.status_code}", "ERROR")
            except requests.RequestException:
                self.print_status(f"{description} API not responding", "ERROR")
        
        return working_endpoints > 0
    
    def check_mqtt_functionality(self):
        """Test MQTT broker functionality"""
        self.print_status("Testing MQTT broker...", "INFO")
        
        try:
            # Test MQTT publish
            result = subprocess.run([
                'docker', 'exec', 'mqtt-broker', 
                'mosquitto_pub', '-h', 'localhost', 
                '-t', 'test/health', '-m', 'health_check'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.print_status("MQTT broker accepts messages", "OK")
                return True
            else:
                self.print_status("MQTT broker test failed", "ERROR")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.print_status("Cannot test MQTT broker", "ERROR")
            return False
    
    def check_data_flow(self):
        """Check if data is flowing between components"""
        self.print_status("Checking data flow...", "INFO")
        
        try:
            # Check if truck data is being generated
            response = requests.get("http://localhost:8080/api/trucks", timeout=5)
            if response.status_code == 200:
                trucks = response.json()
                if trucks and len(trucks) > 0:
                    self.print_status(f"Truck data flowing: {len(trucks)} trucks active", "OK")
                    
                    # Check if actions are being generated
                    time.sleep(2)  # Wait for some actions
                    response = requests.get("http://localhost:8080/api/actions", timeout=5)
                    if response.status_code == 200:
                        actions = response.json()
                        if actions and len(actions) > 0:
                            self.print_status(f"RL actions being generated: {len(actions)} actions", "OK")
                            return True
                        else:
                            self.print_status("No RL actions detected yet", "WARNING")
                            return False
                else:
                    self.print_status("No truck data available", "ERROR")
                    return False
            else:
                self.print_status("Cannot access truck data API", "ERROR")
                return False
                
        except requests.RequestException:
            self.print_status("Cannot check data flow", "ERROR")
            return False
    
    def check_dashboard_accessibility(self):
        """Check if dashboard is accessible"""
        self.print_status("Checking dashboard accessibility...", "INFO")
        
        try:
            response = requests.get("http://localhost:3000", timeout=10)
            if response.status_code == 200:
                if "Supply Chain" in response.text or "React" in response.text:
                    self.print_status("Dashboard is accessible and loading", "OK")
                    return True
                else:
                    self.print_status("Dashboard accessible but content unclear", "WARNING")
                    return False
            else:
                self.print_status(f"Dashboard returned status {response.status_code}", "ERROR")
                return False
                
        except requests.RequestException:
            self.print_status("Dashboard not accessible", "ERROR")
            return False
    
    def run_comprehensive_check(self):
        """Run all validation checks"""
        print("🏥 Supply Chain RL System - Comprehensive Service Validation")
        print("=" * 60)
        print()
        
        checks = [
            ("File Structure", self.check_file_structure),
            ("Docker Status", self.check_docker_status),
            ("Docker Services", self.check_docker_compose_services),
            ("Port Connectivity", self.check_port_connectivity),
            ("API Endpoints", self.check_api_endpoints),
            ("MQTT Functionality", self.check_mqtt_functionality),
            ("Data Flow", self.check_data_flow),
            ("Dashboard Access", self.check_dashboard_accessibility)
        ]
        
        passed_checks = 0
        total_checks = len(checks)
        
        for check_name, check_func in checks:
            print(f"\n📋 {check_name}")
            print("-" * 30)
            
            try:
                if check_func():
                    passed_checks += 1
            except Exception as e:
                self.print_status(f"Check failed with error: {str(e)}", "ERROR")
        
        print("\n" + "=" * 60)
        print(f"🎯 VALIDATION SUMMARY")
        print("=" * 60)
        
        if passed_checks == total_checks:
            self.print_status(f"All checks passed! ({passed_checks}/{total_checks})", "OK")
            print("\n🎉 System is fully operational!")
            print("\n📱 Access Points:")
            print("   🌐 Dashboard: http://localhost:3000")
            print("   🤖 Edge Agent: http://localhost:8080/api/health")
            print("   📊 Truck Data: http://localhost:8080/api/trucks")
            
        elif passed_checks >= total_checks * 0.7:
            self.print_status(f"Most checks passed ({passed_checks}/{total_checks})", "WARNING")
            print("\n⚠️  System is mostly working but has some issues")
            
        else:
            self.print_status(f"Multiple failures ({passed_checks}/{total_checks})", "ERROR")
            print("\n❌ System has significant issues")
            
        print("\n🔧 Troubleshooting:")
        print("   docker-compose logs -f     # View all logs")
        print("   docker-compose ps          # Check container status")
        print("   ./health_check.sh          # Run detailed health check")
        
        return passed_checks == total_checks

def main():
    validator = ServiceValidator()
    return validator.run_comprehensive_check()

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
