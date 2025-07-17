// Internationalization (i18n) System
// Multi-language support for Collective Memory v3.0

const translations = {
  tr: {
    // Navigation
    nav: {
      dashboard: "Ana Panel",
      search: "Akıllı Arama", 
      analytics: "Analitikler",
      settings: "Ayarlar",
      enterprise: "Kurumsal"
    },
    
    // Dashboard
    dashboard: {
      title: "Collective Memory - Akıllı Bağlam Yönetimi",
      welcome: "Hoş Geldiniz",
      quickActions: "Hızlı İşlemler",
      recentActivity: "Son Aktiviteler",
      systemStatus: "Sistem Durumu",
      stats: {
        totalFiles: "Toplam Dosya",
        searchQueries: "Arama Sorgusu", 
        cacheHitRate: "Önbellek Oranı",
        uptime: "Çalışma Süresi"
      }
    },
    
    // Search
    search: {
      title: "Akıllı Arama",
      placeholder: "Arama terimini girin...",
      semanticSearch: "Anlamsal Arama",
      advancedOptions: "Gelişmiş Seçenekler",
      fileTypes: "Dosya Türleri",
      dateRange: "Tarih Aralığı",
      results: "arama sonucu",
      noResults: "Sonuç bulunamadı",
      searchHistory: "Arama Geçmişi",
      exportResults: "Sonuçları Dışa Aktar"
    },
    
    // Analytics
    analytics: {
      title: "Sistem Analitikleri",
      overview: "Genel Bakış",
      performance: "Performans Metrikleri",
      trends: "Eğilimler",
      popularQueries: "Popüler Sorgular",
      fileDistribution: "Dosya Dağılımı",
      systemResources: "Sistem Kaynakları",
      realTimeUpdates: "Canlı Güncellemeler"
    },
    
    // Settings
    settings: {
      title: "Sistem Ayarları",
      general: "Genel",
      search: "Arama",
      system: "Sistem",
      security: "Güvenlik",
      theme: "Tema",
      language: "Dil",
      notifications: "Bildirimler",
      autoSave: "Otomatik Kaydet",
      indexing: "İndeksleme",
      cache: "Önbellek",
      performance: "Performans"
    },
    
    // Enterprise
    enterprise: {
      title: "Kurumsal Özellikler",
      teamManagement: "Takım Yönetimi",
      userRoles: "Kullanıcı Rolleri",
      collaboration: "İşbirliği",
      realTimeChat: "Canlı Sohbet",
      analytics: "Kurumsal Analitikler",
      cloudSync: "Bulut Senkronizasyonu",
      security: "Kurumsal Güvenlik"
    },
    
    // Common
    common: {
      save: "Kaydet",
      cancel: "İptal",
      delete: "Sil",
      edit: "Düzenle",
      create: "Oluştur",
      update: "Güncelle",
      refresh: "Yenile",
      loading: "Yükleniyor...",
      error: "Hata oluştu",
      success: "Başarılı",
      confirm: "Onayla",
      yes: "Evet",
      no: "Hayır",
      close: "Kapat",
      open: "Aç",
      export: "Dışa Aktar",
      import: "İçe Aktar"
    },
    
    // System Messages
    messages: {
      searchCompleted: "Arama tamamlandı",
      indexingInProgress: "İndeksleme devam ediyor",
      systemHealthy: "Sistem sağlıklı",
      connectionLost: "Bağlantı kaybedildi",
      dataSaved: "Veriler kaydedildi",
      settingsUpdated: "Ayarlar güncellendi"
    }
  },
  
  en: {
    // Navigation
    nav: {
      dashboard: "Dashboard",
      search: "Smart Search",
      analytics: "Analytics", 
      settings: "Settings",
      enterprise: "Enterprise"
    },
    
    // Dashboard
    dashboard: {
      title: "Collective Memory - Smart Context Management",
      welcome: "Welcome",
      quickActions: "Quick Actions",
      recentActivity: "Recent Activity",
      systemStatus: "System Status",
      stats: {
        totalFiles: "Total Files",
        searchQueries: "Search Queries",
        cacheHitRate: "Cache Hit Rate",
        uptime: "Uptime"
      }
    },
    
    // Search
    search: {
      title: "Smart Search",
      placeholder: "Enter search term...",
      semanticSearch: "Semantic Search",
      advancedOptions: "Advanced Options",
      fileTypes: "File Types",
      dateRange: "Date Range",
      results: "search results",
      noResults: "No results found",
      searchHistory: "Search History",
      exportResults: "Export Results"
    },
    
    // Analytics
    analytics: {
      title: "System Analytics",
      overview: "Overview",
      performance: "Performance Metrics",
      trends: "Trends",
      popularQueries: "Popular Queries",
      fileDistribution: "File Distribution",
      systemResources: "System Resources",
      realTimeUpdates: "Real-time Updates"
    },
    
    // Settings
    settings: {
      title: "System Settings",
      general: "General",
      search: "Search",
      system: "System",
      security: "Security",
      theme: "Theme",
      language: "Language",
      notifications: "Notifications",
      autoSave: "Auto Save",
      indexing: "Indexing",
      cache: "Cache",
      performance: "Performance"
    },
    
    // Enterprise
    enterprise: {
      title: "Enterprise Features",
      teamManagement: "Team Management",
      userRoles: "User Roles",
      collaboration: "Collaboration",
      realTimeChat: "Real-time Chat",
      analytics: "Enterprise Analytics",
      cloudSync: "Cloud Sync",
      security: "Enterprise Security"
    },
    
    // Common
    common: {
      save: "Save",
      cancel: "Cancel",
      delete: "Delete", 
      edit: "Edit",
      create: "Create",
      update: "Update",
      refresh: "Refresh",
      loading: "Loading...",
      error: "Error occurred",
      success: "Success",
      confirm: "Confirm",
      yes: "Yes",
      no: "No",
      close: "Close",
      open: "Open",
      export: "Export",
      import: "Import"
    },
    
    // System Messages
    messages: {
      searchCompleted: "Search completed",
      indexingInProgress: "Indexing in progress",
      systemHealthy: "System healthy",
      connectionLost: "Connection lost",
      dataSaved: "Data saved",
      settingsUpdated: "Settings updated"
    }
  }
};

class I18n {
  constructor() {
    this.currentLanguage = this.detectLanguage();
    this.translations = translations;
  }
  
  detectLanguage() {
    // Check localStorage first
    const saved = localStorage.getItem('collective-memory-language');
    if (saved && translations[saved]) {
      return saved;
    }
    
    // Check browser language
    const browserLang = navigator.language.split('-')[0];
    if (translations[browserLang]) {
      return browserLang;
    }
    
    // Default to Turkish (primary language)
    return 'tr';
  }
  
  setLanguage(lang) {
    if (translations[lang]) {
      this.currentLanguage = lang;
      localStorage.setItem('collective-memory-language', lang);
      // Trigger re-render
      window.dispatchEvent(new CustomEvent('languageChanged', { detail: lang }));
    }
  }
  
  t(key, params = {}) {
    const keys = key.split('.');
    let value = this.translations[this.currentLanguage];
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        // Fallback to English
        value = this.translations.en;
        for (const fallbackKey of keys) {
          if (value && typeof value === 'object' && fallbackKey in value) {
            value = value[fallbackKey];
          } else {
            return key; // Return key if not found
          }
        }
        break;
      }
    }
    
    // Replace parameters
    if (typeof value === 'string' && Object.keys(params).length > 0) {
      for (const [param, replacement] of Object.entries(params)) {
        value = value.replace(new RegExp(`{{${param}}}`, 'g'), replacement);
      }
    }
    
    return value || key;
  }
  
  getCurrentLanguage() {
    return this.currentLanguage;
  }
  
  getAvailableLanguages() {
    return Object.keys(this.translations).map(code => ({
      code,
      name: code === 'tr' ? 'Türkçe' : 'English',
      flag: code === 'tr' ? '🇹🇷' : '🇺🇸'
    }));
  }
}

// Export singleton instance
export const i18n = new I18n();
export default i18n; 