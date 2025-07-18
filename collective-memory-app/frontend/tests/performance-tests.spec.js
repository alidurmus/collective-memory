import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  test('should load homepage within acceptable time', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('http://localhost:5173/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    
    // Homepage should load within 3 seconds
    expect(loadTime).toBeLessThan(3000);
  });

  test('should load all pages within acceptable time', async ({ page }) => {
    const routes = ['/', '/search', '/analytics', '/settings'];
    
    for (const route of routes) {
      const startTime = Date.now();
      
      await page.goto(`http://localhost:5173${route}`);
      await page.waitForLoadState('networkidle');
      
      const loadTime = Date.now() - startTime;
      
      // Each page should load within 3 seconds
      expect(loadTime).toBeLessThan(3000);
    }
  });

  test('should handle navigation without performance issues', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    const routes = ['/search', '/analytics', '/settings'];
    
    for (const route of routes) {
      const startTime = Date.now();
      
      await page.goto(`http://localhost:5173${route}`);
      await page.waitForLoadState('networkidle');
      
      const loadTime = Date.now() - startTime;
      
      // Navigation should be fast
      expect(loadTime).toBeLessThan(2000);
    }
  });

  test('should not have memory leaks', async ({ page }) => {
    // Navigate multiple times to check for memory leaks
    for (let i = 0; i < 5; i++) {
      await page.goto('http://localhost:5173/');
      await page.waitForLoadState('networkidle');
      
      await page.goto('http://localhost:5173/search');
      await page.waitForLoadState('networkidle');
      
      await page.goto('http://localhost:5173/analytics');
      await page.waitForLoadState('networkidle');
      
      await page.goto('http://localhost:5173/settings');
      await page.waitForLoadState('networkidle');
    }
    
    // Final page should still load quickly
    const startTime = Date.now();
    await page.goto('http://localhost:5173/');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    expect(loadTime).toBeLessThan(3000);
  });

  test('should handle large viewport without performance issues', async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    
    const startTime = Date.now();
    await page.goto('http://localhost:5173/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(3000);
  });

  test('should handle mobile viewport without performance issues', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    
    const startTime = Date.now();
    await page.goto('http://localhost:5173/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    expect(loadTime).toBeLessThan(3000);
  });

  test('should not have excessive network requests', async ({ page }) => {
    const requests = [];
    
    page.on('request', request => {
      requests.push(request.url());
    });
    
    await page.goto('http://localhost:5173/');
    await page.waitForLoadState('networkidle');
    
    // Should not have excessive requests (less than 50)
    expect(requests.length).toBeLessThan(50);
  });

  test('should handle rapid navigation', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Rapidly navigate between pages
    for (let i = 0; i < 10; i++) {
      await page.goto('http://localhost:5173/search');
      await page.goto('http://localhost:5173/analytics');
      await page.goto('http://localhost:5173/settings');
      await page.goto('http://localhost:5173/');
    }
    
    // Should still be responsive
    await expect(page.locator('main')).toBeVisible();
  });

  test('should handle concurrent page loads', async ({ browser }) => {
    const context1 = await browser.newContext();
    const context2 = await browser.newContext();
    
    const page1 = await context1.newPage();
    const page2 = await context2.newPage();
    
    const startTime = Date.now();
    
    // Load pages concurrently
    await Promise.all([
      page1.goto('http://localhost:5173/'),
      page2.goto('http://localhost:5173/search')
    ]);
    
    await Promise.all([
      page1.waitForLoadState('networkidle'),
      page2.waitForLoadState('networkidle')
    ]);
    
    const loadTime = Date.now() - startTime;
    
    // Concurrent loads should still be fast
    expect(loadTime).toBeLessThan(4000);
    
    await context1.close();
    await context2.close();
  });

  test('should maintain performance after multiple refreshes', async ({ page }) => {
    for (let i = 0; i < 5; i++) {
      const startTime = Date.now();
      
      await page.goto('http://localhost:5173/');
      await page.waitForLoadState('networkidle');
      
      const loadTime = Date.now() - startTime;
      expect(loadTime).toBeLessThan(3000);
      
      await page.reload();
    }
  });
}); 