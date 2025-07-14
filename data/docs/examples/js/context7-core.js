/**
 * Context7 ERP System - Core JavaScript Framework
 * @version 2.2.0-glassmorphism-enhanced
 * @author Context7 Development Team
 * @date 11 Ocak 2025
 */

// Main namespace
window.Context7 = window.Context7 || {};

// Core utilities
Context7.Utils = {
    /**
     * Debounce function for performance optimization
     * @param {Function} func - Function to debounce
     * @param {number} wait - Wait time in milliseconds
     * @param {boolean} immediate - Execute immediately
     * @returns {Function} Debounced function
     */
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func.apply(this, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(this, args);
        };
    },

    /**
     * Throttle function for performance optimization
     * @param {Function} func - Function to throttle
     * @param {number} limit - Time limit in milliseconds
     * @returns {Function} Throttled function
     */
    throttle: function(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    /**
     * Get CSRF token from Django
     * @returns {string} CSRF token
     */
    getCSRFToken: function() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    },

    /**
     * Format currency for display
     * @param {number} amount - Amount to format
     * @param {string} currency - Currency code (default: TRY)
     * @returns {string} Formatted currency string
     */
    formatCurrency: function(amount, currency = 'TRY') {
        return new Intl.NumberFormat('tr-TR', {
            style: 'currency',
            currency: currency
        }).format(amount);
    },

    /**
     * Format date for display
     * @param {Date|string} date - Date to format
     * @param {string} locale - Locale (default: tr-TR)
     * @returns {string} Formatted date string
     */
    formatDate: function(date, locale = 'tr-TR') {
        return new Date(date).toLocaleDateString(locale, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    /**
     * Generate UUID v4
     * @returns {string} UUID string
     */
    generateUUID: function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },

    /**
     * Validate email address
     * @param {string} email - Email to validate
     * @returns {boolean} Is valid email
     */
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    /**
     * Sanitize HTML to prevent XSS
     * @param {string} str - String to sanitize
     * @returns {string} Sanitized string
     */
    sanitizeHTML: function(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    }
};

// Event system
Context7.Events = {
    listeners: {},

    /**
     * Add event listener
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     */
    on: function(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    },

    /**
     * Remove event listener
     * @param {string} event - Event name
     * @param {Function} callback - Callback function
     */
    off: function(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }
    },

    /**
     * Emit event
     * @param {string} event - Event name
     * @param {*} data - Event data
     */
    emit: function(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => callback(data));
        }
    }
};

// Storage utilities
Context7.Storage = {
    /**
     * Set item in localStorage with expiration
     * @param {string} key - Storage key
     * @param {*} value - Value to store
     * @param {number} ttl - Time to live in milliseconds
     */
    setItem: function(key, value, ttl = null) {
        const item = {
            value: value,
            timestamp: Date.now(),
            ttl: ttl
        };
        localStorage.setItem(`context7_${key}`, JSON.stringify(item));
    },

    /**
     * Get item from localStorage
     * @param {string} key - Storage key
     * @returns {*} Stored value or null
     */
    getItem: function(key) {
        const item = localStorage.getItem(`context7_${key}`);
        if (!item) return null;

        try {
            const parsed = JSON.parse(item);
            if (parsed.ttl && Date.now() - parsed.timestamp > parsed.ttl) {
                localStorage.removeItem(`context7_${key}`);
                return null;
            }
            return parsed.value;
        } catch (e) {
            return null;
        }
    },

    /**
     * Remove item from localStorage
     * @param {string} key - Storage key
     */
    removeItem: function(key) {
        localStorage.removeItem(`context7_${key}`);
    }
}; 