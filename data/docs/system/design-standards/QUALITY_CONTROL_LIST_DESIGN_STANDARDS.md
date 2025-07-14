# 🎨 Kalite Kontrol Liste Tasarım Standartları

**Versiyon**: v1.0  
**Son Güncelleme**: 29 Aralık 2024  
**Durum**: ✅ UYGULANMIŞ  
**QMS Referans**: REC-QUALITY-DESIGN-241229-001  

---

## 📋 Genel Bakış

Context7 ERP sistemindeki tüm kalite kontrol listeleri için standart tasarım kuralları ve yazı okunabilirlik standartları tanımlanmıştır. Bu standartlar, tutarlı kullanıcı deneyimi ve maksimum yazı okunabilirliği sağlamak için oluşturulmuştur.

### 🎯 Hedefler
- **Yazı Okunabilirliği**: Maksimum text contrast ve font optimization
- **Tutarlılık**: Tüm kalite kontrol listelerinde aynı tasarım
- **Context7 Uyumluluğu**: Glassmorphism framework standartlarına uygunluk
- **Erişilebilirlik**: WCAG 2.1 AA uyumluluğu
- **Responsive Tasarım**: Tüm cihaz boyutlarında optimal görünüm

---

## 🎨 Tasarım Sistemi

### **CSS Dosyası**: `static/css/quality_control_list_styles.css`

Bu dosya tüm kalite kontrol listelerinde kullanılacak standart stilleri içerir:

#### **Renk Paleti**
```css
:root {
    /* Quality Control Color Palette */
    --qc-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --qc-success: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
    --qc-warning: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --qc-danger: linear-gradient(135deg, #fc466b 0%, #3f5efb 100%);
    --qc-info: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}
```

#### **Yazı Okunabilirlik Renkleri**
```css
:root {
    /* Enhanced Text Readability */
    --qc-text-primary: #ffffff;           /* Ana yazılar için */
    --qc-text-secondary: rgba(255, 255, 255, 0.9);  /* İkincil yazılar */
    --qc-text-muted: rgba(255, 255, 255, 0.75);     /* Açıklama yazıları */
    --qc-text-dark: #2d3748;             /* Koyu arkaplan için */
    --qc-text-dark-secondary: #4a5568;   /* Koyu arkaplan ikincil */
}
```

---

## 📝 Uygulanan Template'ler

### ✅ Güncellenmiş Dosyalar
1. **`erp/templates/erp/quality/incoming_control_list.html`**
2. **`erp/templates/erp/quality/inprocess_control_list.html`**  
3. **`erp/templates/erp/quality/final_control_list.html`**

### 🔄 CSS Entegrasyonu
Her template'in `{% block extra_css %}` bölümüne eklenen:
```html
<link rel="stylesheet" href="{% static 'css/quality_control_list_styles.css' %}">
```

---

## 🏗️ Standart Bileşenler

### **1. Ana Container**
```html
<div class="container-fluid py-4 quality-control-page">
```
- **Amaç**: Sayfa düzeni ve font ayarları
- **Özellikler**: Enhanced font family, line-height, letter-spacing

### **2. Breadcrumb Navigation**
```html
<div class="qc-breadcrumb-container">
    <nav aria-label="breadcrumb">
        <ol class="qc-breadcrumb breadcrumb">
```
- **Yazı Okunabilirliği**: Text shadow, enhanced contrast
- **Hover Efektleri**: Smooth transitions, glow effects

### **3. Kalite Kontrol Sekmeler**
```html
<div class="qc-tabs">
    <a href="#" class="qc-tab active">
```
- **Active State**: Gradient background, enhanced text contrast
- **Hover State**: Improved visibility, smooth animations

### **4. Başlık Bölümü**
```html
<div class="qc-glass-container">
    <h1 class="qc-header">{{ page_title }}</h1>
```
- **Text Enhancement**: Gradient text, text shadow for depth
- **Module Colors**:
  - Incoming: Primary gradient
  - Inprocess: Warning gradient
  - Final: Success gradient

### **5. İstatistik Kartları**
```html
<div class="qc-stats-row">
    <div class="qc-stat-card">
        <div class="qc-stat-number">{{ count }}</div>
        <div class="qc-stat-label">Label</div>
```
- **Number Display**: Gradient text, larger font size
- **Label Text**: Enhanced contrast, uppercase styling

### **6. Arama Kontrolleri**
```html
<div class="qc-search-controls">
    <input type="text" class="qc-search-box">
    <button class="qc-btn-search">
```
- **Input Styling**: Enhanced background, border contrast
- **Placeholder**: Improved visibility, emoji icons

### **7. Veri Tablosu**
```html
<div class="qc-table">
    <table class="table table-transparent mb-0">
        <thead>
            <tr>
                <th class="qc-table th">Header</th>
```
- **Header Styling**: Enhanced background, text shadow
- **Cell Styling**: Improved padding, border contrast
- **Hover Effects**: Smooth transitions, enhanced visibility

### **8. Durum Rozetleri**
```html
<span class="qc-status-badge qc-status-approved">
    <i class="fas fa-check"></i> Onaylı
</span>
```
- **Colors**:
  - **Approved**: Success gradient
  - **Rejected**: Danger gradient
  - **Pending**: Warning gradient
  - **Conditional**: Info gradient
- **Styling**: Text shadow, enhanced contrast, min-width

### **9. Aksiyon Butonları**
```html
<a href="#" class="qc-action-btn">
    <i class="fas fa-eye"></i> Detay
</a>
```
- **Base Styling**: Glassmorphism background, enhanced borders
- **Hover Effects**: Color change, scale animation, shadow

### **10. Boş Durum**
```html
<div class="qc-empty-state">
    <i class="fas fa-clipboard-list"></i>
    <h3>Mesaj</h3>
    <p>Açıklama</p>
```
- **Icon**: Large gradient icon, opacity effects
- **Text**: Enhanced contrast, proper hierarchy

### **11. Sayfalama**
```html
<div class="qc-pagination-container">
    <ul class="qc-pagination pagination">
        <li class="qc-page-item page-item">
            <a class="qc-page-link page-link">
```
- **Styling**: Enhanced backgrounds, improved hover states
- **Active State**: Gradient background, text shadow

---

## 🔧 Yazı Okunabilirlik Geliştirmeleri

### **1. Font Optimizasyonu**
- **Font Family**: 'Segoe UI', 'Roboto', system fonts
- **Font Weight**: 500 (normal), 600-700 (headings)
- **Line Height**: 1.6 for optimal readability
- **Letter Spacing**: 0.025em for better character separation

### **2. Text Shadow Kullanımı**
```css
text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);  /* Normal text */
text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);  /* Important text */
```

### **3. Contrast Enhancement**
- **Light Text on Dark**: White text with transparency levels
- **Dark Background**: `rgba(0, 0, 0, 0.2)` for better contrast
- **Border Enhancement**: `rgba(255, 255, 255, 0.3)` for visibility

### **4. Info Card Styling**
```html
<div class="qc-info-card">
    <strong>Primary Info</strong><br>
    <small>Secondary Info</small>
</div>
```
- **Background**: Enhanced glassmorphism
- **Text Colors**: Primary white, secondary muted
- **Font Weights**: Bold for primary, normal for secondary

---

## 📱 Responsive Design

### **Mobile Optimizations**
```css
@media (max-width: 768px) {
    .qc-tabs { flex-direction: column; }
    .qc-tab { margin: 0.25rem 0; }
    .qc-table th, .qc-table td { 
        padding: 0.8rem 0.5rem;
        font-size: 0.85rem;
    }
    .qc-header { font-size: 2rem; }
}
```

### **Print Styles**
```css
@media print {
    /* Hide interactive elements */
    .qc-tabs, .qc-search-controls, .qc-action-btn { 
        display: none !important; 
    }
    /* Optimize for printing */
    .qc-glass-container { 
        background: white !important;
        color: black !important;
    }
}
```

---

## 🎯 Uygulama Kılavuzu

### **1. Yeni Liste Sayfası Oluşturma**
```html
{% extends 'base.html' %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/quality_control_list_styles.css' %}">
{% endblock %}

{% block content %}
<div class="container-fluid py-4 quality-control-page">
    <!-- Standart bileşenleri kullan -->
</div>
{% endblock %}
```

### **2. CSS Class Kullanımı**
- **Container**: `qc-glass-container`
- **Header**: `qc-header`
- **Table**: `qc-table`
- **Status**: `qc-status-badge qc-status-[type]`
- **Button**: `qc-action-btn` veya `qc-btn-create`

### **3. Renk Tutarlılığı**
- **Incoming Control**: Primary colors
- **Inprocess Control**: Warning colors  
- **Final Control**: Success colors
- **General Elements**: CSS variables kullan

---

## ✅ Kontrol Listesi

### **Template Güncellemesi İçin**
- [ ] CSS dosyasını include et
- [ ] Class isimlerini güncelle (`.qc-` prefix)
- [ ] Text shadow ve contrast ayarlarını uygula
- [ ] Status badge'leri standartlaştır
- [ ] Action button'ları güncelleVaist
- [ ] Mobile responsive kontrol et
- [ ] Print styles test et

### **Yazı Okunabilirlik Kontrol**
- [ ] Text contrast ratio >4.5:1
- [ ] Text shadow uygulandı
- [ ] Font size mobile'da uygun
- [ ] Line height optimal (1.6)
- [ ] Letter spacing uygulandı

---

## 🚀 Sonuç

Bu standartlar sayesinde:

- ✅ **Tutarlı Tasarım**: Tüm kalite kontrol listelerinde aynı görünüm
- ✅ **Gelişmiş Okunabilirlik**: Text shadow, contrast, font optimizasyonu
- ✅ **Context7 Uyumluluğu**: Glassmorphism framework ile entegrasyon
- ✅ **Responsive Design**: Tüm cihazlarda optimal görünüm
- ✅ **Erişilebilirlik**: WCAG 2.1 AA uyumluluğu
- ✅ **Maintainability**: Tek CSS dosyasında merkezi yönetim

### **Gelecek Geliştirmeler**
1. Dark mode support
2. High contrast mode
3. Animation preferences
4. Font size user settings

---

**📞 Destek**: Bu standartlarla ilgili sorular için development team ile iletişime geçin.  
**🔄 Güncelleme**: Tasarım standartları sürekli olarak geliştirilmektedir.  
**📊 QMS**: Bu dokümantasyon QMS Central Protocol v1.0 uyumludur. 