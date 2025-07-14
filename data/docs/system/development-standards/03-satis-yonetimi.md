# Context7 ERP - Satış Yönetimi Modülü
**Modül Kodu:** SALES-MGT  
**Öncelik:** 2 - Yüksek  
**Tahmini Süre:** 4-6 hafta  
**Bağımlılıklar:** Stok Yönetimi, CRM, Finans Modülü  

---

## 📋 Modül Açıklaması

Uçtan uca satış süreci yönetimi; teklif verme, sipariş alma, sevkiyat planlama, promosyon yönetimi ve saha satış operasyonlarını içeren kapsamlı satış çözümü.

---

## 🎯 Ana Özellikler

### **1. Satış Süreci Yönetimi**

#### **Quote Management (Teklif Yönetimi)**
- **Teklif Oluşturma**
  - Ürün bazlı teklifler
  - Paket teklifler
  - Özelleştirilmiş çözümler
  - Geçerlilik süreleri

- **Pricing Engine**
  - Dinamik fiyatlandırma
  - Müşteri bazlı özel fiyatlar
  - Miktar iskontları
  - Otomatik maliyet hesaplama

#### **Order Processing (Sipariş İşleme)**
- **Sipariş Alma**
  - Online sipariş formu
  - Telefon siparişleri
  - Email siparişleri
  - EDI entegrasyonu

- **Order Validation**
  - Stok kontrolleri
  - Kredi limit kontrolleri
  - Fiyat doğrulaması
  - Teslimat uygunluğu

#### **Sales Invoice Management**
- Otomatik fatura oluşturma
- Kısmi faturalama
- Pro-forma faturalar
- E-fatura entegrasyonu

### **2. Transfer ve Sevkiyat Sistemi**

#### **Inter-Branch Transfer**
- **Transfer Talepleri**
  - Kaynak depo seçimi
  - Hedef depo ataması
  - Transfer sebepleri
  - Aciliyet seviyesi

- **Transfer Approval**
  - Onay gerektiren işlemler
  - Maliyet dağılımı
  - Belgelendirme
  - Transfer takibi

#### **Shipment Planning**
- **Carrier Selection**
  - Kargo firması seçimi
  - Maliyet karşılaştırması
  - Teslimat süresi analizi
  - SLA uyumluluğu

- **Route Optimization**
  - En optimal rotalar
  - Teslimat programlama
  - GPS takip entegrasyonu
  - Gerçek zamanlı güncelleme

#### **Tracking System**
- Sevkiyat durumu takibi
- GPS takip sistemi
  - Teslimat onayı
  - POD (Proof of Delivery)

### **3. Promosyon Yönetimi**

#### **Campaign Management**
- **Campaign Definition**
  - Kampanya tipi
  - Hedef kitle
  - Promosyon mekaniği
  - Bütçe yönetimi

- **Customer Targeting**
  - Segmentasyon kriterleri
  - Uygunluk kuralları
  - Hariç tutulacak listeler
  - Kişiselleştirme

#### **Performance Tracking**
- **Campaign Metrics**
  - Kampanya metrikleri
  - ROI hesaplaması
  - Dönüşüm oranları
  - Müşteri tepkileri

#### **Loyalty Program Integration**
- Puan sistemi
- Ödül kullanımı
- Kademeli faydalar
- Üyelik seviyeleri

### **4. Saha Satış Yönetimi**

#### **Sales Representative Management**
- **Territory Mapping**
  - Bölge haritalama
  - Müşteri ataması
  - Hedef belirleme
  - Performans takibi

- **Route Planning**
  - Optimal rotalar
  - Ziyaret sıklığı
  - Seyahat süresi tahmini
  - Verimlilik analizi

#### **Mobile Sales Support**
- **Offline Capability**
  - Çevrimdışı çalışma
  - Veri senkronizasyonu
  - Mobil sipariş girişi
  - Fotoğraf dokümantasyonu

- **Performance Dashboard**
  - Satış başarıları
  - Ziyaret uyumluluğu
  - Müşteri memnuniyeti
  - Hedef gerçekleşme

### **5. Konsinye ve Depozito Satışları**

#### **Consignment Tracking**
- **Konsinyedeki Mallar**
  - Mal takibi
  - Uzlaştırma dönemleri
  - İade işlemleri
  - Mülkiyet transferi

#### **Deposit Management**
- **Depozito İşlemleri**
  - Depozito tahsilâtı
  - İade işlemleri
  - Şişe iade takibi
  - Otomatik mahsup

#### **Settlement Processing**
- Otomatik faturalama
- Komisyon hesaplama
- Ödeme şartları
- Uzlaştırma raporları

### **6. E-Arşiv ve QR Kod Sistemi**

#### **E-Archive Integration**
- **Gelen Kutu**
  - QR Kod ile fatura aktarımı
  - Otomatik veri çıkarımı
  - Belge sınıflandırması
  - Onay süreçleri

- **Document Processing**
  - OCR ile metin tanıma
  - Otomatik kayıt
  - Hata kontrolü
  - Manuel düzeltme

---

## 🗄️ Database Models

### **1. SalesQuote (Satış Teklifi)**
```python
class SalesQuote(models.Model):
    quote_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quote_date = models.DateField(auto_now_add=True)
    valid_until = models.DateField()
    status = models.CharField(max_length=20, choices=QUOTE_STATUS_CHOICES)
    currency = models.CharField(max_length=3, default='TRY')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    delivery_terms = models.TextField(blank=True)
    payment_terms = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_converted = models.BooleanField(default=False)
    converted_to_order = models.ForeignKey('SalesOrder', on_delete=models.SET_NULL, null=True, blank=True)
```

### **2. SalesOrder (Satış Siparişi)**
```python
class SalesOrder(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    requested_delivery_date = models.DateField()
    confirmed_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    currency = models.CharField(max_length=3, default='TRY')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_terms = models.CharField(max_length=100)
    delivery_address = models.TextField()
    shipping_method = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales_orders')
```

### **3. InterBranchTransfer (Şubeler Arası Transfer)**
```python
class InterBranchTransfer(models.Model):
    transfer_number = models.CharField(max_length=20, unique=True)
    source_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='transfers_out')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='transfers_in')
    transfer_date = models.DateField(auto_now_add=True)
    transfer_reason = models.CharField(max_length=100)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES)
    status = models.CharField(max_length=20, choices=TRANSFER_STATUS_CHOICES)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    transportation_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    carrier = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=50, blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_transfers')
    approval_date = models.DateTimeField(null=True, blank=True)
    shipped_date = models.DateTimeField(null=True, blank=True)
    received_date = models.DateTimeField(null=True, blank=True)
```

### **4. SalesPromotion (Satış Promosyonu)**
```python
class SalesPromotion(models.Model):
    promotion_code = models.CharField(max_length=20, unique=True)
    promotion_name = models.CharField(max_length=100)
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=PROMOTION_STATUS_CHOICES)
    target_audience = models.CharField(max_length=50, choices=TARGET_AUDIENCE_CHOICES)
    budget = models.DecimalField(max_digits=15, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_quantity = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    minimum_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    customer_segments = models.ManyToManyField('CustomerSegment', blank=True)
    product_categories = models.ManyToManyField('ProductCategory', blank=True)
    is_active = models.BooleanField(default=True)
```

### **5. SalesTerritory (Satış Bölgesi)**
```python
class SalesTerritory(models.Model):
    territory_name = models.CharField(max_length=100)
    territory_code = models.CharField(max_length=20, unique=True)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='Turkey')
    sales_rep = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='territories')
    backup_rep = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='backup_territories')
    target_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    customer_count = models.IntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    visit_frequency = models.IntegerField(default=30)  # days
    travel_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
```

### **6. CustomerVisit (Müşteri Ziyareti)**
```python
class CustomerVisit(models.Model):
    visit_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES)
    visit_purpose = models.CharField(max_length=100)
    planned_duration = models.IntegerField()  # minutes
    actual_duration = models.IntegerField(null=True, blank=True)
    location_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    location_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    visit_notes = models.TextField(blank=True)
    next_action = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=VISIT_STATUS_CHOICES)
    photos = models.JSONField(default=list)  # Store photo URLs
    documents = models.JSONField(default=list)  # Store document URLs
```

### **7. ConsignmentStock (Konsinye Stok)**
```python
class ConsignmentStock(models.Model):
    consignment_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_consigned = models.DecimalField(max_digits=15, decimal_places=3)
    quantity_sold = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    quantity_returned = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    consignment_date = models.DateField()
    settlement_period = models.IntegerField(default=30)  # days
    next_settlement_date = models.DateField()
    status = models.CharField(max_length=20, choices=CONSIGNMENT_STATUS_CHOICES)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
```

---

## 🔧 API Endpoints

### **Sales Quote APIs**
```
GET    /api/v1/sales/quotes/                      # Teklif listesi
POST   /api/v1/sales/quotes/                      # Yeni teklif
GET    /api/v1/sales/quotes/{id}/                 # Teklif detayı
PUT    /api/v1/sales/quotes/{id}/                 # Teklif güncelleme
POST   /api/v1/sales/quotes/{id}/convert/         # Siparişe çevirme
POST   /api/v1/sales/quotes/{id}/send/            # Teklif gönderimi
```

### **Sales Order APIs**
```
GET    /api/v1/sales/orders/                      # Sipariş listesi
POST   /api/v1/sales/orders/                      # Yeni sipariş
GET    /api/v1/sales/orders/{id}/                 # Sipariş detayı
PUT    /api/v1/sales/orders/{id}/                 # Sipariş güncelleme
POST   /api/v1/sales/orders/{id}/confirm/         # Sipariş onaylama
POST   /api/v1/sales/orders/{id}/ship/            # Sevkiyat başlatma
```

### **Transfer Management APIs**
```
GET    /api/v1/sales/transfers/                   # Transfer listesi
POST   /api/v1/sales/transfers/                   # Yeni transfer
GET    /api/v1/sales/transfers/{id}/              # Transfer detayı
PUT    /api/v1/sales/transfers/{id}/              # Transfer güncelleme
POST   /api/v1/sales/transfers/{id}/approve/      # Transfer onaylama
POST   /api/v1/sales/transfers/{id}/ship/         # Transfer sevkiyatı
```

### **Promotion APIs**
```
GET    /api/v1/sales/promotions/                  # Promosyon listesi
POST   /api/v1/sales/promotions/                  # Yeni promosyon
GET    /api/v1/sales/promotions/{id}/             # Promosyon detayı
PUT    /api/v1/sales/promotions/{id}/             # Promosyon güncelleme
GET    /api/v1/sales/promotions/{id}/performance/ # Promosyon performansı
```

### **Field Sales APIs**
```
GET    /api/v1/sales/territories/                 # Bölge listesi
POST   /api/v1/sales/territories/                 # Yeni bölge
GET    /api/v1/sales/visits/                      # Ziyaret listesi
POST   /api/v1/sales/visits/                      # Yeni ziyaret
POST   /api/v1/sales/visits/{id}/checkin/         # Ziyaret başlatma
POST   /api/v1/sales/visits/{id}/checkout/        # Ziyaret bitirme
```

---

## 🎨 UI/UX Gereksinimleri

### **Sales Dashboard**
- Sales pipeline görünümü
- Revenue tracking
- Target vs actual performance
- Top customers/products

### **Quote Management Interface**
- Quote builder wizard
- Product catalog integration
- Pricing calculator
- Template management

### **Order Processing Interface**
- Order entry forms
- Inventory availability check
- Credit limit validation
- Delivery scheduling

### **Mobile Sales App**
- Customer lookup
- Product catalog
- Order entry
- Visit tracking
- Offline capability

---

## 🚀 Implementation Plan

### **Phase 1: Core Sales (2 hafta)**
- Quote management
- Order processing
- Basic customer management
- Product catalog integration

### **Phase 2: Advanced Features (2 hafta)**
- Transfer management
- Promotion system
- Pricing engine
- Approval workflows

### **Phase 3: Field Sales (1 hafta)**
- Territory management
- Visit tracking
- Mobile application
- GPS integration

### **Phase 4: Specialized Sales (1 hafta)**
- Consignment tracking
- Deposit management
- E-archive integration
- Performance analytics

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 