import { useQuery } from 'react-query'
import { systemAPI } from '../services/api'

export const useSystemStatus = () => {
  return useQuery(
    'systemStatus',
    systemAPI.getStatus,
    {
      refetchInterval: 30000, // Refresh every 30 seconds
      staleTime: 10000, // Consider data stale after 10 seconds
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    }
  )
}

export const useSystemStats = () => {
  return useQuery(
    'systemStats',
    systemAPI.getStats,
    {
      refetchInterval: 60000, // Refresh every minute
      staleTime: 30000,
      retry: 2,
    }
  )
}

export const useIndexingStatus = () => {
  return useQuery(
    'indexingStatus',
    systemAPI.getIndexingStatus,
    {
      refetchInterval: 5000, // Refresh every 5 seconds during indexing
      staleTime: 2000,
      retry: 1,
    }
  )
} 