# 🔄 Context7 ERP - Çoklu Server Cache Yönetim Rehberi

**Tarih:** 21 Haziran 2025  
**Proje:** Django ERP System v2.2.0-glassmorphism-enhanced  
**Durum:** ✅ Multi-Server Cache Strategy Implemented

## 🎯 **Özet**
Chat uygulaması ve diğer real-time özellikleri için çoklu Django server kullanımında cache çakışmalarını önleyen kapsamlı çözüm rehberi.

## ⚠️ **ÇOKLU SERVER CACHE PROBLEMLERİ**

### **🚨 Ana Problemler:**

1. **Database Lock Conflicts**
   ```
   ❌ Aynı SQLite dosyasına birden çok server erişimi
   ❌ Concurrent write operations
   ❌ Database corruption riski
   ```

2. **Cache Key Collisions**
   ```
   ❌ Aynı cache key'leri farklı server'lar kullanır
   ❌ Data inconsistency
   ❌ Outdated cache data
   ```

3. **Session Mixups**
   ```
   ❌ User session'ları karışır
   ❌ Authentication problemleri
   ❌ Security risks
   ```

4. **Static Files Conflicts**
   ```
   ❌ Concurrent static file generation
   ❌ File lock issues
   ❌ Asset corruption
   ```

## 🛡️ **CONTEXT7 ÇÖZÜMLERİ**

### **1. Server Instance Isolation**

```bash
# Her server için benzersiz identifier
export DJANGO_SERVER_INSTANCE="chat_main"
export DJANGO_SERVER_PORT="8000"
export DJANGO_SETTINGS_MODULE="dashboard_project.multi_server_settings"
```

### **2. Database Separation**

```python
# Her server için ayrı database
DATABASE_NAME = f'db_{SERVER_INSTANCE}.sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / DATABASE_NAME,  # ✅ Isolated per instance
        'OPTIONS': {
            'timeout': 20,
            'isolation_level': None,
        }
    }
}
```

### **3. Cache Isolation**

```python
# Redis ile proper isolation
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
        'KEY_PREFIX': f'context7_{SERVER_INSTANCE}',  # ✅ Isolated keys
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Local memory cache (development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': f'context7-cache-{SERVER_INSTANCE}',  # ✅ Isolated
    }
}
```

### **4. Session Security**

```python
# Session isolation
SESSION_COOKIE_NAME = f'sessionid_{SERVER_INSTANCE}'  # ✅ Unique cookies
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### **5. Static Files Separation**

```python
# Per-instance static files
STATIC_ROOT = BASE_DIR / f'staticfiles_{SERVER_INSTANCE}'
MEDIA_ROOT = BASE_DIR / f'media_{SERVER_INSTANCE}'
```

## 🚀 **MULTI-SERVER BAŞLATMA**

### **Chat Uygulaması için:**

```bash
# Method 1: Script ile
python scripts/start_multi_server.py start-chat

# Method 2: Manuel
DJANGO_SERVER_INSTANCE=chat_main DJANGO_SERVER_PORT=8000 python manage.py runserver 127.0.0.1:8000 --settings=dashboard_project.multi_server_settings

DJANGO_SERVER_INSTANCE=chat_api DJANGO_SERVER_PORT=8001 python manage.py runserver 127.0.0.1:8001 --settings=dashboard_project.multi_server_settings

DJANGO_SERVER_INSTANCE=chat_websocket DJANGO_SERVER_PORT=8002 python manage.py runserver 127.0.0.1:8002 --settings=dashboard_project.multi_server_settings
```

### **Development için:**

```bash
# 2 server ile test
python scripts/start_multi_server.py start-dev
```

## 📊 **CACHE MONITORING**

### **Health Check Endpoints:**

```bash
# Her server için health check
curl http://127.0.0.1:8000/health/  # chat_main
curl http://127.0.0.1:8001/health/  # chat_api  
curl http://127.0.0.1:8002/health/  # chat_websocket
```

### **Cache Status Monitoring:**

```python
# Multi-server cache durumu
def check_multi_server_cache():
    for instance in ['chat_main', 'chat_api', 'chat_websocket']:
        cache_key = f'health_check_{instance}'
        status = cache.get(cache_key)
        print(f"Instance {instance}: {status}")
```

## 🔧 **CACHE TEMIZLEME STRATEJİLERİ**

### **1. Per-Instance Cache Clear:**

```bash
# Sadece belirli bir instance'ın cache'ini temizle
DJANGO_SERVER_INSTANCE=chat_main python manage.py clear_cache --type=all

# Veya web arayüzünden
http://127.0.0.1:8000/settings/ → Cache Temizle
```

### **2. Global Cache Clear:**

```bash
# Tüm instance'ların cache'lerini temizle
for instance in chat_main chat_api chat_websocket; do
    DJANGO_SERVER_INSTANCE=$instance python manage.py clear_cache --type=all
done
```

### **3. Redis Cache Clear:**

```bash
# Redis'teki tüm Context7 cache'lerini temizle
redis-cli --scan --pattern "context7_*" | xargs redis-cli del
```

## 📈 **PERFORMANS OPTİMİZASYONLARI**

### **Database Connection Pooling:**

```python
# PostgreSQL ile production setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': f'context7_erp_{SERVER_INSTANCE}',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'options': f'-c application_name=context7_{SERVER_INSTANCE}'
        },
    }
}
```

### **Cache Strategies:**

| Instance | Cache Strategy | Timeout | Purpose |
|----------|---------------|---------|---------|
| `chat_main` | Redis + LocMem | 1 hour | Main app data |
| `chat_api` | Redis | 30 min | API responses |
| `chat_websocket` | Redis | 5 min | Real-time data |

### **Load Balancing:**

```nginx
# Nginx configuration for load balancing
upstream context7_chat {
    server 127.0.0.1:8000 weight=3;  # Main app
    server 127.0.0.1:8001 weight=2;  # API
    server 127.0.0.1:8002 weight=1;  # WebSocket
}
```

## 🛠️ **TROUBLESHOOTİNG**

### **Problem: Cache Key Collisions**

```bash
# Çözüm: Key prefix kontrolü
redis-cli --scan --pattern "context7_chat_main:*"
redis-cli --scan --pattern "context7_chat_api:*"

# Her instance farklı prefix kullanmalı
```

### **Problem: Database Lock Issues**

```bash
# Çözüm: Database file kontrolü
ls -la db_*.sqlite3

# Her instance'ın kendi database'i olmalı:
# db_chat_main.sqlite3
# db_chat_api.sqlite3
# db_chat_websocket.sqlite3
```

### **Problem: Session Conflicts**

```bash
# Çözüm: Cookie name kontrolü
# Browser Developer Tools → Application → Cookies
# Farklı cookie names olmalı:
# sessionid_chat_main
# sessionid_chat_api
# sessionid_chat_websocket
```

## ⚡ **BEst PRACTİCES**

### **1. Development:**
- ✅ DummyCache ile development
- ✅ Separate SQLite per instance
- ✅ Different ports (8000, 8001, 8002)
- ✅ Instance-specific logs

### **2. Production:**
- ✅ Redis ile shared cache (isolated keys)
- ✅ PostgreSQL ile proper database
- ✅ Load balancer ile traffic distribution
- ✅ Health checks ve monitoring

### **3. Security:**
- ✅ CSRF token isolation
- ✅ Session cookie isolation
- ✅ Secret key per instance
- ✅ Access log separation

## 🎯 **SONUÇ**

**✅ Çoklu server cache problemleri Context7 çözümleri ile tamamen önlenebilir:**

1. **Server Instance Isolation** → Her server benzersiz identifier
2. **Database Separation** → Per-instance database files
3. **Cache Key Prefixing** → Isolated cache namespaces
4. **Session Security** → Unique cookie names
5. **Static Files Separation** → Per-instance directories

**🚀 Chat uygulaması artık güvenle çoklu server ile çalışabilir!** 