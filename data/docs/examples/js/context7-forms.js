/**
 * Context7 Form Management System
 * @version 2.2.0-glassmorphism-enhanced
 * @author Context7 Development Team
 * @date 11 Ocak 2025
 * @description Advanced form validation, submission, and UX
 */

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
        if (Context7.Notifications) {
            Context7.Notifications.show(message, 'success');
        }
    },

    /**
     * Show form error message
     * @param {string} message - Error message
     */
    showFormError: function(message) {
        if (Context7.Notifications) {
            Context7.Notifications.show(message, 'error');
        }
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