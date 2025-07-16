import React, { useState, useEffect, useCallback } from 'react';
import { useSearch } from '../hooks/useSearch';
import { promptAPI } from '../services/api';
import '../styles/context7.css';

const SearchPanel = ({ embedded = false }) => {
  const [query, setQuery] = useState('');
  const [useSemanticSearch, setUseSemanticSearch] = useState(false);
  const [similarPrompts, setSimilarPrompts] = useState([]);
  const [contextSuggestions, setContextSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [exportFormat, setExportFormat] = useState('markdown');
  
  const {
    results,
    isLoading,
    error,
    searchStats,
    performSearch,
    exportResults
  } = useSearch();

  // Benzer promptları getir
  const fetchSimilarPrompts = useCallback(async (searchQuery) => {
    if (searchQuery.length < 3) {
      setSimilarPrompts([]);
      return;
    }

    try {
      const response = await promptAPI.getSimilarPrompts(searchQuery);
      if (response.success && response.data) {
        setSimilarPrompts(response.data.slice(0, 5)); // İlk 5 benzer prompt
      }
    } catch (error) {
      console.error('Benzer promptlar alınamadı:', error);
    }
  }, []);

  // Bağlam önerilerini getir
  const fetchContextSuggestions = useCallback(async () => {
    try {
      const response = await promptAPI.getContextSuggestions();
      if (response.success && response.data) {
        setContextSuggestions(response.data.slice(0, 3)); // İlk 3 öneri
      }
    } catch (error) {
      console.error('Bağlam önerileri alınamadı:', error);
    }
  }, []);

  // Arama yapıldığında prompt'u kaydet
  const trackSearchPrompt = useCallback(async (searchQuery, resultsCount) => {
    try {
      await promptAPI.addPrompt({
        prompt_text: searchQuery,
        search_type: useSemanticSearch ? 'semantic' : 'standard',
        results_count: resultsCount || 0
      });
    } catch (error) {
      console.error('Prompt kaydedilemedi:', error);
    }
  }, [useSemanticSearch]);

  useEffect(() => {
    fetchContextSuggestions();
  }, [fetchContextSuggestions]);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (query.trim()) {
        fetchSimilarPrompts(query.trim());
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [query, fetchSimilarPrompts]);

  const handleSearch = async (searchQuery = query) => {
    if (!searchQuery.trim()) return;

    setShowSuggestions(false);
    
    const searchParams = {
      q: searchQuery.trim(),
      semantic: useSemanticSearch,
      limit: 50
    };

    const searchResults = await performSearch(searchParams);
    
    // Prompt'u izleme sistemine kaydet
    if (searchResults && searchResults.length > 0) {
      await trackSearchPrompt(searchQuery.trim(), searchResults.length);
    }
    
    // Benzer promptları güncelle
    await fetchSimilarPrompts(searchQuery.trim());
  };

  const handleExport = async () => {
    if (results.length === 0) return;
    
    const success = await exportResults({
      query,
      results,
      format: exportFormat
    });
    
    if (success) {
      // Export başarılı mesajı göster
      console.log('Sonuçlar başarıyla dışa aktarıldı');
    }
  };

  const handleSimilarPromptClick = (promptText) => {
    setQuery(promptText);
    handleSearch(promptText);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const containerClass = embedded 
    ? 'space-y-4' 
    : 'context7-card p-6 max-w-4xl mx-auto';

  return (
    <div className={`${containerClass} turkish-ui`}>
      {!embedded && (
        <div className="text-center mb-6">
          <h1 className="context7-heading context7-heading--xl context7-gradient-text mb-2">
            Akıllı Arama
          </h1>
          <p className="context7-text context7-text--muted">
            Dosyalarınızda hızlı ve akıllı arama yapın
          </p>
        </div>
      )}
      
      {/* Ana Arama Arayüzü */}
      <div className="space-y-4">
        
        {/* Arama Giriş Alanı */}
        <div className="relative">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                onFocus={() => setShowSuggestions(true)}
                placeholder="Arama yapın... (örn: Django models, React hooks)"
                className="context7-input text-base"
                disabled={isLoading}
              />
              {query && (
                <button
                  onClick={() => setQuery('')}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  aria-label="Aramayı temizle"
                >
                  ✕
                </button>
              )}
            </div>
            
            <button
              onClick={() => handleSearch()}
              disabled={!query.trim() || isLoading}
              className="context7-button px-6 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  <span>Arıyor...</span>
                </div>
              ) : (
                <div className="flex items-center">
                  <span className="mr-2">🔍</span>
                  <span>Ara</span>
                </div>
              )}
            </button>
          </div>
        </div>
        
        {/* Arama Seçenekleri */}
        <div className="flex flex-wrap items-center gap-4">
          <label className="flex items-center context7-interactive">
            <input
              type="checkbox"
              checked={useSemanticSearch}
              onChange={(e) => setUseSemanticSearch(e.target.checked)}
              className="mr-2 rounded"
            />
            <span className="context7-text text-sm">
              Semantik Arama (AI Destekli)
            </span>
          </label>
          
          {results.length > 0 && (
            <div className="flex items-center gap-2 ml-auto">
              <select
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value)}
                className="context7-input text-sm py-2"
              >
                <option value="markdown">Markdown</option>
                <option value="json">JSON</option>
                <option value="text">Metin</option>
              </select>
              <button
                onClick={handleExport}
                className="context7-button context7-button--secondary text-sm"
              >
                <span className="mr-1">📤</span>
                Dışa Aktar
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Öneriler ve Benzer Aramalar */}
      {showSuggestions && (query.length > 0 || contextSuggestions.length > 0) && (
        <div className="context7-card p-4 mt-4 border border-gray-200">
          
          {/* Benzer Aramalar */}
          {similarPrompts.length > 0 && (
            <div className="mb-4">
              <h4 className="context7-heading context7-heading--sm mb-3 flex items-center">
                <span className="mr-2">🔗</span>
                Benzer Aramalar
              </h4>
              <div className="space-y-2">
                {similarPrompts.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => handleSimilarPromptClick(prompt.prompt_text)}
                    className="block w-full text-left p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors context7-interactive"
                  >
                    <div className="flex items-center justify-between">
                      <span className="context7-text text-sm">{prompt.prompt_text}</span>
                      <span className="context7-text context7-text--muted text-xs">
                        %{Math.round(prompt.similarity_score * 100)} benzer
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
          
          {/* Önerilen Bağlam */}
          {contextSuggestions.length > 0 && (
            <div>
              <h4 className="context7-heading context7-heading--sm mb-3 flex items-center">
                <span className="mr-2">💡</span>
                Önerilen Bağlam
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                {contextSuggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => handleSimilarPromptClick(suggestion.suggestion)}
                    className="p-2 text-left rounded-lg bg-blue-50 hover:bg-blue-100 transition-colors context7-interactive"
                  >
                    <span className="context7-text text-sm">{suggestion.suggestion}</span>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
      
      {/* Hata Mesajı */}
      {error && (
        <div className="context7-card p-4 border-l-4 border-red-500 bg-red-50">
          <div className="flex items-center">
            <span className="text-red-500 mr-2">⚠️</span>
            <span className="context7-text text-red-700">
              Arama sırasında bir hata oluştu: {error}
            </span>
          </div>
        </div>
      )}
      
      {/* Arama Sonuçları */}
      {results.length > 0 && (
        <div className="mt-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="context7-heading context7-heading--sm">
              Arama Sonuçları ({results.length})
            </h3>
            {searchStats && (
              <span className="context7-text context7-text--muted text-sm">
                {searchStats.searchTime}ms içinde bulundu
              </span>
            )}
          </div>
          
          <div className="space-y-4">
            {results.map((result, index) => (
              <div key={index} className="context7-card p-4 context7-interactive">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="context7-heading context7-heading--sm context7-gradient-text">
                    {result.title || result.filename}
                  </h4>
                  <span className="context7-status context7-status--info text-xs">
                    Skor: {(result.score * 100).toFixed(1)}%
                  </span>
                </div>
                
                <p className="context7-text text-sm mb-2">
                  📁 {result.path}
                </p>
                
                {result.snippet && (
                  <div className="context7-text text-sm bg-gray-50 p-3 rounded-lg">
                    <div 
                      dangerouslySetInnerHTML={{ 
                        __html: result.snippet.replace(
                          new RegExp(`(${query})`, 'gi'),
                          '<span class="context7-highlight">$1</span>'
                        )
                      }}
                    />
                  </div>
                )}
                
                <div className="flex items-center justify-between mt-3 text-xs">
                  <span className="context7-text context7-text--muted">
                    {result.size ? `${(result.size / 1024).toFixed(1)} KB` : ''} • 
                    {result.lastModified ? new Date(result.lastModified).toLocaleDateString('tr-TR') : ''}
                  </span>
                  <button className="context7-button context7-button--secondary text-xs">
                    Dosyayı Aç
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Sonuç Bulunamadı */}
      {!isLoading && results.length === 0 && query && (
        <div className="text-center py-8">
          <div className="context7-card p-6">
            <span className="text-4xl mb-4 block">🔍</span>
            <h3 className="context7-heading context7-heading--md mb-2">
              Sonuç Bulunamadı
            </h3>
            <p className="context7-text context7-text--muted">
              "{query}" araması için sonuç bulunamadı. Farklı anahtar kelimeler deneyin.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchPanel; 