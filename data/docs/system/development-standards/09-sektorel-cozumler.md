# Context7 ERP - Sektörel Çözümler Modülü
**Modül Kodu:** SECTOR-SOLUTIONS  
**Öncelik:** 4 - Düşük (Özelleştirilmiş)  
**Tahmini Süre:** 8-12 hafta  
**Bağımlılıklar:** Core ERP, POS, CRM, Stok Yönetimi  

---

## 📋 Modül Açıklaması

Sektöre özel entegre çözümler; restoran, otel ve süpermarket yönetimi için özelleştirilmiş iş süreçleri, POS entegrasyonu ve sektörel raporlama özelliklerini içeren vertical solutions paketi.

---

## 🎯 Ana Özellikler

### **1. Restoran Yönetimi Sistemi**

#### **Adisyon ve POS Sistemi**
- **Order Management**
  - Masa bazlı sipariş takibi
  - Menü kategorileri
  - Modifikasyonlar ve notlar
  - Split bill functionality

- **Table Management**
  - Masa düzeni yapılandırması
  - Kapasite yönetimi
  - Rezervasyon sistemi
  - Table status tracking

#### **Kitchen Display System**
- **Order Processing**
  - Mutfak ekranı entegrasyonu
  - Sipariş önceliklendirme
  - Preparation time tracking
  - Order completion alerts

#### **Touch Screen Interface**
- **Staff Interface**
  - Dokunmatik sipariş girişi
  - Quick access buttons
  - Category-based navigation
  - Modifier management

#### **Delivery Management**
- **Courier Tracking**
  - Kurye ataması
  - GPS takip sistemi
  - Teslimat süre takibi
  - Performance metrics

#### **Mobile Integration**
- **PDA Support**
  - Mobile order taking
  - Table service optimization
  - Inventory checking
  - Staff communication

#### **QR Menu System**
- **Contactless Ordering**
  - QR kod ile menü erişimi
  - Online sipariş sistemi
  - Payment integration
  - Order status tracking

### **2. Otel Yönetimi Sistemi**

#### **Ön Büro İşlemleri**
- **Front Desk Operations**
  - Check-in/check-out procedures
  - Guest registration
  - Room assignment
  - Key card management

- **Reservation Management**
  - Online booking integration
  - Room availability
  - Rate management
  - Cancellation policies

#### **Acente ve Sözleşme Yönetimi**
- **Travel Agent Relations**
  - Agent contracts
  - Commission structures
  - Booking allocations
  - Performance tracking

#### **Folio İşlemleri**
- **Guest Billing**
  - Room charges
  - Service charges
  - Incidental expenses
  - Payment processing

#### **Grup Rezervasyonu**
- **Group Bookings**
  - Block booking management
  - Group rates
  - Rooming lists
  - Group billing

#### **Online Rezervasyon Entegrasyonu**
- **Channel Management**
  - OTA integrations
  - Rate distribution
  - Inventory sync
  - Review management

#### **Kimlik Bildirim Sistemi**
- **Government Reporting**
  - Automated guest reporting
  - Police notification
  - Compliance tracking
  - Data security

### **3. Süpermarket Yönetimi (Hızlı Satış)**

#### **Hızlı Satış Sistemi**
- **Point of Sale**
  - Dokunmatik satış ekranı
  - Barcode scanning
  - Quick product lookup
  - Price checking

#### **Vardiyalı Kasa Sistemi**
- **Shift Management**
  - Cashier shifts
  - Till management
  - Shift reconciliation
  - Performance tracking

#### **Yaşlı Dostu Arayüz**
- **Accessibility Features**
  - Large buttons
  - High contrast
  - Voice assistance
  - Simple navigation

#### **Kargo Entegrasyonu**
- **Shipping Integration**
  - Multiple carrier support
  - Label printing
  - Tracking integration
  - Delivery scheduling

#### **İndirim ve Promosyon**
- **Promotion Management**
  - Happy hour pricing
  - Bundle deals
  - Loyalty discounts
  - Seasonal promotions

---

## 🗄️ Database Models

### **Restaurant Management Models**

#### **1. Restaurant (Restoran)**
```python
class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=200)
    restaurant_code = models.CharField(max_length=20, unique=True)
    cuisine_type = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    operating_hours = models.JSONField(default=dict)
    delivery_radius = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_delivery_enabled = models.BooleanField(default=False)
    is_takeaway_enabled = models.BooleanField(default=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    service_charge_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
```

#### **2. Table (Masa)**
```python
class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table_number = models.CharField(max_length=10)
    seating_capacity = models.IntegerField()
    table_type = models.CharField(max_length=20, choices=TABLE_TYPE_CHOICES)
    location = models.CharField(max_length=50)  # Indoor/Outdoor/Terrace
    status = models.CharField(max_length=20, choices=TABLE_STATUS_CHOICES)
    current_order = models.ForeignKey('RestaurantOrder', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

#### **3. MenuItem (Menü Ürünü)**
```python
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    item_code = models.CharField(max_length=20)
    category = models.ForeignKey('MenuCategory', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    preparation_time = models.IntegerField(default=0)  # minutes
    calories = models.IntegerField(null=True, blank=True)
    allergens = models.JSONField(default=list)
    ingredients = models.JSONField(default=list)
    is_available = models.BooleanField(default=True)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    image = models.ImageField(upload_to='menu_items/', blank=True)
```

#### **4. RestaurantOrder (Restoran Siparişi)**
```python
class RestaurantOrder(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    customer_name = models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    delivery_address = models.TextField(blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    served_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    special_instructions = models.TextField(blank=True)
```

### **Hotel Management Models**

#### **1. Hotel (Otel)**
```python
class Hotel(models.Model):
    hotel_name = models.CharField(max_length=200)
    hotel_code = models.CharField(max_length=20, unique=True)
    star_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    total_rooms = models.IntegerField()
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='12:00')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=8)
    city_tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='TRY')
    is_active = models.BooleanField(default=True)
```

#### **2. Room (Oda)**
```python
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    floor = models.IntegerField()
    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES)
    max_occupancy = models.IntegerField()
    amenities = models.JSONField(default=list)
    view_type = models.CharField(max_length=20, choices=VIEW_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES)
    last_cleaned = models.DateTimeField(null=True, blank=True)
    maintenance_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

#### **3. Reservation (Rezervasyon)**
```python
class Reservation(models.Model):
    reservation_number = models.CharField(max_length=20, unique=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    guest = models.ForeignKey('Guest', on_delete=models.CASCADE)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE)
    assigned_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    nights = models.IntegerField()
    room_rate = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    booking_source = models.CharField(max_length=50)
    agent = models.ForeignKey('TravelAgent', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### **4. Guest (Misafir)**
```python
class Guest(models.Model):
    guest_number = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=20, blank=True)
    id_number = models.CharField(max_length=11, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    company = models.CharField(max_length=200, blank=True)
    vip_status = models.BooleanField(default=False)
    preferences = models.JSONField(default=dict)
    blacklisted = models.BooleanField(default=False)
    last_stay_date = models.DateField(null=True, blank=True)
```

### **Supermarket Management Models**

#### **1. Store (Mağaza)**
```python
class Store(models.Model):
    store_name = models.CharField(max_length=200)
    store_code = models.CharField(max_length=20, unique=True)
    store_type = models.CharField(max_length=20, choices=STORE_TYPE_CHOICES)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    opening_hours = models.JSONField(default=dict)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_checkout_lanes = models.IntegerField(default=1)
    self_checkout_lanes = models.IntegerField(default=0)
    total_area = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

#### **2. CashRegister (Kasa)**
```python
class CashRegister(models.Model):
    register_number = models.CharField(max_length=10)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    register_type = models.CharField(max_length=20, choices=REGISTER_TYPE_CHOICES)
    is_self_checkout = models.BooleanField(default=False)
    current_cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    current_shift = models.ForeignKey('CashierShift', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=REGISTER_STATUS_CHOICES)
    last_maintenance = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

#### **3. CashierShift (Kasiyer Vardiyası)**
```python
class CashierShift(models.Model):
    shift_number = models.CharField(max_length=20, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    cashier = models.ForeignKey(User, on_delete=models.CASCADE)
    register = models.ForeignKey(CashRegister, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    opening_cash = models.DecimalField(max_digits=10, decimal_places=2)
    closing_cash = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    card_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_variance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    transaction_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=SHIFT_STATUS_CHOICES)
    notes = models.TextField(blank=True)
```

---

## 🔧 API Endpoints

### **Restaurant Management APIs**
```
GET    /api/v1/restaurant/orders/               # Sipariş listesi
POST   /api/v1/restaurant/orders/               # Yeni sipariş
GET    /api/v1/restaurant/tables/               # Masa durumu
POST   /api/v1/restaurant/tables/{id}/occupy/   # Masa işgal
GET    /api/v1/restaurant/menu/                 # Menü listesi
GET    /api/v1/restaurant/kitchen-display/      # Mutfak ekranı
```

### **Hotel Management APIs**
```
GET    /api/v1/hotel/reservations/              # Rezervasyon listesi
POST   /api/v1/hotel/reservations/              # Yeni rezervasyon
POST   /api/v1/hotel/checkin/                   # Check-in işlemi
POST   /api/v1/hotel/checkout/                  # Check-out işlemi
GET    /api/v1/hotel/room-availability/         # Oda müsaitliği
GET    /api/v1/hotel/folio/{id}/                # Misafir hesabı
```

### **Supermarket APIs**
```
GET    /api/v1/supermarket/pos/                 # POS işlemleri
POST   /api/v1/supermarket/sale/                # Satış kaydı
GET    /api/v1/supermarket/shifts/              # Vardiya listesi
POST   /api/v1/supermarket/shift/start/         # Vardiya başlatma
POST   /api/v1/supermarket/shift/end/           # Vardiya kapatma
```

---

## 🎨 UI/UX Gereksinimleri

### **Restaurant Interface**
- Touch-optimized order entry
- Table layout visualization
- Kitchen display system
- QR menu generation

### **Hotel Interface**
- Front desk dashboard
- Room status board
- Guest folio management
- Reservation calendar

### **Supermarket Interface**
- Large button POS system
- Barcode scanning
- Shift management
- Senior-friendly design

---

## 🚀 Implementation Plan

### **Phase 1: Restaurant Management (4 hafta)**
- POS system
- Table management
- Menu management
- Order processing

### **Phase 2: Hotel Management (3 hafta)**
- Reservation system
- Front desk operations
- Guest management
- Folio processing

### **Phase 3: Supermarket Management (2 hafta)**
- POS system
- Shift management
- Cashier interface
- Basic reporting

### **Phase 4: Integration & Mobile (3 hafta)**
- Mobile applications
- Third-party integrations
- Advanced reporting
- Performance optimization

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 