#!/usr/bin/env python3
"""
Smart Context Bridge CLI - Command Line Interface
Smart Context Bridge sistemini yönetmek için terminal arayüzü
"""

import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init()

# Local imports
try:
    from smart_context_bridge import (
        SmartContextBridge,
        ContextBridgeConfig,
        ChatContext,
    )
except ImportError:
    print(f"{Fore.RED}❌ Smart Context Bridge modülü bulunamadı!{Style.RESET_ALL}")
    sys.exit(1)


class ContextBridgeCLI:
    """Smart Context Bridge CLI sınıfı"""

    def __init__(self):
        self.bridge = None
        self.config_file = ".collective-memory/config/context_bridge.json"

    def load_config(self) -> ContextBridgeConfig:
        """Konfigürasyon dosyasını yükler"""
        config_path = Path(self.config_file)

        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                return ContextBridgeConfig(**config_data)
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Config yükleme hatası: {e}{Style.RESET_ALL}")

        # Default config
        return ContextBridgeConfig()

    def save_config(self, config: ContextBridgeConfig):
        """Konfigürasyonu dosyaya kaydeder"""
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        config_dict = {
            "json_chat_path": config.json_chat_path,
            "cursor_rules_path": config.cursor_rules_path,
            "auto_context_file": config.auto_context_file,
            "context_generation_enabled": config.context_generation_enabled,
            "max_context_length": config.max_context_length,
            "min_relevance_score": config.min_relevance_score,
            "update_interval_seconds": config.update_interval_seconds,
            "max_conversations_to_analyze": config.max_conversations_to_analyze,
        }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=2)

    def cmd_start(self, args):
        """Smart Context Bridge'i başlatır"""
        print(f"{Fore.CYAN}🚀 Smart Context Bridge başlatılıyor...{Style.RESET_ALL}")

        config = self.load_config()

        # CLI args ile config'i override et
        if args.json_path:
            config.json_chat_path = args.json_path
        if args.rules_path:
            config.cursor_rules_path = args.rules_path
        if args.min_score:
            config.min_relevance_score = args.min_score
        if args.max_conversations:
            config.max_conversations_to_analyze = args.max_conversations

        # Config'i kaydet
        self.save_config(config)

        # Bridge oluştur ve başlat
        self.bridge = SmartContextBridge(config)

        if args.daemon:
            # Background mode (gelecekte implement edilecek)
            print(f"{Fore.YELLOW}⚠️ Daemon mode henüz desteklenmemiyor{Style.RESET_ALL}")
            return False
        else:
            # Foreground mode
            return self.bridge.run_forever()

    def cmd_stop(self, args):
        """Smart Context Bridge'i durdurur"""
        print(f"{Fore.YELLOW}⏹️ Smart Context Bridge durduruluyor...{Style.RESET_ALL}")

        if self.bridge and self.bridge.is_running:
            self.bridge.stop_monitoring()
            print(f"{Fore.GREEN}✅ Smart Context Bridge durduruldu{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.YELLOW}⚠️ Smart Context Bridge zaten çalışmıyor{Style.RESET_ALL}"
            )

    def cmd_status(self, args):
        """Smart Context Bridge durumunu gösterir"""
        print(f"{Fore.CYAN}📊 Smart Context Bridge Durumu{Style.RESET_ALL}")
        print("=" * 50)

        config = self.load_config()

        # Dizin durumları
        json_path = Path(config.json_chat_path)
        rules_path = Path(config.cursor_rules_path)
        auto_context_path = rules_path / config.auto_context_file

        print(f"{Fore.BLUE}📁 Paths:{Style.RESET_ALL}")
        print(f"  JSON Chat: {json_path.absolute()}")
        print(f"  Cursor Rules: {rules_path.absolute()}")
        print(f"  Auto Context: {auto_context_path.absolute()}")
        print()

        print(f"{Fore.BLUE}📊 Status:{Style.RESET_ALL}")
        print(f"  JSON Chat Directory: {'✅ Var' if json_path.exists() else '❌ Yok'}")
        print(
            f"  Cursor Rules Directory: {'✅ Var' if rules_path.exists() else '❌ Yok'}"
        )
        print(
            f"  Auto Context File: {'✅ Var' if auto_context_path.exists() else '❌ Yok'}"
        )
        print()

        # JSON dosyaları
        if json_path.exists():
            json_files = list(json_path.glob("**/*.json"))
            print(f"{Fore.BLUE}💬 JSON Chat Files:{Style.RESET_ALL}")
            print(f"  Toplam Dosya: {len(json_files)}")

            if json_files:
                latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
                latest_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
                print(f"  Son Güncelleme: {latest_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  Son Dosya: {latest_file.name}")
        else:
            print(f"{Fore.YELLOW}⚠️ JSON Chat dizini bulunamadı{Style.RESET_ALL}")

        print()

        # Config bilgileri
        print(f"{Fore.BLUE}⚙️ Configuration:{Style.RESET_ALL}")
        print(
            f"  Context Generation: {'✅ Aktif' if config.context_generation_enabled else '❌ Pasif'}"
        )
        print(f"  Min Relevance Score: {config.min_relevance_score}")
        print(f"  Max Conversations: {config.max_conversations_to_analyze}")
        print(f"  Update Interval: {config.update_interval_seconds}s")

    def cmd_analyze(self, args):
        """Mevcut JSON chat dosyalarını analiz eder"""
        print(f"{Fore.CYAN}🔍 JSON Chat analizi başlatılıyor...{Style.RESET_ALL}")

        config = self.load_config()
        bridge = SmartContextBridge(config)

        # Sadece initial analysis yap
        bridge._initial_context_analysis()

        # Sonuçları göster
        status = bridge.get_status()
        print()
        print(f"{Fore.GREEN}📊 Analiz Tamamlandı{Style.RESET_ALL}")
        print(f"  Toplam Context: {status['contexts_count']}")
        print(f"  Yüksek Relevance (>0.7): {status['high_relevance_count']}")
        print(f"  Auto Context Güncellendi: .cursor/rules/auto_context.md")

        if args.conversation:
            # Belirli bir conversation analiz et
            json_path = Path(config.json_chat_path) / f"{args.conversation}.json"
            if json_path.exists():
                context = bridge._analyze_json_file(str(json_path))
                if context:
                    self._display_context_details(context)
                else:
                    print(
                        f"{Fore.YELLOW}⚠️ Conversation analiz edilemedi{Style.RESET_ALL}"
                    )
            else:
                print(
                    f"{Fore.RED}❌ Conversation bulunamadı: {json_path}{Style.RESET_ALL}"
                )

    def cmd_config(self, args):
        """Konfigürasyon yönetimi"""
        config = self.load_config()

        if args.show:
            print(f"{Fore.CYAN}⚙️ Smart Context Bridge Configuration{Style.RESET_ALL}")
            print("=" * 50)
            print(f"JSON Chat Path: {config.json_chat_path}")
            print(f"Cursor Rules Path: {config.cursor_rules_path}")
            print(f"Auto Context File: {config.auto_context_file}")
            print(f"Context Generation: {config.context_generation_enabled}")
            print(f"Max Context Length: {config.max_context_length}")
            print(f"Min Relevance Score: {config.min_relevance_score}")
            print(f"Update Interval: {config.update_interval_seconds}s")
            print(f"Max Conversations: {config.max_conversations_to_analyze}")
            return

        # Config değişiklikleri
        changed = False

        if args.json_path:
            config.json_chat_path = args.json_path
            changed = True
            print(
                f"{Fore.GREEN}✅ JSON Chat path güncellendi: {args.json_path}{Style.RESET_ALL}"
            )

        if args.rules_path:
            config.cursor_rules_path = args.rules_path
            changed = True
            print(
                f"{Fore.GREEN}✅ Cursor Rules path güncellendi: {args.rules_path}{Style.RESET_ALL}"
            )

        if args.min_score is not None:
            config.min_relevance_score = args.min_score
            changed = True
            print(
                f"{Fore.GREEN}✅ Min relevance score güncellendi: {args.min_score}{Style.RESET_ALL}"
            )

        if args.max_conversations is not None:
            config.max_conversations_to_analyze = args.max_conversations
            changed = True
            print(
                f"{Fore.GREEN}✅ Max conversations güncellendi: {args.max_conversations}{Style.RESET_ALL}"
            )

        if args.enable_generation is not None:
            config.context_generation_enabled = args.enable_generation
            changed = True
            status = "aktif" if args.enable_generation else "pasif"
            print(f"{Fore.GREEN}✅ Context generation {status} edildi{Style.RESET_ALL}")

        if changed:
            self.save_config(config)
            print(f"{Fore.BLUE}💾 Konfigürasyon kaydedildi{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ Hiçbir değişiklik yapılmadı{Style.RESET_ALL}")

    def cmd_test(self, args):
        """Test ve demo fonksiyonları"""
        print(f"{Fore.CYAN}🧪 Smart Context Bridge Test{Style.RESET_ALL}")

        if args.create_sample:
            self._create_sample_conversation()
            print(f"{Fore.GREEN}✅ Örnek conversation oluşturuldu{Style.RESET_ALL}")

        if args.simulate_change:
            self._simulate_chat_change()
            print(f"{Fore.GREEN}✅ Chat değişikliği simule edildi{Style.RESET_ALL}")

    def _display_context_details(self, context: ChatContext):
        """Context detaylarını gösterir"""
        print(f"\n{Fore.CYAN}📋 Context Detayları{Style.RESET_ALL}")
        print("=" * 50)
        print(f"ID: {context.conversation_id}")
        print(f"Title: {context.title}")
        print(f"Project: {context.project_path}")
        print(f"Relevance Score: {context.relevance_score:.2f}")
        print(f"Tags: {', '.join(context.tags)}")
        print(f"Timestamp: {context.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        extracted = context.extracted_context

        if extracted.get("summary"):
            print(f"{Fore.BLUE}📝 Summary:{Style.RESET_ALL}")
            print(f"  {extracted['summary']}")
            print()

        if extracted.get("key_decisions"):
            print(f"{Fore.BLUE}🎯 Key Decisions:{Style.RESET_ALL}")
            for decision in extracted["key_decisions"]:
                print(f"  • {decision}")
            print()

        if extracted.get("technical_details"):
            print(f"{Fore.BLUE}🔧 Technical Details:{Style.RESET_ALL}")
            for tech in extracted["technical_details"]:
                print(f"  • {tech}")
            print()

        if extracted.get("next_steps"):
            print(f"{Fore.BLUE}▶️ Next Steps:{Style.RESET_ALL}")
            for step in extracted["next_steps"]:
                print(f"  • {step}")
            print()

    def _create_sample_conversation(self):
        """Test için örnek conversation oluşturur"""
        config = self.load_config()
        json_path = Path(config.json_chat_path)
        json_path.mkdir(parents=True, exist_ok=True)

        sample_conversation = {
            "id": f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "title": "Test Smart Context Bridge",
            "project_path": "/test/project",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "tags": ["test", "smart-context", "bridge"],
            "metadata": {
                "project_type": "test",
                "framework": "context7",
                "language": "turkish",
            },
            "messages": [
                {
                    "id": "msg-1",
                    "role": "user",
                    "content": "Smart Context Bridge sistemini test ediyorum. Context7 framework kullanacağız.",
                    "timestamp": datetime.now().isoformat(),
                },
                {
                    "id": "msg-2",
                    "role": "assistant",
                    "content": "Mükemmel! Smart Context Bridge testi başlatıldı. Sistem JSON chat değişikliklerini izleyecek ve otomatik context oluşturacak.",
                    "timestamp": datetime.now().isoformat(),
                },
                {
                    "id": "msg-3",
                    "role": "user",
                    "content": "Sonraki adım olarak .cursor/rules/auto_context.md dosyasının güncellenmesini bekliyorum.",
                    "timestamp": datetime.now().isoformat(),
                },
            ],
        }

        sample_file = (
            json_path
            / f"test_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(sample_file, "w", encoding="utf-8") as f:
            json.dump(sample_conversation, f, indent=2, ensure_ascii=False)

    def _simulate_chat_change(self):
        """Chat değişikliğini simule eder"""
        config = self.load_config()
        json_path = Path(config.json_chat_path)

        # Mevcut dosyaları bul
        json_files = list(json_path.glob("*.json"))
        if json_files:
            # İlk dosyayı güncelle
            target_file = json_files[0]

            with open(target_file, "r", encoding="utf-8") as f:
                conversation = json.load(f)

            # Yeni mesaj ekle
            new_message = {
                "id": f"msg-{len(conversation['messages']) + 1}",
                "role": "user",
                "content": f"Smart Context Bridge test mesajı - {datetime.now().strftime('%H:%M:%S')}",
                "timestamp": datetime.now().isoformat(),
            }

            conversation["messages"].append(new_message)
            conversation["updated_at"] = datetime.now().isoformat()

            # Dosyayı güncelle
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(conversation, f, indent=2, ensure_ascii=False)

            print(f"  Güncellenen dosya: {target_file.name}")
        else:
            print(
                f"{Fore.YELLOW}⚠️ Güncellenecek JSON dosyası bulunamadı{Style.RESET_ALL}"
            )


def main():
    """Ana CLI fonksiyonu"""
    parser = argparse.ArgumentParser(
        description="Smart Context Bridge CLI - Cross-Chat Memory for Cursor AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s start                 # Smart Context Bridge'i başlat
  %(prog)s status               # Sistem durumunu göster
  %(prog)s analyze              # Mevcut chat'leri analiz et
  %(prog)s analyze --conversation test-123  # Belirli conversation analiz et
  %(prog)s config --show        # Konfigürasyonu göster
  %(prog)s config --min-score 0.7  # Min relevance score ayarla
  %(prog)s test --create-sample # Test conversation oluştur
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Start command
    start_parser = subparsers.add_parser("start", help="Smart Context Bridge başlat")
    start_parser.add_argument("--json-path", help="JSON Chat dosyaları yolu")
    start_parser.add_argument("--rules-path", help="Cursor rules yolu")
    start_parser.add_argument("--min-score", type=float, help="Minimum relevance score")
    start_parser.add_argument(
        "--max-conversations", type=int, help="Maximum conversation sayısı"
    )
    start_parser.add_argument(
        "--daemon", action="store_true", help="Background modda çalıştır"
    )

    # Stop command
    stop_parser = subparsers.add_parser("stop", help="Smart Context Bridge durdur")

    # Status command
    status_parser = subparsers.add_parser("status", help="Sistem durumunu göster")

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="JSON Chat dosyalarını analiz et"
    )
    analyze_parser.add_argument(
        "--conversation", help="Belirli conversation ID analiz et"
    )

    # Config command
    config_parser = subparsers.add_parser("config", help="Konfigürasyon yönetimi")
    config_parser.add_argument(
        "--show", action="store_true", help="Mevcut konfigürasyonu göster"
    )
    config_parser.add_argument("--json-path", help="JSON Chat yolu ayarla")
    config_parser.add_argument("--rules-path", help="Cursor rules yolu ayarla")
    config_parser.add_argument(
        "--min-score", type=float, help="Min relevance score ayarla"
    )
    config_parser.add_argument(
        "--max-conversations", type=int, help="Max conversation sayısı ayarla"
    )
    config_parser.add_argument(
        "--enable-generation", type=bool, help="Context generation aktif/pasif"
    )

    # Test command
    test_parser = subparsers.add_parser("test", help="Test ve demo fonksiyonları")
    test_parser.add_argument(
        "--create-sample", action="store_true", help="Örnek conversation oluştur"
    )
    test_parser.add_argument(
        "--simulate-change", action="store_true", help="Chat değişikliğini simule et"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = ContextBridgeCLI()

    try:
        if args.command == "start":
            cli.cmd_start(args)
        elif args.command == "stop":
            cli.cmd_stop(args)
        elif args.command == "status":
            cli.cmd_status(args)
        elif args.command == "analyze":
            cli.cmd_analyze(args)
        elif args.command == "config":
            cli.cmd_config(args)
        elif args.command == "test":
            cli.cmd_test(args)
        else:
            print(f"{Fore.RED}❌ Bilinmeyen komut: {args.command}{Style.RESET_ALL}")
            parser.print_help()

    except KeyboardInterrupt:
        print(
            f"\n{Fore.YELLOW}🛑 İşlem kullanıcı tarafından iptal edildi{Style.RESET_ALL}"
        )
    except Exception as e:
        print(f"{Fore.RED}❌ Hata: {e}{Style.RESET_ALL}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
