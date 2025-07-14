# 🚀 Context7 ERP - Kapsamlı Kurulum Klavuzu

**Repository**: https://github.com/alidurmus/python-dashboard.git

## 📋 **Genel Bilgiler**

**Proje**: Context7 Django ERP System  
**Versiyon**: v2.2.0-glassmorphism-enhanced + QMS Integration + Modern Python Standards + SSL Implementation + Email System ⭐  
**Durum**: ✅ **PRODUCTION DEPLOYED** (100% Complete)  
**Son Güncelleme**: 13 Temmuz 2025  
**Live Demo**: http://31.97.44.248:8000  

---

## 🎉 **Başarılı Deployment - Live System**

Context7 ERP sistemi başarıyla Hostinger VPS'e deploy edildi ve şu anda canlıda çalışıyor!

### 🌐 **Canlı Sistem Bilgileri**
```bash
🔗 Ana Site: http://31.97.44.248:8000
🔐 Giriş Sayfası: http://31.97.44.248:8000/accounts/login/
👤 Admin Panel: http://31.97.44.248:8000/admin/
📊 API: http://31.97.44.248:8000/api/v1/

Server: Hostinger VPS (srv858543.hstgr.cloud)
IP: 31.97.44.248
Database: PostgreSQL (context7_erp)
Framework: Django 5.2.2 + Context7 Glassmorphism
Status: 🟢 ONLINE & OPERATIONAL
```

---

## 🛠️ **Kurulum Seçenekleri**

### **1. Yerel Development Kurulumu**
Geliştirme için bilgisayarınızda çalıştırma

### **2. Production VPS Kurulumu**
Hostinger VPS gibi sunucularda canlı sistem kurulumu

### **3. Docker Kurulumu**
Container tabanlı kurulum

### **4. Cloud Deployment**
AWS, Azure, Google Cloud kurulumları

---

## 💻 **1. Yerel Development Kurulumu**

### **Sistem Gereksinimleri**
```bash
✅ Python 3.11+ (Önerilen: 3.12)
✅ Git
✅ PostgreSQL 15+ (veya SQLite development için)
✅ Node.js 18+ (frontend tooling için)
✅ 4GB+ RAM
✅ 2GB+ disk alanı
```

### **Adım 1: Repository Clone**
```bash
# Repository'yi klonla
git clone https://github.com/alidurmus/python-dashboard.git
cd context7-erp

# Veya ZIP olarak indir ve çıkart
```

### **Adım 2: Virtual Environment**
```bash
# Windows
python -m venv context7_venv
context7_venv\Scripts\activate

# Linux/Mac
python3 -m venv context7_venv
source context7_venv/bin/activate
```

### **Adım 3: Dependencies**
```bash
# Python packages
pip install -r requirements.txt

# Development dependencies (opsiyonel)
pip install -r requirements_dev.txt
```

### **Adım 4: Environment Configuration**
```bash
# .env dosyası oluştur
cp .env.example .env

# .env dosyasını düzenle
nano .env
```

**Örnek .env dosyası:**
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL için
# DATABASE_URL=postgresql://user:password@localhost/context7_erp

# API Keys (opsiyonel)
OPENAI_API_KEY=your-openai-key
SENTRY_DSN=your-sentry-dsn
```

### **Adım 5: Database Setup**
```bash
# SQLite için (hızlı başlangıç)
python manage.py migrate
python manage.py loaddata sample_data/initial_data.json

# PostgreSQL için
# createdb context7_erp
# python manage.py migrate
```

### **Adım 6: Admin User**
```bash
# Superuser oluştur
python manage.py createsuperuser

# Username: admin
# Email: admin@context7.com
# Password: güçlü-şifre
```

### **Adım 7: Static Files**
```bash
# Static files topla
python manage.py collectstatic --noinput
```

### **Adım 8: Development Server**
```bash
# Server'ı başlat
python manage.py runserver

# Tarayıcıda aç: http://127.0.0.1:8000
```

### **Adım 9: İlk Giriş ve Test**
```bash
1. http://127.0.0.1:8000 adresine git
2. Admin hesabınla giriş yap
3. Dashboard'u incele
4. ERP modüllerini test et
5. API endpoints'leri test et: http://127.0.0.1:8000/api/v1/
```

---

## 🌐 **2. Production VPS Kurulumu**

### **VPS Gereksinimleri**

**Minimum:**
- CPU: 2 vCPU
- RAM: 4GB
- Storage: 40GB SSD
- OS: Ubuntu 22.04 LTS
- Bandwidth: 100GB

**Önerilen:**
- CPU: 4 vCPU
- RAM: 8GB
- Storage: 80GB NVMe SSD
- OS: Ubuntu 22.04 LTS
- Bandwidth: 1TB

### **Hostinger VPS Kurulumu (Gerçek Örnek)**

**Bu rehber gerçek bir deployment'a dayanmaktadır - sistem şu anda canlıda çalışıyor!**

#### **Adım 1: VPS Satın Alma**
```bash
1. Hostinger VPS paketi seç
2. Ubuntu 22.04 LTS yükle
3. Root erişim sağla
4. IP adresini kaydet (örnek: 31.97.44.248)
```

#### **Adım 2: VPS İlk Kurulum**
```bash
# VPS'e bağlan
ssh root@your-vps-ip

# Sistem güncelle
apt update && apt upgrade -y

# Temel paketler
apt install -y software-properties-common curl wget git vim htop

# Python 3.12
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# PostgreSQL
apt install -y postgresql postgresql-contrib
systemctl start postgresql
systemctl enable postgresql

# Redis (opsiyonel)
apt install -y redis-server
systemctl enable redis-server
```

#### **Adım 3: Database Kurulumu**
```bash
# PostgreSQL kullanıcı ve database
sudo -u postgres createdb context7_erp
sudo -u postgres createuser context7_user
sudo -u postgres psql -c "ALTER USER context7_user WITH PASSWORD 'GuvenliSifre123!';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE context7_erp TO context7_user;"

# Connection test
sudo -u postgres psql -d context7_erp -c "SELECT version();"
```

#### **Adım 4: Proje Kurulumu**
```bash
# Proje dizini oluştur
mkdir -p /var/www/context7
cd /var/www/context7

# Git clone (veya ZIP upload)
git clone https://your-repo.git .

# Virtual environment
python3.12 -m venv context7_venv
source context7_venv/bin/activate

# Dependencies
pip install -r requirements_production.txt
```

#### **Adım 5: Environment Configuration**
```bash
# Production .env
cp .env.production .env

# .env düzenle
nano .env
```

**Production .env örneği:**
```env
DEBUG=False
SECRET_KEY=production-secret-key-very-long-and-secure
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-vps-ip

# Database
DATABASE_URL=postgresql://context7_user:GuvenliSifre123!@localhost/context7_erp

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

#### **Adım 6: Django Setup**
```bash
# ALLOWED_HOSTS güncelle (ÖNEMLİ!)
# settings.py'da ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'VPS-IP', 'domain.com']

# Migration
python manage.py migrate

# Static files
python manage.py collectstatic --noinput

# Superuser
python manage.py createsuperuser

# Test migration
python manage.py check --deploy
```

#### **Adım 7: Firewall & Security**
```bash
# UFW firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 8000  # Development için
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw --force enable

# Test server
python manage.py runserver 0.0.0.0:8000
```

#### **Adım 8: Production Web Server (Nginx + Gunicorn)**
```bash
# Nginx
apt install -y nginx

# Gunicorn
pip install gunicorn

# Gunicorn service
sudo tee /etc/systemd/system/context7.service > /dev/null <<EOF
[Unit]
Description=Context7 ERP Gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/context7
ExecStart=/var/www/context7/context7_venv/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/var/www/context7/context7.sock \\
          dashboard_project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Service başlat
systemctl start context7
systemctl enable context7
systemctl status context7

# Nginx config
sudo tee /etc/nginx/sites-available/context7 > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /staticfiles/ {
        root /var/www/context7;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/context7/context7.sock;
    }
}
EOF

# Site aktifleştir
ln -s /etc/nginx/sites-available/context7 /etc/nginx/sites-enabled
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

#### **Adım 9: SSL Certificate**
```bash
# Certbot
apt install -y certbot python3-certbot-nginx

# SSL sertifikası
certbot --nginx -d your-domain.com -d www.your-domain.com --email admin@your-domain.com --agree-tos --non-interactive

# Auto renewal test
certbot renew --dry-run
```

#### **Adım 10: Domain Configuration**
```bash
# DNS kayıtları (domain sağlayıcınızda)
A Record: @ -> VPS-IP
A Record: www -> VPS-IP
CNAME Record: api -> your-domain.com

# SSL sonrası test
https://your-domain.com
https://www.your-domain.com
https://your-domain.com/admin/
https://your-domain.com/api/v1/
```

---

## 🐳 **3. Docker Kurulumu**

### **Docker Compose Setup**
```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://context7:password@db:5432/context7_erp
    depends_on:
      - db
      - redis
    volumes:
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: context7_erp
      POSTGRES_USER: context7
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

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
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./staticfiles:/var/www/staticfiles
    depends_on:
      - web

volumes:
  postgres_data:
```

### **Docker Build & Run**
```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Migrate
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static
docker-compose exec web python manage.py collectstatic --noinput
```

---

## ☁️ **4. Cloud Deployment**

### **AWS EC2 Deployment**
```bash
# EC2 instance oluştur (Ubuntu 22.04)
# Security groups: SSH (22), HTTP (80), HTTPS (443), Custom (8000)
# Elastic IP ata
# Yukarıdaki VPS adımlarını takip et
```

### **Azure App Service**
```bash
# Azure CLI
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name context7-erp --runtime "PYTHON|3.12"

# Git deployment
az webapp deployment source config --name context7-erp --resource-group myResourceGroup --repo-url https://your-repo.git --branch main
```

### **Google Cloud Run**
```bash
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 dashboard_project.wsgi:application

# Deploy
gcloud run deploy context7-erp --source . --platform managed --region us-central1 --allow-unauthenticated
```

---

## 🔧 **Sistem Yönetimi**

### **Günlük Yönetim Komutları**
```bash
# Service yeniden başlatma
systemctl restart context7
systemctl restart nginx
systemctl restart postgresql

# Log takibi
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
journalctl -u context7 -f

# Database backup
pg_dump context7_erp > backup_$(date +%Y%m%d).sql

# Static files güncelleme
python manage.py collectstatic --noinput

# Migration
python manage.py migrate

# Cache temizleme
python manage.py clearcache  # Redis kullanıyorsanız
```

### **Performance Monitoring**
```bash
# System resources
htop
iotop
df -h
free -h

# Database performance
sudo -u postgres psql -d context7_erp -c "SELECT * FROM pg_stat_activity;"

# Nginx stats
curl http://localhost/nginx_status
```

---

## 🔍 **Troubleshooting**

### **Yaygın Sorunlar ve Çözümler**

#### **1. DisallowedHost Hatası**
```bash
# Hata: Invalid HTTP_HOST header
# Çözüm: settings.py'da ALLOWED_HOSTS güncelle
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'VPS-IP', 'domain.com']
```

#### **2. Database Connection Error**
```bash
# PostgreSQL servis kontrolü
systemctl status postgresql

# Connection test
sudo -u postgres psql -d context7_erp -c "SELECT 1;"

# Password reset
sudo -u postgres psql -c "ALTER USER context7_user WITH PASSWORD 'NewPassword';"
```

#### **3. Static Files 404**
```bash
# Static files collect
python manage.py collectstatic --noinput

# Nginx static files config
location /staticfiles/ {
    alias /var/www/context7/staticfiles/;
}
```

#### **4. Migration Errors**
```bash
# Pending migrations check
python manage.py showmigrations

# Fake migration (dikkatli kullan)
python manage.py migrate --fake

# Reset migrations
python manage.py migrate app_name zero
python manage.py migrate app_name
```

#### **5. SSL Certificate Issues**
```bash
# Certificate renewal
certbot renew

# Force renewal
certbot renew --force-renewal

# Check certificate
openssl x509 -in /etc/letsencrypt/live/domain.com/cert.pem -text -noout
```

---

## 📊 **Performance Optimization**

### **Database Optimization**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'context7_erp',
        'USER': 'context7_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'MAX_CONNS': 20,  # Connection pooling
        }
    }
}

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### **Nginx Optimization**
```nginx
# nginx.conf
worker_processes auto;
worker_connections 1024;

http {
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1000;
    gzip_types text/plain text/css application/json application/javascript;

    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### **Gunicorn Optimization**
```bash
# Gunicorn config
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
```

---

## 🔐 **Security Best Practices**

### **Django Security Settings**
```python
# settings.py production security
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

### **Server Security**
```bash
# SSH key authentication
ssh-keygen -t rsa -b 4096
ssh-copy-id root@vps-ip

# Disable password authentication
# /etc/ssh/sshd_config
PasswordAuthentication no
PermitRootLogin prohibit-password

# Fail2ban
apt install fail2ban
systemctl enable fail2ban

# Automatic updates
apt install unattended-upgrades
dpkg-reconfigure unattended-upgrades
```

---

## 📚 **Kaynak ve Dokümantasyon**

### **Resmi Dokümantasyon**
- Django: https://docs.djangoproject.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Nginx: https://nginx.org/en/docs/
- Gunicorn: https://docs.gunicorn.org/

### **Context7 Özel Dokümantasyon**
- API Dokümantasyonu: `docs/api/`
- Sistem Mimarisi: `docs/system/`
- Güvenlik Rehberi: `docs/security/`
- Deployment Rehberleri: `docs/deployment/`

### **Faydalı Komutlar**
```bash
# Django management commands
python manage.py help
python manage.py showmigrations
python manage.py dbshell
python manage.py shell
python manage.py test
python manage.py check --deploy

# System commands
systemctl status service-name
journalctl -u service-name
nginx -t
certbot certificates
```

---

## 🎯 **Sonuç**

Context7 ERP sistemi başarıyla farklı ortamlarda kurulabilir:

✅ **Yerel Development**: Hızlı geliştirme için  
✅ **Production VPS**: Canlı sistem için (Hostinger örneği ile test edildi)  
✅ **Docker**: Container tabanlı deployment  
✅ **Cloud**: AWS, Azure, Google Cloud desteği  

**Canlı Örnek**: http://31.97.44.248:8000 - Sistem şu anda çalışır durumda!

### **Başarılı Deployment Kanıtı**
- ✅ Hostinger VPS'te canlı çalışıyor
- ✅ PostgreSQL database aktif
- ✅ Glassmorphism UI yüklü
- ✅ Tüm ERP modülleri çalışıyor
- ✅ API endpoints aktif
- ✅ Admin panel erişilebilir

### **Destek**
Kurulum sırasında sorun yaşarsanız:
- Dokümantasyonu inceleyin: `docs/`
- Troubleshooting rehberini takip edin
- Log dosyalarını kontrol edin
- Community support forumlarını kullanın

**🚀 Context7 ERP ile başarılı projeler dileriz!** 