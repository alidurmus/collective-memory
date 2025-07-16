// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Collective Memory Basic Smoke Tests
 * Temel işlevsellik kontrolü için hızlı testler
 */

test.describe('Temel Smoke Tests', () => {
  test('ana sayfa yükleniyor', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Sayfa yüklendiğini kontrol et - body yerine daha uygun kontroller
    await expect(page.locator('#root')).toBeVisible();
    
    // Title kontrol et
    await expect(page).toHaveTitle(/Collective Memory|React App/);
    
    // React uygulaması yüklenmiş olmalı
    await page.waitForLoadState('networkidle');
    
    // Body en azından mevcut olmalı (hidden olsa bile)
    await expect(page.locator('body')).toHaveCount(1);
  });

  test('404 sayfası çalışıyor', async ({ page }) => {
    await page.goto('http://localhost:3000/nonexistent-page');
    
    // 404 yönlendirmesi veya Not Found component'i
    await expect(page.locator('#root')).toBeVisible();
    
    // Sayfa crash olmadığından emin ol
    await expect(page.locator('body')).toHaveCount(1);
  });

  test('javascript hataları yok', async ({ page }) => {
    const consoleErrors = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    page.on('pageerror', error => {
      consoleErrors.push(error.message);
    });

    await page.goto('http://localhost:3000');
    await page.waitForTimeout(3000);

    // Kritik JavaScript hataları olmamalı - favicon ve network hatalarını ignore et
    const criticalErrors = consoleErrors.filter(error => 
      !error.includes('favicon') && 
      !error.includes('404') &&
      !error.includes('net::ERR_INTERNET_DISCONNECTED') &&
      !error.includes('favicon.ico') &&
      !error.includes('logo.svg') &&
      !error.includes('Failed to load resource')
    );
    
    if (criticalErrors.length > 0) {
      console.log('JavaScript Hataları:', criticalErrors);
    }
    
    expect(criticalErrors.length).toBe(0);
  });

  test('responsive tasarım çalışıyor', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page.locator('#root')).toBeVisible();
    
    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('#root')).toBeVisible();
    
    // Horizontal scroll olmamalı
    const hasHorizontalScroll = await page.evaluate(() => {
      return document.body.scrollWidth > window.innerWidth;
    });
    
    expect(hasHorizontalScroll).toBe(false);
  });

  test('temel navigasyon', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // React app yüklenene kadar bekle
    await page.waitForLoadState('networkidle');
    await expect(page.locator('#root')).toBeVisible();
    
    // Herhangi bir navigation link varsa test et
    const navLinks = page.locator('nav a, header a, [data-testid*="nav"], [data-testid*="link"]');
    const linkCount = await navLinks.count();
    
    if (linkCount > 0) {
      const firstLink = navLinks.first();
      const href = await firstLink.getAttribute('href');
      
      if (href && !href.startsWith('http') && href !== '#') {
        await firstLink.click();
        await page.waitForLoadState('networkidle');
        await expect(page.locator('#root')).toBeVisible();
      }
    } else {
      // Link yoksa en azından sayfa yüklenmiş olmalı
      console.log('Navigation linkler bulunamadı, temel yükleme testi yapıldı');
    }
  });
}); 