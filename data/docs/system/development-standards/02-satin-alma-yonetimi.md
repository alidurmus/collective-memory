# Context7 ERP - Satın Alma Yönetimi Modülü
**Modül Kodu:** PROCUREMENT  
**Öncelik:** 1 - Kritik  
**Tahmini Süre:** 5-7 hafta  
**Bağımlılıklar:** Stok Yönetimi, Finansal Modül, Tedarikçi Yönetimi  

---

## 📋 Modül Açıklaması

Uçtan uca satın alma süreci yönetimi; teklif değerlendirmesi, otomatik satın alma, mal kabul sistemi ve masraf yönetimini içeren kapsamlı tedarik zinciri çözümü.

---

## 🎯 Ana Özellikler

### **1. RFQ (Request for Quotation) - Teklif Yönetimi**

#### **RFQ Creation Workflow**
- **Gereksinim Tanımlama**
  - Teknik spesifikasyonlar
  - Miktar gereksinimleri
  - Kalite standartları
  - Teslimat şartları
  - Ödeme koşulları

- **Tedarikçi Davet Sistemi**
  - Tedarikçi veritabanı
  - Yetenek eşleştirme
  - Otomatik davet gönderimi
  - Davet takip sistemi

#### **Quote Evaluation Matrix**
- **Değerlendirme Kriterleri**
  - Fiyat skoru (40%)
  - Kalite skoru (30%)
  - Teslimat skoru (20%)
  - Servis skoru (10%)

- **Scoring System**
  - Ağırlıklı puanlama
  - Objektif değerlendirme
  - Karşılaştırma matrisi
  - Otomatik sıralama

#### **Award Decision Process**
- Karar kriterleri
- Gerekçe notları
- Onay süreci
- Sözleşme oluşturma

### **2. Otomatik Satın Alma Sistemi**

#### **Auto-Reorder Rules**
- **Tetikleme Koşulları**
  - Minimum stok seviyesi
  - Yeniden sipariş noktası
  - Tahmini tükenme tarihi
  - Mevsimsel faktörler

- **Tedarikçi Seçimi**
  - Tercihli tedarikçi listesi
  - Performans geçmişi
  - Fiyat karşılaştırması
  - Teslimat süresi analizi

#### **Purchase Requisition Workflow**
- **Talep Süreci**
  - Departman talepleri
  - Bütçe doğrulaması
  - Onay zinciri
  - Otorizasyon limitleri

- **Approval Chain**
  - Departman onayı
  - Bütçe onayı
  - Genel müdür onayı
  - Mali işler onayı

#### **Supplier Performance Tracking**
- **Performans Metrikleri**
  - Teslimat performansı
  - Kalite derecelendirmeleri
  - Fiyat rekabetçiliği
  - Servis kalitesi

- **Automated Ratings**
  - Otomatik puan hesaplama
  - Performans trendleri
  - Uyarı sistemleri
  - Blacklist yönetimi

### **3. Purchase Order Management**

#### **PO Generation**
- Otomatik PO oluşturma
- Şablon kullanımı
- Özelleştirilebilir formatlar
- Çoklu para birimi desteği

#### **Supplier Notification**
- Otomatik email gönderimi
- PDF ekleri
- Onay talepleri
- Teslimat planlaması

#### **Delivery Scheduling**
- Teslimat takvimi
- Kapasite planlaması
- Rota optimizasyonu
- GPS takip entegrasyonu

### **4. Masraf Faturası ve Müstahsil Yönetimi**

#### **Expense Categories**
- **Kategori Tanımları**
  - Seyahat masrafları
  - Kamu hizmetleri
  - Profesyonel hizmetler
  - Ofis malzemeleri
  - Bakım ve onarım

#### **Producer Receipt (Müstahsil) Handling**
- **Çiftçi Bilgileri**
  - Üretici kayıt sistemi
  - Vergi numarası
  - İletişim bilgileri
  - Ürün yetkileri

- **Tax Calculations**
  - KDV hesaplamaları
  - Stopaj hesaplamaları
  - Muhtasar beyanname
  - E-beyanname entegrasyonu

#### **3-Way Matching**
- **Document Matching**
  - PO vs Fatura eşleştirme
  - Makbuz vs Fatura kontrol
  - Miktar doğrulaması
  - Fiyat uyum kontrolü

- **Discrepancy Handling**
  - Uyumsuzluk raporlama
  - Çözüm süreçleri
  - Escalation rules
  - Onay mekanizmaları

#### **Approval Workflow**
- **Onay Seviyeleri**
  - Departman seviyesi
  - Bütçe kontrolü
  - Otorizasyon limitleri
  - Mali onay

### **5. Mal Kabul Sistemi**

#### **Quality Inspection at Receipt**
- **Kalite Kontrol Listeleri**
  - Görsel muayene
  - Teknik testler
  - Belge kontrolü
  - Kalite sertifikaları

- **Quality Ratings**
  - Kalite puanlaması
  - Kabul/ret kriterleri
  - Non-conformance raporları
  - Corrective actions

#### **Quantity Verification**
- **Miktar Kontrolü**
  - Sipariş vs teslimat
  - Eksik teslimat işleme
  - Fazla teslimat yönetimi
  - Kısmi teslimat kabul

#### **Barcode/QR Scanning**
- **Batch Scanning**
  - Toplu tarama sistemi
  - Seri numarası yakalama
  - Lokasyon ataması
  - Etiket bastırma

#### **Automatic Inventory Update**
- Stok düzeltmesi
- Lokasyon ataması
- Maliyet dağılımı
- Finansal entegrasyon

### **6. Vendor Management**

#### **Vendor Database**
- Tedarikçi profilleri
- Yetenek matrisi
- Sertifikalar
- Performans geçmişi

#### **Vendor Assessment**
- Periyodik değerlendirmeler
- Audit sonuçları
- Risk değerlendirmesi
- Development plans

---

## 🗄️ Database Models

### **1. PurchaseRequisition (Satın Alma Talebi)**
```python
class PurchaseRequisition(models.Model):
    requisition_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    required_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=REQ_STATUS_CHOICES)
    total_budget = models.DecimalField(max_digits=15, decimal_places=2)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_requisitions')
    approval_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
```

### **2. RFQ (Request for Quotation)**
```python
class RFQ(models.Model):
    rfq_number = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    rfq_date = models.DateField(auto_now_add=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=RFQ_STATUS_CHOICES)
    requirements = models.JSONField(default=dict)
    technical_specs = models.TextField(blank=True)
    delivery_terms = models.TextField(blank=True)
    payment_terms = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
```

### **3. VendorQuote (Tedarikçi Teklifi)**
```python
class VendorQuote(models.Model):
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quote_number = models.CharField(max_length=30)
    quote_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    delivery_time = models.IntegerField()  # days
    validity_period = models.IntegerField()  # days
    payment_terms = models.CharField(max_length=100)
    price_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    quality_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    delivery_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_awarded = models.BooleanField(default=False)
```

### **4. PurchaseOrder (Satın Alma Siparişi)**
```python
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=20, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=PO_STATUS_CHOICES)
    currency = models.CharField(max_length=3, default='TRY')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_terms = models.CharField(max_length=100)
    delivery_address = models.TextField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_pos')
```

### **5. GoodsReceipt (Mal Kabul)**
```python
class GoodsReceipt(models.Model):
    receipt_number = models.CharField(max_length=20, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    receipt_date = models.DateField(auto_now_add=True)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_note_number = models.CharField(max_length=50, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    quality_check_status = models.CharField(max_length=20, choices=QUALITY_STATUS_CHOICES)
    quantity_status = models.CharField(max_length=20, choices=QUANTITY_STATUS_CHOICES)
    inspection_notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
```

### **6. ExpenseCategory (Masraf Kategorisi)**
```python
class ExpenseCategory(models.Model):
    category_name = models.CharField(max_length=100)
    category_code = models.CharField(max_length=20, unique=True)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    account_code = models.CharField(max_length=20)
    is_tax_deductible = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    approval_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

### **7. ProducerReceipt (Müstahsil Makbuzu)**
```python
class ProducerReceipt(models.Model):
    receipt_number = models.CharField(max_length=20, unique=True)
    producer_name = models.CharField(max_length=100)
    producer_tax_number = models.CharField(max_length=11)
    producer_address = models.TextField()
    receipt_date = models.DateField()
    product_description = models.TextField()
    quantity = models.DecimalField(max_digits=15, decimal_places=3)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    gross_amount = models.DecimalField(max_digits=15, decimal_places=2)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    commission_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    stoppage_tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stoppage_tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

### **8. VendorPerformance (Tedarikçi Performansı)**
```python
class VendorPerformance(models.Model):
    vendor = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    evaluation_period = models.CharField(max_length=7)  # YYYY-MM format
    delivery_performance = models.DecimalField(max_digits=5, decimal_places=2)  # %
    quality_rating = models.DecimalField(max_digits=3, decimal_places=1)  # 1-10
    price_competitiveness = models.DecimalField(max_digits=5, decimal_places=2)  # %
    service_quality = models.DecimalField(max_digits=3, decimal_places=1)  # 1-10
    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    total_orders = models.IntegerField(default=0)
    on_time_deliveries = models.IntegerField(default=0)
    quality_issues = models.IntegerField(default=0)
    cost_savings = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    comments = models.TextField(blank=True)
```

---

## 🔧 API Endpoints

### **Purchase Requisition APIs**
```
GET    /api/v1/procurement/requisitions/          # Talep listesi
POST   /api/v1/procurement/requisitions/          # Yeni talep
GET    /api/v1/procurement/requisitions/{id}/     # Talep detayı
PUT    /api/v1/procurement/requisitions/{id}/     # Talep güncelleme
POST   /api/v1/procurement/requisitions/{id}/approve/  # Talep onaylama
```

### **RFQ Management APIs**
```
GET    /api/v1/procurement/rfqs/                  # RFQ listesi
POST   /api/v1/procurement/rfqs/                  # Yeni RFQ
GET    /api/v1/procurement/rfqs/{id}/             # RFQ detayı
PUT    /api/v1/procurement/rfqs/{id}/             # RFQ güncelleme
POST   /api/v1/procurement/rfqs/{id}/publish/     # RFQ yayınlama
GET    /api/v1/procurement/rfqs/{id}/quotes/      # RFQ teklifleri
POST   /api/v1/procurement/rfqs/{id}/evaluate/    # Teklif değerlendirmesi
```

### **Purchase Order APIs**
```
GET    /api/v1/procurement/orders/                # PO listesi
POST   /api/v1/procurement/orders/                # Yeni PO
GET    /api/v1/procurement/orders/{id}/           # PO detayı
PUT    /api/v1/procurement/orders/{id}/           # PO güncelleme
POST   /api/v1/procurement/orders/{id}/approve/   # PO onaylama
POST   /api/v1/procurement/orders/{id}/send/      # PO gönderimi
```

### **Goods Receipt APIs**
```
GET    /api/v1/procurement/receipts/              # Makbuz listesi
POST   /api/v1/procurement/receipts/              # Yeni makbuz
GET    /api/v1/procurement/receipts/{id}/         # Makbuz detayı
PUT    /api/v1/procurement/receipts/{id}/         # Makbuz güncelleme
POST   /api/v1/procurement/receipts/{id}/complete/  # Makbuz tamamlama
```

### **Vendor Management APIs**
```
GET    /api/v1/procurement/vendors/               # Tedarikçi listesi
POST   /api/v1/procurement/vendors/               # Yeni tedarikçi
GET    /api/v1/procurement/vendors/{id}/          # Tedarikçi detayı
GET    /api/v1/procurement/vendors/{id}/performance/  # Performans raporu
PUT    /api/v1/procurement/vendors/{id}/rating/   # Performans güncelleme
```

---

## 🎨 UI/UX Gereksinimleri

### **Dashboard Components**
- Purchase pipeline widget
- Pending approvals
- Vendor performance metrics
- Cost savings tracker

### **RFQ Management Interface**
- RFQ builder wizard
- Quote comparison matrix
- Evaluation scorecards
- Award decision workflow

### **Purchase Order Interface**
- PO creation wizard
- Template management
- Approval workflow
- Status tracking

### **Goods Receipt Interface**
- Mobile-friendly scanning
- Quality check forms
- Photo documentation
- Digital signatures

---

## 📊 Raporlama Gereksinimleri

### **Operational Reports**
- Purchase order status
- Goods receipt summary
- Vendor performance
- Expense analysis

### **Management Reports**
- Cost analysis
- Spend by category
- Vendor comparison
- ROI analysis

### **Compliance Reports**
- Tax reports
- Audit trails
- Müstahsil raporları
- Regulatory compliance

---

## 🚀 Implementation Plan

### **Phase 1: Core Procurement (2 hafta)**
- Purchase requisitions
- Basic PO management
- Vendor database
- Approval workflows

### **Phase 2: RFQ System (2 hafta)**
- RFQ creation
- Quote management
- Evaluation system
- Award process

### **Phase 3: Goods Receipt (1 hafta)**
- Receipt processing
- Quality control
- Inventory integration
- Mobile scanning

### **Phase 4: Advanced Features (2 hafta)**
- Expense management
- Müstahsil system
- Performance tracking
- Analytics & reporting

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 