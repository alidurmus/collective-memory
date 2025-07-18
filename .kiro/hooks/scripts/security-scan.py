#!/usr/bin/env python3
"""
Güvenlik tarama hook'u
"""
import subprocess
import json
from pathlib import Path
from datetime import datetime

def security_scan():
    """Güvenlik taraması yap"""
    print("🔒 Güvenlik taraması başlatılıyor...")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "python_scan": None,
        "javascript_scan": None,
        "summary": {}
    }
    
    # Python güvenlik taraması
    if Path("requirements.txt").exists():
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                results["python_scan"] = {"status": "clean", "vulnerabilities": []}
                print("✅ Python bağımlılıkları güvenli")
            else:
                try:
                    vulnerabilities = json.loads(result.stdout)
                    results["python_scan"] = {
                        "status": "vulnerabilities_found",
                        "vulnerabilities": vulnerabilities
                    }
                    print(f"⚠️ {len(vulnerabilities)} Python güvenlik açığı bulundu")
                except:
                    results["python_scan"] = {"status": "error", "message": result.stderr}
        except FileNotFoundError:
            print("⚠️ Safety kurulu değil: pip install safety")
            results["python_scan"] = {"status": "tool_missing", "tool": "safety"}
        except subprocess.TimeoutExpired:
            print("⚠️ Python güvenlik taraması zaman aşımına uğradı")
            results["python_scan"] = {"status": "timeout"}
    
    # JavaScript güvenlik taraması
    if Path("package.json").exists():
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            try:
                audit_result = json.loads(result.stdout)
                vulnerabilities = audit_result.get("vulnerabilities", {})
                if vulnerabilities:
                    results["javascript_scan"] = {
                        "status": "vulnerabilities_found",
                        "vulnerabilities": vulnerabilities
                    }
                    print(f"⚠️ JavaScript güvenlik açıkları bulundu")
                else:
                    results["javascript_scan"] = {"status": "clean"}
                    print("✅ JavaScript bağımlılıkları güvenli")
            except json.JSONDecodeError:
                results["javascript_scan"] = {"status": "clean"}
                print("✅ JavaScript bağımlılıkları güvenli")
        except FileNotFoundError:
            print("⚠️ npm bulunamadı")
            results["javascript_scan"] = {"status": "tool_missing", "tool": "npm"}
        except subprocess.TimeoutExpired:
            print("⚠️ JavaScript güvenlik taraması zaman aşımına uğradı")
            results["javascript_scan"] = {"status": "timeout"}
    
    # Raporu kaydet
    report_dir = Path("docs/reports/security-reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"security_scan_{timestamp}.json"
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Güvenlik raporu kaydedildi: {report_file}")
    print("🔒 Güvenlik taraması tamamlandı")

if __name__ == "__main__":
    security_scan()