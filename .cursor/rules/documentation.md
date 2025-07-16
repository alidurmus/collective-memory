# 📚 Dokümantasyon Kuralları

## Dokümantasyon Standartları
- **README**: Türkçe + İngilizce paralel
- **API Dokümantasyonu**: İngilizce
- **Kullanıcı Kılavuzu**: Türkçe
- **Kod İçi Dokümantasyon**: İngilizce docstring + Türkçe açıklama

## Test Raporu Organizasyonu
- **Test Raporları**: `docs/reports/test-reports/` altında saklanır
- **Hata Raporları**: `docs/reports/error-reports/` altında saklanır
- **Otomatik Taşıma**: Ana dizinde biriken test sonuçları organize edilir

## Dokümantasyon Klasör Yapısı
```
docs/
├── reports/
│   ├── test-reports/         # Test sonuçları
│   ├── error-reports/        # Hata raporları
│   ├── system-health/        # Sistem sağlık raporları
│   └── analysis-reports/     # Analiz raporları
├── user-guides/              # Kullanıcı kılavuzları
├── technical/                # Teknik dokümantasyon
├── context-engineering/      # Context Engineering Template
└── INDEX.md                  # Dokümantasyon merkezi
```

## Rapor Yazma Kuralları
- **Başlık**: Tarih, saat ve açıklayıcı başlık
- **Durum**: ✅ (başarılı), ❌ (başarısız), 🔄 (devam ediyor)
- **Özet**: Executive summary ile başla
- **Detay**: Test sonuçları, hata açıklamaları, çözüm önerileri 