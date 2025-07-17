#!/usr/bin/env python3
"""
Agent Hook Manager - Kiro hooks'larını yöneten ana script
"""

import os
import sys
import json
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class HookManager:
    def __init__(self, hooks_config_path=".kiro/hooks/hooks.json"):
        self.hooks_config_path = Path(hooks_config_path)
        self.hooks = {}
        self.observers = []
        self.running = False
        self.load_hooks()

    def load_hooks(self):
        """Hook konfigürasyonunu yükle"""
        if not self.hooks_config_path.exists():
            print(f"❌ Hook konfigürasyonu bulunamadı: {self.hooks_config_path}")
            return

        try:
            with open(self.hooks_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            self.hooks = {
                hook["id"]: hook
                for hook in config["hooks"]
                if hook.get("enabled", True)
            }
            self.global_settings = config.get("global_settings", {})

            print(f"✅ {len(self.hooks)} hook yüklendi")

        except Exception as e:
            print(f"❌ Hook konfigürasyonu yüklenemedi: {e}")

    def start(self):
        """Hook manager'ı başlat"""
        print("🚀 Agent Hook Manager başlatılıyor...")

        self.running = True

        # File save hooks için file watcher başlat
        self.setup_file_watchers()

        # Scheduled hooks için scheduler başlat
        self.setup_scheduler()

        print("✅ Agent Hook Manager aktif!")
        print("📋 Aktif hooks:")
        for hook_id, hook in self.hooks.items():
            trigger_type = hook["trigger"]["type"]
            print(f"  - {hook['name']} ({trigger_type})")

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Hook manager'ı durdur"""
        print("\n🛑 Agent Hook Manager durduruluyor...")
        self.running = False

        for observer in self.observers:
            observer.stop()
            observer.join()

        print("✅ Agent Hook Manager durduruldu")

    def setup_file_watchers(self):
        """Dosya değişikliklerini izleyen watcher'ları kur"""
        file_save_hooks = [
            h for h in self.hooks.values() if h["trigger"]["type"] == "file_save"
        ]

        if not file_save_hooks:
            return

        # Tüm pattern'leri topla
        all_patterns = set()
        for hook in file_save_hooks:
            patterns = hook["trigger"].get("patterns", [])
            all_patterns.update(patterns)

        if all_patterns:
            handler = FileChangeHandler(self, list(all_patterns))
            observer = Observer()
            observer.schedule(handler, ".", recursive=True)
            observer.start()
            self.observers.append(observer)

            print(f"👁️ Dosya izleme başlatıldı: {len(all_patterns)} pattern")

    def setup_scheduler(self):
        """Zamanlanmış hook'lar için scheduler kur"""
        scheduled_hooks = [
            h for h in self.hooks.values() if h["trigger"]["type"] == "scheduled"
        ]

        if scheduled_hooks:
            scheduler_thread = threading.Thread(
                target=self.run_scheduler, args=(scheduled_hooks,)
            )
            scheduler_thread.daemon = True
            scheduler_thread.start()

            print(f"⏰ Scheduler başlatıldı: {len(scheduled_hooks)} zamanlanmış hook")

    def run_scheduler(self, scheduled_hooks):
        """Zamanlanmış hook'ları çalıştır"""
        # Basit scheduler implementasyonu
        # Gerçek projede crontab veya APScheduler kullanılabilir
        while self.running:
            current_time = datetime.now()

            for hook in scheduled_hooks:
                # Basit zaman kontrolü (gerçek cron parsing gerekir)
                # Şimdilik her 6 saatte bir çalıştır
                if current_time.minute == 0 and current_time.hour % 6 == 0:
                    self.execute_hook(hook["id"], context={"trigger": "scheduled"})

            time.sleep(60)  # Her dakika kontrol et

    def execute_hook(self, hook_id, context=None):
        """Hook'u çalıştır"""
        if hook_id not in self.hooks:
            print(f"❌ Hook bulunamadı: {hook_id}")
            return

        hook = self.hooks[hook_id]

        print(f"🔄 Hook çalıştırılıyor: {hook['name']}")

        try:
            for action in hook["actions"]:
                self.execute_action(action, context or {})

            print(f"✅ Hook başarılı: {hook['name']}")

        except Exception as e:
            print(f"❌ Hook hatası ({hook['name']}): {e}")

    def execute_action(self, action, context):
        """Hook action'ını çalıştır"""
        action_type = action["type"]
        config = action.get("config", {})

        if action_type == "run_tests":
            self.run_tests_action(config, context)
        elif action_type == "format_code":
            self.format_code_action(config, context)
        elif action_type == "security_scan":
            self.security_scan_action(config, context)
        elif action_type == "generate_test_report":
            self.generate_test_report_action(config, context)
        elif action_type == "health_check":
            self.health_check_action(config, context)
        elif action_type == "cleanup":
            self.cleanup_action(config, context)
        else:
            print(f"⚠️ Bilinmeyen action türü: {action_type}")

    def run_tests_action(self, config, context):
        """Test çalıştırma action'ı"""
        changed_file = context.get("file_path", "")

        if changed_file:
            # Test runner script'ini çalıştır
            cmd = [
                "python",
                ".kiro/hooks/scripts/test-runner.py",
                changed_file,
                json.dumps(config),
            ]

            subprocess.run(cmd, cwd=Path.cwd())

    def format_code_action(self, config, context):
        """Kod formatlama action'ı"""
        changed_file = context.get("file_path", "")

        if not changed_file:
            return

        file_path = Path(changed_file)

        if file_path.suffix == ".py":
            # Python formatla
            formatter = config.get("python_formatter", "black")
            args = config.get("python_args", [])
            cmd = [formatter] + args + [str(file_path)]

        elif file_path.suffix in [".js", ".ts", ".jsx", ".tsx"]:
            # JavaScript formatla
            formatter = config.get("javascript_formatter", "prettier")
            args = config.get("javascript_args", ["--write"])
            cmd = [formatter] + args + [str(file_path)]

        else:
            return

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Kod formatlandı: {file_path}")
            else:
                print(f"❌ Formatlama hatası: {result.stderr}")
        except Exception as e:
            print(f"❌ Formatlama hatası: {e}")

    def security_scan_action(self, config, context):
        """Güvenlik taraması action'ı"""
        print("🔒 Güvenlik taraması başlatılıyor...")

        # Python güvenlik taraması
        if Path("requirements.txt").exists():
            try:
                result = subprocess.run(
                    ["safety", "check"], capture_output=True, text=True
                )
                print("🐍 Python güvenlik taraması tamamlandı")
            except FileNotFoundError:
                print("⚠️ Safety kurulu değil: pip install safety")

        # JavaScript güvenlik taraması
        if Path("package.json").exists():
            try:
                result = subprocess.run(
                    ["npm", "audit"], capture_output=True, text=True
                )
                print("⚛️ JavaScript güvenlik taraması tamamlandı")
            except FileNotFoundError:
                print("⚠️ npm bulunamadı")

    def generate_test_report_action(self, config, context):
        """Test raporu oluşturma action'ı"""
        print("📊 Kapsamlı test raporu oluşturuluyor...")

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "backend_tests": {},
            "frontend_tests": {},
            "e2e_tests": {},
        }

        # Backend testleri
        if config.get("backend_tests"):
            try:
                result = subprocess.run(
                    config["backend_tests"].split(),
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                report_data["backend_tests"] = {
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            except Exception as e:
                report_data["backend_tests"] = {"error": str(e)}

        # Frontend testleri
        if config.get("frontend_tests"):
            try:
                result = subprocess.run(
                    config["frontend_tests"].split(),
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd="collective-memory-app/frontend",
                )
                report_data["frontend_tests"] = {
                    "exit_code": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            except Exception as e:
                report_data["frontend_tests"] = {"error": str(e)}

        # Raporu kaydet
        output_path = Path(config.get("output_path", "docs/reports/test-reports/"))
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"comprehensive_test_report_{timestamp}.json"

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"📋 Test raporu kaydedildi: {report_file}")

    def health_check_action(self, config, context):
        """Sistem sağlık kontrolü action'ı"""
        print("🏥 Sistem sağlık kontrolü başlatılıyor...")

        health_data = {"timestamp": datetime.now().isoformat(), "checks": {}}

        checks = config.get("checks", [])

        for check in checks:
            if check == "disk_space":
                health_data["checks"]["disk_space"] = self.check_disk_space()
            elif check == "memory_usage":
                health_data["checks"]["memory_usage"] = self.check_memory_usage()
            elif check == "database_connection":
                health_data["checks"]["database_connection"] = self.check_database()

        # Raporu kaydet
        output_path = Path(config.get("report_path", "docs/reports/system-health/"))
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_path / f"health_check_{timestamp}.json"

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(health_data, f, indent=2, ensure_ascii=False)

        print(f"🏥 Sağlık raporu kaydedildi: {report_file}")

    def check_disk_space(self):
        """Disk alanını kontrol et"""
        try:
            import shutil

            total, used, free = shutil.disk_usage(".")
            usage_percent = (used / total) * 100

            return {
                "status": "healthy" if usage_percent < 80 else "warning",
                "usage_percent": round(usage_percent, 2),
                "free_gb": round(free / (1024**3), 2),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def check_memory_usage(self):
        """Bellek kullanımını kontrol et"""
        try:
            import psutil

            memory = psutil.virtual_memory()

            return {
                "status": "healthy" if memory.percent < 80 else "warning",
                "usage_percent": memory.percent,
                "available_gb": round(memory.available / (1024**3), 2),
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def check_database(self):
        """Veritabanı bağlantısını kontrol et"""
        try:
            import sqlite3

            db_files = list(Path(".").glob("**/*.db"))

            if not db_files:
                return {"status": "warning", "message": "Veritabanı dosyası bulunamadı"}

            # İlk veritabanını test et
            conn = sqlite3.connect(db_files[0])
            conn.execute("SELECT 1")
            conn.close()

            return {"status": "healthy", "database_count": len(db_files)}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def cleanup_action(self, config, context):
        """Temizlik action'ı"""
        print("🧹 Geçici dosyalar temizleniyor...")

        patterns = config.get("patterns", [])
        max_age_days = config.get("max_age_days", 7)
        dry_run = config.get("dry_run", False)

        deleted_count = 0

        for pattern in patterns:
            for file_path in Path(".").glob(pattern):
                if file_path.is_file():
                    # Dosya yaşını kontrol et
                    file_age = time.time() - file_path.stat().st_mtime
                    if file_age > (max_age_days * 24 * 3600):
                        if not dry_run:
                            file_path.unlink()
                        deleted_count += 1
                        print(f"🗑️ Silindi: {file_path}")

        print(
            f"✅ Temizlik tamamlandı: {deleted_count} dosya {'silinecek' if dry_run else 'silindi'}"
        )


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, hook_manager, patterns):
        self.hook_manager = hook_manager
        self.patterns = patterns

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Pattern'leri kontrol et
        for pattern in self.patterns:
            if file_path.match(pattern):
                # İlgili hook'ları bul ve çalıştır
                for hook_id, hook in self.hook_manager.hooks.items():
                    if hook["trigger"]["type"] == "file_save" and any(
                        file_path.match(p) for p in hook["trigger"].get("patterns", [])
                    ):

                        context = {"file_path": str(file_path), "trigger": "file_save"}
                        self.hook_manager.execute_hook(hook_id, context)
                break


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "start":
            manager = HookManager()
            manager.start()
        elif command == "status":
            manager = HookManager()
            print(f"📋 Yüklü hooks: {len(manager.hooks)}")
            for hook_id, hook in manager.hooks.items():
                print(
                    f"  - {hook['name']} ({'aktif' if hook.get('enabled', True) else 'pasif'})"
                )
        elif command == "test":
            # Test hook'u çalıştır
            manager = HookManager()
            if len(sys.argv) > 2:
                hook_id = sys.argv[2]
                manager.execute_hook(hook_id, {"trigger": "manual"})
            else:
                print("Hook ID belirtiniz: python hook-manager.py test <hook_id>")
        else:
            print("Kullanım: python hook-manager.py [start|status|test]")
    else:
        print("Kullanım: python hook-manager.py [start|status|test]")


if __name__ == "__main__":
    main()
