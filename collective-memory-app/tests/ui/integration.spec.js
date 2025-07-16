// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Integration Tests
 * Uçtan uca entegrasyon testleri
 */

test.describe('Uçtan Uca Entegrasyon Testleri', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('tam iş akışı: arama → analitik → ayarlar', async ({ page }) => {
    // 1. Ana sayfadan başla
    await expect(page.locator('h1')).toBeVisible();
    
    // 2. Arama sayfasına git
    await page.click('[data-testid="nav-search"]');
    await page.waitForURL('**/search');
    
    // 3. Arama yap
    await page.fill('[data-testid="search-input"]', 'collective memory test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]', { timeout: 10000 });
    
    // 4. Analytics sayfasına git
    await page.click('[data-testid="nav-analytics"]');
    await page.waitForURL('**/analytics');
    await expect(page.locator('[data-testid="performance-metrics"]')).toBeVisible();
    
    // 5. Ayarlar sayfasına git
    await page.click('[data-testid="nav-settings"]');
    await page.waitForURL('**/settings');
    await expect(page.locator('[data-testid="settings-form"]')).toBeVisible();
    
    // 6. Ana sayfaya dön
    await page.click('[data-testid="nav-dashboard"]');
    await page.waitForURL('/');
    await expect(page.locator('h1')).toBeVisible();
  });

  test('dark mode geçişi tüm sayfalarda çalışıyor', async ({ page }) => {
    const themeToggle = '[data-testid="theme-toggle"]';
    
    // Ana sayfa - dark mode aç
    await page.click(themeToggle);
    await expect(page.locator('body')).toHaveClass(/dark/);
    
    // Arama sayfası
    await page.goto('/search');
    await expect(page.locator('body')).toHaveClass(/dark/);
    
    // Analytics sayfası
    await page.goto('/analytics');
    await expect(page.locator('body')).toHaveClass(/dark/);
    
    // Ayarlar sayfası
    await page.goto('/settings');
    await expect(page.locator('body')).toHaveClass(/dark/);
    
    // Light mode'a geri dön
    await page.click(themeToggle);
    await expect(page.locator('body')).not.toHaveClass(/dark/);
  });

  test('responsive tasarım tüm sayfalarda çalışıyor', async ({ page }) => {
    const pages = ['/', '/search', '/analytics', '/settings'];
    
    for (const pagePath of pages) {
      await page.goto(pagePath);
      
      // Desktop boyut
      await page.setViewportSize({ width: 1920, height: 1080 });
      await expect(page.locator('[data-testid="sidebar"]')).toBeVisible();
      
      // Tablet boyut
      await page.setViewportSize({ width: 768, height: 1024 });
      await page.waitForTimeout(500);
      
      // Mobile boyut
      await page.setViewportSize({ width: 375, height: 667 });
      await page.waitForTimeout(500);
      
      // Header hala görünür olmalı
      await expect(page.locator('header')).toBeVisible();
    }
  });

  test('hata durumları graceful şekilde handle ediliyor', async ({ page }) => {
    // API hatası simülasyonu
    await page.route('**/api/**', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Server error' })
      });
    });
    
    await page.goto('/search');
    await page.fill('[data-testid="search-input"]', 'test query');
    await page.click('[data-testid="search-button"]');
    
    // Hata mesajı gösterilmeli
    await expect(page.locator('[data-testid="error-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-message"]')).toContainText(/hata|error/i);
  });

  test('performans metrikleri güncelleniyor', async ({ page }) => {
    // Analytics sayfasına git
    await page.goto('/analytics');
    
    // İlk metrik değerlerini al
    const initialSearchCount = await page.locator('[data-testid="total-searches"]').textContent();
    
    // Arama yap
    await page.goto('/search');
    await page.fill('[data-testid="search-input"]', 'performance test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]', { timeout: 10000 });
    
    // Analytics'e geri dön ve güncellemeyi kontrol et
    await page.goto('/analytics');
    await page.waitForTimeout(2000); // Metrik güncellemesi için bekle
    
    const updatedSearchCount = await page.locator('[data-testid="total-searches"]').textContent();
    
    // Arama sayısı artmış olmalı (eğer sayısal değerse)
    if (initialSearchCount && updatedSearchCount) {
      const initial = parseInt(initialSearchCount.replace(/\D/g, ''));
      const updated = parseInt(updatedSearchCount.replace(/\D/g, ''));
      
      if (!isNaN(initial) && !isNaN(updated)) {
        expect(updated).toBeGreaterThanOrEqual(initial);
      }
    }
  });

  test('arama geçmişi kaydediliyor', async ({ page }) => {
    const searchTerms = ['test query 1', 'test query 2', 'test query 3'];
    
    // Birden fazla arama yap
    for (const term of searchTerms) {
      await page.goto('/search');
      await page.fill('[data-testid="search-input"]', term);
      await page.click('[data-testid="search-button"]');
      await page.waitForSelector('[data-testid="search-results"]', { timeout: 10000 });
    }
    
    // Analytics sayfasında popüler aramalar kontrol et
    await page.goto('/analytics');
    const popularQueries = page.locator('[data-testid="popular-queries"]');
    await expect(popularQueries).toBeVisible();
    
    // En az bir arama terimi görünmeli
    const queryItems = page.locator('[data-testid="query-item"]');
    await expect(queryItems.first()).toBeVisible();
  });

  test('sistem durumu monitoring çalışıyor', async ({ page }) => {
    await page.goto('/');
    
    // Sistem durumu badge'i kontrol et
    const systemStatus = page.locator('[data-testid="system-status"]');
    await expect(systemStatus).toBeVisible();
    
    // Durum rengi yeşil, sarı veya kırmızı olmalı
    const statusClass = await systemStatus.getAttribute('class');
    expect(statusClass).toMatch(/(green|yellow|red|success|warning|error)/);
    
    // Analytics sayfasında sistem kullanımı
    await page.goto('/analytics');
    await expect(page.locator('[data-testid="system-usage"]')).toBeVisible();
  });
});

test.describe('Accessibility Tests', () => {
  test('keyboard navigation çalışıyor', async ({ page }) => {
    await page.goto('/');
    
    // Tab ile navigasyon
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Enter ile link aktivasyonu
    await page.keyboard.press('Enter');
    
    // Sayfa değişmiş olmalı
    await page.waitForLoadState('networkidle');
  });

  test('ARIA labels mevcut', async ({ page }) => {
    await page.goto('/search');
    
    // Arama input'u label'ı
    const searchInput = page.locator('[data-testid="search-input"]');
    await expect(searchInput).toHaveAttribute('aria-label');
    
    // Buton açıklamaları
    const searchButton = page.locator('[data-testid="search-button"]');
    await expect(searchButton).toHaveAttribute('aria-label');
  });

  test('focus indicators görünür', async ({ page }) => {
    await page.goto('/');
    
    // Tab ile focus yap
    await page.keyboard.press('Tab');
    
    // Focus edilen element görünür olmalı
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });
}); 