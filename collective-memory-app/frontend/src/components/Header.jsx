import React from 'react'
import { motion } from 'framer-motion'
import { 
  Menu, 
  X, 
  Sun, 
  Moon, 
  Search, 
  Bell, 
  Settings, 
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react'

const Header = ({ 
  toggleSidebar, 
  toggleDarkMode, 
  darkMode, 
  sidebarOpen, 
  systemStatus 
}) => {
  const getStatusIcon = () => {
    if (!systemStatus) return <Clock className="w-4 h-4" />
    
    switch (systemStatus.status) {
      case 'healthy':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />
      case 'error':
        return <AlertTriangle className="w-4 h-4 text-red-500" />
      default:
        return <Activity className="w-4 h-4 text-blue-500" />
    }
  }

  const getStatusBadge = () => {
    if (!systemStatus) return null

    const statusConfig = {
      healthy: { text: 'Sistem Çalışıyor', class: 'status-badge success' },
      warning: { text: 'Uyarı', class: 'status-badge warning' },
      error: { text: 'Hata', class: 'status-badge error' },
      indexing: { text: 'İndeksleniyor', class: 'status-badge info' },
    }

    const config = statusConfig[systemStatus.status] || statusConfig.healthy

    return (
      <div className="flex items-center space-x-2">
        {getStatusIcon()}
        <span className={config.class}>
          {config.text}
        </span>
      </div>
    )
  }

  return (
    <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 h-16 flex items-center justify-between px-6 shadow-sm">
      {/* Left Section */}
      <div className="flex items-center space-x-4">
        {/* Sidebar Toggle */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={toggleSidebar}
          className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          aria-label={sidebarOpen ? 'Sidebar\'ı Kapat' : 'Sidebar\'ı Aç'}
        >
          {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </motion.button>

        {/* Logo and Title */}
        <div className="flex items-center space-x-3">
          <motion.div
            whileHover={{ rotate: 360 }}
            transition={{ duration: 0.5 }}
            className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center"
          >
            <Search className="w-4 h-4 text-white" />
          </motion.div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Collective Memory
            </h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              v2.1 Dashboard
            </p>
          </div>
        </div>
      </div>

      {/* Center Section - Quick Search */}
      <div className="hidden md:flex flex-1 max-w-lg mx-8">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Hızlı arama..."
            className="w-full pl-10 pr-4 py-2 text-sm bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center space-x-4">
        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="hidden lg:flex"
        >
          {getStatusBadge()}
        </motion.div>

        {/* Notifications */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="relative p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          aria-label="Bildirimler"
        >
          <Bell className="w-5 h-5" />
          {systemStatus?.notifications > 0 && (
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
            >
              {systemStatus.notifications > 9 ? '9+' : systemStatus.notifications}
            </motion.span>
          )}
        </motion.button>

        {/* Dark Mode Toggle */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={toggleDarkMode}
          className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          aria-label={darkMode ? 'Açık Tema' : 'Koyu Tema'}
        >
          {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </motion.button>

        {/* Settings */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="p-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          aria-label="Ayarlar"
        >
          <Settings className="w-5 h-5" />
        </motion.button>
      </div>
    </header>
  )
}

export default Header 