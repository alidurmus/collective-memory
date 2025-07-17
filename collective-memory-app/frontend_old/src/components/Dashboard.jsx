import React, { useState, useEffect } from 'react';
import Header from './Header';
import SearchInterface from './SearchInterface';
import SystemStatus from './SystemStatus';
import Analytics from './Analytics';
import '../styles/context7.css';

const Dashboard = () => {
  const [systemStats, setSystemStats] = useState({
    file_count: 0,
    search_count: 0,
    uptime: '0:00:00',
    status: 'healthy'
  });
  
  const [recentActivity, setRecentActivity] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchSystemStats();
    fetchRecentActivity();
    
    // Pollling için interval setup
    const interval = setInterval(() => {
      fetchSystemStats();
    }, 30000); // 30 saniye
    
    return () => clearInterval(interval);
  }, []);

  const fetchSystemStats = async () => {
    try {
      const response = await fetch('/api/system/status');
      const data = await response.json();
      if (data.success) {
        setSystemStats(data.data);
      }
    } catch (error) {
      console.error('Sistem durumu alınamadı:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchRecentActivity = async () => {
    try {
      const response = await fetch('/api/system/stats');
      const data = await response.json();
      if (data.success && data.data.recent_activity) {
        setRecentActivity(data.data.recent_activity);
      }
    } catch (error) {
      console.error('Son aktiviteler alınamadı:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'context7-status--success';
      case 'warning':
        return 'context7-status--warning';
      case 'error':
        return 'context7-status--error';
      default:
        return 'context7-status--info';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'healthy':
        return 'Sağlıklı';
      case 'warning':
        return 'Uyarı';
      case 'error':
        return 'Hata';
      default:
        return 'Bilinmiyor';
    }
  };

  if (isLoading) {
    return (
      <div className="context7-dashboard turkish-ui">
        <div className="min-h-screen flex items-center justify-center">
          <div className="context7-card p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
            <p className="context7-text">Sistem yükleniyor...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="context7-dashboard turkish-ui">
      <div className="min-h-screen p-6">
        {/* Header */}
        <Header />
        
        {/* Ana İçerik Grid */}
        <div className="max-w-7xl mx-auto mt-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            
            {/* Hoş Geldin Kartı */}
            <div className="lg:col-span-2">
              <div className="context7-card p-6 context7-shine">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h1 className="context7-heading context7-heading--lg context7-gradient-text">
                      Collective Memory
                    </h1>
                    <p className="context7-text mt-2">
                      Akıllı bağlam yönetimi ve arama sisteminiz
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={`context7-status ${getStatusColor(systemStats.status)}`}>
                      {getStatusText(systemStats.status)}
                    </span>
                    <p className="context7-text context7-text--muted text-sm mt-2">
                      Çalışma Süresi: {systemStats.uptime}
                    </p>
                  </div>
                </div>
                
                {/* Hızlı İstatistikler */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                  <div className="text-center">
                    <div className="context7-heading context7-heading--md context7-gradient-text">
                      {systemStats.file_count?.toLocaleString('tr-TR') || 0}
                    </div>
                    <p className="context7-text context7-text--muted text-sm">Dosya Sayısı</p>
                  </div>
                  <div className="text-center">
                    <div className="context7-heading context7-heading--md context7-gradient-text">
                      {systemStats.search_count?.toLocaleString('tr-TR') || 0}
                    </div>
                    <p className="context7-text context7-text--muted text-sm">Arama Sayısı</p>
                  </div>
                  <div className="text-center">
                    <div className="context7-heading context7-heading--md context7-gradient-text">
                      {systemStats.index_size ? `${(systemStats.index_size / 1024 / 1024).toFixed(1)}MB` : '0MB'}
                    </div>
                    <p className="context7-text context7-text--muted text-sm">İndeks Boyutu</p>
                  </div>
                  <div className="text-center">
                    <div className="context7-heading context7-heading--md context7-gradient-text">
                      {systemStats.performance?.avg_search_time ? `${systemStats.performance.avg_search_time}ms` : '<50ms'}
                    </div>
                    <p className="context7-text context7-text--muted text-sm">Ortalama Arama</p>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Hızlı Eylemler */}
            <div className="space-y-4">
              <div className="context7-card p-6">
                <h3 className="context7-heading context7-heading--sm mb-4">Hızlı Eylemler</h3>
                <div className="space-y-3">
                  <button className="context7-button w-full context7-interactive">
                    <span className="mr-2">🔍</span>
                    Akıllı Arama
                  </button>
                  <button className="context7-button context7-button--secondary w-full context7-interactive">
                    <span className="mr-2">📊</span>
                    Analitik Raporlar
                  </button>
                  <button className="context7-button context7-button--secondary w-full context7-interactive">
                    <span className="mr-2">⚙️</span>
                    Sistem Ayarları
                  </button>
                </div>
              </div>
              
              {/* Son Aktiviteler */}
              <div className="context7-card p-6">
                <h3 className="context7-heading context7-heading--sm mb-4">Son Aktiviteler</h3>
                <div className="space-y-3 max-h-48 overflow-y-auto">
                  {recentActivity.length > 0 ? (
                    recentActivity.map((activity, index) => (
                      <div key={index} className="flex items-center text-sm">
                        <div className="w-2 h-2 bg-blue-400 rounded-full mr-3 flex-shrink-0"></div>
                        <div className="flex-1">
                          <p className="context7-text">{activity.description}</p>
                          <p className="context7-text context7-text--muted text-xs">
                            {new Date(activity.timestamp).toLocaleTimeString('tr-TR')}
                          </p>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="context7-text context7-text--muted text-sm">
                      Henüz aktivite kaydı bulunmuyor
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
          
          {/* Ana Özellikler Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Arama Arayüzü */}
            <div className="context7-card p-6">
              <div className="flex items-center mb-4">
                <span className="text-2xl mr-3">🔍</span>
                <h2 className="context7-heading context7-heading--md">Akıllı Arama</h2>
              </div>
              <SearchInterface embedded={true} />
            </div>
            
            {/* Sistem Durumu */}
            <div className="context7-card p-6">
              <div className="flex items-center mb-4">
                <span className="text-2xl mr-3">📊</span>
                <h2 className="context7-heading context7-heading--md">Sistem Durumu</h2>
              </div>
              <SystemStatus stats={systemStats} />
            </div>
          </div>
          
          {/* Alt Bölüm - Analytics */}
          <div className="mt-6">
            <div className="context7-card p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">📈</span>
                  <h2 className="context7-heading context7-heading--md">Performans Analitikleri</h2>
                </div>
                <button className="context7-button context7-button--secondary">
                  Detaylı Rapor
                </button>
              </div>
              <Analytics />
            </div>
          </div>
        </div>
        
        {/* Alt Bilgi */}
        <footer className="max-w-7xl mx-auto mt-12 text-center">
          <p className="context7-text context7-text--muted">
            Collective Memory v2.1 - Context7 Framework ile güçlendirilmiştir
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Dashboard; 