#!/usr/bin/env python3
"""
Collective Memory - Cursor AI için Akıllı Bağlam Orkestratörü
Copyright (c) 2025 - MIT License
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init()

# Local imports
from cursor_reader import CursorDatabaseReader
from context_collector import ContextCollector
from query_builder import QueryBuilder
from trigger_parser import TriggerParser
from terminal_interface import TerminalInterface
from database_manager import DatabaseManager
from file_monitor import DataFolderMonitor


class CollectiveMemory:
    """Ana uygulama sınıfı"""

    def __init__(self):
        self.version = "1.0.0"
        self.config = self.load_config()
        self.cursor_reader = CursorDatabaseReader()
        self.context_collector = ContextCollector()
        self.query_builder = QueryBuilder()
        self.trigger_parser = TriggerParser()

    def load_config(self):
        """Yapılandırma dosyasını yükle"""
        config_path = Path(__file__).parent.parent / "config" / "config.json"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return self.get_default_config()

    def get_default_config(self):
        """Varsayılan yapılandırma"""
        return {
            "cursor_db_paths": [
                "~/Library/Application Support/Cursor/User/workspaceStorage",
                "~/.config/Cursor/User/workspaceStorage",
                "%APPDATA%/Cursor/User/workspaceStorage",
            ],
            "max_context_length": 8000,
            "include_sources": {
                "cursor_rules": True,
                "past_chats": True,
                "project_docs": True,
                "git_history": False,
            },
            "query_template": "structured_prompt",
        }

    def find_trigger_comment(self, project_path):
        """Proje içinde @collect-memory tetikleyicisini bul"""
        try:
            return self.trigger_parser.find_trigger_in_project(project_path)
        except Exception as e:
            self.log_error(f"Tetikleyici bulunamadı: {e}")
            return None

    def collect_context(self, project_path, user_request):
        """Bağlam toplama ana fonksiyonu"""
        context_data = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(project_path),
            "user_request": user_request,
            "sources": {},
        }

        # 1. Proje kurallarını topla (.cursor/rules)
        if self.config["include_sources"]["cursor_rules"]:
            self.log_info("📜 Proje kuralları toplanıyor...")
            context_data["sources"]["rules"] = self.context_collector.fetch_rules(
                project_path
            )

        # 2. Geçmiş sohbetleri topla
        if self.config["include_sources"]["past_chats"]:
            self.log_info("💬 Geçmiş sohbetler toplanıyor...")
            context_data["sources"]["chats"] = self.context_collector.fetch_chats(
                project_path, self.cursor_reader
            )

        # 3. Proje dokümanlarını topla
        if self.config["include_sources"]["project_docs"]:
            self.log_info("📚 Proje dokümanları toplanıyor...")
            context_data["sources"]["docs"] = self.context_collector.fetch_docs(
                project_path
            )

        return context_data

    def run(self, args):
        """Ana çalışma fonksiyonu"""
        try:
            # Yeni query sistem komutları
            if (
                args.query
                or args.interactive
                or args.search
                or args.monitor
                or args.index
                or args.stats
            ):
                return self.run_query_system(args)

            # Mevcut dizini al
            project_path = Path.cwd()

            if args.scan:
                # Tetikleyici yorumu bul
                trigger_data = self.find_trigger_comment(project_path)
                if not trigger_data:
                    self.log_error("❌ @collect-memory tetikleyicisi bulunamadı!")
                    return False

                user_request = trigger_data["request"]
                self.log_success(f"✅ Tetikleyici bulundu: {user_request}")
            else:
                # Manuel istek
                user_request = args.request or "Genel proje bağlamı"

            # Bağlam toplama
            self.log_info(f"🔄 Bağlam toplanıyor: {user_request}")
            context_data = self.collect_context(project_path, user_request)

            # Sorgu oluştur
            self.log_info("⚙️ Yapılandırılmış sorgu oluşturuluyor...")
            query = self.query_builder.build_query(context_data)

            # Panoya kopyala
            if self.query_builder.copy_to_clipboard(query):
                self.log_success("✅ Sorgu panoya kopyalandı!")
                self.log_info("📋 Artık Cursor'a yapıştırabilirsiniz!")
                return True
            else:
                self.log_error("❌ Panoya kopyalama başarısız!")
                return False

        except Exception as e:
            self.log_error(f"❌ Hata: {e}")
            return False

    def run_query_system(self, args):
        """Yeni query sistemini çalıştırır"""
        try:
            # Terminal interface oluştur
            terminal = TerminalInterface(args.data_path)

            if args.interactive or args.query:
                # İnteraktif mod
                terminal.interactive_mode()
                return True

            elif args.search:
                # Doğrudan arama
                from query_engine import SearchQuery

                query = SearchQuery(text=args.search)
                results = terminal.query_engine.search(query)
                # Dosya kaydetme parametresi varsa kullan
                save_file = getattr(args, "save_to", None)
                terminal._display_search_results(results, query, save_file)
                return True

            elif args.monitor:
                # Dosya izleme
                terminal._start_file_monitoring()
                return True

            elif args.index:
                # Reindexing
                terminal._reindex_all_files()
                return True

            elif args.stats:
                # İstatistikler
                terminal._show_statistics()
                return True

            return False

        except Exception as e:
            self.log_error(f"❌ Query sistem hatası: {e}")
            return False

    def log_info(self, message):
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} {message}")

    def log_success(self, message):
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")

    def log_error(self, message):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {message}")


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description="Collective Memory - Cursor AI için Akıllı Bağlam Orkestratörü"
    )

    # Orijinal komutlar
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Proje içinde @collect-memory tetikleyicisini tara",
    )
    parser.add_argument(
        "--request", type=str, help="Manuel olarak bağlam isteği belirt"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    # Yeni query sistem komutları
    parser.add_argument(
        "--query", "-q", action="store_true", help="Query/arama modunu başlat"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="İnteraktif arama modu"
    )
    parser.add_argument("--search", "-s", type=str, help="Doğrudan arama yap")
    parser.add_argument(
        "--monitor", "-m", action="store_true", help="Dosya izleme modunu başlat"
    )
    parser.add_argument(
        "--index", action="store_true", help="Tüm dosyaları yeniden indeksle"
    )
    parser.add_argument(
        "--stats", action="store_true", help="Sistem istatistiklerini göster"
    )
    parser.add_argument(
        "--save-to", type=str, help="Arama sonuçlarını belirtilen dosyaya kaydet"
    )
    parser.add_argument(
        "--data-path", default="./data", help="Data klasörü yolu (varsayılan: ./data)"
    )

    args = parser.parse_args()

    # Uygulama başlat
    app = CollectiveMemory()

    # Başlık
    print(f"{Fore.CYAN}Collective Memory v{app.version}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Cursor AI Akıllı Bağlam Orkestratörü{Style.RESET_ALL}")
    print(f"{Fore.CYAN}+ Dosya İzleme + Arama + İndeksleme{Style.RESET_ALL}")
    print()

    # Yeni özellikler varsa bilgi göster
    if (
        args.query
        or args.interactive
        or args.search
        or args.monitor
        or args.index
        or args.stats
    ):
        print(
            f"{Fore.YELLOW}Query System Mode - Enhanced Features Active{Style.RESET_ALL}"
        )
        print()

    # Start system health monitoring
    try:
        from performance_monitor import start_system_monitoring

        start_system_monitoring(data_path=args.data_path, interval=60)
        print(f"{Fore.GREEN}System health monitoring started{Style.RESET_ALL}")
    except ImportError:
        print(f"{Fore.YELLOW}⚠️  Performance monitoring not available{Style.RESET_ALL}")

    # Çalıştır
    success = app.run(args)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
