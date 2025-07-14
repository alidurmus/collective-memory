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
    
    def __init__(self, db_path: str = "./data/collective_memory.db"):
        self.db_path = Path(db_path).resolve()
        self.connection = None
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Database schema
        self.schema = {
            'files': '''
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
            ''',
            'file_contents': '''
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
            ''',
            'search_index': '''
                CREATE TABLE IF NOT EXISTS search_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_id INTEGER NOT NULL,
                    keyword TEXT NOT NULL,
                    keyword_count INTEGER NOT NULL,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (file_id) REFERENCES files (id) ON DELETE CASCADE
                )
            ''',
            'file_changes': '''
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
            '''
        }
        
    def connect(self) -> bool:
        """Veritabanına bağlanır"""
        try:
            # Veritabanı dizinini oluştur
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row  # Dict-like access
            
            print(f"{Fore.GREEN}✅ Database connected: {Fore.YELLOW}{self.db_path}{Style.RESET_ALL}")
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
                print(f"{Fore.CYAN}📋 Table created/verified: {table_name}{Style.RESET_ALL}")
                
            # İndeksleri oluştur
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_files_path ON files(file_path)",
                "CREATE INDEX IF NOT EXISTS idx_files_modified ON files(modified_at)",
                "CREATE INDEX IF NOT EXISTS idx_files_extension ON files(file_extension)",
                "CREATE INDEX IF NOT EXISTS idx_search_keyword ON search_index(keyword)",
                "CREATE INDEX IF NOT EXISTS idx_changes_timestamp ON file_changes(change_timestamp)"
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
                'file_path': str(path.resolve()),
                'file_name': path.name,
                'file_extension': path.suffix.lower(),
                'directory_path': str(path.parent),
                'file_size': path.stat().st_size,
                'content_hash': self.calculate_file_hash(file_path),
                'created_at': datetime.fromtimestamp(path.stat().st_ctime),
                'modified_at': datetime.fromtimestamp(path.stat().st_mtime)
            }
            
            # İçeriği oku
            if content is None:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except Exception as e:
                    self.logger.error(f"Content reading failed for {file_path}: {e}")
                    content = ""
            
            cursor = self.connection.cursor()
            
            # Dosya zaten var mı kontrol et
            cursor.execute(
                "SELECT id, content_hash FROM files WHERE file_path = ?",
                (file_info['file_path'],)
            )
            existing_file = cursor.fetchone()
            
            if existing_file:
                # Dosya var - güncelle
                file_id = existing_file['id']
                old_hash = existing_file['content_hash']
                
                if old_hash != file_info['content_hash']:
                    # İçerik değişmiş - güncelle
                    cursor.execute('''
                        UPDATE files SET
                            file_name = ?, file_extension = ?, directory_path = ?,
                            file_size = ?, content_hash = ?, modified_at = ?,
                            indexed_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (
                        file_info['file_name'], file_info['file_extension'],
                        file_info['directory_path'], file_info['file_size'],
                        file_info['content_hash'], file_info['modified_at'],
                        file_id
                    ))
                    
                    # İçeriği güncelle
                    self._update_file_content(file_id, content)
                    
                    # Değişiklik kaydı
                    self._record_file_change(file_id, 'modified', old_hash, file_info['content_hash'])
                    
                    print(f"{Fore.YELLOW}📝 File updated: {file_info['file_name']}{Style.RESET_ALL}")
                    
                return file_id
                
            else:
                # Yeni dosya - ekle
                cursor.execute('''
                    INSERT INTO files (
                        file_path, file_name, file_extension, directory_path,
                        file_size, content_hash, created_at, modified_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    file_info['file_path'], file_info['file_name'],
                    file_info['file_extension'], file_info['directory_path'],
                    file_info['file_size'], file_info['content_hash'],
                    file_info['created_at'], file_info['modified_at']
                ))
                
                file_id = cursor.lastrowid
                
                # İçeriği ekle
                self._update_file_content(file_id, content)
                
                # Değişiklik kaydı
                self._record_file_change(file_id, 'created', None, file_info['content_hash'])
                
                print(f"{Fore.GREEN}✅ File added: {file_info['file_name']}{Style.RESET_ALL}")
                
                self.connection.commit()
                return file_id
                
        except sqlite3.Error as e:
            self.logger.error(f"Database error in add_or_update_file: {e}")
            return None
            
    def _update_file_content(self, file_id: int, content: str):
        """Dosya içeriğini günceller"""
        cursor = self.connection.cursor()
        
        # İçerik istatistiklerini hesapla
        lines = content.count('\n') + 1 if content else 0
        words = len(content.split()) if content else 0
        chars = len(content) if content else 0
        preview = content[:500] + "..." if len(content) > 500 else content
        
        # Mevcut içeriği sil
        cursor.execute("DELETE FROM file_contents WHERE file_id = ?", (file_id,))
        
        # Yeni içeriği ekle
        cursor.execute('''
            INSERT INTO file_contents (
                file_id, content_text, content_preview,
                line_count, word_count, char_count
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (file_id, content, preview, lines, words, chars))
        
    def _record_file_change(self, file_id: int, change_type: str, old_hash: str, new_hash: str):
        """Dosya değişikliğini kaydeder"""
        cursor = self.connection.cursor()
        
        cursor.execute('''
            INSERT INTO file_changes (
                file_id, change_type, old_content_hash, new_content_hash
            ) VALUES (?, ?, ?, ?)
        ''', (file_id, change_type, old_hash, new_hash))
        
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
                file_id = file_record['id']
                
                # Dosyayı pasif yap (soft delete)
                cursor.execute(
                    "UPDATE files SET is_active = 0, indexed_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (file_id,)
                )
                
                # Değişiklik kaydı
                self._record_file_change(file_id, 'deleted', None, None)
                
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
            
            cursor.execute('''
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
            ''', (search_query, search_query, search_query, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row['id'],
                    'file_path': row['file_path'],
                    'file_name': row['file_name'],
                    'file_extension': row['file_extension'],
                    'file_size': row['file_size'],
                    'modified_at': row['modified_at'],
                    'content_preview': row['content_preview'],
                    'line_count': row['line_count'],
                    'word_count': row['word_count']
                })
                
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
            total_files = cursor.fetchone()['total']
            
            # Dosya türleri
            cursor.execute('''
                SELECT file_extension, COUNT(*) as count
                FROM files 
                WHERE is_active = 1 
                GROUP BY file_extension
                ORDER BY count DESC
            ''')
            file_types = {row['file_extension']: row['count'] for row in cursor.fetchall()}
            
            # Toplam boyut
            cursor.execute("SELECT SUM(file_size) as total_size FROM files WHERE is_active = 1")
            total_size = cursor.fetchone()['total_size'] or 0
            
            # Son değişiklik
            cursor.execute("SELECT MAX(modified_at) as last_modified FROM files WHERE is_active = 1")
            last_modified = cursor.fetchone()['last_modified']
            
            return {
                'total_files': total_files,
                'file_types': file_types,
                'total_size': total_size,
                'last_modified': last_modified
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
            
            cursor.execute('''
                SELECT fc.*, f.file_name, f.file_path
                FROM file_changes fc
                JOIN files f ON fc.file_id = f.id
                WHERE f.is_active = 1
                ORDER BY fc.change_timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            changes = []
            for row in cursor.fetchall():
                changes.append({
                    'file_name': row['file_name'],
                    'file_path': row['file_path'],
                    'change_type': row['change_type'],
                    'change_timestamp': row['change_timestamp'],
                    'change_description': row['change_description']
                })
                
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
            cursor.execute('SELECT COUNT(*) as count FROM files WHERE is_active = 1')
            result = cursor.fetchone()
            return result['count'] if result else 0
            
        except sqlite3.Error as e:
            self.logger.error(f"Database error in get_total_file_count: {e}")
            return 0

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
                    print(f"{Fore.GREEN}✅ Test file added with ID: {file_id}{Style.RESET_ALL}")
                    
                    # İstatistikleri göster
                    stats = db_manager.get_file_stats()
                    print(f"{Fore.YELLOW}📊 Database stats: {stats}{Style.RESET_ALL}")
                    
                    # Arama testi
                    results = db_manager.search_files("README")
                    print(f"{Fore.CYAN}🔍 Search results: {len(results)} files found{Style.RESET_ALL}")
                    
        db_manager.disconnect()
        
    print(f"{Fore.GREEN}✅ Database Manager test completed{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 