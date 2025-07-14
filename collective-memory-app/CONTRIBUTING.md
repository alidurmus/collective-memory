# Contributing to Collective Memory

Collective Memory v2.1'e katkıda bulunduğunuz için teşekkür ederiz! Bu rehber katkı sürecinizi kolaylaştırmak için hazırlanmıştır.

## 🤝 Katkı Türleri

Aşağıdaki türlerde katkıları memnuniyetle karşılıyoruz:

- 🐛 **Bug Reports**: Hata bildirimleri
- ✨ **Feature Requests**: Yeni özellik önerileri  
- 📝 **Documentation**: Dokümantasyon iyileştirmeleri
- 🧪 **Tests**: Test coverage artırımı
- 🔧 **Bug Fixes**: Hata düzeltmeleri
- ⚡ **Performance**: Performans iyileştirmeleri
- 🎨 **UI/UX**: Arayüz geliştirmeleri
- 🌐 **Translations**: Çeviri katkıları

## 🚀 Başlangıç

### 1. Development Environment Setup

```bash
# 1. Repository'yi fork edin ve clone yapın
git clone https://github.com/YOUR_USERNAME/collective-memory.git
cd collective-memory

# 2. Backend dependencies kurun
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Frontend dependencies kurun
cd frontend
npm install

# 4. Pre-commit hooks kurma (opsiyonel)
pip install pre-commit
pre-commit install
```

### 2. Branch Strategy

```bash
# Ana branch'den yeni feature branch oluşturun
git checkout main
git pull origin main
git checkout -b feature/amazing-new-feature

# Veya bugfix için
git checkout -b fix/important-bug-fix
```

### 3. Development Workflow

#### Backend Development
```bash
# API server'ı development modunda başlatın
python api_server.py --debug

# Test modunda çalıştırın
python -m pytest tests/ -v

# Code quality kontrolleri
flake8 src/
black src/
```

#### Frontend Development
```bash
cd frontend

# Development server başlatın
npm run dev

# Test çalıştırın
npm test

# UI testleri için Playwright
npx playwright test --ui
```

## 📋 Coding Standards

### Python (Backend)

#### Code Style
- **Formatter**: Black (line length: 88)
- **Linter**: Flake8
- **Import sorting**: isort
- **Type hints**: Encouraged for public APIs

```python
# Good example
def search_documents(
    query: str, 
    max_results: int = 50, 
    semantic: bool = False
) -> List[SearchResult]:
    """Search documents with optional semantic processing.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        semantic: Enable semantic search using AI
        
    Returns:
        List of search results with relevance scores
    """
    # Implementation here
    pass
```

#### Testing
- **Test coverage**: Minimum %80
- **Test naming**: `test_function_name_scenario`
- **Fixtures**: Use pytest fixtures for setup/teardown
- **Mocking**: Mock external dependencies

```python
def test_search_documents_with_semantic_enabled():
    """Test that semantic search returns relevant results."""
    # Given
    query = "machine learning algorithms"
    
    # When
    results = search_documents(query, semantic=True)
    
    # Then
    assert len(results) > 0
    assert all(result.score > 0.5 for result in results)
```

### JavaScript/React (Frontend)

#### Code Style
- **Formatter**: Prettier
- **Linter**: ESLint
- **Component naming**: PascalCase
- **File naming**: camelCase

```javascript
// Good example - React component
import React, { useState, useEffect } from 'react';
import { useSearch } from '../hooks/useSearch';

export const SearchPanel = ({ onResults }) => {
  const [query, setQuery] = useState('');
  const { searchResults, isLoading, search } = useSearch();

  const handleSearch = async (event) => {
    event.preventDefault();
    if (query.trim()) {
      await search(query);
      onResults(searchResults);
    }
  };

  return (
    <form onSubmit={handleSearch} data-testid="search-form">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Arama yapın..."
        data-testid="search-input"
      />
      <button type="submit" disabled={isLoading} data-testid="search-button">
        {isLoading ? 'Aranıyor...' : 'Ara'}
      </button>
    </form>
  );
};
```

#### Testing
- **Test runner**: Playwright for UI tests
- **Test IDs**: Use `data-testid` attributes
- **Accessibility**: Test keyboard navigation and screen readers

```javascript
// Good example - Playwright test
test('search functionality works correctly', async ({ page }) => {
  // Given
  await page.goto('/search');
  
  // When
  await page.fill('[data-testid="search-input"]', 'test query');
  await page.click('[data-testid="search-button"]');
  
  // Then
  await expect(page.locator('[data-testid="search-results"]')).toBeVisible();
});
```

## 🐛 Bug Reports

### Issue Template

Hata bildirimi yaparken şu bilgileri ekleyin:

```markdown
## Bug Description
Hatanın kısa ve net açıklaması

## Steps to Reproduce
1. '...' adımını yapın
2. '...' seçeneğini tıklayın
3. '...' sonucunu gözlemleyin

## Expected Behavior
Beklenen davranışın açıklaması

## Actual Behavior
Gerçek davranışın açıklaması

## Environment
- OS: [Windows 10, macOS 12, Ubuntu 20.04]
- Python version: [3.9, 3.10, 3.11]
- Node version: [16.x, 18.x, 20.x]
- Browser: [Chrome 118, Firefox 119, Safari 17]

## Additional Context
Ekran görüntüleri, log dosyaları, vb.
```

### Priority Labels

- 🔴 **Critical**: Sistem çökmeleri, data kaybı
- 🟠 **High**: Ana özellikler çalışmıyor
- 🟡 **Medium**: Küçük özellik sorunları
- 🟢 **Low**: Kozmetik sorunlar, iyileştirmeler

## ✨ Feature Requests

### Feature Template

```markdown
## Feature Description
Özelliğin detaylı açıklaması

## Use Case
Bu özellik hangi sorunu çözüyor?

## Proposed Solution
Çözüm öneriniz (opsiyonel)

## Alternatives Considered
Değerlendirdiğiniz alternatifler

## Additional Context
Mockup'lar, referans linkler, vb.
```

## 🔄 Pull Request Process

### 1. Before Creating PR

```bash
# Kod kalitesi kontrolleri
python -m pytest tests/
flake8 src/
black --check src/

# Frontend testleri
cd frontend
npm test
npx playwright test
```

### 2. PR Template

```markdown
## Description
Bu PR'ın yaptığı değişikliklerin özeti

## Type of Change
- [ ] Bug fix (breaking olmayan değişiklik)
- [ ] New feature (breaking olmayan yeni özellik)
- [ ] Breaking change (mevcut işlevselliği bozabilir)
- [ ] Documentation update

## Testing
- [ ] Unit tests eklendi/güncellendi
- [ ] Integration tests çalıştırıldı
- [ ] UI tests passed

## Checklist
- [ ] Self-review yapıldı
- [ ] Code style guide'a uygun
- [ ] Yorum satırları güncellendi
- [ ] Dokümantasyon güncellendi
- [ ] Test coverage korundu

## Screenshots (UI değişiklikleri için)
Öncesi/sonrası ekran görüntüleri
```

### 3. Review Process

1. **Automated Checks**: CI/CD pipeline otomatik kontroller yapar
2. **Peer Review**: En az 1 maintainer review yapar
3. **Testing**: Functionality ve regression testleri
4. **Documentation**: Gerekli dokümantasyon güncellemeleri
5. **Merge**: Squash merge ile main branch'e alınır

## 🧪 Testing Guidelines

### Test Structure

```python
# Backend test structure
def test_feature_name_scenario():
    """Test description explaining what is being tested."""
    # Given - Setup test data and conditions
    setup_data()
    
    # When - Execute the action being tested
    result = function_under_test()
    
    # Then - Assert the expected outcome
    assert expected_condition(result)
```

```javascript
// Frontend test structure
test('feature name scenario', async ({ page }) => {
  // Given - Setup page state
  await page.goto('/test-page');
  
  // When - Perform action
  await page.click('[data-testid="action-button"]');
  
  // Then - Verify result
  await expect(page.locator('[data-testid="result"]')).toBeVisible();
});
```

### Coverage Requirements

- **Backend**: Minimum %80 test coverage
- **Frontend**: Critical user paths must be tested
- **API**: All endpoints must have integration tests
- **UI**: Key user workflows must have E2E tests

## 📝 Documentation

### Documentation Types

1. **Code Comments**: Complex logic açıklamaları
2. **Docstrings**: Function/class açıklamaları
3. **README Updates**: Yeni özellikler için
4. **API Documentation**: Endpoint değişiklikleri
5. **User Guides**: Kullanıcı dokümantasyonu

### Writing Guidelines

- **Clear and concise**: Kısa ve anlaşılır yazın
- **Examples**: Code örnekleri ekleyin
- **Turkish support**: Türkçe arayüz için Türkçe dokümantasyon
- **Screenshots**: UI değişiklikleri için görsel ekleyin
- **Links**: İlgili dokümanlara link verin

## 🌐 Internationalization

### Adding New Languages

1. **Frontend i18n**: React-i18next kullanımı
2. **Backend messages**: Multi-language error messages
3. **Documentation**: README ve guide'ların çevirisi
4. **Test coverage**: Çeviri testleri

```javascript
// i18n key example
const t = useTranslation();

return (
  <button>
    {t('search.button.label', 'Ara')}
  </button>
);
```

## 🚀 Release Process

### Version Numbering

- **Major** (x.0.0): Breaking changes
- **Minor** (x.y.0): New features, backward compatible
- **Patch** (x.y.z): Bug fixes

### Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version numbers bumped
- [ ] Release notes prepared
- [ ] Security review completed

## ⚡ Performance Guidelines

### Backend Performance

- **Database queries**: Use appropriate indexes
- **Caching**: Implement intelligent caching
- **Memory usage**: Monitor and optimize
- **API response time**: Target < 100ms

### Frontend Performance

- **Bundle size**: Monitor and optimize
- **Loading states**: Provide user feedback
- **Code splitting**: Lazy load components
- **Accessibility**: Maintain performance

## 🔒 Security Guidelines

### Security Best Practices

- **Input validation**: Validate all user inputs
- **SQL injection**: Use parameterized queries
- **XSS protection**: Sanitize HTML output
- **Authentication**: Secure session management
- **HTTPS**: Enforce secure connections

### Security Review Process

1. **Code review**: Security-focused review
2. **Dependency scan**: Check for vulnerabilities
3. **Penetration testing**: Manual security testing
4. **Compliance**: Follow security standards

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports ve feature requests
- **GitHub Discussions**: Genel sorular ve tartışmalar
- **Email**: security@collective-memory.dev (güvenlik sorunları)
- **Documentation**: Önce mevcut dokümantasyonu kontrol edin

### Mentorship

Yeni katkıcılar için mentor desteği mevcuttur:

- **Good first issue**: Yeni başlayanlar için etiketli issue'lar
- **Pair programming**: Deneyimli geliştiricilerle çalışma
- **Code review**: Detaylı feedback ve öğrenme

## 🎉 Recognition

Katkıcılarımızı takdir etme yollarımız:

- **Contributors file**: Tüm katkıcıların listesi
- **Release notes**: Major katkıların belirtilmesi
- **Hall of fame**: Önemli katkılar için özel bölüm

---

**Collective Memory'ye katkıda bulunduğunuz için tekrar teşekkür ederiz! Birlikte daha iyi bir knowledge management sistemi oluşturuyoruz.** 🚀 