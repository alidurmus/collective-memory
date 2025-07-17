#!/usr/bin/env python3
"""
Chat CLI - JSON Konuşma Yönetimi için Komut Satırı Arayüzü
Collective Memory JSON Chat Manager CLI interface
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from colorama import Fore, Style, init
import subprocess
import os

# Initialize colorama
init()

from json_chat_manager import JSONChatManager


class ChatCLI:
    """JSON Chat Manager için CLI sınıfı"""

    def __init__(self, data_folder: str = None):
        self.chat_manager = JSONChatManager(data_folder)
        self.data_folder = data_folder or os.getcwd()

    def create_conversation(
        self, title: str, project_path: str = None, initial_message: str = None
    ):
        """Yeni konuşma oluştur"""
        try:
            conversation_id = self.chat_manager.create_conversation(
                title=title,
                project_path=project_path or self.data_folder,
                initial_message=initial_message,
            )

            print(f"{Fore.GREEN}✅ Yeni konuşma oluşturuldu:{Style.RESET_ALL}")
            print(f"   ID: {conversation_id}")
            print(f"   Başlık: {title}")
            print(f"   Proje: {project_path or self.data_folder}")

            return conversation_id

        except Exception as e:
            print(f"{Fore.RED}❌ Konuşma oluşturulamadı: {e}{Style.RESET_ALL}")
            return None

    def add_message(self, conversation_id: str, content: str, role: str = "user"):
        """Konuşmaya mesaj ekle"""
        try:
            message_id = self.chat_manager.add_message(
                conversation_id=conversation_id, role=role, content=content
            )

            print(f"{Fore.GREEN}✅ Mesaj eklendi:{Style.RESET_ALL}")
            print(f"   Mesaj ID: {message_id}")
            print(f"   Rol: {role}")
            print(f"   İçerik: {content[:100]}{'...' if len(content) > 100 else ''}")

            return message_id

        except Exception as e:
            print(f"{Fore.RED}❌ Mesaj eklenemedi: {e}{Style.RESET_ALL}")
            return None

    def list_conversations(self, limit: int = 20, project_path: str = None):
        """Konuşmaları listele"""
        try:
            conversations = self.chat_manager.search_conversations(
                project_path=project_path, limit=limit
            )

            if not conversations:
                print(f"{Fore.YELLOW}📭 Hiç konuşma bulunamadı{Style.RESET_ALL}")
                return

            print(
                f"{Fore.CYAN}📋 Konuşmalar ({len(conversations)} adet):{Style.RESET_ALL}\n"
            )

            for i, conv in enumerate(conversations, 1):
                created_date = conv["created_at"][:10]  # YYYY-MM-DD
                updated_date = conv["updated_at"][:10]

                print(f"{Fore.WHITE}{i:2d}.{Style.RESET_ALL} {conv['title']}")
                print(f"    ID: {conv['id']}")
                print(f"    Proje: {Path(conv['project_path']).name}")
                print(f"    Mesajlar: {conv['message_count']}")
                print(f"    Oluşturulma: {created_date}")
                print(f"    Güncellenme: {updated_date}")
                if conv["tags"]:
                    print(f"    Etiketler: {', '.join(conv['tags'])}")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Konuşmalar listelenemedi: {e}{Style.RESET_ALL}")

    def show_conversation(self, conversation_id: str):
        """Konuşma detaylarını göster"""
        try:
            conversation = self.chat_manager.load_conversation(conversation_id)
            if not conversation:
                print(
                    f"{Fore.RED}❌ Konuşma bulunamadı: {conversation_id}{Style.RESET_ALL}"
                )
                return

            print(f"{Fore.CYAN}💬 Konuşma Detayları:{Style.RESET_ALL}\n")
            print(f"{Fore.WHITE}Başlık:{Style.RESET_ALL} {conversation.title}")
            print(f"{Fore.WHITE}ID:{Style.RESET_ALL} {conversation.id}")
            print(f"{Fore.WHITE}Proje:{Style.RESET_ALL} {conversation.project_path}")
            print(
                f"{Fore.WHITE}Oluşturulma:{Style.RESET_ALL} {conversation.created_at}"
            )
            print(
                f"{Fore.WHITE}Güncellenme:{Style.RESET_ALL} {conversation.updated_at}"
            )
            print(
                f"{Fore.WHITE}Mesaj Sayısı:{Style.RESET_ALL} {len(conversation.messages)}"
            )
            if conversation.tags:
                print(
                    f"{Fore.WHITE}Etiketler:{Style.RESET_ALL} {', '.join(conversation.tags)}"
                )

            print(f"\n{Fore.CYAN}📝 Mesajlar:{Style.RESET_ALL}\n")

            for i, msg in enumerate(conversation.messages, 1):
                role_color = {
                    "user": Fore.BLUE,
                    "assistant": Fore.GREEN,
                    "system": Fore.YELLOW,
                }.get(msg.role, Fore.WHITE)

                role_emoji = {"user": "👤", "assistant": "🤖", "system": "⚙️"}.get(
                    msg.role, "❓"
                )

                timestamp = msg.timestamp[:19].replace("T", " ")  # YYYY-MM-DD HH:MM:SS

                print(
                    f"{role_color}{role_emoji} {msg.role.upper()}{Style.RESET_ALL} - {timestamp}"
                )
                print(f"{msg.content}\n")
                print("-" * 80 + "\n")

        except Exception as e:
            print(f"{Fore.RED}❌ Konuşma gösterilemedi: {e}{Style.RESET_ALL}")

    def search_conversations(self, query: str, limit: int = 10):
        """Konuşmalarda arama yap"""
        try:
            conversations = self.chat_manager.search_conversations(
                query=query, limit=limit
            )

            if not conversations:
                print(
                    f"{Fore.YELLOW}🔍 '{query}' için sonuç bulunamadı{Style.RESET_ALL}"
                )
                return

            print(
                f"{Fore.CYAN}🔍 Arama Sonuçları '{query}' ({len(conversations)} adet):{Style.RESET_ALL}\n"
            )

            for i, conv in enumerate(conversations, 1):
                print(f"{Fore.WHITE}{i}.{Style.RESET_ALL} {conv['title']}")
                print(f"   ID: {conv['id']}")
                print(f"   Proje: {Path(conv['project_path']).name}")
                print(f"   Mesajlar: {conv['message_count']}")
                print()

        except Exception as e:
            print(f"{Fore.RED}❌ Arama yapılamadı: {e}{Style.RESET_ALL}")

    def export_conversation(
        self, conversation_id: str, format: str = "json", output_path: str = None
    ):
        """Konuşmayı export et"""
        try:
            export_path = self.chat_manager.export_conversation(conversation_id, format)
            if not export_path:
                print(f"{Fore.RED}❌ Export başarısız{Style.RESET_ALL}")
                return

            # Eğer output_path belirtildiyse dosyayı taşı
            if output_path:
                import shutil

                shutil.move(export_path, output_path)
                export_path = output_path

            print(f"{Fore.GREEN}✅ Konuşma export edildi:{Style.RESET_ALL}")
            print(f"   Dosya: {export_path}")
            print(f"   Format: {format}")

        except Exception as e:
            print(f"{Fore.RED}❌ Export başarısız: {e}{Style.RESET_ALL}")

    def show_stats(self):
        """Konuşma istatistiklerini göster"""
        try:
            stats = self.chat_manager.get_conversation_stats()

            print(f"{Fore.CYAN}📊 Konuşma İstatistikleri:{Style.RESET_ALL}\n")
            print(
                f"{Fore.WHITE}Toplam Konuşma:{Style.RESET_ALL} {stats['total_conversations']}"
            )
            print(
                f"{Fore.WHITE}Toplam Mesaj:{Style.RESET_ALL} {stats['total_messages']}"
            )
            print(
                f"{Fore.WHITE}Storage Boyutu:{Style.RESET_ALL} {stats['storage_size']}"
            )
            if stats["last_activity"]:
                print(
                    f"{Fore.WHITE}Son Aktivite:{Style.RESET_ALL} {stats['last_activity'][:19].replace('T', ' ')}"
                )

            if stats["projects"]:
                print(f"\n{Fore.CYAN}📁 Projeler:{Style.RESET_ALL}")
                for project, count in stats["projects"].items():
                    print(f"   {project}: {count} konuşma")

            if stats["tags"]:
                print(f"\n{Fore.CYAN}🏷️  Etiketler:{Style.RESET_ALL}")
                for tag, count in stats["tags"].items():
                    print(f"   {tag}: {count} konuşma")

        except Exception as e:
            print(f"{Fore.RED}❌ İstatistikler alınamadı: {e}{Style.RESET_ALL}")

    def import_from_cursor(self):
        """Cursor chat'lerini import et"""
        try:
            from cursor_reader import EnhancedCursorDatabaseReader

            cursor_reader = EnhancedCursorDatabaseReader()

            print(f"{Fore.CYAN}🔄 Cursor chat'leri import ediliyor...{Style.RESET_ALL}")
            imported_count = self.chat_manager.import_from_cursor(cursor_reader)

            print(
                f"{Fore.GREEN}✅ {imported_count} konuşma Cursor'dan import edildi{Style.RESET_ALL}"
            )

        except Exception as e:
            print(f"{Fore.RED}❌ Cursor import başarısız: {e}{Style.RESET_ALL}")


def main():
    """Ana CLI fonksiyonu"""
    parser = argparse.ArgumentParser(
        description="Collective Memory JSON Chat Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnek Kullanımlar:
  # Yeni konuşma oluştur
  python chat_cli.py create "Yeni Proje Planı" --project "/path/to/project"
  
  # Konuşmaları listele
  python chat_cli.py list --limit 10
  
  # Konuşma detaylarını göster
  python chat_cli.py show CONVERSATION_ID
  
  # Konuşmalarda arama yap
  python chat_cli.py search "Context7 ERP"
  
  # İstatistikleri göster
  python chat_cli.py stats
  
  # Cursor'dan import et
  python chat_cli.py import-cursor
        """,
    )

    parser.add_argument("--data-folder", type=str, help="Veri klasörü yolu")

    subparsers = parser.add_subparsers(dest="command", help="Komutlar")

    # Create conversation
    create_parser = subparsers.add_parser("create", help="Yeni konuşma oluştur")
    create_parser.add_argument("title", help="Konuşma başlığı")
    create_parser.add_argument("--project", type=str, help="Proje yolu")
    create_parser.add_argument("--message", type=str, help="İlk mesaj")

    # Add message
    message_parser = subparsers.add_parser("add-message", help="Konuşmaya mesaj ekle")
    message_parser.add_argument("conversation_id", help="Konuşma ID")
    message_parser.add_argument("content", help="Mesaj içeriği")
    message_parser.add_argument(
        "--role", default="user", choices=["user", "assistant", "system"]
    )

    # List conversations
    list_parser = subparsers.add_parser("list", help="Konuşmaları listele")
    list_parser.add_argument(
        "--limit", type=int, default=20, help="Maksimum sonuç sayısı"
    )
    list_parser.add_argument("--project", type=str, help="Proje filtresi")

    # Show conversation
    show_parser = subparsers.add_parser("show", help="Konuşma detaylarını göster")
    show_parser.add_argument("conversation_id", help="Konuşma ID")

    # Search conversations
    search_parser = subparsers.add_parser("search", help="Konuşmalarda arama yap")
    search_parser.add_argument("query", help="Arama sorgusu")
    search_parser.add_argument(
        "--limit", type=int, default=10, help="Maksimum sonuç sayısı"
    )

    # Export conversation
    export_parser = subparsers.add_parser("export", help="Konuşmayı export et")
    export_parser.add_argument("conversation_id", help="Konuşma ID")
    export_parser.add_argument("--format", choices=["json", "markdown"], default="json")
    export_parser.add_argument("--output", type=str, help="Çıktı dosya yolu")

    # Stats
    subparsers.add_parser("stats", help="İstatistikleri göster")

    # Import from Cursor
    subparsers.add_parser("import-cursor", help="Cursor chat'lerini import et")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = ChatCLI(args.data_folder)

    try:
        if args.command == "create":
            cli.create_conversation(args.title, args.project, args.message)

        elif args.command == "add-message":
            cli.add_message(args.conversation_id, args.content, args.role)

        elif args.command == "list":
            cli.list_conversations(args.limit, args.project)

        elif args.command == "show":
            cli.show_conversation(args.conversation_id)

        elif args.command == "search":
            cli.search_conversations(args.query, args.limit)

        elif args.command == "export":
            cli.export_conversation(args.conversation_id, args.format, args.output)

        elif args.command == "stats":
            cli.show_stats()

        elif args.command == "import-cursor":
            cli.import_from_cursor()

    except KeyboardInterrupt:
        print(
            f"\n{Fore.YELLOW}⚠️  İşlem kullanıcı tarafından durduruldu{Style.RESET_ALL}"
        )
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}❌ Beklenmeyen hata: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
