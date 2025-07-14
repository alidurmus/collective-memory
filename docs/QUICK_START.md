# 🚀 Collective Memory - Hızlı Başlangıç Rehberi

**5 dakikada sistemi çalıştırın!** ⚡  
**Version:** 2.1 - Directory Management & Search Export  

---

## 🆕 **YENİ ÖZELLİKLER (v2.1)**

✅ **Otomatik `.collective-memory/` klasörü** - Organize veri yönetimi  
✅ **Arama sonucu kaydetme** - `--save-to` ile dosyaya export  
✅ **Gelişmiş konfigürasyon** - JSON ayar dosyaları  
✅ **Cross-platform uyumluluk** - Windows, macOS, Linux  

---

## 🔥 **En Hızlı Başlangıç**

```bash
# 1. Doğru klasöre gidin (ÖNEMLİ!)
cd collective-memory-app

# 2. Kendi projenizi indeksleyin
python src/main.py --index --data-path "C:\path\to\your\project"
# ✅ Otomatik olarak .collective-memory/ klasörü oluşturulur

# 3. Arama yapın
python src/main.py --search "Django ayarları" --data-path "C:\path\to\your\project"

# 4. Sonuçları kaydedin (YENİ!)
python src/main.py --search "hata çözümü" --save-to "errors.md" --data-path "C:\path\to\your\project"
```

---

## 🚨 **En Yaygın Hata ve Çözümü**

### ❌ **Problem:**
```bash
PS C:\cursor\collective-memory> python src/main.py --interactive --data-path ../data
# Hata: can't open file 'src/main.py': No such file or directory
```

### ✅ **Çözüm:**
```bash
PS C:\cursor\collective-memory> cd collective-memory-app
PS C:\cursor\collective-memory\collective-memory-app> python src/main.py --interactive --data-path "C:\your\project"
# ✅ Başarılı! Sistem .collective-memory/ klasörü oluşturacak
```

### 🔍 **Neden oluyor?**
`main.py` dosyası `collective-memory-app/src/` klasöründe, ana klasörde değil!

---

## ⚡ **4 Adımda Kurulum**

### **Adım 1: Klasöre Gidin**
```bash
cd collective-memory/collective-memory-app
```

### **Adım 2: Projenizi İndeksleyin**
```bash
# Kendi projeniz için
python src/main.py --index --data-path "C:\Users\YourName\MyProject"

# ✅ Otomatik oluşturulur:
# C:\Users\YourName\MyProject\.collective-memory\
#   ├── database/collective_memory.db
#   ├── config/settings.json
#   └── [diğer sistem dosyaları]
```

### **Adım 3: Arama Yapın**
```bash
# Basit arama
python src/main.py --search "anahtar kelime" --data-path "C:\Users\YourName\MyProject"

# Sonuçları dosyaya kaydet (YENİ!)
python src/main.py --search "Django error" --save-to "django-errors.md" --data-path "C:\Users\YourName\MyProject"
```

### **Adım 4: İnteraktif Modu Kullanın**
```bash
# İnteraktif mod başlat
python src/main.py --interactive --data-path "C:\Users\YourName\MyProject"

# Komutlar:
> help         # Yardım
> stats        # İstatistikler
> search term  # Arama
> quit         # Çıkış
```

---

## 📁 **Otomatik Oluşturulan Yapı** ⭐ **YENİ**

Sistem ilk çalıştığında projenizde otomatik oluşturur:

```
[Proje Klasörünüz]/
├── [Mevcut dosyalarınız...]
└── .collective-memory/
    ├── database/
    │   └── collective_memory.db     # Arama veritabanı
    ├── config/
    │   ├── settings.json            # Sistem ayarları
    │   └── project_status.json      # Durum bilgisi
    ├── cache/                       # Arama önbelleği
    ├── logs/                        # Sistem logları
    ├── [search-results].md          # Kaydedilen aramalar
    └── README.md                    # Sistem açıklaması
```

---

## 🔍 **Arama Örnekleri**

### **Temel Arama**
```bash
python src/main.py --search "React component" --data-path "C:\MyProject"
```

### **Arama + Dosyaya Kaydet** ⭐ **YENİ**
```bash
python src/main.py --search "authentication system" --save-to "auth-docs.md" --data-path "C:\MyProject"
# ✅ Sonuç: C:\MyProject\.collective-memory\auth-docs.md
```

### **İstatistik Görüntüleme**
```bash
python src/main.py --stats --data-path "C:\MyProject"
# ✅ Çıktı: Dosya sayısı, boyut, son değişiklikler
```

### **İnteraktif Mod Kullanımı**
```bash
python src/main.py --interactive --data-path "C:\MyProject"

# İnteraktif komutlar:
> search Django settings
> search error handling  
> stats
> help
> quit
```

---

## 💻 **İlk Kullanım Komutları**

Sistem açıldıktan sonra terminal'de:

```bash
help                    # Tüm komutları göster
search "dokumentasyon"  # Dokümantasyon ara
search "API"           # API bilgileri ara
search "error"         # Hata raporları ara
files                  # Tüm dosyaları listele
stats                  # Sistem durumu
exit                   # Çıkış
```

---

## 🐛 **Hızlı Troubleshooting**

### **Problem: Modül bulunamadı**
```bash
pip install watchdog colorama pathlib
```

### **Problem: İzin hatası**
```bash
# Linux/Mac:
chmod +x src/main.py

# Windows: PowerShell'i yönetici olarak çalıştır
```

### **Problem: Python versiyonu**
```bash
python --version  # 3.9+ olmalı
```

---

## 🎯 **En Kullanışlı Özellikler**

### **1. Cursor Chat Geçmişi**
```bash
cursor_history          # Son chatler
cursor_history --limit=20  # Son 20 chat
```

### **2. Gelişmiş Arama**
```bash
search "react component" --limit=10    # Sınırlı sonuç
search "API" --type=markdown          # Sadece .md dosyalarda
```

### **3. Dosya İzleme**
```bash
files --recent          # Son değişen dosyalar
files --count          # Toplam dosya sayısı
```

---

## 🔧 **Sistem Kontrolü**

Herhangi bir sorun yaşıyorsanız:

```bash
# Sistem durumu
python src/main.py --stats --data-path ../data

# Yardım menüsü
python src/main.py --help

# Versiyon kontrolü
python src/main.py --version
```

---

## 📚 **Daha Fazla Bilgi**

- **Detaylı Rehber:** [`USAGE_GUIDE.md`](USAGE_GUIDE.md)
- **Ana Dokümantasyon:** [`../README.md`](../README.md)
- **Sistem Rehberi:** [`../collective-memory.md`](../collective-memory.md)

---

## 🎉 **Başarılı Kurulum Testi**

Sistem doğru çalışıyorsa şu çıktıyı görmelisiniz:

```
╔═══════════════════════════════════════════════════╗
║          Collective Memory v1.0                  ║
║        Cursor AI Akıllı Bağlam Orkestratörü      ║
║      + Dosya İzleme + Arama + İndeksleme        ║
╚═══════════════════════════════════════════════════╝

🔍 Query System Mode - Enhanced Features Active

[2025-01-14 12:00:00] INFO: Database initialized successfully
[2025-01-14 12:00:00] INFO: File monitoring started
[2025-01-14 12:00:00] SUCCESS: System ready!

Collective Memory Terminal (type 'help' for commands)
> 
```

**Tebrikler! Sistem hazır! 🎉**

---

**⚡ Bu rehber 5 dakikada sistemi çalıştırmanız için tasarlandı. Detaylı bilgi için diğer dokümanlara bakın.** 