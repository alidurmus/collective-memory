// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Security Tests
 * Güvenlik ve XSS koruması testleri
 */

test.describe('Güvenlik Testleri', () => {
  test('XSS koruması - arama input', async ({ page }) => {
    await page.goto('/search');
    
    // Zararlı script injection denemesi
    const maliciousScript = '<script>alert("XSS")</script>';
    
    await page.fill('[data-testid="search-input"]', maliciousScript);
    await page.click('[data-testid="search-button"]');
    
    // Alert dialog açılmamalı
    let alertTriggered = false;
    page.on('dialog', () => {
      alertTriggered = true;
    });
    
    await page.waitForTimeout(2000);
    expect(alertTriggered).toBe(false);
    
    // Input değeri escape edilmiş olmalı
    const inputValue = await page.inputValue('[data-testid="search-input"]');
    expect(inputValue).not.toContain('<script>');
  });

  test('SQL injection koruması', async ({ page }) => {
    await page.goto('/search');
    
    // SQL injection denemesi
    const sqlInjection = "'; DROP TABLE users; --";
    
    await page.fill('[data-testid="search-input"]', sqlInjection);
    await page.click('[data-testid="search-button"]');
    
    // Sayfa crash olmamalı
    await page.waitForTimeout(3000);
    await expect(page.locator('body')).toBeVisible();
    
    // Hata mesajı SQL detayları içermemeli
    const errorMessage = page.locator('[data-testid="error-message"]');
    if (await errorMessage.isVisible()) {
      const errorText = await errorMessage.textContent();
      expect(errorText?.toLowerCase()).not.toContain('sql');
      expect(errorText?.toLowerCase()).not.toContain('database');
      expect(errorText?.toLowerCase()).not.toContain('table');
    }
  });

  test('CSRF token kontrolü', async ({ page }) => {
    await page.goto('/settings');
    
    // Form submit etmeye çalış
    const form = page.locator('[data-testid="settings-form"]');
    if (await form.isVisible()) {
      // CSRF token varlığını kontrol et
      const csrfToken = page.locator('input[name="csrf_token"], input[name="_token"]');
      
      if (await csrfToken.count() > 0) {
        await expect(csrfToken.first()).toHaveAttribute('value');
        
        const tokenValue = await csrfToken.first().getAttribute('value');
        expect(tokenValue).toBeTruthy();
        expect(tokenValue?.length).toBeGreaterThan(10);
      }
    }
  });

  test('file upload güvenliği', async ({ page }) => {
    await page.goto('/settings');
    
    const fileInput = page.locator('input[type="file"]');
    if (await fileInput.isVisible()) {
      // Sadece izin verilen dosya türleri kabul edilmeli
      const acceptAttribute = await fileInput.getAttribute('accept');
      
      if (acceptAttribute) {
        // Executable dosyalar kabul edilmemeli
        expect(acceptAttribute).not.toContain('.exe');
        expect(acceptAttribute).not.toContain('.bat');
        expect(acceptAttribute).not.toContain('.sh');
        expect(acceptAttribute).not.toContain('.php');
      }
      
      // Maksimum dosya boyutu kontrolü
      const maxSize = await page.evaluate(() => {
        const input = document.querySelector('input[type="file"]');
        return input?.getAttribute('data-max-size') || null;
      });
      
      if (maxSize) {
        expect(parseInt(maxSize)).toBeLessThan(10 * 1024 * 1024); // 10MB limit
      }
    }
  });

  test('URL manipulation koruması', async ({ page }) => {
    // Path traversal denemesi
    const maliciousUrls = [
      '/search?q=../../../etc/passwd',
      '/search?q=..\\..\\windows\\system32',
      '/analytics?filter=<script>alert("xss")</script>',
      '/settings?redirect=javascript:alert("xss")'
    ];
    
    for (const url of maliciousUrls) {
      await page.goto(url);
      
      // Sayfa normal şekilde yüklenmeli, zararlı kod çalışmamalı
      await expect(page.locator('body')).toBeVisible();
      
      // Alert dialog açılmamalı
      let alertTriggered = false;
      page.on('dialog', () => {
        alertTriggered = true;
      });
      
      await page.waitForTimeout(1000);
      expect(alertTriggered).toBe(false);
    }
  });

  test('session güvenliği', async ({ page }) => {
    await page.goto('/');
    
    // Session cookie kontrolleri
    const cookies = await page.context().cookies();
    const sessionCookie = cookies.find(cookie => 
      cookie.name.toLowerCase().includes('session') || 
      cookie.name.toLowerCase().includes('auth')
    );
    
    if (sessionCookie) {
      // HttpOnly flag olmalı
      expect(sessionCookie.httpOnly).toBe(true);
      
      // Secure flag olmalı (HTTPS'de)
      if (page.url().startsWith('https://')) {
        expect(sessionCookie.secure).toBe(true);
      }
      
      // SameSite attribute olmalı
      expect(['Strict', 'Lax']).toContain(sessionCookie.sameSite);
    }
  });

  test('content security policy', async ({ page }) => {
    const response = await page.goto('/');
    
    // CSP header kontrol et
    const cspHeader = response?.headers()['content-security-policy'] || 
                     response?.headers()['content-security-policy-report-only'];
    
    if (cspHeader) {
      // Inline script'ler kısıtlanmalı
      expect(cspHeader).toContain("script-src");
      expect(cspHeader).not.toContain("'unsafe-inline'");
      
      // Eval kısıtlanmalı
      expect(cspHeader).not.toContain("'unsafe-eval'");
    }
  });

  test('clickjacking koruması', async ({ page }) => {
    const response = await page.goto('/');
    
    // X-Frame-Options veya frame-ancestors kontrol et
    const xFrameOptions = response?.headers()['x-frame-options'];
    const csp = response?.headers()['content-security-policy'];
    
    const hasClickjackingProtection = 
      xFrameOptions === 'DENY' || 
      xFrameOptions === 'SAMEORIGIN' ||
      (csp && csp.includes('frame-ancestors'));
    
    expect(hasClickjackingProtection).toBe(true);
  });

  test('information disclosure önleme', async ({ page }) => {
    await page.goto('/');
    
    // Server header'ları hassas bilgi içermemeli
    const response = await page.goto('/');
    const serverHeader = response?.headers()['server'];
    
    if (serverHeader) {
      // Versiyon numaraları gizlenmeli
      expect(serverHeader).not.toMatch(/\d+\.\d+/);
      expect(serverHeader.toLowerCase()).not.toContain('apache');
      expect(serverHeader.toLowerCase()).not.toContain('nginx');
    }
    
    // Powered-by header'ı olmamalı
    const poweredBy = response?.headers()['x-powered-by'];
    expect(poweredBy).toBeUndefined();
  });

  test('rate limiting', async ({ page }) => {
    await page.goto('/search');
    
    const searchInput = '[data-testid="search-input"]';
    const searchButton = '[data-testid="search-button"]';
    
    // Hızlı ardışık istekler gönder
    const requests = [];
    for (let i = 0; i < 20; i++) {
      const promise = (async () => {
        await page.fill(searchInput, `test query ${i}`);
        await page.click(searchButton);
        await page.waitForTimeout(100);
      })();
      requests.push(promise);
    }
    
    await Promise.all(requests);
    
    // Rate limiting uyarısı gösterilmeli
    const rateLimitWarning = page.locator('[data-testid="rate-limit-warning"]');
    if (await rateLimitWarning.isVisible()) {
      await expect(rateLimitWarning).toContainText(/limit|sınır/i);
    }
  });

  test('input validation', async ({ page }) => {
    await page.goto('/search');
    
    // Çok uzun input
    const veryLongInput = 'a'.repeat(10000);
    await page.fill('[data-testid="search-input"]', veryLongInput);
    
    const inputValue = await page.inputValue('[data-testid="search-input"]');
    expect(inputValue.length).toBeLessThan(1000); // Maksimum limit olmalı
    
    // Özel karakterler
    const specialChars = '!@#$%^&*()[]{}|;:,.<>?';
    await page.fill('[data-testid="search-input"]', specialChars);
    await page.click('[data-testid="search-button"]');
    
    // Sayfa crash olmamalı
    await expect(page.locator('body')).toBeVisible();
  });

  test('error handling güvenliği', async ({ page }) => {
    // 404 sayfası
    await page.goto('/nonexistent-page');
    
    // Error page stack trace içermemeli
    const pageContent = await page.textContent('body');
    expect(pageContent?.toLowerCase()).not.toContain('stack trace');
    expect(pageContent?.toLowerCase()).not.toContain('exception');
    expect(pageContent?.toLowerCase()).not.toContain('error at line');
    
    // 500 error simülasyonu
    await page.route('**/api/**', route => {
      route.fulfill({
        status: 500,
        body: 'Internal Server Error'
      });
    });
    
    await page.goto('/search');
    await page.fill('[data-testid="search-input"]', 'test');
    await page.click('[data-testid="search-button"]');
    
    // Generic error mesajı gösterilmeli
    const errorMessage = page.locator('[data-testid="error-message"]');
    if (await errorMessage.isVisible()) {
      const errorText = await errorMessage.textContent();
      expect(errorText).not.toContain('database');
      expect(errorText).not.toContain('connection');
      expect(errorText).not.toContain('sql');
    }
  });
});

test.describe('Data Privacy Tests', () => {
  test('localStorage güvenliği', async ({ page }) => {
    await page.goto('/');
    
    // Hassas veri localStorage'da saklanmamalı
    const localStorageData = await page.evaluate(() => {
      const data = {};
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key) {
          data[key] = localStorage.getItem(key);
        }
      }
      return data;
    });
    
    for (const [key, value] of Object.entries(localStorageData)) {
      expect(key.toLowerCase()).not.toContain('password');
      expect(key.toLowerCase()).not.toContain('token');
      expect(key.toLowerCase()).not.toContain('secret');
      
      if (typeof value === 'string') {
        expect(value.toLowerCase()).not.toContain('password');
        expect(value.toLowerCase()).not.toContain('secret');
      }
    }
  });

  test('console log temizliği', async ({ page }) => {
    await page.goto('/');
    
    // Console logları hassas bilgi içermemeli
    const consoleLogs = [];
    page.on('console', msg => {
      consoleLogs.push(msg.text());
    });
    
    // Birkaç işlem yap
    await page.goto('/search');
    await page.fill('[data-testid="search-input"]', 'test');
    await page.click('[data-testid="search-button"]');
    
    await page.waitForTimeout(2000);
    
    for (const log of consoleLogs) {
      expect(log.toLowerCase()).not.toContain('password');
      expect(log.toLowerCase()).not.toContain('token');
      expect(log.toLowerCase()).not.toContain('secret');
      expect(log.toLowerCase()).not.toContain('api_key');
    }
  });

  test('network request güvenliği', async ({ page }) => {
    const requests = [];
    
    page.on('request', request => {
      requests.push({
        url: request.url(),
        headers: request.headers(),
        postData: request.postData()
      });
    });
    
    await page.goto('/search');
    await page.fill('[data-testid="search-input"]', 'sensitive data');
    await page.click('[data-testid="search-button"]');
    
    await page.waitForTimeout(2000);
    
    for (const request of requests) {
      // URL'de hassas bilgi olmamalı
      expect(request.url.toLowerCase()).not.toContain('password');
      expect(request.url.toLowerCase()).not.toContain('secret');
      
      // POST data encrypt edilmiş olmalı veya hassas bilgi içermemeli
      if (request.postData) {
        expect(request.postData.toLowerCase()).not.toContain('password');
        expect(request.postData.toLowerCase()).not.toContain('secret');
      }
      
      // Authorization header kontrol
      if (request.headers['authorization']) {
        expect(request.headers['authorization']).not.toContain('password');
      }
    }
  });
}); 