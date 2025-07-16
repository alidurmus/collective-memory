# 📚 Collective Memory - Detaylı Kullanım Rehberi

**Last Updated:** 14 Temmuz 2025  
**Version:** v2.1 Enhanced with Directory Management  
**Status:** Production Ready  

---

## 🚨 **ÖNEMLİ: Data Klasörü Hakkında**

> **UYARI:** `/data` klasörü sadece **örnek ve test amaçlıdır!**
> 
> - ❌ **Ana program değildir** - Asıl sistem `collective-memory-app/` klasöründedir
> - ✅ **Demo içerik** - Sadece test ve öğrenme için
> - ✅ **Gerçek kullanım** - Kendi klasörünüzü belirtin: `--data-path /path/to/your/docs`
> 
> **Detaylı bilgi:** [Data Klasörü Açıklaması](DATA_USAGE_NOTE.md)

---

## 🆕 **YENİ ÖZELLİKLER (v2.1)**

✅ **Otomatik Klasör Organizasyonu** - `.collective-memory/` klasörü otomatik oluşturulur  
✅ **Arama Sonucu Dışa Aktarma** - `--save-to dosya.md` ile sonuçları kaydet  
✅ **Gelişmiş Veritabanı Yönetimi** - Daha iyi organizasyon ve önbellekleme  
✅ **Platform Bağımsızlığı** - Windows, macOS, Linux desteği  

### 📁 **Otomatik Dizin Yapısı**

Sistem ilk çalıştırıldığında projenizde şu yapıyı oluşturur:

```
[Proje Klasörünüz]/
├── [Mevcut dosyalarınız...]
└── .collective-memory/
    ├── database/
    │   └── collective_memory.db    # SQLite veritabanı
    ├── cache/                      # Arama önbelleği
    ├── logs/                       # Sistem logları
    ├── config/                     # Yapılandırma dosyaları
    │   ├── settings.json          # Sistem ayarları
    │   └── project_status.json    # Proje durumu
    └── README.md                   # Sistem dokümantasyonu
```

---

## 🚨 **Hızlı Sorun Çözme (Troubleshooting)**

### **En Yaygın Hata: "can't open file" Sorunu**

❌ **YANLIŞ:**
```bash
PS C:\cursor\collective-memory> python src/main.py --interactive --data-path ../data
```

✅ **DOĞRU:**
```bash
PS C:\cursor\collective-memory> cd collective-memory-app
PS C:\cursor\collective-memory\collective-memory-app> python src/main.py --interactive --data-path ../data
```

### **Temel Sorun Giderme Kontrol Listesi**

1. **Klasör Konumu Kontrolü:**
   ```bash
   pwd                           # Bulunduğunuz klasörü gösterir
   ls -la                        # Dosyaları listeler (Linux/Mac)
   dir                          # Dosyaları listeler (Windows)
   ```

2. **Gerekli Dosya Kontrolü:**
   ```bash
   ls collective-memory-app/src/main.py    # Dosya var mı?
   python --version                        # Python versiyonu (3.9+ gerekli)
   ```

3. **Dizin Yapısı Kontrolü:**
   ```bash
   # Collective memory dizini oluştu mu?
   ls -la [proje-klasörü]/.collective-memory/
   
   # Veritabanı dosyası var mı?
   ls -la [proje-klasörü]/.collective-memory/database/collective_memory.db
   ```

---

## 🔧 **KURULUM VE İLK KULLANIM**

### **1. Temel Kurulum**
```bash
# Projeyi klonlayın
git clone https://github.com/your-username/collective-memory.git
cd collective-memory

# Ana uygulamaya gidin  
cd collective-memory-app

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### **2. İlk İndeksleme**
```bash
# Kendi proje klasörünüzü indeksleyin
python src/main.py --index --data-path "C:\path\to\your\project"

# Sistem otomatik olarak .collective-memory/ klasörü oluşturacak
```

### **3. Arama ve Sorgu Kullanımı**

#### **A. Temel Arama**
```bash
# Basit metin arama
python src/main.py --search "Django ayarları" --data-path "C:\your\project"

# Sonuçları ekranda gösterir
```

#### **B. Arama Sonuçlarını Dosyaya Kaydetme** ⭐ **YENİ**
```bash
# Arama yap ve sonuçları dosyaya kaydet
python src/main.py --search "hata çözümü" --save-to "error-solutions.md" --data-path "C:\your\project"

# Dosya .collective-memory/ klasöründe kaydedilir
```

#### **C. İnteraktif Mod**
```bash
# İnteraktif modda başlat
python src/main.py --interactive --data-path "C:\your\project"

# Komutlar:
# help         - Yardım göster
# stats        - İstatistikleri göster  
# search term  - Arama yap
# quit         - Çıkış
```

#### **D. Sistem İstatistikleri**
```bash
# Proje istatistiklerini göster
python src/main.py --stats --data-path "C:\your\project"
```

---

## 📖 **KULLANIM ÖRNEKLERİ**

### **Örnek 1: Django Projesinde Hata Araştırması**
```bash
# Django hatalarını ara ve kaydet
python src/main.py --search "NoReverseMatch error" --save-to "django-errors.md" --data-path "C:\projects\django-app"

# Çıktı: .collective-memory/django-errors.md dosyasında
```

### **Örnek 2: API Dokümantasyonu Araması**
```bash
# API endpoint'lerini ara
python src/main.py --search "API endpoint configuration" --data-path "C:\projects\api-docs"

# İnteraktif modda detay araştırması
python src/main.py --interactive --data-path "C:\projects\api-docs"
```

### **Örnek 3: Proje Genel Araştırması**
```bash
# İlk olarak proje istatistiklerini kontrol et
python src/main.py --stats --data-path "C:\projects\my-project"

# Genel arama yap
python src/main.py --search "authentication system" --save-to "auth-research.md" --data-path "C:\projects\my-project"
```

---

## 💻 **Temel Kullanım Komutları**

### **1. İnteraktif Terminal Modu (Ana Özellik)**

```bash
cd collective-memory-app
# Kendi klasörünüzü kullanın:
python src/main.py --interactive --data-path /path/to/your/documents
# VEYA test için demo data:
python src/main.py --interactive --data-path ../data

# Terminal açıldıktan sonra kullanılabilir komutlar:
search keyword                    # Anahtar kelime arama
search "birden fazla kelime"     # Çok kelimeli arama
search keyword --limit=20        # Sonuç sayısını sınırla
search keyword --type=markdown   # Dosya türü filtresi
files                           # Tüm dosyaları listele
files --recent                  # Son değişen dosyalar
stats                          # Sistem istatistikleri
cursor_history                 # Cursor chat geçmişi
cursor_history --limit=20      # Son 20 chat
cursor_history --workspaces    # Tüm workspace'ler
help                           # Tüm komutlar
exit                           # Çıkış
```

### **2. Tek Seferlik Sorgular**

```bash
# Direkte arama yap:
python src/main.py --search "react component" --data-path ../data

# Dosya listesi al:
python src/main.py --list-files --data-path ../data

# Sistem durumu kontrol et:
python src/main.py --status --data-path ../data
```

### **3. Cursor Chat Geçmişi Erişimi**

```bash
# Cursor chat geçmişini göster:
python src/main.py --cursor-history --data-path ../data

# Son 10 chat'i göster:
python src/main.py --cursor-history --limit=10 --data-path ../data

# Workspace'leri listele:
python src/main.py --cursor-workspaces --data-path ../data
```

---

## 🔧 **Gelişmiş Kullanım Senaryoları**

### **Senaryo 1: Proje Dokümantasyonu Araması**

```bash
# Terminal modunda:
search "API documentation"           # API dokümanları
search "deployment guide"           # Deployment rehberleri
search "database schema"            # Veritabanı şemaları
search "test coverage" --type=md    # Test kapsamı bilgileri
```

### **Senaryo 2: Hata Çözümü ve Troubleshooting**

```bash
# Hata pattern arama:
search "error" --limit=50           # Tüm hata raporları
search "fix" --type=markdown        # Çözüm dokümanları
search "resolution"                 # Problem çözümleri
```

### **Senaryo 3: Kod Referansları ve Örnekler**

```bash
# Kod örneği arama:
search "javascript"                 # JS kod örnekleri
search "python function"           # Python fonksiyonları
search "django model"              # Django model örnekleri
```

### **Senaryo 4: Cursor Context Collection**

```bash
# Cursor'dan context topla ve panoya kopyala:
# Kod içinde yorum olarak:
# @collect-memory: React modal component implement et

# Manuel trigger:
python src/main.py --collect-context --request "React modal component" --data-path ../data
```

---

## 📊 **Sistem Monitoring ve İstatistikler**

### **Real-time Sistem Durumu**

```bash
# İnteraktif modda:
stats                              # Genel sistem istatistikleri
files --recent                     # Son değişen dosyalar
files --count                      # Toplam dosya sayısı
```

### **Performans Metrikleri**

```bash
# Sistem performance testi:
python src/main.py --performance-test --data-path ../data

# Database durumu:
python src/main.py --db-status --data-path ../data

# İndeksleme durumu:
python src/main.py --index-status --data-path ../data
```

---

## 🛠️ **Konfigürasyon ve Özelleştirme**

### **Config Dosyası (config/settings.json)**

```json
{
    "data_path": "../data",
    "database_path": "collective_memory.db",
    "log_level": "INFO",
    "max_search_results": 50,
    "file_types": [".md", ".txt", ".py", ".js"],
    "ignore_patterns": ["*.log", "*.tmp", ".git/*"],
    "cursor_integration": true,
    "auto_monitoring": true
}
```

### **Ortam Değişkenleri**

```bash
# Windows:
set COLLECTIVE_MEMORY_DATA_PATH=C:\path\to\data
set COLLECTIVE_MEMORY_LOG_LEVEL=DEBUG

# Linux/Mac:
export COLLECTIVE_MEMORY_DATA_PATH=/path/to/data
export COLLECTIVE_MEMORY_LOG_LEVEL=DEBUG
```

---

## 🔍 **Arama İpuçları ve Best Practices**

### **Etkili Arama Teknikleri**

1. **Anahtar Kelime Seçimi:**
   ```bash
   search "implementation"          # Geniş arama
   search "react implementation"    # Spesifik arama
   search "react modal component"   # Çok spesifik arama
   ```

2. **Filtre Kullanımı:**
   ```bash
   search keyword --type=markdown   # Sadece .md dosyalarda ara
   search keyword --limit=10        # İlk 10 sonucu göster
   search keyword --recent          # Son değişen dosyalarda ara
   ```

3. **Boolean Aramalar:**
   ```bash
   search "django AND model"        # Her iki kelimeyi içeren
   search "react OR vue"           # Herhangi birini içeren
   search "NOT deprecated"         # İçermeyen
   ```

### **Sık Kullanılan Arama Komutları**

```bash
# Dokümantasyon araması:
search "documentation" --type=md
search "README" --type=md
search "guide" --limit=20

# Kod örnekleri:
search "example" --type=py
search "sample" --type=js
search "template" --type=html

# Hata çözümü:
search "error" --recent
search "fix" --limit=30
search "solution" --type=md

# API ve endpoint'ler:
search "API" --type=md
search "endpoint" --type=py
search "route" --type=js
```

---

## 🐛 **Sorun Giderme ve Hata Çözümü**

### **Yaygın Hatalar ve Çözümleri**

#### **1. "FileNotFoundError: No such file or directory"**

**Problem:** main.py dosyası bulunamıyor  
**Çözüm:**
```bash
# Doğru klasöre git:
cd collective-memory-app
ls src/main.py                     # Dosya var mı kontrol et
```

#### **2. "ModuleNotFoundError: No module named 'watchdog'"**

**Problem:** Bağımlılıklar kurulmamış  
**Çözüm:**
```bash
pip install -r requirements.txt
# veya
pip install watchdog colorama pathlib
```

#### **3. "Permission denied" veya "Access denied"**

**Problem:** Dosya izinleri  
**Çözüm:**
```bash
# Linux/Mac:
chmod +x setup.sh
chmod 755 src/main.py

# Windows: PowerShell'i Administrator olarak çalıştır
```

#### **4. "Database locked" hatası**

**Problem:** SQLite veritabanı kilitli  
**Çözüm:**
```bash
# Veritabanı dosyasını sil ve yeniden oluştur:
rm collective_memory.db
python src/main.py --rebuild-db --data-path ../data
```

#### **5. Cursor chat history erişim hatası**

**Problem:** Cursor veritabanına erişim yok  
**Çözüm:**
```bash
# Cursor'ın kapalı olduğundan emin ol
# Yönetici izinleri ile çalıştır
python src/main.py --test-cursor --data-path ../data
```

### **Debug Modu**

```bash
# Detaylı log çıktısı için:
python src/main.py --debug --interactive --data-path ../data

# Log dosyası oluştur:
python src/main.py --interactive --data-path ../data --log-file debug.log
```

---

## 📈 **Performans Optimizasyonu**

### **Sistem Performansını Artırma**

1. **Database Optimizasyonu:**
   ```bash
   python src/main.py --optimize-db --data-path ../data
   ```

2. **İndeks Yenileme:**
   ```bash
   python src/main.py --rebuild-index --data-path ../data
   ```

3. **Cache Temizleme:**
   ```bash
   python src/main.py --clear-cache --data-path ../data
   ```

### **Bellek Kullanımı**

```bash
# Hafif mod (düşük bellek kullanımı):
python src/main.py --memory-efficient --interactive --data-path ../data

# Hızlı mod (yüksek performans):
python src/main.py --high-performance --interactive --data-path ../data
```

---

## 🔐 **Güvenlik ve Gizlilik**

### **Veri Güvenliği**

- Tüm veriler yerel makinenizde saklanır
- Hiçbir veri internete gönderilmez
- Cursor chat geçmişi sadece okunur, değiştirilmez
- SQLite veritabanı şifreleme opsiyonu mevcuttur

### **Güvenlik Ayarları**

```bash
# Veritabanı şifreleme aktif et:
python src/main.py --enable-encryption --data-path ../data

# Yedekleme oluştur:
python src/main.py --backup --data-path ../data
```

---

## 📚 **İleri Seviye Özellikler**

### **API Kullanımı**

```python
# Python kodu içinden kullanım:
from src.collective_memory import CollectiveMemory

cm = CollectiveMemory()
results = cm.search("react component")
print(results)
```

### **Custom Extensions**

```python
# Özel arama filtreleri:
def custom_filter(file_path, content):
    return "react" in content.lower()

cm.add_custom_filter("react_filter", custom_filter)
```

### **Batch Operations**

```bash
# Toplu işlemler:
python src/main.py --batch-search queries.txt --data-path ../data
python src/main.py --batch-index folder/ --data-path ../data
```

---

## 📞 **Destek ve Yardım**

### **Yardım Komutları**

```bash
python src/main.py --help              # Genel yardım
python src/main.py --version           # Versiyon bilgisi
python src/main.py --system-info       # Sistem bilgileri
```

### **Log Dosyaları**

```bash
# Log dosyalarını kontrol et:
tail -f logs/collective-memory.log     # Real-time loglar
cat logs/error.log                     # Hata logları
```

### **Sistem Sağlık Kontrolü**

```bash
python src/main.py --health-check --data-path ../data
```

---

## 🎯 **Sonuç ve Best Practices**

### **En İyi Kullanım Pratikleri:**

1. **Düzenli İnteraktif Kullanım:** `--interactive` modunu tercih edin
2. **Spesifik Aramalar:** Genel kelimeler yerine spesifik terimler kullanın
3. **Filtre Kullanımı:** `--type` ve `--limit` parametrelerini aktif kullanın
4. **Regular Maintenance:** Haftalık `--optimize-db` çalıştırın

### **Performans İpuçları:**

- Büyük projeler için `--memory-efficient` mod kullanın
- Çok sık kullanılan aramalar için alias oluşturun
- Database'i düzenli olarak optimize edin

---

**Bu rehber sürekli güncellenmektedir. Son versiyon için GitHub repository'sine başvurun.** 