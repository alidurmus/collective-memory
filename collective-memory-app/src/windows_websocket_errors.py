#!/usr/bin/env python3
"""
Windows WebSocket Error Handling
Handles Windows-specific WebSocket errors and provides solutions
"""

import logging
import platform
import socket
import subprocess
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
import os

logger = logging.getLogger(__name__)


@dataclass
class WindowsWebSocketError:
    """Windows WebSocket error information"""
    error_code: str
    error_message: str
    error_type: str
    timestamp: datetime
    platform_info: Dict
    suggested_solutions: List[str]
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL


class WindowsWebSocketErrorHandler:
    """Handles Windows-specific WebSocket errors and provides solutions"""
    
    def __init__(self):
        self.is_windows = platform.system().lower() == "windows"
        self.error_patterns = self._initialize_error_patterns()
        self.solution_registry = self._initialize_solution_registry()
        self.error_history: List[WindowsWebSocketError] = []
        
        if self.is_windows:
            self._detect_windows_environment()
    
    def _initialize_error_patterns(self) -> Dict[str, Dict]:
        """Initialize Windows-specific error patterns"""
        return {
            "connection_refused": {
                "patterns": [
                    r"Connection refused",
                    r"WSAECONNREFUSED",
                    r"10061",
                    r"Target machine actively refused"
                ],
                "type": "network",
                "severity": "HIGH"
            },
            "timeout": {
                "patterns": [
                    r"Connection timed out",
                    r"WSAETIMEDOUT",
                    r"10060",
                    r"Operation timed out"
                ],
                "type": "network",
                "severity": "MEDIUM"
            },
            "firewall_blocked": {
                "patterns": [
                    r"Permission denied",
                    r"WSAEACCES",
                    r"10013",
                    r"Firewall",
                    r"Blocked by security software"
                ],
                "type": "security",
                "severity": "HIGH"
            },
            "proxy_issues": {
                "patterns": [
                    r"Proxy",
                    r"WSAECONNABORTED",
                    r"10053",
                    r"Corporate network",
                    r"VPN"
                ],
                "type": "network",
                "severity": "MEDIUM"
            },
            "socket_limit": {
                "patterns": [
                    r"Too many open files",
                    r"WSAEMFILE",
                    r"10024",
                    r"Socket limit exceeded"
                ],
                "type": "resource",
                "severity": "MEDIUM"
            },
            "port_in_use": {
                "patterns": [
                    r"Address already in use",
                    r"WSAEADDRINUSE",
                    r"10048",
                    r"Port already in use"
                ],
                "type": "resource",
                "severity": "MEDIUM"
            },
            "dns_resolution": {
                "patterns": [
                    r"Name or service not known",
                    r"WSAHOST_NOT_FOUND",
                    r"11001",
                    r"DNS resolution failed"
                ],
                "type": "network",
                "severity": "MEDIUM"
            },
            "ssl_tls": {
                "patterns": [
                    r"SSL",
                    r"TLS",
                    r"Certificate",
                    r"Handshake failed"
                ],
                "type": "security",
                "severity": "HIGH"
            }
        }
    
    def _initialize_solution_registry(self) -> Dict[str, List[str]]:
        """Initialize solution registry for different error types"""
        return {
            "connection_refused": [
                "Check if the WebSocket server is running on the specified port",
                "Verify the server address and port number",
                "Check Windows Firewall settings for the application",
                "Try running the application as administrator",
                "Check if antivirus software is blocking the connection"
            ],
            "timeout": [
                "Increase WebSocket timeout settings",
                "Check network connectivity and stability",
                "Verify server response times",
                "Consider using HTTP polling as fallback",
                "Check for network congestion or proxy delays"
            ],
            "firewall_blocked": [
                "Add application exception to Windows Firewall",
                "Check antivirus software firewall settings",
                "Verify corporate firewall policies",
                "Try running the application as administrator",
                "Contact network administrator for firewall rules"
            ],
            "proxy_issues": [
                "Configure proxy settings in the application",
                "Check corporate proxy authentication",
                "Verify proxy server is accessible",
                "Try direct connection if possible",
                "Configure WebSocket to use HTTP proxy tunneling"
            ],
            "socket_limit": [
                "Increase Windows socket limit in registry",
                "Restart the application to free up sockets",
                "Check for socket leaks in the application",
                "Monitor socket usage with netstat",
                "Consider connection pooling"
            ],
            "port_in_use": [
                "Find and stop the process using the port",
                "Use a different port for the WebSocket server",
                "Check for multiple instances of the application",
                "Use 'netstat -ano' to identify the process",
                "Restart the system if necessary"
            ],
            "dns_resolution": [
                "Check DNS server configuration",
                "Try using IP address instead of hostname",
                "Flush DNS cache with 'ipconfig /flushdns'",
                "Check hosts file for incorrect entries",
                "Verify network adapter settings"
            ],
            "ssl_tls": [
                "Update SSL/TLS certificates",
                "Check certificate validity and trust chain",
                "Configure proper SSL/TLS version",
                "Verify certificate hostname matching",
                "Consider using self-signed certificates for development"
            ]
        }
    
    def _detect_windows_environment(self):
        """Detect Windows environment and potential issues"""
        try:
            self.windows_version = platform.version()
            self.windows_edition = platform.win32_edition()
            self.architecture = platform.architecture()[0]
            
            # Check for common Windows networking issues
            self.network_issues = self._check_network_issues()
            self.firewall_status = self._check_firewall_status()
            self.proxy_settings = self._check_proxy_settings()
            
            logger.info(f"Windows environment detected: {self.windows_version} {self.windows_edition} {self.architecture}")
            
        except Exception as e:
            logger.error(f"Error detecting Windows environment: {e}")
    
    def _check_network_issues(self) -> Dict:
        """Check for common Windows networking issues"""
        issues = {}
        
        try:
            # Check network adapters
            result = subprocess.run(
                ["ipconfig", "/all"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                issues["network_adapters"] = "Available"
                
                # Check for IPv6 issues
                if "IPv6 Address" in result.stdout:
                    issues["ipv6"] = "Enabled"
                else:
                    issues["ipv6"] = "Disabled"
                
                # Check for DNS issues
                if "DNS Servers" in result.stdout:
                    issues["dns"] = "Configured"
                else:
                    issues["dns"] = "Not configured"
            else:
                issues["network_adapters"] = "Error checking"
                
        except Exception as e:
            logger.error(f"Error checking network issues: {e}")
            issues["network_adapters"] = "Error"
        
        return issues
    
    def _check_firewall_status(self) -> Dict:
        """Check Windows Firewall status"""
        status = {}
        
        try:
            # Check Windows Firewall status
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse firewall status
                if "ON" in result.stdout:
                    status["firewall"] = "Enabled"
                else:
                    status["firewall"] = "Disabled"
            else:
                status["firewall"] = "Unknown"
                
        except Exception as e:
            logger.error(f"Error checking firewall status: {e}")
            status["firewall"] = "Error"
        
        return status
    
    def _check_proxy_settings(self) -> Dict:
        """Check Windows proxy settings"""
        settings = {}
        
        try:
            # Check proxy settings from registry
            result = subprocess.run(
                ["reg", "query", "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                if "ProxyEnable" in result.stdout and "0x1" in result.stdout:
                    settings["proxy_enabled"] = True
                else:
                    settings["proxy_enabled"] = False
            else:
                settings["proxy_enabled"] = "Unknown"
                
        except Exception as e:
            logger.error(f"Error checking proxy settings: {e}")
            settings["proxy_enabled"] = "Error"
        
        return settings
    
    def analyze_error(self, error_message: str, error_code: str = None) -> WindowsWebSocketError:
        """Analyze WebSocket error and provide solutions"""
        error_type = "unknown"
        severity = "MEDIUM"
        suggested_solutions = []
        
        # Match error patterns
        for error_key, error_info in self.error_patterns.items():
            for pattern in error_info["patterns"]:
                if re.search(pattern, error_message, re.IGNORECASE):
                    error_type = error_key
                    severity = error_info["severity"]
                    suggested_solutions = self.solution_registry.get(error_key, [])
                    break
            if error_type != "unknown":
                break
        
        # Add Windows-specific solutions
        if self.is_windows:
            suggested_solutions.extend(self._get_windows_specific_solutions(error_type))
        
        # Create error object
        error = WindowsWebSocketError(
            error_code=error_code or "UNKNOWN",
            error_message=error_message,
            error_type=error_type,
            timestamp=datetime.now(timezone.utc),
            platform_info={
                "is_windows": self.is_windows,
                "windows_version": getattr(self, 'windows_version', 'Unknown'),
                "architecture": getattr(self, 'architecture', 'Unknown'),
                "firewall_status": getattr(self, 'firewall_status', {}),
                "proxy_settings": getattr(self, 'proxy_settings', {})
            },
            suggested_solutions=suggested_solutions,
            severity=severity
        )
        
        # Add to history
        self.error_history.append(error)
        
        logger.warning(f"WebSocket error detected: {error_type} - {error_message}")
        
        return error
    
    def _get_windows_specific_solutions(self, error_type: str) -> List[str]:
        """Get Windows-specific solutions for error types"""
        solutions = []
        
        if error_type in ["firewall_blocked", "connection_refused"]:
            solutions.extend([
                "Run 'netsh advfirewall firewall add rule name=\"WebSocket App\" dir=in action=allow program=\"%path_to_app%\"'",
                "Check Windows Defender Firewall with Advanced Security",
                "Add application to Windows Firewall exceptions"
            ])
        
        if error_type in ["proxy_issues", "timeout"]:
            solutions.extend([
                "Configure proxy settings in Internet Explorer/Edge",
                "Check Windows proxy configuration with 'netsh winhttp show proxy'",
                "Set proxy environment variables: HTTP_PROXY, HTTPS_PROXY"
            ])
        
        if error_type in ["socket_limit", "port_in_use"]:
            solutions.extend([
                "Increase Windows socket limit: 'netsh int ipv4 set dynamicport tcp start=49152 num=16384'",
                "Check for port conflicts with 'netstat -ano | findstr :<port>'",
                "Restart Windows TCP/IP stack: 'netsh winsock reset'"
            ])
        
        return solutions
    
    def get_error_history(self, hours: int = 24) -> List[WindowsWebSocketError]:
        """Get error history for the last N hours"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        return [error for error in self.error_history if error.timestamp > cutoff_time]
    
    def get_error_summary(self) -> Dict:
        """Get summary of recent errors"""
        recent_errors = self.get_error_history(1)  # Last hour
        
        summary = {
            "total_errors": len(recent_errors),
            "error_types": {},
            "severity_counts": {
                "LOW": 0,
                "MEDIUM": 0,
                "HIGH": 0,
                "CRITICAL": 0
            },
            "most_common_error": None,
            "most_common_solution": None
        }
        
        error_type_counts = {}
        solution_counts = {}
        
        for error in recent_errors:
            # Count error types
            error_type_counts[error.error_type] = error_type_counts.get(error.error_type, 0) + 1
            
            # Count severity levels
            summary["severity_counts"][error.severity] += 1
            
            # Count solutions
            for solution in error.suggested_solutions:
                solution_counts[solution] = solution_counts.get(solution, 0) + 1
        
        # Find most common
        if error_type_counts:
            summary["most_common_error"] = max(error_type_counts, key=error_type_counts.get)
        
        if solution_counts:
            summary["most_common_solution"] = max(solution_counts, key=solution_counts.get)
        
        summary["error_types"] = error_type_counts
        
        return summary
    
    def clear_error_history(self):
        """Clear error history"""
        self.error_history.clear()
        logger.info("WebSocket error history cleared")
    
    def get_diagnostic_info(self) -> Dict:
        """Get comprehensive diagnostic information"""
        return {
            "platform": {
                "system": platform.system(),
                "version": platform.version(),
                "architecture": platform.architecture(),
                "is_windows": self.is_windows
            },
            "network": getattr(self, 'network_issues', {}),
            "firewall": getattr(self, 'firewall_status', {}),
            "proxy": getattr(self, 'proxy_settings', {}),
            "error_summary": self.get_error_summary(),
            "recent_errors": len(self.get_error_history(1))
        }


class WindowsNetworkingConfig:
    """Windows-specific networking configuration helper"""
    
    def __init__(self):
        self.is_windows = platform.system().lower() == "windows"
    
    def configure_tcp_keepalive(self, socket_obj):
        """Configure TCP keepalive for Windows"""
        if not self.is_windows:
            return
        
        try:
            # Windows-specific TCP keepalive settings
            socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            # Set keepalive parameters (Windows-specific)
            socket_obj.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 30000, 3000))
            
            logger.debug("TCP keepalive configured for Windows")
            
        except Exception as e:
            logger.warning(f"Failed to configure TCP keepalive: {e}")
    
    def configure_tcp_nodelay(self, socket_obj):
        """Configure TCP nodelay for Windows"""
        if not self.is_windows:
            return
        
        try:
            socket_obj.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            logger.debug("TCP nodelay configured for Windows")
            
        except Exception as e:
            logger.warning(f"Failed to configure TCP nodelay: {e}")
    
    def add_firewall_exception(self, application_path: str, rule_name: str = None):
        """Add Windows Firewall exception for application"""
        if not self.is_windows:
            return False
        
        try:
            if not rule_name:
                rule_name = f"WebSocket App - {os.path.basename(application_path)}"
            
            # Add inbound rule
            inbound_cmd = [
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name=\"{rule_name}\"",
                "dir=in",
                "action=allow",
                f"program=\"{application_path}\""
            ]
            
            result = subprocess.run(inbound_cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"Added Windows Firewall inbound rule: {rule_name}")
                return True
            else:
                logger.error(f"Failed to add Windows Firewall rule: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding Windows Firewall exception: {e}")
            return False
    
    def remove_firewall_exception(self, rule_name: str):
        """Remove Windows Firewall exception"""
        if not self.is_windows:
            return False
        
        try:
            cmd = ["netsh", "advfirewall", "firewall", "delete", "rule", f"name=\"{rule_name}\""]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"Removed Windows Firewall rule: {rule_name}")
                return True
            else:
                logger.error(f"Failed to remove Windows Firewall rule: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing Windows Firewall exception: {e}")
            return False
    
    def get_network_adapters(self) -> List[Dict]:
        """Get Windows network adapters information"""
        if not self.is_windows:
            return []
        
        try:
            result = subprocess.run(
                ["ipconfig", "/all"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                adapters = []
                current_adapter = {}
                
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    
                    if line and not line.startswith(' '):
                        if current_adapter:
                            adapters.append(current_adapter)
                        current_adapter = {"name": line.rstrip(':')}
                    elif line.startswith('   ') and current_adapter:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            current_adapter[key.strip()] = value.strip()
                
                if current_adapter:
                    adapters.append(current_adapter)
                
                return adapters
            else:
                logger.error(f"Failed to get network adapters: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting network adapters: {e}")
            return []
    
    def test_connectivity(self, host: str, port: int) -> Dict:
        """Test network connectivity to host:port"""
        result = {
            "success": False,
            "error": None,
            "response_time": None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            import time
            start_time = time.time()
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            # Configure Windows-specific socket options
            if self.is_windows:
                self.configure_tcp_keepalive(sock)
                self.configure_tcp_nodelay(sock)
            
            sock.connect((host, port))
            sock.close()
            
            result["success"] = True
            result["response_time"] = (time.time() - start_time) * 1000  # ms
            
        except Exception as e:
            result["error"] = str(e)
        
        return result 