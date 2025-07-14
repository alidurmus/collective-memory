# 🚀 Context7 ERP - Hostinger Deployment Adım Adım Talimatlar

## 📋 Sunucu Bilgileri
- **Sunucu**: srv858543.hstgr.cloud
- **IP**: 31.97.44.248
- **Root Şifre**: Qz@2C9E0h9tjq)s6ghtD
- **Veritabanı Şifresi**: s6ghtD.fdSSadasf
- **Admin Giriş**: admin / XG3sWT3rDcuRhbhN

## 🎯 Deployment Süreci (4 Adım)

### Adım 1: Dosyaları Sunucuya Yükle
```bash
# Windows üzerinden (PowerShell):
scp Context7-ERP-Hostinger-Deployment.zip root@31.97.44.248:/tmp/

# Alternatif olarak WinSCP veya FileZilla kullanabilirsiniz
# Hedef konum: /tmp/Context7-ERP-Hostinger-Deployment.zip
```

### Adım 2: Sunucuya Bağlan ve Dosyaları Çıkar
```bash
# SSH ile bağlan
ssh root@31.97.44.248

# Dosyaları çıkar
cd /tmp
unzip Context7-ERP-Hostinger-Deployment.zip -d context7-erp-hostinger/
cd context7-erp-hostinger/

# Deployment script'ini çalıştırılabilir yap
chmod +x hostinger_deploy_final.sh
```

### Adım 3: Deployment Script'ini Çalıştır
```bash
# Deployment script'ini çalıştır
./hostinger_deploy_final.sh

# Script şunları yapacak:
# - context7 kullanıcısı oluştur
# - Sistem bağımlılıklarını yükle
# - Python virtual environment kur
# - Django uygulamasını yapılandır
# - Veritabanını hazırla
# - Superuser oluştur
# - Systemd servisi kur
```

### Adım 4: Servisi Başlat
```bash
# Systemd servisi ile başlat (önerilen)
sudo systemctl start context7-erp
sudo systemctl enable context7-erp

# Durumu kontrol et
sudo systemctl status context7-erp

# Alternatif: Manuel başlatma
su - context7
cd /home/context7/context7-erp
./start_server.sh
```

## 🌐 Sisteme Erişim

### URL'ler
- **Ana Site**: http://31.97.44.248
- **Admin Panel**: http://31.97.44.248/admin/
- **API**: http://31.97.44.248/api/

### Giriş Bilgileri
- **Kullanıcı Adı**: admin
- **Şifre**: XG3sWT3rDcuRhbhN

## 🔧 Alternatif Deployment (Manuel)

Eğer otomatik script çalışmazsa:

### 1. Manuel Kurulum
```bash
# Bağımlılıkları yükle
apt-get update
apt-get install -y python3 python3-pip python3-venv python3-dev nginx

# Kullanıcı oluştur
useradd -m -s /bin/bash context7
echo "context7:s6ghtD.fdSSadasf" | chpasswd

# Proje dizinini oluştur
mkdir -p /home/context7/context7-erp
cp -r /tmp/context7-erp-hostinger/* /home/context7/context7-erp/
chown -R context7:context7 /home/context7/

# context7 kullanıcısına geç
su - context7
cd /home/context7/context7-erp
```

### 2. Python Environment Kurulumu
```bash
# Virtual environment oluştur
python3 -m venv /home/context7/venv
source /home/context7/venv/bin/activate

# Bağımlılıkları yükle
pip install Django==5.2.3 djangorestframework==3.15.2 gunicorn==21.2.0

# .env dosyası oluştur
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=dashboard_project.sqlite_settings
DATABASE_URL=sqlite:///$(pwd)/db.sqlite3
ALLOWED_HOSTS=31.97.44.248,srv858543.hstgr.cloud,localhost
EOF
```

### 3. Django Kurulumu
```bash
# Django kurulumu
export DJANGO_SETTINGS_MODULE=dashboard_project.sqlite_settings
python manage.py collectstatic --noinput
python manage.py migrate

# Superuser oluştur
python manage.py createsuperuser
# Username: admin
# Email: admin@intermeks.com
# Password: XG3sWT3rDcuRhbhN
```

## 🎯 Sistem Yönetimi

### Servis Kontrolü
```bash
# Servisi başlat/durdur
sudo systemctl start context7-erp
sudo systemctl stop context7-erp
sudo systemctl restart context7-erp

# Durumu kontrol et
sudo systemctl status context7-erp

# Logları görüntüle
sudo journalctl -u context7-erp -f
```

### Troubleshooting
```bash
# Port kontrolü
netstat -tlnp | grep 8000

# Django kontrolü
cd /home/context7/context7-erp
source /home/context7/venv/bin/activate
python manage.py check

# Veritabanı kontrolü
python manage.py migrate --run-syncdb
```

## 🔐 Güvenlik Özellikleri

Sistem şu güvenlik özelliklerini içerir:
- **Rate Limiting**: API için 1000/saat, Dashboard için 200/saat
- **Security Headers**: XSS, CSRF koruması
- **Input Validation**: SQL injection koruması
- **Session Security**: Güvenli oturum yönetimi

## 📊 Sistem Özellikleri

- **Framework**: Django 5.2.3
- **Veritabanı**: SQLite (production ready)
- **UI Framework**: Context7 Glassmorphism v2.2.0
- **API**: Django REST Framework + JWT
- **Sunucu**: Gunicorn + Nginx

## 🏢 ERP Modülleri

1. **Satış Yönetimi**: Müşteri yönetimi, satış siparişleri
2. **Satın Alma**: Tedarikçi yönetimi, satın alma siparişleri
3. **Üretim**: İş emirleri, üretim planlama
4. **Stok**: Stok yönetimi, depo operasyonları
5. **Finans**: Mali raporlama, muhasebe
6. **İnsan Kaynakları**: Personel yönetimi
7. **Kalite Kontrol**: Kalite güvencesi, denetim raporları
8. **İş Emirleri**: Görev yönetimi, iş akışı takibi

## ✅ Deployment Kontrol Listesi

- [ ] Sunucu bağlantısı kuruldu
- [ ] Dosyalar yüklendi
- [ ] Bağımlılıklar yüklendi
- [ ] Virtual environment oluşturuldu
- [ ] Veritabanı migrate edildi
- [ ] Superuser oluşturuldu
- [ ] Static dosyalar toplandı
- [ ] Servis yapılandırıldı
- [ ] Sistem tarayıcıdan erişilebilir
- [ ] Admin paneli çalışıyor
- [ ] API endpoint'leri çalışıyor

## 🎉 Başarılı Deployment!

Deployment tamamlandıktan sonra:
- Tam fonksiyonel ERP sistemi
- Modern glassmorphism UI
- 8 entegre iş modülü
- JWT authentication ile REST API
- Test için örnek veriler
- Production-ready konfigürasyon

**Sisteme erişin**: http://31.97.44.248
**Admin giriş**: admin / XG3sWT3rDcuRhbhN 