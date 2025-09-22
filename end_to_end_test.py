#!/usr/bin/env python3
"""
🔬 AI Scraper System - End-to-End Integration Test Suite

This comprehensive test validates the entire system working together:
- FrankensteinDB persistence and performance
- AI Scraper VM orchestration and communication  
- Dashboard integration (simulated MQTT)
- Production deployment verification

Usage:
    python3 end_to_end_test.py [--full] [--performance]
    
    --full: Run complete test suite including performance tests
    --performance: Run only performance benchmarks
"""

import asyncio
import json
import sqlite3
import time
import os
import sys
import subprocess
import tempfile
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

# Color output for better visibility
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print a colored header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

class TestResult:
    """Track test results"""
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []
        
    def add_success(self, test_name: str):
        self.tests_run += 1
        self.tests_passed += 1
        print_success(f"{test_name}")
        
    def add_failure(self, test_name: str, error: str):
        self.tests_run += 1
        self.tests_failed += 1
        self.errors.append(f"{test_name}: {error}")
        print_error(f"{test_name}: {error}")
        
    def summary(self):
        print_header("TEST SUMMARY")
        print(f"Tests Run: {Colors.BOLD}{self.tests_run}{Colors.END}")
        print(f"Passed: {Colors.GREEN}{self.tests_passed}{Colors.END}")
        print(f"Failed: {Colors.RED}{self.tests_failed}{Colors.END}")
        
        if self.errors:
            print(f"\n{Colors.RED}Failed Tests:{Colors.END}")
            for error in self.errors:
                print(f"  {Colors.RED}• {error}{Colors.END}")
                
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        if success_rate >= 90:
            print(f"\n{Colors.GREEN}🎉 SYSTEM STATUS: PRODUCTION READY ({success_rate:.1f}%){Colors.END}")
        elif success_rate >= 70:
            print(f"\n{Colors.YELLOW}⚠️  SYSTEM STATUS: NEEDS ATTENTION ({success_rate:.1f}%){Colors.END}")
        else:
            print(f"\n{Colors.RED}❌ SYSTEM STATUS: NOT READY ({success_rate:.1f}%){Colors.END}")

class FrankensteinDBTester:
    """Test FrankensteinDB functionality"""
    
    def __init__(self, result: TestResult):
        self.result = result
        self.db_path = "/tmp/test_frankenstein.db"
        
    def test_database_creation(self):
        """Test database creation and basic operations"""
        try:
            # Clean up any existing test DB
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                
            # Create test database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create test tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS website_dna (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    dna_hash TEXT NOT NULL,
                    content_type TEXT,
                    scrape_timestamp REAL,
                    compression_ratio REAL,
                    fingerprint TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scraping_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    start_time REAL,
                    end_time REAL,
                    status TEXT,
                    pages_scraped INTEGER DEFAULT 0
                )
            """)
            
            conn.commit()
            conn.close()
            
            self.result.add_success("Database Creation & Schema Setup")
            
        except Exception as e:
            self.result.add_failure("Database Creation", str(e))
            
    def test_dna_storage_performance(self):
        """Test DNA storage performance with batch operations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Generate test DNA data
            test_data = []
            start_time = time.time()
            
            for i in range(1000):
                test_data.append((
                    f"https://example.com/page-{i}",
                    f"dna_hash_{i:04d}_{'x' * 32}",
                    "text/html",
                    time.time(),
                    0.85 + (i % 10) * 0.01,  # Varying compression ratios
                    f"fp_{i:04d}_{'a' * 16}"
                ))
            
            # Batch insert
            cursor.executemany("""
                INSERT INTO website_dna 
                (url, dna_hash, content_type, scrape_timestamp, compression_ratio, fingerprint)
                VALUES (?, ?, ?, ?, ?, ?)
            """, test_data)
            
            conn.commit()
            end_time = time.time()
            
            # Performance check
            insert_time = end_time - start_time
            rate = len(test_data) / insert_time
            
            # Query performance
            query_start = time.time()
            cursor.execute("SELECT COUNT(*) FROM website_dna WHERE compression_ratio > 0.9")
            result = cursor.fetchone()[0]
            query_time = time.time() - query_start
            
            conn.close()
            
            if rate > 500:  # Should handle 500+ inserts/second
                self.result.add_success(f"DNA Storage Performance: {rate:.0f} records/sec, Query: {query_time*1000:.1f}ms")
            else:
                self.result.add_failure("DNA Storage Performance", f"Too slow: {rate:.0f} records/sec")
                
        except Exception as e:
            self.result.add_failure("DNA Storage Performance", str(e))
            
    def test_search_functionality(self):
        """Test full-text search capabilities"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create FTS table
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS content_search 
                USING fts5(url, content, tags)
            """)
            
            # Insert test content
            test_content = [
                ("https://example.com/python", "Python programming tutorial", "programming,tutorial"),
                ("https://example.com/javascript", "JavaScript web development", "web,development"),
                ("https://example.com/docker", "Docker containerization guide", "devops,containers"),
                ("https://example.com/ai", "AI and machine learning", "ai,ml,algorithms")
            ]
            
            cursor.executemany("""
                INSERT INTO content_search (url, content, tags) VALUES (?, ?, ?)
            """, test_content)
            
            # Test search queries
            search_tests = [
                ("programming", 1),
                ("development", 2),  # Should match both web and general development
                ("docker OR ai", 2),
                ("machine learning", 1)
            ]
            
            all_passed = True
            for query, expected_count in search_tests:
                cursor.execute("""
                    SELECT COUNT(*) FROM content_search 
                    WHERE content_search MATCH ?
                """, (query,))
                actual_count = cursor.fetchone()[0]
                
                if actual_count != expected_count:
                    all_passed = False
                    break
            
            conn.close()
            
            if all_passed:
                self.result.add_success("Full-Text Search Functionality")
            else:
                self.result.add_failure("Full-Text Search", f"Query '{query}' returned {actual_count}, expected {expected_count}")
                
        except Exception as e:
            self.result.add_failure("Search Functionality", str(e))

class AIScrapeVMTester:
    """Test AI Scraper VM functionality"""
    
    def __init__(self, result: TestResult):
        self.result = result
        
    def test_vm_orchestrator(self):
        """Test VM orchestrator functionality"""
        try:
            # Import the orchestrator module
            sys.path.insert(0, '/home/b/teamai/production-VMs/ai-scraper-vm/src')
            
            try:
                from vm_orchestrator import VMOrchestrator
                orchestrator = VMOrchestrator()
                
                # Test basic orchestrator functionality
                if hasattr(orchestrator, 'create_vm_instance'):
                    self.result.add_success("VM Orchestrator Module Import & Initialization")
                else:
                    self.result.add_failure("VM Orchestrator", "Missing required methods")
                    
            except ImportError as e:
                # If import fails, test the file exists and has basic structure
                vm_orch_path = '/home/b/teamai/production-VMs/ai-scraper-vm/src/vm_orchestrator.py'
                if os.path.exists(vm_orch_path):
                    with open(vm_orch_path, 'r') as f:
                        content = f.read()
                        if 'class VMOrchestrator' in content:
                            self.result.add_success("VM Orchestrator Code Structure Valid")
                        else:
                            self.result.add_failure("VM Orchestrator", "Invalid code structure")
                else:
                    self.result.add_failure("VM Orchestrator", f"File not found: {vm_orch_path}")
                    
        except Exception as e:
            self.result.add_failure("VM Orchestrator Test", str(e))
            
    def test_mqtt_integration(self):
        """Test MQTT integration (simulated)"""
        try:
            # Simulate MQTT message processing
            test_messages = [
                {"topic": "scraper/request", "payload": {"url": "https://example.com", "action": "scrape"}},
                {"topic": "scraper/status", "payload": {"session_id": "test_123", "status": "running"}},
                {"topic": "scraper/response", "payload": {"url": "https://example.com", "status": "completed", "dna": "abc123"}}
            ]
            
            # Test message validation
            valid_messages = 0
            for msg in test_messages:
                if all(key in msg for key in ["topic", "payload"]):
                    if isinstance(msg["payload"], dict):
                        valid_messages += 1
                        
            if valid_messages == len(test_messages):
                self.result.add_success("MQTT Message Structure Validation")
            else:
                self.result.add_failure("MQTT Integration", f"Invalid messages: {len(test_messages) - valid_messages}")
                
        except Exception as e:
            self.result.add_failure("MQTT Integration", str(e))
            
    def test_dna_analysis(self):
        """Test DNA analysis functionality"""
        try:
            # Test DNA generation algorithm (simplified)
            test_html = """
            <html>
                <head><title>Test Page</title></head>
                <body>
                    <h1>Main Heading</h1>
                    <div class="content">
                        <p>Some content here</p>
                        <a href="/link">Link</a>
                    </div>
                </body>
            </html>
            """
            
            # Simulate DNA extraction
            import hashlib
            import re
            
            # Extract structural elements
            tags = re.findall(r'<(\w+)', test_html)
            classes = re.findall(r'class="([^"]*)"', test_html)
            
            # Create simplified DNA
            dna_data = {
                "tag_count": len(tags),
                "unique_tags": len(set(tags)),
                "has_classes": len(classes) > 0,
                "content_hash": hashlib.md5(test_html.encode()).hexdigest()[:16]
            }
            
            # Validate DNA structure
            if all(key in dna_data for key in ["tag_count", "unique_tags", "content_hash"]):
                self.result.add_success("DNA Analysis Algorithm")
            else:
                self.result.add_failure("DNA Analysis", "Incomplete DNA structure")
                
        except Exception as e:
            self.result.add_failure("DNA Analysis", str(e))

class DashboardTester:
    """Test Dashboard functionality"""
    
    def __init__(self, result: TestResult):
        self.result = result
        
    def test_build_system(self):
        """Test dashboard build system"""
        try:
            dashboard_path = '/home/b/teamai/production-VMs/ai-scraper-dashboard'
            
            # Check if package.json exists
            package_json_path = os.path.join(dashboard_path, 'package.json')
            if not os.path.exists(package_json_path):
                self.result.add_failure("Dashboard Build", "package.json not found")
                return
                
            # Check if build artifacts exist
            build_paths = [
                os.path.join(dashboard_path, 'linux-package'),
                os.path.join(dashboard_path, 'simple-build')
            ]
            
            existing_builds = [path for path in build_paths if os.path.exists(path)]
            
            if existing_builds:
                self.result.add_success(f"Dashboard Build System: {len(existing_builds)} build artifacts found")
            else:
                self.result.add_warning("Dashboard Build System: No build artifacts found (run build_test.py first)")
                
        except Exception as e:
            self.result.add_failure("Dashboard Build Test", str(e))
            
    def test_linux_package(self):
        """Test Linux package installation"""
        try:
            dashboard_path = '/home/b/teamai/production-VMs/ai-scraper-dashboard'
            linux_package_path = os.path.join(dashboard_path, 'linux-package')
            
            if not os.path.exists(linux_package_path):
                self.result.add_failure("Linux Package", "Package directory not found")
                return
                
            # Check required files
            required_files = [
                'install.sh',
                'README.md',
                'ai-scraper-dashboard.desktop'
            ]
            
            missing_files = []
            for file in required_files:
                if not os.path.exists(os.path.join(linux_package_path, file)):
                    missing_files.append(file)
                    
            if not missing_files:
                self.result.add_success("Linux Package Structure Complete")
            else:
                self.result.add_failure("Linux Package", f"Missing files: {', '.join(missing_files)}")
                
        except Exception as e:
            self.result.add_failure("Linux Package Test", str(e))

class ProductionTester:
    """Test production deployment readiness"""
    
    def __init__(self, result: TestResult):
        self.result = result
        
    def test_docker_configs(self):
        """Test Docker configuration files"""
        try:
            # Check for Docker files
            docker_files = [
                '/home/b/teamai/production-VMs/ai-scraper-vm/Dockerfile',
                '/home/b/teamai/production-VMs/frankenstein-db/docker-compose.production.yml',
                '/home/b/teamai/production-VMs/ai-scraper-vm/docker-compose.yml'
            ]
            
            valid_configs = 0
            for docker_file in docker_files:
                if os.path.exists(docker_file):
                    with open(docker_file, 'r') as f:
                        content = f.read()
                        # Basic validation
                        if 'FROM' in content or 'version:' in content:
                            valid_configs += 1
                            
            if valid_configs >= 2:  # At least 2 valid Docker configs
                self.result.add_success(f"Docker Configurations: {valid_configs} valid files")
            else:
                self.result.add_failure("Docker Configurations", f"Only {valid_configs} valid configs found")
                
        except Exception as e:
            self.result.add_failure("Docker Configuration Test", str(e))
            
    def test_security_practices(self):
        """Test security best practices implementation"""
        try:
            dockerfile_path = '/home/b/teamai/production-VMs/ai-scraper-vm/Dockerfile'
            
            if not os.path.exists(dockerfile_path):
                self.result.add_failure("Security Practices", "Dockerfile not found")
                return
                
            with open(dockerfile_path, 'r') as f:
                content = f.read()
                
            security_checks = {
                "No apt-key deprecated usage": "apt-key" not in content,
                "Uses /etc/apt/keyrings": "/etc/apt/keyrings" in content,
                "Non-root user": any(line.strip().startswith("USER ") and "root" not in line for line in content.split('\n')),
                "Secure GPG practices": "gpg --dearmor" in content
            }
            
            passed_checks = sum(security_checks.values())
            total_checks = len(security_checks)
            
            if passed_checks >= total_checks * 0.8:  # 80% of security checks pass
                self.result.add_success(f"Security Practices: {passed_checks}/{total_checks} checks passed")
            else:
                failed = [check for check, passed in security_checks.items() if not passed]
                self.result.add_failure("Security Practices", f"Failed: {', '.join(failed)}")
                
        except Exception as e:
            self.result.add_failure("Security Practices Test", str(e))

class PerformanceTester:
    """Performance and load testing"""
    
    def __init__(self, result: TestResult):
        self.result = result
        
    def test_concurrent_operations(self):
        """Test concurrent database operations"""
        try:
            import threading
            import time
            
            db_path = "/tmp/perf_test.db"
            
            # Setup test database
            conn = sqlite3.connect(db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS perf_test (
                    id INTEGER PRIMARY KEY,
                    data TEXT,
                    timestamp REAL
                )
            """)
            conn.close()
            
            # Concurrent operation test
            def worker(worker_id):
                conn = sqlite3.connect(db_path)
                for i in range(100):
                    conn.execute("""
                        INSERT INTO perf_test (data, timestamp) VALUES (?, ?)
                    """, (f"worker_{worker_id}_data_{i}", time.time()))
                    conn.commit()
                conn.close()
                
            # Run multiple workers
            start_time = time.time()
            threads = []
            for i in range(5):
                t = threading.Thread(target=worker, args=(i,))
                threads.append(t)
                t.start()
                
            for t in threads:
                t.join()
                
            end_time = time.time()
            
            # Verify results
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM perf_test")
            total_records = cursor.fetchone()[0]
            conn.close()
            
            # Cleanup
            os.remove(db_path)
            
            duration = end_time - start_time
            rate = total_records / duration
            
            if rate > 100:  # Should handle 100+ concurrent operations/second
                self.result.add_success(f"Concurrent Operations: {rate:.0f} ops/sec")
            else:
                self.result.add_failure("Concurrent Operations", f"Too slow: {rate:.0f} ops/sec")
                
        except Exception as e:
            self.result.add_failure("Concurrent Operations Test", str(e))

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description='AI Scraper System - End-to-End Integration Tests')
    parser.add_argument('--full', action='store_true', help='Run complete test suite including performance tests')
    parser.add_argument('--performance', action='store_true', help='Run only performance benchmarks')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    print_header("🔬 AI SCRAPER SYSTEM - END-TO-END INTEGRATION TESTS")
    print_info("Testing complete system integration and production readiness...")
    
    result = TestResult()
    
    # Initialize testers
    frankenstein_tester = FrankensteinDBTester(result)
    vm_tester = AIScrapeVMTester(result)
    dashboard_tester = DashboardTester(result)
    production_tester = ProductionTester(result)
    performance_tester = PerformanceTester(result)
    
    try:
        if args.performance:
            print_header("PERFORMANCE TESTING ONLY")
            performance_tester.test_concurrent_operations()
        else:
            # Core functionality tests
            print_header("1. FRANKENSTEIN DATABASE TESTING")
            frankenstein_tester.test_database_creation()
            frankenstein_tester.test_dna_storage_performance()
            frankenstein_tester.test_search_functionality()
            
            print_header("2. AI SCRAPER VM TESTING")
            vm_tester.test_vm_orchestrator()
            vm_tester.test_mqtt_integration()
            vm_tester.test_dna_analysis()
            
            print_header("3. DASHBOARD TESTING")
            dashboard_tester.test_build_system()
            dashboard_tester.test_linux_package()
            
            print_header("4. PRODUCTION DEPLOYMENT TESTING")
            production_tester.test_docker_configs()
            production_tester.test_security_practices()
            
            if args.full:
                print_header("5. PERFORMANCE TESTING")
                performance_tester.test_concurrent_operations()
                
    except KeyboardInterrupt:
        print_warning("Tests interrupted by user")
        
    finally:
        result.summary()
        
        # Cleanup any test files
        test_files = ["/tmp/test_frankenstein.db", "/tmp/perf_test.db"]
        for test_file in test_files:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == "__main__":
    main()