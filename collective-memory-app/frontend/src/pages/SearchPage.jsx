import React, { useState, useEffect } from 'react';
import { 
  MagnifyingGlassIcon, 
  DocumentTextIcon, 
  ClockIcon,
  SparklesIcon,
  FunnelIcon,
  ArrowUpIcon,
  BookmarkIcon,
  ShareIcon,
  XMarkIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchHistory, setSearchHistory] = useState([]);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    type: 'all',
    date: 'all',
    relevance: 'high'
  });

  // Load search history from localStorage
  useEffect(() => {
    const history = localStorage.getItem('searchHistory');
    if (history) {
      setSearchHistory(JSON.parse(history));
    }
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    
    // Add to search history
    const newHistory = [query, ...searchHistory.filter(item => item !== query)].slice(0, 8);
    setSearchHistory(newHistory);
    localStorage.setItem('searchHistory', JSON.stringify(newHistory));

    try {
      // Simulate API call with realistic delay
      await new Promise(resolve => setTimeout(resolve, 600));
      
      // Enhanced mock results with more realistic data
      setResults([
        {
          id: 1,
          title: 'Smart Context Bridge Implementation',
          content: 'Complete implementation of the Smart Context Bridge system with real-time JSON monitoring, automatic context generation, and 100% cross-chat memory continuity.',
          path: '/docs/smart-context-bridge.md',
          lastModified: '2025-07-18',
          score: 0.98,
          type: 'documentation',
          tags: ['context', 'memory', 'ai', 'bridge']
        },
        {
          id: 2,
          title: 'Query Processing System Architecture',
          content: 'Advanced query processing system that automatically detects "query:" prefixed messages and generates comprehensive documentation.',
          path: '/docs/query-processing.md',
          lastModified: '2025-07-17',
          score: 0.95,
          type: 'documentation',
          tags: ['query', 'processing', 'documentation']
        },
        {
          id: 3,
          title: 'JSON Chat System Integration',
          content: 'Structured conversation storage system with REST API endpoints, CLI interface, and advanced search capabilities.',
          path: '/docs/json-chat-system.md',
          lastModified: '2025-07-16',
          score: 0.92,
          type: 'documentation',
          tags: ['chat', 'json', 'api']
        },
        {
          id: 4,
          title: 'Enterprise Features Implementation',
          content: 'Complete enterprise-grade features including team collaboration, user management, real-time messaging, and analytics.',
          path: '/docs/enterprise-features.md',
          lastModified: '2025-07-15',
          score: 0.89,
          type: 'documentation',
          tags: ['enterprise', 'collaboration', 'analytics']
        },
        {
          id: 5,
          title: 'Memory Engine Optimization',
          content: 'A-Mem and Mem0 hybrid memory system with importance scoring, dynamic evolution, and perfect recall accuracy.',
          path: '/docs/memory-engines.md',
          lastModified: '2025-07-14',
          score: 0.87,
          type: 'documentation',
          tags: ['memory', 'engine', 'optimization']
        }
      ]);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickSearch = (term) => {
    setQuery(term);
    setTimeout(() => {
      handleSearch({ preventDefault: () => {} });
    }, 100);
  };

  const clearHistory = () => {
    setSearchHistory([]);
    localStorage.removeItem('searchHistory');
  };

  const clearSearch = () => {
    setQuery('');
    setResults([]);
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <MagnifyingGlassIcon className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-slate-900 dark:text-white">
              Search
            </h1>
          </div>
          <p className="text-slate-600 dark:text-slate-400 text-sm">
            Find conversations, documents, and memories instantly
          </p>
        </div>

        {/* Search Form */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-4 mb-6">
          <form onSubmit={handleSearch} className="space-y-3">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon className="w-5 h-5 text-slate-400" />
              </div>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search anything..."
                className="w-full pl-10 pr-12 py-3 bg-slate-50 dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg text-slate-900 dark:text-white placeholder-slate-500 dark:placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              />
              {query && (
                <button
                  type="button"
                  onClick={clearSearch}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  <XMarkIcon className="w-4 h-4 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300" />
                </button>
              )}
            </div>
            
            <div className="flex gap-2">
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Searching...
                  </>
                ) : (
                  <>
                    <MagnifyingGlassIcon className="w-4 h-4" />
                    Search
                  </>
                )}
              </button>
              
              <button
                type="button"
                onClick={() => setShowFilters(!showFilters)}
                className={`px-3 py-2.5 border rounded-lg transition-all duration-200 flex items-center gap-2 ${
                  showFilters 
                    ? 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700 text-blue-700 dark:text-blue-300' 
                    : 'bg-white dark:bg-slate-700 border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-600'
                }`}
              >
                <AdjustmentsHorizontalIcon className="w-4 h-4" />
                Filters
              </button>
            </div>

            {/* Filters Panel */}
            {showFilters && (
              <div className="bg-slate-50 dark:bg-slate-700/50 rounded-lg p-3 space-y-3">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Type
                    </label>
                    <select 
                      value={filters.type}
                      onChange={(e) => setFilters({...filters, type: e.target.value})}
                      className="w-full px-2 py-1.5 text-sm bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      <option value="all">All Types</option>
                      <option value="documentation">Documentation</option>
                      <option value="conversation">Conversation</option>
                      <option value="code">Code</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Date
                    </label>
                    <select 
                      value={filters.date}
                      onChange={(e) => setFilters({...filters, date: e.target.value})}
                      className="w-full px-2 py-1.5 text-sm bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      <option value="all">All Time</option>
                      <option value="today">Today</option>
                      <option value="week">This Week</option>
                      <option value="month">This Month</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                      Relevance
                    </label>
                    <select 
                      value={filters.relevance}
                      onChange={(e) => setFilters({...filters, relevance: e.target.value})}
                      className="w-full px-2 py-1.5 text-sm bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
                    >
                      <option value="high">High</option>
                      <option value="medium">Medium</option>
                      <option value="low">Low</option>
                    </select>
                  </div>
                </div>
              </div>
            )}
          </form>
        </div>

        {/* Search History */}
        {searchHistory.length > 0 && !query && (
          <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-4 mb-6">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-slate-900 dark:text-white">Recent Searches</h3>
              <button
                onClick={clearHistory}
                className="text-xs text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 transition-colors"
              >
                Clear All
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {searchHistory.map((term, index) => (
                <button
                  key={index}
                  onClick={() => handleQuickSearch(term)}
                  className="px-3 py-1.5 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-md hover:bg-slate-200 dark:hover:bg-slate-600 transition-all duration-200 text-sm"
                >
                  {term}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Search Results */}
        {results.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                  Results
                </h2>
                <p className="text-sm text-slate-600 dark:text-slate-400">
                  {results.length} results for "{query}"
                </p>
              </div>
              <div className="flex items-center gap-1 text-xs text-slate-500 dark:text-slate-400">
                <ArrowUpIcon className="w-3 h-3" />
                <span>Sorted by relevance</span>
              </div>
            </div>

            {results.map((result) => (
              <div 
                key={result.id} 
                className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-4 hover:shadow-md transition-all duration-200 group"
              >
                <div className="flex items-start gap-3">
                  <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <DocumentTextIcon className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="text-base font-medium text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors truncate">
                        {result.title}
                      </h3>
                      <div className="flex items-center gap-1 ml-2">
                        <button className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
                          <BookmarkIcon className="w-4 h-4" />
                        </button>
                        <button className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
                          <ShareIcon className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-3 leading-relaxed">
                      {result.content}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3 text-xs">
                        <span className="text-slate-500 dark:text-slate-400 font-mono">{result.path}</span>
                        <div className="flex items-center gap-1 text-slate-500 dark:text-slate-400">
                          <ClockIcon className="w-3 h-3" />
                          <span>{result.lastModified}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          {result.tags.slice(0, 3).map((tag, index) => (
                            <span 
                              key={index}
                              className="px-2 py-0.5 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded text-xs"
                            >
                              {tag}
                            </span>
                          ))}
                          {result.tags.length > 3 && (
                            <span className="text-slate-500 dark:text-slate-400 text-xs">
                              +{result.tags.length - 3}
                            </span>
                          )}
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <div className="w-12 h-1.5 bg-slate-200 dark:bg-slate-600 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all duration-500"
                            style={{ width: `${result.score * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-green-600 dark:text-green-400 font-medium text-xs">
                          {Math.round(result.score * 100)}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {results.length === 0 && query && !isLoading && (
          <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-8 text-center">
            <div className="w-12 h-12 bg-slate-100 dark:bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
              <MagnifyingGlassIcon className="w-6 h-6 text-slate-400" />
            </div>
            <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">No results found</h3>
            <p className="text-slate-600 dark:text-slate-400 mb-4 text-sm">
              Try adjusting your search terms or check for typos
            </p>
            <div className="flex gap-2 justify-center">
              <button
                onClick={clearSearch}
                className="px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-all duration-200 text-sm"
              >
                Clear Search
              </button>
              <button
                onClick={() => handleQuickSearch('Smart Context Bridge')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all duration-200 text-sm"
              >
                Try Example
              </button>
            </div>
          </div>
        )}

        {/* Initial State */}
        {results.length === 0 && !query && !searchHistory.length && (
          <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 p-8 text-center">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-full flex items-center justify-center mx-auto mb-4">
              <MagnifyingGlassIcon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">Start searching</h3>
            <p className="text-slate-600 dark:text-slate-400 mb-6 text-sm">
              Search across all your conversations, documents, and memory systems
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 max-w-2xl mx-auto">
              <div className="p-3 bg-slate-50 dark:bg-slate-700 rounded-lg">
                <DocumentTextIcon className="w-5 h-5 text-blue-600 dark:text-blue-400 mx-auto mb-1" />
                <h4 className="font-medium text-slate-900 dark:text-white mb-1 text-sm">Documents</h4>
                <p className="text-slate-600 dark:text-slate-400 text-xs">Search documentation</p>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-700 rounded-lg">
                <SparklesIcon className="w-5 h-5 text-purple-600 dark:text-purple-400 mx-auto mb-1" />
                <h4 className="font-medium text-slate-900 dark:text-white mb-1 text-sm">Conversations</h4>
                <p className="text-slate-600 dark:text-slate-400 text-xs">Find chat history</p>
              </div>
              <div className="p-3 bg-slate-50 dark:bg-slate-700 rounded-lg">
                <BookmarkIcon className="w-5 h-5 text-emerald-600 dark:text-emerald-400 mx-auto mb-1" />
                <h4 className="font-medium text-slate-900 dark:text-white mb-1 text-sm">Memory</h4>
                <p className="text-slate-600 dark:text-slate-400 text-xs">Access AI memory</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;