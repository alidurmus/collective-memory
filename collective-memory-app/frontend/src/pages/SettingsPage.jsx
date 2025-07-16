import React, { useState } from 'react';
import { Cog6ToothIcon, LockClosedIcon, BellIcon } from '@heroicons/react/24/outline';

const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    theme: 'light',
    language: 'tr',
    notifications: true,
    autoSave: true,
    searchType: 'semantic',
    maxResults: 50,
    fileTypes: ['md', 'txt', 'py', 'js'],
    cacheEnabled: true,
    indexingEnabled: true,
  });

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSaveSettings = () => {
    // TODO: Implement save settings API call
    console.log('Saving settings:', settings);
  };

  const handleResetSettings = () => {
    // TODO: Implement reset settings
    console.log('Resetting settings');
  };

  const tabs = [
    { id: 'general', name: 'Genel', icon: Cog6ToothIcon, testId: 'general-tab' },
    { id: 'search', name: 'Arama', icon: Cog6ToothIcon, testId: 'search-tab' },
    { id: 'system', name: 'Sistem', icon: Cog6ToothIcon, testId: 'system-tab' },
    { id: 'security', name: 'Güvenlik', icon: LockClosedIcon, testId: 'security-tab' },
  ];

  return (
    <div className="max-w-6xl mx-auto" data-testid="settings-page">
      {/* Page Header */}
      <div className="mb-8" data-testid="settings-header">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Ayarlar
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Sistem konfigürasyonu ve kişiselleştirme seçenekleri
        </p>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar Tabs */}
        <div className="lg:w-64 space-y-2" data-testid="settings-tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`w-full flex items-center px-4 py-3 text-left rounded-lg transition-colors ${
                activeTab === tab.id
                  ? 'bg-indigo-100 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              }`}
              data-testid={tab.testId}
            >
              <tab.icon className="h-5 w-5 mr-3" />
              {tab.name}
            </button>
          ))}
        </div>

        {/* Settings Content */}
        <div className="flex-1">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6" data-testid="settings-content">
            {activeTab === 'general' && (
              <div data-testid="general-settings">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                  Genel Ayarlar
                </h2>
                
                <div className="space-y-6">
                  {/* Theme Selection */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Tema
                    </label>
                    <select
                      value={settings.theme}
                      onChange={(e) => handleSettingChange('theme', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
                      data-testid="theme-selector"
                    >
                      <option value="light">Açık Tema</option>
                      <option value="dark">Koyu Tema</option>
                      <option value="system">Sistem Teması</option>
                    </select>
                  </div>

                  {/* Language Selection */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Dil
                    </label>
                    <select
                      value={settings.language}
                      onChange={(e) => handleSettingChange('language', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
                      data-testid="language-selector"
                    >
                      <option value="tr">Türkçe</option>
                      <option value="en">English</option>
                    </select>
                  </div>

                  {/* Notifications */}
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Bildirimler
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Sistem bildirimleri ve uyarıları
                      </p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.notifications}
                      onChange={(e) => handleSettingChange('notifications', e.target.checked)}
                      className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                      data-testid="notifications-toggle"
                    />
                  </div>

                  {/* Auto Save */}
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Otomatik Kaydetme
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Ayarları otomatik olarak kaydet
                      </p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.autoSave}
                      onChange={(e) => handleSettingChange('autoSave', e.target.checked)}
                      className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                      data-testid="auto-save-toggle"
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'search' && (
              <div data-testid="search-settings">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                  Arama Ayarları
                </h2>
                
                <div className="space-y-6">
                  {/* Default Search Type */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Varsayılan Arama Türü
                    </label>
                    <select
                      value={settings.searchType}
                      onChange={(e) => handleSettingChange('searchType', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
                      data-testid="default-search-type"
                    >
                      <option value="basic">Temel Arama</option>
                      <option value="semantic">Semantic Arama</option>
                    </select>
                  </div>

                  {/* Max Results */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Maksimum Sonuç Sayısı
                    </label>
                    <select
                      value={settings.maxResults}
                      onChange={(e) => handleSettingChange('maxResults', parseInt(e.target.value))}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white"
                      data-testid="max-results-selector"
                    >
                      <option value="10">10</option>
                      <option value="25">25</option>
                      <option value="50">50</option>
                      <option value="100">100</option>
                    </select>
                  </div>

                  {/* File Types */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Aranacak Dosya Türleri
                    </label>
                    <div className="space-y-2" data-testid="file-type-checkboxes">
                      {[
                        { value: 'md', label: 'Markdown (.md)' },
                        { value: 'txt', label: 'Text (.txt)' },
                        { value: 'py', label: 'Python (.py)' },
                        { value: 'js', label: 'JavaScript (.js)' },
                        { value: 'json', label: 'JSON (.json)' },
                      ].map((fileType) => (
                        <label key={fileType.value} className="flex items-center">
                          <input
                            type="checkbox"
                            checked={settings.fileTypes.includes(fileType.value)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                handleSettingChange('fileTypes', [...settings.fileTypes, fileType.value]);
                              } else {
                                handleSettingChange('fileTypes', settings.fileTypes.filter(t => t !== fileType.value));
                              }
                            }}
                            className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 mr-3"
                            data-testid={`filetype-${fileType.value}`}
                          />
                          <span className="text-sm text-gray-700 dark:text-gray-300">
                            {fileType.label}
                          </span>
                        </label>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'system' && (
              <div data-testid="system-settings">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                  Sistem Ayarları
                </h2>
                
                <div className="space-y-6">
                  {/* Cache Settings */}
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Cache Sistemi
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Arama sonuçlarını önbellekte sakla
                      </p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.cacheEnabled}
                      onChange={(e) => handleSettingChange('cacheEnabled', e.target.checked)}
                      className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                      data-testid="cache-toggle"
                    />
                  </div>

                  {/* Indexing Settings */}
                  <div className="flex items-center justify-between">
                    <div>
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Otomatik İndeksleme
                      </label>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        Dosya değişikliklerini otomatik indeksle
                      </p>
                    </div>
                    <input
                      type="checkbox"
                      checked={settings.indexingEnabled}
                      onChange={(e) => handleSettingChange('indexingEnabled', e.target.checked)}
                      className="h-4 w-4 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500"
                      data-testid="indexing-toggle"
                    />
                  </div>

                  {/* Performance Settings */}
                  <div>
                    <h3 className="text-md font-medium text-gray-900 dark:text-white mb-3">
                      Performans Ayarları
                    </h3>
                    <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                      <div className="text-sm text-gray-600 dark:text-gray-300">
                        <p>• Cache boyutu: 512 MB</p>
                        <p>• İndeks güncellemesi: Her 5 dakikada bir</p>
                        <p>• Maksimum thread sayısı: 4</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'security' && (
              <div data-testid="security-settings">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                  Güvenlik Ayarları
                </h2>
                
                <div className="space-y-6">
                  <div className="bg-yellow-50 dark:bg-yellow-900 border border-yellow-200 dark:border-yellow-700 rounded-lg p-4">
                    <p className="text-sm text-yellow-800 dark:text-yellow-200">
                      Güvenlik ayarları geliştirme aşamasındadır. Gelecek güncellemelerde eklenecektir.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
              <div className="flex gap-4" data-testid="settings-form">
                <button
                  onClick={handleSaveSettings}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                  data-testid="save-settings"
                >
                  Ayarları Kaydet
                </button>
                <button
                  onClick={handleResetSettings}
                  className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
                  data-testid="reset-settings"
                >
                  Sıfırla
                </button>
                <button
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  data-testid="export-settings"
                >
                  Dışa Aktar
                </button>
                <button
                  className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                  data-testid="import-settings"
                >
                  İçe Aktar
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage; 