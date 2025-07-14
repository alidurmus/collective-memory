# Collective Memory v2.1 User Guide

Collective Memory ile bilgi yönetimi ve akıllı arama için kapsamlı kullanıcı kılavuzunuz.

## 🎯 Collective Memory Nedir?

Collective Memory, AI destekli gelişmiş bir bilgi yönetimi ve arama sistemidir. Belgelerinizi otomatik olarak indeksler, akıllı arama yetenekleri sağlar ve modern bir web arayüzü ile kolay erişim sunar.

### Temel Özellikler

- **🔍 Akıllı Arama**: Hem temel hem de semantik arama
- **🤖 AI Destekli**: Makine öğrenmesi ile alakalı sonuçlar  
- **⚡ Hızlı İndeksleme**: Otomatik dosya keşfi ve indeksleme
- **🌐 Modern Arayüz**: React tabanlı web dashboard
- **📊 Analytics**: Detaylı kullanım istatistikleri
- **🔄 Real-time**: Canlı güncellemeler ve bildirimler

## 🚀 Hızlı Başlangıç

### 1. Sistem Başlatma

#### Web Dashboard (Önerilen)

```bash
# 1. Backend server'ı başlatın
python api_server.py

# 2. Yeni terminal'de frontend'i başlatın
cd frontend
npm run dev

# 3. Web tarayıcınızda açın
# http://localhost:5173
```

#### Komut Satırı (CLI)

```bash
# Mevcut dizini indeksle
python main.py

# Belirli klasörü indeksle
python main.py --data-folder /home/user/documents

# Arama yap
python main.py --search "machine learning"

# Sonuçları kaydet
python main.py --search "Django models" --save-to results.md
```

### 2. İlk Kurulum

1. **Veri Klasörü Belirleme**: İndekslemek istediğiniz ana klasörü seçin
2. **İlk İndeksleme**: Sistem dosyalarınızı otomatik tarar
3. **Arama Testi**: İlk aramanızı yaparak sistemi test edin

## 🌐 Web Dashboard Kullanımı

### Ana Sayfa (Dashboard)

#### Sistem Durumu
- **Yeşil Badge**: Sistem normal çalışıyor
- **Sarı Badge**: Dikkat gerektiren durum
- **Kırmızı Badge**: Sistem sorunu var

#### İstatistik Kartları
- **Toplam Dosya**: İndekslenmiş dosya sayısı
- **Toplam Boyut**: İndekslenmiş veri boyutu
- **Son Arama**: En son arama zamanı
- **Sistem Durumu**: Genel sağlık durumu

#### Hızlı İşlemler
- **Yeniden İndeksle**: Tüm dosyaları tekrar tara
- **Cache Temizle**: Arama cache'ini temizle
- **Ayarlara Git**: Sistem konfigürasyonu

#### Son Aktiviteler
- Yapılan aramaların geçmişi
- İndeksleme işlemleri
- Sistem olayları

### 🔍 Arama Sayfası

#### Temel Arama

1. **Arama Kutusuna** terimi yazın
2. **Arama Türü** olarak "Basic" seçin
3. **"Ara" butonuna** tıklayın

```
Örnek: "Python function"
```

**Temel arama özellikleri:**
- Exact kelime eşleşmesi
- Joker karakterler: `*`, `?`
- Boolean operatörler: `AND`, `OR`, `NOT`
- Phrase arama: `"exact phrase"`

#### Semantik Arama (AI Destekli)

1. **Arama türü** olarak "Semantic" seçin
2. **Doğal dil** kullanarak arama yapın
3. **Threshold** değerini ayarlayın (0.5-0.9)

```
Örnek: "makine öğrenmesi algoritmaları"
```

**Semantik arama özellikleri:**
- Kavramsal anlama
- Eş anlamlı kelime tanıma
- Context-aware sonuçlar
- Relevance scoring

#### Gelişmiş Arama Seçenekleri

**Dosya Türü Filtreleri:**
- ✅ Python dosyaları (.py)
- ✅ JavaScript dosyaları (.js, .ts)
- ✅ Markdown dosyaları (.md)
- ✅ Text dosyaları (.txt)
- ✅ JSON dosyaları (.json)

**Tarih Filtreleri:**
- Son 24 saat
- Son hafta  
- Son ay
- Özel aralık

**Boyut Filtreleri:**
- Küçük dosyalar (< 10KB)
- Orta dosyalar (10KB - 100KB)  
- Büyük dosyalar (> 100KB)

#### Arama Sonuçları

**Sonuç Kartı Bilgileri:**
- **Dosya Adı**: Clickable link
- **Dosya Yolu**: Full path to file
- **Relevance Score**: 0.0-1.0 arası
- **Dosya Boyutu**: Human readable format
- **Son Düzenleme**: Timestamp
- **Content Snippet**: Eşleşen kısım

**Sıralama Seçenekleri:**
- Relevance (Varsayılan)
- Dosya adı (A-Z)
- Boyut (Küçük->Büyük)
- Tarih (Yeni->Eski)

#### Arama Geçmişi

- **Son aramalar** otomatik kaydedilir
- **History** butonundan erişim
- **Favori aramalar** yıldızlama
- **Export** özelliği ile backup

### 📊 Analytics Sayfası

#### Performans Metrikleri

**Sistem Performansı:**
- Ortalama arama süresi
- Toplam arama sayısı
- Cache hit oranı
- İndeks büyüklüğü

**Kullanım İstatistikleri:**
- Günlük arama grafiği
- Saatlik dağılım
- Popüler arama terimleri
- Dosya türü dağılımı

#### Popüler Aramalar

En çok aranan terimler:
1. **machine learning** (145 arama)
2. **React components** (89 arama)
3. **Django models** (67 arama)

#### Sistem Kaynakları

**Real-time Monitoring:**
- CPU kullanımı (%)
- Memory kullanımı (MB)
- Disk kullanımı (GB)
- Network trafiği

### ⚙️ Ayarlar Sayfası

#### Genel Ayarlar

**Tema Seçenekleri:**
- 🌞 Light Mode
- 🌙 Dark Mode  
- 🔄 Auto (Sistem teması)

**Dil Seçenekleri:**
- 🇹🇷 Türkçe
- 🇺🇸 English

**Bildirim Ayarları:**
- ✅ Desktop bildirimleri
- ✅ Email bildirimleri
- ✅ Push bildirimleri

#### Arama Ayarları

**Varsayılan Arama Türü:**
- Basic Search
- Semantic Search

**Semantik Arama:**
- Threshold: 0.7 (0.5-0.9)
- Model: all-MiniLM-L6-v2

**Sonuç Ayarları:**
- Maksimum sonuç: 50
- Snippet uzunluğu: 200 karakter
- Cache süresi: 30 dakika

#### Sistem Ayarları

**İndeksleme:**
- ✅ Otomatik indeksleme
- 📁 İzlenen klasörler
- 🕐 İndeksleme aralığı: 1 saat
- 📄 Max dosya boyutu: 100MB

**Performans:**
- Worker thread sayısı: 4
- Memory limiti: 2GB
- ✅ Multi-threading
- ✅ Cache aktif

**Güvenlik:**
- ✅ Rate limiting
- 🔐 API key koruması
- 📊 Audit logging

## 🔧 Gelişmiş Kullanım

### Arama İpuçları

#### Temel Arama Operators

```bash
# AND operatörü
"Python AND Django"

# OR operatörü  
"React OR Vue"

# NOT operatörü
"JavaScript NOT jQuery"

# Phrase arama
"machine learning algorithm"

# Wildcard
"function*"  # function, functions, functionality
"test?"      # test, tests

# Field-specific arama (gelecek versiyon)
filename:models.py
path:/home/user/projects/
type:python
size:>100KB
modified:2024-01-01..2024-12-31
```

#### Semantik Arama İpuçları

```bash
# Doğal dil kullanın
"Nasıl bir API oluşturabilirim?"

# Kavramsal arama
"veri analizi ve görselleştirme"

# Problem tanımı
"memory leak hatası çözümü"

# Teknoloji kombinasyonu  
"React ile backend bağlantısı"
```

### Sonuç Export Işlemleri

#### Markdown Export

```markdown
# Search Results for "Django models"

## Summary
- **Query**: Django models  
- **Results**: 15 files found
- **Search time**: 45ms
- **Generated**: 2025-01-15 10:30:00

## Results

### 1. models.py (Score: 0.98)
**Path**: `/project/django_app/models.py`
**Size**: 5.2 KB
**Modified**: 2024-12-10

Django model definitions for the application...

[Content snippet...]

### 2. admin.py (Score: 0.85)
...
```

#### Text Export

```text
COLLECTIVE MEMORY SEARCH RESULTS
================================

Query: Django models
Results: 15 files found  
Search time: 45ms
Generated: 2025-01-15 10:30:00

1. models.py (Score: 0.98)
   Path: /project/django_app/models.py
   Size: 5.2 KB
   Modified: 2024-12-10
   
   Django model definitions for the application...

2. admin.py (Score: 0.85)
   ...
```

### Keyboard Shortcuts

| Shortcut | Açıklama |
|----------|----------|
| `Ctrl+K` | Hızlı arama |
| `Ctrl+/` | Arama geçmişi |
| `Ctrl+E` | Export menüsü |
| `Ctrl+,` | Ayarlar sayfası |
| `F5` | Sayfa yenile |
| `Esc` | Modal'ları kapat |
| `Tab` | Sonuçlar arası geçiş |
| `Enter` | Seçili sonuca git |

## 📱 Mobil Kullanım

### Responsive Design

Collective Memory tüm cihazlarda optimize edilmiştir:

- **📱 Mobil (320px+)**: Touch-friendly arayüz
- **📱 Tablet (768px+)**: Optimized layout
- **🖥️ Desktop (1024px+)**: Full feature set

### Mobil Özellikler

- Touch gestures
- Swipe navigation
- Mobile-optimized search
- Offline cache support

### PWA Support (Gelecek)

- Install to home screen
- Offline functionality  
- Push notifications
- Background sync

## 🔐 Güvenlik ve Gizlilik

### Veri Güvenliği

- **Local-first**: Tüm veriler lokal olarak saklanır
- **No cloud sync**: İnternet bağlantısı gerekmez
- **Encrypted cache**: Hassas veriler şifrelenir
- **Access control**: Dosya izinleri korunur

### Gizlilik

- **No tracking**: Kullanıcı takibi yapılmaz
- **No analytics**: Kişisel veri toplanmaz
- **Local processing**: AI modeller lokal çalışır
- **Opt-in telemetry**: İsteğe bağlı telemetri

## 🚀 Performans Optimizasyonu

### Sistem Gereksinimleri

**Minimum:**
- CPU: 2 cores, 2.4 GHz
- RAM: 4 GB
- Storage: 10 GB SSD
- OS: Windows 10, macOS 10.15, Ubuntu 18.04

**Önerilen:**
- CPU: 4 cores, 3.0 GHz  
- RAM: 8 GB
- Storage: 50 GB NVMe SSD
- OS: Latest versions

### Performans İpuçları

#### Hızlı Arama İçin

1. **Specific terms kullanın**: "func" yerine "function"
2. **Threshold'ı ayarlayın**: 0.7-0.8 optimal
3. **File type filtresi**: Gereksiz türleri hariç tutun
4. **Cache'i aktif tutun**: Repeated searches için

#### İndeksleme Optimizasyonu

1. **Exclude patterns**: `.git`, `node_modules`, `__pycache__`
2. **File size limit**: 100MB altı dosyalar
3. **Watch mode**: Sadece gerekli klasörler
4. **Scheduled indexing**: Peak saatlerin dışı

#### Memory Management

1. **Worker threads**: CPU core sayısına göre ayarla
2. **Cache limit**: RAM'in %25'i kadar
3. **Semantic model**: Küçük model seç
4. **Cleanup**: Düzenli cache temizliği

## 📞 Destek ve Yardım

### Yaygın Sorunlar

#### "Arama sonucu bulunamadı"

1. **Spelling kontrol**: Yazım hatası var mı?
2. **Synonyms dene**: Eş anlamlı kelimeler
3. **Broader terms**: Daha genel terimler
4. **File filters**: Filtreler çok kısıtlayıcı mı?

#### "Sistem yavaş çalışıyor"

1. **Cache clear**: Settings > Clear cache
2. **Reindex**: Settings > Reindex files
3. **Resource check**: Task manager kontrol
4. **Restart**: Frontend ve backend restart

#### "Dosyalar indekslenmiyor"

1. **Path check**: Dosya yolu erişilebilir mi?
2. **Permissions**: Okuma izinleri var mı?
3. **File size**: Size limit aşılmış mı?
4. **Extensions**: Desteklenen format mı?

### Kaynak Bağlantıları

- **📚 Dokümantasyon**: `/docs` klasörü
- **🐛 Bug Reports**: GitHub Issues
- **💬 Discussions**: GitHub Discussions  
- **📧 Email**: support@collective-memory.dev
- **🎥 Video Tutorials**: YouTube playlist

### Community

- **GitHub**: Star ve watch repository
- **Discord**: Community chat (gelecek)
- **Reddit**: r/CollectiveMemory (gelecek)
- **Twitter**: @CollectiveMemory (gelecek)

## 🔮 Roadmap

### v2.2 (Gelecek Çeyrek)

- **🔐 Authentication**: User accounts ve permissions
- **🌐 Multi-language**: Arayüz çevirisi
- **📱 PWA**: Progressive Web App
- **🔗 Integrations**: VS Code, Notion, Obsidian
- **📊 Advanced Analytics**: Machine learning insights

### v2.3 (Gelecek Yarı Yıl)

- **☁️ Cloud Sync**: Optional cloud backup
- **👥 Collaboration**: Team sharing features
- **🎨 Custom Themes**: Theme marketplace
- **🔌 Plugin System**: Extension framework
- **📈 Enterprise**: Advanced features for teams

---

**Collective Memory v2.1 ile verimli bilgi yönetimi deneyimi yaşayın! Sorularınız için community kaynaklarımızı kullanın.** 🚀 