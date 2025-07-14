# 🚀 Context7 ERP Sistemi - Gelişmiş Geliştirme Standartları ve Mimari

Bu belge, Context7 ERP projesinde uygulanacak olan geliştirme, dökümantasyon, test ve yönetim süreçlerine yönelik gelişmiş standartları ve sistemin detaylı mimari yapısını tanımlar.

## 📋 İçindekiler
1. [Proje Dökümantasyonu ve Haritalama](#1-proje-dökümantasyonu-ve-haritalama)
2. [Veritabanı Yönetim Standartları](#2-veritabanı-yönetim-standartları)
3. [Kod Geliştirme Standartları](#3-kod-geliştirme-standartları)
4. [Bağımlılık ve Dağıtım Yönetimi](#4-bağımlılık-ve-dağıtım-yönetimi)
5. [Güvenlik Standartları](#5-güvenlik-standartları)
6. [Performans ve Ölçeklenebilirlik](#6-performans-ve-ölçeklenebilirlik)
7. [Uygulama Mimarisi ve Veri Yapısı](#7-uygulama-mimarisi-ve-veri-yapısı)
8. [Birimler Arası Bilgi Akışı](#8-birimler-arası-bilgi-akışı)
9. [API Tasarım Standartları](#9-api-tasarım-standartları)
10. [Test Stratejileri](#10-test-stratejileri)
11. [Deployment ve DevOps](#11-deployment-ve-devops)
12. [Monitoring ve Logging](#12-monitoring-ve-logging)

---

## 1. Proje Dökümantasyonu ve Haritalama

### 1.1. Dosya Haritası (filemap.md)
**Kural:** Proje dizin yapısındaki her dosya ve klasörün amacı, sorumluluğu ve projedeki rolü net şekilde açıklanmalıdır.

**Uygulama:**
```markdown
# Context7 Dosya Haritası
├── apps/                    # Django uygulamaları
│   ├── authentication/     # Kullanıcı kimlik doğrulama
│   ├── customers/          # Müşteri yönetimi
│   ├── suppliers/          # Tedarikçi yönetimi
│   ├── products/           # Ürün katalogu
│   ├── inventory/          # Stok yönetimi
│   ├── sales/              # Satış süreçleri
│   ├── procurement/        # Satın alma
│   ├── production/         # Üretim yönetimi
│   ├── finance/            # Finans ve muhasebe
│   ├── hr/                 # İnsan kaynakları
│   └── reporting/          # Raporlama ve analitik
├── core/                   # Temel sistem bileşenleri
├── static/                 # Statik dosyalar (CSS, JS, img)
├── templates/              # HTML şablonları
├── tests/                  # Test dosyaları
├── docs/                   # Dokümantasyon
└── requirements/           # Bağımlılık dosyaları
```

### 1.2. Site Haritası (sitemap.xml)
**Kural:** SEO standartlarına uygun dinamik site haritası oluşturulmalı.

**Uygulama:**
- Django sitemap framework kullanılmalı
- Her modül için ayrı sitemap sınıfı oluşturulmalı
- Güncellenme sıklığı ve öncelik değerleri belirlenmeli

### 1.3. API Dokümantasyonu
**Kural:** Tüm API endpoint'leri OpenAPI 3.0 standardında dokümante edilmeli.

**Uygulama:**
- Django REST Framework + drf-spectacular kullanılmalı
- Otomatik Swagger UI oluşturulmalı
- Örnek istekler ve yanıtlar dahil edilmeli

---

## 2. Veritabanı Yönetim Standartları

### 2.1. Model Tasarım Prensipleri
**Kural:** Veritabanı modelleri SOLID prensiplere uygun tasarlanmalı.

**Uygulama:**
```python
# Temel Abstract Model
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
```

### 2.2. Veritabanı İndeksleme Stratejisi
**Kural:** Performans kritik alanlar için uygun indeksler oluşturulmalı.

**Uygulama:**
- Arama sık yapılan alanlar: `db_index=True`
- Composite indeksler: `indexes = [models.Index(fields=['field1', 'field2'])]`
- Unique constraint'ler: `unique_together` veya `UniqueConstraint`

### 2.3. Migration Yönetimi
**Kural:** Veritabanı değişiklikleri güvenli ve geri dönülebilir olmalı.

**Uygulama:**
- Her migration için rollback scripti hazırlanmalı
- Data migration'lar ayrı dosyalarda tutulmalı
- Production deployment öncesi staging'de test edilmeli

---

## 3. Kod Geliştirme Standartları

### 3.1. Python ve Django Standartları
**Kural:** PEP 8 ve Django best practices'e uyulmalı.

**Uygulama:**
```python
# Kod kalite araçları
- black (kod formatlama)
- isort (import sıralama)
- flake8 (linting)
- mypy (type checking)
- bandit (güvenlik)
```

### 3.2. Clean Architecture Uygulama
**Kural:** Business logic, framework'den bağımsız tutulmalı.

**Uygulama:**
```
apps/customers/
├── models.py           # Django modelleri
├── serializers.py      # API serializers
├── views.py           # API views
├── services.py        # Business logic
├── repositories.py    # Data access layer
└── validators.py      # Custom validators
```

### 3.3. Error Handling Standartları
**Kural:** Hata yönetimi tutarlı ve kapsamlı olmalı.

**Uygulama:**
```python
# Custom Exception Classes
class Context7Exception(Exception):
    """Base exception for Context7"""
    pass

class ValidationError(Context7Exception):
    """Validation errors"""
    pass

class BusinessRuleViolation(Context7Exception):
    """Business rule violations"""
    pass
```

---

## 4. Bağımlılık ve Dağıtım Yönetimi

### 4.1. Dependency Management
**Kural:** Bağımlılıklar çevre bazlı yönetilmeli.

**Uygulama:**
```
requirements/
├── base.txt        # Temel bağımlılıklar
├── local.txt       # Geliştirme ortamı
├── staging.txt     # Test ortamı
└── production.txt  # Üretim ortamı
```

### 4.2. Environment Configuration
**Kural:** Konfigürasyon bilgileri environment variables ile yönetilmeli.

**Uygulama:**
- django-environ kullanılmalı
- .env.example dosyası sağlanmalı
- Hassas bilgiler version control'e commit edilmemeli

---

## 5. Güvenlik Standartları

### 5.1. Authentication & Authorization
**Kural:** JWT tabanlı authentication kullanılmalı.

**Uygulama:**
```python
# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 5.2. Permission System
**Kural:** Granular izin sistemi uygulanmalı.

**Uygulama:**
```python
# Custom Permissions
class CanViewCustomers(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('customers.view_customer')
        
class CanManageOwnCustomers(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
```

### 5.3. Data Encryption
**Kural:** Hassas veriler şifrelenerek saklanmalı.

**Uygulama:**
- django-cryptography kullanılmalı
- PII veriler için field-level encryption
- Database backup'ları şifreli olmalı

---

## 6. Performans ve Ölçeklenebilirlik

### 6.1. Caching Strategy
**Kural:** Çok katmanlı cache stratejisi uygulanmalı.

**Uygulama:**
```python
# Cache Layers
1. Database Query Cache (Redis)
2. Template Fragment Cache
3. API Response Cache
4. Static File Cache (CDN)
```

### 6.2. Database Optimization
**Kural:** Veritabanı performansı sürekli izlenmeli.

**Uygulama:**
- select_related ve prefetch_related kullanımı
- N+1 query problemlerinin önlenmesi
- Database connection pooling
- Read replica kullanımı

### 6.3. Asynchronous Processing
**Kural:** Uzun süren işlemler asenkron yapılmalı.

**Uygulama:**
```python
# Celery Task Configuration
@shared_task
def process_bulk_invoice():
    # Bulk operations
    pass

@shared_task
def send_notification_email():
    # Email sending
    pass
```

---

## 7. Uygulama Mimarisi ve Veri Yapısı

### 7.1. Modüler Mimari
**Kural:** Her iş domain'i ayrı Django app olarak organize edilmeli.

### 7.2. Detaylı Veri Modelleri

#### 7.2.1. Müşteri Yönetimi Modülleri
```python
class Customer(BaseModel):
    """Ana müşteri modeli"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CUSTOMER_CATEGORIES)
    type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    tax_office = models.CharField(max_length=100)
    tax_number = models.CharField(max_length=20)
    trade_registry_number = models.CharField(max_length=30, blank=True)
    mersis_number = models.CharField(max_length=20, blank=True)
    
class CustomerAddress(BaseModel):
    """Müşteri adres bilgileri"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    street_address = models.TextField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='Turkey')
    
class CustomerContact(BaseModel):
    """Müşteri iletişim bilgileri"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES)
    value = models.CharField(max_length=200)
    is_primary = models.BooleanField(default=False)
```

#### 7.2.2. Ürün Yönetimi Modülleri
```python
class ProductCategory(BaseModel):
    """Ürün kategorileri"""
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)
    
class Product(BaseModel):
    """Ana ürün modeli"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    unit = models.CharField(max_length=10, choices=UNITS)
    barcode = models.CharField(max_length=50, blank=True)
    gtip_code = models.CharField(max_length=20, blank=True)
    
class ProductSpecification(BaseModel):
    """Ürün teknik özellikleri"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification_name = models.CharField(max_length=100)
    specification_value = models.CharField(max_length=200)
    
class ProductPricing(BaseModel):
    """Ürün fiyatlandırma"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_list = models.ForeignKey('PriceList', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
```

#### 7.2.3. Stok Yönetimi Modülleri
```python
class Warehouse(BaseModel):
    """Depo tanımları"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    warehouse_type = models.CharField(max_length=20, choices=WAREHOUSE_TYPES)
    address = models.TextField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    responsible_person = models.ForeignKey(User, on_delete=models.PROTECT)
    
class WarehouseLocation(BaseModel):
    """Depo lokasyonları (raf sistemi)"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    code = models.CharField(max_length=30)
    aisle = models.CharField(max_length=10)
    rack = models.CharField(max_length=10)
    level = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    
class StockMovement(BaseModel):
    """Stok hareketleri"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    location = models.ForeignKey(WarehouseLocation, on_delete=models.PROTECT, null=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    reference_document = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    unit_cost = models.DecimalField(max_digits=15, decimal_places=4, null=True)
    lot_number = models.CharField(max_length=50, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
```

#### 7.2.4. Satış Yönetimi Modülleri
```python
class SalesQuotation(BaseModel):
    """Satış teklifleri"""
    quotation_number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    quotation_date = models.DateField()
    valid_until = models.DateField()
    status = models.CharField(max_length=20, choices=QUOTATION_STATUS)
    customer_reference = models.CharField(max_length=100, blank=True)
    delivery_terms = models.TextField(blank=True)
    payment_terms = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
class SalesOrder(BaseModel):
    """Satış siparişleri"""
    order_number = models.CharField(max_length=30, unique=True)
    quotation = models.ForeignKey(SalesQuotation, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS)
    customer_order_number = models.CharField(max_length=100, blank=True)
    shipping_address = models.ForeignKey(CustomerAddress, on_delete=models.PROTECT)
    
class SalesOrderItem(BaseModel):
    """Satış sipariş kalemleri"""
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    unit_price = models.DecimalField(max_digits=15, decimal_places=4)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    delivered_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
```

#### 7.2.5. Satın Alma Modülleri
```python
class PurchaseRequest(BaseModel):
    """Satın alma talepleri"""
    request_number = models.CharField(max_length=30, unique=True)
    requesting_department = models.CharField(max_length=100)
    requester = models.ForeignKey(User, on_delete=models.PROTECT)
    request_date = models.DateField()
    required_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS)
    justification = models.TextField()
    
class RFQ(BaseModel):
    """Teklif isteme (Request for Quotation)"""
    rfq_number = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_date = models.DateField()
    response_deadline = models.DateField()
    status = models.CharField(max_length=20, choices=RFQ_STATUS)
    technical_specifications = models.TextField(blank=True)
    
class PurchaseOrder(BaseModel):
    """Satın alma siparişleri"""
    order_number = models.CharField(max_length=30, unique=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT)
    order_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=PO_STATUS)
    incoterms = models.CharField(max_length=10, choices=INCOTERMS)
    payment_terms = models.TextField()
    
class GoodsReceipt(BaseModel):
    """Mal kabul"""
    receipt_number = models.CharField(max_length=30, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    delivery_note_number = models.CharField(max_length=50)
    receipt_date = models.DateField()
    received_by = models.ForeignKey(User, on_delete=models.PROTECT)
    quality_check_status = models.CharField(max_length=20, choices=QC_STATUS)
```

#### 7.2.6. Üretim Yönetimi Modülleri
```python
class BillOfMaterials(BaseModel):
    """Ürün reçeteleri (BOM)"""
    bom_code = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version = models.CharField(max_length=10)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=BOM_STATUS)
    
class BOMComponent(BaseModel):
    """Reçete bileşenleri"""
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE)
    component = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    unit = models.CharField(max_length=10)
    scrap_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_alternative = models.BooleanField(default=False)
    
class ProductionOrder(BaseModel):
    """Üretim emirleri"""
    order_number = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.PROTECT)
    planned_quantity = models.DecimalField(max_digits=15, decimal_places=4)
    produced_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCTION_STATUS)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    
class WorkOrder(BaseModel):
    """İş emirleri"""
    work_order_number = models.CharField(max_length=30, unique=True)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE)
    operation_code = models.CharField(max_length=20)
    operation_name = models.CharField(max_length=100)
    work_center = models.ForeignKey('WorkCenter', on_delete=models.PROTECT)
    planned_duration = models.DurationField()
    actual_duration = models.DurationField(null=True, blank=True)
    operator = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=20, choices=WORK_ORDER_STATUS)
```

#### 7.2.7. Kalite Kontrol Modülleri
```python
class QualityControlPlan(BaseModel):
    """Kalite kontrol planları"""
    plan_code = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    control_point = models.CharField(max_length=50, choices=CONTROL_POINTS)
    sampling_plan = models.TextField()
    acceptance_criteria = models.TextField()
    
class QualityInspection(BaseModel):
    """Kalite muayene kayıtları"""
    inspection_number = models.CharField(max_length=30, unique=True)
    qc_plan = models.ForeignKey(QualityControlPlan, on_delete=models.PROTECT)
    inspection_date = models.DateField()
    inspector = models.ForeignKey(User, on_delete=models.PROTECT)
    batch_lot_number = models.CharField(max_length=50)
    sample_size = models.PositiveIntegerField()
    result = models.CharField(max_length=20, choices=INSPECTION_RESULTS)
    notes = models.TextField(blank=True)
    
class QualityDefect(BaseModel):
    """Kalite kusur kayıtları"""
    inspection = models.ForeignKey(QualityInspection, on_delete=models.CASCADE)
    defect_type = models.CharField(max_length=100)
    defect_count = models.PositiveIntegerField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    corrective_action = models.TextField(blank=True)
```

#### 7.2.8. İnsan Kaynakları Modülleri
```python
class Employee(BaseModel):
    """Personel bilgileri"""
    employee_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    
class EmploymentInfo(BaseModel):
    """İstihdam bilgileri"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.PROTECT)
    position = models.ForeignKey('Position', on_delete=models.PROTECT)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    social_security_number = models.CharField(max_length=20, unique=True)
    
class LeaveRequest(BaseModel):
    """İzin talepleri"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    days_count = models.PositiveIntegerField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LEAVE_STATUS)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    approved_date = models.DateField(null=True, blank=True)
```

#### 7.2.9. Finans ve Muhasebe Modülleri
```python
class Invoice(BaseModel):
    """Fatura bilgileri"""
    invoice_number = models.CharField(max_length=30, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, null=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    e_invoice_uuid = models.UUIDField(null=True, blank=True)
    e_archive_number = models.CharField(max_length=50, blank=True)
    
class Payment(BaseModel):
    """Ödeme kayıtları"""
    payment_number = models.CharField(max_length=30, unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    bank_account = models.ForeignKey('BankAccount', on_delete=models.PROTECT, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
class CheckPromissoryNote(BaseModel):
    """Çek/Senet takibi"""
    document_type = models.CharField(max_length=10, choices=[('CHECK', 'Çek'), ('NOTE', 'Senet')])
    document_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    due_date = models.DateField()
    bank = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50