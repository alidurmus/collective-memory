---
description: Performance optimization patterns ve best practices
globs: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "api/**/*", "src/**/*"]
alwaysApply: false
---

# ⚡ Performance Optimization Patterns

Cursor.directory community best practices ile optimize edilmiş performance kuralları.

## 🚀 Frontend Performance

### React Performance Patterns
```typescript
// ✅ Memoization Best Practices
import React, { memo, useMemo, useCallback, lazy, Suspense } from 'react';

// Component memoization
const KullaniciKarti = memo<{
  readonly kullanici: KullaniciData;
  readonly onKullaniciClick: (id: string) => void;
}>(({ kullanici, onKullaniciClick }) => {
  const handleClick = useCallback(() => {
    onKullaniciClick(kullanici.id);
  }, [kullanici.id, onKullaniciClick]);

  return (
    <div className="context7-card" onClick={handleClick}>
      <h3>{kullanici.ad}</h3>
      <p>{kullanici.email}</p>
    </div>
  );
});

// Complex computation memoization
const AramaSonuclari = memo<{
  readonly sonuclar: SearchResult[];
  readonly aramaKelimesi: string;
}>(({ sonuclar, aramaKelimesi }) => {
  const islenmisSonuclar = useMemo(() => {
    return sonuclar.map(sonuc => ({
      ...sonuc,
      vurgulanmisIcerik: highlightSearchTerms(sonuc.content, aramaKelimesi),
      formatlanmisTarih: formatTurkishDate(sonuc.lastModified),
      boyutMB: Math.round(sonuc.fileSize / 1024 / 1024 * 100) / 100
    }));
  }, [sonuclar, aramaKelimesi]);

  return (
    <div className="arama-sonuclari">
      {islenmisSonuclar.map(sonuc => (
        <SonucKarti key={sonuc.id} sonuc={sonuc} />
      ))}
    </div>
  );
});

// Lazy loading with error boundaries
const LazyAnalitikler = lazy(() => import('./Analitikler'));
const LazyAyarlar = lazy(() => import('./Ayarlar'));

function App() {
  return (
    <Suspense fallback={<div className="context7-loading">Yükleniyor...</div>}>
      <ErrorBoundary>
        <Routes>
          <Route path="/analitikler" element={<LazyAnalitikler />} />
          <Route path="/ayarlar" element={<LazyAyarlar />} />
        </Routes>
      </ErrorBoundary>
    </Suspense>
  );
}
```

### Virtual Scrolling
```typescript
// ✅ Virtual Scrolling for Large Lists
import { FixedSizeList as List } from 'react-window';

interface VirtualizedListProps {
  readonly items: SearchResult[];
  readonly onItemClick: (item: SearchResult) => void;
}

const VirtualizedSearchResults: React.FC<VirtualizedListProps> = ({ 
  items, 
  onItemClick 
}) => {
  const Row = useCallback(({ index, style }: { index: number; style: React.CSSProperties }) => {
    const item = items[index];
    
    return (
      <div style={style}>
        <div 
          className="context7-result-item"
          onClick={() => onItemClick(item)}
        >
          <h4>{item.fileName}</h4>
          <p>{item.snippet}</p>
          <span className="dosya-boyutu">{item.fileSizeMB} MB</span>
        </div>
      </div>
    );
  }, [items, onItemClick]);

  return (
    <List
      height={600}
      itemCount={items.length}
      itemSize={80}
      width="100%"
    >
      {Row}
    </List>
  );
};
```

### Bundle Optimization
```typescript
// ✅ Code Splitting Strategies
// Dynamic imports for route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const SearchPage = lazy(() => import('./pages/SearchPage'));

// Feature-based splitting
const AyarlarModal = lazy(() => import('./components/AyarlarModal'));

// Third-party library splitting
const ChartComponent = lazy(() => 
  import('recharts').then(module => ({ default: module.LineChart }))
);

// Webpack bundle analysis
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@headlessui/react', '@heroicons/react'],
          charts: ['recharts', 'd3'],
          utils: ['lodash', 'date-fns']
        }
      }
    }
  }
});
```

## 🐍 Backend Performance

### Database Optimization
```python
# ✅ Database Query Optimization
from django.db import models
from django.db.models import Prefetch, Q, F, Case, When, Count, Avg
from django.core.cache import cache
from django.views.decorators.cache import cache_page

class OptimizedFileManager(models.Manager):
    """Optimized manager with select_related and prefetch_related."""
    
    def get_with_relations(self):
        """Get files with optimized relations."""
        return self.select_related(
            'created_by', 'updated_by'
        ).prefetch_related(
            Prefetch(
                'tags',
                queryset=Tag.objects.select_related('category')
            ),
            'comments__author'
        )
    
    def bulk_update_scores(self, score_updates):
        """Bulk update relevance scores."""
        cases = [
            When(id=file_id, then=score)
            for file_id, score in score_updates.items()
        ]
        
        self.filter(id__in=score_updates.keys()).update(
            relevance_score=Case(*cases)
        )

class FileIndex(models.Model):
    # ... existing fields ...
    
    objects = OptimizedFileManager()
    
    class Meta:
        indexes = [
            models.Index(fields=['file_path']),
            models.Index(fields=['content_type', 'created_at']),
            models.Index(fields=['relevance_score', 'last_modified']),
            models.Index(fields=['file_size', 'content_type']),
        ]

# Query optimization decorators
def optimize_queryset(select_related=None, prefetch_related=None):
    """Decorator for queryset optimization."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            queryset = func(self, *args, **kwargs)
            
            if select_related:
                queryset = queryset.select_related(*select_related)
            
            if prefetch_related:
                queryset = queryset.prefetch_related(*prefetch_related)
            
            return queryset
        return wrapper
    return decorator

class SearchView(generics.ListAPIView):
    """Optimized search view."""
    
    @optimize_queryset(
        select_related=['created_by'],
        prefetch_related=['tags', 'comments']
    )
    def get_queryset(self):
        """Get optimized queryset."""
        return FileIndex.objects.get_with_relations()
```

### Caching Strategies
```python
# ✅ Multi-Level Caching
import redis
from functools import wraps
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

class CacheOptimizer:
    """Advanced caching with Turkish UI support."""
    
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.default_timeout = 300
    
    def cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key."""
        key_parts = [prefix] + list(args) + [f"{k}:{v}" for k, v in kwargs.items()]
        return ":".join(str(part) for part in key_parts)
    
    def multi_level_cache(self, 
                         memory_timeout: int = 60,
                         redis_timeout: int = 300):
        """Multi-level caching decorator."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self.cache_key(func.__name__, *args, **kwargs)
                
                # Level 1: Memory cache
                result = cache.get(cache_key)
                if result is not None:
                    return result
                
                # Level 2: Redis cache
                result = self.redis_client.get(cache_key)
                if result is not None:
                    result = json.loads(result)
                    cache.set(cache_key, result, memory_timeout)
                    return result
                
                # Level 3: Database
                result = func(*args, **kwargs)
                
                # Cache at both levels
                cache.set(cache_key, result, memory_timeout)
                self.redis_client.setex(
                    cache_key, 
                    redis_timeout, 
                    json.dumps(result)
                )
                
                return result
            return wrapper
        return decorator
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache keys matching pattern."""
        for key in self.redis_client.scan_iter(match=pattern):
            self.redis_client.delete(key)
            cache.delete(key.decode())

# Usage example
cache_optimizer = CacheOptimizer()

@cache_optimizer.multi_level_cache(memory_timeout=60, redis_timeout=300)
def get_arama_sonuclari(query: str, filters: dict) -> List[dict]:
    """Get search results with caching."""
    return FileIndex.objects.filter(
        search_keywords__icontains=query
    ).values()
```

### Async Performance
```python
# ✅ Async Performance Patterns
import asyncio
import aiohttp
import aioredis
from asgiref.sync import sync_to_async

class AsyncSearchEngine:
    """Async search engine for better performance."""
    
    def __init__(self):
        self.redis_pool = None
        self.session = None
    
    async def __aenter__(self):
        self.redis_pool = aioredis.ConnectionPool.from_url(
            "redis://localhost", 
            max_connections=10
        )
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        if self.redis_pool:
            await self.redis_pool.disconnect()
    
    async def search_files(self, query: str, limit: int = 50) -> List[dict]:
        """Async file search."""
        # Check cache first
        redis = aioredis.Redis(connection_pool=self.redis_pool)
        cache_key = f"search:{hash(query)}"
        
        cached_result = await redis.get(cache_key)
        if cached_result:
            return json.loads(cached_result)
        
        # Async database query
        results = await sync_to_async(list)(
            FileIndex.objects.filter(
                search_keywords__icontains=query
            ).values()[:limit]
        )
        
        # Cache results
        await redis.setex(
            cache_key, 
            300, 
            json.dumps(results)
        )
        
        return results
    
    async def batch_process_files(self, file_paths: List[str]) -> List[dict]:
        """Batch process files async."""
        semaphore = asyncio.Semaphore(10)  # Limit concurrency
        
        async def process_file(path: str) -> dict:
            async with semaphore:
                # Simulate file processing
                await asyncio.sleep(0.1)
                return {
                    'path': path,
                    'processed': True,
                    'timestamp': datetime.now().isoformat()
                }
        
        tasks = [process_file(path) for path in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r for r in results if not isinstance(r, Exception)]
```

## 📊 Performance Monitoring

### Performance Metrics
```python
# ✅ Performance Monitoring
import time
import psutil
import threading
from functools import wraps
from contextlib import contextmanager

class PerformanceMonitor:
    """Performance monitoring utilities."""
    
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()
    
    def measure_execution_time(self, func_name: str = None):
        """Measure function execution time."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    name = func_name or func.__name__
                    with self.lock:
                        if name not in self.metrics:
                            self.metrics[name] = []
                        self.metrics[name].append(execution_time)
                    
                    # Turkish logging
                    if execution_time > 1.0:
                        logger.warning(
                            f"Yavaş işlem: {name} - {execution_time:.2f} saniye"
                        )
            
            return wrapper
        return decorator
    
    def get_system_metrics(self) -> dict:
        """Get system performance metrics."""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict()
        }
    
    def get_performance_report(self) -> dict:
        """Get performance report in Turkish."""
        report = {
            'sistem_metrikleri': self.get_system_metrics(),
            'fonksiyon_metrikleri': {}
        }
        
        with self.lock:
            for func_name, times in self.metrics.items():
                report['fonksiyon_metrikleri'][func_name] = {
                    'ortalama_süre': sum(times) / len(times),
                    'en_yavaş': max(times),
                    'en_hızlı': min(times),
                    'toplam_çağrı': len(times)
                }
        
        return report

# Usage
monitor = PerformanceMonitor()

@monitor.measure_execution_time('arama_işlemi')
def search_files(query: str) -> List[dict]:
    """Search files with performance monitoring."""
    return FileIndex.objects.filter(
        search_keywords__icontains=query
    ).values()
```

### Database Performance
```python
# ✅ Database Performance Monitoring
from django.db import connection
from django.core.management.base import BaseCommand

class DatabasePerformanceMonitor:
    """Database performance monitoring."""
    
    @contextmanager
    def monitor_queries(self):
        """Monitor database queries."""
        queries_before = len(connection.queries)
        start_time = time.time()
        
        yield
        
        queries_after = len(connection.queries)
        end_time = time.time()
        
        queries_count = queries_after - queries_before
        execution_time = end_time - start_time
        
        if queries_count > 5:
            logger.warning(
                f"Yüksek sorgu sayısı: {queries_count} sorgu, "
                f"{execution_time:.2f} saniye"
            )
    
    def analyze_slow_queries(self):
        """Analyze slow queries."""
        slow_queries = []
        
        for query in connection.queries:
            if float(query['time']) > 0.1:  # 100ms threshold
                slow_queries.append({
                    'sql': query['sql'],
                    'time': query['time'],
                    'türkçe_açıklama': 'Yavaş sorgu tespit edildi'
                })
        
        return slow_queries
    
    def get_query_statistics(self) -> dict:
        """Get query statistics."""
        total_queries = len(connection.queries)
        total_time = sum(float(q['time']) for q in connection.queries)
        
        return {
            'toplam_sorgu': total_queries,
            'toplam_süre': total_time,
            'ortalama_süre': total_time / total_queries if total_queries > 0 else 0,
            'yavaş_sorgu_sayısı': len(self.analyze_slow_queries())
        }
```

## 🔧 Performance Best Practices

### Frontend Guidelines
```typescript
// ✅ Performance Best Practices
// 1. Debounce user inputs
const useDebounce = (value: string, delay: number) => {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => clearTimeout(handler);
  }, [value, delay]);
  
  return debouncedValue;
};

// 2. Optimize re-renders
const SearchInput = memo(({ onSearch }: { onSearch: (query: string) => void }) => {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);
  
  useEffect(() => {
    if (debouncedQuery) {
      onSearch(debouncedQuery);
    }
  }, [debouncedQuery, onSearch]);
  
  return (
    <input
      type="text"
      placeholder="Akıllı arama yap..."
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      className="context7-input"
    />
  );
});

// 3. Optimize images
const OptimizedImage = ({ src, alt, ...props }: ImageProps) => {
  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      decoding="async"
      {...props}
    />
  );
};
```

### Backend Guidelines
```python
# ✅ Backend Performance Guidelines
# 1. Use database indexes
class FileIndex(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['file_path']),
            models.Index(fields=['content_type', 'created_at']),
            models.Index(fields=['search_keywords']),
            models.Index(fields=['relevance_score', 'last_modified']),
        ]

# 2. Optimize querysets
def get_search_results(query: str, limit: int = 50):
    """Get search results with optimizations."""
    return FileIndex.objects.select_related(
        'created_by'
    ).prefetch_related(
        'tags'
    ).filter(
        search_keywords__icontains=query
    ).order_by('-relevance_score')[:limit]

# 3. Use bulk operations
def bulk_update_files(updates: List[dict]):
    """Bulk update files for better performance."""
    FileIndex.objects.bulk_update(
        updates,
        ['relevance_score', 'last_modified'],
        batch_size=1000
    )

# 4. Cache expensive operations
@cache_optimizer.multi_level_cache(redis_timeout=600)
def get_analytics_data():
    """Get analytics data with caching."""
    return {
        'toplam_dosya': FileIndex.objects.count(),
        'dosya_türleri': FileIndex.objects.values('content_type').annotate(
            count=Count('id')
        ),
        'son_aramalar': SearchHistory.objects.order_by('-created_at')[:10]
    }
```

@utils/performance.py
@hooks/usePerformance.ts
@components/VirtualizedList.tsx
@monitoring/performance.py 