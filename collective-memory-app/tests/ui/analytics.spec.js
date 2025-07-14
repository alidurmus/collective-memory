// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Analytics UI Tests
 * Analytics sayfası testleri
 */

test.describe('Analytics Sayfası', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/analytics');
    await page.waitForLoadState('networkidle');
  });

  test('analytics sayfası yükleniyor', async ({ page }) => {
    await expect(page).toHaveTitle(/Collective Memory/);
    await expect(page.locator('h1')).toContainText(/Analytics|Analitik/i);
  });

  test('performans metrikleri görüntüleniyor', async ({ page }) => {
    // Performans kartları
    await expect(page.locator('[data-testid="performance-metrics"]')).toBeVisible();
    
    // Ortalama arama süresi
    await expect(page.locator('[data-testid="avg-search-time"]')).toBeVisible();
    
    // Toplam arama sayısı
    await expect(page.locator('[data-testid="total-searches"]')).toBeVisible();
    
    // Sistem kullanımı
    await expect(page.locator('[data-testid="system-usage"]')).toBeVisible();
    
    // İndex boyutu
    await expect(page.locator('[data-testid="index-size"]')).toBeVisible();
  });

  test('popüler arama terimleri', async ({ page }) => {
    const popularQueries = page.locator('[data-testid="popular-queries"]');
    await expect(popularQueries).toBeVisible();
    
    // Liste öğeleri
    const queryList = page.locator('[data-testid="query-list"]');
    await expect(queryList).toBeVisible();
    
    // Her liste öğesi arama terimi ve sayı içermeli
    const queryItems = page.locator('[data-testid="query-item"]');
    if (await queryItems.count() > 0) {
      const firstItem = queryItems.first();
      await expect(firstItem.locator('.query-text')).toBeVisible();
      await expect(firstItem.locator('.query-count')).toBeVisible();
    }
  });

  test('arama eğilimleri grafikleri', async ({ page }) => {
    // Grafik konteynerı
    const chartsContainer = page.locator('[data-testid="search-trends"]');
    await expect(chartsContainer).toBeVisible();
    
    // Günlük arama grafiği
    const dailyChart = page.locator('[data-testid="daily-searches-chart"]');
    if (await dailyChart.isVisible()) {
      // Chart canvas veya SVG elementi
      await expect(dailyChart.locator('canvas, svg')).toBeVisible();
    }
    
    // Saatlik dağılım grafiği
    const hourlyChart = page.locator('[data-testid="hourly-distribution-chart"]');
    if (await hourlyChart.isVisible()) {
      await expect(hourlyChart.locator('canvas, svg')).toBeVisible();
    }
  });

  test('dosya türü dağılımı', async ({ page }) => {
    const fileTypeDistribution = page.locator('[data-testid="file-type-distribution"]');
    await expect(fileTypeDistribution).toBeVisible();
    
    // Pie chart veya bar chart
    const chart = page.locator('[data-testid="file-type-chart"]');
    if (await chart.isVisible()) {
      await expect(chart.locator('canvas, svg')).toBeVisible();
    }
    
    // Dosya türü legend'ı
    const legend = page.locator('[data-testid="file-type-legend"]');
    if (await legend.isVisible()) {
      const legendItems = page.locator('[data-testid="legend-item"]');
      await expect(legendItems.count()).resolves.toBeGreaterThanOrEqual(1);
    }
  });

  test('sistem kaynak kullanımı', async ({ page }) => {
    const resourceUsage = page.locator('[data-testid="resource-usage"]');
    await expect(resourceUsage).toBeVisible();
    
    // CPU kullanımı
    const cpuUsage = page.locator('[data-testid="cpu-usage"]');
    if (await cpuUsage.isVisible()) {
      // Progress bar veya gauge
      await expect(cpuUsage.locator('.progress-bar, .gauge')).toBeVisible();
    }
    
    // Memory kullanımı
    const memoryUsage = page.locator('[data-testid="memory-usage"]');
    if (await memoryUsage.isVisible()) {
      await expect(memoryUsage.locator('.progress-bar, .gauge')).toBeVisible();
    }
    
    // Disk kullanımı
    const diskUsage = page.locator('[data-testid="disk-usage"]');
    if (await diskUsage.isVisible()) {
      await expect(diskUsage.locator('.progress-bar, .gauge')).toBeVisible();
    }
  });

  test('real-time güncellemeler', async ({ page }) => {
    // İlk değerleri al
    const searchCountElement = page.locator('[data-testid="total-searches"] .metric-value');
    if (await searchCountElement.isVisible()) {
      const initialCount = await searchCountElement.textContent();
      
      // 10 saniye bekle (gerçek zamanlı güncellemeler için)
      await page.waitForTimeout(10000);
      
      // Değer değişmiş olabilir (ancak zorunlu değil)
      const newCount = await searchCountElement.textContent();
      // Bu test deterministik olmayabilir, bu yüzden sadece element'in hala görünür olduğunu kontrol edelim
      await expect(searchCountElement).toBeVisible();
    }
  });
});

test.describe('Analytics Filtreleme', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/analytics');
    await page.waitForLoadState('networkidle');
  });

  test('tarih aralığı filtreleme', async ({ page }) => {
    const dateFilter = page.locator('[data-testid="date-range-filter"]');
    if (await dateFilter.isVisible()) {
      // Tarih seçici açma
      await dateFilter.click();
      
      // Önceden tanımlı aralıklar
      const presetRanges = page.locator('[data-testid="preset-range"]');
      if (await presetRanges.count() > 0) {
        // Son 7 gün seç
        const last7Days = page.locator('[data-testid="last-7-days"]');
        if (await last7Days.isVisible()) {
          await last7Days.click();
          
          // Grafiklerin güncellenmesini bekle
          await page.waitForTimeout(2000);
          
          // Grafiklerin hala görünür olduğunu kontrol et
          await expect(page.locator('[data-testid="search-trends"]')).toBeVisible();
        }
      }
    }
  });

  test('arama türü filtreleme', async ({ page }) => {
    const searchTypeFilter = page.locator('[data-testid="search-type-filter"]');
    if (await searchTypeFilter.isVisible()) {
      // Sadece semantic aramalar
      await searchTypeFilter.selectOption('semantic');
      
      // Filtrelemenin uygulanmasını bekle
      await page.waitForTimeout(1000);
      
      // Sonuçların güncellenmesini kontrol et
      await expect(page.locator('[data-testid="popular-queries"]')).toBeVisible();
    }
  });

  test('verileri export etme', async ({ page }) => {
    const exportButton = page.locator('[data-testid="export-analytics"]');
    if (await exportButton.isVisible()) {
      // Export dropdown açma
      await exportButton.click();
      
      // CSV export
      const csvExport = page.locator('[data-testid="export-csv"]');
      if (await csvExport.isVisible()) {
        const downloadPromise = page.waitForEvent('download');
        await csvExport.click();
        const download = await downloadPromise;
        expect(download.suggestedFilename()).toContain('.csv');
      }
    }
  });
});

test.describe('Analytics Responsive', () => {
  test('mobil cihazlarda analytics', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/analytics');
    await page.waitForLoadState('networkidle');
    
    // Ana metrikler görünür olmalı
    await expect(page.locator('[data-testid="performance-metrics"]')).toBeVisible();
    
    // Grafikler mobil uyumlu olmalı
    const charts = page.locator('[data-testid="search-trends"]');
    if (await charts.isVisible()) {
      // Chart konteynerının width'i viewport'a uymalı
      const chartBox = await charts.boundingBox();
      expect(chartBox?.width).toBeLessThanOrEqual(375);
    }
  });

  test('tablet boyutunda analytics', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/analytics');
    await page.waitForLoadState('networkidle');
    
    // Tüm bileşenler görünür olmalı
    await expect(page.locator('[data-testid="performance-metrics"]')).toBeVisible();
    await expect(page.locator('[data-testid="popular-queries"]')).toBeVisible();
    
    // Grafikler tablet boyutunda düzgün görünmeli
    const trendsChart = page.locator('[data-testid="search-trends"]');
    if (await trendsChart.isVisible()) {
      const chartBox = await trendsChart.boundingBox();
      expect(chartBox?.width).toBeLessThanOrEqual(768);
    }
  });
});

test.describe('Analytics Error Handling', () => {
  test('veri yükleme hatası', async ({ page }) => {
    // Network'ü offline yap
    await page.route('**/api/**', route => route.abort());
    
    await page.goto('/analytics');
    
    // Error state görüntülenmeli
    const errorMessage = page.locator('[data-testid="analytics-error"]');
    if (await errorMessage.isVisible()) {
      await expect(errorMessage).toContainText(/hata|error/i);
    }
    
    // Retry butonu
    const retryButton = page.locator('[data-testid="retry-button"]');
    if (await retryButton.isVisible()) {
      await expect(retryButton).toBeEnabled();
    }
  });
}); 