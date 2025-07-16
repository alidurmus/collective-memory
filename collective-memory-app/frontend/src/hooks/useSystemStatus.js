import { useState, useEffect } from 'react';
import { useQuery } from 'react-query';

// API base URL
const API_BASE_URL = 'http://localhost:8000';

// System stats API hook
export const useSystemStats = () => {
  return useQuery(
    'systemStats',
    async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/system/status`);
        if (!response.ok) {
          throw new Error('Sistem durumu alınamadı');
        }
        const data = await response.json();
        return data.success ? data.data : null;
      } catch (error) {
        console.error('System stats error:', error);
        // Return mock data for development
        return {
          file_count: 1245,
          search_count: 3456,
          uptime: '2:34:56',
          status: 'healthy',
          avg_search_time: 89,
          index_size: 50 * 1024 * 1024, // 50MB
          performance: {
            avg_search_time: 89
          }
        };
      }
    },
    {
      refetchInterval: 30000, // Refetch every 30 seconds
      staleTime: 25000, // Consider data stale after 25 seconds
      cacheTime: 60000, // Keep in cache for 1 minute
      retry: 2,
      retryDelay: 1000
    }
  );
};

// System status hook with more details
export const useSystemStatus = () => {
  return useQuery(
    'systemStatus',
    async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/system/stats`);
        if (!response.ok) {
          throw new Error('Sistem istatistikleri alınamadı');
        }
        const data = await response.json();
        return data.success ? data.data : null;
      } catch (error) {
        console.error('System status error:', error);
        // Return mock data for development
        return {
          totalFiles: 1245,
          totalSearches: 3456,
          indexSize: '50.2 MB',
          lastSearchTime: '2 dakika önce',
          watchedDirectories: 3,
          systemHealth: 'healthy',
          uptime: '2:34:56',
          memoryUsage: '145 MB',
          cpuUsage: '12%'
        };
      }
    },
    {
      refetchInterval: 30000,
      staleTime: 25000,
      cacheTime: 60000,
      retry: 2
    }
  );
};

// Real-time stats hook with WebSocket
export const useRealTimeStats = () => {
  const [stats, setStats] = useState({
    connections: 0,
    activeSearches: 0,
    queuedTasks: 0,
    lastActivity: null
  });

  useEffect(() => {
    // Try to connect to WebSocket for real-time updates
    let ws = null;
    
    try {
      ws = new WebSocket('ws://localhost:8000/ws');
      
      ws.onopen = () => {
        console.log('WebSocket connected for real-time stats');
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'stats_update') {
            setStats(prevStats => ({
              ...prevStats,
              ...data.payload
            }));
          }
        } catch (error) {
          console.error('WebSocket message parsing error:', error);
        }
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('WebSocket connection failed:', error);
    }

    // Cleanup on unmount
    return () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  return stats;
};

// Performance metrics hook
export const usePerformanceMetrics = () => {
  return useQuery(
    'performanceMetrics',
    async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/system/performance`);
        if (!response.ok) {
          throw new Error('Performans metrikleri alınamadı');
        }
        const data = await response.json();
        return data.success ? data.data : null;
      } catch (error) {
        console.error('Performance metrics error:', error);
        // Return mock data
        return {
          searchResponseTime: {
            avg: 89,
            min: 12,
            max: 245,
            p95: 156
          },
          indexingSpeed: {
            filesPerMinute: 850,
            bytesPerSecond: 2.5 * 1024 * 1024 // 2.5MB/s
          },
          memoryUsage: {
            current: 145 * 1024 * 1024, // 145MB
            peak: 180 * 1024 * 1024,    // 180MB
            available: 8 * 1024 * 1024 * 1024 // 8GB
          },
          diskUsage: {
            indexSize: 50 * 1024 * 1024,  // 50MB
            totalUsed: 2.5 * 1024 * 1024 * 1024, // 2.5GB
            available: 100 * 1024 * 1024 * 1024  // 100GB
          }
        };
      }
    },
    {
      refetchInterval: 60000, // Refetch every minute
      staleTime: 55000,
      cacheTime: 120000,
      retry: 1
    }
  );
};

// Helper function to format bytes
export const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];
  
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

// Helper function to format duration
export const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  } else {
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  }
}; 