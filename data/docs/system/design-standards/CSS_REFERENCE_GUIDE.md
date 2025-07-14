# 🎨 Context7 ERP - CSS Reference Guide

**Version**: v2.2.0-glassmorphism-enhanced  
**Date**: 11 Ocak 2025  
**Status**: ✅ **ACTIVE CSS REFERENCE**  
**QMS Reference**: REC-CSS-REFERENCE-250111-001

---

## 📋 **CSS Dosyaları Organizasyonu**

### **Ana CSS Framework Dosyaları**
```
static/css/
├── context7_page_type_framework.css    # 🎯 ANA FRAMEWORK (500+ lines)
├── context7_universal_list_styles.css  # 📋 Liste sayfaları standartları
├── quality_control_list_styles.css     # 🔍 Kalite kontrol özel stilleri
├── quality_detail_fixed.css            # 🔧 Kalite detay sayfası düzeltmeleri
└── erp_common_list_styles.css          # 📊 ERP ortak liste stilleri
```

---

## 🎯 **1. Context7 Page Type Framework CSS**
**📄 Dosya**: `static/css/context7_page_type_framework.css`

### **CSS Custom Properties (Değişkenler)**
**📄 Dosya Linki**: [`docs/examples/css/context7-variables.css`](../examples/css/context7-variables.css)

```css
/* CSS Custom Properties - Kod örneği için yukarıdaki dosya linkini kullanın */
:root {
    /* Layout Variables */
    --content-padding: 2rem;
    --card-border-radius: 16px;
    --section-spacing: 2rem;
    /* ... diğer değişkenler için dosyaya bakın */
}
```

### **Ana Component Sınıfları**

#### **Detail Pages (Detay Sayfaları)**
**📄 Dosya Linki**: [`docs/examples/css/detail-pages.css`](../examples/css/detail-pages.css)

```css
/* Detail Pages CSS - Kod örneği için yukarıdaki dosya linkini kullanın */
.detail-page-content {
    padding: var(--content-padding);
    min-height: calc(100vh - 200px);
}
/* ... diğer detail page sınıfları için dosyaya bakın */
```

#### **Form Pages (Form Sayfaları)**
**📄 Dosya Linki**: [`docs/examples/css/form-pages.css`](../examples/css/form-pages.css)

```css
/* Form Pages CSS - Kod örneği için yukarıdaki dosya linkini kullanın */
.form-page-content {
    padding: var(--content-padding);
}
/* ... diğer form page sınıfları için dosyaya bakın */
```

#### **Quality Forms (Kalite Kontrol Formları)**
```css
.glass-container {
    background: var(--glass-bg-medium);
    backdrop-filter: blur(var(--backdrop-blur-strong));
    border: 1px solid var(--glass-border-light);
    border-radius: 20px;
    box-shadow: var(--glass-shadow);
    padding: 2rem;
    margin-bottom: var(--section-spacing);
}

.quality-header {
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: var(--font-weight-black);
    text-align: center;
    margin-bottom: 2rem;
    font-size: 2rem;
}
```

### **Status Badge System**
**📄 Dosya Linki**: [`docs/examples/css/status-badges.css`](../examples/css/status-badges.css)

```css
/* Status Badge System - Kod örneği için yukarıdaki dosya linkini kullanın */
.status-badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.9em;
    /* ... diğer status badge sınıfları için dosyaya bakın */
}
```

### **Action Button System**
**📄 Dosya Linki**: [`docs/examples/css/action-buttons.css`](../examples/css/action-buttons.css)

```css
/* Action Button System - Kod örneği için yukarıdaki dosya linkini kullanın */
.action-button {
    background: var(--primary-gradient);
    border: none;
    border-radius: 12px;
    /* ... diğer action button sınıfları için dosyaya bakın */
}
```

---

## 📋 **2. Universal List Styles CSS**
**📄 Dosya**: `static/css/context7_universal_list_styles.css`

### **Liste Sayfaları Ana Yapısı**
```css
.list-page-header {
    background: var(--glass-bg-light);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--card-border-radius);
    padding: 2rem;
    margin-bottom: 2rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: var(--glass-bg-light);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: var(--transition-spring);
}

.stat-card:hover {
    transform: var(--hover-transform);
    box-shadow: 0 8px 25px rgba(31, 38, 135, 0.5);
}
```

### **Arama ve Filtreleme**
```css
.search-filter-section {
    background: var(--glass-bg-light);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--card-border-radius);
    padding: 1.5rem;
    margin-bottom: 2rem;
}

.search-input {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    width: 100%;
    transition: var(--transition-base);
}

.search-input:focus {
    background: white;
    border-color: rgba(102, 126, 234, 0.5);
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    outline: none;
}
```

### **Tablo Stilleri**
**📄 Dosya Linki**: [`docs/examples/css/data-tables.css`](../examples/css/data-tables.css)

```css
/* Data Tables CSS - Kod örneği için yukarıdaki dosya linkini kullanın */
.data-table {
    background: var(--glass-bg-light);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
    /* ... diğer tablo sınıfları için dosyaya bakın */
}
```

---

## 🔍 **3. Quality Control Styles CSS**
**📄 Dosya**: `static/css/quality_control_list_styles.css`

### **Kalite Kontrol Özel Stilleri**
```css
.quality-hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: var(--card-border-radius);
    margin-bottom: 2rem;
    text-align: center;
}

.quality-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: var(--glass-bg-light);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: var(--transition-spring);
}

.metric-value {
    font-size: 2rem;
    font-weight: var(--font-weight-black);
    color: #667eea;
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 0.875rem;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
```

### **Kalite Durumu Göstergeleri**
```css
.quality-status-excellent {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.quality-status-good {
    background-color: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
}

.quality-status-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.quality-status-critical {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}
```

---

## 🔧 **4. Quality Detail Fixed CSS**
**📄 Dosya**: `static/css/quality_detail_fixed.css`

### **Sidebar Uyumlu Tasarım**
```css
.quality-detail-content {
    width: 100%;
    max-width: 100%;
    margin: 0;
    padding: 2rem;
    box-sizing: border-box;
}

.quality-detail-content * {
    box-sizing: border-box;
}

.glass-container {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    padding: 2rem;
    margin-bottom: 2rem;
}
```

---

## 📱 **Responsive Design Patterns**

### **Breakpoint Sistemi**
```css
/* Desktop (1200px+) */
@media (min-width: 1200px) {
    .detail-layout { grid-template-columns: 2fr 1fr; }
    .form-layout { grid-template-columns: 2fr 1fr; }
    .stats-grid { grid-template-columns: repeat(4, 1fr); }
}

/* Tablet (768px - 1199px) */
@media (min-width: 768px) and (max-width: 1199px) {
    .detail-layout { grid-template-columns: 1fr; }
    .form-layout { grid-template-columns: 1fr; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); }
    .section-card { padding: 1rem; }
}

/* Mobile (< 768px) */
@media (max-width: 767px) {
    .detail-page-content { padding: 1rem; }
    .stats-grid { grid-template-columns: 1fr; }
    .action-button { 
        width: 100%; 
        justify-content: center; 
        margin-bottom: 0.5rem; 
    }
}
```

---

## 🎨 **Utility Classes**

### **Spacing Utilities**
```css
.section-spacing { margin-bottom: var(--section-spacing); }
.content-padding { padding: var(--content-padding); }
.no-margin { margin: 0; }
.no-padding { padding: 0; }
```

### **Glass Effect Utilities**
```css
.glass-light {
    background: var(--glass-bg-light);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
}

.glass-medium {
    background: var(--glass-bg-medium);
    backdrop-filter: blur(var(--backdrop-blur-strong));
    border: 1px solid var(--glass-border-light);
}

.glass-dark {
    background: var(--glass-bg-dark);
    backdrop-filter: blur(var(--backdrop-blur-strong));
    border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### **Animation Utilities**
```css
.hover-lift {
    transition: var(--transition-spring);
}

.hover-lift:hover {
    transform: var(--hover-transform);
}

.fade-in {
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
```

### **Text Utilities**
```css
.gradient-text {
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: var(--font-weight-black);
}

.text-weight-bold { font-weight: var(--font-weight-bold); }
.text-weight-black { font-weight: var(--font-weight-black); }
.text-center { text-align: center; }
.text-uppercase { text-transform: uppercase; }
```

---

## ♿ **Accessibility Features**

### **Focus Indicators**
```css
.action-button:focus,
.form-control:focus,
.search-input:focus {
    outline: 2px solid #667eea;
    outline-offset: 2px;
}
```

### **High Contrast Support**
```css
@media (prefers-contrast: high) {
    .detail-section,
    .glassmorphism-card {
        border: 2px solid #000;
    }
    
    .status-badge {
        border: 1px solid #000;
    }
}
```

### **Reduced Motion Support**
```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
    
    .hover-lift:hover,
    .action-button:hover {
        transform: none;
    }
}
```

---

## 🖨️ **Print Styles**

### **Print Optimizations**
```css
@media print {
    .detail-page-content,
    .form-page-content {
        padding: 0;
    }
    
    .detail-section,
    .glassmorphism-card {
        background: white !important;
        border: 1px solid #000 !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
    }
    
    .action-button {
        display: none;
    }
}
```

---

## 🔧 **CSS Implementation Guidelines**

### **1. CSS Dosya Dahil Etme Sırası**
```html
<!-- Base Template -->
<link rel="stylesheet" href="{% static 'css/context7_page_type_framework.css' %}">
<link rel="stylesheet" href="{% static 'css/context7_universal_list_styles.css' %}">

<!-- Sayfa Özel CSS -->
<link rel="stylesheet" href="{% static 'css/quality_control_list_styles.css' %}">
<link rel="stylesheet" href="{% static 'css/quality_detail_fixed.css' %}">
```

### **2. CSS Custom Properties Kullanımı**
```css
/* Özel değişken tanımlama */
.custom-component {
    background: var(--glass-bg-light);
    border-radius: var(--card-border-radius);
    padding: var(--content-padding);
    transition: var(--transition-spring);
}

/* Değişken override etme */
:root {
    --custom-primary-color: #ff6b6b;
    --custom-border-radius: 8px;
}
```

### **3. Component Class Naming Convention**
```css
/* Block Element Modifier (BEM) benzeri yaklaşım */
.component-name { }          /* Ana component */
.component-name__element { } /* Component elementi */
.component-name--modifier { }/* Component varyasyonu */

/* Context7 özel prefix */
.c7-component { }           /* Context7 component */
.c7-component--large { }    /* Büyük varyasyon */
.c7-component__header { }   /* Component header */
```

---

## 📊 **Performance Optimization**

### **CSS Optimization Tips**
1. **CSS Variables**: Consistent theming ve easy maintenance
2. **GPU Acceleration**: `transform` ve `opacity` kullanımı
3. **Efficient Selectors**: Specific selectors yerine class-based approach
4. **Minification**: Production'da CSS minification
5. **Critical CSS**: Above-the-fold content için critical CSS

### **Browser Support**
- **Chrome 90+**: Full glassmorphism support
- **Firefox 88+**: Fallback backgrounds for backdrop-filter
- **Safari 14+**: Webkit prefix support
- **Edge 90+**: Full feature support

---

**🎯 Mission**: Bu CSS referans guide'ı Context7 ERP sistemindeki tüm CSS dosyalarının kullanımını, yapısını ve best practices'lerini kapsamlı şekilde açıklar.

**📞 QMS Compliance**: Bu referans Context7 Central Protocol v1.0 standartlarına uygun olarak hazırlanmıştır.

---

*Context7 CSS Reference Guide - Complete Styling Documentation for Enterprise ERP System* 