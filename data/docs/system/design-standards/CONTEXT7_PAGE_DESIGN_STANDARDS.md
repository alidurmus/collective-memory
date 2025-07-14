# 🎨 Context7 ERP - Sayfa Tasarım Standartları

**Version**: v2.2.0-glassmorphism-enhanced  
**Date**: 11 Ocak 2025  
**Status**: ✅ **ACTIVE DESIGN STANDARDS**  
**QMS Reference**: REC-DESIGN-STANDARDS-250111-001

---

## 🎯 **Problem Analizi**

### **Tespit Edilen Sorunlar**
1. **Sol Menü Tasarım Bozulması**: Quality control detail sayfasında sol menü ile çakışma
2. **Tutarsız Layout**: Farklı detail sayfalarında farklı tasarım yaklaşımları
3. **CSS Çakışması**: Inline CSS'ler base template'i eziyor
4. **Responsive Sorunlar**: Mobile cihazlarda layout bozukluğu

### **Analiz Edilen Sayfalar**
- ❌ **Problem**: `/erp/quality/incoming/af5de92a-bfdf-4ab2-8c35-93acf694549b/`
- ✅ **Referans**: `/erp/suppliers/d0d01e81-2fcb-441f-ac8a-d1a8d90096d1/`

---

## 🏗️ **Context7 Layout Architecture**

### **Base Layout Structure**
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Context7 Core CSS -->
    <link href="bootstrap.min.css" rel="stylesheet">
    <link href="fontawesome-all.min.css" rel="stylesheet">
    <style>
        /* Context7 Glassmorphism Variables */
        :root {
            --sidebar-width: 300px;
            --sidebar-collapsed-width: 80px;
            --glass-bg: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.3);
            --backdrop-blur: 20px;
        }
        
        /* Sidebar Layout */
        .sidebar {
            position: fixed;
            width: var(--sidebar-width);
            height: 100vh;
            background: var(--glass-bg);
            backdrop-filter: blur(var(--backdrop-blur));
        }
        
        /* Main Content */
        .main-content {
            margin-left: var(--sidebar-width);
            min-height: 100vh;
            padding: 2rem;
        }
    </style>
</head>
<body>
    <!-- Sidebar -->
    <div class="sidebar">...</div>
    
    <!-- Main Content -->
    <div class="main-content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

---

## 📋 **Standardized Page Templates**

### **1. Detail Page Template Structure**
```html
{% extends "base.html" %}
{% load static %}

{% block title %}{{ page_title }}{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/context7_detail_page.css' %}">
{% endblock %}

{% block content %}
<div class="detail-page-content">
    <div class="container-fluid">
        <!-- Header Section -->
        <div class="page-header">
            <div class="row">
                <div class="col-md-8">
                    <h2 class="page-title">
                        <i class="fas fa-icon me-2"></i>
                        {{ object.name }}
                        <span class="status-badge">{{ object.status }}</span>
                    </h2>
                    <nav class="breadcrumb-nav">
                        <!-- Breadcrumb -->
                    </nav>
                </div>
                <div class="col-md-4 text-end">
                    <div class="action-buttons">
                        <!-- Action Buttons -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Content Grid -->
        <div class="row">
            <div class="col-lg-8">
                <!-- Main Content -->
                <div class="glass-card">
                    <div class="card-header">
                        <h5>{{ section_title }}</h5>
                    </div>
                    <div class="card-body">
                        <!-- Content -->
                    </div>
                </div>
            </div>
            <div class="col-lg-4">
                <!-- Sidebar Content -->
                <div class="glass-card">
                    <!-- Quick Actions -->
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### **2. List Page Template Structure**
```html
{% extends "base.html" %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/context7_universal_list_styles.css' %}">
{% endblock %}

{% block content %}
<div class="list-page-content">
    <!-- Hero Section -->
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">{{ page_title }}</h1>
            <p class="hero-subtitle">{{ page_description }}</p>
        </div>
        <div class="hero-stats">
            <!-- Statistics Cards -->
        </div>
    </div>

    <!-- Filters & Search -->
    <div class="filters-section">
        <!-- Filter Components -->
    </div>

    <!-- Data Table -->
    <div class="table-section">
        <!-- Responsive Table -->
    </div>
</div>
{% endblock %}
```

---

## 🎨 **CSS Architecture Standards**

### **File Organization**
```
static/css/
├── context7_core.css              # Core glassmorphism framework
├── context7_universal_list_styles.css  # Universal list design
├── context7_detail_page.css       # Detail page standards
├── context7_form_styles.css       # Form styling standards
└── modules/
    ├── quality_control.css         # Module-specific styles
    ├── suppliers.css              # Supplier module styles
    └── sales.css                  # Sales module styles
```

### **CSS Naming Convention**
```css
/* Component-based naming */
.context7-[component]-[element]-[modifier]

/* Examples */
.context7-card-header-primary
.context7-button-action-secondary
.context7-table-row-highlighted
.context7-badge-status-approved
```

### **CSS Variables Standard**
```css
:root {
    /* Layout */
    --sidebar-width: 300px;
    --sidebar-collapsed-width: 80px;
    --content-max-width: 1200px;
    --content-padding: 2rem;
    
    /* Glassmorphism */
    --glass-bg: rgba(255, 255, 255, 0.15);
    --glass-bg-strong: rgba(255, 255, 255, 0.25);
    --glass-border: rgba(255, 255, 255, 0.3);
    --glass-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    --backdrop-blur: 20px;
    
    /* Colors */
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --success-gradient: linear-gradient(135deg, #28a745 0%, #20c997 100%);
    --warning-gradient: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
    --danger-gradient: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%);
    
    /* Typography */
    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-bold: 700;
    --font-weight-black: 900;
    
    /* Animation */
    --animation-duration: 0.3s;
    --animation-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
    
    /* Border Radius */
    --border-radius: 20px;
    --border-radius-sm: 12px;
    --border-radius-lg: 28px;
}
```

---

## 🔧 **Component Standards**

### **1. Glass Cards**
```css
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--backdrop-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    box-shadow: var(--glass-shadow);
    margin-bottom: 2rem;
    transition: all var(--animation-duration) var(--animation-spring);
    overflow: hidden;
    position: relative;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 64px rgba(31, 38, 135, 0.5);
    border-color: rgba(255, 255, 255, 0.4);
}
```

### **2. Action Buttons**
```css
.action-btn {
    background: var(--primary-gradient);
    border: 2px solid transparent;
    color: white;
    padding: 1rem 2rem;
    border-radius: var(--border-radius-sm);
    font-weight: var(--font-weight-bold);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    transition: all var(--animation-duration) var(--animation-spring);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    min-width: 160px;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.action-btn:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    color: white;
    text-decoration: none;
}
```

### **3. Status Badges**
```css
.status-badge {
    padding: 0.6rem 1.2rem;
    border-radius: 25px;
    font-weight: var(--font-weight-bold);
    font-size: 0.9rem;
    text-transform: uppercase;
    border: 2px solid;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    letter-spacing: 0.5px;
    transition: all var(--animation-duration) ease;
}

.status-approved {
    background: var(--success-gradient);
    color: white;
    border-color: #28a745;
    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}
```

### **4. Data Tables**
```css
.context7-table {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid var(--glass-border);
    border-radius: var(--border-radius-sm);
    overflow: hidden;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    width: 100%;
    margin-bottom: 2rem;
}

.context7-table th {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    color: #212529;
    font-weight: var(--font-weight-bold);
    border: none;
    padding: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 0.9rem;
    position: relative;
}

.context7-table td {
    color: #212529;
    border: 1px solid rgba(0, 0, 0, 0.1);
    padding: 1.2rem;
    vertical-align: middle;
    background: rgba(255, 255, 255, 0.8);
    transition: background-color var(--animation-duration) ease;
}

.context7-table tr:hover td {
    background: rgba(255, 255, 255, 0.95);
}
```

---

## 📱 **Responsive Design Standards**

### **Breakpoints**
```css
/* Mobile First Approach */
@media (max-width: 480px) {
    .detail-page-content {
        padding: 0.5rem;
    }
    
    .glass-card {
        padding: 1rem;
        border-radius: var(--border-radius-sm);
    }
    
    .action-btn {
        width: 100%;
        margin-bottom: 0.5rem;
    }
}

@media (max-width: 768px) {
    .detail-page-content {
        padding: 1rem;
    }
    
    .glass-card {
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .action-btn {
        padding: 0.8rem 1.5rem;
        min-width: 140px;
        font-size: 0.85rem;
    }
}

@media (max-width: 1024px) {
    .sidebar.collapsed + .main-content {
        margin-left: var(--sidebar-collapsed-width);
    }
}
```

### **Sidebar Responsive Behavior**
```css
/* Auto-collapse on tablet */
@media (max-width: 1024px) {
    .sidebar {
        width: var(--sidebar-collapsed-width);
    }
    
    .main-content {
        margin-left: var(--sidebar-collapsed-width);
    }
}

/* Mobile overlay */
@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
        transition: transform var(--animation-duration) ease;
    }
    
    .sidebar.mobile-open {
        transform: translateX(0);
    }
    
    .main-content {
        margin-left: 0;
    }
}
```

---

## 🎯 **Implementation Checklist**

### **Page Development Checklist**
- [ ] **Layout Compatibility**: Sidebar width respected
- [ ] **CSS Organization**: External CSS file, no inline styles
- [ ] **Responsive Design**: Mobile-first approach
- [ ] **Glassmorphism**: Consistent glass effects
- [ ] **Typography**: Inter font family used
- [ ] **Color Scheme**: CSS variables utilized
- [ ] **Animation**: Spring animations applied
- [ ] **Accessibility**: WCAG 2.1 AA compliance
- [ ] **Performance**: Optimized CSS delivery
- [ ] **Browser Support**: Cross-browser compatibility

### **Quality Assurance Tests**
- [ ] **Desktop**: 1920x1080, 1366x768 resolutions
- [ ] **Tablet**: iPad, Android tablet orientations
- [ ] **Mobile**: iPhone, Android phone sizes
- [ ] **Browser**: Chrome, Firefox, Safari, Edge
- [ ] **Sidebar**: Collapsed/expanded states
- [ ] **Print**: Print-friendly styles
- [ ] **Dark Mode**: Theme compatibility
- [ ] **Performance**: <2s page load time

---

## 📊 **Metrics & Standards**

### **Performance Targets**
- **First Contentful Paint**: <1.5s
- **Largest Contentful Paint**: <2.5s
- **Cumulative Layout Shift**: <0.1
- **Time to Interactive**: <3s

### **Accessibility Standards**
- **WCAG 2.1 AA**: Full compliance
- **Color Contrast**: 4.5:1 minimum ratio
- **Keyboard Navigation**: Full support
- **Screen Reader**: Compatible markup
- **Focus Indicators**: Visible and clear

### **Browser Support**
- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+
- **Mobile Safari**: iOS 14+
- **Chrome Mobile**: Android 10+

---

## 🔄 **Maintenance & Updates**

### **Regular Reviews**
- **Monthly**: Design consistency check
- **Quarterly**: Performance optimization
- **Semi-annually**: Accessibility audit
- **Annually**: Design system update

### **Update Process**
1. **Design Review**: UX/UI evaluation
2. **Technical Review**: Performance analysis
3. **User Testing**: Usability validation
4. **Implementation**: Gradual rollout
5. **Monitoring**: Post-deployment tracking

---

**🎯 Mission**: Establish consistent, accessible, and performant design standards across all Context7 ERP pages while maintaining the glassmorphism aesthetic and ensuring sidebar layout compatibility.

**📞 Support**: This standard follows Context7 Central Protocol v1.0 and QMS compliance requirements.

---

*Context7 ERP Design Standards - Ensuring Beautiful, Functional, and Consistent User Experience* 