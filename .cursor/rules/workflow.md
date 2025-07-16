# 🔄 Workflow ve Instruction Processing Kuralları

## Otomatik Talimat İşleme Süreci [[memory:3190909]]

### Ana Süreç Kuralları
1. **Talimat Analizi**: Her talimat anlamsal parçalara bölünür
2. **Terminal Integration**: Her parça için gerekli komutlar çalıştırılır
3. **Context Building**: Komut çıktıları analiz edilip context'e eklenir
4. **Parallel Execution**: Mümkün olan tüm işlemler paralel yapılır
5. **Progress Reporting**: Her adım için detaylı rapor verilir
6. **Validation**: Sonuçlar doğrulanır ve kalite kontrol yapılır

### Workflow Adımları
```
1. ANALIZ AŞAMASI
   ├── Talimatı parse et
   ├── Anlamsal parçalara böl
   ├── Bağımlılıkları belirle
   └── Paralel çalıştırılabilecekleri tespit et

2. BİLGİ TOPLAMA AŞAMASI
   ├── codebase_search: Semantic arama
   ├── grep_search: Exact text arama
   ├── file_search: Dosya bulma
   ├── read_file: Dosya okuma
   └── list_dir: Dizin listeleme

3. UYGULAMA AŞAMASI
   ├── Paralel işlem önceliği
   ├── Bağımlı parçaları önceliklendir
   ├── Her adımda sonucu doğrula
   └── Context'e sürekli ekleme

4. DOĞRULAMA AŞAMASI
   ├── Değişiklikleri test et
   ├── Sistemin çalışır durumunu kontrol et
   ├── Hataları düzelt
   └── Sonuçları raporla
```

### Context Ekleme Formatı
```
[PARÇA {n}] - {Parça Açıklaması}
Terminal Komutu: {komut}
Çıktı: {sonuç}
Analiz: {değerlendirme}
Sonraki Adım: {action_item}
```

### Raporlama Formatı
```
🔄 TALIMAT İŞLEME BAŞLADI
📋 Toplam Parça: {count}
⏱️  Tahmini Süre: {estimate}
🎯 Hedef: {objective}

✅ PARÇA {n} TAMAMLANDI
📊 Context Eklendi: {size}KB
⚡ İşlem Süresi: {duration}s
➡️  Sonraki: Parça {n+1}

🎉 TALIMAT TAMAMLANDI
✅ Başarılı Parça: {success_count}
❌ Başarısız Parça: {fail_count}
📈 Toplam Context: {total_context}KB
🕐 Toplam Süre: {total_duration}
```

## Paralel İşlem Kuralları

### Paralel Çalıştırılabilir İşlemler
- **Dosya Okuma**: Tüm dosyaları paralel oku
- **Search Operations**: Farklı pattern'leri paralel ara
- **Test Running**: Bağımsız testleri paralel çalıştır
- **Build Operations**: Module'leri paralel build et

### Bağımlılık Yönetimi
```python
# ✅ Dependency management örneği
dependency_graph = {
    'task1': [],                    # No dependencies
    'task2': ['task1'],            # Depends on task1
    'task3': ['task1'],            # Depends on task1 
    'task4': ['task2', 'task3'],   # Depends on task2 and task3
}

# Parallel execution order:
# Level 1: task1
# Level 2: task2, task3 (parallel)
# Level 3: task4
```

## Hafıza Yönetimi [[memory:3235989]]

### Hafıza Kontrol Kuralları
- **İşlem Öncesi**: Her talimat alındığında hafızayı kontrol et
- **İlgili Bilgileri Hatırla**: Konuyla ilgili memory'leri getir
- **Context Oluştur**: Hafıza bilgilerini context'e ekle
- **İşlem Yap**: Hazırlanmış context ile talimatı uygula

### Memory Usage Pattern
```
1. MEMORY CHECK
   ├── Talimat konusunu analiz et
   ├── İlgili hafıza kayıtlarını bul
   ├── Memory'leri context'e ekle
   └── Güncel bilgileri kontrol et

2. CONTEXT BUILDING
   ├── Hafıza bilgilerini entegre et
   ├── Mevcut proje durumunu ekle
   ├── İlgili dosyaları okut
   └── Comprehensive context oluştur

3. EXECUTION
   ├── Hazırlanmış context ile çalış
   ├── Hafıza kurallarını uygula
   ├── Sonuçları hafızaya kaydet
   └── Memory'leri güncelle
```

## Hata Yönetimi Kuralları

### Hata Kategorileri
- **Terminal Hatası**: Komutu yeniden dene, alternatif komut kullan
- **Dosya Hatası**: Yetki kontrol et, path doğrula
- **Dependency Hatası**: Kurulumları kontrol et, eksikleri kur
- **Network Hatası**: Bağlantı kontrol et, proxy ayarları kontrol et

### Hata Çözüm Adımları
```
1. HATA TESPİTİ
   ├── Hatayı yakala ve logla
   ├── Hata tipini belirle
   ├── Context bilgilerini topla
   └── Root cause analizi yap

2. ÇÖZÜM STRATEJİSİ
   ├── Alternatif yöntemleri belirle
   ├── Retry mekanizması uygula
   ├── Fallback seçenekleri hazırla
   └── Kullanıcı bilgilendirme planı

3. UYGULAMA VE TEST
   ├── Çözümü uygula
   ├── Sonucu test et
   ├── Başarı durumunu kontrol et
   └── Başarısızlık durumunda escalate et
```

## Performans Optimizasyonu

### Cache Stratejileri
- **Dosya İçeriği**: Session boyunca cache'le
- **Komut Çıktıları**: Geçici olarak sakla
- **Dependency Lists**: Cache'le ve güncelle
- **Git Status**: Periyodik güncelleme

### Monitoring Kuralları
```python
# ✅ Performance monitoring örneği
import time
import psutil

def monitor_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        execution_time = end_time - start_time
        memory_usage = end_memory - start_memory
        
        print(f"⚡ İşlem Süresi: {execution_time:.2f}s")
        print(f"💾 Bellek Kullanımı: {memory_usage / 1024 / 1024:.2f}MB")
        
        return result
    return wrapper
```

## Kalite Kontrol Kuralları

### Pre-Execution Checks
- [ ] Talimat anlaşıldı mı?
- [ ] Gerekli izinler var mı?
- [ ] Backup durumu kontrol edildi mi?
- [ ] Test environment hazır mı?

### Post-Execution Validation
- [ ] Tüm parçalar tamamlandı mı?
- [ ] System çalışır durumda mı?
- [ ] Tests geçiyor mu?
- [ ] Documentation güncellendi mi?

### Context Engineering Integration
- **Memory System**: Her işlemi memory'e kaydet
- **Template Usage**: Benzer talimatlar için template oluştur
- **Best Practices**: Başarılı pattern'leri dokümante et
- **Continuous Improvement**: Sürekli iyileştirme döngüsü 