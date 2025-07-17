import React, { useState } from 'react';
import { MagnifyingGlassIcon, DocumentTextIcon, ClockIcon } from '@heroicons/react/24/outline';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock results
      setResults([
        {
          id: 1,
          title: 'React Component Best Practices',
          content: 'This document covers the best practices for writing React components...',
          path: '/docs/react-best-practices.md',
          lastModified: '2024-01-15',
          score: 0.95
        },
        {
          id: 2,
          title: 'API Integration Guide',
          content: 'Learn how to integrate with external APIs in your React application...',
          path: '/docs/api-integration.md',
          lastModified: '2024-01-14',
          score: 0.87
        },
        {
          id: 3,
          title: 'State Management Patterns',
          content: 'Explore different state management patterns in React applications...',
          path: '/docs/state-management.md',
          lastModified: '2024-01-13',
          score: 0.82
        }
      ]);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="context7-card mb-8">
        <h1 className="context7-heading-1">Search</h1>
        <p className="context7-text-muted">Find information across all conversations and documents</p>
      </header>

      {/* Search Form */}
      <div className="context7-card mb-8">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter your search query..."
              className="context7-input"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="context7-button context7-button-primary"
          >
            {isLoading ? (
              <div className="context7-loading"></div>
            ) : (
              <>
                <MagnifyingGlassIcon className="w-5 h-5" />
                Search
              </>
            )}
          </button>
        </form>
      </div>

      {/* Search Results */}
      {results.length > 0 && (
        <div className="space-y-4">
          <div className="context7-card">
            <h2 className="context7-heading-3">Search Results ({results.length})</h2>
            <p className="context7-text-muted">Found {results.length} results for "{query}"</p>
          </div>

          {results.map((result) => (
            <div key={result.id} className="context7-card hover:scale-[1.02] transition-transform">
              <div className="flex items-start gap-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <DocumentTextIcon className="w-5 h-5 text-blue-600" />
                </div>
                <div className="flex-1">
                  <h3 className="context7-heading-3 mb-2">{result.title}</h3>
                  <p className="context7-text mb-3">{result.content}</p>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="context7-text-muted">{result.path}</span>
                    <div className="flex items-center gap-1">
                      <ClockIcon className="w-4 h-4" />
                      <span className="context7-text-muted">{result.lastModified}</span>
                    </div>
                    <span className="context7-status-success font-semibold">
                      {Math.round(result.score * 100)}% match
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {results.length === 0 && query && !isLoading && (
        <div className="context7-card text-center py-12">
          <MagnifyingGlassIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="context7-heading-3 mb-2">No results found</h3>
          <p className="context7-text-muted">Try adjusting your search terms or check for typos</p>
        </div>
      )}

      {/* Initial State */}
      {results.length === 0 && !query && (
        <div className="context7-card text-center py-12">
          <MagnifyingGlassIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="context7-heading-3 mb-2">Start searching</h3>
          <p className="context7-text-muted">Enter a search query to find relevant information</p>
        </div>
      )}
    </div>
  );
};

export default SearchPage;