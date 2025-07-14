# Context7 ERP - İnsan Kaynakları Modülü
**Modül Kodu:** HR-MGT  
**Öncelik:** 3 - Orta  
**Tahmini Süre:** 6-8 hafta  
**Bağımlılıklar:** Core User Management, Finans, Bordro Sistemi  

---

## 📋 Modül Açıklaması

Kapsamlı insan kaynakları yönetimi; personel bilgi sistemi, bordro hesaplama, izin yönetimi, performans değerlendirme, eğitim takibi ve işe alım süreçlerini içeren tam entegre HR çözümü.

---

## 🎯 Ana Özellikler

### **1. Personel Bilgi Sistemi**

#### **Employee Database**
- **Personal Information**
  - Kimlik bilgileri
  - İletişim bilgileri
  - Acil durum kişileri
  - Aile bilgileri
  - Eğitim geçmişi

- **Employment Details**
  - İş başlangıç tarihi
  - Pozisyon bilgileri
  - Departman ataması
  - Maaş bilgileri
  - Sözleşme türü

#### **Document Management**
- **HR Documents**
  - Özgeçmiş
  - Diploma/sertifikalar
  - İş sözleşmeleri
  - Performans değerlendirmeleri
  - Disiplin kayıtları

#### **Organizational Structure**
- **Hierarchy Management**
  - Organizasyon şeması
  - Raporlama ilişkileri
  - Departman yapıları
  - Pozisyon tanımları

### **2. Bordro ve Maaş Sistemi**

#### **Payroll Calculation**
- **Salary Components**
  - Temel maaş
  - Primler ve ikramiyeler
  - Yan haklar
  - Mesai ücreti
  - Komisyon ödemeleri

- **Deductions**
  - Vergi kesintileri
  - SGK primleri
  - Sendika aidatları
  - Avans mahsuplaştırma
  - Diğer kesintiler

#### **Tax Calculations**
- **Turkish Tax System**
  - Gelir vergisi hesaplama
  - Damga vergisi
  - İşsizlik sigortası
  - SGK işveren payı
  - Vergi dilimi hesaplamaları

#### **Payroll Reports**
- **Legal Reports**
  - Bordro bordrosu
  - SGK bildirgeleri
  - Gelir vergisi beyannamesi
  - Müze beyannamesi
  - İstatistik raporları

### **3. İzin ve Devamsızlık Yönetimi**

#### **Leave Management**
- **Leave Types**
  - Yıllık izin
  - Hastalık izni
  - Doğum izni
  - Babalık izni
  - Mazeret izni

- **Leave Calculation**
  - Otomatik hak hesaplama
  - Devir işlemleri
  - İzin planlaması
  - Onay süreçleri

#### **Attendance Tracking**
- **Time Tracking**
  - Giriş/çıkış kayıtları
  - Mesai hesaplamaları
  - Geç kalma/erken çıkma
  - Molalar ve ara dinlenme

#### **Shift Management**
- **Work Schedules**
  - Vardiya planlaması
  - Rotating shifts
  - Overtime management
  - Weekend planning

### **4. Performans Yönetimi**

#### **Performance Evaluation**
- **Evaluation Periods**
  - Yıllık değerlendirmeler
  - Periyodik review'lar
  - Probation assessments
  - Project-based evaluations

- **KPI Management**
  - Hedef belirleme
  - Ölçüm kriterleri
  - Progress tracking
  - Achievement analysis

#### **Goal Setting**
- **SMART Goals**
  - Specific objectives
  - Measurable targets
  - Achievable goals
  - Relevant metrics
  - Time-bound plans

#### **360-Degree Feedback**
- **Multi-source evaluation**
  - Manager feedback
  - Peer reviews
  - Subordinate feedback
  - Self-assessment

### **5. Eğitim ve Gelişim**

#### **Training Management**
- **Training Programs**
  - İç eğitimler
  - Dış eğitimler
  - Online kurslar
  - Sertifika programları

- **Skill Development**
  - Beceri matrisi
  - Gelişim planları
  - Mentoring programs
  - Career pathing

#### **Training Records**
- **Certification Tracking**
  - Eğitim geçmişi
  - Sertifika takibi
  - Yenileme tarihleri
  - Compliance tracking

### **6. İşe Alım Süreci**

#### **Recruitment Process**
- **Job Posting**
  - İş ilanları
  - Pozisyon tanımları
  - Aranan nitelikler
  - Başvuru süreçleri

- **Candidate Management**
  - CV veritabanı
  - Başvuru takibi
  - Mülakat planlaması
  - Referans kontrolleri

#### **Onboarding Process**
- **New Employee Setup**
  - Oryantasyon programı
  - Doküman teslimi
  - Sistem erişimleri
  - Buddy assignment

### **7. Çıkış İşlemleri**

#### **Termination Process**
- **Exit Procedures**
  - İstifa işlemleri
  - Fesih süreçleri
  - Kıdem tazminatı
  - İhbar tazminatı

#### **Final Calculations**
- **Settlement**
  - Son maaş hesaplama
  - İzin ödemeleri
  - Prim ödemeleri
  - Kesinti hesaplamaları

---

## 🗄️ Database Models

### **1. Employee (Çalışan)**
```python
class Employee(models.Model):
    employee_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50, default='Turkish')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    
    # Identification
    identity_number = models.CharField(max_length=11, unique=True)
    passport_number = models.CharField(max_length=20, blank=True)
    driving_license = models.CharField(max_length=20, blank=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    mobile_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relation = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=20)
    
    # Employment Details
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    work_location = models.CharField(max_length=100)
    
    # Salary Information
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='TRY')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    bank_account = models.CharField(max_length=30, blank=True)
    iban = models.CharField(max_length=34, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=EMPLOYEE_STATUS_CHOICES)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **2. Department (Departman)**
```python
class Department(models.Model):
    department_name = models.CharField(max_length=100)
    department_code = models.CharField(max_length=20, unique=True)
    parent_department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    cost_center = models.CharField(max_length=20, blank=True)
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    location = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **3. Position (Pozisyon)**
```python
class Position(models.Model):
    position_title = models.CharField(max_length=100)
    position_code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=POSITION_LEVEL_CHOICES)
    job_description = models.TextField()
    required_qualifications = models.TextField()
    min_salary = models.DecimalField(max_digits=12, decimal_places=2)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2)
    reports_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **4. Payroll (Bordro)**
```python
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    pay_date = models.DateField()
    
    # Earnings
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Deductions
    income_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    social_security_employee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unemployment_insurance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    union_dues = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    advance_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Employer Costs
    social_security_employer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unemployment_insurance_employer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Net Pay
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=PAYROLL_STATUS_CHOICES)
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    processed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'pay_period_start', 'pay_period_end']
```

### **5. LeaveRequest (İzin Talebi)**
```python
class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey('LeaveType', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.DecimalField(max_digits=5, decimal_places=1)
    reason = models.TextField(blank=True)
    replacement_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='covering_leaves')
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Supporting Documents
    medical_certificate = models.FileField(upload_to='leave_documents/', blank=True)
    supporting_documents = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### **6. LeaveType (İzin Türü)**
```python
class LeaveType(models.Model):
    leave_name = models.CharField(max_length=100)
    leave_code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    max_days_per_year = models.IntegerField(default=0)
    carry_forward_allowed = models.BooleanField(default=False)
    max_carry_forward_days = models.IntegerField(default=0)
    requires_approval = models.BooleanField(default=True)
    requires_documentation = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=True)
    gender_specific = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
```

### **7. Attendance (Devam)**
```python
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    late_minutes = models.IntegerField(default=0)
    early_departure_minutes = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS_CHOICES)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['employee', 'date']
```

### **8. PerformanceReview (Performans Değerlendirmesi)**
```python
class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPE_CHOICES)
    
    # Overall Ratings
    overall_rating = models.DecimalField(max_digits=3, decimal_places=1)  # 1.0 to 5.0
    goal_achievement = models.DecimalField(max_digits=3, decimal_places=1)
    competency_rating = models.DecimalField(max_digits=3, decimal_places=1)
    
    # Comments
    achievements = models.TextField(blank=True)
    areas_for_improvement = models.TextField(blank=True)
    development_goals = models.TextField(blank=True)
    manager_comments = models.TextField(blank=True)
    employee_comments = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES)
    submitted_date = models.DateTimeField(null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
```

### **9. Training (Eğitim)**
```python
class Training(models.Model):
    training_name = models.CharField(max_length=200)
    training_code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    trainer = models.CharField(max_length=100)
    training_type = models.CharField(max_length=20, choices=TRAINING_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.IntegerField()
    location = models.CharField(max_length=200, blank=True)
    max_participants = models.IntegerField(default=0)
    cost_per_participant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    materials_provided = models.TextField(blank=True)
    prerequisites = models.TextField(blank=True)
    certification_provided = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=TRAINING_STATUS_CHOICES)
    is_mandatory = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **10. JobApplication (İş Başvurusu)**
```python
class JobApplication(models.Model):
    application_number = models.CharField(max_length=20, unique=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    
    # Applicant Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    birth_date = models.DateField()
    nationality = models.CharField(max_length=50)
    
    # Application Details
    cv_file = models.FileField(upload_to='applications/cv/')
    cover_letter = models.TextField(blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    available_start_date = models.DateField(null=True, blank=True)
    
    # Education & Experience
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    university = models.CharField(max_length=200, blank=True)
    major = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    years_of_experience = models.IntegerField(default=0)
    
    # Application Status
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES)
    source = models.CharField(max_length=50, choices=APPLICATION_SOURCE_CHOICES)
    assigned_recruiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Screening & Interview
    screening_score = models.IntegerField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_notes = models.TextField(blank=True)
    final_decision = models.CharField(max_length=20, choices=DECISION_CHOICES, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## 🔧 API Endpoints

### **Employee Management APIs**
```
GET    /api/v1/hr/employees/                     # Çalışan listesi
POST   /api/v1/hr/employees/                     # Yeni çalışan
GET    /api/v1/hr/employees/{id}/                # Çalışan detayı
PUT    /api/v1/hr/employees/{id}/                # Çalışan güncelleme
GET    /api/v1/hr/employees/{id}/profile/        # Çalışan profili
```

### **Payroll APIs**
```
GET    /api/v1/hr/payroll/                       # Bordro listesi
POST   /api/v1/hr/payroll/calculate/             # Bordro hesaplama
GET    /api/v1/hr/payroll/{id}/                  # Bordro detayı
POST   /api/v1/hr/payroll/bulk-process/          # Toplu bordro işleme
GET    /api/v1/hr/payroll/reports/               # Bordro raporları
```

### **Leave Management APIs**
```
GET    /api/v1/hr/leave-requests/                # İzin talep listesi
POST   /api/v1/hr/leave-requests/                # Yeni izin talebi
PUT    /api/v1/hr/leave-requests/{id}/approve/   # İzin onaylama
PUT    /api/v1/hr/leave-requests/{id}/reject/    # İzin reddetme
GET    /api/v1/hr/leave-balance/{employee_id}/   # İzin bakiyesi
```

### **Attendance APIs**
```
GET    /api/v1/hr/attendance/                    # Devam listesi
POST   /api/v1/hr/attendance/checkin/            # Giriş kaydı
POST   /api/v1/hr/attendance/checkout/           # Çıkış kaydı
GET    /api/v1/hr/attendance/{employee_id}/      # Çalışan devam durumu
GET    /api/v1/hr/attendance/reports/            # Devam raporları
```

### **Performance APIs**
```
GET    /api/v1/hr/performance-reviews/           # Performans değerlendirme listesi
POST   /api/v1/hr/performance-reviews/           # Yeni değerlendirme
GET    /api/v1/hr/performance-reviews/{id}/      # Değerlendirme detayı
POST   /api/v1/hr/performance-reviews/{id}/submit/ # Değerlendirme gönderimi
```

### **Training APIs**
```
GET    /api/v1/hr/trainings/                     # Eğitim listesi
POST   /api/v1/hr/trainings/                     # Yeni eğitim
POST   /api/v1/hr/trainings/{id}/enroll/         # Eğitime kayıt
GET    /api/v1/hr/training-records/{employee_id}/ # Eğitim geçmişi
```

### **Recruitment APIs**
```
GET    /api/v1/hr/job-applications/              # Başvuru listesi
POST   /api/v1/hr/job-applications/              # Yeni başvuru
PUT    /api/v1/hr/job-applications/{id}/status/  # Başvuru durumu güncelleme
GET    /api/v1/hr/positions/                     # Açık pozisyonlar
```

---

## 🎨 UI/UX Gereksinimleri

### **HR Dashboard**
- Employee overview
- Pending approvals
- Payroll summary
- Training calendar

### **Employee Management Interface**
- Employee directory
- Organizational chart
- Employee profiles
- Document management

### **Payroll Interface**
- Payroll calculation wizard
- Batch processing
- Tax reporting
- Payslip generation

### **Leave Management**
- Leave calendar
- Approval workflows
- Balance tracking
- Team coverage planning

---

## 🚀 Implementation Plan

### **Phase 1: Core HR Management (3 hafta)**
- Employee database
- Department/position setup
- Basic document management
- User profile integration

### **Phase 2: Payroll System (2 hafta)**
- Payroll calculation engine
- Tax calculations
- Payment processing
- Reporting system

### **Phase 3: Time & Attendance (2 hafta)**
- Attendance tracking
- Leave management
- Shift planning
- Overtime calculations

### **Phase 4: Performance & Development (1 hafta)**
- Performance reviews
- Training management
- Goal setting
- Career development

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 