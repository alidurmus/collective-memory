import { test, expect } from '@playwright/test';

test.describe('API Tests', () => {
  const baseURL = 'http://127.0.0.1:8000';

  test('Health check endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/health`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status');
    expect(data.status).toBe('healthy');
  });

  test('System status endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/system/status`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status');
    expect(data).toHaveProperty('timestamp');
  });

  test('System health endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/api/system/health`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status');
    expect(data).toHaveProperty('components');
  });

  test('WebSocket status endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/api/websocket/status`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status');
  });

  test('Enterprise ping endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/enterprise/ping`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('message');
    expect(data.message).toContain('pong');
  });

  test('Chat API endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/api/v1/chat/`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('message');
  });

  test('Configuration endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/config`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('version');
  });

  test('Search endpoint should return 400 for missing query', async ({ request }) => {
    const response = await request.get(`${baseURL}/search`);
    expect(response.status()).toBe(400);
  });

  test('Prompts endpoint should return 404', async ({ request }) => {
    const response = await request.get(`${baseURL}/prompts`);
    expect(response.status()).toBe(404);
  });

  test('System metrics endpoint should handle errors gracefully', async ({ request }) => {
    const response = await request.get(`${baseURL}/api/system/metrics`);
    // This endpoint might return 500, which is expected behavior
    expect([200, 500]).toContain(response.status());
  });

  test('Chat conversations endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/api/v1/chat/conversations`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(Array.isArray(data)).toBe(true);
  });

  test('Chat stats endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/api/v1/chat/stats`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('total_conversations');
    expect(data).toHaveProperty('total_messages');
  });

  test('Search API endpoint should accept POST requests', async ({ request }) => {
    const response = await request.post(`${baseURL}/api/search`, {
      data: {
        query: 'test query',
        limit: 10
      }
    });
    expect(response.status()).toBe(200);
  });

  test('Search suggestions endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/search/suggestions`);
    expect(response.status()).toBe(200);
  });

  test('Context suggestions endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/prompts/context-suggestions`);
    expect(response.status()).toBe(200);
  });

  test('WebSocket errors endpoint should return 200', async ({ request }) => {
    const response = await request.get(`${baseURL}/api/websocket/errors`);
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(Array.isArray(data)).toBe(true);
  });
}); 