import { test, expect } from '@playwright/test';

test.describe('Frontend Smoke Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
  });

  test('should load homepage successfully', async ({ page }) => {
    // Check if page loads without errors
    await expect(page).toHaveTitle(/Collective Memory/);
    
    // Check if main content is visible
    await expect(page.locator('main')).toBeVisible();
    
    // Check if navigation works
    await expect(page.locator('nav')).toBeVisible();
  });

  test('should navigate to all pages without errors', async ({ page }) => {
    // Test homepage
    await page.goto('http://localhost:5173/');
    await expect(page.locator('main')).toBeVisible();
    
    // Test search page
    await page.goto('http://localhost:5173/search');
    await expect(page.locator('main')).toBeVisible();
    
    // Test analytics page
    await page.goto('http://localhost:5173/analytics');
    await expect(page.locator('main')).toBeVisible();
    
    // Test settings page
    await page.goto('http://localhost:5173/settings');
    await expect(page.locator('main')).toBeVisible();
  });

  test('should handle 404 page correctly', async ({ page }) => {
    await page.goto('http://localhost:5173/nonexistent-page');
    
    // Should show 404 page
    await expect(page.locator('h1')).toContainText('404');
    await expect(page.locator('h2')).toContainText('Page Not Found');
  });

  test('should have working navigation links', async ({ page }) => {
    // Test navigation between pages
    await page.goto('http://localhost:5173/');
    
    // Navigate to search
    await page.click('a[href="/search"]');
    await expect(page).toHaveURL('http://localhost:5173/search');
    
    // Navigate to analytics
    await page.click('a[href="/analytics"]');
    await expect(page).toHaveURL('http://localhost:5173/analytics');
    
    // Navigate to settings
    await page.click('a[href="/settings"]');
    await expect(page).toHaveURL('http://localhost:5173/settings');
  });

  test('should load without console errors', async ({ page }) => {
    const consoleErrors = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });
    
    await page.goto('http://localhost:5173/');
    await page.waitForLoadState('networkidle');
    
    // Check for console errors
    expect(consoleErrors.length).toBe(0);
  });

  test('should have responsive design', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('main')).toBeVisible();
    
    // Test tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page.locator('main')).toBeVisible();
    
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page.locator('main')).toBeVisible();
  });

  test('should handle settings page functionality', async ({ page }) => {
    await page.goto('http://localhost:5173/settings');
    
    // Check if settings tabs are visible
    await expect(page.locator('nav')).toBeVisible();
    
    // Test tab switching
    await page.click('button:has-text("Profile")');
    await expect(page.locator('h3')).toContainText('Profile Settings');
    
    await page.click('button:has-text("Security")');
    await expect(page.locator('h3')).toContainText('Security Settings');
  });

  test('should have proper accessibility', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Check for proper heading structure
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').count();
    expect(headings).toBeGreaterThan(0);
    
    // Check for proper button accessibility
    const buttons = await page.locator('button').count();
    if (buttons > 0) {
      await expect(page.locator('button').first()).toBeVisible();
    }
  });
}); 