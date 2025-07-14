import React from 'react'
import { motion } from 'framer-motion'
import { 
  Search, 
  FileText, 
  RefreshCw, 
  Download, 
  Activity,
  Clock,
  User,
  Eye
} from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { tr } from 'date-fns/locale'

const RecentActivity = () => {
  // Mock data - gerçek uygulamada API'den gelecek
  const activities = [
    {
      id: 1,
      type: 'search',
      description: 'Django hata çözümü arandı',
      user: 'Sistem',
      timestamp: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
      details: '43 sonuç bulundu',
      icon: Search
    },
    {
      id: 2,
      type: 'file_added',
      description: 'Yeni dosya eklendi',
      user: 'Sistem',
      timestamp: new Date(Date.now() - 15 * 60 * 1000), // 15 minutes ago
      details: 'collective-memory.md',
      icon: FileText
    },
    {
      id: 3,
      type: 'reindex',
      description: 'Yeniden indeksleme tamamlandı',
      user: 'Sistem',
      timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
      details: '1,234 dosya işlendi',
      icon: RefreshCw
    },
    {
      id: 4,
      type: 'export',
      description: 'Arama sonuçları dışa aktarıldı',
      user: 'Kullanıcı',
      timestamp: new Date(Date.now() - 45 * 60 * 1000), // 45 minutes ago
      details: 'search-result.md',
      icon: Download
    },
    {
      id: 5,
      type: 'search',
      description: 'Context7 ERP modülleri arandı',
      user: 'Sistem',
      timestamp: new Date(Date.now() - 60 * 60 * 1000), // 1 hour ago
      details: '52 sonuç bulundu',
      icon: Search
    }
  ]

  const getActivityColor = (type) => {
    const colors = {
      search: 'text-blue-600 dark:text-blue-400',
      file_added: 'text-green-600 dark:text-green-400',
      reindex: 'text-purple-600 dark:text-purple-400',
      export: 'text-orange-600 dark:text-orange-400',
      default: 'text-gray-600 dark:text-gray-400'
    }
    return colors[type] || colors.default
  }

  const getActivityBgColor = (type) => {
    const colors = {
      search: 'bg-blue-50 dark:bg-blue-900/20',
      file_added: 'bg-green-50 dark:bg-green-900/20',
      reindex: 'bg-purple-50 dark:bg-purple-900/20',
      export: 'bg-orange-50 dark:bg-orange-900/20',
      default: 'bg-gray-50 dark:bg-gray-900/20'
    }
    return colors[type] || colors.default
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Son Aktiviteler
        </h3>
        <Activity className="w-5 h-5 text-primary-600 dark:text-primary-400" />
      </div>

      <div className="space-y-4">
        {activities.map((activity, index) => {
          const Icon = activity.icon
          const activityColor = getActivityColor(activity.type)
          const activityBgColor = getActivityBgColor(activity.type)

          return (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors duration-200"
            >
              {/* Icon */}
              <div className={`p-2 rounded-lg ${activityBgColor}`}>
                <Icon className={`w-4 h-4 ${activityColor}`} />
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                    {activity.description}
                  </p>
                  <div className="flex items-center space-x-1 text-xs text-gray-500 dark:text-gray-400">
                    <Clock className="w-3 h-3" />
                    <span>
                      {formatDistanceToNow(activity.timestamp, { 
                        addSuffix: true, 
                        locale: tr 
                      })}
                    </span>
                  </div>
                </div>

                <div className="mt-1 flex items-center justify-between">
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {activity.details}
                  </p>
                  <div className="flex items-center space-x-1 text-xs text-gray-400 dark:text-gray-500">
                    <User className="w-3 h-3" />
                    <span>{activity.user}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* View All Button */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700"
      >
        <button className="w-full flex items-center justify-center space-x-2 py-2 text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 transition-colors">
          <Eye className="w-4 h-4" />
          <span>Tüm aktiviteleri görüntüle</span>
        </button>
      </motion.div>

      {/* Activity Summary */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div className="text-lg font-bold text-gray-900 dark:text-gray-100">
            {activities.filter(a => a.type === 'search').length}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Bu saatte arama
          </div>
        </div>
        <div className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <div className="text-lg font-bold text-gray-900 dark:text-gray-100">
            {activities.filter(a => a.type === 'file_added').length}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Yeni dosya
          </div>
        </div>
      </div>
    </div>
  )
}

export default RecentActivity 