# 🚀 Collective Memory - Quick Start Guide

**Run the system in 5 minutes!** ⚡  
**Version:** 2.1 - Directory Management & Search Export  

---

## 🆕 **New Features (v2.1)**

✅ **Automatic `.collective-memory/` directory** - Organize data management  
✅ **Save search results** - Export with `--save-to`  
✅ **Advanced configuration** - JSON configuration files  
✅ **Cross-platform compatibility** - Windows, macOS, Linux  

---

## 🔥 **Quick Start**

```bash
# 1. Navigate to the correct directory (IMPORTANT!)
cd collective-memory-app

# 2. Index your project
python src/main.py --index --data-path "C:\path\to\your\project"
# ✅ Automatically creates .collective-memory/ directory

# 3. Perform a search
python src/main.py --search "Django settings" --data-path "C:\path\to\your\project"

# 4. Save results (NEW!)
python src/main.py --search "error resolution" --save-to "errors.md" --data-path "C:\path\to\your\project"
```

---

## 🚨 **Common Errors and Solutions**

### ❌ **Problem:**
```bash
PS C:\cursor\collective-memory> python src/main.py --interactive --data-path ../data
# Error: can't open file 'src/main.py': No such file or directory
```

### ✅ **Solution:**
```bash
PS C:\cursor\collective-memory> cd collective-memory-app
PS C:\cursor\collective-memory\collective-memory-app> python src/main.py --interactive --data-path "C:\your\project"
# ✅ Success! System will create .collective-memory/ directory
```

### 🔍 **Why is this happening?**
`main.py` file is in `collective-memory-app/src/`, not in the main directory!

---

## ⚡ **4-Step Installation**

### **Step 1: Navigate to the Directory**
```bash
cd collective-memory/collective-memory-app
```

### **Step 2: Index Your Project**
```bash
# For your project
python src/main.py --index --data-path "C:\Users\YourName\MyProject"

# ✅ Automatically created:
# C:\Users\YourName\MyProject\.collective-memory\
#   ├── database/collective_memory.db
#   ├── config/settings.json
#   └── [other system files]
```

### **Step 3: Perform a Search**
```bash
# Simple search
python src/main.py --search "keyword" --data-path "C:\Users\YourName\MyProject"

# Save results to a file (NEW!)
python src/main.py --search "Django error" --save-to "django-errors.md" --data-path "C:\Users\YourName\MyProject"
```

### **Step 4: Use Interactive Mode**
```bash
# Start interactive mode
python src/main.py --interactive --data-path "C:\Users\YourName\MyProject"

# Commands:
> help         # Help
> stats        # Statistics
> search term  # Search
> quit         # Exit
```

---

## 📁 **Automatically Generated Structure** ⭐ **NEW**

The system automatically creates this structure when it first runs:

```
[Your Project Directory]/
├── [Your existing files...]
└── .collective-memory/
    ├── database/
    │   └── collective_memory.db     # Search database
    ├── config/
    │   ├── settings.json            # System settings
    │   └── project_status.json      # Status information
    ├── cache/                       # Search cache
    ├── logs/                        # System logs
    ├── [search-results].md          # Saved searches
    └── README.md                    # System description
```

---

## 🔍 **Search Examples**

### **Basic Search**
```bash
python src/main.py --search "React component" --data-path "C:\MyProject"
```

### **Search + Save to File** ⭐ **NEW**
```bash
python src/main.py --search "authentication system" --save-to "auth-docs.md" --data-path "C:\MyProject"
# ✅ Result: C:\MyProject\.collective-memory\auth-docs.md
```

### **View Statistics**
```bash
python src/main.py --stats --data-path "C:\MyProject"
# ✅ Output: File count, size, last changes
```

### **Interactive Mode Usage**
```bash
python src/main.py --interactive --data-path "C:\MyProject"

# Interactive commands:
> search Django settings
> search error handling  
> stats
> help
> quit
```

---

## 💻 **First Use Commands**

After the system opens, in the terminal:

```bash
help                    # Show all commands
search "documentation"  # Search documentation
search "API"           # Search API information
search "error"         # Search error reports
files                  # List all files
stats                  # System status
exit                   # Exit
```

---

## 🐛 **Quick Troubleshooting**

### **Problem: Module not found**
```bash
pip install watchdog colorama pathlib
```

### **Problem: Permission error**
```bash
# Linux/Mac:
chmod +x src/main.py

# Windows: Run PowerShell as administrator
```

### **Problem: Python version**
```bash
python --version  # Should be 3.9+
```

---

## 🎯 **Most Useful Features**

### **1. Cursor Chat History**
```bash
cursor_history          # Recent chats
cursor_history --limit=20  # Last 20 chats
```

### **2. Advanced Search**
```bash
search "react component" --limit=10    # Limited results
search "API" --type=markdown          # Only .md files
```

### **3. File Monitoring**
```bash
files --recent          # Recently changed files
files --count          # Total file count
```

---

## 🔧 **System Control**

If you encounter any issues:

```bash
# System status
python src/main.py --stats --data-path ../data

# Help menu
python src/main.py --help

# Version check
python src/main.py --version
```

---

## 📚 **More Information**

- **Detailed Guide:** [`USAGE_GUIDE.md`](USAGE_GUIDE.md)
- **Main Documentation:** [`../README.md`](../README.md)
- **System Guide:** [`../collective-memory.md`](../collective-memory.md)

---

## 🎉 **Successful Installation Test**

If the system is working correctly, you should see this output:

```
╔═══════════════════════════════════════════════════╗
║          Collective Memory v1.0                  ║
║        AI Agent Smart Context Orchestrator      ║
║      + File Monitoring + Search + Indexing      ║
╚═══════════════════════════════════════════════════╝

🔍 Query System Mode - Enhanced Features Active

[2025-01-14 12:00:00] INFO: Database initialized successfully
[2025-01-14 12:00:00] INFO: File monitoring started
[2025-01-14 12:00:00] SUCCESS: System ready!

Collective Memory Terminal (type 'help' for commands)
> 
```

**Congratulations! System ready! 🎉**

---

**⚡ This guide is designed to run the system in 5 minutes. For more details, refer to other documents.** 