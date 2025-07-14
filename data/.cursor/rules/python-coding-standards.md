# 🐍 Context7 ERP System - Python Coding Standards

**Last Updated:** 13 Temmuz 2025  
**System Status:** 100% Complete - Production Ready + **Reports Organization Excellence** ✅ 🏆  
**QMS Reference:** REC-PYTHON-STANDARDS-250713-001  
**Modern Tools:** Ruff, Black, MyPy, isort, pre-commit + **Enterprise Reports Management** ✅

## 🛠️ Modern Python Development Tools

### **Automated Code Quality Tools** ✅
```bash
# Ultra-fast linting and formatting
ruff check .                 # 10-100x faster than alternatives
ruff format .                # Modern formatter

# Code formatting standards
black .                      # Opinionated code formatter
isort .                      # Import organization

# Type checking and security
mypy .                       # Static type checking
bandit -r .                  # Security vulnerability scanning
safety check                 # Dependency vulnerability detection
```

### **Development Workflow Integration** ✅
- **VS Code Integration**: `.vscode/settings.json` with auto-formatting
- **Pre-commit Hooks**: `.pre-commit-config.yaml` with quality gates
- **CI/CD Pipeline**: GitHub Actions with multi-stage quality checks
- **Makefile Commands**: `make format`, `make lint`, `make qa`

### **Configuration Standards** ✅
- **pyproject.toml**: Modern Python project configuration
- **Line length**: 88 characters (Black standard)
- **Python version**: >=3.8 compatibility
- **Django plugin**: MyPy Django plugin for better type checking

## General Code Quality
- Kod basit, modüler ve okunabilir olmalı
- DRY (Don't Repeat Yourself) ilkesine uy
- KISS (Keep It Simple, Stupid) ilkesine uy
- Kodda gereksiz tekrarları önle, işlevleri böl
- Single Responsibility Principle (SRP) uygula
- Fonksiyon ve sınıf adları açıklayıcı olsun
- Magic number'lar yerine named constant'lar kullan

## Python Coding Rules
### Code Style
- **PEP8 standartlarına uygun** yaz (Ruff ile otomatik kontrol)
- **Type hints** tüm fonksiyonlara ve sınıflara ekle (MyPy ile kontrol)
- **Docstrings** fonksiyonlara ekle (PEP257)
- **`try/except` bloklarında** yalnızca belirli istisnaları yakala
- **F-string'leri** format() yerine tercih et
- **List/dict comprehension'ları** gereksiz loop'lar yerine kullan

### Import Organization
- Import'ları standart, third-party, local olarak grupla:
  ```python
  # Standard library imports
  import os
  import sys
  
  # Third-party imports
  import Django
  import requests
  
  # Local application imports
  from .models import MyModel
  from .utils import my_function
  ```

## Django Framework Rules
### Models
- Model'larda Meta class ile ordering, verbose_name tanımla
- Model field'larında appropriate validators kullan
- Foreign key'lerde on_delete davranışını explicit belirt
- CharField için max_length, DecimalField için max_digits/decimal_places belirt
- Financial calculations için Decimal field kullan
- Audit trail için created_at, updated_at fields ekle

### Views
- View'larda Class-Based View'ları Function-Based View'lar yerine tercih et
- Business logic'i service layer'da implement et
- User permissions için department-based access control

### Templates
- Template'lerde {% load %} tag'lerini dosya başında topla
- Department-specific templates'leri organize et

### URLs
- URL pattern'ları descriptive name'ler ile tanımla
- API versioning için /api/v1/ pattern kullan

### Settings
- Settings'i environment variables ile yönet (.env kullan)
- Middleware'leri doğru sırada yerleştir
- Environment-specific settings files oluştur (.env, .env.production)

### Management Commands
- Custom management command'ları `management/commands/` altında oluştur

### Admin
- Admin interface'i custom AdminConfig ile genişlet

### ORM Best Practices
- Django ORM'de select_related ve prefetch_related kullan
- Migration dosyalarını manuel olarak düzenleme
- N+1 query problemini select_related/prefetch_related ile çöz
- Raw SQL yerine ORM queryset'lerini tercih et
- Model method'larında business logic, manager'larda query logic

## ERP System Specific Rules
### Department Structure
- 8 departmental dashboard'ları maintain et (Production, Inventory, Sales, etc.)
- Model relationships için ForeignKey/ManyToMany kullan
- ERP data validation'ı model level'da yap

### Business Logic
- Business logic'i service layer'da implement et
- Service katmanında iş mantığını, API katmanında yönlendirmeyi yaz

## Database and ORM Rules
### Performance
- Database query'lerini optimize et (select_related, prefetch_related)
- Database index'leri performance-critical field'lara ekle
- Bulk operations için bulk_create, bulk_update kullan
- Database connection pooling implement et

### Transactions
- Database transaction'ları @transaction.atomic ile yönet

### PostgreSQL/SQLite
- PostgreSQL production, SQLite development için hazır ol

## Error Handling & Logging

### Exception Handling
- **Specific exceptions**: Genel `Exception` catch etme, spesifik exception'ları yakala
- **Business logic errors**: Custom exception classes oluştur (ERPValidationError vs.)
- **Context preservation**: Exception'da yeterli context bilgisi ver
- **Logging**: Her exception'ı proper logging ile kaydet

### **🔍 Proaktif Hata Düzeltme Kuralı** ✅ **CRITICAL METHODOLOGY**

#### **Python Geliştirmede Benzer Pattern Test Yaklaşımı**
- **Kural**: Düzeltilen hatalar, tespit edilen hatalar, düzeltilen sorunlar gibi durumları benzer yapılarda test et ve düzelt
- **Python-Specific Implementation**:
  1. **Import Hataları**: Düzeltilen import issue'larını benzer modüllerde kontrol et
  2. **Function Signatures**: Değiştirilen function'ların benzer kullanımlarını ara  
  3. **Exception Handling**: Fix edilen try-catch pattern'lerini system-wide kontrol et
  4. **Database Queries**: ORM optimization'larını benzer query'lerde uygula
  5. **Type Hints**: Eklenen type hint'leri benzer function'larda da implement et

#### **Python-Specific Search Patterns**
```python
# Example proactive fix methodology for Python
def proactive_python_fixes():
    """
    After fixing a Python issue, search for similar patterns
    """
    # 1. Import pattern fixes
    grep_patterns = [
        "from.*import.*",  # Import statements
        "def.*\\(.*\\):",  # Function definitions
        "class.*\\(.*\\):", # Class definitions
        "try:.*except.*:", # Exception handling
        "models\\..*\\.objects\\.", # Django ORM queries
    ]
    
    # 2. Search and validate each pattern
    for pattern in grep_patterns:
        similar_files = grep_search(pattern)
        validate_pattern_consistency(similar_files)
```

#### **Django-Specific Proactive Rules**
- **Model Changes**: Model field değişikliklerini related model'lerde kontrol et
- **View Patterns**: CBV/FBV pattern'lerini consistent şekilde uygula
- **URL Patterns**: URL configuration değişikliklerini related views'ta kontrol et
- **Template Usage**: Template değişikliklerini kullanan tüm view'larda test et
- **Migration Impact**: Migration'ların benzer field'larda impact'ini kontrol et

#### **Code Quality Integration**
- **Ruff/Black**: Format değişikliklerini project-wide uygula
- **MyPy**: Type checking issue'larını benzer pattern'lerde fix et
- **Security**: Bandit warning'lerini benzer code pattern'lerde kontrol et
- **Performance**: Performance optimization'ları benzer functionality'lerde uygula

### Logging Standards

## Security Implementation
### General Security
- Input validation middleware ile XSS/SQL injection prevention
- Custom password validators kullan
- File upload security validation yap
- IP address based security rules implement et
- Security audit logging yap

### Sensitive Data
- Ortam değişkenleri `.env` ile yönetilmeli, hardcode yapılmamalı
- Session security monitoring implement et

## Performance Optimization
### Database Performance
- Caching strategy'si implement et (Redis, Memcached)
- Lazy loading yerine eager loading kullan gerektiğinde
- Database indexing strategy'si oluştur
- Memory usage'ı monitor et, memory leak'lerden kaçın

### Application Performance
- Static files'ı CDN'den serve et
- Image optimization ve compression kullan
- Response compression (GZIP) aktifleştir
- Asynchronous task'lar için Celery kullan

## Code Documentation
### Docstrings
- Python'da fonksiyonlara docstring ekle
- Karmaşık işlem varsa neden yapıldığını açıklayan yorum ekle
- Code comment'larda "what" değil "why" açıkla

### Project Documentation
- README.md içinde proje açıklaması, kurulum talimatları ve örnek kullanım olsun
- API endpoints için comprehensive documentation oluştur
- Database schema documentation maintain et
- Deployment guide ve troubleshooting docs hazırla 