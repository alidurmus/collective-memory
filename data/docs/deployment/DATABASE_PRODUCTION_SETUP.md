# 🗄️ **DATABASE PRODUCTION SETUP GUIDE - ÖNCELİK #2**

## 📅 **SETUP PLAN**
**Başlangıç**: 16 Ocak 2024  
**Hedef Tamamlama**: 20 Ocak 2024 (4 gün)  
**Mevcut Durum**: SQLite Development → PostgreSQL Production

---

## ✅ **4 GÜNLÜK DATABASE SETUP ADIMLAR**

### **GÜN 1: PostgreSQL Installation & Configuration**

#### 🐘 **1. PostgreSQL Installation (Ubuntu/Debian)**
```bash
# System update
sudo apt update && sudo apt upgrade -y

# PostgreSQL installation
sudo apt install postgresql postgresql-contrib postgresql-client -y

# PostgreSQL service management
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql

# Version verification
psql --version
```

#### 🔧 **2. PostgreSQL Initial Configuration**
```bash
# Switch to postgres user
sudo -i -u postgres

# Access PostgreSQL prompt
psql

# Create production database and user
CREATE DATABASE erp_production;
CREATE USER erp_user WITH PASSWORD 'your-strong-password-here';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE erp_production TO erp_user;
ALTER USER erp_user CREATEDB;

# Exit psql
\q

# Exit postgres user
exit
```

#### 🔒 **3. PostgreSQL Security Configuration**
```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/*/main/postgresql.conf

# Key settings to modify:
listen_addresses = 'localhost'          # Restrict to localhost for security
max_connections = 100                   # Adjust based on your needs
shared_buffers = 256MB                  # 25% of RAM for small systems
effective_cache_size = 1GB              # 75% of RAM

# Edit authentication configuration
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Add line for local connections (replace existing local line):
local   all             erp_user                                md5
host    erp_production  erp_user        127.0.0.1/32           md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### **GÜN 2: Database Migration & Data Transfer**

#### 📦 **4. Install Production Database Dependencies**
```bash
# Python PostgreSQL adapter
pip install psycopg2-binary

# Database URL parser
pip install dj-database-url

# Update requirements.txt
echo "psycopg2-binary==2.9.9" >> requirements.txt
echo "dj-database-url==3.0.0" >> requirements.txt
```

#### 🔄 **5. Create Production Environment File**
```bash
# Create production .env file
cat > .env.production << 'EOF'
# Database Production Configuration
DEBUG=False
SECRET_KEY=your-production-secret-key-change-this-50-chars-minimum
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# PostgreSQL Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_production
DB_USER=erp_user
DB_PASSWORD=your-strong-password-here
DB_HOST=localhost
DB_PORT=5432
DATABASE_URL=postgresql://erp_user:your-strong-password-here@localhost:5432/erp_production

# Redis Configuration
REDIS_URL=redis://localhost:6379/1

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-app-password

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
EOF
```

#### 🚀 **6. Database Migration to Production**
```bash
# Test database connection
python manage.py dbshell --settings=dashboard_project.production_settings_simple

# Run migrations with production settings
python manage.py migrate --settings=dashboard_project.production_settings_simple

# Create superuser for production
python manage.py createsuperuser --settings=dashboard_project.production_settings_simple

# Load sample data (optional)
python manage.py loaddata sample_data.json --settings=dashboard_project.production_settings_simple
```

### **GÜN 3: Database Optimization & Performance**

#### ⚡ **7. Database Performance Optimization**
```sql
-- Connect to production database
psql -U erp_user -d erp_production

-- Create indexes for frequently queried fields
CREATE INDEX idx_erp_product_code ON erp_product(code);
CREATE INDEX idx_erp_product_name ON erp_product(name);
CREATE INDEX idx_erp_product_status ON erp_product(status);
CREATE INDEX idx_erp_salesorder_customer ON erp_salesorder(customer_id);
CREATE INDEX idx_erp_salesorder_date ON erp_salesorder(order_date);
CREATE INDEX idx_erp_salesorder_status ON erp_salesorder(status);
CREATE INDEX idx_erp_purchaseorder_supplier ON erp_purchaseorder(supplier_id);
CREATE INDEX idx_erp_purchaseorder_date ON erp_purchaseorder(order_date);
CREATE INDEX idx_erp_inventory_product ON erp_inventory(product_id);
CREATE INDEX idx_erp_inventory_location ON erp_inventory(location);

-- Analyze tables for query optimization
ANALYZE;

-- Exit psql
\q
```

#### 📊 **8. Database Monitoring Setup**
```bash
# Install database monitoring tools
sudo apt install postgresql-contrib

# Create monitoring script
cat > monitor_db.sh << 'EOF'
#!/bin/bash
echo "=== PostgreSQL Database Status ==="
sudo systemctl status postgresql --no-pager
echo ""

echo "=== Database Connections ==="
sudo -u postgres psql -c "SELECT count(*) as active_connections FROM pg_stat_activity WHERE state = 'active';"
echo ""

echo "=== Database Size ==="
sudo -u postgres psql -c "SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname)) AS size FROM pg_database;"
echo ""

echo "=== Top 5 Largest Tables ==="
sudo -u postgres psql -d erp_production -c "SELECT schemaname,tablename,attname,n_distinct,correlation FROM pg_stats WHERE schemaname = 'public' ORDER BY n_distinct DESC LIMIT 5;"
EOF

chmod +x monitor_db.sh
```

### **GÜN 4: Backup Strategy & Recovery**

#### 💾 **9. Automated Backup System**
```bash
# Create backup directory
sudo mkdir -p /var/backups/erp
sudo chown postgres:postgres /var/backups/erp

# Create backup script
sudo tee /usr/local/bin/backup_erp_db.sh << 'EOF'
#!/bin/bash

# Configuration
DB_NAME="erp_production"
DB_USER="erp_user"
BACKUP_DIR="/var/backups/erp"
DATE=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=7

# Create backup
pg_dump -U $DB_USER -h localhost $DB_NAME | gzip > $BACKUP_DIR/erp_backup_$DATE.sql.gz

# Log backup
echo "$(date): Backup completed - erp_backup_$DATE.sql.gz" >> $BACKUP_DIR/backup.log

# Remove old backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Check backup size
BACKUP_SIZE=$(du -h $BACKUP_DIR/erp_backup_$DATE.sql.gz | cut -f1)
echo "$(date): Backup size: $BACKUP_SIZE" >> $BACKUP_DIR/backup.log

# Verify backup integrity
if gzip -t $BACKUP_DIR/erp_backup_$DATE.sql.gz; then
    echo "$(date): Backup integrity verified" >> $BACKUP_DIR/backup.log
else
    echo "$(date): ERROR - Backup integrity check failed!" >> $BACKUP_DIR/backup.log
    exit 1
fi
EOF

# Make script executable
sudo chmod +x /usr/local/bin/backup_erp_db.sh

# Test backup script
sudo -u postgres /usr/local/bin/backup_erp_db.sh
```

#### 📅 **10. Schedule Automated Backups**
```bash
# Add to postgres user crontab
sudo -u postgres crontab -e

# Add these lines:
# Daily backup at 2:00 AM
0 2 * * * /usr/local/bin/backup_erp_db.sh

# Weekly full backup on Sunday at 1:00 AM
0 1 * * 0 /usr/local/bin/backup_erp_db.sh

# Verify crontab
sudo -u postgres crontab -l
```

---

## 🧪 **DATABASE PRODUCTION TESTING**

### 📊 **Performance Tests**
```bash
# Database connection test
python manage.py dbshell --settings=dashboard_project.production_settings_simple

# Migration verification
python manage.py showmigrations --settings=dashboard_project.production_settings_simple

# Database size check
du -h db.sqlite3  # Old SQLite database
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('erp_production'));"

# Performance test with sample queries
python manage.py shell --settings=dashboard_project.production_settings_simple
```

### 🔍 **Python Performance Test Script**
```python
# Create test_db_performance.py
import time
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.production_settings_simple')
django.setup()

from erp.models import Product, Customer, SalesOrder
from django.db import connection

def test_query_performance():
    print("=== Database Performance Test ===")
    
    # Test 1: Product queries
    start_time = time.time()
    products = list(Product.objects.all()[:100])
    end_time = time.time()
    print(f"Product query (100 records): {end_time - start_time:.4f} seconds")
    
    # Test 2: Complex join query
    start_time = time.time()
    orders = list(SalesOrder.objects.select_related('customer').prefetch_related('items')[:50])
    end_time = time.time()
    print(f"Sales order with joins (50 records): {end_time - start_time:.4f} seconds")
    
    # Test 3: Database connection info
    print(f"Database vendor: {connection.vendor}")
    print(f"Database version: {connection.pg_version if hasattr(connection, 'pg_version') else 'N/A'}")
    
    # Test 4: Query count
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
        table_count = cursor.fetchone()[0]
        print(f"Number of tables: {table_count}")

if __name__ == "__main__":
    test_query_performance()
```

---

## 📋 **DATABASE MIGRATION CHECKLIST**

### ✅ **Pre-Migration Checklist**
- [ ] **PostgreSQL Installed**: Version 12+ installed and running
- [ ] **Database Created**: `erp_production` database created
- [ ] **User Created**: `erp_user` with appropriate permissions
- [ ] **Backup Created**: SQLite database backed up
- [ ] **Dependencies Installed**: `psycopg2-binary`, `dj-database-url`

### ✅ **Migration Checklist**
- [ ] **Settings Updated**: Production settings configured
- [ ] **Migrations Run**: All Django migrations applied
- [ ] **Superuser Created**: Admin user created for production
- [ ] **Sample Data Loaded**: Test data loaded (optional)
- [ ] **Indexes Created**: Performance indexes applied

### ✅ **Post-Migration Checklist**
- [ ] **Performance Tested**: Query performance verified
- [ ] **Backup Tested**: Backup script working
- [ ] **Monitoring Setup**: Database monitoring configured
- [ ] **Cron Jobs**: Automated backups scheduled
- [ ] **Documentation Updated**: Database credentials documented

---

## 🚨 **TROUBLESHOOTING GUIDE**

### ❌ **Common Issues & Solutions**

#### **Issue 1: Connection Refused**
```bash
# Solution: Check PostgreSQL service
sudo systemctl status postgresql
sudo systemctl restart postgresql

# Check port availability
netstat -tlnp | grep 5432
```

#### **Issue 2: Authentication Failed**
```bash
# Solution: Check pg_hba.conf
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Ensure md5 authentication is enabled for erp_user

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### **Issue 3: Migration Errors**
```bash
# Solution: Check migration dependencies
python manage.py showmigrations --settings=dashboard_project.production_settings_simple

# Apply specific migration
python manage.py migrate app_name migration_number --settings=dashboard_project.production_settings_simple
```

#### **Issue 4: Performance Issues**
```sql
-- Solution: Check slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- Rebuild indexes
REINDEX DATABASE erp_production;
```

---

## 📊 **DATABASE MONITORING DASHBOARD**

### 📈 **Key Metrics to Monitor**
```sql
-- Database size monitoring
SELECT 
    pg_database.datname, 
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size,
    pg_database_size(pg_database.datname) as size_bytes
FROM pg_database 
WHERE datname = 'erp_production';

-- Connection monitoring
SELECT 
    count(*) as total_connections,
    count(*) FILTER (WHERE state = 'active') as active_connections,
    count(*) FILTER (WHERE state = 'idle') as idle_connections
FROM pg_stat_activity;

-- Table size monitoring
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 🎯 **SUCCESS CRITERIA**

### 📊 **Database Performance Targets**
- [ ] **Query Response Time**: <100ms for simple queries
- [ ] **Connection Time**: <1 second
- [ ] **Backup Time**: <5 minutes for full backup
- [ ] **Recovery Time**: <10 minutes for full restore

### 🔒 **Security Targets**
- [ ] **Access Control**: Only authorized users can connect
- [ ] **Encryption**: SSL connections enabled
- [ ] **Backup Security**: Backups encrypted and secured
- [ ] **Audit Logging**: All database activities logged

### 💾 **Backup Targets**
- [ ] **Backup Frequency**: Daily automated backups
- [ ] **Backup Retention**: 7 days minimum
- [ ] **Backup Verification**: Automated integrity checks
- [ ] **Recovery Testing**: Monthly recovery tests

---

**📅 Timeline**: 4 gün  
**👥 Sorumlu**: Database Admin + Development Team  
**🎯 Başarı Kriteri**: PostgreSQL production database fully operational  
**📞 Support**: Database monitoring active 

## 📋 **BAŞLANGIÇ ADIMI: Windows'ta PostgreSQL Test**

Windows'ta test edebilmek için önce PostgreSQL kurulumu yapalım: 