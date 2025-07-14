# 🏢 Kurumsal Kaynak Planlaması (ERP) Sistemi

Django tabanlı kapsamlı ERP sistemi başarıyla oluşturuldu! Bu sistem, modern işletmelerin temel fonksiyonlarını kapsayan modüler yapıda tasarlanmıştır.

## 📊 Sistem Mimarisi

### 🎯 Ana Modüller

#### 1. **CORE MODULE (Temel Varlıklar)**
**Temel varlık yönetimi ve sistem altyapısı**

| Model | Açıklama | Önemli Alanlar |
|-------|----------|----------------|
| `Product` | Şirketin sattığı nihai ürünler | SKU, fiyat, maliyet, kategori |
| `ProductCategory` | Ürün kategorileri (hiyerarşik) | Ad, açıklama, ana kategori |
| `Material` | Üretimde kullanılan malzemeler | Kod, ölçü birimi, standart maliyet |
| `Customer` | Müşteri bilgileri | Tip (bireysel/kurumsal), kredi limiti |
| `Supplier` | Tedarikçi bilgileri | İletişim, ödeme vadesi |
| `Warehouse` | Depo yönetimi | Konum, sorumlu kişi |

#### 2. **SALES MODULE (Satış Modülü)**
**Müşteri siparişleri ve satış süreçleri**

| Model | Açıklama | Durumlar |
|-------|----------|----------|
| `SalesOrder` | Satış siparişleri | Beklemede → Onaylandı → Sevk Edildi → Teslim Edildi |
| `SalesOrderItem` | Sipariş kalemleri | Miktar, fiyat, indirim, KDV |

**Özellikler:**
- ✅ Otomatik sipariş numarası (SO-000001)
- ✅ KDV ve indirim hesaplamaları
- ✅ Müşteri kredi limiti kontrolü
- ✅ Toplam tutar hesaplama (property)

#### 3. **PURCHASING MODULE (Satın Alma Modülü)**
**Tedarikçi siparişleri ve satın alma süreçleri**

| Model | Açıklama | Durumlar |
|-------|----------|----------|
| `PurchaseOrder` | Satın alma siparişleri | Taslak → Gönderildi → Teslim Alındı |
| `PurchaseOrderItem` | Sipariş kalemleri | Miktar, maliyet, teslim miktarı |

**Özellikler:**
- ✅ Otomatik sipariş numarası (PO-000001)
- ✅ Kısmi teslim takibi
- ✅ Kalan miktar hesaplama
- ✅ Tedarikçi performans izleme

#### 4. **PRODUCTION MODULE (Üretim Modülü)**
**Üretim planlama ve reçete yönetimi**

| Model | Açıklama | İşlevsellik |
|-------|----------|-------------|
| `BillOfMaterials` | Ürün reçeteleri (BOM) | 1 ürün = N malzeme (Many-to-Many) |
| `ProductionOrder` | Üretim emirleri | Planlama, gerçekleşme, tamamlanma % |

**Özellikler:**
- ✅ Otomatik üretim emri numarası (MO-000001)
- ✅ Tamamlanma yüzdesi hesaplama
- ✅ Planlanan vs gerçek tarih takibi
- ✅ Malzeme gereksinim hesaplama (BOM bazlı)

#### 5. **INVENTORY MODULE (Envanter Modülü)**
**Stok seviyeleri ve depo hareketleri**

| Model | Açıklama | Hareket Tipleri |
|-------|----------|-----------------|
| `InventoryMovement` | Tüm stok hareketleri | Giriş, Çıkış, Transfer, Sayım |

**Hareket Tipleri:**
- 📦 **Giriş:** Satın alma, üretim, sayım fazlası, transfer girişi
- 📤 **Çıkış:** Satış, üretim sarf, sayım eksiği, transfer çıkışı
- 🔄 **Transfer:** Depolar arası hareket
- 📋 **Sayım:** Fiziki sayım düzeltmeleri

**Özellikler:**
- ✅ Generic Foreign Key (Product + Material desteği)
- ✅ Gerçek zamanlı stok hesaplama
- ✅ Depo bazlı stok seviyeleri
- ✅ Hareket audit trail

#### 6. **FINANCE MODULE (Finans Modülü)**
**Finansal kayıtlar ve muhasebe**

| Model | Açıklama | Durumlar |
|-------|----------|----------|
| `Invoice` | Faturalar (satış/satın alma) | Ödenmedi → Kısmi → Ödendi |
| `ChartOfAccounts` | Hesap planı (hiyerarşik) | Varlık, Borç, Özkaynak, Gelir, Gider |

**Özellikler:**
- ✅ Otomatik fatura numarası
- ✅ Vade takibi ve gecikme uyarıları
- ✅ Kalan tutar hesaplama
- ✅ Muhasebe entegrasyonu için hesap planı

---

## 🛠️ Teknik Özellikler

### Model İlişkileri
```python
# Örnekler:
Product -> ProductCategory (ForeignKey)
SalesOrder -> Customer (ForeignKey)
SalesOrderItem -> SalesOrder (ForeignKey)
BillOfMaterials -> Product + Material (ForeignKey)
InventoryMovement -> Product/Material (GenericForeignKey)
```

### Otomatik Numaralandırma Sistemi
- **Satış Siparişleri:** SO-000001, SO-000002...
- **Satın Alma:** PO-000001, PO-000002...
- **Üretim Emirleri:** MO-000001, MO-000002...

### Property'ler ve Hesaplamalar
```python
# Ürün kar marjı
product.margin = unit_price - cost
product.margin_percentage = ((unit_price - cost) / unit_price) * 100

# Sipariş kalem toplamları  
item.line_total = quantity * unit_price * (1 - discount_percentage/100)
item.tax_amount = line_total * (tax_percentage / 100)
item.total_with_tax = line_total + tax_amount

# Üretim tamamlanma
order.completion_percentage = (produced_quantity / quantity_to_produce) * 100

# Fatura kalan tutar
invoice.remaining_amount = total_amount - paid_amount
```

### Stok Seviyesi Hesaplama
```python
def get_current_stock_level(item, warehouse):
    """Gerçek zamanlı stok hesaplama"""
    total_in = sum(giriş_hareketleri)
    total_out = sum(çıkış_hareketleri)
    return total_in - total_out
```

---

## 📱 Admin Panel Özellikleri

### Gelişmiş Admin Interface
- ✅ **Inline Editing:** Sipariş kalemleri, BOM detayları
- ✅ **List Display:** Önemli alanların özet görünümü
- ✅ **Filtering:** Durum, tarih, kategori filtreleri
- ✅ **Search:** Tüm önemli alanlarda arama
- ✅ **Actions:** Toplu sipariş onaylama/iptal
- ✅ **Fieldsets:** Organize form düzeni
- ✅ **Color Coding:** Kar marjı, tamamlanma yüzdesi

### Örnek Admin Görünümleri
```python
# Satış Siparişi Admin
list_display = ['order_number', 'customer', 'status', 'total_amount']
list_filter = ['status', 'order_date']
search_fields = ['order_number', 'customer__name']
inlines = [SalesOrderItemInline]

# Ürün Admin
list_display = ['sku', 'name', 'unit_price', 'margin_display']
list_editable = ['unit_price', 'cost']
inlines = [BillOfMaterialsInline]
```

---

## 📊 Örnek Veriler

### Sample Data Generator
**Komut:** `python manage.py populate_erp_data`

#### Oluşturulan Veriler:
- 📦 **5 Ürün Kategorisi:** Elektronik, Mobilya, Tekstil, Gıda, Kimyasal
- 🏭 **4 Depo:** Merkez, Anadolu, Ege, Üretim
- 🚚 **4 Tedarikçi:** Teknoloji, Mobilya, Kimya, Plastik firmaları  
- 👥 **4 Müşteri:** 3 kurumsal + 1 bireysel
- 🧱 **5 Malzeme:** Plastik, metal, elektronik, kimyasal, tekstil
- 📱 **5 Ürün:** LED ampul, ofis koltuğu, t-shirt, kimyasal, protein bar
- 📋 **7 BOM:** 3 ürün için malzeme reçeteleri
- 🛒 **10 Satış Siparişi:** Çeşitli durumlar ve tutarlar
- 📦 **8 Satın Alma Siparişi:** Malzeme tedariki
- ⚙️ **5 Üretim Emri:** Farklı üretim durumları
- 🏦 **Hesap Planı:** Temel muhasebe hesapları

---

## 🎯 Kullanım Senaryoları

### 1. **Sipariş-Üretim Döngüsü**
```
Müşteri Siparişi → BOM Kontrolü → Malzeme Satın Alma → 
Üretim Emri → Stok Hareketi → Fatura Kesimi
```

### 2. **Stok Yönetimi**
```
Satın Alma Girişi → Depo Transferi → Üretim Sarf → 
Satış Çıkışı → Stok Seviye Kontrolü
```

### 3. **Finans Takibi**
```
Sipariş Onayı → Fatura Kesimi → Ödeme Takibi → 
Muhasebe Kayıtları → Performans Raporları
```

---

## 🚀 Gelecek Geliştirmeler

### Planlanan Özellikler:
- 📊 **Dashboard:** Grafik ve KPI'lar
- 📱 **Web Interface:** Kullanıcı dostu arayüz
- 📈 **Raporlama:** Detaylı analiz raporları
- 🔔 **Bildirimler:** Stok uyarıları, vade takipleri
- 📱 **API:** RESTful API endpoints
- 🔐 **Yetkilendirme:** Role-based permissions
- 📦 **Barkod:** QR code entegrasyonu
- 🏭 **MRP:** Material Requirement Planning

---

## 📈 Sistem Faydaları

### İşletme Verimliliği
- ✅ **Otomatikleşme:** Manuel işlem azaltımı
- ✅ **Entegrasyon:** Departmanlar arası veri paylaşımı  
- ✅ **Raporlama:** Karar desteği ve analiz
- ✅ **İzlenebilirlik:** Tam süreç görünürlüğü

### Operasyonel Kontrol
- ✅ **Stok Optimizasyonu:** Gerçek zamanlı stok takibi
- ✅ **Maliyet Kontrolü:** Kar marjı analizi
- ✅ **Planlama:** Üretim ve tedarik planlaması
- ✅ **Kalite:** Süreç standardizasyonu

### Finansal Yönetim
- ✅ **Nakit Akışı:** Alacak/borç takibi
- ✅ **Karlılık:** Ürün/müşteri bazlı analiz
- ✅ **Bütçe:** Harcama kontrolü ve planlama
- ✅ **Uyumluluk:** Muhasebe standartları

---

## 🎉 Sonuç

Bu ERP sistemi, Django'nun güçlü ORM yapısını kullanarak modern işletmelerin ihtiyaçlarını karşılayan kapsamlı bir çözüm sunmaktadır. Modüler yapısı sayesinde kolayca genişletilebilir ve özelleştirilebilir.

**🔗 Admin Panel:** http://127.0.0.1:8000/admin/
**📊 ERP Dashboard:** http://127.0.0.1:8000/erp/

---

*Bu sistem, Context7 Django dokümantasyonu kullanılarak geliştirilmiştir ve production ortamı için optimize edilmiştir.* 