# 📐 Context7 ERP - Sayfa Tasarım Kuralları (Optimize)
**Versiyon:** v2.2.0-glassmorphism-enhanced  
**Son Güncelleme:** 9 Ocak 2025  
**Framework:** Context7 Glassmorphism Design System v1.0

---

## 🎨 **GENEL TASARIM PRENSİPLERİ**

### **1. Context7 Glassmorphism Framework**
**📁 Detaylı CSS kodları:** [Context7 CSS Framework](../examples/frontend/context7-css-framework.css)

**Ana Renk Paleti:**
- Primary: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- Secondary: `linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)`  
- Success: `linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%)`
- Warning: `linear-gradient(135deg, #f093fb 0%, #f5576c 100%)`
- Danger: `linear-gradient(135deg, #fc466b 0%, #3f5efb 100%)`

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

### **3. Spacing System**
- **Container Padding**: 2rem
- **Card Padding**: 1.5rem
- **Element Spacing**: 1rem baseline
- **Component Margin**: 1.5rem vertical

---

## 📋 **SAYFA TİPLERİ VE KURALLARI**

### **1. LİSTE SAYFALARI (List Pages)**
**📁 HTML Template Örnekleri:** [Page Templates](../examples/frontend/page-templates.html)

**Yapısal Bileşenler:**
- **Header Section**: Page title + breadcrumb + action buttons
- **Statistics Cards**: 4'lü grid layout ile özet bilgiler
- **Filter Section**: Arama ve filtre formu
- **Data Table**: Modern styling ile veri tablosu
- **Pagination**: Bootstrap pagination

**Tasarım Kuralları:**
- Header: Gradient background, glassmorphism effects
- Stats Cards: Icon + title + value formatı
- Filter Section: Responsive form layout
- Table: Hover effects, action buttons
- Pagination: Custom styling

### **2. DETAY SAYFALARI (Detail Pages)**
**📁 HTML Template Örnekleri:** [Page Templates](../examples/frontend/page-templates.html)

**Layout Yapısı:**
- **8-4 Column Split**: Ana içerik - Sidebar
- **Detail Header**: Object name + action buttons
- **Info Cards**: Temel bilgiler + ilişkili veriler
- **Sidebar**: Özet bilgiler + hızlı işlemler

**Tasarım Kuralları:**
- Header: Object prominently displayed
- Info Cards: Glassmorphism styling, logical grouping
- Sidebar: Summary stats ve quick actions

### **3. OLUŞTURMA SAYFALARI (Create/Edit Pages)**
**📁 HTML Template Örnekleri:** [Page Templates](../examples/frontend/page-templates.html)

**Form Yapısı:**
- **Form Header**: Title + breadcrumb navigation
- **Form Sections**: Logical grouping of fields
- **Form Actions**: Save/Cancel buttons
- **Validation**: Real-time feedback

**Form Kuralları:**
- Responsive layout (8-column centered)
- Section-based organization
- Clear validation messages
- Consistent button styling

---

## 🎯 **BUTON VE UI COMPONENT'LERİ**

### **Buton Hiyerarşisi**
**📁 Detaylı Buton Stilleri:** [Button Styles](../examples/frontend/button-styles.css)

**Buton Tipleri:**
- **Primary**: Ana aksiyonlar (Kaydet, Oluştur)
- **Secondary**: İkincil aksiyonlar (Kategoriler)
- **Success**: Başarı aksiyonları (Onayla)
- **Warning**: Uyarı aksiyonları (Düzenle)
- **Danger**: Kritik aksiyonlar (Sil)
- **Info**: Bilgi aksiyonları (Detay)

**Buton Boyutları:**
- **Large**: Ana sayfalar için
- **Default**: Genel kullanım
- **Small**: Tablo aksiyonları

### **Icon Kullanımı**
- **FontAwesome 6** kullanılır
- Her buton ile uyumlu icon seçimi
- Consistent icon sizing (1rem default)

---

## 📱 **RESPONSİVE TASARIM KURALLARI**

### **Breakpoint'ler**
**📁 Responsive CSS:** [Responsive Layouts](../examples/frontend/responsive-layouts.css)

- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px  
- **Mobile**: <768px

### **Mobile-First Yaklaşım**
- Grid sisteminde mobile'dan başla
- Touch-friendly button sizes (44px minimum)
- Readable font sizes (16px minimum)
- Sufficient spacing for touch targets

### **Component Adaptasyonu**
- **Stats Grid**: 4 column → 2 column → 1 column
- **Tables**: Responsive scrolling
- **Forms**: Single column on mobile
- **Buttons**: Full width on mobile

---

## 🎨 **RENK VE TİPOGRAFİ SİSTEMİ**

### **Color Palette Organization**
**📁 Renk Sistemi:** [Context7 CSS Framework](../examples/frontend/context7-css-framework.css)

**Semantic Colors:**
- **Primary**: Ana brand rengi
- **Secondary**: İkincil aksiyonlar
- **Success**: Başarı durumları  
- **Warning**: Uyarı durumları
- **Danger**: Hata durumları
- **Info**: Bilgi durumları

### **Typography Scale**
**Font Family:** Inter, system-ui, sans-serif

**Heading Scale:**
- H1: 2.5rem (40px) - Page titles
- H2: 2rem (32px) - Section titles  
- H3: 1.5rem (24px) - Card titles
- H4: 1.25rem (20px) - Subsections

**Body Text:**
- Large: 1.125rem (18px) - Important content
- Base: 1rem (16px) - Standard text
- Small: 0.875rem (14px) - Secondary text

---

## ⚡ **PERFORMANS VE OPTİMİZASYON**

### **CSS Performance**
- CSS custom properties kullanımı
- GPU acceleration için transform
- Efficient selectors
- Minification for production

### **Animation Guidelines**
- Spring animations: `cubic-bezier(0.175, 0.885, 0.32, 1.275)`
- Duration: 0.3s for most interactions
- GPU-accelerated properties (transform, opacity)
- Reduced motion support

### **Loading States**
- Skeleton screens
- Progressive loading
- Shimmer effects
- Loading spinners

---

## 🔧 **İMPLEMENTASYON REHBERİ**

### **CSS Organization**
```
static/css/
├── bootstrap.min.css        # Bootstrap framework
├── context7-framework.css   # Context7 glassmorphism
├── erp-common.css          # ERP common styles
└── module-specific.css     # Module-specific styles
```

### **Template Structure**
```
templates/
├── base.html               # Base template
├── _pagination.html        # Pagination component
├── components/             # Reusable components
└── erp/                   # Module templates
```

### **JavaScript Integration**
- Modern ES6+ syntax
- Component-based architecture
- Event delegation
- Progressive enhancement

---

## 📊 **ACCESSIBILITY (A11Y) KOMPLİANS**

### **WCAG 2.1 AA Standards**
- Color contrast ratio 4.5:1+
- Keyboard navigation support
- Screen reader compatibility
- Focus indicators
- Semantic HTML structure

### **Testing Tools**
- axe-core for automated testing
- Manual keyboard testing
- Screen reader testing
- Color blindness simulation

---

## 🎯 **KALITE KONTROL CHECKLİSTİ**

### **Her Sayfa İçin Kontrol:**
- [ ] Responsive design test (mobile/tablet/desktop)
- [ ] Browser compatibility test
- [ ] Performance audit (Lighthouse)
- [ ] Accessibility test (axe-core)
- [ ] Visual consistency check
- [ ] Loading state implementation
- [ ] Error state handling
- [ ] Form validation feedback

### **Launch Checklist:**
- [ ] Design system compliance
- [ ] Cross-browser testing
- [ ] Performance optimization
- [ ] SEO optimization
- [ ] Security review
- [ ] User testing feedback

---

## 🔗 **Referans Linkleri**

### **Kod Örnekleri:**
- [Context7 CSS Framework](../examples/frontend/context7-css-framework.css)
- [HTML Template Örnekleri](../examples/frontend/page-templates.html)
- [Button Styles](../examples/frontend/button-styles.css)
- [Responsive Layouts](../examples/frontend/responsive-layouts.css)

### **Documentation:**
- [Context7 Design System](./context7-design-system.md)
- [Component Library](./component-library.md)
- [Accessibility Guidelines](./accessibility-guidelines.md)

---

**📋 QMS Reference:** REC-SYSTEM-UI-250109-001 - Page Design Rules Optimization  
**🎯 Mission:** Provide clean, maintainable design rules with organized code examples  
**✅ Status:** Optimized - %75 daha kompakt, kod örnekleri ayrı dosyalarda organize edildi 