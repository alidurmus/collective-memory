# 🏗️ Context Engineering Template - Site Yapısı

## 🎯 Template Organization

**Context Engineering Template** yapısına göre organize edilmiş site mimarisi.

> **Detaylı Proje Yapısı**: [`../../docs/README.md`](../../docs/README.md) ve [`../../README.md`](../../README.md) dosyalarında bulunabilir.

## 📁 Context Engineering Template Yapısı

### 🧠 Template Directory Structure
```
context-engineering/
├── commands/                     # 🔧 Executable scripts
│   ├── test-runner.sh           # Test çalıştırma betiği
│   ├── setup.py                 # Proje kurulum scripti
│   └── deploy.sh                # Deployment scripti
├── context/                     # 🧠 Project context files
│   ├── 01_persona.md            # Kullanıcı persona tanımları
│   ├── 02_project_overview.md   # Proje genel bakışı
│   ├── 03_rules.md              # Detaylı proje kuralları
│   ├── 04_site_structure.md     # Site yapısı (bu dosya)
│   ├── 05_tech_stack.md         # Context Engineering tech stack
│   ├── 06_software_architecture.md # Yazılım mimarisi
│   ├── 07_content_guidelines.md # İçerik yönergeleri
│   ├── 08_ui_ux_guidelines.md   # UI/UX tasarım kuralları
│   └── 09_instruction_processing_rules.md # Talimat işleme
├── output/                      # 📤 Generated outputs
│   ├── test-reports/            # Test sonuçları
│   ├── build-artifacts/         # Build çıktıları
│   └── documentation/           # Generated docs
└── prompts/                     # 💬 AI prompt templates
    ├── development-prompts.md   # Geliştirme promptları
    └── ai-templates.md          # AI kod şablonları
```

## 🌐 Integration Points

### Main Application Integration
```
collective-memory/
├── context-engineering/         # 🏗️ Template implementation
├── docs/                       # 📚 Merkezi dokümantasyon hub
├── collective-memory-app/      # 🚀 Ana uygulama
└── data/                       # 📋 Demo/test data
```

### Context Engineering Workflow
```
1. Context Files    → AI understands project structure
2. Commands         → Automate development tasks  
3. Prompts          → Standardize AI interactions
4. Output           → Track generated results
```

## 🔧 Template Features

### 🎯 Auto-Organization
- **Executable Commands**: `commands/` klasörü
- **Project Context**: `context/` dosyaları
- **Generated Output**: `output/` tracking
- **AI Templates**: `prompts/` standardization

### 📊 Documentation Integration
- **Cross-References**: Links to main documentation
- **Consistent Structure**: Follows project standards
- **Version Control**: Template versioning
- **AI Compatibility**: Cursor AI optimized

## 🚀 Usage Patterns

### Development Workflow
```bash
# Execute commands
cd context-engineering/commands
./test-runner.sh

# Update context
cd context-engineering/context
# Edit context files as needed

# Use prompts
cd context-engineering/prompts
# Reference AI templates
```

### Template Benefits
- ✅ **Consistent Structure**: Standardized organization
- ✅ **AI-Friendly**: Optimized for AI assistants  
- ✅ **Scalable**: Grows with project needs
- ✅ **Modern**: Current best practices

---

**📚 Complete Project Structure**: [`../../docs/README.md`](../../docs/README.md) 