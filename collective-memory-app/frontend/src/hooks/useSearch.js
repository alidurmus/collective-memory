import { useState, useCallback, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { searchAPI } from '../services/api'
import { useDebounce } from './useDebounce'

export const useSearch = () => {
  const [query, setQuery] = useState('')
  const [searchOptions, setSearchOptions] = useState({
    semantic: false,
    limit: 50,
    offset: 0,
    filters: {}
  })
  const [searchHistory, setSearchHistory] = useState(() => {
    const saved = localStorage.getItem('searchHistory')
    return saved ? JSON.parse(saved) : []
  })

  const debouncedQuery = useDebounce(query, 300)
  const queryClient = useQueryClient()
  const abortControllerRef = useRef()

  // Main search query
  const searchQuery = useQuery(
    ['search', debouncedQuery, searchOptions],
    async () => {
      if (!debouncedQuery.trim()) return { results: [], total: 0 }
      
      // Cancel previous request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
      
      // Create new abort controller
      abortControllerRef.current = new AbortController()

      const searchFunction = searchOptions.semantic 
        ? searchAPI.semanticSearch 
        : searchAPI.search

      return await searchFunction(debouncedQuery, {
        ...searchOptions,
        signal: abortControllerRef.current.signal
      })
    },
    {
      enabled: !!debouncedQuery.trim(),
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 30 * 60 * 1000, // 30 minutes
      keepPreviousData: true,
      onSuccess: (data) => {
        if (debouncedQuery.trim() && data.results.length > 0) {
          addToSearchHistory(debouncedQuery)
        }
      },
      onError: (error) => {
        if (error.name !== 'AbortError') {
          console.error('Search error:', error)
        }
      }
    }
  )

  // Search suggestions
  const suggestionsQuery = useQuery(
    ['suggestions', debouncedQuery],
    () => searchAPI.getSuggestions(debouncedQuery),
    {
      enabled: !!debouncedQuery.trim() && debouncedQuery.length > 2,
      staleTime: 10 * 60 * 1000,
      cacheTime: 20 * 60 * 1000,
    }
  )

  // Export mutation
  const exportMutation = useMutation(
    ({ query, format }) => searchAPI.exportResults(query, format),
    {
      onSuccess: (blob, variables) => {
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `search-results-${Date.now()}.${variables.format === 'markdown' ? 'md' : 'txt'}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }
    }
  )

  // Add query to search history
  const addToSearchHistory = useCallback((searchQuery) => {
    if (!searchQuery.trim()) return

    setSearchHistory(prev => {
      const newHistory = [
        searchQuery,
        ...prev.filter(item => item !== searchQuery)
      ].slice(0, 20) // Keep only last 20 searches

      localStorage.setItem('searchHistory', JSON.stringify(newHistory))
      return newHistory
    })
  }, [])

  // Clear search history
  const clearSearchHistory = useCallback(() => {
    setSearchHistory([])
    localStorage.removeItem('searchHistory')
  }, [])

  // Update search options
  const updateSearchOptions = useCallback((newOptions) => {
    setSearchOptions(prev => ({ ...prev, ...newOptions }))
  }, [])

  // Clear search
  const clearSearch = useCallback(() => {
    setQuery('')
    setSearchOptions(prev => ({ ...prev, offset: 0 }))
    queryClient.removeQueries(['search'])
  }, [queryClient])

  // Load more results
  const loadMore = useCallback(() => {
    if (searchQuery.data && searchQuery.data.results.length < searchQuery.data.total) {
      setSearchOptions(prev => ({ 
        ...prev, 
        offset: prev.offset + prev.limit 
      }))
    }
  }, [searchQuery.data])

  return {
    query,
    setQuery,
    searchOptions,
    updateSearchOptions,
    searchResults: searchQuery.data,
    isSearching: searchQuery.isLoading,
    searchError: searchQuery.error,
    suggestions: suggestionsQuery.data,
    isSuggestionsLoading: suggestionsQuery.isLoading,
    searchHistory,
    addToSearchHistory,
    clearSearchHistory,
    clearSearch,
    loadMore,
    canLoadMore: searchQuery.data && searchQuery.data.results.length < searchQuery.data.total,
    exportResults: exportMutation.mutate,
    isExporting: exportMutation.isLoading
  }
} 