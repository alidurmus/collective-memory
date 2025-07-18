import { test, expect } from '@playwright/test';

test('Frontpage should load successfully', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveTitle(/Collective Memory/);
});

test('API server should be accessible', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/health');
  expect(response.status()).toBe(200);
});

test('System status endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/system/status');
  expect(response.status()).toBe(200);
});

test('Documentation should be accessible', async ({ page }) => {
  await page.goto('http://localhost:3000');
  // Check if documentation links are present
  await expect(page.locator('text=Documentation')).toBeVisible();
});

test('Project status should show 100% completion', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('text=100% Complete')).toBeVisible();
});

test('Query Processing System should be mentioned', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('text=Query Processing')).toBeVisible();
});

test('Smart Context Bridge should be mentioned', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('text=Smart Context Bridge')).toBeVisible();
});

test('Performance metrics should be displayed', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('text=85ms')).toBeVisible();
});

test('System health should show 10/10', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('text=10/10')).toBeVisible();
}); 