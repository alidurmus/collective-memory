// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Search UI Tests
 * Arama sayfası ve işlevsellik testleri
 */

test.describe('Arama Sayfası', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/search');
    await page.waitForLoadState('networkidle');
  });

  test('arama sayfası yükleniyor', async ({ page }) => {
    await expect(page).toHaveTitle(/Collective Memory/);
    await expect(page.locator('h1')).toContainText(/Arama/i);
  });

  test('arama formu bileşenleri', async ({ page }) => {
    // Ana arama input'u
    await expect(page.locator('[data-testid="search-input"]')).toBeVisible();
    
    // Arama türü seçici
    await expect(page.locator('[data-testid="search-type"]')).toBeVisible();
    
    // Maksimum sonuç sayısı
    await expect(page.locator('[data-testid="max-results"]')).toBeVisible();
    
    // Arama butonu
    await expect(page.locator('[data-testid="search-button"]')).toBeVisible();
    
    // Gelişmiş seçenekler toggle
    await expect(page.locator('[data-testid="advanced-options"]')).toBeVisible();
  });

  test('basic arama gerçekleştirme', async ({ page }) => {
    // Arama terimi gir
    await page.fill('[data-testid="search-input"]', 'test query');
    
    // Basic search seç
    await page.selectOption('[data-testid="search-type"]', 'basic');
    
    // Arama yap
    await page.click('[data-testid="search-button"]');
    
    // Sonuçlar yüklenene kadar bekle
    await page.waitForSelector('[data-testid="search-results"]', { timeout: 10000 });
    
    // Sonuçlar konteynerı görünür olmalı
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
    
    // Arama istatistikleri
    await expect(page.locator('[data-testid="search-stats"]')).toBeVisible();
  });

  test('semantic arama gerçekleştirme', async ({ page }) => {
    await page.fill('[data-testid="search-input"]', 'authentication system');
    await page.selectOption('[data-testid="search-type"]', 'semantic');
    await page.click('[data-testid="search-button"]');
    
    await page.waitForSelector('[data-testid="search-results"]', { timeout: 15000 });
    await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
  });

  test('gelişmiş arama seçenekleri', async ({ page }) => {
    // Gelişmiş seçenekleri aç
    await page.click('[data-testid="advanced-options"]');
    
    // Dosya türü filtreleri
    await expect(page.locator('[data-testid="file-type-filter"]')).toBeVisible();
    
    // Tarih aralığı filtreleri
    await expect(page.locator('[data-testid="date-range-filter"]')).toBeVisible();
    
    // Boyut filtreleri
    await expect(page.locator('[data-testid="size-filter"]')).toBeVisible();
  });

  test('arama sonucu filtreleme', async ({ page }) => {
    // Önce bir arama yap
    await page.fill('[data-testid="search-input"]', 'test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]');
    
    // Sıralama seçenekleri
    const sortSelect = page.locator('[data-testid="sort-select"]');
    if (await sortSelect.isVisible()) {
      await sortSelect.selectOption('date');
      await page.waitForTimeout(1000); // Sıralama için bekle
    }
    
    // Dosya türü filtresi
    const fileTypeFilter = page.locator('[data-testid="file-type-filter"]');
    if (await fileTypeFilter.isVisible()) {
      await fileTypeFilter.click();
      const pythonOption = page.locator('input[value="py"]');
      if (await pythonOption.isVisible()) {
        await pythonOption.check();
        await page.waitForTimeout(1000);
      }
    }
  });

  test('arama sonucu dışa aktarma', async ({ page }) => {
    // Arama yap
    await page.fill('[data-testid="search-input"]', 'export test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]');
    
    // Export butonu
    const exportButton = page.locator('[data-testid="export-button"]');
    if (await exportButton.isVisible()) {
      // Export menüsünü aç
      await exportButton.click();
      
      // Markdown export
      const markdownExport = page.locator('[data-testid="export-markdown"]');
      if (await markdownExport.isVisible()) {
        // Download beklentisi
        const downloadPromise = page.waitForEvent('download');
        await markdownExport.click();
        const download = await downloadPromise;
        expect(download.suggestedFilename()).toContain('.md');
      }
    }
  });
});

test.describe('Arama Geçmişi', () => {
  test('arama geçmişi kaydetme', async ({ page }) => {
    await page.goto('/search');
    
    // Birkaç arama yap
    const searchTerms = ['first search', 'second search', 'third search'];
    
    for (const term of searchTerms) {
      await page.fill('[data-testid="search-input"]', term);
      await page.click('[data-testid="search-button"]');
      await page.waitForSelector('[data-testid="search-results"]');
      await page.waitForTimeout(1000);
    }
    
    // Arama geçmişine bak
    const historyButton = page.locator('[data-testid="search-history-toggle"]');
    if (await historyButton.isVisible()) {
      await historyButton.click();
      
      // Geçmiş öğeleri görünür olmalı
      const historyItems = page.locator('[data-testid="history-item"]');
      await expect(historyItems.count()).resolves.toBeGreaterThanOrEqual(1);
    }
  });

  test('geçmişten arama tekrarlama', async ({ page }) => {
    await page.goto('/search');
    
    // Bir arama yap
    await page.fill('[data-testid="search-input"]', 'history test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]');
    
    // Farklı bir arama yap
    await page.fill('[data-testid="search-input"]', 'new search');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]');
    
    // Geçmişi aç
    const historyButton = page.locator('[data-testid="search-history-toggle"]');
    if (await historyButton.isVisible()) {
      await historyButton.click();
      
      // İlk geçmiş öğesine tıkla
      const firstHistoryItem = page.locator('[data-testid="history-item"]').first();
      if (await firstHistoryItem.isVisible()) {
        await firstHistoryItem.click();
        
        // Arama input'u eski terme döner
        const searchInput = page.locator('[data-testid="search-input"]');
        const inputValue = await searchInput.inputValue();
        expect(inputValue.length).toBeGreaterThan(0);
      }
    }
  });
});

test.describe('Arama Performansı', () => {
  test('arama yanıt süresi', async ({ page }) => {
    await page.goto('/search');
    
    // Arama zamanını ölç
    const startTime = Date.now();
    
    await page.fill('[data-testid="search-input"]', 'performance test');
    await page.click('[data-testid="search-button"]');
    
    await page.waitForSelector('[data-testid="search-results"]');
    
    const endTime = Date.now();
    const responseTime = endTime - startTime;
    
    // 10 saniyeden kısa olmalı
    expect(responseTime).toBeLessThan(10000);
    
    // Arama süresi istatistiği görüntülenmeli
    const searchStats = page.locator('[data-testid="search-stats"]');
    await expect(searchStats).toContainText(/ms|saniye/i);
  });

  test('boş arama sonucu', async ({ page }) => {
    await page.goto('/search');
    
    // Sonuç bulunamayacak bir arama
    await page.fill('[data-testid="search-input"]', 'xyzqwertynonexistent123');
    await page.click('[data-testid="search-button"]');
    
    await page.waitForSelector('[data-testid="search-results"]');
    
    // "Sonuç bulunamadı" mesajı
    await expect(page.locator('[data-testid="no-results"]')).toBeVisible();
  });
});

test.describe('Arama Sonuçları', () => {
  test('sonuç kartları format', async ({ page }) => {
    await page.goto('/search');
    
    await page.fill('[data-testid="search-input"]', 'test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]');
    
    // İlk sonuç kartı
    const firstResult = page.locator('[data-testid="result-card"]').first();
    if (await firstResult.isVisible()) {
      // Dosya adı
      await expect(firstResult.locator('.result-filename')).toBeVisible();
      
      // Dosya yolu
      await expect(firstResult.locator('.result-path')).toBeVisible();
      
      // Eşleşme skoru
      await expect(firstResult.locator('.result-score')).toBeVisible();
      
      // Dosya boyutu
      await expect(firstResult.locator('.result-size')).toBeVisible();
    }
  });

  test('sonuç kartı tıklama', async ({ page }) => {
    await page.goto('/search');
    
    await page.fill('[data-testid="search-input"]', 'test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]');
    
    // İlk sonuca tıkla
    const firstResult = page.locator('[data-testid="result-card"]').first();
    if (await firstResult.isVisible()) {
      await firstResult.click();
      
      // Dosya detay modal'ı veya yeni sayfa açılmalı
      const fileModal = page.locator('[data-testid="file-detail-modal"]');
      const fileDetailPage = page.locator('[data-testid="file-detail-page"]');
      
      // Modal veya detay sayfası görünür olmalı
      const isModalVisible = await fileModal.isVisible();
      const isDetailPageVisible = await fileDetailPage.isVisible();
      
      expect(isModalVisible || isDetailPageVisible).toBeTruthy();
    }
  });

  test('pagination çalışması', async ({ page }) => {
    await page.goto('/search');
    
    // Çok sonuç döndürecek bir arama
    await page.fill('[data-testid="search-input"]', 'test');
    await page.selectOption('[data-testid="max-results"]', '5'); // Az sonuç limiti
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('[data-testid="search-results"]');
    
    // Pagination kontrolleri
    const pagination = page.locator('[data-testid="pagination"]');
    if (await pagination.isVisible()) {
      const nextButton = page.locator('[data-testid="pagination-next"]');
      if (await nextButton.isVisible() && !await nextButton.isDisabled()) {
        await nextButton.click();
        await page.waitForTimeout(1000);
        
        // Sayfa değişmiş olmalı
        await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
      }
    }
  });
}); 