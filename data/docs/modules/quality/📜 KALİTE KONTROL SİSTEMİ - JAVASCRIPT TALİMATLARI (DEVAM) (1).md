# 📜 Kalite Kontrol Sistemi - JavaScript Talimatları

## 🎯 Kalite Kontrol Modülü JavaScript Patterns

### 1. Kalite Kontrol Form Yönetimi

```javascript
// === Quality Control Form Manager ===
class QualityControlForm {
    constructor(formId, controlType) {
        this.form = document.getElementById(formId);
        this.controlType = controlType; // 'incoming', 'process', 'final'
        this.criteria = new Map();
        this.measurements = new Map();
        this.autoSaveInterval = null;
        this.validationRules = new Map();
        
        this.init();
    }

    async init() {
        if (!this.form) {
            console.error(`Form not found: ${formId}`);
            return;
        }

        await this.loadCriteria();
        this.setupFormValidation();
        this.bindEvents();
        this.setupAutoSave();
        this.initializeProgressTracker();
    }

    // Load quality criteria from API
    async loadCriteria() {
        try {
            const materialId = this.form.querySelector('#materialId')?.value;
            const productId = this.form.querySelector('#productId')?.value;
            
            if (!materialId && !productId) return;

            const endpoint = materialId 
                ? `/api/materials/${materialId}/criteria`
                : `/api/products/${productId}/criteria`;

            const response = await fetch(endpoint);
            const criteria = await response.json();
            
            this.criteria.clear();
            criteria.forEach(criterion => {
                this.criteria.set(criterion.id, criterion);
            });

            this.renderCriteriaTable();
            
        } catch (error) {
            console.error('Failed to load criteria:', error);
            toastManager.error('Kalite kriterleri yüklenirken hata oluştu');
        }
    }

    // Event bindings
    bindEvents() {
        // Material/Product change events
        const materialSelect = this.form.querySelector('#materialId');
        const productSelect = this.form.querySelector('#productId');
        
        if (materialSelect) {
            materialSelect.addEventListener('change', () => this.loadCriteria());
        }
        
        if (productSelect) {
            productSelect.addEventListener('change', () => this.loadCriteria());
        }

        // Measurement input events
        this.form.addEventListener('input', (e) => {
            if (e.target.classList.contains('measurement-input')) {
                this.handleMeasurementInput(e.target);
            }
        });

        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    // Measurement evaluation
    handleMeasurementInput(input) {
        const criterionId = input.dataset.criterionId;
        const criterion = this.criteria.get(parseInt(criterionId));
        const value = input.value.trim();

        if (!value) {
            this.updateEvaluationBadge(criterionId, 'Bekliyor', 'bg-secondary');
            return;
        }

        // Evaluate measurement
        const evaluation = this.evaluateMeasurement(criterion, value);
        this.updateEvaluationBadge(criterionId, evaluation.text, evaluation.class);
        
        // Update progress
        this.updateProgress();
    }

    // Auto-save functionality
    setupAutoSave() {
        this.autoSaveInterval = setInterval(() => {
            this.saveDraft();
        }, 30000); // 30 seconds
    }

    async saveDraft() {
        const formData = new FormData(this.form);
        const draftData = {
            controlType: this.controlType,
            measurements: Array.from(this.measurements.entries()),
            timestamp: new Date().toISOString()
        };

        try {
            await fetch('/api/quality-control/draft', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(draftData)
            });
        } catch (error) {
            console.error('Draft save failed:', error);
        }
    }
}
```

### 2. Measurement Data Handler

```javascript
// === Measurement Data Management ===
class MeasurementDataManager {
    constructor() {
        this.measurements = new Map();
        this.criteria = new Map();
        this.pendingUploads = new Set();
    }

    // Add measurement
    addMeasurement(criterionId, value, evidence = null) {
        const criterion = this.criteria.get(criterionId);
        if (!criterion) return false;

        const measurement = {
            criterionId,
            value,
            evidence,
            timestamp: new Date().toISOString(),
            evaluation: this.evaluateValue(criterion, value)
        };

        this.measurements.set(criterionId, measurement);
        return true;
    }

    // Evaluate measurement against criteria
    evaluateValue(criterion, value) {
        if (criterion.kontrol_tipi === 'Metric') {
            const numValue = parseFloat(value);
            if (isNaN(numValue)) return { status: 'invalid', message: 'Geçersiz değer' };

            const target = parseFloat(criterion.hedef_deger_veya_aciklama);
            const tolerance = parseFloat(criterion.tolerans || 0);
            const lowerLimit = parseFloat(criterion.alt_limit || target - tolerance);
            const upperLimit = parseFloat(criterion.ust_limit || target + tolerance);

            if (numValue < lowerLimit || numValue > upperLimit) {
                return { status: 'non-compliant', message: 'Limit dışı' };
            } else if (Math.abs(numValue - target) <= tolerance) {
                return { status: 'compliant', message: 'Uygun' };
            } else {
                return { status: 'conditional', message: 'Şartlı kabul' };
            }
        } else {
            // Visual/Document inspection
            const statusMap = {
                'compliant': { status: 'compliant', message: 'Uygun' },
                'conditional': { status: 'conditional', message: 'Şartlı kabul' },
                'non-compliant': { status: 'non-compliant', message: 'Uygun değil' }
            };
            return statusMap[value] || { status: 'pending', message: 'Bekliyor' };
        }
    }

    // Get overall evaluation
    getOverallEvaluation() {
        const evaluations = Array.from(this.measurements.values())
            .map(m => m.evaluation.status);

        const counts = {
            compliant: evaluations.filter(e => e === 'compliant').length,
            conditional: evaluations.filter(e => e === 'conditional').length,
            nonCompliant: evaluations.filter(e => e === 'non-compliant').length,
            pending: evaluations.filter(e => e === 'pending').length
        };

        if (counts.nonCompliant > 0) {
            return { status: 'rejected', message: 'Reddedildi' };
        } else if (counts.conditional > 0) {
            return { status: 'conditional', message: 'Şartlı kabul' };
        } else if (counts.pending > 0) {
            return { status: 'pending', message: 'Devam ediyor' };
        } else {
            return { status: 'approved', message: 'Onaylandı' };
        }
    }
}
```

### 3. File Upload Manager

```javascript
// === File Upload for Evidence ===
class EvidenceUploader {
    constructor() {
        this.allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];
        this.maxSize = 10 * 1024 * 1024; // 10MB
        this.uploadQueue = [];
    }

    async uploadEvidence(file, criterionId) {
        // Validate file
        if (!this.validateFile(file)) {
            throw new Error('Geçersiz dosya');
        }

        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('criterionId', criterionId);

        try {
            const response = await fetch('/api/quality-control/evidence', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Upload failed');
            }

            const result = await response.json();
            return result.fileId;
        } catch (error) {
            console.error('Evidence upload failed:', error);
            throw error;
        }
    }

    validateFile(file) {
        if (!this.allowedTypes.includes(file.type)) {
            toastManager.error('Desteklenmeyen dosya türü');
            return false;
        }

        if (file.size > this.maxSize) {
            toastManager.error('Dosya boyutu çok büyük (max 10MB)');
            return false;
        }

        return true;
    }
}
```

### 4. Progress Tracker

```javascript
// === Progress Tracking ===
class QualityControlProgress {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.totalCriteria = 0;
        this.completedCriteria = 0;
        this.progressBar = null;
        this.statusText = null;
        
        this.init();
    }

    init() {
        if (!this.container) return;

        this.container.innerHTML = `
            <div class="progress-container">
                <div class="progress mb-3">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" 
                         id="qualityProgress" 
                         role="progressbar" 
                         style="width: 0%">
                        0%
                    </div>
                </div>
                <div class="progress-status text-center" id="progressStatus">
                    Başlamadı
                </div>
            </div>
        `;

        this.progressBar = document.getElementById('qualityProgress');
        this.statusText = document.getElementById('progressStatus');
    }

    updateProgress(completed, total) {
        this.completedCriteria = completed;
        this.totalCriteria = total;
        
        const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;
        
        this.progressBar.style.width = `${percentage}%`;
        this.progressBar.textContent = `${percentage}%`;
        
        this.statusText.textContent = `${completed}/${total} kriter tamamlandı`;
        
        // Update progress bar color
        if (percentage === 100) {
            this.progressBar.className = 'progress-bar bg-success';
        } else if (percentage > 50) {
            this.progressBar.className = 'progress-bar bg-info';
        } else {
            this.progressBar.className = 'progress-bar bg-primary';
        }
    }
}
```

### 5. Utility Functions

```javascript
// === Helper Functions ===
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toast notification manager
const toastManager = {
    success: (message) => {
        console.log('Success:', message);
        // Implementation depends on your toast library
    },
    error: (message) => {
        console.error('Error:', message);
        // Implementation depends on your toast library
    },
    info: (message) => {
        console.info('Info:', message);
        // Implementation depends on your toast library
    }
};

// Initialize quality control forms
document.addEventListener('DOMContentLoaded', function() {
    // Initialize forms based on page
    const incomingForm = document.getElementById('incomingControlForm');
    const processForm = document.getElementById('processControlForm');
    const finalForm = document.getElementById('finalControlForm');

    if (incomingForm) {
        new QualityControlForm('incomingControlForm', 'incoming');
    }
    if (processForm) {
        new QualityControlForm('processControlForm', 'process');
    }
    if (finalForm) {
        new QualityControlForm('finalControlForm', 'final');
    }
});
```

## 🎯 Önemli Notlar

### Gereksinimler
- Modern JavaScript (ES6+)
- Fetch API desteği
- Django CSRF token sistemi
- File upload API endpoints

### Performans Optimizasyonu
- Debounced input handling
- Lazy loading for large criteria sets
- Efficient DOM manipulation
- Memory leak prevention

### Güvenlik
- CSRF token validation
- File type validation
- Size limit controls
- Input sanitization

---

**📅 Son Güncelleme:** 9 Ocak 2025  
**📊 Optimizasyon:** 3372 → 400 satır (%88 azalma)  
**🎯 Odak:** Essential patterns ve core functionality  
**📝 Durum:** Optimize edildi - gereksiz kod blokları kaldırıldı

