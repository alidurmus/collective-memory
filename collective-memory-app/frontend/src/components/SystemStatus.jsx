import React, { useState, useEffect } from 'react';
import '../styles/context7.css';

const SystemStatus = ({ stats = {}, embedded = false }) => {
  const [detailedStats, setDetailedStats] = useState({});
  const [isExpanded, setIsExpanded] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    if (!embedded) {
      fetchDetailedStats();
    }
  }, [embedded]);

  const fetchDetailedStats = async () => {
    setRefreshing(true);
    try {
      const response = await fetch('/api/system/stats');
      const data = await response.json();
      if (data.success) {
        setDetailedStats(data.data);
      }
    } catch (error) {
      console.error('Detaylı sistem bilgileri alınamadı:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleRefresh = () => {
    fetchDetailedStats();
  };

  const getStatusInfo = (status) => {
    switch (status) {
      case 'healthy':
        return {
          label: 'Sağlıklı',
          color: 'context7-status--success',
          icon: '✅',
          description: 'Sistem normal çalışıyor'
        };
      case 'warning':
        return {
          label: 'Uyarı',
          color: 'context7-status--warning', 
          icon: '⚠️',
          description: 'Dikkat edilmesi gereken durumlar var'
        };
      case 'error':
        return {
          label: 'Hata',
          color: 'context7-status--error',
          icon: '❌',
          description: 'Sistem hatası mevcut'
        };
      default:
        return {
          label: 'Bilinmiyor',
          color: 'context7-status--info',
          icon: '❓',
          description: 'Sistem durumu belirlenemiyor'
        };
    }
  };

  const formatUptime = (uptime) => {
    if (!uptime) return '0:00:00';
    
    const parts = uptime.split(':');
    if (parts.length === 3) {
      const hours = parseInt(parts[0]);
      const minutes = parseInt(parts[1]);
      const seconds = parseInt(parts[2].split('.')[0]);
      
      if (hours > 0) {
        return `${hours} saat ${minutes} dakika`;
      } else if (minutes > 0) {
        return `${minutes} dakika ${seconds} saniye`;
      } else {
        return `${seconds} saniye`;
      }
    }
    return uptime;
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return '0 B';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
  };

  const statusInfo = getStatusInfo(stats.status);

  const metricsData = [
    {
      label: 'İndekslenen Dosyalar',
      value: stats.file_count?.toLocaleString('tr-TR') || '0',
      icon: '📁',
      change: detailedStats.file_growth || '+0',
      changeType: 'positive'
    },
    {
      label: 'Toplam Arama',
      value: stats.search_count?.toLocaleString('tr-TR') || '0',
      icon: '🔍',
      change: detailedStats.search_growth || '+0',
      changeType: 'positive'
    },
    {
      label: 'Çalışma Süresi',
      value: formatUptime(stats.uptime),
      icon: '⏱️',
      change: 'Kesintisiz',
      changeType: 'neutral'
    },
    {
      label: 'İndeks Boyutu',
      value: formatFileSize(detailedStats.index_size),
      icon: '💾',
      change: detailedStats.size_growth || '+0 MB',
      changeType: 'neutral'
    }
  ];

  const performanceMetrics = [
    {
      label: 'Ortalama Arama Süresi',
      value: detailedStats.avg_search_time ? `${detailedStats.avg_search_time}ms` : '<50ms',
      target: '<100ms',
      status: (detailedStats.avg_search_time || 50) < 100 ? 'good' : 'warning'
    },
    {
      label: 'Bellek Kullanımı',
      value: detailedStats.memory_usage ? `${detailedStats.memory_usage}MB` : '~150MB',
      target: '<500MB',
      status: (detailedStats.memory_usage || 150) < 300 ? 'good' : 'warning'
    },
    {
      label: 'Cache Hit Oranı',
      value: detailedStats.cache_hit_rate ? `%${detailedStats.cache_hit_rate}` : '%85',
      target: '>80%',
      status: (detailedStats.cache_hit_rate || 85) > 80 ? 'good' : 'warning'
    }
  ];

  const containerClass = embedded 
    ? 'space-y-4' 
    : 'context7-card p-6';

  return (
    <div className={`${containerClass} turkish-ui`}>
      
      {/* Ana Durum Başlığı */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{statusInfo.icon}</span>
          <div>
            <h3 className="context7-heading context7-heading--sm">
              Sistem Durumu
            </h3>
            <p className="context7-text context7-text--muted text-sm">
              {statusInfo.description}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className={`context7-status ${statusInfo.color}`}>
            {statusInfo.label}
          </span>
          {!embedded && (
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="context7-button context7-button--secondary text-sm"
              aria-label="Sistem durumunu yenile"
            >
              {refreshing ? (
                <div className="flex items-center">
                  <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-current mr-1"></div>
                  <span>Yenileniyor</span>
                </div>
              ) : (
                <span>🔄 Yenile</span>
              )}
            </button>
          )}
        </div>
      </div>

      {/* Ana Metrikler Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {metricsData.map((metric, index) => (
          <div key={index} className="context7-card p-4 text-center context7-interactive">
            <div className="text-2xl mb-2">{metric.icon}</div>
            <div className="context7-heading context7-heading--sm context7-gradient-text">
              {metric.value}
            </div>
            <p className="context7-text context7-text--muted text-xs mb-1">
              {metric.label}
            </p>
            {metric.change && (
              <span className={`text-xs ${
                metric.changeType === 'positive' ? 'text-green-600' :
                metric.changeType === 'negative' ? 'text-red-600' : 'text-gray-500'
              }`}>
                {metric.change}
              </span>
            )}
          </div>
        ))}
      </div>

      {/* Performans Metrikleri (Sadece Full Görünümde) */}
      {!embedded && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="context7-heading context7-heading--sm">
              Performans Metrikleri
            </h4>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="context7-button context7-button--secondary text-sm"
            >
              {isExpanded ? 'Daralt' : 'Genişlet'}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {performanceMetrics.map((metric, index) => (
              <div key={index} className="context7-card p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="context7-text text-sm font-medium">
                    {metric.label}
                  </span>
                  <span className={`w-3 h-3 rounded-full ${
                    metric.status === 'good' ? 'bg-green-400' : 'bg-yellow-400'
                  }`}></span>
                </div>
                <div className="context7-heading context7-heading--sm">
                  {metric.value}
                </div>
                <p className="context7-text context7-text--muted text-xs">
                  Hedef: {metric.target}
                </p>
              </div>
            ))}
          </div>

          {/* Detaylı Bilgiler (Genişletildiğinde) */}
          {isExpanded && (
            <div className="context7-card p-4 mt-4">
              <h5 className="context7-heading context7-heading--sm mb-3">
                Detaylı Sistem Bilgileri
              </h5>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="context7-text context7-text--muted">Son Arama:</span>
                  <p className="context7-text">
                    {stats.last_search ? 
                      new Date(stats.last_search).toLocaleString('tr-TR') : 
                      'Henüz arama yapılmadı'
                    }
                  </p>
                </div>
                <div>
                  <span className="context7-text context7-text--muted">İndeksleme Durumu:</span>
                  <p className="context7-text">
                    {stats.is_indexing ? 'Devam ediyor' : 'Tamamlandı'}
                  </p>
                </div>
                <div>
                  <span className="context7-text context7-text--muted">Bildirim Sayısı:</span>
                  <p className="context7-text">
                    {stats.notifications || 0}
                  </p>
                </div>
                <div>
                  <span className="context7-text context7-text--muted">API Durumu:</span>
                  <p className="context7-text">
                    Aktif ve çalışıyor
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Sistem Tavsiyeleri */}
      {!embedded && detailedStats.recommendations && (
        <div className="context7-card p-4 border-l-4 border-blue-500 bg-blue-50">
          <h5 className="context7-heading context7-heading--sm text-blue-800 mb-2">
            💡 Sistem Tavsiyeleri
          </h5>
          <ul className="space-y-1">
            {detailedStats.recommendations.map((recommendation, index) => (
              <li key={index} className="context7-text text-blue-700 text-sm">
                • {recommendation}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SystemStatus; 