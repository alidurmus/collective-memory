# 📤 Output Directory

**Context Engineering Template - Generated Outputs**

Bu klasör, proje sürecinde üretilen tüm çıktıları, raporları ve sonuçları içerir.

## 📁 İçerik Türleri

### 🧪 Test Sonuçları
- `test-results.json` - Playwright UI test sonuçları
- `pytest-results.xml` - Backend test raporları  
- `coverage-report.html` - Test coverage raporu

### 🏗️ Build Artifacts
- `build-logs/` - Build süreç logları
- `dist/` - Distribution dosyaları
- `compiled/` - Derlenmiş dosyalar

### 📊 Raporlar ve Analizler
- `performance-report.json` - Performans analizi
- `security-scan.json` - Güvenlik tarama sonuçları
- `dependency-check.json` - Bağımlılık analizi

### 📈 Metrics
- `code-quality.json` - Kod kalite metrikleri
- `project-stats.json` - Proje istatistikleri
- `usage-analytics.json` - Kullanım analitiği

## 🔄 Otomatik Üretim

Output dosyaları aşağıdaki komutlar tarafından otomatik üretilir:

```bash
# Test runner - test sonuçları üretir
../commands/test-runner.sh

# Setup script - konfigürasyon üretir  
python ../commands/setup.py

# Analysis tools - rapor ve metrikler üretir
npm run analyze
```

## 📋 Dosya Formatları

- **JSON**: Structured data ve API sonuçları
- **XML**: Test framework çıktıları  
- **HTML**: Görsel raporlar ve dashboardlar
- **CSV**: Data export ve analiz
- **Markdown**: Documentation ve raporlar

## ⚠️ Önemli Notlar

- Bu klasördeki dosyalar otomatik üretilir
- Manuel düzenleme önerilmez
- Git'e commit edilmeyebilir (büyük dosyalar)
- Backup gerekirse scripts ile export edin

---

**🔗 İlgili**: [`../commands/`](../commands/) | [`../context/`](../context/) | [`../prompts/`](../prompts/) 