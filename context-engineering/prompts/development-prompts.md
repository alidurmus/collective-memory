# 💬 Development Prompts

**Context Engineering Template - AI Development Prompts**

Bu dosya, Collective Memory projesinde AI destekli geliştirme için hazırlanmış prompt şablonlarını içerir.

## 🧪 Test Development Prompts

### Backend Test Creation
```
Bu Python modülü için kapsamlı pytest testleri oluştur:
- Test coverage minimum %80 olmalı
- Edge case'leri dahil et
- Mock kullanarak external dependencies'i izole et
- [[memory:592592]] - Playwright UI testleri için ayrı dosya oluştur

Modül: [MODULE_NAME]
Fonksiyonlar: [FUNCTION_LIST]
```

### UI Test Creation  
```
Bu React/Context7 komponenti için Playwright testleri yaz:
- Kullanıcı etkileşimlerini test et
- Responsive design kontrolü dahil et  
- Türkçe UI elementlerini test et [[memory:2176195]]
- Error state'leri kontrol et

Komponent: [COMPONENT_NAME] 
Sayfalar: [PAGE_LIST]
```

## 🎨 UI/UX Development Prompts

### Context7 Component Creation
```
Context7 framework kullanarak modern bir [COMPONENT_TYPE] komponenti oluştur:
- Glassmorphism effect'leri uygula
- Türkçe arayüz dili [[memory:2176195]]
- Responsive design (mobile-first)
- Accessibility standartlarına uygun
- Dark/light mode desteği

Özellikler: [FEATURE_LIST]
```

### Database Schema Design
```
Django ORM kullanarak bu veri modeli için schema tasarla:
- UUID primary keys kullan
- Soft delete pattern uygula
- Created/updated tracking ekle
- Multi-company support dahil et

Entity: [ENTITY_NAME]
Relationships: [RELATIONSHIP_LIST]
```

## 🔧 Integration Prompts

### API Integration
```
Bu REST API endpoint'i için Django view oluştur:
- JWT authentication kullan
- Pagination dahil et
- Error handling ekle
- API documentation (swagger) ready
- Context7 tools entegrasyonu [[memory:592593]]

Endpoint: [ENDPOINT_NAME]
Method: [HTTP_METHOD]
Parameters: [PARAM_LIST]
```

### Context7 Library Integration
```
Context7 kütüphanesi kullanarak bu özelliği entegre et:
- Library documentation araçlarını kullan [[memory:592593]]  
- Modern API design patterns uygula
- Error handling ve logging ekle
- Performance optimization dahil et

Feature: [FEATURE_NAME]
Integration Points: [INTEGRATION_LIST]
```

## 🐛 Debugging Prompts

### Error Analysis
```
Bu hata için kapsamlı analiz ve çözüm öner:
- Root cause analysis yap
- Context Engineering Template yapısına uygun çözüm
- Prevention strategies dahil et
- Test case'leri öner

Error: [ERROR_MESSAGE]
Stack Trace: [STACK_TRACE]
Context: [ERROR_CONTEXT]
```

### Performance Optimization  
```
Bu kod bloğunu optimize et:
- Performance bottleneck'leri tespit et
- Memory usage optimize et
- Database query optimization
- Context7 best practices uygula

Code Block: [CODE_SNIPPET]
Performance Issue: [ISSUE_DESCRIPTION]
```

## 📚 Documentation Prompts

### Technical Documentation
```
Bu özellik için kapsamlı teknik dokümantasyon oluştur:
- Context Engineering Template formatında
- Code examples dahil et
- Usage guidelines ekle  
- Troubleshooting section

Feature: [FEATURE_NAME]
Target Audience: [AUDIENCE_TYPE]
```

## 🚀 Deployment Prompts

### Production Setup
```
Bu uygulamayı production ortamına deploy etmek için:
- Environment configuration
- Security checklist
- Performance monitoring setup
- Backup strategies

Environment: [ENV_TYPE]
Platform: [PLATFORM_NAME]
```

---

**⚙️ Usage**: Bu prompt'ları kullanırken [PLACEHOLDER] değerlerini gerçek değerlerle değiştirin.  
**🔗 Context**: Her prompt'ta ilgili memory referansları dahil edilmiştir.  
**📋 Update**: Yeni özellikler eklendiğinde bu prompt'ları güncelleyin. 