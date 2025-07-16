// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Collective Memory Frontend - Playwright Configuration
 * UI testleri için konfigürasyon - Sadece Chrome Browser
 */
module.exports = defineConfig({
  testDir: './ui',
  /* Maximum time one test can run for. */
  timeout: 60 * 1000, // Increased timeout
  expect: {
    /* Maximum time expect() should wait for the condition to be met. */
    timeout: 10000 // Increased expect timeout
  },
  /* Run tests in files in parallel */
  fullyParallel: false, // Safer for single browser
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 1, // Add retry for stability
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : 2, // Limited workers for stability
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['html', { outputFolder: 'test-results/html' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['list']
  ],
  
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Maximum time each action such as `click()` can take. Defaults to 0 (no limit). */
    actionTimeout: 15000, // Increased action timeout
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://localhost:3000',
    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
    
    /* Take screenshot on failure */
    screenshot: 'only-on-failure',
    /* Record video on failure */
    video: 'retain-on-failure',
    
    /* Wait for page load state */
    navigationTimeout: 30000
  },

  /* WebServer configuration for automatic frontend startup */
  webServer: {
    command: 'cd frontend && npm run dev',
    cwd: '../', // Relative to tests directory
    port: 3000,
    timeout: 180 * 1000, // 3 minutes for server startup
    reuseExistingServer: !process.env.CI,
    stdout: 'pipe',
    stderr: 'pipe',
    env: {
      NODE_ENV: 'development'
    }
  },

  /* Configure projects - ONLY CHROME as requested */
  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Additional Chrome-specific settings
        channel: 'chrome', // Use actual Chrome if available
        headless: !process.env.HEADED, // Allow headed mode
        viewport: { width: 1280, height: 720 },
        ignoreHTTPSErrors: true,
        permissions: ['clipboard-read', 'clipboard-write']
      },
    }
  ],

  /* Folder for test artifacts such as screenshots, videos, traces, etc. */
  outputDir: 'test-results/',
  
  /* Global test setup and teardown */
  globalSetup: require.resolve('./global-setup.js'),
  globalTeardown: require.resolve('./global-teardown.js'),
}); 