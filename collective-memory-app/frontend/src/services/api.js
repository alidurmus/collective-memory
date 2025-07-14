import axios from 'axios'

// Base API configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Search API
export const searchAPI = {
  // Basic search
  search: async (query, options = {}) => {
    const params = {
      q: query,
      limit: options.limit || 50,
      offset: options.offset || 0,
      ...options
    }
    const response = await api.get('/search', { params })
    return response.data
  },

  // Semantic search
  semanticSearch: async (query, options = {}) => {
    const params = {
      q: query,
      semantic: true,
      limit: options.limit || 50,
      offset: options.offset || 0,
      ...options
    }
    const response = await api.get('/search', { params })
    return response.data
  },

  // Get search suggestions
  getSuggestions: async (query) => {
    const response = await api.get('/search/suggestions', {
      params: { q: query }
    })
    return response.data
  },

  // Advanced search with filters
  advancedSearch: async (filters) => {
    const response = await api.post('/search/advanced', filters)
    return response.data
  },

  // Export search results
  exportResults: async (query, format = 'markdown') => {
    const response = await api.post('/search/export', {
      query,
      format
    }, {
      responseType: 'blob'
    })
    return response.data
  }
}

// System API
export const systemAPI = {
  // Get system status
  getStatus: async () => {
    const response = await api.get('/system/status')
    return response.data
  },

  // Get statistics
  getStats: async () => {
    const response = await api.get('/system/stats')
    return response.data
  },

  // Get indexing status
  getIndexingStatus: async () => {
    const response = await api.get('/system/indexing')
    return response.data
  },

  // Trigger reindexing
  reindex: async (path = null) => {
    const response = await api.post('/system/reindex', { path })
    return response.data
  },

  // Clear cache
  clearCache: async () => {
    const response = await api.post('/system/cache/clear')
    return response.data
  },

  // Get logs
  getLogs: async (level = 'info', limit = 100) => {
    const response = await api.get('/system/logs', {
      params: { level, limit }
    })
    return response.data
  }
}

// Files API
export const filesAPI = {
  // Get file tree
  getFileTree: async (path = '') => {
    const response = await api.get('/files/tree', {
      params: { path }
    })
    return response.data
  },

  // Get file content
  getFileContent: async (filePath) => {
    const response = await api.get('/files/content', {
      params: { path: filePath }
    })
    return response.data
  },

  // Get file metadata
  getFileMetadata: async (filePath) => {
    const response = await api.get('/files/metadata', {
      params: { path: filePath }
    })
    return response.data
  },

  // Watch file changes
  watchFiles: async (paths) => {
    const response = await api.post('/files/watch', { paths })
    return response.data
  }
}

// Analytics API
export const analyticsAPI = {
  // Get search analytics
  getSearchAnalytics: async (timeRange = '7d') => {
    const response = await api.get('/analytics/search', {
      params: { range: timeRange }
    })
    return response.data
  },

  // Get popular queries
  getPopularQueries: async (limit = 10) => {
    const response = await api.get('/analytics/queries/popular', {
      params: { limit }
    })
    return response.data
  },

  // Get file access patterns
  getFileAccessPatterns: async (timeRange = '7d') => {
    const response = await api.get('/analytics/files/access', {
      params: { range: timeRange }
    })
    return response.data
  },

  // Get performance metrics
  getPerformanceMetrics: async (timeRange = '24h') => {
    const response = await api.get('/analytics/performance', {
      params: { range: timeRange }
    })
    return response.data
  }
}

// Configuration API
export const configAPI = {
  // Get configuration
  getConfig: async () => {
    const response = await api.get('/config')
    return response.data
  },

  // Update configuration
  updateConfig: async (config) => {
    const response = await api.put('/config', config)
    return response.data
  },

  // Reset configuration
  resetConfig: async () => {
    const response = await api.post('/config/reset')
    return response.data
  }
}

export default api 