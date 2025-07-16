#!/usr/bin/env python3
"""
Context Engineering Template - Performance Optimizer
Collective Memory System Performance Enhancement Script

Bu script, Collective Memory sisteminin performansını optimize eder:
- Database query optimization
- Memory usage analysis
- Cache effectiveness monitoring
- System resource optimization
"""

import os
import sys
import json
import time
import sqlite3
import psutil
from datetime import datetime
from pathlib import Path

class PerformanceOptimizer:
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())
        self.app_root = self.project_root / "collective-memory-app"
        self.db_path = self.app_root / ".collective-memory" / "database" / "app_database.db"
        self.report_path = self.project_root / "context-engineering" / "output" / "performance-report.json"
        
        # Performance thresholds (from tech stack requirements)
        self.thresholds = {
            "api_response_time": 500,  # ms
            "search_time": 100,        # ms
            "memory_usage": 512,       # MB
            "cpu_usage": 70,           # %
            "cache_hit_rate": 80       # %
        }
        
        self.optimization_results = {
            "timestamp": datetime.now().isoformat(),
            "system_info": {},
            "performance_metrics": {},
            "optimizations_applied": [],
            "recommendations": []
        }

    def run_optimization(self):
        """Ana optimizasyon sürecini çalıştır"""
        print("🚀 Collective Memory Performance Optimizer")
        print("=" * 50)
        
        # 1. Sistem bilgilerini topla
        self._collect_system_info()
        
        # 2. Mevcut performans metriklerini ölç
        self._measure_performance()
        
        # 3. Database optimizasyonları uygula
        self._optimize_database()
        
        # 4. Memory optimizasyonları uygula
        self._optimize_memory()
        
        # 5. Cache optimizasyonları uygula
        self._optimize_cache()
        
        # 6. Rapor oluştur
        self._generate_report()
        
        print("\n✅ Performance optimization completed!")
        print(f"📊 Report saved to: {self.report_path}")

    def _collect_system_info(self):
        """Sistem bilgilerini topla"""
        print("\n📊 Collecting system information...")
        
        # System resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage(str(self.project_root))
        
        self.optimization_results["system_info"] = {
            "cpu_count": psutil.cpu_count(),
            "cpu_usage": cpu_percent,
            "memory_total": memory.total // (1024**3),  # GB
            "memory_available": memory.available // (1024**2),  # MB
            "memory_usage_percent": memory.percent,
            "disk_total": disk.total // (1024**3),  # GB
            "disk_free": disk.free // (1024**3),   # GB
            "disk_usage_percent": (disk.used / disk.total) * 100
        }
        
        print(f"  CPU Usage: {cpu_percent}%")
        print(f"  Memory Usage: {memory.percent}%")
        print(f"  Available Memory: {memory.available // (1024**2)} MB")

    def _measure_performance(self):
        """Mevcut performans metriklerini ölç"""
        print("\n⏱️ Measuring current performance...")
        
        metrics = {}
        
        # Database size and query performance
        if self.db_path.exists():
            db_size = self.db_path.stat().st_size / (1024**2)  # MB
            metrics["database_size"] = db_size
            
            # Sample database query performance
            query_time = self._measure_db_query_time()
            metrics["avg_query_time"] = query_time
            
            print(f"  Database Size: {db_size:.2f} MB")
            print(f"  Average Query Time: {query_time:.2f} ms")
        
        # Application memory usage (if running)
        app_memory = self._get_app_memory_usage()
        if app_memory:
            metrics["app_memory_usage"] = app_memory
            print(f"  App Memory Usage: {app_memory:.2f} MB")
        
        self.optimization_results["performance_metrics"] = metrics

    def _measure_db_query_time(self):
        """Database sorgu süresini ölç"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Test query
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM files")
            result = cursor.fetchone()
            end_time = time.time()
            
            conn.close()
            
            query_time = (end_time - start_time) * 1000  # ms
            return query_time
            
        except Exception as e:
            print(f"  Warning: Could not measure DB performance: {e}")
            return 0

    def _get_app_memory_usage(self):
        """Uygulama memory kullanımını al"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                if 'python' in proc.info['name'].lower():
                    # Check if this is our API server process
                    try:
                        cmdline = proc.cmdline()
                        if any('api_server.py' in arg for arg in cmdline):
                            return proc.info['memory_info'].rss / (1024**2)  # MB
                    except:
                        continue
            return None
        except:
            return None

    def _optimize_database(self):
        """Database optimizasyonları uygula"""
        print("\n🗄️ Optimizing database...")
        
        if not self.db_path.exists():
            print("  No database found, skipping optimization")
            return
        
        optimizations = []
        
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # 1. VACUUM - Database defragmentation
            print("  Running VACUUM...")
            start_size = self.db_path.stat().st_size
            cursor.execute("VACUUM")
            end_size = self.db_path.stat().st_size
            space_saved = (start_size - end_size) / (1024**2)  # MB
            optimizations.append(f"VACUUM saved {space_saved:.2f} MB")
            
            # 2. ANALYZE - Update query planner statistics
            print("  Running ANALYZE...")
            cursor.execute("ANALYZE")
            optimizations.append("Query planner statistics updated")
            
            # 3. Create indexes if missing
            print("  Checking indexes...")
            
            # File path index for faster searches
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_files_path 
                ON files(file_path)
            """)
            
            # Content search index
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_search_content 
                ON search_index(content)
            """)
            
            # Timestamp indexes for better filtering
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_files_modified 
                ON files(last_modified)
            """)
            
            optimizations.append("Database indexes verified/created")
            
            # 4. Set optimal PRAGMA settings
            cursor.execute("PRAGMA journal_mode = WAL")
            cursor.execute("PRAGMA synchronous = NORMAL")
            cursor.execute("PRAGMA cache_size = 1000000")  # 1GB cache
            cursor.execute("PRAGMA temp_store = MEMORY")
            optimizations.append("Database PRAGMA settings optimized")
            
            conn.commit()
            conn.close()
            
            self.optimization_results["optimizations_applied"].extend(optimizations)
            
            for opt in optimizations:
                print(f"  ✅ {opt}")
                
        except Exception as e:
            print(f"  ❌ Database optimization failed: {e}")

    def _optimize_memory(self):
        """Memory optimizasyonları uygula"""
        print("\n🧠 Analyzing memory optimization opportunities...")
        
        recommendations = []
        
        current_memory = psutil.virtual_memory()
        available_mb = current_memory.available // (1024**2)
        
        if available_mb < 1000:  # Less than 1GB available
            recommendations.append("System has low available memory (<1GB)")
            recommendations.append("Consider closing unnecessary applications")
        
        if current_memory.percent > 80:
            recommendations.append("High memory usage detected (>80%)")
            recommendations.append("Consider restarting the application periodically")
        
        # Python-specific optimizations
        recommendations.extend([
            "Enable garbage collection optimization in Python",
            "Use generator expressions for large data processing",
            "Implement result caching to reduce memory allocation"
        ])
        
        self.optimization_results["recommendations"].extend(recommendations)
        
        for rec in recommendations:
            print(f"  💡 {rec}")

    def _optimize_cache(self):
        """Cache optimizasyonları uygula"""
        print("\n💾 Optimizing cache strategies...")
        
        optimizations = []
        recommendations = []
        
        # Cache configuration recommendations
        cache_recommendations = [
            "Implement Redis for session caching",
            "Use in-memory cache for frequent searches",
            "Cache search results for 5-10 minutes",
            "Implement cache invalidation on file changes"
        ]
        
        recommendations.extend(cache_recommendations)
        optimizations.append("Cache strategy recommendations generated")
        
        self.optimization_results["optimizations_applied"].extend(optimizations)
        self.optimization_results["recommendations"].extend(recommendations)
        
        for rec in cache_recommendations:
            print(f"  💡 {rec}")

    def _generate_report(self):
        """Performance raporu oluştur"""
        print("\n📋 Generating performance report...")
        
        # Performance score calculation
        score = self._calculate_performance_score()
        self.optimization_results["performance_score"] = score
        
        # Create output directory
        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save JSON report
        with open(self.report_path, 'w', encoding='utf-8') as f:
            json.dump(self.optimization_results, f, indent=2, ensure_ascii=False)
        
        # Generate markdown summary
        self._generate_markdown_summary()
        
        print(f"  Performance Score: {score}/100")
        print(f"  Report saved to: {self.report_path}")

    def _calculate_performance_score(self):
        """Performance skoru hesapla"""
        score = 100
        metrics = self.optimization_results["performance_metrics"]
        
        # Database size penalty
        db_size = metrics.get("database_size", 0)
        if db_size > 100:  # > 100MB
            score -= 10
        
        # Query time penalty
        query_time = metrics.get("avg_query_time", 0)
        if query_time > self.thresholds["search_time"]:
            score -= 20
        
        # Memory usage penalty
        memory_percent = self.optimization_results["system_info"]["memory_usage_percent"]
        if memory_percent > 80:
            score -= 15
        
        # CPU usage penalty
        cpu_percent = self.optimization_results["system_info"]["cpu_usage"]
        if cpu_percent > self.thresholds["cpu_usage"]:
            score -= 10
        
        return max(0, score)

    def _generate_markdown_summary(self):
        """Markdown özeti oluştur"""
        summary_path = self.report_path.parent / "performance-summary.md"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# 🚀 Collective Memory Performance Report\n\n")
            f.write(f"**Generated:** {self.optimization_results['timestamp']}\n\n")
            f.write(f"**Performance Score:** {self.optimization_results['performance_score']}/100\n\n")
            
            f.write("## 📊 System Information\n\n")
            sys_info = self.optimization_results["system_info"]
            f.write(f"- **CPU Usage:** {sys_info['cpu_usage']}%\n")
            f.write(f"- **Memory Usage:** {sys_info['memory_usage_percent']}%\n")
            f.write(f"- **Available Memory:** {sys_info['memory_available']} MB\n\n")
            
            f.write("## ⚡ Optimizations Applied\n\n")
            for opt in self.optimization_results["optimizations_applied"]:
                f.write(f"- ✅ {opt}\n")
            
            f.write("\n## 💡 Recommendations\n\n")
            for rec in self.optimization_results["recommendations"]:
                f.write(f"- {rec}\n")


def main():
    """Ana fonksiyon"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Collective Memory Performance Optimizer")
    parser.add_argument("--project-root", help="Project root directory", default=None)
    parser.add_argument("--output", help="Output report path", default=None)
    
    args = parser.parse_args()
    
    optimizer = PerformanceOptimizer(args.project_root)
    
    if args.output:
        optimizer.report_path = Path(args.output)
    
    try:
        optimizer.run_optimization()
    except KeyboardInterrupt:
        print("\n⚠️  Optimization interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Optimization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 