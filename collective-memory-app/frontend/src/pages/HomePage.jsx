import React from 'react';
import { Link } from 'react-router-dom';
import { 
  MagnifyingGlassIcon, 
  ChartBarIcon, 
  Cog6ToothIcon,
  DocumentTextIcon,
  ClockIcon,
  ServerIcon
} from '@heroicons/react/24/outline';

const HomePage = () => {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="context7-card mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="context7-heading-1">Collective Memory</h1>
            <p className="context7-text-muted">AI-Powered Context Management System</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="context7-status-success flex items-center gap-2">
              <ServerIcon className="w-5 h-5" />
              <span>System Active</span>
            </div>
          </div>
        </div>
      </header>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <Link to="/search" className="context7-card hover:scale-105 transition-transform">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-blue-100 rounded-lg">
              <MagnifyingGlassIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">Search</h3>
              <p className="context7-text-muted">Find information across all conversations</p>
            </div>
          </div>
        </Link>

        <Link to="/analytics" className="context7-card hover:scale-105 transition-transform">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-green-100 rounded-lg">
              <ChartBarIcon className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">Analytics</h3>
              <p className="context7-text-muted">View system performance and insights</p>
            </div>
          </div>
        </Link>

        <Link to="/settings" className="context7-card hover:scale-105 transition-transform">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Cog6ToothIcon className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h3 className="context7-heading-3">Settings</h3>
              <p className="context7-text-muted">Configure system preferences</p>
            </div>
          </div>
        </Link>
      </div>

      {/* System Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="context7-card">
          <h3 className="context7-heading-3 mb-4">System Overview</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="context7-text">Total Files Indexed</span>
              <span className="context7-text font-semibold">1,247</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="context7-text">Active Conversations</span>
              <span className="context7-text font-semibold">23</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="context7-text">Search Queries Today</span>
              <span className="context7-text font-semibold">156</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="context7-text">System Uptime</span>
              <span className="context7-status-success font-semibold">99.9%</span>
            </div>
          </div>
        </div>

        <div className="context7-card">
          <h3 className="context7-heading-3 mb-4">Recent Activity</h3>
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <ClockIcon className="w-4 h-4 text-gray-400" />
              <div>
                <p className="context7-text text-sm">New conversation indexed</p>
                <p className="context7-text-muted text-xs">2 minutes ago</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <DocumentTextIcon className="w-4 h-4 text-gray-400" />
              <div>
                <p className="context7-text text-sm">Search query processed</p>
                <p className="context7-text-muted text-xs">5 minutes ago</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <ServerIcon className="w-4 h-4 text-gray-400" />
              <div>
                <p className="context7-text text-sm">System health check completed</p>
                <p className="context7-text-muted text-xs">15 minutes ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;