# Context7 ERP System - Database Documentation

**Versiyon:** v2.2.0-glassmorphism-enhanced + QMS Integration + Modern Python Standards + SSL Implementation + Email System ⭐  
**Son Güncelleme:** 13 Temmuz 2025  
**Veritabanı:** SQLite (1,088 kayıt, 73 tablo) + PostgreSQL Hazır  
**Durum:** Production Ready (100% Complete)

## 📋 Genel Bakış

Context7 ERP sistemi, modern işletme ihtiyaçlarını karşılayan kapsamlı veritabanı yapısına sahiptir. Sistem, 8 ana departmanı destekleyen 73 tablo içermektedir.

### Ana Özellikler:
- **UUID Primary Keys**: Güvenlik ve ölçeklenebilirlik
- **Multi-Company Support**: Çoklu şirket desteği  
- **Audit Trail**: Tüm değişikliklerin takibi
- **Soft Delete**: Veri kaybını önleyen yumuşak silme
- **User Tracking**: Oluşturan/güncelleyen kullanıcı takibi

## 🏗️ Temel Modeller

### Context7BaseModel
Tüm modellerin temel sınıfı, ortak özellikleri sağlar.

```python
class Context7BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
```

## 🏢 ERP Modül Yapısı

### 1. Organizasyon Modülleri

#### Company (Şirket)
```python
class Company(Context7BaseModel):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    tax_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Turkey')
    default_currency = models.CharField(max_length=3, default='TRY')
    fiscal_year_start = models.DateField()
```

#### Department (Departman)
```python
class Department(Context7BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey('Employee', on_delete=models.SET_NULL, null=True)
```

#### Role (Rol)
```python
class Role(Context7BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    permissions = models.ManyToManyField('Permission', blank=True)
```

### 2. İnsan Kaynakları Modülleri

#### Employee (Çalışan)
```python
class Employee(Context7BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    hire_date = models.DateField(null=True)
    employee_code = models.CharField(max_length=20, unique=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
```

#### LeaveRequest (İzin Talebi)
```python
class LeaveRequest(Context7BaseModel):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

#### PayrollRecord (Bordro Kaydı)
```python
class PayrollRecord(Context7BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)
```

### 3. İş Süreçleri Modülleri

#### Customer (Müşteri)
```python
class Customer(Context7BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    tax_number = models.CharField(max_length=20, unique=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    customer_type = models.CharField(max_length=20, choices=[("individual", "Individual"), ("corporate", "Corporate")])
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_terms_days = models.PositiveIntegerField(default=0)
```

#### Product (Ürün)
```python
class Product(Context7BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
```

#### ProductCategory (Ürün Kategorisi)
```python
class ProductCategory(Context7BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
```

### 4. Satış Modülleri

#### SalesOrder (Satış Siparişi)
```python
class SalesOrder(Context7BaseModel):
    STATUS_CHOICES = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('shipped', 'Shipped'), ('delivered', 'Delivered')]
    
    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateField()
    delivery_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)
```

#### SalesOrderItem (Satış Sipariş Kalemi)
```python
class SalesOrderItem(Context7BaseModel):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
```

### 5. Satın Alma Modülleri

#### Supplier (Tedarikçi)
```python
class Supplier(Context7BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    tax_number = models.CharField(max_length=20, unique=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    payment_terms_days = models.PositiveIntegerField(default=30)
```

#### PurchaseOrder (Satın Alma Siparişi)
```python
class PurchaseOrder(Context7BaseModel):
    STATUS_CHOICES = [('draft', 'Draft'), ('sent', 'Sent'), ('received', 'Received'), ('invoiced', 'Invoiced')]
    
    order_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    order_date = models.DateField()
    expected_delivery_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
```

### 6. Stok Modülleri

#### Warehouse (Depo)
```python
class Warehouse(Context7BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=200, blank=True)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
```

#### StockTransaction (Stok Hareketi)
```python
class StockTransaction(Context7BaseModel):
    TRANSACTION_TYPES = [('in', 'Stock In'), ('out', 'Stock Out'), ('transfer', 'Transfer')]
    
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reference_document = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
```

### 7. Üretim Modülleri

#### ProductionOrder (Üretim Emri)
```python
class ProductionOrder(Context7BaseModel):
    STATUS_CHOICES = [('planned', 'Planned'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    
    order_number = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
```

#### QualityControl (Kalite Kontrol)
```python
class QualityControl(Context7BaseModel):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, null=True)
    control_date = models.DateField()
    control_type = models.CharField(max_length=50)
    results = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
```

### 8. Muhasebe Modülleri

#### Account (Hesap)
```python
class Account(Context7BaseModel):
    ACCOUNT_TYPES = [('asset', 'Asset'), ('liability', 'Liability'), ('equity', 'Equity'), ('revenue', 'Revenue'), ('expense', 'Expense')]
    
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

#### Invoice (Fatura)
```python
class Invoice(Context7BaseModel):
    STATUS_CHOICES = [('draft', 'Draft'), ('sent', 'Sent'), ('paid', 'Paid'), ('overdue', 'Overdue')]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    invoice_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
```

#### Payment (Ödeme)
```python
class Payment(Context7BaseModel):
    PAYMENT_TYPES = [('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'), ('credit_card', 'Credit Card')]
    
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    reference = models.CharField(max_length=100, blank=True)
```

## 📊 Veri İstatistikleri

### Tablo Sayıları
- **Toplam Tablo**: 73
- **Ana Modüller**: 8
- **Audit Tabloları**: 12
- **Lookup Tabloları**: 15
- **İlişkisel Tablolar**: 18

### Kayıt Sayıları (Örnek Veriler)
- **Ürünler**: 150+ kayıt
- **Müşteriler**: 85+ kayıt
- **Tedarikçiler**: 42+ kayıt
- **Çalışanlar**: 25+ kayıt
- **Stok Hareketleri**: 500+ kayıt
- **Satış Siparişleri**: 200+ kayıt

## 🔧 Veritabanı Ayarları

### SQLite Konfigürasyonu
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        }
    }
}
```

### PostgreSQL Konfigürasyonu (Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'context7_erp',
        'USER': 'context7_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
        }
    }
}
```

## 🛠️ Maintenance & Backup

### Backup Stratejisi
- **Daily Backup**: Otomatik günlük yedek
- **Weekly Full Backup**: Haftalık tam yedek
- **Monthly Archive**: Aylık arşiv
- **Backup Verification**: Yedek doğrulama

### Performance Optimizasyonu
- **Database Indexing**: Optimize edilmiş indeksler
- **Query Optimization**: Sorgu optimizasyonu
- **Connection Pooling**: Bağlantı havuzu
- **Caching Strategy**: Önbellek stratejisi

---

**📅 Son Güncelleme:** 9 Ocak 2025  
**📊 Optimizasyon:** 957 → 300 satır (%69 azalma)  
**🎯 Odak:** Essential model definitions ve core schema  
**📝 Durum:** Optimize edildi - gereksiz detaylar kaldırıldı 