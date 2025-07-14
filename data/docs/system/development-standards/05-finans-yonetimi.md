# Context7 ERP - Finans Yönetimi Modülü
**Modül Kodu:** FINANCE-MGT  
**Öncelik:** 1 - Kritik  
**Tahmini Süre:** 6-8 hafta  
**Bağımlılıklar:** Cari Hesap, Muhasebe, Banka Entegrasyonu  

---

## 📋 Modül Açıklaması

Gelişmiş finansal yönetim sistemi; çok para birimi desteği, kredi yönetimi, çek/senet takibi, nakit akış yönetimi ve kapsamlı finansal raporlama özelliklerini içeren enterprise-level finans çözümü.

---

## 🎯 Ana Özellikler

### **1. Gelişmiş Muhasebe Sistemi**

#### **Multi-Currency Accounting**
- **Real-time Exchange Rates**
  - Canlı döviz kurları
  - Otomatik kur güncellemesi
  - Kur geçmişi takibi
  - Merkez Bankası entegrasyonu

- **Currency Hedging**
  - Kur riski yönetimi
  - Forward kontratları
  - Hedge accounting
  - Risk analizi raporları

- **Revaluation Process**
  - Periyodik yeniden değerleme
  - Kur farkı hesaplama
  - Otomatik muhasebe kayıtları
  - Varyans analizi

#### **Credit Management**
- **Customer Credit Limits**
  - Kredi limit tanımlama
  - Risk değerlendirmesi
  - Ödeme davranışı analizi
  - Otomatik limit kontrolü

- **Credit Scoring**
  - Kredi puanlama sistemi
  - Risk kategorileri
  - Geçmiş performans analizi
  - Otomatik uyarı sistemi

- **Payment Behavior Analysis**
  - Ödeme vadesi analizi
  - Gecikme paternleri
  - DSO (Days Sales Outstanding) hesaplama
  - Collection efficiency

#### **Cash Flow Management**
- **Cash Flow Forecasting**
  - Nakit akış tahminleri
  - Senaryolu planlamalar
  - Trend analizleri
  - Early warning sistem

- **Liquidity Planning**
  - Likidite planlaması
  - Minimum nakit seviyesi
  - Fazlalık yatırım önerileri
  - Kısa vadeli borçlanma planı

### **2. Çek ve Senet Yönetimi**

#### **Check Tracking**
- **Check Register**
  - Çek kayıt sistemi
  - Vade tarihi takibi
  - Tahsilat durumu
  - Banka detayları

- **Due Date Monitoring**
  - Vade tarihi uyarıları
  - Otomatik hatırlatıcılar
  - Tahsilat planlaması
  - Vadesinde tahsilat raporu

- **Collection Status**
  - Tahsilat durumu takibi
  - Ödenmemiş çekler
  - İptal edilen çekler
  - Protestolu çekler

#### **Promissory Note Management**
- **Note Tracking**
  - Senet kayıt sistemi
  - Vade takibi
  - Ciro işlemleri
  - Teminat durumu

- **Maturity Management**
  - Vade yönetimi
  - Otomatik uyarılar
  - Yenileme önerileri
  - Collection scheduling

- **Endorsement Handling**
  - Ciro işlemleri
  - Ciro zinciri takibi
  - Yasal sorumluluk
  - Risk değerlendirmesi

#### **Bank Reconciliation**
- **Automatic Matching**
  - Otomatik eşleştirme
  - Hesap mutabakatı
  - Fark analizi
  - Exception reporting

- **Discrepancy Resolution**
  - Uyumsuzluk çözümü
  - Araştırma süreci
  - Düzeltme kayıtları
  - Onay süreçleri

#### **Risk Management**
- **Bounced Check Tracking**
  - Karşılıksız çek takibi
  - Müşteri blacklisti
  - Risk skorlaması
  - Legal action tracking

- **Credit Hold Automation**
  - Otomatik kredi durdurma
  - Risk eşik değerleri
  - Escalation procedures
  - Override approvals

### **3. Kredi ve Transfer İşlemleri**

#### **Credit Facility Management**
- **Credit Lines**
  - Kredi line'ları
  - Kullanım takibi
  - Faiz hesaplaması
  - Geri ödeme planları

- **Utilization Tracking**
  - Kullanım oranları
  - Available credit
  - Commitment fees
  - Covenant monitoring

- **Interest Calculation**
  - Faiz hesaplamaları
  - Compound interest
  - Rate changes
  - Accrual accounting

#### **Inter-Bank Transfers**
- **Transfer Processing**
  - Transfer işleme
  - EFT/SWIFT transferler
  - Confirmation tracking
  - Fee management

- **Reconciliation**
  - Transfer mutabakatı
  - Status tracking
  - Exception handling
  - Audit trail

#### **Payment Processing**
- **Supplier Payments**
  - Tedarikçi ödemeleri
  - Batch payments
  - Approval workflow
  - Payment methods

- **Customer Receipts**
  - Müşteri tahsilatları
  - Multiple payment methods
  - Allocation rules
  - Cash application

#### **Installment Management**
- **Payment Schedules**
  - Ödeme planları
  - Otomatik hatırlatıcılar
  - Collection tracking
  - Default management

### **4. Treasury Management**

#### **Cash Position Management**
- Günlük nakit pozisyonu
- Banka bakiyeleri
- Yatırım portföyü
- Borç pozisyonu

#### **Investment Management**
- Kısa vadeli yatırımlar
- Portföy yönetimi
- Yield optimization
- Risk management

### **5. Financial Reporting**

#### **Standard Financial Reports**
- **P&L Automation**
  - Otomatik kar/zarar
  - Periyodik raporlar
  - Trend analizleri
  - Budget vs actual

- **Balance Sheet Generation**
  - Bilanço oluşturma
  - Asset/liability tracking
  - Equity calculations
  - Ratio analysis

- **Cash Flow Statements**
  - Nakit akış tablosu
  - Operating activities
  - Investing activities
  - Financing activities

#### **Management Reports**
- DSO/DPO analysis
- Working capital analysis
- ROI/ROA calculations
- Financial ratios

---

## 🗄️ Database Models

### **1. Currency (Para Birimi)**
```python
class Currency(models.Model):
    currency_code = models.CharField(max_length=3, unique=True)  # TRY, USD, EUR
    currency_name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=5)
    decimal_places = models.IntegerField(default=2)
    is_base_currency = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **2. ExchangeRate (Döviz Kuru)**
```python
class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_to')
    rate_date = models.DateField()
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    source = models.CharField(max_length=50, default='TCMB')
    is_manual = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['from_currency', 'to_currency', 'rate_date']
```

### **3. Bank (Banka)**
```python
class Bank(models.Model):
    bank_code = models.CharField(max_length=10, unique=True)
    bank_name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=11, blank=True)
    country = models.CharField(max_length=50, default='Turkey')
    contact_info = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
```

### **4. BankAccount (Banka Hesabı)**
```python
class BankAccount(models.Model):
    account_number = models.CharField(max_length=30)
    account_name = models.CharField(max_length=100)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    branch_code = models.CharField(max_length=10, blank=True)
    iban = models.CharField(max_length=34, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    minimum_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    overdraft_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)
```

### **5. Check (Çek)**
```python
class Check(models.Model):
    check_number = models.CharField(max_length=20)
    check_type = models.CharField(max_length=20, choices=CHECK_TYPE_CHOICES)  # Received/Issued
    customer = models.ForeignKey('crm.Customer', on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey('procurement.Supplier', on_delete=models.CASCADE, null=True, blank=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=CHECK_STATUS_CHOICES)
    collection_date = models.DateField(null=True, blank=True)
    bounce_reason = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_postdated = models.BooleanField(default=False)
```

### **6. PromissoryNote (Senet)**
```python
class PromissoryNote(models.Model):
    note_number = models.CharField(max_length=20)
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES)  # Received/Issued
    customer = models.ForeignKey('crm.Customer', on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey('procurement.Supplier', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    issue_date = models.DateField()
    maturity_date = models.DateField()
    status = models.CharField(max_length=20, choices=NOTE_STATUS_CHOICES)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    guarantor = models.CharField(max_length=100, blank=True)
    collateral_description = models.TextField(blank=True)
    endorsements = models.JSONField(default=list)
    collection_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

### **7. CreditLimit (Kredi Limiti)**
```python
class CreditLimit(models.Model):
    customer = models.OneToOneField('crm.Customer', on_delete=models.CASCADE)
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    available_credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit_score = models.IntegerField(default=0)  # 0-1000
    risk_category = models.CharField(max_length=10, choices=RISK_CATEGORY_CHOICES)
    payment_terms = models.CharField(max_length=50)
    last_review_date = models.DateField()
    next_review_date = models.DateField()
    credit_hold = models.BooleanField(default=False)
    hold_reason = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
```

### **8. CashFlowForecast (Nakit Akış Tahmini)**
```python
class CashFlowForecast(models.Model):
    forecast_date = models.DateField()
    period_start = models.DateField()
    period_end = models.DateField()
    opening_balance = models.DecimalField(max_digits=20, decimal_places=2)
    projected_inflows = models.DecimalField(max_digits=20, decimal_places=2)
    projected_outflows = models.DecimalField(max_digits=20, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=20, decimal_places=2)
    minimum_required = models.DecimalField(max_digits=20, decimal_places=2)
    surplus_deficit = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    scenario = models.CharField(max_length=20, choices=SCENARIO_CHOICES)
    confidence_level = models.DecimalField(max_digits=5, decimal_places=2, default=80)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **9. BankTransaction (Banka Hareketi)**
```python
class BankTransaction(models.Model):
    transaction_number = models.CharField(max_length=30, unique=True)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    value_date = models.DateField()
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=15, decimal_places=6, default=1)
    base_amount = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.CharField(max_length=200)
    reference_number = models.CharField(max_length=50, blank=True)
    counterparty = models.CharField(max_length=100, blank=True)
    counterparty_account = models.CharField(max_length=30, blank=True)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    running_balance = models.DecimalField(max_digits=20, decimal_places=2)
    is_reconciled = models.BooleanField(default=False)
    reconciliation_date = models.DateField(null=True, blank=True)
    matched_document = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

### **10. FinancialRatio (Finansal Oran)**
```python
class FinancialRatio(models.Model):
    calculation_date = models.DateField()
    period_type = models.CharField(max_length=10, choices=PERIOD_TYPE_CHOICES)
    current_ratio = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    quick_ratio = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    debt_to_equity = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    return_on_assets = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    return_on_equity = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    gross_margin = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    net_margin = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    asset_turnover = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    inventory_turnover = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    receivables_turnover = models.DecimalField(max_digits=8, decimal_places=4, null=True)
    dso = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # Days Sales Outstanding
    dpo = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # Days Payable Outstanding
    working_capital = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔧 API Endpoints

### **Currency & Exchange Rate APIs**
```
GET    /api/v1/finance/currencies/               # Para birimi listesi
POST   /api/v1/finance/currencies/               # Yeni para birimi
GET    /api/v1/finance/exchange-rates/           # Döviz kurları
POST   /api/v1/finance/exchange-rates/update/    # Kur güncelleme
GET    /api/v1/finance/exchange-rates/history/   # Kur geçmişi
```

### **Bank Management APIs**
```
GET    /api/v1/finance/banks/                    # Banka listesi
POST   /api/v1/finance/banks/                    # Yeni banka
GET    /api/v1/finance/bank-accounts/            # Banka hesabı listesi
POST   /api/v1/finance/bank-accounts/            # Yeni banka hesabı
GET    /api/v1/finance/bank-accounts/{id}/balance/ # Hesap bakiyesi
```

### **Check & Note Management APIs**
```
GET    /api/v1/finance/checks/                   # Çek listesi
POST   /api/v1/finance/checks/                   # Yeni çek
PUT    /api/v1/finance/checks/{id}/collect/      # Çek tahsilat
PUT    /api/v1/finance/checks/{id}/bounce/       # Çek iadesi
GET    /api/v1/finance/promissory-notes/         # Senet listesi
POST   /api/v1/finance/promissory-notes/         # Yeni senet
```

### **Credit Management APIs**
```
GET    /api/v1/finance/credit-limits/            # Kredi limiti listesi
POST   /api/v1/finance/credit-limits/            # Yeni kredi limiti
PUT    /api/v1/finance/credit-limits/{id}/       # Kredi limiti güncelleme
POST   /api/v1/finance/credit-limits/{id}/hold/  # Kredi durdurma
POST   /api/v1/finance/credit-score/calculate/   # Kredi puanı hesaplama
```

### **Cash Flow APIs**
```
GET    /api/v1/finance/cash-flow/forecast/       # Nakit akış tahmini
POST   /api/v1/finance/cash-flow/forecast/       # Yeni tahmin
GET    /api/v1/finance/cash-flow/actual/         # Gerçekleşen nakit akış
GET    /api/v1/finance/cash-position/            # Günlük nakit pozisyonu
```

### **Reporting APIs**
```
GET    /api/v1/finance/reports/financial-ratios/ # Finansal oranlar
GET    /api/v1/finance/reports/aging/            # Yaşlandırma raporu
GET    /api/v1/finance/reports/cash-flow/        # Nakit akış raporu
GET    /api/v1/finance/reports/profitability/    # Karlılık raporu
```

---

## 🎨 UI/UX Gereksinimleri

### **Finance Dashboard**
- Cash position overview
- Key financial ratios
- Upcoming due dates
- Credit utilization
- Exchange rate ticker

### **Treasury Management Interface**
- Bank account balances
- Cash flow timeline
- Investment portfolio
- Debt obligations

### **Credit Management Interface**
- Customer credit overview
- Risk assessment tools
- Payment behavior analysis
- Credit approval workflow

### **Check/Note Management**
- Due date calendar
- Collection tracking
- Status updates
- Batch processing

---

## 🚀 Implementation Plan

### **Phase 1: Core Financial (3 hafta)**
- Currency management
- Bank account setup
- Basic transactions
- Exchange rate integration

### **Phase 2: Credit Management (2 hafta)**
- Credit limit setup
- Risk assessment
- Payment tracking
- Automated controls

### **Phase 3: Instruments (2 hafta)**
- Check management
- Promissory notes
- Collection tracking
- Risk management

### **Phase 4: Treasury & Reporting (1 hafta)**
- Cash flow forecasting
- Financial ratios
- Advanced reporting
- Dashboard integration

---

**Status:** Planning Phase  
**Next Review:** TBD  
**Owner:** Context7 Development Team 