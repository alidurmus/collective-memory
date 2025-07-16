---
description: Advanced testing patterns - pytest, Playwright, vitest, modern testing strategies
globs: ["tests/**/*.py", "tests/**/*.js", "tests/**/*.ts", "**/*.test.js", "**/*.test.ts", "**/*.spec.js", "**/*.spec.ts", "**/*test*.py", "**/*spec*.py"]
alwaysApply: false
---

# 🧪 Advanced Testing Patterns

Cursor.directory community best practices ile optimize edilmiş modern testing kuralları [[memory:592592]].

## 🐍 Advanced Backend Testing (pytest)

### Test Configuration & Fixtures
```python
# ✅ Advanced pytest Configuration
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from django.test import override_settings
from django.core.cache import cache
from django.db import transaction
from faker import Faker
from factory import Factory, SubFactory, Sequence

# conftest.py
@pytest.fixture(scope="session")
def django_db_setup():
    """Set up test database."""
    from django.conf import settings
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

@pytest.fixture
def sample_user():
    """Create sample user with Turkish name."""
    fake = Faker('tr_TR')
    return User.objects.create_user(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email()
    )

@pytest.fixture
def sample_files():
    """Create sample files for testing."""
    files = []
    for i in range(10):
        file_obj = FileIndex.objects.create(
            file_path=f'/test/dosya_{i}.py',
            content_hash=f'hash_{i}',
            file_size=1024 * (i + 1),
            content_type='python',
            search_keywords=f'test keyword_{i} django',
            last_modified=timezone.now()
        )
        files.append(file_obj)
    return files

@pytest.fixture
def mock_search_engine():
    """Mock search engine for testing."""
    engine = Mock()
    engine.search.return_value = [
        {
            'id': '1',
            'file_path': '/test/result.py',
            'content_snippet': 'Test content',
            'relevance_score': 0.95
        }
    ]
    return engine

@pytest.fixture
def async_client():
    """Async HTTP client for testing."""
    import aiohttp
    return aiohttp.ClientSession()

# Factory pattern for test data
class FileIndexFactory(Factory):
    class Meta:
        model = FileIndex
    
    file_path = Sequence(lambda n: f'/test/file_{n}.py')
    content_hash = Sequence(lambda n: f'hash_{n}')
    file_size = 1024
    content_type = 'python'
    search_keywords = 'test django python'
    last_modified = timezone.now()
```

### Comprehensive Test Patterns
```python
# ✅ Advanced Test Patterns
import pytest
from unittest.mock import Mock, patch, call
from django.test import TestCase, TransactionTestCase
from django.db import transaction
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status

class TestFileIndexModel(TestCase):
    """Comprehensive model testing with Turkish support."""
    
    def setUp(self):
        """Set up test environment."""
        self.file_data = {
            'file_path': '/projeler/çalışma_dosyası.py',
            'content_hash': 'abc123',
            'file_size': 1024,
            'content_type': 'python',
            'last_modified': timezone.now()
        }
    
    def test_turkish_file_path_handling(self):
        """Test Turkish character handling in file paths."""
        turkish_paths = [
            '/projeler/çalışma_dosyası.py',
            '/belgeler/öğrenci_listesi.txt',
            '/raporlar/ürün_analizi.md',
            '/kodlar/türkçe_yorum.js'
        ]
        
        for path in turkish_paths:
            file_obj = FileIndex.objects.create(
                file_path=path,
                content_hash='test_hash',
                file_size=1024,
                content_type='text',
                last_modified=timezone.now()
            )
            
            # Verify Turkish characters preserved
            self.assertEqual(file_obj.file_path, path)
            
            # Verify database roundtrip
            retrieved = FileIndex.objects.get(id=file_obj.id)
            self.assertEqual(retrieved.file_path, path)
    
    def test_soft_delete_queryset_behavior(self):
        """Test soft delete queryset behavior."""
        # Create test files
        active_file = FileIndex.objects.create(
            file_path='/test/active.py',
            content_hash='active_hash',
            file_size=1024,
            content_type='python',
            last_modified=timezone.now()
        )
        
        deleted_file = FileIndex.objects.create(
            file_path='/test/deleted.py',
            content_hash='deleted_hash',
            file_size=1024,
            content_type='python',
            last_modified=timezone.now()
        )
        
        # Soft delete one file
        deleted_file.soft_delete()
        
        # Test default queryset (should only show active)
        active_files = FileIndex.objects.all()
        self.assertEqual(active_files.count(), 1)
        self.assertEqual(active_files.first().id, active_file.id)
        
        # Test all_objects queryset (should show both)
        all_files = FileIndex.all_objects.all()
        self.assertEqual(all_files.count(), 2)
        
        # Test deleted_only queryset
        deleted_files = FileIndex.objects.deleted_only()
        self.assertEqual(deleted_files.count(), 1)
        self.assertEqual(deleted_files.first().id, deleted_file.id)
        
        # Test restore functionality
        deleted_file.restore()
        self.assertEqual(FileIndex.objects.count(), 2)
    
    def test_bulk_operations_performance(self):
        """Test bulk operations performance with large dataset."""
        # Create large dataset
        files = []
        for i in range(1000):
            files.append(FileIndex(
                file_path=f'/bulk/file_{i}.py',
                content_hash=f'bulk_hash_{i}',
                file_size=1024,
                content_type='python',
                search_keywords=f'bulk test_{i}',
                last_modified=timezone.now()
            ))
        
        # Measure bulk create performance
        start_time = time.time()
        FileIndex.objects.bulk_create(files, batch_size=100)
        end_time = time.time()
        
        # Performance assertions
        self.assertLess(end_time - start_time, 5.0)  # Should complete in 5 seconds
        self.assertEqual(FileIndex.objects.count(), 1000)
        
        # Test bulk update performance
        bulk_updates = {
            file.id: {'file_size': 2048} 
            for file in FileIndex.objects.all()[:100]
        }
        
        start_time = time.time()
        DatabaseOptimizer.bulk_update_with_case(FileIndex, bulk_updates)
        end_time = time.time()
        
        self.assertLess(end_time - start_time, 2.0)  # Should complete in 2 seconds
    
    def test_database_constraints(self):
        """Test database constraints and validation."""
        # Test unique constraint
        file_data = self.file_data.copy()
        FileIndex.objects.create(**file_data)
        
        with self.assertRaises(IntegrityError):
            FileIndex.objects.create(**file_data)  # Duplicate file_path
        
        # Test field validation
        with self.assertRaises(ValidationError):
            FileIndex.objects.create(
                file_path='',  # Empty path
                content_hash='test',
                file_size=-1,  # Negative size
                content_type='python',
                last_modified=timezone.now()
            )

class TestSearchAPI(APITestCase):
    """Advanced API testing with Turkish UI."""
    
    def setUp(self):
        """Set up API test environment."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create diverse test data
        self.test_files = [
            {
                'file_path': '/projeler/django_app.py',
                'content_type': 'python',
                'search_keywords': 'django web framework python',
                'file_size': 2048
            },
            {
                'file_path': '/belgeler/kullanici_rehberi.md',
                'content_type': 'markdown',
                'search_keywords': 'kullanıcı rehberi dokümantasyon',
                'file_size': 1024
            },
            {
                'file_path': '/frontend/ana_sayfa.tsx',
                'content_type': 'typescript',
                'search_keywords': 'react typescript ana sayfa',
                'file_size': 3072
            }
        ]
        
        for file_data in self.test_files:
            FileIndex.objects.create(
                **file_data,
                content_hash='test_hash',
                last_modified=timezone.now()
            )
    
    def test_search_with_turkish_query(self):
        """Test search API with Turkish query."""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/search/', {'q': 'kullanıcı'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Arama başarılı')
        
        # Should find markdown file
        results = response.data['data']
        self.assertGreater(len(results), 0)
        
        found_file = next(
            (r for r in results if 'kullanici_rehberi.md' in r['file_path']), 
            None
        )
        self.assertIsNotNone(found_file)
    
    def test_search_filters_and_sorting(self):
        """Test search with multiple filters."""
        self.client.force_authenticate(user=self.user)
        
        # Filter by file type
        response = self.client.get('/api/search/', {
            'q': 'django',
            'type': 'python',
            'min_size': 1024,
            'max_size': 4096
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['data']
        
        # All results should be Python files
        for result in results:
            self.assertEqual(result['content_type'], 'python')
            self.assertGreaterEqual(result['file_size'], 1024)
            self.assertLessEqual(result['file_size'], 4096)
    
    def test_search_pagination(self):
        """Test search pagination."""
        # Create many files
        for i in range(50):
            FileIndex.objects.create(
                file_path=f'/test/file_{i}.py',
                content_hash=f'hash_{i}',
                file_size=1024,
                content_type='python',
                search_keywords=f'test file_{i}',
                last_modified=timezone.now()
            )
        
        self.client.force_authenticate(user=self.user)
        
        # Test first page
        response = self.client.get('/api/search/', {
            'q': 'test',
            'page': 1,
            'page_size': 10
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        
        # Test second page
        response = self.client.get('/api/search/', {
            'q': 'test',
            'page': 2,
            'page_size': 10
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
    
    def test_search_performance_monitoring(self):
        """Test search performance monitoring."""
        self.client.force_authenticate(user=self.user)
        
        with patch('collective_memory.views.logger') as mock_logger:
            response = self.client.get('/api/search/', {'q': 'django'})
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Should log performance metrics
            mock_logger.info.assert_called()
            call_args = mock_logger.info.call_args[0][0]
            self.assertIn('search_time_ms', call_args)
    
    def test_search_error_handling(self):
        """Test search error handling."""
        self.client.force_authenticate(user=self.user)
        
        # Test with invalid parameters
        response = self.client.get('/api/search/', {
            'q': 'test',
            'min_size': 'invalid',  # Invalid size
            'date_from': 'invalid_date'  # Invalid date
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('error', response.data)
    
    def test_search_rate_limiting(self):
        """Test search rate limiting."""
        self.client.force_authenticate(user=self.user)
        
        # Make requests up to rate limit
        for i in range(100):
            response = self.client.get('/api/search/', {'q': f'test_{i}'})
            
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                # Rate limit reached
                self.assertIn('detail', response.data)
                break
        else:
            # Should hit rate limit within 100 requests
            self.fail("Rate limit not reached within 100 requests")
    
    @override_settings(CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    })
    def test_search_caching(self):
        """Test search result caching."""
        self.client.force_authenticate(user=self.user)
        
        # Clear cache
        cache.clear()
        
        # First request - should not be cached
        response1 = self.client.get('/api/search/', {'q': 'django'})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Second request - should be cached
        response2 = self.client.get('/api/search/', {'q': 'django'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        
        # Results should be identical
        self.assertEqual(response1.data['data'], response2.data['data'])
```

## 🎭 Advanced Frontend Testing (Playwright + Vitest)

### Playwright Configuration
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results.json' }],
    ['junit', { outputFile: 'test-results.xml' }]
  ],
  use: {
    baseURL: 'http://localhost:3003',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    locale: 'tr-TR',
    timezoneId: 'Europe/Istanbul'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] }
    }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3003',
    reuseExistingServer: !process.env.CI
  }
});
```

### Advanced UI Testing
```typescript
// ✅ Advanced Playwright Tests
import { test, expect, Page } from '@playwright/test';

test.describe('Dashboard Functionality', () => {
  let page: Page;
  
  test.beforeEach(async ({ page: testPage }) => {
    page = testPage;
    await page.goto('/dashboard');
  });
  
  test('should display Turkish UI elements correctly', async () => {
    // Test all Turkish UI elements
    const turkishElements = [
      'Ana Panel',
      'Akıllı Arama',
      'Analitikler',
      'Ayarlar',
      'Profil',
      'Sistem Durumu'
    ];
    
    for (const element of turkishElements) {
      await expect(page.locator(`text=${element}`)).toBeVisible();
    }
  });
  
  test('should apply Context7 glassmorphism styles', async () => {
    // Test glassmorphism CSS properties
    const card = page.locator('.context7-card').first();
    
    await expect(card).toHaveCSS('backdrop-filter', 'blur(10px)');
    await expect(card).toHaveCSS('background', /rgba\(255, 255, 255, 0\.1\)/);
    await expect(card).toHaveCSS('border-radius', '12px');
    
    // Test button styles
    const button = page.locator('.context7-button').first();
    await expect(button).toHaveCSS('background', /linear-gradient/);
  });
  
  test('should handle responsive design', async () => {
    // Test different viewport sizes
    const viewports = [
      { width: 320, height: 568 },  // Mobile
      { width: 768, height: 1024 }, // Tablet
      { width: 1920, height: 1080 } // Desktop
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      
      // Dashboard should be visible and properly formatted
      await expect(page.locator('.context7-dashboard')).toBeVisible();
      
      // Navigation should adapt to viewport
      const nav = page.locator('.context7-nav');
      await expect(nav).toBeVisible();
    }
  });
  
  test('should handle Turkish character input', async () => {
    // Test Turkish character input in search
    const searchInput = page.locator('[data-testid="search-input"]');
    
    const turkishPhrases = [
      'çalışma belgesi',
      'öğrenci listesi',
      'ürün analizi',
      'şirket raporu'
    ];
    
    for (const phrase of turkishPhrases) {
      await searchInput.fill(phrase);
      await expect(searchInput).toHaveValue(phrase);
      
      // Trigger search
      await page.click('[data-testid="search-button"]');
      
      // Should show search results
      await expect(page.locator('.search-results')).toBeVisible();
      
      // Clear for next test
      await searchInput.clear();
    }
  });
});

test.describe('Search Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/search');
  });
  
  test('should perform semantic search', async () => {
    // Enable semantic search
    await page.check('[data-testid="semantic-toggle"]');
    await expect(page.locator('[data-testid="semantic-toggle"]')).toBeChecked();
    
    // Perform search
    await page.fill('[data-testid="search-input"]', 'django web framework');
    await page.click('[data-testid="search-button"]');
    
    // Should show semantic search results
    await expect(page.locator('.semantic-results')).toBeVisible();
    await expect(page.locator('.result-item')).toHaveCount({ min: 1 });
  });
  
  test('should handle search filters', async () => {
    // Open filters
    await page.click('[data-testid="filters-toggle"]');
    await expect(page.locator('.filters-panel')).toBeVisible();
    
    // Select file type filter
    await page.selectOption('[data-testid="file-type-filter"]', 'python');
    
    // Select date range
    await page.fill('[data-testid="date-from"]', '2024-01-01');
    await page.fill('[data-testid="date-to"]', '2024-12-31');
    
    // Apply filters
    await page.click('[data-testid="apply-filters"]');
    
    // Should show filtered results
    await expect(page.locator('.filtered-results')).toBeVisible();
    
    // All results should be Python files
    const results = page.locator('.result-item');
    const count = await results.count();
    
    for (let i = 0; i < count; i++) {
      const result = results.nth(i);
      await expect(result.locator('.file-type')).toContainText('python');
    }
  });
  
  test('should handle search errors gracefully', async () => {
    // Mock API error
    await page.route('/api/search*', route => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          success: false,
          message: 'Sunucu hatası'
        })
      });
    });
    
    // Perform search
    await page.fill('[data-testid="search-input"]', 'test query');
    await page.click('[data-testid="search-button"]');
    
    // Should show error message in Turkish
    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page.locator('.error-message')).toContainText('Sunucu hatası');
  });
});

test.describe('Performance Tests', () => {
  test('should load dashboard within performance budget', async ({ page }) => {
    const start = Date.now();
    
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - start;
    
    // Should load within 3 seconds
    expect(loadTime).toBeLessThan(3000);
  });
  
  test('should handle large search results efficiently', async ({ page }) => {
    // Mock large search results
    const largeResults = Array.from({ length: 1000 }, (_, i) => ({
      id: i,
      file_path: `/test/file_${i}.py`,
      content_snippet: `Content snippet ${i}`,
      relevance_score: Math.random()
    }));
    
    await page.route('/api/search*', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          success: true,
          data: largeResults.slice(0, 50), // Paginated
          total: largeResults.length
        })
      });
    });
    
    await page.goto('/search');
    
    const start = Date.now();
    await page.fill('[data-testid="search-input"]', 'test');
    await page.click('[data-testid="search-button"]');
    await page.waitForSelector('.search-results');
    const end = Date.now();
    
    // Should handle large results quickly
    expect(end - start).toBeLessThan(2000);
  });
});
```

### Component Testing with Vitest
```typescript
// ✅ Advanced Component Tests
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SearchPanel } from './SearchPanel';

describe('SearchPanel', () => {
  let queryClient: QueryClient;
  
  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false }
      }
    });
  });
  
  const renderWithProviders = (component: React.ReactElement) => {
    return render(
      <QueryClientProvider client={queryClient}>
        {component}
      </QueryClientProvider>
    );
  };
  
  it('renders Turkish UI elements correctly', () => {
    renderWithProviders(<SearchPanel />);
    
    expect(screen.getByPlaceholderText('Akıllı arama yap...')).toBeInTheDocument();
    expect(screen.getByText('Ara')).toBeInTheDocument();
    expect(screen.getByText('Filtreler')).toBeInTheDocument();
    expect(screen.getByText('Anlamsal Arama')).toBeInTheDocument();
  });
  
  it('handles Turkish character input correctly', async () => {
    const mockOnSearch = vi.fn();
    renderWithProviders(<SearchPanel onSearch={mockOnSearch} />);
    
    const searchInput = screen.getByPlaceholderText('Akıllı arama yap...');
    
    // Test Turkish characters
    fireEvent.change(searchInput, { target: { value: 'çalışma belgesi' } });
    
    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith('çalışma belgesi');
    });
    
    // Test special characters
    fireEvent.change(searchInput, { target: { value: 'öğrenci listesi' } });
    
    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith('öğrenci listesi');
    });
  });
  
  it('applies Context7 styles correctly', () => {
    renderWithProviders(<SearchPanel />);
    
    const panel = screen.getByTestId('search-panel');
    expect(panel).toHaveClass('context7-search-panel');
    
    const button = screen.getByRole('button', { name: /ara/i });
    expect(button).toHaveClass('context7-button');
  });
  
  it('handles search errors with Turkish messages', async () => {
    const mockOnSearch = vi.fn().mockRejectedValue(new Error('API Error'));
    renderWithProviders(<SearchPanel onSearch={mockOnSearch} />);
    
    const searchInput = screen.getByPlaceholderText('Akıllı arama yap...');
    const searchButton = screen.getByText('Ara');
    
    fireEvent.change(searchInput, { target: { value: 'test' } });
    fireEvent.click(searchButton);
    
    await waitFor(() => {
      expect(screen.getByText('Arama sırasında hata oluştu')).toBeInTheDocument();
    });
  });
  
  it('supports keyboard navigation', () => {
    renderWithProviders(<SearchPanel />);
    
    const searchInput = screen.getByPlaceholderText('Akıllı arama yap...');
    const searchButton = screen.getByText('Ara');
    
    // Tab navigation
    searchInput.focus();
    fireEvent.keyDown(searchInput, { key: 'Tab' });
    expect(searchButton).toHaveFocus();
    
    // Enter key search
    fireEvent.keyDown(searchInput, { key: 'Enter' });
    // Should trigger search
  });
});
```

## 🚀 Performance & Load Testing

### Performance Testing
```python
# ✅ Performance Testing
import pytest
import time
import concurrent.futures
from django.test import TestCase
from django.test.utils import override_settings
from django.db import connections

class PerformanceTestCase(TestCase):
    """Performance testing utilities."""
    
    def setUp(self):
        """Set up performance test environment."""
        self.start_time = time.time()
        
        # Create baseline data
        self.create_baseline_data()
    
    def tearDown(self):
        """Clean up and report performance."""
        end_time = time.time()
        test_duration = end_time - self.start_time
        
        print(f"Test completed in {test_duration:.2f} seconds")
        
        # Report database queries
        for conn in connections.all():
            queries = len(conn.queries)
            print(f"Database queries: {queries}")
    
    def create_baseline_data(self):
        """Create baseline data for performance tests."""
        # Create 10,000 files for performance testing
        files = []
        for i in range(10000):
            files.append(FileIndex(
                file_path=f'/perf/file_{i}.py',
                content_hash=f'perf_hash_{i}',
                file_size=1024 * (i % 10 + 1),
                content_type='python',
                search_keywords=f'performance test_{i} keyword',
                last_modified=timezone.now()
            ))
        
        # Bulk create for performance
        FileIndex.objects.bulk_create(files, batch_size=1000)
    
    def test_search_performance_with_large_dataset(self):
        """Test search performance with large dataset."""
        search_queries = [
            'performance',
            'test',
            'keyword',
            'python',
            'file'
        ]
        
        for query in search_queries:
            start_time = time.time()
            
            results = FileIndex.objects.filter(
                search_keywords__icontains=query
            )[:50]
            
            # Force evaluation
            list(results)
            
            end_time = time.time()
            query_time = end_time - start_time
            
            # Should complete within 500ms
            self.assertLess(query_time, 0.5, f"Query '{query}' took {query_time:.2f}s")
    
    def test_concurrent_search_performance(self):
        """Test concurrent search performance."""
        def perform_search(query):
            start_time = time.time()
            results = list(FileIndex.objects.filter(
                search_keywords__icontains=query
            )[:10])
            end_time = time.time()
            return end_time - start_time, len(results)
        
        # Test with 10 concurrent searches
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(perform_search, f'test_{i}')
                for i in range(10)
            ]
            
            results = [future.result() for future in futures]
        
        # All searches should complete quickly
        for query_time, result_count in results:
            self.assertLess(query_time, 1.0)
            self.assertGreaterEqual(result_count, 0)
    
    def test_database_query_optimization(self):
        """Test database query optimization."""
        # Reset query log
        for conn in connections.all():
            conn.queries_log.clear()
        
        # Perform complex query
        files = FileIndex.objects.select_related().filter(
            content_type='python'
        ).order_by('-last_modified')[:100]
        
        # Force evaluation
        list(files)
        
        # Should use minimal queries
        total_queries = sum(len(conn.queries) for conn in connections.all())
        self.assertLessEqual(total_queries, 2, f"Used {total_queries} queries")
```

### Load Testing
```javascript
// ✅ Load Testing with Artillery
// artillery.yml
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 10
    - duration: 120
      arrivalRate: 50
    - duration: 60
      arrivalRate: 100
  processor: "./load-test-processor.js"

scenarios:
  - name: "Search API Load Test"
    weight: 70
    flow:
      - post:
          url: "/api/auth/login/"
          json:
            username: "testuser"
            password: "testpass"
          capture:
            - json: "$.token"
              as: "auth_token"
      - get:
          url: "/api/search/"
          qs:
            q: "{{ $randomString() }}"
            limit: 20
          headers:
            Authorization: "Bearer {{ auth_token }}"
  
  - name: "Dashboard Load Test"
    weight: 30
    flow:
      - get:
          url: "/dashboard"
          headers:
            Authorization: "Bearer {{ auth_token }}"
```

## 🔧 Test Automation & CI/CD

### GitHub Actions Testing
```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run backend tests
      run: |
        python -m pytest tests/ -v --cov=src --cov-report=xml
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run unit tests
      run: npm run test:unit
    
    - name: Install Playwright
      run: npx playwright install --with-deps
    
    - name: Run E2E tests
      run: npm run test:e2e
    
    - name: Upload Playwright results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: playwright-report/
```

@tests/conftest.py
@tests/test_performance.py
@tests/ui/dashboard.spec.ts
@tests/components/SearchPanel.test.tsx 