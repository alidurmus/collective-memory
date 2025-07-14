# Django Yedekleme Sistemi

Bu sistem, Django uygulamanız için kapsamlı bir yedekleme ve geri yükleme çözümü sağlar.

## Özellikler

### 1. Yedekleme Türleri
- **Tam Yedekleme**: Veritabanı, medya dosyaları ve sistem ayarlarının tamamı
- **Veritabanı Yedeklemesi**: Sadece veritabanı verilerinin yedeklenmesi
- **Medya Dosyaları**: Yüklenen dosyaların yedeklenmesi
- **Sistem Ayarları**: Konfigürasyon ayarlarının yedeklenmesi

### 2. Otomatik Yedekleme
- Günlük, haftalık ve aylık yedekleme programları
- Eski yedeklerin otomatik temizlenmesi
- Esnek zamanlama seçenekleri

### 3. Web Arayüzü
- Kullanıcı dostu yedekleme yönetimi
- Yedekleme durumu takibi
- Dosya indirme ve geri yükleme

## Kurulum

### 1. Migration'ları Çalıştırın
```bash
python manage.py makemigrations settings_app
python manage.py migrate settings_app
```

### 2. Yedekleme Dizinini Oluşturun
```bash
mkdir backups
```

### 3. Gerekli İzinleri Verin
Backup dizinine yazma izni verin.

## Kullanım

### Manuel Yedekleme
```bash
# Tam yedekleme
python manage.py create_backup --type=full --name="manuel_tam_yedek"

# Sadece veritabanı
python manage.py create_backup --type=database --name="db_yedek"

# Sadece ayarlar
python manage.py create_backup --type=settings --name="ayar_yedek"

# Sadece medya dosyaları
python manage.py create_backup --type=media --name="medya_yedek"
```

### Geri Yükleme
```bash
# Yedek dosyasını geri yükle
python manage.py restore_backup backups/yedek_dosyasi.zip

# Onay almadan geri yükle (dikkatli kullanın!)
python manage.py restore_backup backups/yedek_dosyasi.zip --force
```

### Programlanmış Yedeklemeler
```bash
# Programlanmış yedeklemeleri çalıştır (cron job için)
python manage.py run_scheduled_backups
```

## Web Arayüzü

### Erişim
- Ana menüden **Settings > Backup Management** seçin
- URL: `/settings/backup/`

### Özellikler
1. **Yedekleme Oluştur**: Yeni yedekleme başlatma
2. **Yedekleme Listesi**: Mevcut yedeklemeleri görüntüleme ve indirme
3. **Otomatik Yedekleme**: Programlanmış yedekleme oluşturma
4. **Geri Yükleme**: Yedek dosyasından geri yükleme

## Otomatik Yedekleme Kurulumu

### Linux/Mac (Cron Job)
```bash
# Crontab'ı düzenle
crontab -e

# Her gün saat 02:00'da çalıştır
0 2 * * * cd /path/to/project && python manage.py run_scheduled_backups

# Her saat başı kontrol et
0 * * * * cd /path/to/project && python manage.py run_scheduled_backups
```

### Windows (Task Scheduler)
1. Task Scheduler'ı açın
2. "Create Basic Task" seçin
3. Trigger olarak "Daily" veya "Weekly" seçin
4. Action olarak şu komutu ekleyin:
   ```
   python C:\path\to\project\manage.py run_scheduled_backups
   ```

## Güvenlik

### Erişim Kontrolü
- Yedekleme sayfası sadece admin kullanıcılar için erişilebilir
- `@user_passes_test(is_admin)` decorator kullanılır

### Dosya Güvenliği
- Yedek dosyalar `backups/` dizininde saklanır
- Hassas bilgiler için şifreleme önerilir

## Dosya Formatları

### Veritabanı Yedekleri
- SQLite: `.db` dosyası kopyası
- Diğer DB'ler: JSON formatında export

### Ayar Yedekleri
- JSON formatında
- Tüm settings_app modellerini içerir

### Medya Yedekleri
- ZIP formatında sıkıştırılmış
- Tüm MEDIA_ROOT içeriği

### Tam Yedekleme
- ZIP formatında
- Veritabanı + Ayarlar + Medya dosyaları

## Sorun Giderme

### Yaygın Hatalar

1. **Permission Denied**
   ```bash
   chmod 755 backups/
   ```

2. **Disk Alanı Yetersiz**
   - Eski yedekleri temizleyin
   - `keep_count` ayarını düşürün

3. **Büyük Dosya Sorunları**
   - PHP/Django upload limitlerini artırın
   - Medya dosyalarını ayrı yedekleyin

### Log Kontrolü
```bash
# Django loglarını kontrol edin
tail -f logs/django.log

# Backup komut çıktısını kontrol edin
python manage.py create_backup --type=database 2>&1 | tee backup.log
```

## API Endpoints

### Backup Status API
```
GET /settings/api/backup-status/
```
Çalışan yedeklemelerin durumunu JSON formatında döner.

## Özelleştirme

### Yeni Yedekleme Türü Ekleme
1. `SystemBackup.BACKUP_TYPES` listesine ekleyin
2. `create_backup.py` command'ına yeni metod ekleyin
3. `restore_backup.py` command'ına geri yükleme mantığı ekleyin

### Bildirim Sistemi
E-posta bildirimleri için `EmailSetting` modelini kullanabilirsiniz.

## Performans İpuçları

1. **Büyük Veritabanları**: Incremental backup kullanın
2. **Medya Dosyaları**: Rsync veya benzeri araçlar kullanın
3. **Sıkıştırma**: ZIP yerine tar.gz kullanın
4. **Paralel İşlem**: Celery ile asenkron yedekleme

## Lisans

Bu yedekleme sistemi MIT lisansı altında dağıtılmaktadır. 