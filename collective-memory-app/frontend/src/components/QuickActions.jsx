import React from 'react'
import { motion } from 'framer-motion'
import { 
  RefreshCw, 
  Settings, 
  Download, 
  Upload, 
  FolderPlus, 
  Trash2,
  BarChart3,
  Zap
} from 'lucide-react'
import { useMutation, useQueryClient } from 'react-query'
import { systemAPI } from '../services/api'
import { toast } from 'react-hot-toast'

const QuickActions = () => {
  const queryClient = useQueryClient()

  const reindexMutation = useMutation(
    systemAPI.reindex,
    {
      onSuccess: () => {
        toast.success('Yeniden indeksleme başlatıldı')
        queryClient.invalidateQueries(['systemStatus', 'systemStats'])
      },
      onError: (error) => {
        toast.error('Yeniden indeksleme başlatılamadı: ' + error.message)
      }
    }
  )

  const clearCacheMutation = useMutation(
    systemAPI.clearCache,
    {
      onSuccess: () => {
        toast.success('Önbellek temizlendi')
        queryClient.invalidateQueries(['systemStats'])
      },
      onError: (error) => {
        toast.error('Önbellek temizlenemedi: ' + error.message)
      }
    }
  )

  const quickActions = [
    {
      title: 'Yeniden İndeksle',
      description: 'Tüm dosyaları yeniden tara',
      icon: RefreshCw,
      color: 'blue',
      action: () => reindexMutation.mutate(),
      loading: reindexMutation.isLoading
    },
    {
      title: 'Önbellek Temizle',
      description: 'Sistem önbelleğini temizle',
      icon: Trash2,
      color: 'red',
      action: () => clearCacheMutation.mutate(),
      loading: clearCacheMutation.isLoading
    },
    {
      title: 'Ayarlar',
      description: 'Sistem konfigürasyonu',
      icon: Settings,
      color: 'gray',
      action: () => window.location.href = '/settings'
    },
    {
      title: 'Analitik',
      description: 'Detaylı raporlar',
      icon: BarChart3,
      color: 'green',
      action: () => window.location.href = '/analytics'
    },
    {
      title: 'Klasör Ekle',
      description: 'Yeni klasör izlemeye ekle',
      icon: FolderPlus,
      color: 'purple',
      action: () => {
        // TODO: Implement folder selection dialog
        toast.info('Klasör seçme özelliği yakında eklenecek')
      }
    },
    {
      title: 'Verileri Dışa Aktar',
      description: 'İndeks verilerini dışa aktar',
      icon: Download,
      color: 'orange',
      action: () => {
        // TODO: Implement data export
        toast.info('Veri dışa aktarma özelliği yakında eklenecek')
      }
    }
  ]

  const colorClasses = {
    blue: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      text: 'text-blue-700 dark:text-blue-300',
      icon: 'text-blue-600 dark:text-blue-400',
      border: 'border-blue-200 dark:border-blue-800'
    },
    red: {
      bg: 'bg-red-50 dark:bg-red-900/20',
      text: 'text-red-700 dark:text-red-300',
      icon: 'text-red-600 dark:text-red-400',
      border: 'border-red-200 dark:border-red-800'
    },
    gray: {
      bg: 'bg-gray-50 dark:bg-gray-900/20',
      text: 'text-gray-700 dark:text-gray-300',
      icon: 'text-gray-600 dark:text-gray-400',
      border: 'border-gray-200 dark:border-gray-800'
    },
    green: {
      bg: 'bg-green-50 dark:bg-green-900/20',
      text: 'text-green-700 dark:text-green-300',
      icon: 'text-green-600 dark:text-green-400',
      border: 'border-green-200 dark:border-green-800'
    },
    purple: {
      bg: 'bg-purple-50 dark:bg-purple-900/20',
      text: 'text-purple-700 dark:text-purple-300',
      icon: 'text-purple-600 dark:text-purple-400',
      border: 'border-purple-200 dark:border-purple-800'
    },
    orange: {
      bg: 'bg-orange-50 dark:bg-orange-900/20',
      text: 'text-orange-700 dark:text-orange-300',
      icon: 'text-orange-600 dark:text-orange-400',
      border: 'border-orange-200 dark:border-orange-800'
    }
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Hızlı Eylemler
        </h3>
        <Zap className="w-5 h-5 text-primary-600 dark:text-primary-400" />
      </div>

      <div className="grid grid-cols-1 gap-3">
        {quickActions.map((action, index) => {
          const Icon = action.icon
          const colorClass = colorClasses[action.color] || colorClasses.gray

          return (
            <motion.button
              key={action.title}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={action.action}
              disabled={action.loading}
              className={`p-4 border rounded-lg transition-all duration-200 hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed ${colorClass.bg} ${colorClass.border}`}
            >
              <div className="flex items-center space-x-3">
                <div className={`p-2 rounded-lg ${colorClass.bg} border ${colorClass.border}`}>
                  {action.loading ? (
                    <div className="w-4 h-4 border-2 border-gray-300 border-t-primary-600 rounded-full animate-spin"></div>
                  ) : (
                    <Icon className={`w-4 h-4 ${colorClass.icon}`} />
                  )}
                </div>
                <div className="text-left flex-1">
                  <h4 className={`font-medium ${colorClass.text}`}>
                    {action.title}
                  </h4>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {action.description}
                  </p>
                </div>
              </div>
            </motion.button>
          )
        })}
      </div>

      {/* Performance Tip */}
      <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
        <div className="flex items-start space-x-2">
          <Zap className="w-4 h-4 text-blue-600 dark:text-blue-400 mt-0.5" />
          <div>
            <h5 className="text-sm font-medium text-blue-800 dark:text-blue-300">
              Performans İpucu
            </h5>
            <p className="text-xs text-blue-600 dark:text-blue-400 mt-1">
              Düzenli yeniden indeksleme ve önbellek temizleme sistem performansını artırır.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default QuickActions 