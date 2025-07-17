import React, { useState } from 'react';
import '../styles/context7.css';

const Header = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [notifications, setNotifications] = useState(3);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  React.useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (date) => {
    return date.toLocaleTimeString('tr-TR', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const formatDate = (date) => {
    return date.toLocaleDateString('tr-TR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const navigationItems = [
    { id: 'dashboard', label: 'Ana Panel', icon: '🏠', active: true },
    { id: 'search', label: 'Akıllı Arama', icon: '🔍', active: false },
    { id: 'analytics', label: 'Analitikler', icon: '📊', active: false },
    { id: 'settings', label: 'Ayarlar', icon: '⚙️', active: false }
  ];

  const handleNavigationClick = (itemId) => {
    console.log(`Navigating to: ${itemId}`);
    // Navigation logic will be implemented here
  };

  const handleNotificationClick = () => {
    console.log('Bildirimler açılıyor...');
    // Notification panel logic
  };

  const toggleUserMenu = () => {
    setUserMenuOpen(!userMenuOpen);
  };

  return (
    <header className="context7-card mx-6 mb-6 sticky top-6 z-50">
      <div className="flex items-center justify-between p-4">
        
        {/* Sol Bölüm - Logo ve Navigasyon */}
        <div className="flex items-center space-x-6">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">CM</span>
            </div>
            <div>
              <h1 className="context7-heading context7-heading--sm context7-gradient-text">
                Collective Memory
              </h1>
              <p className="context7-text context7-text--muted text-xs">
                v2.1 Context7 Framework
              </p>
            </div>
          </div>

          {/* Ana Navigasyon */}
          <nav className="hidden md:flex items-center space-x-1">
            {navigationItems.map((item) => (
              <button
                key={item.id}
                onClick={() => handleNavigationClick(item.id)}
                className={`
                  flex items-center space-x-2 px-4 py-2 rounded-lg transition-all
                  ${item.active 
                    ? 'context7-button' 
                    : 'context7-interactive hover:bg-white/10'
                  }
                `}
              >
                <span className="text-lg">{item.icon}</span>
                <span className="context7-text text-sm font-medium">
                  {item.label}
                </span>
              </button>
            ))}
          </nav>
        </div>

        {/* Orta Bölüm - Tarih ve Saat */}
        <div className="hidden lg:flex items-center space-x-4 text-center">
          <div>
            <div className="context7-heading context7-heading--sm">
              {formatTime(currentTime)}
            </div>
            <div className="context7-text context7-text--muted text-xs">
              {formatDate(currentTime)}
            </div>
          </div>
        </div>

        {/* Sağ Bölüm - Bildirimler ve Kullanıcı */}
        <div className="flex items-center space-x-4">
          
          {/* Sistem Durumu İndikatörü */}
          <div className="hidden sm:flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="context7-text context7-text--muted text-sm">
              Sistem Aktif
            </span>
          </div>

          {/* Bildirimler */}
          <div className="relative">
            <button
              onClick={handleNotificationClick}
              className="context7-interactive p-2 rounded-lg relative"
              aria-label="Bildirimleri görüntüle"
            >
              <span className="text-xl">🔔</span>
              {notifications > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {notifications}
                </span>
              )}
            </button>
          </div>

          {/* Kullanıcı Menüsü */}
          <div className="relative">
            <button
              onClick={toggleUserMenu}
              className="context7-interactive flex items-center space-x-2 p-2 rounded-lg"
              aria-label="Kullanıcı menüsünü aç"
            >
              <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-bold">U</span>
              </div>
              <span className="hidden sm:block context7-text text-sm">
                Kullanıcı
              </span>
              <span className="text-gray-400 text-xs">
                {userMenuOpen ? '▲' : '▼'}
              </span>
            </button>

            {/* Kullanıcı Dropdown Menüsü */}
            {userMenuOpen && (
              <div className="absolute right-0 mt-2 w-48 context7-card p-2 shadow-lg">
                <div className="space-y-1">
                  <button className="w-full text-left px-3 py-2 rounded-lg context7-interactive">
                    <span className="mr-2">👤</span>
                    <span className="context7-text text-sm">Profil Ayarları</span>
                  </button>
                  <button className="w-full text-left px-3 py-2 rounded-lg context7-interactive">
                    <span className="mr-2">🎨</span>
                    <span className="context7-text text-sm">Tema Değiştir</span>
                  </button>
                  <button className="w-full text-left px-3 py-2 rounded-lg context7-interactive">
                    <span className="mr-2">📱</span>
                    <span className="context7-text text-sm">Kısayollar</span>
                  </button>
                  <div className="border-t border-gray-200 my-2"></div>
                  <button className="w-full text-left px-3 py-2 rounded-lg context7-interactive text-red-600">
                    <span className="mr-2">🚪</span>
                    <span className="context7-text text-sm">Çıkış Yap</span>
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Mobil Menü Butonu */}
          <button className="md:hidden context7-interactive p-2 rounded-lg">
            <span className="text-xl">☰</span>
          </button>
        </div>
      </div>

      {/* Mobil Navigasyon (Gizli) */}
      <div className="md:hidden border-t border-gray-200 p-4">
        <nav className="grid grid-cols-2 gap-2">
          {navigationItems.map((item) => (
            <button
              key={item.id}
              onClick={() => handleNavigationClick(item.id)}
              className={`
                flex items-center space-x-2 p-3 rounded-lg transition-all
                ${item.active 
                  ? 'context7-button' 
                  : 'context7-interactive'
                }
              `}
            >
              <span className="text-lg">{item.icon}</span>
              <span className="context7-text text-sm">
                {item.label}
              </span>
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
};

export default Header; 