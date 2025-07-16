#!/usr/bin/env python3
"""
Database Optimization Script
SQLite veritabanını optimize eder ve cache ayarlarını yapar
"""
import sqlite3
import os


def optimize_database():
    """Ana veritabanı optimizasyonu"""
    db_files = [
        'collective_memory.db',
        'comprehensive_system.db',
        'collective_memory_errors.db'
    ]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"🔧 {db_file} optimize ediliyor...")
            
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Optimize komutları
                cursor.execute("PRAGMA optimize;")
                cursor.execute("PRAGMA vacuum;")
                cursor.execute("PRAGMA journal_mode = WAL;")
                cursor.execute("PRAGMA synchronous = NORMAL;")
                cursor.execute("PRAGMA cache_size = 10000;")
                cursor.execute("PRAGMA temp_store = MEMORY;")
                
                conn.commit()
                conn.close()
                
                print(f"✅ {db_file} başarıyla optimize edildi")
                
            except Exception as e:
                print(f"❌ {db_file} optimize edilirken hata: {e}")
        else:
            print(f"⚠️  {db_file} bulunamadı")
    
    print("\n🎉 Database optimization tamamlandı!")


if __name__ == "__main__":
    optimize_database() 