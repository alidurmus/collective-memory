# Context7 ERP - Servis Yönetimi Modülü
**Modül Kodu:** SERVICE-MGT  
**Öncelik:** 3 - Orta  
**Tahmini Süre:** 4-5 hafta  
**Bağımlılıklar:** CRM, İnsan Kaynakları, Stok Yönetimi  

---

## 📋 Modül Açıklaması

Kapsamlı teknik servis yönetimi; garanti takibi, randevu sistemi, personel/araç ataması, periyodik bakım anlaşmaları ve müşteri bildirimleri içeren tam entegre servis operasyon çözümü.

---

## 🎯 Ana Özellikler

### **1. Garanti ve Seri Numarası Takibi**

#### **Product Registration**
- **Serial Number Database**
  - Ürün seri numarası kayıtları
  - Satış tarihi bağlantısı
  - Müşteri ataması
  - Garanti süreleri

- **Warranty Management**
  - Garanti başlangıç/bitiş tarihleri
  - Garanti kapsamı tanımları
  - Koşullu garantiler
  - Uzatılmış garanti seçenekleri

#### **Service History Tracking**
- **Complete Service Records**
  - Tüm servis geçmişi
  - Yapılan işlemler
  - Değiştirilen parçalar
  - Teknisyen notları

### **2. Randevu Yönetimi Sistemi**

#### **Appointment Scheduling**
- **Calendar Integration**
  - Teknisyen takvimleri
  - Müsaitlik kontrolü
  - Otomatik planlama
  - Çakışma kontrolü

- **Customer Self-Service**
  - Online randevu sistemi
  - Müsait saat görüntüleme
  - Randevu iptal/değiştirme
  - SMS/Email onayları

#### **Appointment Types**
- **Service Categories**
  - Garanti servisi
  - Ücretli onarım
  - Periyodik bakım
  - Acil servis

### **3. Periyodik Bakım Anlaşmaları**

#### **Maintenance Contracts**
- **Contract Management**
  - Anlaşma şartları
  - Bakım periyodları
  - Kapsam tanımları
  - Fiyat listeleri

- **Automated Scheduling**
  - Otomatik randevu oluşturma
  - Önceden hatırlatma
  - Esnek programlama
  - Seasonal adjustments

#### **SLA Management**
- **Service Level Agreements**
  - Response time guarantees
  - Resolution time targets
  - Availability commitments
  - Performance metrics

### **4. Personel ve Araç Yönetimi**

#### **Technician Management**
- **Skill Matrix**
  - Uzmanlık alanları
  - Sertifikalar
  - Eğitim durumu
  - Performans skorları

- **Workload Management**
  - İş yükü dağılımı
  - Kapasite planlaması
  - Optimal atama
  - Efficiency tracking

#### **Vehicle Fleet Management**
- **Fleet Tracking**
  - Araç konumları
  - Fuel consumption
  - Maintenance schedules
  - Route optimization

- **Resource Allocation**
  - Araç ataması
  - Ekipman takibi
  - Spare parts stock
  - Tool management

### **5. Servis Fişi Yönetimi**

#### **Work Order Management**
- **Service Ticket Creation**
  - Problem tanımlama
  - Öncelik seviyeleri
  - Kategorizasyon
  - Initial assessment

- **Parts Management**
  - Gerekli yedek parçalar
  - Stok kontrolü
  - Sipariş işlemleri
  - Cost estimation

#### **External Service Integration**
- **Subcontractor Management**
  - Partner service providers
  - SLA agreements
  - Quality monitoring
  - Cost management

### **6. Otomatik Bildirimler**

#### **Status Update Notifications**
- **Multi-Channel Alerts**
  - SMS bildirimleri
  - Email güncellemeleri
  - Push notifications
  - Voice alerts

- **Automated Workflows**
  - Durum değişiklik tetikleyicileri
  - Escalation rules
  - Approval workflows
  - Customer notifications

#### **Reminder System**
- **Proactive Communications**
  - Bakım hatırlatmaları
  - Garanti son tarihi uyarıları
  - Follow-up calls
  - Satisfaction surveys

---

## 🗄️ Database Models

### **1. ServiceRequest (Servis Talebi)**
```python
class ServiceRequest(models.Model):
    ticket_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=50, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    issue_description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=SERVICE_STATUS_CHOICES)
    warranty_status = models.CharField(max_length=20, choices=WARRANTY_STATUS_CHOICES)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    customer_satisfaction = models.IntegerField(null=True, blank=True)  # 1-5 scale
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_service_requests')
```

### **2. ServiceAppointment (Servis Randevusu)**
```python
class ServiceAppointment(models.Model):
    appointment_number = models.CharField(max_length=20, unique=True)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    duration = models.IntegerField(default=60)  # minutes
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPE_CHOICES)
    customer_address = models.TextField(blank=True)
    service_location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS_CHOICES)
    confirmation_status = models.CharField(max_length=20, choices=CONFIRMATION_STATUS_CHOICES)
    reminder_sent = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **3. MaintenanceContract (Bakım Anlaşması)**
```python
class MaintenanceContract(models.Model):
    contract_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contract_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES)
    service_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    products = models.ManyToManyField(Product, through='ContractProduct')
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    payment_terms = models.CharField(max_length=100)
    sla_response_time = models.IntegerField(default=24)  # hours
    sla_resolution_time = models.IntegerField(default=72)  # hours
    coverage_details = models.TextField()
    exclusions = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS_CHOICES)
    assigned_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
```

### **4. TechnicianProfile (Teknisyen Profili)**
```python
class TechnicianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    specializations = models.ManyToManyField('ServiceSpecialization')
    certifications = models.JSONField(default=list)
    experience_years = models.IntegerField(default=0)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    service_territory = models.CharField(max_length=100, blank=True)
    availability_schedule = models.JSONField(default=dict)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    performance_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    assigned_vehicle = models.ForeignKey('ServiceVehicle', on_delete=models.SET_NULL, null=True, blank=True)
    tools_assigned = models.ManyToManyField('ServiceTool', blank=True)
    is_active = models.BooleanField(default=True)
```

### **5. ServiceVehicle (Servis Aracı)**
```python
class ServiceVehicle(models.Model):
    vehicle_number = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    capacity = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    current_mileage = models.IntegerField(default=0)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_due = models.DateField(null=True, blank=True)
    insurance_expiry = models.DateField()
    gps_device_id = models.CharField(max_length=50, blank=True)
    current_location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=VEHICLE_STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

### **6. ServiceWorkOrder (Servis İş Emri)**
```python
class ServiceWorkOrder(models.Model):
    work_order_number = models.CharField(max_length=20, unique=True)
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE)
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    work_performed = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    resolution = models.TextField(blank=True)
    parts_used = models.ManyToManyField(Product, through='ServicePartUsage')
    labor_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    travel_time = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    customer_signature = models.TextField(blank=True)  # Digital signature
    before_photos = models.JSONField(default=list)
    after_photos = models.JSONField(default=list)
    quality_check_passed = models.BooleanField(default=False)
    warranty_provided = models.IntegerField(default=0)  # days
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=WORK_ORDER_STATUS_CHOICES)
```

### **7. ServiceNotification (Servis Bildirimi)**
```python
class ServiceNotification(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    recipient = models.CharField(max_length=100)
    message = models.TextField()
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHOD_CHOICES)
    sent_date = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES)
    delivery_date = models.DateTimeField(null=True, blank=True)
    read_date = models.DateTimeField(null=True, blank=True)
    response_received = models.BooleanField(default=False)
    response_date = models.DateTimeField(null=True, blank=True)
    template_used = models.CharField(max_length=50, blank=True)
    trigger_event = models.CharField(max_length=50)
```

### **8. ServiceSpecialization (Servis Uzmanlığı)**
```python
class ServiceSpecialization(models.Model):
    specialization_name = models.CharField(max_length=100)
    specialization_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    required_certifications = models.JSONField(default=list)
    training_hours_required = models.IntegerField(default=0)
    category = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
```

### **9. PerformanceMetrics (Performans Metrikleri)**
```python
class PerformanceMetrics(models.Model):
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    total_service_calls = models.IntegerField(default=0)
    completed_on_time = models.IntegerField(default=0)
    first_time_fix_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_resolution_time = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # hours
    customer_satisfaction_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    revenue_generated = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    travel_efficiency = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    training_hours_completed = models.IntegerField(default=0)
    safety_incidents = models.IntegerField(default=0)
    calculated_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔧 API Endpoints

### **Service Request APIs**
```
GET    /api/v1/service/requests/                 # Servis talep listesi
POST   /api/v1/service/requests/                 # Yeni servis talebi
GET    /api/v1/service/requests/{id}/            # Servis talebi detayı
PUT    /api/v1/service/requests/{id}/            # Servis talebi güncelleme
POST   /api/v1/service/requests/{id}/assign/     # Teknisyen ataması
```

### **Appointment Management APIs**
```
GET    /api/v1/service/appointments/             # Randevu listesi
POST   /api/v1/service/appointments/             # Yeni randevu
PUT    /api/v1/service/appointments/{id}/        # Randevu güncelleme
GET    /api/v1/service/calendar/                 # Takvim görünümü
GET    /api/v1/service/availability/             # Müsaitlik kontrolü
```

### **Maintenance Contract APIs**
```
GET    /api/v1/service/contracts/                # Bakım anlaşması listesi
POST   /api/v1/service/contracts/                # Yeni bakım anlaşması
GET    /api/v1/service/contracts/{id}/           # Anlaşma detayı
POST   /api/v1/service/contracts/{id}/schedule/  # Otomatik programlama
```

### **Technician Management APIs**
```
GET    /api/v1/service/technicians/              # Teknisyen listesi
GET    /api/v1/service/technicians/{id}/profile/ # Teknisyen profili
GET    /api/v1/service/technicians/{id}/schedule/ # Teknisyen programı
GET    /api/v1/service/performance/              # Performans metrikleri
```

### **Fleet Management APIs**
```
GET    /api/v1/service/vehicles/                 # Araç filosu
GET    /api/v1/service/vehicles/{id}/location/   # Araç konumu
GET    /api/v1/service/vehicles/{id}/maintenance/ # Bakım durumu
POST   /api/v1/service/route-optimization/       # Rota optimizasyonu
```

---

## 🎨 UI/UX Gereksinimleri

### **Service Dashboard**
- Active service requests
- Technician schedules
- Performance metrics
- Customer satisfaction

### **Appointment Scheduler**
- Calendar view
- Drag & drop scheduling
- Conflict detection
- Resource availability

### **Mobile Service App**
- Work order management
- Photo documentation
- Digital signatures
- GPS tracking

### **Customer Portal**
- Service request submission
- Appointment booking
- Status tracking
- History view

---

## 🚀 Implementation Plan

### **Phase 1: Core Service Management (2 hafta)**
- Service request system
- Basic appointment scheduling
- Technician management
- Work order processing

### **Phase 2: Advanced Scheduling (1 hafta)**
- Calendar integration
- Automated scheduling
- Resource optimization
- Conflict resolution

### **Phase 3: Contract Management (1 hafta)**
- Maintenance contracts
- SLA management
- Automated reminders
- Performance tracking

### **Phase 4: Mobile & Integration (1 hafta)**
- Mobile applications
- Notification system
- Customer portal
- Analytics dashboard

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 