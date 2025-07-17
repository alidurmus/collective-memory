import { useState, useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../services/api';

export const useSearch = () => {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  const searchQuery = useQuery({
    queryKey: ['search', query],
    queryFn: async () => {
      if (!query.trim()) return { results: [], total: 0 };
      
      const response = await apiClient.get('/api/search', { q: query });
      return response.data || { results: [], total: 0 };
    },
    enabled: false, // Manual trigger
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (v4 uses gcTime instead of cacheTime)
  });

  const performSearch = useCallback(async (searchTerm) => {
    if (!searchTerm?.trim()) return;
    
    setQuery(searchTerm);
    setIsSearching(true);
    
    try {
      await searchQuery.refetch();
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsSearching(false);
    }
  }, [searchQuery]);

  const clearSearch = useCallback(() => {
    setQuery('');
    searchQuery.remove();
  }, [searchQuery]);

  return {
    query,
    setQuery,
    results: searchQuery.data?.results || [],
    total: searchQuery.data?.total || 0,
    isLoading: isSearching || searchQuery.isLoading,
    error: searchQuery.error,
    performSearch,
    clearSearch,
    isSearching,
  };
};