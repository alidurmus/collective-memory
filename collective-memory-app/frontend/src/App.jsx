import React, { useState, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Moon, Sun } from 'lucide-react'
import Dashboard from './components/Dashboard'
import SearchResults from './components/SearchResults'
import Analytics from './components/Analytics'
import Settings from './components/Settings'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import LoadingSpinner from './components/LoadingSpinner'
import { useSystemStatus } from './hooks/useSystemStatus'

function App() {
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('darkMode') === 'true' ||
             (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches)
    }
    return false
  })
  
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const { data: systemStatus, isLoading: statusLoading } = useSystemStatus()

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    localStorage.setItem('darkMode', darkMode.toString())
  }, [darkMode])

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  if (statusLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
      {/* Sidebar */}
      <AnimatePresence mode="wait">
        {sidebarOpen && (
          <motion.div
            initial={{ x: -300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="w-64 bg-white dark:bg-gray-800 shadow-lg border-r border-gray-200 dark:border-gray-700"
          >
            <Sidebar />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <Header 
          toggleSidebar={toggleSidebar}
          toggleDarkMode={toggleDarkMode}
          darkMode={darkMode}
          sidebarOpen={sidebarOpen}
          systemStatus={systemStatus}
        />

        {/* Main Content Area */}
        <main className="flex-1 overflow-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="p-6"
          >
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/search" element={<SearchResults />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </motion.div>
        </main>
      </div>
    </div>
  )
}

export default App 