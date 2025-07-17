#!/usr/bin/env python3
"""
Database Manager - Dosya metadata ve içerik saklama sistemi
SQLite veritabanı ile dosya bilgilerini yönetir
"""

import sqlite3
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from colorama import init, Fore, Style
import logging

# Colorama initialize
init()


class DatabaseManager:
    """Dosya metadata ve içerik veritabanı yöneticisi"""

    def __init__(self, db_path: str = "data/collective_memory.db"):
        self.db_path = Path(db_path).resolve()
        self.connection = None

        # Logging setup
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(__name__)

        # Stopwords for prompt similarity
        self.stopwords = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "as",
            "is",
            "was",
            "are",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "shall",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            # Turkish stop words
            "ve",
            "bir",
            "bu",
            "da",
            "de",
            "ile",
            "o",
            "için",
            "var",
            "olan",
            "den",
            "dan",
            "deki",
            "nin",
            "nın",
            "nun",
            "nün",
            "si",
            "sı",
            "su",
            "şu",
            "her",
            "hiç",
            "daha",
            "çok",
            "az",
            "en",
            "gibi",
            "kadar",
        }

        # Database schema
        self.schema = {
            "files": """
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    file_name TEXT NOT NULL,
                    file_extension TEXT NOT NULL,
                    directory_path TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    content_hash TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    modified_at TIMESTAMP NOT NULL,
                    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER DEFAULT 1
                )
            """,
            "file_contents": """
                CREATE TABLE IF NOT EXISTS file_contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER NOT NULL,
                    content_text TEXT NOT NULL,
                    content_preview TEXT,
                    line_count INTEGER NOT NULL,
                    word_count INTEGER NOT NULL,
                    char_count INTEGER NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE
                )
            """,
            "search_index": """
                CREATE TABLE IF NOT EXISTS search_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER NOT NULL,
                    keyword TEXT NOT NULL,
                    keyword_count INTEGER NOT NULL,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE
                )
            """,
            "file_changes": """
                CREATE TABLE IF NOT EXISTS file_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER NOT NULL,
                    change_type TEXT NOT NULL,
                    old_content_hash TEXT,
                    new_content_hash TEXT,
                    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    change_description TEXT,
                    FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE
                )
            """,
            "prompt_history": """
                CREATE TABLE IF NOT EXISTS prompt_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_text TEXT NOT NULL,
                    prompt_hash TEXT UNIQUE NOT NULL,
                    search_type TEXT DEFAULT 'basic',
                    results_count INTEGER DEFAULT 0,
                    response_time_ms INTEGER DEFAULT 0,
                    context_preserved TEXT,
                    user_session TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "prompt_relationships": """
                CREATE TABLE IF NOT EXISTS prompt_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id_1 INTEGER NOT NULL,
                    prompt_id_2 INTEGER NOT NULL,
                    similarity_score REAL NOT NULL,
                    relationship_type TEXT DEFAULT 'semantic',
                    context_overlap REAL DEFAULT 0.0,
                    time_distance_hours REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (prompt_id_1) REFERENCES prompt_history (id) ON DELETE CASCADE,
                    FOREIGN KEY (prompt_id_2) REFERENCES prompt_history (id) ON DELETE CASCADE,
                    UNIQUE(prompt_id_1, prompt_id_2)
                )
            """,
            "prompt_context": """
                CREATE TABLE IF NOT EXISTS prompt_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_id INTEGER NOT NULL,
                    context_key TEXT NOT NULL,
                    context_value TEXT NOT NULL,
                    context_weight REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (prompt_id) REFERENCES prompt_history (id) ON DELETE CASCADE
                )
            """,
        }

    def connect(self) -> bool:
        """Veritabanına bağlanır"""
        try:
            # Veritabanı dizinini oluştur
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row  # Dict-like access

            print(
                f"{Fore.GREEN}✅ Database connected: {Fore.YELLOW}{self.db_path}{Style.RESET_ALL}"
            )
            return True

        except sqlite3.Error as e:
            print(f"{Fore.RED}❌ Database connection failed: {e}{Style.RESET_ALL}")
            return False

    def disconnect(self):
        """Veritabanı bağlantısını kapatır"""
        if self.connection:
            self.connection.close()
            self.connection = None
            print(f"{Fore.YELLOW}📴 Database disconnected{Style.RESET_ALL}")

    def initialize_database(self) -> bool:
        """Veritabanı tablolarını oluşturur"""
        if not self.connection:
            if not self.connect():
                return False

        try:
            cursor = self.connection.cursor()

            # Tabloları oluştur
            for table_name, schema in self.schema.items():
                cursor.execute(schema)
                print(
                    f"{Fore.CYAN}📋 Table created/verified: {table_name}{Style.RESET_ALL}"
                )

            # İndeksleri oluştur
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_files_path ON files(file_path)",
                "CREATE INDEX IF NOT EXISTS idx_files_modified ON files(modified_at)",
                "CREATE INDEX IF NOT EXISTS idx_files_extension ON files(file_extension)",
                "CREATE INDEX IF NOT EXISTS idx_search_keyword ON search_index(keyword)",
                "CREATE INDEX IF NOT EXISTS idx_changes_timestamp ON file_changes(change_timestamp)",
            ]

            for index in indexes:
                cursor.execute(index)

            self.connection.commit()
            print(f"{Fore.GREEN}✅ Database initialized successfully{Style.RESET_ALL}")
            return True

        except sqlite3.Error as e:
            print(f"{Fore.RED}❌ Database initialization failed: {e}{Style.RESET_ALL}")
            return False

    def calculate_file_hash(self, file_path: str) -> str:
        """Dosya hash'ini hesaplar"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.logger.error(f"Hash calculation failed for {file_path}: {e}")
            return ""

    def add_or_update_file(self, file_path: str, content: str = None) -> Optional[int]:
        """Dosya bilgisini ekler veya günceller"""
        if not self.connection:
            return None

        try:
            path = Path(file_path)
            if not path.exists():
                return None

            # Dosya bilgilerini topla
            file_info = {
                "file_path": str(path.resolve()),
                "file_name": path.name,
                "file_extension": path.suffix.lower(),
                "directory_path": str(path.parent),
                "file_size": path.stat().st_size,
                "content_hash": self.calculate_file_hash(file_path),
                "created_at": datetime.fromtimestamp(path.stat().st_ctime),
                "modified_at": datetime.fromtimestamp(path.stat().st_mtime),
            }

            # İçeriği oku
            if content is None:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    self.logger.error(f"Content reading failed for {file_path}: {e}")
                    content = ""

            cursor = self.connection.cursor()

            # Dosya zaten var mı kontrol et
            cursor.execute(
                "SELECT id, content_hash FROM files WHERE file_path = ?",
                (file_info["file_path"],),
            )
            existing_file = cursor.fetchone()

            if existing_file:
                # Dosya var - güncelle
                file_id = existing_file["id"]
                old_hash = existing_file["content_hash"]

                if old_hash != file_info["content_hash"]:
                    # İçerik değişmiş - güncelle
                    cursor.execute(
                        """
                        UPDATE files SET
                            file_name = ?, file_extension = ?, directory_path = ?,
                            file_size = ?, content_hash = ?, modified_at = ?,
                            indexed_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """,
                        (
                            file_info["file_name"],
                            file_info["file_extension"],
                            file_info["directory_path"],
                            file_info["file_size"],
                            file_info["content_hash"],
                            file_info["modified_at"],
                            file_id,
                        ),
                    )

                    # İçeriği güncelle
                    self._update_file_content(file_id, content)

                    # Değişiklik kaydı
                    self._record_file_change(
                        file_id, "modified", old_hash, file_info["content_hash"]
                    )

                    print(
                        f"{Fore.YELLOW}📝 File updated: {file_info['file_name']}{Style.RESET_ALL}"
                    )

                return file_id

            else:
                # Yeni dosya - ekle
                cursor.execute(
                    """
                    INSERT INTO files (
                        file_path, file_name, file_extension, directory_path,
                        file_size, content_hash, created_at, modified_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        file_info["file_path"],
                        file_info["file_name"],
                        file_info["file_extension"],
                        file_info["directory_path"],
                        file_info["file_size"],
                        file_info["content_hash"],
                        file_info["created_at"],
                        file_info["modified_at"],
                    ),
                )

                file_id = cursor.lastrowid

                # İçeriği ekle
                self._update_file_content(file_id, content)

                # Değişiklik kaydı
                self._record_file_change(
                    file_id, "created", None, file_info["content_hash"]
                )

                print(
                    f"{Fore.GREEN}✅ File added: {file_info['file_name']}{Style.RESET_ALL}"
                )

                self.connection.commit()
                return file_id

        except sqlite3.Error as e:
            self.logger.error(f"Database error in add_or_update_file: {e}")
            return None

    def _update_file_content(self, file_id: int, content: str):
        """Dosya içeriğini günceller"""
        cursor = self.connection.cursor()

        # İçerik istatistiklerini hesapla
        lines = content.count("\n") + 1 if content else 0
        words = len(content.split()) if content else 0
        chars = len(content) if content else 0
        preview = content[:500] + "..." if len(content) > 500 else content

        # Mevcut içeriği sil
        cursor.execute("DELETE FROM file_contents WHERE file_id = ?", (file_id,))

        # Yeni içeriği ekle
        cursor.execute(
            """
            INSERT INTO file_contents (
                file_id, content_text, content_preview,
                line_count, word_count, char_count
            ) VALUES (?, ?, ?, ?, ?, ?)
        """,
            (file_id, content, preview, lines, words, chars),
        )

    def _record_file_change(
        self, file_id: int, change_type: str, old_hash: str, new_hash: str
    ):
        """Dosya değişikliğini kaydeder"""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO file_changes (
                file_id, change_type, old_content_hash, new_content_hash
            ) VALUES (?, ?, ?, ?)
        """,
            (file_id, change_type, old_hash, new_hash),
        )

    def remove_file(self, file_path: str) -> bool:
        """Dosyayı veritabanından kaldırır"""
        if not self.connection:
            return False

        try:
            cursor = self.connection.cursor()

            # Dosya ID'sini bul
            cursor.execute("SELECT id FROM files WHERE file_path = ?", (file_path,))
            file_record = cursor.fetchone()

            if file_record:
                file_id = file_record["id"]

                # Dosyayı pasif yap (soft delete)
                cursor.execute(
                    "UPDATE files SET is_active = 0, indexed_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (file_id,),
                )

                # Değişiklik kaydı
                self._record_file_change(file_id, "deleted", None, None)

                self.connection.commit()
                print(f"{Fore.RED}🗑️  File removed: {file_path}{Style.RESET_ALL}")
                return True

            return False

        except sqlite3.Error as e:
            self.logger.error(f"Database error in remove_file: {e}")
            return False

    def search_files(self, query: str, limit: int = 50) -> List[Dict]:
        """Dosyalarda arama yapar"""
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()

            # Basit full-text search
            search_query = f"%{query}%"

            cursor.execute(
                """
                SELECT f.*, fc.content_preview, fc.line_count, fc.word_count
                FROM files f
                LEFT JOIN file_contents fc ON f.id = fc.file_id
                WHERE f.is_active = 1 AND (
                    f.file_name LIKE ? OR
                    f.file_path LIKE ? OR
                    fc.content_text LIKE ?
                )
                ORDER BY f.modified_at DESC
                LIMIT ?
            """,
                (search_query, search_query, search_query, limit),
            )

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "id": row["id"],
                        "file_path": row["file_path"],
                        "file_name": row["file_name"],
                        "file_extension": row["file_extension"],
                        "file_size": row["file_size"],
                        "modified_at": row["modified_at"],
                        "content_preview": row["content_preview"],
                        "line_count": row["line_count"],
                        "word_count": row["word_count"],
                    }
                )

            return results

        except sqlite3.Error as e:
            self.logger.error(f"Database error in search_files: {e}")
            return []

    def get_file_stats(self) -> Dict:
        """Dosya istatistiklerini döndürür"""
        if not self.connection:
            return {}

        try:
            cursor = self.connection.cursor()

            # Toplam dosya sayısı
            cursor.execute("SELECT COUNT(*) as total FROM files WHERE is_active = 1")
            total_files = cursor.fetchone()["total"]

            # Dosya türleri
            cursor.execute(
                """
                SELECT file_extension, COUNT(*) as count
                FROM files 
                WHERE is_active = 1 
                GROUP BY file_extension
                ORDER BY count DESC
            """
            )
            file_types = {
                row["file_extension"]: row["count"] for row in cursor.fetchall()
            }

            # Toplam boyut
            cursor.execute(
                "SELECT SUM(file_size) as total_size FROM files WHERE is_active = 1"
            )
            total_size = cursor.fetchone()["total_size"] or 0

            # Son değişiklik
            cursor.execute(
                "SELECT MAX(modified_at) as last_modified FROM files WHERE is_active = 1"
            )
            last_modified = cursor.fetchone()["last_modified"]

            return {
                "total_files": total_files,
                "file_types": file_types,
                "total_size": total_size,
                "last_modified": last_modified,
            }

        except sqlite3.Error as e:
            self.logger.error(f"Database error in get_file_stats: {e}")
            return {}

    def get_recent_changes(self, limit: int = 20) -> List[Dict]:
        """Son değişiklikleri döndürür"""
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                """
                SELECT fc.*, f.file_name, f.file_path
                FROM file_changes fc
                JOIN files f ON fc.file_id = f.id
                WHERE f.is_active = 1
                ORDER BY fc.change_timestamp DESC
                LIMIT ?
            """,
                (limit,),
            )

            changes = []
            for row in cursor.fetchall():
                changes.append(
                    {
                        "file_name": row["file_name"],
                        "file_path": row["file_path"],
                        "change_type": row["change_type"],
                        "change_timestamp": row["change_timestamp"],
                        "change_description": row["change_description"],
                    }
                )

            return changes

        except sqlite3.Error as e:
            self.logger.error(f"Database error in get_recent_changes: {e}")
            return []

    def get_total_file_count(self) -> int:
        """Toplam dosya sayısını döndürür"""
        if not self.connection:
            return 0

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM files WHERE is_active = 1")
            result = cursor.fetchone()
            return result["count"] if result else 0

        except sqlite3.Error as e:
            self.logger.error(f"Database error in get_total_file_count: {e}")
            return 0

    def add_prompt(
        self,
        prompt_text: str,
        search_type: str = "basic",
        results_count: int = 0,
        response_time_ms: int = 0,
        context_preserved: str = None,
        user_session: str = None,
    ) -> Optional[int]:
        """Yeni prompt ekler ve benzer promptlarla ilişkilendirir"""
        if not self.connection:
            return None

        try:
            import hashlib
            from datetime import datetime

            # Prompt hash hesapla
            prompt_hash = hashlib.md5(prompt_text.encode()).hexdigest()

            cursor = self.connection.cursor()

            # Mevcut prompt var mı kontrol et
            cursor.execute(
                "SELECT id, last_used_at FROM prompt_history WHERE prompt_hash = ?",
                (prompt_hash,),
            )
            existing = cursor.fetchone()

            if existing:
                # Varolan prompt'u güncelle
                cursor.execute(
                    """
                    UPDATE prompt_history 
                    SET last_used_at = CURRENT_TIMESTAMP, results_count = ?, response_time_ms = ?
                    WHERE id = ?
                """,
                    (results_count, response_time_ms, existing["id"]),
                )
                prompt_id = existing["id"]
            else:
                # Yeni prompt ekle
                cursor.execute(
                    """
                    INSERT INTO prompt_history 
                    (prompt_text, prompt_hash, search_type, results_count, response_time_ms, 
                     context_preserved, user_session)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        prompt_text,
                        prompt_hash,
                        search_type,
                        results_count,
                        response_time_ms,
                        context_preserved,
                        user_session,
                    ),
                )
                prompt_id = cursor.lastrowid

            self.connection.commit()

            # Benzer promptlarla ilişki kur (async task için)
            self._update_prompt_relationships(prompt_id, prompt_text)

            return prompt_id

        except sqlite3.Error as e:
            self.logger.error(f"Database error in add_prompt: {e}")
            return None

    def get_similar_prompts(
        self, prompt_text: str, limit: int = 5, similarity_threshold: float = 0.6
    ) -> List[Dict]:
        """Benzer promptları bulur"""
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()

            # Basit keyword matching ile başla
            words = prompt_text.lower().split()
            if len(words) < 2:
                return []

            # En sık kullanılan kelimeleri al
            important_words = [
                w for w in words if len(w) > 3 and w not in self.stopwords
            ][:5]

            if not important_words:
                return []

            # LIKE sorgusu oluştur
            like_conditions = []
            params = []
            for word in important_words:
                like_conditions.append("LOWER(prompt_text) LIKE ?")
                params.append(f"%{word}%")

            params.append(limit)

            query = f"""
                SELECT ph.*, 
                       COUNT(*) as keyword_matches,
                       (julianday('now') - julianday(ph.last_used_at)) * 24 as hours_ago
                FROM prompt_history ph
                WHERE ({' OR '.join(like_conditions)})
                AND prompt_text != ?
                GROUP BY ph.id
                ORDER BY keyword_matches DESC, hours_ago ASC
                LIMIT ?
            """
            params.insert(-1, prompt_text)  # Aynı prompt'u hariç tut

            cursor.execute(query, params)
            results = []

            for row in cursor.fetchall():
                similarity_score = min(
                    row["keyword_matches"] / len(important_words), 1.0
                )
                if similarity_score >= similarity_threshold:
                    results.append(
                        {
                            "id": row["id"],
                            "prompt_text": row["prompt_text"],
                            "similarity_score": similarity_score,
                            "last_used_at": row["last_used_at"],
                            "results_count": row["results_count"],
                            "search_type": row["search_type"],
                        }
                    )

            return results

        except sqlite3.Error as e:
            self.logger.error(f"Database error in get_similar_prompts: {e}")
            return []

    def get_related_prompts(self, prompt_id: int, limit: int = 5) -> List[Dict]:
        """Bir prompt'un ilişkili promptlarını getirir"""
        if not self.connection:
            return []

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                """
                SELECT ph.*, pr.similarity_score, pr.relationship_type, pr.context_overlap
                FROM prompt_relationships pr
                JOIN prompt_history ph ON (
                    (pr.prompt_id_1 = ? AND ph.id = pr.prompt_id_2) OR 
                    (pr.prompt_id_2 = ? AND ph.id = pr.prompt_id_1)
                )
                ORDER BY pr.similarity_score DESC, ph.last_used_at DESC
                LIMIT ?
            """,
                (prompt_id, prompt_id, limit),
            )

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "id": row["id"],
                        "prompt_text": row["prompt_text"],
                        "similarity_score": row["similarity_score"],
                        "relationship_type": row["relationship_type"],
                        "context_overlap": row["context_overlap"],
                        "last_used_at": row["last_used_at"],
                        "results_count": row["results_count"],
                    }
                )

            return results

        except sqlite3.Error as e:
            self.logger.error(f"Database error in get_related_prompts: {e}")
            return []

    def _update_prompt_relationships(self, prompt_id: int, prompt_text: str):
        """Prompt ile diğer promptlar arasındaki ilişkileri günceller"""
        try:
            similar_prompts = self.get_similar_prompts(
                prompt_text, limit=10, similarity_threshold=0.5
            )

            cursor = self.connection.cursor()

            for similar in similar_prompts:
                similarity_score = similar["similarity_score"]
                other_id = similar["id"]

                # Zaman mesafesi hesapla
                cursor.execute(
                    """
                    SELECT (julianday('now') - julianday(created_at)) * 24 as hours_ago
                    FROM prompt_history WHERE id = ?
                """,
                    (other_id,),
                )
                result = cursor.fetchone()
                time_distance = result["hours_ago"] if result else 0

                # İlişki kaydı ekle/güncelle
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO prompt_relationships
                    (prompt_id_1, prompt_id_2, similarity_score, relationship_type, 
                     time_distance_hours)
                    VALUES (?, ?, ?, 'semantic', ?)
                """,
                    (
                        min(prompt_id, other_id),
                        max(prompt_id, other_id),
                        similarity_score,
                        time_distance,
                    ),
                )

            self.connection.commit()

        except sqlite3.Error as e:
            self.logger.error(f"Database error in _update_prompt_relationships: {e}")

    def get_prompt_context_suggestions(
        self, current_prompt: str, limit: int = 3
    ) -> List[Dict]:
        """Mevcut prompt'a göre context önerileri getirir"""
        if not self.connection:
            return []

        try:
            # Benzer promptları bul
            similar_prompts = self.get_similar_prompts(current_prompt, limit=limit * 2)

            suggestions = []
            for prompt in similar_prompts:
                # Bu prompt'un context'ini al
                related = self.get_related_prompts(prompt["id"], limit=2)

                for rel in related:
                    if rel["similarity_score"] > 0.7:  # Yüksek benzerlik
                        suggestions.append(
                            {
                                "suggested_prompt": rel["prompt_text"],
                                "context_reason": f"'{prompt['prompt_text'][:50]}...' ile ilişkili",
                                "confidence": rel["similarity_score"],
                                "last_used": rel["last_used_at"],
                            }
                        )

            # Benzersiz önerileri döndür
            seen = set()
            unique_suggestions = []
            for sugg in sorted(
                suggestions, key=lambda x: x["confidence"], reverse=True
            ):
                if sugg["suggested_prompt"] not in seen:
                    seen.add(sugg["suggested_prompt"])
                    unique_suggestions.append(sugg)
                    if len(unique_suggestions) >= limit:
                        break

            return unique_suggestions

        except sqlite3.Error as e:
            self.logger.error(f"Database error in get_prompt_context_suggestions: {e}")
            return []


def main():
    """Ana fonksiyon - test için"""
    print(f"{Fore.CYAN}🚀 Database Manager Test Starting...{Style.RESET_ALL}")

    # Database manager oluştur
    db_manager = DatabaseManager("../data/test_collective_memory.db")

    # Bağlan ve initialize et
    if db_manager.connect():
        if db_manager.initialize_database():
            # Test dosyası ekle
            test_file = "../data/README.md"
            if Path(test_file).exists():
                file_id = db_manager.add_or_update_file(test_file)
                if file_id:
                    print(
                        f"{Fore.GREEN}✅ Test file added with ID: {file_id}{Style.RESET_ALL}"
                    )

                    # İstatistikleri göster
                    stats = db_manager.get_file_stats()
                    print(f"{Fore.YELLOW}📊 Database stats: {stats}{Style.RESET_ALL}")

                    # Arama testi
                    results = db_manager.search_files("README")
                    print(
                        f"{Fore.CYAN}🔍 Search results: {len(results)} files found{Style.RESET_ALL}"
                    )

        db_manager.disconnect()

    print(f"{Fore.GREEN}✅ Database Manager test completed{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
