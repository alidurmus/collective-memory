# Query Solution System Rules

## Overview
Bu kurallar, Collective Memory sisteminde sorgu çözümü için standart yaklaşımı tanımlar. Her sorgu için hafızadaki bilgileri kullanarak kapsamlı dokümantasyon oluşturulur.

## Core Rules

### 1. Memory Integration Rules
- Her sorgu öncesi hafızadaki ilgili bilgileri kontrol et
- Smart Context Bridge durumunu göz önünde bulundur
- JSON Chat System entegrasyonunu değerlendir
- Enterprise Features durumunu analiz et

### 2. Documentation Structure Rules
Her sorgu çözümü için 4 ana doküman oluştur:
- **design.md** - Teknik tasarım dokümanı
- **requirements.md** - Gereksinimler dokümanı
- **tasks.md** - Implementasyon planı
- **solution.md** - Çözüm referans dokümanı

### 3. Template Usage Rules
- Verdiğiniz örnek yapıya uygun template'leri kullan
- docs/query/templates/ altındaki template'leri referans al
- Memory context bölümünü her dokümanda ekle
- System status bilgilerini güncel tut

### 4. Quality Standards Rules
- **Completeness**: Tüm gerekli bilgileri içer
- **Consistency**: Proje standartlarına uy
- **Accuracy**: Hafızadaki bilgileri doğru kullan
- **Usability**: Kolay navigasyon ve pratik örnekler

### 5. Integration Rules
- Mevcut sistem mimarisine uyum sağla
- Smart Context Bridge entegrasyonunu göz önünde bulundur
- JSON Chat System ile uyumlu çalış
- Enterprise Features ile entegre et

## Process Rules

### Query Processing Workflow
1. **Query Reception**: Sorguyu al ve analiz et
2. **Memory Context Analysis**: Hafızadaki bilgileri kontrol et
3. **Solution Design**: Template'lere uygun dokümanlar oluştur
4. **Solution Reference**: Çözüm referansını hazırla

### Task Execution Rules
- Oluşturulan task'ları sırayla işleme al
- Her task için progress raporu ver
- Çözümle ilgili tüm bilgileri bir çatı altında topla
- Genel dokümanları uygun yerlerde güncelle

## Memory Context Rules

### Smart Context Bridge Context
```markdown
### Memory Context: Smart Context Bridge
- **Status:** Phase 4 %100 tamamlanmış
- **Features:** Real-time JSON monitoring, automatic context generation
- **Performance:** 85ms context generation, 12ms file monitoring
- **Integration:** .cursor/rules/auto_context.md auto-update
- **User Experience:** Zero manual work required
```

### JSON Chat System Context
```markdown
### Memory Context: JSON Chat System
- **Status:** Tam entegre edilmiş
- **Features:** Structured conversation storage, REST API endpoints
- **CLI Interface:** chat_cli.py with create, search, export commands
- **Storage:** .collective-memory/conversations/ structure
- **Integration:** Cursor chat import functionality
```

### Enterprise Features Context
```markdown
### Memory Context: Enterprise Features
- **Status:** Phase 3 %100 tamamlanmış
- **Features:** Team collaboration, user management, real-time messaging
- **WebSocket:** Windows compatibility gerekli
- **API Server:** api_server.py with enterprise endpoints
- **Frontend:** React-based dashboard with Context7 framework
```

## Documentation Update Rules

### General Documentation Updates
- INDEX.md'yi güncelle
- README.md'yi güncelle
- İlgili user-guides'ları güncelle
- Cross-references ekle

### Specific Update Rules
- Yeni özellikler için uygun bölümlere ekle
- Mevcut bilgileri güncelle
- Tutarsızlıkları düzelt
- Eksik bilgileri tamamla

## Error Handling Rules

### CLI Error Handling
- ContextBridgeCLI'da `start()` metodu yok, `cmd_start()` kullan
- CLI komutlarını doğru şekilde uygula
- Hata mesajlarını anlaşılır hale getir

### System Integration Errors
- WebSocket Windows compatibility sorunlarını çöz
- Import hatalarını düzelt
- Configuration sorunlarını gider

## Success Criteria Rules

### Documentation Success
- 100% template coverage
- Standardized structure
- Memory integration accuracy
- Clear navigation

### System Integration Success
- INDEX.md integration completed
- Cross-references active
- Template availability ready
- Memory integration active

## Usage Instructions

### For New Queries
1. Hafızadaki bilgileri kontrol et
2. Template'leri kullanarak 4 doküman oluştur
3. Memory context ekle
4. Quality standards uygula
5. System integration sağla

### For Existing Solutions
1. Mevcut çözümleri referans al
2. Hafızadaki bilgileri güncelle
3. Cross-references ekle
4. General documentation güncelle

---

**Last Updated:** 18 Temmuz 2025  
**Version:** 1.0  
**Status:** Active  
**Memory Integration:** ✅ Active 