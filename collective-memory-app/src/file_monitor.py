#!/usr/bin/env python3
"""
File Monitor System - /data klasörü için real-time monitoring
Markdown dosyalarını izler ve değişiklikleri tespit eder
"""

import os
import time
import logging
import threading
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Style
from typing import Dict, List, Callable, Optional, Union

# Colorama initialize
init()


class FileChangeHandler(FileSystemEventHandler):
    """Dosya değişikliklerini handle eden sınıf"""

    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
        self.file_extensions = {".md", ".markdown", ".txt"}
        self.ignored_paths = {"__pycache__", ".git", ".vscode", "node_modules"}

    def _should_process(self, file_path: str) -> bool:
        """Dosyanın işlenmesi gerekip gerekmediğini kontrol eder"""
        path = Path(file_path)

        # Ignore directories
        if path.is_dir():
            return False

        # Check file extension
        if path.suffix.lower() not in self.file_extensions:
            return False

        # Check ignored paths
        for ignored in self.ignored_paths:
            if ignored in str(path):
                return False

        return True

    def on_created(self, event):
        """Dosya oluşturulduğunda çalışır"""
        if self._should_process(event.src_path):
            self._notify_change("created", event.src_path)

    def on_modified(self, event):
        """Dosya değiştirildiğinde çalışır"""
        if self._should_process(event.src_path):
            self._notify_change("modified", event.src_path)

    def on_deleted(self, event):
        """Dosya silindiğinde çalışır"""
        if self._should_process(event.src_path):
            self._notify_change("deleted", event.src_path)

    def on_moved(self, event):
        """Dosya taşındığında çalışır"""
        if self._should_process(event.src_path):
            self._notify_change("moved", event.src_path, event.dest_path)

    def _notify_change(
        self, event_type: str, src_path: str, dest_path: Optional[str] = None
    ):
        """Değişiklik bildirimini yapar"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(
            f"{Fore.BLUE}[{timestamp}] {Fore.GREEN}FILE {event_type.upper()}: {Fore.YELLOW}{src_path}{Style.RESET_ALL}"
        )

        if dest_path:
            print(
                f"{Fore.BLUE}[{timestamp}] {Fore.GREEN}MOVED TO: {Fore.YELLOW}{dest_path}{Style.RESET_ALL}"
            )

        if self.callback:
            self.callback(event_type, src_path, dest_path)


class DataFolderMonitor:
    """Data klasörü monitoring sistemi"""

    def __init__(self, data_path: str = "./data", callback: Optional[Callable] = None):
        self.data_path = Path(data_path).resolve()
        self.callback = callback
        self.observer = None
        self.is_running = False
        self.file_stats = {}

        # Logging setup
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def start_monitoring(self):
        """Monitoring'i başlatır"""
        if not self.data_path.exists():
            print(
                f"{Fore.RED}ERROR: Data path does not exist: {self.data_path}{Style.RESET_ALL}"
            )
            return False

        print(
            f"{Fore.GREEN}🔍 Starting file monitoring for: {Fore.YELLOW}{self.data_path}{Style.RESET_ALL}"
        )

        # Event handler oluştur
        event_handler = FileChangeHandler(callback=self._on_file_change)

        # Observer oluştur ve başlat
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.data_path), recursive=True)
        self.observer.start()

        self.is_running = True
        print(f"{Fore.GREEN}✅ File monitoring started successfully{Style.RESET_ALL}")

        # İlk tarama yap
        self._initial_scan()

        return True

    def stop_monitoring(self):
        """Monitoring'i durdurur"""
        if self.observer and self.is_running:
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            print(f"{Fore.YELLOW}⏹️  File monitoring stopped{Style.RESET_ALL}")

    def _initial_scan(self):
        """İlk tarama - mevcut dosyaları tespit eder"""
        print(f"{Fore.CYAN}🔍 Performing initial scan...{Style.RESET_ALL}")

        file_count = 0
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in {".md", ".markdown", ".txt"}:
                    file_count += 1
                    self.file_stats[str(file_path)] = {
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                        "created": datetime.fromtimestamp(file_path.stat().st_ctime),
                    }

        print(f"{Fore.GREEN}📊 Found {file_count} markdown files{Style.RESET_ALL}")

    def _on_file_change(
        self, event_type: str, src_path: str, dest_path: Optional[str] = None
    ):
        """Dosya değişikliği callback'i"""
        if self.callback:
            self.callback(event_type, src_path, dest_path)

        # File stats güncelle
        if event_type in ["created", "modified"]:
            file_path = Path(src_path)
            if file_path.exists():
                self.file_stats[str(file_path)] = {
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime),
                    "created": datetime.fromtimestamp(file_path.stat().st_ctime),
                }
        elif event_type == "deleted":
            self.file_stats.pop(str(src_path), None)

    def get_file_stats(self) -> Dict:
        """Dosya istatistiklerini döndürür"""
        return self.file_stats.copy()

    def run_forever(self):
        """Sürekli çalışır - daemon mode"""
        if not self.is_running:
            if not self.start_monitoring():
                return

        try:
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Monitoring interrupted by user{Style.RESET_ALL}")
        finally:
            self.stop_monitoring()

    def get_monitored_files(self) -> List[str]:
        """İzlenen dosyaların listesini döndürür"""
        return list(self.file_stats.keys())

    def get_file_info(self, file_path: str) -> Optional[Dict]:
        """Belirli bir dosyanın bilgilerini döndürür"""
        return self.file_stats.get(file_path)


def main():
    """Ana fonksiyon - test için"""

    def file_change_callback(
        event_type: str, src_path: str, dest_path: Optional[str] = None
    ):
        """Test callback fonksiyonu"""
        print(f"{Fore.MAGENTA}📝 Callback: {event_type} - {src_path}{Style.RESET_ALL}")

    # Monitor oluştur
    monitor = DataFolderMonitor(
        data_path="../data",  # collective-memory-app/src'dan data'ya
        callback=file_change_callback,
    )

    print(f"{Fore.CYAN}🚀 Data Folder Monitor Starting...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop monitoring{Style.RESET_ALL}")

    # Sürekli çalışır
    monitor.run_forever()


if __name__ == "__main__":
    main()
