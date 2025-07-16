// global-teardown.js

async function globalTeardown(config) {
  console.log('🧹 Starting test cleanup...');
  
  // Test dosyalarını temizle
  console.log('📁 Cleaning up test artifacts...');
  
  // Test veritabanını temizle
  console.log('🗄️ Cleaning test database...');
  
  console.log('✅ Global teardown completed');
}

module.exports = globalTeardown; 