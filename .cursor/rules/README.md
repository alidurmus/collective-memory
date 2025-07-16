---
description: Collective Memory Cursor Rules - Cursor.directory optimized
globs: []
alwaysApply: true
---

# 📜 Collective Memory - Cursor Rules (Enhanced)

**Cursor.directory Community Best Practices ile Optimize Edilmiş Kural Sistemi**

Bu sistem, Cursor'ın resmi dokümantasyonuna ve cursor.directory'nin 46.5k+ topluluk deneyimlerine göre optimize edilmiştir.

## 🚀 Cursor.directory Enhancements

### **Yeni Eklenen Kurallar**
- **[performance.md](performance.md)** - Performance optimization patterns *(Auto: all files)*
- **[error-handling.md](error-handling.md)** - Error handling best practices *(Auto: all files)*

### **Optimize Edilmiş Kurallar**
- **[frontend.md](frontend.md)** - Modern React/TypeScript patterns ile güçlendirildi
- **[backend.md](backend.md)** - Advanced Python/Django patterns eklendi
- **[testing.md](testing.md)** - Modern testing strategies ile genişletildi

## 🎯 MDC Format Kural Dosyaları

### 📋 Always Apply Kurallar
- **[general.md](general.md)** - Genel proje kuralları *(Always Active)*
- **[language.md](language.md)** - Dil standartları *(Always Active)*
- **[workflow.md](workflow.md)** - Instruction processing kuralları *(Always Active)*

### 🔧 Auto-Attached Kurallar
- **[backend.md](backend.md)** - Advanced Python/Django kuralları *(Auto: *.py files)*
- **[frontend.md](frontend.md)** - Modern React/TypeScript kuralları *(Auto: *.jsx, *.tsx files)*
- **[context7.md](context7.md)** - Context7 framework kuralları *(Auto: frontend files)*
- **[testing.md](testing.md)** - Comprehensive test kuralları *(Auto: test files)*
- **[performance.md](performance.md)** - Performance optimization *(Auto: all files)*
- **[error-handling.md](error-handling.md)** - Error handling patterns *(Auto: all files)*

### 🛡️ Manual Kurallar
- **[security.md](security.md)** - Güvenlik kuralları *(Manual: @security)*
- **[documentation.md](documentation.md)** - Dokümantasyon kuralları *(Manual: @documentation)*

## 🌟 Cursor.directory Best Practices

### **Frontend Enhancements**
```typescript
// ✅ Modern React Patterns
import { memo, useMemo, useCallback, lazy, Suspense } from 'react';

// Comprehensive TypeScript interfaces
interface KullaniciProps {
  readonly id: string;
  readonly ad: string;
  readonly email?: string;
  readonly aktifMi: boolean;
  readonly roller: readonly string[];
  readonly onKullaniciClick: (id: string) => void;
}

// Performance optimized components
const KullaniciKarti = memo<KullaniciProps>(({ kullanici, onKullaniciClick }) => {
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
```

### **Backend Enhancements**
```python
# ✅ Advanced Python Patterns
from typing import Dict, List, Optional, TypeVar, Generic
from dataclasses import dataclass
import asyncio

@dataclass(frozen=True)
class SearchResult:
    """Immutable search result with comprehensive metadata."""
    id: str
    file_path: str
    content_snippet: str
    relevance_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

# Async performance patterns
async def process_files_batch(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Process files in batches with concurrency control."""
    semaphore = asyncio.Semaphore(10)
    
    async def process_file(path: str) -> Dict[str, Any]:
        async with semaphore:
            # Process file
            return {'path': path, 'processed': True}
    
    return await asyncio.gather(*[process_file(path) for path in file_paths])
```

### **Error Handling Enhancements**
```typescript
// ✅ Advanced Error Boundaries
class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Turkish error logging
    console.error('Uygulama hatası:', error);
    
    // Report to monitoring service
    this.reportError(error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="context7-error-boundary">
          <h2>Beklenmeyen bir hata oluştu</h2>
          <button onClick={() => window.location.reload()}>
            Sayfayı Yenile
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}
```

### **Performance Enhancements**
```python
# ✅ Multi-Level Caching
class CacheOptimizer:
    def multi_level_cache(self, memory_timeout=60, redis_timeout=300):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Level 1: Memory cache
                # Level 2: Redis cache
                # Level 3: Database
                return result
            return wrapper
        return decorator

@cache_optimizer.multi_level_cache()
def get_arama_sonuclari(query: str) -> List[dict]:
    """Get search results with multi-level caching."""
    return FileIndex.objects.filter(search_keywords__icontains=query).values()
```

## 🏗️ MDC Format Yapısı

Her kural dosyası şu yapıya sahiptir:

```mdc
---
description: Kural açıklaması
globs: ["**/*.py", "**/*.js"]  # Otomatik tetiklenme dosyaları
alwaysApply: false             # Her zaman aktif olsun mu?
---

# Kural İçeriği

Cursor.directory best practices ile optimize edilmiş kurallar...

@reference-files.py  # Referans dosyalar
```

## 🎯 Kural Tipleri

### 1. **Always** (Her Zaman Aktif)
```mdc
---
alwaysApply: true
---
```
- Tüm etkileşimlerde aktif
- Genel proje kuralları için
- Örnek: `general.md`, `language.md`

### 2. **Auto Attached** (Otomatik Tetiklenen)
```mdc
---
globs: ["**/*.py", "**/*.js"]
alwaysApply: false
---
```
- Belirli dosyalar açıldığında aktif
- Dosya türü spesifik kurallar için
- Örnek: `backend.md`, `frontend.md`, `performance.md`

### 3. **Manual** (Manuel Çağrılan)
```mdc
---
description: "Manual rule description"
globs: []
alwaysApply: false
---
```
- Sadece `@ruleName` ile çağrıldığında aktif
- Spesifik durumlar için
- Örnek: `@security`, `@documentation`

## 🚀 Kullanım Kuralları

### 1. Her İşlem Öncesi [[memory:3235989]]
```
✅ Hafızayı kontrol et (ilgili bilgileri hatırla)
✅ Cursor.directory patterns uygula
✅ Kuralları oku (.cursor/rules/ kontrol et)
✅ Context oluştur (proje durumunu analiz et)
✅ Paralel işlem planı yap
✅ Test stratejisi belirle
```

### 2. İşlem Sırası [[memory:3190909]]
```
1. ANALIZ → Talimatı parçalara böl
2. BİLGİ TOPLAMA → Terminal komutları ile context oluştur
3. PATTERN UYGULA → Cursor.directory best practices kullan
4. UYGULAMA → Paralel işlem önceliği ile uygula
5. TEST → Sonuçları test et ve doğrula
6. OPTIMIZE → Performance ve error handling uygula
7. RAPOR → Detaylı rapor oluştur
```

### 3. Kalite Kontrol
```
✅ Türkçe UI / İngilizce kod kuralına uygun mu? [[memory:2176195]]
✅ Context7 framework standartlarına uygun mu? [[memory:592593]]
✅ Playwright testleri eklendi mi? [[memory:592592]]
✅ Memory-aware development uygulandı mı? [[memory:3235989]]
✅ Performance optimizations uygulandı mı?
✅ Error handling patterns kullanıldı mı?
✅ Modern React/TypeScript patterns kullanıldı mı?
✅ Advanced Python/Django patterns kullanıldı mı?
```

## 🔧 Kural Yönetimi

### Enhanced Rule Creation
```bash
# Yeni kural dosyası oluştur
touch .cursor/rules/new-rule.md

# Cursor.directory patterns ile MDC formatında başlık ekle
---
description: "New rule with cursor.directory best practices"
globs: ["**/*.ext"]
alwaysApply: false
---

# Advanced Pattern Implementation
Modern community patterns ile optimize edilmiş kurallar...
```

### Rule Performance Optimization
```javascript
// Kural aktivasyon performansı
// Otomatik aktivasyon - dosya türüne göre
// Python dosyası açılınca: backend.md + performance.md + error-handling.md
// React dosyası açılınca: frontend.md + context7.md + performance.md + error-handling.md
```

## 📊 Proje Hafıza Sistemi

### Enhanced Memory Integration
```
[[memory:3235989]] → Her işlem öncesi hafızayı kontrol et
[[memory:2176195]] → Türkçe UI / İngilizce kod standardı
[[memory:592593]]  → Context7 framework kullanımı
[[memory:592592]]  → Playwright testing implementasyonu
[[memory:3190909]] → Paralel işlem workflow'u
[[memory:3247027]] → Console odaklı development
[[memory:3248721]] → Sistem progress monitoring + Cursor.directory optimizations
```

## 🎯 Örnek Kullanım Senaryoları

### Backend Development
```python
# Python dosyası açıldığında otomatik aktif:
# - general.md (Always)
# - language.md (Always)
# - workflow.md (Always)
# - backend.md (Auto: *.py) - Enhanced with async patterns
# - performance.md (Auto: all files) - Multi-level caching
# - error-handling.md (Auto: all files) - Exception handling

@handle_errors(fallback_value=[], reraise=False)
async def process_search(query: str) -> List[Dict]:
    """Arama işlemi - Enhanced with cursor.directory patterns."""
    async with error_context('search_operation'):
        # Multi-level caching
        cache_key = f"search:{hash(query)}"
        
        # Performance monitoring
        with monitor.measure_execution_time('search_files'):
            results = await search_files_async(query)
        
        return {
            'success': True,
            'message': 'Arama başarılı',  # Turkish UI
            'data': results
        }
```

### Frontend Development
```tsx
// React dosyası açıldığında otomatik aktif:
// - general.md (Always)
// - language.md (Always)
// - workflow.md (Always)
// - frontend.md (Auto: *.jsx) - Enhanced with modern patterns
// - context7.md (Auto: frontend files) - Glassmorphism
// - performance.md (Auto: all files) - Memoization
// - error-handling.md (Auto: all files) - Error boundaries

const SearchPanel = memo(() => {
  const { data, error, isLoading, retry } = useAsyncOperation(
    () => fetch('/api/search').then(res => res.json()),
    {
      retryCount: 3,
      onError: (error) => reportError(error)
    }
  );
  
  return (
    <ErrorBoundary fallback={ErrorFallback}>
      <div className="context7-card">
        <h2>Akıllı Arama</h2>  {/* Turkish UI */}
        {error && <ErrorMessage error={error} />}
        {isLoading && <LoadingSpinner />}
        <SearchResults data={data} />
      </div>
    </ErrorBoundary>
  );
});
```

## 🌍 Community Contributions

### Cursor.directory Learning
- **46.5k+ developers** deneyimlerinden öğrenildi
- **Modern patterns** React, TypeScript, Python için
- **Performance optimizations** best practices
- **Error handling** comprehensive patterns
- **Testing strategies** modern approaches

### Integration Benefits
- **Faster development** with proven patterns
- **Better performance** with optimized code
- **Fewer errors** with comprehensive handling
- **Higher quality** with modern practices
- **Community standards** alignment

## 🔍 Troubleshooting

### Enhanced Debugging
1. **Kural aktif olmuyorsa**: MDC format ve glob patterns kontrol et
2. **Performance sorunları**: Multi-level caching ve memoization uygula
3. **Error handling**: Comprehensive error boundaries ve exception handling
4. **Modern patterns**: Cursor.directory best practices referansı

### Performance Monitoring
```typescript
// Performance metrics
const performanceMetrics = {
  'frontend_render_time': '<50ms',
  'backend_response_time': '<100ms',
  'cache_hit_rate': '>80%',
  'error_rate': '<1%'
};
```

---

**🎯 Bu sistem, Cursor'ın resmi standartlarına + Cursor.directory'nin 46.5k+ topluluk deneyimlerine %100 uyumlu!**

**📚 Referanslar**: 
- https://docs.cursor.com/context/rules
- https://cursor.directory/ (46.5k+ community patterns)

**🚀 Enhanced Features:**
- Modern React/TypeScript patterns
- Advanced Python/Django patterns
- Performance optimization strategies
- Comprehensive error handling
- Modern testing approaches 