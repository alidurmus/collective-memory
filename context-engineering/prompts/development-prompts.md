# 🤖 AI Development Prompts - Context Engineering Template

**Collective Memory System Development Prompts**

Bu dosya, Collective Memory sisteminin geliştirilmesi için AI asistanlarına gönderilecek standart prompt'ları içerir. Her prompt, Context Engineering Template metodolojisine uygun olarak tasarlanmıştır.

---

## 🏗️ System Architecture Prompts

### 1. Sistem Mimarisi Analizi
```
Context Engineering Template yapısına uygun olarak Collective Memory sisteminin mevcut mimarisini analiz et. 
Şu klasör yapısını incele:
- context-engineering/commands/ (executable scripts)
- context-engineering/context/ (project context)
- context-engineering/output/ (generated results)
- context-engineering/prompts/ (AI templates)
- collective-memory-app/ (main application)

Analiz sonucunda:
1. Mimari güçlü yönleri
2. İyileştirme alanları
3. Context Engineering Template standardına uyumluluk
4. Önerilen değişiklikler

Raporu markdown formatında oluştur.
```

### 2. Performance Optimization
```
Collective Memory sisteminin performansını optimize et. Şu metrikleri hedefle:
- API Response Time: <500ms
- Search Response Time: <100ms
- Memory Usage: <512MB
- CPU Usage: <70%
- Cache Hit Rate: >80%

Optimizasyon alanları:
1. Database query optimization
2. Frontend bundle size reduction
3. Memory leak prevention
4. Caching strategies
5. Lazy loading implementation

Tüm değişiklikleri Context Engineering Template yapısına uygun olarak uygula.
```

---

## 🎨 UI/UX Development Prompts

### 3. Context7 Framework Enhancement
```
Context7 glassmorphism framework'ünü geliştir ve şu özellikleri ekle:

Turkish UI Requirements [[memory:2176195]]:
- Tüm kullanıcı arayüzü metinleri Türkçe
- Değişken isimleri ve kod yorumları İngilizce
- Türkçe tarih/saat formatları (tr-TR locale)
- Türkçe sayı formatları

Context7 Design Features:
- Modern glassmorphism efektleri
- Gradient renk paleti (#667eea, #764ba2)
- Backdrop-filter blur effects
- Responsive design patterns
- Accessibility compliance (WCAG 2.1 AA)

Uygulama dosyaları:
- frontend/src/styles/context7.css
- frontend/src/components/Dashboard.jsx
- frontend/src/components/SearchPanel.jsx
- frontend/src/components/Header.jsx
```

### 4. Responsive Design Implementation
```
Collective Memory web dashboard'ını tamamen responsive hale getir:

Breakpoints:
- Mobile: 320px - 768px
- Tablet: 768px - 1024px  
- Desktop: 1024px+
- Wide: 1440px+

Requirements:
1. Mobile-first approach
2. Touch-friendly UI elements (min 44px)
3. iOS zoom prevention (font-size: 16px for inputs)
4. Optimized performance on mobile
5. Context7 glassmorphism preserved on all devices

Turkish UI Standards:
- "Ana Panel", "Akıllı Arama", "Analitikler", "Ayarlar"
- Turkish error messages and user feedback
- Proper Turkish typography (line-height: 1.7)
```

---

## 🔍 Search & AI Integration Prompts

### 5. Semantic Search Enhancement
```
Collective Memory'ye gelişmiş semantic search özelliği ekle:

Technical Requirements:
- Sentence Transformers model integration (all-MiniLM-L6-v2)
- Vector similarity search
- Hybrid search (traditional + semantic)
- Query expansion
- Result re-ranking

Features:
1. Intelligent query understanding
2. Context-aware search results
3. Similar document suggestions
4. Multi-language support (Turkish/English)
5. Search result export (markdown, JSON)

Implementation:
- backend: enhanced_query_engine.py
- frontend: SearchPanel.jsx with semantic toggle
- API: /search endpoint with semantic parameter
```

### 6. Prompt Relationship System
```
AI prompt'ları arasında ilişki kuran akıllı sistem geliştir:

Database Schema:
- prompt_history table (text, hash, search_type, results_count)
- prompt_relationships table (similarity_score, relationship_type)
- prompt_context table (weighted key-value pairs)

Features:
1. Automatic prompt tracking
2. Similarity calculation (keyword overlap)
3. Context preservation across sessions
4. Smart suggestions based on history
5. One-click prompt reuse

Turkish UI:
- "Benzer Aramalar" section
- "Önerilen Bağlam" suggestions
- "%85 benzer" similarity percentages
```

---

## 🧪 Testing & Quality Prompts

### 7. Playwright UI Testing
```
Collective Memory için kapsamlı Playwright testleri yaz [[memory:592592]]:

Test Categories:
1. Dashboard functionality tests
2. Search interface tests
3. Context7 component tests
4. Turkish UI validation tests
5. Responsive design tests
6. Performance tests

Turkish UI Test Cases:
- Turkish text rendering correctly
- Turkish date/time formats working
- Turkish input validation
- Error messages in Turkish
- Navigation labels in Turkish

Test Files:
- tests/ui/dashboard.spec.js
- tests/ui/search.spec.js
- tests/ui/turkish-ui.spec.js
- tests/ui/responsive.spec.js

Configuration:
- playwright.config.js with Turkish locale
- Multi-browser testing (Chrome, Firefox, Safari)
- Screenshot comparison tests
```

### 8. Performance Testing Suite
```
Comprehensive performance testing suite oluştur:

Performance Metrics:
1. Lighthouse scores (>90)
2. Core Web Vitals
   - LCP: <2.5s
   - FID: <100ms
   - CLS: <0.1
3. API response times
4. Memory usage monitoring
5. Bundle size analysis

Test Implementation:
- Automated performance regression tests
- Real-world usage simulation
- Memory leak detection
- Database query optimization validation

Reports:
- Performance dashboard
- Trend analysis over time
- Alerting for performance degradation
```

---

## 🔧 Development Workflow Prompts

### 9. Context Engineering Integration
```
Context Engineering Template metodolojisini tam olarak entegre et:

Required Components:
1. commands/ - Executable scripts
   - setup.py (environment setup)
   - test-runner.py (comprehensive testing)
   - performance-optimizer.py (system optimization)
   - deploy.sh (deployment automation)

2. context/ - Project context
   - config.json (system configuration)
   - project-rules.md (development standards)
   - architecture.md (system documentation)

3. output/ - Generated results
   - test-reports/ (test execution results)
   - performance-reports/ (optimization results)
   - build-artifacts/ (deployment packages)

4. prompts/ - AI templates
   - development-prompts.md (this file)
   - debugging-prompts.md (troubleshooting)
   - optimization-prompts.md (performance tuning)

Integration Requirements:
- All scripts executable from project root
- Consistent output formatting
- Error handling and logging
- Progress reporting
```

### 10. Continuous Integration Setup
```
GitHub Actions CI/CD pipeline kur:

Workflow Stages:
1. Code Quality Checks
   - ESLint (frontend)
   - Flake8 (backend)
   - Prettier formatting
   - Type checking

2. Testing
   - Unit tests (pytest)
   - Integration tests
   - UI tests (Playwright)
   - Performance tests

3. Build & Deploy
   - Frontend build (Vite)
   - Docker image creation
   - Security scanning
   - Deployment automation

Turkish UI Validation:
- Check for Turkish text consistency
- Validate tr-TR locale usage
- Ensure English code standards
- Turkish documentation generation

Context Engineering Template Integration:
- Run context-engineering/commands/test-runner.py
- Generate reports in context-engineering/output/
- Validate project structure compliance
```

---

## 🚀 Deployment & Production Prompts

### 11. Production Deployment
```
Production-ready deployment stratejisi geliştir:

Infrastructure:
1. Docker containerization
2. Reverse proxy setup (nginx)
3. SSL certificate implementation
4. Database backup strategy
5. Monitoring and logging

Security:
- Input validation and sanitization
- Rate limiting
- CORS configuration
- Security headers
- Authentication (optional)

Performance:
- CDN integration
- Asset optimization
- Caching strategies
- Load balancing
- Database optimization

Monitoring:
- Health checks
- Error tracking
- Performance monitoring
- User analytics (privacy-compliant)
```

### 12. Documentation Generation
```
Comprehensive documentation oluştur:

Documentation Types:
1. User Guide (Turkish)
   - Hızlı başlangıç kılavuzu
   - Detaylı kullanım rehberi
   - Sorun giderme
   - SSS

2. Developer Documentation (English)
   - API documentation
   - Architecture overview
   - Contributing guidelines
   - Code standards

3. Deployment Guide
   - Installation instructions
   - Configuration options
   - Troubleshooting
   - Security best practices

Auto-generation:
- API docs from code comments
- Component documentation from JSDoc
- Database schema documentation
- Performance benchmarks

Turkish Localization:
- All user-facing documentation in Turkish
- Technical documentation in English
- Bilingual README.md
- Context-sensitive help in UI
```

---

## 🎯 Usage Instructions

### Prompt Selection Guidelines

1. **System Development**: Use prompts 1-2 for architecture and performance
2. **UI/UX Enhancement**: Use prompts 3-4 for interface improvements  
3. **Search Features**: Use prompts 5-6 for AI and search functionality
4. **Quality Assurance**: Use prompts 7-8 for testing and validation
5. **DevOps**: Use prompts 9-12 for workflow and deployment

### Context Preparation

Before using any prompt, provide this context:
```
@Files frontend/src/components/
@Files backend/src/
@Docs context-engineering/context/config.json
@Rules Turkish UI + English code standard
@Rules Context7 framework usage
@Rules Playwright testing requirements
```

### Expected Outputs

Each prompt should generate:
- ✅ Working code implementations
- ✅ Updated documentation
- ✅ Test coverage
- ✅ Performance considerations
- ✅ Turkish UI compliance
- ✅ Context Engineering Template adherence

---

*Generated by Context Engineering Template - Collective Memory v2.1* 