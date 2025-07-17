import React, { useState } from 'react';
import { MagnifyingGlassIcon, AdjustmentsHorizontalIcon } from '@heroicons/react/24/outline';

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchType, setSearchType] = useState('basic');
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    // TODO: Implement search logic
    console.log('Search:', searchQuery, searchType);
  };

  return (
    <div className="max-w-4xl mx-auto" data-testid="search-page">
      {/* Page Header */}
      <div className="mb-8" data-testid="search-header">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Arama
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Gelişmiş arama ve filtreleme seçenekleri
        </p>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-8" data-testid="search-form">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
          {/* Main Search Input */}
          <div className="relative mb-4" data-testid="search-input-container">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Arama yapmak için buraya yazın..."
              className="w-full pl-10 pr-4 py-3 text-lg border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              data-testid="search-input"
            />
          </div>

          {/* Search Type Selection */}
          <div className="flex flex-wrap gap-4 mb-4" data-testid="search-type-selection">
            <label className="flex items-center">
              <input
                type="radio"
                name="searchType"
                value="basic"
                checked={searchType === 'basic'}
                onChange={(e) => setSearchType(e.target.value)}
                className="mr-2"
                data-testid="basic-search-radio"
              />
              <span className="text-gray-700 dark:text-gray-300">Temel Arama</span>
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="searchType"
                value="semantic"
                checked={searchType === 'semantic'}
                onChange={(e) => setSearchType(e.target.value)}
                className="mr-2"
                data-testid="semantic-search-radio"
              />
              <span className="text-gray-700 dark:text-gray-300">Semantic Arama</span>
            </label>
          </div>

          {/* Advanced Options Toggle */}
          <div className="flex justify-between items-center mb-4">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="flex items-center text-indigo-600 hover:text-indigo-700"
              data-testid="advanced-options-toggle"
            >
              <AdjustmentsHorizontalIcon className="h-5 w-5 mr-2" />
              Gelişmiş Seçenekler
            </button>
          </div>

          {/* Advanced Options */}
          {showAdvanced && (
            <div className="border-t pt-4 space-y-4" data-testid="advanced-options">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Dosya Türü
                  </label>
                  <select 
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
                    data-testid="file-type-filter"
                  >
                    <option value="">Tümü</option>
                    <option value="md">Markdown (.md)</option>
                    <option value="txt">Text (.txt)</option>
                    <option value="py">Python (.py)</option>
                    <option value="js">JavaScript (.js)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Sonuç Sayısı
                  </label>
                  <select 
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
                    data-testid="result-limit"
                  >
                    <option value="10">10</option>
                    <option value="25">25</option>
                    <option value="50">50</option>
                    <option value="100">100</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Search Button */}
          <div className="flex gap-4">
            <button
              type="submit"
              className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
              data-testid="search-button"
            >
              Ara
            </button>
            <button
              type="button"
              className="px-6 py-3 bg-gray-500 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors"
              data-testid="export-button"
            >
              Sonuçları Dışa Aktar
            </button>
          </div>
        </div>
      </form>

      {/* Search Results */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6" data-testid="search-results">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
          Arama Sonuçları
        </h2>
        
        {/* Sample Results */}
        <div className="space-y-4" data-testid="results-list">
          <div className="border-b border-gray-200 dark:border-gray-700 pb-4" data-testid="result-item">
            <h3 className="text-lg font-medium text-indigo-600 mb-1">
              Örnek Dosya 1.md
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-2">
              Bu bir örnek arama sonucudur. Gerçek arama fonksiyonalitesi henüz implement edilmemiştir.
            </p>
            <div className="text-sm text-gray-500">
              /path/to/file1.md • 2.3 KB • Son değişiklik: 2 saat önce
            </div>
          </div>
          
          <div className="border-b border-gray-200 dark:border-gray-700 pb-4" data-testid="result-item">
            <h3 className="text-lg font-medium text-indigo-600 mb-1">
              Örnek Dosya 2.md
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-2">
              İkinci örnek arama sonucu. API entegrasyonu tamamlandığında gerçek sonuçlar gösterilecek.
            </p>
            <div className="text-sm text-gray-500">
              /path/to/file2.md • 1.8 KB • Son değişiklik: 1 gün önce
            </div>
          </div>
        </div>

        {/* Pagination */}
        <div className="mt-6 flex justify-center" data-testid="pagination">
          <div className="flex space-x-2">
            <button className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50">
              Önceki
            </button>
            <button className="px-3 py-2 text-sm bg-indigo-600 text-white rounded-md">
              1
            </button>
            <button className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50">
              2
            </button>
            <button className="px-3 py-2 text-sm border border-gray-300 rounded-md hover:bg-gray-50">
              Sonraki
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage; 