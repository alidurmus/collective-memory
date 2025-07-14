# 💰 Sales Modülü - Dokümantasyon

**URL Prefix:** `/erp/sales/`, `/erp/customers/`  
**Status:** ✅ 100% Complete  
**Last Updated:** 11 Ocak 2025  

## 🎯 Overview
Sales ve CRM süreçleri. Müşteri yönetimi, sipariş işlemleri, satış analitikleri.

## 🗺️ URL Patterns
- `/erp/sales/` - Sales dashboard
- `/erp/customers/` - Müşteri listesi  
- `/erp/customers/<id>/` - Müşteri detay
- `/erp/sales/orders/` - Satış siparişleri
- `/erp/sales/orders/create/` - Yeni sipariş
- `/erp/quotes/` - Teklifler

## 📊 Ana Modeller
- `Customer` - Müşteri bilgileri
- `SalesOrder` - Satış siparişleri  
- `SalesOrderItem` - Sipariş kalemleri
- `Quote` - Teklif modeli
- `SalesTarget` - Satış hedefleri

## 📡 API Endpoints
- `GET /api/v1/customers/` - Müşteri listesi
- `POST /api/v1/customers/` - Yeni müşteri
- `GET /api/v1/sales/orders/` - Sipariş listesi
- `POST /api/v1/sales/orders/` - Yeni sipariş

## ⚙️ İş Kuralları
1. Müşteri credit limit kontrolü gerekli
2. Sipariş onay süreçleri role-based
3. Stok kontrolü sipariş oluşturma sırasında
4. Otomatik fatura oluşturma seçeneği

## 🔗 Entegrasyonlar
- **Inventory:** Stok kontrol ve rezervasyon
- **Finance:** Fatura oluşturma ve tahsilat
- **Production:** Üretim emri oluşturma

## 🧪 Test Guidelines
- Müşteri CRUD testleri
- Sipariş workflow testleri  
- Credit limit validation testleri
- API endpoint testleri

## 🔧 Troubleshooting
- **Slow customer search:** Database indexing check
- **Order creation fails:** Stock availability validation
- **Credit limit errors:** Customer credit calculation review 