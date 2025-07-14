# 🛠️ Context7 ERP Utilities

Django ERP System için yardımcı araçlar ve scriptler.

## 📋 İçindekiler

### 🗄️ PostgreSQL Yönetimi
- **postgresql_manager.py** - PostgreSQL veritabanı yönetim aracı

### 🧹 Sistem Bakımı  
- **clean_logs.py** - Log dosyalarını temizleme aracı
- **debug_*.py** - Sistem hata ayıklama scriptleri

### 📊 Monitoring
- **todo_progress_checker.py** - TODO item progress tracking

## 🚀 Kullanım

### PostgreSQL Yönetimi

```bash
# Tüm kontrolleri çalıştır
python utilities/postgresql_manager.py

# Bağlantı testi
python utilities/postgresql_manager.py test

# Veritabanı istatistikleri
python utilities/postgresql_manager.py stats

# Performans analizi
python utilities/postgresql_manager.py performance

# Backup al
python utilities/postgresql_manager.py backup

# Veritabanı optimizasyonu
python utilities/postgresql_manager.py optimize

# Docker konteyner durumu
python utilities/postgresql_manager.py docker
```

### Log Temizleme

```bash
# Log dosyalarını temizle
python utilities/clean_logs.py
```

### TODO Progress Tracking

```bash
# TODO progress kontrolü
python utilities/todo_progress_checker.py
```

## 📊 PostgreSQL Manager Özellikleri

### ✅ Bağlantı Testi
- PostgreSQL bağlantı durumu
- Version bilgisi
- Server detayları
- Aktif bağlantı sayısı

### 📈 Veritabanı İstatistikleri
- Veritabanı boyutu
- Tablo sayısı
- ERP tablolarının boyutları
- Aktif bağlantı bilgileri

### 🚀 Performans Analizi
- Yavaş sorgu analizi
- Index kullanım önerileri
- Query performance metrics

### 💾 Backup Özellikleri
- Otomatik timestamp ile backup
- Docker container üzerinden pg_dump
- Backup boyut raporlama
- Organized backup directory

### 🧹 Optimizasyon
- VACUUM ANALYZE işlemleri
- İstatistik güncellemeleri
- Performance tuning

## 🐳 Docker Entegrasyonu

Tüm PostgreSQL işlemleri Docker container üzerinden çalışır:

```bash
# Container durumu
docker ps

# PostgreSQL health check
docker exec -it postgres-erp pg_isready -U postgres -d erp_db

# Direct SQL access
docker exec -it postgres-erp psql -U postgres -d erp_db
```

## 📁 Backup Yönetimi

### Backup Konumları
```
backups/
├── database/
│   ├── postgresql_backup_YYYYMMDD_HHMMSS.sql
│   └── ...
└── media/
```

### Backup Restoration

```bash
# Backup restore
docker exec -i postgres-erp psql -U postgres -d erp_db < backups/database/postgresql_backup_20250610_195901.sql
```

## 🔧 Konfigürasyon

### Environment Variables
```env
POSTGRES_DB=erp_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Docker Compose
```yaml
services:
  postgres-erp:
    image: postgres:15
    container_name: postgres-erp
    environment:
      POSTGRES_DB: erp_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 📊 Monitoring & Alerting

### Performance Metrics
- Query execution time
- Connection counts  
- Database size growth
- Table size statistics

### Health Checks
- Connection availability
- Response time monitoring
- Resource usage tracking

## 🔐 Güvenlik

### Backup Security
- Encrypted backup files
- Access control lists
- Retention policies
- Secure transmission

### Connection Security
- SSL/TLS encryption
- Password protection
- IP restrictions
- Connection pooling

## 🚨 Troubleshooting

### Yaygın Sorunlar

#### Connection Refused
```bash
# Docker container'ı kontrol et
docker ps
docker restart postgres-erp

# Port kontrolü
netstat -an | findstr 5432
```

#### Memory Issues
```bash
# PostgreSQL logs
docker logs postgres-erp

# Container resource usage
docker stats postgres-erp
```

#### Backup Failures
```bash
# Disk space kontrolü
df -h

# Permission kontrolü
ls -la backups/database/
```

## 📝 Best Practices

### Regular Maintenance
1. **Daily**: Connection health checks
2. **Weekly**: Performance analysis
3. **Monthly**: Full backup verification
4. **Quarterly**: Optimization review

### Monitoring
1. Database size trends
2. Query performance metrics
3. Connection pool utilization
4. Backup success rates

### Security
1. Regular password rotation
2. Access log monitoring
3. Backup encryption
4. Network security

## 🔗 İlgili Belgeler

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker PostgreSQL Guide](https://hub.docker.com/_/postgres)
- [Django Database Documentation](https://docs.djangoproject.com/en/stable/ref/databases/)

## 🤝 Katkıda Bulunma

1. Script'leri test edin
2. Hata raporları gönderin
3. İyileştirme önerileri yapın
4. Dokümantasyonu güncelleyin

---

**Context7 ERP System** - Professional Database Management Tools 