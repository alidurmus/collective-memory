# 🏛️ **Context7 Django ERP System - Merkezi Protokol v1.0**

**Amaç:** Context7 Django ERP System projesindeki tüm geliştirme süreçlerinin, proje hedeflerine ve mimarisine tam uyumlu bir şekilde yürütülmesi için oluşturulmuş ana kural setidir. Tüm AI Coder'lar ve geliştiriciler bu protokole uymakla yükümlüdür.

**Teknoloji Stack:** Django 4.x + SQLite/PostgreSQL + Context7 Glassmorphism Framework + REST API + JWT Authentication

---

## **📜 1. Ana Kural: Single Source of Truth - Merkezi Dokümantasyon Otoritesi**

### **Tek Yetkili Doküman:** 
Projenin amacı, kapsamı, modülleri, mimarisi ve hedefleri ile ilgili tüm temel bilgiler için tek ve nihai kaynak **Repository-specific rules** ve **`docs/system/bekleyen-isler.md`** dosyalarıdır.

### **Öncelik Sırası:** 
1. **Repository-specific rules** (En yüksek otorite)
2. **`docs/system/bekleyen-isler.md`** (Güncel görevler ve hedefler)
3. **Bu protokol dosyası** (İş akışı kuralları)
4. **Diğer dokümantasyon dosyaları**

### **Değişiklik Yönetimi:** 
Projenin ana yapısını etkileyen tüm değişiklikler öncelikle Repository-specific rules'a işlenmeli, ardından bekleyen-isler.md güncellenmeli ve son olarak ilgili dokümantasyon dosyalarına yansıtılmalıdır.

---

## **🗺️ 2. Context7 ERP Dokümantasyon Haritası**

### **2.1. Dokümantasyon Hiyerarşisi**
```
Repository Root/
├── 📋 Repository-specific rules        # 🎯 ANA OTORİTE - Tüm kurallar ve standartlar
├── docs/system/bekleyen-isler.md      # 📅 GÜNCEL HEDEFLER - Aktif görevler
├── docs/system/                       # 🏗️ SİSTEM DOKÜMANTASYONU
│   ├── CONTEXT7_CENTRAL_PROTOCOL.md   # 🏛️ Bu dosya - Merkezi protokol
│   ├── ERROR_REFERENCE_SYSTEM.md      # 🏷️ Hata referans sistemi  
│   ├── KNOWLEDGE_BASE.md              # 🧠 Bilgi tabanı sistemi
│   ├── PERFORMANCE_MONITORING_RULES.md # 📊 Performans izleme kuralları
│   └── API_DOCUMENTATION_STANDARDS.md # 📚 API dokümantasyon standartları
├── docs/deployment/                   # 🚀 DEPLOYMENT DOKÜMANTASYONU
├── docs/api/                         # 📡 API DOKÜMANTASYONU
├── docs/reports/                     # 📈 RAPOR VE ANALİZ
└── .cursor/rules/                    # 🤖 AI ASSISTANT KURALLARI
```

### **2.2. AI Coder Başvuru Protokolü (ZORUNLU)**
Her AI Coder, herhangi bir göreve başlamadan önce aşağıdaki adımları izlemelidir:

1. **Adım 1: Repository Rules'u Oku:** Her zaman önce Repository-specific rules'u tamamen oku
2. **Adım 2: Bekleyen İşleri Kontrol Et:** `docs/system/bekleyen-isler.md` dosyasından mevcut durumu anla
3. **Adım 3: Spesifik Dokümanları İncele:** İlgili alan için dokümantasyon haritasını kullan
4. **Adım 4: Görevi Uygula:** Tüm standartlara uyarak görevi gerçekleştir

---

## **🏗️ 3. Django ERP Modül Yapısı ve Merkezi Konfigürasyon**

### **3.1. Context7 ERP Modül Organizasyonu**
```
Django Apps Structure:
├── 📊 Dashboard (ana kontrol paneli)
├── 👥 ERP System (8 departmental modules)
│   ├── Production (Üretim Yönetimi)
│   ├── Inventory (Envanter Yönetimi)
│   ├── Sales (Satış Yönetimi)
│   ├── Purchasing (Satın Alma Yönetimi)
│   ├── Quality (Kalite Yönetimi)
│   ├── Finance (Finans Yönetimi)
│   ├── HR (İnsan Kaynakları)
│   └── Reports (Raporlama)
├── 🔐 Core (güvenlik, kullanıcı yönetimi)
├── 📡 API (REST API endpoints)
└── 🎨 UI Framework (Glassmorphism components)
```

### **3.2. Merkezi Konfigürasyon Prensibi**
- **Django Settings**: Environment-based configuration (development, production)
- **ERP Configuration**: `core/erp_config.py` merkezi ERP ayarları
- **UI Configuration**: `static/js/context7-config.js` arayüz konfigürasyonu
- **Security Configuration**: `core/security_settings.py` güvenlik ayarları

---

## **🤖 4. AI Coder Rolleri ve Uzmanlık Alanları (Django ERP Context)**

### **4.1. Rol: 💻 Kodlayıcı (Django Developer AI)**

**Ana Hedef:** Django ERP sisteminin yeni özelliklerini ve fonksiyonlarını Context7 standartlarına uygun olarak geliştirmek.

**Sorumluluklar:**
- `[TYPE: CODING]` olarak etiketlenmiş görevleri üstlenir
- Django best practices, DRY, SOLID prensiplerini uygular
- Context7 Glassmorphism Framework ile modern UI geliştirir
- Django ORM kullanarak veritabanı işlemlerini optimize eder
- Django REST Framework ile API endpoint'lerini oluşturur
- Unit test'leri yazarak %80+ test coverage sağlar
- PEP8 ve Django coding standards'ına uyar

**Geliştirme Checklist:**
- [ ] Django models, views, templates, services oluştur
- [ ] Unit tests yaz (%80+ coverage)
- [ ] Django admin interface konfigure et
- [ ] API documentation güncelleçleştir
- [ ] Security best practices uygula
- [ ] Görevi 🧪 **TEST GEREKLİ** durumuna getir

### **4.2. Rol: 🐞 Hata Düzenleyici ve Test Uzmanı (QA & Testing AI)**

**Ana Hedef:** Django ERP sisteminin kararlılığını sağlamak, hataları tespit edip düzeltmek ve test süreçlerini yönetmek.

**Sorumluluklar:**
- `[TYPE: ERROR]` ve `[TYPE: TESTING]` görevlerini üstlenir
- ERR-[TYPE]-[YYMMDD]-[SEQUENCE] format'ı kullanarak hata takibi yapar
- Django test framework + Playwright ile comprehensive testing
- Performance monitoring ve bottleneck detection
- Security vulnerability assessment
- Code quality analysis ve improvement suggestions
- CI/CD pipeline monitoring

**Test & QA Checklist:**
- [ ] Django unit tests çalıştır
- [ ] Playwright E2E tests yaz ve çalıştır
- [ ] Security scan yap (Django security framework)
- [ ] Performance benchmark yap
- [ ] Code coverage analyze et
- [ ] Error handling test et

### **4.3. Rol: ✍️ Dokümantasyoncu ve Bilgi Yöneticisi (Documentation & Knowledge AI)**

**Ana Hedef:** Django ERP projesinin dokümantasyonunun güncel, tutarlı ve erişilebilir olmasını sağlamak. Context7 kolektif hafızasını yönetmek.

**Sorumluluklar:**
- `[TYPE: DOCUMENTATION]` görevlerini üstlenir
- Repository-specific rules güncellemeleri
- API documentation maintenance (Swagger/OpenAPI)
- User manual ve deployment guide'ları
- Knowledge base management (REC-[MODULE]-[YYMMDD]-[SEQUENCE])
- Code comment'leri ve docstring'leri
- Architecture documentation

**Dokümantasyon Checklist:**
- [ ] Repository rules güncelleştirildi mi?
- [ ] API endpoints documented mi?
- [ ] User manual güncel mi?
- [ ] Knowledge base'e experience record eklendi mi?
- [ ] Code adequately documented mi?

---

## **🔄 5. Django ERP İş Akışı ve Görev Yönetimi**

### **5.1. Görev Tanımlama ve Etiketleme Sistemi**

**Görev Türleri:**
- `[TYPE: CODING]` - Yeni özellik geliştirme, bug fix
- `[TYPE: ERROR]` - Hata çözümü, debugging
- `[TYPE: TESTING]` - Test yazımı, QA süreçleri
- `[TYPE: DOCUMENTATION]` - Dokümantasyon güncelleme
- `[TYPE: DEPLOYMENT]` - Deployment ve DevOps görevleri
- `[TYPE: SECURITY]` - Güvenlik iyileştirmeleri
- `[TYPE: PERFORMANCE]` - Performans optimizasyonu

**Öncelik Seviyeleri:**
- 🔥 **URGENT** - Production'ı etkileyen kritik hatalar
- ⚠️ **HIGH** - Ana fonksiyonları etkileyen önemli görevler
- 🔄 **MEDIUM** - Geliştirme sürecini iyileştiren görevler
- 🔵 **LOW** - Minor iyileştirmeler ve optimizasyonlar

### **5.2. Django ERP Geliştirme Döngüsü**

1. **Görev Seçimi:** AI Coder rolüne uygun etiketteki en öncelikli görevi seçer
2. **Protokol Uygulaması:** Bölüm 2.2'deki başvuru protokolünü uygular
3. **Geliştirme:** Django best practices ile development
4. **Test:** Comprehensive testing (unit + E2E)
5. **Documentation:** İlgili dökümanları güncelle
6. **Review:** Code review ve quality assurance
7. **Deploy:** Production deployment (if applicable)

---

## **🔗 6. Context7 ERP Entegrasyon Protokolleri**

### **6.1. Database Integration**
- **SQLite**: Development ve testing environment
- **PostgreSQL**: Production environment
- **Migration Strategy**: Django migrations ile version control
- **Backup Strategy**: Automated backup system

### **6.2. API Integration**
- **Django REST Framework**: RESTful API development
- **JWT Authentication**: Token-based authentication
- **API Versioning**: /api/v1/ pattern
- **Swagger Documentation**: Interactive API documentation

### **6.3. Frontend Integration**
- **Context7 Glassmorphism Framework**: Modern UI/UX
- **Progressive Enhancement**: Graceful degradation
- **Responsive Design**: Mobile-first approach
- **Performance Optimization**: Asset minification, caching

---

## **📊 7. Kalite Kontrol ve Metrikler**

### **7.1. Code Quality Metrics**
- **Test Coverage**: Minimum %80
- **Code Complexity**: Cyclomatik complexity < 10
- **Performance**: Response time < 400ms
- **Security**: Zero critical vulnerabilities
- **Documentation**: %100 API coverage

### **7.2. ERP Business Metrics**
- **System Uptime**: %99.9+
- **User Satisfaction**: %95+
- **Data Accuracy**: %99.9+
- **Processing Speed**: Real-time operations
- **Audit Compliance**: %100

---

**Protokol Mottosu:** "Modern Django ile Enterprise ERP. Context7 standardı ile kaliteli kod. Glassmorphism ile güzel arayüz. Kolektif öğrenme ile sürekli gelişim."

---

**🔄 Version:** v1.0 (Django ERP Adaptation)  
**📅 Son Güncelleme:** 9 Haziran 2025  
**🏷️ Durum:** Context7 Central Protocol Aktif ✅  
**🎯 Scope:** Django ERP System + Context7 Framework + Production Ready Standards 