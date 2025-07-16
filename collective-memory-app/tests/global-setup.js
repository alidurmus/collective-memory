// global-setup.js
const { chromium } = require('@playwright/test');

async function globalSetup(config) {
  console.log('🚀 Starting Collective Memory Test Suite...');
  
  // Test veritabanını temizle/hazırla
  console.log('📊 Preparing test database...');
  
  // Backend server'ın çalışıp çalışmadığını kontrol et
  console.log('🔍 Checking backend server availability...');
  
  try {
    const response = await fetch('http://localhost:8000/api/system/status');
    if (response.ok) {
      console.log('✅ Backend server is running');
    } else {
      console.log('⚠️ Backend server not responding properly');
    }
  } catch (error) {
    console.log('❌ Backend server not available:', error.message);
  }
  
  // Frontend test için environment hazırla
  console.log('🎨 Setting up frontend test environment...');
  
  console.log('✅ Global setup completed');
}

module.exports = globalSetup; 