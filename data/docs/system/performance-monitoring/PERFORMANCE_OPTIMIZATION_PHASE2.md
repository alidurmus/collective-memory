# ⚡ Context7 ERP - Performance Optimization Phase 2

**Version:** v2.2.0-glassmorphism-enhanced + QMS Integration  
**Last Updated:** 12 Temmuz 2025  
**Status:** ✅ **PHASE 2 OPTIMIZATION READY**  
**Target:** <1s Response Time, 95%+ Cache Hit Rate  
**QMS Reference:** REC-PERFORMANCE-OPT-PHASE2-250712-001

---

## 🎯 **Phase 2 Optimization Goals**

### **Performance Targets**
- **Page Load Time:** <1 second (Target: 0.5s)
- **API Response:** <200ms (Target: 100ms)
- **Database Queries:** <50ms (Target: 25ms)
- **Cache Hit Rate:** 95%+ (Target: 98%)
- **CDN Delivery:** <100ms globally
- **Concurrent Users:** 1000+ simultaneous

### **Optimization Strategy**
- **Multi-Level Caching:** Redis + Memory + CDN
- **Database Optimization:** Query optimization, connection pooling
- **Frontend Performance:** Code splitting, lazy loading
- **CDN Integration:** Global content delivery
- **Monitoring & Analytics:** Real-time performance tracking

---

## 🔧 **Database Performance Optimization**

### **1. Advanced PostgreSQL Configuration**
```bash
# /etc/postgresql/15/main/postgresql.conf
# Context7 ERP Performance Configuration

# Memory Settings
shared_buffers = 512MB                    # 25% of RAM
effective_cache_size = 2GB                # 75% of RAM
work_mem = 16MB                           # Per query work memory
maintenance_work_mem = 256MB              # Maintenance operations

# Connection Settings
max_connections = 200                     # Concurrent connections
max_prepared_transactions = 200           # Prepared transactions

# WAL Settings
wal_buffers = 16MB                        # WAL buffer size
checkpoint_completion_target = 0.9        # Checkpoint target
wal_compression = on                      # WAL compression
max_wal_size = 2GB                        # Maximum WAL size
min_wal_size = 1GB                        # Minimum WAL size

# Query Optimization
default_statistics_target = 100           # Statistics detail
random_page_cost = 1.1                    # SSD optimization
seq_page_cost = 1.0                       # Sequential read cost
cpu_tuple_cost = 0.01                     # CPU cost per tuple
cpu_index_tuple_cost = 0.005              # CPU cost per index tuple
cpu_operator_cost = 0.0025                # CPU cost per operator

# Autovacuum Settings
autovacuum = on                           # Enable autovacuum
autovacuum_max_workers = 3                # Autovacuum workers
autovacuum_naptime = 20s                  # Autovacuum frequency
autovacuum_vacuum_threshold = 50          # Vacuum threshold
autovacuum_analyze_threshold = 50         # Analyze threshold

# Logging for Performance Analysis
log_min_duration_statement = 200          # Log slow queries (200ms+)
log_checkpoints = on                      # Log checkpoints
log_connections = on                      # Log connections
log_disconnections = on                   # Log disconnections
log_lock_waits = on                       # Log lock waits
```

### **2. Advanced Database Indexing**
```sql
-- Context7 ERP Performance Indexes
-- Connect to PostgreSQL: psql -U context7_user -d context7_erp

-- Customer Performance Indexes
CREATE INDEX CONCURRENTLY idx_customer_name_gin 
    ON erp_customer USING gin(to_tsvector('english', name));
CREATE INDEX CONCURRENTLY idx_customer_type_active 
    ON erp_customer(customer_type, is_active) WHERE is_active = true;
CREATE INDEX CONCURRENTLY idx_customer_created_date 
    ON erp_customer(created_at DESC);

-- Product Performance Indexes
CREATE INDEX CONCURRENTLY idx_product_name_gin 
    ON erp_product USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '')));
CREATE INDEX CONCURRENTLY idx_product_category_active 
    ON erp_product(category_id, is_active) WHERE is_active = true;
CREATE INDEX CONCURRENTLY idx_product_code_upper 
    ON erp_product(UPPER(code));
CREATE INDEX CONCURRENTLY idx_product_price_range 
    ON erp_product(unit_price) WHERE unit_price > 0;

-- Sales Order Performance Indexes
CREATE INDEX CONCURRENTLY idx_salesorder_customer_date 
    ON erp_salesorder(customer_id, order_date DESC);
CREATE INDEX CONCURRENTLY idx_salesorder_status_date 
    ON erp_salesorder(status, order_date DESC);
CREATE INDEX CONCURRENTLY idx_salesorder_total_amount 
    ON erp_salesorder(total_amount DESC) WHERE total_amount > 0;

-- Sales Order Items Composite Index
CREATE INDEX CONCURRENTLY idx_salesorderitem_order_product_qty 
    ON erp_salesorderitem(order_id, product_id, quantity);

-- Purchase Order Performance Indexes
CREATE INDEX CONCURRENTLY idx_purchaseorder_supplier_date 
    ON erp_purchaseorder(supplier_id, order_date DESC);
CREATE INDEX CONCURRENTLY idx_purchaseorder_status_date 
    ON erp_purchaseorder(status, expected_delivery_date);

-- Stock Transaction Indexes
CREATE INDEX CONCURRENTLY idx_stocktransaction_product_date 
    ON erp_stocktransaction(product_id, created_at DESC);
CREATE INDEX CONCURRENTLY idx_stocktransaction_warehouse_type 
    ON erp_stocktransaction(warehouse_id, transaction_type);
CREATE INDEX CONCURRENTLY idx_stocktransaction_date_type 
    ON erp_stocktransaction(created_at DESC, transaction_type);

-- TODO Performance Indexes
CREATE INDEX CONCURRENTLY idx_todos_assignee_status_priority 
    ON todos(assigned_to_id, status, priority) WHERE NOT is_deleted;
CREATE INDEX CONCURRENTLY idx_todos_due_date_status 
    ON todos(due_date, status) WHERE due_date IS NOT NULL AND NOT is_deleted;
CREATE INDEX CONCURRENTLY idx_todos_category_status 
    ON todos(category_id, status) WHERE NOT is_deleted;

-- Quality Control Indexes
CREATE INDEX CONCURRENTLY idx_qualitycontrol_product_date 
    ON erp_qualitycontrol(product_id, control_date DESC);
CREATE INDEX CONCURRENTLY idx_qualitycontrol_status_date 
    ON erp_qualitycontrol(status, control_date DESC);

-- Financial Indexes
CREATE INDEX CONCURRENTLY idx_invoice_customer_date 
    ON erp_invoice(customer_id, invoice_date DESC);
CREATE INDEX CONCURRENTLY idx_invoice_status_date 
    ON erp_invoice(status, due_date);
CREATE INDEX CONCURRENTLY idx_payment_invoice_date 
    ON erp_payment(invoice_id, payment_date DESC);

-- Partial Indexes for Better Performance
CREATE INDEX CONCURRENTLY idx_active_customers 
    ON erp_customer(name) WHERE is_active = true;
CREATE INDEX CONCURRENTLY idx_active_products 
    ON erp_product(name) WHERE is_active = true;
CREATE INDEX CONCURRENTLY idx_pending_orders 
    ON erp_salesorder(order_date DESC) WHERE status = 'pending';
CREATE INDEX CONCURRENTLY idx_overdue_invoices 
    ON erp_invoice(due_date) WHERE status = 'overdue';

-- Update statistics for better query planning
ANALYZE;

-- Create materialized views for complex reports
CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT 
    DATE_TRUNC('month', order_date) as month,
    COUNT(*) as order_count,
    SUM(total_amount) as total_sales,
    AVG(total_amount) as avg_order_value
FROM erp_salesorder 
WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month DESC;

CREATE UNIQUE INDEX idx_mv_monthly_sales_month ON mv_monthly_sales(month);

-- Refresh materialized view daily
-- Add to crontab: 0 1 * * * psql -U context7_user -d context7_erp -c "REFRESH MATERIALIZED VIEW mv_monthly_sales;"
```

### **3. Connection Pool Configuration**
```python
# dashboard_project/db_pool_settings.py
"""
Context7 ERP - Database Connection Pool Configuration
QMS Reference: REC-DB-POOL-CONFIG-250712-001
"""

import os
from .postgresql_settings import *

# PgBouncer Configuration for Production
if not DEBUG:
    DATABASES['default'].update({
        'CONN_MAX_AGE': 0,  # Disable Django connection pooling
        'OPTIONS': {
            **DATABASES['default']['OPTIONS'],
            'host': os.environ.get('PGBOUNCER_HOST', 'localhost'),
            'port': os.environ.get('PGBOUNCER_PORT', '6432'),
        }
    })

# Connection Pool Settings
DATABASE_POOL_SETTINGS = {
    'pool_size': 20,                    # Number of connections to maintain
    'max_overflow': 10,                 # Additional connections when needed
    'pool_timeout': 30,                 # Timeout for getting connection
    'pool_recycle': 3600,               # Recycle connections every hour
    'pool_pre_ping': True,              # Validate connections before use
}

print("🔗 Database Connection Pool Configured")
print(f"   Pool Size: {DATABASE_POOL_SETTINGS['pool_size']}")
print(f"   Max Overflow: {DATABASE_POOL_SETTINGS['max_overflow']}")
print(f"   Pool Timeout: {DATABASE_POOL_SETTINGS['pool_timeout']}s")
```

---

## 🚀 **Multi-Level Caching Strategy**

### **1. Redis Cache Configuration**
```python
# dashboard_project/cache_settings.py
"""
Context7 ERP - Advanced Caching Configuration
QMS Reference: REC-CACHE-CONFIG-250712-001
"""

import os
from .settings import *

# Redis Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
                'socket_timeout': 5,
                'socket_connect_timeout': 5,
            },
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
        'TIMEOUT': 300,  # 5 minutes default
        'VERSION': 1,
        'KEY_PREFIX': 'context7_erp',
    },
    'sessions': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/2",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 86400,  # 24 hours for sessions
        'KEY_PREFIX': 'context7_sessions',
    },
    'api': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{os.environ.get('REDIS_HOST', 'localhost')}:{os.environ.get('REDIS_PORT', '6379')}/3",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 600,  # 10 minutes for API responses
        'KEY_PREFIX': 'context7_api',
    }
}

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Cache Settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 300  # 5 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'context7_middleware'

# Custom Cache Timeouts
CACHE_TIMEOUTS = {
    'customer_list': 600,        # 10 minutes
    'product_list': 1800,        # 30 minutes
    'dashboard_stats': 300,      # 5 minutes
    'reports': 3600,            # 1 hour
    'settings': 86400,          # 24 hours
    'user_permissions': 1800,    # 30 minutes
}

print("🔄 Advanced Caching Configured")
print(f"   Redis Host: {os.environ.get('REDIS_HOST', 'localhost')}")
print(f"   Cache Backends: {len(CACHES)}")
print(f"   Session Cache: Enabled")
```

### **2. Django Cache Framework Enhancement**
```python
# core/cache_utils.py
"""
Context7 ERP - Advanced Cache Utilities
QMS Reference: REC-CACHE-UTILS-250712-001
"""

import json
import hashlib
from functools import wraps
from django.core.cache import cache, caches
from django.conf import settings
from django.utils.encoding import force_str
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """Advanced cache management for Context7 ERP"""
    
    def __init__(self):
        self.default_cache = caches['default']
        self.api_cache = caches.get('api', caches['default'])
        self.timeouts = getattr(settings, 'CACHE_TIMEOUTS', {})
    
    def generate_cache_key(self, prefix, *args, **kwargs):
        """Generate consistent cache keys"""
        key_data = f"{prefix}:{':'.join(map(str, args))}"
        if kwargs:
            key_data += f":{json.dumps(kwargs, sort_keys=True)}"
        
        # Hash long keys
        if len(key_data) > 200:
            key_data = hashlib.md5(key_data.encode()).hexdigest()
        
        return f"context7:{key_data}"
    
    def cache_result(self, key_prefix, timeout=None):
        """Decorator for caching function results"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self.generate_cache_key(key_prefix, *args, **kwargs)
                
                # Try to get from cache
                result = self.default_cache.get(cache_key)
                if result is not None:
                    logger.debug(f"Cache hit: {cache_key}")
                    return result
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                
                # Determine timeout
                cache_timeout = timeout or self.timeouts.get(key_prefix, 300)
                
                # Cache the result
                self.default_cache.set(cache_key, result, cache_timeout)
                logger.debug(f"Cache set: {cache_key} (timeout: {cache_timeout}s)")
                
                return result
            return wrapper
        return decorator
    
    def invalidate_pattern(self, pattern):
        """Invalidate cache keys matching pattern"""
        try:
            # Redis-specific pattern deletion
            if hasattr(self.default_cache, 'delete_pattern'):
                deleted = self.default_cache.delete_pattern(f"*{pattern}*")
                logger.info(f"Invalidated {deleted} cache keys matching: {pattern}")
            else:
                logger.warning("Pattern deletion not supported by cache backend")
        except Exception as e:
            logger.error(f"Cache invalidation failed: {e}")
    
    def get_cache_stats(self):
        """Get cache performance statistics"""
        try:
            # Redis-specific stats
            if hasattr(self.default_cache, '_cache'):
                stats = self.default_cache._cache.get_stats()
                return {
                    'cache_backend': 'Redis',
                    'stats': stats
                }
        except Exception as e:
            logger.error(f"Could not get cache stats: {e}")
        
        return {'cache_backend': 'Unknown', 'stats': {}}

# Global cache manager instance
cache_manager = CacheManager()

# Convenient decorators
def cache_page_result(timeout=300):
    """Cache page results"""
    return cache_manager.cache_result('page', timeout)

def cache_api_result(timeout=600):
    """Cache API results"""
    return cache_manager.cache_result('api', timeout)

def cache_database_query(timeout=1800):
    """Cache database query results"""
    return cache_manager.cache_result('db_query', timeout)

# Cache warming functions
def warm_dashboard_cache():
    """Pre-warm dashboard cache with frequently accessed data"""
    from erp.models import Customer, Product, SalesOrder
    
    logger.info("Warming dashboard cache...")
    
    # Pre-cache dashboard statistics
    cache_manager.default_cache.set(
        'dashboard:customer_count',
        Customer.objects.filter(is_active=True).count(),
        cache_manager.timeouts.get('dashboard_stats', 300)
    )
    
    cache_manager.default_cache.set(
        'dashboard:product_count',
        Product.objects.filter(is_active=True).count(),
        cache_manager.timeouts.get('dashboard_stats', 300)
    )
    
    cache_manager.default_cache.set(
        'dashboard:recent_orders',
        list(SalesOrder.objects.select_related('customer').order_by('-order_date')[:10].values(
            'order_number', 'customer__name', 'total_amount', 'order_date'
        )),
        cache_manager.timeouts.get('dashboard_stats', 300)
    )
    
    logger.info("Dashboard cache warmed successfully")

def warm_product_cache():
    """Pre-warm product cache"""
    from erp.models import Product, ProductCategory
    
    logger.info("Warming product cache...")
    
    # Cache active products
    cache_manager.default_cache.set(
        'products:active_list',
        list(Product.objects.filter(is_active=True).values('id', 'name', 'code', 'unit_price')),
        cache_manager.timeouts.get('product_list', 1800)
    )
    
    # Cache product categories
    cache_manager.default_cache.set(
        'products:categories',
        list(ProductCategory.objects.filter(is_active=True).values('id', 'name')),
        cache_manager.timeouts.get('product_list', 1800)
    )
    
    logger.info("Product cache warmed successfully")

print("🔄 Cache Utilities Loaded")
print("   Features: Advanced caching, pattern invalidation, cache warming")
print("   Backends: Redis multi-database support")
```

### **3. Template Fragment Caching**
```python
# templates/base.html - Add cache tags
{% load cache %}

<!-- Cache navigation for 1 hour -->
{% cache 3600 navigation user.id %}
<nav class="context7-nav">
    {% include 'includes/navigation.html' %}
</nav>
{% endcache %}

<!-- Cache user stats for 5 minutes -->
{% cache 300 user_stats user.id %}
<div class="user-stats">
    {% include 'includes/user_stats.html' %}
</div>
{% endcache %}

<!-- Cache dashboard widgets for 10 minutes -->
{% cache 600 dashboard_widgets user.id %}
<div class="dashboard-widgets">
    {% include 'dashboard/widgets.html' %}
</div>
{% endcache %}
```

---

## 🌐 **CDN Integration**

### **1. CDN Configuration**
```python
# dashboard_project/cdn_settings.py
"""
Context7 ERP - CDN Configuration
QMS Reference: REC-CDN-CONFIG-250712-001
"""

import os
from .settings import *

# CDN Configuration
USE_CDN = os.environ.get('USE_CDN', 'False').lower() == 'true'
CDN_DOMAIN = os.environ.get('CDN_DOMAIN', 'cdn.context7.com')

if USE_CDN and not DEBUG:
    # Static files CDN
    STATIC_URL = f'https://{CDN_DOMAIN}/static/'
    MEDIA_URL = f'https://{CDN_DOMAIN}/media/'
    
    # CDN-specific settings
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'context7-erp-assets')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = CDN_DOMAIN
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',  # 24 hours
    }
    
    # Static files storage
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Image optimization settings
IMAGE_OPTIMIZATION = {
    'FORMATS': ['WEBP', 'JPEG'],
    'QUALITY': 85,
    'PROGRESSIVE': True,
    'OPTIMIZE': True,
}

print(f"🌐 CDN Configuration: {'Enabled' if USE_CDN else 'Disabled'}")
if USE_CDN:
    print(f"   CDN Domain: {CDN_DOMAIN}")
    print(f"   Static URL: {STATIC_URL}")
    print(f"   Media URL: {MEDIA_URL}")
```

### **2. Asset Optimization**
```bash
#!/bin/bash
# optimize_assets.sh
# Context7 ERP Asset Optimization Script

echo "🚀 Optimizing Context7 ERP Assets..."

# Create optimized directories
mkdir -p static/optimized/{css,js,images}

# CSS Optimization
echo "📄 Optimizing CSS..."
for file in static/css/*.css; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file" .css)
        # Minify CSS
        npx cleancss -o "static/optimized/css/${filename}.min.css" "$file"
        # Create gzipped version
        gzip -9 -c "static/optimized/css/${filename}.min.css" > "static/optimized/css/${filename}.min.css.gz"
    fi
done

# JavaScript Optimization
echo "📜 Optimizing JavaScript..."
for file in static/js/*.js; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file" .js)
        # Minify JavaScript
        npx terser "$file" -o "static/optimized/js/${filename}.min.js" --compress --mangle
        # Create gzipped version
        gzip -9 -c "static/optimized/js/${filename}.min.js" > "static/optimized/js/${filename}.min.js.gz"
    fi
done

# Image Optimization
echo "🖼️ Optimizing Images..."
find static/images -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" | while read image; do
    filename=$(basename "$image")
    extension="${filename##*.}"
    name="${filename%.*}"
    
    # Create WebP version
    cwebp -q 85 "$image" -o "static/optimized/images/${name}.webp"
    
    # Optimize original format
    if [[ "$extension" == "jpg" || "$extension" == "jpeg" ]]; then
        jpegoptim --max=85 --dest="static/optimized/images/" "$image"
    elif [[ "$extension" == "png" ]]; then
        optipng -o7 -out "static/optimized/images/$filename" "$image"
    fi
done

echo "✅ Asset optimization completed!"
echo "📊 Optimization Results:"
echo "   CSS files: $(ls static/optimized/css/*.min.css 2>/dev/null | wc -l)"
echo "   JS files: $(ls static/optimized/js/*.min.js 2>/dev/null | wc -l)"
echo "   WebP images: $(ls static/optimized/images/*.webp 2>/dev/null | wc -l)"
```

---

## 📊 **Performance Monitoring**

### **1. Performance Monitoring Middleware**
```python
# core/middleware/performance_middleware.py
"""
Context7 ERP - Performance Monitoring Middleware
QMS Reference: REC-PERFORMANCE-MONITOR-250712-001
"""

import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.conf import settings
from django.db import connection

logger = logging.getLogger('performance')

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """Monitor and log performance metrics"""
    
    def process_request(self, request):
        """Start performance monitoring"""
        request._performance_start = time.time()
        request._db_queries_start = len(connection.queries)
        return None
    
    def process_response(self, request, response):
        """Log performance metrics"""
        if not hasattr(request, '_performance_start'):
            return response
        
        # Calculate metrics
        duration = time.time() - request._performance_start
        db_queries = len(connection.queries) - request._db_queries_start
        
        # Log slow requests
        if duration > 1.0:  # Log requests slower than 1 second
            logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"Duration: {duration:.3f}s, DB queries: {db_queries}"
            )
        
        # Store metrics in cache for monitoring
        metrics_key = f"performance:metrics:{int(time.time() // 60)}"  # Per minute
        current_metrics = cache.get(metrics_key, {
            'requests': 0,
            'total_duration': 0,
            'total_queries': 0,
            'slow_requests': 0
        })
        
        current_metrics['requests'] += 1
        current_metrics['total_duration'] += duration
        current_metrics['total_queries'] += db_queries
        if duration > 1.0:
            current_metrics['slow_requests'] += 1
        
        cache.set(metrics_key, current_metrics, 300)  # Store for 5 minutes
        
        # Add performance headers
        response['X-Response-Time'] = f"{duration:.3f}s"
        response['X-DB-Queries'] = str(db_queries)
        
        return response

class DatabaseQueryLoggingMiddleware(MiddlewareMixin):
    """Log database queries for performance analysis"""
    
    def process_response(self, request, response):
        """Log database queries if in debug mode or slow queries"""
        if settings.DEBUG or hasattr(request, '_log_queries'):
            total_time = sum(float(q['time']) for q in connection.queries)
            
            if total_time > 0.1:  # Log if total query time > 100ms
                slow_queries = [
                    q for q in connection.queries 
                    if float(q['time']) > 0.05  # Individual queries > 50ms
                ]
                
                if slow_queries:
                    logger.warning(
                        f"Slow DB queries for {request.path}: "
                        f"{len(slow_queries)} slow queries, "
                        f"total time: {total_time:.3f}s"
                    )
                    
                    for query in slow_queries:
                        logger.warning(
                            f"Slow query ({query['time']}s): "
                            f"{query['sql'][:200]}..."
                        )
        
        return response

print("📊 Performance Monitoring Middleware Loaded")
print("   Features: Request timing, DB query monitoring, slow request alerts")
```

### **2. Performance Dashboard**
```python
# core/views/performance_views.py
"""
Context7 ERP - Performance Dashboard Views
QMS Reference: REC-PERFORMANCE-DASHBOARD-250712-001
"""

import json
import time
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.db import connection
from django.views.decorators.cache import cache_page

@staff_member_required
def performance_dashboard(request):
    """Performance monitoring dashboard"""
    return render(request, 'core/performance_dashboard.html', {
        'title': 'Performance Dashboard'
    })

@staff_member_required
def performance_metrics_api(request):
    """API endpoint for performance metrics"""
    current_time = int(time.time() // 60)  # Current minute
    metrics_data = []
    
    # Get last 60 minutes of data
    for i in range(60):
        minute = current_time - i
        metrics_key = f"performance:metrics:{minute}"
        metrics = cache.get(metrics_key, {})
        
        if metrics:
            avg_duration = metrics['total_duration'] / metrics['requests'] if metrics['requests'] > 0 else 0
            avg_queries = metrics['total_queries'] / metrics['requests'] if metrics['requests'] > 0 else 0
            
            metrics_data.append({
                'timestamp': minute * 60,
                'requests': metrics['requests'],
                'avg_duration': round(avg_duration, 3),
                'avg_queries': round(avg_queries, 1),
                'slow_requests': metrics.get('slow_requests', 0)
            })
    
    return JsonResponse({
        'metrics': list(reversed(metrics_data))
    })

@staff_member_required
def database_performance_api(request):
    """API endpoint for database performance metrics"""
    with connection.cursor() as cursor:
        # Get database statistics
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_tuples,
                n_dead_tup as dead_tuples
            FROM pg_stat_user_tables 
            ORDER BY n_live_tup DESC 
            LIMIT 20
        """)
        
        table_stats = [
            dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()
        ]
        
        # Get index usage
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                indexname,
                idx_scan,
                idx_tup_read,
                idx_tup_fetch
            FROM pg_stat_user_indexes 
            WHERE idx_scan > 0
            ORDER BY idx_scan DESC 
            LIMIT 20
        """)
        
        index_stats = [
            dict(zip([col[0] for col in cursor.description], row))
            for row in cursor.fetchall()
        ]
        
        # Get slow queries (requires pg_stat_statements extension)
        try:
            cursor.execute("""
                SELECT 
                    query,
                    calls,
                    total_time,
                    mean_time,
                    max_time
                FROM pg_stat_statements 
                WHERE mean_time > 100  -- Queries slower than 100ms
                ORDER BY mean_time DESC 
                LIMIT 10
            """)
            
            slow_queries = [
                dict(zip([col[0] for col in cursor.description], row))
                for row in cursor.fetchall()
            ]
        except:
            slow_queries = []
    
    return JsonResponse({
        'table_stats': table_stats,
        'index_stats': index_stats,
        'slow_queries': slow_queries
    })

@staff_member_required
@cache_page(300)  # Cache for 5 minutes
def cache_performance_api(request):
    """API endpoint for cache performance metrics"""
    cache_stats = {}
    
    # Get Redis stats if available
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()
        
        cache_stats = {
            'redis_version': info.get('redis_version'),
            'used_memory': info.get('used_memory_human'),
            'connected_clients': info.get('connected_clients'),
            'total_commands_processed': info.get('total_commands_processed'),
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0),
            'hit_rate': 0
        }
        
        # Calculate hit rate
        hits = cache_stats['keyspace_hits']
        misses = cache_stats['keyspace_misses']
        if hits + misses > 0:
            cache_stats['hit_rate'] = round((hits / (hits + misses)) * 100, 2)
    
    except Exception as e:
        cache_stats = {'error': str(e)}
    
    return JsonResponse({
        'cache_stats': cache_stats
    })

print("📊 Performance Dashboard Views Loaded")
print("   Features: Real-time metrics, database stats, cache performance")
```

---

## 🎯 **Performance Testing & Benchmarking**

### **1. Load Testing Script**
```python
# tests/performance/load_test.py
"""
Context7 ERP - Load Testing Script
QMS Reference: REC-LOAD-TEST-250712-001
"""

import asyncio
import aiohttp
import time
import json
import statistics
from datetime import datetime

class LoadTester:
    """Asynchronous load testing for Context7 ERP"""
    
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.results = []
        
    async def make_request(self, session, url, method='GET', data=None):
        """Make an async HTTP request and measure response time"""
        start_time = time.time()
        
        try:
            async with session.request(method, url, json=data) as response:
                await response.text()
                duration = time.time() - start_time
                
                return {
                    'url': url,
                    'method': method,
                    'status': response.status,
                    'duration': duration,
                    'success': 200 <= response.status < 300
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'url': url,
                'method': method,
                'status': 0,
                'duration': duration,
                'success': False,
                'error': str(e)
            }
    
    async def run_concurrent_test(self, urls, concurrent_users=10, requests_per_user=10):
        """Run concurrent load test"""
        print(f"🚀 Starting load test:")
        print(f"   URLs: {len(urls)}")
        print(f"   Concurrent users: {concurrent_users}")
        print(f"   Requests per user: {requests_per_user}")
        print(f"   Total requests: {len(urls) * concurrent_users * requests_per_user}")
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            for user in range(concurrent_users):
                for request in range(requests_per_user):
                    for url in urls:
                        task = self.make_request(session, f"{self.base_url}{url}")
                        tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Analyze results
        successful_requests = [r for r in results if r['success']]
        failed_requests = [r for r in results if not r['success']]
        
        if successful_requests:
            response_times = [r['duration'] for r in successful_requests]
            
            analysis = {
                'total_requests': len(results),
                'successful_requests': len(successful_requests),
                'failed_requests': len(failed_requests),
                'success_rate': len(successful_requests) / len(results) * 100,
                'total_duration': total_duration,
                'requests_per_second': len(results) / total_duration,
                'avg_response_time': statistics.mean(response_times),
                'median_response_time': statistics.median(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'p95_response_time': self.percentile(response_times, 95),
                'p99_response_time': self.percentile(response_times, 99),
            }
        else:
            analysis = {
                'total_requests': len(results),
                'successful_requests': 0,
                'failed_requests': len(failed_requests),
                'success_rate': 0,
                'total_duration': total_duration,
                'requests_per_second': 0,
                'error': 'No successful requests'
            }
        
        return analysis, results
    
    def percentile(self, data, p):
        """Calculate percentile"""
        sorted_data = sorted(data)
        index = int((p / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]
    
    def print_results(self, analysis):
        """Print formatted test results"""
        print(f"\n📊 Load Test Results:")
        print(f"{'='*50}")
        print(f"Total Requests: {analysis['total_requests']}")
        print(f"Successful: {analysis['successful_requests']}")
        print(f"Failed: {analysis['failed_requests']}")
        print(f"Success Rate: {analysis['success_rate']:.2f}%")
        print(f"Total Duration: {analysis['total_duration']:.2f}s")
        print(f"Requests/Second: {analysis['requests_per_second']:.2f}")
        
        if 'avg_response_time' in analysis:
            print(f"\n⏱️  Response Times:")
            print(f"Average: {analysis['avg_response_time']:.3f}s")
            print(f"Median: {analysis['median_response_time']:.3f}s")
            print(f"Min: {analysis['min_response_time']:.3f}s")
            print(f"Max: {analysis['max_response_time']:.3f}s")
            print(f"95th percentile: {analysis['p95_response_time']:.3f}s")
            print(f"99th percentile: {analysis['p99_response_time']:.3f}s")
        
        # Performance evaluation
        print(f"\n🎯 Performance Evaluation:")
        avg_time = analysis.get('avg_response_time', float('inf'))
        if avg_time < 0.5:
            print("✅ EXCELLENT - Average response time < 0.5s")
        elif avg_time < 1.0:
            print("✅ GOOD - Average response time < 1.0s")
        elif avg_time < 2.0:
            print("⚠️  ACCEPTABLE - Average response time < 2.0s")
        else:
            print("❌ NEEDS IMPROVEMENT - Average response time > 2.0s")

async def main():
    """Main load testing function"""
    tester = LoadTester()
    
    # Test URLs
    test_urls = [
        '/',
        '/erp/',
        '/erp/customers/',
        '/erp/products/',
        '/erp/sales/orders/',
        '/api/v1/customers/',
        '/api/v1/products/',
    ]
    
    # Run load test
    analysis, results = await tester.run_concurrent_test(
        urls=test_urls,
        concurrent_users=20,
        requests_per_user=5
    )
    
    tester.print_results(analysis)
    
    # Save detailed results
    with open(f'load_test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
        json.dump({
            'analysis': analysis,
            'results': results
        }, f, indent=2, default=str)

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 📋 **Performance Optimization Checklist**

### **Database Optimization**
- [ ] PostgreSQL configuration optimized
- [ ] Performance indexes created
- [ ] Query optimization applied
- [ ] Connection pooling configured
- [ ] Database statistics updated

### **Caching Implementation**
- [ ] Redis cache configured
- [ ] Multi-level caching strategy implemented
- [ ] Template fragment caching applied
- [ ] API response caching enabled
- [ ] Cache warming implemented

### **Frontend Optimization**
- [ ] Static files minified and compressed
- [ ] Images optimized (WebP conversion)
- [ ] CDN integration configured
- [ ] Browser caching headers set
- [ ] Code splitting implemented

### **Performance Monitoring**
- [ ] Performance monitoring middleware enabled
- [ ] Database query logging configured
- [ ] Performance dashboard implemented
- [ ] Real-time metrics collection active
- [ ] Alert system configured

### **Load Testing**
- [ ] Load testing scripts created
- [ ] Performance benchmarks established
- [ ] Stress testing completed
- [ ] Bottlenecks identified and resolved
- [ ] Performance targets achieved

---

## 🎯 **Expected Performance Improvements**

### **Response Time Improvements**
- **Page Load:** 2s → 0.5s (75% improvement)
- **API Calls:** 500ms → 100ms (80% improvement)
- **Database Queries:** 100ms → 25ms (75% improvement)
- **Static Assets:** 1s → 100ms (90% improvement)

### **Scalability Improvements**
- **Concurrent Users:** 100 → 1000+ (10x improvement)
- **Requests/Second:** 50 → 500+ (10x improvement)
- **Cache Hit Rate:** 70% → 98% (40% improvement)
- **Database Connections:** Optimized pooling

### **User Experience**
- **Perceived Performance:** Near-instant responses
- **Global Performance:** CDN reduces latency globally
- **Mobile Performance:** Optimized for mobile devices
- **Reliability:** 99.9% uptime with performance monitoring

---

**🎯 Mission:** Achieve enterprise-grade performance with <1s response times and 1000+ concurrent user support.

**🏆 Success Criteria:** Performance targets met, monitoring active, user experience optimized, scalability validated.

**📞 QMS Reference:** REC-PERFORMANCE-OPT-PHASE2-250712-001 - Enterprise Performance Optimization

---

*Context7 ERP System - Performance Excellence by Design* ⚡ 