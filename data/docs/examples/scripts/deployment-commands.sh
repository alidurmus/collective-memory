#!/bin/bash

#
# Context7 ERP - Deployment Script Örnekleri
# Version: v2.2.0-glassmorphism-enhanced
# Source: Çeşitli deployment docs dosyaları
# Purpose: Deployment komutları - büyük kod örnekleri
#

# =============================
# 1. TEMEL DEPLOYMENT KOMUTLARI
# =============================

# Git pull ve update işlemi
update_codebase() {
    echo "🔄 Kod güncellemesi yapılıyor..."
    git pull origin main
    echo "✅ Kod güncellendi"
}

# Virtual environment kurulumu
setup_virtualenv() {
    echo "🐍 Python virtual environment kurulumu..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Virtual environment hazır"
}

# Database migrations
run_migrations() {
    echo "📊 Database migration işlemi..."
    python manage.py makemigrations
    python manage.py migrate
    echo "✅ Migration tamamlandı"
}

# Static files collection
collect_static() {
    echo "📁 Static files toplama işlemi..."
    python manage.py collectstatic --noinput
    echo "✅ Static files toplandı"
}

# =============================
# 2. HOSTINGER VPS DEPLOYMENT
# =============================

# Hostinger'a deployment
deploy_to_hostinger() {
    echo "🚀 Hostinger VPS'e deployment başlıyor..."
    
    # Sunucu bilgileri
    SERVER_IP="31.97.44.248"
    SERVER_USER="root"
    PROJECT_PATH="/opt/context7"
    
    # Uzak sunucuya bağlan ve deployment yap
    ssh $SERVER_USER@$SERVER_IP << 'ENDSSH'
        cd /opt/context7
        
        # Backup oluştur
        echo "💾 Backup oluşturuluyor..."
        sudo systemctl stop context7
        cp -r /opt/context7 /opt/context7_backup_$(date +%Y%m%d_%H%M%S)
        
        # Git pull
        echo "🔄 Kod güncelleniyor..."
        git pull origin main
        
        # Python dependencies
        echo "📦 Dependencies güncelleniyor..."
        source venv/bin/activate
        pip install -r requirements.txt
        
        # Database migrations
        echo "📊 Database migration..."
        python manage.py migrate
        
        # Static files
        echo "📁 Static files..."
        python manage.py collectstatic --noinput
        
        # Restart services
        echo "🔄 Servisler restart ediliyor..."
        sudo systemctl start context7
        sudo systemctl restart nginx
        
        echo "✅ Deployment tamamlandı!"
ENDSSH
    
    echo "🎉 Hostinger deployment başarılı!"
}

# =============================
# 3. DOCKER DEPLOYMENT
# =============================

# Docker container build
build_docker_image() {
    echo "🐳 Docker image build ediliyor..."
    docker build -t context7-erp:latest .
    echo "✅ Docker image hazır"
}

# Docker compose deployment
deploy_with_docker() {
    echo "🐳 Docker Compose ile deployment..."
    
    # Docker Compose dosyası
    cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=dashboard_project.settings.production
      - DATABASE_URL=postgresql://context7:password@db:5432/context7_erp
    volumes:
      - ./media:/app/media
      - ./static:/app/static
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: context7_erp
      POSTGRES_USER: context7
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/var/www/static
      - ./media:/var/www/media
    depends_on:
      - web

volumes:
  postgres_data:
EOF
    
    # Deploy
    docker-compose down
    docker-compose up -d --build
    
    echo "✅ Docker deployment tamamlandı"
}

# =============================
# 4. DATABASE OPERATIONS
# =============================

# Database backup
backup_database() {
    echo "💾 Database backup oluşturuluyor..."
    BACKUP_DIR="backups/database"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    
    mkdir -p $BACKUP_DIR
    
    # PostgreSQL backup
    if command -v pg_dump &> /dev/null; then
        pg_dump context7_erp > $BACKUP_DIR/postgresql_backup_$TIMESTAMP.sql
        echo "✅ PostgreSQL backup: $BACKUP_DIR/postgresql_backup_$TIMESTAMP.sql"
    fi
    
    # SQLite backup
    if [ -f "db.sqlite3" ]; then
        cp db.sqlite3 $BACKUP_DIR/sqlite_backup_$TIMESTAMP.sqlite3
        echo "✅ SQLite backup: $BACKUP_DIR/sqlite_backup_$TIMESTAMP.sqlite3"
    fi
    
    # Data export
    python manage.py dumpdata --indent=2 > $BACKUP_DIR/data_backup_$TIMESTAMP.json
    echo "✅ Data export: $BACKUP_DIR/data_backup_$TIMESTAMP.json"
}

# Database restore
restore_database() {
    local backup_file=$1
    
    if [ -z "$backup_file" ]; then
        echo "❌ Backup dosyası belirtilmedi"
        echo "Kullanım: restore_database <backup_dosyası>"
        return 1
    fi
    
    echo "🔄 Database restore işlemi: $backup_file"
    
    # JSON data restore
    if [[ "$backup_file" == *.json ]]; then
        python manage.py loaddata "$backup_file"
        echo "✅ JSON data restore tamamlandı"
    fi
    
    # SQL restore
    if [[ "$backup_file" == *.sql ]]; then
        psql context7_erp < "$backup_file"
        echo "✅ SQL restore tamamlandı"
    fi
    
    # SQLite restore
    if [[ "$backup_file" == *.sqlite3 ]]; then
        cp "$backup_file" db.sqlite3
        echo "✅ SQLite restore tamamlandı"
    fi
}

# =============================
# 5. SSL CERTIFICATE SETUP
# =============================

# Let's Encrypt SSL kurulumu
setup_ssl_certificate() {
    echo "🔒 SSL Certificate kurulumu..."
    
    # Certbot kurulumu
    sudo apt update
    sudo apt install certbot python3-certbot-nginx -y
    
    # SSL certificate alma
    sudo certbot --nginx -d context7.example.com
    
    # Auto-renewal setup
    sudo crontab -l | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -
    
    echo "✅ SSL Certificate kuruldu"
}

# =============================
# 6. MONITORING VE LOGS
# =============================

# Log monitoring
monitor_logs() {
    echo "📊 Log monitoring başlatılıyor..."
    
    # Django logs
    echo "🔍 Django logs:"
    tail -f logs/django_info.log &
    
    # Nginx logs
    echo "🔍 Nginx logs:"
    sudo tail -f /var/log/nginx/access.log &
    
    # System logs
    echo "🔍 System logs:"
    sudo journalctl -u context7 -f &
    
    echo "📊 Log monitoring aktif (Ctrl+C ile durdur)"
    wait
}

# System status check
check_system_status() {
    echo "🔍 Sistem durumu kontrol ediliyor..."
    
    # Service status
    echo "📋 Service durumları:"
    sudo systemctl status context7 --no-pager
    sudo systemctl status nginx --no-pager
    
    # Disk usage
    echo "💾 Disk kullanımı:"
    df -h
    
    # Memory usage
    echo "🧠 Memory kullanımı:"
    free -h
    
    # CPU usage
    echo "⚡ CPU kullanımı:"
    top -bn1 | grep "Cpu(s)"
    
    # Network status
    echo "🌐 Network durumu:"
    ss -tulpn | grep :8000
    
    echo "✅ Sistem durumu kontrol tamamlandı"
}

# =============================
# 7. PERFORMANCE OPTIMIZATION
# =============================

# Cache clear
clear_cache() {
    echo "🧹 Cache temizleme işlemi..."
    
    # Redis cache clear
    if command -v redis-cli &> /dev/null; then
        redis-cli FLUSHALL
        echo "✅ Redis cache temizlendi"
    fi
    
    # Django cache clear
    python manage.py clear_cache
    echo "✅ Django cache temizlendi"
    
    # Browser cache headers
    sudo systemctl reload nginx
    echo "✅ Nginx cache headers güncellendi"
}

# Database optimization
optimize_database() {
    echo "⚡ Database optimizasyon işlemi..."
    
    # PostgreSQL vacuum
    if command -v psql &> /dev/null; then
        psql context7_erp -c "VACUUM ANALYZE;"
        echo "✅ PostgreSQL vacuum tamamlandı"
    fi
    
    # SQLite optimize
    if [ -f "db.sqlite3" ]; then
        echo "VACUUM;" | sqlite3 db.sqlite3
        echo "✅ SQLite optimize tamamlandı"
    fi
    
    echo "✅ Database optimizasyon tamamlandı"
}

# =============================
# 8. MAIN DEPLOYMENT FUNCTION
# =============================

# Full deployment
full_deployment() {
    echo "🚀 Context7 ERP Full Deployment Başlıyor..."
    echo "========================================"
    
    # Pre-deployment checks
    echo "1️⃣ Pre-deployment kontrolleri..."
    check_system_status
    
    # Backup
    echo "2️⃣ Backup oluşturuluyor..."
    backup_database
    
    # Code update
    echo "3️⃣ Kod güncelleniyor..."
    update_codebase
    
    # Dependencies
    echo "4️⃣ Dependencies güncelleniyor..."
    setup_virtualenv
    
    # Database
    echo "5️⃣ Database migration..."
    run_migrations
    
    # Static files
    echo "6️⃣ Static files..."
    collect_static
    
    # Cache clear
    echo "7️⃣ Cache temizleniyor..."
    clear_cache
    
    # Performance optimization
    echo "8️⃣ Performance optimizasyon..."
    optimize_database
    
    # Service restart
    echo "9️⃣ Servisler restart ediliyor..."
    sudo systemctl restart context7
    sudo systemctl restart nginx
    
    # Post-deployment checks
    echo "🔟 Post-deployment kontrolleri..."
    sleep 5
    check_system_status
    
    echo "🎉 Full Deployment Tamamlandı!"
    echo "🌐 Sistem aktif: http://31.97.44.248:8000"
}

# =============================
# 9. USAGE INSTRUCTIONS
# =============================

show_usage() {
    echo "📖 Context7 ERP Deployment Scripts Kullanım Kılavuzu"
    echo "=================================================="
    echo ""
    echo "🚀 Deployment Komutları:"
    echo "  full_deployment           - Tam deployment işlemi"
    echo "  deploy_to_hostinger       - Hostinger'a deployment"
    echo "  deploy_with_docker        - Docker ile deployment"
    echo ""
    echo "💾 Database İşlemleri:"
    echo "  backup_database           - Database backup"
    echo "  restore_database <file>   - Database restore"
    echo "  optimize_database         - Database optimizasyon"
    echo ""
    echo "🔧 Sistem İşlemleri:"
    echo "  update_codebase           - Kod güncelleme"
    echo "  run_migrations            - Database migration"
    echo "  collect_static            - Static files toplama"
    echo "  clear_cache               - Cache temizleme"
    echo ""
    echo "📊 Monitoring:"
    echo "  monitor_logs              - Log monitoring"
    echo "  check_system_status       - Sistem durumu"
    echo ""
    echo "🔒 SSL:"
    echo "  setup_ssl_certificate     - SSL kurulumu"
    echo ""
    echo "Örnek kullanım:"
    echo "  bash deployment-commands.sh"
    echo "  source deployment-commands.sh && full_deployment"
}

# Script direkt çalıştırıldığında usage göster
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_usage
fi 