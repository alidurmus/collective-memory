# 📊 Dashboard Modülü - Dokümantasyon

**Modül:** Dashboard (Ana Kontrol Paneli)  
**URL Prefix:** `/dashboard/`, `/erp/`  
**App Name:** `dashboard`, `core`  
**Last Updated:** 11 Ocak 2025  
**Status:** ✅ 100% Complete  

---

## 🎯 Modül Overview

Dashboard modülü, Context7 ERP sisteminin ana kontrol paneli ve giriş noktasıdır. Kullanıcılara sistem genelinde önemli KPI'lar, hızlı erişim linkleri ve durum bilgileri sunar.

### **Ana Özellikler**
- ✅ Executive dashboard with glassmorphism design
- ✅ Real-time KPI monitoring
- ✅ Quick action panels
- ✅ Role-based dashboard customization
- ✅ Responsive design for all devices

---

## 🗺️ Sayfa Haritası ve URL Patterns

### **Ana Dashboard Sayfaları**
| URL Pattern | View | Template | Açıklama |
|-------------|------|----------|----------|
| `/` | `core.views.index` | `index.html` | Ana sayfa - Dashboard'a yönlendirme |
| `/dashboard/` | `dashboard.views.DashboardView` | `dashboard/index.html` | Ana dashboard görünümü |
| `/erp/` | `core.views.erp_dashboard` | `core/erp_dashboard.html` | ERP ana dashboard |
| `/erp/departments/` | `core.views.departments_overview` | `core/departments.html` | Departman genel bakış |

### **Quick Action Links**
| URL | Target Module | Açıklama |
|-----|---------------|----------|
| `/erp/sales/` | Sales | Satış modülü |
| `/erp/production/` | Production | Üretim modülü |
| `/erp/inventory/` | Inventory | Stok modülü |
| `/erp/purchasing/` | Purchasing | Satın alma modülü |
| `/erp/finance/` | Finance | Finans modülü |
| `/erp/hr/` | HR | İnsan kaynakları |
| `/erp/quality/` | Quality | Kalite kontrol |
| `/reports/` | Reports | Raporlama |

---

## 📊 Model Tanımları

### **DashboardWidget Model**
```python
class DashboardWidget(models.Model):
    """Dashboard widget configuration"""
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50)
    position = models.PositiveIntegerField()
    size = models.CharField(max_length=20)  # small, medium, large
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField('auth.Permission')
    config = models.JSONField(default=dict)
```

### **UserDashboardPreferences Model**
```python
class UserDashboardPreferences(models.Model):
    """User-specific dashboard preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    layout = models.JSONField(default=dict)
    widgets = models.ManyToManyField(DashboardWidget)
    theme_preference = models.CharField(max_length=20, default='auto')
```

---

## 🔗 View Patterns

### **DashboardView (Class-Based View)**
```python
class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'kpi_data': self.get_kpi_data(),
            'recent_activities': self.get_recent_activities(),
            'quick_stats': self.get_quick_stats(),
            'system_alerts': self.get_system_alerts(),
            'user_widgets': self.get_user_widgets(),
        })
        return context
    
    def get_kpi_data(self):
        """Get KPI data for dashboard"""
        return {
            'total_sales': self.calculate_total_sales(),
            'active_orders': self.get_active_orders_count(),
            'stock_alerts': self.get_stock_alerts_count(),
            'pending_approvals': self.get_pending_approvals(),
        }
```

### **AJAX Endpoints**
```python
# Real-time dashboard updates
@require_http_methods(["GET"])
@login_required
def dashboard_stats_api(request):
    """Real-time dashboard statistics"""
    return JsonResponse({
        'sales_today': get_sales_today(),
        'production_status': get_production_status(),
        'inventory_alerts': get_inventory_alerts(),
        'system_health': get_system_health(),
    })
```

---

## 🎨 Template Patterns

### **Base Dashboard Template**
```html
<!-- dashboard/templates/dashboard/base.html -->
{% extends "base.html" %}
{% load static %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/dashboard.css' %}">
<link rel="stylesheet" href="{% static 'css/context7_glassmorphism.css' %}">
{% endblock %}

{% block content %}
<div class="dashboard-container glassmorphism-bg">
    <div class="dashboard-header">
        <h1 class="gradient-text">{% block dashboard_title %}Dashboard{% endblock %}</h1>
        <div class="dashboard-actions">
            {% block dashboard_actions %}{% endblock %}
        </div>
    </div>
    
    <div class="dashboard-grid">
        {% block dashboard_content %}{% endblock %}
    </div>
</div>
{% endblock %}
```

### **Widget Template Pattern**
```html
<!-- dashboard/templates/dashboard/widgets/base_widget.html -->
<div class="dashboard-widget glass-card" data-widget-id="{{ widget.id }}">
    <div class="widget-header">
        <h3>{{ widget.title }}</h3>
        <div class="widget-actions">
            <button class="btn-refresh" onclick="refreshWidget('{{ widget.id }}')">
                <i class="fas fa-sync-alt"></i>
            </button>
        </div>
    </div>
    <div class="widget-content">
        {% block widget_content %}{% endblock %}
    </div>
</div>
```

---

## 📡 API Endpoints

### **Dashboard API Endpoints**
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/api/v1/dashboard/stats/` | GET | Dashboard istatistikleri |
| `/api/v1/dashboard/widgets/` | GET, POST | Widget management |
| `/api/v1/dashboard/preferences/` | GET, PUT | Kullanıcı tercihleri |
| `/api/v1/dashboard/alerts/` | GET | Sistem uyarıları |

### **Real-time Updates**
```javascript
// Dashboard real-time updates
class DashboardManager {
    constructor() {
        this.updateInterval = 30000; // 30 seconds
        this.init();
    }
    
    init() {
        this.startAutoUpdate();
        this.bindEvents();
    }
    
    async updateStats() {
        try {
            const response = await fetch('/api/v1/dashboard/stats/');
            const data = await response.json();
            this.updateWidgets(data);
        } catch (error) {
            console.error('Dashboard update failed:', error);
        }
    }
}
```

---

## ⚙️ İş Kuralları

### **Dashboard Access Rules**
1. **Authentication Required:** Tüm dashboard sayfaları authentication gerektirir
2. **Role-Based Widgets:** Widget'lar kullanıcı rolüne göre gösterilir
3. **Data Privacy:** Kullanıcı sadece yetkili olduğu verileri görür
4. **Real-time Updates:** Critical data 30 saniyede bir güncellenir

### **KPI Calculation Rules**
```python
class DashboardKPIService:
    def calculate_sales_performance(self):
        """Sales performance calculation"""
        today_sales = SalesOrder.objects.filter(
            order_date=timezone.now().date(),
            status='confirmed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        monthly_target = self.get_monthly_sales_target()
        return {
            'today_sales': today_sales,
            'monthly_progress': (today_sales / monthly_target) * 100,
            'trend': self.calculate_sales_trend(),
        }
```

---

## 🔗 Entegrasyon Noktaları

### **Modül Entegrasyonları**
- **Sales Module:** Order statistics, sales performance
- **Production Module:** Production status, capacity utilization
- **Inventory Module:** Stock levels, reorder alerts
- **Finance Module:** Financial KPIs, budget status
- **HR Module:** Employee activities, leave requests
- **Quality Module:** Quality metrics, inspection status

### **External Integrations**
- **OpenAI API:** AI-powered insights (if configured)
- **Chart.js:** Data visualization
- **Real-time APIs:** Live data updates

---

## 🧪 Test Guidelines

### **Dashboard Test Strategy**
```python
class DashboardTestCase(TestCase):
    def test_dashboard_view_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')
    
    def test_dashboard_kpi_calculation(self):
        """Test KPI calculation accuracy"""
        # Create test data
        self.create_test_sales_orders()
        
        # Test KPI calculation
        view = DashboardView()
        kpi_data = view.get_kpi_data()
        
        self.assertIn('total_sales', kpi_data)
        self.assertIsInstance(kpi_data['total_sales'], Decimal)
```

### **Frontend Testing**
```javascript
// Dashboard widget tests
describe('Dashboard Widgets', () => {
    test('Widget refreshes on button click', async () => {
        const widget = document.querySelector('[data-widget-id="sales-stats"]');
        const refreshBtn = widget.querySelector('.btn-refresh');
        
        // Mock API response
        jest.spyOn(window, 'fetch').mockResolvedValueOnce({
            ok: true,
            json: async () => ({ sales_today: 1500 })
        });
        
        refreshBtn.click();
        
        await waitFor(() => {
            expect(widget.querySelector('.sales-amount')).toHaveTextContent('1500');
        });
    });
});
```

---

## 🎨 UI/UX Patterns

### **Glassmorphism Design**
```css
/* Dashboard glassmorphism effects */
.dashboard-widget {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 20px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.dashboard-widget:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
}
```

### **Responsive Grid System**
```css
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 2rem;
}

@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
        padding: 1rem;
    }
}
```

---

## 🔧 Troubleshooting

### **Common Issues**

#### **Dashboard Loading Slow**
```python
# Problem: N+1 queries in KPI calculation
# Solution: Use select_related and prefetch_related
def get_kpi_data(self):
    orders = SalesOrder.objects.select_related('customer').prefetch_related('items')
    # Process optimized queryset
```

#### **Widget Not Updating**
```javascript
// Problem: AJAX cache issues
// Solution: Add cache-busting parameter
const response = await fetch(`/api/v1/dashboard/stats/?t=${Date.now()}`);
```

#### **Permission Errors**
```python
# Problem: Widget access control
# Solution: Check user permissions in view
def get_user_widgets(self):
    return DashboardWidget.objects.filter(
        permissions__in=self.request.user.get_all_permissions()
    )
```

---

## 📈 Performance Optimizations

### **Caching Strategy**
```python
from django.core.cache import cache

def get_kpi_data(self):
    cache_key = f"dashboard_kpi_{self.request.user.id}"
    kpi_data = cache.get(cache_key)
    
    if not kpi_data:
        kpi_data = self.calculate_kpi_data()
        cache.set(cache_key, kpi_data, 300)  # 5 minutes
    
    return kpi_data
```

### **Database Optimization**
```python
# Efficient dashboard queries
class DashboardQueryOptimizer:
    @staticmethod
    def get_optimized_stats():
        return {
            'sales_stats': SalesOrder.objects.aggregate(
                total_sales=Sum('total_amount'),
                order_count=Count('id'),
                avg_order_value=Avg('total_amount')
            ),
            'inventory_alerts': Product.objects.filter(
                current_stock__lt=F('minimum_stock')
            ).count(),
        }
```

---

**🎯 Mission:** Context7 ERP sisteminin merkezi kontrol noktası olarak kullanıcılara kapsamlı sistem görünümü sağlamak.

**📞 QMS Reference:** REC-DASHBOARD-MODULE-250111-001 - Dashboard Module Documentation

---

*Dashboard Module - Central Control Hub of Context7 ERP* 