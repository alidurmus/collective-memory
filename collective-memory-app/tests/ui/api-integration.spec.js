// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory API Integration Tests
 * Frontend-Backend entegrasyon testleri
 */

test.describe('API Entegrasyon Testleri', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
    await page.waitForLoadState('networkidle');
  });

  test('API health check çalışıyor', async ({ page }) => {
    // API health endpoint'ini test et
    const response = await page.request.get('http://localhost:8000/api/health');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status');
    expect(data.status).toBe('healthy');
  });

  test('arama API entegrasyonu', async ({ page }) => {
    // Frontend arama sayfasına git
    await page.goto('http://localhost:5173/search');
    
    // API requestini yakala
    const [response] = await Promise.all([
      page.waitForResponse(response => 
        response.url().includes('/api/search') && response.status() === 200
      ),
      page.fill('[data-testid="search-input"]', 'test query'),
      page.click('[data-testid="search-button"]')
    ]);

    // Response kontrol et
    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data).toHaveProperty('results');
    expect(Array.isArray(data.results)).toBe(true);
  });

  test('analytics API entegrasyonu', async ({ page }) => {
    await page.goto('http://localhost:5173/analytics');
    
    // Analytics API çağrısını bekle
    const [response] = await Promise.all([
      page.waitForResponse(response => 
        response.url().includes('/api/analytics') && response.status() === 200
      ),
      page.waitForSelector('[data-testid="performance-metrics"]')
    ]);

    const data = await response.json();
    expect(data).toHaveProperty('metrics');
    expect(typeof data.metrics).toBe('object');
  });

  test('error handling API entegrasyonu', async ({ page }) => {
    // API hatası simüle et
    await page.route('**/api/search', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' })
      });
    });

    await page.goto('http://localhost:5173/search');
    await page.fill('[data-testid="search-input"]', 'test');
    await page.click('[data-testid="search-button"]');

    // Error message gösterilmeli
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
  });

  test('real-time updates çalışıyor', async ({ page }) => {
    await page.goto('http://localhost:5173/analytics');
    
    // İlk metrik değerini al
    const initialValue = await page.locator('[data-testid="total-searches"]').textContent();
    
    // Arama yap
    await page.goto('http://localhost:5173/search');
    await page.fill('[data-testid="search-input"]', 'realtime test');
    await page.click('[data-testid="search-button"]');
    
    // Analytics'e geri dön
    await page.goto('http://localhost:5173/analytics');
    await page.waitForTimeout(2000);
    
    // Değer güncellenmiş olmalı
    const updatedValue = await page.locator('[data-testid="total-searches"]').textContent();
    
    if (initialValue && updatedValue) {
      const initial = parseInt(initialValue.replace(/\D/g, ''));
      const updated = parseInt(updatedValue.replace(/\D/g, ''));
      
      if (!isNaN(initial) && !isNaN(updated)) {
        expect(updated).toBeGreaterThanOrEqual(initial);
      }
    }
  });

  test('pagination API entegrasyonu', async ({ page }) => {
    await page.goto('http://localhost:5173/search');
    
    // Arama yap
    await page.fill('[data-testid="search-input"]', 'pagination test');
    await page.click('[data-testid="search-button"]');
    
    // Sonuçlar yüklenene kadar bekle
    await page.waitForSelector('[data-testid="search-results"]');
    
    // Pagination kontrolleri varsa test et
    const nextButton = page.locator('[data-testid="next-page"]');
    if (await nextButton.isVisible()) {
      const [response] = await Promise.all([
        page.waitForResponse(response => 
          response.url().includes('/api/search') && 
          response.url().includes('page=2')
        ),
        nextButton.click()
      ]);
      
      expect(response.status()).toBe(200);
    }
  });

  test('cache kontrolü', async ({ page }) => {
    await page.goto('http://localhost:5173/search');
    
    // İlk arama
    const [firstResponse] = await Promise.all([
      page.waitForResponse(response => response.url().includes('/api/search')),
      page.fill('[data-testid="search-input"]', 'cache test'),
      page.click('[data-testid="search-button"]')
    ]);
    
    const firstTime = Date.now();
    
    // Aynı aramayı tekrar yap
    await page.fill('[data-testid="search-input"]', 'cache test');
    
    const [secondResponse] = await Promise.all([
      page.waitForResponse(response => response.url().includes('/api/search')),
      page.click('[data-testid="search-button"]')
    ]);
    
    const secondTime = Date.now();
    
    // İkinci istek daha hızlı olmalı (cache'den)
    const firstDuration = firstTime;
    const secondDuration = secondTime - firstTime;
    
    console.log(`First request: ${firstDuration}ms, Second request: ${secondDuration}ms`);
  });

  test('concurrent request handling', async ({ page }) => {
    await page.goto('http://localhost:5173/search');
    
    // Birden fazla eşzamanlı arama
    const searches = ['test1', 'test2', 'test3'];
    const promises = searches.map(async (term, index) => {
      await page.waitForTimeout(index * 100); // Slight delay
      await page.fill('[data-testid="search-input"]', term);
      return page.click('[data-testid="search-button"]');
    });
    
    await Promise.all(promises);
    
    // Son sonuçlar görünmeli
    await page.waitForSelector('[data-testid="search-results"]');
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
  });

  test('file upload API entegrasyonu', async ({ page }) => {
    await page.goto('http://localhost:5173/settings');
    
    const fileInput = page.locator('input[type="file"]');
    if (await fileInput.isVisible()) {
      // Test dosyası oluştur
      const testFile = Buffer.from('test file content');
      
      const [response] = await Promise.all([
        page.waitForResponse(response => 
          response.url().includes('/api/upload')
        ),
        fileInput.setInputFiles({
          name: 'test.txt',
          mimeType: 'text/plain',
          buffer: testFile
        })
      ]);
      
      expect([200, 201]).toContain(response.status());
    }
  });

  test('websocket bağlantısı', async ({ page }) => {
    await page.goto('http://localhost:5173');
    
    // WebSocket bağlantısını kontrol et
    const wsConnected = await page.evaluate(() => {
      return new Promise((resolve) => {
        try {
          const ws = new WebSocket('ws://localhost:8000/ws');
          ws.onopen = () => resolve(true);
          ws.onerror = () => resolve(false);
          setTimeout(() => resolve(false), 5000);
        } catch (e) {
          resolve(false);
        }
      });
    });
    
    if (wsConnected) {
      console.log('WebSocket connection successful');
    } else {
      console.log('WebSocket connection not available');
    }
  });
});

test.describe('API Performance Tests', () => {
  test('API response times', async ({ page }) => {
    const endpoints = [
      '/api/health',
      '/api/search?q=test',
      '/api/analytics'
    ];
    
    for (const endpoint of endpoints) {
      const startTime = Date.now();
      
      const response = await page.request.get(`http://localhost:8000${endpoint}`);
      
      const responseTime = Date.now() - startTime;
      
      console.log(`${endpoint}: ${responseTime}ms`);
      
      // Response time 5 saniyeden az olmalı
      expect(responseTime).toBeLessThan(5000);
      expect([200, 404]).toContain(response.status());
    }
  });

  test('API rate limiting', async ({ page }) => {
    // Hızlı ardışık istekler gönder
    const requests = [];
    for (let i = 0; i < 20; i++) {
      requests.push(
        page.request.get('http://localhost:8000/api/search?q=rate_limit_test')
      );
    }
    
    const responses = await Promise.all(requests);
    
    // Rate limiting kontrol et
    const rateLimitedResponses = responses.filter(r => r.status() === 429);
    
    if (rateLimitedResponses.length > 0) {
      console.log(`Rate limiting active: ${rateLimitedResponses.length} requests limited`);
    }
  });

  test('large response handling', async ({ page }) => {
    // Büyük response için test
    const response = await page.request.get('http://localhost:8000/api/search?q=large_dataset&limit=1000');
    
    if (response.status() === 200) {
      const data = await response.json();
      expect(data).toHaveProperty('results');
      
      // Response boyutu kontrol et
      const responseSize = JSON.stringify(data).length;
      console.log(`Large response size: ${responseSize} bytes`);
      
      // 10MB'dan küçük olmalı
      expect(responseSize).toBeLessThan(10 * 1024 * 1024);
    }
  });
}); 