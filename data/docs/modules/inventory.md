# 📦 Inventory Modülü

**URL:** `/erp/inventory/`  
**Status:** ✅ Complete  

## 🎯 Overview
Stok yönetimi, depo işlemleri, stok hareketleri.

## 🗺️ Pages
- `/erp/inventory/` - Stock dashboard
- `/erp/products/` - Ürün listesi
- `/erp/inventory/movements/` - Stok hareketleri
- `/erp/inventory/warehouses/` - Depo yönetimi

## 📊 Models
- `Product` - Ürün tanımları
- `Warehouse` - Depo bilgileri
- `StockTransaction` - Stok hareketleri
- `StockLevel` - Stok seviyeleri

## ⚙️ Business Rules
1. Minimum stock alerts
2. FIFO/LIFO inventory methods
3. Multi-warehouse support
4. Automatic reorder points 