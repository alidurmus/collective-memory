# Query Processing Rules - Smart Context Bridge Integration

## Overview

Bu dosya, "query:" ile başlayan sorgular için otomatik dokümantasyon oluşturma kurallarını içerir. Smart Context Bridge sistemi ile entegre edilmiş ve Collective Memory projesinin standartlarına uygun olarak oluşturulmuştur.

## Query Detection Rules

### 🔍 Query Detection System

#### 1. **"query:" Prefix Detection**
- **Trigger:** Kullanıcı mesajı "query:" ile başladığında
- **Action:** Otomatik README.md dokümantasyonu oluştur
- **Format:** Standart 4-doküman yapısı (design.md, requirements.md, tasks.md, solution.md)

#### 2. **Query Processing Workflow**
1. **Query Detection:** "query:" prefix'i tespit et
2. **Memory Context:** Hafızadaki ilgili bilgileri analiz et
3. **Documentation Creation:** README.md ve 4 ana dokümanı oluştur
4. **Rule Update:** Sisteme yeni kuralları ekle
5. **Integration:** Mevcut sistemle entegre et

#### 3. **README.md Generation Standards**
- **Structure:** Proje genelinde tutarlı format
- **Content:** Query'nin çözümü ve implementasyonu
- **Integration:** Smart Context Bridge ile entegrasyon
- **Documentation:** 4 ana doküman referansları
- **Memory Context:** Hafızadaki ilgili bilgiler

## Memory Integration Rules

### 🧠 Smart Context Bridge Integration

#### 1. **Memory Context Analysis**
- Hafızadaki ilgili bilgileri tespit et
- Önceki çözümleri ve yaklaşımları analiz et
- Sistem durumunu ve mevcut implementasyonları kontrol et

#### 2. **Pattern Recognition**
- Benzer sorunların çözümlerini tanımla
- Tekrar eden pattern'ları belirle
- En iyi pratikleri uygula

#### 3. **Context Continuity**
- Smart Context Bridge bilgilerini kullan
- JSON Chat System entegrasyonunu göz önünde bulundur
- Mevcut sistem mimarisine uyum sağla

### 📊 Memory Utilization Guidelines

#### 1. **Smart Context Bridge Status**
- **Status:** Phase 4 %100 tamamlanmış
- **Features:** Real-time JSON monitoring, Automatic context generation, Zero manual work required
- **Performance:** Context generation in 85ms, File monitoring in 12ms
- **Accuracy:** 1.0/1.0 relevance score

#### 2. **System Architecture Context**
- **JSON Chat System:** Tam entegre edilmiş
- **Enterprise Features:** Phase 3 %100 tamamlanmış
- **WebSocket Integration:** Windows compatibility gerekli
- **CLI Interface:** Güncellenmiş ve tutarlı

#### 3. **Documentation Standards**
- **Consistency:** Düzeltilmiş
- **Structure:** Standartlaştırılmış
- **Templates:** Hazır
- **Quality:** Kontrol edilmiş

## Query Processing Implementation

### 🔧 Automatic Documentation Generation

#### 1. **Query Detection System**
```python
def detect_query(message: str) -> bool:
    """Query prefix'ini tespit et"""
    return message.strip().lower().startswith("query:")

def process_query(query_message: str) -> Dict[str, Any]:
    """Query'yi işle ve dokümantasyon oluştur"""
    # Query analizi
    query_analysis = analyze_query(query_message)
    
    # Memory context extraction
    memory_context = extract_memory_context(query_analysis)
    
    # Documentation generation
    documentation = generate_documentation(query_analysis, memory_context)
    
    # Rule updates
    update_rules(query_analysis)
    
    return documentation
```

#### 2. **README.md Template for Query Solutions**
```markdown
# [Query Solution Name] - Implementation Guide

## Overview
Brief description of the query solution and its purpose

## Problem Statement
- Query description
- Context and background
- Impact assessment

## Solution Approach
- High-level solution overview
- Key components and features
- Integration points

## Implementation
### Prerequisites
- System requirements
- Dependencies
- Configuration

### Installation
- Step-by-step installation guide
- Configuration instructions
- Verification steps

### Usage
- Basic usage examples
- Advanced features
- Troubleshooting

## Documentation Structure
- **Design Document:** [design.md](design.md)
- **Requirements:** [requirements.md](requirements.md)
- **Implementation Plan:** [tasks.md](tasks.md)
- **Solution Reference:** [solution.md](solution.md)

## Memory Integration
- Smart Context Bridge integration
- JSON Chat System usage
- Enterprise features utilization

## Testing and Validation
- Test scenarios
- Performance metrics
- Quality assurance

## Maintenance and Updates
- Regular maintenance tasks
- Update procedures
- Monitoring and alerts
```

#### 3. **Rule Update System**
```python
def update_rules(query_analysis: Dict[str, Any]) -> None:
    """Query analizine göre kuralları güncelle"""
    # Yeni kuralları sisteme ekle
    new_rules = generate_rules_from_query(query_analysis)
    
    # Mevcut kuralları güncelle
    existing_rules = load_existing_rules()
    updated_rules = merge_rules(existing_rules, new_rules)
    
    # Kuralları kaydet
    save_rules(updated_rules)
    
    # Smart Context Bridge'e bildir
    notify_context_bridge(updated_rules)
```

## Processed Queries

### Create a new feature for user authentication

#### Query
create a new feature for user authentication

#### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

#### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

#### Status
- **Created:** 2025-07-18 11:10:19
- **Status:** Active
- **Complexity:** High

## Quality Standards

### 📋 Documentation Quality Standards

#### 1. **Completeness**
- Tüm gerekli bilgileri içer
- Edge cases ve error scenarios kapsa
- Cross-references sağla

#### 2. **Consistency**
- Mevcut proje standartlarına uy
- Terminology tutarlılığı sağla
- Formatting standartlarını takip et

#### 3. **Accuracy**
- Hafızadaki bilgileri doğru kullan
- Technical specifications doğrula
- Implementation details kontrol et

#### 4. **Usability**
- Kolay navigasyon sağla
- Clear target audience identification
- Practical examples ekle

## Best Practices

### 📚 Documentation Best Practices

#### 1. **Structure Consistency**
- Her sorgu için aynı 4-doküman yapısını kullan
- Template'leri tutarlı şekilde uygula
- Cross-references sağla

#### 2. **Memory Integration**
- Hafızadaki bilgileri aktif olarak kullan
- Mevcut sistem durumunu göz önünde bulundur
- Önceki çözümleri referans al

#### 3. **Quality Assurance**
- Technical accuracy kontrol et
- Completeness doğrula
- Usability test et

#### 4. **Maintenance**
- Regular updates sağla
- Version control kullan
- User feedback entegre et

### 🔧 Technical Best Practices

#### 1. **Code Examples**
- Language-specific syntax highlighting kullan
- Complete, runnable examples sağla
- Error handling include et

#### 2. **Configuration**
- Environment variables kullan
- Platform-specific settings belirt
- Security considerations ekle

#### 3. **Testing**
- Unit test examples ekle
- Integration test scenarios belirt
- Performance test metrics sağla

## Tools and Resources

### 📝 Documentation Tools
- Markdown editors
- Version control systems
- Template management
- Quality check tools

### 🧠 Memory Integration Tools
- Smart Context Bridge monitoring
- JSON Chat System analysis
- System status tracking
- Context generation tools

### 🔍 Query Analysis Tools
- Problem pattern recognition
- Solution template matching
- Memory context extraction
- Cross-reference validation

## Contact and Support

For questions about query processing or documentation standards:

- **Project Repository:** [GitHub Repository](https://github.com/alidurmus/collective-memory)
- **Documentation Issues:** [GitHub Issues](https://github.com/alidurmus/collective-memory/issues)
- **Main Documentation:** [docs/INDEX.md](../../docs/INDEX.md)
- **Smart Context Bridge:** [SMART_CONTEXT_BRIDGE_GUIDE.md](../../docs/user-guides/SMART_CONTEXT_BRIDGE_GUIDE.md)

---

**Last Updated:** 18 Temmuz 2025  
**Version:** 2.0  
**Status:** Active Development  
**Memory Integration:** ✅ Active  
**Query Processing:** ✅ Active with README.md Generation


## Test smart context bridge integration

### Query
test smart context bridge integration

### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

### Status
- **Created:** 2025-07-18 11:13:09
- **Status:** Active
- **Complexity:** Medium


## Test query processing system

### Query
test query processing system

### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

### Status
- **Created:** 2025-07-18 11:14:48
- **Status:** Active
- **Complexity:** Medium


## Create a new feature for user authentication

### Query
create a new feature for user authentication

### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

### Status
- **Created:** 2025-07-18 11:14:53
- **Status:** Active
- **Complexity:** High


## Frontpage güncelle

### Query
frontpage güncelle

### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

### Status
- **Created:** 2025-07-18 11:26:03
- **Status:** Active
- **Complexity:** Low


## Standartlarına uygun dokümante et

### Query
standartlarına uygun dokümante et

### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

### Status
- **Created:** 2025-07-18 14:28:57
- **Status:** Active
- **Complexity:** Medium


## Dokümantasyon standartları özeti

### Query
dokümantasyon standartları özeti

### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

### Status
- **Created:** 2025-07-18 14:33:34
- **Status:** Active
- **Complexity:** Low


## Görevleri tamamla özeti

### Query
görevleri tamamla özeti

### Processing Rules
- **Trigger:** "query:" prefix detection
- **Action:** Automatic documentation generation
- **Output:** README.md + 4 core documents
- **Integration:** Smart Context Bridge

### Memory Context
- Smart Context Bridge Phase 4: Active
- JSON Chat System: Integrated
- Enterprise Features: Available

### Status
- **Created:** 2025-07-18 14:47:12
- **Status:** Active
- **Complexity:** Low
