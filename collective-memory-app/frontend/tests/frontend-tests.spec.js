import { test, expect } from '@playwright/test';

test.describe('Frontend Tests', () => {
  test('Frontend should load successfully', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page).toHaveTitle(/Collective Memory v3\.0\.1/);
  });

  test('Project title should be visible', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h1:has-text("Collective Memory v3.0.1")')).toBeVisible();
  });

  test('100% Complete status should be displayed', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('text=100% Complete')).toBeVisible();
  });

  test('System Health 10/10 should be displayed', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('.metric-value:has-text("10/10")')).toBeVisible();
  });

  test('Smart Context Bridge should be mentioned', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h3:has-text("Smart Context Bridge")')).toBeVisible();
  });

  test('Query Processing should be mentioned', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h3:has-text("Query Processing")')).toBeVisible();
  });

  test('Performance metrics should be displayed', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('.metric-value:has-text("85ms")')).toBeVisible();
    await expect(page.locator('.metric-value:has-text("12ms")')).toBeVisible();
  });

  test('API Server Status should be shown', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('text=API Server Status')).toBeVisible();
  });

  test('Quick Start section should be present', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h2:has-text("Quick Start")')).toBeVisible();
  });

  test('API Documentation link should be available', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('a:has-text("API Documentation")')).toBeVisible();
  });

  test('Project Overview section should be displayed', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h2:has-text("Project Overview")')).toBeVisible();
  });

  test('Performance Metrics section should be shown', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h2:has-text("Performance Metrics")')).toBeVisible();
  });

  test('Key Benefits section should be present', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('h2:has-text("Key Benefits")')).toBeVisible();
  });

  test('Footer should show project information', async ({ page }) => {
    await page.goto('http://localhost:3000');
    await expect(page.locator('p:has-text("© 2025 Collective Memory v3.0.1")')).toBeVisible();
    await expect(page.locator('p:has-text("Production Ready")')).toBeVisible();
  });
}); 