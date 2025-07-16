# Collective Memory Test Suite

Bu dokümantasyon, Collective Memory uygulaması için kapsamlı test suite'ini açıklar.

## Test Türleri

### 1. UI Tests (Playwright)
- **dashboard.spec.js**: Ana dashboard sayfası testleri
- **search.spec.js**: Arama işlevselliği testleri  
- **analytics.spec.js**: Analitik sayfası testleri
- **settings.spec.js**: Ayarlar sayfası testleri
- **integration.spec.js**: Uçtan uca entegrasyon testleri
- **performance.spec.js**: Performans ve yükleme süresi testleri
- **security.spec.js**: Güvenlik ve XSS koruması testleri

### 2. API Tests (Python)
- **test_api_endpoints.py**: API endpoint testleri
- **test_basic.py**: Temel işlevsellik testleri

## Test Çalıştırma

### Tüm UI Testleri
```bash
npm test
# veya
npm run test:ui
```

### Belirli Test Dosyası
```bash
npx playwright test tests/ui/dashboard.spec.js
```

### Debug Mode
```bash
npm run test:debug
```

### Headed Mode (Browser Görünür)
```bash
npm run test:headed
```

### Test Raporu
```bash
npm run test:report
```

## Test Konfigürasyonu

### Playwright Config (playwright.config.js)
- **Base URL**: http://localhost:3003
- **Timeout**: 30 saniye
- **Retry**: CI'da 2 defa
- **Browsers**: Chromium, Firefox, Safari
- **Reporter**: HTML

### Test Data
Testler aşağıdaki test verilerini kullanır:
- Arama sorguları: "test query", "collective memory test"
- Performans eşikleri: 5s yükleme, 10s arama
- Güvenlik testleri: XSS, SQL injection, CSRF

## Test Kategorileri

### 1. Functional Tests
- Sayfa yükleme ve navigasyon
- Form gönderimi ve validasyon
- Arama işlevselliği
- Kullanıcı etkileşimleri

### 2. Performance Tests
- Sayfa yükleme süreleri
- Memory leak kontrolü
- Network request optimizasyonu
- Responsive performans
- Cache performansı

### 3. Security Tests
- XSS koruması
- SQL injection önleme
- CSRF token kontrolü
- File upload güvenliği
- Session güvenliği
- Content Security Policy

### 4. Integration Tests
- Uçtan uca iş akışları
- Cross-page functionality
- Dark mode persistence
- Error handling
- Analytics tracking

### 5. Accessibility Tests
- Keyboard navigation
- ARIA labels
- Focus indicators
- Screen reader compatibility

## Test Best Practices

### 1. Test Data Attributes
Testlerde element seçimi için `data-testid` kullanın:
```html
<button data-testid="search-button">Ara</button>
```

### 2. Wait Strategies
```javascript
// Network idle bekle
await page.waitForLoadState('networkidle');

// Element görünür olana kadar bekle
await page.waitForSelector('[data-testid="results"]');

// Timeout ile bekle
await page.waitForTimeout(1000);
```

### 3. Error Handling
```javascript
// Dialog'ları yakalama
page.on('dialog', dialog => dialog.dismiss());

// Network hatalarını simülasyon
await page.route('**/api/**', route => {
  route.fulfill({ status: 500 });
});
```

### 4. Test Organization
```javascript
test.describe('Feature Group', () => {
  test.beforeEach(async ({ page }) => {
    // Her test öncesi setup
  });

  test('specific functionality', async ({ page }) => {
    // Test implementation
  });
});
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Run Playwright tests
  run: |
    npm ci
    npx playwright install
    npm test
```

### Test Reports
- HTML report: `playwright-report/index.html`
- Video recordings: `test-results/`
- Screenshots: `test-results/`

## Performance Benchmarks

### Kabul Edilebilir Sınırlar
- Sayfa yükleme: < 5 saniye
- Arama süresi: < 10 saniye
- Memory artışı: < %50
- Layout shift: < 0.1
- API response: < 3 saniye

### Monitoring
- Core Web Vitals tracking
- Performance metrics collection
- Error rate monitoring
- User experience metrics

## Troubleshooting

### Yaygın Sorunlar

1. **Browser yüklenmedi**
```bash
npx playwright install
```

2. **Timeout hatası**
- Test timeout'unu artırın
- `waitForLoadState` kullanın
- Network durumunu kontrol edin

3. **Element bulunamadı**
- `data-testid` attribute'unu kontrol edin
- Element yüklenmesini bekleyin
- Selector'ı doğrulayın

4. **Flaky tests**
- Explicit wait'ler ekleyin
- Race condition'ları kontrol edin
- Test verilerini stabilize edin

## Test Coverage

### Current Coverage
- UI Components: %95
- API Endpoints: %90
- Error Scenarios: %85
- Performance Cases: %80
- Security Tests: %90

### Coverage Goals
- Functional: %95+
- Performance: %85+
- Security: %95+
- Accessibility: %90+

## Maintenance

### Regular Tasks
- Test data güncellemesi
- Performance benchmark'ları
- Security test pattern'ları
- Browser compatibility
- Dependency updates

### Review Process
1. Test sonuçlarını gözden geçir
2. Flaky test'leri tespit et
3. Performance regression'ları kontrol et
4. Coverage gap'lerini belirle
5. Test strategy'sini güncelle

## Contact

Test suite ile ilgili sorular için development team'e başvurun.

## Changelog

### v1.0.0
- Initial test suite implementation
- Playwright configuration
- Basic UI tests
- Performance monitoring
- Security test coverage 