import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Search, 
  FileText, 
  Clock,
  Activity,
  Download,
  RefreshCw,
  Calendar
} from 'lucide-react'
import { useQuery } from 'react-query'
import { analyticsAPI } from '../services/api'
import LoadingSpinner from './LoadingSpinner'

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d')
  
  const { data: searchAnalytics, isLoading: searchLoading } = useQuery(
    ['searchAnalytics', timeRange],
    () => analyticsAPI.getSearchAnalytics(timeRange),
    { staleTime: 5 * 60 * 1000 }
  )

  const { data: popularQueries, isLoading: queriesLoading } = useQuery(
    'popularQueries',
    () => analyticsAPI.getPopularQueries(10),
    { staleTime: 10 * 60 * 1000 }
  )

  const { data: fileAccess, isLoading: accessLoading } = useQuery(
    ['fileAccess', timeRange],
    () => analyticsAPI.getFileAccessPatterns(timeRange),
    { staleTime: 5 * 60 * 1000 }
  )

  const { data: performance, isLoading: perfLoading } = useQuery(
    ['performance', timeRange],
    () => analyticsAPI.getPerformanceMetrics(timeRange),
    { staleTime: 2 * 60 * 1000 }
  )

  const analyticsCards = [
    {
      title: 'Toplam Arama',
      value: searchAnalytics?.totalSearches || '0',
      change: searchAnalytics?.searchChange || '0%',
      changeType: 'increase',
      icon: Search,
      color: 'blue'
    },
    {
      title: 'Benzersiz Kullanıcı',
      value: searchAnalytics?.uniqueUsers || '0',
      change: searchAnalytics?.userChange || '0%',
      changeType: 'increase',
      icon: Users,
      color: 'green'
    },
    {
      title: 'Ortalama Yanıt Süresi',
      value: performance?.averageResponseTime || '0ms',
      change: performance?.responseTimeChange || '0%',
      changeType: performance?.responseTimeChange?.startsWith('-') ? 'increase' : 'decrease',
      icon: Clock,
      color: 'purple'
    },
    {
      title: 'En Çok Erişilen',
      value: fileAccess?.topAccessedCount || '0',
      change: fileAccess?.accessChange || '0%',
      changeType: 'increase',
      icon: FileText,
      color: 'orange'
    }
  ]

  const timeRanges = [
    { value: '24h', label: 'Son 24 Saat' },
    { value: '7d', label: 'Son 7 Gün' },
    { value: '30d', label: 'Son 30 Gün' },
    { value: '90d', label: 'Son 90 Gün' }
  ]

  if (searchLoading || queriesLoading || accessLoading || perfLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" text="Analitik veriler yükleniyor..." />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Analitik ve Raporlar
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Sistem kullanımı ve performans metrikleri
          </p>
        </div>
        
        <div className="mt-4 sm:mt-0 flex items-center space-x-3">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            {timeRanges.map((range) => (
              <option key={range.value} value={range.value}>
                {range.label}
              </option>
            ))}
          </select>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="btn-secondary flex items-center space-x-2"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Yenile</span>
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="btn-primary flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Rapor İndir</span>
          </motion.button>
        </div>
      </motion.div>

      {/* Analytics Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {analyticsCards.map((card, index) => {
          const Icon = card.icon
          const colorClasses = {
            blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400',
            green: 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400',
            purple: 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400',
            orange: 'bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400'
          }

          return (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              className="card p-6"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-lg ${colorClasses[card.color]}`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div className={`flex items-center text-sm ${
                  card.changeType === 'increase' 
                    ? 'text-green-600 dark:text-green-400' 
                    : 'text-red-600 dark:text-red-400'
                }`}>
                  <TrendingUp className="w-3 h-3 mr-1" />
                  {card.change}
                </div>
              </div>
              
              <div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-1">
                  {card.value}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {card.title}
                </p>
              </div>
            </motion.div>
          )
        })}
      </motion.div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Search Trends */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Arama Trendleri
            </h3>
            <BarChart3 className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          </div>
          
          <div className="h-64 flex items-center justify-center bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div className="text-center">
              <Activity className="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-500 dark:text-gray-400">
                Grafik özelliği yakında eklenecek
              </p>
            </div>
          </div>
        </motion.div>

        {/* Performance Metrics */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Performans Metrikleri
            </h3>
            <Clock className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Ortalama Arama Süresi</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                  <div className="h-2 bg-green-500 rounded-full" style={{ width: '75%' }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {performance?.averageSearchTime || '120ms'}
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">İndeksleme Hızı</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                  <div className="h-2 bg-blue-500 rounded-full" style={{ width: '60%' }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {performance?.indexingSpeed || '850 files/min'}
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Önbellek Hit Oranı</span>
              <div className="flex items-center space-x-2">
                <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                  <div className="h-2 bg-purple-500 rounded-full" style={{ width: '90%' }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {performance?.cacheHitRate || '89%'}
                </span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Popular Queries and File Access */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Popular Queries */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Popüler Aramalar
            </h3>
            <Search className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          </div>
          
          <div className="space-y-3">
            {(popularQueries || [
              { query: 'Django hata çözümü', count: 43, change: '+12%' },
              { query: 'React component', count: 38, change: '+8%' },
              { query: 'Python script', count: 32, change: '+5%' },
              { query: 'Context7 framework', count: 28, change: '+15%' },
              { query: 'Database migration', count: 25, change: '+3%' }
            ]).map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {item.query}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {item.count} arama
                  </p>
                </div>
                <span className="text-xs text-green-600 dark:text-green-400">
                  {item.change}
                </span>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Most Accessed Files */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              En Çok Erişilen Dosyalar
            </h3>
            <FileText className="w-5 h-5 text-primary-600 dark:text-primary-400" />
          </div>
          
          <div className="space-y-3">
            {(fileAccess?.topFiles || [
              { name: 'README.md', path: '/project/', access: 156, type: 'md' },
              { name: 'main.py', path: '/src/', access: 134, type: 'py' },
              { name: 'config.json', path: '/config/', access: 89, type: 'json' },
              { name: 'styles.css', path: '/assets/', access: 76, type: 'css' },
              { name: 'api-docs.md', path: '/docs/', access: 65, type: 'md' }
            ]).map((file, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: 10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div className="flex items-center space-x-3 flex-1">
                  <FileText className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                      {file.path}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100">
                    {file.access}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    erişim
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Analytics 