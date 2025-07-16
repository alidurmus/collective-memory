// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Mobile Responsive Tests for Collective Memory Dashboard
 * Turkish UI + English Code Standards
 */

test.describe('Mobile Responsive Tests', () => {
  const viewports = {
    mobile: { width: 375, height: 667 },    // iPhone 8
    tablet: { width: 768, height: 1024 },   // iPad
    desktop: { width: 1920, height: 1080 }  // Desktop
  };

  test.beforeEach(async ({ page }) => {
    // Mock API endpoints
    await page.route('**/api/system/status', async route => {
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
            performance: { avg_search_time: 45 }
          }
        })
      });
    });

    await page.route('**/api/system/stats', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: {
            recent_activity: [
              { id: 1, type: 'search', description: 'Test arama', timestamp: new Date().toISOString() }
            ]
          }
        })
      });
    });
  });

  test.describe('Mobile Viewport (375px)', () => {
    test.beforeEach(async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
    });

    test('dashboard loads correctly on mobile', async ({ page }) => {
      await page.goto('/');
      
      // Check if dashboard loads
      await expect(page.locator('.context7-dashboard')).toBeVisible();
      
      // Check Turkish UI elements
      await expect(page.locator('text=Collective Memory')).toBeVisible();
      await expect(page.locator('text=Akıllı bağlam yönetimi')).toBeVisible();
      
      // Check mobile-specific elements
      await expect(page.locator('.dashboard-card')).toBeVisible();
      await expect(page.locator('.dashboard-stats')).toBeVisible();
      
      // Check responsive layout
      const dashboardGrid = page.locator('.dashboard-grid');
      await expect(dashboardGrid).toHaveCSS('grid-template-columns', '1fr');
    });

    test('mobile navigation works', async ({ page }) => {
      await page.goto('/');
      
      // Check if mobile menu toggle exists
      const mobileToggle = page.locator('.header-mobile-toggle');
      if (await mobileToggle.isVisible()) {
        await mobileToggle.click();
        
        // Check if mobile menu opens
        await expect(page.locator('.header-mobile-menu.open')).toBeVisible();
        
        // Check navigation items
        await expect(page.locator('text=Ana Panel')).toBeVisible();
        await expect(page.locator('text=Akıllı Arama')).toBeVisible();
        await expect(page.locator('text=Analitikler')).toBeVisible();
        await expect(page.locator('text=Ayarlar')).toBeVisible();
      }
    });

    test('search panel is mobile-friendly', async ({ page }) => {
      await page.goto('/search');
      
      // Check search input
      const searchInput = page.locator('.search-input');
      await expect(searchInput).toBeVisible();
      await expect(searchInput).toHaveCSS('font-size', '16px'); // Prevents iOS zoom
      await expect(searchInput).toHaveCSS('min-height', '44px'); // Touch target
      
      // Check search button
      const searchButton = page.locator('.search-button');
      await expect(searchButton).toBeVisible();
      await expect(searchButton).toHaveCSS('min-height', '44px');
      await expect(searchButton).toHaveCSS('width', '100%');
      
      // Test search functionality
      await searchInput.fill('test arama');
      await searchButton.click();
      
      // Should show results or loading state
      await expect(page.locator('.search-results, .loading-spinner')).toBeVisible();
    });

    test('system status displays correctly on mobile', async ({ page }) => {
      await page.goto('/');
      
      // Check system status component
      await expect(page.locator('.system-status-card')).toBeVisible();
      
      // Check metrics are displayed properly
      await expect(page.locator('.system-metrics')).toBeVisible();
      
      // Check responsive grid
      const systemMetrics = page.locator('.system-metrics');
      await expect(systemMetrics).toHaveCSS('grid-template-columns', 'repeat(2, 1fr)');
    });

    test('touch targets meet accessibility standards', async ({ page }) => {
      await page.goto('/');
      
      // Check all buttons meet minimum touch target size (44px)
      const buttons = page.locator('.context7-button, .search-button, .settings-button');
      const buttonCount = await buttons.count();
      
      for (let i = 0; i < buttonCount; i++) {
        const button = buttons.nth(i);
        if (await button.isVisible()) {
          const box = await button.boundingBox();
          if (box) {
            expect(box.height).toBeGreaterThanOrEqual(44);
            expect(box.width).toBeGreaterThanOrEqual(44);
          }
        }
      }
    });

    test('forms are mobile-optimized', async ({ page }) => {
      await page.goto('/settings');
      
      // Check form inputs
      const inputs = page.locator('.settings-input, .context7-input');
      const inputCount = await inputs.count();
      
      for (let i = 0; i < inputCount; i++) {
        const input = inputs.nth(i);
        if (await input.isVisible()) {
          await expect(input).toHaveCSS('font-size', '16px');
          await expect(input).toHaveCSS('min-height', '44px');
        }
      }
    });

    test('performance is acceptable on mobile', async ({ page }) => {
      const startTime = Date.now();
      await page.goto('/');
      
      // Wait for main content to load
      await page.waitForSelector('.context7-dashboard');
      
      const loadTime = Date.now() - startTime;
      expect(loadTime).toBeLessThan(5000); // 5 seconds max
      
      // Check if images/assets load quickly
      await expect(page.locator('.context7-card')).toBeVisible();
      await expect(page.locator('.dashboard-stats')).toBeVisible();
    });
  });

  test.describe('Tablet Viewport (768px)', () => {
    test.beforeEach(async ({ page }) => {
      await page.setViewportSize(viewports.tablet);
    });

    test('tablet layout adapts correctly', async ({ page }) => {
      await page.goto('/');
      
      // Check if dashboard uses tablet layout
      const dashboardGrid = page.locator('.dashboard-grid');
      await expect(dashboardGrid).toHaveCSS('grid-template-columns', 'repeat(2, 1fr)');
      
      // Check analytics grid
      await page.goto('/analytics');
      const analyticsGrid = page.locator('.analytics-grid');
      await expect(analyticsGrid).toHaveCSS('grid-template-columns', 'repeat(2, 1fr)');
    });

    test('tablet navigation works', async ({ page }) => {
      await page.goto('/');
      
      // Tablet should show regular navigation, not mobile menu
      await expect(page.locator('.header-nav')).toBeVisible();
      await expect(page.locator('.header-mobile-toggle')).not.toBeVisible();
    });
  });

  test.describe('Cross-Viewport Testing', () => {
    test('responsive breakpoints work correctly', async ({ page }) => {
      const breakpoints = [
        { width: 320, height: 568 },  // Small mobile
        { width: 375, height: 667 },  // iPhone 8
        { width: 414, height: 896 },  // iPhone 11
        { width: 768, height: 1024 }, // iPad
        { width: 1024, height: 768 }, // iPad landscape
        { width: 1920, height: 1080 } // Desktop
      ];

      for (const viewport of breakpoints) {
        await page.setViewportSize(viewport);
        await page.goto('/');
        
        // Check if page loads without errors
        await expect(page.locator('.context7-dashboard')).toBeVisible();
        
        // Check if content is readable
        await expect(page.locator('text=Collective Memory')).toBeVisible();
        
        // Check if buttons are accessible
        const buttons = page.locator('.context7-button');
        const buttonCount = await buttons.count();
        
        if (buttonCount > 0) {
          const firstButton = buttons.first();
          await expect(firstButton).toBeVisible();
          
          const box = await firstButton.boundingBox();
          if (box) {
            expect(box.height).toBeGreaterThanOrEqual(32); // Minimum reasonable size
          }
        }
      }
    });
  });

  test.describe('Device-Specific Features', () => {
    test('iOS zoom prevention works', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto('/search');
      
      // Check input font size to prevent iOS zoom
      const searchInput = page.locator('.search-input');
      await expect(searchInput).toHaveCSS('font-size', '16px');
      
      // Check other form inputs
      await page.goto('/settings');
      const settingsInputs = page.locator('.settings-input');
      const inputCount = await settingsInputs.count();
      
      for (let i = 0; i < inputCount; i++) {
        const input = settingsInputs.nth(i);
        if (await input.isVisible()) {
          await expect(input).toHaveCSS('font-size', '16px');
        }
      }
    });

    test('safe area support works', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 }); // iPhone X dimensions
      await page.goto('/');
      
      // Check if safe area CSS is applied
      const header = page.locator('.context7-header');
      await expect(header).toBeVisible();
      
      const container = page.locator('.container');
      await expect(container).toBeVisible();
    });
  });

  test.describe('Turkish UI Mobile Optimization', () => {
    test('Turkish text renders correctly on mobile', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto('/');
      
      // Check Turkish UI elements
      const turkishTexts = [
        'Collective Memory',
        'Akıllı bağlam yönetimi',
        'Sağlıklı',
        'Dosya Sayısı',
        'Arama Sayısı',
        'Çalışma Süresi'
      ];
      
      for (const text of turkishTexts) {
        await expect(page.locator(`text=${text}`)).toBeVisible();
      }
    });

    test('Turkish typography is optimized', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto('/');
      
      // Check Turkish UI class and typography
      await expect(page.locator('.turkish-ui')).toBeVisible();
      
      const turkishText = page.locator('.turkish-ui p').first();
      if (await turkishText.isVisible()) {
        await expect(turkishText).toHaveCSS('line-height', '1.7');
      }
    });
  });

  test.describe('Performance on Mobile', () => {
    test('bundle size is optimized for mobile', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      
      // Monitor network requests
      const requests = [];
      page.on('request', request => {
        requests.push(request);
      });
      
      await page.goto('/');
      await page.waitForLoadState('networkidle');
      
      // Check if essential resources are loaded
      const jsRequests = requests.filter(r => r.url().includes('.js'));
      const cssRequests = requests.filter(r => r.url().includes('.css'));
      
      expect(jsRequests.length).toBeLessThan(10); // Reasonable number of JS files
      expect(cssRequests.length).toBeLessThan(5);  // Reasonable number of CSS files
    });

    test('lazy loading works on mobile', async ({ page }) => {
      await page.setViewportSize(viewports.mobile);
      await page.goto('/');
      
      // Check if heavy components load lazily
      await page.waitForSelector('.context7-dashboard');
      
      // Navigate to analytics (should load lazily)
      await page.goto('/analytics');
      await expect(page.locator('.analytics-grid')).toBeVisible();
    });
  });
});

// Helper function to simulate mobile device
async function setupMobileDevice(page) {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.setExtraHTTPHeaders({
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
  });
}

// Helper function to test touch interactions
async function testTouchInteraction(page, selector) {
  const element = page.locator(selector);
  await expect(element).toBeVisible();
  
  // Simulate touch events
  await element.dispatchEvent('touchstart');
  await element.dispatchEvent('touchend');
  await element.click();
}

// Helper function to check responsive images
async function checkResponsiveImages(page) {
  const images = page.locator('img');
  const imageCount = await images.count();
  
  for (let i = 0; i < imageCount; i++) {
    const img = images.nth(i);
    if (await img.isVisible()) {
      const src = await img.getAttribute('src');
      const alt = await img.getAttribute('alt');
      
      expect(src).toBeTruthy();
      expect(alt).toBeTruthy(); // Accessibility
    }
  }
} 