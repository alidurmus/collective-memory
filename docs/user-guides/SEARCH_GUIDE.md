# 🔍 Arama Rehberi - Collective Memory

**Versiyon:** v2.1  
**Tarih:** 14 Temmuz 2025  
**Kategori:** Kullanıcı Rehberleri  

---

## 🎯 Genel Bakış

Collective Memory sisteminin güçlü arama özelliklerini etkili şekilde kullanmak için hazırlanmış rehber.

## 📋 Arama Türleri

### 1. **Temel Arama**
```bash
python src/main.py --search "Django model" --data-path "C:\projeler"
```

### 2. **Semantic Arama**
```bash
python src/main.py --search "Python hata çözümü" --semantic --data-path "C:\projeler"
```

### 3. **Sonuçları Kaydetme**
```bash
python src/main.py --search "API dokümantasyonu" --save-to "api-docs.md" --data-path "C:\projeler"
```

## 🔧 Arama Filtreleri

### Dosya Türü Filtresi
- `.md` - Markdown dosyalar
- `.py` - Python dosyaları
- `.js` - JavaScript dosyaları
- `.txt` - Metin dosyaları

### Tarih Filtresi
- Son 24 saat
- Son hafta
- Son ay
- Özel tarih aralığı

### Boyut Filtresi
- Küçük dosyalar (< 10KB)
- Orta dosyalar (10KB - 1MB)
- Büyük dosyalar (> 1MB)

## 🎯 Arama İpuçları

### 1. **Etkili Anahtar Kelimeler**
- Spesifik terimler kullanın
- Kısaltmalar yerine tam kelimeler
- Türkçe ve İngilizce karışık arama

### 2. **Boolean Operatörler**
- `VE` - Her iki kelimeyi de içeren
- `VEYA` - Herhangi birini içeren
- `DEĞİL` - İçermeyen

### 3. **Wildcard Kullanımı**
- `*` - Herhangi bir karakter dizisi
- `?` - Tek karakter
- `[abc]` - Belirtilen karakterlerden biri

## 📊 Arama Sonuçları

### Relevance Score
- **0.9-1.0:** Mükemmel eşleşme
- **0.7-0.9:** Yüksek uygunluk
- **0.5-0.7:** Orta uygunluk
- **0.3-0.5:** Düşük uygunluk

### Sonuç Formatı
```
Dosya: path/to/file.md
Score: 0.95
Snippet: "Arama sonucu önizlemesi..."
Boyut: 2.3 KB
Değişiklik: 2 saat önce
```

## 🚀 Gelişmiş Özellikler

### 1. **İnteraktif Arama**
```bash
python src/main.py --interactive --data-path "C:\projeler"
> search "machine learning"
> search "Django settings" --type=py
```

### 2. **Arama Geçmişi**
```bash
> history
> search-history --limit=10
```

### 3. **Kayıtlı Aramalar**
```bash
> save-search "API docs" "API endpoint documentation"
> list-saved-searches
```

## 🔍 Arama Stratejileri

### Kod Araması
```bash
search "class definition" --type=py
search "function implementation" --type=js
search "import statement" --type=py
```

### Dokümantasyon Araması
```bash
search "installation guide" --type=md
search "API reference" --type=md
search "troubleshooting" --type=md
```

### Hata Araması
```bash
search "error" --type=log
search "exception" --type=py
search "bug fix" --type=md
```

## 📈 Performans İpuçları

### 1. **Hızlı Arama**
- Kısa anahtar kelimeler
- Dosya türü filtresi
- Boyut limiti

### 2. **Kapsamlı Arama**
- Uzun anahtar kelimeler
- Semantic arama
- Geniş tarih aralığı

### 3. **Bellek Optimizasyonu**
- Küçük proje klasörleri
- Sık kullanılan terimler
- Cache kullanımı

## 🛠️ Sorun Giderme

### Yaygın Sorunlar
1. **Sonuç Bulunamadı**
   - Anahtar kelimeyi kontrol edin
   - Dosya türü filtresini genişletin
   - Semantic arama deneyin

2. **Yavaş Arama**
   - Daha spesifik terimler
   - Dosya türü filtresi
   - Küçük klasörler

3. **Yanlış Sonuçlar**
   - Daha uzun anahtar kelimeler
   - Boolean operatörler
   - Tam eşleşme modu

## 🎯 Örnekler

### Proje Geliştirme
```bash
# Django projesi
search "Django model" --type=py --save-to "django-models.md"

# React komponenti
search "React component" --type=js --save-to "react-components.md"

# API dokümantasyonu
search "API endpoint" --type=md --save-to "api-endpoints.md"
```

### Hata Çözümü
```bash
# Python hataları
search "Python error" --type=py --save-to "python-errors.md"

# JavaScript hataları
search "JavaScript error" --type=js --save-to "js-errors.md"

# Sistem hataları
search "system error" --type=log --save-to "system-errors.md"
```

---

**📝 Bu rehber sürekli güncellenmektedir. Yeni özellikler eklendiğinde dokümantasyon güncellenecektir.** 