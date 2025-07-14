# TALIMAT İŞLEME KURALLARI (Instruction Processing Rules)

## Ana Kural: Otomatik Talimat İşleme Süreci

### 1. Talimat Alındığında Uygulanacak Süreç

#### A. Talimat Analizi ve Parçalama
```
1. Gelen talimatı anlamsal olarak parçalara böl
2. Her parçayı sıralı numara ile işaretle
3. Bağımlılıkları belirle (hangi parça diğerine bağlı)
4. Paralel çalıştırılabilecek parçaları tespit et
```

#### B. Terminal Okuma ve Context Toplama
```
1. Her parça için gerekli terminal komutlarını belirle
2. Komutları paralel olarak çalıştır (mümkün olduğunda)
3. Çıktıları analiz et ve context'e ekle
4. Hata durumlarını yakala ve raporla
```

#### C. İşlem Gerçekleştirme
```
1. Toplanan context ile talimatı uygula
2. Her adımda progress raporu ver
3. Başarı/başarısızlık durumlarını belge
4. Sonuçları doğrula
```

### 2. Uygulama Standartları

#### Talimat Parçalama Kriterleri:
- **Teknik Bileşenler**: Frontend, Backend, Database, Testing ayrı parçalar
- **Dosya Operasyonları**: Her dosya grubu ayrı parça
- **Konfigürasyon**: Her konfig türü ayrı parça
- **Test Operasyonları**: Her test türü ayrı parça

#### Terminal Komut Stratejileri:
```bash
# Bilgi Toplama
- codebase_search: Semantic arama
- grep_search: Exact text arama
- file_search: Dosya bulma
- read_file: Dosya okuma
- list_dir: Dizin listeleme

# Analiz Komutları
- git status
- npm ls
- pip list
- docker ps
- systemctl status
```

#### Context Ekleme Formatı:
```
[PARÇA {n}] - {Parça Açıklaması}
Terminal Komutu: {komut}
Çıktı: {sonuç}
Analiz: {değerlendirme}
Sonraki Adım: {action_item}
```

### 3. Workflow Sıralaması

#### Adım 1: Talimat Hazırlığı
1. Talimatı parse et
2. Proje durumunu kontrol et (git status, server status)
3. Gerekli araçları ve dosyaları belirle

#### Adım 2: Bilgi Toplama
1. İlgili dosyaları oku
2. Mevcut konfigürasyonları kontrol et
3. Bağımlılıkları analiz et
4. Test durumlarını kontrol et

#### Adım 3: Uygulama
1. Her parçayı sıralı olarak uygula
2. Bağımlı parçaları önceliklendir
3. Paralel çalışabilecekleri eş zamanlı yap
4. Her adımda sonucu doğrula

#### Adım 4: Doğrulama
1. Değişiklikleri test et
2. Sistemin çalışır durumda olduğunu kontrol et
3. Hata varsa düzelt
4. Sonuçları raporla

### 4. Hata Yönetimi

#### Hata Durumları:
- **Terminal Hatası**: Komutu yeniden dene, alternatif komut kullan
- **Dosya Hatası**: Yetki kontrol et, path doğrula
- **Dependency Hatası**: Kurulumları kontrol et, eksikleri kur
- **Network Hatası**: Bağlantı kontrol et, proxy ayarları kontrol et

#### Hata Çözüm Adımları:
1. Hatayı logla
2. Root cause analizi yap
3. Çözüm stratejisi belirle
4. Uygula ve test et
5. Başarısızlık durumunda kullanıcıya bildir

### 5. Performans Optimizasyonu

#### Paralel İşlem Kuralları:
- **Dosya Okuma**: Tüm dosyaları paralel oku
- **Search Operasyonları**: Farklı pattern'leri paralel ara
- **Test Çalıştırma**: Bağımsız testleri paralel çalıştır
- **Build İşlemleri**: Module'leri paralel build et

#### Cache Stratejileri:
- Dosya içeriklerini session boyunca cache'le
- Komut çıktılarını geçici olarak sakla
- Dependency listelerini cache'le
- Git durumunu periyodik güncelle

### 6. Raporlama Formatı

#### İşlem Başında:
```
🔄 TALIMAT İŞLEME BAŞLADI
📋 Toplam Parça: {count}
⏱️  Tahmini Süre: {estimate}
🎯 Hedef: {objective}
```

#### Her Parça İçin:
```
✅ PARÇA {n} TAMAMLANDI
📊 Context Eklendi: {size}KB
⚡ İşlem Süresi: {duration}s
➡️  Sonraki: Parça {n+1}
```

#### İşlem Sonunda:
```
🎉 TALIMAT TAMAMLANDI
✅ Başarılı Parça: {success_count}
❌ Başarısız Parça: {fail_count}
📈 Toplam Context: {total_context}KB
🕐 Toplam Süre: {total_duration}
```

### 7. Context Engineering Integration

#### Memory System:
- Her işlemi memory'e kaydet
- Başarılı pattern'leri sakla
- Hata pattern'lerini öğren
- Kullanıcı tercihlerini hatırla

#### Template Usage:
- Benzer talimatlar için template oluştur
- Workflow'ları standardize et
- Best practice'leri dokümante et
- Reusable component'ler geliştir

### 8. Kalite Kontrol

#### Pre-Execution Checks:
- [ ] Talimat anlaşıldı mı?
- [ ] Gerekli izinler var mı?
- [ ] Backup durumu kontrol edildi mi?
- [ ] Test environment hazır mı?

#### Post-Execution Validation:
- [ ] Tüm parçalar tamamlandı mı?
- [ ] System çalışır durumda mı?
- [ ] Tests geçiyor mu?
- [ ] Documentation güncellendi mi?

---

## UYGULAMA NOTLARI

### Önemli Hatırlatmalar:
1. **Her zaman paralel işlem önceliği**
2. **Context'i maksimum kullan**
3. **Hata durumlarında proaktif çözüm**
4. **Kullanıcı memory'lerini koru**
5. **Turkish UI / English Code kuralını uygula**

### Teknik Gereksinimler:
- Context7 tools kullanımı [[memory:592593]]
- Playwright testing framework [[memory:592592]]
- Turkish/English language separation [[memory:2176195]]

Bu kurallar her talimat alındığında otomatik olarak uygulanacaktır. 