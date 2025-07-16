#!/usr/bin/env python3
import sqlite3


def check_database():
    """Mevcut veritabanı yapısını kontrol et"""
    conn = sqlite3.connect('comprehensive_system.db')
    cursor = conn.cursor()
    
    # Tablo listesi
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("📋 TABLOLAR:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Tasks tablosu yapısı
    if any('tasks' in table for table in tables):
        cursor.execute("PRAGMA table_info(tasks)")
        columns = cursor.fetchall()
        print("\n📋 TASKS TABLOSU:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    # Errors tablosu yapısı
    if any('errors' in table for table in tables):
        cursor.execute("PRAGMA table_info(errors)")
        columns = cursor.fetchall()
        print("\n🔴 ERRORS TABLOSU:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()


if __name__ == "__main__":
    check_database() 