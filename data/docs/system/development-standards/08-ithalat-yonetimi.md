# Context7 ERP - İthalat Yönetimi Modülü
**Modül Kodu:** IMPORT-MGT  
**Öncelik:** 3 - Orta  
**Tahmini Süre:** 3-4 hafta  
**Bağımlılıklar:** Finans, Stok Yönetimi, Muhasebe Sistemi  

---

## 📋 Modül Açıklaması

Kapsamlı ithalat süreç yönetimi; dosya takibi, dağıtım anahtarları, stok millileştirme, maliyet hesaplamaları ve gümrük işlemleri entegrasyonu içeren uluslararası ticaret çözümü.

---

## 🎯 Ana Özellikler

### **1. İthalat Dosyası Yönetimi**

#### **Import File Creation**
- **File Registration**
  - İthalat dosya numarası
  - Tedarikçi bilgileri
  - Sevkiyat detayları
  - Belge takibi

- **Documentation Management**
  - Proforma invoice
  - Commercial invoice
  - Packing list
  - Certificate of origin
  - Insurance documents

#### **Customs Documentation**
- **GTİP Classification**
  - Harmonized code assignment
  - Tariff calculations
  - Tax assessments
  - Duty calculations

- **Regulatory Compliance**
  - Import licenses
  - Quality certificates
  - Conformity assessments
  - Special authorizations

### **2. Dağıtım Anahtarları Sistemi**

#### **Cost Distribution Keys**
- **Distribution Methods**
  - Ağırlık bazlı dağılım
  - Değer bazlı dağılım
  - Hacim bazlı dağılım
  - Karma dağılım metodları

- **Cost Categories**
  - Ürün maliyeti (FOB)
  - Freight costs
  - Insurance premiums
  - Customs duties
  - Handling charges

#### **Allocation Rules**
- **Automatic Distribution**
  - Rule-based allocation
  - Proportional distribution
  - Manual adjustments
  - Exception handling

### **3. Stok Millileştirme İşlemleri**

#### **Naturalization Process**
- **Complete Naturalization**
  - Tam millileştirme süreci
  - Final cost calculation
  - Inventory value update
  - Accounting integration

- **Partial Naturalization**
  - Kısmi millileştirme
  - Interim cost updates
  - Phased processing
  - Progress tracking

#### **Cost Calculation Engine**
- **Automated Calculations**
  - Real-time cost updates
  - Multi-currency handling
  - Exchange rate impacts
  - Tax calculations

### **4. Gümrük İşlemleri Entegrasyonu**

#### **Customs Clearance**
- **Declaration Processing**
  - Electronic declarations
  - Document submission
  - Status tracking
  - Approval workflows

#### **Duty and Tax Management**
- **Tax Calculations**
  - Import duties
  - VAT calculations
  - Special consumption tax
  - Additional fees

### **5. Tedarikçi ve Kargo Yönetimi**

#### **International Supplier Management**
- **Supplier Profiles**
  - International credentials
  - Payment terms
  - Incoterms preferences
  - Quality certifications

#### **Shipping Management**
- **Freight Coordination**
  - Shipping schedules
  - Container tracking
  - Port operations
  - Delivery coordination

---

## 🗄️ Database Models

### **1. ImportFile (İthalat Dosyası)**
```python
class ImportFile(models.Model):
    file_number = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey('procurement.Supplier', on_delete=models.CASCADE)
    purchase_order = models.ForeignKey('procurement.PurchaseOrder', on_delete=models.CASCADE)
    incoterm = models.CharField(max_length=10, choices=INCOTERM_CHOICES)
    origin_country = models.CharField(max_length=50)
    destination_port = models.CharField(max_length=100)
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHOD_CHOICES)
    estimated_arrival = models.DateField()
    actual_arrival = models.DateField(null=True, blank=True)
    total_fob_value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    freight_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    insurance_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cif_value = models.DecimalField(max_digits=15, decimal_places=2)
    customs_duty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    customs_duty_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_landed_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=IMPORT_STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **2. ImportItem (İthalat Ürünü)**
```python
class ImportItem(models.Model):
    import_file = models.ForeignKey(ImportFile, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=3)
    unit_price_fob = models.DecimalField(max_digits=12, decimal_places=4)
    total_fob_value = models.DecimalField(max_digits=15, decimal_places=2)
    gtip_code = models.CharField(max_length=12)
    country_of_origin = models.CharField(max_length=50)
    weight_gross = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    weight_net = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    volume = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    package_count = models.IntegerField(default=1)
    package_type = models.CharField(max_length=20, blank=True)
    allocated_freight = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allocated_insurance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allocated_duty = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allocated_vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allocated_other = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_landed_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    total_landed_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    is_naturalized = models.BooleanField(default=False)
    naturalization_date = models.DateField(null=True, blank=True)
```

### **3. DistributionKey (Dağıtım Anahtarı)**
```python
class DistributionKey(models.Model):
    key_name = models.CharField(max_length=100)
    key_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    distribution_method = models.CharField(max_length=20, choices=DISTRIBUTION_METHOD_CHOICES)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **4. CostAllocation (Maliyet Dağılımı)**
```python
class CostAllocation(models.Model):
    import_file = models.ForeignKey(ImportFile, on_delete=models.CASCADE)
    cost_type = models.CharField(max_length=20, choices=COST_TYPE_CHOICES)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    distribution_key = models.ForeignKey(DistributionKey, on_delete=models.CASCADE)
    allocation_method = models.CharField(max_length=20, choices=ALLOCATION_METHOD_CHOICES)
    is_allocated = models.BooleanField(default=False)
    allocation_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
```

### **5. CustomsDeclaration (Gümrük Beyannamesi)**
```python
class CustomsDeclaration(models.Model):
    declaration_number = models.CharField(max_length=30, unique=True)
    import_file = models.OneToOneField(ImportFile, on_delete=models.CASCADE)
    declaration_type = models.CharField(max_length=10, choices=DECLARATION_TYPE_CHOICES)
    declaration_date = models.DateField()
    customs_office = models.CharField(max_length=100)
    declarant = models.CharField(max_length=200)
    tax_identification = models.CharField(max_length=20)
    total_packages = models.IntegerField()
    total_gross_weight = models.DecimalField(max_digits=12, decimal_places=3)
    total_net_weight = models.DecimalField(max_digits=12, decimal_places=3)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=DECLARATION_STATUS_CHOICES)
    clearance_date = models.DateField(null=True, blank=True)
    examination_required = models.BooleanField(default=False)
    examination_date = models.DateField(null=True, blank=True)
    customs_officer = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
```

### **6. ShippingDocument (Sevkiyat Belgesi)**
```python
class ShippingDocument(models.Model):
    import_file = models.ForeignKey(ImportFile, on_delete=models.CASCADE, related_name='shipping_documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    document_number = models.CharField(max_length=50)
    document_date = models.DateField()
    issuer = models.CharField(max_length=200)
    file_path = models.FileField(upload_to='import_documents/', blank=True)
    is_original = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **7. ImportLicense (İthalat Lisansı)**
```python
class ImportLicense(models.Model):
    license_number = models.CharField(max_length=30, unique=True)
    import_file = models.ForeignKey(ImportFile, on_delete=models.CASCADE)
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPE_CHOICES)
    issuing_authority = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    permitted_quantity = models.DecimalField(max_digits=15, decimal_places=3)
    utilized_quantity = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    remaining_quantity = models.DecimalField(max_digits=15, decimal_places=3)
    product_description = models.TextField()
    restrictions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LICENSE_STATUS_CHOICES)
    is_transferable = models.BooleanField(default=False)
```

### **8. ExchangeRateSnapshot (Kur Anlık Durumu)**
```python
class ExchangeRateSnapshot(models.Model):
    import_file = models.ForeignKey(ImportFile, on_delete=models.CASCADE)
    currency_from = models.CharField(max_length=3)
    currency_to = models.CharField(max_length=3, default='TRY')
    rate_date = models.DateField()
    official_rate = models.DecimalField(max_digits=15, decimal_places=6)
    applied_rate = models.DecimalField(max_digits=15, decimal_places=6)
    rate_source = models.CharField(max_length=50, default='TCMB')
    snapshot_reason = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **9. ImportExpense (İthalat Gideri)**
```python
class ImportExpense(models.Model):
    import_file = models.ForeignKey(ImportFile, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPE_CHOICES)
    expense_category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    amount_in_base_currency = models.DecimalField(max_digits=12, decimal_places=2)
    vendor = models.CharField(max_length=200, blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    is_allocated = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
```

---

## 🔧 API Endpoints

### **Import File Management APIs**
```
GET    /api/v1/import/files/                     # İthalat dosyası listesi
POST   /api/v1/import/files/                     # Yeni ithalat dosyası
GET    /api/v1/import/files/{id}/                # İthalat dosyası detayı
PUT    /api/v1/import/files/{id}/                # İthalat dosyası güncelleme
POST   /api/v1/import/files/{id}/finalize/       # Dosya sonlandırma
```

### **Cost Distribution APIs**
```
GET    /api/v1/import/distribution-keys/         # Dağıtım anahtarları
POST   /api/v1/import/distribution-keys/         # Yeni dağıtım anahtarı
POST   /api/v1/import/files/{id}/allocate-costs/ # Maliyet dağılımı
GET    /api/v1/import/files/{id}/cost-breakdown/ # Maliyet kırılımı
```

### **Naturalization APIs**
```
POST   /api/v1/import/files/{id}/naturalize/     # Stok millileştirme
GET    /api/v1/import/naturalization-status/     # Millileştirme durumu
POST   /api/v1/import/files/{id}/partial-naturalize/ # Kısmi millileştirme
```

### **Customs Integration APIs**
```
GET    /api/v1/import/customs-declarations/      # Gümrük beyannameleri
POST   /api/v1/import/customs-declarations/      # Yeni beyanname
GET    /api/v1/import/gtip-codes/                # GTİP kodları
GET    /api/v1/import/duty-rates/                # Gümrük vergisi oranları
```

### **Documentation APIs**
```
GET    /api/v1/import/files/{id}/documents/      # Belge listesi
POST   /api/v1/import/files/{id}/documents/      # Belge yükleme
GET    /api/v1/import/licenses/                  # İthalat lisansları
POST   /api/v1/import/licenses/                  # Yeni lisans
```

---

## 🎨 UI/UX Gereksinimleri

### **Import Dashboard**
- Active import files
- Pending clearances
- Cost summaries
- Timeline tracking

### **File Management Interface**
- Import wizard
- Document upload
- Cost allocation tools
- Status tracking

### **Cost Distribution Interface**
- Visual allocation tools
- Cost breakdown charts
- Distribution key management
- Adjustment capabilities

### **Customs Integration**
- Declaration forms
- Status tracking
- Document verification
- Compliance monitoring

---

## 🚀 Implementation Plan

### **Phase 1: Core Import Management (2 hafta)**
- Import file creation
- Basic document management
- Product registration
- Status tracking

### **Phase 2: Cost Management (1 hafta)**
- Distribution keys
- Cost allocation
- Calculation engine
- Reporting tools

### **Phase 3: Naturalization (1 hafta)**
- Naturalization process
- Inventory integration
- Cost finalization
- Accounting updates

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 