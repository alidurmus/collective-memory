# Context7 ERP - Üretim Yönetimi Modülü
**Modül Kodu:** MANUFACTURING  
**Öncelik:** 2 - Yüksek  
**Tahmini Süre:** 6-8 hafta  
**Bağımlılıklar:** Stok Yönetimi, Kalite Kontrol, İnsan Kaynakları  

---

## 📋 Modül Açıklaması

Basit üretimden MRP II seviyesine kadar tüm üretim süreçlerini kapsayan, reçete yönetimi, operasyon takibi, fason işlemler ve gerçek zamanlı maliyet hesaplaması içeren kapsamlı üretim yönetim sistemi.

---

## 🎯 Ana Özellikler

### **1. Basit Üretim Sistemi**

#### **Production Recipe Management (BOM)**
- **Bill of Materials**
  - Malzeme listesi
  - Miktarlar ve oranlar
  - Alternatif malzemeler
  - Maliyet hesaplamaları

- **Process Instructions**
  - Üretim talimatları
  - Kalite kontrol noktaları
  - Güvenlik prosedürleri
  - Standart çalışma süreleri

#### **Assembly Operations**
- **Work Instructions**
  - Adım adım talimatlar
  - Görsel rehberler
  - Kalite checkpointleri
  - Zaman standartları

- **Quality Checkpoints**
  - Kontrol noktaları
  - Test prosedürleri
  - Kabul kriterleri
  - Hata kodları

#### **Disassembly Tracking**
- **Return Processing**
  - İade ürün işleme
  - Komponent kurtarma
  - Yenileme süreçleri
  - Atık yönetimi

#### **Order-to-Production Flow**
- Otomatik üretim emirleri
- Kapasite kontrolü
- Malzeme uygunluğu
- Üretim programlama

### **2. MRP II - İleri Seviye Üretim**

#### **Advanced Manufacturing Resource Planning**
- **Master Production Schedule**
  - Ana üretim planı
  - Kapasite gereksinimleri
  - Kaynak planlaması
  - Darboğaz analizi

- **Material Requirements Planning**
  - Malzeme ihtiyaç planlaması
  - Lead time hesaplama
  - Safety stock yönetimi
  - Otomatik satın alma

#### **Detailed Operations**
- **Operation Sequence**
  - Operasyon sıralaması
  - Makine gereksinimleri
  - Setup süreleri
  - Çalışma süreleri

- **Skill Requirements**
  - Beceri gereksinimleri
  - Sertifika zorunlulukları
  - Eğitim durumu
  - Yetkinlik seviyeleri

#### **Work Order Management**
- **Job Scheduling**
  - İş programlama
  - Kaynak tahsisi
  - İlerleme takibi
  - Performans ölçümü

- **Resource Allocation**
  - Makine ataması
  - İşçi ataması
  - Araç gereç tahsisi
  - Kapasite optimizasyonu

#### **Gantt Chart Integration**
- **Visual Scheduling**
  - Timeline görselleştirme
  - Kaynak çakışmaları
  - Darboğaz tanımlama
  - Optimizasyon önerileri

#### **Shop Floor Control**
- **Real-time Updates**
  - Gerçek zamanlı güncellemeler
  - Kalite kapıları
  - Duruş zamanı takibi
  - Performans metrikleri

#### **Cost Accounting**
- **Real-time Costing**
  - Malzeme maliyetleri
  - İşçilik maliyetleri
  - Genel gider dağılımı
  - Varyans analizi

### **3. Fason İşlemler**

#### **Subcontractor Management**
- **Subcontractor Database**
  - Yetenek profilleri
  - Kapasite bilgileri
  - Kalite derecelendirmeleri
  - Performans geçmişi

#### **Subcontract Orders**
- **Work Specifications**
  - İş spesifikasyonları
  - Teslimat programları
  - Kalite gereksinimleri
  - SLA şartları

#### **Material Provision**
- **Material Delivery**
  - Malzeme teslimatı
  - Takip sistemi
  - İade işlemleri
  - Maliyet dağılımı

#### **Quality Control Integration**
- **Incoming Inspection**
  - Gelen mal muayenesi
  - Sertifika gereksinimleri
  - Red işlemleri
  - Düzeltici faaliyetler

### **4. Kalite Kontrol Entegrasyonu**

#### **In-Process Quality Control**
- Süreç içi kalite kontrolleri
- SPC (Statistical Process Control)
- Kalite trend analizi
- Preventive actions

#### **Quality Standards**
- ISO standartları
- Müşteri spesifikasyonları
- Internal standards
- Continuous improvement

### **5. Personel Verimlilik Raporları**

#### **Performance Tracking**
- **Individual Performance**
  - Çalışan verimliliği
  - Kalite performansı
  - Attendance tracking
  - Skill development

- **Team Performance**
  - Ekip verimliliği
  - Departman performansı
  - Shift performance
  - Cross-training progress

#### **Training Management**
- Eğitim ihtiyaç analizi
- Eğitim planlaması
- Sertifika takibi
- Competency assessment

---

## 🗄️ Database Models

### **1. BillOfMaterials (Malzeme Listesi)**
```python
class BillOfMaterials(models.Model):
    bom_number = models.CharField(max_length=20, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version = models.CharField(max_length=10, default='1.0')
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=BOM_STATUS_CHOICES)
    bom_type = models.CharField(max_length=20, choices=BOM_TYPE_CHOICES)
    base_quantity = models.DecimalField(max_digits=15, decimal_places=3, default=1)
    unit_of_measure = models.CharField(max_length=10)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_boms')
    is_active = models.BooleanField(default=True)
```

### **2. BOMComponent (BOM Bileşeni)**
```python
class BOMComponent(models.Model):
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='components')
    component = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=3)
    unit_of_measure = models.CharField(max_length=10)
    scrap_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # %
    component_type = models.CharField(max_length=20, choices=COMPONENT_TYPE_CHOICES)
    sequence = models.IntegerField(default=1)
    is_critical = models.BooleanField(default=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    lead_time = models.IntegerField(default=0)  # days
    cost_per_unit = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    notes = models.TextField(blank=True)
```

### **3. ProductionOrder (Üretim Emri)**
```python
class ProductionOrder(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE)
    quantity_planned = models.DecimalField(max_digits=15, decimal_places=3)
    quantity_completed = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    quantity_scrapped = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCTION_STATUS_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    sales_order = models.ForeignKey('sales.SalesOrder', on_delete=models.SET_NULL, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supervised_orders')
```

### **4. Operation (Operasyon)**
```python
class Operation(models.Model):
    operation_code = models.CharField(max_length=20, unique=True)
    operation_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    work_center = models.ForeignKey('WorkCenter', on_delete=models.CASCADE)
    setup_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # minutes
    run_time_per_unit = models.DecimalField(max_digits=8, decimal_places=4, default=0)  # minutes
    queue_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # minutes
    move_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # minutes
    required_skills = models.ManyToManyField('Skill', blank=True)
    safety_requirements = models.TextField(blank=True)
    quality_checkpoints = models.JSONField(default=list)
    is_outsourced = models.BooleanField(default=False)
    outsource_cost_per_unit = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    is_active = models.BooleanField(default=True)
```

### **5. WorkCenter (İş Merkezi)**
```python
class WorkCenter(models.Model):
    work_center_code = models.CharField(max_length=20, unique=True)
    work_center_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    work_center_type = models.CharField(max_length=20, choices=WORK_CENTER_TYPE_CHOICES)
    capacity = models.DecimalField(max_digits=8, decimal_places=2)  # hours/day
    efficiency = models.DecimalField(max_digits=5, decimal_places=2, default=100)  # %
    overhead_rate = models.DecimalField(max_digits=10, decimal_places=4, default=0)  # per hour
    location = models.CharField(max_length=100, blank=True)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    shift_pattern = models.CharField(max_length=20, choices=SHIFT_PATTERN_CHOICES)
    maintenance_schedule = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
```

### **6. ProductionOrderOperation (Üretim Emri Operasyonu)**
```python
class ProductionOrderOperation(models.Model):
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE, related_name='operations')
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    sequence = models.IntegerField()
    planned_start_date = models.DateTimeField()
    planned_end_date = models.DateTimeField()
    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=OPERATION_STATUS_CHOICES)
    setup_time_actual = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    run_time_actual = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity_completed = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    quantity_scrapped = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    machine = models.ForeignKey('Machine', on_delete=models.SET_NULL, null=True, blank=True)
    labor_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    overhead_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
```

### **7. SubcontractOrder (Fason Siparişi)**
```python
class SubcontractOrder(models.Model):
    subcontract_number = models.CharField(max_length=20, unique=True)
    subcontractor = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    quantity = models.DecimalField(max_digits=15, decimal_places=3)
    unit_price = models.DecimalField(max_digits=12, decimal_places=4)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    status = models.CharField(max_length=20, choices=SUBCONTRACT_STATUS_CHOICES)
    quality_requirements = models.TextField(blank=True)
    delivery_terms = models.TextField(blank=True)
    payment_terms = models.CharField(max_length=100)
    materials_provided = models.BooleanField(default=False)
    material_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

### **8. ProductionCost (Üretim Maliyeti)**
```python
class ProductionCost(models.Model):
    production_order = models.OneToOneField(ProductionOrder, on_delete=models.CASCADE)
    material_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    labor_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    overhead_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    subcontract_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    scrap_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cost_per_unit = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    standard_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    variance_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    variance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calculation_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
```

---

## 🔧 API Endpoints

### **BOM Management APIs**
```
GET    /api/v1/manufacturing/boms/                # BOM listesi
POST   /api/v1/manufacturing/boms/                # Yeni BOM
GET    /api/v1/manufacturing/boms/{id}/           # BOM detayı
PUT    /api/v1/manufacturing/boms/{id}/           # BOM güncelleme
POST   /api/v1/manufacturing/boms/{id}/copy/      # BOM kopyalama
POST   /api/v1/manufacturing/boms/{id}/approve/   # BOM onaylama
```

### **Production Order APIs**
```
GET    /api/v1/manufacturing/orders/              # Üretim emri listesi
POST   /api/v1/manufacturing/orders/              # Yeni üretim emri
GET    /api/v1/manufacturing/orders/{id}/         # Üretim emri detayı
PUT    /api/v1/manufacturing/orders/{id}/         # Üretim emri güncelleme
POST   /api/v1/manufacturing/orders/{id}/start/   # Üretim başlatma
POST   /api/v1/manufacturing/orders/{id}/complete/ # Üretim tamamlama
```

### **Operation Management APIs**
```
GET    /api/v1/manufacturing/operations/          # Operasyon listesi
POST   /api/v1/manufacturing/operations/          # Yeni operasyon
GET    /api/v1/manufacturing/workcenters/         # İş merkezi listesi
POST   /api/v1/manufacturing/workcenters/         # Yeni iş merkezi
```

### **Subcontract APIs**
```
GET    /api/v1/manufacturing/subcontracts/        # Fason sipariş listesi
POST   /api/v1/manufacturing/subcontracts/        # Yeni fason sipariş
GET    /api/v1/manufacturing/subcontracts/{id}/   # Fason sipariş detayı
PUT    /api/v1/manufacturing/subcontracts/{id}/   # Fason sipariş güncelleme
```

### **Cost Management APIs**
```
GET    /api/v1/manufacturing/costs/               # Maliyet analizi
POST   /api/v1/manufacturing/costs/calculate/     # Maliyet hesaplama
GET    /api/v1/manufacturing/variance/            # Varyans analizi
GET    /api/v1/manufacturing/reports/efficiency/  # Verimlilik raporu
```

---

## 🎨 UI/UX Gereksinimleri

### **Production Dashboard**
- Production schedule overview
- WIP (Work in Progress) tracking
- Performance metrics
- Capacity utilization

### **BOM Management Interface**
- BOM builder/editor
- Multi-level BOM view
- Cost rollup calculator
- Version control

### **Shop Floor Interface**
- Work order tracking
- Operation reporting
- Quality checkpoints
- Real-time updates

### **Gantt Chart Scheduler**
- Visual production schedule
- Drag & drop scheduling
- Resource allocation view
- Bottleneck identification

---

## 🚀 Implementation Plan

### **Phase 1: Basic Manufacturing (3 hafta)**
- BOM management
- Basic production orders
- Work center setup
- Simple operations

### **Phase 2: Advanced MRP (2 hafta)**
- MRP calculations
- Capacity planning
- Advanced scheduling
- Gantt chart integration

### **Phase 3: Shop Floor Control (2 hafta)**
- Operation tracking
- Real-time reporting
- Quality integration
- Performance monitoring

### **Phase 4: Cost & Subcontracting (1 hafta)**
- Cost accounting
- Subcontract management
- Variance analysis
- Advanced reporting

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 