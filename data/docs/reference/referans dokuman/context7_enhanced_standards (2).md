# Context7 Enhanced Standards - Optimized Reference

## 🏛️ ERP Modules Integration Standards

### 1. Core Module Definitions

#### 1.1. Production Module
```python
class ProductionOrder(BaseModel):
    """Üretim emri"""
    order_number = models.CharField(max_length=20, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS)
    start_date = models.DateField()
    end_date = models.DateField()
    
class QualityControl(BaseModel):
    """Kalite kontrol"""
    control_type = models.CharField(max_length=20, choices=CONTROL_TYPES)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    criteria = models.JSONField()
    results = models.JSONField()
    status = models.CharField(max_length=20, choices=QUALITY_STATUS)
```

#### 1.2. Inventory Module
```python
class StockTransaction(BaseModel):
    """Stok hareketi"""
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=50)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    
class InventoryCount(BaseModel):
    """Stok sayımı"""
    count_date = models.DateField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=COUNT_STATUS)
    items = models.JSONField()
```

#### 1.3. Financial Module
```python
class Invoice(BaseModel):
    """Fatura"""
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    invoice_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS)
    
class Payment(BaseModel):
    """Ödeme"""
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
```

### 2. Business Process Flows

#### 2.1. Order-to-Cash Process
```python
class OrderToCashWorkflow:
    def process_order(self, order):
        # 1. Stok kontrolü
        self.check_stock_availability(order)
        
        # 2. Üretim planlaması
        if self.needs_production(order):
            self.create_production_order(order)
        
        # 3. Sevkiyat hazırlığı
        self.prepare_shipment(order)
        
        # 4. Faturalama
        self.create_invoice(order)
        
        # 5. Tahsilat takibi
        self.track_collection(order)
```

#### 2.2. Procurement Process
```python
class ProcurementWorkflow:
    def process_purchase(self, request):
        # 1. Satın alma talebi
        purchase_request = self.create_purchase_request(request)
        
        # 2. Tedarikçi seçimi
        supplier = self.select_supplier(purchase_request)
        
        # 3. Sipariş oluşturma
        purchase_order = self.create_purchase_order(purchase_request, supplier)
        
        # 4. Teslim alma
        self.receive_goods(purchase_order)
        
        # 5. Fatura kontrolü
        self.verify_invoice(purchase_order)
```

### 3. Data Integration Patterns

#### 3.1. Master Data Synchronization
```python
class MasterDataSync:
    def sync_customers(self):
        # External system integration
        external_customers = self.get_external_customers()
        
        for ext_customer in external_customers:
            customer, created = Customer.objects.update_or_create(
                external_id=ext_customer['id'],
                defaults={
                    'name': ext_customer['name'],
                    'email': ext_customer['email'],
                    'phone': ext_customer['phone']
                }
            )
            
            if created:
                self.log_sync_event('CREATE', customer)
            else:
                self.log_sync_event('UPDATE', customer)
```

#### 3.2. Financial Integration
```python
class FinancialIntegration:
    def sync_with_accounting(self, invoice):
        # Accounting system integration
        accounting_entry = {
            'reference': invoice.invoice_number,
            'date': invoice.invoice_date,
            'customer': invoice.customer.accounting_code,
            'amount': invoice.total_amount,
            'currency': invoice.currency
        }
        
        self.post_to_accounting_system(accounting_entry)
```

### 4. Reporting and Analytics

#### 4.1. Standard Reports
```python
class StandardReports:
    def production_efficiency_report(self, start_date, end_date):
        """Üretim verimliliği raporu"""
        return ProductionOrder.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date
        ).aggregate(
            total_orders=Count('id'),
            completed_orders=Count('id', filter=Q(status='COMPLETED')),
            efficiency_rate=F('completed_orders') / F('total_orders') * 100
        )
    
    def inventory_turnover_report(self, period):
        """Stok devir hızı raporu"""
        return StockTransaction.objects.filter(
            transaction_date__gte=period['start'],
            transaction_date__lte=period['end']
        ).values('product__name').annotate(
            total_in=Sum('quantity', filter=Q(transaction_type='IN')),
            total_out=Sum('quantity', filter=Q(transaction_type='OUT')),
            turnover_rate=F('total_out') / F('total_in')
        )
```

#### 4.2. Dashboard Widgets
```python
class DashboardWidgets:
    def get_kpi_data(self):
        """Ana KPI'lar"""
        today = timezone.now().date()
        return {
            'daily_production': ProductionOrder.objects.filter(
                production_date=today
            ).count(),
            'pending_orders': SalesOrder.objects.filter(
                status='PENDING'
            ).count(),
            'inventory_value': StockTransaction.objects.aggregate(
                total=Sum('quantity') * F('unit_price')
            )['total'] or 0,
            'overdue_payments': Invoice.objects.filter(
                due_date__lt=today,
                status='UNPAID'
            ).count()
        }
```

### 5. System Configuration

#### 5.1. User Management
```python
class UserProfile(BaseModel):
    """Kullanıcı profili"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    role = models.CharField(max_length=50, choices=ROLES)
    permissions = models.JSONField(default=dict)
    
class SystemConfiguration(BaseModel):
    """Sistem konfigürasyonu"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True)
```

#### 5.2. Audit Trail
```python
class AuditLog(BaseModel):
    """Audit kaydı"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50, choices=AUDIT_ACTIONS)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    changes = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
```

### 6. API Standards

#### 6.1. REST API Patterns
```python
class APIViewSet(viewsets.ModelViewSet):
    """Standart API ViewSet"""
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    def get_queryset(self):
        """Kullanıcı bazlı filtreleme"""
        queryset = self.queryset
        if hasattr(self.request.user, 'profile'):
            department = self.request.user.profile.department
            queryset = queryset.filter(department=department)
        return queryset
    
    def perform_create(self, serializer):
        """Kayıt oluşturma"""
        serializer.save(
            created_by=self.request.user,
            created_at=timezone.now()
        )
```

#### 6.2. Authentication & Authorization
```python
class DepartmentPermission(BasePermission):
    """Departman bazlı yetkilendirme"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_department = request.user.profile.department
        required_department = getattr(view, 'required_department', None)
        
        if required_department and user_department != required_department:
            return False
        
        return True
```

### 7. Performance Optimization

#### 7.1. Database Optimization
```python
class OptimizedQueryMixin:
    """Optimize edilmiş sorgu mixin'i"""
    def get_queryset(self):
        return super().get_queryset().select_related(
            'customer', 'product', 'warehouse'
        ).prefetch_related(
            'items', 'items__product'
        )
    
    def get_aggregated_data(self):
        """Aggregate veriler"""
        return self.get_queryset().aggregate(
            total_amount=Sum('amount'),
            avg_amount=Avg('amount'),
            count=Count('id')
        )
```

#### 7.2. Caching Strategy
```python
from django.core.cache import cache

class CacheManager:
    def get_dashboard_data(self, user_id):
        """Dashboard verilerini cache'den al"""
        cache_key = f'dashboard_data_{user_id}'
        data = cache.get(cache_key)
        
        if data is None:
            data = self.calculate_dashboard_data(user_id)
            cache.set(cache_key, data, 300)  # 5 dakika
        
        return data
    
    def invalidate_cache(self, pattern):
        """Cache'i temizle"""
        cache.delete_pattern(pattern)
```

### 8. Security Standards

#### 8.1. Data Protection
```python
class SecureModelMixin:
    """Güvenli model mixin'i"""
    def save(self, *args, **kwargs):
        # Sensitive data encryption
        if hasattr(self, 'sensitive_fields'):
            for field in self.sensitive_fields:
                value = getattr(self, field)
                if value:
                    setattr(self, field, encrypt_data(value))
        
        super().save(*args, **kwargs)
    
    def clean(self):
        # Input validation
        for field_name, value in self.get_field_values().items():
            if not self.validate_input(field_name, value):
                raise ValidationError(f'Invalid input for {field_name}')
```

#### 8.2. Access Control
```python
class AccessControlMixin:
    """Erişim kontrol mixin'i"""
    def check_access(self, user, action):
        """Erişim kontrolü"""
        if not user.is_authenticated:
            return False
        
        user_permissions = user.get_all_permissions()
        required_permission = f'{self._meta.app_label}.{action}_{self._meta.model_name}'
        
        return required_permission in user_permissions
```

---

## 🎯 Implementation Guidelines

### Development Standards
- Follow Django best practices
- Use Class-Based Views (CBVs)
- Implement proper error handling
- Write comprehensive tests
- Document all APIs

### Performance Requirements
- Database queries < 50ms
- API responses < 200ms
- Page loads < 2 seconds
- 99.5% uptime target

### Security Requirements
- JWT authentication
- Role-based access control
- Input validation
- Data encryption
- Audit logging

---

**📅 Last Updated:** 9 Ocak 2025  
**📊 Optimization:** 2096 → 400 satır (%80 azalma)  
**🎯 Focus:** Essential patterns ve core integration  
**📝 Status:** Optimized - redundant code removed