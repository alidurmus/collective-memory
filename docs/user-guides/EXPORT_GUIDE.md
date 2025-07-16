# 📤 Dışa Aktarma Rehberi - Collective Memory

**Versiyon:** v2.1  
**Tarih:** 14 Temmuz 2025  
**Kategori:** Kullanıcı Rehberleri  

---

## 🎯 Genel Bakış

Collective Memory sistemindeki arama sonuçlarını ve verileri çeşitli formatlarda dışa aktarma rehberi.

## 📋 Desteklenen Formatlar

### 1. **Markdown (.md)**
- Okunabilir format
- GitHub uyumlu
- Bağlantılar ve resimler
- Kod bloğu desteği

### 2. **Plain Text (.txt)**
- Basit metin formatı
- Evrensel uyumluluk
- Küçük dosya boyutu
- Hızlı yükleme

### 3. **JSON (.json)**
- Programatik erişim
- Yapılandırılmış veri
- API entegrasyonu
- Otomatik işlem

### 4. **CSV (.csv)**
- Spreadsheet uyumluluğu
- Tablo formatı
- Excel/Sheets açılabilir
- Veri analizi

## 🔧 Dışa Aktarma Komutları

### Temel Dışa Aktarma
```bash
# Markdown formatında
python src/main.py --search "Django" --save-to "django-docs.md" --data-path "C:\projeler"

# Metin formatında
python src/main.py --search "Python" --save-to "python-docs.txt" --data-path "C:\projeler"

# JSON formatında
python src/main.py --search "API" --save-to "api-docs.json" --data-path "C:\projeler"
```

### Gelişmiş Dışa Aktarma
```bash
# Filtreleme ile
python src/main.py --search "error" --type=py --save-to "python-errors.md" --data-path "C:\projeler"

# Tarih aralığı ile
python src/main.py --search "bug fix" --date-range="2025-01-01,2025-12-31" --save-to "bugs-2025.md" --data-path "C:\projeler"

# Semantic arama ile
python src/main.py --search "machine learning" --semantic --save-to "ml-docs.md" --data-path "C:\projeler"
```

## 📊 Dışa Aktarma Seçenekleri

### Dosya Yapısı
```
[Proje Klasörü]/.collective-memory/
├── exports/
│   ├── search-results/
│   │   ├── django-docs.md
│   │   ├── python-docs.txt
│   │   └── api-docs.json
│   ├── reports/
│   │   ├── daily-report.md
│   │   └── weekly-report.csv
│   └── backups/
│       └── full-backup.json
```

### Otomatik İsimlendirme
```bash
# Tarih damgalı dosyalar
--save-to "search-results-{date}.md"
# Çıktı: search-results-2025-07-14.md

# Sorgu bazlı isimlendirme
--save-to "{query}-results.md"
# Çıktı: Django-results.md
```

## 🚀 Gelişmiş Özellikler

### 1. **Batch Export**
```bash
# Birden fazla arama sonucu
python src/main.py --batch-export searches.txt --data-path "C:\projeler"

# searches.txt içeriği:
# Django models
# Python functions
# API endpoints
```

### 2. **Scheduled Export**
```bash
# Günlük export
python src/main.py --schedule-export daily --format=md --data-path "C:\projeler"

# Haftalık export
python src/main.py --schedule-export weekly --format=csv --data-path "C:\projeler"
```

### 3. **Template Based Export**
```bash
# Özel template kullanma
python src/main.py --search "API" --template="api-report.template" --save-to "api-report.md" --data-path "C:\projeler"
```

## 📝 Export Templates

### Markdown Template
```markdown
# {{title}}

**Arama Sorgusu:** {{query}}  
**Tarih:** {{date}}  
**Sonuç Sayısı:** {{result_count}}

## Sonuçlar

{{#results}}
### {{filename}}
- **Yol:** {{path}}
- **Boyut:** {{size}}
- **Değişiklik:** {{modified}}
- **Score:** {{score}}

{{snippet}}

---
{{/results}}
```

### JSON Template
```json
{
  "search_query": "{{query}}",
  "date": "{{date}}",
  "result_count": {{result_count}},
  "results": [
    {{#results}}
    {
      "filename": "{{filename}}",
      "path": "{{path}}",
      "size": "{{size}}",
      "modified": "{{modified}}",
      "score": {{score}},
      "snippet": "{{snippet}}"
    }{{#unless @last}},{{/unless}}
    {{/results}}
  ]
}
```

## 🔍 Console Entegrasyonu

### Console ile Export
```bash
comprehensive> doc-export DOC_ID --format=md --output="exported-doc.md"
comprehensive> search-export "Django models" --format=json --output="django-models.json"
comprehensive> batch-export --query-file="searches.txt" --format=csv
```

### Otomatik Export
```bash
# Otomatik sistem raporu
comprehensive> auto-export --type=system-report --schedule=daily

# Otomatik hata raporu
comprehensive> auto-export --type=error-report --schedule=weekly
```

## 📈 Export Metrikleri

### Dosya Boyutu
- **Markdown:** Orta boyut, okunabilir
- **JSON:** Küçük boyut, yapılandırılmış
- **CSV:** Çok küçük, tablo formatı
- **TXT:** En küçük, basit metin

### Performans
- **Hızlı:** TXT, CSV
- **Orta:** Markdown
- **Yavaş:** JSON (büyük veri setleri)

### Uyumluluk
- **Evrensel:** TXT
- **Geliştirici:** JSON
- **Dokümantasyon:** Markdown
- **Analiz:** CSV

## 🛠️ Sorun Giderme

### Yaygın Sorunlar

1. **Dosya Oluşturulamadı**
   ```bash
   # Çözüm: Yazma izni kontrol et
   ls -la .collective-memory/exports/
   chmod 755 .collective-memory/exports/
   ```

2. **Büyük Dosya Boyutu**
   ```bash
   # Çözüm: Filtreleme kullan
   --limit=50 --type=md --date-range="2025-07-01,2025-07-31"
   ```

3. **Bozuk Format**
   ```bash
   # Çözüm: Template kontrol et
   --template="default.template" --validate
   ```

## 🎯 Kullanım Örnekleri

### Proje Dokümantasyonu
```bash
# API dokümantasyonu
python src/main.py --search "API endpoint" --save-to "api-docs.md" --data-path "C:\projeler"

# Hata dokümantasyonu
python src/main.py --search "error solution" --save-to "error-fixes.md" --data-path "C:\projeler"
```

### Rapor Oluşturma
```bash
# Günlük rapor
python src/main.py --daily-report --save-to "daily-report-{date}.md" --data-path "C:\projeler"

# Haftalık özet
python src/main.py --weekly-summary --save-to "weekly-summary.csv" --data-path "C:\projeler"
```

### Yedekleme
```bash
# Tam yedekleme
python src/main.py --full-backup --save-to "backup-{date}.json" --data-path "C:\projeler"

# Seçili yedekleme
python src/main.py --backup-search "important" --save-to "important-backup.json" --data-path "C:\projeler"
```

---

**📝 Bu rehber tüm dışa aktarma özelliklerini kapsar. Yeni formatlar eklendiğinde güncellenir.** 