#!/usr/bin/env python3
"""
Performance Monitor - Real-time system health monitoring
Sistem sağlığı izleme ve performance tracking
"""

import psutil
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import deque
import threading

@dataclass
class SystemMetrics:
    """System performance metrics data structure"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_gb: float
    disk_usage_percent: float
    disk_free_gb: float
    active_connections: int
    process_count: int
    python_memory_mb: float
    load_average: List[float] = None

@dataclass
class ApplicationMetrics:
    """Application-specific metrics"""
    timestamp: str
    search_requests_count: int
    api_response_time_avg: float
    database_connections: int
    cache_hit_rate: float
    active_sessions: int
    error_count: int
    uptime_seconds: int

class SystemHealthMonitor:
    """Real-time system health monitoring"""
    
    def __init__(self, data_path: Optional[str] = None):
        self.data_path = Path(data_path) if data_path else Path.cwd()
        self.metrics_file = self.data_path / '.collective-memory' / 'system_metrics.json'
        self.metrics_file.parent.mkdir(exist_ok=True)
        
        # Metrics storage (keep last 1000 entries)
        self.system_metrics = deque(maxlen=1000)
        self.app_metrics = deque(maxlen=1000)
        
        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None
        self.start_time = datetime.now()
        
        # Counters
        self.search_requests = 0
        self.api_response_times = deque(maxlen=100)
        self.error_count = 0
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # İlk veri toplama (deque boşsa)
        self.system_metrics.append(self._collect_system_metrics())
        self.app_metrics.append(self._collect_application_metrics())
        
    def start_monitoring(self, interval: int = 30):
        """Start real-time monitoring"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info("System health monitoring started")
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("System health monitoring stopped")
        
    def _monitoring_loop(self, interval: int):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                system_metrics = self._collect_system_metrics()
                self.system_metrics.append(system_metrics)
                
                # Collect application metrics
                app_metrics = self._collect_application_metrics()
                self.app_metrics.append(app_metrics)
                
                # Save to file
                self._save_metrics()
                
                # Log critical issues
                self._check_alerts(system_metrics, app_metrics)
                
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(interval)
                
    def _collect_system_metrics(self) -> SystemMetrics:
        """Collect system performance metrics"""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net_connections = len(psutil.net_connections())
        
        # Python process memory
        python_process = psutil.Process()
        python_memory_mb = python_process.memory_info().rss / 1024 / 1024
        
        # Load average (Unix only)
        load_avg = None
        try:
            load_avg = list(psutil.getloadavg())
        except (AttributeError, OSError):
            # Windows doesn't have load average
            pass
            
        return SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=memory.percent,
            memory_used_gb=memory.used / 1024**3,
            disk_usage_percent=disk.percent,
            disk_free_gb=disk.free / 1024**3,
            active_connections=net_connections,
            process_count=len(psutil.pids()),
            python_memory_mb=python_memory_mb,
            load_average=load_avg
        )
        
    def _collect_application_metrics(self) -> ApplicationMetrics:
        """Collect application-specific metrics"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        # Calculate average response time
        avg_response_time = 0.0
        if self.api_response_times:
            avg_response_time = sum(self.api_response_times) / len(self.api_response_times)
            
        # Mock values for now - these would be collected from actual app
        return ApplicationMetrics(
            timestamp=datetime.now().isoformat(),
            search_requests_count=self.search_requests,
            api_response_time_avg=avg_response_time,
            database_connections=1,  # SQLite typically 1 connection
            cache_hit_rate=0.85,  # Mock cache hit rate
            active_sessions=1,  # Single user for now
            error_count=self.error_count,
            uptime_seconds=int(uptime)
        )
        
    def _save_metrics(self):
        """Save metrics to file"""
        try:
            data = {
                'system_metrics': [asdict(m) for m in list(self.system_metrics)[-10:]],
                'app_metrics': [asdict(m) for m in list(self.app_metrics)[-10:]],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.metrics_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save metrics: {e}")
            
    def _check_alerts(self, system_metrics: SystemMetrics, app_metrics: ApplicationMetrics):
        """Check for critical issues and log alerts"""
        # CPU usage alert
        if system_metrics.cpu_percent > 90:
            self.logger.warning(f"High CPU usage: {system_metrics.cpu_percent:.1f}%")
            
        # Memory usage alert
        if system_metrics.memory_percent > 90:
            self.logger.warning(f"High memory usage: {system_metrics.memory_percent:.1f}%")
            
        # Disk space alert
        if system_metrics.disk_usage_percent > 90:
            self.logger.warning(f"Low disk space: {system_metrics.disk_usage_percent:.1f}% used")
            
        # Application response time alert
        if app_metrics.api_response_time_avg > 5000:  # 5 seconds
            self.logger.warning(f"Slow API response: {app_metrics.api_response_time_avg:.0f}ms")
            
    # Public methods for application integration
    def record_search_request(self):
        """Record a search request"""
        self.search_requests += 1
        
    def record_api_response_time(self, response_time_ms: float):
        """Record API response time"""
        self.api_response_times.append(response_time_ms)
        
    def record_error(self):
        """Record an error occurrence"""
        self.error_count += 1
        
    def get_current_status(self) -> Dict[str, Any]:
        """Get current system status"""
        if not self.system_metrics or not self.app_metrics:
            return {
                "status": "no_data",
                "message": "Monitoring not started or no data available",
                "system_metrics": {},
                "app_metrics": {}
            }
            
        latest_system = self.system_metrics[-1]
        latest_app = self.app_metrics[-1]
        
        # Determine overall health
        health_score = 100
        issues = []
        
        if latest_system.cpu_percent > 80:
            health_score -= 20
            issues.append(f"High CPU: {latest_system.cpu_percent:.1f}%")
            
        if latest_system.memory_percent > 80:
            health_score -= 20
            issues.append(f"High Memory: {latest_system.memory_percent:.1f}%")
            
        if latest_system.disk_usage_percent > 85:
            health_score -= 15
            issues.append(f"Low Disk: {latest_system.disk_free_gb:.1f}GB free")
            
        if latest_app.api_response_time_avg > 2000:
            health_score -= 25
            issues.append(f"Slow API: {latest_app.api_response_time_avg:.0f}ms")
            
        # Health status
        if health_score >= 90:
            status = "excellent"
        elif health_score >= 70:
            status = "good"
        elif health_score >= 50:
            status = "fair"
        else:
            status = "poor"
            
        return {
            "status": status,
            "health_score": health_score,
            "issues": issues,
            "system_metrics": asdict(latest_system),
            "app_metrics": asdict(latest_app),
            "uptime_hours": latest_app.uptime_seconds / 3600
        }
        
    def get_metrics_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics summary for specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter metrics by time
        recent_system = [
            m for m in self.system_metrics 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        recent_app = [
            m for m in self.app_metrics 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_system or not recent_app:
            return {"error": "Insufficient data for summary"}
            
        # Calculate averages
        avg_cpu = sum(m.cpu_percent for m in recent_system) / len(recent_system)
        avg_memory = sum(m.memory_percent for m in recent_system) / len(recent_system)
        max_cpu = max(m.cpu_percent for m in recent_system)
        max_memory = max(m.memory_percent for m in recent_system)
        
        avg_response_time = sum(m.api_response_time_avg for m in recent_app) / len(recent_app)
        total_searches = recent_app[-1].search_requests_count if recent_app else 0
        total_errors = recent_app[-1].error_count if recent_app else 0
        
        return {
            "period_hours": hours,
            "data_points": len(recent_system),
            "cpu_usage": {
                "average": round(avg_cpu, 1),
                "maximum": round(max_cpu, 1)
            },
            "memory_usage": {
                "average": round(avg_memory, 1),
                "maximum": round(max_memory, 1)
            },
            "api_performance": {
                "avg_response_time_ms": round(avg_response_time, 1),
                "total_searches": total_searches,
                "total_errors": total_errors
            },
            "system_stability": "stable" if max_cpu < 90 and max_memory < 90 else "unstable"
        }

# Global monitor instance
_monitor_instance = None

def get_monitor(data_path: Optional[str] = None) -> SystemHealthMonitor:
    """Get global monitor instance"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = SystemHealthMonitor(data_path)
    return _monitor_instance

def start_system_monitoring(data_path: Optional[str] = None, interval: int = 30):
    """Start system monitoring (convenience function)"""
    monitor = get_monitor(data_path)
    monitor.start_monitoring(interval)
    return monitor 