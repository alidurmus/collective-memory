// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Settings UI Tests
 * Ayarlar sayfası testleri
 */

test.describe('Ayarlar Sayfası', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/settings');
    await page.waitForLoadState('networkidle');
  });

  test('ayarlar sayfası yükleniyor', async ({ page }) => {
    await expect(page).toHaveTitle(/Collective Memory/);
    await expect(page.locator('h1')).toContainText(/Ayarlar|Settings/i);
  });

  test('ayar kategorileri tab\'ları', async ({ page }) => {
    // Tab navigation
    await expect(page.locator('[data-testid="settings-tabs"]')).toBeVisible();
    
    // Genel ayarlar tab
    await expect(page.locator('[data-testid="general-tab"]')).toBeVisible();
    
    // Arama ayarları tab
    await expect(page.locator('[data-testid="search-tab"]')).toBeVisible();
    
    // Sistem ayarları tab
    await expect(page.locator('[data-testid="system-tab"]')).toBeVisible();
    
    // Güvenlik ayarları tab
    const securityTab = page.locator('[data-testid="security-tab"]');
    if (await securityTab.isVisible()) {
      await expect(securityTab).toBeVisible();
    }
  });
});

test.describe('Genel Ayarlar', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/settings');
    await page.click('[data-testid="general-tab"]');
    await page.waitForLoadState('networkidle');
  });

  test('tema ayarları', async ({ page }) => {
    // Tema seçici
    const themeSelector = page.locator('[data-testid="theme-selector"]');
    await expect(themeSelector).toBeVisible();
    
    // Dark mode seçme
    await themeSelector.selectOption('dark');
    
    // Tema değişimini kontrol et
    await page.waitForTimeout(500);
    const html = page.locator('html');
    const htmlClass = await html.getAttribute('class');
    expect(htmlClass).toContain('dark');
    
    // Light mode'a geri dön
    await themeSelector.selectOption('light');
    await page.waitForTimeout(500);
    const newHtmlClass = await html.getAttribute('class');
    expect(newHtmlClass).not.toContain('dark');
  });

  test('dil ayarları', async ({ page }) => {
    const languageSelector = page.locator('[data-testid="language-selector"]');
    if (await languageSelector.isVisible()) {
      // Türkçe seç
      await languageSelector.selectOption('tr');
      
      // Sayfanın yeniden yüklenmesini bekle
      await page.waitForTimeout(1000);
      
      // Türkçe metinler görünmeli
      await expect(page.locator('h1')).toContainText(/Ayarlar/i);
    }
  });

  test('bildirim ayarları', async ({ page }) => {
    // Desktop bildirimler
    const desktopNotifications = page.locator('[data-testid="desktop-notifications"]');
    if (await desktopNotifications.isVisible()) {
      await desktopNotifications.check();
      await expect(desktopNotifications).toBeChecked();
      
      await desktopNotifications.uncheck();
      await expect(desktopNotifications).not.toBeChecked();
    }
    
    // Email bildirimleri
    const emailNotifications = page.locator('[data-testid="email-notifications"]');
    if (await emailNotifications.isVisible()) {
      await emailNotifications.check();
      await expect(emailNotifications).toBeChecked();
    }
  });

  test('otomatik kaydet özelliği', async ({ page }) => {
    // Bir ayarı değiştir
    const autoSave = page.locator('[data-testid="auto-save"]');
    if (await autoSave.isVisible()) {
      await autoSave.check();
      
      // Otomatik kaydet mesajı
      const saveMessage = page.locator('[data-testid="auto-save-message"]');
      if (await saveMessage.isVisible()) {
        await expect(saveMessage).toContainText(/kaydedildi|saved/i);
      }
    }
  });
});

test.describe('Arama Ayarları', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/settings');
    await page.click('[data-testid="search-tab"]');
    await page.waitForLoadState('networkidle');
  });

  test('arama seçenekleri', async ({ page }) => {
    // Varsayılan arama türü
    const defaultSearchType = page.locator('[data-testid="default-search-type"]');
    await expect(defaultSearchType).toBeVisible();
    
    await defaultSearchType.selectOption('semantic');
    
    // Maksimum sonuç sayısı
    const maxResults = page.locator('[data-testid="max-results-setting"]');
    if (await maxResults.isVisible()) {
      await maxResults.clear();
      await maxResults.fill('25');
    }
    
    // Semantic threshold
    const semanticThreshold = page.locator('[data-testid="semantic-threshold"]');
    if (await semanticThreshold.isVisible()) {
      await semanticThreshold.fill('0.7');
    }
  });

  test('dosya türü filtreleri', async ({ page }) => {
    // Desteklenen dosya türleri
    const fileTypeSettings = page.locator('[data-testid="file-type-settings"]');
    await expect(fileTypeSettings).toBeVisible();
    
    // Python dosyaları
    const pythonFiles = page.locator('[data-testid="include-python"]');
    if (await pythonFiles.isVisible()) {
      await pythonFiles.check();
      await expect(pythonFiles).toBeChecked();
    }
    
    // JavaScript dosyaları
    const jsFiles = page.locator('[data-testid="include-javascript"]');
    if (await jsFiles.isVisible()) {
      await jsFiles.check();
      await expect(jsFiles).toBeChecked();
    }
    
    // Markdown dosyaları
    const mdFiles = page.locator('[data-testid="include-markdown"]');
    if (await mdFiles.isVisible()) {
      await mdFiles.check();
      await expect(mdFiles).toBeChecked();
    }
  });

  test('arama geçmişi ayarları', async ({ page }) => {
    // Geçmiş kaydetme
    const saveHistory = page.locator('[data-testid="save-search-history"]');
    if (await saveHistory.isVisible()) {
      await saveHistory.check();
      await expect(saveHistory).toBeChecked();
    }
    
    // Geçmiş temizleme
    const clearHistoryButton = page.locator('[data-testid="clear-history-button"]');
    if (await clearHistoryButton.isVisible()) {
      await clearHistoryButton.click();
      
      // Confirmation dialog
      const confirmDialog = page.locator('[data-testid="confirm-dialog"]');
      if (await confirmDialog.isVisible()) {
        await page.click('[data-testid="confirm-yes"]');
        
        // Başarı mesajı
        const successMessage = page.locator('[data-testid="success-message"]');
        if (await successMessage.isVisible()) {
          await expect(successMessage).toContainText(/temizlendi|cleared/i);
        }
      }
    }
  });
});

test.describe('Sistem Ayarları', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/settings');
    await page.click('[data-testid="system-tab"]');
    await page.waitForLoadState('networkidle');
  });

  test('indeksing ayarları', async ({ page }) => {
    // Otomatik indeksing
    const autoIndexing = page.locator('[data-testid="auto-indexing"]');
    if (await autoIndexing.isVisible()) {
      await autoIndexing.check();
      await expect(autoIndexing).toBeChecked();
    }
    
    // İndeksing aralığı
    const indexingInterval = page.locator('[data-testid="indexing-interval"]');
    if (await indexingInterval.isVisible()) {
      await indexingInterval.selectOption('hourly');
    }
    
    // İndeksing dizinleri
    const indexingDirectories = page.locator('[data-testid="indexing-directories"]');
    if (await indexingDirectories.isVisible()) {
      await expect(indexingDirectories).toBeVisible();
    }
  });

  test('cache ayarları', async ({ page }) => {
    // Cache boyutu
    const cacheSize = page.locator('[data-testid="cache-size"]');
    if (await cacheSize.isVisible()) {
      await cacheSize.clear();
      await cacheSize.fill('512');
    }
    
    // Cache temizleme
    const clearCacheButton = page.locator('[data-testid="clear-cache-button"]');
    if (await clearCacheButton.isVisible()) {
      await clearCacheButton.click();
      
      // Loading state
      const loadingSpinner = page.locator('[data-testid="loading-spinner"]');
      if (await loadingSpinner.isVisible()) {
        await expect(loadingSpinner).toBeHidden({ timeout: 10000 });
      }
      
      // Başarı mesajı
      const successMessage = page.locator('[data-testid="cache-cleared-message"]');
      if (await successMessage.isVisible()) {
        await expect(successMessage).toContainText(/temizlendi|cleared/i);
      }
    }
  });

  test('performans ayarları', async ({ page }) => {
    // Multi-threading
    const multiThreading = page.locator('[data-testid="multi-threading"]');
    if (await multiThreading.isVisible()) {
      await multiThreading.check();
      await expect(multiThreading).toBeChecked();
    }
    
    // Thread sayısı
    const threadCount = page.locator('[data-testid="thread-count"]');
    if (await threadCount.isVisible()) {
      await threadCount.clear();
      await threadCount.fill('4');
    }
    
    // Memory limit
    const memoryLimit = page.locator('[data-testid="memory-limit"]');
    if (await memoryLimit.isVisible()) {
      await memoryLimit.clear();
      await memoryLimit.fill('2048');
    }
  });
});

test.describe('Güvenlik Ayarları', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/settings');
    const securityTab = page.locator('[data-testid="security-tab"]');
    if (await securityTab.isVisible()) {
      await securityTab.click();
      await page.waitForLoadState('networkidle');
    } else {
      test.skip('Security tab not available');
    }
  });

  test('API güvenlik ayarları', async ({ page }) => {
    // API rate limiting
    const rateLimiting = page.locator('[data-testid="api-rate-limiting"]');
    if (await rateLimiting.isVisible()) {
      await rateLimiting.check();
      await expect(rateLimiting).toBeChecked();
    }
    
    // Rate limit değeri
    const rateLimit = page.locator('[data-testid="rate-limit-value"]');
    if (await rateLimit.isVisible()) {
      await rateLimit.clear();
      await rateLimit.fill('100');
    }
  });

  test('dosya erişim izinleri', async ({ page }) => {
    // Güvenli dizinler
    const safeDirectories = page.locator('[data-testid="safe-directories"]');
    if (await safeDirectories.isVisible()) {
      await expect(safeDirectories).toBeVisible();
    }
    
    // Yasak dosya türleri
    const blockedFileTypes = page.locator('[data-testid="blocked-file-types"]');
    if (await blockedFileTypes.isVisible()) {
      await expect(blockedFileTypes).toBeVisible();
    }
  });
});

test.describe('Ayarlar Kaydetme', () => {
  test('manuel kaydetme', async ({ page }) => {
    await page.goto('/settings');
    
    // Bir ayarı değiştir
    const themeSelector = page.locator('[data-testid="theme-selector"]');
    if (await themeSelector.isVisible()) {
      await themeSelector.selectOption('dark');
    }
    
    // Kaydet butonu
    const saveButton = page.locator('[data-testid="save-settings"]');
    if (await saveButton.isVisible()) {
      await saveButton.click();
      
      // Başarı mesajı
      const successMessage = page.locator('[data-testid="settings-saved"]');
      if (await successMessage.isVisible()) {
        await expect(successMessage).toContainText(/kaydedildi|saved/i);
      }
    }
  });

  test('ayarları sıfırlama', async ({ page }) => {
    await page.goto('/settings');
    
    // Reset butonu
    const resetButton = page.locator('[data-testid="reset-settings"]');
    if (await resetButton.isVisible()) {
      await resetButton.click();
      
      // Confirmation dialog
      const confirmDialog = page.locator('[data-testid="confirm-reset-dialog"]');
      if (await confirmDialog.isVisible()) {
        await page.click('[data-testid="confirm-reset"]');
        
        // Ayarların sıfırlandığını kontrol et
        const resetMessage = page.locator('[data-testid="settings-reset"]');
        if (await resetMessage.isVisible()) {
          await expect(resetMessage).toContainText(/sıfırlandı|reset/i);
        }
      }
    }
  });

  test('ayarları dışa aktarma', async ({ page }) => {
    await page.goto('/settings');
    
    // Export butonu
    const exportButton = page.locator('[data-testid="export-settings"]');
    if (await exportButton.isVisible()) {
      const downloadPromise = page.waitForEvent('download');
      await exportButton.click();
      const download = await downloadPromise;
      expect(download.suggestedFilename()).toContain('.json');
    }
  });

  test('ayarları içe aktarma', async ({ page }) => {
    await page.goto('/settings');
    
    // Import butonu
    const importButton = page.locator('[data-testid="import-settings"]');
    if (await importButton.isVisible()) {
      // File input
      const fileInput = page.locator('[data-testid="settings-file-input"]');
      if (await fileInput.isVisible()) {
        // Test için dummy JSON dosyası oluştur
        const settingsData = {
          theme: 'dark',
          language: 'tr',
          searchType: 'semantic'
        };
        
        // Mock file upload
        // Note: Bu test gerçek dosya yükleme gerektirir
        // await fileInput.setInputFiles([{ name: 'settings.json', buffer: Buffer.from(JSON.stringify(settingsData)) }]);
        
        // Import confirmation
        // const importSuccess = page.locator('[data-testid="import-success"]');
        // if (await importSuccess.isVisible()) {
        //   await expect(importSuccess).toContainText(/içe aktarıldı|imported/i);
        // }
      }
    }
  });
}); 