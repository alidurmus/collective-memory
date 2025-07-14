# 📐 Context7 ERP - Sayfa Tasarım Kuralları
**Versiyon:** v2.2.0-glassmorphism-enhanced + **Modern Detail Page Standards**  
**Son Güncelleme:** 13 Ocak 2025  
**Framework:** Context7 Glassmorphism Design System v2.2.0

---

## 🎨 **GENEL TASARIM PRENSİPLERİ**

### **1. Context7 Glassmorphism Framework v2.2.0**
**📁 Detaylı CSS kodları:** [Context7 CSS Framework](../examples/frontend/context7-css-framework.css)  
**📁 Detail Page Header CSS:** [Context7 Detail Page Header](../../static/css/context7_detail_page_header.css)

**Ana Renk Paleti:**
- Primary: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Secondary: `linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)`  
- Success: `linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%)`
- Warning: `linear-gradient(135deg, #f093fb 0%, #f5576c 100%)`
- Danger: `linear-gradient(135deg, #fc466b 0%, #3f5efb 100%)`
- Info: `linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)`

**Glassmorphism Efektleri:**
- `backdrop-filter: blur(25px)`
- `background: rgba(255, 255, 255, 0.08)`
- `border-radius: 20px`
- `box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37)`

### **2. Typography Hierarchy**
- **H1 (Page Title)**: font-weight: 800, gradient text, 2.5rem
- **H2 (Section Title)**: font-weight: 700, 2rem
- **H3 (Card Title)**: font-weight: 600, 1.5rem
- **Body Text**: font-weight: 400, 1rem, line-height: 1.6
- **Small Text**: font-weight: 400, 0.875rem

### **3. Enhanced Animation System**
- **Spring Animations**: `cubic-bezier(0.175, 0.885, 0.32, 1.275)`
- **Transition Duration**: 0.3s for smooth interactions
- **Hover Effects**: `translateY(-2px) scale(1.02)` pattern
- **GPU Acceleration**: `transform` properties for performance

### **4. Accessibility Standards**
- **WCAG 2.1 AA Compliance**: All components meet accessibility standards
- **High Contrast Mode**: Support for users with visual impairments
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and semantic HTML

---

## 📋 **SAYFA TİPLERİ VE KURALLARI**

## **1. DETAY SAYFALARI (Detail Pages) - MODERNIZED** ⭐

### **🆕 Modern Detail Page Header Component**
**Component Template:** `templates/components/detail_page_header.html`

```html
<!-- Modern Glassmorphism Detail Header -->
<div class="ctx7-detail-header">
    <div class="ctx7-header-content">
        <div class="row align-items-center">
            <div class="col-lg-8">
                <h1 class="ctx7-header-title">
                    <i class="fas fa-[icon] ctx7-header-icon"></i>
                    {{ title }}
                    <span class="ctx7-status-badge {{ status_class }}">
                        <i class="fas fa-[status-icon] me-1"></i>{{ status_text }}
                    </span>
                </h1>
                
                <nav aria-label="breadcrumb" class="ctx7-breadcrumb">
                    <ol class="breadcrumb">
                        <!-- Dynamic breadcrumb items -->
                    </ol>
                </nav>
            </div>
            
            <div class="col-lg-4">
                <div class="ctx7-action-buttons text-end">
                    <!-- Dynamic action buttons -->
                </div>
            </div>
        </div>
    </div>
</div>
```

### **Yapısal Gereksinimler:**

#### **1. Header Section (Modernized)**
```html
<!-- Include the modern header CSS -->
{% block extra_css %}
<link href="{% static 'css/context7_detail_page_header.css' %}" rel="stylesheet">
{% endblock %}

<!-- Use the modern header component -->
{% include 'components/detail_page_header.html' with title=object.name icon="user" status_class="active" status_text="Aktif" %}
```

#### **2. Main Content Layout**
```html
<div class="container-fluid py-4">
    <!-- Modern Header Component -->
    {% include 'components/detail_page_header.html' %}
    
    <!-- Main Content -->
    <div class="row">
        <div class="col-lg-8">
            <!-- Primary Information Card -->
            <div class="ctx7-glass-card primary-info">
                <div class="card-header">
                    <h3><i class="fas fa-info-circle me-2"></i>Temel Bilgiler</h3>
                </div>
                <div class="card-body">
                    <div class="info-grid">
                        <!-- Key-value pairs -->
                    </div>
                </div>
            </div>
            
            <!-- Related Data Section -->
            <div class="ctx7-glass-card related-data">
                <div class="card-header">
                    <h3><i class="fas fa-link me-2"></i>İlişkili Kayıtlar</h3>
                </div>
                <div class="card-body">
                    <!-- Related items list/table -->
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <!-- Sidebar Information -->
            <div class="ctx7-glass-card sidebar-stats">
                <div class="card-header">
                    <h4><i class="fas fa-chart-bar me-2"></i>Özet Bilgiler</h4>
                </div>
                <div class="card-body">
                    <!-- Summary stats -->
                </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="ctx7-glass-card quick-actions">
                <div class="card-header">
                    <h4><i class="fas fa-bolt me-2"></i>Hızlı İşlemler</h4>
                </div>
                <div class="card-body">
                    <!-- Action buttons -->
                </div>
            </div>
        </div>
    </div>
</div>
```

### **🎨 Modern Design Features:**

#### **1. Advanced Glassmorphism Effects**
- **Primary Glass Cards**: Enhanced transparency and blur effects
- **Secondary Glass Cards**: Lighter transparency for hierarchy
- **Tertiary Glass Cards**: Subtle effects for supporting content

#### **2. Status Badge System**
```css
.ctx7-status-badge.active { background: var(--ctx7-success-gradient); }
.ctx7-status-badge.inactive { background: var(--ctx7-danger-gradient); }
.ctx7-status-badge.pending { background: var(--ctx7-warning-gradient); }
.ctx7-status-badge.completed { background: var(--ctx7-info-gradient); }
.ctx7-status-badge.cancelled { background: var(--ctx7-secondary-gradient); }
```

#### **3. Enhanced Animations**
- **Header Slide-in**: 0.8s spring animation on page load
- **Icon Pulse**: 2s infinite pulse for active status
- **Badge Animations**: Staggered appearance with spring easing
- **Button Hover**: Scale and elevation effects

#### **4. Responsive Design**
- **Desktop (>1200px)**: Full layout with sidebar
- **Tablet (768px-1199px)**: Stacked layout with responsive header
- **Mobile (<768px)**: Single column with collapsible elements

### **🔧 Implementation Standards:**

#### **1. CSS Classes Hierarchy**
```css
.ctx7-detail-header          /* Main header container */
├── .ctx7-header-content     /* Content wrapper */
├── .ctx7-header-title       /* Main title styling */
├── .ctx7-header-icon        /* Icon styling */
├── .ctx7-status-badge       /* Status badge */
├── .ctx7-breadcrumb         /* Breadcrumb navigation */
└── .ctx7-action-buttons     /* Action buttons container */

.ctx7-glass-card             /* Glass effect cards */
├── .primary-info            /* Main information card */
├── .related-data            /* Related data card */
├── .sidebar-stats           /* Sidebar statistics */
└── .quick-actions           /* Quick actions card */
```

#### **2. Performance Optimization**
- **GPU Acceleration**: All animations use `transform` properties
- **Lazy Loading**: Non-critical content loaded after main render
- **Optimized Images**: WebP format with fallbacks
- **Critical CSS**: Above-the-fold styles inlined

#### **3. Accessibility Features**
- **ARIA Labels**: Comprehensive labeling for screen readers
- **Keyboard Navigation**: Full keyboard accessibility
- **High Contrast**: Support for high contrast mode
- **Reduced Motion**: Respect user motion preferences

---

## **2. LİSTE SAYFALARI (List Pages)**

### **Yapısal Gereksinimler:**
```html
<!-- Header Section -->
<div class="page-header">
    <div class="row align-items-center">
        <div class="col-md-8">
            <h1 class="page-title">[Sayfa Başlığı]</h1>
            <nav aria-label="breadcrumb" class="breadcrumb-modern">
                <!-- Breadcrumb navigation -->
            </nav>
        </div>
        <div class="col-md-4 text-end">
            <a href="[kategori-url]" class="btn-secondary me-2">
                <i class="fas fa-layer-group"></i> Kategoriler
            </a>
            <a href="[create-url]" class="btn-primary">
                <i class="fas fa-plus"></i> Yeni [Item]
            </a>
        </div>
    </div>
</div>

<!-- Statistics Cards -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon primary">
            <i class="fas fa-[icon]"></i>
        </div>
        <div class="stat-content">
            <div class="stat-title">Toplam [Item]</div>
            <div class="stat-value">{{ total_count }}</div>
        </div>
    </div>
    <!-- Diğer istatistik kartları -->
</div>

<!-- Filter Section -->
<div class="filter-card">
    <form method="get" class="row g-3">
        <!-- Filter dropdowns ve search -->
    </form>
</div>

<!-- Data Table -->
<div class="data-table-card">
    <div class="table-responsive">
        <table class="table modern-table">
            <!-- Table content -->
        </table>
    </div>
    <!-- Pagination -->
</div>
```

### **Tasarım Kuralları:**
- **Header**: Gradient background, glassmorphism effects
- **Stats Cards**: 4'lü grid layout, icon + title + value
- **Filter Section**: Responsive form layout, glassmorphism card
- **Table**: Modern styling, hover effects, action buttons
- **Pagination**: Bootstrap pagination with custom styling

### **CSS Sınıfları:**
```css
.page-header { background: var(--primary-gradient); }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }
.stat-card { @extend .glass-card; @extend .smooth-transition; }
.filter-card { @extend .glass-card; margin: 2rem 0; }
.data-table-card { @extend .glass-card; }
.modern-table { background: transparent; }
```

---

## **3. OLUŞTURMA SAYFALARI (Create Pages)**

### **Yapısal Gereksinimler:**
```html
<!-- Header Section -->
<div class="form-header">
    <h1 class="form-title">Yeni [Item] Oluştur</h1>
    <nav aria-label="breadcrumb" class="breadcrumb-modern">
        <!-- Breadcrumb -->
    </nav>
</div>

<!-- Form Section -->
<div class="row justify-content-center">
    <div class="col-md-8">
        <div class="form-card">
            <form method="post">
                {% csrf_token %}
                <!-- Form fields -->
            </form>
        </div>
    </div>
</div>
```

---

## **🚀 MIGRATION GUIDE - EXISTING PAGES TO MODERN STANDARDS**

### **Step 1: Add Modern CSS**
```html
{% block extra_css %}
<link href="{% static 'css/context7_detail_page_header.css' %}" rel="stylesheet">
{% endblock %}
```

### **Step 2: Replace Header Section**
```html
<!-- OLD HEADER -->
<div class="row mb-4">
    <div class="col-md-8">
        <h2>{{ object.name }}</h2>
    </div>
    <div class="col-md-4 text-end">
        <!-- Action buttons -->
    </div>
</div>

<!-- NEW MODERN HEADER -->
{% include 'components/detail_page_header.html' with title=object.name icon="user" status_class="active" status_text="Aktif" %}
```

### **Step 3: Update Content Cards**
```html
<!-- OLD CARD -->
<div class="card">
    <div class="card-body">
        <!-- Content -->
    </div>
</div>

<!-- NEW GLASS CARD -->
<div class="ctx7-glass-card">
    <div class="card-header">
        <h3><i class="fas fa-info-circle me-2"></i>Başlık</h3>
    </div>
    <div class="card-body">
        <!-- Content -->
    </div>
</div>
```

---

## **📊 PERFORMANCE & ACCESSIBILITY STANDARDS**

### **Performance Targets:**
- **Page Load Time**: <2 seconds
- **First Contentful Paint**: <1.2 seconds
- **Largest Contentful Paint**: <2.5 seconds
- **Cumulative Layout Shift**: <0.1

### **Accessibility Requirements:**
- **WCAG 2.1 AA Compliance**: All pages must meet AA standards
- **Color Contrast**: Minimum 4.5:1 ratio for normal text
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper semantic HTML and ARIA labels

### **Browser Compatibility:**
- **Chrome**: 90+ (100% support)
- **Firefox**: 88+ (100% support)
- **Safari**: 14+ (100% support)
- **Edge**: 90+ (100% support)

---

**🎯 Mission:** Provide consistent, modern, and accessible design patterns across all Context7 ERP pages with the new glassmorphism framework standards.

**🏆 Achievement:** Successfully established modern detail page header standards with comprehensive component system and migration guide.

---

*Context7 ERP Design Standards - Modern, Accessible, and Performance-Optimized* ⭐ 