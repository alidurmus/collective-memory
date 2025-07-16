---
description: Error handling patterns ve exception management best practices
globs: ["**/*.py", "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "src/**/*", "api/**/*", "utils/**/*"]
alwaysApply: false
---

# 🛡️ Error Handling Patterns

Cursor.directory community best practices ile optimize edilmiş error handling kuralları.

## 🚨 Frontend Error Handling

### React Error Boundaries
```typescript
// ✅ Comprehensive Error Boundary
interface ErrorBoundaryState {
  readonly hasError: boolean;
  readonly error: Error | null;
  readonly errorInfo: ErrorInfo | null;
  readonly errorId: string;
}

class ErrorBoundary extends Component<
  {
    children: React.ReactNode;
    fallback?: React.ComponentType<{ error: Error; errorId: string }>;
    onError?: (error: Error, errorInfo: ErrorInfo) => void;
  },
  ErrorBoundaryState
> {
  private retryCount = 0;
  private maxRetries = 3;
  
  constructor(props: any) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
      errorId: ''
    };
  }
  
  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    const errorId = `error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    return {
      hasError: true,
      error,
      errorId
    };
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ errorInfo });
    
    // Turkish error logging
    console.error('Uygulama hatası yakalandı:', error);
    console.error('Hata detayları:', errorInfo);
    
    // Report to error tracking service
    if (typeof window !== 'undefined') {
      this.reportError(error, errorInfo);
    }
    
    // Call parent error handler
    this.props.onError?.(error, errorInfo);
  }
  
  private reportError(error: Error, errorInfo: ErrorInfo) {
    const errorReport = {
      message: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      userAgent: navigator.userAgent,
      url: window.location.href,
      timestamp: new Date().toISOString(),
      errorId: this.state.errorId
    };
    
    // Send to error tracking service
    fetch('/api/errors/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(errorReport)
    }).catch(err => {
      console.error('Hata raporu gönderilemedi:', err);
    });
  }
  
  private handleRetry = () => {
    if (this.retryCount < this.maxRetries) {
      this.retryCount++;
      this.setState({
        hasError: false,
        error: null,
        errorInfo: null,
        errorId: ''
      });
    }
  };
  
  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return (
        <FallbackComponent
          error={this.state.error!}
          errorId={this.state.errorId}
          onRetry={this.handleRetry}
          canRetry={this.retryCount < this.maxRetries}
        />
      );
    }
    
    return this.props.children;
  }
}

// Default error fallback with Turkish UI
const DefaultErrorFallback: React.FC<{
  error: Error;
  errorId: string;
  onRetry?: () => void;
  canRetry?: boolean;
}> = ({ error, errorId, onRetry, canRetry = true }) => {
  const [detailsOpen, setDetailsOpen] = useState(false);
  
  return (
    <div className="context7-error-boundary">
      <div className="context7-card error-card">
        <div className="error-icon">
          <svg className="w-12 h-12 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.982 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        
        <h2 className="error-title">Beklenmeyen Bir Hata Oluştu</h2>
        <p className="error-message">
          Üzgünüz, bir şeyler ters gitti. Lütfen sayfayı yenilemeyi deneyin.
        </p>
        
        <div className="error-actions">
          {canRetry && onRetry && (
            <button 
              onClick={onRetry}
              className="context7-button retry-button"
            >
              Tekrar Dene
            </button>
          )}
          
          <button 
            onClick={() => window.location.reload()}
            className="context7-button reload-button"
          >
            Sayfayı Yenile
          </button>
        </div>
        
        <div className="error-details">
          <button
            onClick={() => setDetailsOpen(!detailsOpen)}
            className="details-toggle"
          >
            {detailsOpen ? 'Detayları Gizle' : 'Hata Detayları'}
          </button>
          
          {detailsOpen && (
            <div className="error-details-content">
              <p><strong>Hata ID:</strong> {errorId}</p>
              <p><strong>Hata Mesajı:</strong> {error.message}</p>
              <details>
                <summary>Stack Trace</summary>
                <pre>{error.stack}</pre>
              </details>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
```

### Async Error Handling
```typescript
// ✅ Advanced Async Error Handling
interface AsyncOperationResult<T> {
  readonly data: T | null;
  readonly error: string | null;
  readonly isLoading: boolean;
  readonly retry: () => Promise<void>;
}

function useAsyncOperation<T>(
  operation: () => Promise<T>,
  options: {
    readonly retryCount?: number;
    readonly retryDelay?: number;
    readonly onError?: (error: Error) => void;
  } = {}
): AsyncOperationResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [retryAttempts, setRetryAttempts] = useState(0);
  
  const { retryCount = 3, retryDelay = 1000, onError } = options;
  
  const executeOperation = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await operation();
      setData(result);
      setRetryAttempts(0);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Bilinmeyen hata';
      setError(errorMessage);
      
      // Turkish error notification
      toast.error(`İşlem başarısız: ${errorMessage}`);
      
      onError?.(err instanceof Error ? err : new Error(errorMessage));
      
      // Auto-retry logic
      if (retryAttempts < retryCount) {
        setTimeout(() => {
          setRetryAttempts(prev => prev + 1);
          executeOperation();
        }, retryDelay * Math.pow(2, retryAttempts)); // Exponential backoff
      }
    } finally {
      setIsLoading(false);
    }
  }, [operation, retryAttempts, retryCount, retryDelay, onError]);
  
  const retry = useCallback(async () => {
    setRetryAttempts(0);
    await executeOperation();
  }, [executeOperation]);
  
  useEffect(() => {
    executeOperation();
  }, [executeOperation]);
  
  return {
    data,
    error,
    isLoading,
    retry
  };
}

// Usage example
const SearchComponent: React.FC = () => {
  const { data, error, isLoading, retry } = useAsyncOperation(
    () => fetch('/api/search').then(res => res.json()),
    {
      retryCount: 3,
      retryDelay: 1000,
      onError: (error) => {
        console.error('Arama hatası:', error);
        // Report to error tracking
        reportError(error);
      }
    }
  );
  
  if (isLoading) return <div>Yükleniyor...</div>;
  if (error) return (
    <div className="error-state">
      <p>Hata: {error}</p>
      <button onClick={retry}>Tekrar Dene</button>
    </div>
  );
  
  return <div>{/* Render data */}</div>;
};
```

### Network Error Handling
```typescript
// ✅ Network Error Handling
class NetworkErrorHandler {
  private static instance: NetworkErrorHandler;
  private errorQueue: Array<{ error: Error; timestamp: number }> = [];
  
  static getInstance(): NetworkErrorHandler {
    if (!NetworkErrorHandler.instance) {
      NetworkErrorHandler.instance = new NetworkErrorHandler();
    }
    return NetworkErrorHandler.instance;
  }
  
  async handleNetworkError(error: Error, context: string): Promise<void> {
    // Add to error queue
    this.errorQueue.push({
      error,
      timestamp: Date.now()
    });
    
    // Determine error type
    const errorType = this.categorizeError(error);
    
    // Turkish error messages
    const turkishMessages = {
      network: 'Ağ bağlantısı hatası. Lütfen internet bağlantınızı kontrol edin.',
      timeout: 'İstek zaman aşımına uğradı. Lütfen tekrar deneyin.',
      server: 'Sunucu hatası. Lütfen daha sonra tekrar deneyin.',
      unauthorized: 'Yetkilendirme hatası. Lütfen giriş yapın.',
      forbidden: 'Bu işlem için yetkiniz yok.',
      notFound: 'Aradığınız kaynak bulunamadı.',
      validation: 'Gönderilen veriler geçersiz.',
      generic: 'Bir hata oluştu. Lütfen tekrar deneyin.'
    };
    
    const message = turkishMessages[errorType] || turkishMessages.generic;
    
    // Show user-friendly error
    toast.error(message);
    
    // Report to monitoring service
    await this.reportError(error, context, errorType);
  }
  
  private categorizeError(error: Error): string {
    if (error.name === 'NetworkError' || error.message.includes('fetch')) {
      return 'network';
    }
    
    if (error.name === 'TimeoutError') {
      return 'timeout';
    }
    
    if (error.message.includes('500')) {
      return 'server';
    }
    
    if (error.message.includes('401')) {
      return 'unauthorized';
    }
    
    if (error.message.includes('403')) {
      return 'forbidden';
    }
    
    if (error.message.includes('404')) {
      return 'notFound';
    }
    
    if (error.message.includes('400')) {
      return 'validation';
    }
    
    return 'generic';
  }
  
  private async reportError(error: Error, context: string, type: string): Promise<void> {
    try {
      await fetch('/api/errors/report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          error: {
            message: error.message,
            stack: error.stack,
            name: error.name
          },
          context,
          type,
          timestamp: new Date().toISOString(),
          userAgent: navigator.userAgent,
          url: window.location.href
        })
      });
    } catch (reportError) {
      console.error('Hata raporu gönderilemedi:', reportError);
    }
  }
  
  getErrorStatistics(): { errorCount: number; lastError: Date | null } {
    return {
      errorCount: this.errorQueue.length,
      lastError: this.errorQueue.length > 0 
        ? new Date(this.errorQueue[this.errorQueue.length - 1].timestamp)
        : null
    };
  }
}

// HTTP client with error handling
class HTTPClient {
  private errorHandler = NetworkErrorHandler.getInstance();
  
  async get<T>(url: string, options: RequestInit = {}): Promise<T> {
    return this.request<T>(url, { ...options, method: 'GET' });
  }
  
  async post<T>(url: string, data: any, options: RequestInit = {}): Promise<T> {
    return this.request<T>(url, {
      ...options,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      body: JSON.stringify(data)
    });
  }
  
  private async request<T>(url: string, options: RequestInit): Promise<T> {
    try {
      const response = await fetch(url, {
        ...options,
        signal: AbortSignal.timeout(10000) // 10 second timeout
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      await this.errorHandler.handleNetworkError(
        error instanceof Error ? error : new Error('Unknown error'),
        `${options.method} ${url}`
      );
      throw error;
    }
  }
}
```

## 🐍 Backend Error Handling

### Python Exception Handling
```python
# ✅ Comprehensive Exception Handling
import logging
import traceback
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass
from contextlib import contextmanager

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ErrorContext:
    """Error context information."""
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    operation: Optional[str] = None
    metadata: Dict[str, Any] = None

class CollectiveMemoryError(Exception):
    """Base exception for Collective Memory application."""
    
    def __init__(self, 
                 message: str, 
                 severity: ErrorSeverity = ErrorSeverity.MEDIUM,
                 context: Optional[ErrorContext] = None,
                 original_error: Optional[Exception] = None):
        super().__init__(message)
        self.severity = severity
        self.context = context or ErrorContext()
        self.original_error = original_error
        self.timestamp = datetime.now()
        self.error_id = f"error_{int(time.time())}_{random.randint(1000, 9999)}"

class ValidationError(CollectiveMemoryError):
    """Validation error with Turkish message."""
    
    def __init__(self, field: str, message: str, value: Any = None):
        turkish_message = f"Doğrulama hatası - {field}: {message}"
        super().__init__(turkish_message, ErrorSeverity.MEDIUM)
        self.field = field
        self.value = value

class DatabaseError(CollectiveMemoryError):
    """Database operation error."""
    
    def __init__(self, operation: str, original_error: Exception):
        turkish_message = f"Veritabanı hatası - {operation}: {str(original_error)}"
        super().__init__(
            turkish_message, 
            ErrorSeverity.HIGH,
            original_error=original_error
        )
        self.operation = operation

class SearchError(CollectiveMemoryError):
    """Search operation error."""
    
    def __init__(self, query: str, original_error: Exception):
        turkish_message = f"Arama hatası - Sorgu: '{query}': {str(original_error)}"
        super().__init__(
            turkish_message,
            ErrorSeverity.MEDIUM,
            original_error=original_error
        )
        self.query = query

# Error handler decorator
def handle_errors(
    fallback_value: Any = None,
    reraise: bool = True,
    log_errors: bool = True
):
    """Decorator for comprehensive error handling."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CollectiveMemoryError as e:
                if log_errors:
                    logger.error(f"Uygulama hatası: {e}", extra={
                        'error_id': e.error_id,
                        'severity': e.severity.value,
                        'context': e.context.__dict__
                    })
                
                if reraise:
                    raise
                return fallback_value
            
            except Exception as e:
                # Convert to application error
                app_error = CollectiveMemoryError(
                    f"Beklenmeyen hata: {str(e)}",
                    ErrorSeverity.HIGH,
                    original_error=e
                )
                
                if log_errors:
                    logger.error(f"Beklenmeyen hata: {e}", extra={
                        'error_id': app_error.error_id,
                        'traceback': traceback.format_exc()
                    })
                
                if reraise:
                    raise app_error
                return fallback_value
        
        return wrapper
    return decorator

# Context manager for error handling
@contextmanager
def error_context(operation: str, user_id: str = None):
    """Context manager for error tracking."""
    context = ErrorContext(
        user_id=user_id,
        operation=operation,
        request_id=getattr(threading.current_thread(), 'request_id', None)
    )
    
    try:
        yield context
    except Exception as e:
        if isinstance(e, CollectiveMemoryError):
            e.context = context
        else:
            # Convert to application error with context
            app_error = CollectiveMemoryError(
                f"Hata - {operation}: {str(e)}",
                ErrorSeverity.HIGH,
                context=context,
                original_error=e
            )
            raise app_error from e
```

### Django Error Handling
```python
# ✅ Django Error Handling
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """Custom exception handler with Turkish responses."""
    response = exception_handler(exc, context)
    
    # Turkish error messages
    turkish_messages = {
        'ValidationError': 'Doğrulama hatası',
        'PermissionDenied': 'Bu işlem için yetkiniz yok',
        'NotFound': 'Aradığınız kaynak bulunamadı',
        'MethodNotAllowed': 'Bu işlem desteklenmiyor',
        'Throttled': 'Çok fazla istek gönderdiniz, lütfen bekleyin',
        'AuthenticationFailed': 'Kimlik doğrulama başarısız',
        'ParseError': 'Gönderilen veri formatı hatalı'
    }
    
    if response is not None:
        error_type = exc.__class__.__name__
        turkish_message = turkish_messages.get(error_type, 'Bir hata oluştu')
        
        custom_response_data = {
            'success': False,
            'message': turkish_message,
            'error_type': error_type,
            'details': response.data if isinstance(response.data, dict) else str(response.data),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add error ID for tracking
        if hasattr(exc, 'error_id'):
            custom_response_data['error_id'] = exc.error_id
        
        response.data = custom_response_data
    
    return response

class ErrorHandlingMixin:
    """Mixin for consistent error handling in views."""
    
    def handle_exception(self, exc):
        """Handle exceptions with Turkish messages."""
        if isinstance(exc, CollectiveMemoryError):
            return Response({
                'success': False,
                'message': str(exc),
                'error_id': exc.error_id,
                'severity': exc.severity.value,
                'timestamp': exc.timestamp.isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return super().handle_exception(exc)

class SearchAPIView(ErrorHandlingMixin, generics.ListAPIView):
    """Search API with comprehensive error handling."""
    
    @handle_errors(fallback_value=[], reraise=False)
    def get_queryset(self):
        """Get search results with error handling."""
        query = self.request.query_params.get('q', '')
        
        if not query:
            raise ValidationError('q', 'Arama sorgusu boş olamaz')
        
        if len(query) < 2:
            raise ValidationError('q', 'Arama sorgusu en az 2 karakter olmalıdır')
        
        try:
            with error_context('search_operation', self.request.user.id):
                return FileIndex.objects.filter(
                    search_keywords__icontains=query
                ).select_related('created_by')
        except Exception as e:
            raise SearchError(query, e)
    
    def list(self, request, *args, **kwargs):
        """List with error handling."""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            
            return Response({
                'success': True,
                'message': 'Arama başarılı',
                'data': serializer.data,
                'count': len(serializer.data)
            })
        
        except CollectiveMemoryError as e:
            return Response({
                'success': False,
                'message': str(e),
                'error_id': e.error_id,
                'error_type': e.__class__.__name__
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Beklenmeyen arama hatası: {e}", exc_info=True)
            
            return Response({
                'success': False,
                'message': 'Arama sırasında beklenmeyen bir hata oluştu',
                'error_type': 'UnexpectedError'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### Error Monitoring & Reporting
```python
# ✅ Error Monitoring System
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

class ErrorMonitor:
    """Error monitoring and reporting system."""
    
    def __init__(self):
        self.setup_sentry()
        self.setup_logging()
    
    def setup_sentry(self):
        """Setup Sentry for error tracking."""
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )
        
        sentry_sdk.init(
            dsn="YOUR_SENTRY_DSN",
            integrations=[
                DjangoIntegration(),
                sentry_logging
            ],
            traces_sample_rate=1.0,
            send_default_pii=True
        )
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                    'style': '{',
                },
                'simple': {
                    'format': '{levelname} {message}',
                    'style': '{',
                },
            },
            'handlers': {
                'file': {
                    'level': 'ERROR',
                    'class': 'logging.FileHandler',
                    'filename': 'errors.log',
                    'formatter': 'verbose',
                },
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },
            },
            'loggers': {
                'collective_memory': {
                    'handlers': ['file', 'console'],
                    'level': 'INFO',
                    'propagate': True,
                },
            },
        })
    
    def report_error(self, error: Exception, context: Dict[str, Any] = None):
        """Report error to monitoring service."""
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_extra(key, value)
            
            scope.set_tag("error_type", error.__class__.__name__)
            
            if hasattr(error, 'severity'):
                scope.set_level(error.severity.value)
            
            sentry_sdk.capture_exception(error)
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics."""
        # Implementation depends on your monitoring setup
        return {
            'hata_sayisi': 0,
            'son_hata_tarihi': None,
            'en_sik_hatalar': []
        }

# Global error monitor instance
error_monitor = ErrorMonitor()
```

## 🔧 Error Handling Best Practices

### Guidelines
```python
# ✅ Error Handling Best Practices
# 1. Always use specific exceptions
def validate_file_upload(file_data):
    """Validate file upload with specific errors."""
    if not file_data:
        raise ValidationError('file', 'Dosya seçilmedi')
    
    if file_data.size > 10 * 1024 * 1024:  # 10MB
        raise ValidationError('file', 'Dosya boyutu 10MB\'dan büyük olamaz')
    
    allowed_types = ['image/jpeg', 'image/png', 'text/plain']
    if file_data.content_type not in allowed_types:
        raise ValidationError('file', 'Desteklenmeyen dosya türü')

# 2. Use context managers for cleanup
@contextmanager
def database_transaction():
    """Database transaction with error handling."""
    try:
        transaction.set_autocommit(False)
        yield
        transaction.commit()
    except Exception as e:
        transaction.rollback()
        raise DatabaseError('transaction', e)
    finally:
        transaction.set_autocommit(True)

# 3. Implement circuit breaker pattern
class CircuitBreaker:
    """Circuit breaker for external service calls."""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        """Call function with circuit breaker."""
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'half-open'
            else:
                raise Exception('Servis şu anda kullanılamıyor (circuit breaker open)')
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        """Handle successful call."""
        self.failure_count = 0
        self.state = 'closed'
    
    def on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'open'
```

@utils/errors.py
@handlers/errorBoundary.tsx
@services/errorMonitor.ts
@middleware/errorHandler.py 