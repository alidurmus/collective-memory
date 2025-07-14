# 📜 Collective Memory - Proje Kuralları

## 🎯 Genel Proje Kuralları

### 🌐 Dil Standartları [[memory:2176195]]
- **Kullanıcı Arayüzü**: Türkçe (frontend, dokümantasyon, mesajlar)
- **Kod**: İngilizce (değişkenler, fonksiyonlar, class isimleri)
- **Yorumlar**: Türkçe (kullanıcı dostu açıklamalar)
- **Commit Mesajları**: İngilizce (uluslararası standart)

### 📚 Dokümantasyon Kuralları
- **README**: Türkçe + İngilizce paralel
- **API Dokümantasyonu**: İngilizce
- **Kullanıcı Kılavuzu**: Türkçe
- **Kod İçi Dokümantasyon**: İngilizce docstring + Türkçe açıklama

## 🔧 Teknical Kuralları

### 🐍 Python Standartları
- **Versiyon**: Python 3.9+ zorunlu
- **Type Hints**: Tüm fonksiyonlarda zorunlu
- **Docstring**: Google style dokümantasyon
- **Import Order**: isort ile otomatik sıralama
- **Code Style**: Black formatter + flake8 linter

```python
# ✅ Doğru örnek
def kullanici_bilgisi_getir(user_id: int) -> Dict[str, Any]:
    """
    Kullanıcı bilgilerini veritabanından getirir.
    
    Args:
        user_id: Kullanıcının benzersiz ID'si
        
    Returns:
        Kullanıcı bilgilerini içeren sözlük
        
    Raises:
        UserNotFoundError: Kullanıcı bulunamadığında
    """
    return {"id": user_id, "name": "Ali"}
```

### ⚛️ React/JavaScript Standartları
- **TypeScript**: Yeni component'lar için zorunlu
- **Functional Components**: Class component yasak
- **Hooks**: useState, useEffect, custom hooks
- **Props Interface**: TypeScript interface tanımı
- **Component Naming**: PascalCase

```tsx
// ✅ Doğru örnek
interface KullaniciKartProps {
  kullaniciId: number;
  isActive: boolean;
  onKullaniciClick: (id: number) => void;
}

const KullaniciKart: React.FC<KullaniciKartProps> = ({ 
  kullaniciId, 
  isActive, 
  onKullaniciClick 
}) => {
  // Türkçe state isimleri UI için
  const [kullaniciDetay, setKullaniciDetay] = useState<UserDetail | null>(null);
  
  return (
    <div className="kullanici-kart">
      {/* Component içeriği */}
    </div>
  );
};
```

### 🎨 Context7 Framework Kuralları [[memory:592593]]
- **Glassmorphism**: Modern UI efektleri zorunlu
- **Color Scheme**: Context7 standardı
- **Responsive**: Mobile-first approach
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Lighthouse score > 90

```css
/* ✅ Context7 standard */
.collective-memory-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}
```

## 🧪 Test Kuralları

### 🐍 Backend Testing [[memory:592592]]
- **Framework**: pytest zorunlu
- **Coverage**: Minimum %80 kod coverage
- **Test Structure**: AAA pattern (Arrange, Act, Assert)
- **Mocking**: unittest.mock kullanımı
- **Fixtures**: pytest fixtures for setup

```python
# ✅ Test örneği
def test_kullanici_bilgisi_getir_basarili():
    # Arrange (Hazırlık)
    user_id = 123
    expected_data = {"id": 123, "name": "Test User"}
    
    # Act (İşlem)
    result = kullanici_bilgisi_getir(user_id)
    
    # Assert (Doğrulama)
    assert result == expected_data
    assert result["id"] == user_id
```

### 🎭 Frontend Testing (Playwright) [[memory:592592]]
- **Framework**: Playwright zorunlu (sayfa testleri için)
- **Browser**: Chromium, Firefox, Safari
- **Selectors**: data-testid attribute kullanımı
- **Page Objects**: Sayfa nesnesi modeli
- **Turkish UI**: Türkçe element'ler için test

```javascript
// ✅ Playwright test örneği
import { test, expect } from '@playwright/test';

test('kullanıcı girişi başarıyla tamamlanır', async ({ page }) => {
  // Arrange
  await page.goto('http://localhost:3003');
  
  // Act
  await page.fill('[data-testid="kullanici-adi"]', 'testuser');
  await page.fill('[data-testid="sifre"]', 'password123');
  await page.click('[data-testid="giris-yap-btn"]');
  
  // Assert
  await expect(page.locator('[data-testid="hosgeldin-mesaj"]')).toBeVisible();
  await expect(page.locator('text=Hoşgeldin')).toBeVisible();
});
```

## 🔄 Instruction Processing Rules

### 🎯 Otomatik Talimat İşleme Süreci [[memory:3190909]]
- **Parçalama**: Her talimat anlamsal parçalara bölünür
- **Terminal Integration**: Her parça için gerekli komutlar çalıştırılır
- **Context Building**: Komut çıktıları analiz edilip context'e eklenir
- **Parallel Execution**: Mümkün olan tüm işlemler paralel yapılır
- **Progress Reporting**: Her adım için detaylı rapor verilir
- **Validation**: Sonuçlar doğrulanır ve kalite kontrol yapılır

### 📋 Workflow Adımları
1. **Analiz**: Talimatı parse et ve parçalara böl
2. **Bilgi Toplama**: Terminal komutları ile context oluştur
3. **Uygulama**: Paralel işlem önceliği ile talimatı yerine getir
4. **Doğrulama**: Sonuçları test et ve raporla

```bash
# ✅ Terminal komut örnek workflow
# Bilgi toplama aşaması
codebase_search "user authentication"
grep_search "login" --include="*.py"
read_file src/auth/views.py
git status

# Context'e ekleme formatı
[PARÇA 1] - Kullanıcı Authentication Analizi
Terminal Komutu: codebase_search "user authentication"
Çıktı: Authentication logic found in auth/views.py
Analiz: Django authentication kullanılıyor
Sonraki Adım: Login view implementation
```

## 📁 Dosya ve Klasör Kuralları

### 📂 Directory Structure
```
collective-memory/
├── context-engineering/     # Context Engineering Template
│   ├── commands/           # Executable scripts (.sh, .py)
│   ├── context/           # Project context files
│   ├── output/            # Generated outputs
│   └── prompts/           # AI prompt templates
├── collective-memory-app/  # Main application
│   ├── src/               # Python source code
│   ├── frontend/          # React application
│   ├── tests/             # Test files
│   ├── config/            # Configuration files
│   └── docs/              # API documentation
├── data/                  # Demo/example data only
└── docs/                  # General documentation
```

### 📝 Dosya Adlandırma
- **Python**: snake_case (user_manager.py)
- **JavaScript/TypeScript**: camelCase (userManager.ts)
- **CSS**: kebab-case (user-card.css)
- **Components**: PascalCase (UserCard.tsx)
- **Test Files**: test_ prefix (test_user_manager.py)
- **Documentation**: UPPER_CASE.md (README.md)

### 🏷️ Import Organizasyonu
```python
# ✅ Python import sırası
# 1. Standard library
import os
import json
from typing import Dict, List, Optional

# 2. Third party
import django
import pytest
from django.shortcuts import render

# 3. Local imports
from .models import User
from .utils import helper_function
```

## 🔒 Güvenlik Kuralları

### 🛡️ Veri Güvenliği
- **API Keys**: Environment variables'da sakla
- **Passwords**: Asla hardcode etme
- **Sensitive Data**: .gitignore'a ekle
- **SQL Injection**: ORM kullan, raw SQL yasak
- **XSS Protection**: Input sanitization zorunlu

### 🔐 Authentication/Authorization
- **Session Management**: Django sessions
- **CSRF Protection**: Django CSRF middleware
- **Rate Limiting**: API endpoint'ler için
- **Input Validation**: Tüm user input'ları validate et

## 📈 Performans Kuralları

### ⚡ Backend Performance
- **Database**: Query optimization, N+1 problem'i önle
- **Caching**: Redis ile cache stratejisi
- **API Response**: < 500ms response time
- **Memory Usage**: Profiling ve monitoring

### 🌐 Frontend Performance
- **Bundle Size**: < 2MB gzipped
- **Loading Time**: < 3 seconds first paint
- **Lighthouse Score**: > 90 performance
- **Image Optimization**: WebP format, lazy loading

## 🚀 Deployment Kuralları

### 🐳 Docker
- **Multi-stage builds**: Production için
- **Health checks**: Container health monitoring
- **Environment**: Development, staging, production
- **Security**: Non-root user, minimal base image

### 📦 CI/CD Pipeline
- **Git Flow**: Feature branch → develop → main
- **Pre-commit Hooks**: Black, flake8, tests
- **Automated Testing**: All tests pass before merge
- **Deployment**: Automated to staging, manual to production

## 📊 Monitoring ve Logging

### 📈 Monitoring
- **Health Checks**: System status endpoints
- **Performance Metrics**: Response time, memory usage
- **Error Tracking**: Automated error reporting
- **User Analytics**: Usage patterns, feature adoption

### 📝 Logging
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Structured Logging**: JSON format
- **Log Rotation**: Daily rotation, 30 day retention
- **Sensitive Data**: Never log passwords, API keys

```python
# ✅ Logging örneği
import logging

logger = logging.getLogger(__name__)

def kullanici_olustur(kullanici_data: Dict) -> User:
    logger.info(f"Yeni kullanıcı oluşturuluyor: {kullanici_data['email']}")
    try:
        user = User.objects.create(**kullanici_data)
        logger.info(f"Kullanıcı başarıyla oluşturuldu: {user.id}")
        return user
    except Exception as e:
        logger.error(f"Kullanıcı oluşturma hatası: {str(e)}")
        raise
```

## ✅ Code Review Kuralları

### 👀 Review Checklist
- [ ] Kod standartlarına uygun mu?
- [ ] Test coverage yeterli mi?
- [ ] Performance impact değerlendirildi mi?
- [ ] Security açığı var mı?
- [ ] Documentation güncel mi?
- [ ] Türkçe UI / İngilizce kod kuralına uyuyor mu?

### 📝 Pull Request Kuralları
- **Title**: feat/fix/docs: açıklayıcı başlık
- **Description**: Ne değiştirildi, neden değiştirildi
- **Screenshots**: UI değişiklikleri için
- **Testing**: Test sonuçları ve coverage report
- **Breaking Changes**: Varsa açıkça belirt 