# Context7 ERP System - Site Map Documentation

## 📊 Overview
Bu dokümantasyon, Context7 ERP sistemindeki tüm sayfaların ve URL'lerin kapsamlı listesini içerir.

**Last Updated:** 11 Haziran 2025  
**Version:** v2.2.0-glassmorphism-enhanced  
**Total Pages:** 35+ URL patterns

---

## 🏠 Main Dashboard & Navigation

### Core Dashboard
- **Main Dashboard:** `/`
- **Dashboard Overview:** `/dashboard/`

---

## 🏭 ERP Department Modules

### ERP Main Hub
- **ERP Main Dashboard:** `/erp/`

### Department Dashboards
- **Production Department:** `/erp/production/`
- **Inventory Department:** `/erp/inventory/`
- **Sales Department:** `/erp/sales/`
- **Purchasing Department:** `/erp/purchasing/`
- **Finance Department:** `/erp/finance/`
- **Human Resources:** `/erp/hr/`
- **Quality Control:** `/erp/quality/`
- **Materials Management:** `/erp/materials/`

---

## 🔍 Quality Control CRUD Operations

### Incoming Control Forms (Gelen Malzeme Kontrolü)
- **List All Forms:** `/erp/quality/incoming/`
- **Create New Form:** `/erp/quality/incoming/create/`
- **View Form Details:** `/erp/quality/incoming/<id>/`
- **Edit Form:** `/erp/quality/incoming/<id>/edit/`
- **Delete Form:** `/erp/quality/incoming/<id>/delete/`

### In-Process Control Forms (Süreç İçi Kontrol)
- **List All Forms:** `/erp/quality/inprocess/`
- **Create New Form:** `/erp/quality/inprocess/create/`
- **View Form Details:** `/erp/quality/inprocess/<id>/`
- **Edit Form:** `/erp/quality/inprocess/<id>/edit/`
- **Delete Form:** `/erp/quality/inprocess/<id>/delete/`

### Final Control Forms (Final Kontrol)
- **List All Forms:** `/erp/quality/final/`
- **Create New Form:** `/erp/quality/final/create/`
- **View Form Details:** `/erp/quality/final/<id>/`
- **Edit Form:** `/erp/quality/final/<id>/edit/`
- **Delete Form:** `/erp/quality/final/<id>/delete/`

---

## 📦 Core CRUD Operations

### Product Management
- **Product List:** `/erp/products/`
- **Create Product:** `/erp/products/create/`
- **Product Details:** `/erp/products/<id>/`
- **Edit Product:** `/erp/products/<id>/edit/`
- **Delete Product:** `/erp/products/<id>/delete/`

### Customer Management
- **Customer List:** `/erp/customers/`
- **Create Customer:** `/erp/customers/create/`
- **Customer Details:** `/erp/customers/<id>/`
- **Edit Customer:** `/erp/customers/<id>/edit/`
- **Delete Customer:** `/erp/customers/<id>/delete/`

### Supplier Management
- **Supplier List:** `/erp/suppliers/`
- **Create Supplier:** `/erp/suppliers/create/`
- **Supplier Details:** `/erp/suppliers/<id>/`
- **Edit Supplier:** `/erp/suppliers/<id>/edit/`
- **Delete Supplier:** `/erp/suppliers/<id>/delete/`

### Material Management
- **Material List:** `/erp/materials/list/`
- **Create Material:** `/erp/materials/create/`
- **Material Details:** `/erp/materials/<id>/`
- **Edit Material:** `/erp/materials/<id>/edit/`
- **Delete Material:** `/erp/materials/<id>/delete/`

---

## 📊 Operational Modules

### Inventory Management
- **Inventory Dashboard:** `/inventory/`
- **Inventory Items:** `/inventory/items/`
- **Create Inventory Item:** `/inventory/items/create/`
- **Item Details:** `/inventory/items/<id>/`
- **Edit Item:** `/inventory/items/<id>/edit/`

### Production Management
- **Production Dashboard:** `/production/`
- **Work Orders:** `/production/work-orders/`
- **Create Work Order:** `/production/work-orders/create/`
- **Work Order Details:** `/production/work-orders/<id>/`

### Work Orders (Standalone)
- **Work Orders List:** `/work-orders/`
- **Create Work Order:** `/work-orders/create/`
- **Work Order Details:** `/work-orders/<id>/`
- **Edit Work Order:** `/work-orders/<id>/edit/`

---

## 📈 Reports & Analytics

### Report Hub
- **Reports Dashboard:** `/reports/`
- **Production Reports:** `/reports/production/`
- **Inventory Reports:** `/reports/inventory/`
- **Quality Control Reports:** `/reports/quality/`

---

## ⚙️ System Administration

### Settings & Configuration
- **System Settings:** `/settings/`
- **User Management:** `/users/`

### Labels & Printing
- **Label Management:** `/labels/`

---

## 🔌 API Endpoints

### API Root
- **API Root:** `/api/`
- **API v1:** `/api/v1/`

### API Resources
- **Products API:** `/api/v1/products/`
- **Customers API:** `/api/v1/customers/`
- **Suppliers API:** `/api/v1/suppliers/`
- **Quality Control API:** `/api/v1/quality/`

---

## 🔐 Authentication

### Auth Pages
- **Login:** `/auth/login/`
- **Logout:** `/auth/logout/`

---

## 📊 SEO & Priority Information

### Priority Levels
- **Priority 1.0:** Main Dashboard (Highest)
- **Priority 0.9:** Dashboard Overview
- **Priority 0.8:** Department Dashboards, Core Modules
- **Priority 0.7:** CRUD List Pages, Reports
- **Priority 0.6:** Create/Edit Forms, Detail Views
- **Priority 0.5:** Settings, User Management
- **Priority 0.4:** API Endpoints
- **Priority 0.3-0.2:** Authentication (Lowest)

### Update Frequency
- **Daily:** Main Dashboard, Inventory, Production
- **Weekly:** Department Dashboards, CRUD Operations, Reports
- **Monthly:** Create Forms, Settings, API
- **Rarely:** Authentication Pages

---

## 🔄 Maintenance & Updates

### Sitemap File Locations
- **Primary Sitemap:** `static/sitemap.xml`
- **Documentation:** `docs/system/sitemap.md`

### Update Guidelines
1. Update `lastmod` date when content changes
2. Adjust `changefreq` based on actual usage patterns
3. Review priorities quarterly for SEO optimization
4. Add new URLs when features are added
5. Remove deprecated URLs after migration

---

## 🚀 Context7 Standards Compliance

### URL Pattern Standards
- Clean, RESTful URL structure
- Consistent naming conventions
- Descriptive path segments
- Proper HTTP method usage (GET, POST, PUT, DELETE)

### SEO Optimization
- Structured sitemap.xml format
- Appropriate meta tags
- Schema.org markup (planned)
- Mobile-friendly URLs

---

*This sitemap documentation is part of the Context7 ERP System v2.2.0-glassmorphism-enhanced and follows Context7 documentation standards.* 