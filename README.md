# 🧠 Collective Memory + Context7 ERP System

**Enterprise-grade AI-powered Context Management & ERP Solution**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg)](docs)

## 🎯 Project Overview

This repository contains a powerful AI-powered context management system:

### 🔍 **Collective Memory System**
An intelligent context orchestrator that solves Cursor AI's memory loss problem through real-time file monitoring, database indexing, and intelligent context collection.

**Main Program Location:** `collective-memory-app/` directory

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

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ [[memory:2176195]]
- Docker (optional)
- Git

### Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/collective-memory.git
cd collective-memory

# Navigate to the main application
cd collective-memory-app

# Install dependencies
pip install -r requirements.txt

# Setup your project folder and index files
python src/main.py --index --data-path "C:\path\to\your\documents"

# Start interactive search
python src/main.py --interactive --data-path "C:\path\to\your\documents"
```

### 🎯 **New Features (v2.1)**

✅ **Organized Directory Structure** - Automatically creates `.collective-memory/` in your project  
✅ **Search Results Export** - Save results to files with `--save-to filename.md`  
✅ **Enhanced Database Management** - Better organization and caching  
✅ **Cross-Platform Support** - Windows, macOS, Linux compatibility  

### 📁 **Automatic Directory Structure**

When you run the system on your folder, it creates:

```
[Your Project Folder]/
├── [Your existing files...]
└── .collective-memory/
    ├── database/
    │   └── collective_memory.db    # SQLite database
    ├── cache/                      # Search cache
    ├── logs/                       # System logs  
    ├── config/                     # Configuration files
    └── README.md                   # System documentation
```

### 🔍 **Search & Export Examples**

```bash
# Basic search
python src/main.py --search "Django setup" --data-path "C:\your\project"

# Search and save results to file
python src/main.py --search "error resolution" --save-to "errors-found.md" --data-path "C:\your\project"

# Interactive mode with stats
python src/main.py --interactive --data-path "C:\your\project"

# View system statistics  
python src/main.py --stats --data-path "C:\your\project"
```

### Quick Test & Common Issues

⚠️ **En Yaygın Hata:**
```bash
# ❌ YANLIŞ - Ana klasörde çalıştırmayın:
python src/main.py --interactive --data-path ../data
# Hata: can't open file 'src/main.py': No such file or directory
```

✅ **DOĞRU Kullanım:**
```bash
# 1. Önce doğru klasöre gidin:
cd collective-memory-app

# 2. Sonra komutu çalıştırın (kendi data klasörünüzü belirtin):
python src/main.py --interactive --data-path /path/to/your/documents
# VEYA test için example data:
python src/main.py --interactive --data-path ../data

# Note: Django/ERP references in /data are examples only
```

📋 **Hızlı Sorun Giderme:**
```bash
# Bulunduğunuz klasörü kontrol edin:
pwd
ls -la collective-memory-app/src/main.py  # Dosya var mı?

# Bağımlılıkları kontrol edin:
pip list | grep watchdog
```

---

## 🏗️ Project Structure

```
collective-memory/
├── 📂 collective-memory-app/        # Collective Memory System
│   ├── 📂 src/                      # Core Python modules
│   │   ├── main.py                  # Main CLI interface
│   │   ├── file_monitor.py          # Real-time file monitoring
│   │   ├── database_manager.py      # SQLite database operations
│   │   ├── content_indexer.py       # Content parsing & indexing
│   │   ├── query_engine.py          # Advanced search engine
│   │   ├── cursor_reader.py         # Enhanced Cursor database reader
│   │   └── terminal_interface.py    # Interactive CLI
│   ├── 📂 config/                   # Configuration files
│   ├── 📂 tests/                    # Test suite
│   ├── 📂 docs/                     # Documentation
│   ├── requirements.txt             # Python dependencies
│   ├── setup.sh                     # Installation script
│   ├── Dockerfile                   # Docker configuration
│   └── README.md                    # Detailed usage guide
├── 📂 data/                         # 📋 EXAMPLE/DEMO DATA ONLY (not main system)
│   ├── 📂 docs/                     # Sample documentation for testing
│   │   ├── 📂 features/             # Example feature docs
│   │   ├── 📂 deployment/           # Sample deployment guides
│   │   ├── 📂 system/               # Example system docs
│   │   └── 📂 reports/              # Demo status reports
│   ├── .cursor/                     # Example Cursor configurations
│   ├── PRD.md                       # Sample PRD for testing
│   └── todo.md                      # Demo task list
├── 📂 docs/                         # Root documentation
├── collective-memory.md             # System overview
├── techstack.md                     # Technology documentation
├── PRD.md                          # Main PRD
└── DOCUMENTATION_STANDARDS.md      # Documentation guidelines
```

---

## 🔍 Collective Memory System

### Problem Statement
Cursor AI users face constant "amnesia" issues:
- Repeatedly explaining project rules in each conversation
- Manually gathering past context and conversations
- Constantly adding files with @ commands
- Time-consuming searches for relevant project information

### Solution Features

#### 🎯 **Intelligent Context Orchestrator**
Trigger with a simple comment in your code:
```python
# @collect-memory: Implement React modal dialog component
```

This automatically:
- ✅ Collects project rules (.cursor/rules)
- ✅ Gathers past conversation summaries
- ✅ Finds relevant documentation
- ✅ Creates structured queries and copies to clipboard

#### 📊 **File Monitoring & Search System**
- ✅ **Real-time File Monitoring**: Instant detection of file changes
- ✅ **Full-text Search**: Advanced search in Markdown files
- ✅ **Content Indexing**: Automatic content indexing
- ✅ **Interactive Terminal**: Powerful CLI search interface
- ✅ **Enhanced Cursor Integration**: Access to Cursor chat history
- ✅ **Cross-platform Support**: Windows, macOS, Linux

### Usage Examples

```bash
# ✅ DOĞRU: Önce doğru klasöre gidin
cd collective-memory-app

# ✅ Sonra interactive mode'u başlatın (kendi klasörünüzü kullanın):
python src/main.py --interactive --data-path /path/to/your/documents
# VEYA test için:
python src/main.py --interactive --data-path ../data

# Available commands (terminal açıldıktan sonra):
search keyword                    # Search in all files
search keyword --limit=20        # Limit results
search keyword --type=markdown   # Filter by file type
files                           # List all monitored files
files --recent                  # Show recently modified files
stats                          # Show system statistics
cursor_history                 # Show Cursor chat history
cursor_history --limit=20      # Show last 20 chats
cursor_history --workspaces    # Show all workspaces
help                           # Show all commands
exit                           # Exit the application
```

---

## 📋 Example Content & Documentation

The `/data` folder contains extensive **sample documentation** that demonstrates various project management and system documentation patterns. This includes:

### Sample Documentation Categories
- **Feature Specifications** - Example requirements and specs
- **Deployment Guides** - Sample deployment procedures  
- **System Architecture** - Example system design docs
- **Status Reports** - Demo project reporting templates
- **API Documentation** - Sample API reference formats

### What's in `/data` folder:
- ✅ **Educational Examples** - Learn documentation patterns
- ✅ **Template References** - Copy document structures
- ✅ **Testing Content** - Test the search system
- ❌ **Not Production Data** - Use your own folders for real work

### Context7 Framework References
The sample docs include references to Context7 framework patterns and ERP modules as **examples only** - these demonstrate how the system can index and search complex project documentation.

---

## 📚 Documentation

### 🚀 **Quick Start Guides**
- **[Hızlı Başlangıç](docs/QUICK_START.md)** ⚡ - 5 dakikada sistemi çalıştırın
- **[Detaylı Kullanım Rehberi](docs/USAGE_GUIDE.md)** 📖 - Kapsamlı kullanım talimatları
- **[Dokümantasyon İndeksi](docs/README.md)** 📚 - Tüm rehberlere erişim

### 🔧 **Core Documentation**
- [`collective-memory.md`](collective-memory.md) - Complete system guide
- [`techstack.md`](techstack.md) - Technology stack details
- [`PRD.md`](PRD.md) - Product requirements document
- [`DOCUMENTATION_STANDARDS.md`](DOCUMENTATION_STANDARDS.md) - Documentation guidelines

### 📋 **Planning & Management**
- **[Görev Listesi](docs/todo.md)** 📋 - Proje planlaması ve task tracking
- **[Data Klasörü Rehberi](docs/DATA_USAGE_NOTE.md)** 📁 - `/data` klasörünün doğru kullanımı
- [`data/docs/features/`](data/docs/features/) - Example feature specifications
- [`data/docs/reports/`](data/docs/reports/) - Sample status reports

### 🏗️ **Technical Guides**
- [`data/docs/deployment/`](data/docs/deployment/) - Example deployment guides
- [`data/docs/system/`](data/docs/system/) - Sample system architecture
- [`collective-memory-app/docs/`](collective-memory-app/docs/) - Main technical documentation

### 🔌 **API Documentation**
- [`data/docs/api/CONTEXT7_REST_API_DOCUMENTATION.md`](data/docs/api/CONTEXT7_REST_API_DOCUMENTATION.md) - Complete API reference

---

## 🔧 Technology Stack

### Backend
- **Python 3.9+** - Core programming language
- **Django 4.2+** - Web framework (ERP system)
- **SQLite** - Database engine

### Frontend
- **Context7** - Custom CSS/JS framework [[memory:592593]]
- **HTML5/CSS3** - Modern web standards
- **JavaScript ES6+** - Client-side functionality

### Development Tools
- **Cursor AI** - Primary development environment
- **Playwright** - End-to-end testing [[memory:592592]]
- **Docker** - Containerization
- **Git** - Version control

### Key Libraries
```python
watchdog>=3.0.0      # File monitoring
sqlite3              # Database operations
argparse             # CLI interface
pathlib              # Path operations
json                 # Data serialization
datetime             # Time handling
re                   # Pattern matching
hashlib              # File hashing
```

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests
cd collective-memory-app
python -m pytest tests/

# Run specific test
python test_cursor_integration.py

# Test Cursor integration
python src/main.py --test-cursor

# Test file monitoring
python src/main.py --test-monitoring
```

### Test Coverage
- **File Monitoring**: ✅ Real-time change detection
- **Database Operations**: ✅ CRUD operations
- **Search Engine**: ✅ Full-text search
- **Cursor Integration**: ✅ Chat history access
- **Cross-platform**: ✅ Windows/macOS/Linux

---

## 🚀 Deployment

### Local Development
```bash
# Development server
cd collective-memory-app
python src/main.py --interactive --data-path ../data
```

### Docker Deployment
```bash
# Build and run with Docker
cd collective-memory-app
docker-compose up -d
```

### Production Deployment
See detailed guides in [`data/docs/deployment/`](data/docs/deployment/):
- [Hostinger Deployment Guide](data/docs/deployment/HOSTINGER_DEPLOYMENT_GUIDE_FINAL.md)
- [SSL Implementation Guide](data/docs/deployment/SSL_IMPLEMENTATION_GUIDE.md)
- [Production Setup](data/docs/deployment/PRODUCTION_DEPLOYMENT_SUCCESS_REPORT.md)

---

## 🤝 Contributing

### Development Standards
- **Code**: English identifiers, Turkish UI text [[memory:2176195]]
- **Framework**: Use Context7 for UI development [[memory:592593]]
- **Testing**: Use Playwright for page testing [[memory:592592]]
- **Documentation**: Follow [`DOCUMENTATION_STANDARDS.md`](DOCUMENTATION_STANDARDS.md)

### Getting Started
1. Fork the repository
2. Create a feature branch
3. Follow coding standards
4. Add tests for new features
5. Update documentation
6. Submit a pull request

---

## 📞 Support

### Documentation
- **System Guide**: [`collective-memory.md`](collective-memory.md)
- **Technology Stack**: [`techstack.md`](techstack.md)
- **API Reference**: [`data/docs/api/`](data/docs/api/)

### Community
- **Issues**: [GitHub Issues](https://github.com/your-username/collective-memory/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/collective-memory/discussions)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 Roadmap

### Phase 1: Core System (✅ Completed)
- ✅ File monitoring system
- ✅ Database management
- ✅ Content indexing
- ✅ Search engine
- ✅ Terminal interface
- ✅ Cursor integration

### Phase 2: Advanced Features (🔄 In Progress)
- 🔄 Advanced search algorithms
- 🔄 Web dashboard
- 🔄 API development
- 🔄 Performance optimization

### Phase 3: Enterprise Features (📋 Planned)
- 📋 Team collaboration
- 📋 Cloud synchronization
- 📋 Mobile application
- 📋 Advanced analytics

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ by the Collective Memory Team** 