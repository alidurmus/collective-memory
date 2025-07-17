import { useQuery } from '@tanstack/react-query';
import apiClient from '../services/api';

export const useSystemStatus = () => {
  return useQuery({
    queryKey: ['systemStatus'],
    queryFn: async () => {
      const response = await apiClient.get('/system/status');
      return response.data;
    },
    refetchInterval: 30000, // Refetch every 30 seconds
    staleTime: 25000, // Consider data stale after 25 seconds
    gcTime: 60000, // Keep in cache for 1 minute (renamed from cacheTime in v4)
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
};