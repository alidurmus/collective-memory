#!/usr/bin/env python3
"""
Document Analyzer - Detects errors and tasks from documentation
Analyzes documentation files to extract issues and tasks
"""

import re
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class DocumentAnalyzer:
    """Dokümantasyon analiz sistemi"""
    
    def __init__(self):
        self.error_patterns = [
            # Port conflicts
            r'port.*(?:conflict|çakış|busy|in use)',
            r'ECONNREFUSED',
            r'Address already in use',
            
            # Test failures  
            r'test.*(?:fail|hata|error)',
            r'(\d+)\/(\d+).*(?:fail|başarısız)',
            r'başarı.*oranı.*(\d+)%',
            
            # Server issues
            r'server.*(?:down|çalışmıyor|not running)',
            r'cannot.*start.*server',
            
            # File/dependency issues
            r'file.*(?:not found|bulunamadı)',
            r'module.*(?:not found|missing)',
            r'ENOENT.*no such file',
            
            # Database issues
            r'database.*(?:lock|corrupt|missing)',
            r'SQLite.*error',
            
            # API issues
            r'API.*(?:error|fail|timeout)',
            r'proxy error',
            r'connection refused'
        ]
        
        self.task_patterns = [
            # Fix/improvement tasks
            r'(?:fix|düzelt|çöz).*(.{20,100})',
            r'TODO:?\s*(.{10,100})',
            r'TASK.*:?\s*(.{10,100})',
            r'implement.*(.{10,100})',
            r'geliştir.*(.{10,100})',
            
            # Testing tasks
            r'test.*(?:coverage|improvement|iyileştir)',
            r'playwright.*(?:fix|implement)',
            
            # Performance tasks
            r'optimization.*(.{10,100})',
            r'performance.*(.{10,100})',
            r'optimize.*(.{10,100})',
            
            # Deployment tasks
            r'deploy.*(.{10,100})',
            r'setup.*(.{10,100})',
            r'install.*(.{10,100})'
        ]
        
        self.priority_keywords = {
            'YÜKSEK': ['kritik', 'critical', 'urgent', 'acil', 'major'],
            'ORTA': ['important', 'önemli', 'medium', 'should'],
            'DÜŞÜK': ['minor', 'enhancement', 'nice to have', 'gelecek']
        }
    
    def analyze_document(self, file_path: str) -> Dict:
        """Doküman analiz eder"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            errors = self._extract_errors(content, file_path)
            tasks = self._extract_tasks(content, file_path)
            
            return {
                'file_path': file_path,
                'errors': errors,
                'tasks': tasks,
                'analyzed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'file_path': file_path,
                'errors': [],
                'tasks': [],
                'error': str(e),
                'analyzed_at': datetime.now().isoformat()
            }
    
    def _extract_errors(self, content: str, file_path: str) -> List[Dict]:
        """İçerikten hataları çıkarır"""
        errors = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Port conflicts
            if re.search(r'port.*(?:3000|8000).*(?:in use|çakış)', line_lower):
                errors.append({
                    'error_code': f'DOC_PORT_CONFLICT_{i}',
                    'error_title': 'Port Çakışması (Dokümantasyon)',
                    'error_description': f'Dokümantasyonda port çakışması tespit edildi: {line.strip()}',
                    'error_type': 'PORT_CONFLICT',
                    'severity_level': 'ORTA',
                    'source_file': file_path,
                    'line_number': i + 1,
                    'resolution_notes': 'Farklı port kullan veya çakışan servisi kapat'
                })
            
            # Test failures
            if re.search(r'(\d+)\/(\d+).*(?:fail|başarısız|error)', line_lower):
                match = re.search(r'(\d+)\/(\d+)', line)
                if match:
                    passed, total = match.groups()
                    failure_rate = (int(total) - int(passed)) / int(total) * 100
                    
                    errors.append({
                        'error_code': f'DOC_TEST_FAILURE_{i}',
                        'error_title': f'Test Başarısızlığı ({failure_rate:.1f}%)',
                        'error_description': f'Test suite başarısızlık oranı yüksek: {line.strip()}',
                        'error_type': 'TEST_FAILURE',
                        'severity_level': 'YÜKSEK' if failure_rate > 50 else 'ORTA',
                        'source_file': file_path,
                        'line_number': i + 1,
                        'resolution_notes': 'Test case\'leri kontrol et ve düzelt'
                    })
            
            # ECONNREFUSED errors
            if 'econnrefused' in line_lower:
                errors.append({
                    'error_code': f'DOC_CONNECTION_REFUSED_{i}',
                    'error_title': 'Bağlantı Reddedildi',
                    'error_description': f'Bağlantı hatası tespit edildi: {line.strip()}',
                    'error_type': 'CONNECTION_ERROR',
                    'severity_level': 'YÜKSEK',
                    'source_file': file_path,
                    'line_number': i + 1,
                    'resolution_notes': 'Server durumunu kontrol et ve başlat'
                })
        
        return errors
    
    def _extract_tasks(self, content: str, file_path: str) -> List[Dict]:
        """İçerikten görevleri çıkarır"""
        tasks = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # TODO tasks
            if re.search(r'todo:?\s*(.{10,100})', line_lower):
                match = re.search(r'todo:?\s*(.{10,100})', line, re.IGNORECASE)
                if match:
                    task_desc = match.group(1).strip()
                    tasks.append({
                        'task_code': f'DOC_TODO_{i}',
                        'task_title': f'TODO: {task_desc[:50]}...',
                        'task_description': task_desc,
                        'task_type': 'DEVELOPMENT',
                        'priority_level': self._determine_priority(line),
                        'notes': f'Dokümantasyondan çıkarıldı: {file_path}:{i+1}'
                    })
            
            # Fix patterns
            if re.search(r'(?:fix|düzelt|çöz)\s+(.{10,100})', line_lower):
                match = re.search(r'(?:fix|düzelt|çöz)\s+(.{10,100})', line, re.IGNORECASE)
                if match:
                    fix_desc = match.group(1).strip()
                    tasks.append({
                        'task_code': f'DOC_FIX_{i}',
                        'task_title': f'Düzeltme: {fix_desc[:50]}...',
                        'task_description': fix_desc,
                        'task_type': 'BUGFIX',
                        'priority_level': self._determine_priority(line),
                        'notes': f'Dokümantasyondan çıkarıldı: {file_path}:{i+1}'
                    })
            
            # Implementation tasks
            if re.search(r'implement\s+(.{10,100})', line_lower):
                match = re.search(r'implement\s+(.{10,100})', line, re.IGNORECASE)
                if match:
                    impl_desc = match.group(1).strip()
                    tasks.append({
                        'task_code': f'DOC_IMPL_{i}',
                        'task_title': f'Uygulama: {impl_desc[:50]}...',
                        'task_description': impl_desc,
                        'task_type': 'FEATURE',
                        'priority_level': self._determine_priority(line),
                        'notes': f'Dokümantasyondan çıkarıldı: {file_path}:{i+1}'
                    })
        
        return tasks
    
    def _determine_priority(self, text: str) -> str:
        """Metinden öncelik seviyesi belirler"""
        text_lower = text.lower()
        
        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return priority
        
        return 'ORTA'  # Default priority
    
    def analyze_all_docs(self, base_path: str = ".") -> List[Dict]:
        """Tüm dokümantasyonları analiz eder"""
        results = []
        
        # Dokümantasyon dosyalarını bul
        doc_patterns = ["*.md", "*.txt", "*REPORT*.md", "*TODO*.md"]
        doc_dirs = ["docs", ".", "tests", "frontend"]
        
        for doc_dir in doc_dirs:
            dir_path = Path(base_path) / doc_dir
            if dir_path.exists():
                for pattern in doc_patterns:
                    for file_path in dir_path.rglob(pattern):
                        if file_path.is_file():
                            result = self.analyze_document(str(file_path))
                            if result['errors'] or result['tasks']:
                                results.append(result)
        
        return results
    
    def save_analysis_to_db(self, etm, analysis_results: List[Dict]) -> Dict:
        """Analiz sonuçlarını veritabanına kaydeder"""
        saved_errors = 0
        saved_tasks = 0
        failed_saves = 0
        
        for result in analysis_results:
            # Hataları kaydet
            for error in result.get('errors', []):
                if etm.save_error(error):
                    saved_errors += 1
                else:
                    failed_saves += 1
            
            # Görevleri kaydet
            for task in result.get('tasks', []):
                if etm.save_task(task):
                    saved_tasks += 1
                else:
                    failed_saves += 1
        
        return {
            'saved_errors': saved_errors,
            'saved_tasks': saved_tasks,
            'failed_saves': failed_saves,
            'analyzed_files': len(analysis_results)
        }


def main():
    """Ana fonksiyon - dokümantasyon analizi çalıştır"""
    import sys
    sys.path.append('../src')
    from error_task_manager import ErrorTaskManager
    from colorama import init, Fore, Style
    
    init()
    
    print(f"\n{Fore.CYAN}📚 Dokümantasyon Analizi Başlatılıyor...{Style.RESET_ALL}")
    
    # Analiz et
    analyzer = DocumentAnalyzer()
    results = analyzer.analyze_all_docs(".")
    
    print(f"{Fore.YELLOW}📊 {len(results)} dosya analiz edildi{Style.RESET_ALL}")
    
    # Veritabanına kaydet
    etm = ErrorTaskManager()
    if etm.connect():
        save_stats = analyzer.save_analysis_to_db(etm, results)
        
        print(f"\n{Fore.GREEN}✅ KAYDETME İSTATİSTİKLERİ:{Style.RESET_ALL}")
        print(f"📄 Analiz edilen dosyalar: {save_stats['analyzed_files']}")
        print(f"🔴 Kaydedilen hatalar: {save_stats['saved_errors']}")
        print(f"📋 Kaydedilen görevler: {save_stats['saved_tasks']}")
        print(f"❌ Kaydetme hataları: {save_stats['failed_saves']}")
        
        etm.close()
    else:
        print(f"{Fore.RED}❌ Veritabanı bağlantısı kurulamadı!{Style.RESET_ALL}")


if __name__ == "__main__":
    main() 