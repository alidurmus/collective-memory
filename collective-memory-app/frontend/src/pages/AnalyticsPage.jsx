import React from 'react';
import { 
  ChartBarIcon, 
  ClockIcon, 
  DocumentTextIcon,
  MagnifyingGlassIcon,
  UserGroupIcon,
  ServerIcon
} from '@heroicons/react/24/outline';

const AnalyticsPage = () => {
  // Mock data for analytics
  const stats = {
    totalSearches: 1247,
    totalFiles: 3456,
    activeUsers: 23,
    systemUptime: '99.9%',
    avgResponseTime: '120ms',
    indexSize: '2.3 GB'
  };

  const recentActivity = [
    { id: 1, action: 'Search performed', user: 'User123', time: '2 minutes ago' },
    { id: 2, action: 'File indexed', user: 'System', time: '5 minutes ago' },
    { id: 3, action: 'New conversation', user: 'User456', time: '8 minutes ago' },
    { id: 4, action: 'Search performed', user: 'User789', time: '12 minutes ago' },
  ];

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="context7-card mb-8">
        <h1 className="context7-heading-1">Analytics</h1>
        <p className="context7-text-muted">System performance and usage insights</p>
      </header>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="context7-card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 rounded-lg">
              <MagnifyingGlassIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">{stats.totalSearches.toLocaleString()}</h3>
              <p className="context7-text-muted">Total Searches</p>
            </div>
          </div>
        </div>

        <div className="context7-card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 rounded-lg">
              <DocumentTextIcon className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">{stats.totalFiles.toLocaleString()}</h3>
              <p className="context7-text-muted">Indexed Files</p>
            </div>
          </div>
        </div>

        <div className="context7-card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 rounded-lg">
              <UserGroupIcon className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">{stats.activeUsers}</h3>
              <p className="context7-text-muted">Active Users</p>
            </div>
          </div>
        </div>

        <div className="context7-card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-yellow-100 rounded-lg">
              <ServerIcon className="w-6 h-6 text-yellow-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">{stats.systemUptime}</h3>
              <p className="context7-text-muted">System Uptime</p>
            </div>
          </div>
        </div>

        <div className="context7-card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-red-100 rounded-lg">
              <ClockIcon className="w-6 h-6 text-red-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">{stats.avgResponseTime}</h3>
              <p className="context7-text-muted">Avg Response Time</p>
            </div>
          </div>
        </div>

        <div className="context7-card">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-indigo-100 rounded-lg">
              <DocumentTextIcon className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">{stats.indexSize}</h3>
              <p className="context7-text-muted">Index Size</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="context7-card">
          <h3 className="context7-heading-3 mb-4">Search Activity</h3>
          <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <p className="context7-text-muted">Chart placeholder - Search activity over time</p>
          </div>
        </div>

        <div className="context7-card">
          <h3 className="context7-heading-3 mb-4">System Performance</h3>
          <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
            <p className="context7-text-muted">Chart placeholder - System performance metrics</p>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="context7-card">
        <h3 className="context7-heading-3 mb-4">Recent Activity</h3>
        <div className="space-y-3">
          {recentActivity.map((activity) => (
            <div key={activity.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-3">
                <ClockIcon className="w-4 h-4 text-gray-400" />
                <div>
                  <p className="context7-text text-sm font-medium">{activity.action}</p>
                  <p className="context7-text-muted text-xs">by {activity.user}</p>
                </div>
              </div>
              <span className="context7-text-muted text-sm">{activity.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;