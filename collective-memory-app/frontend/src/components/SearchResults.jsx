import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Search, 
  Filter, 
  SortDesc, 
  FileText, 
  Clock, 
  Download,
  ExternalLink,
  ChevronDown,
  ChevronRight,
  Hash,
  Calendar
} from 'lucide-react'
import { useSearch } from '../hooks/useSearch'
import LoadingSpinner from './LoadingSpinner'

const SearchResults = () => {
  const [expandedResults, setExpandedResults] = useState(new Set())
  const [sortBy, setSortBy] = useState('relevance')
  
  const {
    query,
    setQuery,
    searchOptions,
    updateSearchOptions,
    searchResults,
    isSearching,
    suggestions,
    searchHistory,
    exportResults,
    isExporting,
    loadMore,
    canLoadMore
  } = useSearch()

  const toggleResultExpansion = (resultId) => {
    const newExpanded = new Set(expandedResults)
    if (newExpanded.has(resultId)) {
      newExpanded.delete(resultId)
    } else {
      newExpanded.add(resultId)
    }
    setExpandedResults(newExpanded)
  }

  const handleExport = () => {
    if (query) {
      exportResults({ query, format: 'markdown' })
    }
  }

  const highlightText = (text, searchQuery) => {
    if (!searchQuery) return text
    
    const regex = new RegExp(`(${searchQuery})`, 'gi')
    return text.split(regex).map((part, index) =>
      regex.test(part) ? (
        <mark key={index} className="bg-yellow-200 dark:bg-yellow-800 px-1 rounded">
          {part}
        </mark>
      ) : part
    )
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Arama Sonuçları
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            {searchResults 
              ? `"${query}" için ${searchResults.total} sonuç bulundu`
              : 'Aramaya başlamak için yukarıdaki kutucuğa yazmaya başlayın'
            }
          </p>
        </div>
        
        <div className="mt-4 sm:mt-0 flex items-center space-x-3">
          {query && searchResults && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleExport}
              disabled={isExporting}
              className="btn-secondary flex items-center space-x-2"
            >
              {isExporting ? (
                <LoadingSpinner size="sm" />
              ) : (
                <Download className="w-4 h-4" />
              )}
              <span>Dışa Aktar</span>
            </motion.button>
          )}
        </div>
      </motion.div>

      {/* Search Bar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card p-6"
      >
        <div className="space-y-4">
          {/* Main Search Input */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Aramak istediğiniz içeriği yazın..."
              className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            />
            {isSearching && (
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <LoadingSpinner size="sm" />
              </div>
            )}
          </div>

          {/* Options and Filters */}
          <div className="flex flex-wrap items-center gap-4">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={searchOptions.semantic}
                onChange={(e) => updateSearchOptions({ semantic: e.target.checked })}
                className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">
                Semantik Arama
              </span>
            </label>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            >
              <option value="relevance">İlgi Seviyesi</option>
              <option value="date">Tarih (Yeni)</option>
              <option value="date_asc">Tarih (Eski)</option>
              <option value="size">Dosya Boyutu</option>
              <option value="name">Dosya Adı</option>
            </select>

            <div className="text-sm text-gray-500 dark:text-gray-400">
              {searchResults?.limit} / {searchResults?.total || 0} sonuç gösteriliyor
            </div>
          </div>
        </div>
      </motion.div>

      {/* Search Results */}
      <AnimatePresence mode="wait">
        {isSearching ? (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex items-center justify-center h-64"
          >
            <LoadingSpinner size="lg" text="Aranıyor..." />
          </motion.div>
        ) : searchResults?.results?.length > 0 ? (
          <motion.div
            key="results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-4"
          >
            {searchResults.results.map((result, index) => {
              const isExpanded = expandedResults.has(result.id)
              
              return (
                <motion.div
                  key={result.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="card hover:shadow-md transition-shadow duration-200"
                >
                  <div className="p-6">
                    {/* Result Header */}
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-start space-x-3 flex-1">
                        <FileText className="w-5 h-5 text-primary-600 dark:text-primary-400 mt-0.5" />
                        <div className="flex-1 min-w-0">
                          <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 truncate">
                            {highlightText(result.title || result.filename, query)}
                          </h3>
                          <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
                            {result.path}
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <span className="text-xs px-2 py-1 bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 rounded-full">
                          {result.score ? `${Math.round(result.score * 100)}%` : 'N/A'}
                        </span>
                        <button
                          onClick={() => toggleResultExpansion(result.id)}
                          className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                        >
                          {isExpanded ? (
                            <ChevronDown className="w-4 h-4" />
                          ) : (
                            <ChevronRight className="w-4 h-4" />
                          )}
                        </button>
                      </div>
                    </div>

                    {/* Result Summary */}
                    <div className="mb-3">
                      <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-3">
                        {highlightText(result.snippet || result.content?.substring(0, 300) + '...', query)}
                      </p>
                    </div>

                    {/* Result Metadata */}
                    <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-1">
                          <Calendar className="w-3 h-3" />
                          <span>{new Date(result.lastModified).toLocaleDateString('tr-TR')}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Hash className="w-3 h-3" />
                          <span>{formatFileSize(result.size || 0)}</span>
                        </div>
                      </div>
                      
                      <button className="flex items-center space-x-1 text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300">
                        <ExternalLink className="w-3 h-3" />
                        <span>Dosyayı Aç</span>
                      </button>
                    </div>

                    {/* Expanded Content */}
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: 'auto', opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3 }}
                          className="overflow-hidden"
                        >
                          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                            <h4 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-2">
                              Dosya İçeriği Önizlemesi
                            </h4>
                            <div className="code-block max-h-64 overflow-y-auto">
                              <pre className="whitespace-pre-wrap text-xs">
                                {highlightText(result.content || 'İçerik mevcut değil', query)}
                              </pre>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </motion.div>
              )
            })}

            {/* Load More Button */}
            {canLoadMore && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-center pt-6"
              >
                <button
                  onClick={loadMore}
                  className="btn-primary flex items-center space-x-2"
                >
                  <span>Daha Fazla Yükle</span>
                  <ChevronDown className="w-4 h-4" />
                </button>
              </motion.div>
            )}
          </motion.div>
        ) : query ? (
          <motion.div
            key="no-results"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="card p-12 text-center"
          >
            <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">
              Sonuç Bulunamadı
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              "{query}" için herhangi bir sonuç bulunamadı. Farklı anahtar kelimeler deneyin.
            </p>
            {suggestions?.length > 0 && (
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                  Bunları deneyin:
                </p>
                <div className="flex flex-wrap justify-center gap-2">
                  {suggestions.map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => setQuery(suggestion)}
                      className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        ) : (
          <motion.div
            key="welcome"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="card p-12 text-center"
          >
            <Search className="w-16 h-16 text-gray-400 mx-auto mb-6" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Collective Memory'de Arama Yapın
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8 max-w-md mx-auto">
              Binlerce dosya arasından istediğiniz bilgiyi hızlıca bulun. 
              Semantik arama ile daha akıllı sonuçlar alın.
            </p>
            
            {searchHistory.length > 0 && (
              <div>
                <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Son Aramalarınız
                </h3>
                <div className="flex flex-wrap justify-center gap-2">
                  {searchHistory.slice(0, 6).map((item, index) => (
                    <button
                      key={index}
                      onClick={() => setQuery(item)}
                      className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                    >
                      {item}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default SearchResults 