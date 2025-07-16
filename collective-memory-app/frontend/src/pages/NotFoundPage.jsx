import React from 'react';
import { Link } from 'react-router-dom';
import { HomeIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';

const NotFoundPage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center" data-testid="not-found-page">
      <div className="text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-gray-300 dark:text-gray-600">
            404
          </h1>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Sayfa Bulunamadı
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
            Aradığınız sayfa mevcut değil veya taşınmış olabilir.
          </p>
        </div>

        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/"
              className="inline-flex items-center px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
              data-testid="home-link"
            >
              <HomeIcon className="h-5 w-5 mr-2" />
              Ana Sayfaya Dön
            </Link>
            
            <Link
              to="/search"
              className="inline-flex items-center px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition-colors"
              data-testid="search-link"
            >
              <MagnifyingGlassIcon className="h-5 w-5 mr-2" />
              Arama Yap
            </Link>
          </div>

          <div className="mt-8">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
              Veya şu sayfalara göz atabilirsiniz:
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                to="/analytics"
                className="text-indigo-600 hover:text-indigo-700 text-sm"
                data-testid="analytics-link"
              >
                Analitik
              </Link>
              <Link
                to="/settings"
                className="text-indigo-600 hover:text-indigo-700 text-sm"
                data-testid="settings-link"
              >
                Ayarlar
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFoundPage; 