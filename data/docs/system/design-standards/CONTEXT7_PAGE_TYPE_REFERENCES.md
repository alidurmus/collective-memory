# 🎨 Context7 ERP - Sayfa Türü Tasarım Referansları

**Version**: v2.2.0-glassmorphism-enhanced  
**Date**: 11 Ocak 2025  
**Status**: ✅ **ACTIVE DESIGN REFERENCES**  
**QMS Reference**: REC-DESIGN-REFERENCES-250111-001

---

## 🎯 **Sayfa Türü Analizi**

Context7 ERP sisteminde 3 ana sayfa türü tespit edilmiştir ve her biri için tasarım standartları oluşturulmuştur:

### **📊 Analiz Edilen Sayfalar**
1. **Detail Pages**: `/erp/production/orders/4b0808f4-1e3b-457e-b0cd-30c58a7ca0d3/`
2. **Create/Edit Forms**: `/erp/purchasing/orders/create/`
3. **Quality Edit Forms**: `/erp/quality/incoming/create/?edit=af5de92a-bfdf-4ab2-8c35-93acf694549b`

---

## 📋 **1. DETAIL PAGES (Detay Sayfaları)**

### **🔍 Referans**: Production Order Detail
**URL**: `/erp/production/orders/{id}/`

### **Yapısal Özellikler**
```html
<!-- Header Section -->
<div class="row mb-4">
    <div class="col-md-8">
        <h2>
            <i class="fas fa-icon me-2"></i>
            {Title} #{object.number}
            <span class="status-badge status-{status}">
                {Status Display}
            </span>
        </h2>
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <!-- Breadcrumb Navigation -->
            </ol>
        </nav>
    </div>
    <div class="col-md-4 text-end">
        <div class="btn-group" role="group">
            <!-- Action Buttons -->
        </div>
    </div>
</div>

<!-- Content Grid -->
<div class="row">
    <div class="col-lg-8">
        <!-- Main Content Cards -->
    </div>
    <div class="col-lg-4">
        <!-- Sidebar Cards -->
    </div>
</div>
```

### **CSS Standartları**
```css
/* Detail Section Cards */
.detail-section {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Status Badges */
.status-badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.status-planned { background-color: #fff3cd; color: #856404; }
.status-in_progress { background-color: #d1ecf1; color: #0c5460; }
.status-completed { background-color: #d4edda; color: #155724; }
.status-cancelled { background-color: #f8d7da; color: #721c24; }

/* Progress Indicators */
.progress-section {
    margin: 20px 0;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
}

.progress {
    height: 25px;
    font-size: 14px;
    border-radius: 12px;
    overflow: hidden;
}
```

### **Layout Pattern**
- **8/4 Grid**: Main content (col-lg-8) + Sidebar (col-lg-4)
- **Header Structure**: Title + Status + Breadcrumb + Actions
- **Card-based Content**: Information grouped in cards
- **Progress Indicators**: Visual progress bars for completion tracking
- **Quick Actions**: Context-sensitive action buttons

---

## 📝 **2. CREATE/EDIT FORMS (Form Sayfaları)**

### **🔍 Referans**: Purchase Order Create
**URL**: `/erp/purchasing/orders/create/`

### **Yapısal Özellikler**
```html
<!-- Header Section -->
<div class="d-sm-flex align-items-center justify-content-between mb-4">
    <div>
        <h1 class="h3 mb-0 text-gray-800">
            <i class="fas fa-plus mr-2"></i>
            New {Entity}
        </h1>
        <p class="text-muted mb-0">Create {entity} information</p>
    </div>
    <a href="{list_url}" class="btn btn-secondary">
        <i class="fas fa-arrow-left mr-2"></i>Back to List
    </a>
</div>

<!-- Form Grid -->
<div class="row">
    <div class="col-lg-8">
        <!-- Form Sections -->
        <div class="card shadow mb-4 glassmorphism-card">
            <div class="card-header glassmorphism-header">
                <h6 class="m-0 font-weight-bold text-primary">
                    <i class="fas fa-icon mr-2"></i>Section Title
                </h6>
            </div>
            <div class="card-body">
                <!-- Form Fields -->
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <!-- Help & Tips Sidebar -->
    </div>
</div>
```

### **CSS Standartları**
```css
/* Glassmorphism Cards */
.glassmorphism-card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    margin-bottom: 2rem;
}

.glassmorphism-header {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(25px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1.5rem;
    border-radius: 16px 16px 0 0;
}

/* Form Controls */
.form-control, .form-select {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
    background: white;
    border-color: rgba(102, 126, 234, 0.5);
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    outline: none;
}

/* Input Groups */
.input-group-text {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: #495057;
}

/* Help Sidebar */
.help-card {
    background: rgba(255, 193, 7, 0.1);
    border: 1px solid rgba(255, 193, 7, 0.3);
    border-radius: 12px;
    padding: 1.5rem;
}

.help-card .small {
    color: rgba(0, 0, 0, 0.7);
    line-height: 1.5;
}
```

### **Form Section Pattern**
- **Grouped Information**: Related fields in cards
- **Progressive Disclosure**: Basic → Financial → Additional info
- **Help Integration**: Tips and guidance in sidebar
- **Validation Ready**: Client-side validation classes
- **Responsive Layout**: Mobile-friendly form structure

---

## ✨ **3. QUALITY EDIT FORMS (Kalite Kontrol Formları)**

### **🔍 Referans**: Quality Control Edit
**URL**: `/erp/quality/incoming/create/?edit={id}`

### **Yapısal Özellikler**
```html
<!-- Glass Container Wrapper -->
<div class="glass-container">
    <h1 class="quality-header">{{ page_title }}</h1>
</div>

<!-- Form Sections -->
<div class="glass-container">
    <div class="form-section">
        <h3 class="section-title">
            <i class="fas fa-icon me-2"></i>Section Title
        </h3>
        <div class="row">
            <!-- Form Fields -->
        </div>
    </div>
</div>

<!-- Criteria Table -->
<div class="glass-container">
    <div class="criteria-table">
        <table class="table">
            <!-- Quality Criteria -->
        </table>
    </div>
</div>
```

### **CSS Standartları**
```css
/* Glass Container */
.glass-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    padding: 2rem;
    margin-bottom: 2rem;
}

/* Quality Header */
.quality-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    text-align: center;
    margin-bottom: 2rem;
}

/* Form Sections */
.form-section {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.section-title {
    color: white;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(102, 126, 234, 0.3);
}

/* Dark Theme Form Controls */
.form-control, .form-select {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: white;
    padding: 0.75rem;
}

.form-control:focus, .form-select:focus {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
    color: white;
    outline: none;
}

.form-control::placeholder {
    color: rgba(255, 255, 255, 0.7);
}

.form-label {
    color: white;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

/* Criteria Table */
.criteria-table {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    overflow: hidden;
}

.criteria-table th {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    padding: 0.75rem;
    border: none;
    font-weight: 600;
}

.criteria-table td {
    padding: 0.75rem;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
}
```

### **Quality Form Pattern**
- **Dark Glass Theme**: Enhanced glassmorphism with dark overlay
- **Section-based Layout**: Grouped form sections
- **Specialized Controls**: Quality-specific input types
- **Criteria Tables**: Structured quality measurement tables
- **Enhanced Visibility**: High contrast for quality data

---

## 🎨 **Unified Design Standards**

### **Common CSS Variables**
```css
:root {
    /* Layout */
    --content-padding: 2rem;
    --card-border-radius: 16px;
    --section-spacing: 2rem;
    
    /* Glassmorphism */
    --glass-bg-light: rgba(255, 255, 255, 0.15);
    --glass-bg-medium: rgba(255, 255, 255, 0.08);
    --glass-bg-dark: rgba(255, 255, 255, 0.05);
    --glass-border: rgba(255, 255, 255, 0.3);
    --glass-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    --backdrop-blur: 20px;
    --backdrop-blur-strong: 25px;
    
    /* Colors */
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --success-color: #28a745;
    --warning-color: #ffc107;
    --danger-color: #dc3545;
    --info-color: #17a2b8;
    
    /* Typography */
    --font-weight-normal: 500;
    --font-weight-bold: 600;
    --font-weight-black: 800;
    
    /* Animation */
    --transition-base: all 0.3s ease;
    --transition-spring: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### **Component Hierarchy**
```css
/* Page Wrapper */
.page-content {
    padding: var(--content-padding);
}

/* Section Cards */
.section-card {
    background: var(--glass-bg-light);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--card-border-radius);
    box-shadow: var(--glass-shadow);
    margin-bottom: var(--section-spacing);
    padding: 1.5rem;
}

/* Form Sections */
.form-section {
    background: var(--glass-bg-dark);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Action Buttons */
.action-button {
    background: var(--primary-gradient);
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    color: white;
    font-weight: var(--font-weight-bold);
    transition: var(--transition-spring);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

.action-button:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    color: white;
}
```

---

## 📱 **Responsive Design Patterns**

### **Breakpoint Behavior**
```css
/* Desktop (1200px+) */
@media (min-width: 1200px) {
    .detail-layout { grid-template-columns: 2fr 1fr; }
    .form-layout { grid-template-columns: 2fr 1fr; }
    .quality-layout { grid-template-columns: 1fr; }
}

/* Tablet (768px - 1199px) */
@media (min-width: 768px) and (max-width: 1199px) {
    .detail-layout { grid-template-columns: 1fr; }
    .form-layout { grid-template-columns: 1fr; }
    .section-card { padding: 1rem; }
}

/* Mobile (< 768px) */
@media (max-width: 767px) {
    .page-content { padding: 1rem; }
    .section-card { 
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 12px;
    }
    .action-button {
        width: 100%;
        justify-content: center;
        margin-bottom: 0.5rem;
    }
}
```

---

## 🔧 **Implementation Guidelines**

### **1. Detail Pages Checklist**
- [ ] **Header Structure**: Title + Status + Breadcrumb + Actions
- [ ] **8/4 Grid Layout**: Main content + Sidebar
- [ ] **Status Badges**: Consistent status visualization
- [ ] **Progress Indicators**: Visual completion tracking
- [ ] **Action Buttons**: Context-sensitive operations
- [ ] **Information Cards**: Grouped data presentation

### **2. Form Pages Checklist**
- [ ] **Header with Back Button**: Clear navigation
- [ ] **Glassmorphism Cards**: Section grouping
- [ ] **Progressive Disclosure**: Logical information flow
- [ ] **Help Sidebar**: User guidance
- [ ] **Validation Ready**: Client-side validation
- [ ] **Responsive Layout**: Mobile-friendly forms

### **3. Quality Forms Checklist**
- [ ] **Dark Glass Theme**: Enhanced glassmorphism
- [ ] **Section-based Layout**: Logical grouping
- [ ] **Specialized Controls**: Quality-specific inputs
- [ ] **Criteria Tables**: Structured measurements
- [ ] **High Contrast**: Enhanced visibility
- [ ] **White Text**: Dark theme compatibility

---

## 📊 **Performance Standards**

### **Loading Targets**
- **Detail Pages**: <1.5s first paint
- **Form Pages**: <2s interactive
- **Quality Forms**: <2.5s with criteria loading

### **Accessibility Standards**
- **WCAG 2.1 AA**: Full compliance
- **Keyboard Navigation**: Complete support
- **Screen Reader**: Compatible markup
- **Color Contrast**: 4.5:1 minimum ratio

### **Browser Support**
- **Chrome 90+**: Full glassmorphism support
- **Firefox 88+**: Fallback backgrounds
- **Safari 14+**: Webkit prefix support
- **Edge 90+**: Full feature support

---

## 🔄 **Maintenance & Updates**

### **Design Review Process**
1. **Monthly Review**: Consistency check across page types
2. **Quarterly Update**: Performance optimization
3. **Semi-annual Audit**: Accessibility compliance
4. **Annual Refresh**: Design system evolution

### **Implementation Priority**
1. **High**: Detail pages (most frequently used)
2. **Medium**: Form pages (create/edit operations)
3. **Low**: Specialized forms (quality control)

---

**🎯 Mission**: Establish consistent, reusable design patterns for all Context7 ERP page types while maintaining glassmorphism aesthetic and ensuring optimal user experience.

**📞 QMS Compliance**: This reference follows Context7 Central Protocol v1.0 and maintains design consistency across the entire ERP system.

---

*Context7 ERP Page Type References - Ensuring Consistent and Beautiful User Experience Across All Page Types* 