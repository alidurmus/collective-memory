#!/usr/bin/env python3
"""
Collective Memory - Quick Console v2.0
Hafıza tabanlı görev ve hata yönetim sistemi
"""

import sys
import sqlite3
import datetime
import hashlib
import os
from pathlib import Path


class QuickConsole:
    def __init__(self):
        self.db_path = "comprehensive_system.db"
        self.session_start = datetime.datetime.now()
        self.command_history = []
        self.load_memory_rules()
        self.initialize_database()

    def load_memory_rules(self):
        """Hafıza kurallarını yükle"""
        self.memory_rules = {
            "auto_mark_completed": True,
            "track_completion_time": True,
            "save_solutions": True,
            "categorize_tasks": True,
            "priority_system": True,
            "document_tracking": True,  # Yeni: Doküman izleme
        }

    def initialize_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Processed documents tablosunu oluştur
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_documents (
                id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                processing_type TEXT NOT NULL,
                processing_date DATETIME NOT NULL,
                last_modified DATETIME NOT NULL,
                status TEXT DEFAULT 'processed',
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Index oluştur
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_processed_documents_hash 
            ON processed_documents(file_hash)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_processed_documents_path 
            ON processed_documents(file_path)
        """
        )

        conn.commit()
        conn.close()

    def calculate_file_hash(self, file_path):
        """Dosya hash'ini hesapla"""
        if not os.path.exists(file_path):
            return None

        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"❌ Hash hesaplama hatası: {e}")
            return None

    def is_document_processed(self, file_path):
        """Dokümanın daha önce işlenip işlenmediğini kontrol et"""
        if not os.path.exists(file_path):
            return False

        current_hash = self.calculate_file_hash(file_path)
        if not current_hash:
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT file_hash, last_modified FROM processed_documents 
            WHERE file_path = ? AND status = 'processed'
        """,
            (file_path,),
        )

        result = cursor.fetchone()
        conn.close()

        if not result:
            return False

        stored_hash, last_modified = result

        # Hash aynı mı kontrol et
        if stored_hash == current_hash:
            # Dosya değişiklik tarihi kontrol et
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            stored_mtime = datetime.datetime.fromisoformat(last_modified)

            if file_mtime <= stored_mtime:
                return True

        return False

    def mark_document_processed(self, file_path, processing_type="indexed", notes=None):
        """Dokümanı işlenmiş olarak işaretle"""
        if not os.path.exists(file_path):
            print(f"❌ Dosya bulunamadı: {file_path}")
            return False

        file_hash = self.calculate_file_hash(file_path)
        if not file_hash:
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        file_stats = os.stat(file_path)
        file_name = os.path.basename(file_path)
        file_size = file_stats.st_size
        last_modified = datetime.datetime.fromtimestamp(file_stats.st_mtime)
        current_time = datetime.datetime.now()

        doc_id = f"DOC_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{file_name}"

        # Mevcut kaydı kontrol et
        cursor.execute(
            """
            SELECT id FROM processed_documents WHERE file_path = ?
        """,
            (file_path,),
        )

        existing = cursor.fetchone()

        if existing:
            # Güncelle
            cursor.execute(
                """
                UPDATE processed_documents 
                SET file_hash = ?, file_size = ?, last_modified = ?, 
                    processing_type = ?, notes = ?, updated_at = ?
                WHERE file_path = ?
            """,
                (
                    file_hash,
                    file_size,
                    last_modified.isoformat(),
                    processing_type,
                    notes,
                    current_time.isoformat(),
                    file_path,
                ),
            )
        else:
            # Yeni kayıt
            cursor.execute(
                """
                INSERT INTO processed_documents 
                (id, file_path, file_name, file_hash, file_size, processing_type, 
                 processing_date, last_modified, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    doc_id,
                    file_path,
                    file_name,
                    file_hash,
                    file_size,
                    processing_type,
                    current_time.isoformat(),
                    last_modified.isoformat(),
                    notes,
                ),
            )

        conn.commit()
        conn.close()

        print(f"✅ Doküman işlendi: {file_name}")
        return True

    def list_processed_documents(self, limit=10):
        """İşlenmiş dokümanları listele"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT file_name, file_path, processing_type, processing_date, 
                   file_size, status
            FROM processed_documents 
            ORDER BY processing_date DESC 
            LIMIT ?
        """,
            (limit,),
        )

        documents = cursor.fetchall()
        conn.close()

        if not documents:
            print("📄 İşlenmiş doküman bulunamadı")
            return

        print(f"📄 İşlenmiş Dokümanlar (Son {limit}):")
        print("-" * 80)

        for doc in documents:
            file_name, file_path, proc_type, proc_date, file_size, status = doc

            # Dosya boyutunu formatla
            if file_size > 1024 * 1024:
                size_str = f"{file_size / (1024*1024):.1f} MB"
            elif file_size > 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size} B"

            print(f"📄 {file_name}")
            print(f"   📁 {file_path}")
            print(f"   🔄 {proc_type} | 📅 {proc_date} | 📊 {size_str}")
            print(f"   ✅ {status}")
            print()

    def get_document_stats(self):
        """Doküman istatistiklerini al"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_docs,
                COUNT(CASE WHEN status = 'processed' THEN 1 END) as processed_docs,
                SUM(file_size) as total_size,
                processing_type
            FROM processed_documents
            GROUP BY processing_type
        """
        )

        results = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) as total_docs, SUM(file_size) as total_size
            FROM processed_documents
        """
        )

        total_stats = cursor.fetchone()
        conn.close()

        return {
            "total_docs": total_stats[0] if total_stats else 0,
            "total_size": total_stats[1] if total_stats and total_stats[1] else 0,
            "by_type": results,
        }

    def check_unprocessed_documents(self, directory_path):
        """Dizindeki işlenmemiş dokümanları kontrol et"""
        if not os.path.exists(directory_path):
            print(f"❌ Dizin bulunamadı: {directory_path}")
            return

        unprocessed = []
        supported_extensions = [".md", ".txt", ".py", ".js", ".json", ".yaml", ".yml"]

        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()

                if file_ext in supported_extensions:
                    if not self.is_document_processed(file_path):
                        unprocessed.append(file_path)

        if unprocessed:
            print(f"📄 İşlenmemiş dokümanlar ({len(unprocessed)}):")
            for doc in unprocessed[:10]:  # İlk 10'u göster
                print(f"  📄 {doc}")

            if len(unprocessed) > 10:
                print(f"  ... ve {len(unprocessed) - 10} tane daha")
        else:
            print("✅ Tüm dokümanlar işlenmiş")

        return unprocessed

    def get_task_stats(self):
        """Görev istatistiklerini al"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
        completed_tasks = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'pending'")
        pending_tasks = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'in_progress'")
        in_progress_tasks = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM errors WHERE status = 'resolved'")
        resolved_errors = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM errors WHERE status = 'active'")
        active_errors = cursor.fetchone()[0]

        conn.close()

        return {
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "resolved_errors": resolved_errors,
            "active_errors": active_errors,
        }

    def complete_task(self, task_search, solution=None):
        """Görevi tamamla"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        current_time = datetime.datetime.now().isoformat()

        # ID ile ara
        cursor.execute(
            """
            UPDATE tasks 
            SET status = 'completed', 
                updated_at = ?
            WHERE id = ?
        """,
            (current_time, task_search),
        )

        # Eğer ID ile bulunamazsa başlıkta ara
        if cursor.rowcount == 0:
            cursor.execute(
                """
                UPDATE tasks 
                SET status = 'completed', 
                    updated_at = ?
                WHERE title LIKE ?
            """,
                (current_time, f"%{task_search}%"),
            )

        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Görev tamamlandı: {task_search}")
            if solution:
                print(f"💡 Çözüm: {solution}")
        else:
            print(f"❌ Görev bulunamadı: {task_search}")

        conn.close()

    def resolve_error(self, error_search, solution=None):
        """Hatayı çözümle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        current_time = datetime.datetime.now().isoformat()

        # ID ile ara
        cursor.execute(
            """
            UPDATE errors 
            SET status = 'resolved', 
                updated_at = ?,
                solution = ?
            WHERE id = ?
        """,
            (current_time, solution, error_search),
        )

        # Eğer ID ile bulunamazsa başlıkta ara
        if cursor.rowcount == 0:
            cursor.execute(
                """
                UPDATE errors 
                SET status = 'resolved', 
                    updated_at = ?,
                    solution = ?
                WHERE title LIKE ?
            """,
                (current_time, solution, f"%{error_search}%"),
            )

        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Hata çözüldü: {error_search}")
            if solution:
                print(f"💡 Çözüm: {solution}")
        else:
            print(f"❌ Hata bulunamadı: {error_search}")

        conn.close()

    def add_task(
        self, title, description=None, priority="medium", project="collective-memory"
    ):
        """Yeni görev ekle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        task_id = f"TASK_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        current_time = datetime.datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO tasks (id, title, description, priority, status, 
                              created_at, updated_at, project)
            VALUES (?, ?, ?, ?, 'pending', ?, ?, ?)
        """,
            (
                task_id,
                title,
                description,
                priority,
                current_time,
                current_time,
                project,
            ),
        )

        conn.commit()
        conn.close()

        print(f"📝 Yeni görev eklendi: {task_id}")
        print(f"📋 Başlık: {title}")

    def add_error(
        self, title, description=None, severity="medium", error_type="general"
    ):
        """Yeni hata ekle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        error_id = f"ERROR_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        current_time = datetime.datetime.now().isoformat()

        cursor.execute(
            """
            INSERT INTO errors (id, title, description, severity, error_type, 
                               status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
        """,
            (
                error_id,
                title,
                description,
                severity,
                error_type,
                current_time,
                current_time,
            ),
        )

        conn.commit()
        conn.close()

        print(f"🔴 Yeni hata eklendi: {error_id}")
        print(f"📋 Başlık: {title}")

    def list_tasks(self, status=None, limit=10):
        """Görevleri listele"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if status:
            cursor.execute(
                """
                SELECT id, title, status, priority, created_at, updated_at
                FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?
            """,
                (status, limit),
            )
        else:
            cursor.execute(
                """
                SELECT id, title, status, priority, created_at, updated_at
                FROM tasks ORDER BY created_at DESC LIMIT ?
            """,
                (limit,),
            )

        tasks = cursor.fetchall()
        conn.close()

        if not tasks:
            print("📋 Görev bulunamadı.")
            return

        print(f"📋 GÖREVLER ({len(tasks)}):")
        print("=" * 60)

        for task in tasks:
            task_id, title, status, priority, created_at, updated_at = task
            status_icon = (
                "✅"
                if status == "completed"
                else "⏳" if status == "in_progress" else "📋"
            )

            print(f"{status_icon} {task_id}")
            print(f"   📝 {title}")
            print(f"   📊 Status: {status} | Priority: {priority}")
            print(f"   📅 Created: {created_at}")
            if updated_at != created_at:
                print(f"   🔄 Updated: {updated_at}")
            print()

    def list_errors(self, status=None, limit=10):
        """Hataları listele"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if status:
            cursor.execute(
                """
                SELECT id, title, status, severity, created_at, updated_at, solution
                FROM errors WHERE status = ? ORDER BY created_at DESC LIMIT ?
            """,
                (status, limit),
            )
        else:
            cursor.execute(
                """
                SELECT id, title, status, severity, created_at, updated_at, solution
                FROM errors ORDER BY created_at DESC LIMIT ?
            """,
                (limit,),
            )

        errors = cursor.fetchall()
        conn.close()

        if not errors:
            print("🔴 Hata bulunamadı.")
            return

        print(f"🔴 HATALAR ({len(errors)}):")
        print("=" * 60)

        for error in errors:
            error_id, title, status, severity, created_at, updated_at, solution = error
            status_icon = "✅" if status == "resolved" else "🔴"

            print(f"{status_icon} {error_id}")
            print(f"   📝 {title}")
            print(f"   📊 Status: {status} | Severity: {severity}")
            print(f"   📅 Created: {created_at}")
            if updated_at != created_at:
                print(f"   🔄 Updated: {updated_at}")
            if solution:
                print(f"   💡 Çözüm: {solution}")
            print()

    def status(self):
        """Sistem durumunu göster"""
        stats = self.get_task_stats()
        uptime = datetime.datetime.now() - self.session_start

        print("📊 SİSTEM DURUMU")
        print("=" * 50)
        print(f"✅ Tamamlanan Görevler: {stats['completed_tasks']}")
        print(f"⏳ Bekleyen Görevler: {stats['pending_tasks']}")
        print(f"🔄 Devam Eden Görevler: {stats['in_progress_tasks']}")
        print(f"✅ Çözümlenen Hatalar: {stats['resolved_errors']}")
        print(f"🔴 Aktif Hatalar: {stats['active_errors']}")
        print(f"⏱️ Session Uptime: {uptime}")

    def bulk_complete(self, task_ids):
        """Birden fazla görevi toplu tamamla"""
        completed = []
        for task_id in task_ids:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            current_time = datetime.datetime.now().isoformat()

            cursor.execute(
                """
                UPDATE tasks 
                SET status = 'completed', 
                    updated_at = ?
                WHERE id = ? OR title LIKE ?
            """,
                (current_time, task_id, f"%{task_id}%"),
            )

            if cursor.rowcount > 0:
                completed.append(task_id)

            conn.commit()
            conn.close()

        if completed:
            print(f"✅ {len(completed)} görev tamamlandı:")
            for task_id in completed:
                print(f"  - {task_id}")
        else:
            print("❌ Hiç görev bulunamadı.")

    def bulk_resolve(self, error_ids):
        """Birden fazla hatayı toplu çözümle"""
        resolved = []
        for error_id in error_ids:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            current_time = datetime.datetime.now().isoformat()

            cursor.execute(
                """
                UPDATE errors 
                SET status = 'resolved', 
                    updated_at = ?
                WHERE id = ? OR title LIKE ?
            """,
                (current_time, error_id, f"%{error_id}%"),
            )

            if cursor.rowcount > 0:
                resolved.append(error_id)

            conn.commit()
            conn.close()

        if resolved:
            print(f"✅ {len(resolved)} hata çözüldü:")
            for error_id in resolved:
                print(f"  - {error_id}")
        else:
            print("❌ Hiç hata bulunamadı.")

    def help(self):
        """Yardım menüsü"""
        print("🔧 QUICK CONSOLE - KOMUTLAR")
        print("=" * 50)
        print("📋 GÖREV YÖNETİMİ:")
        print("  tasks                    - Görevleri listele")
        print("  tasks-pending            - Bekleyen görevleri listele")
        print("  tasks-completed          - Tamamlanan görevleri listele")
        print("  complete-task <id>       - Görevi tamamla")
        print("  add-task <title>         - Yeni görev ekle")
        print("  bulk-complete <id1,id2>  - Birden fazla görev tamamla")
        print("")
        print("🔴 HATA YÖNETİMİ:")
        print("  errors                   - Hataları listele")
        print("  errors-active            - Aktif hataları listele")
        print("  errors-resolved          - Çözümlenen hataları listele")
        print("  resolve-error <id>       - Hatayı çözümle")
        print("  add-error <title>        - Yeni hata ekle")
        print("  bulk-resolve <id1,id2>   - Birden fazla hata çözümle")
        print("")
        print("📊 SİSTEM:")
        print("  status                   - Sistem durumu")
        print("  memory                   - Hafıza bilgileri")
        print("  context                  - Context bilgileri")
        print("  help                     - Bu yardım menüsü")
        print("")
        print("📄 DOKÜMAN İZLEME:")
        print("  document-tracking        - Doküman izleme komutları")
        print("  check-unprocessed <dir>  - İşlenmemiş dokümanları kontrol et")
        print("  list-processed-docs <n>  - İşlenmiş dokümanları listele")
        print("  get-doc-stats            - Doküman istatistikleri")
        print("  mark-processed <file>    - Dokümanı işlenmiş olarak işaretle")
        print("  check-processed <file>   - Doküman işlenme durumunu kontrol et")

    def run_command(self, command, args=None):
        """Komut çalıştır"""
        self.command_history.append(command)

        if command == "help":
            self.help()
        elif command == "status":
            self.status()
        elif command == "tasks":
            self.list_tasks()
        elif command == "tasks-pending":
            self.list_tasks(status="pending")
        elif command == "tasks-completed":
            self.list_tasks(status="completed")
        elif command == "errors":
            self.list_errors()
        elif command == "errors-active":
            self.list_errors(status="active")
        elif command == "errors-resolved":
            self.list_errors(status="resolved")
        elif command.startswith("complete-task"):
            if len(command.split()) > 1:
                task_search = command.split()[1]
                solution = (
                    " ".join(command.split()[2:]) if len(command.split()) > 2 else None
                )
                self.complete_task(task_search, solution)
            else:
                print("❌ Kullanım: complete-task <task_id> [solution]")
        elif command.startswith("resolve-error"):
            if len(command.split()) > 1:
                error_search = command.split()[1]
                solution = (
                    " ".join(command.split()[2:]) if len(command.split()) > 2 else None
                )
                self.resolve_error(error_search, solution)
            else:
                print("❌ Kullanım: resolve-error <error_id> [solution]")
        elif command.startswith("add-task"):
            if len(command.split()) > 1:
                title = " ".join(command.split()[1:])
                self.add_task(title)
            else:
                print("❌ Kullanım: add-task <title>")
        elif command.startswith("add-error"):
            if len(command.split()) > 1:
                title = " ".join(command.split()[1:])
                self.add_error(title)
            else:
                print("❌ Kullanım: add-error <title>")
        elif command.startswith("bulk-complete"):
            if len(command.split()) > 1:
                task_ids = command.split()[1].split(",")
                self.bulk_complete(task_ids)
            else:
                print("❌ Kullanım: bulk-complete <id1,id2,id3>")
        elif command.startswith("bulk-resolve"):
            if len(command.split()) > 1:
                error_ids = command.split()[1].split(",")
                self.bulk_resolve(error_ids)
            else:
                print("❌ Kullanım: bulk-resolve <id1,id2,id3>")
        elif command == "memory":
            print("🧠 HAFIZA KURALLARI:")
            print("=" * 40)
            for key, value in self.memory_rules.items():
                print(f"  {key}: {value}")
        elif command == "context":
            print("🔍 CONTEXT BİLGİLERİ:")
            print("=" * 40)
            print(f"  Database: {self.db_path}")
            print(f"  Session Start: {self.session_start}")
            print(f"  Commands Run: {len(self.command_history)}")
        elif command == "document-tracking":
            print("📄 DOKÜMAN İZLEME:")
            print("=" * 40)
            print("  1. İşlenmemiş Dokümanları Kontrol Et:")
            print("  check-unprocessed <dizin_yolu>")
            print("  2. İşlenmiş Dokümanları Listele:")
            print("  list-processed-docs <limit>")
            print("  3. Doküman İşleme Durumunu Görüntüle:")
            print("  get-doc-stats")
            print("  4. Dokümanı İşlenmiş Olarak İşaretle:")
            print("  mark-processed <dosya_yolu> [işlem_türü]")
            print("  5. Doküman İşleme Durumunu Kontrol Et:")
            print("  check-processed <dosya_yolu>")
        elif command.startswith("check-unprocessed"):
            if len(command.split()) > 1:
                directory_path = " ".join(command.split()[1:])
                self.check_unprocessed_documents(directory_path)
            else:
                print("❌ Kullanım: check-unprocessed <dizin_yolu>")
        elif command.startswith("list-processed-docs"):
            limit = 10
            if len(command.split()) > 1:
                try:
                    limit = int(command.split()[1])
                except ValueError:
                    print("❌ Limit sayı olmalı")
                    return
            self.list_processed_documents(limit)
        elif command == "get-doc-stats":
            stats = self.get_document_stats()
            print("📊 DOKÜMAN İSTATİSTİKLERİ:")
            print("=" * 40)
            print(f"  📄 Toplam Doküman: {stats['total_docs']}")

            if stats["total_size"] > 1024 * 1024:
                size_str = f"{stats['total_size'] / (1024*1024):.1f} MB"
            elif stats["total_size"] > 1024:
                size_str = f"{stats['total_size'] / 1024:.1f} KB"
            else:
                size_str = f"{stats['total_size']} B"

            print(f"  📊 Toplam Boyut: {size_str}")
            print(f"  📋 İşlem Türlerine Göre:")

            for type_stat in stats["by_type"]:
                total, processed, size, proc_type = type_stat
                print(f"    {proc_type}: {total} doküman")
        elif command.startswith("mark-processed"):
            parts = command.split()
            if len(parts) > 1:
                file_path = " ".join(parts[1:2])
                processing_type = parts[2] if len(parts) > 2 else "indexed"
                notes = " ".join(parts[3:]) if len(parts) > 3 else None
                self.mark_document_processed(file_path, processing_type, notes)
            else:
                print("❌ Kullanım: mark-processed <dosya_yolu> [işlem_türü]")
        elif command.startswith("check-processed"):
            if len(command.split()) > 1:
                file_path = " ".join(command.split()[1:])
                is_processed = self.is_document_processed(file_path)
                if is_processed:
                    print(f"✅ {file_path} - İşlenmiş")
                else:
                    print(f"❌ {file_path} - İşlenmemiş")
            else:
                print("❌ Kullanım: check-processed <dosya_yolu>")
        else:
            print(f"❌ Bilinmeyen komut: {command}")
            print("💡 'help' komutunu kullanın.")


def main():
    if len(sys.argv) < 2:
        print("❌ Kullanım: python quick_console.py <komut>")
        print("💡 Örnek: python quick_console.py help")
        return

    console = QuickConsole()
    command = " ".join(sys.argv[1:])
    console.run_command(command)


if __name__ == "__main__":
    main()
