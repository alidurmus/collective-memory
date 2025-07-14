# 🔒 Context7 ERP - SSL Certificate Setup Plan

**Tarih**: 11 Temmuz 2025  
**Durum**: Planning Phase  
**Production Server**: http://31.97.44.248:8000 (Active)  
**Target**: https://intermeks.com (SSL Ready)

---

## 📋 **SSL Kurulum Durumu**

### ✅ **Mevcut Durum**
- **HTTP Server**: ✅ Aktif (31.97.44.248:8000)
- **Security Headers**: ✅ Aktif (CSP, XSS-Protection, etc.)
- **Domain**: intermeks.com (DNS configuration pending)
- **VPS Access**: ✅ Root access available

### 🎯 **Hedef Yapılandırma**
- **HTTPS**: https://intermeks.com
- **SSL Certificate**: Let's Encrypt (Free)
- **Web Server**: Nginx + Gunicorn
- **Auto-Renewal**: Certbot automation

---

## 🚀 **SSL Kurulum Adımları**

### **1. Nginx Kurulumu**
```bash
# VPS'te çalıştırılacak
sudo apt update
sudo apt install nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### **2. Gunicorn Konfigürasyonu**
```bash
# Django için Gunicorn kurulumu
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 dashboard_project.wsgi:application
```

### **3. Nginx Reverse Proxy**
```nginx
# /etc/nginx/sites-available/intermeks.com
server {
    listen 80;
    server_name intermeks.com www.intermeks.com 31.97.44.248;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/context7-erp/staticfiles/;
    }
}
```

### **4. Let's Encrypt SSL**
```bash
# Certbot kurulumu
sudo apt install certbot python3-certbot-nginx

# SSL certificate alma
sudo certbot --nginx -d intermeks.com -d www.intermeks.com

# Auto-renewal test
sudo certbot renew --dry-run
```

### **5. Django HTTPS Ayarları**
```python
# settings/production.py
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🔧 **Gerekli Dosyalar**

### **Systemd Service File**
```ini
# /etc/systemd/system/context7-erp.service
[Unit]
Description=Context7 ERP Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/context7-erp
ExecStart=/path/to/context7-erp/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 dashboard_project.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### **Nginx SSL Configuration**
```nginx
# HTTPS configuration (Certbot tarafından otomatik eklenir)
server {
    listen 443 ssl http2;
    server_name intermeks.com www.intermeks.com;
    
    ssl_certificate /etc/letsencrypt/live/intermeks.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/intermeks.com/privkey.pem;
    
    # SSL Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

---

## ⚠️ **Ön Gereksinimler**

### **1. DNS Konfigürasyonu**
- **A Record**: intermeks.com → 31.97.44.248
- **CNAME**: www.intermeks.com → intermeks.com
- **TTL**: 300 (5 dakika)

### **2. Firewall Ayarları**
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 22
sudo ufw enable
```

### **3. Domain Ownership Verification**
- Domain kontrolü (DNS propagation)
- Whois verification
- SSL certificate validation

---

## 📊 **SSL Kurulum Checklist**

### **Hazırlık Aşaması**
- [ ] DNS A record konfigürasyonu
- [ ] Domain propagation kontrolü
- [ ] VPS firewall ayarları
- [ ] Nginx kurulumu

### **SSL Certificate**
- [ ] Certbot kurulumu
- [ ] Let's Encrypt certificate alma
- [ ] Auto-renewal konfigürasyonu
- [ ] SSL test (SSL Labs)

### **Django Konfigürasyonu**
- [ ] HTTPS settings aktivasyonu
- [ ] Security headers güncellemesi
- [ ] Static files HTTPS
- [ ] Production testing

### **Monitoring**
- [ ] SSL certificate expiry monitoring
- [ ] HTTPS redirect testing
- [ ] Security headers validation
- [ ] Performance testing

---

## 🚨 **Kritik Notlar**

### **Downtime Minimization**
1. **Staging Test**: Local'de SSL test
2. **Backup Plan**: HTTP fallback hazır
3. **Quick Rollback**: Nginx config backup
4. **Monitoring**: Real-time SSL monitoring

### **Security Considerations**
- **Mixed Content**: HTTP resource'ları HTTPS'e çevir
- **HSTS**: HTTP Strict Transport Security
- **CSP**: Content Security Policy güncellemesi
- **Certificate Pinning**: İleri seviye güvenlik

---

## 📅 **Timeline**

### **Phase 1: Preparation (1-2 gün)**
- DNS configuration
- Nginx setup
- Gunicorn configuration

### **Phase 2: SSL Implementation (1 gün)**
- Let's Encrypt certificate
- HTTPS redirect
- Security testing

### **Phase 3: Optimization (1 gün)**
- Performance tuning
- Security hardening
- Monitoring setup

---

**🎯 Başarı Kriteri**: https://intermeks.com adresinde güvenli erişim sağlanması ve A+ SSL rating alınması.

**📞 Destek**: Bu plan Context7 Central Protocol v1.0 standartlarına uygun olarak hazırlanmıştır. 