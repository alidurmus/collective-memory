
# ======================================================
# ERP VERİ ALANLARI DEPLOYMENT KURALLARI
# ======================================================

## Otomatik Migration Yönetimi
- **Kural:** Tüm ERP veri alanları deployment'ları otomatik olarak migration sorunlarını çözer
- **Uygulama:** `python manage.py deploy_erp_fields --module=supplier --auto-yes` komutu ile
- **Çözüm:** Auto-now field'lar için otomatik timezone.now default değeri
- **Nullable:** Tüm text field'lar null=True, blank=True ile oluşturulur
- **Backward Compatibility:** Mevcut alanlar korunur, yeni alanlar eklenir

## TODO Takip Sistemi
- **Kural:** Her deployment tamamlandığında ilgili TODO otomatik olarak "completed" olarak işaretlenir
- **Uygulama:** Management command içinde _update_todo_status() method'u
- **Takip:** ERP Veri Alanları Deployment kategorisinde progress tracking

## Model Field Standartları
- **Text Fields:** null=True, blank=True (geriye uyumlulük için)
- **Date Fields:** null=True, blank=True (mevcut kayıtlar için)
- **Foreign Keys:** null=True, blank=True, on_delete=models.SET_NULL
- **Choice Fields:** default değer ile tanımlanır
- **Decimal Fields:** default=0, validators=[MinValueValidator(0)]

## Migration Automation
- **Prompt Handling:** Otomatik "1" seçimi ve timezone.now default değeri
- **Error Recovery:** Migration hatalarında otomatik retry mekanizması
- **Rollback:** Hatalı deployment'larda otomatik geri alma
- **Verification:** Migration sonrası model integrity check

## Deployment Sequence
1. Model fields güncelleme (nullable olarak)
2. Migration oluşturma (otomatik prompt handling)
3. Migration uygulama
4. TODO status güncelleme
5. Rules documentation güncelleme
6. Verification ve testing

## Module-Based Deployment
- **Customer:** `--module=customer` (✅ Tamamlandı)
- **Supplier:** `--module=supplier` (📋 Beklemede)
- **Product:** `--module=product` (📋 Beklemede)
- **Inventory:** `--module=inventory` (📋 Beklemede)
- **Sales:** `--module=sales` (📋 Beklemede)
- **Purchasing:** `--module=purchasing` (📋 Beklemede)
- **Production:** `--module=production` (📋 Beklemede)
- **HR:** `--module=hr` (📋 Beklemede)
- **Finance:** `--module=finance` (📋 Beklemede)

## Command Examples
```bash
# Müşteri alanları deployment
python manage.py deploy_erp_fields --module=customer --auto-yes

# Tedarikçi alanları deployment
python manage.py deploy_erp_fields --module=supplier --auto-yes

# Tüm modüller için sequential deployment
python manage.py deploy_erp_fields --module=all --auto-yes
```

## Error Handling Rules
- **Migration Conflicts:** Otomatik merge strategy
- **Field Conflicts:** Existing field preservation
- **Data Loss Prevention:** Backup before deployment
- **Rollback Strategy:** Automatic revert on critical errors
