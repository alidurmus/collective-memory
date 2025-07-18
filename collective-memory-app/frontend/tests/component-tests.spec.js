import { test, expect } from '@playwright/test';

test.describe('Component Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
  });

  test('should render HomePage component correctly', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Check for main content
    await expect(page.locator('main')).toBeVisible();
    
    // Check for page title or heading
    const heading = await page.locator('h1, h2, h3').first();
    await expect(heading).toBeVisible();
  });

  test('should render SearchPage component correctly', async ({ page }) => {
    await page.goto('http://localhost:5173/search');
    
    // Check for search functionality
    await expect(page.locator('main')).toBeVisible();
    
    // Check for search input if exists
    const searchInput = page.locator('input[type="search"], input[placeholder*="search"]');
    if (await searchInput.count() > 0) {
      await expect(searchInput.first()).toBeVisible();
    }
  });

  test('should render AnalyticsPage component correctly', async ({ page }) => {
    await page.goto('http://localhost:5173/analytics');
    
    // Check for analytics content
    await expect(page.locator('main')).toBeVisible();
    
    // Check for charts or analytics data
    const charts = page.locator('canvas, svg, [data-testid*="chart"]');
    if (await charts.count() > 0) {
      await expect(charts.first()).toBeVisible();
    }
  });

  test('should render SettingsPage component correctly', async ({ page }) => {
    await page.goto('http://localhost:5173/settings');
    
    // Check for settings content
    await expect(page.locator('main')).toBeVisible();
    
    // Check for settings tabs
    const tabs = page.locator('button[role="tab"], nav button');
    if (await tabs.count() > 0) {
      await expect(tabs.first()).toBeVisible();
    }
  });

  test('should render NotFoundPage component correctly', async ({ page }) => {
    await page.goto('http://localhost:5173/nonexistent-page');
    
    // Check for 404 content
    await expect(page.locator('h1')).toContainText('404');
    await expect(page.locator('h2')).toContainText('Page Not Found');
    
    // Check for navigation buttons
    const homeButton = page.locator('a:has-text("Go to Homepage"), button:has-text("Home")');
    if (await homeButton.count() > 0) {
      await expect(homeButton.first()).toBeVisible();
    }
  });

  test('should handle React Query integration', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Check if React Query DevTools are available (in development)
    const devtools = page.locator('[data-testid="react-query-devtools"]');
    if (await devtools.count() > 0) {
      await expect(devtools.first()).toBeVisible();
    }
  });

  test('should handle routing correctly', async ({ page }) => {
    // Test direct navigation
    const routes = ['/', '/search', '/analytics', '/settings'];
    
    for (const route of routes) {
      await page.goto(`http://localhost:5173${route}`);
      await expect(page.locator('main')).toBeVisible();
      
      // Check for no console errors
      const consoleErrors = [];
      page.on('console', msg => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });
      
      await page.waitForLoadState('networkidle');
      expect(consoleErrors.length).toBe(0);
    }
  });

  test('should handle responsive components', async ({ page }) => {
    const viewports = [
      { width: 375, height: 667, name: 'mobile' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 1920, height: 1080, name: 'desktop' }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.goto('http://localhost:5173/');
      
      // Check if main content is visible in all viewports
      await expect(page.locator('main')).toBeVisible();
      
      // Check for no layout breaking
      const mainElement = page.locator('main');
      const boundingBox = await mainElement.boundingBox();
      expect(boundingBox).toBeTruthy();
    }
  });

  test('should handle component interactions', async ({ page }) => {
    await page.goto('http://localhost:5173/settings');
    
    // Test tab interactions if they exist
    const tabButtons = page.locator('button[role="tab"], nav button');
    const tabCount = await tabButtons.count();
    
    if (tabCount > 1) {
      // Click on first tab
      await tabButtons.first().click();
      await expect(tabButtons.first()).toHaveAttribute('aria-selected', 'true');
      
      // Click on second tab
      await tabButtons.nth(1).click();
      await expect(tabButtons.nth(1)).toHaveAttribute('aria-selected', 'true');
    }
  });

  test('should handle form components', async ({ page }) => {
    await page.goto('http://localhost:5173/settings');
    
    // Test form inputs if they exist
    const inputs = page.locator('input, select, textarea');
    const inputCount = await inputs.count();
    
    if (inputCount > 0) {
      const firstInput = inputs.first();
      await expect(firstInput).toBeVisible();
      
      // Test input interaction
      await firstInput.click();
      await expect(firstInput).toBeFocused();
    }
  });

  test('should handle loading states', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Check for loading indicators if they exist
    const loadingIndicators = page.locator('[data-testid*="loading"], .loading, [aria-busy="true"]');
    if (await loadingIndicators.count() > 0) {
      // Loading indicators should eventually disappear
      await expect(loadingIndicators.first()).not.toBeVisible({ timeout: 10000 });
    }
  });
}); 