import { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';

// API base URL
const API_BASE_URL = 'http://localhost:8000';

// Main search hook
export const useSearch = () => {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchOptions, setSearchOptions] = useState({
    semantic: false,
    limit: 50,
    fileTypes: [],
    dateRange: null,
    sortBy: 'relevance'
  });
  const [isSearching, setIsSearching] = useState(false);
  const [lastSearchTime, setLastSearchTime] = useState(null);

  const queryClient = useQueryClient();

  // Search mutation
  const searchMutation = useMutation(
    async ({ query, options = {} }) => {
      const searchParams = new URLSearchParams({
        q: query,
        semantic: options.semantic || false,
        limit: options.limit || 50,
        sort_by: options.sortBy || 'relevance'
      });

      if (options.fileTypes && options.fileTypes.length > 0) {
        searchParams.append('file_types', options.fileTypes.join(','));
      }

      const response = await fetch(`${API_BASE_URL}/api/search?${searchParams}`);
      if (!response.ok) {
        throw new Error('Arama işlemi başarısız');
      }
      
      const data = await response.json();
      return data;
    },
    {
      onMutate: () => {
        setIsSearching(true);
      },
      onSuccess: (data) => {
        if (data.success) {
          setSearchResults(data.results || []);
          setLastSearchTime(new Date());
        }
      },
      onError: (error) => {
        console.error('Search error:', error);
        setSearchResults([]);
      },
      onSettled: () => {
        setIsSearching(false);
      }
    }
  );

  // Export mutation
  const exportMutation = useMutation(
    async ({ query, format = 'markdown', filename }) => {
      const response = await fetch(`${API_BASE_URL}/api/search/export`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          format,
          filename
        })
      });

      if (!response.ok) {
        throw new Error('Dışa aktarma başarısız');
      }

      // Download the file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename || `search-results-${Date.now()}.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      return { success: true };
    }
  );

  // Suggestions query
  const { data: suggestions = [] } = useQuery(
    ['searchSuggestions', query],
    async () => {
      if (!query || query.length < 2) return [];

      const response = await fetch(`${API_BASE_URL}/api/search/suggestions?q=${encodeURIComponent(query)}`);
      if (!response.ok) return [];
      
      const data = await response.json();
      return data.success ? data.suggestions : [];
    },
    {
      enabled: query.length >= 2,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    }
  );

  // Search history query
  const { data: searchHistory = [] } = useQuery(
    'searchHistory',
    async () => {
      const response = await fetch(`${API_BASE_URL}/api/search/history`);
      if (!response.ok) return [];
      
      const data = await response.json();
      return data.success ? data.history : [];
    },
    {
      staleTime: 10 * 60 * 1000, // 10 minutes
      cacheTime: 30 * 60 * 1000, // 30 minutes
    }
  );

  // Perform search function
  const performSearch = useCallback((searchQuery = query, options = searchOptions) => {
    if (!searchQuery.trim()) return;
    
    searchMutation.mutate({ 
      query: searchQuery, 
      options 
    });
  }, [query, searchOptions, searchMutation]);

  // Export results function
  const exportResults = useCallback((options = {}) => {
    const filename = options.filename || `search-${query.replace(/\s+/g, '-')}-${Date.now()}.md`;
    
    exportMutation.mutate({
      query,
      format: options.format || 'markdown',
      filename
    });
  }, [query, exportMutation]);

  // Update search options
  const updateSearchOptions = useCallback((newOptions) => {
    setSearchOptions(prev => ({ ...prev, ...newOptions }));
  }, []);

  // Clear search
  const clearSearch = useCallback(() => {
    setQuery('');
    setSearchResults([]);
    setLastSearchTime(null);
  }, []);

  // Load more results (pagination)
  const [canLoadMore, setCanLoadMore] = useState(false);
  const [totalResults, setTotalResults] = useState(0);

  const loadMore = useCallback(() => {
    const currentLimit = searchOptions.limit;
    updateSearchOptions({ limit: currentLimit + 50 });
    performSearch();
  }, [searchOptions.limit, performSearch, updateSearchOptions]);

  return {
    // State
    query,
    setQuery,
    searchResults,
    searchOptions,
    isSearching: searchMutation.isLoading,
    isExporting: exportMutation.isLoading,
    lastSearchTime,
    suggestions,
    searchHistory,
    canLoadMore,
    totalResults,
    
    // Actions
    performSearch,
    exportResults,
    updateSearchOptions,
    clearSearch,
    loadMore,
    
    // Computed
    hasResults: searchResults.length > 0,
    searchStats: {
      resultCount: searchResults.length,
      searchTime: searchMutation.data?.search_time || 0,
      totalFiles: searchMutation.data?.total_files || 0
    },
    
    // Error states
    searchError: searchMutation.error,
    exportError: exportMutation.error
  };
};

// Quick search hook for embedded components
export const useQuickSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const searchMutation = useMutation(
    async (searchQuery) => {
      const response = await fetch(`${API_BASE_URL}/api/search/quick?q=${encodeURIComponent(searchQuery)}`);
      if (!response.ok) {
        throw new Error('Hızlı arama başarısız');
      }
      const data = await response.json();
      return data;
    },
    {
      onMutate: () => setIsLoading(true),
      onSuccess: (data) => {
        setResults(data.success ? data.results?.slice(0, 5) || [] : []);
      },
      onError: (error) => {
        console.error('Quick search error:', error);
        setResults([]);
      },
      onSettled: () => setIsLoading(false)
    }
  );

  const performQuickSearch = useCallback((searchQuery) => {
    if (!searchQuery || searchQuery.length < 2) {
      setResults([]);
      return;
    }
    searchMutation.mutate(searchQuery);
  }, [searchMutation]);

  return {
    query,
    setQuery,
    results,
    isLoading,
    performQuickSearch,
    clearResults: () => setResults([])
  };
};

// Search analytics hook
export const useSearchAnalytics = () => {
  return useQuery(
    'searchAnalytics',
    async () => {
      const response = await fetch(`${API_BASE_URL}/api/analytics/search`);
      if (!response.ok) return null;
      
      const data = await response.json();
      return data.success ? data.analytics : null;
    },
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 15 * 60 * 1000, // 15 minutes
    }
  );
};

// Popular queries hook
export const usePopularQueries = (limit = 10) => {
  return useQuery(
    ['popularQueries', limit],
    async () => {
      const response = await fetch(`${API_BASE_URL}/api/analytics/popular-queries?limit=${limit}`);
      if (!response.ok) return [];
      
      const data = await response.json();
      return data.success ? data.queries : [];
    },
    {
      staleTime: 10 * 60 * 1000, // 10 minutes
      cacheTime: 30 * 60 * 1000, // 30 minutes
    }
  );
}; 