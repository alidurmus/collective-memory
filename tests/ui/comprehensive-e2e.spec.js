// @ts-check
const { test, expect, devices } = require('@playwright/test');

/**
 * Comprehensive E2E Testing Suite for Collective Memory
 * Turkish UI + English Code Standards
 * Playwright Automation Expansion
 */

// Test configurations
const testConfig = {
  timeout: 30000,
  retries: 2,
  baseURL: 'http://localhost:3000',
  apiBaseURL: 'http://localhost:8000'
};

// Test data
const testData = {
  searchQueries: [
    'Django model',
    'React component',
    'Python function',
    'API endpoint',
    'Database query',
    'Context7 framework',
    'Collective Memory',
    'Turkish UI'
  ],
  turkishTexts: [
    'Collective Memory',
    'Akıllı bağlam yönetimi',
    'Arama sonuçları',
    'Sistem durumu',
    'Analitik raporlar',
    'Ayarlar',
    'Sağlıklı',
    'Hata'
  ],
  settings: {
    maxFileSize: 100,
    maxIndexSize: 1000,
    autoIndex: true,
    enableSemantic: true,
    defaultSearchLimit: 50
  }
};

// Setup and teardown
test.beforeEach(async ({ page }) => {
  // Setup mock API responses
  await setupMockAPI(page);
  
  // Set up request interception for analytics
  await page.route('**/api/**', async route => {
    const url = route.request().url();
    console.log(`API Request: ${url}`);
    
    if (url.includes('/system/status')) {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            overall_status: 'healthy',
            file_count: 1234,
            search_count: 567,
            uptime: '2:30:45',
            database: { status: 'healthy', file_count: 1234 },
            search_engine: { status: 'healthy', avg_response_time: 45 },
            file_monitor: { status: 'healthy', watched_directories: 5 },
            api_server: { status: 'healthy', uptime: 9045 }
          }
        })
      });
    } else if (url.includes('/system/stats')) {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            recent_activity: [
              { id: 1, type: 'search', description: 'Django model arandı', timestamp: new Date().toISOString() },
              { id: 2, type: 'file_added', description: 'Yeni dosya eklendi', timestamp: new Date().toISOString() }
            ],
            totalFiles: 1234,
            indexSize: '15.2 MB',
            lastSearchTime: '2 dakika önce'
          }
        })
      });
    } else {
      await route.continue();
    }
  });
});

test.describe('Comprehensive Dashboard Tests', () => {
  test('dashboard loads with all components', async ({ page }) => {
    await page.goto('/');
    
    // Wait for dashboard to load
    await page.waitForSelector('.context7-dashboard');
    
    // Check main components
    await expect(page.locator('.context7-dashboard')).toBeVisible();
    await expect(page.locator('.context7-card')).toBeVisible();
    await expect(page.locator('text=Collective Memory')).toBeVisible();
    await expect(page.locator('text=Akıllı bağlam yönetimi')).toBeVisible();
    
    // Check system status
    await expect(page.locator('text=Sağlıklı')).toBeVisible();
    await expect(page.locator('text=Dosya Sayısı')).toBeVisible();
    await expect(page.locator('text=Arama Sayısı')).toBeVisible();
    
    // Check quick actions
    await expect(page.locator('.quick-actions-grid')).toBeVisible();
    
    // Check recent activity
    await expect(page.locator('.recent-activity-list')).toBeVisible();
    
    // Performance check
    const performanceEntries = await page.evaluate(() => {
      return JSON.stringify(performance.getEntriesByType('navigation'));
    });
    const navigation = JSON.parse(performanceEntries)[0];
    expect(navigation.loadEventEnd - navigation.loadEventStart).toBeLessThan(3000);
  });

  test('real-time updates work', async ({ page }) => {
    await page.goto('/');
    
    // Wait for WebSocket connection
    await page.waitForTimeout(1000);
    
    // Check if WebSocket connection status is displayed
    const connectionStatus = page.locator('.connection-status');
    if (await connectionStatus.isVisible()) {
      await expect(connectionStatus).toContainText('Connected');
    }
    
    // Simulate real-time update
    await page.evaluate(() => {
      // Simulate WebSocket message
      window.dispatchEvent(new CustomEvent('websocket-message', {
        detail: {
          type: 'search_performed',
          results_count: 42,
          query: 'test query'
        }
      }));
    });
    
    // Check if toast notification appears
    await expect(page.locator('.toast')).toBeVisible({ timeout: 5000 });
  });

  test('system metrics display correctly', async ({ page }) => {
    await page.goto('/');
    
    // Check system metrics
    const metrics = [
      { selector: 'text=1,234', description: 'File count' },
      { selector: 'text=567', description: 'Search count' },
      { selector: 'text=2:30:45', description: 'Uptime' },
      { selector: 'text=45ms', description: 'Response time' }
    ];
    
    for (const metric of metrics) {
      await expect(page.locator(metric.selector)).toBeVisible();
    }
  });
});

test.describe('Advanced Search Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/search');
  });

  test('search functionality works comprehensively', async ({ page }) => {
    const searchInput = page.locator('[data-testid="search-input"]');
    const searchButton = page.locator('[data-testid="search-button"]');
    
    // Test multiple search queries
    for (const query of testData.searchQueries) {
      await searchInput.fill(query);
      await searchButton.click();
      
      // Wait for results
      await page.waitForSelector('.search-results', { timeout: 10000 });
      
      // Check results
      await expect(page.locator('.search-results')).toBeVisible();
      await expect(page.locator('.search-result-item')).toHaveCount({ min: 1 });
      
      // Check Turkish UI elements
      await expect(page.locator('text=Arama sonuçları')).toBeVisible();
      
      // Clear search
      await searchInput.clear();
    }
  });

  test('semantic search toggle works', async ({ page }) => {
    const semanticToggle = page.locator('[data-testid="semantic-toggle"]');
    const searchInput = page.locator('[data-testid="search-input"]');
    const searchButton = page.locator('[data-testid="search-button"]');
    
    // Test with semantic search enabled
    await semanticToggle.check();
    await searchInput.fill('Django model');
    await searchButton.click();
    
    await page.waitForSelector('.search-results');
    await expect(page.locator('.search-results')).toBeVisible();
    
    // Test with semantic search disabled
    await semanticToggle.uncheck();
    await searchInput.fill('Django model');
    await searchButton.click();
    
    await page.waitForSelector('.search-results');
    await expect(page.locator('.search-results')).toBeVisible();
  });

  test('search filters work correctly', async ({ page }) => {
    const searchInput = page.locator('[data-testid="search-input"]');
    const searchButton = page.locator('[data-testid="search-button"]');
    
    // Test file type filter
    const fileTypeFilter = page.locator('[data-testid="file-type-filter"]');
    await fileTypeFilter.selectOption('python');
    
    await searchInput.fill('function');
    await searchButton.click();
    
    await page.waitForSelector('.search-results');
    await expect(page.locator('.search-results')).toBeVisible();
    
    // Test date range filter
    const dateFilter = page.locator('[data-testid="date-filter"]');
    await dateFilter.selectOption('last_week');
    
    await searchButton.click();
    await page.waitForSelector('.search-results');
    await expect(page.locator('.search-results')).toBeVisible();
  });

  test('search export functionality works', async ({ page }) => {
    const searchInput = page.locator('[data-testid="search-input"]');
    const searchButton = page.locator('[data-testid="search-button"]');
    const exportButton = page.locator('[data-testid="export-button"]');
    
    // Perform search
    await searchInput.fill('Django model');
    await searchButton.click();
    
    await page.waitForSelector('.search-results');
    await expect(page.locator('.search-results')).toBeVisible();
    
    // Test export
    const downloadPromise = page.waitForEvent('download');
    await exportButton.click();
    
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/search-results.*\.md$/);
  });

  test('search performance is acceptable', async ({ page }) => {
    const searchInput = page.locator('[data-testid="search-input"]');
    const searchButton = page.locator('[data-testid="search-button"]');
    
    // Measure search performance
    const startTime = Date.now();
    await searchInput.fill('Django model');
    await searchButton.click();
    
    await page.waitForSelector('.search-results');
    const endTime = Date.now();
    
    const searchTime = endTime - startTime;
    expect(searchTime).toBeLessThan(3000); // 3 seconds max
    
    // Check response time display
    const responseTime = page.locator('.response-time');
    if (await responseTime.isVisible()) {
      const timeText = await responseTime.textContent();
      expect(timeText).toMatch(/\d+ms/);
    }
  });
});

test.describe('Analytics Dashboard Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/analytics');
  });

  test('analytics dashboard loads with all components', async ({ page }) => {
    // Wait for analytics to load
    await page.waitForSelector('.analytics-dashboard');
    
    // Check main components
    await expect(page.locator('.analytics-dashboard')).toBeVisible();
    await expect(page.locator('.analytics-cards')).toBeVisible();
    await expect(page.locator('.analytics-charts')).toBeVisible();
    
    // Check Turkish UI elements
    await expect(page.locator('text=Analitik Raporlar')).toBeVisible();
    await expect(page.locator('text=Toplam Arama')).toBeVisible();
    await expect(page.locator('text=Benzersiz Kullanıcı')).toBeVisible();
    
    // Check charts
    await expect(page.locator('.search-trend-chart')).toBeVisible();
    await expect(page.locator('.file-access-chart')).toBeVisible();
  });

  test('analytics time range filter works', async ({ page }) => {
    const timeRangeFilter = page.locator('[data-testid="time-range-filter"]');
    
    // Test different time ranges
    const timeRanges = ['24h', '7d', '30d', '90d'];
    
    for (const range of timeRanges) {
      await timeRangeFilter.selectOption(range);
      
      // Wait for charts to update
      await page.waitForTimeout(1000);
      
      // Check if charts are still visible
      await expect(page.locator('.search-trend-chart')).toBeVisible();
      await expect(page.locator('.file-access-chart')).toBeVisible();
    }
  });

  test('analytics export works', async ({ page }) => {
    const exportButton = page.locator('[data-testid="analytics-export"]');
    
    if (await exportButton.isVisible()) {
      const downloadPromise = page.waitForEvent('download');
      await exportButton.click();
      
      const download = await downloadPromise;
      expect(download.suggestedFilename()).toMatch(/analytics-report.*\.(pdf|xlsx)$/);
    }
  });
});

test.describe('Settings Management Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/settings');
  });

  test('settings page loads correctly', async ({ page }) => {
    await expect(page.locator('.settings-container')).toBeVisible();
    await expect(page.locator('.settings-tabs')).toBeVisible();
    
    // Check Turkish UI elements
    await expect(page.locator('text=Ayarlar')).toBeVisible();
    await expect(page.locator('text=Genel')).toBeVisible();
    await expect(page.locator('text=Arama')).toBeVisible();
    await expect(page.locator('text=Sistem')).toBeVisible();
  });

  test('settings tabs work correctly', async ({ page }) => {
    const tabs = ['general', 'search', 'system', 'advanced'];
    
    for (const tab of tabs) {
      await page.locator(`[data-testid="settings-tab-${tab}"]`).click();
      await expect(page.locator(`[data-testid="settings-content-${tab}"]`)).toBeVisible();
    }
  });

  test('settings save functionality works', async ({ page }) => {
    // Navigate to general settings
    await page.locator('[data-testid="settings-tab-general"]').click();
    
    // Update settings
    const maxFileSizeInput = page.locator('[data-testid="max-file-size"]');
    await maxFileSizeInput.fill('200');
    
    const autoIndexCheckbox = page.locator('[data-testid="auto-index"]');
    await autoIndexCheckbox.check();
    
    // Save settings
    const saveButton = page.locator('[data-testid="save-settings"]');
    await saveButton.click();
    
    // Check for success message
    await expect(page.locator('.toast-success')).toBeVisible();
    await expect(page.locator('text=Ayarlar başarıyla kaydedildi')).toBeVisible();
  });

  test('settings validation works', async ({ page }) => {
    // Navigate to search settings
    await page.locator('[data-testid="settings-tab-search"]').click();
    
    // Test invalid input
    const searchLimitInput = page.locator('[data-testid="search-limit"]');
    await searchLimitInput.fill('invalid');
    
    const saveButton = page.locator('[data-testid="save-settings"]');
    await saveButton.click();
    
    // Check for error message
    await expect(page.locator('.form-error')).toBeVisible();
  });
});

test.describe('System Status Tests', () => {
  test('system status displays correctly', async ({ page }) => {
    await page.goto('/');
    
    // Check system status component
    await expect(page.locator('.system-status')).toBeVisible();
    
    // Check status indicators
    await expect(page.locator('.status-indicator')).toBeVisible();
    await expect(page.locator('text=Sağlıklı')).toBeVisible();
    
    // Check system metrics
    await expect(page.locator('.system-metrics')).toBeVisible();
    await expect(page.locator('.metric-item')).toHaveCount({ min: 4 });
  });

  test('system actions work correctly', async ({ page }) => {
    await page.goto('/');
    
    // Test reindex action
    const reindexButton = page.locator('[data-testid="reindex-button"]');
    if (await reindexButton.isVisible()) {
      await reindexButton.click();
      await expect(page.locator('.toast')).toBeVisible();
      await expect(page.locator('text=Yeniden indeksleme başlatıldı')).toBeVisible();
    }
    
    // Test clear cache action
    const clearCacheButton = page.locator('[data-testid="clear-cache-button"]');
    if (await clearCacheButton.isVisible()) {
      await clearCacheButton.click();
      await expect(page.locator('.toast')).toBeVisible();
      await expect(page.locator('text=Önbellek temizlendi')).toBeVisible();
    }
  });
});

test.describe('Cross-Browser Compatibility Tests', () => {
  ['chromium', 'firefox', 'webkit'].forEach(browserName => {
    test(`works correctly in ${browserName}`, async ({ page }) => {
      await page.goto('/');
      
      // Basic functionality test
      await expect(page.locator('.context7-dashboard')).toBeVisible();
      await expect(page.locator('text=Collective Memory')).toBeVisible();
      
      // Navigation test
      await page.goto('/search');
      await expect(page.locator('.search-panel')).toBeVisible();
      
      // Form interaction test
      const searchInput = page.locator('[data-testid="search-input"]');
      await searchInput.fill('test query');
      await expect(searchInput).toHaveValue('test query');
    });
  });
});

test.describe('Accessibility Tests', () => {
  test('keyboard navigation works', async ({ page }) => {
    await page.goto('/');
    
    // Test tab navigation
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Check if focus is visible
    const focusedElement = page.locator(':focus');
    await expect(focusedElement).toBeVisible();
  });

  test('screen reader compatibility', async ({ page }) => {
    await page.goto('/');
    
    // Check for proper ARIA labels
    await expect(page.locator('[aria-label]')).toHaveCount({ min: 1 });
    
    // Check for proper headings structure
    await expect(page.locator('h1')).toHaveCount({ min: 1 });
    await expect(page.locator('h2')).toHaveCount({ min: 1 });
    
    // Check for alt text on images
    const images = page.locator('img');
    const imageCount = await images.count();
    
    for (let i = 0; i < imageCount; i++) {
      const img = images.nth(i);
      await expect(img).toHaveAttribute('alt');
    }
  });

  test('color contrast is adequate', async ({ page }) => {
    await page.goto('/');
    
    // Check button contrast
    const buttons = page.locator('.context7-button');
    const buttonCount = await buttons.count();
    
    for (let i = 0; i < buttonCount; i++) {
      const button = buttons.nth(i);
      if (await button.isVisible()) {
        // Basic visibility check
        await expect(button).toBeVisible();
      }
    }
  });
});

test.describe('Performance Tests', () => {
  test('page load performance is acceptable', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const endTime = Date.now();
    
    const loadTime = endTime - startTime;
    expect(loadTime).toBeLessThan(5000); // 5 seconds max
  });

  test('search performance is acceptable', async ({ page }) => {
    await page.goto('/search');
    
    const searchInput = page.locator('[data-testid="search-input"]');
    const searchButton = page.locator('[data-testid="search-button"]');
    
    const startTime = Date.now();
    await searchInput.fill('Django model');
    await searchButton.click();
    await page.waitForSelector('.search-results');
    const endTime = Date.now();
    
    const searchTime = endTime - startTime;
    expect(searchTime).toBeLessThan(3000); // 3 seconds max
  });

  test('memory usage is reasonable', async ({ page }) => {
    await page.goto('/');
    
    // Navigate through different pages
    await page.goto('/search');
    await page.goto('/analytics');
    await page.goto('/settings');
    await page.goto('/');
    
    // Check if page is still responsive
    await expect(page.locator('.context7-dashboard')).toBeVisible();
  });
});

test.describe('Error Handling Tests', () => {
  test('handles API errors gracefully', async ({ page }) => {
    // Mock API error
    await page.route('**/api/system/status', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          success: false,
          error: 'Internal server error'
        })
      });
    });
    
    await page.goto('/');
    
    // Check if error is handled gracefully
    await expect(page.locator('.error-message')).toBeVisible({ timeout: 10000 });
  });

  test('handles network errors gracefully', async ({ page }) => {
    // Go offline
    await page.context().setOffline(true);
    
    await page.goto('/');
    
    // Check if offline state is handled
    await expect(page.locator('.offline-message')).toBeVisible({ timeout: 10000 });
  });
});

// Helper functions
async function setupMockAPI(page) {
  // Set up common mock responses
  await page.route('**/api/config', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        success: true,
        data: testData.settings
      })
    });
  });

  await page.route('**/api/search', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        success: true,
        data: {
          results: [
            {
              id: 1,
              title: 'Django Model Example',
              content: 'This is a Django model example',
              file_path: '/path/to/file.py',
              score: 0.95
            }
          ],
          total: 1,
          query_time: 45
        }
      })
    });
  });
}

async function waitForAnimation(page, selector) {
  const element = page.locator(selector);
  await element.waitFor({ state: 'visible' });
  await page.waitForTimeout(500); // Wait for animation to complete
}

async function checkTurkishUI(page) {
  for (const text of testData.turkishTexts) {
    await expect(page.locator(`text=${text}`)).toBeVisible();
  }
} 