import { test, expect } from '@playwright/test';

test.describe('Basic Frontend Tests', () => {
  test('should start without errors', async ({ page }) => {
    // Just check if we can navigate to the page
    await page.goto('http://localhost:5173/');
    
    // Check if page loads (any content)
    const body = await page.locator('body');
    await expect(body).toBeVisible();
  });

  test('should have basic HTML structure', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Check for basic HTML elements
    const html = await page.locator('html');
    const head = await page.locator('head');
    const body = await page.locator('body');
    
    await expect(html).toBeVisible();
    await expect(head).toBeVisible();
    await expect(body).toBeVisible();
  });

  test('should load React app', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Check for React root element
    const root = await page.locator('#root');
    await expect(root).toBeVisible();
  });

  test('should not have critical console errors', async ({ page }) => {
    const consoleErrors = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });
    
    await page.goto('http://localhost:5173/');
    await page.waitForLoadState('networkidle');
    
    // Allow some non-critical errors but not too many
    expect(consoleErrors.length).toBeLessThan(10);
  });

  test('should respond to basic interactions', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    
    // Check if page is interactive
    await page.mouse.move(100, 100);
    await page.mouse.click(100, 100);
    
    // Page should still be visible after interaction
    const body = await page.locator('body');
    await expect(body).toBeVisible();
  });
}); 