// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Dashboard UI Tests
 * Ana dashboard sayfası testleri
 */

test.describe('Dashboard Ana Sayfa', () => {
  test.beforeEach(async ({ page }) => {
    // Ana sayfaya git
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('sayfa başlığı doğru gösteriliyor', async ({ page }) => {
    await expect(page).toHaveTitle(/Collective Memory/);
  });

  test('header bileşenleri yükleniyor', async ({ page }) => {
    // Header elementi
    await expect(page.locator('header')).toBeVisible();
    
    // Logo veya başlık
    await expect(page.locator('h1, .logo').first()).toBeVisible();
    
    // Sistem durumu badge'i
    await expect(page.locator('[data-testid="system-status"]')).toBeVisible();
    
    // Dark mode toggle
    await expect(page.locator('[data-testid="theme-toggle"]')).toBeVisible();
  });

  test('sidebar navigasyon menüsü çalışıyor', async ({ page }) => {
    // Sidebar görünür
    await expect(page.locator('[data-testid="sidebar"]')).toBeVisible();
    
    // Dashboard linki
    const dashboardLink = page.locator('[data-testid="nav-dashboard"]');
    await expect(dashboardLink).toBeVisible();
    await dashboardLink.click();
    await expect(page).toHaveURL('/');
    
    // Arama linki
    const searchLink = page.locator('[data-testid="nav-search"]');
    await expect(searchLink).toBeVisible();
    
    // Analytics linki
    const analyticsLink = page.locator('[data-testid="nav-analytics"]');
    await expect(analyticsLink).toBeVisible();
    
    // Ayarlar linki
    const settingsLink = page.locator('[data-testid="nav-settings"]');
    await expect(settingsLink).toBeVisible();
  });

  test('istatistik kartları görüntüleniyor', async ({ page }) => {
    // Stats card'ları bekle
    await page.waitForSelector('[data-testid="stats-card"]');
    
    // En az 4 stats card olmalı
    const statsCards = page.locator('[data-testid="stats-card"]');
    await expect(statsCards).toHaveCount(4);
    
    // Her kart başlık ve değer içermeli
    const firstCard = statsCards.first();
    await expect(firstCard.locator('.card-title')).toBeVisible();
    await expect(firstCard.locator('.card-value')).toBeVisible();
  });

  test('arama paneli çalışıyor', async ({ page }) => {
    // Arama input'u
    const searchInput = page.locator('[data-testid="search-input"]');
    await expect(searchInput).toBeVisible();
    
    // Placeholder text
    await expect(searchInput).toHaveAttribute('placeholder', /arama/i);
    
    // Arama türü seçici
    const searchType = page.locator('[data-testid="search-type"]');
    await expect(searchType).toBeVisible();
    
    // Arama butonu
    const searchButton = page.locator('[data-testid="search-button"]');
    await expect(searchButton).toBeVisible();
  });

  test('hızlı işlemler paneli', async ({ page }) => {
    // Quick actions panel
    await expect(page.locator('[data-testid="quick-actions"]')).toBeVisible();
    
    // Reindex butonu
    await expect(page.locator('[data-testid="reindex-button"]')).toBeVisible();
    
    // Clear cache butonu
    await expect(page.locator('[data-testid="clear-cache-button"]')).toBeVisible();
  });

  test('son aktiviteler görüntüleniyor', async ({ page }) => {
    // Recent activity paneli
    const recentActivity = page.locator('[data-testid="recent-activity"]');
    await expect(recentActivity).toBeVisible();
    
    // Aktivite listesi
    const activityItems = recentActivity.locator('.activity-item');
    await expect(activityItems.count()).resolves.toBeGreaterThanOrEqual(0);
  });
});

test.describe('Arama İşlevselliği', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('basic arama çalışıyor', async ({ page }) => {
    // Arama input'una yaz
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('test query');
    
    // Basic search seç
    const searchType = page.locator('[data-testid="search-type"]');
    await searchType.selectOption('basic');
    
    // Arama butonuna bas
    const searchButton = page.locator('[data-testid="search-button"]');
    await searchButton.click();
    
    // Sonuçlar sayfasına yönlendirilmeli
    await page.waitForURL('**/search**');
    
    // Sonuçlar görüntülenmeli
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
  });

  test('semantic arama çalışıyor', async ({ page }) => {
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('authentication system');
    
    const searchType = page.locator('[data-testid="search-type"]');
    await searchType.selectOption('semantic');
    
    const searchButton = page.locator('[data-testid="search-button"]');
    await searchButton.click();
    
    await page.waitForURL('**/search**');
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
  });

  test('arama geçmişi çalışıyor', async ({ page }) => {
    // İlk arama
    const searchInput = page.locator('[data-testid="search-input"]');
    await searchInput.fill('first search');
    
    const searchButton = page.locator('[data-testid="search-button"]');
    await searchButton.click();
    
    await page.waitForURL('**/search**');
    await page.goBack();
    
    // İkinci arama
    await searchInput.fill('second search');
    await searchButton.click();
    
    await page.waitForURL('**/search**');
    
    // Arama geçmişi paneli
    const historyButton = page.locator('[data-testid="search-history"]');
    if (await historyButton.isVisible()) {
      await historyButton.click();
      const historyItems = page.locator('.search-history-item');
      await expect(historyItems.count()).resolves.toBeGreaterThanOrEqual(1);
    }
  });
});

test.describe('Dark Mode Toggle', () => {
  test('dark mode geçişi çalışıyor', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // İlk tema durumunu al
    const html = page.locator('html');
    const initialTheme = await html.getAttribute('class');
    
    // Theme toggle butonuna bas
    const themeToggle = page.locator('[data-testid="theme-toggle"]');
    await themeToggle.click();
    
    // Tema değişmiş olmalı
    await page.waitForTimeout(500); // Animation için bekle
    const newTheme = await html.getAttribute('class');
    expect(newTheme).not.toBe(initialTheme);
    
    // Tekrar bas, eski tema geri gelmeli
    await themeToggle.click();
    await page.waitForTimeout(500);
    const finalTheme = await html.getAttribute('class');
    expect(finalTheme).toBe(initialTheme);
  });
});

test.describe('Responsive Design', () => {
  test('mobil cihazlarda düzgün görünüm', async ({ page }) => {
    // Mobil boyutuna ayarla
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Ana içerik görünür olmalı
    await expect(page.locator('main')).toBeVisible();
    
    // Stats kartları mobilde uyumlu olmalı
    const statsCards = page.locator('[data-testid="stats-card"]');
    await expect(statsCards.first()).toBeVisible();
    
    // Arama paneli responsive olmalı
    await expect(page.locator('[data-testid="search-input"]')).toBeVisible();
  });

  test('tablet boyutunda düzgün görünüm', async ({ page }) => {
    // Tablet boyutuna ayarla
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // İçerik düzenli görünmeli
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('[data-testid="sidebar"]')).toBeVisible();
  });
});

test.describe('Loading States', () => {
  test('loading spinner\'ları görüntüleniyor', async ({ page }) => {
    await page.goto('/');
    
    // Sayfa yüklenirken loading göstergesi olabilir
    const loadingSpinner = page.locator('[data-testid="loading-spinner"]');
    
    // Spinner varsa, sonra kaybolmalı
    if (await loadingSpinner.isVisible()) {
      await expect(loadingSpinner).toBeHidden({ timeout: 10000 });
    }
    
    // Ana içerik yüklenmeli
    await expect(page.locator('main')).toBeVisible();
  });
}); 