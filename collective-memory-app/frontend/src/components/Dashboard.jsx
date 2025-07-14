import React from 'react'
import { motion } from 'framer-motion'
import { 
  Search, 
  FileText, 
  Database, 
  Activity, 
  TrendingUp, 
  Clock,
  Folder,
  Zap,
  BarChart3,
  Settings
} from 'lucide-react'
import { useSystemStats, useIndexingStatus } from '../hooks/useSystemStatus'
import { useSearch } from '../hooks/useSearch'
import LoadingSpinner from './LoadingSpinner'
import SearchPanel from './SearchPanel'
import StatsCard from './StatsCard'
import RecentActivity from './RecentActivity'
import QuickActions from './QuickActions'

const Dashboard = () => {
  const { data: stats, isLoading: statsLoading } = useSystemStats()
  const { data: indexingStatus } = useIndexingStatus()
  const { searchHistory } = useSearch()

  const dashboardStats = [
    {
      title: 'Toplam Dosya',
      value: stats?.totalFiles?.toLocaleString() || '0',
      change: stats?.filesChange || '+0',
      changeType: 'increase',
      icon: FileText,
      color: 'blue',
      description: 'İndekslenen dosya sayısı'
    },
    {
      title: 'İndeks Boyutu',
      value: stats?.indexSize || '0 MB',
      change: stats?.indexSizeChange || '+0 MB',
      changeType: 'increase',
      icon: Database,
      color: 'green',
      description: 'Toplam indeks veri boyutu'
    },
    {
      title: 'Arama Performansı',
      value: stats?.averageSearchTime || '0ms',
      change: stats?.searchTimeChange || '0ms',
      changeType: stats?.searchTimeChange?.startsWith('-') ? 'increase' : 'decrease',
      icon: Zap,
      color: 'purple',
      description: 'Ortalama arama süresi'
    },
    {
      title: 'Aktif İzleme',
      value: stats?.watchedDirectories || '0',
      change: stats?.watchedDirChange || '+0',
      changeType: 'increase',
      icon: Folder,
      color: 'orange',
      description: 'İzlenen klasör sayısı'
    }
  ]

  const recentSearches = searchHistory.slice(0, 5)

  if (statsLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" text="Dashboard yükleniyor..." />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex flex-col sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Dashboard
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Collective Memory sistem durumu ve genel bakış
          </p>
        </div>
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="mt-4 sm:mt-0 flex items-center space-x-3"
        >
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Son güncelleme: {new Date().toLocaleTimeString('tr-TR')}
          </div>
          {indexingStatus?.isIndexing && (
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-blue-600 dark:text-blue-400">
                İndeksleniyor...
              </span>
            </div>
          )}
        </motion.div>
      </motion.div>

      {/* Stats Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {dashboardStats.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * index }}
          >
            <StatsCard {...stat} />
          </motion.div>
        ))}
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Search Panel */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="lg:col-span-2"
        >
          <SearchPanel />
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          <QuickActions />
        </motion.div>
      </div>

      {/* Bottom Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          <RecentActivity />
        </motion.div>

        {/* System Health */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Sistem Sağlığı
            </h3>
            <Activity className="w-5 h-5 text-green-500" />
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">CPU Kullanımı</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                  <div className="h-2 bg-green-500 rounded-full" style={{ width: `${stats?.cpuUsage || 0}%` }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {stats?.cpuUsage || 0}%
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Bellek Kullanımı</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                  <div className="h-2 bg-blue-500 rounded-full" style={{ width: `${stats?.memoryUsage || 0}%` }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {stats?.memoryUsage || 0}%
                </span>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600 dark:text-gray-400">Disk Kullanımı</span>
              <div className="flex items-center space-x-2">
                <div className="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full">
                  <div className="h-2 bg-orange-500 rounded-full" style={{ width: `${stats?.diskUsage || 0}%` }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900 dark:text-gray-100">
                  {stats?.diskUsage || 0}%
                </span>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Sistem {stats?.uptime || '0'} süredir çalışıyor
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Dashboard 