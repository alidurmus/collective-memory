# ERP Sistemi Test Dokümantasyonu

## 1. Test Ortamı
- **İşletim Sistemi**: Windows 11
- **Python Sürümü**: 3.13.4
- **Django Sürümü**: 5.2.2
- **Test Kütüphaneleri**:
  - pytest
  - pytest-django
  - pytest-cov
  - Selenium

## 2. Test Türleri

### 2.1. Birim Testleri
- **Amaç**: Bireysel fonksiyon ve metodların doğru çalıştığını doğrulamak
- **Kapsam**: 
  - Modeller (Models)
  - Görünümler (Views)
  - Formlar (Forms)
  - Yardımcı Fonksiyonlar

### 2.2. Entegrasyon Testleri
- **Amaç**: Farklı modüllerin birlikte düzgün çalıştığını doğrulamak
- **Kapsam**:
  - Kullanıcı kimlik doğrulama akışı
  - Sipariş işleme süreci
  - Stok yönetimi entegrasyonu

### 2.3. Kullanıcı Arayüzü Testleri
- **Amaç**: Kullanıcı arayüzünün doğru şekilde çalıştığını doğrulamak
- **Araçlar**:
  - Selenium WebDriver
  - Playwright

## 3. Test Senaryoları

### 3.1. Kimlik Doğrulama
```python
# tests/test_authentication.py
def test_user_login(self):
    # Test kodu buraya gelecek
    pass
```

### 3.2. Ürün Yönetimi
```python
# tests/test_products.py
def test_product_creation(self):
    # Test kodu buraya gelecek
    pass
```

## 4. Test Çalıştırma
```bash
# Tüm testleri çalıştır
pytest

# Belirli bir test modülünü çalıştır
pytest tests/test_products.py

# Detaylı çıktı ile çalıştır
pytest -v

# Coverage raporu ile çalıştır
pytest --cov=.

# Belirli bir test sınıfını çalıştır
pytest tests/test_products.py::ProductTests
```

## 5. Test Verileri
Test verileri `fixtures/test_data.json` dosyasında bulunmaktadır. Testler çalıştırılmadan önce bu veriler test veritabanına yüklenmelidir.

## 6. Test Sonuçları
Test sonuçları `htmlcov` klasöründe HTML formatında raporlanmaktadır. Tarayıcıda `htmlcov/index.html` dosyasını açarak detaylı sonuçları görüntüleyebilirsiniz.

## 7. Bilinen Sorunlar
- [ ] Bazı testlerde zaman damgası uyumsuzluğu
- [ ] Çoklu tarayıcı testlerinde senkronizasyon sorunları

## 8. İletişim
Testlerle ilgili sorunlar için:
- E-posta: destek@sirketiniz.com
- İç Sistem: #test-ekibi kanalı
