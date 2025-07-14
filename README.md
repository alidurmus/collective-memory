# 🧠 Collective Memory + Context7 ERP System

**Enterprise-grade AI-powered Context Management & ERP Solution**  
**🏗️ Context Engineering Template Implementation**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![Context Engineering](https://img.shields.io/badge/Architecture-Context_Engineering_Template-orange.svg)](https://github.com/Therayz1/Context-Engineering-Template)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg)](docs)

## 🎯 Project Overview

This repository contains a powerful AI-powered context management system organized with the **Context Engineering Template** architecture:

### 🔍 **Collective Memory System**
An intelligent context orchestrator that solves Cursor AI's memory loss problem through real-time file monitoring, database indexing, and intelligent context collection.

**Main Program Location:** `collective-memory-app/` directory

### 🏗️ **Context Engineering Template Structure**
**NEW:** Organized development structure following modern engineering practices:

```
collective-memory/
├── context-engineering/     # 🏗️ Context Engineering Template
│   ├── commands/           # 🔧 Scripts and executables
│   ├── context/           # 🧠 Project context and config
│   ├── output/            # 📤 Generated results
│   └── prompts/           # 💬 AI templates
├── collective-memory-app/  # 🚀 Main application
├── data/                  # 🧪 Demo/example data
└── docs/                  # 📚 Documentation
```

### 📋 **Demo/Example Data**
The `/data` folder contains **sample documentation and test files only** - not the main system.

**Note:** Use your own document folders for real work, `/data` is for demonstration purposes.

---

## 🚨 **IMPORTANT: About `/data` Folder**

> **⚠️ WARNING:** The `/data` folder is **for examples and testing only!**
> 
> - ❌ **Not the main program** - The real system is in `collective-memory-app/`
> - ✅ **Demo content only** - Sample files for testing and learning
> - ✅ **For real use** - Specify your own folder: `--data-path /path/to/your/documents`
> 
> **📋 More details:** [Data Folder Usage Guide](docs/DATA_USAGE_NOTE.md)

## 🏗️ Context Engineering Template Features

### 🔧 **Commands Directory**
Executable scripts and operational tools:
- `test-runner.sh` - Comprehensive test suite
- `setup.py` - Environment setup and configuration

### 🧠 **Context Directory**  
Project context and configuration management:
- `project-rules.md` - Development rules and standards
- `config.json` - Project configuration

### 📤 **Output Directory**
Generated outputs and results:
- Test results and reports
- Build artifacts
- Performance metrics

### 💬 **Prompts Directory**
AI prompts and templates:
- `development-prompts.md` - AI development assistance
- `ai-templates.md` - Code generation templates

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ [[memory:2176195]]
- Docker (optional)
- Git

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/alidurmus/collective-memory.git
cd collective-memory

# Setup using Context Engineering Template
cd context-engineering
python commands/setup.py

# Or setup manually
cd collective-memory-app

# Install dependencies
pip install -r requirements.txt

# Setup frontend
cd frontend
npm install
npm run dev
```

### 🧪 Running Tests

```bash
# Using Context Engineering Template
cd context-engineering
./commands/test-runner.sh

# Or manually
cd collective-memory-app
python -m pytest tests/test_basic.py -v
npx playwright test tests/ui/ --headed
```

### 🌐 Access Application

- **Frontend Dashboard**: http://localhost:3003/
- **Backend API**: http://localhost:8000/
- **Test Results**: `context-engineering/output/`

## 🎯 Context Engineering Benefits

✅ **Better Organization**: Logical folder structure  
✅ **Easy Navigation**: Everything in its place  
✅ **Scalable Structure**: Suitable for growing projects  
✅ **Modern Approach**: Context Engineering best practices  
✅ **AI-Friendly**: Optimized for AI-assisted development  

## 📚 Documentation Structure

- **📁 context-engineering/**: [Template implementation](context-engineering/README.md)
- **📚 docs/**: [Comprehensive documentation](docs/README.md)
- **🔧 collective-memory-app/**: [Main application docs](collective-memory-app/README.md)
- **🧪 data/**: [Demo data usage](docs/DATA_USAGE_NOTE.md)

## 🧠 AI Memory Integration

This project uses intelligent memory management:
- **Turkish UI** [[memory:2176195]] for user-facing elements
- **Context7 tools** [[memory:592593]] for library documentation
- **Playwright testing** [[memory:592592]] for UI automation

## 🎨 Technology Stack

- **Backend**: Python 3.9+, Django 4.2+
- **Frontend**: React, Context7 Framework
- **Database**: SQLite (development), PostgreSQL (production)  
- **Testing**: pytest (backend), Playwright (UI)
- **Architecture**: Context Engineering Template
- **AI Tools**: Cursor AI, Context7 library tools

## 🔧 Development

### Context Engineering Workflow

1. **Setup**: Use `context-engineering/commands/setup.py`
2. **Development**: Follow `context-engineering/context/project-rules.md`
3. **Testing**: Run `context-engineering/commands/test-runner.sh`
4. **Templates**: Use `context-engineering/prompts/` for AI assistance

### Traditional Workflow  

1. Navigate to `collective-memory-app/`
2. Run development commands directly
3. Check `docs/` for documentation

## 🤝 Contributing

1. Follow Context Engineering Template structure
2. Maintain Turkish UI / English code separation [[memory:2176195]]
3. Use Context7 tools [[memory:592593]] for library docs
4. Include Playwright tests [[memory:592592]] for UI features
5. Test before commit using provided scripts

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Context Engineering Template**: https://github.com/Therayz1/Context-Engineering-Template
- **Repository**: https://github.com/alidurmus/collective-memory.git
- **Documentation**: [docs/](docs/)
- **Live Demo**: [Coming Soon]

---

**🏆 Powered by Context Engineering Template - Modern AI-Assisted Development** 