# 📚 Collective Memory - Dokümantasyon İndeksi

**Collective Memory Sistemi için kapsamlı dokümantasyon rehberi**  
**Version:** 2.1 - Enhanced Directory Management & Search Export  

---

## 🆕 **YENİ ÖZELLİKLER (v2.1)**

✅ **Otomatik Klasör Yönetimi** - `.collective-memory/` dizin yapısı  
✅ **Arama Sonucu Dışa Aktarma** - `--save-to filename.md` parametresi  
✅ **Gelişmiş Konfigürasyon** - JSON ayar dosyaları  
✅ **Cross-platform Uyumluluk** - Windows, macOS, Linux desteği  

---

## 🚀 **Hızlı Başlangıç**

### **İlk Kez Kullanıcılar İçin:**
1. **[Hızlı Başlangıç Rehberi](QUICK_START.md)** ⚡ - 5 dakikada sistemi çalıştırın (v2.1 güncel)
2. **[Detaylı Kullanım Rehberi](USAGE_GUIDE.md)** 📖 - Kapsamlı kullanım talimatları (v2.1 güncel)

### **Sistem Yöneticileri İçin:**
1. **[Ana README](../README.md)** 🏠 - Proje genel bakışı (v2.1 güncel)
2. **[Teknoloji Stack'i](../techstack.md)** 🔧 - Teknik detaylar (v2.1 güncel)
3. **[Sistem Rehberi](../collective-memory.md)** 🧠 - Kapsamlı sistem dokümantasyonu (v2.1 güncel)

---

## 📖 **Dokümantasyon Rehberleri**

### **🚀 Kullanıcı Rehberleri**
| Dosya | Açıklama | Hedef Kitle | Versiyon |
|-------|----------|-------------|----------|
| **[QUICK_START.md](QUICK_START.md)** | 5 dakikalık hızlı başlangıç | Yeni kullanıcılar | v2.1 ✅ |
| **[USAGE_GUIDE.md](USAGE_GUIDE.md)** | Detaylı kullanım rehberi | Tüm kullanıcılar | v2.1 ✅ |

### **🔧 Teknik Dokümantasyon**
| Dosya | Açıklama | Hedef Kitle | Versiyon |
|-------|----------|-------------|----------|
| **[../README.md](../README.md)** | Ana proje dokümantasyonu | Geliştiriciler | v2.1 ✅ |
| **[../techstack.md](../techstack.md)** | Teknoloji stack detayları | Teknik ekip | v2.1 ✅ |
| **[../collective-memory.md](../collective-memory.md)** | Sistem mimarisi | Sistem yöneticileri | v2.1 ✅ |

### **📋 Planlama ve Proje**
| Dosya | Açıklama | Hedef Kitle | Durum |
|-------|----------|-------------|-------|
| **[../PRD.md](../PRD.md)** | Ürün gereksinimleri | Proje yöneticileri | Aktif |
| **[todo.md](todo.md)** | Görev listesi ve planlama | Geliştirme ekibi | Güncel |

---

## 🎯 **Kullanım Senaryolarına Göre Rehberler**

### **🆘 Sorun Yaşıyorsanız:**
1. **[QUICK_START.md](QUICK_START.md)** - En yaygın hatalar ve çözümleri (v2.1 güncel)
2. **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Troubleshooting bölümü (v2.1 güncel)

### **📖 İlk Kez Öğreniyorsanız:**
1. **[../README.md](../README.md)** - Proje hakkında genel bilgi (v2.1 güncel)

### **⚡ Hemen Başlamak İstiyorsanız:**
```bash
# 1. Doğru klasöre gidin
cd collective-memory-app

# 2. Projenizi indeksleyin  
python src/main.py --index --data-path "C:\your\project"

# 3. Arama yapın ve kaydedin (YENİ!)
python src/main.py --search "anahtar kelime" --save-to "results.md" --data-path "C:\your\project"
```

### **🔧 Gelişmiş Özellikler:**
- **Otomatik klasör yapısı** - `.collective-memory/` organizasyonu ⭐ **YENİ**
- **Arama sonuçları export** - Markdown dosyalarına kaydetme ⭐ **YENİ**  
- **İnteraktif mod** - Terminal-based sorgu arayüzü
- **Cross-platform** - Windows/macOS/Linux uyumluluğu ⭐ **YENİ**

---

## 🗂️ **Proje Dokümantasyon Yapısı**

```
collective-memory/
├── 📄 README.md                    # Ana proje dokümantasyonu
├── 📄 collective-memory.md         # Kapsamlı sistem rehberi
├── 📄 techstack.md                 # Teknoloji stack dokümantasyonu
├── 📄 PRD.md                       # Ürün gereksinimleri dokümanı
├── 📂 docs/                        # Kullanıcı dokümantasyonu
│   ├── 📄 README.md               # Bu dosya - dokümantasyon indeksi
│   ├── 📄 QUICK_START.md          # Hızlı başlangıç rehberi
│   ├── 📄 USAGE_GUIDE.md          # Detaylı kullanım rehberi
│   └── 📄 todo.md                 # Görev listesi
├── 📂 collective-memory-app/       # ANA UYGULAMA (asıl sistem)
│   ├── 📄 README.md               # Uygulama dokümantasyonu
│   └── 📂 docs/                   # Teknik dokümantasyon
└── 📂 data/                        # 📋 DEMO/TEST KLASÖRÜ (örnek içerik)
    └── 📂 docs/                    # Örnek dokümantasyon
```

---

## 🔍 **Hızlı Erişim Linkleri**

### **En Çok Kullanılan Dokümantasyon:**
- **[Hızlı Başlangıç](QUICK_START.md)** - İlk kurulum için
- **[Kullanım Rehberi](USAGE_GUIDE.md)** - Tüm özellikler için
- **[Ana README](../README.md)** - Proje genel bakışı için
- **[Data Klasörü Açıklaması](DATA_USAGE_NOTE.md)** - `/data` klasörünün rolü

### **Sorun Giderme:**
- **[QUICK_START.md - Troubleshooting](QUICK_START.md#-hızlı-troubleshooting)**
- **[USAGE_GUIDE.md - Hata Çözümü](USAGE_GUIDE.md#-sorun-giderme-ve-hata-çözümü)**

### **Gelişmiş Özellikler:**
- **[USAGE_GUIDE.md - Gelişmiş Kullanım](USAGE_GUIDE.md#-gelişmiş-kullanım-senaryoları)**
- **[collective-memory.md](../collective-memory.md)** - Sistem detayları

---

## 📊 **Dokümantasyon Durumu**

| Dokümantasyon | Durum | Son Güncelleme |
|---------------|-------|----------------|
| README.md | ✅ Tamamlandı | 14 Ocak 2025 |
| QUICK_START.md | ✅ Tamamlandı | 14 Ocak 2025 |
| USAGE_GUIDE.md | ✅ Tamamlandı | 14 Ocak 2025 |
| collective-memory.md | ✅ Tamamlandı | 14 Ocak 2025 |
| techstack.md | ✅ Tamamlandı | 14 Ocak 2025 |
| PRD.md | ✅ Tamamlandı | 13 Temmuz 2025 |

---

## 🤝 **Katkıda Bulunma**

Dokümantasyonu geliştirmek için:

1. **Hata Bildirimi:** Yanlış bilgi bulursanız issue açın
2. **İyileştirme Önerisi:** Pull request gönderin
3. **Eksik Konu:** Hangi konuların eksik olduğunu belirtin

### **Dokümantasyon Standartları:**
- Türkçe kullanıcı arayüzü, İngilizce kod tanımlamaları [[memory:2176195]]
- Context7 framework standartlarına uygun [[memory:592593]]
- Playwright kullanarak test edilen örnekler [[memory:592592]]

---

## 📞 **Destek ve İletişim**

- **GitHub Issues:** Teknik sorular için
- **GitHub Discussions:** Genel tartışmalar için
- **Dokümantasyon Geri Bildirimi:** Pull request ile

---

**🎯 Bu dokümantasyon sistemi, Collective Memory projesinin tüm özelliklerini etkin şekilde kullanmanız için tasarlanmıştır.** 