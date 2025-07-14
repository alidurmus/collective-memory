import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Search, 
  Filter, 
  X, 
  Clock, 
  Zap, 
  Download,
  Settings as SettingsIcon
} from 'lucide-react'
import { useSearch } from '../hooks/useSearch'
import LoadingSpinner from './LoadingSpinner'

const SearchPanel = () => {
  const [showAdvanced, setShowAdvanced] = useState(false)
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
    isExporting
  } = useSearch()

  const handleSearch = (searchQuery) => {
    setQuery(searchQuery)
  }

  const handleAdvancedSearch = () => {
    setShowAdvanced(!showAdvanced)
  }

  const handleExport = () => {
    if (query) {
      exportResults({ query, format: 'markdown' })
    }
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Hızlı Arama
        </h3>
        <div className="flex items-center space-x-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleAdvancedSearch}
            className={`p-2 rounded-lg transition-colors ${
              showAdvanced
                ? 'bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
            aria-label="Gelişmiş Arama"
          >
            <Filter className="w-4 h-4" />
          </motion.button>
          
          {query && searchResults && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleExport}
              disabled={isExporting}
              className="p-2 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors disabled:opacity-50"
              aria-label="Sonuçları Dışa Aktar"
            >
              {isExporting ? (
                <LoadingSpinner size="sm" />
              ) : (
                <Download className="w-4 h-4" />
              )}
            </motion.button>
          )}
        </div>
      </div>

      {/* Search Input */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ne aramak istiyorsunuz?"
          className="w-full pl-12 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400"
        />
        {isSearching && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <LoadingSpinner size="sm" />
          </div>
        )}
      </div>

      {/* Search Options */}
      <div className="flex items-center space-x-4 mb-4">
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={searchOptions.semantic}
            onChange={(e) => updateSearchOptions({ semantic: e.target.checked })}
            className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
          />
          <span className="text-sm text-gray-700 dark:text-gray-300 flex items-center space-x-1">
            <Zap className="w-3 h-3" />
            <span>Semantik Arama</span>
          </span>
        </label>
      </div>

      {/* Advanced Search */}
      <AnimatePresence>
        {showAdvanced && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg mb-4 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Dosya Türü
                  </label>
                  <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                    <option value="">Tümü</option>
                    <option value="md">Markdown (.md)</option>
                    <option value="txt">Text (.txt)</option>
                    <option value="py">Python (.py)</option>
                    <option value="js">JavaScript (.js)</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Tarih Aralığı
                  </label>
                  <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                    <option value="">Tüm zamanlar</option>
                    <option value="1d">Son 24 saat</option>
                    <option value="7d">Son 7 gün</option>
                    <option value="30d">Son 30 gün</option>
                    <option value="90d">Son 90 gün</option>
                  </select>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Search History */}
      {searchHistory.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 flex items-center space-x-1">
            <Clock className="w-3 h-3" />
            <span>Son Aramalar</span>
          </h4>
          <div className="flex flex-wrap gap-2">
            {searchHistory.slice(0, 5).map((item, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleSearch(item)}
                className="px-3 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
              >
                {item}
              </motion.button>
            ))}
          </div>
        </div>
      )}

      {/* Search Results Summary */}
      {searchResults && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="border-t border-gray-200 dark:border-gray-700 pt-4"
        >
          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
            <span>
              {searchResults.total} sonuç bulundu
              {searchResults.searchTime && ` (${searchResults.searchTime}ms)`}
            </span>
            {searchResults.total > 0 && (
              <span className="text-primary-600 dark:text-primary-400">
                İlk {Math.min(searchOptions.limit, searchResults.total)} sonuç gösteriliyor
              </span>
            )}
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default SearchPanel 