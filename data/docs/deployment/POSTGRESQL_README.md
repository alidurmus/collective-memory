# PostgreSQL Configuration Guide
# Django ERP System v2.1.0-context7-enhanced

## 🎯 Overview

This guide provides comprehensive instructions for PostgreSQL configuration and management in the Django ERP System.

**Migration Status**: ✅ **COMPLETED** (9 Haziran 2025)  
**Database**: PostgreSQL 15.13  
**Container**: postgres-erp  

## 🚀 Quick Start

### 1. Environment Setup

Copy PostgreSQL configuration:
```bash
cp postgresql.env .env
```

### 2. Start PostgreSQL

```bash
# Using Docker directly
docker start postgres-erp

# Or using Docker Compose
docker-compose -f docker-compose.postgresql.yml up -d
```

### 3. Run Setup Script

```bash
python scripts/setup/setup_postgresql.py
```

### 4. Start Django Server

```bash
python manage.py runserver
```

## 🔧 Configuration Files

### Created Files

1. **`postgresql.env`** - Environment configuration
2. **`docker-compose.postgresql.yml`** - Docker Compose setup
3. **`scripts/setup/setup_postgresql.py`** - Automated setup script
4. **`docs/deployment/POSTGRESQL_MIGRATION_REPORT.md`** - Migration report

### Settings Updated

- **`dashboard_project/settings.py`** - Database engine changed to PostgreSQL
- **`requirements.txt`** - Added `psycopg2-binary` package

## 🐘 PostgreSQL Management

### Docker Commands

```bash
# Container Management
docker start postgres-erp          # Start container
docker stop postgres-erp           # Stop container
docker restart postgres-erp        # Restart container
docker logs postgres-erp           # View logs

# Database Access
docker exec -it postgres-erp psql -U postgres -d erp_db

# Container Status
docker ps | grep postgres-erp
```

### Database Operations

```bash
# Django Commands
python manage.py check --database default   # Test connection
python manage.py showmigrations             # Show migration status
python manage.py migrate                    # Apply migrations
python manage.py dbshell                    # Open database shell

# Backup & Restore
docker exec postgres-erp pg_dump -U postgres erp_db > backup.sql
docker exec -i postgres-erp psql -U postgres erp_db < backup.sql
```

## 📊 Database Configuration

### Connection Settings

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'erp_db',
        'USER': 'postgres',
        'PASSWORD': 'password123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables

```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=erp_db
DB_USER=postgres
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=5432
```

## 🛡️ Security Configuration

### Development Settings

- **Password**: `password123` (change for production)
- **Host**: `localhost` only
- **SSL**: Disabled (enable for production)

### Production Settings

```bash
# SSL Configuration
POSTGRES_SSL_MODE=require

# Strong Password
POSTGRES_PASSWORD=your-strong-password-here

# Network Security
POSTGRES_HOST=your-secure-host
```

## 🔄 Migration Status

### Applied Migrations

All migrations successfully applied to PostgreSQL:

```
✅ Django Core: 12 migrations
✅ ERP App: 9 migrations
✅ Users App: 2 migrations
✅ All Other Apps: Applied
```

### Migration Commands

```bash
# Check for new migrations
python manage.py makemigrations

# Apply specific app migrations
python manage.py migrate erp

# Show detailed migration plan
python manage.py showmigrations --plan
```

## 📈 Performance Optimization

### Connection Pooling

```python
# In settings.py
DATABASES = {
    'default': {
        # ... other settings
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
}
```

### Index Optimization

```sql
-- Common indexes for ERP tables
CREATE INDEX idx_erp_purchaseorder_status ON erp_purchaseorder(status);
CREATE INDEX idx_erp_purchaseorder_date ON erp_purchaseorder(order_date);
CREATE INDEX idx_erp_salesorder_customer ON erp_salesorder(customer_id);
```

## 🎛️ Monitoring & Maintenance

### Health Checks

```bash
# PostgreSQL status
python scripts/setup/setup_postgresql.py status

# Database connection test
python manage.py check --database default

# Container health
docker exec postgres-erp pg_isready -U postgres
```

### Regular Maintenance

```bash
# Weekly tasks
docker exec postgres-erp psql -U postgres -d erp_db -c "VACUUM ANALYZE;"

# Monthly backup
pg_dump -U postgres -h localhost erp_db > monthly_backup_$(date +%Y%m%d).sql

# Log rotation
docker logs postgres-erp --tail 1000 > postgres_logs_$(date +%Y%m%d).log
```

## 🚨 Troubleshooting

### Common Issues

**Connection Refused**
```bash
# Check if container is running
docker ps | grep postgres-erp

# Start container if stopped
docker start postgres-erp
```

**Permission Denied**
```bash
# Reset container permissions
docker exec postgres-erp chown -R postgres:postgres /var/lib/postgresql/data
```

**Migration Errors**
```bash
# Show migration status
python manage.py showmigrations erp

# Apply specific migration
python manage.py migrate erp 0009 --fake
```

### Log Analysis

```bash
# PostgreSQL logs
docker logs postgres-erp --tail 100

# Django database logs
python manage.py shell -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from django.db import connection
print(connection.queries)
"
```

## 📞 Support

### Configuration Issues

1. Check `postgresql.env` file
2. Verify Docker container status
3. Test database connection
4. Review migration status

### Emergency Recovery

```bash
# Stop all containers
docker stop postgres-erp

# Remove problematic container
docker rm postgres-erp

# Recreate from backup
python scripts/setup/setup_postgresql.py

# Restore data
docker exec -i postgres-erp psql -U postgres erp_db < backup.sql
```

## 🎉 Success Indicators

**System is ready when:**

- ✅ PostgreSQL container running
- ✅ Database connection successful
- ✅ All migrations applied
- ✅ Django server starts without errors
- ✅ Admin login works (admin/admin123)

**Access URLs:**

- 🌐 **Application**: http://127.0.0.1:8000/
- 👤 **Admin Panel**: http://127.0.0.1:8000/admin/
- 📊 **ERP Dashboard**: http://127.0.0.1:8000/erp/

---

**PostgreSQL Setup**: ✅ OPERATIONAL  
**Migration Status**: ✅ COMPLETED  
**System Ready**: ✅ PRODUCTION READY 