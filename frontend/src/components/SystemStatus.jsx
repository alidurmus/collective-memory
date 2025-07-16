import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Activity, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  RefreshCw,
  Database,
  HardDrive,
  Cpu,
  MemoryStick,
  Network,
  Clock,
  TrendingUp,
  TrendingDown,
  Zap
} from 'lucide-react';
import { useQuery } from 'react-query';
import { systemAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const SystemStatus = ({ compact = false }) => {
  const [lastUpdate, setLastUpdate] = useState(new Date());
  
  const { data: systemStatus, isLoading, error, refetch } = useQuery(
    'systemStatus',
    systemAPI.getSystemStatus,
    {
      refetchInterval: 30000, // 30 saniye
      staleTime: 15000, // 15 saniye
      onSuccess: () => setLastUpdate(new Date())
    }
  );

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600 bg-green-50';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50';
      case 'error':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return CheckCircle;
      case 'warning':
        return AlertTriangle;
      case 'error':
        return XCircle;
      default:
        return Activity;
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

  const formatUptime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}sa ${minutes}dk ${secs}sn`;
    } else if (minutes > 0) {
      return `${minutes}dk ${secs}sn`;
    } else {
      return `${secs}sn`;
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const systemComponents = [
    {
      name: 'Veritabanı',
      status: systemStatus?.database?.status || 'unknown',
      details: systemStatus?.database?.details || 'Bağlantı kontrol ediliyor...',
      icon: Database,
      metrics: {
        'Dosya Sayısı': systemStatus?.database?.file_count || 0,
        'Boyut': formatBytes(systemStatus?.database?.size || 0),
        'Son Güncelleme': systemStatus?.database?.last_update || 'Bilinmiyor'
      }
    },
    {
      name: 'Arama Motoru',
      status: systemStatus?.search_engine?.status || 'unknown',
      details: systemStatus?.search_engine?.details || 'Arama motoru kontrol ediliyor...',
      icon: Zap,
      metrics: {
        'Ortalama Süre': `${systemStatus?.search_engine?.avg_response_time || 0}ms`,
        'Cache Hit Rate': `${systemStatus?.search_engine?.cache_hit_rate || 0}%`,
        'Toplam Arama': systemStatus?.search_engine?.total_searches || 0
      }
    },
    {
      name: 'Dosya İzleyici',
      status: systemStatus?.file_monitor?.status || 'unknown',
      details: systemStatus?.file_monitor?.details || 'Dosya izleyici kontrol ediliyor...',
      icon: HardDrive,
      metrics: {
        'İzlenen Klasör': systemStatus?.file_monitor?.watched_directories || 0,
        'Son Tarama': systemStatus?.file_monitor?.last_scan || 'Bilinmiyor',
        'Değişiklik Sayısı': systemStatus?.file_monitor?.changes_detected || 0
      }
    },
    {
      name: 'API Server',
      status: systemStatus?.api_server?.status || 'unknown',
      details: systemStatus?.api_server?.details || 'API server kontrol ediliyor...',
      icon: Network,
      metrics: {
        'Uptime': formatUptime(systemStatus?.api_server?.uptime || 0),
        'Aktif Bağlantı': systemStatus?.api_server?.active_connections || 0,
        'Request Rate': `${systemStatus?.api_server?.request_rate || 0}/dk`
      }
    }
  ];

  const resourceMetrics = [
    {
      name: 'CPU Kullanımı',
      value: systemStatus?.resources?.cpu_usage || 0,
      unit: '%',
      threshold: 80,
      icon: Cpu,
      trend: systemStatus?.resources?.cpu_trend || 'stable'
    },
    {
      name: 'Bellek Kullanımı',
      value: systemStatus?.resources?.memory_usage || 0,
      unit: '%',
      threshold: 85,
      icon: MemoryStick,
      trend: systemStatus?.resources?.memory_trend || 'stable'
    },
    {
      name: 'Disk Kullanımı',
      value: systemStatus?.resources?.disk_usage || 0,
      unit: '%',
      threshold: 90,
      icon: HardDrive,
      trend: systemStatus?.resources?.disk_trend || 'stable'
    },
    {
      name: 'Network I/O',
      value: systemStatus?.resources?.network_io || 0,
      unit: 'MB/s',
      threshold: 100,
      icon: Network,
      trend: systemStatus?.resources?.network_trend || 'stable'
    }
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-48">
        <LoadingSpinner size="md" text="Sistem durumu yükleniyor..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center">
          <XCircle className="h-5 w-5 text-red-600 mr-2" />
          <span className="text-red-800">Sistem durumu alınamadı: {error.message}</span>
          <button 
            onClick={() => refetch()}
            className="ml-auto text-red-600 hover:text-red-800"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
      </div>
    );
  }

  if (compact) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Sistem Durumu
          </h3>
          <div className="flex items-center space-x-2">
            <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(systemStatus?.overall_status)}`}>
              {React.createElement(getStatusIcon(systemStatus?.overall_status), { className: "h-3 w-3 mr-1" })}
              {getStatusText(systemStatus?.overall_status)}
            </div>
            <button 
              onClick={() => refetch()}
              className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          {resourceMetrics.map((metric, index) => (
            <div key={index} className="text-center">
              <div className="flex items-center justify-center mb-1">
                {React.createElement(metric.icon, { className: "h-4 w-4 text-gray-500" })}
              </div>
              <div className="text-sm font-medium text-gray-900 dark:text-white">
                {metric.value}{metric.unit}
              </div>
              <div className="text-xs text-gray-500">{metric.name}</div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Genel Sistem Durumu */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Sistem Durumu
          </h2>
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-500">
              Son güncelleme: {lastUpdate.toLocaleTimeString('tr-TR')}
            </div>
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(systemStatus?.overall_status)}`}>
              {React.createElement(getStatusIcon(systemStatus?.overall_status), { className: "h-4 w-4 mr-1" })}
              {getStatusText(systemStatus?.overall_status)}
            </div>
            <button 
              onClick={() => refetch()}
              className="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Sistem Bileşenleri */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {systemComponents.map((component, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center">
                  {React.createElement(component.icon, { className: "h-5 w-5 text-gray-600 dark:text-gray-400 mr-2" })}
                  <span className="font-medium text-gray-900 dark:text-white">{component.name}</span>
                </div>
                <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(component.status)}`}>
                  {React.createElement(getStatusIcon(component.status), { className: "h-3 w-3 mr-1" })}
                  {getStatusText(component.status)}
                </div>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">{component.details}</p>
              <div className="space-y-1">
                {Object.entries(component.metrics).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-xs">
                    <span className="text-gray-500">{key}:</span>
                    <span className="font-medium text-gray-900 dark:text-white">{value}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Kaynak Kullanımı */}
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Kaynak Kullanımı
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {resourceMetrics.map((metric, index) => (
              <div key={index} className="text-center">
                <div className="flex items-center justify-center mb-2">
                  {React.createElement(metric.icon, { className: "h-8 w-8 text-gray-600 dark:text-gray-400" })}
                </div>
                <div className="text-2xl font-bold text-gray-900 dark:text-white">
                  {metric.value}{metric.unit}
                </div>
                <div className="text-sm text-gray-500 mb-1">{metric.name}</div>
                <div className="flex items-center justify-center">
                  {metric.trend === 'up' && <TrendingUp className="h-4 w-4 text-red-500" />}
                  {metric.trend === 'down' && <TrendingDown className="h-4 w-4 text-green-500" />}
                  {metric.trend === 'stable' && <Activity className="h-4 w-4 text-gray-500" />}
                </div>
                <div className="mt-2">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all duration-300 ${
                        metric.value > metric.threshold ? 'bg-red-500' : 
                        metric.value > metric.threshold * 0.7 ? 'bg-yellow-500' : 
                        'bg-green-500'
                      }`}
                      style={{ width: `${Math.min(metric.value, 100)}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemStatus; 