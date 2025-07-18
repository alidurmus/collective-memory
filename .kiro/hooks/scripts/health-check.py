#!/usr/bin/env python3
"""
Sistem sağlık kontrolü hook'u
"""
import os
import sys
import json
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime

def check_system_health():
    """Sistem sağlığını kontrol et"""
    print("🏥 Sistem sağlık kontrolü başlatılıyor...")
    
    health_data = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "healthy",
        "checks": {}
    }
    
    # Disk alanı kontrolü
    try:
        total, used, free = shutil.disk_usage(".")
        usage_percent = (used / total) * 100
        
        disk_status = "healthy" if usage_percent < 80 else "warning" if usage_percent < 90 else "critical"
        
        health_data["checks"]["disk_space"] = {
            "status": disk_status,
            "usage_percent": round(usage_percent, 2),
            "free_gb": round(free / (1024**3), 2),
            "total_gb": round(total / (1024**3), 2)
        }
        
        print(f"💾 Disk kullanımı: %{usage_percent:.1f} ({disk_status})")
        
    except Exception as e:
        health_data["checks"]["disk_space"] = {"status": "error", "error": str(e)}
        print(f"❌ Disk kontrolü hatası: {e}")
    
    # Bellek kontrolü (basit)
    try:
        # Windows için basit bellek kontrolü
        if os.name == 'nt':
            import subprocess
            result = subprocess.run(
                ['wmic', 'OS', 'get', 'TotalVisibleMemorySize,FreePhysicalMemory', '/format:csv'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    data = lines[1].split(',')
                    if len(data) >= 3:
                        free_kb = int(data[1]) if data[1].isdigit() else 0
                        total_kb = int(data[2]) if data[2].isdigit() else 0
                        if total_kb > 0:
                            usage_percent = ((total_kb - free_kb) / total_kb) * 100
                            memory_status = "healthy" if usage_percent < 80 else "warning"
                            
                            health_data["checks"]["memory"] = {
                                "status": memory_status,
                                "usage_percent": round(usage_percent, 2),
                                "free_gb": round(free_kb / (1024**2), 2)
                            }
                            
                            print(f"🧠 Bellek kullanımı: %{usage_percent:.1f} ({memory_status})")
        
        if "memory" not in health_data["checks"]:
            health_data["checks"]["memory"] = {"status": "unknown", "message": "Bellek bilgisi alınamadı"}
            print("⚠️ Bellek bilgisi alınamadı")
            
    except Exception as e:
        health_data["checks"]["memory"] = {"status": "error", "error": str(e)}
        print(f"❌ Bellek kontrolü hatası: {e}")
    
    # Veritabanı kontrolü
    try:
        db_files = list(Path(".").glob("**/*.db"))
        
        if db_files:
            db_status = "healthy"
            db_info = []
            
            for db_file in db_files[:3]:  # İlk 3 veritabanını kontrol et
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    conn.close()
                    
                    db_info.append({
                        "file": str(db_file),
                        "tables": len(tables),
                        "size_mb": round(db_file.stat().st_size / (1024**2), 2)
                    })
                    
                except Exception as e:
                    db_status = "warning"
                    db_info.append({
                        "file": str(db_file),
                        "error": str(e)
                    })
            
            health_data["checks"]["database"] = {
                "status": db_status,
                "database_count": len(db_files),
                "databases": db_info
            }
            
            print(f"🗄️ Veritabanları: {len(db_files)} dosya ({db_status})")
            
        else:
            health_data["checks"]["database"] = {
                "status": "info",
                "message": "Veritabanı dosyası bulunamadı"
            }
            print("ℹ️ Veritabanı dosyası bulunamadı")
            
    except Exception as e:
        health_data["checks"]["database"] = {"status": "error", "error": str(e)}
        print(f"❌ Veritabanı kontrolü hatası: {e}")
    
    # Genel durum değerlendirmesi
    statuses = [check.get("status", "unknown") for check in health_data["checks"].values()]
    
    if "critical" in statuses:
        health_data["overall_status"] = "critical"
    elif "error" in statuses:
        health_data["overall_status"] = "error"
    elif "warning" in statuses:
        health_data["overall_status"] = "warning"
    else:
        health_data["overall_status"] = "healthy"
    
    # Raporu kaydet
    report_dir = Path("docs/reports/system-health")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"health_check_{timestamp}.json"
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(health_data, f, indent=2, ensure_ascii=False)
    
    # Son durum dosyasını güncelle
    latest_file = report_dir / "latest_health_status.json"
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(health_data, f, indent=2, ensure_ascii=False)
    
    status_emoji = {
        "healthy": "✅",
        "warning": "⚠️",
        "error": "❌",
        "critical": "🚨"
    }.get(health_data["overall_status"], "❓")
    
    print(f"{status_emoji} Genel sistem durumu: {health_data['overall_status']}")
    print(f"📋 Sağlık raporu kaydedildi: {report_file}")

if __name__ == "__main__":
    check_system_health()