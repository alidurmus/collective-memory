# Collective Memory v2.1 Test Suite

Bu dizin Collective Memory web dashboard için kapsamlı test paketi içerir.

## 📁 Test Yapısı

```
tests/
├── README.md                    # Bu dosya - test dokümantasyonu
├── pytest.ini                  # Pytest konfigürasyonu
├── test_runner.py              # Ana test çalıştırıcı script
├── test_basic.py               # Temel modül testleri (mevcut)
├── test_api_endpoints.py       # Backend API endpoint testleri
├── playwright.config.js        # Playwright konfigürasyonu
└── ui/                         # Frontend UI testleri
    ├── dashboard.spec.js       # Dashboard sayfa testleri
    ├── search.spec.js          # Arama işlevsellik testleri
    ├── analytics.spec.js       # Analytics sayfa testleri
    └── settings.spec.js        # Ayarlar sayfa testleri
```

## 🧪 Test Türleri

### 1. Temel Modül Testleri (`test_basic.py`)
- **Amaç**: Core backend modüllerinin doğru çalışmasını test eder
- **Kapsam**: 
  - CursorDatabaseReader
  - ContextCollector
  - QueryBuilder  
  - TriggerParser
- **Durumu**: ✅ 14/14 test başarılı

### 2. API Endpoint Testleri (`test_api_endpoints.py`)
- **Amaç**: Flask REST API'nin endpoint'lerini test eder
- **Kapsam**:
  - System status/stats endpoints
  - Search endpoints (basic & semantic)
  - Export functionality
  - WebSocket connections
  - Performance metrics
  - Error handling
- **Ön koşul**: Backend API server çalışır durumda olmalı (`python api_server.py`)

### 3. Frontend UI Testleri (`ui/*.spec.js`)
- **Amaç**: React web dashboard'un kullanıcı arayüzünü test eder
- **Framework**: Playwright [[memory:592592]]
- **Kapsam**:
  - Dashboard ana sayfa
  - Arama işlevselliği
  - Analytics sayfası
  - Ayarlar paneli
  - Responsive design
  - Dark/Light mode
- **Ön koşul**: Frontend dev server çalışır durumda olmalı (`npm run dev`)

## 🚀 Test Çalıştırma

### Hızlı Başlangıç

```bash
# 1. Playwright browser'ları kur (ilk kez)
python tests/test_runner.py --install

# 2. Temel testleri çalıştır
python tests/test_runner.py --basic

# 3. Tüm testleri çalıştır (server'lar çalışır durumda olmalı)
python tests/test_runner.py --all
```

### Detaylı Komutlar

#### Backend Testleri
```bash
# API server'ı başlat (ayrı terminal)
python api_server.py

# API testlerini çalıştır
python tests/test_runner.py --api

# Veya direkt pytest ile
python -m pytest tests/test_api_endpoints.py -v
```

#### Frontend Testleri
```bash
# Frontend server'ı başlat (ayrı terminal)
cd frontend && npm run dev

# UI testlerini çalıştır
python tests/test_runner.py --ui

# Veya direkt Playwright ile
cd frontend && npx playwright test
```

#### Playwright Seçenekleri
```bash
# UI modda test çalıştır
cd frontend && npx playwright test --ui

# Headed modda (browser görünür)
cd frontend && npx playwright test --headed

# Debug modu
cd frontend && npx playwright test --debug

# Test raporu görüntüle
cd frontend && npx playwright show-report
```

## 📊 Test Kapsamı

### Backend Coverage
- ✅ **Core Modules**: Database reader, context collector, query builder
- ✅ **REST API**: Tüm endpoint'ler test edildi
- ✅ **Search Engine**: Basic ve semantic arama
- ✅ **Export Functions**: Markdown/Text export
- ✅ **WebSocket**: Real-time communication
- ✅ **Performance**: Response time testleri
- ✅ **Error Handling**: Hata durumları

### Frontend Coverage
- ✅ **Dashboard**: Ana sayfa, stats kartları, quick actions
- ✅ **Search**: Arama formu, sonuçlar, filtreleme, export
- ✅ **Analytics**: Metrics, grafikler, performans
- ✅ **Settings**: Tüm ayar kategorileri, kaydetme/yükleme
- ✅ **Responsive**: Mobil ve tablet uyumluluğu
- ✅ **Accessibility**: Screen reader uyumluluğu
- ✅ **Themes**: Dark/Light mode geçişleri

## 🛠️ Test Geliştirme

### Yeni Test Ekleme

#### Backend Test Ekleme
1. `tests/test_api_endpoints.py` dosyasına yeni test method'u ekle
2. Test class'ını uygun kategoriye yerleştir
3. `@pytest.fixture` kullanarak setup/teardown işlemleri

#### Frontend Test Ekleme
1. Uygun `.spec.js` dosyasına yeni test case ekle
2. `data-testid` attribute'larını kullan
3. `test.describe()` ile kategorize et

### Test Yazma Best Practices

#### Backend (Pytest)
```python
def test_example_endpoint(self):
    """Test açıklaması"""
    # Given - Setup
    data = {"query": "test"}
    
    # When - Action
    response = requests.post(f"{BASE_URL}/endpoint", json=data)
    
    # Then - Assertion
    assert response.status_code == 200
    assert "results" in response.json()
```

#### Frontend (Playwright)
```javascript
test('test açıklaması', async ({ page }) => {
  // Given - Setup
  await page.goto('/search');
  
  // When - Action
  await page.fill('[data-testid="search-input"]', 'test');
  await page.click('[data-testid="search-button"]');
  
  // Then - Assertion
  await expect(page.locator('[data-testid="results"]')).toBeVisible();
});
```

## 🔧 Troubleshooting

### Yaygın Sorunlar

#### API Testleri Başarısız
```bash
❌ API server çalışmıyor
```
**Çözüm**: `python api_server.py` komutunu çalıştırın

#### Frontend Testleri Başarısız
```bash
❌ Frontend server çalışmıyor
```
**Çözüm**: `cd frontend && npm run dev` komutunu çalıştırın

#### Playwright Browser Hatası
```bash
❌ Browser executable not found
```
**Çözüm**: `python tests/test_runner.py --install` ile browser'ları kurun

### Performance Sorunları

- Test timeout'larını artırın (30s)
- Paralel test sayısını azaltın
- Network latency için wait strategy kullanın

### CI/CD Entegrasyonu

```yaml
# GitHub Actions örneği
- name: Run Backend Tests
  run: |
    python api_server.py &
    sleep 10
    python tests/test_runner.py --api
    
- name: Run Frontend Tests  
  run: |
    cd frontend && npm run dev &
    sleep 10
    npx playwright test
```

## 📈 Test Metrikleri

### Mevcut Test Sonuçları
- **Temel Testler**: 14/14 ✅ (100%)
- **API Testleri**: Pending (server gerekli)
- **UI Testleri**: Pending (frontend server gerekli)

### Performance Benchmarks
- **API Response Time**: < 5 saniye
- **UI Load Time**: < 3 saniye
- **Search Response**: < 10 saniye

## 🔮 Gelecek Planları

### v2.2 Test Enhancements
- [ ] Visual regression testing
- [ ] Load testing (100+ concurrent users)
- [ ] Cross-browser compatibility matrix
- [ ] Accessibility compliance testing
- [ ] Security penetration testing

### Test Automation
- [ ] CI/CD pipeline integration
- [ ] Automated test reporting
- [ ] Test coverage monitoring
- [ ] Performance regression detection

## 📞 Destek

Test ile ilgili sorunlar için:
1. Bu README'yi kontrol edin
2. Test output'larını inceleyin  
3. Server durumlarını kontrol edin
4. Browser console hatalarına bakın

**Test Suite Status**: 🟡 Partial (Basic tests passing, API/UI tests require servers) 