# 🏭 Production Modülü

**URL:** `/erp/production/`  
**Status:** ✅ Complete  

## 🎯 Overview
Üretim planlama, üretim emirleri, kapasite yönetimi.

## 🗺️ Pages
- `/erp/production/` - Production dashboard
- `/erp/production/orders/` - Üretim emirleri
- `/erp/production/bom/` - Malzeme listesi (BOM)
- `/erp/production/capacity/` - Kapasite planlama

## 📊 Models
- `ProductionOrder` - Üretim emirleri
- `BillOfMaterials` - Malzeme listesi
- `WorkCenter` - İş merkezleri
- `ProductionTask` - Üretim görevleri

## ⚙️ Business Rules
1. BOM validation before production
2. Material availability check
3. Capacity scheduling
4. Quality control integration

## 🔗 Integrations
- **Inventory:** Material consumption
- **Quality:** QC checkpoints
- **Sales:** Production to order 