import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, 
  BarChart3, 
  Settings, 
  Zap,
  FileText,
  Clock,
  Activity,
  TrendingUp,
  Database,
  RefreshCw,
  ArrowRight,
  Sparkles,
  Brain,
  Target
} from 'lucide-react';
import { Link } from 'react-router-dom';
import Header from '../components/Header';
import SearchPanel from '../components/SearchPanel';
import SystemStatus from '../components/SystemStatus';
import { useSystemStats } from '../hooks/useSystemStatus';
import '../styles/context7.css';

const HomePage = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [greeting, setGreeting] = useState('');
  const { data: systemStats, isLoading } = useSystemStats();

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    // Set greeting based on time
    const hour = new Date().getHours();
    if (hour < 12) setGreeting('Günaydın');
    else if (hour < 18) setGreeting('İyi öğleden sonra');
    else setGreeting('İyi akşamlar');

    return () => clearInterval(timer);
  }, []);

  const quickActions = [
    {
      title: 'Akıllı Arama',
      description: 'AI destekli semantik arama',
      icon: Search,
      color: 'from-blue-500 to-cyan-500',
      href: '/search',
      shortcut: 'Ctrl+K'
    },
    {
      title: 'Analitik',
      description: 'Kullanım istatistikleri',
      icon: BarChart3,
      color: 'from-green-500 to-emerald-500',
      href: '/analytics',
      shortcut: 'Ctrl+A'
    },
    {
      title: 'Ayarlar',
      description: 'Sistem konfigürasyonu',
      icon: Settings,
      color: 'from-purple-500 to-violet-500',
      href: '/settings',
      shortcut: 'Ctrl+S'
    }
  ];

  const systemOverview = [
    {
      label: 'Toplam Dosya',
      value: systemStats?.file_count?.toLocaleString('tr-TR') || '0',
      icon: FileText,
      change: '+12%',
      changeType: 'positive'
    },
    {
      label: 'Arama Sayısı',
      value: systemStats?.search_count?.toLocaleString('tr-TR') || '0',
      icon: Search,
      change: '+8%',
      changeType: 'positive'
    },
    {
      label: 'Yanıt Süresi',
      value: systemStats?.avg_search_time ? `${systemStats.avg_search_time}ms` : '<50ms',
      icon: Zap,
      change: '-15%',
      changeType: 'positive'
    },
    {
      label: 'Çalışma Süresi',
      value: systemStats?.uptime || '0:00:00',
      icon: Clock,
      change: 'Çalışıyor',
      changeType: 'neutral'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      action: 'Django hata çözümü arandı',
      time: '5 dakika önce',
      type: 'search',
      icon: Search
    },
    {
      id: 2,
      action: 'collective-memory.md dosyası eklendi',
      time: '15 dakika önce',
      type: 'file',
      icon: FileText
    },
    {
      id: 3,
      action: 'Sistem yeniden indekslendi',
      time: '30 dakika önce',
      type: 'system',
      icon: RefreshCw
    }
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Sistem yükleniyor...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen context7-dashboard turkish-ui">
      <Header />
      
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden rounded-3xl mx-6 mb-8"
      >
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-teal-600"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/90 via-purple-600/90 to-teal-600/90 backdrop-blur-sm"></div>
        
        <div className="relative p-8 md:p-12">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="mb-6 md:mb-0">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="flex items-center space-x-3 mb-4"
              >
                <div className="w-12 h-12 bg-white/20 backdrop-blur-lg rounded-2xl flex items-center justify-center">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-3xl md:text-4xl font-bold text-white">
                    {greeting}! 👋
                  </h1>
                  <p className="text-white/80 text-lg">
                    Collective Memory'ye hoş geldiniz
                  </p>
                </div>
              </motion.div>
              
              <motion.p
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 }}
                className="text-white/90 text-lg max-w-2xl mb-6"
              >
                Akıllı bağlam yönetimi ve AI destekli arama sisteminiz ile bilgilerinizi 
                organize edin, hızla bulun ve verimli çalışın.
              </motion.p>
              
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 }}
                className="flex items-center space-x-4"
              >
                <Link
                  to="/search"
                  className="bg-white/20 backdrop-blur-lg text-white px-6 py-3 rounded-xl hover:bg-white/30 transition-all duration-300 flex items-center space-x-2"
                >
                  <Search className="w-5 h-5" />
                  <span>Hemen Ara</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <span className="text-white/60 text-sm">
                  {currentTime.toLocaleTimeString('tr-TR')}
                </span>
              </motion.div>
            </div>
            
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.8 }}
              className="relative"
            >
              <div className="w-64 h-64 bg-white/10 backdrop-blur-lg rounded-3xl p-6 flex items-center justify-center">
                <div className="text-center">
                  <Sparkles className="w-16 h-16 text-white mx-auto mb-4" />
                  <p className="text-white text-sm">
                    AI Destekli Arama<br />Aktif ve Hazır
                  </p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* Quick Actions */}
      <div className="mx-6 mb-8">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl font-bold text-gray-900 dark:text-white mb-6"
        >
          Hızlı Eylemler
        </motion.h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action, index) => (
            <motion.div
              key={action.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="group"
            >
              <Link
                to={action.href}
                className="block p-6 bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-2xl border border-white/20 hover:bg-white/90 dark:hover:bg-gray-800/90 transition-all duration-300"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 rounded-xl bg-gradient-to-r ${action.color}`}>
                    <action.icon className="w-6 h-6 text-white" />
                  </div>
                  <span className="text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded-lg">
                    {action.shortcut}
                  </span>
                </div>
                
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                  {action.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  {action.description}
                </p>
                
                <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 mt-4 transition-colors" />
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* System Overview */}
      <div className="mx-6 mb-8">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl font-bold text-gray-900 dark:text-white mb-6"
        >
          Sistem Durumu
        </motion.h2>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {systemOverview.map((item, index) => (
            <motion.div
              key={item.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-6 bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-2xl border border-white/20"
            >
              <div className="flex items-center justify-between mb-2">
                <item.icon className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                <span className={`text-xs px-2 py-1 rounded-full ${
                  item.changeType === 'positive' 
                    ? 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400'
                    : item.changeType === 'negative'
                    ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
                    : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
                }`}>
                  {item.change}
                </span>
              </div>
              
              <div className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                {item.value}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {item.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="mx-6 grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        
        {/* Quick Search */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-6 bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-2xl border border-white/20"
          >
            <div className="flex items-center space-x-3 mb-6">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg">
                <Search className="w-5 h-5 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                Hızlı Arama
              </h3>
            </div>
            
            <SearchPanel embedded={true} />
          </motion.div>
        </div>

        {/* Recent Activity */}
        <div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="p-6 bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-2xl border border-white/20"
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-purple-100 dark:bg-purple-900/30 rounded-lg">
                  <Activity className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Son Aktiviteler
                </h3>
              </div>
              <Target className="w-5 h-5 text-gray-400" />
            </div>
            
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <motion.div
                  key={activity.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                >
                  <div className="p-2 bg-gray-100 dark:bg-gray-700 rounded-lg">
                    <activity.icon className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-gray-900 dark:text-white truncate">
                      {activity.action}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {activity.time}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
            
            <Link
              to="/analytics"
              className="block mt-4 text-center text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors"
            >
              Tüm aktiviteleri görüntüle →
            </Link>
          </motion.div>
        </div>
      </div>

      {/* System Status Component */}
      <div className="mx-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="p-6 bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-2xl border border-white/20"
        >
          <SystemStatus stats={systemStats} />
        </motion.div>
      </div>
    </div>
  );
};

export default HomePage; 