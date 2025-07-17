#!/usr/bin/env python3
"""
Enhanced Cursor Database Reader - Gelişmiş Cursor SQLite veritabanı okuma modülü
vscode-cursorchat-downloader projesinden insights ile geliştirildi
"""

import sqlite3
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any


class EnhancedCursorDatabaseReader:
    """Gelişmiş Cursor SQLite veritabanını okuma sınıfı"""

    def __init__(self):
        self.cursor_db_paths = self._get_cursor_db_paths()
        self.workspace_mappings = {}

    def _get_cursor_db_paths(self) -> List[Path]:
        """Cursor veritabanı yollarını al - vscode-cursorchat-downloader insights"""
        possible_paths = []

        # macOS - vscode-cursorchat-downloader confirmed path
        mac_path = (
            Path.home()
            / "Library"
            / "Application Support"
            / "Cursor"
            / "User"
            / "workspaceStorage"
        )
        if mac_path.exists():
            possible_paths.append(mac_path)

        # Linux
        linux_path = Path.home() / ".config" / "Cursor" / "User" / "workspaceStorage"
        if linux_path.exists():
            possible_paths.append(linux_path)

        # Windows - enhanced detection
        if os.name == "nt":
            windows_paths = [
                Path(os.environ.get("APPDATA", ""))
                / "Cursor"
                / "User"
                / "workspaceStorage",
                Path(os.environ.get("LOCALAPPDATA", ""))
                / "Cursor"
                / "User"
                / "workspaceStorage",
            ]

            for win_path in windows_paths:
                if win_path.exists():
                    possible_paths.append(win_path)

        return possible_paths

    def find_workspace_databases(self) -> Dict[str, Dict[str, Any]]:
        """Tüm workspace veritabanlarını bul ve mapping'ini oluştur"""
        workspace_dbs = {}

        for cursor_path in self.cursor_db_paths:
            if not cursor_path.exists():
                continue

            # Her workspace storage klasörünü tara
            for workspace_dir in cursor_path.iterdir():
                if workspace_dir.is_dir():
                    # state.vscdb dosyasını ara
                    db_file = workspace_dir / "state.vscdb"
                    if db_file.exists():
                        # Workspace name ve path bilgisini al
                        workspace_info = self._get_workspace_info(db_file)
                        if workspace_info:
                            workspace_key = (
                                f"{workspace_info['name']}_{workspace_dir.name}"
                            )
                            workspace_dbs[workspace_key] = {
                                "db_path": db_file,
                                "workspace_dir": workspace_dir,
                                "info": workspace_info,
                            }

        return workspace_dbs

    def _get_workspace_info(self, db_file: Path) -> Optional[Dict]:
        """Workspace bilgilerini çıkar"""
        try:
            with sqlite3.connect(str(db_file)) as conn:
                cursor = conn.cursor()

                # Workspace folder path
                cursor.execute(
                    "SELECT value FROM ItemTable WHERE key = 'workbench.panel.explorer'"
                )
                explorer_result = cursor.fetchone()

                # Recently opened folders
                cursor.execute(
                    "SELECT value FROM ItemTable WHERE key LIKE '%recently.opened%'"
                )
                recent_result = cursor.fetchone()

                # Extract workspace name and path
                workspace_info = {
                    "name": "unknown",
                    "path": None,
                    "last_accessed": datetime.now().isoformat(),
                }

                if recent_result and recent_result[0]:
                    try:
                        recent_data = json.loads(recent_result[0])
                        if isinstance(recent_data, dict) and "entries" in recent_data:
                            entries = recent_data["entries"]
                            if entries and len(entries) > 0:
                                first_entry = entries[0]
                                if "folderUri" in first_entry:
                                    folder_uri = first_entry["folderUri"]
                                    if "path" in folder_uri:
                                        workspace_path = folder_uri["path"]
                                        workspace_info["path"] = workspace_path
                                        workspace_info["name"] = Path(
                                            workspace_path
                                        ).name
                    except (json.JSONDecodeError, KeyError, IndexError):
                        pass

                return workspace_info

        except Exception as e:
            print(f"Workspace info çıkarma hatası: {e}")
            return None

    def extract_complete_chat_history(self, db_file: Path) -> List[Dict]:
        """Tam sohbet geçmişini çıkar - vscode-cursorchat-downloader approach"""
        all_chats = []

        try:
            with sqlite3.connect(str(db_file)) as conn:
                cursor = conn.cursor()

                # Chat data için daha spesifik sorgular
                chat_queries = [
                    # AI Chat conversations
                    "SELECT key, value FROM ItemTable WHERE key LIKE '%aichat%'",
                    "SELECT key, value FROM ItemTable WHERE key LIKE '%aiService%'",
                    "SELECT key, value FROM ItemTable WHERE key LIKE '%chatdata%'",
                    "SELECT key, value FROM ItemTable WHERE key LIKE '%conversation%'",
                    # Code generations
                    "SELECT key, value FROM ItemTable WHERE key LIKE '%codeGeneration%'",
                    "SELECT key, value FROM ItemTable WHERE key LIKE '%inline%chat%'",
                ]

                for query in chat_queries:
                    cursor.execute(query)
                    results = cursor.fetchall()

                    for key, value in results:
                        if value:
                            try:
                                chat_entry = self._parse_enhanced_chat_data(key, value)
                                if chat_entry:
                                    all_chats.append(chat_entry)
                            except Exception as e:
                                print(f"Chat parsing hatası {key}: {e}")
                                continue

        except Exception as e:
            print(f"Veritabanı okuma hatası: {e}")

        # Timestamp'e göre sırala (en yeni ilk)
        return sorted(all_chats, key=lambda x: x.get("timestamp", ""), reverse=True)

    def _parse_enhanced_chat_data(
        self, key: str, value: str
    ) -> Optional[Dict[str, Any]]:
        """Enhanced chat data parsing"""
        try:
            data = json.loads(value)

            chat_entry: Dict[str, Any] = {
                "id": hashlib.md5(f"{key}{value}".encode()).hexdigest()[:8],
                "key_type": self._classify_chat_key(key),
                "timestamp": datetime.now().isoformat(),
                "raw_key": key,
            }

            # Farklı veri tiplerini handle et
            if isinstance(data, dict):
                # Standard chat format
                if "messages" in data and isinstance(data["messages"], list):
                    chat_entry["type"] = "conversation"
                    chat_entry["messages"] = data["messages"]
                    chat_entry["message_count"] = len(data["messages"])
                    chat_entry["summary"] = self._create_conversation_summary(
                        data["messages"]
                    )

                # Code generation format
                elif "prompt" in data or "request" in data:
                    prompt = data.get("prompt", data.get("request", ""))
                    response = data.get("response", data.get("completion", ""))

                    chat_entry["type"] = "code_generation"
                    chat_entry["prompt"] = prompt
                    chat_entry["response"] = response
                    chat_entry["summary"] = self._create_code_summary(prompt, response)

                # Inline chat format
                elif "content" in data:
                    chat_entry["type"] = "inline_chat"
                    chat_entry["content"] = data["content"]
                    chat_entry["summary"] = self._create_content_summary(
                        data["content"]
                    )

                # Generic format
                else:
                    chat_entry["type"] = "generic"
                    chat_entry["data"] = data
                    chat_entry["summary"] = self._create_generic_summary(data)

            elif isinstance(data, list):
                # Array of messages
                chat_entry["type"] = "message_array"
                chat_entry["messages"] = data
                chat_entry["message_count"] = len(data)
                chat_entry["summary"] = self._create_array_summary(data)

            else:
                # String or other format
                chat_entry["type"] = "raw_content"
                chat_entry["content"] = str(data)
                chat_entry["summary"] = (
                    str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                )

            return chat_entry

        except json.JSONDecodeError:
            # Raw string content
            return {
                "id": hashlib.md5(f"{key}{value}".encode()).hexdigest()[:8],
                "type": "raw_string",
                "key_type": self._classify_chat_key(key),
                "content": value,
                "summary": value[:200] + "..." if len(value) > 200 else value,
                "timestamp": datetime.now().isoformat(),
                "raw_key": key,
            }
        except Exception as e:
            print(f"Enhanced parsing hatası: {e}")
            return None

    def _classify_chat_key(self, key: str) -> str:
        """Chat key'ini classify et"""
        key_lower = key.lower()

        if "aichat" in key_lower:
            return "ai_chat"
        elif "codegeneration" in key_lower:
            return "code_generation"
        elif "inline" in key_lower and "chat" in key_lower:
            return "inline_chat"
        elif "conversation" in key_lower:
            return "conversation"
        elif "aiservice" in key_lower:
            return "ai_service"
        else:
            return "unknown"

    def _create_conversation_summary(self, messages: List[Dict]) -> str:
        """Conversation summary oluştur"""
        if not messages:
            return "Boş konuşma"

        summary_parts = []
        user_count = assistant_count = 0

        for message in messages[-5:]:  # Son 5 mesaj
            if isinstance(message, dict):
                role = message.get("role", message.get("sender", "unknown"))
                content = message.get("content", message.get("text", ""))

                if role in ["user", "human"]:
                    user_count += 1
                    if len(summary_parts) < 2:
                        summary_parts.append(f"👤: {content[:100]}...")
                elif role in ["assistant", "ai", "gpt"]:
                    assistant_count += 1
                    if len(summary_parts) < 2:
                        summary_parts.append(f"🤖: {content[:100]}...")

        summary = " | ".join(summary_parts)
        summary += f" [{user_count} kullanıcı, {assistant_count} AI mesajı]"

        return summary

    def _create_code_summary(self, prompt: str, response: str) -> str:
        """Code generation summary"""
        prompt_preview = prompt[:80] + "..." if len(prompt) > 80 else prompt
        response_preview = response[:80] + "..." if len(response) > 80 else response
        return f"💻 Kod: {prompt_preview} → {response_preview}"

    def _create_content_summary(self, content: str) -> str:
        """Content summary"""
        return f"📝 İçerik: {content[:150]}..." if len(content) > 150 else content

    def _create_generic_summary(self, data: Dict) -> str:
        """Generic data summary"""
        keys = list(data.keys())[:3]
        return f"📊 Veri: {', '.join(keys)}"

    def _create_array_summary(self, data: List) -> str:
        """Array summary"""
        return f"📋 Liste: {len(data)} öğe"

    def get_project_chat_history(
        self, project_path: Path, limit: int = 20
    ) -> List[Dict]:
        """Proje için chat geçmişini al"""
        workspace_dbs = self.find_workspace_databases()

        # Project path ile en yakın workspace'i bul
        project_str = str(project_path.resolve()).lower()
        best_match = None
        best_score = 0

        for workspace_key, workspace_data in workspace_dbs.items():
            workspace_info = workspace_data["info"]
            if workspace_info["path"]:
                workspace_path_str = workspace_info["path"].lower()

                # Simple path matching score
                if (
                    project_str in workspace_path_str
                    or workspace_path_str in project_str
                ):
                    score = len(
                        set(project_str.split("/")) & set(workspace_path_str.split("/"))
                    )
                    if score > best_score:
                        best_score = score
                        best_match = workspace_data

        if best_match:
            chats = self.extract_complete_chat_history(best_match["db_path"])
            return chats[:limit]

        return []

    def get_all_workspaces_summary(self) -> Dict[str, Dict]:
        """Tüm workspace'lerin özet bilgilerini al"""
        workspace_dbs = self.find_workspace_databases()
        summary = {}

        for workspace_key, workspace_data in workspace_dbs.items():
            workspace_info = workspace_data["info"]
            chats = self.extract_complete_chat_history(workspace_data["db_path"])

            summary[workspace_key] = {
                "info": workspace_info,
                "chat_count": len(chats),
                "last_activity": chats[0]["timestamp"] if chats else None,
                "db_path": str(workspace_data["db_path"]),
            }

        return summary

    def is_cursor_available(self) -> bool:
        """Cursor veritabanına erişim var mı?"""
        return len(self.cursor_db_paths) > 0


# Backward compatibility
CursorDatabaseReader = EnhancedCursorDatabaseReader
