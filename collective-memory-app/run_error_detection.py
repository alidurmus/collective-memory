#!/usr/bin/env python3
"""
Automated Error Detection Script
Quickly run error detection and save to database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/src')

from error_task_manager import ErrorTaskManager
from colorama import init, Fore, Style

# Colorama initialize
init()


def run_detection():
    """Hata tespiti çalıştır ve kaydet"""
    etm = ErrorTaskManager()
    
    if not etm.connect():
        print(f"{Fore.RED}❌ Veritabanı bağlantısı kurulamadı!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}🔍 Otomatik Sistem Hata Tespiti{Style.RESET_ALL}")
    print("=" * 50)
    
    # Hata tespiti çalıştır
    etm.run_error_detection()
    
    # Tüm hataları listele
    print(f"\n{Fore.YELLOW}📋 TESPİT EDİLEN HATALAR:{Style.RESET_ALL}")
    etm.list_errors_console('aktif')
    
    # Sistem durumunu da ekle
    create_initial_tasks(etm)
    
    print(f"\n{Fore.YELLOW}📋 OLUŞTURULAN GÖREVLER:{Style.RESET_ALL}")
    etm.list_tasks_console('beklemede')
    
    etm.close()

def create_initial_tasks(etm):
    """İlk görevleri oluştur"""
    tasks = [
        {
            'task_code': 'TASK_001',
            'task_title': 'Backend Server Başlatma',
            'task_description': 'API server port 8000\'de başlatılması gerekiyor',
            'task_type': 'DEPLOYMENT',
            'priority_level': 'YÜKSEK',
            'notes': 'python api_server.py --host localhost --port 8000 --debug'
        },
        {
            'task_code': 'TASK_002', 
            'task_title': 'Frontend Port Çakışması Çözümü',
            'task_description': 'Frontend port 3000 çakışması çözülmeli, port 3003 kullanılmalı',
            'task_type': 'CONFIGURATION',
            'priority_level': 'ORTA',
            'notes': 'cd frontend && npm run dev -- --port 3003'
        },
        {
            'task_code': 'TASK_003',
            'task_title': 'Test Infrastructure İyileştirilmesi',
            'task_description': 'Playwright testleri ve backend testleri stabilize edilmeli',
            'task_type': 'TESTING',
            'priority_level': 'ORTA',
            'notes': 'Test success rate %88.4 -> %95+ hedefleniyor'
        },
        {
            'task_code': 'TASK_004',
            'task_title': 'Database Optimization',
            'task_description': 'Veritabanı indexleme ve cache optimizasyonu',
            'task_type': 'OPTIMIZATION',
            'priority_level': 'DÜŞÜK',
            'notes': 'SQLite performance tuning ve index optimization'
        }
    ]
    
    for task in tasks:
        success = etm.save_task(task)
        if success:
            print(f"✅ Görev oluşturuldu: {task['task_code']}")
        else:
            print(f"❌ Görev oluşturulamadı: {task['task_code']}")

def show_status():
    """Sistem durumunu göster"""
    etm = ErrorTaskManager()
    
    if not etm.connect():
        print(f"{Fore.RED}❌ Veritabanı bağlantısı kurulamadı!{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}📊 SİSTEM DURUMU{Style.RESET_ALL}")
    print("=" * 50)
    
    # Aktif hatalar
    active_errors = etm.get_errors('aktif')
    print(f"🔴 Aktif Hatalar: {len(active_errors)}")
    
    # Tüm hatalar
    all_errors = etm.get_errors()
    print(f"📋 Toplam Hatalar: {len(all_errors)}")
    
    # Bekleyen görevler
    pending_tasks = etm.get_tasks('beklemede')
    print(f"⏳ Bekleyen Görevler: {len(pending_tasks)}")
    
    # Tamamlanan görevler
    completed_tasks = etm.get_tasks('tamamlandı')
    print(f"✅ Tamamlanan Görevler: {len(completed_tasks)}")
    
    etm.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'status':
            show_status()
        elif sys.argv[1] == 'errors':
            etm = ErrorTaskManager()
            etm.connect()
            etm.list_errors_console()
            etm.close()
        elif sys.argv[1] == 'tasks':
            etm = ErrorTaskManager()
            etm.connect()
            etm.list_tasks_console()
            etm.close()
    else:
        run_detection() 