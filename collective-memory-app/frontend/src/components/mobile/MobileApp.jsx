// Mobile App Foundation - PWA Component
// Mobile-optimized interface for Collective Memory

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  HomeIcon, 
  MagnifyingGlassIcon, 
  ChartBarIcon, 
  Cog6ToothIcon,
  Bars3Icon,
  XMarkIcon 
} from '@heroicons/react/24/outline';
import { useTranslation } from '../../hooks/useTranslation';

const MobileApp = ({ children }) => {
  const { t } = useTranslation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  
  // PWA Installation state
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [showInstallPrompt, setShowInstallPrompt] = useState(false);
  
  useEffect(() => {
    // Online/offline detection
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    // PWA install prompt
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowInstallPrompt(true);
    };
    
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);
  
  const handleInstallPWA = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      
      if (outcome === 'accepted') {
        setShowInstallPrompt(false);
      }
      setDeferredPrompt(null);
    }
  };
  
  const navigationItems = [
    { id: 'dashboard', icon: HomeIcon, label: t('nav.dashboard') },
    { id: 'search', icon: MagnifyingGlassIcon, label: t('nav.search') },
    { id: 'analytics', icon: ChartBarIcon, label: t('nav.analytics') },
    { id: 'settings', icon: Cog6ToothIcon, label: t('nav.settings') }
  ];
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      {/* Mobile Header */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-white/10 backdrop-blur-lg border-b border-white/20">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">CM</span>
            </div>
            <h1 className="text-white font-semibold text-lg">
              {t('dashboard.title')}
            </h1>
          </div>
          
          <div className="flex items-center space-x-2">
            {/* Connection Status */}
            <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-400' : 'bg-red-400'}`} />
            
            {/* Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
            >
              {isMenuOpen ? (
                <XMarkIcon className="w-5 h-5 text-white" />
              ) : (
                <Bars3Icon className="w-5 h-5 text-white" />
              )}
            </button>
          </div>
        </div>
        
        {/* PWA Install Banner */}
        <AnimatePresence>
          {showInstallPrompt && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="px-4 py-2 bg-blue-600/90 backdrop-blur-sm"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-white text-sm font-medium">
                    {t('common.installApp', 'Install App')}
                  </p>
                  <p className="text-blue-100 text-xs">
                    {t('common.installDescription', 'Add to home screen for better experience')}
                  </p>
                </div>
                <button
                  onClick={handleInstallPWA}
                  className="ml-3 px-3 py-1 bg-white/20 rounded text-white text-sm font-medium hover:bg-white/30 transition-colors"
                >
                  {t('common.install', 'Install')}
                </button>
                <button
                  onClick={() => setShowInstallPrompt(false)}
                  className="ml-2 p-1 text-white/70 hover:text-white"
                >
                  <XMarkIcon className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
            onClick={() => setIsMenuOpen(false)}
          >
            <motion.div
              initial={{ x: '-100%' }}
              animate={{ x: 0 }}
              exit={{ x: '-100%' }}
              className="w-80 h-full bg-white/95 backdrop-blur-lg shadow-xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-6">
                <div className="mb-8">
                  <h2 className="text-xl font-bold text-gray-800">
                    {t('nav.menu', 'Menu')}
                  </h2>
                  <p className="text-gray-600 text-sm">
                    {t('nav.menuDescription', 'Navigate through the app')}
                  </p>
                </div>
                
                <nav className="space-y-2">
                  {navigationItems.map((item) => (
                    <button
                      key={item.id}
                      onClick={() => {
                        setActiveTab(item.id);
                        setIsMenuOpen(false);
                      }}
                      className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                        activeTab === item.id
                          ? 'bg-blue-100 text-blue-900'
                          : 'text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <item.icon className="w-5 h-5" />
                      <span className="font-medium">{item.label}</span>
                    </button>
                  ))}
                </nav>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Main Content */}
      <div className="pt-16 pb-20 px-4">
        <div className="max-w-lg mx-auto">
          {children}
        </div>
      </div>
      
      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 z-50 bg-white/10 backdrop-blur-lg border-t border-white/20">
        <div className="flex">
          {navigationItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex-1 flex flex-col items-center justify-center py-3 transition-colors ${
                activeTab === item.id
                  ? 'text-blue-400'
                  : 'text-white/60 hover:text-white/80'
              }`}
            >
              <item.icon className="w-5 h-5 mb-1" />
              <span className="text-xs font-medium">{item.label}</span>
              {activeTab === item.id && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-400"
                />
              )}
            </button>
          ))}
        </div>
      </div>
      
      {/* Offline Indicator */}
      <AnimatePresence>
        {!isOnline && (
          <motion.div
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            exit={{ y: -100 }}
            className="fixed top-16 left-4 right-4 z-40 bg-red-500/90 backdrop-blur-sm rounded-lg p-3"
          >
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-red-200 rounded-full animate-pulse" />
              <span className="text-white text-sm font-medium">
                {t('messages.connectionLost', 'Connection lost - Working offline')}
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default MobileApp; 