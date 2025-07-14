import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Settings as SettingsIcon, 
  Save, 
  RefreshCw, 
  Folder, 
  Database,
  Bell,
  Shield,
  Zap,
  HardDrive,
  Globe,
  User,
  Trash2,
  Plus,
  X
} from 'lucide-react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { configAPI, systemAPI } from '../services/api'
import { toast } from 'react-hot-toast'
import LoadingSpinner from './LoadingSpinner'

const Settings = () => {
  const [activeTab, setActiveTab] = useState('general')
  const [watchedPaths, setWatchedPaths] = useState([])
  const [newPath, setNewPath] = useState('')
  
  const queryClient = useQueryClient()

  const { data: config, isLoading: configLoading } = useQuery(
    'config',
    configAPI.getConfig,
    { staleTime: 5 * 60 * 1000 }
  )

  const updateConfigMutation = useMutation(
    configAPI.updateConfig,
    {
      onSuccess: () => {
        toast.success('Ayarlar başarıyla kaydedildi')
        queryClient.invalidateQueries(['config', 'systemStatus'])
      },
      onError: (error) => {
        toast.error('Ayarlar kaydedilemedi: ' + error.message)
      }
    }
  )

  const resetConfigMutation = useMutation(
    configAPI.resetConfig,
    {
      onSuccess: () => {
        toast.success('Ayarlar sıfırlandı')
        queryClient.invalidateQueries(['config'])
      },
      onError: (error) => {
        toast.error('Ayarlar sıfırlanamadı: ' + error.message)
      }
    }
  )

  const [formData, setFormData] = useState({
    // General settings
    maxFileSize: config?.maxFileSize || 100,
    maxIndexSize: config?.maxIndexSize || 1000,
    autoIndex: config?.autoIndex || true,
    
    // Search settings
    enableSemantic: config?.enableSemantic || true,
    defaultSearchLimit: config?.defaultSearchLimit || 50,
    cacheEnabled: config?.cacheEnabled || true,
    
    // Notifications
    notifyOnIndex: config?.notifyOnIndex || true,
    notifyOnError: config?.notifyOnError || true,
    emailNotifications: config?.emailNotifications || false,
    
    // Security
    enableAuth: config?.enableAuth || false,
    sessionTimeout: config?.sessionTimeout || 3600,
    logLevel: config?.logLevel || 'info'
  })

  React.useEffect(() => {
    if (config) {
      setFormData({
        maxFileSize: config.maxFileSize || 100,
        maxIndexSize: config.maxIndexSize || 1000,
        autoIndex: config.autoIndex || true,
        enableSemantic: config.enableSemantic || true,
        defaultSearchLimit: config.defaultSearchLimit || 50,
        cacheEnabled: config.cacheEnabled || true,
        notifyOnIndex: config.notifyOnIndex || true,
        notifyOnError: config.notifyOnError || true,
        emailNotifications: config.emailNotifications || false,
        enableAuth: config.enableAuth || false,
        sessionTimeout: config.sessionTimeout || 3600,
        logLevel: config.logLevel || 'info'
      })
      setWatchedPaths(config.watchedPaths || [])
    }
  }, [config])

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSave = () => {
    updateConfigMutation.mutate({
      ...formData,
      watchedPaths
    })
  }

  const handleReset = () => {
    if (window.confirm('Tüm ayarları sıfırlamak istediğinizden emin misiniz?')) {
      resetConfigMutation.mutate()
    }
  }

  const addWatchedPath = () => {
    if (newPath.trim() && !watchedPaths.includes(newPath.trim())) {
      setWatchedPaths([...watchedPaths, newPath.trim()])
      setNewPath('')
    }
  }

  const removeWatchedPath = (path) => {
    setWatchedPaths(watchedPaths.filter(p => p !== path))
  }

  const tabs = [
    { id: 'general', label: 'Genel', icon: SettingsIcon },
    { id: 'indexing', label: 'İndeksleme', icon: Database },
    { id: 'search', label: 'Arama', icon: Zap },
    { id: 'notifications', label: 'Bildirimler', icon: Bell },
    { id: 'security', label: 'Güvenlik', icon: Shield },
    { id: 'storage', label: 'Depolama', icon: HardDrive }
  ]

  if (configLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" text="Ayarlar yükleniyor..." />
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
            Sistem Ayarları
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Collective Memory sistem konfigürasyonu ve tercihler
          </p>
        </div>
        
        <div className="mt-4 sm:mt-0 flex items-center space-x-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleReset}
            disabled={resetConfigMutation.isLoading}
            className="btn-secondary flex items-center space-x-2"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Sıfırla</span>
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleSave}
            disabled={updateConfigMutation.isLoading}
            className="btn-primary flex items-center space-x-2"
          >
            {updateConfigMutation.isLoading ? (
              <LoadingSpinner size="sm" />
            ) : (
              <Save className="w-4 h-4" />
            )}
            <span>Kaydet</span>
          </motion.button>
        </div>
      </motion.div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:w-64"
        >
          <div className="card p-4">
            <nav className="space-y-2">
              {tabs.map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 text-sm font-medium rounded-lg transition-colors ${
                      activeTab === tab.id
                        ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </nav>
          </div>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex-1"
        >
          <div className="card p-6">
            {/* General Settings */}
            {activeTab === 'general' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Genel Ayarlar
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Maksimum Dosya Boyutu (MB)
                    </label>
                    <input
                      type="number"
                      value={formData.maxFileSize}
                      onChange={(e) => handleInputChange('maxFileSize', parseInt(e.target.value))}
                      className="input-field"
                      min="1"
                      max="1000"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Maksimum İndeks Boyutu (MB)
                    </label>
                    <input
                      type="number"
                      value={formData.maxIndexSize}
                      onChange={(e) => handleInputChange('maxIndexSize', parseInt(e.target.value))}
                      className="input-field"
                      min="100"
                      max="10000"
                    />
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  <input
                    type="checkbox"
                    id="autoIndex"
                    checked={formData.autoIndex}
                    onChange={(e) => handleInputChange('autoIndex', e.target.checked)}
                    className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                  />
                  <label htmlFor="autoIndex" className="text-sm text-gray-700 dark:text-gray-300">
                    Otomatik indeksleme etkin
                  </label>
                </div>
              </div>
            )}

            {/* Indexing Settings */}
            {activeTab === 'indexing' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  İndeksleme Ayarları
                </h3>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    İzlenen Klasörler
                  </label>
                  
                  <div className="space-y-3">
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        value={newPath}
                        onChange={(e) => setNewPath(e.target.value)}
                        placeholder="Klasör yolu ekleyin..."
                        className="flex-1 input-field"
                        onKeyPress={(e) => e.key === 'Enter' && addWatchedPath()}
                      />
                      <button
                        onClick={addWatchedPath}
                        className="btn-primary flex items-center space-x-2"
                      >
                        <Plus className="w-4 h-4" />
                        <span>Ekle</span>
                      </button>
                    </div>
                    
                    <div className="space-y-2">
                      {watchedPaths.map((path, index) => (
                        <div
                          key={index}
                          className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
                        >
                          <div className="flex items-center space-x-2">
                            <Folder className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                            <span className="text-sm text-gray-900 dark:text-gray-100">
                              {path}
                            </span>
                          </div>
                          <button
                            onClick={() => removeWatchedPath(path)}
                            className="p-1 text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Search Settings */}
            {activeTab === 'search' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Arama Ayarları
                </h3>
                
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      id="enableSemantic"
                      checked={formData.enableSemantic}
                      onChange={(e) => handleInputChange('enableSemantic', e.target.checked)}
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="enableSemantic" className="text-sm text-gray-700 dark:text-gray-300">
                      Semantik arama etkin
                    </label>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      id="cacheEnabled"
                      checked={formData.cacheEnabled}
                      onChange={(e) => handleInputChange('cacheEnabled', e.target.checked)}
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="cacheEnabled" className="text-sm text-gray-700 dark:text-gray-300">
                      Arama önbelleği etkin
                    </label>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Varsayılan Sonuç Limiti
                    </label>
                    <select
                      value={formData.defaultSearchLimit}
                      onChange={(e) => handleInputChange('defaultSearchLimit', parseInt(e.target.value))}
                      className="input-field"
                    >
                      <option value={25}>25</option>
                      <option value={50}>50</option>
                      <option value={100}>100</option>
                      <option value={200}>200</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Notifications */}
            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Bildirim Ayarları
                </h3>
                
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      id="notifyOnIndex"
                      checked={formData.notifyOnIndex}
                      onChange={(e) => handleInputChange('notifyOnIndex', e.target.checked)}
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="notifyOnIndex" className="text-sm text-gray-700 dark:text-gray-300">
                      İndeksleme tamamlandığında bildir
                    </label>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      id="notifyOnError"
                      checked={formData.notifyOnError}
                      onChange={(e) => handleInputChange('notifyOnError', e.target.checked)}
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="notifyOnError" className="text-sm text-gray-700 dark:text-gray-300">
                      Hata durumunda bildir
                    </label>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      id="emailNotifications"
                      checked={formData.emailNotifications}
                      onChange={(e) => handleInputChange('emailNotifications', e.target.checked)}
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="emailNotifications" className="text-sm text-gray-700 dark:text-gray-300">
                      E-posta bildirimleri (yakında)
                    </label>
                  </div>
                </div>
              </div>
            )}

            {/* Security */}
            {activeTab === 'security' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Güvenlik Ayarları
                </h3>
                
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <input
                      type="checkbox"
                      id="enableAuth"
                      checked={formData.enableAuth}
                      onChange={(e) => handleInputChange('enableAuth', e.target.checked)}
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="enableAuth" className="text-sm text-gray-700 dark:text-gray-300">
                      Kimlik doğrulama etkin (yakında)
                    </label>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Oturum Zaman Aşımı (saniye)
                    </label>
                    <input
                      type="number"
                      value={formData.sessionTimeout}
                      onChange={(e) => handleInputChange('sessionTimeout', parseInt(e.target.value))}
                      className="input-field"
                      min="300"
                      max="86400"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Log Seviyesi
                    </label>
                    <select
                      value={formData.logLevel}
                      onChange={(e) => handleInputChange('logLevel', e.target.value)}
                      className="input-field"
                    >
                      <option value="debug">Debug</option>
                      <option value="info">Info</option>
                      <option value="warning">Warning</option>
                      <option value="error">Error</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Storage */}
            {activeTab === 'storage' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  Depolama Ayarları
                </h3>
                
                <div className="space-y-6">
                  <div className="bg-gray-50 dark:bg-gray-800 p-4 rounded-lg">
                    <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-3">
                      Disk Kullanımı
                    </h4>
                    <div className="space-y-3">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">İndeks Verileri</span>
                        <span className="font-medium text-gray-900 dark:text-gray-100">234 MB</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Önbellek</span>
                        <span className="font-medium text-gray-900 dark:text-gray-100">45 MB</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Loglar</span>
                        <span className="font-medium text-gray-900 dark:text-gray-100">12 MB</span>
                      </div>
                      <div className="border-t border-gray-200 dark:border-gray-700 pt-2">
                        <div className="flex justify-between text-sm font-medium">
                          <span className="text-gray-900 dark:text-gray-100">Toplam</span>
                          <span className="text-gray-900 dark:text-gray-100">291 MB</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex space-x-3">
                    <button className="btn-secondary flex items-center space-x-2">
                      <Trash2 className="w-4 h-4" />
                      <span>Önbelleği Temizle</span>
                    </button>
                    <button className="btn-secondary flex items-center space-x-2">
                      <Trash2 className="w-4 h-4" />
                      <span>Logları Temizle</span>
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default Settings 