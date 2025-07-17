#!/usr/bin/env python3
"""
Otomatik test çalıştırma script'i
Dosya değişikliklerine göre uygun testleri çalıştırır
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime


class TestRunner:
    def __init__(self, config):
        self.config = config
        self.project_root = Path.cwd()
        self.report_path = Path("docs/reports/test-reports")
        self.report_path.mkdir(parents=True, exist_ok=True)

    def run_python_tests(self, changed_file):
        """Python testlerini çalıştır"""
        print(f"🐍 Python testleri çalıştırılıyor: {changed_file}")

        # Test dosyasını belirle
        test_file = self.find_related_test_file(changed_file)

        if test_file and test_file.exists():
            cmd = f"python -m pytest {test_file} -v --tb=short"
        else:
            cmd = self.config.get(
                "python_command", "python -m pytest tests/ -v --tb=short"
            )

        return self.run_command(cmd, "python_tests")

    def run_javascript_tests(self, changed_file):
        """JavaScript testlerini çalıştır"""
        print(f"⚛️ JavaScript testleri çalıştırılıyor: {changed_file}")

        # Frontend dizininde mi?
        if "frontend" in str(changed_file):
            frontend_dir = self.project_root / "collective-memory-app" / "frontend"
            if frontend_dir.exists():
                os.chdir(frontend_dir)
                cmd = "npm test -- --watchAll=false"
            else:
                print("⚠️ Frontend dizini bulunamadı, test atlanıyor")
                return {"success": True, "skipped": True}
        else:
            # Root dizinde package.json yoksa test'i atla
            if not Path("package.json").exists():
                print("⚠️ package.json bulunamadı, test atlanıyor")
                return {"success": True, "skipped": True}
            cmd = self.config.get("javascript_command", "npm test")

        return self.run_command(cmd, "javascript_tests")

    def find_related_test_file(self, source_file):
        """İlgili test dosyasını bul"""
        source_path = Path(source_file)

        # Test dosyası isimleri
        possible_names = [
            f"test_{source_path.stem}.py",
            f"{source_path.stem}_test.py",
            f"test_{source_path.stem.replace('_', '')}.py",
        ]

        # Test dizinlerinde ara
        test_dirs = [
            self.project_root / "tests",
            self.project_root / "collective-memory-app" / "tests",
            source_path.parent / "tests",
        ]

        for test_dir in test_dirs:
            if test_dir.exists():
                for name in possible_names:
                    test_file = test_dir / name
                    if test_file.exists():
                        return test_file

        return None

    def run_command(self, cmd, test_type):
        """Komutu çalıştır ve sonucu kaydet"""
        start_time = time.time()

        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.config.get("timeout", 30),
            )

            end_time = time.time()
            duration = end_time - start_time

            # Sonucu kaydet
            report = {
                "timestamp": datetime.now().isoformat(),
                "test_type": test_type,
                "command": cmd,
                "duration_seconds": round(duration, 2),
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }

            self.save_report(report, test_type)

            # Türkçe bildirim
            if result.returncode == 0:
                print(f"✅ {test_type} testleri başarılı ({duration:.2f}s)")
            else:
                print(f"❌ {test_type} testleri başarısız ({duration:.2f}s)")
                print(f"Hata: {result.stderr}")

            return report

        except subprocess.TimeoutExpired:
            print(f"⏰ Test zaman aşımına uğradı: {cmd}")
            return {"success": False, "error": "timeout"}
        except Exception as e:
            print(f"❌ Test çalıştırma hatası: {e}")
            return {"success": False, "error": str(e)}

    def save_report(self, report, test_type):
        """Test raporunu kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_type}_{timestamp}.json"

        report_file = self.report_path / filename

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"📊 Test raporu kaydedildi: {report_file}")


def main():
    if len(sys.argv) < 2:
        print("Kullanım: python test-runner.py <changed_file> [config_json]")
        sys.exit(1)

    changed_file = sys.argv[1]
    config = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    runner = TestRunner(config)

    # Dosya uzantısına göre test türünü belirle
    file_ext = Path(changed_file).suffix.lower()

    if file_ext == ".py":
        runner.run_python_tests(changed_file)
    elif file_ext in [".js", ".ts", ".jsx", ".tsx"]:
        runner.run_javascript_tests(changed_file)
    else:
        print(f"⚠️ Desteklenmeyen dosya türü: {file_ext}")


if __name__ == "__main__":
    main()
