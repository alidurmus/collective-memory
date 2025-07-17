import React, { useState } from 'react';
import { ChartBarIcon, ClockIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

const AnalyticsPage = () => {
  const [dateRange, setDateRange] = useState('7d');
  const [filterType, setFilterType] = useState('all');

  return (
    <div className="max-w-6xl mx-auto" data-testid="analytics-page">
      {/* Page Header */}
      <div className="mb-8" data-testid="analytics-header">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Analitik
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Sistem performansı ve kullanım istatistikleri
        </p>
      </div>

      {/* Filter Controls */}
      <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-lg mb-8" data-testid="analytics-filters">
        <div className="flex flex-wrap gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Tarih Aralığı
            </label>
            <select 
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
              data-testid="date-range-filter"
            >
              <option value="1d">Son 24 Saat</option>
              <option value="7d">Son 7 Gün</option>
              <option value="30d">Son 30 Gün</option>
              <option value="90d">Son 90 Gün</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Arama Türü
            </label>
            <select 
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
              data-testid="search-type-filter"
            >
              <option value="all">Tümü</option>
              <option value="basic">Temel Arama</option>
              <option value="semantic">Semantic Arama</option>
            </select>
          </div>
          <div className="flex items-end">
            <button
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              data-testid="export-analytics"
            >
              Verileri Dışa Aktar
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Cards */}
      <div className="grid md:grid-cols-4 gap-6 mb-8" data-testid="metrics-cards">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="total-searches-card">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <ChartBarIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Toplam Arama</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white" data-testid="total-searches-count">
                3,456
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="avg-response-card">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <ClockIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Ortalama Yanıt</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white" data-testid="avg-response-time">
                89ms
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="indexed-files-card">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <DocumentTextIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">İndeksli Dosya</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white" data-testid="indexed-files-count">
                1,245
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="cache-hit-card">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
              <ChartBarIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Cache Hit Rate</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white" data-testid="cache-hit-rate">
                87%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid md:grid-cols-2 gap-8 mb-8">
        {/* Search Trends Chart */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="search-trends-chart">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Arama Eğilimleri
          </h3>
          <div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="text-gray-500 dark:text-gray-400">
              Chart will be implemented here
            </p>
          </div>
        </div>

        {/* File Types Distribution */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="file-types-chart">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Dosya Türü Dağılımı
          </h3>
          <div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-700 rounded-lg">
            <p className="text-gray-500 dark:text-gray-400">
              Pie chart will be implemented here
            </p>
          </div>
        </div>
      </div>

      {/* Popular Search Terms */}
      <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="popular-searches">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Popüler Arama Terimleri
        </h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span className="text-gray-900 dark:text-white">Django</span>
            <span className="text-sm text-gray-500 dark:text-gray-400">145 arama</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span className="text-gray-900 dark:text-white">React</span>
            <span className="text-sm text-gray-500 dark:text-gray-400">98 arama</span>
          </div>
          <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span className="text-gray-900 dark:text-white">API</span>
            <span className="text-sm text-gray-500 dark:text-gray-400">87 arama</span>
          </div>
        </div>
      </div>

      {/* System Resources */}
      <div className="mt-8 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg" data-testid="system-resources">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Sistem Kaynak Kullanımı
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">CPU Kullanımı</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">25%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-blue-600 h-2 rounded-full" style={{ width: '25%' }}></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Bellek Kullanımı</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">67%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-green-600 h-2 rounded-full" style={{ width: '67%' }}></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between mb-2">
              <span className="text-sm text-gray-600 dark:text-gray-400">Disk Kullanımı</span>
              <span className="text-sm font-medium text-gray-900 dark:text-white">43%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-purple-600 h-2 rounded-full" style={{ width: '43%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage; 