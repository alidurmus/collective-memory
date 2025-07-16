---
description: Advanced Python/Django/FastAPI backend geliştirme kuralları
globs: ["**/*.py", "src/**/*.py", "backend/**/*.py", "api/**/*.py", "models/**/*.py", "views/**/*.py", "serializers/**/*.py", "tests/**/*.py"]
alwaysApply: false
---

# 🐍 Advanced Python/Django Backend Kuralları

Cursor.directory community best practices ile optimize edilmiş modern Python backend geliştirme kuralları.

## 🚀 Modern Python Patterns (3.9+)

### Type Safety & Annotations
```python
# ✅ Comprehensive Type Annotations
from typing import Dict, List, Optional, Union, Any, Callable, TypeVar, Generic
from typing_extensions import Literal, TypedDict
from dataclasses import dataclass, field
from enum import Enum
import asyncio

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

# Turkish UI types with English internals
class UILabelType(TypedDict):
    dashboard: str
    search: str
    analytics: str
    settings: str
    error: str
    success: str

UI_LABELS: UILabelType = {
    "dashboard": "Ana Panel",
    "search": "Akıllı Arama", 
    "analytics": "Analitikler",
    "settings": "Ayarlar",
    "error": "Hata oluştu",
    "success": "Başarılı"
}

class SearchResultType(Enum):
    FILE = "file"
    CONTENT = "content"
    CONTEXT = "context"
    CHAT = "chat"

@dataclass(frozen=True)
class SearchResult:
    """Immutable search result with comprehensive metadata."""
    id: str
    file_path: str
    content_snippet: str
    relevance_score: float
    result_type: SearchResultType
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    last_modified: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'file_path': self.file_path,
            'content_snippet': self.content_snippet,
            'relevance_score': self.relevance_score,
            'result_type': self.result_type.value,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'last_modified': self.last_modified
        }

# Generic repository pattern
class Repository(Generic[T]):
    """Generic repository for type-safe data operations."""
    
    def __init__(self, model_class: type[T]):
        self.model_class = model_class
    
    async def get_by_id(self, id: str) -> Optional[T]:
        """Get entity by ID."""
        raise NotImplementedError
    
    async def save(self, entity: T) -> T:
        """Save entity."""
        raise NotImplementedError
    
    async def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        raise NotImplementedError
```

### Async/Await Patterns
```python
# ✅ Advanced Async Patterns
import asyncio
import aiohttp
import aiofiles
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

class AsyncContextManager:
    """Async context manager for resource management."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        # Initialize async connection
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        if self.connection:
            await self.connection.close()

# Async decorator for retry logic
def async_retry(max_retries: int = 3, delay: float = 1.0):
    """Async retry decorator with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (2 ** attempt))
                    else:
                        raise last_exception
            
            raise last_exception
        return wrapper
    return decorator

# Async batch processing
async def process_files_batch(
    file_paths: List[str],
    batch_size: int = 10,
    max_workers: int = 4
) -> List[Dict[str, Any]]:
    """Process files in batches with concurrency control."""
    semaphore = asyncio.Semaphore(max_workers)
    
    async def process_single_file(file_path: str) -> Dict[str, Any]:
        async with semaphore:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                content = await file.read()
                return {
                    'file_path': file_path,
                    'content_length': len(content),
                    'processed_at': datetime.now().isoformat()
                }
    
    results = []
    for i in range(0, len(file_paths), batch_size):
        batch = file_paths[i:i + batch_size]
        batch_results = await asyncio.gather(
            *[process_single_file(path) for path in batch],
            return_exceptions=True
        )
        results.extend(batch_results)
    
    return [r for r in results if not isinstance(r, Exception)]
```

## 🏗️ Django Advanced Patterns

### Custom Model Managers
```python
# ✅ Advanced Django Model Patterns
from django.db import models
from django.db.models import QuerySet, Q
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class TimestampedModel(models.Model):
    """Base model with automatic timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class SoftDeleteQuerySet(QuerySet):
    """QuerySet with soft delete functionality."""
    
    def delete(self):
        """Soft delete all objects in queryset."""
        return self.update(deleted_at=timezone.now())
    
    def hard_delete(self):
        """Actually delete objects from database."""
        return super().delete()
    
    def alive(self):
        """Return only non-deleted objects."""
        return self.filter(deleted_at__isnull=True)
    
    def dead(self):
        """Return only deleted objects."""
        return self.filter(deleted_at__isnull=False)

class SoftDeleteManager(models.Manager):
    """Manager with soft delete capabilities."""
    
    def get_queryset(self):
        """Return only non-deleted objects by default."""
        return SoftDeleteQuerySet(self.model, using=self._db).alive()
    
    def all_with_deleted(self):
        """Return all objects including deleted ones."""
        return SoftDeleteQuerySet(self.model, using=self._db)
    
    def deleted_only(self):
        """Return only deleted objects."""
        return SoftDeleteQuerySet(self.model, using=self._db).dead()

class FileIndex(TimestampedModel):
    """Advanced file index model with soft delete."""
    file_path = models.CharField(max_length=1000, unique=True, db_index=True)
    content_hash = models.CharField(max_length=64, db_index=True)
    file_size = models.PositiveIntegerField()
    content_type = models.CharField(max_length=100, db_index=True)
    search_keywords = models.TextField(blank=True)
    last_modified = models.DateTimeField(db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Access to all objects
    
    class Meta:
        db_table = 'file_index'
        indexes = [
            models.Index(fields=['file_path']),
            models.Index(fields=['content_hash']),
            models.Index(fields=['last_modified', 'deleted_at']),
            models.Index(fields=['content_type', 'deleted_at']),
        ]
        
    def __str__(self):
        return f"FileIndex({self.file_path})"
    
    def soft_delete(self):
        """Soft delete this object."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    
    def restore(self):
        """Restore soft deleted object."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])
```

### Advanced API Views
```python
# ✅ Advanced DRF Views with Turkish UI
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from django.core.cache import cache
from django.db.models import Q, Count, Avg
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

class SearchThrottle(UserRateThrottle):
    """Custom throttle for search operations."""
    scope = 'search'
    rate = '100/hour'

class AdvancedSearchAPIView(generics.ListAPIView):
    """Advanced search with caching, pagination, and filtering."""
    serializer_class = FileIndexSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [SearchThrottle]
    
    def get_queryset(self):
        """Build complex query with multiple filters."""
        query = self.request.query_params.get('q', '')
        file_type = self.request.query_params.get('type', '')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        min_size = self.request.query_params.get('min_size')
        max_size = self.request.query_params.get('max_size')
        
        # Build cache key
        cache_key = f"search:{hash(str(self.request.query_params))}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        queryset = FileIndex.objects.select_related().prefetch_related()
        
        # Text search
        if query:
            queryset = queryset.filter(
                Q(file_path__icontains=query) |
                Q(search_keywords__icontains=query)
            )
        
        # File type filter
        if file_type:
            queryset = queryset.filter(content_type=file_type)
        
        # Date range filter
        if date_from:
            queryset = queryset.filter(last_modified__gte=date_from)
        if date_to:
            queryset = queryset.filter(last_modified__lte=date_to)
        
        # Size range filter
        if min_size:
            queryset = queryset.filter(file_size__gte=min_size)
        if max_size:
            queryset = queryset.filter(file_size__lte=max_size)
        
        # Cache results for 5 minutes
        cache.set(cache_key, queryset, 300)
        
        return queryset.order_by('-last_modified')
    
    @method_decorator(cache_page(60))  # Cache view for 1 minute
    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request, *args, **kwargs):
        """Handle search with comprehensive Turkish response."""
        try:
            # Performance tracking
            start_time = timezone.now()
            
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                paginated_response = self.get_paginated_response(serializer.data)
                
                # Add Turkish metadata
                paginated_response.data.update({
                    'success': True,
                    'message': 'Arama başarılı',
                    'metadata': {
                        'total_results': queryset.count(),
                        'search_time_ms': (timezone.now() - start_time).total_seconds() * 1000,
                        'cached': cache.get(f"search:{hash(str(request.query_params))}") is not None
                    }
                })
                
                return paginated_response
            
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'success': True,
                'message': 'Arama başarılı',
                'data': serializer.data,
                'metadata': {
                    'total_results': len(serializer.data),
                    'search_time_ms': (timezone.now() - start_time).total_seconds() * 1000
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': 'Arama sırasında hata oluştu',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Advanced analytics endpoint
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_api(request):
    """Advanced analytics with Turkish UI."""
    try:
        # Cache key with user-specific data
        cache_key = f"analytics:{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({
                'success': True,
                'message': 'Analitik veriler başarıyla alındı',
                'data': cached_data,
                'cached': True
            })
        
        # Complex aggregations
        file_stats = FileIndex.objects.aggregate(
            total_files=Count('id'),
            total_size=models.Sum('file_size'),
            avg_size=Avg('file_size'),
            recent_files=Count('id', filter=Q(
                created_at__gte=timezone.now() - timezone.timedelta(days=7)
            ))
        )
        
        # File type distribution
        file_types = FileIndex.objects.values('content_type').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # Search patterns
        search_patterns = SearchHistory.objects.values('query').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        analytics_data = {
            'genel_istatistikler': {
                'toplam_dosya': file_stats['total_files'],
                'toplam_boyut_mb': round((file_stats['total_size'] or 0) / 1024 / 1024, 2),
                'ortalama_boyut_kb': round((file_stats['avg_size'] or 0) / 1024, 2),
                'son_hafta_dosya': file_stats['recent_files']
            },
            'dosya_turleri': [
                {'tur': ft['content_type'], 'adet': ft['count']} 
                for ft in file_types
            ],
            'populer_aramalar': [
                {'sorgu': sp['query'], 'adet': sp['count']} 
                for sp in search_patterns
            ]
        }
        
        # Cache for 15 minutes
        cache.set(cache_key, analytics_data, 900)
        
        return Response({
            'success': True,
            'message': 'Analitik veriler başarıyla alındı',
            'data': analytics_data,
            'cached': False
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Analitik veriler alınamadı',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

## 🔍 Advanced Search Engine

### Semantic Search Implementation
```python
# ✅ Advanced Semantic Search
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import faiss

class SemanticSearchEngine:
    """Advanced semantic search with vector similarity."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.embeddings = None
    
    async def build_index(self, documents: List[Dict[str, Any]]) -> None:
        """Build FAISS index for semantic search."""
        self.documents = documents
        
        # Extract content for embedding
        texts = [doc['content'] for doc in documents]
        
        # Generate embeddings
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Build FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings.astype(np.float32))
    
    async def search(
        self, 
        query: str, 
        k: int = 10,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Perform semantic search."""
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(
            query_embedding.astype(np.float32), k
        )
        
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if distance < threshold:  # Distance threshold
                doc = self.documents[idx]
                results.append({
                    **doc,
                    'similarity_score': float(1 - distance),  # Convert to similarity
                    'rank': i + 1
                })
        
        return results
    
    def update_document(self, doc_id: str, new_content: str) -> None:
        """Update document in index."""
        # Find document index
        doc_idx = None
        for i, doc in enumerate(self.documents):
            if doc['id'] == doc_id:
                doc_idx = i
                break
        
        if doc_idx is not None:
            # Update document
            self.documents[doc_idx]['content'] = new_content
            
            # Update embedding
            new_embedding = self.model.encode([new_content])
            self.embeddings[doc_idx] = new_embedding[0]
            
            # Rebuild index (for simplicity, in production use incremental updates)
            self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
            self.index.add(self.embeddings.astype(np.float32))
```

## 🚀 Performance Optimization

### Database Optimization
```python
# ✅ Advanced Database Optimization
from django.db import transaction
from django.db.models import Prefetch, F, Case, When
from django.core.cache import cache
from functools import wraps

class DatabaseOptimizer:
    """Database performance optimization utilities."""
    
    @staticmethod
    def bulk_create_with_ignore_conflicts(model, objects, batch_size=1000):
        """Bulk create with conflict resolution."""
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            model.objects.bulk_create(batch, ignore_conflicts=True)
    
    @staticmethod
    def bulk_update_with_case(model, updates, id_field='id'):
        """Bulk update using CASE statements."""
        if not updates:
            return
        
        # Build CASE statement for each field
        cases = {}
        ids = []
        
        for obj_id, fields in updates.items():
            ids.append(obj_id)
            for field, value in fields.items():
                if field not in cases:
                    cases[field] = []
                cases[field].append(When(pk=obj_id, then=value))
        
        # Build update kwargs
        update_kwargs = {}
        for field, whens in cases.items():
            update_kwargs[field] = Case(*whens)
        
        # Perform bulk update
        model.objects.filter(pk__in=ids).update(**update_kwargs)
    
    @staticmethod
    def optimize_queryset(queryset, select_related=None, prefetch_related=None):
        """Apply common optimizations to queryset."""
        if select_related:
            queryset = queryset.select_related(*select_related)
        
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)
        
        return queryset

# Performance monitoring decorator
def monitor_db_queries(func):
    """Monitor database queries for performance."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from django.db import connection
        
        queries_before = len(connection.queries)
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        queries_after = len(connection.queries)
        end_time = time.time()
        
        queries_count = queries_after - queries_before
        execution_time = end_time - start_time
        
        # Log performance metrics
        logger.info(
            f"Function {func.__name__} executed in {execution_time:.2f}s "
            f"with {queries_count} database queries"
        )
        
        # Alert if too many queries
        if queries_count > 10:
            logger.warning(f"High query count ({queries_count}) in {func.__name__}")
        
        return result
    return wrapper
```

### Caching Strategies
```python
# ✅ Advanced Caching Patterns
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import hashlib
import json

class CacheManager:
    """Advanced caching with Turkish UI support."""
    
    def __init__(self, default_timeout=300):
        self.default_timeout = default_timeout
    
    def get_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate consistent cache key."""
        key_data = {
            'prefix': prefix,
            'args': args,
            'kwargs': kwargs
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        
        return f"{prefix}:{key_hash}"
    
    def cached_result(self, key_prefix: str, timeout: int = None):
        """Decorator for caching function results."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self.get_cache_key(key_prefix, *args, **kwargs)
                
                # Try to get from cache
                result = cache.get(cache_key)
                if result is not None:
                    return result
                
                # Execute function
                result = func(*args, **kwargs)
                
                # Cache result
                cache.set(cache_key, result, timeout or self.default_timeout)
                
                return result
            return wrapper
        return decorator
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate cache keys matching pattern."""
        # Implementation depends on cache backend
        # For Redis: use SCAN with pattern matching
        pass

# Multi-level caching
class MultiLevelCache:
    """Multi-level caching system."""
    
    def __init__(self):
        self.memory_cache = {}
        self.memory_timeout = 60  # 1 minute
        self.redis_timeout = 300  # 5 minutes
    
    def get(self, key: str) -> Any:
        """Get value from multi-level cache."""
        # Level 1: Memory cache
        if key in self.memory_cache:
            value, timestamp = self.memory_cache[key]
            if time.time() - timestamp < self.memory_timeout:
                return value
            else:
                del self.memory_cache[key]
        
        # Level 2: Redis cache
        value = cache.get(key)
        if value is not None:
            # Store in memory cache
            self.memory_cache[key] = (value, time.time())
            return value
        
        return None
    
    def set(self, key: str, value: Any, timeout: int = None):
        """Set value in multi-level cache."""
        # Store in memory cache
        self.memory_cache[key] = (value, time.time())
        
        # Store in Redis cache
        cache.set(key, value, timeout or self.redis_timeout)
```

## 🧪 Advanced Testing

### Comprehensive Test Suite
```python
# ✅ Advanced Testing Patterns
import pytest
from unittest.mock import Mock, patch, AsyncMock
from django.test import TestCase, TransactionTestCase
from django.test.utils import override_settings
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status

class TestFileIndexModel(TestCase):
    """Comprehensive model testing."""
    
    def setUp(self):
        """Set up test data."""
        self.file_data = {
            'file_path': '/test/sample.py',
            'content_hash': 'abc123',
            'file_size': 1024,
            'content_type': 'python',
            'last_modified': timezone.now()
        }
    
    def test_file_creation_with_turkish_path(self):
        """Test file creation with Turkish characters."""
        turkish_path = '/projeler/çalışma_dosyası.py'
        
        file_obj = FileIndex.objects.create(
            file_path=turkish_path,
            content_hash='def456',
            file_size=2048,
            content_type='python',
            last_modified=timezone.now()
        )
        
        self.assertEqual(file_obj.file_path, turkish_path)
        self.assertTrue(file_obj.created_at)
        self.assertIsNone(file_obj.deleted_at)
    
    def test_soft_delete_functionality(self):
        """Test soft delete behavior."""
        file_obj = FileIndex.objects.create(**self.file_data)
        
        # Soft delete
        file_obj.soft_delete()
        
        # Should not appear in default queryset
        self.assertFalse(FileIndex.objects.filter(id=file_obj.id).exists())
        
        # Should appear in all_objects queryset
        self.assertTrue(FileIndex.all_objects.filter(id=file_obj.id).exists())
        
        # Should appear in deleted_only queryset
        self.assertTrue(FileIndex.objects.deleted_only().filter(id=file_obj.id).exists())
    
    def test_bulk_operations_performance(self):
        """Test bulk operations performance."""
        # Create large dataset
        files = []
        for i in range(1000):
            files.append(FileIndex(
                file_path=f'/test/file_{i}.py',
                content_hash=f'hash_{i}',
                file_size=1024,
                content_type='python',
                last_modified=timezone.now()
            ))
        
        # Measure bulk create performance
        start_time = time.time()
        FileIndex.objects.bulk_create(files, batch_size=100)
        end_time = time.time()
        
        # Should complete in reasonable time
        self.assertLess(end_time - start_time, 5.0)
        self.assertEqual(FileIndex.objects.count(), 1000)

class TestSearchAPI(APITestCase):
    """Advanced API testing."""
    
    def setUp(self):
        """Set up test environment."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data
        self.files = []
        for i in range(20):
            file_obj = FileIndex.objects.create(
                file_path=f'/test/file_{i}.py',
                content_hash=f'hash_{i}',
                file_size=1024,
                content_type='python',
                search_keywords=f'keyword_{i} test django',
                last_modified=timezone.now()
            )
            self.files.append(file_obj)
    
    def test_search_with_turkish_query(self):
        """Test search with Turkish characters."""
        self.client.force_authenticate(user=self.user)
        
        # Create file with Turkish content
        FileIndex.objects.create(
            file_path='/test/türkçe_dosya.py',
            content_hash='turkish_hash',
            file_size=2048,
            content_type='python',
            search_keywords='türkçe içerik çalışma',
            last_modified=timezone.now()
        )
        
        response = self.client.get('/api/search/', {'q': 'türkçe'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Arama başarılı')
        self.assertGreater(len(response.data['data']), 0)
    
    def test_search_performance_with_large_dataset(self):
        """Test search performance with large dataset."""
        # Create large dataset
        files = []
        for i in range(1000):
            files.append(FileIndex(
                file_path=f'/large/file_{i}.py',
                content_hash=f'large_hash_{i}',
                file_size=1024,
                content_type='python',
                search_keywords=f'large keyword_{i}',
                last_modified=timezone.now()
            ))
        
        FileIndex.objects.bulk_create(files, batch_size=100)
        
        self.client.force_authenticate(user=self.user)
        
        # Measure search performance
        start_time = time.time()
        response = self.client.get('/api/search/', {'q': 'large'})
        end_time = time.time()
        
        # Should complete quickly
        self.assertLess(end_time - start_time, 2.0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
    
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
        
        # First request
        response1 = self.client.get('/api/search/', {'q': 'test'})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertFalse(response1.data['metadata']['cached'])
        
        # Second request (should be cached)
        response2 = self.client.get('/api/search/', {'q': 'test'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        # Note: This depends on implementation details
    
    def test_search_throttling(self):
        """Test search API throttling."""
        self.client.force_authenticate(user=self.user)
        
        # Make many requests quickly
        for i in range(105):  # Exceed rate limit
            response = self.client.get('/api/search/', {'q': f'test_{i}'})
            if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                break
        
        # Should eventually hit rate limit
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

@pytest.mark.asyncio
class TestAsyncPatterns:
    """Test async patterns."""
    
    async def test_async_file_processing(self):
        """Test async file processing."""
        file_paths = [f'/test/file_{i}.py' for i in range(10)]
        
        # Mock async file processing
        async def mock_process_file(path):
            await asyncio.sleep(0.1)  # Simulate processing
            return {'path': path, 'processed': True}
        
        with patch('aiofiles.open') as mock_open:
            mock_open.return_value.__aenter__.return_value.read = AsyncMock(
                return_value='test content'
            )
            
            results = await process_files_batch(file_paths, batch_size=3)
            
            assert len(results) == 10
            assert all(r['processed'] for r in results)
    
    async def test_async_search_engine(self):
        """Test async search engine."""
        engine = SemanticSearchEngine()
        
        documents = [
            {'id': '1', 'content': 'Python programming tutorial'},
            {'id': '2', 'content': 'Django web framework guide'},
            {'id': '3', 'content': 'Machine learning basics'},
        ]
        
        await engine.build_index(documents)
        results = await engine.search('Python programming', k=2)
        
        assert len(results) <= 2
        assert all('similarity_score' in r for r in results)
```

@src/models.py
@src/serializers.py
@src/views.py
@tests/test_advanced.py 