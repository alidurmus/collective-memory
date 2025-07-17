#!/usr/bin/env python3
"""
Smart Context Bridge - Phase 4 Implementation
Cursor AI cross-chat memory çözümü - JSON Chat monitoring ve otomatik context bridge
"""

import os
import json
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Style

# Initialize colorama
init()


@dataclass
class ChatContext:
    """Chat context veri yapısı"""

    conversation_id: str
    title: str
    project_path: str
    last_messages: List[Dict]
    extracted_context: Dict
    relevance_score: float
    timestamp: datetime
    tags: List[str] = field(default_factory=list)


@dataclass
class ContextBridgeConfig:
    """Smart Context Bridge konfigürasyonu"""

    json_chat_path: str = ".collective-memory/conversations"
    cursor_rules_path: str = ".cursor/rules"
    auto_context_file: str = "auto_context.md"
    context_generation_enabled: bool = True
    max_context_length: int = 8000
    min_relevance_score: float = 0.6
    update_interval_seconds: int = 5
    max_conversations_to_analyze: int = 10


class JSONChatMonitor(FileSystemEventHandler):
    """JSON Chat dosyalarını real-time izleyen monitor"""

    def __init__(self, callback: Callable[[str, str], None]):
        self.callback = callback
        self.debounce_time = 2  # 2 saniye debounce
        self.last_events = {}

    def on_modified(self, event):
        """JSON dosyası değiştiğinde tetiklenir"""
        if event.is_directory:
            return

        file_path = event.src_path
        if not file_path.endswith(".json"):
            return

        # Debounce - aynı dosyaya çok hızlı değişiklik yapılmasını önler
        current_time = time.time()
        if file_path in self.last_events:
            if current_time - self.last_events[file_path] < self.debounce_time:
                return

        self.last_events[file_path] = current_time

        print(
            f"{Fore.BLUE}📁 JSON Chat değişikliği tespit edildi: {file_path}{Style.RESET_ALL}"
        )

        # Callback'i çağır
        self.callback("modified", file_path)

    def on_created(self, event):
        """Yeni JSON dosyası oluşturulduğunda"""
        if not event.is_directory and event.src_path.endswith(".json"):
            print(
                f"{Fore.GREEN}📝 Yeni JSON Chat oluşturuldu: {event.src_path}{Style.RESET_ALL}"
            )
            self.callback("created", event.src_path)


class ContextExtractor:
    """Chat'lerden context çıkaran akıllı sistem"""

    def __init__(self):
        self.important_keywords = [
            "proje",
            "geliştirme",
            "modül",
            "özellik",
            "bug",
            "hata",
            "database",
            "model",
            "api",
            "frontend",
            "backend",
            "test",
            "kural",
            "standart",
            "framework",
            "context7",
            "django",
            "react",
        ]

    def extract_context_from_conversation(self, conversation: Dict) -> Dict:
        """Bir konuşmadan context çıkarır"""
        try:
            context = {
                "summary": "",
                "key_decisions": [],
                "technical_details": [],
                "next_steps": [],
                "project_info": {},
                "relevance_score": 0.0,
            }

            messages = conversation.get("messages", [])
            if not messages:
                return context

            # Son 5 mesajı analiz et
            recent_messages = messages[-5:]

            # Özet oluştur
            context["summary"] = self._create_summary(recent_messages)

            # Önemli kararları çıkar
            context["key_decisions"] = self._extract_decisions(recent_messages)

            # Teknik detayları çıkar
            context["technical_details"] = self._extract_technical_details(
                recent_messages
            )

            # Sonraki adımları belirle
            context["next_steps"] = self._extract_next_steps(recent_messages)

            # Proje bilgilerini çıkar
            context["project_info"] = self._extract_project_info(conversation)

            # Relevance score hesapla
            context["relevance_score"] = self._calculate_relevance_score(
                recent_messages
            )

            return context

        except Exception as e:
            print(f"{Fore.RED}❌ Context çıkarma hatası: {e}{Style.RESET_ALL}")
            return {}

    def _create_summary(self, messages: List[Dict]) -> str:
        """Mesajlardan özet oluşturur"""
        if not messages:
            return ""

        # Son user ve assistant mesajlarını al
        user_messages = [
            msg["content"] for msg in messages if msg.get("role") == "user"
        ]
        assistant_messages = [
            msg["content"] for msg in messages if msg.get("role") == "assistant"
        ]

        if user_messages:
            last_user_msg = user_messages[-1]
            # İlk 100 karakter özet olarak kullan
            summary = (
                last_user_msg[:100] + "..."
                if len(last_user_msg) > 100
                else last_user_msg
            )
            return summary

        return "Konuşma devam ediyor"

    def _extract_decisions(self, messages: List[Dict]) -> List[str]:
        """Önemli kararları çıkarır"""
        decisions = []
        decision_keywords = [
            "karar",
            "seçtik",
            "yapacağız",
            "kullanacağız",
            "implements",
            "decided",
        ]

        for msg in messages:
            content = msg.get("content", "").lower()
            for keyword in decision_keywords:
                if keyword in content:
                    # Kararın bulunduğu cümleyi al
                    sentences = content.split(".")
                    for sentence in sentences:
                        if keyword in sentence:
                            decisions.append(sentence.strip().capitalize())
                            break
                    break

        return decisions[:3]  # En fazla 3 karar

    def _extract_technical_details(self, messages: List[Dict]) -> List[str]:
        """Teknik detayları çıkarır"""
        technical = []
        tech_keywords = [
            "model",
            "class",
            "function",
            "api",
            "database",
            "framework",
            "library",
        ]

        for msg in messages:
            content = msg.get("content", "")

            # Kod blokları varsa onları çıkar
            if "```" in content:
                code_blocks = content.split("```")
                for i in range(1, len(code_blocks), 2):  # Odd indices are code blocks
                    if code_blocks[i].strip():
                        technical.append(f"Kod: {code_blocks[i].strip()[:50]}...")

            # Teknik kelimeler içeren cümleler
            for keyword in tech_keywords:
                if keyword.lower() in content.lower():
                    sentences = content.split(".")
                    for sentence in sentences:
                        if keyword.lower() in sentence.lower():
                            technical.append(sentence.strip())
                            break
                    break

        return technical[:5]  # En fazla 5 teknik detay

    def _extract_next_steps(self, messages: List[Dict]) -> List[str]:
        """Sonraki adımları belirler"""
        next_steps = []
        step_keywords = [
            "sonraki",
            "şimdi",
            "daha sonra",
            "next",
            "then",
            "yapacak",
            "geliştir",
        ]

        # Son mesajlarda gelecek zaman ifadeleri ara
        for msg in reversed(messages):  # Son mesajdan başla
            content = msg.get("content", "").lower()
            for keyword in step_keywords:
                if keyword in content:
                    sentences = content.split(".")
                    for sentence in sentences:
                        if keyword in sentence and len(sentence.strip()) > 10:
                            next_steps.append(sentence.strip().capitalize())

        return next_steps[:3]  # En fazla 3 adım

    def _extract_project_info(self, conversation: Dict) -> Dict:
        """Proje bilgilerini çıkarır"""
        project_info = {}

        # Metadata'dan bilgi al
        metadata = conversation.get("metadata", {})
        project_info.update(metadata)

        # Tags'lerden bilgi al
        tags = conversation.get("tags", [])
        if tags:
            project_info["tags"] = tags

        # Project path
        project_path = conversation.get("project_path", "")
        if project_path:
            project_info["project_path"] = project_path

        return project_info

    def _calculate_relevance_score(self, messages: List[Dict]) -> float:
        """Relevance score hesaplar"""
        if not messages:
            return 0.0

        score = 0.0
        total_content = ""

        # Tüm mesaj içeriğini birleştir
        for msg in messages:
            total_content += msg.get("content", "") + " "

        total_content = total_content.lower()

        # Önemli kelimeler varsa score artır
        for keyword in self.important_keywords:
            if keyword in total_content:
                score += 0.1

        # Kod blokları varsa score artır
        if "```" in total_content:
            score += 0.2

        # Uzun mesajlar daha önemli
        if len(total_content) > 500:
            score += 0.1

        # En son mesaj son 1 saat içindeyse score artır
        if messages:
            last_msg = messages[-1]
            timestamp_str = last_msg.get("timestamp", "")
            if timestamp_str:
                try:
                    last_time = datetime.fromisoformat(
                        timestamp_str.replace("Z", "+00:00")
                    )
                    if datetime.now().astimezone() - last_time < timedelta(hours=1):
                        score += 0.3
                except:
                    pass

        return min(score, 1.0)  # Max 1.0


class CursorRulesUpdater:
    """Cursor rules dosyalarını otomatik güncelleyen sistem"""

    def __init__(self, config: ContextBridgeConfig):
        self.config = config

    def update_auto_context(self, contexts: List[ChatContext]) -> bool:
        """Auto context dosyasını günceller"""
        try:
            # .cursor/rules klasörünü oluştur
            rules_dir = Path(self.config.cursor_rules_path)
            rules_dir.mkdir(parents=True, exist_ok=True)

            # Auto context dosyasının yolu
            auto_context_path = rules_dir / self.config.auto_context_file

            # Context'leri relevance score'a göre sırala
            sorted_contexts = sorted(
                contexts, key=lambda x: x.relevance_score, reverse=True
            )

            # Markdown content oluştur
            content = self._generate_context_markdown(sorted_contexts)

            # Dosyaya yaz
            with open(auto_context_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(
                f"{Fore.GREEN}✅ Auto context güncellendi: {auto_context_path}{Style.RESET_ALL}"
            )
            return True

        except Exception as e:
            print(f"{Fore.RED}❌ Auto context güncelleme hatası: {e}{Style.RESET_ALL}")
            return False

    def _generate_context_markdown(self, contexts: List[ChatContext]) -> str:
        """Context'lerden markdown oluşturur"""
        content = f"""# 🧠 Otomatik Context Bridge
**Oluşturulma:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Smart Context Bridge** tarafından otomatik oluşturuldu.

## 📋 Son Konuşmalardan Devam Eden Projeler

"""

        for i, context in enumerate(contexts[:5], 1):  # En önemli 5 context
            if context.relevance_score < 0.5:
                continue

            content += f"""### {i}. {context.title}
**Relevance Score:** {context.relevance_score:.1f}/1.0
**Proje:** {context.project_path}
**Son Güncelleme:** {context.timestamp.strftime('%Y-%m-%d %H:%M')}

**📋 Özet:** {context.extracted_context.get('summary', 'Bilgi yok')}

"""

            # Önemli kararlar
            decisions = context.extracted_context.get("key_decisions", [])
            if decisions:
                content += "**🎯 Önemli Kararlar:**\n"
                for decision in decisions:
                    content += f"- {decision}\n"
                content += "\n"

            # Teknik detaylar
            technical = context.extracted_context.get("technical_details", [])
            if technical:
                content += "**🔧 Teknik Detaylar:**\n"
                for tech in technical[:3]:
                    content += f"- {tech}\n"
                content += "\n"

            # Sonraki adımlar
            next_steps = context.extracted_context.get("next_steps", [])
            if next_steps:
                content += "**▶️ Sonraki Adımlar:**\n"
                for step in next_steps:
                    content += f"- {step}\n"
                content += "\n"

            # Proje bilgileri
            project_info = context.extracted_context.get("project_info", {})
            if project_info:
                content += "**📊 Proje Bilgileri:**\n"
                for key, value in project_info.items():
                    if key != "project_path":
                        content += f"- **{key.title()}:** {value}\n"
                content += "\n"

            content += "---\n\n"

        content += f"""## 🎯 Kullanım Talimatları

Bu context'i yeni chat'te kullanmak için:
1. Cursor AI'da yeni chat başlatın
2. **@Rules** yazarak bu context'i dahil edin
3. Projenize devam edin!

## ⚙️ Smart Context Bridge Bilgileri
- **Analiz Edilen Konuşma Sayısı:** {len(contexts)}
- **Yüksek Relevance (>0.7):** {len([c for c in contexts if c.relevance_score > 0.7])}
- **Orta Relevance (0.5-0.7):** {len([c for c in contexts if 0.5 <= c.relevance_score <= 0.7])}
- **Son Güncelleme:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

*Bu dosya Smart Context Bridge tarafından otomatik oluşturulur ve güncellenir.*
"""

        return content


class SmartContextBridge:
    """Smart Context Bridge ana sistem"""

    def __init__(self, config: Optional[ContextBridgeConfig] = None):
        self.config = config or ContextBridgeConfig()
        self.observer = None
        self.context_extractor = ContextExtractor()
        self.rules_updater = CursorRulesUpdater(self.config)
        self.is_running = False
        self.contexts_cache = []

        # Logging setup
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

    def start_monitoring(self) -> bool:
        """Smart Context Bridge monitoring'i başlatır"""
        try:
            # JSON chat path kontrolü
            json_chat_path = Path(self.config.json_chat_path)
            if not json_chat_path.exists():
                json_chat_path.mkdir(parents=True, exist_ok=True)
                print(
                    f"{Fore.YELLOW}📁 JSON Chat dizini oluşturuldu: {json_chat_path}{Style.RESET_ALL}"
                )

            print(
                f"{Fore.CYAN}🚀 Smart Context Bridge başlatılıyor...{Style.RESET_ALL}"
            )
            print(
                f"{Fore.BLUE}📁 İzlenen dizin: {json_chat_path.absolute()}{Style.RESET_ALL}"
            )

            # İlk context analizi yap
            self._initial_context_analysis()

            # File monitor başlat
            event_handler = JSONChatMonitor(self._on_json_change)
            self.observer = Observer()
            self.observer.schedule(event_handler, str(json_chat_path), recursive=True)
            self.observer.start()

            self.is_running = True
            print(f"{Fore.GREEN}✅ Smart Context Bridge aktif!{Style.RESET_ALL}")
            print(
                f"{Fore.YELLOW}💡 JSON Chat dosyalarınızda değişiklik yapın, otomatik context bridge oluşturulacak{Style.RESET_ALL}"
            )

            return True

        except Exception as e:
            print(
                f"{Fore.RED}❌ Smart Context Bridge başlatma hatası: {e}{Style.RESET_ALL}"
            )
            return False

    def stop_monitoring(self):
        """Monitoring'i durdurur"""
        if self.observer and self.is_running:
            self.observer.stop()
            self.observer.join()
            self.is_running = False
            print(f"{Fore.YELLOW}⏹️ Smart Context Bridge durduruldu{Style.RESET_ALL}")

    def _initial_context_analysis(self):
        """İlk başlangıçta mevcut JSON chat dosyalarını analiz eder"""
        print(
            f"{Fore.CYAN}🔍 Mevcut JSON Chat dosyaları analiz ediliyor...{Style.RESET_ALL}"
        )

        json_chat_path = Path(self.config.json_chat_path)
        json_files = list(json_chat_path.glob("**/*.json"))

        if not json_files:
            print(
                f"{Fore.YELLOW}📝 Henüz JSON Chat dosyası bulunamadı{Style.RESET_ALL}"
            )
            return

        contexts = []
        for json_file in json_files:
            context = self._analyze_json_file(str(json_file))
            if context:
                contexts.append(context)

        if contexts:
            self.contexts_cache = contexts
            self.rules_updater.update_auto_context(contexts)
            print(
                f"{Fore.GREEN}📊 {len(contexts)} konuşma analiz edildi{Style.RESET_ALL}"
            )
        else:
            print(
                f"{Fore.YELLOW}⚠️ Analiz edilebilir konuşma bulunamadı{Style.RESET_ALL}"
            )

    def _on_json_change(self, event_type: str, file_path: str):
        """JSON dosyası değiştiğinde tetiklenen callback"""
        print(
            f"{Fore.BLUE}🔄 JSON Chat değişikliği işleniyor: {event_type} - {file_path}{Style.RESET_ALL}"
        )

        # Dosyayı analiz et
        context = self._analyze_json_file(file_path)
        if context:
            # Cache'i güncelle
            self._update_contexts_cache(context)

            # Auto context'i güncelle
            if self.config.context_generation_enabled:
                self.rules_updater.update_auto_context(self.contexts_cache)
                print(f"{Fore.GREEN}🧠 Context bridge güncellendi!{Style.RESET_ALL}")

    def _analyze_json_file(self, file_path: str) -> Optional[ChatContext]:
        """Bir JSON dosyasını analiz eder"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                conversation = json.load(f)

            if not isinstance(conversation, dict):
                return None

            # Context çıkar
            extracted_context = (
                self.context_extractor.extract_context_from_conversation(conversation)
            )

            if extracted_context["relevance_score"] < self.config.min_relevance_score:
                return None

            # ChatContext oluştur
            context = ChatContext(
                conversation_id=conversation.get("id", ""),
                title=conversation.get("title", "İsimsiz Konuşma"),
                project_path=conversation.get("project_path", ""),
                last_messages=conversation.get("messages", [])[-3:],  # Son 3 mesaj
                extracted_context=extracted_context,
                relevance_score=extracted_context["relevance_score"],
                timestamp=datetime.now(),
                tags=conversation.get("tags", []),
            )

            return context

        except Exception as e:
            print(
                f"{Fore.RED}❌ JSON analiz hatası ({file_path}): {e}{Style.RESET_ALL}"
            )
            return None

    def _update_contexts_cache(self, new_context: ChatContext):
        """Context cache'ini günceller"""
        # Aynı conversation_id varsa güncelle
        for i, context in enumerate(self.contexts_cache):
            if context.conversation_id == new_context.conversation_id:
                self.contexts_cache[i] = new_context
                return

        # Yoksa ekle
        self.contexts_cache.append(new_context)

        # Cache boyutunu sınırla
        if len(self.contexts_cache) > self.config.max_conversations_to_analyze:
            # En düşük relevance score'lu context'leri çıkar
            self.contexts_cache.sort(key=lambda x: x.relevance_score, reverse=True)
            self.contexts_cache = self.contexts_cache[
                : self.config.max_conversations_to_analyze
            ]

    def run_forever(self):
        """Sürekli çalışır (blocking)"""
        if not self.is_running:
            if not self.start_monitoring():
                return

        try:
            print(
                f"{Fore.YELLOW}🎯 Smart Context Bridge çalışıyor... (Ctrl+C ile çıkış){Style.RESET_ALL}"
            )
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}🛑 Kullanıcı tarafından durduruldu{Style.RESET_ALL}")
        finally:
            self.stop_monitoring()

    def get_status(self) -> Dict:
        """Smart Context Bridge durumunu döndürür"""
        return {
            "is_running": self.is_running,
            "monitored_path": self.config.json_chat_path,
            "contexts_count": len(self.contexts_cache),
            "high_relevance_count": len(
                [c for c in self.contexts_cache if c.relevance_score > 0.7]
            ),
            "last_update": datetime.now().isoformat(),
            "config": {
                "context_generation_enabled": self.config.context_generation_enabled,
                "min_relevance_score": self.config.min_relevance_score,
                "max_conversations": self.config.max_conversations_to_analyze,
            },
        }


def main():
    """Ana fonksiyon - test ve demo için"""
    print(f"{Fore.CYAN}🧠 Smart Context Bridge v1.0{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Cross-Chat Memory Solution for Cursor AI{Style.RESET_ALL}")
    print()

    # Konfigürasyon
    config = ContextBridgeConfig(
        json_chat_path=".collective-memory/conversations",
        cursor_rules_path=".cursor/rules",
        context_generation_enabled=True,
        min_relevance_score=0.5,
    )

    # Smart Context Bridge başlat
    bridge = SmartContextBridge(config)

    print(f"{Fore.GREEN}🚀 Smart Context Bridge Demo{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. JSON Chat dosyalarınızı düzenleyin{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Otomatik context generation izleyin{Style.RESET_ALL}")
    print(
        f"{Fore.YELLOW}3. .cursor/rules/auto_context.md dosyasını kontrol edin{Style.RESET_ALL}"
    )
    print()

    # Sürekli çalışır
    bridge.run_forever()


if __name__ == "__main__":
    main()
