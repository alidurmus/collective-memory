#!/usr/bin/env python3
"""
JSON Chat Manager - Konuşma JSON Depolama Sistemi
Collective Memory için JSON tabanlı konuşma saklama ve yönetim modülü
"""

import json
import os
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from collections import defaultdict
import uuid
import sqlite3
from colorama import Fore, Style, init

# Initialize colorama
init()


@dataclass
class ChatMessage:
    """Chat mesaj veri yapısı"""

    id: str
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class ChatConversation:
    """Chat konuşma veri yapısı"""

    id: str
    title: str
    project_path: str
    created_at: str
    updated_at: str
    messages: List[ChatMessage]
    tags: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at


class JSONChatManager:
    """JSON tabanlı konuşma yönetim sistemi"""

    def __init__(self, data_folder: str = None):
        self.data_folder = Path(data_folder) if data_folder else Path.cwd()
        self.collective_memory_dir = self.data_folder / ".collective-memory"
        self.conversations_dir = self.collective_memory_dir / "conversations"
        self.index_file = self.conversations_dir / "index.json"

        # Directory structure oluştur
        self._ensure_directories()

        # Index dosyası yükle
        self.conversation_index = self._load_index()

        print(
            f"{Fore.GREEN}📁 JSON Chat Manager initialized: {self.conversations_dir}{Style.RESET_ALL}"
        )

    def _ensure_directories(self):
        """Gerekli dizin yapısını oluştur"""
        directories = [
            self.conversations_dir,
            self.conversations_dir / "daily",
            self.conversations_dir / "projects",
            self.conversations_dir / "archived",
            self.conversations_dir / "exports",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def _load_index(self) -> Dict[str, Any]:
        """Konuşma index'ini yükle"""
        if self.index_file.exists():
            try:
                with open(self.index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(
                    f"{Fore.YELLOW}⚠️  Index dosyası yüklenemedi: {e}{Style.RESET_ALL}"
                )

        # Varsayılan index
        return {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "total_conversations": 0,
            "conversations": {},
            "projects": {},
            "tags": {},
            "daily_stats": {},
        }

    def _save_index(self):
        """Index dosyasını kaydet"""
        try:
            self.conversation_index["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()
            with open(self.index_file, "w", encoding="utf-8") as f:
                json.dump(self.conversation_index, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Fore.RED}❌ Index kaydedilemedi: {e}{Style.RESET_ALL}")

    def create_conversation(
        self, title: str, project_path: str = None, initial_message: str = None
    ) -> str:
        """Yeni konuşma oluştur"""
        conversation_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        # İlk mesajı ekle
        messages = []
        if initial_message:
            messages.append(
                ChatMessage(
                    id=str(uuid.uuid4()),
                    role="user",
                    content=initial_message,
                    timestamp=now,
                )
            )

        conversation = ChatConversation(
            id=conversation_id,
            title=title,
            project_path=project_path or str(self.data_folder),
            created_at=now,
            updated_at=now,
            messages=messages,
        )

        # Dosyaya kaydet
        self._save_conversation(conversation)

        # Index'i güncelle
        self._update_index_for_conversation(conversation)

        print(
            f"{Fore.GREEN}✅ Yeni konuşma oluşturuldu: {title} ({conversation_id}){Style.RESET_ALL}"
        )
        return conversation_id

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Dict[str, Any] = None,
    ) -> str:
        """Konuşmaya mesaj ekle"""
        conversation = self.load_conversation(conversation_id)
        if not conversation:
            raise ValueError(f"Konuşma bulunamadı: {conversation_id}")

        message_id = str(uuid.uuid4())
        message = ChatMessage(
            id=message_id,
            role=role,
            content=content,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )

        conversation.messages.append(message)
        conversation.updated_at = message.timestamp

        # Kaydet
        self._save_conversation(conversation)
        self._update_index_for_conversation(conversation)

        return message_id

    def load_conversation(self, conversation_id: str) -> Optional[ChatConversation]:
        """Konuşmayı yükle"""
        if conversation_id not in self.conversation_index["conversations"]:
            return None

        file_path = self._get_conversation_file_path(conversation_id)
        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Messages'i ChatMessage objelerine dönüştür
            messages = [ChatMessage(**msg) for msg in data["messages"]]
            data["messages"] = messages

            return ChatConversation(**data)
        except Exception as e:
            print(
                f"{Fore.RED}❌ Konuşma yüklenemedi {conversation_id}: {e}{Style.RESET_ALL}"
            )
            return None

    def search_conversations(
        self,
        query: str = None,
        project_path: str = None,
        tags: List[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Konuşmalarda arama yap"""
        results = []

        for conv_id, conv_info in self.conversation_index["conversations"].items():
            # Project filter
            if project_path and conv_info.get("project_path") != project_path:
                continue

            # Tags filter
            if tags and not any(tag in conv_info.get("tags", []) for tag in tags):
                continue

            # Text search
            if query:
                query_lower = query.lower()
                title_match = query_lower in conv_info.get("title", "").lower()

                # Load conversation for content search
                conversation = self.load_conversation(conv_id)
                content_match = False
                if conversation:
                    content_match = any(
                        query_lower in msg.content.lower()
                        for msg in conversation.messages
                    )

                if not (title_match or content_match):
                    continue

            results.append(
                {
                    "id": conv_id,
                    "title": conv_info.get("title"),
                    "project_path": conv_info.get("project_path"),
                    "created_at": conv_info.get("created_at"),
                    "updated_at": conv_info.get("updated_at"),
                    "message_count": conv_info.get("message_count", 0),
                    "tags": conv_info.get("tags", []),
                }
            )

        # Sort by updated_at (newest first)
        results.sort(key=lambda x: x["updated_at"], reverse=True)

        return results[:limit]

    def export_conversation(
        self, conversation_id: str, format: str = "json"
    ) -> Optional[str]:
        """Konuşmayı export et"""
        conversation = self.load_conversation(conversation_id)
        if not conversation:
            return None

        export_dir = self.conversations_dir / "exports"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "json":
            filename = f"conversation_{conversation_id}_{timestamp}.json"
            export_path = export_dir / filename

            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(asdict(conversation), f, indent=2, ensure_ascii=False)

            return str(export_path)

        elif format == "markdown":
            filename = f"conversation_{conversation_id}_{timestamp}.md"
            export_path = export_dir / filename

            md_content = self._conversation_to_markdown(conversation)
            with open(export_path, "w", encoding="utf-8") as f:
                f.write(md_content)

            return str(export_path)

        return None

    def get_conversation_stats(self) -> Dict[str, Any]:
        """Konuşma istatistikleri"""
        total_conversations = len(self.conversation_index["conversations"])
        total_messages = sum(
            conv.get("message_count", 0)
            for conv in self.conversation_index["conversations"].values()
        )

        # Project statistics
        project_stats = defaultdict(int)
        for conv in self.conversation_index["conversations"].values():
            project_path = conv.get("project_path", "unknown")
            project_name = (
                Path(project_path).name if project_path != "unknown" else "unknown"
            )
            project_stats[project_name] += 1

        # Tag statistics
        tag_stats = defaultdict(int)
        for conv in self.conversation_index["conversations"].values():
            for tag in conv.get("tags", []):
                tag_stats[tag] += 1

        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "projects": dict(project_stats),
            "tags": dict(tag_stats),
            "storage_size": self._calculate_storage_size(),
            "last_activity": self._get_last_activity(),
        }

    def import_from_cursor(self, cursor_reader) -> int:
        """Cursor chat'lerini import et"""
        imported_count = 0

        try:
            # Cursor workspace'lerini bul
            workspaces = cursor_reader.find_workspace_databases()

            for workspace_key, workspace_data in workspaces.items():
                workspace_info = workspace_data["info"]
                chats = cursor_reader.extract_complete_chat_history(
                    workspace_data["db_path"]
                )

                for chat in chats:
                    # Chat'i conversation'a dönüştür
                    conv_id = self._import_cursor_chat(chat, workspace_info)
                    if conv_id:
                        imported_count += 1

            print(
                f"{Fore.GREEN}✅ {imported_count} Cursor konuşması import edildi{Style.RESET_ALL}"
            )

        except Exception as e:
            print(f"{Fore.RED}❌ Cursor import hatası: {e}{Style.RESET_ALL}")

        return imported_count

    def _save_conversation(self, conversation: ChatConversation):
        """Konuşmayı dosyaya kaydet"""
        file_path = self._get_conversation_file_path(conversation.id)

        # Messages'i dict'e dönüştür
        conversation_dict = asdict(conversation)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(conversation_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Fore.RED}❌ Konuşma kaydedilemedi: {e}{Style.RESET_ALL}")

    def _get_conversation_file_path(self, conversation_id: str) -> Path:
        """Konuşma dosya yolunu al"""
        # Daily organization
        today = datetime.now().strftime("%Y-%m-%d")
        daily_dir = self.conversations_dir / "daily" / today
        daily_dir.mkdir(parents=True, exist_ok=True)

        return daily_dir / f"{conversation_id}.json"

    def _update_index_for_conversation(self, conversation: ChatConversation):
        """Index'i konuşma için güncelle"""
        self.conversation_index["conversations"][conversation.id] = {
            "title": conversation.title,
            "project_path": conversation.project_path,
            "created_at": conversation.created_at,
            "updated_at": conversation.updated_at,
            "message_count": len(conversation.messages),
            "tags": conversation.tags,
            "file_path": str(self._get_conversation_file_path(conversation.id)),
        }

        # Project index
        project_name = Path(conversation.project_path).name
        if project_name not in self.conversation_index["projects"]:
            self.conversation_index["projects"][project_name] = []

        if conversation.id not in self.conversation_index["projects"][project_name]:
            self.conversation_index["projects"][project_name].append(conversation.id)

        # Tag index
        for tag in conversation.tags:
            if tag not in self.conversation_index["tags"]:
                self.conversation_index["tags"][tag] = []
            if conversation.id not in self.conversation_index["tags"][tag]:
                self.conversation_index["tags"][tag].append(conversation.id)

        # Total count
        self.conversation_index["total_conversations"] = len(
            self.conversation_index["conversations"]
        )

        self._save_index()

    def _conversation_to_markdown(self, conversation: ChatConversation) -> str:
        """Konuşmayı Markdown'a dönüştür"""
        md_lines = [
            f"# {conversation.title}",
            "",
            f"**Project:** {conversation.project_path}",
            f"**Created:** {conversation.created_at}",
            f"**Updated:** {conversation.updated_at}",
            f"**Messages:** {len(conversation.messages)}",
            f"**Tags:** {', '.join(conversation.tags)}",
            "",
            "---",
            "",
        ]

        for msg in conversation.messages:
            role_emoji = {"user": "👤", "assistant": "🤖", "system": "⚙️"}.get(
                msg.role, "❓"
            )
            md_lines.extend(
                [
                    f"## {role_emoji} {msg.role.title()} - {msg.timestamp}",
                    "",
                    msg.content,
                    "",
                    "---",
                    "",
                ]
            )

        return "\n".join(md_lines)

    def _calculate_storage_size(self) -> str:
        """Storage boyutunu hesapla"""
        total_size = 0
        for root, dirs, files in os.walk(self.conversations_dir):
            for file in files:
                file_path = Path(root) / file
                total_size += file_path.stat().st_size

        # Human readable format
        for unit in ["B", "KB", "MB", "GB"]:
            if total_size < 1024:
                return f"{total_size:.1f} {unit}"
            total_size /= 1024
        return f"{total_size:.1f} TB"

    def _get_last_activity(self) -> Optional[str]:
        """Son aktivite tarihini al"""
        if not self.conversation_index["conversations"]:
            return None

        last_updated = max(
            conv.get("updated_at", "")
            for conv in self.conversation_index["conversations"].values()
        )
        return last_updated

    def _import_cursor_chat(
        self, chat_data: Dict[str, Any], workspace_info: Dict[str, Any]
    ) -> Optional[str]:
        """Cursor chat'ini import et"""
        try:
            # Conversation title oluştur
            title = f"Cursor Chat - {chat_data.get('type', 'unknown')}"
            if "summary" in chat_data:
                title = (
                    chat_data["summary"][:50] + "..."
                    if len(chat_data["summary"]) > 50
                    else chat_data["summary"]
                )

            # Conversation oluştur
            conversation_id = self.create_conversation(
                title=title, project_path=workspace_info.get("path", "unknown")
            )

            # Messages'i ekle
            if chat_data.get("type") == "conversation" and "messages" in chat_data:
                for msg in chat_data["messages"]:
                    self.add_message(
                        conversation_id=conversation_id,
                        role=msg.get("role", "user"),
                        content=msg.get("content", ""),
                        metadata={"imported_from": "cursor", "original_data": msg},
                    )
            elif chat_data.get("type") == "code_generation":
                # Prompt as user message
                if "prompt" in chat_data:
                    self.add_message(
                        conversation_id=conversation_id,
                        role="user",
                        content=chat_data["prompt"],
                        metadata={"imported_from": "cursor", "type": "code_generation"},
                    )

                # Response as assistant message
                if "response" in chat_data:
                    self.add_message(
                        conversation_id=conversation_id,
                        role="assistant",
                        content=chat_data["response"],
                        metadata={"imported_from": "cursor", "type": "code_generation"},
                    )

            return conversation_id

        except Exception as e:
            print(f"{Fore.YELLOW}⚠️  Cursor chat import hatası: {e}{Style.RESET_ALL}")
            return None
