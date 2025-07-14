# 🧭 Context7 ERP - Menü Yapısı, Buton ve Yerleşim Kuralları
**Versiyon:** v2.2.0-glassmorphism-enhanced  
**Son Güncelleme:** 11 Ocak 2025  
**Framework:** Context7 Glassmorphism Design System v1.0

---

## 🧭 **MENÜ YAPISI VE NAVİGASYON KURALLARI**

### **1. Ana Menü Yapısı**
```html
<!-- Main Navigation -->
<nav class="main-navigation">
    <div class="nav-header">
        <div class="nav-brand">
            <img src="/static/images/context7-logo.png" alt="Context7 ERP" class="nav-logo">
            <span class="nav-title">Context7 ERP</span>
        </div>
        <button class="nav-toggle" id="navToggle">
            <i class="fas fa-bars"></i>
        </button>
    </div>
    
    <div class="nav-body">
        <!-- Dashboard -->
        <div class="nav-section">
            <a href="{% url 'dashboard:dashboard' %}" class="nav-item {% if request.resolver_match.namespace == 'dashboard' %}active{% endif %}">
                <i class="fas fa-tachometer-alt nav-icon"></i>
                <span class="nav-text">Dashboard</span>
            </a>
        </div>
        
        <!-- ERP Modules -->
        <div class="nav-section">
            <div class="nav-section-header">
                <i class="fas fa-industry"></i>
                <span>ERP Modülleri</span>
            </div>
            
            <div class="nav-group">
                <a href="{% url 'erp:sales_dashboard' %}" class="nav-item">
                    <i class="fas fa-chart-line nav-icon"></i>
                    <span class="nav-text">Satış Yönetimi</span>
                </a>
                <a href="{% url 'erp:materials' %}" class="nav-item">
                    <i class="fas fa-boxes nav-icon"></i>
                    <span class="nav-text">Malzeme Yönetimi</span>
                </a>
                <a href="{% url 'erp:products' %}" class="nav-item">
                    <i class="fas fa-cube nav-icon"></i>
                    <span class="nav-text">Ürün Yönetimi</span>
                </a>
                <a href="{% url 'erp:purchasing_dashboard' %}" class="nav-item">
                    <i class="fas fa-shopping-cart nav-icon"></i>
                    <span class="nav-text">Satın Alma</span>
                </a>
                <a href="{% url 'erp:production_dashboard' %}" class="nav-item">
                    <i class="fas fa-cogs nav-icon"></i>
                    <span class="nav-text">Üretim</span>
                </a>
                <a href="{% url 'erp:inventory_dashboard' %}" class="nav-item">
                    <i class="fas fa-warehouse nav-icon"></i>
                    <span class="nav-text">Envanter</span>
                </a>
                <a href="{% url 'erp:finance_dashboard' %}" class="nav-item">
                    <i class="fas fa-calculator nav-icon"></i>
                    <span class="nav-text">Finans</span>
                </a>
                <a href="{% url 'erp:hr_dashboard' %}" class="nav-item">
                    <i class="fas fa-users nav-icon"></i>
                    <span class="nav-text">İnsan Kaynakları</span>
                </a>
                <a href="{% url 'erp:quality_dashboard' %}" class="nav-item">
                    <i class="fas fa-medal nav-icon"></i>
                    <span class="nav-text">Kalite Kontrol</span>
                </a>
            </div>
        </div>
        
        <!-- System Settings -->
        <div class="nav-section">
            <div class="nav-section-header">
                <i class="fas fa-cog"></i>
                <span>Sistem</span>
            </div>
            
            <div class="nav-group">
                <a href="{% url 'settings_app:settings' %}" class="nav-item">
                    <i class="fas fa-sliders-h nav-icon"></i>
                    <span class="nav-text">Ayarlar</span>
                </a>
                <a href="{% url 'users:profile' %}" class="nav-item">
                    <i class="fas fa-user nav-icon"></i>
                    <span class="nav-text">Profil</span>
                </a>
            </div>
        </div>
    </div>
</nav>
```

### **2. Breadcrumb Navigation**
```html
<!-- Breadcrumb yapısı -->
<nav aria-label="breadcrumb" class="breadcrumb-modern">
    <ol class="breadcrumb">
        <li class="breadcrumb-item">
            <a href="{% url 'dashboard:dashboard' %}">
                <i class="fas fa-home"></i> Ana Sayfa
            </a>
        </li>
        <li class="breadcrumb-item">
            <a href="{% url 'erp:materials' %}">Malzemeler</a>
        </li>
        <li class="breadcrumb-item active" aria-current="page">
            Kategori Yönetimi
        </li>
    </ol>
</nav>
```

### **3. Menü CSS Kuralları**
```css
/* Ana Navigation */
.main-navigation {
    width: 280px;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 0;
    background: linear-gradient(180deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    backdrop-filter: blur(25px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 1000;
    overflow-y: auto;
    padding: 20px 0;
}

.nav-header {
    padding: 0 20px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 20px;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.nav-logo {
    width: 32px;
    height: 32px;
}

.nav-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: white;
}

.nav-section {
    margin-bottom: 24px;
}

.nav-section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 20px;
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.nav-group {
    padding-left: 12px;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: all 0.3s ease;
    border-radius: 8px;
    margin: 4px 12px;
    gap: 12px;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #fff;
    transform: translateX(4px);
}

.nav-item.active {
    background: var(--primary-gradient);
    color: #fff;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.nav-icon {
    width: 18px;
    text-align: center;
}

/* Breadcrumb Styling */
.breadcrumb-modern {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 8px;
    padding: 8px 16px;
    margin-top: 12px;
}

.breadcrumb {
    margin: 0;
    background: none;
}

.breadcrumb-item a {
    color: rgba(255, 255, 255, 0.7);
    text-decoration: none;
    transition: color 0.3s ease;
}

.breadcrumb-item a:hover {
    color: white;
}

.breadcrumb-item.active {
    color: rgba(255, 255, 255, 0.9);
}

/* Responsive Navigation */
@media (max-width: 768px) {
    .main-navigation {
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .main-navigation.open {
        transform: translateX(0);
    }
    
    .nav-toggle {
        display: block;
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        padding: 8px;
    }
}

@media (min-width: 769px) {
    .nav-toggle {
        display: none;
    }
}
```

---

## 🔘 **BUTON TASARIM VE YERLEŞİM KURALLARI**

### **1. Buton Tipleri ve Kullanım Alanları**

#### **Primary Buttons (Ana İşlemler)**
```html
<!-- Kaydet, Oluştur, Onayla gibi ana işlemler -->
<button type="submit" class="btn btn-primary">
    <i class="fas fa-save"></i> Kaydet
</button>

<a href="{% url 'erp:material_create' %}" class="btn btn-primary">
    <i class="fas fa-plus"></i> Yeni Malzeme
</a>

<button type="button" class="btn btn-primary" onclick="confirmAction()">
    <i class="fas fa-check"></i> Onayla
</button>
```

#### **Secondary Buttons (İkincil İşlemler)**
```html
<!-- İptal, Geri, Kategoriler gibi ikincil işlemler -->
<a href="{% url 'erp:materials' %}" class="btn btn-secondary">
    <i class="fas fa-arrow-left"></i> Geri
</a>

<a href="{% url 'erp:material_categories' %}" class="btn btn-secondary">
    <i class="fas fa-layer-group"></i> Kategoriler
</a>

<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
    <i class="fas fa-times"></i> İptal
</button>
```

#### **Action Buttons (Eylem Butonları)**
```html
<!-- Düzenle, Sil, Görüntüle gibi eylemler -->
<a href="{% url 'erp:material_edit' material.pk %}" class="btn btn-warning btn-sm">
    <i class="fas fa-edit"></i> Düzenle
</a>

<a href="{% url 'erp:material_delete' material.pk %}" class="btn btn-danger btn-sm" 
   onclick="return confirm('Bu malzemeyi silmek istediğinizden emin misiniz?')">
    <i class="fas fa-trash"></i> Sil
</a>

<a href="{% url 'erp:material_detail' material.pk %}" class="btn btn-info btn-sm">
    <i class="fas fa-eye"></i> Detay
</a>

<button type="button" class="btn btn-success btn-sm" onclick="approveItem({{ material.pk }})">
    <i class="fas fa-check"></i> Onayla
</button>
```

#### **Utility Buttons (Yardımcı Butonlar)**
```html
<!-- Yazdır, İndir, Paylaş gibi yardımcı işlemler -->
<button type="button" class="btn btn-outline-primary" onclick="window.print()">
    <i class="fas fa-print"></i> Yazdır
</button>

<a href="{% url 'erp:material_export' %}" class="btn btn-outline-success">
    <i class="fas fa-download"></i> Excel İndir
</a>

<button type="button" class="btn btn-outline-info" onclick="shareItem()">
    <i class="fas fa-share"></i> Paylaş
</button>
```

### **2. Buton Yerleşim Kuralları**

#### **Sayfa Header'ında Buton Yerleşimi**
```html
<div class="page-header">
    <div class="row align-items-center">
        <div class="col-md-8">
            <h1 class="page-title">Malzemeler</h1>
            <nav aria-label="breadcrumb" class="breadcrumb-modern">
                <!-- Breadcrumb -->
            </nav>
        </div>
        <div class="col-md-4 text-end">
            <!-- Yardımcı butonlar -->
            <button class="btn btn-outline-primary me-2" onclick="window.print()">
                <i class="fas fa-print"></i>
            </button>
            
            <!-- İkincil butonlar -->
            <a href="{% url 'erp:material_categories' %}" class="btn btn-secondary me-2">
                <i class="fas fa-layer-group"></i> Kategoriler
            </a>
            
            <!-- Ana buton (en sağda) -->
            <a href="{% url 'erp:material_create' %}" class="btn btn-primary">
                <i class="fas fa-plus"></i> Yeni Malzeme
            </a>
        </div>
    </div>
</div>
```

#### **Form Sayfalarında Buton Yerleşimi**
```html
<div class="form-actions">
    <!-- Ana işlem butonu (en solda) -->
    <button type="submit" class="btn btn-primary me-3">
        <i class="fas fa-save"></i> Kaydet
    </button>
    
    <!-- İkincil işlem butonları -->
    <button type="button" class="btn btn-outline-primary me-2" onclick="saveDraft()">
        <i class="fas fa-save"></i> Taslak Kaydet
    </button>
    
    <!-- Navigasyon butonları (sağda) -->
    <div class="ms-auto">
        <a href="{% url 'erp:material_detail' object.pk %}" class="btn btn-secondary me-2">
            <i class="fas fa-eye"></i> Detayları Gör
        </a>
        
        <a href="{% url 'erp:materials' %}" class="btn btn-outline-secondary">
            <i class="fas fa-arrow-left"></i> Listeye Dön
        </a>
    </div>
</div>
```

#### **Tablo İçinde Action Butonları**
```html
<td class="text-end">
    <div class="btn-group" role="group" aria-label="İşlemler">
        <!-- Görüntüleme (mavi) -->
        <a href="{% url 'erp:material_detail' material.pk %}" 
           class="btn btn-info btn-sm" title="Detayları Görüntüle">
            <i class="fas fa-eye"></i>
        </a>
        
        <!-- Düzenleme (turuncu) -->
        <a href="{% url 'erp:material_edit' material.pk %}" 
           class="btn btn-warning btn-sm" title="Düzenle">
            <i class="fas fa-edit"></i>
        </a>
        
        <!-- Silme (kırmızı - en sağda) -->
        <a href="{% url 'erp:material_delete' material.pk %}" 
           class="btn btn-danger btn-sm" title="Sil"
           onclick="return confirm('{{ material.name }} malzemesini silmek istediğinizden emin misiniz?')">
            <i class="fas fa-trash"></i>
        </a>
    </div>
</td>
```

#### **Card İçinde Action Butonları**
```html
<div class="card-actions">
    <div class="row">
        <div class="col-md-8">
            <!-- Ana bilgiler -->
            <h5 class="card-title">{{ material.name }}</h5>
            <p class="card-text">{{ material.description|truncatewords:10 }}</p>
        </div>
        <div class="col-md-4 text-end">
            <!-- Action butonları -->
            <div class="btn-group-vertical" role="group">
                <a href="{% url 'erp:material_detail' material.pk %}" class="btn btn-info btn-sm">
                    <i class="fas fa-eye"></i> Detay
                </a>
                <a href="{% url 'erp:material_edit' material.pk %}" class="btn btn-warning btn-sm">
                    <i class="fas fa-edit"></i> Düzenle
                </a>
            </div>
        </div>
    </div>
</div>
```

### **3. Buton CSS Stilleri**
```css
/* Temel Buton Stilleri */
.btn {
    padding: 12px 24px;
    border-radius: 12px;
    font-weight: 600;
    text-transform: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: none;
    cursor: pointer;
    text-decoration: none;
    font-size: 0.875rem;
    line-height: 1.5;
}

/* Buton Boyutları */
.btn-sm {
    padding: 8px 16px;
    font-size: 0.8125rem;
    border-radius: 8px;
}

.btn-lg {
    padding: 16px 32px;
    font-size: 1rem;
    border-radius: 16px;
}

/* Buton Renkleri - Primary */
.btn-primary {
    background: var(--primary-gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    color: white;
}

/* Buton Renkleri - Secondary */
.btn-secondary {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
}

.btn-secondary:hover {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    transform: translateY(-1px);
}

/* Buton Renkleri - Success */
.btn-success {
    background: var(--success-gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
}

.btn-success:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(78, 205, 196, 0.6);
    color: white;
}

/* Buton Renkleri - Warning */
.btn-warning {
    background: var(--warning-gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
}

.btn-warning:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(240, 147, 251, 0.6);
    color: white;
}

/* Buton Renkleri - Danger */
.btn-danger {
    background: var(--danger-gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(252, 70, 107, 0.4);
}

.btn-danger:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(252, 70, 107, 0.6);
    color: white;
}

/* Buton Renkleri - Info */
.btn-info {
    background: var(--info-gradient);
    color: white;
    box-shadow: 0 4px 15px rgba(168, 237, 234, 0.4);
}

.btn-info:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(168, 237, 234, 0.6);
    color: white;
}

/* Outline Butonlar */
.btn-outline-primary {
    background: transparent;
    color: #667eea;
    border: 2px solid #667eea;
}

.btn-outline-primary:hover {
    background: var(--primary-gradient);
    color: white;
    transform: translateY(-1px);
}

.btn-outline-secondary {
    background: transparent;
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-outline-secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
    transform: translateY(-1px);
}

/* Button Groups */
.btn-group .btn {
    border-radius: 0;
}

.btn-group .btn:first-child {
    border-top-left-radius: 8px;
    border-bottom-left-radius: 8px;
}

.btn-group .btn:last-child {
    border-top-right-radius: 8px;
    border-bottom-right-radius: 8px;
}

.btn-group-vertical .btn {
    border-radius: 0;
    width: 100%;
}

.btn-group-vertical .btn:first-child {
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

.btn-group-vertical .btn:last-child {
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}

/* Floating Action Button */
.fab {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: var(--primary-gradient);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    z-index: 1000;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.fab:hover {
    transform: scale(1.1);
    box-shadow: 0 12px 35px rgba(102, 126, 234, 0.6);
}

/* Button Loading State */
.btn.loading {
    position: relative;
    color: transparent;
}

.btn.loading::after {
    content: '';
    position: absolute;
    width: 16px;
    height: 16px;
    top: 50%;
    left: 50%;
    margin-left: -8px;
    margin-top: -8px;
    border: 2px solid transparent;
    border-top-color: currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

---

## ⬅️ **GERİ BUTONU VE NAVİGASYON KURALLARI**

### **1. Geri Butonu Yerleşim Kuralları**

#### **Liste Sayfalarında**
```html
<!-- Liste sayfalarında geri butonu genelde dashboard'a döner -->
<div class="page-header">
    <div class="row align-items-center">
        <div class="col-md-8">
            <div class="d-flex align-items-center">
                <a href="{% url 'dashboard:dashboard' %}" class="btn btn-outline-secondary me-3 btn-back">
                    <i class="fas fa-arrow-left"></i>
                </a>
                <div>
                    <h1 class="page-title mb-0">Malzemeler</h1>
                    <nav aria-label="breadcrumb" class="breadcrumb-modern">
                        <!-- Breadcrumb -->
                    </nav>
                </div>
            </div>
        </div>
    </div>
</div>
```

#### **Form Sayfalarında**
```html
<!-- Form sayfalarında geri butonu liste sayfasına döner -->
<div class="form-header">
    <div class="d-flex align-items-center mb-3">
        <a href="{% url 'erp:materials' %}" class="btn btn-outline-secondary me-3 btn-back">
            <i class="fas fa-arrow-left"></i>
        </a>
        <div>
            <h1 class="form-title mb-0">Yeni Malzeme Oluştur</h1>
            <p class="form-subtitle text-muted">Sisteme yeni malzeme ekleyin</p>
        </div>
    </div>
</div>
```

#### **Detay Sayfalarında**
```html
<!-- Detay sayfalarında geri butonu liste sayfasına döner -->
<div class="detail-header">
    <div class="row align-items-center">
        <div class="col-md-8">
            <div class="d-flex align-items-center">
                <a href="{% url 'erp:materials' %}" class="btn btn-outline-secondary me-3 btn-back">
                    <i class="fas fa-arrow-left"></i>
                </a>
                <div>
                    <h1 class="detail-title mb-0">{{ material.name }}</h1>
                    <div class="detail-meta">
                        <span class="badge bg-success">{{ material.status }}</span>
                        <span class="text-muted ms-2">Son güncelleme: {{ material.updated_at|date:"d.m.Y H:i" }}</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-4 text-end">
            <a href="{% url 'erp:material_edit' material.pk %}" class="btn btn-warning me-2">
                <i class="fas fa-edit"></i> Düzenle
            </a>
            <div class="dropdown d-inline-block">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <i class="fas fa-ellipsis-v"></i>
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="{% url 'erp:material_duplicate' material.pk %}">
                        <i class="fas fa-copy"></i> Kopyala
                    </a></li>
                    <li><a class="dropdown-item" href="{% url 'erp:material_history' material.pk %}">
                        <i class="fas fa-history"></i> Geçmiş
                    </a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item text-danger" href="{% url 'erp:material_delete' material.pk %}">
                        <i class="fas fa-trash"></i> Sil
                    </a></li>
                </ul>
            </div>
        </div>
    </div>
</div>
```

### **2. Navigation Hierarchy (Navigasyon Hiyerarşisi)**
```
Dashboard (Ana Sayfa)
├── ERP Modülleri
│   ├── Malzeme Yönetimi
│   │   ├── Malzeme Listesi ← Geri: Dashboard
│   │   ├── Yeni Malzeme ← Geri: Malzeme Listesi
│   │   ├── Malzeme Detay ← Geri: Malzeme Listesi
│   │   ├── Malzeme Düzenle ← Geri: Malzeme Detay
│   │   └── Kategori Yönetimi
│   │       ├── Kategori Listesi ← Geri: Malzeme Listesi
│   │       ├── Yeni Kategori ← Geri: Kategori Listesi
│   │       ├── Kategori Detay ← Geri: Kategori Listesi
│   │       └── Kategori Düzenle ← Geri: Kategori Detay
│   ├── Ürün Yönetimi
│   │   ├── Ürün Listesi ← Geri: Dashboard
│   │   ├── Yeni Ürün ← Geri: Ürün Listesi
│   │   ├── Ürün Detay ← Geri: Ürün Listesi
│   │   └── Ürün Kategorileri ← Geri: Ürün Listesi
│   └── Diğer Modüller...
```

### **3. Mobile Navigation**
```html
<!-- Mobile hamburger menu -->
<div class="mobile-nav-header d-md-none">
    <button class="mobile-nav-toggle" id="mobileNavToggle">
        <i class="fas fa-bars"></i>
    </button>
    <div class="mobile-nav-title">Context7 ERP</div>
    <button class="mobile-back-btn" onclick="history.back()">
        <i class="fas fa-arrow-left"></i>
    </button>
</div>

<!-- Mobile navigation overlay -->
<div class="mobile-nav-overlay" id="mobileNavOverlay">
    <div class="mobile-nav-content">
        <div class="mobile-nav-header-inner">
            <h5>Context7 ERP</h5>
            <button class="mobile-nav-close" id="mobileNavClose">
                <i class="fas fa-times"></i>
            </button>
        </div>
        
        <div class="mobile-nav-body">
            <!-- Navigation items -->
            <a href="{% url 'dashboard:dashboard' %}" class="mobile-nav-item">
                <i class="fas fa-tachometer-alt"></i>
                <span>Dashboard</span>
            </a>
            
            <div class="mobile-nav-section">
                <div class="mobile-nav-section-title">ERP Modülleri</div>
                <a href="{% url 'erp:materials' %}" class="mobile-nav-item">
                    <i class="fas fa-boxes"></i>
                    <span>Malzemeler</span>
                </a>
                <a href="{% url 'erp:products' %}" class="mobile-nav-item">
                    <i class="fas fa-cube"></i>
                    <span>Ürünler</span>
                </a>
                <!-- Diğer modüller -->
            </div>
        </div>
    </div>
</div>
```

### **4. Geri Butonu CSS Stilleri**
```css
/* Geri Butonu Stilleri */
.btn-back {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.8);
    padding: 10px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
    min-width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.btn-back:hover {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    transform: translateX(-2px);
    border-color: rgba(255, 255, 255, 0.3);
}

.btn-back:focus {
    box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
}

/* Mobile Navigation Styles */
.mobile-nav-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    background: var(--primary-gradient);
    color: white;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1001;
}

.mobile-nav-toggle,
.mobile-back-btn,
.mobile-nav-close {
    background: none;
    border: none;
    color: white;
    font-size: 18px;
    padding: 8px;
    border-radius: 6px;
    transition: background 0.3s ease;
    cursor: pointer;
}

.mobile-nav-toggle:hover,
.mobile-back-btn:hover,
.mobile-nav-close:hover {
    background: rgba(255, 255, 255, 0.1);
}

.mobile-nav-title {
    font-weight: 600;
    font-size: 1.1rem;
}

.mobile-nav-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1002;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.mobile-nav-overlay.show {
    opacity: 1;
    visibility: visible;
}

.mobile-nav-content {
    position: absolute;
    left: 0;
    top: 0;
    width: 280px;
    height: 100%;
    background: linear-gradient(180deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
    backdrop-filter: blur(25px);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    overflow-y: auto;
}

.mobile-nav-overlay.show .mobile-nav-content {
    transform: translateX(0);
}

.mobile-nav-header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.mobile-nav-body {
    padding: 20px 0;
}

.mobile-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 20px;
    color: rgba(255, 255, 255, 0.9);
    text-decoration: none;
    transition: all 0.3s ease;
}

.mobile-nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

.mobile-nav-section {
    margin: 20px 0;
}

.mobile-nav-section-title {
    padding: 8px 20px;
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Main content offset for mobile */
@media (max-width: 768px) {
    .main-content {
        margin-top: 70px; /* Mobile header height */
        margin-left: 0;
    }
}

@media (min-width: 769px) {
    .main-content {
        margin-left: 280px; /* Sidebar width */
        margin-top: 0;
    }
    
    .mobile-nav-header {
        display: none;
    }
}
```

---

## 📱 **MOBILE YERLEŞIM KURALLARI**

### **1. Mobile Button Layout**
```css
/* Mobile'da butonlar responsive */
@media (max-width: 768px) {
    .btn-mobile-full {
        width: 100%;
        margin-bottom: 12px;
    }
    
    .btn-group-mobile {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .btn-group-mobile .btn {
        width: 100%;
    }
    
    /* Page header mobile */
    .page-header .col-md-4 {
        margin-top: 16px;
    }
    
    .page-header .text-end {
        text-align: left !important;
    }
    
    /* Form actions mobile */
    .form-actions {
        flex-direction: column;
        gap: 12px;
    }
    
    .form-actions .ms-auto {
        margin-left: 0 !important;
        margin-top: 12px;
    }
    
    /* Table actions mobile */
    .btn-group {
        flex-direction: column;
        width: 100%;
    }
    
    .btn-group .btn {
        border-radius: 8px !important;
        margin-bottom: 4px;
    }
    
    /* Floating Action Button Mobile */
    .fab-mobile {
        bottom: 20px;
        right: 20px;
        width: 56px;
        height: 56px;
    }
}

/* Tablet adjustments */
@media (min-width: 769px) and (max-width: 1024px) {
    .btn {
        padding: 10px 20px;
        font-size: 0.875rem;
    }
    
    .btn-sm {
        padding: 6px 12px;
        font-size: 0.8125rem;
    }
}
```

### **2. Mobile Navigation Patterns**
```html
<!-- Bottom Navigation (Mobile) -->
<nav class="bottom-nav d-md-none">
    <a href="{% url 'dashboard:dashboard' %}" class="bottom-nav-item {% if request.resolver_match.namespace == 'dashboard' %}active{% endif %}">
        <i class="fas fa-home"></i>
        <span>Ana Sayfa</span>
    </a>
    <a href="{% url 'erp:materials' %}" class="bottom-nav-item {% if 'materials' in request.path %}active{% endif %}">
        <i class="fas fa-boxes"></i>
        <span>Malzemeler</span>
    </a>
    <a href="{% url 'erp:products' %}" class="bottom-nav-item {% if 'products' in request.path %}active{% endif %}">
        <i class="fas fa-cube"></i>
        <span>Ürünler</span>
    </a>
    <a href="{% url 'users:profile' %}" class="bottom-nav-item">
        <i class="fas fa-user"></i>
        <span>Profil</span>
    </a>
</nav>

<!-- Bottom Navigation CSS -->
<style>
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(25px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-around;
    padding: 8px 0;
    z-index: 1000;
}

.bottom-nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8px 12px;
    color: rgba(255, 255, 255, 0.6);
    text-decoration: none;
    font-size: 0.75rem;
    transition: all 0.3s ease;
    border-radius: 8px;
    min-width: 60px;
}

.bottom-nav-item:hover,
.bottom-nav-item.active {
    color: #667eea;
    background: rgba(102, 126, 234, 0.1);
}

.bottom-nav-item i {
    font-size: 18px;
    margin-bottom: 4px;
}

/* Main content bottom padding for mobile */
@media (max-width: 768px) {
    .main-content {
        padding-bottom: 80px; /* Bottom nav height */
    }
}
</style>
```

---

## 🎯 **BUTON KULLANIM REHBERİ**

### **1. Buton Öncelik Sırası**
1. **Primary (Mavi)**: Ana işlemler (Kaydet, Oluştur, Onayla)
2. **Secondary (Gri)**: İkincil işlemler (İptal, Geri, Kategoriler)
3. **Success (Yeşil)**: Onay işlemleri (Onayla, Tamamla)
4. **Warning (Turuncu)**: Düzenleme işlemleri (Düzenle, Güncelle)
5. **Danger (Kırmızı)**: Silme işlemleri (Sil, Kaldır)
6. **Info (Açık Mavi)**: Görüntüleme işlemleri (Detay, Görüntüle)

### **2. Buton Boyut Rehberi**
- **btn-lg**: Dashboard ana butonları
- **btn (normal)**: Form ve sayfa butonları
- **btn-sm**: Tablo içi action butonları

### **3. Buton Icon Rehberi**
- **fas fa-save**: Kaydet
- **fas fa-plus**: Yeni/Ekle
- **fas fa-edit**: Düzenle
- **fas fa-trash**: Sil
- **fas fa-eye**: Görüntüle/Detay
- **fas fa-arrow-left**: Geri
- **fas fa-layer-group**: Kategoriler
- **fas fa-check**: Onayla
- **fas fa-times**: İptal/Kapat

---

## 📝 **FORM ELEMENT STYLING RULES**

### **Form Controls CSS:**
```css
.form-control, .form-select {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    color: rgba(255, 255, 255, 0.9);
    padding: 12px 16px;
    transition: all 0.3s ease;
    font-size: 0.875rem;
}

.form-control:focus, .form-select:focus {
    background: rgb(146, 131, 203);
    border-color: rgba(255, 255, 255, 0.4);
    box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
    color: white;
    outline: none;
}

.form-control::placeholder {
    color: rgba(255, 255, 255, 0.6);
    transition: color 0.3s ease;
}

.form-control:focus::placeholder {
    color: rgba(255, 255, 255, 0.8);
}

/* Form Labels */
.form-label {
    color: rgba(255, 255, 255, 0.9);
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 0.875rem;
}

/* Required field indicator */
.form-label.required::after {
    content: ' *';
    color: #fc466b;
}
```

---

**Bu kurallar Context7 ERP sistemindeki tüm menü, buton ve yerleşim tasarımları için standart referans olarak kullanılmalıdır.** 