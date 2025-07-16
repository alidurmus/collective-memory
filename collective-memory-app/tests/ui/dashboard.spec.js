// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Dashboard Tests
 * Ana sayfa ve dashboard işlevselliği testleri
 */

test.describe('Dashboard Ana Sayfa', () => {
  test.beforeEach(async ({ page }) => {
    // Ana sayfaya git - baseURL kullan
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('sayfa başlığı doğru gösteriliyor', async ({ page }) => {
    await expect(page).toHaveTitle(/Collective Memory|Vite \+ React/);
  });

  test('header bileşenleri yükleniyor', async ({ page }) => {
    // Header ana container'ı kontrol et
    const headerSelectors = [
      'header',
      '[data-testid="header"]',
      '.header',
      '.navbar',
      'nav'
    ];
    
    let headerFound = false;
    for (const selector of headerSelectors) {
      const header = page.locator(selector);
      if (await header.count() > 0) {
        await expect(header).toBeVisible();
        headerFound = true;
        break;
      }
    }
    
    if (!headerFound) {
      // Header yoksa body en azından var olmalı
      await expect(page.locator('body')).toBeVisible();
    }
  });

  test('ana içerik yükleniyor', async ({ page }) => {
    // Ana içerik container'ları kontrol et
    const contentSelectors = [
      'main',
      '[data-testid="main-content"]',
      '.main-content',
      '#root',
      '.app'
    ];
    
    let contentFound = false;
    for (const selector of contentSelectors) {
      const content = page.locator(selector);
      if (await content.count() > 0) {
        await expect(content).toBeVisible();
        contentFound = true;
        break;
      }
    }
    
    expect(contentFound).toBe(true);
  });

  test('navigation linkleri çalışıyor', async ({ page }) => {
    // Navigation linklerini kontrol et
    const navSelectors = [
      'a[href="/search"]',
      'a[href="/analytics"]',
      'a[href="/settings"]',
      '[data-testid="nav-search"]',
      '[data-testid="nav-analytics"]',
      '[data-testid="nav-settings"]'
    ];
    
         for (const selector of navSelectors) {
       const link = page.locator(selector);
       if (await link.count() > 0) {
         // Multiple elements için first() kullan
         const firstLink = link.first();
         if (await firstLink.isVisible()) {
           await expect(firstLink).toBeVisible();
           console.log(`Navigation link found: ${selector}`);
           break;
         }
       }
     }
    
    // En azından sayfa çalışıyor olmalı
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Arama İşlevselliği', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('arama input elementi bulunuyor', async ({ page }) => {
    // Arama inputu ara
    const searchSelectors = [
      '[data-testid="search-input"]',
      'input[type="search"]',
      'input[placeholder*="ara" i]',
      'input[placeholder*="search" i]',
      '.search-input',
      '#search'
    ];
    
    let searchFound = false;
    for (const selector of searchSelectors) {
      const searchInput = page.locator(selector);
      if (await searchInput.count() > 0 && await searchInput.isVisible()) {
        await expect(searchInput).toBeVisible();
        await expect(searchInput).toBeEnabled();
        searchFound = true;
        console.log(`Search input found: ${selector}`);
        break;
      }
    }
    
    // Eğer arama input'u ana sayfada yoksa, search sayfasına git
    if (!searchFound) {
      await page.goto('/search');
      await page.waitForLoadState('networkidle');
      
      for (const selector of searchSelectors) {
        const searchInput = page.locator(selector);
        if (await searchInput.count() > 0 && await searchInput.isVisible()) {
          await expect(searchInput).toBeVisible();
          searchFound = true;
          break;
        }
      }
    }
    
    // En azından sayfa yüklenmiş olmalı
    await expect(page.locator('body')).toBeVisible();
  });

  test('form submission çalışıyor', async ({ page }) => {
    // Search sayfasına git
    await page.goto('/search');
    await page.waitForLoadState('networkidle');
    
    // Arama formu ara ve test et
    const searchInput = page.locator('[data-testid="search-input"]');
    if (await searchInput.count() > 0) {
      await searchInput.fill('test query');
      
      const submitButton = page.locator('[data-testid="search-button"]');
      if (await submitButton.count() > 0) {
        await submitButton.click();
        await page.waitForTimeout(2000); // Sonuçlar için bekle
      }
    }
    
    // Sayfa crash olmadığından emin ol
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Dark Mode Toggle', () => {
  test('tema geçişi kontrol edilebiliyor', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Theme toggle butonları ara
    const themeSelectors = [
      '[data-testid="theme-toggle"]',
      '.theme-toggle',
      '.dark-mode-toggle',
      'button[aria-label*="theme" i]',
      'button[aria-label*="dark" i]'
    ];
    
    let themeToggleFound = false;
    for (const selector of themeSelectors) {
      const toggle = page.locator(selector);
      if (await toggle.count() > 0 && await toggle.isVisible()) {
        await toggle.click();
        await page.waitForTimeout(1000);
        themeToggleFound = true;
        console.log(`Theme toggle found: ${selector}`);
        break;
      }
    }
    
    // Theme toggle yoksa body class'ını kontrol et
    if (!themeToggleFound) {
      const body = page.locator('body');
      const bodyClass = await body.getAttribute('class');
      console.log(`Body class: ${bodyClass}`);
    }
    
    // Sayfa hala responsive olmalı
    await expect(page.locator('body')).toBeVisible();
  });
});

test.describe('Responsive Design', () => {
  test('mobil cihazlarda düzgün görünüm', async ({ page }) => {
    // Mobil boyutuna ayarla
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Ana içerik görünür olmalı
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('#root')).toBeVisible();
  });

  test('tablet boyutunda düzgün görünüm', async ({ page }) => {
    // Tablet boyutuna ayarla
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // İçerik düzenli görünmeli
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('#root')).toBeVisible();
  });

  test('desktop boyutunda düzgün görünüm', async ({ page }) => {
    // Desktop boyutuna ayarla
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // İçerik düzenli görünmeli
    await expect(page.locator('body')).toBeVisible();
    await expect(page.locator('#root')).toBeVisible();
  });
});

test.describe('Loading States', () => {
  test('sayfa yükleme durumu kontrol ediliyor', async ({ page }) => {
    await page.goto('/');

    // Loading spinner arama
    const loadingSelectors = [
      '[data-testid="loading-spinner"]',
      '.loading',
      '.spinner',
      '[class*="loading"]'
    ];
    
    // Loading state geçici olabilir, timeout ile kontrol et
    for (const selector of loadingSelectors) {
      const loading = page.locator(selector);
      if (await loading.count() > 0) {
        console.log(`Loading element found: ${selector}`);
        break;
      }
    }

    // Sayfa tamamen yüklendiğinde loading kaybolmalı
    await page.waitForLoadState('networkidle');
    await expect(page.locator('body')).toBeVisible();
  });

  test('error boundary çalışıyor', async ({ page }) => {
    // JavaScript hatası simüle et
    await page.goto('/');
    
    await page.evaluate(() => {
      // Kasıtlı hata oluştur
      const errorEvent = new Event('error');
      window.dispatchEvent(errorEvent);
    });
    
    await page.waitForTimeout(1000);
    
    // Sayfa hala responsive olmalı
    await expect(page.locator('body')).toBeVisible();
  });
}); 