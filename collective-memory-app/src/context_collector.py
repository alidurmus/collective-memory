#!/usr/bin/env python3
"""
Context Collector - Enhanced for Cursor Chat Integration
Cursor chat etkileşimi için optimize edilmiş bağlam toplama motoru
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ContextCollector:
    """Gelişmiş bağlam toplama motoru sınıfı"""

    def __init__(self):
        self.supported_doc_extensions = [".md", ".txt", ".rst", ".adoc"]
        self.supported_code_extensions = [
            ".py",
            ".js",
            ".ts",
            ".jsx",
            ".tsx",
            ".java",
            ".cpp",
            ".c",
            ".h",
        ]
        self.memory_db_path = "comprehensive_system.db"
        self.session_context = {
            "start_time": datetime.now(),
            "interactions": [],
            "context_changes": [],
            "memory_rules": [],
        }

    def initialize_memory_integration(self):
        """Hafıza sistemi entegrasyonu başlat"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()

            # Context tracking tablosu oluştur
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS context_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    context_type TEXT,
                    context_data TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Memory rules tablosu oluştur
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_type TEXT,
                    rule_content TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()
            conn.close()

            # Hafıza kurallarını yükle
            self._load_memory_rules()

        except Exception as e:
            print(f"Hafıza sistemi entegrasyonu hatası: {e}")

    def _load_memory_rules(self):
        """Hafıza kurallarını yükle"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT rule_type, rule_content FROM memory_rules WHERE is_active = TRUE"
            )
            rules = cursor.fetchall()

            self.session_context["memory_rules"] = [
                {"type": rule[0], "content": rule[1]} for rule in rules
            ]

            conn.close()
        except Exception as e:
            print(f"Hafıza kuralları yüklenemedi: {e}")

    def track_context_change(self, context_type: str, context_data: dict):
        """Context değişikliklerini takip et"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            conn = sqlite3.connect(self.memory_db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO context_tracking (session_id, context_type, context_data)
                VALUES (?, ?, ?)
            """,
                (session_id, context_type, json.dumps(context_data)),
            )

            conn.commit()
            conn.close()

            # Session context'i güncelle
            self.session_context["context_changes"].append(
                {
                    "type": context_type,
                    "data": context_data,
                    "timestamp": datetime.now(),
                }
            )

        except Exception as e:
            print(f"Context tracking hatası: {e}")

    def get_cursor_chat_context(self, project_path: Path) -> Dict[str, Any]:
        """Cursor chat etkileşimi için optimize edilmiş context toplama"""
        context = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(project_path),
            "project_name": project_path.name,
            "session_info": self.session_context,
            "cursor_optimized": True,
            "sources": {},
        }

        # Hafıza kurallarını ekle
        context["memory_rules"] = self.session_context["memory_rules"]

        # Aktif kuralları topla
        context["sources"]["rules"] = self.fetch_rules(project_path)

        # Sohbetleri topla (cursor chat focused)
        context["sources"]["chats"] = self.fetch_cursor_chats(project_path)

        # Dokümantasyonu topla
        context["sources"]["docs"] = self.fetch_docs(project_path)

        # Context değişikliğini takip et
        self.track_context_change("cursor_chat_context", context)

        return context

    def fetch_cursor_chats(self, project_path: Path) -> Dict[str, Any]:
        """Cursor chat için optimize edilmiş sohbet toplama"""
        chats_data = {
            "found": False,
            "chats": [],
            "source_files": [],
            "cursor_optimized": True,
        }

        # Cursor chat dosyalarını ara
        cursor_dirs = [".cursor", ".cursorchat", "cursor-chat"]

        for dir_name in cursor_dirs:
            cursor_path = project_path / dir_name
            if cursor_path.exists():
                try:
                    chat_files = list(cursor_path.glob("**/*.json"))
                    chat_files.extend(cursor_path.glob("**/*.md"))

                    for chat_file in chat_files:
                        try:
                            with open(chat_file, "r", encoding="utf-8") as f:
                                content = f.read()
                                chats_data["chats"].append(
                                    {
                                        "name": chat_file.name,
                                        "path": str(chat_file),
                                        "content": content,
                                        "last_modified": datetime.fromtimestamp(
                                            chat_file.stat().st_mtime
                                        ).isoformat(),
                                        "cursor_optimized": True,
                                    }
                                )
                                chats_data["source_files"].append(str(chat_file))
                        except Exception as e:
                            print(f"Chat dosyası okunamadı {chat_file}: {e}")

                    if chats_data["chats"]:
                        chats_data["found"] = True

                except Exception as e:
                    print(f"Cursor chat dizini okunamadı {cursor_path}: {e}")

        return chats_data

    def get_real_time_context(self) -> Dict[str, Any]:
        """Real-time context bilgilerini getir"""
        uptime = datetime.now() - self.session_context["start_time"]

        return {
            "session_uptime": str(uptime),
            "interactions_count": len(self.session_context["interactions"]),
            "context_changes_count": len(self.session_context["context_changes"]),
            "memory_rules_count": len(self.session_context["memory_rules"]),
            "cursor_optimized": True,
            "last_update": datetime.now().isoformat(),
        }

    def add_interaction(self, interaction_type: str, interaction_data: dict):
        """Etkileşim ekle"""
        self.session_context["interactions"].append(
            {
                "type": interaction_type,
                "data": interaction_data,
                "timestamp": datetime.now(),
            }
        )

    def get_context_for_console(self) -> Dict[str, Any]:
        """Console için context bilgilerini getir"""
        return {
            "session_info": self.get_real_time_context(),
            "memory_rules": self.session_context["memory_rules"],
            "recent_interactions": self.session_context["interactions"][-5:],
            "recent_changes": self.session_context["context_changes"][-5:],
        }

    def fetch_rules(self, project_path: Path) -> Dict[str, Any]:
        """Proje kurallarını topla (.cursor/rules)"""
        rules_data = {"found": False, "rules": [], "source_files": []}

        # .cursor/rules klasörünü kontrol et
        cursor_rules_path = project_path / ".cursor" / "rules"
        if cursor_rules_path.exists() and cursor_rules_path.is_dir():
            rules_data["found"] = True
            rules_data["rules"] = self._read_rules_directory(cursor_rules_path)
            rules_data["source_files"].append(str(cursor_rules_path))

        # .cursorrules dosyasını kontrol et (eski format)
        cursorrules_file = project_path / ".cursorrules"
        if cursorrules_file.exists():
            try:
                with open(cursorrules_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        rules_data["found"] = True
                        rules_data["rules"].append(
                            {
                                "type": "legacy_cursorrules",
                                "content": content,
                                "source": str(cursorrules_file),
                            }
                        )
                        rules_data["source_files"].append(str(cursorrules_file))
            except Exception as e:
                print(f"Eski .cursorrules dosyası okunamadı: {e}")

        return rules_data

    def _read_rules_directory(self, rules_path: Path) -> List[Dict[str, Any]]:
        """Rules dizinini oku"""
        rules = []

        try:
            for rule_file in rules_path.rglob("*"):
                if rule_file.is_file() and rule_file.suffix in [".md", ".txt", ".rule"]:
                    try:
                        with open(rule_file, "r", encoding="utf-8") as f:
                            content = f.read().strip()
                            if content:
                                rules.append(
                                    {
                                        "type": "project_rule",
                                        "name": rule_file.name,
                                        "content": content,
                                        "source": str(rule_file),
                                    }
                                )
                    except Exception as e:
                        print(f"Kural dosyası okunamadı {rule_file}: {e}")

        except Exception as e:
            print(f"Rules dizini okunamadı: {e}")

        return rules

    def fetch_chats(self, project_path: Path, cursor_reader) -> Dict[str, Any]:
        """Geçmiş sohbetleri topla"""
        chats_data = {"found": False, "chats": [], "summary": ""}

        try:
            # Cursor veritabanından sohbetleri al
            recent_chats = cursor_reader.get_recent_chats(project_path, limit=5)

            if recent_chats:
                chats_data["found"] = True
                chats_data["chats"] = recent_chats
                chats_data["summary"] = self._create_chats_summary(recent_chats)

        except Exception as e:
            print(f"Sohbet geçmişi alınamadı: {e}")

        return chats_data

    def _create_chats_summary(self, chats: List[Dict]) -> str:
        """Sohbetlerin özetini oluştur"""
        if not chats:
            return ""

        summary_parts = []
        for chat in chats[:3]:  # Son 3 sohbet
            if "summary" in chat:
                summary_parts.append(chat["summary"])

        return " | ".join(summary_parts)

    def fetch_docs(self, project_path: Path) -> Dict[str, Any]:
        """Proje dokümanlarını topla"""
        docs_data = {"found": False, "docs": [], "summary": ""}

        try:
            # README ve önemli dosyaları bul
            important_files = self._find_important_files(project_path)

            # Dokümantasyon klasörlerini tara
            doc_dirs = self._find_doc_directories(project_path)

            all_docs = important_files + doc_dirs

            if all_docs:
                docs_data["found"] = True
                docs_data["docs"] = all_docs
                docs_data["summary"] = self._create_docs_summary(all_docs)

        except Exception as e:
            print(f"Dokümantasyon toplanamadı: {e}")

        return docs_data

    def _find_important_files(self, project_path: Path) -> List[Dict[str, Any]]:
        """Önemli dosyaları bul (README, CHANGELOG, vb.)"""
        important_files = []

        # Önemli dosya isimleri
        important_names = [
            "readme",
            "changelog",
            "license",
            "contributing",
            "code_of_conduct",
            "security",
            "todo",
            "notes",
        ]

        for file_path in project_path.iterdir():
            if file_path.is_file():
                name_lower = file_path.stem.lower()
                if name_lower in important_names:
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if content.strip():
                                important_files.append(
                                    {
                                        "type": "important_file",
                                        "name": file_path.name,
                                        "content": content[:2000],  # İlk 2000 karakter
                                        "source": str(file_path),
                                    }
                                )
                    except Exception as e:
                        print(f"Önemli dosya okunamadı {file_path}: {e}")

        return important_files

    def _find_doc_directories(self, project_path: Path) -> List[Dict[str, Any]]:
        """Dokümantasyon klasörlerini bul"""
        doc_files = []

        # Dokümantasyon klasörü isimleri
        doc_dir_names = ["docs", "documentation", "doc", "wiki", "guide"]

        for dir_name in doc_dir_names:
            doc_dir = project_path / dir_name
            if doc_dir.exists() and doc_dir.is_dir():
                # Klasördeki dosyaları tara
                for doc_file in doc_dir.rglob("*"):
                    if (
                        doc_file.is_file()
                        and doc_file.suffix in self.supported_doc_extensions
                    ):
                        try:
                            with open(doc_file, "r", encoding="utf-8") as f:
                                content = f.read()
                                if content.strip():
                                    doc_files.append(
                                        {
                                            "type": "documentation",
                                            "name": doc_file.name,
                                            "content": content[
                                                :1500
                                            ],  # İlk 1500 karakter
                                            "source": str(doc_file),
                                        }
                                    )
                        except Exception as e:
                            print(f"Dokümantasyon dosyası okunamadı {doc_file}: {e}")

        return doc_files[:10]  # En fazla 10 dosya

    def _create_docs_summary(self, docs: List[Dict[str, Any]]) -> str:
        """Dokümantasyon özetini oluştur"""
        if not docs:
            return ""

        summary_parts = []
        for doc in docs[:5]:  # İlk 5 doküman
            summary_parts.append(f"{doc['name']}: {doc['content'][:100]}...")

        return " | ".join(summary_parts)

    def collect_project_context(
        self, project_path: Path, cursor_reader
    ) -> Dict[str, Any]:
        """Tüm proje bağlamını topla"""
        context = {
            "timestamp": datetime.now().isoformat(),
            "project_path": str(project_path),
            "project_name": project_path.name,
            "sources": {},
        }

        # Kuralları topla
        context["sources"]["rules"] = self.fetch_rules(project_path)

        # Sohbetleri topla
        context["sources"]["chats"] = self.fetch_chats(project_path, cursor_reader)

        # Dokümantasyonu topla
        context["sources"]["docs"] = self.fetch_docs(project_path)

        return context

    def get_context_summary(self, context: Dict[str, Any]) -> str:
        """Bağlam özetini oluştur"""
        summary_parts = []

        if context["sources"]["rules"]["found"]:
            rules_count = len(context["sources"]["rules"]["rules"])
            summary_parts.append(f"Rules: {rules_count} kural")

        if context["sources"]["chats"]["found"]:
            chats_count = len(context["sources"]["chats"]["chats"])
            summary_parts.append(f"Chats: {chats_count} sohbet")

        if context["sources"]["docs"]["found"]:
            docs_count = len(context["sources"]["docs"]["docs"])
            summary_parts.append(f"Docs: {docs_count} doküman")

        return " | ".join(summary_parts) if summary_parts else "Bağlam bulunamadı"
