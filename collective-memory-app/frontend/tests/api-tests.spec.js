import { test, expect } from '@playwright/test';

test('Health endpoint should return 200', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/health');
  expect(response.status()).toBe(200);
});

test('System status endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/system/status');
  expect(response.status()).toBe(200);
});

test('System health endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/api/system/health');
  expect(response.status()).toBe(200);
});

test('System metrics endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/api/system/metrics');
  expect(response.status()).toBe(200);
});

test('WebSocket status endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/api/websocket/status');
  expect(response.status()).toBe(200);
});

test('Enterprise ping endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/enterprise/ping');
  expect(response.status()).toBe(200);
});

test('Chat API index should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/api/v1/chat/');
  expect(response.status()).toBe(200);
});

test('Search endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/search');
  expect(response.status()).toBe(200);
});

test('Config endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/config');
  expect(response.status()).toBe(200);
});

test('Prompts endpoint should work', async ({ page }) => {
  const response = await page.goto('http://127.0.0.1:8000/prompts');
  expect(response.status()).toBe(405); // Method not allowed for GET
}); 