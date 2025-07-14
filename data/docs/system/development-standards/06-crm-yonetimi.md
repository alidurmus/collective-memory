# Context7 ERP - CRM Yönetimi Modülü
**Modül Kodu:** CRM-MGT  
**Öncelik:** 2 - Yüksek  
**Tahmini Süre:** 4-5 hafta  
**Bağımlılıklar:** Müşteri Modülü, İletişim Sistemi, Marketing Automation  

---

## 📋 Modül Açıklaması

360° müşteri deneyimi yönetimi; lead takibi, aktivite yönetimi, segmentasyon, loyalty program, anket sistemi ve otomatik iletişim özelliklerini içeren kapsamlı müşteri ilişkileri çözümü.

---

## 🎯 Ana Özellikler

### **1. 360° Müşteri Görünümü**

#### **Unified Customer Profile**
- **Temel Bilgiler**
  - Demografik veriler
  - İletişim bilgileri
  - Firma/birey ayrımı
  - Vergi/kimlik bilgileri

- **Transaction History**
  - Satış geçmişi
  - Ödeme davranışı
  - İade işlemleri
  - Servis talepleri

- **Communication Log**
  - Tüm iletişim geçmişi
  - E-mail kayıtları
  - Telefon görüşmeleri
  - Sosyal medya etkileşimleri

#### **Document Management**
- **Central Repository**
  - Sözleşmeler
  - Teklifler
  - Faturalar
  - Belgeler

### **2. Lead ve Opportunity Management**

#### **Lead Capture**
- **Multi-Channel Sources**
  - Web formları
  - Social media
  - Referanslar
  - Trade shows
  - Cold calls

- **Lead Qualification**
  - BANT kriterleri
  - Lead scoring
  - Qualification process
  - Assignment rules

#### **Opportunity Pipeline**
- **Sales Stages**
  - Prospecting
  - Qualification
  - Proposal
  - Negotiation
  - Closing

- **Probability Management**
  - Win probability
  - Revenue forecasting
  - Pipeline analytics
  - Conversion rates

### **3. Aktivite ve Görev Yönetimi**

#### **Task Assignment System**
- **Automated Assignment**
  - Rule-based routing
  - Round-robin distribution
  - Skill-based routing
  - Workload balancing

- **Task Types**
  - Phone calls
  - Meetings
  - Follow-ups
  - Demos
  - Proposals

#### **Activity Tracking**
- **Real-time Updates**
  - Status tracking
  - Time logging
  - Outcome recording
  - Next action planning

#### **Reminder System**
- **Smart Notifications**
  - Email reminders
  - SMS alerts
  - Push notifications
  - Calendar integration

### **4. Customer Segmentation**

#### **Advanced Segmentation**
- **Behavioral Segmentation**
  - Purchase patterns
  - Usage behavior
  - Engagement levels
  - Loyalty indicators

- **Demographic Segmentation**
  - Age groups
  - Geographic location
  - Industry sectors
  - Company size

#### **Dynamic Segments**
- **Real-time Updates**
  - Automatic recalculation
  - Trigger-based updates
  - Segment movement tracking
  - Performance monitoring

### **5. Loyalty Program Management**

#### **Program Design**
- **Point Systems**
  - Earn rules
  - Redemption options
  - Point expiration
  - Tier benefits

- **Tier Management**
  - Membership levels
  - Upgrade criteria
  - Tier benefits
  - Status tracking

#### **Reward Management**
- **Catalog Management**
  - Product rewards
  - Service rewards
  - Discount coupons
  - Experience rewards

### **6. Survey and Feedback System**

#### **Survey Builder**
- **Question Types**
  - Multiple choice
  - Rating scales
  - Open text
  - Matrix questions
  - File uploads

- **Survey Logic**
  - Skip patterns
  - Branching logic
  - Display conditions
  - Validation rules

#### **Response Management**
- **Data Collection**
  - Real-time responses
  - Response tracking
  - Completion rates
  - Drop-off analysis

#### **Analytics & Insights**
- **Response Analysis**
  - Statistical analysis
  - Trend identification
  - Sentiment analysis
  - Benchmark comparisons

### **7. Mass Communication**

#### **Email Marketing**
- **Campaign Management**
  - Template library
  - Personalization
  - A/B testing
  - Send scheduling

- **Automation Workflows**
  - Welcome series
  - Nurture campaigns
  - Re-engagement
  - Win-back campaigns

#### **SMS Marketing**
- **Bulk SMS**
  - Personalized messages
  - Delivery tracking
  - Opt-out management
  - Compliance tracking

#### **Special Occasions**
- **Event-Based Marketing**
  - Birthday campaigns
  - Anniversary messages
  - Holiday greetings
  - Milestone celebrations

---

## 🗄️ Database Models

### **1. Customer (Müşteri)**
```python
class Customer(models.Model):
    customer_code = models.CharField(max_length=20, unique=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES)
    title = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, blank=True)
    tax_number = models.CharField(max_length=11, blank=True)
    tax_office = models.CharField(max_length=50, blank=True)
    identity_number = models.CharField(max_length=11, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    primary_email = models.EmailField()
    secondary_email = models.EmailField(blank=True)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=50, blank=True)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, blank=True)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    lead_source = models.CharField(max_length=50, blank=True)
    customer_since = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **2. Lead (Potansiyel Müşteri)**
```python
class Lead(models.Model):
    lead_number = models.CharField(max_length=20, unique=True)
    source = models.CharField(max_length=50, choices=LEAD_SOURCE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    industry = models.CharField(max_length=50, blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    authority = models.CharField(max_length=20, choices=AUTHORITY_CHOICES)
    need = models.TextField(blank=True)
    timeline = models.CharField(max_length=50, blank=True)
    lead_score = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    converted_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    conversion_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **3. Opportunity (Fırsat)**
```python
class Opportunity(models.Model):
    opportunity_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.CharField(max_length=20, choices=OPPORTUNITY_STAGE_CHOICES)
    probability = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # %
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    expected_close_date = models.DateField()
    actual_close_date = models.DateField(null=True, blank=True)
    sales_rep = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=50, blank=True)
    competitor = models.CharField(max_length=100, blank=True)
    next_step = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_won = models.BooleanField(default=False)
    win_reason = models.TextField(blank=True)
    loss_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **4. Activity (Aktivite)**
```python
class Activity(models.Model):
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    completed_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ACTIVITY_STATUS_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    duration = models.IntegerField(null=True, blank=True)  # minutes
    location = models.CharField(max_length=200, blank=True)
    attendees = models.ManyToManyField(User, related_name='activity_attendees', blank=True)
    outcome = models.TextField(blank=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
```

### **5. CustomerSegment (Müşteri Segmenti)**
```python
class CustomerSegment(models.Model):
    segment_name = models.CharField(max_length=100)
    segment_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    segment_type = models.CharField(max_length=20, choices=SEGMENT_TYPE_CHOICES)
    criteria = models.JSONField(default=dict)  # Segmentation criteria
    is_dynamic = models.BooleanField(default=False)
    customer_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
```

### **6. LoyaltyProgram (Sadakat Programı)**
```python
class LoyaltyProgram(models.Model):
    program_name = models.CharField(max_length=100)
    program_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    point_earning_rules = models.JSONField(default=dict)
    point_expiry_days = models.IntegerField(default=365)
    tier_structure = models.JSONField(default=list)
    terms_and_conditions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **7. CustomerLoyalty (Müşteri Sadakat)**
```python
class CustomerLoyalty(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE)
    membership_number = models.CharField(max_length=20, unique=True)
    join_date = models.DateField(auto_now_add=True)
    current_points = models.IntegerField(default=0)
    lifetime_points = models.IntegerField(default=0)
    redeemed_points = models.IntegerField(default=0)
    current_tier = models.CharField(max_length=20, blank=True)
    tier_start_date = models.DateField(null=True, blank=True)
    tier_expire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
```

### **8. Survey (Anket)**
```python
class Survey(models.Model):
    survey_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    survey_type = models.CharField(max_length=20, choices=SURVEY_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_anonymous = models.BooleanField(default=False)
    max_responses = models.IntegerField(null=True, blank=True)
    target_segments = models.ManyToManyField(CustomerSegment, blank=True)
    questions = models.JSONField(default=list)
    thank_you_message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=SURVEY_STATUS_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **9. SurveyResponse (Anket Cevabı)**
```python
class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    response_data = models.JSONField(default=dict)
    completion_status = models.CharField(max_length=20, choices=COMPLETION_STATUS_CHOICES)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    time_taken = models.IntegerField(null=True, blank=True)  # seconds
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
```

### **10. CommunicationLog (İletişim Kaydı)**
```python
class CommunicationLog(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    communication_type = models.CharField(max_length=20, choices=COMMUNICATION_TYPE_CHOICES)
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)  # Inbound/Outbound
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    sender = models.CharField(max_length=100, blank=True)
    recipient = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=COMMUNICATION_STATUS_CHOICES)
    delivery_date = models.DateTimeField(null=True, blank=True)
    opened_date = models.DateTimeField(null=True, blank=True)
    clicked_date = models.DateTimeField(null=True, blank=True)
    campaign = models.ForeignKey('Campaign', on_delete=models.SET_NULL, null=True, blank=True)
    attachments = models.JSONField(default=list)
    tags = models.JSONField(default=list)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔧 API Endpoints

### **Customer Management APIs**
```
GET    /api/v1/crm/customers/                    # Müşteri listesi
POST   /api/v1/crm/customers/                    # Yeni müşteri
GET    /api/v1/crm/customers/{id}/               # Müşteri detayı
PUT    /api/v1/crm/customers/{id}/               # Müşteri güncelleme
GET    /api/v1/crm/customers/{id}/360/           # 360° müşteri görünümü
GET    /api/v1/crm/customers/{id}/timeline/      # Müşteri zaman çizelgesi
```

### **Lead Management APIs**
```
GET    /api/v1/crm/leads/                        # Lead listesi
POST   /api/v1/crm/leads/                        # Yeni lead
PUT    /api/v1/crm/leads/{id}/qualify/           # Lead qualification
POST   /api/v1/crm/leads/{id}/convert/           # Lead conversion
GET    /api/v1/crm/leads/scoring/                # Lead scoring analizi
```

### **Opportunity APIs**
```
GET    /api/v1/crm/opportunities/                # Fırsat listesi
POST   /api/v1/crm/opportunities/                # Yeni fırsat
PUT    /api/v1/crm/opportunities/{id}/stage/     # Stage güncelleme
GET    /api/v1/crm/pipeline/                     # Sales pipeline
GET    /api/v1/crm/forecast/                     # Sales forecast
```

### **Activity Management APIs**
```
GET    /api/v1/crm/activities/                   # Aktivite listesi
POST   /api/v1/crm/activities/                   # Yeni aktivite
PUT    /api/v1/crm/activities/{id}/complete/     # Aktivite tamamlama
GET    /api/v1/crm/calendar/                     # Takvim görünümü
```

### **Segmentation APIs**
```
GET    /api/v1/crm/segments/                     # Segment listesi
POST   /api/v1/crm/segments/                     # Yeni segment
POST   /api/v1/crm/segments/{id}/refresh/        # Segment yenileme
GET    /api/v1/crm/segments/{id}/customers/      # Segment müşterileri
```

### **Survey APIs**
```
GET    /api/v1/crm/surveys/                      # Anket listesi
POST   /api/v1/crm/surveys/                      # Yeni anket
POST   /api/v1/crm/surveys/{id}/launch/          # Anket başlatma
GET    /api/v1/crm/surveys/{id}/responses/       # Anket cevapları
GET    /api/v1/crm/surveys/{id}/analytics/       # Anket analizi
```

---

## 🎨 UI/UX Gereksinimleri

### **CRM Dashboard**
- Activity feed
- Sales pipeline
- Performance metrics
- Recent interactions

### **Customer 360 Interface**
- Unified customer view
- Timeline of interactions
- Document library
- Communication history

### **Lead Management Interface**
- Lead capture forms
- Qualification workflow
- Lead scoring display
- Assignment rules

### **Survey Builder**
- Drag & drop interface
- Question templates
- Logic builder
- Preview functionality

---

## 🚀 Implementation Plan

### **Phase 1: Core CRM (2 hafta)**
- Customer management
- Contact management
- Basic activity tracking
- Document storage

### **Phase 2: Sales Management (2 hafta)**
- Lead management
- Opportunity tracking
- Sales pipeline
- Forecasting

### **Phase 3: Engagement Tools (1 hafta)**
- Survey system
- Communication tracking
- Segmentation
- Mass communication

### **Phase 4: Loyalty & Analytics (1 hafta)**
- Loyalty program
- Advanced analytics
- Reporting dashboard
- Performance metrics

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 