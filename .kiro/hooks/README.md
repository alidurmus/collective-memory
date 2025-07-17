# 🎣 Collective Memory Agent Hooks

Agent Hooks sistemi, geliştirme sürecinde otomatik işlemler gerçekleştiren akıllı tetikleyicilerdir.

## 🚀 Hızlı Başlangıç

### Windows'ta Başlatma
```bash
# Hook manager'ı başlat
.kiro/hooks/start-hooks.bat

# Veya manuel olarak
python .kiro/hooks/scripts/hook-manager.py start
```

### Durum Kontrolü
```bash
python .kiro/hooks/scripts/hook-manager.py status
```

### Manuel Hook Çalıştırma
```bash
python .kiro/hooks/scripts/hook-manager.py test <hook_id>
```

## 📋 Aktif Hook'lar

### 🔄 Otomatik Tetiklenen Hook'lar

| Hook | Tetikleyici | Açıklama |
|------|-------------|----------|
| **Otomatik Test Çalıştırma** | Dosya kaydedildiğinde | Python/JS dosyaları kaydedildiğinde ilgili testleri çalıştırır |
| **Kod Formatlama** | Dosya kaydedildiğinde | Black (Python) ve Prettier (JS) ile kodu formatlar |
| **API Dokümantasyon** | API dosyası değiştiğinde | API dokümantasyonunu otomatik günceller |
| **Güvenlik Taraması** | Dependency değiştiğinde | requirements.txt/package.json değiştiğinde güvenlik tarar |
| **Migration Kontrolü** | Model dosyası değiştiğinde | Django migration gereksinimini kontrol eder |
| **Çeviri Güncelleme** | UI dosyası değiştiğinde | Türkçe çeviri dosyalarını günceller |

### ⏰ Zamanlanmış Hook'lar

| Hook | Zamanlama | Açıklama |
|------|-----------|----------|
| **Sistem Sağlık Kontrolü** | Her 6 saatte | Disk, RAM, veritabanı durumunu kontrol eder |
| **Geçici Dosya Temizleme** | Her gün 02:00 | Cache ve geçici dosyaları temizler |

### 🔘 Manuel Hook'lar

| Hook | Komut | Açıklama |
|------|-------|----------|
| **Test Raporu Oluşturma** | `test generate-test-report` | Kapsamlı test raporu oluşturur |
| **Yazım Kontrolü** | `test spell-check-docs` | Dokümantasyon yazım kontrolü |
| **Veritabanı Yedekleme** | `test backup-database` | Veritabanını yedekler |

## 🔧 Hook Konfigürasyonu

Hook'lar `.kiro/hooks/hooks.json` dosyasında tanımlanır:

```json
{
  "hooks": [
    {
      "id": "auto-test-on-save",
      "name": "Otomatik Test Çalıştırma",
      "description": "Python veya JavaScript dosyası kaydedildiğinde testleri çalıştırır",
      "trigger": {
        "type": "file_save",
        "patterns": ["**/*.py", "**/*.js", "**/*.ts"]
      },
      "enabled": true,
      "actions": [
        {
          "type": "run_tests",
          "config": {
            "python_command": "python -m pytest tests/ -v --tb=short",
            "javascript_command": "npm test",
            "timeout": 30000
          }
        }
      ]
    }
  ]
}
```

## 📊 Raporlama

Hook'lar çalıştıkça otomatik raporlar oluşturur:

- **Test Raporları**: `docs/reports/test-reports/`
- **Güvenlik Raporları**: `docs/reports/security-reports/`
- **Sistem Sağlık**: `docs/reports/system-health/`
- **Performans**: `docs/reports/performance-reports/`

## 🎯 Hook Türleri

### 1. File Save Hooks
Dosya kaydedildiğinde tetiklenir:
```json
{
  "trigger": {
    "type": "file_save",
    "patterns": ["**/*.py", "**/*.js"]
  }
}
```

### 2. Scheduled Hooks
Belirli zamanlarda çalışır:
```json
{
  "trigger": {
    "type": "scheduled",
    "schedule": "0 */6 * * *"
  }
}
```

### 3. Manual Hooks
Manuel tetiklenir:
```json
{
  "trigger": {
    "type": "manual",
    "button_text": "Test Raporu Oluştur"
  }
}
```

## 🛠️ Özelleştirme

### Yeni Hook Ekleme

1. `hooks.json`'a yeni hook tanımı ekleyin
2. Gerekirse `hook-manager.py`'da yeni action türü implement edin
3. Hook manager'ı yeniden başlatın

### Hook Devre Dışı Bırakma

```json
{
  "id": "hook-id",
  "enabled": false
}
```

## 🔍 Troubleshooting

### Hook Çalışmıyor
1. Hook manager'ın çalıştığını kontrol edin: `python .kiro/hooks/scripts/hook-manager.py status`
2. Hook'un enabled olduğunu kontrol edin
3. Pattern'lerin doğru olduğunu kontrol edin

### Performans Sorunları
1. Çok fazla hook aktifse bazılarını devre dışı bırakın
2. `global_settings.max_concurrent_hooks` değerini azaltın
3. File pattern'leri daha spesifik yapın

### Hata Logları
Hook hataları konsola yazdırılır. Detaylı loglar için:
```bash
python .kiro/hooks/scripts/hook-manager.py start > hooks.log 2>&1
```

## 📈 Performans Metrikleri

Hook sistemi şu performans hedeflerini karşılar:

- **Dosya değişiklik tespiti**: <50ms
- **Hook tetikleme**: <100ms
- **Test çalıştırma**: <30s (timeout)
- **Bellek kullanımı**: <50MB
- **CPU kullanımı**: <%5 (idle durumda)

## 🤝 Katkıda Bulunma

Yeni hook türleri veya iyileştirmeler için:

1. Hook önerinizi issue olarak açın
2. Implementation'ı geliştirin
3. Test edin ve dokümante edin
4. Pull request gönderin

---

**🎯 Agent Hooks ile geliştirme sürecinizi otomatikleştirin ve verimliliğinizi artırın!**