#!/usr/bin/env python3
"""
Veritabanı test scripti
"""
import sys
import os
import glob
sys.path.append('src')

from database_manager import DatabaseManager

def main():
    # Veritabanı bağlantısı
    db_path = os.path.join('.collective-memory', 'database', 'collective_memory.db')
    db = DatabaseManager(db_path)

    if db.connect():
        db.initialize_database()
        
        # Markdown ve Python dosyalarını bul
        md_files = glob.glob('**/*.md', recursive=True)
        py_files = glob.glob('src/**/*.py', recursive=True)
        
        all_files = md_files + py_files
        print(f'Bulunan dosyalar: {len(all_files)}')
        
        added_count = 0
        for file_path in all_files[:15]:  # İlk 15 dosyayı ekle
            try:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    file_id = db.add_or_update_file(file_path)
                    if file_id:
                        added_count += 1
                        print(f'✅ Eklendi: {file_path}')
            except Exception as e:
                print(f'❌ Hata ({file_path}): {e}')
        
        print(f'\n📊 Toplam eklenen dosya: {added_count}')
        
        # İstatistikleri göster
        stats = db.get_file_stats()
        print(f'📊 Veritabanındaki toplam dosya: {stats.get("total_files", 0)}')
        print(f'📊 Dosya türleri: {stats.get("file_types", {})}')
        
        # Test arama
        print('\n🔍 Test arama: "database"')
        results = db.search_files("database", limit=5)
        for result in results:
            print(f'  - {result["file_name"]} ({result["file_extension"]})')
        
        db.disconnect()
    else:
        print('❌ Veritabanı bağlantısı başarısız')

if __name__ == "__main__":
    main()