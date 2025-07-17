import React from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  Home, 
  Search, 
  BarChart3, 
  Settings, 
  FileText, 
  Database, 
  Activity,
  Clock,
  Folder,
  Zap
} from 'lucide-react'
import { useSystemStats } from '../hooks/useSystemStatus'

const Sidebar = () => {
  const location = useLocation()
  const { data: stats } = useSystemStats()

  const navigationItems = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: Home,
      description: 'Genel bakış ve özet bilgiler'
    },
    {
      name: 'Arama',
      href: '/search',
      icon: Search,
      description: 'Gelişmiş arama ve filtreleme',
      badge: stats?.totalFiles ? `${stats.totalFiles.toLocaleString()}` : null
    },
    {
      name: 'Analitik',
      href: '/analytics',
      icon: BarChart3,
      description: 'Kullanım istatistikleri ve raporlar'
    },
    {
      name: 'Ayarlar',
      href: '/settings',
      icon: Settings,
      description: 'Sistem konfigürasyonu'
    }
  ]

  const quickStats = [
    {
      label: 'Toplam Dosya',
      value: stats?.totalFiles?.toLocaleString() || '0',
      icon: FileText,
      color: 'text-blue-600 dark:text-blue-400'
    },
    {
      label: 'İndeks Boyutu',
      value: stats?.indexSize || '0 MB',
      icon: Database,
      color: 'text-green-600 dark:text-green-400'
    },
    {
      label: 'Son Arama',
      value: stats?.lastSearchTime || 'Yok',
      icon: Clock,
      color: 'text-purple-600 dark:text-purple-400'
    },
    {
      label: 'Aktif İzleme',
      value: stats?.watchedDirectories || '0',
      icon: Folder,
      color: 'text-orange-600 dark:text-orange-400'
    }
  ]

  return (
    <div className="flex flex-col h-full">
      {/* Logo Section */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-3">
          <motion.div
            whileHover={{ scale: 1.1 }}
            className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-xl flex items-center justify-center"
          >
            <Zap className="w-5 h-5 text-white" />
          </motion.div>
          <div>
            <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100">
              Collective Memory
            </h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Bilgi Yönetim Sistemi
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        <div className="mb-6">
          <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
            Navigasyon
          </h3>
          {navigationItems.map((item) => {
            const isActive = location.pathname === item.href
            const Icon = item.icon

            return (
              <motion.div
                key={item.name}
                whileHover={{ x: 4 }}
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
              >
                <NavLink
                  to={item.href}
                  className={`group flex items-center justify-between px-3 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                    isActive
                      ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className={`w-5 h-5 ${isActive ? 'text-primary-600 dark:text-primary-400' : 'text-gray-500 dark:text-gray-400'}`} />
                    <div>
                      <span className="block">{item.name}</span>
                      <span className="text-xs text-gray-500 dark:text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300">
                        {item.description}
                      </span>
                    </div>
                  </div>
                  {item.badge && (
                    <span className="px-2 py-1 text-xs bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full">
                      {item.badge}
                    </span>
                  )}
                </NavLink>
              </motion.div>
            )
          })}
        </div>
      </nav>

      {/* Quick Stats */}
      <div className="px-4 py-6 border-t border-gray-200 dark:border-gray-700">
        <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
          Hızlı İstatistikler
        </h3>
        <div className="space-y-3">
          {quickStats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between px-3 py-2 bg-gray-50 dark:bg-gray-800 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 ${stat.color}`} />
                  <span className="text-xs text-gray-600 dark:text-gray-400">
                    {stat.label}
                  </span>
                </div>
                <span className="text-xs font-medium text-gray-900 dark:text-gray-100">
                  {stat.value}
                </span>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* System Status */}
      <div className="px-4 py-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4 text-green-500" />
            <span className="text-xs text-gray-600 dark:text-gray-400">
              Sistem Durumu
            </span>
          </div>
          <span className="status-badge success text-xs">
            Çalışıyor
          </span>
        </div>
      </div>
    </div>
  )
}

export default Sidebar 