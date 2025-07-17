// Language Switcher Component
// Allows users to switch between Turkish and English

import React, { useState } from 'react';
import { ChevronDownIcon, LanguageIcon } from '@heroicons/react/24/outline';
import { useTranslation } from '../hooks/useTranslation';

const LanguageSwitcher = ({ className = '' }) => {
  const { language, setLanguage, availableLanguages } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  
  const currentLang = availableLanguages.find(lang => lang.code === language);
  
  const handleLanguageChange = (langCode) => {
    setLanguage(langCode);
    setIsOpen(false);
  };
  
  return (
    <div className={`relative ${className}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2 px-3 py-2 rounded-lg bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/20 transition-all duration-200"
        title="Dil Seçimi / Language Selection"
      >
        <LanguageIcon className="w-4 h-4 text-white/80" />
        <span className="text-sm font-medium text-white/90">
          {currentLang?.flag} {currentLang?.name}
        </span>
        <ChevronDownIcon 
          className={`w-4 h-4 text-white/60 transition-transform duration-200 ${
            isOpen ? 'rotate-180' : ''
          }`} 
        />
      </button>
      
      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-48 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg border border-white/20 z-50">
          {availableLanguages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => handleLanguageChange(lang.code)}
              className={`w-full px-4 py-3 text-left hover:bg-blue-50 first:rounded-t-lg last:rounded-b-lg transition-colors ${
                lang.code === language 
                  ? 'bg-blue-100 text-blue-900 font-medium' 
                  : 'text-gray-700'
              }`}
            >
              <div className="flex items-center space-x-3">
                <span className="text-lg">{lang.flag}</span>
                <div>
                  <div className="font-medium">{lang.name}</div>
                  <div className="text-xs text-gray-500">
                    {lang.code === 'tr' ? 'Ana dil' : 'Secondary language'}
                  </div>
                </div>
                {lang.code === language && (
                  <div className="ml-auto">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  </div>
                )}
              </div>
            </button>
          ))}
        </div>
      )}
      
      {/* Overlay to close dropdown */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40" 
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default LanguageSwitcher; 