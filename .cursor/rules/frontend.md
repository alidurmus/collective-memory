---
description: Modern React/TypeScript/Next.js geliştirme kuralları
globs: ["**/*.tsx", "**/*.jsx", "**/*.ts", "frontend/**/*.js", "components/**/*", "pages/**/*", "hooks/**/*", "utils/**/*"]
alwaysApply: false
---

# ⚛️ Modern React/TypeScript Kuralları

Cursor.directory community best practices ile optimize edilmiş modern React geliştirme kuralları.

## 🎯 TypeScript-First Development

### Interface Definitions
```typescript
// ✅ Comprehensive Interface Design
interface KullaniciProps {
  readonly id: string;
  readonly ad: string;
  readonly email?: string;
  readonly aktifMi: boolean;
  readonly roller: readonly string[];
  readonly onKullaniciClick: (id: string) => void;
  readonly onKullaniciUpdate?: (kullanici: KullaniciData) => Promise<void>;
}

interface ApiResponse<T> {
  readonly success: boolean;
  readonly data: T;
  readonly message?: string;
  readonly error?: string;
  readonly timestamp: string;
}

interface SearchState {
  readonly query: string;
  readonly results: readonly SearchResult[];
  readonly isLoading: boolean;
  readonly error: string | null;
  readonly filters: readonly string[];
}
```

### Advanced Type Utilities
```typescript
// ✅ Utility Types for Complex Scenarios
type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Turkish UI with English types
type TurkishLabels = {
  readonly [K in keyof typeof UI_LABELS]: string;
};

const UI_LABELS = {
  dashboard: "Ana Panel",
  search: "Akıllı Arama",
  analytics: "Analitikler",
  settings: "Ayarlar",
  profile: "Profil",
  logout: "Çıkış Yap"
} as const;

// Type-safe form handling
type FormData<T> = {
  readonly [K in keyof T]: {
    readonly value: T[K];
    readonly error?: string;
    readonly touched: boolean;
  };
};
```

## 🔥 Modern React Patterns

### Custom Hooks with TypeScript
```typescript
// ✅ Advanced Custom Hooks
interface UseApiOptions<T> {
  readonly initialData?: T;
  readonly enabled?: boolean;
  readonly refetchInterval?: number;
  readonly onSuccess?: (data: T) => void;
  readonly onError?: (error: Error) => void;
}

function useApi<T>(
  url: string,
  options: UseApiOptions<T> = {}
): {
  readonly data: T | undefined;
  readonly isLoading: boolean;
  readonly error: Error | null;
  readonly refetch: () => Promise<void>;
} {
  const [data, setData] = useState<T | undefined>(options.initialData);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  const refetch = useCallback(async () => {
    if (!options.enabled) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }
      
      const result = await response.json();
      setData(result);
      options.onSuccess?.(result);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      options.onError?.(error);
    } finally {
      setIsLoading(false);
    }
  }, [url, options.enabled]);
  
  useEffect(() => {
    refetch();
  }, [refetch]);
  
  return { data, isLoading, error, refetch };
}

// Turkish UI Search Hook
function useArama(initialQuery = '') {
  const [query, setQuery] = useState(initialQuery);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  
  const debouncedQuery = useDebounce(query, 300);
  
  const performSearch = useCallback(async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }
    
    setIsLoading(true);
    try {
      const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      
      if (data.success) {
        setResults(data.data);
      } else {
        console.error('Arama hatası:', data.message);
      }
    } catch (error) {
      console.error('Arama API hatası:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);
  
  useEffect(() => {
    performSearch(debouncedQuery);
  }, [debouncedQuery, performSearch]);
  
  return {
    query,
    setQuery,
    results,
    isLoading,
    performSearch
  };
}
```

### Component Composition Patterns
```typescript
// ✅ Compound Components Pattern
interface DashboardContextType {
  readonly activeTab: string;
  readonly setActiveTab: (tab: string) => void;
  readonly kullaniciData: KullaniciData | null;
}

const DashboardContext = createContext<DashboardContextType | null>(null);

export const Dashboard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeTab, setActiveTab] = useState("ana-panel");
  const { data: kullaniciData } = useApi<KullaniciData>('/api/user');
  
  const contextValue = useMemo(() => ({
    activeTab,
    setActiveTab,
    kullaniciData
  }), [activeTab, kullaniciData]);
  
  return (
    <DashboardContext.Provider value={contextValue}>
      <div className="context7-dashboard">
        {children}
      </div>
    </DashboardContext.Provider>
  );
};

Dashboard.Header = function DashboardHeader() {
  const context = useContext(DashboardContext);
  if (!context) throw new Error('DashboardHeader must be used within Dashboard');
  
  return (
    <header className="context7-header">
      <h1>Hoş Geldiniz, {context.kullaniciData?.ad}</h1>
    </header>
  );
};

Dashboard.Navigation = function DashboardNavigation() {
  const context = useContext(DashboardContext);
  if (!context) throw new Error('DashboardNavigation must be used within Dashboard');
  
  return (
    <nav className="context7-nav">
      <button 
        className={`context7-nav-button ${context.activeTab === 'ana-panel' ? 'active' : ''}`}
        onClick={() => context.setActiveTab('ana-panel')}
      >
        Ana Panel
      </button>
      <button 
        className={`context7-nav-button ${context.activeTab === 'arama' ? 'active' : ''}`}
        onClick={() => context.setActiveTab('arama')}
      >
        Akıllı Arama
      </button>
    </nav>
  );
};
```

## 🚀 Performance Optimization

### Memoization Strategies
```typescript
// ✅ Strategic Memoization
const SearchResults = memo<{
  readonly results: SearchResult[];
  readonly onResultClick: (result: SearchResult) => void;
}>(({ results, onResultClick }) => {
  // Heavy computation memoization
  const processedResults = useMemo(() => {
    return results.map(result => ({
      ...result,
      highlightedContent: highlightSearchTerms(result.content, searchQuery),
      formattedDate: formatTurkishDate(result.lastModified)
    }));
  }, [results, searchQuery]);
  
  return (
    <div className="context7-search-results">
      {processedResults.map(result => (
        <SearchResultItem
          key={result.id}
          result={result}
          onClick={onResultClick}
        />
      ))}
    </div>
  );
});

// Callback memoization
const SearchPanel: React.FC = () => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState<string[]>([]);
  
  const handleSearch = useCallback((newQuery: string) => {
    setQuery(newQuery);
    // Analytics tracking
    analytics.track('search_performed', { query: newQuery });
  }, []);
  
  const handleFilterChange = useCallback((filter: string) => {
    setFilters(prev => 
      prev.includes(filter) 
        ? prev.filter(f => f !== filter)
        : [...prev, filter]
    );
  }, []);
  
  return (
    <div className="context7-search-panel">
      <SearchInput onSearch={handleSearch} />
      <SearchFilters filters={filters} onChange={handleFilterChange} />
      <SearchResults results={results} onResultClick={handleResultClick} />
    </div>
  );
};
```

### Code Splitting & Lazy Loading
```typescript
// ✅ Strategic Code Splitting
const LazyAnalytics = lazy(() => import('./components/Analytics'));
const LazySettings = lazy(() => import('./components/Settings'));

function App() {
  return (
    <Router>
      <Suspense fallback={<div className="context7-loading">Yükleniyor...</div>}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/arama" element={<SearchPage />} />
          <Route path="/analitikler" element={<LazyAnalytics />} />
          <Route path="/ayarlar" element={<LazySettings />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

// Bundle optimization
const ChunkedComponent = memo(({ data }: { data: LargeDataType }) => {
  return (
    <div className="context7-large-component">
      {data.map(item => (
        <HeavyComponent key={item.id} item={item} />
      ))}
    </div>
  );
});
```

## 🛡️ Error Handling & Boundaries

### Error Boundaries
```typescript
// ✅ Comprehensive Error Handling
interface ErrorBoundaryState {
  readonly hasError: boolean;
  readonly error: Error | null;
  readonly errorInfo: ErrorInfo | null;
}

class ErrorBoundary extends Component<
  { children: React.ReactNode; fallback?: React.ComponentType<{ error: Error }> },
  ErrorBoundaryState
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }
  
  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.setState({ errorInfo });
    
    // Turkish error logging
    console.error('Uygulama hatası:', error);
    console.error('Hata detayları:', errorInfo);
    
    // Error tracking
    if (typeof window !== 'undefined') {
      analytics.track('error_boundary_triggered', {
        error: error.message,
        stack: error.stack,
        componentStack: errorInfo.componentStack
      });
    }
  }
  
  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return <FallbackComponent error={this.state.error!} />;
    }
    
    return this.props.children;
  }
}

const DefaultErrorFallback: React.FC<{ error: Error }> = ({ error }) => (
  <div className="context7-error-boundary">
    <h2>Beklenmeyen bir hata oluştu</h2>
    <details>
      <summary>Hata detayları</summary>
      <pre>{error.message}</pre>
    </details>
    <button onClick={() => window.location.reload()}>
      Sayfayı Yenile
    </button>
  </div>
);
```

### Async Error Handling
```typescript
// ✅ Async Operations with Error Handling
function useAsyncOperation<T>(
  operation: () => Promise<T>
): {
  readonly execute: () => Promise<T | null>;
  readonly isLoading: boolean;
  readonly error: string | null;
} {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const execute = useCallback(async (): Promise<T | null> => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await operation();
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Bilinmeyen hata';
      setError(errorMessage);
      
      // Turkish error notification
      toast.error(`İşlem başarısız: ${errorMessage}`);
      
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [operation]);
  
  return { execute, isLoading, error };
}
```

## 🧪 Testing Patterns

### Component Testing
```typescript
// ✅ Comprehensive Component Testing
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { SearchPanel } from './SearchPanel';

describe('SearchPanel', () => {
  const mockOnSearch = vi.fn();
  
  beforeEach(() => {
    mockOnSearch.mockClear();
  });
  
  it('renders Turkish UI correctly', () => {
    render(<SearchPanel onSearch={mockOnSearch} />);
    
    expect(screen.getByPlaceholderText('Akıllı arama yap...')).toBeInTheDocument();
    expect(screen.getByText('Ara')).toBeInTheDocument();
    expect(screen.getByText('Filtreler')).toBeInTheDocument();
  });
  
  it('handles search with Turkish characters', async () => {
    render(<SearchPanel onSearch={mockOnSearch} />);
    
    const searchInput = screen.getByPlaceholderText('Akıllı arama yap...');
    fireEvent.change(searchInput, { target: { value: 'çalışma belgesi' } });
    
    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith('çalışma belgesi');
    });
  });
  
  it('applies Context7 styling', () => {
    render(<SearchPanel onSearch={mockOnSearch} />);
    
    const panel = screen.getByRole('search');
    expect(panel).toHaveClass('context7-search-panel');
    
    const button = screen.getByRole('button', { name: /ara/i });
    expect(button).toHaveClass('context7-button');
  });
});
```

### Hook Testing
```typescript
// ✅ Custom Hook Testing
import { renderHook, act } from '@testing-library/react';
import { useArama } from './useArama';

describe('useArama', () => {
  it('performs search with Turkish query', async () => {
    const { result } = renderHook(() => useArama());
    
    act(() => {
      result.current.setQuery('django projeleri');
    });
    
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.results).toHaveLength(expect.any(Number));
    });
  });
});
```

## 🔧 Build & Development Tools

### Vite Configuration
```typescript
// ✅ Optimized Vite Config
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@components': resolve(__dirname, './src/components'),
      '@hooks': resolve(__dirname, './src/hooks'),
      '@utils': resolve(__dirname, './src/utils'),
      '@types': resolve(__dirname, './src/types')
    }
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@headlessui/react', '@heroicons/react']
        }
      }
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
});
```

### ESLint Configuration
```json
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "react/prop-types": "off",
    "@typescript-eslint/no-unused-vars": "error",
    "prefer-const": "error",
    "react-hooks/exhaustive-deps": "warn",
    "react/jsx-no-target-blank": "error"
  }
}
```

@components/Dashboard.tsx
@hooks/useApi.ts
@utils/turkishHelpers.ts
@types/api.ts 