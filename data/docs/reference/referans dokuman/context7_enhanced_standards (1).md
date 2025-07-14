

#### 7.2.10. Raporlama ve Analitik Modülleri
```python
class ReportDefinition(BaseModel):
    """Rapor tanımları"""
    report_code = models.CharField(max_length=30, unique=True)
    report_name = models.CharField(max_length=100)
    report_category = models.CharField(max_length=50, choices=REPORT_CATEGORIES)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    data_source = models.TextField()  # SQL query veya model referansı
    parameters = models.JSONField(default=dict)  # Rapor parametreleri
    filters = models.JSONField(default=dict)  # Varsayılan filtreler
    refresh_frequency = models.CharField(max_length=20, choices=REFRESH_FREQUENCIES)
    
class DashboardWidget(BaseModel):
    """Dashboard widget tanımları"""
    widget_name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    data_query = models.TextField()
    refresh_interval = models.PositiveIntegerField(default=300)  # saniye
    position_x = models.PositiveIntegerField()
    position_y = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    configuration = models.JSONField(default=dict)
    
class UserDashboard(BaseModel):
    """Kullanıcı dashboard konfigürasyonu"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dashboard_name = models.CharField(max_length=100)
    widgets = models.ManyToManyField(DashboardWidget, through='DashboardWidgetConfig')
    is_default = models.BooleanField(default=False)
    
class ScheduledReport(BaseModel):
    """Programlı rapor gönderimi"""
    report = models.ForeignKey(ReportDefinition, on_delete=models.CASCADE)
    recipients = models.JSONField()  # Email listesi
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES)
    schedule_config = models.JSONField()  # Cron expression veya interval
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField()
    is_active = models.BooleanField(default=True)
```

#### 7.2.11. Sistem Yönetimi Modülleri
```python
class Role(BaseModel):
    """Roller"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField('auth.Permission')
    
class UserProfile(BaseModel):
    """Kullanıcı profil bilgileri"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='tr')
    timezone = models.CharField(max_length=50, default='Europe/Istanbul')
    date_format = models.CharField(max_length=20, default='DD.MM.YYYY')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    
class SystemConfiguration(BaseModel):
    """Sistem konfigürasyonu"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    data_type = models.CharField(max_length=20, choices=DATA_TYPES)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_encrypted = models.BooleanField(default=False)
    
class AuditLog(BaseModel):
    """Sistem audit logları"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=AUDIT_ACTIONS)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Notification(BaseModel):
    """Sistem bildirimleri"""
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    action_url = models.URLField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
```

#### 7.2.12. Entegrasyon Modülleri
```python
class ExternalSystem(BaseModel):
    """Harici sistem tanımları"""
    system_name = models.CharField(max_length=100)
    system_type = models.CharField(max_length=50, choices=SYSTEM_TYPES)
    api_endpoint = models.URLField()
    api_key = models.CharField(max_length=200, blank=True)
    api_secret = models.CharField(max_length=200, blank=True)
    configuration = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    
class DataSynchronization(BaseModel):
    """Veri senkronizasyon kayıtları"""
    external_system = models.ForeignKey(ExternalSystem, on_delete=models.CASCADE)
    sync_type = models.CharField(max_length=20, choices=SYNC_TYPES)
    model_name = models.CharField(max_length=50)
    local_id = models.CharField(max_length=50)
    external_id = models.CharField(max_length=50)
    last_sync = models.DateTimeField()
    sync_status = models.CharField(max_length=20, choices=SYNC_STATUS)
    error_message = models.TextField(blank=True)
    
class EInvoiceIntegration(BaseModel):
    """E-Fatura entegrasyon bilgileri"""
    integrator = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)  # Encrypted
    test_environment = models.BooleanField(default=True)
    endpoint_url = models.URLField()
    certificate_file = models.FileField(upload_to='certificates/', blank=True)
    certificate_password = models.CharField(max_length=100, blank=True)
    
class DocumentTemplate(BaseModel):
    """Doküman şablonları"""
    template_name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    template_file = models.FileField(upload_to='templates/')
    variables = models.JSONField(default=dict)  # Şablonda kullanılan değişkenler
    is_default = models.BooleanField(default=False)
```

---

## 8. Birimler Arası Bilgi Akışı ve Süreç Entegrasyonu

### 8.1. Gelişmiş Süreç Akışları

#### 8.1.1. Order-to-Cash (Siparişten Tahsilata) - Detaylı Akış
```python
# 1. Müşteri Talebi ve Teklif Süreci
class QuotationWorkflow:
    def create_quotation(self, customer_request):
        # Müşteri talebini teklif formuna dönüştür
        quotation = SalesQuotation.objects.create(
            customer=customer_request.customer,
            quotation_date=timezone.now().date(),
            valid_until=timezone.now().date() + timedelta(days=30)
        )
        
        # Ürün fiyatlarını güncelle
        self.calculate_pricing(quotation)
        
        # Onay akışını başlat
        self.start_approval_workflow(quotation)
        
        return quotation
    
    def approve_quotation(self, quotation, approver):
        quotation.status = 'APPROVED'
        quotation.save()
        
        # Müşteriye bildirim gönder
        self.send_quotation_to_customer(quotation)
        
    def convert_to_order(self, quotation):
        # Teklifi siparişe dönüştür
        order = SalesOrder.objects.create(
            quotation=quotation,
            customer=quotation.customer,
            order_date=timezone.now().date()
        )
        
        # Stok kontrolü ve rezervasyon
        self.check_and_reserve_stock(order)
        
        return order

# 2. Stok Kontrol ve Üretim Entegrasyonu
class InventoryProductionIntegration:
    def check_and_reserve_stock(self, sales_order):
        for item in sales_order.items.all():
            available_stock = self.get_available_stock(item.product)
            
            if available_stock >= item.quantity:
                # Stok rezervasyonu
                self.reserve_stock(item.product, item.quantity, sales_order)
                
                # Sevkiyat emri oluştur
                self.create_shipment_order(item)
            else:
                # Eksik miktar için üretim talebi
                shortage = item.quantity - available_stock
                self.create_production_request(item.product, shortage, sales_order)
    
    def create_production_request(self, product, quantity, sales_order):
        production_order = ProductionOrder.objects.create(
            product=product,
            planned_quantity=quantity,
            source_document=f"Sales Order: {sales_order.order_number}",
            priority='HIGH' if sales_order.is_urgent else 'NORMAL'
        )
        
        # BOM kontrolü ve malzeme rezervasyonu
        self.check_bom_materials(production_order)
        
        return production_order

# 3. Otomatik Faturalama ve Tahsilat
class AutomatedBilling:
    def process_shipment_completion(self, shipment):
        # Sevkiyat tamamlandığında otomatik fatura kes
        invoice = Invoice.objects.create(
            invoice_type='SALES',
            customer=shipment.sales_order.customer,
            invoice_date=timezone.now().date(),
            due_date=self.calculate_due_date(shipment.sales_order.customer)
        )
        
        # E-Fatura gönderimi
        self.send_e_invoice(invoice)
        
        # Tahsilat takibi başlat
        self.create_collection_schedule(invoice)
        
        return invoice
    
    def automated_collection_reminder(self):
        # Vadesi geçen faturaları tespit et
        overdue_invoices = Invoice.objects.filter(
            due_date__lt=timezone.now().date(),
            status='UNPAID'
        )
        
        for invoice in overdue_invoices:
            self.send_collection_reminder(invoice)
            self.update_customer_credit_score(invoice.customer)
```

#### 8.1.2. Procure-to-Pay (Satın Almadan Ödemeye) - Detaylı Akış
```python
# 1. Otomatik Satın Alma Tetikleme
class AutomatedProcurement:
    def monitor_stock_levels(self):
        """Stok seviyelerini izle ve otomatik satın alma tetikle"""
        low_stock_products = Product.objects.filter(
            current_stock__lte=F('minimum_stock_level')
        )
        
        for product in low_stock_products:
            self.create_purchase_request(product)
    
    def create_purchase_request(self, product):
        # Otomatik sipariş miktarı hesaplama
        order_quantity = self.calculate_order_quantity(product)
        
        purchase_request = PurchaseRequest.objects.create(
            product=product,
            quantity=order_quantity,
            requesting_department='SYSTEM',
            priority='NORMAL'
        )
        
        # Onay akışını başlat
        self.start_approval_workflow(purchase_request)
        
        return purchase_request

# 2. Tedarikçi Seçimi ve RFQ Süreci
class SupplierSelectionProcess:
    def process_approved_request(self, purchase_request):
        # Tedarikçi havuzundan uygun tedarikçileri seç
        suitable_suppliers = self.find_suitable_suppliers(
            purchase_request.product
        )
        
        if len(suitable_suppliers) > 1:
            # Çoklu tedarikçi varsa RFQ başlat
            self.create_rfq(purchase_request, suitable_suppliers)
        else:
            # Tek tedarikçi varsa direkt sipariş oluştur
            self.create_direct_purchase_order(
                purchase_request, 
                suitable_suppliers[0]
            )
    
    def evaluate_rfq_responses(self, rfq):
        """RFQ yanıtlarını otomatik değerlendir"""
        responses = rfq.responses.all()
        
        # Çok kriterli karar verme algoritması
        best_supplier = self.multi_criteria_evaluation(responses)
        
        # Kazanan tedarikçi ile sipariş oluştur
        self.create_purchase_order_from_rfq(rfq, best_supplier)

# 3. Üç Yönlü Eşleştirme (Three-Way Matching)
class ThreeWayMatching:
    def process_goods_receipt(self, goods_receipt):
        """Mal kabul işleminde üç yönlü eşleştirme"""
        purchase_order = goods_receipt.purchase_order
        
        # 1. Sipariş ile mal kabul eşleştirme
        order_match = self.match_with_purchase_order(
            goods_receipt, 
            purchase_order
        )
        
        if order_match['status'] == 'SUCCESS':
            # 2. Fatura geldiğinde eşleştirme yapılacak
            self.register_pending_invoice_match(goods_receipt)
            
            # Stok güncelleme
            self.update_inventory(goods_receipt)
            
        return order_match
    
    def process_supplier_invoice(self, supplier_invoice):
        """Tedarikçi faturası geldiğinde eşleştirme"""
        # İlgili mal kabul kayıtlarını bul
        related_receipts = GoodsReceipt.objects.filter(
            purchase_order=supplier_invoice.purchase_order,
            status='COMPLETED'
        )
        
        # Üç yönlü eşleştirme: Sipariş + Mal Kabul + Fatura
        matching_result = self.perform_three_way_match(
            supplier_invoice.purchase_order,
            related_receipts,
            supplier_invoice
        )
        
        if matching_result['status'] == 'MATCH':
            # Ödeme onayı ver
            self.approve_for_payment(supplier_invoice)
        else:
            # Uyumsuzluk varsa manuel kontrole gönder
            self.flag_for_manual_review(supplier_invoice, matching_result)
```

#### 8.1.3. Lead-to-Quote (Potansiyel Müşteriden Teklife) - CRM Entegrasyonu
```python
class CRMSalesIntegration:
    def process_lead_qualification(self, lead):
        """Lead kalifikasyon süreci"""
        # Lead scoring algoritması
        lead_score = self.calculate_lead_score(lead)
        
        if lead_score >= 70:  # Yüksek puan
            # Satış temsilcisine atama
            sales_rep = self.assign_sales_representative(lead)
            
            # Otomatik takip aktivitesi oluştur
            self.create_follow_up_activity(lead, sales_rep)
            
            # Potansiyel müşteriyi sisteme kaydet
            prospect = self.convert_lead_to_prospect(lead)
            
        return lead_score
    
    def opportunity_to_quotation(self, opportunity):
        """Satış fırsatını teklife dönüştürme"""
        quotation = SalesQuotation.objects.create(
            customer=opportunity.prospect.customer,
            opportunity=opportunity,
            quotation_date=timezone.now().date()
        )
        
        # Ürün önerilerini otomatik ekle
        self.add_recommended_products(quotation, opportunity)
        
        # Fiyat hesaplama
        self.calculate_competitive_pricing(quotation)
        
        return quotation
```

### 8.2. Gerçek Zamanlı Veri Senkronizasyonu
```python
# Django Signals ile Otomatik Süreç Tetikleme
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=SalesOrder)
def handle_sales_order_creation(sender, instance, created, **kwargs):
    if created:
        # Stok rezervasyonu başlat
        InventoryService.reserve_stock_for_order(instance)
        
        # Müşteri kredibilite kontrolü
        CreditCheckService.verify_customer_credit(instance.customer)
        
        # Üretim planlamasına bildir
        ProductionPlanningService.update_demand_forecast(instance)

@receiver(post_save, sender=ProductionOrder)
def handle_production_completion(sender, instance, **kwargs):
    if instance.status == 'COMPLETED':
        # Mamul stoğa giriş
        InventoryService.receive_finished_goods(instance)
        
        # Maliyet hesaplama
        CostingService.calculate_production_cost(instance)
        
        # Bekleyen siparişleri kontrol et
        SalesService.check_pending_orders(instance.product)

@receiver(post_save, sender=GoodsReceipt)
def handle_goods_receipt(sender, instance, created, **kwargs):
    if created:
        # Kalite kontrol süreci başlat
        QualityService.initiate_incoming_inspection(instance)
        
        # Tedarikçi performans güncelle
        SupplierService.update_delivery_performance(instance.supplier)
```

### 8.3. İş Akışı Yönetimi (Workflow Management)
```python
class WorkflowEngine:
    def __init__(self):
        self.workflow_definitions = {
            'purchase_approval': self.purchase_approval_workflow,
            'sales_approval': self.sales_approval_workflow,
            'expense_approval': self.expense_approval_workflow,
        }
    
    def start_workflow(self, workflow_type, document_id, initiator):
        workflow_def = self.workflow_definitions[workflow_type]
        
        workflow_instance = WorkflowInstance.objects.create(
            workflow_type=workflow_type,
            document_id=document_id,
            status='STARTED',
            current_step=1,
            initiator=initiator
        )
        
        # İlk adımı çalıştır
        self.execute_step(workflow_instance)
        
        return workflow_instance
    
    def purchase_approval_workflow(self, instance):
        """Satın alma onay akışı"""
        purchase_request = PurchaseRequest.objects.get(id=instance.document_id)
        
        if purchase_request.total_amount < 1000:
            # Düşük tutar - departman müdürü onayı yeter
            return self.get_department_manager_approval(purchase_request)
        elif purchase_request.total_amount < 10000:
            # Orta tutar - satın alma müdürü + finans müdürü
            return self.get_multi_level_approval(
                purchase_request, 
                ['purchasing_manager', 'finance_manager']
            )
        else:
            # Yüksek tutar - genel müdür onayı gerekli
            return self.get_executive_approval(purchase_request)
```

---

## 9. API Tasarım Standartları

### 9.1. RESTful API Prensipleri
**Kural:** API'lar REST standartlarına uygun tasarlanmalı.

**Uygulama:**
```python
# URL Yapısı
/api/v1/customers/                    # GET, POST
/api/v1/customers/{id}/               # GET, PUT, PATCH, DELETE
/api/v1/customers/{id}/orders/        # İlişkili kaynaklara erişim
/api/v1/customers/{id}/orders/{order_id}/  # Nested resources

# HTTP Status Codes
200 OK - Başarılı GET, PUT, PATCH
201 Created - Başarılı POST
204 No Content - Başarılı DELETE
400 Bad Request - Geçersiz istek
401 Unauthorized - Kimlik doğrulama hatası
403 Forbidden - Yetki hatası
404 Not Found - Kaynak bulunamadı
422 Unprocessable Entity - Validasyon hatası
500 Internal Server Error - Sunucu hatası
```

### 9.2. API Versiyonlama
**Kural:** API versiyonları URL'de belirtilmeli.

**Uygulama:**
```python
# URL Versioning
/api/v1/customers/
/api/v2/customers/

# Header Versioning (alternatif)
Accept: application/vnd.context7.v1+json

# Deprecation Strategy
class APIVersioning:
    v1_deprecation_date = "2024-12-31"
    v2_current_version = True
    v3_beta_version = True
```

### 9.3. API Güvenlik
**Kural:** API güvenliği çok katmanlı olmalı.

**Uygulama:**
```python
# JWT Token Authentication
class JWTAuthentication:
    def authenticate(self, request):
        token = self.get_token_from_header(request)
        if token:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return (user, token)
        return None

# Rate Limiting
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# API Key Authentication (3rd party integrations)
class APIKeyAuthentication:
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')
        if api_key:
            try:
                api_client = APIClient.objects.get(api_key=api_key, is_active=True)
                return (api_client.user, api_key)
            except APIClient.DoesNotExist:
                pass
        return None
```

### 9.4. API Dokümantasyonu
**Kural:** API dokümantasyonu otomatik oluşturulmalı ve güncel tutulmalı.

**Uygulama:**
```python
# OpenAPI Schema with drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'Context7 ERP API',
    'DESCRIPTION': 'Context7 ERP System REST API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'COMPONENT_NO_READ_ONLY_REQUIRED': True,
}

# API Documentation with Examples
class CustomerViewSet(viewsets.ModelViewSet):
    """
    Customer management endpoints
    
    list: Return a list of all customers
    create: Create a new customer
    retrieve: Return a specific customer
    update: Update a specific customer
    destroy: Delete a specific customer
    """
    
    @extend_schema(
        summary="Create a new customer",
        description="Create a new customer with validation",
        examples=[
            OpenApiExample(
                "Customer Creation Example",
                value={
                    "name": "Acme Corp",
                    "tax_number": "1234567890",
                    "email": "info@acme.com"
                }
            )
        ]
    )
    def create(self, request):
        pass
```

---

## 10. Test Stratejileri

### 10.1. Test Piramidi
**Kural:** Test stratejisi piramit modeline uygun olmalı.

**Uygulama:**
```
     /\     E2E Tests (10%)
    /  \    
   /____\   Integration Tests (20%)
  /      \  
 /________\ Unit Tests (70%)
```

### 10.2. Unit Testing
**Kural:** Her fonksiyon için birim testleri yazılmalı.

**Uygulama:**
```python
# Test Organization
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_workflows.py
└── e2e/
    └── test_user_journeys.py

# Unit Test Example
class TestCustomerService(TestCase):
    def setUp(self):
        self.customer_service = CustomerService()
        self.sample_customer_data = {
            'name': 'Test Customer',
            'tax_number': '1234567890'
        }
    
    def test_create_customer_success(self):
        customer = self.customer_service.create_customer(
            self.sample_customer_data
        )
        self.assertIsNotNone(customer.id)
        self.assertEqual(customer.name, 'Test Customer')
    
    def test_create_customer_duplicate_tax_number(self):
        # İlk müşteri oluştur
        self.customer_service.create_customer(self.sample_customer_data)
        
        # Aynı vergi numarası ile ikinci müşteri oluşturmaya çalış
        with self.assertRaises(ValidationError):
            self.customer_service.create_customer(self.sample_customer_data)
    
    @patch('apps.customers.services.send_welcome_email')
    def test_create_customer_sends_welcome_email(self, mock_email):
        customer = self.customer_service.create_customer(
            self.sample_customer_data
        )
        mock_email.assert_called_once_with(customer)
```

### 10.3. Integration Testing
**Kural:** Modüller arası entegrasyon testleri yapılmalı.

**Uygulama:**
```python
class TestOrderToDeliveryFlow(TransactionTestCase):
    def test_complete_order_flow(self):
        # 1. Müşteri oluştur
        customer = CustomerFactory()
        
        # 2. Ürün oluştur ve stok ekle
        product = ProductFactory()
        InventoryFactory(product=product, quantity=100)
        
        # 3. Sipariş oluştur
        order_data = {
            'customer': customer.id,
            'items': [{'product': product.id, 'quantity': 10}]
        }
        response = self.client.post('/api/v1/orders/', order_data)
        self.assertEqual(response.status_code,# 🚀 Context7 ERP Sistemi - Gelişmiş Geliştirme Standartları ve Mimari

Bu belge, Context7 ERP projesinde uygulanacak olan geliştirme, dökümantasyon, test ve yönetim süreçlerine yönelik gelişmiş standartları ve sistemin detaylı mimari yapısını tanımlar.

## 📋 İçindekiler
1. [Proje Dökümantasyonu ve Haritalama](#1-proje-dökümantasyonu-ve-haritalama)
2. [Veritabanı Yönetim Standartları](#2-veritabanı-yönetim-standartları)
3. [Kod Geliştirme Standartları](#3-kod-geliştirme-standartları)
4. [Bağımlılık ve Dağıtım Yönetimi](#4-bağımlılık-ve-dağıtım-yönetimi)
5. [Güvenlik Standartları](#5-güvenlik-standartları)
6. [Performans ve Ölçeklenebilirlik](#6-performans-ve-ölçeklenebilirlik)
7. [Uygulama Mimarisi ve Veri Yapısı](#7-uygulama-mimarisi-ve-veri-yapısı)
8. [Birimler Arası Bilgi Akışı](#8-birimler-arası-bilgi-akışı)
9. [API Tasarım Standartları](#9-api-tasarım-standartları)
10. [Test Stratejileri](#10-test-stratejileri)
11. [Deployment ve DevOps](#11-deployment-ve-devops)
12. [Monitoring ve Logging](#12-monitoring-ve-logging)

---

## 1. Proje Dökümantasyonu ve Haritalama

### 1.1. Dosya Haritası (filemap.md)
**Kural:** Proje dizin yapısındaki her dosya ve klasörün amacı, sorumluluğu ve projedeki rolü net şekilde açıklanmalıdır.

**Uygulama:**
```markdown
# Context7 Dosya Haritası
├── apps/                    # Django uygulamaları
│   ├── authentication/     # Kullanıcı kimlik doğrulama
│   ├── customers/          # Müşteri yönetimi
│   ├── suppliers/          # Tedarikçi yönetimi
│   ├── products/           # Ürün katalogu
│   ├── inventory/          # Stok yönetimi
│   ├── sales/              # Satış süreçleri
│   ├── procurement/        # Satın alma
│   ├── production/         # Üretim yönetimi
│   ├── finance/            # Finans ve muhasebe
│   ├── hr/                 # İnsan kaynakları
│   └── reporting/          # Raporlama ve analitik
├── core/                   # Temel sistem bileşenleri
├── static/                 # Statik dosyalar (CSS, JS, img)
├── templates/              # HTML şablonları
├── tests/                  # Test dosyaları
├── docs/                   # Dokümantasyon
└── requirements/           # Bağımlılık dosyaları
```

### 1.2. Site Haritası (sitemap.xml)
**Kural:** SEO standartlarına uygun dinamik site haritası oluşturulmalı.

**Uygulama:**
- Django sitemap framework kullanılmalı
- Her modül için ayrı sitemap sınıfı oluşturulmalı
- Güncellenme sıklığı ve öncelik değerleri belirlenmeli

### 1.3. API Dokümantasyonu
**Kural:** Tüm API endpoint'leri OpenAPI 3.0 standardında dokümante edilmeli.

**Uygulama:**
- Django REST Framework + drf-spectacular kullanılmalı
- Otomatik Swagger UI oluşturulmalı
- Örnek istekler ve yanıtlar dahil edilmeli

---

## 2. Veritabanı Yönetim Standartları

### 2.1. Model Tasarım Prensipleri
**Kural:** Veritabanı modelleri SOLID prensiplere uygun tasarlanmalı.

**Uygulama:**
```python
# Temel Abstract Model
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
```

### 2.2. Veritabanı İndeksleme Stratejisi
**Kural:** Performans kritik alanlar için uygun indeksler oluşturulmalı.

**Uygulama:**
- Arama sık yapılan alanlar: `db_index=True`
- Composite indeksler: `indexes = [models.Index(fields=['field1', 'field2'])]`
- Unique constraint'ler: `unique_together` veya `UniqueConstraint`

### 2.3. Migration Yönetimi
**Kural:** Veritabanı değişiklikleri güvenli ve geri dönülebilir olmalı.

**Uygulama:**
- Her migration için rollback scripti hazırlanmalı
- Data migration'lar ayrı dosyalarda tutulmalı
- Production deployment öncesi staging'de test edilmeli

---

## 3. Kod Geliştirme Standartları

### 3.1. Python ve Django Standartları
**Kural:** PEP 8 ve Django best practices'e uyulmalı.

**Uygulama:**
```python
# Kod kalite araçları
- black (kod formatlama)
- isort (import sıralama)
- flake8 (linting)
- mypy (type checking)
- bandit (güvenlik)
```

### 3.2. Clean Architecture Uygulama
**Kural:** Business logic, framework'den bağımsız tutulmalı.

**Uygulama:**
```
apps/customers/
├── models.py           # Django modelleri
├── serializers.py      # API serializers
├── views.py           # API views
├── services.py        # Business logic
├── repositories.py    # Data access layer
└── validators.py      # Custom validators
```

### 3.3. Error Handling Standartları
**Kural:** Hata yönetimi tutarlı ve kapsamlı olmalı.

**Uygulama:**
```python
# Custom Exception Classes
class Context7Exception(Exception):
    """Base exception for Context7"""
    pass

class ValidationError(Context7Exception):
    """Validation errors"""
    pass

class BusinessRuleViolation(Context7Exception):
    """Business rule violations"""
    pass
```

---

## 4. Bağımlılık ve Dağıtım Yönetimi

### 4.1. Dependency Management
**Kural:** Bağımlılıklar çevre bazlı yönetilmeli.

**Uygulama:**
```
requirements/
├── base.txt        # Temel bağımlılıklar
├── local.txt       # Geliştirme ortamı
├── staging.txt     # Test ortamı
└── production.txt  # Üretim ortamı
```

### 4.2. Environment Configuration
**Kural:** Konfigürasyon bilgileri environment variables ile yönetilmeli.

**Uygulama:**
- django-environ kullanılmalı
- .env.example dosyası sağlanmalı
- Hassas bilgiler version control'e commit edilmemeli

---

## 5. Güvenlik Standartları

### 5.1. Authentication & Authorization
**Kural:** JWT tabanlı authentication kullanılmalı.

**Uygulama:**
```python
# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### 5.2. Permission System
**Kural:** Granular izin sistemi uygulanmalı.

**Uygulama:**
```python
# Custom Permissions
class CanViewCustomers(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('customers.view_customer')
        
class CanManageOwnCustomers(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
```

### 5.3. Data Encryption
**Kural:** Hassas veriler şifrelenerek saklanmalı.

**Uygulama:**
- django-cryptography kullanılmalı
- PII veriler için field-level encryption
- Database backup'ları şifreli olmalı

---

## 6. Performans ve Ölçeklenebilirlik

### 6.1. Caching Strategy
**Kural:** Çok katmanlı cache stratejisi uygulanmalı.

**Uygulama:**
```python
# Cache Layers
1. Database Query Cache (Redis)
2. Template Fragment Cache
3. API Response Cache
4. Static File Cache (CDN)
```

### 6.2. Database Optimization
**Kural:** Veritabanı performansı sürekli izlenmeli.

**Uygulama:**
- select_related ve prefetch_related kullanımı
- N+1 query problemlerinin önlenmesi
- Database connection pooling
- Read replica kullanımı

### 6.3. Asynchronous Processing
**Kural:** Uzun süren işlemler asenkron yapılmalı.

**Uygulama:**
```python
# Celery Task Configuration
@shared_task
def process_bulk_invoice():
    # Bulk operations
    pass

@shared_task
def send_notification_email():
    # Email sending
    pass
```

---

## 7. Uygulama Mimarisi ve Veri Yapısı

### 7.1. Modüler Mimari
**Kural:** Her iş domain'i ayrı Django app olarak organize edilmeli.

### 7.2. Detaylı Veri Modelleri

#### 7.2.1. Müşteri Yönetimi Modülleri
```python
class Customer(BaseModel):
    """Ana müşteri modeli"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CUSTOMER_CATEGORIES)
    type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    tax_office = models.CharField(max_length=100)
    tax_number = models.CharField(max_length=20)
    trade_registry_number = models.CharField(max_length=30, blank=True)
    mersis_number = models.CharField(max_length=20, blank=True)
    
class CustomerAddress(BaseModel):
    """Müşteri adres bilgileri"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    street_address = models.TextField()
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, default='Turkey')
    
class CustomerContact(BaseModel):
    """Müşteri iletişim bilgileri"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPES)
    value = models.CharField(max_length=200)
    is_primary = models.BooleanField(default=False)
```

#### 7.2.2. Ürün Yönetimi Modülleri
```python
class ProductCategory(BaseModel):
    """Ürün kategorileri"""
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=20, unique=True)
    
class Product(BaseModel):
    """Ana ürün modeli"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    unit = models.CharField(max_length=10, choices=UNITS)
    barcode = models.CharField(max_length=50, blank=True)
    gtip_code = models.CharField(max_length=20, blank=True)
    
class ProductSpecification(BaseModel):
    """Ürün teknik özellikleri"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification_name = models.CharField(max_length=100)
    specification_value = models.CharField(max_length=200)
    
class ProductPricing(BaseModel):
    """Ürün fiyatlandırma"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_list = models.ForeignKey('PriceList', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
```

#### 7.2.3. Stok Yönetimi Modülleri
```python
class Warehouse(BaseModel):
    """Depo tanımları"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    warehouse_type = models.CharField(max_length=20, choices=WAREHOUSE_TYPES)
    address = models.TextField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    responsible_person = models.ForeignKey(User, on_delete=models.PROTECT)
    
class WarehouseLocation(BaseModel):
    """Depo lokasyonları (raf sistemi)"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    code = models.CharField(max_length=30)
    aisle = models.CharField(max_length=10)
    rack = models.CharField(max_length=10)
    level = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    
class StockMovement(BaseModel):
    """Stok hareketleri"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    location = models.ForeignKey(WarehouseLocation, on_delete=models.PROTECT, null=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    reference_document = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    unit_cost = models.DecimalField(max_digits=15, decimal_places=4, null=True)
    lot_number = models.CharField(max_length=50, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
```

#### 7.2.4. Satış Yönetimi Modülleri
```python
class SalesQuotation(BaseModel):
    """Satış teklifleri"""
    quotation_number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    quotation_date = models.DateField()
    valid_until = models.DateField()
    status = models.CharField(max_length=20, choices=QUOTATION_STATUS)
    customer_reference = models.CharField(max_length=100, blank=True)
    delivery_terms = models.TextField(blank=True)
    payment_terms = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
class SalesOrder(BaseModel):
    """Satış siparişleri"""
    order_number = models.CharField(max_length=30, unique=True)
    quotation = models.ForeignKey(SalesQuotation, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS)
    customer_order_number = models.CharField(max_length=100, blank=True)
    shipping_address = models.ForeignKey(CustomerAddress, on_delete=models.PROTECT)
    
class SalesOrderItem(BaseModel):
    """Satış sipariş kalemleri"""
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    unit_price = models.DecimalField(max_digits=15, decimal_places=4)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    delivered_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
```

#### 7.2.5. Satın Alma Modülleri
```python
class PurchaseRequest(BaseModel):
    """Satın alma talepleri"""
    request_number = models.CharField(max_length=30, unique=True)
    requesting_department = models.CharField(max_length=100)
    requester = models.ForeignKey(User, on_delete=models.PROTECT)
    request_date = models.DateField()
    required_date = models.DateField()
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS)
    justification = models.TextField()
    
class RFQ(BaseModel):
    """Teklif isteme (Request for Quotation)"""
    rfq_number = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    issue_date = models.DateField()
    response_deadline = models.DateField()
    status = models.CharField(max_length=20, choices=RFQ_STATUS)
    technical_specifications = models.TextField(blank=True)
    
class PurchaseOrder(BaseModel):
    """Satın alma siparişleri"""
    order_number = models.CharField(max_length=30, unique=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT)
    order_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=PO_STATUS)
    incoterms = models.CharField(max_length=10, choices=INCOTERMS)
    payment_terms = models.TextField()
    
class GoodsReceipt(BaseModel):
    """Mal kabul"""
    receipt_number = models.CharField(max_length=30, unique=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT)
    delivery_note_number = models.CharField(max_length=50)
    receipt_date = models.DateField()
    received_by = models.ForeignKey(User, on_delete=models.PROTECT)
    quality_check_status = models.CharField(max_length=20, choices=QC_STATUS)
```

#### 7.2.6. Üretim Yönetimi Modülleri
```python
class BillOfMaterials(BaseModel):
    """Ürün reçeteleri (BOM)"""
    bom_code = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version = models.CharField(max_length=10)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=BOM_STATUS)
    
class BOMComponent(BaseModel):
    """Reçete bileşenleri"""
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE)
    component = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    unit = models.CharField(max_length=10)
    scrap_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_alternative = models.BooleanField(default=False)
    
class ProductionOrder(BaseModel):
    """Üretim emirleri"""
    order_number = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.PROTECT)
    planned_quantity = models.DecimalField(max_digits=15, decimal_places=4)
    produced_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PRODUCTION_STATUS)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    
class WorkOrder(BaseModel):
    """İş emirleri"""
    work_order_number = models.CharField(max_length=30, unique=True)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.CASCADE)
    operation_code = models.CharField(max_length=20)
    operation_name = models.CharField(max_length=100)
    work_center = models.ForeignKey('WorkCenter', on_delete=models.PROTECT)
    planned_duration = models.DurationField()
    actual_duration = models.DurationField(null=True, blank=True)
    operator = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=20, choices=WORK_ORDER_STATUS)
```

#### 7.2.7. Kalite Kontrol Modülleri
```python
class QualityControlPlan(BaseModel):
    """Kalite kontrol planları"""
    plan_code = models.CharField(max_length=30, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    control_point = models.CharField(max_length=50, choices=CONTROL_POINTS)
    sampling_plan = models.TextField()
    acceptance_criteria = models.TextField()
    
class QualityInspection(BaseModel):
    """Kalite muayene kayıtları"""
    inspection_number = models.CharField(max_length=30, unique=True)
    qc_plan = models.ForeignKey(QualityControlPlan, on_delete=models.PROTECT)
    inspection_date = models.DateField()
    inspector = models.ForeignKey(User, on_delete=models.PROTECT)
    batch_lot_number = models.CharField(max_length=50)
    sample_size = models.PositiveIntegerField()
    result = models.CharField(max_length=20, choices=INSPECTION_RESULTS)
    notes = models.TextField(blank=True)
    
class QualityDefect(BaseModel):
    """Kalite kusur kayıtları"""
    inspection = models.ForeignKey(QualityInspection, on_delete=models.CASCADE)
    defect_type = models.CharField(max_length=100)
    defect_count = models.PositiveIntegerField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    corrective_action = models.TextField(blank=True)
```

#### 7.2.8. İnsan Kaynakları Modülleri
```python
class Employee(BaseModel):
    """Personel bilgileri"""
    employee_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=11, unique=True)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    
class EmploymentInfo(BaseModel):
    """İstihdam bilgileri"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    hire_date = models.DateField()
    termination_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.PROTECT)
    position = models.ForeignKey('Position', on_delete=models.PROTECT)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    social_security_number = models.CharField(max_length=20, unique=True)
    
class LeaveRequest(BaseModel):
    """İzin talepleri"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    days_count = models.PositiveIntegerField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LEAVE_STATUS)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    approved_date = models.DateField(null=True, blank=True)
```

#### 7.2.9. Finans ve Muhasebe Modülleri
```python
class Invoice(BaseModel):
    """Fatura bilgileri"""
    invoice_number = models.CharField(max_length=30, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPES)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, null=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    e_invoice_uuid = models.UUIDField(null=True, blank=True)
    e_archive_number = models.CharField(max_length=50, blank=True)
    
class Payment(BaseModel):
    """Ödeme kayıtları"""
    payment_number = models.CharField(max_length=30, unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    bank_account = models.ForeignKey('BankAccount', on_delete=models.PROTECT, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
class CheckPromissoryNote(BaseModel):
    """Çek/Senet takibi"""
    document_type = models.CharField(max_length=10, choices=[('CHECK', 'Çek'), ('NOTE', 'Senet')])
    document_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    due_date = models.DateField()
    bank = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=DOCUMENT_STATUS)
    holder = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    endorsements = models.TextField(blank=True)  # Ciro bilgileri
    
class CostCenter(BaseModel):
    """Maliyet merkezleri"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    cost_type = models.CharField(max_length=20, choices=COST_TYPES)
    responsible_person = models.ForeignKey(User, on_delete=models.PROTECT)
    
class CostAllocation(BaseModel):
    """Maliyet dağıtımı"""
    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True)
    production_order = models.ForeignKey(ProductionOrder, on_delete=models.PROTECT, null=True)
    cost_element = models.CharField(max_length=50, choices=COST_ELEMENTS)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    allocation_date = models.DateField()
    allocation_method = models.CharField(max_length=20, choices=ALLOCATION_METHODS)