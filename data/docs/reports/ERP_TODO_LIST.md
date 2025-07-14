# 🚨 ERP SİSTEMİ ACİL ONARIM TODO LİSTESİ

## 🔴 **KRİTİK HATALAR - HEMEN DÜZELTİLMELİ**

### 1. ❌ **Import Hatası: get_current_stock_level**
```bash
ImportError: cannot import name 'get_current_stock_level' from 'erp.models'
```
**Sorun:** `views.py` dosyası `get_current_stock_level` ve `get_total_stock_level` fonksiyonlarını import etmeye çalışıyor ama bu fonksiyonlar `models.py`'de tanımlı değil.

**Çözüm:**
- [ ] `erp/models.py` dosyasına eksik stok hesaplama fonksiyonlarını ekle
- [ ] `views.py` import satırını düzelt

### 2. ❌ **Admin.py Syntax Hatası**
```bash
SyntaxError: invalid syntax (erp/admin.py line 10)
```
**Sorun:** Admin.py dosyasında import satırında syntax hatası var.

**Çözüm:**
- [ ] `erp/admin.py` dosyasındaki duplike import satırlarını temizle
- [ ] Syntax hatalarını düzelt

### 3. ❌ **Migration Sorunu**
**Sorun:** Yeni Quality Control ve HR modülleri için migration oluşturulamıyor.

**Çözüm:**
- [ ] İlk önce yukarıdaki hataları düzelt
- [ ] Sonra migration oluştur ve uygula

---

## 🟡 **ORTA ÖNCELİK - BU HAFTA İÇİNDE**

### 4. ⚠️ **Eksik Template Dosyaları**
**Sorun:** ERP modülleri için template dosyaları eksik.

**Çözüm:**
- [ ] `erp/templates/erp/` klasör yapısını oluştur
- [ ] Quality Control ve HR modülleri için template'ler ekle
- [ ] Dashboard template'ini güncelle

### 5. ⚠️ **URL Konfigürasyonu**
**Sorun:** Yeni modüller için URL pattern'leri eksik.

**Çözüm:**
- [ ] Quality Control URLs ekle
- [ ] HR modülü URLs ekle
- [ ] Permission kontrolü ekle

---

## 🟢 **DÜŞÜK ÖNCELİK - GELECEK SPRINTS**

### 6. 📊 **Dashboard Geliştirmeleri**
- [ ] Chart.js entegrasyonu
- [ ] KPI widget'ları
- [ ] Real-time updates

### 7. 🔗 **API Development**
- [ ] Django REST Framework setup
- [ ] API endpoints oluştur
- [ ] Authentication ekle

### 8. 🔔 **Notification System**
- [ ] Email backend setup
- [ ] Celery + Redis entegrasyonu
- [ ] Alert sistemi

---

## 🛠️ **ACİL ONARIM ADIM ADIM PLAN**

### **STEP 1: Import Hatalarını Düzelt (5 dakika)**
```python
# erp/models.py dosyasına eklenecek fonksiyonlar
def get_current_stock_level(item, warehouse):
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(item)
    
    movements = InventoryMovement.objects.filter(
        content_type=content_type,
        object_id=item.id,
        warehouse=warehouse
    )
    
    inbound = movements.filter(
        movement_type__in=['purchase_receipt', 'production_receipt', 'adjustment_in', 'transfer_in', 'return_in']
    ).aggregate(total=Sum('quantity'))['total'] or 0
    
    outbound = movements.filter(
        movement_type__in=['sales_issue', 'production_issue', 'adjustment_out', 'transfer_out', 'return_out']
    ).aggregate(total=Sum('quantity'))['total'] or 0
    
    return inbound - outbound

def get_total_stock_level(item):
    total = 0
    for warehouse in Warehouse.objects.filter(is_active=True):
        total += get_current_stock_level(item, warehouse)
    return total
```

### **STEP 2: Admin.py Syntax Hatalarını Düzelt (2 dakika)**
```python
# erp/admin.py import satırını düzelt
from .models import (
    Product, ProductCategory, Material, Customer, Supplier, Warehouse,
    SalesOrder, SalesOrderItem, PurchaseOrder, PurchaseOrderItem,
    BillOfMaterials, ProductionOrder, InventoryMovement, Invoice, ChartOfAccounts,
    QualityTest, QualityCheck, QualityDefect, Department, Employee, Role, Permission,
    RolePermission, UserRole
)
```

### **STEP 3: Migration Oluştur ve Uygula (3 dakika)**
```bash
python manage.py makemigrations erp
python manage.py migrate
```

### **STEP 4: Server Test Et (1 dakika)**
```bash
python manage.py runserver
```

---

## ✅ **BAŞARILI OLDUĞUNDA KONTROL LİSTESİ**

- [ ] Django server error vermeden başlıyor
- [ ] Admin panel açılıyor: http://127.0.0.1:8000/admin/
- [ ] ERP dashboard açılıyor: http://127.0.0.1:8000/erp/
- [ ] Yeni Quality Control modelleri admin'de görünüyor
- [ ] HR modülleri admin'de görünüyor
- [ ] Migration sorunsuz uygulandı

---

## 🎯 **SONUÇ HEDEFI**

Bu TODO listesi tamamlandığında:
- ✅ Sistem %85 tamamlanmış olacak
- ✅ Tüm modüller çalışır durumda olacak
- ✅ Quality Control + HR modülleri aktif olacak
- ✅ Production-ready sistem elde edilecek

**Tahmini Tamamlanma Süresi: 15-20 dakika**

---

## 📞 **ACİL DESTEK GEREKİRSE**

Eğer bu adımları takip ederken problem yaşarsanız:

1. **Hata logunu kontrol et**
2. **Syntax checker kullan**
3. **Django'yu restart et**
4. **Migration dosyalarını kontrol et**

**İlk önce STEP 1'den başlayın - bu en kritik olanı!** 🚀 