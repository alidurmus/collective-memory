# Collective Memory API Reference

Collective Memory v2.1 REST API dokümantasyonu. Bu API modern web dashboard ve üçüncü parti entegrasyonlar için kullanılabilir.

## 🌐 Base URL

```
Development: http://localhost:5000
Production: https://your-domain.com/api
```

## 🔐 Authentication

Şu anda API public'tir. Gelecek versiyonlarda authentication ekleneceektir.

```http
# Future authentication header
Authorization: Bearer YOUR_API_TOKEN
```

## 📊 Response Format

### Success Response

```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": "SEARCH_FAILED",
    "message": "Search operation failed",
    "details": "Invalid query parameters"
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

## 🔍 Search Endpoints

### POST /search

Ana arama endpoint'i. Basic ve semantic arama destekler.

#### Request

```http
POST /search
Content-Type: application/json

{
  "query": "machine learning algorithms",
  "type": "semantic",
  "max_results": 25,
  "threshold": 0.7,
  "filters": {
    "file_types": ["py", "md", "txt"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "size_range": {
      "min_bytes": 1000,
      "max_bytes": 1000000
    }
  },
  "sort": {
    "field": "relevance",
    "order": "desc"
  }
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | ✅ | - | Arama sorgusu |
| `type` | enum | ❌ | "basic" | Arama türü: "basic", "semantic" |
| `max_results` | integer | ❌ | 50 | Maksimum sonuç sayısı (1-100) |
| `threshold` | float | ❌ | 0.5 | Semantic search için minimum relevance score (0.0-1.0) |
| `filters` | object | ❌ | {} | Arama filtreleri |
| `sort` | object | ❌ | {"field": "relevance", "order": "desc"} | Sıralama seçenekleri |

#### Response

```json
{
  "status": "success",
  "data": {
    "results": [
      {
        "id": "file_123",
        "filename": "machine_learning.py",
        "path": "/projects/ml/algorithms/machine_learning.py",
        "score": 0.95,
        "snippet": "Implementation of various machine learning algorithms...",
        "file_type": "python",
        "size_bytes": 15420,
        "modified_date": "2024-12-15T14:30:00Z",
        "created_date": "2024-12-01T09:15:00Z",
        "metadata": {
          "lines": 412,
          "language": "python",
          "encoding": "utf-8"
        }
      }
    ],
    "total_found": 156,
    "search_time_ms": 45,
    "query_analyzed": {
      "original": "machine learning algorithms",
      "processed": "machine learning algorithm",
      "tokens": ["machine", "learning", "algorithm"],
      "semantic_vector": [0.1, 0.2, 0.3, "..."]
    }
  }
}
```

### GET /search/suggestions

Arama önerileri için autocomplete endpoint'i.

#### Request

```http
GET /search/suggestions?q=mach&limit=10
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | ✅ | - | Partial arama terimi |
| `limit` | integer | ❌ | 10 | Maksimum öneri sayısı (1-20) |

#### Response

```json
{
  "status": "success",
  "data": {
    "suggestions": [
      {
        "text": "machine learning",
        "count": 45,
        "type": "frequent_query"
      },
      {
        "text": "machine learning algorithms",
        "count": 23,
        "type": "frequent_query"
      },
      {
        "text": "machine_learning.py",
        "count": 8,
        "type": "filename"
      }
    ]
  }
}
```

### POST /search/export

Arama sonuçlarını farklı formatlarda export eder.

#### Request

```http
POST /search/export
Content-Type: application/json

{
  "query": "Django models",
  "type": "basic",
  "max_results": 20,
  "format": "markdown",
  "template": "detailed"
}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `format` | enum | ❌ | "markdown" | Export formatı: "markdown", "text", "json", "csv" |
| `template` | enum | ❌ | "standard" | Template türü: "standard", "detailed", "minimal" |

#### Response

```http
Content-Type: text/markdown
Content-Disposition: attachment; filename="search_results_20250115.md"

# Search Results for "Django models"

## Summary
- **Query**: Django models
- **Results**: 15 files found
- **Search time**: 32ms
- **Generated**: 2025-01-15 10:30:00

## Results

### 1. models.py (Score: 0.98)
**Path**: `/project/django_app/models.py`
**Size**: 5.2 KB
**Modified**: 2024-12-10

Django model definitions for the application...

---
```

## 🖥️ System Endpoints

### GET /system/status

Sistem durumu ve sağlık kontrolü.

#### Response

```json
{
  "status": "success",
  "data": {
    "status": "running",
    "uptime_seconds": 3600,
    "version": "2.1.0",
    "components": {
      "search_engine": "healthy",
      "indexer": "healthy", 
      "database": "healthy",
      "file_monitor": "healthy"
    },
    "system_resources": {
      "memory_usage": {
        "used_mb": 185,
        "total_mb": 8192,
        "percentage": 2.3
      },
      "disk_usage": {
        "used_gb": 15.2,
        "total_gb": 512,
        "percentage": 3.0
      },
      "cpu_usage": {
        "percentage": 12.5,
        "load_average": [0.8, 0.6, 0.4]
      }
    }
  }
}
```

### GET /system/stats

Detaylı sistem istatistikleri.

#### Response

```json
{
  "status": "success",
  "data": {
    "indexing": {
      "total_files": 1011,
      "indexed_files": 1009,
      "pending_files": 2,
      "total_size_mb": 245.7,
      "last_indexed": "2025-01-15T10:25:00Z",
      "index_health": "excellent"
    },
    "search": {
      "total_searches": 1547,
      "recent_searches": 23,
      "average_response_time_ms": 78,
      "cache_hit_rate": 0.87
    },
    "file_types": {
      "python": 156,
      "javascript": 89,
      "markdown": 67,
      "text": 234,
      "other": 465
    },
    "performance": {
      "queries_per_minute": 15.3,
      "indexing_rate_files_per_minute": 850,
      "error_rate": 0.001
    }
  }
}
```

### GET /system/indexing

İndexing işlem durumu.

#### Response

```json
{
  "status": "success",
  "data": {
    "status": "indexing",
    "progress": {
      "current": 456,
      "total": 1000,
      "percentage": 45.6
    },
    "current_file": "/path/to/current/file.py",
    "eta_seconds": 120,
    "rate_files_per_second": 14.2,
    "started_at": "2025-01-15T10:20:00Z"
  }
}
```

### POST /system/indexing/start

İndexing işlemini manuel başlatır.

#### Request

```http
POST /system/indexing/start
Content-Type: application/json

{
  "force_reindex": false,
  "paths": ["/path/to/index"],
  "options": {
    "include_hidden": false,
    "max_file_size_mb": 100,
    "file_types": ["py", "js", "md", "txt"]
  }
}
```

#### Response

```json
{
  "status": "success",
  "data": {
    "message": "Indexing started successfully",
    "job_id": "idx_20250115_103000",
    "estimated_files": 1000,
    "estimated_duration_minutes": 12
  }
}
```

### POST /system/indexing/stop

İndexing işlemini durdurur.

#### Response

```json
{
  "status": "success",
  "data": {
    "message": "Indexing stopped successfully",
    "files_processed": 456,
    "time_elapsed_seconds": 180
  }
}
```

### POST /system/cache/clear

Sistem cache'ini temizler.

#### Request

```http
POST /system/cache/clear
Content-Type: application/json

{
  "cache_types": ["search", "index", "all"]
}
```

#### Response

```json
{
  "status": "success",
  "data": {
    "message": "Cache cleared successfully",
    "cleared_items": 1547,
    "memory_freed_mb": 45.2
  }
}
```

## ⚙️ Configuration Endpoints

### GET /config

Sistem konfigürasyonunu getirir.

#### Response

```json
{
  "status": "success",
  "data": {
    "search_settings": {
      "default_type": "semantic",
      "semantic_threshold": 0.7,
      "max_results": 50,
      "cache_enabled": true,
      "cache_ttl_minutes": 30
    },
    "indexing_settings": {
      "auto_index": true,
      "watch_directories": ["/home/user/projects"],
      "file_extensions": ["py", "js", "md", "txt", "json"],
      "max_file_size_mb": 100,
      "exclude_patterns": ["node_modules", ".git", "__pycache__"]
    },
    "system_settings": {
      "log_level": "info",
      "max_memory_mb": 1024,
      "worker_threads": 4,
      "backup_enabled": true
    }
  }
}
```

### PUT /config

Sistem konfigürasyonunu günceller.

#### Request

```http
PUT /config
Content-Type: application/json

{
  "search_settings": {
    "semantic_threshold": 0.8,
    "max_results": 75
  },
  "indexing_settings": {
    "auto_index": false
  }
}
```

#### Response

```json
{
  "status": "success",
  "data": {
    "message": "Configuration updated successfully",
    "restart_required": false,
    "updated_fields": ["search_settings.semantic_threshold", "search_settings.max_results"]
  }
}
```

## 🔌 WebSocket Events

### Connection

```javascript
const socket = io('ws://localhost:5000');

socket.on('connect', () => {
  console.log('Connected to Collective Memory API');
});
```

### Events

#### Indexing Events

```javascript
// İndexing başladığında
socket.on('indexing_started', (data) => {
  console.log('Indexing started:', data);
  // data: { job_id, estimated_files, start_time }
});

// İndexing progress güncellemesi
socket.on('indexing_progress', (data) => {
  console.log('Indexing progress:', data);
  // data: { job_id, current, total, percentage, current_file }
});

// İndexing tamamlandığında
socket.on('indexing_completed', (data) => {
  console.log('Indexing completed:', data);
  // data: { job_id, total_files, duration_seconds, success }
});

// İndexing hatası
socket.on('indexing_error', (data) => {
  console.log('Indexing error:', data);
  // data: { job_id, error_message, failed_file }
});
```

#### Search Events

```javascript
// Arama gerçekleştirildiğinde
socket.on('search_performed', (data) => {
  console.log('Search performed:', data);
  // data: { query, type, results_count, response_time_ms }
});

// Popüler arama güncellenmesi
socket.on('popular_searches_updated', (data) => {
  console.log('Popular searches updated:', data);
  // data: { top_searches }
});
```

#### System Events

```javascript
// Sistem durumu değişikliği
socket.on('system_status_changed', (data) => {
  console.log('System status changed:', data);
  // data: { previous_status, current_status, component }
});

// Performans uyarısı
socket.on('performance_warning', (data) => {
  console.log('Performance warning:', data);
  // data: { metric, value, threshold, recommendation }
});
```

## 📊 Rate Limiting

API rate limiting uygulanmaktadır:

- **Default**: 100 requests/minute per IP
- **Search**: 50 requests/minute per IP
- **Indexing**: 10 requests/minute per IP

Rate limit aşıldığında:

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "details": "Rate limit of 100 requests per minute exceeded"
  },
  "meta": {
    "retry_after_seconds": 60,
    "limit": 100,
    "remaining": 0,
    "reset_time": "2025-01-15T10:31:00Z"
  }
}
```

## 🔍 Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_QUERY` | 400 | Geçersiz arama sorgusu |
| `QUERY_TOO_SHORT` | 400 | Arama sorgusu çok kısa (min 2 karakter) |
| `QUERY_TOO_LONG` | 400 | Arama sorgusu çok uzun (max 500 karakter) |
| `INVALID_PARAMETERS` | 400 | Geçersiz request parametreleri |
| `SEARCH_FAILED` | 500 | Arama işlemi başarısız |
| `INDEXING_IN_PROGRESS` | 409 | İndexing zaten devam ediyor |
| `INDEXING_FAILED` | 500 | İndexing işlemi başarısız |
| `SYSTEM_UNAVAILABLE` | 503 | Sistem geçici olarak kullanılamıyor |
| `RATE_LIMIT_EXCEEDED` | 429 | Rate limit aşıldı |
| `CONFIGURATION_ERROR` | 400 | Geçersiz konfigürasyon |

## 🧪 Testing

### cURL Examples

```bash
# Basic search
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Python functions", "type": "basic"}'

# Semantic search with filters
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning", 
    "type": "semantic",
    "filters": {"file_types": ["py", "md"]},
    "max_results": 10
  }'

# System status
curl http://localhost:5000/system/status

# Start indexing
curl -X POST http://localhost:5000/system/indexing/start \
  -H "Content-Type: application/json" \
  -d '{"force_reindex": false}'
```

### JavaScript Examples

```javascript
// Basic search
const searchResponse = await fetch('/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'React components',
    type: 'semantic',
    max_results: 20
  })
});
const searchData = await searchResponse.json();

// Export search results
const exportResponse = await fetch('/search/export', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'API documentation',
    format: 'markdown'
  })
});
const blob = await exportResponse.blob();
```

## 📝 API Versioning

API versioning şu anda header-based:

```http
Accept: application/vnd.collective-memory.v1+json
```

Gelecek versiyonlar için URL-based versioning planlanmaktadır:

```http
/api/v2/search
```

## 🔮 Upcoming Features

### v2.2 API Enhancements

- **Authentication**: JWT-based authentication
- **Permissions**: Role-based access control
- **Webhooks**: Event-based notifications
- **GraphQL**: Alternative query interface
- **Batch operations**: Multiple file operations
- **Analytics API**: Advanced usage analytics

---

**Bu API dokümantasyonu Collective Memory v2.1 için hazırlanmıştır. Güncellemeler için GitHub repository'sini takip edin.** 