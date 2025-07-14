#!/bin/bash

#
# Context7 ERP - Database Operations Script Examples
# Version: v2.2.0-glassmorphism-enhanced
# Source: utilities-guide.md ve çeşitli dosyalar
# Purpose: Database yönetim komutları - büyük kod örnekleri
#

# =============================
# 1. DATABASE BACKUP OPERATIONS
# =============================

# PostgreSQL full backup
backup_postgresql() {
    local db_name="${1:-context7_erp}"
    local backup_dir="backups/database"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    echo "📊 PostgreSQL backup başlıyor: $db_name"
    
    mkdir -p "$backup_dir"
    
    # Full database backup
    pg_dump "$db_name" > "$backup_dir/postgresql_backup_$timestamp.sql"
    
    # Compressed backup
    pg_dump "$db_name" | gzip > "$backup_dir/postgresql_backup_$timestamp.sql.gz"
    
    echo "✅ PostgreSQL backup tamamlandı: $backup_dir/postgresql_backup_$timestamp.sql"
}

# SQLite backup
backup_sqlite() {
    local db_file="${1:-db.sqlite3}"
    local backup_dir="backups/database"
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    echo "📊 SQLite backup başlıyor: $db_file"
    
    mkdir -p "$backup_dir"
    
    if [ -f "$db_file" ]; then
        cp "$db_file" "$backup_dir/sqlite_backup_$timestamp.sqlite3"
        echo "✅ SQLite backup tamamlandı: $backup_dir/sqlite_backup_$timestamp.sqlite3"
    else
        echo "❌ SQLite dosyası bulunamadı: $db_file"
        return 1
    fi
}

# Django data export
export_django_data() {
    local output_file="${1:-data_export_$(date +%Y%m%d_%H%M%S).json}"
    local backup_dir="backups/database"
    
    echo "📦 Django data export başlıyor..."
    
    mkdir -p "$backup_dir"
    
    # Full data export
    python manage.py dumpdata --indent=2 > "$backup_dir/$output_file"
    
    # Specific app export
    python manage.py dumpdata erp --indent=2 > "$backup_dir/erp_data_$(date +%Y%m%d_%H%M%S).json"
    python manage.py dumpdata users --indent=2 > "$backup_dir/users_data_$(date +%Y%m%d_%H%M%S).json"
    
    echo "✅ Django data export tamamlandı: $backup_dir/$output_file"
}

# =============================
# 2. DATABASE RESTORE OPERATIONS
# =============================

# PostgreSQL restore
restore_postgresql() {
    local backup_file="$1"
    local db_name="${2:-context7_erp}"
    
    if [ -z "$backup_file" ]; then
        echo "❌ Backup dosyası belirtilmedi"
        echo "Kullanım: restore_postgresql <backup_file> [db_name]"
        return 1
    fi
    
    echo "🔄 PostgreSQL restore başlıyor: $backup_file → $db_name"
    
    # Database'i drop ve yeniden oluştur
    dropdb "$db_name" 2>/dev/null || true
    createdb "$db_name"
    
    # Restore data
    if [[ "$backup_file" == *.gz ]]; then
        gunzip -c "$backup_file" | psql "$db_name"
    else
        psql "$db_name" < "$backup_file"
    fi
    
    echo "✅ PostgreSQL restore tamamlandı"
}

# SQLite restore
restore_sqlite() {
    local backup_file="$1"
    local target_file="${2:-db.sqlite3}"
    
    if [ -z "$backup_file" ]; then
        echo "❌ Backup dosyası belirtilmedi"
        echo "Kullanım: restore_sqlite <backup_file> [target_file]"
        return 1
    fi
    
    echo "🔄 SQLite restore başlıyor: $backup_file → $target_file"
    
    # Backup current database
    if [ -f "$target_file" ]; then
        cp "$target_file" "${target_file}.backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Restore from backup
    cp "$backup_file" "$target_file"
    
    echo "✅ SQLite restore tamamlandı"
}

# Django data restore
restore_django_data() {
    local backup_file="$1"
    local flush_first="${2:-no}"
    
    if [ -z "$backup_file" ]; then
        echo "❌ Backup dosyası belirtilmedi"
        echo "Kullanım: restore_django_data <backup_file> [flush_first]"
        return 1
    fi
    
    echo "🔄 Django data restore başlıyor: $backup_file"
    
    # Flush database if requested
    if [ "$flush_first" = "yes" ]; then
        echo "⚠️  Database flush yapılıyor..."
        python manage.py flush --noinput
    fi
    
    # Load data
    python manage.py loaddata "$backup_file"
    
    echo "✅ Django data restore tamamlandı"
}

# =============================
# 3. DATABASE MIGRATION OPERATIONS
# =============================

# Full migration reset
reset_migrations() {
    local app_name="$1"
    
    echo "🔄 Migration reset başlıyor..."
    
    if [ -n "$app_name" ]; then
        # Specific app migration reset
        echo "📱 $app_name app migration reset..."
        rm -rf "$app_name/migrations/"*.py
        rm -rf "$app_name/migrations/"__pycache__
        touch "$app_name/migrations/__init__.py"
        python manage.py makemigrations "$app_name"
    else
        # All apps migration reset
        echo "📱 Tüm app'ların migration reset..."
        find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
        find . -path "*/migrations/*.pyc" -delete
        find . -path "*/migrations/__pycache__" -delete
        python manage.py makemigrations
    fi
    
    python manage.py migrate
    echo "✅ Migration reset tamamlandı"
}

# Fake migrations (for existing data)
fake_migrate() {
    local app_name="$1"
    
    echo "🎭 Fake migration başlıyor..."
    
    if [ -n "$app_name" ]; then
        python manage.py migrate "$app_name" --fake
    else
        python manage.py migrate --fake
    fi
    
    echo "✅ Fake migration tamamlandı"
}

# =============================
# 4. DATABASE OPTIMIZATION
# =============================

# PostgreSQL optimization
optimize_postgresql() {
    local db_name="${1:-context7_erp}"
    
    echo "⚡ PostgreSQL optimizasyon başlıyor: $db_name"
    
    # Vacuum and analyze
    psql "$db_name" -c "VACUUM VERBOSE ANALYZE;"
    
    # Reindex
    psql "$db_name" -c "REINDEX DATABASE $db_name;"
    
    # Update statistics
    psql "$db_name" -c "ANALYZE;"
    
    echo "✅ PostgreSQL optimizasyon tamamlandı"
}

# SQLite optimization
optimize_sqlite() {
    local db_file="${1:-db.sqlite3}"
    
    echo "⚡ SQLite optimizasyon başlıyor: $db_file"
    
    if [ -f "$db_file" ]; then
        # Vacuum database
        echo "VACUUM;" | sqlite3 "$db_file"
        
        # Analyze database
        echo "ANALYZE;" | sqlite3 "$db_file"
        
        # Rebuild indexes
        echo "REINDEX;" | sqlite3 "$db_file"
        
        echo "✅ SQLite optimizasyon tamamlandı"
    else
        echo "❌ SQLite dosyası bulunamadı: $db_file"
        return 1
    fi
}

# =============================
# 5. DATABASE HEALTH CHECK
# =============================

# PostgreSQL health check
check_postgresql_health() {
    local db_name="${1:-context7_erp}"
    
    echo "🔍 PostgreSQL health check: $db_name"
    
    # Connection test
    if pg_isready -d "$db_name" >/dev/null 2>&1; then
        echo "✅ Database connection: OK"
    else
        echo "❌ Database connection: FAILED"
        return 1
    fi
    
    # Table count
    table_count=$(psql -d "$db_name" -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
    echo "📋 Tablo sayısı: $table_count"
    
    # Database size
    db_size=$(psql -d "$db_name" -t -c "SELECT pg_size_pretty(pg_database_size('$db_name'));")
    echo "💾 Database boyutu: $db_size"
    
    # Active connections
    connections=$(psql -d "$db_name" -t -c "SELECT count(*) FROM pg_stat_activity WHERE datname = '$db_name';")
    echo "🔗 Aktif bağlantılar: $connections"
}

# SQLite health check
check_sqlite_health() {
    local db_file="${1:-db.sqlite3}"
    
    echo "🔍 SQLite health check: $db_file"
    
    if [ -f "$db_file" ]; then
        # File size
        file_size=$(du -h "$db_file" | cut -f1)
        echo "💾 Database boyutu: $file_size"
        
        # Table count
        table_count=$(echo "SELECT count(*) FROM sqlite_master WHERE type='table';" | sqlite3 "$db_file")
        echo "📋 Tablo sayısı: $table_count"
        
        # Integrity check
        integrity=$(echo "PRAGMA integrity_check;" | sqlite3 "$db_file")
        if [ "$integrity" = "ok" ]; then
            echo "✅ Database integrity: OK"
        else
            echo "❌ Database integrity: FAILED"
            echo "$integrity"
        fi
        
        echo "✅ SQLite health check tamamlandı"
    else
        echo "❌ SQLite dosyası bulunamadı: $db_file"
        return 1
    fi
}

# =============================
# 6. DATA MANAGEMENT
# =============================

# Clean old data
clean_old_data() {
    echo "🧹 Eski veri temizleme başlıyor..."
    
    # Django management command ile
    python manage.py shell << 'EOF'
from django.utils import timezone
from datetime import timedelta
from django.contrib.sessions.models import Session
from core.models import LogEntry

# Eski session'ları temizle (30 gün öncesi)
old_sessions = Session.objects.filter(expire_date__lt=timezone.now() - timedelta(days=30))
deleted_sessions = old_sessions.count()
old_sessions.delete()
print(f"✅ {deleted_sessions} eski session temizlendi")

# Eski log kayıtlarını temizle (90 gün öncesi)
if 'LogEntry' in locals():
    old_logs = LogEntry.objects.filter(created_at__lt=timezone.now() - timedelta(days=90))
    deleted_logs = old_logs.count()
    old_logs.delete()
    print(f"✅ {deleted_logs} eski log kaydı temizlendi")
EOF
    
    echo "✅ Eski veri temizleme tamamlandı"
}

# Create sample data
create_sample_data() {
    echo "📊 Örnek veri oluşturma başlıyor..."
    
    # Sample data management commands
    python manage.py create_categories_sample_data
    python manage.py create_products_sample_data
    python manage.py create_customers_sample_data
    python manage.py create_suppliers_sample_data
    python manage.py create_sales_sample_data
    
    echo "✅ Örnek veri oluşturma tamamlandı"
}

# =============================
# 7. MAIN FUNCTIONS
# =============================

# Full backup
full_backup() {
    echo "💾 Full backup başlıyor..."
    
    # Database backup
    backup_postgresql
    backup_sqlite
    export_django_data
    
    # Media files backup
    if [ -d "media" ]; then
        tar -czf "backups/media/media_backup_$(date +%Y%m%d_%H%M%S).tar.gz" media/
        echo "✅ Media files backup tamamlandı"
    fi
    
    echo "🎉 Full backup tamamlandı!"
}

# Show usage
show_usage() {
    echo "📖 Context7 ERP Database Operations Usage"
    echo "========================================"
    echo ""
    echo "💾 Backup Operations:"
    echo "  backup_postgresql [db_name]      - PostgreSQL backup"
    echo "  backup_sqlite [db_file]          - SQLite backup"
    echo "  export_django_data [output_file] - Django data export"
    echo "  full_backup                      - Complete backup"
    echo ""
    echo "🔄 Restore Operations:"
    echo "  restore_postgresql <backup_file> [db_name] - PostgreSQL restore"
    echo "  restore_sqlite <backup_file> [target_file] - SQLite restore"
    echo "  restore_django_data <backup_file> [flush]  - Django data restore"
    echo ""
    echo "🔧 Migration Operations:"
    echo "  reset_migrations [app_name]      - Reset migrations"
    echo "  fake_migrate [app_name]          - Fake migrations"
    echo ""
    echo "⚡ Optimization:"
    echo "  optimize_postgresql [db_name]    - PostgreSQL optimize"
    echo "  optimize_sqlite [db_file]        - SQLite optimize"
    echo ""
    echo "🔍 Health Check:"
    echo "  check_postgresql_health [db_name] - PostgreSQL health"
    echo "  check_sqlite_health [db_file]     - SQLite health"
    echo ""
    echo "🧹 Data Management:"
    echo "  clean_old_data                   - Clean old data"
    echo "  create_sample_data               - Create sample data"
    echo ""
    echo "Örnek kullanım:"
    echo "  source database-operations.sh && backup_postgresql"
    echo "  bash database-operations.sh"
}

# Script direkt çalıştırıldığında usage göster
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_usage
fi 