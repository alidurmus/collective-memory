import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EnterpriseAnalytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [userActivities, setUserActivities] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [dateRange, setDateRange] = useState('7d');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, [dateRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/enterprise/analytics');
      if (response.data.success) {
        setAnalytics(response.data.analytics);
      }
    } catch (err) {
      setError('Analitik veriler alınamadı');
      console.error('Failed to fetch analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserActivity = async (userId) => {
    try {
      const response = await axios.get(`/api/enterprise/analytics/user/${userId}/activity`);
      if (response.data.success) {
        setUserActivities(response.data.activities);
      }
    } catch (err) {
      console.error('Failed to fetch user activity:', err);
    }
  };

  const handleUserSelect = (user) => {
    setSelectedUser(user);
    fetchUserActivity(user.user_id);
  };

  const getActivityIcon = (action) => {
    switch (action) {
      case 'login': return '🔑';
      case 'logout': return '🚪';
      case 'search': return '🔍';
      case 'create': return '➕';
      case 'update': return '✏️';
      case 'delete': return '🗑️';
      case 'join_room': return '💬';
      case 'leave_room': return '🚪';
      default: return '📝';
    }
  };

  const getActivityColor = (action) => {
    switch (action) {
      case 'login': return 'text-green-600';
      case 'logout': return 'text-gray-600';
      case 'search': return 'text-blue-600';
      case 'create': return 'text-green-600';
      case 'update': return 'text-yellow-600';
      case 'delete': return 'text-red-600';
      case 'join_room': return 'text-purple-600';
      case 'leave_room': return 'text-gray-600';
      default: return 'text-gray-600';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('tr-TR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="context7-loading">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          <p className="mt-4 text-gray-600">Analitik veriler yükleniyor...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="enterprise-analytics min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                📊 Enterprise Analytics
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="1d">Son 1 Gün</option>
                <option value="7d">Son 7 Gün</option>
                <option value="30d">Son 30 Gün</option>
                <option value="90d">Son 90 Gün</option>
              </select>
              <button
                onClick={fetchAnalytics}
                className="context7-button bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
              >
                🔄 Yenile
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
            <span className="block sm:inline">{error}</span>
            <button
              onClick={() => setError(null)}
              className="absolute top-0 bottom-0 right-0 px-4 py-3"
            >
              <span className="sr-only">Dismiss</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overview Cards */}
        {analytics && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">👥</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Aktif Kullanıcılar</p>
                  <p className="text-2xl font-semibold text-gray-900">{analytics.active_users}</p>
                </div>
              </div>
            </div>

            <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">🏢</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Aktif Takımlar</p>
                  <p className="text-2xl font-semibold text-gray-900">{analytics.active_teams}</p>
                </div>
              </div>
            </div>

            <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">⚡</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Son Aktiviteler</p>
                  <p className="text-2xl font-semibold text-gray-900">{analytics.recent_activities}</p>
                </div>
              </div>
            </div>

            <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <span className="text-2xl">📊</span>
                </div>
                <div className="ml-4">
                  <p className="text-sm text-gray-600">Sistem Skoru</p>
                  <p className="text-2xl font-semibold text-gray-900">9.5/10</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Most Active Users */}
          <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">🏆 En Aktif Kullanıcılar</h2>
            </div>
            <div className="p-6">
              {analytics?.most_active_users?.length === 0 ? (
                <p className="text-gray-500 text-center py-8">Henüz aktivite verisi yok</p>
              ) : (
                <div className="space-y-4">
                  {analytics?.most_active_users?.map((user, index) => (
                    <div
                      key={user.user_id}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => handleUserSelect(user)}
                    >
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                          <span className="text-white font-medium">#{index + 1}</span>
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">
                            Kullanıcı: {user.user_id}
                          </p>
                          <p className="text-sm text-gray-500">
                            {user.activity_count} aktivite
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-blue-500 h-2 rounded-full"
                            style={{
                              width: `${Math.min(
                                (user.activity_count / Math.max(...analytics.most_active_users.map(u => u.activity_count))) * 100,
                                100
                              )}%`
                            }}
                          />
                        </div>
                        <span className="text-sm text-gray-500">
                          {user.activity_count}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* User Activity Detail */}
          <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">
                📋 Kullanıcı Aktivite Detayı
              </h2>
            </div>
            <div className="p-6">
              {!selectedUser ? (
                <p className="text-gray-500 text-center py-8">
                  Aktivite detayını görmek için bir kullanıcı seçin
                </p>
              ) : (
                <div className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-sm text-blue-800">
                      <strong>Seçili Kullanıcı:</strong> {selectedUser.user_id}
                    </p>
                    <p className="text-sm text-blue-600">
                      Toplam Aktivite: {selectedUser.activity_count}
                    </p>
                  </div>
                  
                  <div className="max-h-96 overflow-y-auto">
                    {userActivities.length === 0 ? (
                      <p className="text-gray-500 text-center py-4">
                        Aktivite bulunamadı
                      </p>
                    ) : (
                      <div className="space-y-3">
                        {userActivities.map((activity) => (
                          <div
                            key={activity.id}
                            className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg"
                          >
                            <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm ${getActivityColor(activity.action)}`}>
                              {getActivityIcon(activity.action)}
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center justify-between">
                                <p className="text-sm font-medium text-gray-900 capitalize">
                                  {activity.action} - {activity.resource_type}
                                </p>
                                <p className="text-xs text-gray-500">
                                  {formatDate(activity.timestamp)}
                                </p>
                              </div>
                              <p className="text-xs text-gray-500 mt-1">
                                Resource: {activity.resource_id}
                              </p>
                              {activity.metadata && Object.keys(activity.metadata).length > 0 && (
                                <div className="mt-2 text-xs text-gray-500">
                                  {Object.entries(activity.metadata).map(([key, value]) => (
                                    <span key={key} className="inline-block bg-gray-200 rounded px-2 py-1 mr-2">
                                      {key}: {value}
                                    </span>
                                  ))}
                                </div>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* System Performance Metrics */}
        <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200 mt-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">⚡ Sistem Performans Metrikleri</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-100 text-sm">Ortalama Yanıt Süresi</p>
                    <p className="text-2xl font-bold">< 100ms</p>
                  </div>
                  <div className="text-3xl opacity-80">⚡</div>
                </div>
              </div>

              <div className="bg-gradient-to-r from-green-500 to-teal-600 rounded-lg p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-green-100 text-sm">Sistem Kullanılabilirlik</p>
                    <p className="text-2xl font-bold">99.8%</p>
                  </div>
                  <div className="text-3xl opacity-80">✅</div>
                </div>
              </div>

              <div className="bg-gradient-to-r from-orange-500 to-red-600 rounded-lg p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-orange-100 text-sm">Aktif Oturumlar</p>
                    <p className="text-2xl font-bold">{analytics?.active_users || 0}</p>
                  </div>
                  <div className="text-3xl opacity-80">👥</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Real-time Activity Feed */}
        <div className="context7-card bg-white rounded-lg shadow-sm border border-gray-200 mt-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">🔄 Gerçek Zamanlı Aktivite Akışı</h2>
          </div>
          <div className="p-6">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-500 text-center">
                Gerçek zamanlı aktivite akışı hazırlanıyor...
              </p>
              <div className="mt-4 flex justify-center">
                <div className="animate-pulse flex space-x-4">
                  <div className="rounded-full bg-gray-300 h-3 w-3"></div>
                  <div className="rounded-full bg-gray-300 h-3 w-3"></div>
                  <div className="rounded-full bg-gray-300 h-3 w-3"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnterpriseAnalytics; 