#!/usr/bin/env python3
"""
Error and Task Management System
Console-based error detection and task management for Collective Memory
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from colorama import init, Fore, Style
import logging
import subprocess
import re

# Colorama initialize
init()

class ErrorTaskManager:
    """Hata ve görev yönetimi sistemi"""
    
    def __init__(self, db_path: str = "./collective_memory_errors.db"):
        self.db_path = Path(db_path).resolve()
        self.connection = None
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Database schema for errors and tasks
        self.schema = {
            'errors': '''
                CREATE TABLE IF NOT EXISTS errors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_code TEXT UNIQUE NOT NULL,
                    error_title TEXT NOT NULL,
                    error_description TEXT NOT NULL,
                    error_type TEXT NOT NULL,
                    severity_level TEXT NOT NULL,
                    status TEXT DEFAULT 'aktif',
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TIMESTAMP NULL,
                    source_file TEXT,
                    line_number INTEGER,
                    stack_trace TEXT,
                    resolution_notes TEXT,
                    created_by TEXT DEFAULT 'system',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''',
            'tasks': '''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_code TEXT UNIQUE NOT NULL,
                    task_title TEXT NOT NULL,
                    task_description TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    priority_level TEXT NOT NULL,
                    status TEXT DEFAULT 'beklemede',
                    progress_percentage INTEGER DEFAULT 0,
                    assigned_to TEXT DEFAULT 'system',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP NULL,
                    completed_at TIMESTAMP NULL,
                    due_date TIMESTAMP NULL,
                    dependencies TEXT,
                    notes TEXT,
                    parent_task_id INTEGER NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_task_id) REFERENCES tasks (id)
                )
            ''',
            'error_task_relationships': '''
                CREATE TABLE IF NOT EXISTS error_task_relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error_id INTEGER NOT NULL,
                    task_id INTEGER NOT NULL,
                    relationship_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (error_id) REFERENCES errors (id) ON DELETE CASCADE,
                    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
                    UNIQUE(error_id, task_id, relationship_type)
                )
            ''',
            'system_status': '''
                CREATE TABLE IF NOT EXISTS system_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    component_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    error_count INTEGER DEFAULT 0,
                    warning_count INTEGER DEFAULT 0,
                    info_message TEXT,
                    details TEXT
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
            
            # Tabloları oluştur
            for table_name, schema_sql in self.schema.items():
                self.connection.execute(schema_sql)
            
            self.connection.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Veritabanı bağlantı hatası: {e}")
            return False
    
    def detect_system_errors(self) -> List[Dict]:
        """Sistem hatalarını tespit eder"""
        errors = []
        
        # Frontend port check
        frontend_error = self._check_frontend_port()
        if frontend_error:
            errors.append(frontend_error)
        
        # Backend server check
        backend_error = self._check_backend_server()
        if backend_error:
            errors.append(backend_error)
        
        # Node modules check
        node_error = self._check_node_modules()
        if node_error:
            errors.append(node_error)
        
        # Database file check
        db_error = self._check_database_files()
        if db_error:
            errors.append(db_error)
        
        return errors
    
    def _check_frontend_port(self) -> Optional[Dict]:
        """Frontend port durumunu kontrol eder"""
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            if ':3000' in result.stdout:
                return {
                    'error_code': 'FRONTEND_PORT_CONFLICT',
                    'error_title': 'Frontend Port 3000 Çakışması',
                    'error_description': 'Port 3000 zaten kullanımda. Frontend server başlatılamıyor.',
                    'error_type': 'PORT_CONFLICT',
                    'severity_level': 'YÜKSEK',
                    'source_file': 'frontend/package.json',
                    'resolution_notes': 'Port 3003 veya başka bir port kullan'
                }
        except Exception as e:
            self.logger.error(f"Port kontrol hatası: {e}")
        return None
    
    def _check_backend_server(self) -> Optional[Dict]:
        """Backend server durumunu kontrol eder"""
        try:
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            if ':8000' not in result.stdout:
                return {
                    'error_code': 'BACKEND_SERVER_DOWN',
                    'error_title': 'Backend Server Çalışmıyor',
                    'error_description': 'Port 8000\'de backend server çalışmıyor. API erişilemez durumda.',
                    'error_type': 'SERVER_DOWN',
                    'severity_level': 'KRİTİK',
                    'source_file': 'api_server.py',
                    'resolution_notes': 'python api_server.py --host localhost --port 8000 komutunu çalıştır'
                }
        except Exception as e:
            self.logger.error(f"Backend kontrol hatası: {e}")
        return None
    
    def _check_node_modules(self) -> Optional[Dict]:
        """Node modules varlığını kontrol eder"""
        frontend_node = Path('./frontend/node_modules')
        if not frontend_node.exists():
            return {
                'error_code': 'NODE_MODULES_MISSING',
                'error_title': 'Node Modules Eksik',
                'error_description': 'Frontend node_modules klasörü bulunamadı.',
                'error_type': 'DEPENDENCY_MISSING',
                'severity_level': 'ORTA',
                'source_file': 'frontend/package.json',
                'resolution_notes': 'cd frontend && npm install çalıştır'
            }
        return None
    
    def _check_database_files(self) -> Optional[Dict]:
        """Veritabanı dosyalarını kontrol eder"""
        db_files = [
            './data/collective_memory.db',
            './.collective-memory/database/collective_memory.db'
        ]
        
        for db_file in db_files:
            if Path(db_file).exists():
                return None
        
        return {
            'error_code': 'DATABASE_FILE_MISSING',
            'error_title': 'Veritabanı Dosyası Bulunamadı',
            'error_description': 'Collective Memory veritabanı dosyası bulunamadı.',
            'error_type': 'DATABASE_MISSING',
            'severity_level': 'YÜKSEK',
            'source_file': 'src/database_manager.py',
            'resolution_notes': 'python src/main.py --index komutu ile veritabanını oluştur'
        }
    
    def save_error(self, error_data: Dict) -> bool:
        """Hatayı veritabanına kaydeder"""
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO errors 
                (error_code, error_title, error_description, error_type, 
                 severity_level, source_file, line_number, stack_trace, resolution_notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                error_data.get('error_code'),
                error_data.get('error_title'),
                error_data.get('error_description'),
                error_data.get('error_type'),
                error_data.get('severity_level'),
                error_data.get('source_file'),
                error_data.get('line_number'),
                error_data.get('stack_trace'),
                error_data.get('resolution_notes')
            ))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Hata kaydetme hatası: {e}")
            return False
    
    def get_errors(self, status: str = None) -> List[Dict]:
        """Hataları getirir"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            if status:
                cursor.execute('SELECT * FROM errors WHERE status = ? ORDER BY detected_at DESC', (status,))
            else:
                cursor.execute('SELECT * FROM errors ORDER BY detected_at DESC')
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            self.logger.error(f"Hata getirme hatası: {e}")
            return []
    
    def update_error_status(self, error_code: str, status: str, resolution_notes: str = None) -> bool:
        """Hata durumunu günceller"""
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            if status == 'düzeltildi':
                cursor.execute('''
                    UPDATE errors 
                    SET status = ?, resolved_at = CURRENT_TIMESTAMP, 
                        resolution_notes = COALESCE(?, resolution_notes),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE error_code = ?
                ''', (status, resolution_notes, error_code))
            else:
                cursor.execute('''
                    UPDATE errors 
                    SET status = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE error_code = ?
                ''', (status, error_code))
            
            self.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            self.logger.error(f"Hata güncelleme hatası: {e}")
            return False
    
    def save_task(self, task_data: Dict) -> bool:
        """Görevi veritabanına kaydeder"""
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO tasks 
                (task_code, task_title, task_description, task_type, 
                 priority_level, assigned_to, dependencies, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                task_data.get('task_code'),
                task_data.get('task_title'),
                task_data.get('task_description'),
                task_data.get('task_type'),
                task_data.get('priority_level'),
                task_data.get('assigned_to', 'system'),
                json.dumps(task_data.get('dependencies', [])),
                task_data.get('notes')
            ))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Görev kaydetme hatası: {e}")
            return False
    
    def get_tasks(self, status: str = None) -> List[Dict]:
        """Görevleri getirir"""
        if not self.connection:
            if not self.connect():
                return []
        
        try:
            cursor = self.connection.cursor()
            if status:
                cursor.execute('SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC', (status,))
            else:
                cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            
            tasks = []
            for row in cursor.fetchall():
                task = dict(row)
                if task['dependencies']:
                    try:
                        task['dependencies'] = json.loads(task['dependencies'])
                    except:
                        task['dependencies'] = []
                tasks.append(task)
            
            return tasks
            
        except Exception as e:
            self.logger.error(f"Görev getirme hatası: {e}")
            return []
    
    def update_task_status(self, task_code: str, status: str, progress: int = None, notes: str = None) -> bool:
        """Görev durumunu günceller"""
        if not self.connection:
            if not self.connect():
                return False
        
        try:
            cursor = self.connection.cursor()
            
            update_fields = ['status = ?', 'updated_at = CURRENT_TIMESTAMP']
            params = [status]
            
            if status == 'tamamlandı':
                update_fields.append('completed_at = CURRENT_TIMESTAMP')
                update_fields.append('progress_percentage = 100')
            elif status == 'devam_ediyor':
                update_fields.append('started_at = CURRENT_TIMESTAMP')
                if progress is not None:
                    update_fields.append('progress_percentage = ?')
                    params.append(progress)
            
            if notes:
                update_fields.append('notes = COALESCE(notes || ? || ?, ?)')
                params.extend(['\n---\n', notes, notes])
            
            params.append(task_code)
            
            sql = f'UPDATE tasks SET {", ".join(update_fields)} WHERE task_code = ?'
            cursor.execute(sql, params)
            
            self.connection.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            self.logger.error(f"Görev güncelleme hatası: {e}")
            return False
    
    def run_error_detection(self) -> None:
        """Hata tespiti çalıştırır ve kaydeder"""
        print(f"\n{Fore.CYAN}🔍 Sistem Hata Tespiti Başlatılıyor...{Style.RESET_ALL}")
        
        errors = self.detect_system_errors()
        
        if not errors:
            print(f"{Fore.GREEN}✅ Sistem hatası tespit edilmedi.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}⚠️ {len(errors)} hata tespit edildi:{Style.RESET_ALL}")
        
        for error in errors:
            success = self.save_error(error)
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {error['error_code']}: {error['error_title']}")
            if success:
                print(f"   📝 Veritabanına kaydedildi")
            else:
                print(f"   💥 Kaydetme hatası!")
    
    def list_errors_console(self, status: str = None) -> None:
        """Console'da hataları listeler"""
        errors = self.get_errors(status)
        
        if not errors:
            status_text = f" (Durum: {status})" if status else ""
            print(f"{Fore.GREEN}✅ Hata bulunamadı{status_text}.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}📋 HATA LİSTESİ{Style.RESET_ALL}")
        print("=" * 80)
        
        for error in errors:
            status_color = Fore.RED if error['status'] == 'aktif' else Fore.GREEN
            severity_color = Fore.RED if error['severity_level'] == 'KRİTİK' else Fore.YELLOW
            
            print(f"\n🆔 {Fore.BLUE}{error['error_code']}{Style.RESET_ALL}")
            print(f"📌 {Fore.WHITE}{error['error_title']}{Style.RESET_ALL}")
            print(f"📄 {error['error_description']}")
            print(f"🏷️  Tip: {error['error_type']}")
            print(f"⚡ Önem: {severity_color}{error['severity_level']}{Style.RESET_ALL}")
            print(f"📊 Durum: {status_color}{error['status']}{Style.RESET_ALL}")
            print(f"📅 Tespit: {error['detected_at']}")
            
            if error['source_file']:
                print(f"📁 Dosya: {error['source_file']}")
            
            if error['resolution_notes']:
                print(f"💡 Çözüm: {Fore.CYAN}{error['resolution_notes']}{Style.RESET_ALL}")
            
            if error['resolved_at']:
                print(f"✅ Çözüldü: {error['resolved_at']}")
        
        print("=" * 80)
    
    def list_tasks_console(self, status: str = None) -> None:
        """Console'da görevleri listeler"""
        tasks = self.get_tasks(status)
        
        if not tasks:
            status_text = f" (Durum: {status})" if status else ""
            print(f"{Fore.GREEN}✅ Görev bulunamadı{status_text}.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}📋 GÖREV LİSTESİ{Style.RESET_ALL}")
        print("=" * 80)
        
        for task in tasks:
            status_color = {
                'beklemede': Fore.YELLOW,
                'devam_ediyor': Fore.BLUE,
                'tamamlandı': Fore.GREEN,
                'iptal': Fore.RED
            }.get(task['status'], Fore.WHITE)
            
            priority_color = {
                'YÜKSEK': Fore.RED,
                'ORTA': Fore.YELLOW,
                'DÜŞÜK': Fore.GREEN
            }.get(task['priority_level'], Fore.WHITE)
            
            print(f"\n🆔 {Fore.BLUE}{task['task_code']}{Style.RESET_ALL}")
            print(f"📌 {Fore.WHITE}{task['task_title']}{Style.RESET_ALL}")
            print(f"📄 {task['task_description']}")
            print(f"🏷️  Tip: {task['task_type']}")
            print(f"⚡ Öncelik: {priority_color}{task['priority_level']}{Style.RESET_ALL}")
            print(f"📊 Durum: {status_color}{task['status']}{Style.RESET_ALL}")
            print(f"📈 İlerleme: {task['progress_percentage']}%")
            print(f"👤 Atanan: {task['assigned_to']}")
            print(f"📅 Oluşturulma: {task['created_at']}")
            
            if task['started_at']:
                print(f"▶️ Başlangıç: {task['started_at']}")
            
            if task['completed_at']:
                print(f"✅ Tamamlanma: {task['completed_at']}")
            
            if task['dependencies']:
                print(f"🔗 Bağımlılıklar: {', '.join(task['dependencies'])}")
            
            if task['notes']:
                print(f"📝 Notlar: {task['notes']}")
        
        print("=" * 80)
    
    def close(self):
        """Veritabanı bağlantısını kapatır"""
        if self.connection:
            self.connection.close()
            self.connection = None


def main():
    """Ana console interface"""
    etm = ErrorTaskManager()
    
    if not etm.connect():
        print(f"{Fore.RED}❌ Veritabanı bağlantısı kurulamadı!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}🔧 Collective Memory - Hata ve Görev Yönetimi{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Kullanılabilir komutlar:{Style.RESET_ALL}")
    print("  • hata-tespit     - Sistem hatalarını tespit et")
    print("  • hatalar         - Tüm hataları listele")
    print("  • aktif-hatalar   - Sadece aktif hataları listele")
    print("  • görevler        - Tüm görevleri listele")
    print("  • bekleyen-görevler - Bekleyen görevleri listele")
    print("  • hata-düzelt <kod> - Hatayı düzeltildi olarak işaretle")
    print("  • görev-tamamla <kod> - Görevi tamamlandı olarak işaretle")
    print("  • çıkış          - Programdan çık")
    
    try:
        while True:
            command = input(f"\n{Fore.GREEN}> {Style.RESET_ALL}").strip().lower()
            
            if command == 'çıkış' or command == 'quit' or command == 'exit':
                break
            elif command == 'hata-tespit':
                etm.run_error_detection()
            elif command == 'hatalar':
                etm.list_errors_console()
            elif command == 'aktif-hatalar':
                etm.list_errors_console('aktif')
            elif command == 'görevler':
                etm.list_tasks_console()
            elif command == 'bekleyen-görevler':
                etm.list_tasks_console('beklemede')
            elif command.startswith('hata-düzelt '):
                error_code = command.replace('hata-düzelt ', '').strip()
                if etm.update_error_status(error_code, 'düzeltildi'):
                    print(f"{Fore.GREEN}✅ Hata {error_code} düzeltildi olarak işaretlendi.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Hata bulunamadı veya güncellenemedi.{Style.RESET_ALL}")
            elif command.startswith('görev-tamamla '):
                task_code = command.replace('görev-tamamla ', '').strip()
                if etm.update_task_status(task_code, 'tamamlandı'):
                    print(f"{Fore.GREEN}✅ Görev {task_code} tamamlandı olarak işaretlendi.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}❌ Görev bulunamadı veya güncellenemedi.{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}❓ Bilinmeyen komut. Yardım için geçerli komutları yukarıda görebilirsiniz.{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Çıkış yapılıyor...{Style.RESET_ALL}")
    
    finally:
        etm.close()
        print(f"{Fore.CYAN}✅ Hata ve Görev Yönetimi kapatıldı.{Style.RESET_ALL}")


if __name__ == "__main__":
    main() 