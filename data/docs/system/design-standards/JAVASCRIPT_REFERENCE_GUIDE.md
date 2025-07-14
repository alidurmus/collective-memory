# 🚀 Context7 ERP - JavaScript Reference Guide

**Version**: v2.2.0-glassmorphism-enhanced  
**Date**: 11 Ocak 2025  
**Status**: ✅ **ACTIVE JAVASCRIPT REFERENCE**  
**QMS Reference**: REC-JS-REFERENCE-250111-002

---

## 📋 **JavaScript Dosyaları Organizasyonu**

### **Ana JavaScript Framework Dosyaları**
```
static/js/
├── context7-core.js                     # 🎯 ANA FRAMEWORK
├── context7-glassmorphism.js           # 🎨 Glassmorphism interactive effects
├── context7-forms.js                   # 📝 Form validation & handling
├── context7-tables.js                  # 📊 Table interactions & sorting
├── context7-charts.js                  # 📈 Chart.js integrations
├── context7-api.js                     # 🔗 API client & AJAX utilities
├── context7-notifications.js           # 🔔 Toast notifications & alerts
├── context7-modal.js                   # 🖼️ Modal dialogs & overlays
├── context7-search.js                  # 🔍 Search & filtering
├── context7-dashboard.js               # 📊 Dashboard specific features
├── quality-control.js                  # 🔍 Quality control forms
├── erp-common.js                       # 🏢 Common ERP functionality
└── bootstrap-extensions.js             # 🎛️ Bootstrap customizations
```

---

## 🎯 **1. Context7 Core JavaScript**
**📄 Dosya**: `static/js/context7-core.js`
**📄 Dosya Linki**: [`docs/examples/js/context7-core.js`](../examples/js/context7-core.js)

### **Core Namespace & Utilities**
```javascript
// Context7 Core Framework - Kod örneği için yukarıdaki dosya linkini kullanın
window.Context7 = window.Context7 || {};

// Core utilities - Tam kod için yukarıdaki dosya linkini kullanın
Context7.Utils = {
    debounce: function(func, wait, immediate) { /* ... */ },
    throttle: function(func, limit) { /* ... */ },
    getCSRFToken: function() { /* ... */ },
    formatCurrency: function(amount, currency = 'TRY') { /* ... */ },
    formatDate: function(date, locale = 'tr-TR') { /* ... */ },
    generateUUID: function() { /* ... */ },
    validateEmail: function(email) { /* ... */ },
    sanitizeHTML: function(str) { /* ... */ }
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
```

---

## 🎨 **2. Glassmorphism Interactive Effects**
**📄 Dosya**: `static/js/context7-glassmorphism.js`
**📄 Dosya Linki**: [`docs/examples/js/context7-glassmorphism.js`](../examples/js/context7-glassmorphism.js)

### **Glassmorphism Animations & Effects**
```javascript
// Context7 Glassmorphism Framework - Kod örneği için yukarıdaki dosya linkini kullanın
Context7.Glassmorphism = {
    /**
     * Initialize glassmorphism effects
     */
    init: function() {
        this.initHoverEffects();
        this.initScrollEffects();
        this.initParallaxEffects();
        this.initGlassCards();
    },

    /**
     * Initialize hover effects for glass elements
     */
    initHoverEffects: function() {
        const glassElements = document.querySelectorAll('.glass-card, .glassmorphism-card, .glass-container');
        
        glassElements.forEach(element => {
            element.addEventListener('mouseenter', this.onGlassHover.bind(this));
            element.addEventListener('mouseleave', this.onGlassLeave.bind(this));
            element.addEventListener('mousemove', this.onGlassMove.bind(this));
        });
    },

    /**
     * Glass hover effect
     * @param {Event} e - Mouse event
     */
    onGlassHover: function(e) {
        const element = e.currentTarget;
        element.style.transform = 'translateY(-8px) scale(1.02)';
        element.style.boxShadow = '0 20px 40px rgba(31, 38, 135, 0.5)';
        element.style.borderColor = 'rgba(255, 255, 255, 0.4)';
    },

    /**
     * Glass leave effect
     * @param {Event} e - Mouse event
     */
    onGlassLeave: function(e) {
        const element = e.currentTarget;
        element.style.transform = 'translateY(0) scale(1)';
        element.style.boxShadow = '0 8px 32px rgba(31, 38, 135, 0.37)';
        element.style.borderColor = 'rgba(255, 255, 255, 0.18)';
    },

    /**
     * Glass mouse move effect (subtle tilt)
     * @param {Event} e - Mouse event
     */
    onGlassMove: function(e) {
        const element = e.currentTarget;
        const rect = element.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / centerY * 5;
        const rotateY = (centerX - x) / centerX * 5;
        
        element.style.transform = `translateY(-8px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    },

    /**
     * Initialize scroll-based glass effects
     */
    initScrollEffects: function() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('glass-fade-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.glass-card, .glassmorphism-card').forEach(card => {
            observer.observe(card);
        });
    },

    /**
     * Initialize parallax effects for glass elements
     */
    initParallaxEffects: function() {
        const parallaxElements = document.querySelectorAll('.glass-parallax');
        
        window.addEventListener('scroll', Context7.Utils.throttle(() => {
            const scrollY = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const speed = element.dataset.speed || 0.5;
                const yPos = -(scrollY * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        }, 16));
    },

    /**
     * Initialize interactive glass cards
     */
    initGlassCards: function() {
        const cards = document.querySelectorAll('.interactive-glass-card');
        
        cards.forEach(card => {
            card.addEventListener('click', this.onCardClick.bind(this));
        });
    },

    /**
     * Handle glass card click
     * @param {Event} e - Click event
     */
    onCardClick: function(e) {
        const card = e.currentTarget;
        
        // Create ripple effect
        const ripple = document.createElement('div');
        ripple.className = 'glass-ripple';
        
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        card.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 1000);
    },

    /**
     * Create floating glass particles effect
     * @param {HTMLElement} container - Container element
     */
    createFloatingParticles: function(container) {
        const particleCount = 20;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'glass-particle';
            
            const size = Math.random() * 4 + 2;
            const x = Math.random() * container.offsetWidth;
            const y = Math.random() * container.offsetHeight;
            const duration = Math.random() * 20 + 10;
            
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';
            particle.style.animationDuration = duration + 's';
            
            container.appendChild(particle);
        }
    }
};
```

---

## 📝 **3. Form Handling & Validation**
**📄 Dosya**: `static/js/context7-forms.js`
**📄 Dosya Linki**: [`docs/examples/js/context7-forms.js`](../examples/js/context7-forms.js)

### **Advanced Form Management**
```javascript
// Context7 Form Management System - Kod örneği için yukarıdaki dosya linkini kullanın
Context7.Forms = {
    /**
     * Initialize form handling
     */
    init: function() {
        this.initValidation();
        this.initAjaxForms();
        this.initFileUploads();
        this.initDatePickers();
        this.initSelectEnhancements();
    },

    /**
     * Initialize real-time form validation
     */
    initValidation: function() {
        const forms = document.querySelectorAll('.context7-form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach(input => {
                input.addEventListener('blur', this.validateField.bind(this));
                input.addEventListener('input', Context7.Utils.debounce(this.validateField.bind(this), 300));
            });
            
            form.addEventListener('submit', this.handleSubmit.bind(this));
        });
    },

    /**
     * Validate individual form field
     * @param {Event} e - Input event
     */
    validateField: function(e) {
        const field = e.target;
        const value = field.value.trim();
        const rules = this.getValidationRules(field);
        
        let isValid = true;
        let errorMessage = '';
        
        // Required validation
        if (rules.required && !value) {
            isValid = false;
            errorMessage = 'Bu alan zorunludur.';
        }
        
        // Email validation
        if (rules.email && value && !Context7.Utils.validateEmail(value)) {
            isValid = false;
            errorMessage = 'Geçerli bir email adresi giriniz.';
        }
        
        // Min length validation
        if (rules.minLength && value.length < rules.minLength) {
            isValid = false;
            errorMessage = `En az ${rules.minLength} karakter olmalıdır.`;
        }
        
        // Max length validation
        if (rules.maxLength && value.length > rules.maxLength) {
            isValid = false;
            errorMessage = `En fazla ${rules.maxLength} karakter olabilir.`;
        }
        
        // Pattern validation
        if (rules.pattern && value && !new RegExp(rules.pattern).test(value)) {
            isValid = false;
            errorMessage = rules.patternMessage || 'Geçersiz format.';
        }
        
        this.showFieldValidation(field, isValid, errorMessage);
        return isValid;
    },

    /**
     * Get validation rules for field
     * @param {HTMLElement} field - Input field
     * @returns {Object} Validation rules
     */
    getValidationRules: function(field) {
        return {
            required: field.hasAttribute('required'),
            email: field.type === 'email',
            minLength: field.getAttribute('minlength'),
            maxLength: field.getAttribute('maxlength'),
            pattern: field.getAttribute('pattern'),
            patternMessage: field.getAttribute('data-pattern-message')
        };
    },

    /**
     * Show field validation result
     * @param {HTMLElement} field - Input field
     * @param {boolean} isValid - Is field valid
     * @param {string} message - Error message
     */
    showFieldValidation: function(field, isValid, message) {
        const wrapper = field.closest('.form-group') || field.closest('.mb-3');
        const feedback = wrapper?.querySelector('.invalid-feedback') || wrapper?.querySelector('.field-error');
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            if (feedback) feedback.textContent = '';
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            if (feedback) feedback.textContent = message;
        }
    },

    /**
     * Handle form submission
     * @param {Event} e - Submit event
     */
    handleSubmit: function(e) {
        const form = e.target;
        const inputs = form.querySelectorAll('input, select, textarea');
        
        let isFormValid = true;
        
        // Validate all fields
        inputs.forEach(input => {
            if (!this.validateField({ target: input })) {
                isFormValid = false;
            }
        });
        
        if (!isFormValid) {
            e.preventDefault();
            this.showFormError('Lütfen tüm alanları doğru şekilde doldurunuz.');
            return false;
        }
        
        // Show loading state
        this.showFormLoading(form);
        
        return true;
    },

    /**
     * Initialize AJAX form submissions
     */
    initAjaxForms: function() {
        const ajaxForms = document.querySelectorAll('.ajax-form');
        
        ajaxForms.forEach(form => {
            form.addEventListener('submit', this.handleAjaxSubmit.bind(this));
        });
    },

    /**
     * Handle AJAX form submission
     * @param {Event} e - Submit event
     */
    handleAjaxSubmit: function(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        const url = form.action || window.location.href;
        const method = form.method || 'POST';
        
        // Add CSRF token
        const csrfToken = Context7.Utils.getCSRFToken();
        if (csrfToken) {
            formData.append('csrfmiddlewaretoken', csrfToken);
        }
        
        this.showFormLoading(form);
        
        fetch(url, {
            method: method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            this.hideFormLoading(form);
            
            if (data.success) {
                this.showFormSuccess(data.message || 'İşlem başarıyla tamamlandı.');
                if (data.redirect) {
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1500);
                }
            } else {
                this.showFormError(data.message || 'Bir hata oluştu.');
                if (data.errors) {
                    this.showFieldErrors(form, data.errors);
                }
            }
        })
        .catch(error => {
            this.hideFormLoading(form);
            this.showFormError('Bağlantı hatası oluştu.');
            console.error('Form submission error:', error);
        });
    },

    /**
     * Show form loading state
     * @param {HTMLElement} form - Form element
     */
    showFormLoading: function(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Yükleniyor...';
        }
    },

    /**
     * Hide form loading state
     * @param {HTMLElement} form - Form element
     */
    hideFormLoading: function(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = submitBtn.getAttribute('data-original-text') || 'Kaydet';
        }
    },

    /**
     * Show form success message
     * @param {string} message - Success message
     */
    showFormSuccess: function(message) {
        Context7.Notifications.show(message, 'success');
    },

    /**
     * Show form error message
     * @param {string} message - Error message
     */
    showFormError: function(message) {
        Context7.Notifications.show(message, 'error');
    },

    /**
     * Show field-specific errors
     * @param {HTMLElement} form - Form element
     * @param {Object} errors - Field errors
     */
    showFieldErrors: function(form, errors) {
        Object.keys(errors).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                this.showFieldValidation(field, false, errors[fieldName]);
            }
        });
    }
};
```

---

## 📊 **4. Table Interactions & Data Management**
**📄 Dosya**: `static/js/context7-tables.js`

### **Advanced Table Features**
```javascript
/**
 * Context7 Table Management System
 * Sorting, filtering, pagination, and interactions
 */

Context7.Tables = {
    /**
     * Initialize table features
     */
    init: function() {
        this.initSorting();
        this.initFiltering();
        this.initPagination();
        this.initRowSelection();
        this.initBulkActions();
    },

    /**
     * Initialize table sorting
     */
    initSorting: function() {
        const tables = document.querySelectorAll('.sortable-table');
        
        tables.forEach(table => {
            const headers = table.querySelectorAll('th[data-sortable]');
            
            headers.forEach(header => {
                header.style.cursor = 'pointer';
                header.addEventListener('click', this.handleSort.bind(this));
                
                // Add sort indicator
                const indicator = document.createElement('i');
                indicator.className = 'fas fa-sort sort-indicator';
                header.appendChild(indicator);
            });
        });
    },

    /**
     * Handle table sorting
     * @param {Event} e - Click event
     */
    handleSort: function(e) {
        const header = e.currentTarget;
        const table = header.closest('table');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const column = header.getAttribute('data-sortable');
        const columnIndex = Array.from(header.parentElement.children).indexOf(header);
        
        // Determine sort direction
        let direction = 'asc';
        if (header.classList.contains('sort-asc')) {
            direction = 'desc';
        }
        
        // Reset all headers
        table.querySelectorAll('th').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
            const indicator = th.querySelector('.sort-indicator');
            if (indicator) {
                indicator.className = 'fas fa-sort sort-indicator';
            }
        });
        
        // Set current header
        header.classList.add(`sort-${direction}`);
        const indicator = header.querySelector('.sort-indicator');
        if (indicator) {
            indicator.className = `fas fa-sort-${direction === 'asc' ? 'up' : 'down'} sort-indicator`;
        }
        
        // Sort rows
        rows.sort((a, b) => {
            const aValue = a.children[columnIndex].textContent.trim();
            const bValue = b.children[columnIndex].textContent.trim();
            
            // Try to parse as numbers
            const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, ''));
            const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, ''));
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return direction === 'asc' ? aNum - bNum : bNum - aNum;
            }
            
            // String comparison
            return direction === 'asc' ? 
                aValue.localeCompare(bValue, 'tr') : 
                bValue.localeCompare(aValue, 'tr');
        });
        
        // Re-append sorted rows
        rows.forEach(row => tbody.appendChild(row));
        
        // Emit sort event
        Context7.Events.emit('table:sorted', {
            table: table,
            column: column,
            direction: direction
        });
    },

    /**
     * Initialize table filtering
     */
    initFiltering: function() {
        const searchInputs = document.querySelectorAll('.table-search');
        
        searchInputs.forEach(input => {
            const tableId = input.getAttribute('data-table');
            const table = document.getElementById(tableId);
            
            if (table) {
                input.addEventListener('input', Context7.Utils.debounce((e) => {
                    this.filterTable(table, e.target.value);
                }, 300));
            }
        });
    },

    /**
     * Filter table rows
     * @param {HTMLElement} table - Table element
     * @param {string} query - Search query
     */
    filterTable: function(table, query) {
        const rows = table.querySelectorAll('tbody tr');
        const searchTerm = query.toLowerCase();
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const shouldShow = text.includes(searchTerm);
            
            row.style.display = shouldShow ? '' : 'none';
            
            if (shouldShow) {
                row.classList.remove('filtered-out');
            } else {
                row.classList.add('filtered-out');
            }
        });
        
        // Update row count
        const visibleRows = table.querySelectorAll('tbody tr:not(.filtered-out)');
        const counter = table.parentElement.querySelector('.table-row-count');
        if (counter) {
            counter.textContent = `${visibleRows.length} kayıt gösteriliyor`;
        }
        
        // Emit filter event
        Context7.Events.emit('table:filtered', {
            table: table,
            query: query,
            visibleRows: visibleRows.length
        });
    },

    /**
     * Initialize row selection
     */
    initRowSelection: function() {
        const tables = document.querySelectorAll('.selectable-table');
        
        tables.forEach(table => {
            // Master checkbox
            const masterCheckbox = table.querySelector('.select-all');
            if (masterCheckbox) {
                masterCheckbox.addEventListener('change', this.handleSelectAll.bind(this));
            }
            
            // Row checkboxes
            const rowCheckboxes = table.querySelectorAll('.select-row');
            rowCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', this.handleRowSelect.bind(this));
            });
        });
    },

    /**
     * Handle select all
     * @param {Event} e - Change event
     */
    handleSelectAll: function(e) {
        const table = e.target.closest('table');
        const rowCheckboxes = table.querySelectorAll('.select-row');
        
        rowCheckboxes.forEach(checkbox => {
            checkbox.checked = e.target.checked;
        });
        
        this.updateBulkActions(table);
    },

    /**
     * Handle row selection
     * @param {Event} e - Change event
     */
    handleRowSelect: function(e) {
        const table = e.target.closest('table');
        const masterCheckbox = table.querySelector('.select-all');
        const rowCheckboxes = table.querySelectorAll('.select-row');
        const checkedRows = table.querySelectorAll('.select-row:checked');
        
        // Update master checkbox
        if (masterCheckbox) {
            masterCheckbox.checked = checkedRows.length === rowCheckboxes.length;
            masterCheckbox.indeterminate = checkedRows.length > 0 && checkedRows.length < rowCheckboxes.length;
        }
        
        this.updateBulkActions(table);
    },

    /**
     * Update bulk actions visibility
     * @param {HTMLElement} table - Table element
     */
    updateBulkActions: function(table) {
        const checkedRows = table.querySelectorAll('.select-row:checked');
        const bulkActions = table.parentElement.querySelector('.bulk-actions');
        
        if (bulkActions) {
            if (checkedRows.length > 0) {
                bulkActions.style.display = 'block';
                bulkActions.querySelector('.selected-count').textContent = checkedRows.length;
            } else {
                bulkActions.style.display = 'none';
            }
        }
        
        // Emit selection event
        Context7.Events.emit('table:selection-changed', {
            table: table,
            selectedCount: checkedRows.length,
            selectedRows: Array.from(checkedRows)
        });
    },

    /**
     * Initialize bulk actions
     */
    initBulkActions: function() {
        const bulkActionButtons = document.querySelectorAll('.bulk-action');
        
        bulkActionButtons.forEach(button => {
            button.addEventListener('click', this.handleBulkAction.bind(this));
        });
    },

    /**
     * Handle bulk action
     * @param {Event} e - Click event
     */
    handleBulkAction: function(e) {
        const button = e.target;
        const action = button.getAttribute('data-action');
        const table = button.closest('.table-container').querySelector('table');
        const selectedRows = table.querySelectorAll('.select-row:checked');
        
        if (selectedRows.length === 0) {
            Context7.Notifications.show('Lütfen en az bir kayıt seçiniz.', 'warning');
            return;
        }
        
        const selectedIds = Array.from(selectedRows).map(checkbox => checkbox.value);
        
        // Emit bulk action event
        Context7.Events.emit('table:bulk-action', {
            action: action,
            selectedIds: selectedIds,
            table: table
        });
    }
};
```

---

## 📈 **5. Chart.js Integration**
**📄 Dosya**: `static/js/context7-charts.js`

### **Advanced Chart Management**
```javascript
/**
 * Context7 Chart Management System
 * Chart.js integration with Context7 theming
 */

Context7.Charts = {
    defaultOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#6c757d',
                    font: {
                        family: 'Inter, sans-serif',
                        size: 12
                    }
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: '#6c757d'
                }
            },
            y: {
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                },
                ticks: {
                    color: '#6c757d'
                }
            }
        }
    },

    /**
     * Initialize charts
     */
    init: function() {
        this.initDashboardCharts();
        this.initReportCharts();
        this.initRealTimeCharts();
    },

    /**
     * Create line chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Chart data
     * @param {Object} options - Chart options
     * @returns {Chart} Chart instance
     */
    createLineChart: function(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const config = {
            type: 'line',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options,
                elements: {
                    line: {
                        borderWidth: 3,
                        tension: 0.4
                    },
                    point: {
                        radius: 4,
                        hoverRadius: 8
                    }
                }
            }
        };

        return new Chart(ctx, config);
    },

    /**
     * Create bar chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Chart data
     * @param {Object} options - Chart options
     * @returns {Chart} Chart instance
     */
    createBarChart: function(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const config = {
            type: 'bar',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options,
                elements: {
                    bar: {
                        borderRadius: 8,
                        borderSkipped: false
                    }
                }
            }
        };

        return new Chart(ctx, config);
    },

    /**
     * Create doughnut chart
     * @param {string} canvasId - Canvas element ID
     * @param {Object} data - Chart data
     * @param {Object} options - Chart options
     * @returns {Chart} Chart instance
     */
    createDoughnutChart: function(canvasId, data, options = {}) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const config = {
            type: 'doughnut',
            data: data,
            options: {
                ...this.defaultOptions,
                ...options,
                cutout: '70%',
                elements: {
                    arc: {
                        borderWidth: 0
                    }
                }
            }
        };

        return new Chart(ctx, config);
    },

    /**
     * Initialize dashboard charts
     */
    initDashboardCharts: function() {
        // Sales chart
        if (document.getElementById('salesChart')) {
            this.createSalesChart();
        }

        // Production chart
        if (document.getElementById('productionChart')) {
            this.createProductionChart();
        }

        // Quality metrics chart
        if (document.getElementById('qualityChart')) {
            this.createQualityChart();
        }
    },

    /**
     * Create sales chart
     */
    createSalesChart: function() {
        const data = {
            labels: ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran'],
            datasets: [{
                label: 'Satış Tutarı',
                data: [120000, 150000, 180000, 160000, 200000, 220000],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                fill: true
            }]
        };

        return this.createLineChart('salesChart', data);
    },

    /**
     * Create production chart
     */
    createProductionChart: function() {
        const data = {
            labels: ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma'],
            datasets: [{
                label: 'Üretim Miktarı',
                data: [85, 92, 78, 95, 88],
                backgroundColor: [
                    '#667eea',
                    '#764ba2',
                    '#f093fb',
                    '#f5576c',
                    '#4facfe'
                ]
            }]
        };

        return this.createBarChart('productionChart', data);
    },

    /**
     * Create quality metrics chart
     */
    createQualityChart: function() {
        const data = {
            labels: ['Geçti', 'Reddedildi', 'Beklemede'],
            datasets: [{
                data: [85, 10, 5],
                backgroundColor: [
                    '#28a745',
                    '#dc3545',
                    '#ffc107'
                ]
            }]
        };

        return this.createDoughnutChart('qualityChart', data);
    },

    /**
     * Update chart data
     * @param {Chart} chart - Chart instance
     * @param {Object} newData - New data
     */
    updateChart: function(chart, newData) {
        if (!chart) return;

        chart.data = newData;
        chart.update('active');
    },

    /**
     * Initialize real-time charts
     */
    initRealTimeCharts: function() {
        const realTimeCharts = document.querySelectorAll('.real-time-chart');
        
        realTimeCharts.forEach(canvas => {
            const updateInterval = canvas.getAttribute('data-update-interval') || 5000;
            const dataUrl = canvas.getAttribute('data-url');
            
            if (dataUrl) {
                setInterval(() => {
                    this.updateRealTimeChart(canvas, dataUrl);
                }, updateInterval);
            }
        });
    },

    /**
     * Update real-time chart
     * @param {HTMLElement} canvas - Canvas element
     * @param {string} dataUrl - Data URL
     */
    updateRealTimeChart: function(canvas, dataUrl) {
        fetch(dataUrl)
            .then(response => response.json())
            .then(data => {
                const chart = Chart.getChart(canvas);
                if (chart) {
                    this.updateChart(chart, data);
                }
            })
            .catch(error => {
                console.error('Real-time chart update error:', error);
            });
    }
};
```

---

## 🔔 **6. Notification System**
**📄 Dosya**: `static/js/context7-notifications.js`

### **Advanced Notification Management**
```javascript
/**
 * Context7 Notification System
 * Toast notifications, alerts, and user feedback
 */

Context7.Notifications = {
    container: null,
    notifications: [],

    /**
     * Initialize notification system
     */
    init: function() {
        this.createContainer();
        this.bindEvents();
    },

    /**
     * Create notification container
     */
    createContainer: function() {
        this.container = document.createElement('div');
        this.container.id = 'context7-notifications';
        this.container.className = 'notification-container';
        document.body.appendChild(this.container);
    },

    /**
     * Show notification
     * @param {string} message - Notification message
     * @param {string} type - Notification type (success, error, warning, info)
     * @param {Object} options - Additional options
     */
    show: function(message, type = 'info', options = {}) {
        const notification = this.createNotification(message, type, options);
        this.container.appendChild(notification);
        this.notifications.push(notification);

        // Trigger entrance animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Auto-hide
        const duration = options.duration || this.getDefaultDuration(type);
        if (duration > 0) {
            setTimeout(() => {
                this.hide(notification);
            }, duration);
        }

        return notification;
    },

    /**
     * Create notification element
     * @param {string} message - Notification message
     * @param {string} type - Notification type
     * @param {Object} options - Additional options
     * @returns {HTMLElement} Notification element
     */
    createNotification: function(message, type, options) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icon = this.getTypeIcon(type);
        const closeBtn = options.closable !== false ? '<button class="notification-close">&times;</button>' : '';
        
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    <i class="${icon}"></i>
                </div>
                <div class="notification-message">
                    ${Context7.Utils.sanitizeHTML(message)}
                </div>
                ${closeBtn}
            </div>
        `;

        // Add close functionality
        if (options.closable !== false) {
            const closeButton = notification.querySelector('.notification-close');
            closeButton.addEventListener('click', () => this.hide(notification));
        }

        return notification;
    },

    /**
     * Hide notification
     * @param {HTMLElement} notification - Notification element
     */
    hide: function(notification) {
        if (!notification || !notification.parentElement) return;

        notification.classList.add('hide');
        
        setTimeout(() => {
            if (notification.parentElement) {
                notification.parentElement.removeChild(notification);
            }
            
            const index = this.notifications.indexOf(notification);
            if (index > -1) {
                this.notifications.splice(index, 1);
            }
        }, 300);
    },

    /**
     * Get default duration for notification type
     * @param {string} type - Notification type
     * @returns {number} Duration in milliseconds
     */
    getDefaultDuration: function(type) {
        const durations = {
            success: 4000,
            error: 6000,
            warning: 5000,
            info: 4000
        };
        return durations[type] || 4000;
    },

    /**
     * Get icon for notification type
     * @param {string} type - Notification type
     * @returns {string} Icon class
     */
    getTypeIcon: function(type) {
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        return icons[type] || icons.info;
    },

    /**
     * Show success notification
     * @param {string} message - Success message
     * @param {Object} options - Additional options
     */
    success: function(message, options = {}) {
        return this.show(message, 'success', options);
    },

    /**
     * Show error notification
     * @param {string} message - Error message
     * @param {Object} options - Additional options
     */
    error: function(message, options = {}) {
        return this.show(message, 'error', options);
    },

    /**
     * Show warning notification
     * @param {string} message - Warning message
     * @param {Object} options - Additional options
     */
    warning: function(message, options = {}) {
        return this.show(message, 'warning', options);
    },

    /**
     * Show info notification
     * @param {string} message - Info message
     * @param {Object} options - Additional options
     */
    info: function(message, options = {}) {
        return this.show(message, 'info', options);
    },

    /**
     * Clear all notifications
     */
    clearAll: function() {
        this.notifications.forEach(notification => {
            this.hide(notification);
        });
    },

    /**
     * Bind global events
     */
    bindEvents: function() {
        // Listen for Django messages
        const djangoMessages = document.querySelectorAll('.django-message');
        djangoMessages.forEach(message => {
            const type = message.getAttribute('data-type') || 'info';
            const text = message.textContent.trim();
            
            if (text) {
                this.show(text, type);
            }
            
            // Hide Django message element
            message.style.display = 'none';
        });

        // Listen for AJAX errors
        Context7.Events.on('ajax:error', (data) => {
            this.error(data.message || 'Bir hata oluştu.');
        });

        // Listen for AJAX success
        Context7.Events.on('ajax:success', (data) => {
            if (data.message) {
                this.success(data.message);
            }
        });
    }
};
```

---

## 🔗 **7. API Client & AJAX Utilities**
**📄 Dosya**: `static/js/context7-api.js`

### **Advanced API Management**
```javascript
/**
 * Context7 API Client
 * Modern fetch-based API client with error handling
 */

Context7.API = {
    baseURL: '/api/v1/',
    defaultHeaders: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    },

    /**
     * Initialize API client
     */
    init: function() {
        this.setupInterceptors();
        this.bindGlobalEvents();
    },

    /**
     * Setup request/response interceptors
     */
    setupInterceptors: function() {
        // Add CSRF token to all requests
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            const [url, options = {}] = args;
            
            // Add CSRF token for non-GET requests
            if (options.method && options.method.toUpperCase() !== 'GET') {
                const csrfToken = Context7.Utils.getCSRFToken();
                if (csrfToken) {
                    options.headers = {
                        ...options.headers,
                        'X-CSRFToken': csrfToken
                    };
                }
            }
            
            return originalFetch.apply(this, [url, options]);
        };
    },

    /**
     * Make API request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Request options
     * @returns {Promise} Response promise
     */
    request: function(endpoint, options = {}) {
        const url = endpoint.startsWith('http') ? endpoint : this.baseURL + endpoint;
        const config = {
            headers: {
                ...this.defaultHeaders,
                ...options.headers
            },
            ...options
        };

        return fetch(url, config)
            .then(response => this.handleResponse(response))
            .catch(error => this.handleError(error));
    },

    /**
     * Handle API response
     * @param {Response} response - Fetch response
     * @returns {Promise} Parsed response
     */
    handleResponse: function(response) {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        }

        return response.text();
    },

    /**
     * Handle API error
     * @param {Error} error - Error object
     */
    handleError: function(error) {
        console.error('API Error:', error);
        
        Context7.Events.emit('api:error', {
            message: error.message,
            error: error
        });

        throw error;
    },

    /**
     * GET request
     * @param {string} endpoint - API endpoint
     * @param {Object} params - Query parameters
     * @param {Object} options - Request options
     * @returns {Promise} Response promise
     */
    get: function(endpoint, params = {}, options = {}) {
        const url = new URL(endpoint, window.location.origin);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                url.searchParams.append(key, params[key]);
            }
        });

        return this.request(url.pathname + url.search, {
            method: 'GET',
            ...options
        });
    },

    /**
     * POST request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request data
     * @param {Object} options - Request options
     * @returns {Promise} Response promise
     */
    post: function(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
            ...options
        });
    },

    /**
     * PUT request
     * @param {string} endpoint - API endpoint
     * @param {Object} data - Request data
     * @param {Object} options - Request options
     * @returns {Promise} Response promise
     */
    put: function(endpoint, data = {}, options = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
            ...options
        });
    },

    /**
     * DELETE request
     * @param {string} endpoint - API endpoint
     * @param {Object} options - Request options
     * @returns {Promise} Response promise
     */
    delete: function(endpoint, options = {}) {
        return this.request(endpoint, {
            method: 'DELETE',
            ...options
        });
    },

    /**
     * Upload file
     * @param {string} endpoint - API endpoint
     * @param {File} file - File to upload
     * @param {Object} options - Request options
     * @returns {Promise} Response promise
     */
    upload: function(endpoint, file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);

        return this.request(endpoint, {
            method: 'POST',
            body: formData,
            headers: {
                // Remove Content-Type to let browser set it with boundary
                ...options.headers,
                'Content-Type': undefined
            },
            ...options
        });
    },

    /**
     * Bind global events
     */
    bindGlobalEvents: function() {
        // Handle API errors globally
        Context7.Events.on('api:error', (data) => {
            Context7.Notifications.error(data.message || 'API hatası oluştu.');
        });
    }
};
```

---

## 🔍 **8. Search & Filtering System**
**📄 Dosya**: `static/js/context7-search.js`

### **Advanced Search Features**
```javascript
/**
 * Context7 Search & Filtering System
 * Advanced search with real-time filtering
 */

Context7.Search = {
    searchInstances: new Map(),

    /**
     * Initialize search functionality
     */
    init: function() {
        this.initGlobalSearch();
        this.initAdvancedSearch();
        this.initFilterPanels();
    },

    /**
     * Initialize global search
     */
    initGlobalSearch: function() {
        const globalSearch = document.getElementById('globalSearch');
        if (globalSearch) {
            globalSearch.addEventListener('input', Context7.Utils.debounce((e) => {
                this.performGlobalSearch(e.target.value);
            }, 300));
        }
    },

    /**
     * Perform global search
     * @param {string} query - Search query
     */
    performGlobalSearch: function(query) {
        if (query.length < 2) return;

        Context7.API.get('search/global/', { q: query })
            .then(results => {
                this.displayGlobalResults(results);
            })
            .catch(error => {
                console.error('Global search error:', error);
            });
    },

    /**
     * Display global search results
     * @param {Object} results - Search results
     */
    displayGlobalResults: function(results) {
        const dropdown = document.getElementById('globalSearchDropdown');
        if (!dropdown) return;

        let html = '';
        
        Object.keys(results).forEach(category => {
            if (results[category].length > 0) {
                html += `<div class="search-category">
                    <h6 class="search-category-title">${category}</h6>
                    <div class="search-results">`;
                
                results[category].forEach(item => {
                    html += `<a href="${item.url}" class="search-result-item">
                        <div class="search-result-icon">
                            <i class="${item.icon || 'fas fa-file'}"></i>
                        </div>
                        <div class="search-result-content">
                            <div class="search-result-title">${item.title}</div>
                            <div class="search-result-description">${item.description || ''}</div>
                        </div>
                    </a>`;
                });
                
                html += '</div></div>';
            }
        });

        dropdown.innerHTML = html;
        dropdown.style.display = 'block';
    },

    /**
     * Initialize advanced search
     */
    initAdvancedSearch: function() {
        const advancedSearchForms = document.querySelectorAll('.advanced-search-form');
        
        advancedSearchForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performAdvancedSearch(form);
            });

            // Real-time search on input
            const inputs = form.querySelectorAll('input, select');
            inputs.forEach(input => {
                input.addEventListener('input', Context7.Utils.debounce(() => {
                    this.performAdvancedSearch(form);
                }, 500));
            });
        });
    },

    /**
     * Perform advanced search
     * @param {HTMLElement} form - Search form
     */
    performAdvancedSearch: function(form) {
        const formData = new FormData(form);
        const params = Object.fromEntries(formData.entries());
        const endpoint = form.getAttribute('data-endpoint') || 'search/advanced/';
        
        Context7.API.get(endpoint, params)
            .then(results => {
                this.displayAdvancedResults(form, results);
            })
            .catch(error => {
                console.error('Advanced search error:', error);
            });
    },

    /**
     * Display advanced search results
     * @param {HTMLElement} form - Search form
     * @param {Object} results - Search results
     */
    displayAdvancedResults: function(form, results) {
        const resultsContainer = form.parentElement.querySelector('.search-results-container');
        if (!resultsContainer) return;

        let html = '';
        
        if (results.items && results.items.length > 0) {
            html += `<div class="search-results-header">
                <h5>${results.total} sonuç bulundu</h5>
                <div class="search-results-actions">
                    <button class="btn btn-sm btn-outline-primary" onclick="Context7.Search.exportResults('${form.id}')">
                        <i class="fas fa-download"></i> Dışa Aktar
                    </button>
                </div>
            </div>`;
            
            html += '<div class="search-results-list">';
            
            results.items.forEach(item => {
                html += this.renderSearchResultItem(item);
            });
            
            html += '</div>';
            
            // Pagination
            if (results.pagination) {
                html += this.renderPagination(results.pagination);
            }
        } else {
            html = '<div class="search-no-results">Hiç sonuç bulunamadı.</div>';
        }

        resultsContainer.innerHTML = html;
    },

    /**
     * Render search result item
     * @param {Object} item - Search result item
     * @returns {string} HTML string
     */
    renderSearchResultItem: function(item) {
        return `<div class="search-result-card">
            <div class="search-result-header">
                <h6 class="search-result-title">
                    <a href="${item.url}">${item.title}</a>
                </h6>
                <div class="search-result-meta">
                    <span class="badge badge-${item.status_color}">${item.status}</span>
                    <small class="text-muted">${item.date}</small>
                </div>
            </div>
            <div class="search-result-body">
                <p class="search-result-description">${item.description || ''}</p>
                <div class="search-result-tags">
                    ${item.tags ? item.tags.map(tag => `<span class="badge badge-light">${tag}</span>`).join('') : ''}
                </div>
            </div>
        </div>`;
    },

    /**
     * Initialize filter panels
     */
    initFilterPanels: function() {
        const filterPanels = document.querySelectorAll('.filter-panel');
        
        filterPanels.forEach(panel => {
            const toggleBtn = panel.querySelector('.filter-toggle');
            const clearBtn = panel.querySelector('.filter-clear');
            const applyBtn = panel.querySelector('.filter-apply');
            
            if (toggleBtn) {
                toggleBtn.addEventListener('click', () => {
                    panel.classList.toggle('expanded');
                });
            }
            
            if (clearBtn) {
                clearBtn.addEventListener('click', () => {
                    this.clearFilters(panel);
                });
            }
            
            if (applyBtn) {
                applyBtn.addEventListener('click', () => {
                    this.applyFilters(panel);
                });
            }
        });
    },

    /**
     * Clear all filters
     * @param {HTMLElement} panel - Filter panel
     */
    clearFilters: function(panel) {
        const inputs = panel.querySelectorAll('input, select');
        inputs.forEach(input => {
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });
        
        this.applyFilters(panel);
    },

    /**
     * Apply filters
     * @param {HTMLElement} panel - Filter panel
     */
    applyFilters: function(panel) {
        const form = panel.querySelector('form') || panel.closest('form');
        if (form) {
            this.performAdvancedSearch(form);
        }
    },

    /**
     * Export search results
     * @param {string} formId - Form ID
     */
    exportResults: function(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        const formData = new FormData(form);
        const params = new URLSearchParams(formData);
        const endpoint = form.getAttribute('data-export-endpoint') || 'search/export/';
        
        // Create download link
        const downloadUrl = `${endpoint}?${params.toString()}`;
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = `search-results-${new Date().toISOString().split('T')[0]}.xlsx`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};
```

---

## 🎯 **JavaScript Implementation Guidelines**

### **1. Script Loading Order**
```html
<!-- Base Template -->
<script src="{% static 'js/context7-core.js' %}"></script>
<script src="{% static 'js/context7-glassmorphism.js' %}"></script>
<script src="{% static 'js/context7-notifications.js' %}"></script>
<script src="{% static 'js/context7-api.js' %}"></script>

<!-- Feature-specific scripts -->
<script src="{% static 'js/context7-forms.js' %}"></script>
<script src="{% static 'js/context7-tables.js' %}"></script>
<script src="{% static 'js/context7-search.js' %}"></script>
<script src="{% static 'js/context7-charts.js' %}"></script>

<!-- Page-specific scripts -->
<script src="{% static 'js/quality-control.js' %}"></script>
<script src="{% static 'js/context7-dashboard.js' %}"></script>
```

### **2. Initialization Pattern**
```javascript
// Initialize Context7 components when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Core initialization
    Context7.Notifications.init();
    Context7.API.init();
    Context7.Glassmorphism.init();
    
    // Feature initialization
    Context7.Forms.init();
    Context7.Tables.init();
    Context7.Search.init();
    Context7.Charts.init();
    
    // Custom page initialization
    if (typeof initPage === 'function') {
        initPage();
    }
});
```

### **3. Event Handling Best Practices**
```javascript
// Use Context7 event system for loose coupling
Context7.Events.on('form:submitted', function(data) {
    Context7.Notifications.success('Form başarıyla gönderildi');
});

// Use delegation for dynamic content
document.addEventListener('click', function(e) {
    if (e.target.matches('.dynamic-button')) {
        handleDynamicClick(e);
    }
});

// Clean up event listeners
window.addEventListener('beforeunload', function() {
    Context7.Events.listeners = {};
});
```

### **4. Error Handling Pattern**
```javascript
// Consistent error handling
function handleAsyncOperation() {
    return Context7.API.get('endpoint/')
        .then(data => {
            // Success handling
            return data;
        })
        .catch(error => {
            // Error logging
            console.error('Operation failed:', error);
            
            // User notification
            Context7.Notifications.error('İşlem başarısız oldu');
            
            // Re-throw for caller
            throw error;
        });
}
```

### **5. Performance Optimization**
```javascript
// Use debouncing for frequent events
const debouncedSearch = Context7.Utils.debounce(function(query) {
    performSearch(query);
}, 300);

// Use throttling for scroll events
const throttledScroll = Context7.Utils.throttle(function() {
    updateScrollPosition();
}, 16);

// Lazy load heavy components
function loadChartLibrary() {
    return import('./chart-library.js')
        .then(module => module.default);
}
```

---

## 📊 **Performance Metrics**

### **JavaScript Performance Targets**
- **Bundle Size**: < 200KB minified
- **Load Time**: < 500ms for core scripts
- **Memory Usage**: < 50MB for typical page
- **Event Response**: < 100ms for user interactions

### **Browser Support**
- **Chrome 90+**: Full ES6+ support
- **Firefox 88+**: Full modern JavaScript support
- **Safari 14+**: Webkit compatibility
- **Edge 90+**: Full feature support

---

**🎯 Mission**: Bu JavaScript referans guide'ı Context7 ERP sistemindeki tüm JavaScript dosyalarının kullanımını, yapısını ve best practices'lerini kapsamlı şekilde açıklar.

**📞 QMS Compliance**: Bu referans Context7 Central Protocol v1.0 standartlarına uygun olarak hazırlanmıştır.

---

*Context7 JavaScript Reference Guide - Complete Interactive Documentation for Enterprise ERP System* 