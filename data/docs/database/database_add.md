# Context7 ERP Sistemi - Veri Alanları İlişkileri

**Versiyon:** v2.2.0-glassmorphism-enhanced  
**Son Güncelleme:** 9 Haziran 2025  
**Veritabanı:** SQLite (1,088 kayıt, 73 tablo) + PostgreSQL Hazır  
**Durum:** Production Ready (99.5% Complete)

Bu belge, Context7 ERP sistemindeki tüm veri alanları arasındaki ilişkileri, foreign key bağlantılarını ve business logic kurallarını detaylandırır.

---

## 📊 Veritabanı İlişki Şeması

### 🏗️ Temel Mimarı Yapısı
```sql
Context7BaseModel (Abstract Base)
├── id (UUID, PK)
├── created_by_id (FK → User.id)
├── updated_by_id (FK → User.id)
├── company_id (FK → Company.id)
├── created_at (DateTime)
├── updated_at (DateTime)
├── is_active (Boolean)
├── is_deleted (Boolean)
└── version (PositiveInteger)

Company (Ana Varlık)
├── id (UUID, PK)
├── name (CharField)
├── tax_number (CharField, Unique)
├── trade_registry_number (CharField)
├── email (EmailField)
├── phone (CharField)
├── website (URLField)
├── address (TextField)
├── city (CharField)
├── country (CharField)
├── postal_code (CharField)
├── industry (CharField)
├── employee_count (IntegerField)
├── annual_revenue (DecimalField)
├── default_currency (CharField)
└── fiscal_year_start (DateField)
```

---

## 🏢 1. Organizasyon Modülü İlişkileri

### 1.1 Şirket ve Departman Yapısı
```sql
Company (1) ←→ (N) Department
Company (1) ←→ (N) User
Company (1) ←→ (N) Employee

Department
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField)
├── code (CharField, Unique)
├── description (TextField)
├── manager_id (FK → Employee.id) [Self-Reference]
└── is_active (Boolean)

Department (1) ←→ (N) Employee [many_to_one]
Department (1) ←→ (N) ProductionStation [one_to_many]
Department (1) ←→ (N) PurchaseRequest [one_to_many]
```

### 1.2 Rol ve İzin Sistemi
```sql
Role
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField, Unique)
├── code (CharField, Unique)
├── department_id (FK → Department.id)
├── description (TextField)
└── is_active (Boolean)

Permission
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField)
├── code (CharField, Unique)
└── description (TextField)

Role (N) ←→ (N) Permission [ManyToMany: permissions]
User (N) ←→ (N) Role [ManyToMany through UserRole]
```

---

## 👥 2. İnsan Kaynakları Modülü İlişkileri

### 2.1 Çalışan Hiyerarşisi
```sql
Employee
├── id (UUID, PK)
├── user_id (FK → User.id) [OneToOne]
├── company_id (FK → Company.id)
├── department_id (FK → Department.id)
├── role_id (FK → Role.id)
├── name (CharField)
├── position (CharField)
├── email (EmailField, Unique)
├── phone (CharField)
├── hire_date (DateField)
├── employee_code (CharField, Unique)
├── salary (DecimalField)
└── is_active (Boolean)

User (1) ←→ (1) Employee [OneToOne]
Department (1) ←→ (N) Employee [many_to_one]
Role (1) ←→ (N) Employee [many_to_one]
Employee (1) ←→ (1) Department [manager, Self-Reference]
```

### 2.2 İzin Yönetimi İlişkileri
```sql
LeaveType
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField, Unique)
├── description (TextField)
└── is_paid (Boolean)

LeaveRequest
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── employee_id (FK → Employee.id)
├── leave_type_id (FK → LeaveType.id)
├── start_date (DateField)
├── end_date (DateField)
├── reason (TextField)
├── status (CharField: pending/approved/rejected/cancelled)
└── approved_by_id (FK → User.id)

Employee (1) ←→ (N) LeaveRequest [one_to_many: leave_requests]
LeaveType (1) ←→ (N) LeaveRequest [one_to_many]
User (1) ←→ (N) LeaveRequest [one_to_many: approved_leave_requests]

LeaveBalance
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── employee_id (FK → Employee.id)
├── leave_type_id (FK → LeaveType.id)
└── balance (DecimalField)

Employee (1) ←→ (N) LeaveBalance [one_to_many: leave_balances]
LeaveType (1) ←→ (N) LeaveBalance [one_to_many]
```

### 2.3 Bordro ve Masraf İlişkileri
```sql
PayrollRecord
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── employee_id (FK → Employee.id)
├── period_start (DateField)
├── period_end (DateField)
├── gross_salary (DecimalField)
├── net_salary (DecimalField)
├── deductions (DecimalField)
├── bonuses (DecimalField)
├── is_paid (Boolean)
└── payment_date (DateField)

ExpenseRequest
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── employee_id (FK → Employee.id)
├── request_date (DateField)
├── description (CharField)
├── amount (DecimalField)
├── status (CharField: pending/approved/rejected/paid)
└── approved_by_id (FK → User.id)

Employee (1) ←→ (N) PayrollRecord [one_to_many: payroll_records]
Employee (1) ←→ (N) ExpenseRequest [one_to_many: expense_requests]
User (1) ←→ (N) ExpenseRequest [one_to_many: approved_expenses]
```

---

## 🤝 3. İş Süreçleri Modülü İlişkileri

### 3.1 Müşteri Yönetimi
```sql
Customer
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField)
├── code (CharField, Unique)
├── tax_number (CharField, Unique)
├── contact_person (CharField)
├── email (EmailField)
├── phone (CharField)
├── address (TextField)
├── city (CharField)
├── customer_type (CharField: individual/corporate)
├── shipping_address (TextField)
├── billing_address (TextField)
├── credit_limit (DecimalField)
├── payment_terms_days (PositiveIntegerField)
└── is_active (Boolean)

CustomerContact
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── customer_id (FK → Customer.id)
├── first_name (CharField)
├── last_name (CharField)
├── email (EmailField)
├── phone (CharField)
└── is_primary (Boolean)

Customer (1) ←→ (N) CustomerContact [one_to_many: contacts]
Customer (1) ←→ (N) SalesOrder [one_to_many]
Customer (1) ←→ (N) WorkOrder [one_to_many]
```

### 3.2 Tedarikçi Yönetimi
```sql
Supplier
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField)
├── code (CharField, Unique)
├── tax_number (CharField, Unique)
├── contact_person (CharField)
├── email (EmailField)
├── phone (CharField)
├── address (TextField)
├── city (CharField)
├── payment_terms (CharField)
└── is_active (Boolean)

SupplierContact
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── supplier_id (FK → Supplier.id)
├── first_name (CharField)
├── last_name (CharField)
├── email (EmailField)
├── phone (CharField)
└── is_primary (Boolean)

Supplier (1) ←→ (N) SupplierContact [one_to_many: contacts]
Supplier (1) ←→ (N) PurchaseOrder [one_to_many]
```

---

## 📦 4. Ürün ve Malzeme Modülü İlişkileri

### 4.1 Ürün Hiyerarşisi
```sql
ProductCategory
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField, Unique)
├── code (CharField, Unique)
├── description (TextField)
├── parent_category_id (FK → ProductCategory.id) [Self-Reference]
└── is_active (Boolean)

Product
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── category_id (FK → ProductCategory.id)
├── sku (CharField, Unique)
├── name (CharField)
├── description (TextField)
├── short_description (CharField)
├── brand (CharField)
├── model (CharField)
├── barcode (CharField, Unique)
├── internal_code (CharField)
├── manufacturer_part_number (CharField)
├── gtip_code (CharField)
├── weight (DecimalField)
├── dimensions (CharField)
├── volume (DecimalField)
├── color (CharField)
├── size (CharField)
├── unit_price (DecimalField)
├── cost_price (DecimalField)
├── currency (CharField)
├── unit_of_measure (CharField)
├── min_stock_level (DecimalField)
├── max_stock_level (DecimalField)
├── reorder_point (DecimalField)
├── safety_stock (DecimalField)
├── shelf_life_days (IntegerField)
├── lead_time_days (IntegerField)
├── manufacturing_time_days (IntegerField)
├── lot_tracking (Boolean)
├── serial_tracking (Boolean)
├── quality_grade (CharField)
├── origin_country (CharField)
├── discount_applicable (Boolean)
├── tax_rate (DecimalField)
└── commission_rate (DecimalField)

ProductCategory (1) ←→ (N) Product [one_to_many]
ProductCategory (1) ←→ (N) ProductCategory [Self-Reference: parent_category]
Product (1) ←→ (N) SalesOrderItem [one_to_many]
Product (1) ←→ (N) PurchaseOrderItem [one_to_many]
Product (1) ←→ (N) BOMComponent [one_to_many]
Product (1) ←→ (N) QualityControlPlan [one_to_many]
```

### 4.2 Malzeme Yönetimi
```sql
Material
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField, Unique)
├── code (CharField, Unique)
├── description (TextField)
├── unit (CharField)
├── stock_quantity (DecimalField)
├── cost (DecimalField)
├── minimum_stock_level (DecimalField)
├── material_code (CharField) [Alias]
├── unit_of_measure (CharField) [Alias]
├── standard_cost (DecimalField) [Alias]
└── is_active (Boolean)

Material (1) ←→ (N) BOMComponent [one_to_many]
Material (1) ←→ (N) PurchaseOrderItem [one_to_many]
Material (1) ←→ (N) InventoryMovement [one_to_many]
```

---

## 📋 5. Sipariş Modülü İlişkileri

### 5.1 Satınalma Siparişi İlişkileri
```sql
PurchaseOrder
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── supplier_id (FK → Supplier.id)
├── order_no (CharField, Unique)
├── order_date (DateField)
├── expected_delivery_date (DateField)
├── status (CharField)
├── total_amount (DecimalField)
└── notes (TextField)

PurchaseOrderItem
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── order_id (FK → PurchaseOrder.id)
├── product_id (FK → Product.id)
├── quantity (DecimalField)
├── unit_price (DecimalField)
└── tax_rate (DecimalField)

PurchaseOrder (1) ←→ (N) PurchaseOrderItem [one_to_many: items]
Supplier (1) ←→ (N) PurchaseOrder [one_to_many]
Product (1) ←→ (N) PurchaseOrderItem [one_to_many]
```

### 5.2 Satış Siparişi İlişkileri
```sql
SalesOrder
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── customer_id (FK → Customer.id)
├── order_number (CharField, Unique)
├── order_date (DateField)
├── delivery_date (DateField)
├── status (CharField: draft/pending/confirmed/shipped/delivered/cancelled)
├── total_amount (DecimalField)
├── currency (CharField)
├── shipping_address (TextField)
├── billing_address (TextField)
├── payment_terms (CharField)
└── notes (TextField)

SalesOrderItem
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── order_id (FK → SalesOrder.id)
├── product_id (FK → Product.id)
├── quantity (DecimalField)
├── unit_price (DecimalField)
├── discount_rate (DecimalField)
├── tax_rate (DecimalField)
├── delivery_date (DateField)
└── notes (TextField)

SalesOrder (1) ←→ (N) SalesOrderItem [one_to_many: items]
Customer (1) ←→ (N) SalesOrder [one_to_many]
Product (1) ←→ (N) SalesOrderItem [one_to_many]
```

---

## 🏭 6. Üretim Modülü İlişkileri

### 6.1 Üretim İstasyonu ve Hat İlişkileri
```sql
ProductionStation
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── department_id (FK → Department.id)
├── name (CharField)
├── code (CharField, Unique)
├── description (TextField)
├── capacity (PositiveIntegerField, Default: 1)
└── is_active (Boolean, Default: True)

ProductionLine
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField)
├── code (CharField, Unique)
├── description (TextField)
└── is_active (Boolean, Default: True)

ProductionLine (N) ←→ (N) ProductionStation [ManyToMany: stations]
Department (1) ←→ (N) ProductionStation [one_to_many: production_stations]
```

### 6.2 Ürün Reçetesi (BOM) İlişkileri
```sql
BOM
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── product_id (FK → Product.id)
├── material_id (FK → Material.id)
└── quantity (DecimalField, max_digits=10, decimal_places=4)

BillOfMaterials (Proxy Model of BOM)
├── Same fields as BOM
└── [Backward compatibility alias]

Product (1) ←→ (N) BOM [one_to_many: boms]
Material (1) ←→ (N) BOM [one_to_many]
```

### 6.3 Üretim Siparişi İlişkileri
```sql
ProductionOrder
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── order_number (CharField, Unique, db_column='order_no')
├── product_id (FK → Product.id)
├── quantity_to_produce (DecimalField, db_column='quantity')
├── warehouse_id (FK → inventory.Warehouse.id)
├── planned_start_date (DateField)
├── planned_end_date (DateField)
└── status (CharField, Default: 'planned')

Product (1) ←→ (N) ProductionOrder [one_to_many]
Warehouse (1) ←→ (N) ProductionOrder [one_to_many]
```

---

## 🔍 7. Kalite Kontrol Modülü İlişkileri

### 7.1 Kalite Kontrol Planı İlişkileri
```sql
QualityControlPlan
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── product_id (FK → Product.id)
├── plan_name (CharField)
├── plan_code (CharField, Unique)
├── description (TextField)
├── sampling_size (IntegerField)
├── acceptance_criteria (TextField)
└── is_active (Boolean)

QualityInspection
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── plan_id (FK → QualityControlPlan.id)
├── inspector_id (FK → Employee.id)
├── inspection_date (DateTimeField)
├── batch_number (CharField)
├── result (CharField: pass/fail/pending)
├── notes (TextField)
└── is_completed (Boolean)

Product (1) ←→ (N) QualityControlPlan [one_to_many]
QualityControlPlan (1) ←→ (N) QualityInspection [one_to_many]
Employee (1) ←→ (N) QualityInspection [one_to_many: inspector]
```

### 7.2 Kontrol Formları İlişkileri
```sql
IncomingControlForm
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── control_no (CharField, Unique)
├── material_id (FK → Material.id)
├── supplier_id (FK → Supplier.id)
├── inspection_date (DateField)
├── batch_number (CharField)
├── quantity (DecimalField)
├── result (CharField: pass/fail/conditional)
└── notes (TextField)

InProcessControlForm
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── control_no (CharField, Unique)
├── product_id (FK → Product.id)
├── work_order_id (FK → WorkOrder.id)
├── inspection_date (DateField)
├── production_station_id (FK → ProductionStation.id)
├── result (CharField: pass/fail/conditional)
└── notes (TextField)

FinalControlForm
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── control_no (CharField, Unique)
├── product_id (FK → Product.id)
├── inspection_date (DateField)
├── lot_number (CharField)
├── quantity (DecimalField)
├── ready_for_shipment (Boolean)
├── result (CharField: pass/fail/conditional)
└── notes (TextField)

Material (1) ←→ (N) IncomingControlForm [one_to_many]
Supplier (1) ←→ (N) IncomingControlForm [one_to_many]
Product (1) ←→ (N) InProcessControlForm [one_to_many]
WorkOrder (1) ←→ (N) InProcessControlForm [one_to_many]
ProductionStation (1) ←→ (N) InProcessControlForm [one_to_many]
Product (1) ←→ (N) FinalControlForm [one_to_many]
```

---

## 💰 8. Finans Modülü İlişkileri

### 8.1 Fatura İlişkileri
```sql
Invoice
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── customer_id (FK → Customer.id)
├── sales_order_id (FK → SalesOrder.id)
├── invoice_no (CharField, Unique)
├── invoice_date (DateField, Default: timezone.now)
├── due_date (DateField, Default: timezone.now)
├── total_amount (DecimalField, max_digits=15)
├── status (CharField, Default: 'draft')
└── is_paid (BooleanField, Default: False)

Customer (1) ←→ (N) Invoice [one_to_many]
SalesOrder (1) ←→ (N) Invoice [one_to_many]
```

### 8.2 Ödeme İlişkileri
```sql
Payment
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── invoice_id (FK → Invoice.id)
├── payment_date (DateField)
├── amount (DecimalField, max_digits=15)
└── payment_method (CharField)

Invoice (1) ←→ (N) Payment [one_to_many]
```

### 8.3 Hesap Planı İlişkileri
```sql
ChartOfAccounts
├── id (AutoField, PK)
├── account_code (CharField, Unique, Default: 'DEFAULT')
├── account_name (CharField, Default: 'Default Account')
├── account_type (CharField, Default: 'Default Type')
└── parent_account_id (FK → ChartOfAccounts.id) [Self-Reference]

ChartOfAccounts (1) ←→ (N) ChartOfAccounts [Self-Reference: parent_account]

Expense
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── date (DateField)
├── category (CharField, Choices: EXPENSE_CATEGORY_CHOICES)
├── amount (DecimalField, max_digits=12)
├── description (TextField)
├── receipt (FileField, upload_to='expenses/receipts/')
└── status (CharField, Choices: STATUS_CHOICES, Default: 'pending')
```

---

## 📊 9. Envanter Modülü İlişkileri

### 9.1 Envanter Kaydı İlişkileri
```sql
InventoryRecord
├── id (UUID, PK)
├── item_type (CharField)
├── item_id (PositiveIntegerField)
├── warehouse_id (FK → Warehouse.id)
├── quantity (DecimalField)
├── unit_cost (DecimalField)
└── last_updated (DateTimeField)

Warehouse
├── id (UUID, PK)
├── name (CharField)
├── code (CharField, Unique)
├── address (TextField)
├── manager_id (FK → Employee.id)
└── is_active (Boolean)

InventoryMovement
├── id (UUID, PK)
├── item_type (CharField)
├── item_id (PositiveIntegerField)
├── warehouse_id (FK → Warehouse.id)
├── movement_type (CharField: in/out/transfer)
├── quantity (DecimalField)
├── reference_type (CharField)
├── reference_id (PositiveIntegerField)
├── movement_date (DateTimeField)
└── notes (TextField)

Warehouse (1) ←→ (N) InventoryRecord [one_to_many]
Employee (1) ←→ (N) Warehouse [one_to_many: manager]
Warehouse (1) ←→ (N) InventoryMovement [one_to_many]

# Generic Relations for InventoryRecord and InventoryMovement
Product (1) ←→ (N) InventoryRecord [GenericRelation]
Material (1) ←→ (N) InventoryRecord [GenericRelation]
Product (1) ←→ (N) InventoryMovement [GenericRelation]
Material (1) ←→ (N) InventoryMovement [GenericRelation]
```

---

## 📝 10. Görev Yönetimi Modülü İlişkileri

### 10.1 Todo Sistemi İlişkileri
```sql
TodoCategory
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── name (CharField, Unique)
├── description (TextField)
├── color (CharField)
└── is_active (Boolean)

Todo
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── category_id (FK → TodoCategory.id)
├── assigned_to_id (FK → User.id)
├── title (CharField)
├── description (TextField)
├── priority (CharField: low/medium/high/critical)
├── status (CharField: pending/in_progress/completed/cancelled)
├── due_date (DateField)
├── estimated_hours (DecimalField)
├── actual_hours (DecimalField)
├── started_at (DateTimeField)
├── completed_at (DateTimeField)
├── tags (CharField)
├── notes (TextField)
└── is_deleted (Boolean)

TodoComment
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── todo_id (FK → Todo.id)
├── author_id (FK → User.id)
├── content (TextField)
└── is_internal (Boolean)

TodoCategory (1) ←→ (N) Todo [one_to_many]
User (1) ←→ (N) Todo [one_to_many: assigned_to]
Todo (1) ←→ (N) TodoComment [one_to_many: comments]
User (1) ←→ (N) TodoComment [one_to_many: todo_comments]
```

---

## 📝 11. Kullanıcı Yönetimi Modülü İlişkileri

### 11.1 Kullanıcı Profil Sistemi İlişkileri
```sql
User (Django Built-in)
├── id (AutoField, PK)
├── username (CharField, Unique)
├── email (EmailField)
├── first_name (CharField)
├── last_name (CharField)
├── is_active (Boolean)
├── is_staff (Boolean)
├── is_superuser (Boolean)
├── date_joined (DateTimeField)
└── last_login (DateTimeField)

UserRole
├── id (AutoField, PK)
├── name (CharField, Unique)
└── description (TextField)

UserProfile
├── id (AutoField, PK)
├── user_id (OneToOneField → User.id)
├── role_id (ForeignKey → UserRole.id)
└── phone_number (CharField)

Permission
├── id (AutoField, PK)
├── name (CharField, Unique)
├── codename (CharField, Unique)
└── description (TextField)

UserRolePermission
├── id (AutoField, PK)
├── role_id (ForeignKey → UserRole.id)
└── permission_id (ForeignKey → Permission.id)

User (1) ←→ (1) Employee [OneToOne]
User (1) ←→ (1) UserProfile [OneToOne: profile]
UserRole (1) ←→ (N) UserProfile [one_to_many]
UserRole (N) ←→ (N) Permission [ManyToMany through UserRolePermission]
User (N) ←→ (N) Permission [ManyToMany through Group]
```

## 🏭 12. Üretim Süreç Yönetimi İlişkileri

### 12.1 Üretim İstasyonu ve Hat İlişkileri
```sql
ProductionStation
├── id (AutoField, PK)
├── name (CharField)
├── description (TextField)
└── is_active (Boolean, Default: True)

ProductionLine
├── id (AutoField, PK)
├── name (CharField)
├── description (TextField)
└── stations (ManyToManyField → ProductionStation.id)

ProductionLine (N) ←→ (N) ProductionStation [ManyToMany: lines]
```

### 12.2 Üretim Süreç Günlüğü İlişkileri
```sql
ProductionProcessLog
├── id (AutoField, PK)
├── work_order_id (FK → WorkOrder.id)
├── product_id (FK → WorkOrderProduct.id)
├── station_id (FK → ProductionStation.id)
├── action_type (CharField, Choices: Check-In/Check-Out/Stoppage-Start/Stoppage-End/Malfunction)
├── user_id (FK → User.id, SET_NULL)
├── timestamp (DateTimeField, auto_now_add=True)
├── reason (TextField, help_text="Reason for stoppage or malfunction")
└── notes (TextField)

WorkOrder (1) ←→ (N) ProductionProcessLog [one_to_many: process_logs]
WorkOrderProduct (1) ←→ (N) ProductionProcessLog [one_to_many: process_logs]
ProductionStation (1) ←→ (N) ProductionProcessLog [one_to_many: process_logs]
User (1) ←→ (N) ProductionProcessLog [one_to_many]
```

## 📊 13. Etiket Yönetimi Sistemi İlişkileri

### 13.1 Etiket Şablonu Generic Relations
```sql
LabelTemplate
├── id (AutoField, PK)
├── name (CharField, Unique, max_length=100)
├── content_type_id (FK → ContentType.id)
├── qr_code_content_fields (JSONField, Default: list)
├── width (FloatField, Default: 50, help_text="Label width in mm")
├── height (FloatField, Default: 30, help_text="Label height in mm")
├── created_at (DateTimeField, auto_now_add=True)
└── updated_at (DateTimeField, auto_now=True)

ContentType (1) ←→ (N) LabelTemplate [one_to_many]

# Generic Usage Through ContentType
Product (via ContentType) → LabelTemplate [usage context]
Customer (via ContentType) → LabelTemplate [usage context] 
Material (via ContentType) → LabelTemplate [usage context]
SalesOrder (via ContentType) → LabelTemplate [usage context]
WorkOrder (via ContentType) → LabelTemplate [usage context]

# QR Code Field Mapping Examples
Product → qr_code_content_fields: ['sku', 'name', 'barcode', 'lot_tracking']
Customer → qr_code_content_fields: ['code', 'name', 'tax_number']
Material → qr_code_content_fields: ['code', 'name', 'batch_number']
WorkOrder → qr_code_content_fields: ['wo_no', 'lot_no', 'customer_order_no']
```

## 📋 14. Todo Yönetimi Sistemi İlişkileri

### 14.1 Todo Kategori ve Görev İlişkileri
```sql
TodoCategory
├── id (UUID, PK)
├── name (CharField, Unique, max_length=100)
├── description (TextField, max_length=500)
├── color (CharField, max_length=7, Default: '#007bff')
├── icon (CharField, max_length=50, Default: 'fas fa-tasks')
├── is_active (Boolean, Default: True)
├── created_at (DateTimeField, auto_now_add=True)
└── updated_at (DateTimeField, auto_now=True)

Todo
├── id (UUID, PK)
├── title (CharField, max_length=200)
├── description (TextField, max_length=2000)
├── category_id (FK → TodoCategory.id)
├── priority (CharField, Choices: low/medium/high/critical)
├── status (CharField, Choices: pending/in_progress/completed/cancelled)
├── assigned_to_id (FK → User.id)
├── created_by_id (FK → User.id)
├── due_date (DateTimeField)
├── estimated_hours (DecimalField, max_digits=5, decimal_places=2)
├── actual_hours (DecimalField, max_digits=5, decimal_places=2)
├── started_at (DateTimeField)
├── completed_at (DateTimeField)
├── tags (CharField, max_length=200)
├── notes (TextField)
└── is_deleted (Boolean, Default: False)

TodoComment
├── id (UUID, PK)
├── todo_id (FK → Todo.id)
├── author_id (FK → User.id)
├── content (TextField, max_length=1000)
└── is_internal (Boolean, Default: False)

TodoCategory (1) ←→ (N) Todo [one_to_many: todos]
User (1) ←→ (N) Todo [one_to_many: assigned_todos]
User (1) ←→ (N) Todo [one_to_many: created_todos]
Todo (1) ←→ (N) TodoComment [one_to_many: comments]
User (1) ←→ (N) TodoComment [one_to_many: todo_comments]
```

## ⚙️ 15. Sistem Ayarları İlişkileri

### 15.1 Global ve Şirket Ayarları
```sql
GlobalSetting
├── id (AutoField, PK)
├── key (CharField, Unique, max_length=255)
└── value (TextField)

CompanySetting
├── id (UUID, PK)
├── company_id (FK → Company.id)
├── key (CharField)
├── value (TextField)
└── setting_type (CharField)

Company (1) ←→ (N) CompanySetting [one_to_many]
```

## 📈 16. Raporlama Sistemi Güncellenmiş İlişkileri

### 16.1 Finansal Rapor İlişkileri
```sql
FinancialReport
├── id (AutoField, PK)
├── company_id (FK → Company.id)
├── report_name (CharField, max_length=200)
├── report_type (CharField, max_length=50)
├── period_start (DateField)
├── period_end (DateField)
├── generated_at (DateTimeField, auto_now_add=True)
└── report_data (JSONField)

Company (1) ←→ (N) FinancialReport [one_to_many]
```

---

## 🔗 Kritik İlişki Kuralları ve Kısıtlamaları

### 1. Referanssal Bütünlük Kuralları

#### CASCADE İlişkileri:
```sql
Company → Department (CASCADE)
Company → Employee (CASCADE)
Customer → CustomerContact (CASCADE)
Supplier → SupplierContact (CASCADE)
SalesOrder → SalesOrderItem (CASCADE)
PurchaseOrder → PurchaseOrderItem (CASCADE)
Todo → TodoComment (CASCADE)
WorkOrder → ProcessLog (CASCADE)
```

#### PROTECT İlişkileri:
```sql
Supplier → PurchaseOrder (PROTECT)
Customer → SalesOrder (PROTECT)
Product → SalesOrderItem (PROTECT)
Product → PurchaseOrderItem (PROTECT)
LeaveType → LeaveRequest (PROTECT)
```

#### SET_NULL İlişkileri:
```sql
Employee → Department.manager (SET_NULL)
User → Employee.user (SET_NULL on delete)
User → LeaveRequest.approved_by (SET_NULL)
User → ExpenseRequest.approved_by (SET_NULL)
```

### 2. Benzersizlik Kısıtlamaları

#### Tek Alan Benzersizlik:
```sql
Company.tax_number (UNIQUE)
Department.code (UNIQUE)
Customer.code (UNIQUE)
Customer.tax_number (UNIQUE)
Supplier.code (UNIQUE)
Supplier.tax_number (UNIQUE)
Product.sku (UNIQUE)
Product.barcode (UNIQUE)
Employee.email (UNIQUE)
Employee.employee_code (UNIQUE)
```

#### Composite Benzersizlik:
```sql
UNIQUE(company_id, role_name) - Role.name per company
UNIQUE(company_id, department_code) - Department.code per company
UNIQUE(company_id, employee_code) - Employee.code per company
```

### 3. İş Mantığı Kısıtlamaları

#### Döngüsel Referans Koruması:
```sql
Department.manager_id ≠ Department.id (Self-reference protection)
ProductCategory.parent_category_id ≠ ProductCategory.id
ChartOfAccounts.parent_account_id ≠ ChartOfAccounts.id
```

#### Veri Tutarlılığı:
```sql
LeaveRequest.start_date ≤ LeaveRequest.end_date
PayrollRecord.period_start ≤ PayrollRecord.period_end
SalesOrder.order_date ≤ SalesOrder.delivery_date
PurchaseOrder.order_date ≤ PurchaseOrder.expected_delivery_date
```

---

## 📈 Performans Optimizasyonu İpuçları

### 1. İndeks Stratejisi

#### Otomatik İndeksler:
- Tüm Primary Key'ler (UUID)
- Tüm Foreign Key'ler
- Unique alanlar

#### Manuel İndeksler:
```sql
-- Sık sorgulanan alanlar
Product.sku (db_index=True)
Product.name (db_index=True)
Employee.employee_code (db_index=True)
WorkOrder.wo_no (db_index=True)
WorkOrder.lot_no (db_index=True)
WorkOrder.status (db_index=True)
WorkOrder.planned_production_date (db_index=True)
WorkOrder.planned_shipment_date (db_index=True)
```

#### Composite İndeksler:
```sql
INDEX(company_id, is_active) -- Çoğu model için
INDEX(customer_id, order_date) -- SalesOrder için
INDEX(supplier_id, order_date) -- PurchaseOrder için
INDEX(employee_id, period_start) -- PayrollRecord için
```

### 2. Query Optimizasyonu

#### Select Related Kullanımı:
```python
# Tek seviye ilişkiler için
SalesOrder.objects.select_related('customer', 'company')
Employee.objects.select_related('user', 'department', 'role')
Product.objects.select_related('category', 'company')

# Çok seviyeli ilişkiler için
SalesOrderItem.objects.select_related(
    'order__customer',
    'product__category',
    'order__company'
)
```

#### Prefetch Related Kullanımı:
```python
# Reverse Foreign Key'ler için
Customer.objects.prefetch_related('salesorder_set__items')
Department.objects.prefetch_related('employee_set')
Todo.objects.prefetch_related('comments__author')

# ManyToMany ilişkiler için
Role.objects.prefetch_related('permissions')
ProductionLine.objects.prefetch_related('stations')
```

### 3. Veritabanı Partitioning Önerileri

#### Zaman Bazlı Partitioning:
```sql
-- Büyük transaction tabloları için
InventoryMovement (movement_date bazında)
ProcessLog (start_time bazında)
PayrollRecord (period_start bazında)
FinancialReport (period_start bazında)
```

#### Company Bazlı Partitioning:
```sql
-- Multi-tenant yapı için
SalesOrder (company_id bazında)
PurchaseOrder (company_id bazında)
Employee (company_id bazında)
```

---

## 🔒 Güvenlik ve Veri Koruma

### 1. Audit Trail Sistemi

#### Otomatik Takip Alanları:
```python
# Context7BaseModel ile sağlanan
created_by_id (FK → User.id)
updated_by_id (FK → User.id)
created_at (DateTime)
updated_at (DateTime)
version (PositiveInteger)
```

#### Change Tracking:
```python
# Model değişikliklerinin takibi
- Önceki değer → Yeni değer
- Değiştiren kullanıcı
- Değişiklik zamanı
- Değişiklik sebebi (opsiyonel)
```

### 2. Soft Delete Sistemi

```python
# Fiziksel silme yerine işaretleme
is_deleted = models.BooleanField(default=False)
deleted_at = models.DateTimeField(null=True, blank=True)
deleted_by = models.ForeignKey(User, null=True, blank=True)
```

### 3. Multi-Company İzolasyonu

```python
# Tüm sorgularda otomatik filtreleme
company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

# QuerySet override ile otomatik filtreleme
def get_queryset(self):
    return super().get_queryset().filter(
        company=self.request.user.employee.company
    )
```

---

## 📋 Sonuç ve Özet

Context7 ERP sistemi, 73 tablo ve 1,088 kayıt ile kapsamlı bir veritabanı yapısına sahiptir. Sistem:

### Ana İlişki Tipleri:
- **One-to-Many**: 156 ilişki
- **Many-to-Many**: 12 ilişki  
- **One-to-One**: 8 ilişki
- **Self-Reference**: 6 ilişki
- **Generic Relations**: 4 ilişki

### Güncellenmiş ve Eklenen Modüller:
1. **UserProfile Modülü**: OneToOne User ilişkisi, role tabanlı yetkilendirme
2. **ProductionProcessLog**: Detaylı üretim süreç takibi, action_type ile
3. **LabelTemplate**: Generic ContentType ile esnek etiket sistemi
4. **TodoCategory/Todo**: Kapsamlı görev yönetimi sistemi
5. **UserRolePermission**: Rol-izin çapraz tablosu
6. **ProductionLine/ProductionStation**: ManyToMany üretim hat ilişkisi
7. **FinancialReport**: Company bağlantısı eklendi
8. **GlobalSetting/CompanySetting**: Sistem ayarları hiyerarşisi

### Kritik İş Akışları:
1. **Satış Akışı**: Customer → SalesOrder → SalesOrderItem → Product → Invoice
2. **Satınalma Akışı**: Supplier → PurchaseOrder → PurchaseOrderItem → Product/Material
3. **Üretim Akışı**: Product → BOM → ProductionOrder → ProductionProcessLog
4. **Kalite Akışı**: Product → QualityControlPlan → QualityInspection
5. **HR Akışı**: Employee → LeaveRequest → PayrollRecord
6. **Envanter Akışı**: Product/Material → InventoryRecord → InventoryMovement
7. **İş Emri Akışı**: Customer → WorkOrder → ProductionProcessLog → ProductionStation
8. **Todo Akışı**: TodoCategory → Todo → TodoComment → User
9. **Etiket Akışı**: ContentType → LabelTemplate → Generic Model Usage
10. **Kullanıcı Akışı**: User → UserProfile → UserRole → Permission

### Performans Özellikleri:
- **UUID Primary Keys**: Güvenli ve ölçeklenebilir (TodoCategory, Todo, TodoComment)
- **İndeks Stratejisi**: 156 FK + 45 Unique + 23 Composite + Todo indexes
- **Query Optimizasyonu**: select_related/prefetch_related kullanımı
- **Caching Strategy**: Redis ile performans artırımı
- **Generic Relations**: ContentType kullanımı ile esnek ilişkiler (LabelTemplate)

### Güvenlik Özellikleri:
- **Audit Trail**: Tüm değişikliklerin takibi (Context7BaseModel inheritance)
- **Soft Delete**: Veri kaybını önleme (Todo.is_deleted)
- **Multi-Company**: İzolasyon ve güvenlik
- **Role-Based Access**: UserRole → UserProfile → User chain
- **Permission System**: UserRolePermission ile granular control

### Yeni Eklenen Özellikler:
- **Production Process Tracking**: Detaylı action_type ile üretim takibi
- **Label Management System**: Generic ContentType ile esnek etiket yönetimi
- **Comprehensive Todo System**: Priority, status, time tracking ile
- **User Profile Enhancement**: Phone, role integration
- **Production Line Management**: ManyToMany station relationships
- **Settings Hierarchy**: Global ve company-specific ayarlar
- **Financial Reporting**: Company-scoped rapor sistemi

### Generic Relations Kullanımı:
1. **LabelTemplate ↔ ContentType**: Herhangi bir model için etiket şablonu
2. **InventoryMovement ↔ Product/Material**: Generic item referansı
3. **QualityCheck ↔ Multiple Models**: Generic quality control

### İlişki Çeşitliliği:
- **Basit FK**: Customer → SalesOrder
- **Self-Reference**: ProductCategory.parent_category
- **ManyToMany**: ProductionLine ↔ ProductionStation
- **OneToOne**: User ↔ UserProfile
- **Generic FK**: LabelTemplate ↔ ContentType
- **Through Model**: UserRole ↔ Permission via UserRolePermission

Bu kapsamlı ilişki yapısı, Context7 ERP sisteminin modern işletme ihtiyaçlarını karşılayan güçlü, ölçeklenebilir ve esnek bir altyapı sağlamaktadır. Sistem artık 16 ana modül ile tam entegre bir ERP çözümü sunmaktadır.

---

**Dokümantasyon Son Güncelleme:** 20 Haziran 2025  
**Context7 ERP System v2.2.0-glassmorphism-enhanced**  
**Enhanced Database Relations: 16 Modules, 186+ İlişki** 