// useTranslation Hook for Collective Memory i18n
// Provides easy access to translations in React components

import { useState, useEffect } from 'react';
import { i18n } from '../i18n';

export function useTranslation() {
  const [language, setLanguage] = useState(i18n.getCurrentLanguage());
  
  useEffect(() => {
    const handleLanguageChange = (event) => {
      setLanguage(event.detail);
    };
    
    window.addEventListener('languageChanged', handleLanguageChange);
    
    return () => {
      window.removeEventListener('languageChanged', handleLanguageChange);
    };
  }, []);
  
  return {
    t: i18n.t.bind(i18n),
    language,
    setLanguage: i18n.setLanguage.bind(i18n),
    availableLanguages: i18n.getAvailableLanguages()
  };
}

export default useTranslation; 