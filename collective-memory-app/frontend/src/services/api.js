// API Services for Collective Memory Frontend
// Turkish UI + English code standard

const API_BASE_URL = 'http://localhost:8000';

// Base API client
class APIClient {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  get(endpoint, params = {}) {
    const searchParams = new URLSearchParams(params);
    const url = searchParams.toString() ? `${endpoint}?${searchParams}` : endpoint;
    return this.request(url, { method: 'GET' });
  }

  post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

const apiClient = new APIClient();

// Search API
export const searchAPI = {
  // Main search
  search: (query, options = {}) => {
    const params = {
      q: query,
      semantic: options.semantic || false,
      limit: options.limit || 50,
      sort_by: options.sortBy || 'relevance',
      ...options
    };
    return apiClient.get('/api/search', params);
  },

  // Quick search for autocomplete
  quickSearch: (query, limit = 5) => {
    return apiClient.get('/api/search/quick', { q: query, limit });
  },

  // Get search suggestions
  getSuggestions: (query) => {
    return apiClient.get('/api/search/suggestions', { q: query });
  },

  // Get search history
  getHistory: (limit = 20) => {
    return apiClient.get('/api/search/history', { limit });
  },

  // Export search results
  exportResults: async (query, format = 'markdown', filename = null) => {
    const response = await fetch(`${API_BASE_URL}/api/search/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, format, filename })
    });
    
    if (!response.ok) {
      throw new Error('Dışa aktarma başarısız');
    }
    
    return response.blob();
  }
};

// System API
export const systemAPI = {
  // Get system status
  getStatus: () => apiClient.get('/api/system/status'),

  // Get system statistics
  getStats: () => apiClient.get('/api/system/stats'),

  // Get performance metrics
  getPerformance: () => apiClient.get('/api/system/performance'),

  // Reindex system
  reindex: () => apiClient.post('/api/system/reindex'),

  // Clear cache
  clearCache: () => apiClient.post('/api/system/cache/clear'),

  // Get indexing status
  getIndexingStatus: () => apiClient.get('/api/system/indexing'),

  // Health check
  healthCheck: () => apiClient.get('/api/health')
};

// Analytics API
export const analyticsAPI = {
  // Get search analytics
  getSearchAnalytics: (timeRange = '7d') => {
    return apiClient.get('/api/analytics/search', { time_range: timeRange });
  },

  // Get popular queries
  getPopularQueries: (limit = 10) => {
    return apiClient.get('/api/analytics/popular-queries', { limit });
  },

  // Get file access patterns
  getFileAccessPatterns: (timeRange = '7d') => {
    return apiClient.get('/api/analytics/file-access', { time_range: timeRange });
  },

  // Get performance metrics over time
  getPerformanceMetrics: (timeRange = '7d') => {
    return apiClient.get('/api/analytics/performance', { time_range: timeRange });
  },

  // Get user activity
  getUserActivity: (timeRange = '7d') => {
    return apiClient.get('/api/analytics/user-activity', { time_range: timeRange });
  }
};

// Configuration API
export const configAPI = {
  // Get current configuration
  getConfig: () => apiClient.get('/api/config'),

  // Update configuration
  updateConfig: (config) => apiClient.put('/api/config', config),

  // Reset configuration to defaults
  resetConfig: () => apiClient.post('/api/config/reset'),

  // Get available settings schema
  getSchema: () => apiClient.get('/api/config/schema')
};

// Prompt Relationship API (for enhanced features)
export const promptAPI = {
  // Add new prompt
  addPrompt: (promptData) => apiClient.post('/api/prompts', promptData),

  // Get similar prompts
  getSimilarPrompts: (query, limit = 5) => {
    return apiClient.get('/api/prompts/similar', { q: query, limit });
  },

  // Get related prompts for specific prompt ID
  getRelatedPrompts: (promptId, limit = 5) => {
    return apiClient.get(`/api/prompts/${promptId}/related`, { limit });
  },

  // Get context suggestions
  getContextSuggestions: (limit = 10) => {
    return apiClient.get('/api/prompts/context-suggestions', { limit });
  },

  // Get prompt history
  getPromptHistory: (limit = 20) => {
    return apiClient.get('/api/prompts/history', { limit });
  }
};

// File Management API
export const fileAPI = {
  // Get file details
  getFileDetails: (filePath) => {
    return apiClient.get('/api/files/details', { path: filePath });
  },

  // Get file content preview
  getFilePreview: (filePath, maxLength = 500) => {
    return apiClient.get('/api/files/preview', { path: filePath, max_length: maxLength });
  },

  // Get recently modified files
  getRecentFiles: (limit = 10) => {
    return apiClient.get('/api/files/recent', { limit });
  },

  // Get file statistics
  getFileStats: () => apiClient.get('/api/files/stats')
};

// WebSocket connection for real-time updates
export class WebSocketClient {
  constructor(url = 'ws://localhost:8000/ws') {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.listeners = new Map();
  }

  connect() {
    try {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.emit('connected');
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.emit(data.type, data.payload);
        } catch (error) {
          console.error('WebSocket message parsing error:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.emit('disconnected');
        this.reconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.emit('error', error);
      };
    } catch (error) {
      console.error('WebSocket connection failed:', error);
      this.reconnect();
    }
  }

  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(type, payload) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, payload }));
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  emit(event, data = null) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`Error in WebSocket event handler for ${event}:`, error);
        }
      });
    }
  }
}

// Create singleton WebSocket instance
export const wsClient = new WebSocketClient();

// Error handling utilities
export const handleAPIError = (error, fallbackMessage = 'Bir hata oluştu') => {
  if (error.message.includes('fetch')) {
    return 'Sunucuya bağlanılamıyor. Lütfen bağlantınızı kontrol edin.';
  }
  
  if (error.message.includes('400')) {
    return 'Geçersiz istek. Lütfen girdilerinizi kontrol edin.';
  }
  
  if (error.message.includes('401')) {
    return 'Yetkilendirme hatası. Lütfen giriş yapın.';
  }
  
  if (error.message.includes('403')) {
    return 'Bu işlem için yetkiniz bulunmuyor.';
  }
  
  if (error.message.includes('404')) {
    return 'İstenen kaynak bulunamadı.';
  }
  
  if (error.message.includes('500')) {
    return 'Sunucu hatası. Lütfen daha sonra tekrar deneyin.';
  }
  
  return error.message || fallbackMessage;
};

// Request timeout utility
export const withTimeout = (promise, timeout = 10000) => {
  return Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('İstek zaman aşımına uğradı')), timeout)
    )
  ]);
};

// Retry utility
export const withRetry = async (fn, maxRetries = 3, delay = 1000) => {
  let lastError;
  
  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      if (i === maxRetries) {
        break;
      }
      
      await new Promise(resolve => setTimeout(resolve, delay * (i + 1)));
    }
  }
  
  throw lastError;
};

export default {
  searchAPI,
  systemAPI,
  analyticsAPI,
  configAPI,
  promptAPI,
  fileAPI,
  wsClient,
  handleAPIError,
  withTimeout,
  withRetry
}; 