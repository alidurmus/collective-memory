# 📊 Sample Data & Migration Scripts

Bu klasör, ERP sistemi için sample data oluşturma ve database migration script'lerini içerir.

## 📋 Script Listesi

### 🏗️ Sample Data Creation Scripts

#### 1. `create_final_sample_data.py`
- **Açıklama**: En kapsamlı sample data creation script'i
- **Özellikler**: Tüm modüller için gerçekçi test verisi oluşturur
- **Kullanım**: `python sample_data/create_final_sample_data.py`

#### 2. `create_sample_data.py`
- **Açıklama**: Ana sample data oluşturma script'i
- **Özellikler**: Temel ERP modülleri için örnek veriler
- **Kullanım**: `python sample_data/create_sample_data.py`

#### 3. `create_sample_data_fixed.py`
- **Açıklama**: Düzeltilmiş sample data script'i
- **Özellikler**: Bug fix'leri ve iyileştirmeler içerir
- **Kullanım**: `python sample_data/create_sample_data_fixed.py`

### 🏭 Specialized Data Scripts

#### 4. `create_bom_test_data.py`
- **Açıklama**: Bill of Materials (BOM) test data oluşturur
- **Özellikler**: Üretim modülü için malzeme listesi verileri
- **Kullanım**: `python sample_data/create_bom_test_data.py`

#### 5. `create_sample_todo_data.py`
- **Açıklama**: TODO/Task management örnek verileri
- **Özellikler**: Görev yönetimi modülü için sample data
- **Kullanım**: `python sample_data/create_sample_todo_data.py`

#### 6. `create_simple_todos.py`
- **Açıklama**: Basit TODO verileri oluşturur
- **Özellikler**: Hızlı test için minimal TODO verileri
- **Kullanım**: `python sample_data/create_simple_todos.py`

### 🔄 Migration Scripts

#### 7. `database_migration_script.py`
- **Açıklama**: SQLite'dan PostgreSQL'e migration script'i
- **Özellikler**: Production database migration işlemleri
- **Kullanım**: `python sample_data/database_migration_script.py`

#### 8. `migrate_tasks_to_todo.py`
- **Açıklama**: Task verilerini TODO modülüne migrate eder
- **Özellikler**: Veri modeli değişiklikleri için migration
- **Kullanım**: `python sample_data/migrate_tasks_to_todo.py`

## 🚀 Kullanım Önerileri

### Development Environment
```bash
# Tam sample data set'i için
python sample_data/create_final_sample_data.py

# Sadece TODO verileri için
python sample_data/create_sample_todo_data.py

# BOM test verileri için
python sample_data/create_bom_test_data.py
```

### Production Migration
```bash
# Database migration için
python sample_data/database_migration_script.py

# Task migration için
python sample_data/migrate_tasks_to_todo.py
```

## ⚠️ Önemli Notlar

1. **Backup**: Script'leri çalıştırmadan önce mutlaka database backup'ı alın
2. **Environment**: Development environment'da test ettikten sonra production'da kullanın
3. **Dependencies**: Script'leri çalıştırmadan önce tüm requirements'ların yüklü olduğundan emin olun
4. **Order**: Migration script'lerini doğru sırada çalıştırın

## 📊 Generated Data Overview

Bu script'ler aşağıdaki türde verileri oluşturur:

- **Users**: Admin, manager, operator kullanıcıları
- **Products**: Ürün kataloğu ve fiyat listeleri
- **Customers**: Müşteri bilgileri ve iletişim detayları
- **Suppliers**: Tedarikçi bilgileri ve sözleşmeler
- **Orders**: Satış ve satın alma siparişleri
- **Inventory**: Stok hareketleri ve envanter verileri
- **Production**: Üretim planları ve BOM'lar
- **Finance**: Faturalar ve ödeme kayıtları

## 🔧 Troubleshooting

**Import Error**: Eğer import hatası alırsanız:
```bash
export DJANGO_SETTINGS_MODULE=dashboard_project.settings
```

**Database Lock**: SQLite lock hatası için:
```bash
python manage.py migrate --run-syncdb
```

**Permission Error**: Windows'ta permission hatası için PowerShell'i admin olarak çalıştırın. 