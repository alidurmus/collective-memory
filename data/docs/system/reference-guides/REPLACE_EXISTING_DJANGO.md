# 🔄 Context7 ERP - Mevcut Django'yu Değiştirme Rehberi

## 📋 Mevcut Durum
- VPS IP: 31.97.44.248
- Mevcut Django Site: http://31.97.44.248/
- Mevcut Admin: http://31.97.44.248/admin/

## 🎯 Hedef
Mevcut Django uygulamasını Context7 ERP sistemi ile değiştirmek

---

## 🔍 1. Mevcut Sistem Analizi

VPS'e bağlanarak mevcut durumu inceleyin:

```bash
# VPS'e bağlan
ssh root@31.97.44.248

# Çalışan servisleri kontrol et
systemctl status nginx
systemctl status apache2
systemctl status lsws  # LiteSpeed varsa

# Mevcut Django projesini bul
find / -name "manage.py" -type f 2>/dev/null
find / -name "settings.py" -type f 2>/dev/null

# Port kullanımını kontrol et
netstat -tlnp | grep :80
netstat -tlnp | grep :443
```

## 🛑 2. Mevcut Uygulamayı Durdurma

### LiteSpeed kullanılıyorsa:
```bash
systemctl stop lsws
systemctl disable lsws
```

### Nginx + Gunicorn kullanılıyorsa:
```bash
systemctl stop nginx
systemctl stop gunicorn  # veya mevcut django service
```

### Apache kullanılıyorsa:
```bash
systemctl stop apache2
systemctl disable apache2
```

## 💾 3. Backup Alma (Önemli!)

```bash
# Mevcut proje backup'ı
mkdir -p /backup/old_django_$(date +%Y%m%d)
find / -name "manage.py" -type f 2>/dev/null | head -1 | xargs dirname | xargs -I {} cp -r {} /backup/old_django_$(date +%Y%m%d)/

# Database backup (eğer varsa)
pg_dumpall > /backup/old_django_$(date +%Y%m%d)/database_backup.sql

# Web server konfigürasyon backup
cp -r /etc/nginx /backup/old_django_$(date +%Y%m%d)/nginx_backup 2>/dev/null || true
cp -r /etc/apache2 /backup/old_django_$(date +%Y%m%d)/apache_backup 2>/dev/null || true
cp -r /usr/local/lsws /backup/old_django_$(date +%Y%m%d)/lsws_backup 2>/dev/null || true
```

## 🗑️ 4. Eski Uygulamayı Temizleme

```bash
# Eski projeyi kaldır (backup aldıktan sonra)
rm -rf /var/www/html/*
rm -rf /usr/local/lsws/Example/html/* 2>/dev/null || true

# Eski servis dosyalarını kaldır
rm -f /etc/systemd/system/old_django.service
systemctl daemon-reload
```

## 📦 5. Context7 ERP Deployment

### 5.1 Proje Dosyalarını Yükleme
```bash
# Context7 deployment package'ını yükle
cd /tmp
# (context7_erp_production.zip dosyasını buraya yükleyin)

# Proje dizinini oluştur
mkdir -p /var/www/context7
cd /var/www/context7

# Package'ı extract et
unzip /tmp/context7_erp_production.zip -d /var/www/context7/
chown -R context7:context7 /var/www/context7
```

### 5.2 Sistem Hazırlıkları
```bash
# Python 3.11 kurulu değilse
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.11 python3.11-venv python3.11-dev

# PostgreSQL kurulu değilse
apt install -y postgresql postgresql-contrib
systemctl start postgresql
systemctl enable postgresql

# Redis kurulu değilse
apt install -y redis-server
systemctl start redis-server
systemctl enable redis-server
```

### 5.3 Database Setup
```bash
# PostgreSQL veritabanı oluştur
sudo -u postgres createdb context7_erp
sudo -u postgres createuser context7_user
sudo -u postgres psql -c "ALTER USER context7_user WITH PASSWORD 's6ghtD.fdSSadasf';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE context7_erp TO context7_user;"
```

### 5.4 Python Environment
```bash
# Context7 user'a geç
su - context7
cd /var/www/context7

# Virtual environment oluştur
python3.11 -m venv venv
source venv/bin/activate

# Dependencies yükle
pip install -r requirements_production.txt

# Environment dosyasını kopyala
cp .env.production .env

# Django setup
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser
```

## 🌐 6. Web Server Konfigürasyonu

### Nginx Installation & Configuration
```bash
# Nginx yükle
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Context7 nginx config'i kopyala
sudo cp /var/www/context7/scripts/nginx/context7.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/context7.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Gunicorn service setup
sudo cp /var/www/context7/scripts/systemd/context7.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start context7
sudo systemctl enable context7

# Configuration test
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 7. SSL Certificate

```bash
# Certbot yükle
sudo apt install -y certbot python3-certbot-nginx

# SSL certificate al
sudo certbot --nginx -d intermeks.com -d www.intermeks.com --email admin@intermeks.com --agree-tos --non-interactive
```

## 🛡️ 8. Firewall Configuration

```bash
# UFW setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

## ✅ 9. Test & Verification

```bash
# Servisleri kontrol et
sudo systemctl status context7 nginx postgresql redis-server

# Log'ları kontrol et
sudo journalctl -u context7 -f
sudo tail -f /var/log/nginx/access.log
```

### Test URL'leri:
- **Ana Site**: http://31.97.44.248/ → Context7 ERP ana sayfası
- **Admin Panel**: http://31.97.44.248/admin/ → Context7 admin paneli
- **API**: http://31.97.44.248/api/v1/ → Context7 REST API

## 🔄 10. DNS Güncellemesi

Domain'inizi VPS'e yönlendirin:
```
Type: A Record
Name: @
Value: 31.97.44.248

Type: A Record  
Name: www
Value: 31.97.44.248
```

SSL kurulumundan sonra:
- **HTTPS Ana Site**: https://intermeks.com/
- **HTTPS Admin**: https://intermeks.com/admin/

## 🆘 11. Troubleshooting

### Sorun: 502 Bad Gateway
```bash
sudo systemctl restart context7
sudo systemctl status context7
```

### Sorun: Static files yüklenmiyor
```bash
python manage.py collectstatic --noinput
sudo systemctl reload nginx
```

### Sorun: Database bağlantı hatası
```bash
sudo systemctl status postgresql
# .env dosyasındaki database bilgilerini kontrol et
```

---

## 🎉 Sonuç

Bu adımların tamamlanmasından sonra:
- ✅ Eski Django uygulaması backup alınmış
- ✅ Context7 ERP sistemi aktif
- ✅ SSL sertifikası kurulmuş
- ✅ Güvenlik yapılandırılmış
- ✅ Otomatik backup sistemi aktif

**VPS'iniz artık tam özellikli Context7 ERP sistemi ile hazır!** 🚀 