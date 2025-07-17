# 📚 Collective Memory - Detailed Usage Guide

**Last Updated:** 14 Temmuz 2025  
**Version:** v2.1 Enhanced with Directory Management  
**Status:** Production Ready  

---

## 🚨 **IMPORTANT: Data Directory**

> **WARNING:** `/data` directory is only for **example and testing purposes!**
> 
> - ❌ **Not the main program** - The actual system is in the `collective-memory-app/` directory
> - ✅ **Demo content** - Only for testing and learning
> - ✅ **Real usage** - Specify your own folder: `--data-path /path/to/your/docs`
> 
> **Detailed information:** [Data Directory Description](DATA_USAGE_NOTE.md)

---

## 🆕 **NEW FEATURES (v2.1)**

✅ **Automatic Directory Organization** - `.collective-memory/` directory is automatically created  
✅ **Export Search Results** - Save results with `--save-to dosya.md`  
✅ **Advanced Database Management** - Better organization and caching  
✅ **Platform Independence** - Windows, macOS, Linux support  

### 📁 **Automatic Directory Structure**

When the system is first run, it creates this structure in your project:

```
[Your Project Directory]/
├── [Your existing files...]
└── .collective-memory/
    ├── database/
    │   └── collective_memory.db    # SQLite database
    ├── cache/                      # Search cache
    ├── logs/                       # System logs
    ├── config/                     # Configuration files
    │   ├── settings.json          # System settings
    │   └── project_status.json    # Project status
    └── README.md                   # System documentation
```

---

## 🚨 **Quick Troubleshooting**

### **Common Error: "can't open file"**

❌ **WRONG:**
```bash
PS C:\cursor\collective-memory> python src/main.py --interactive --data-path ../data
```

✅ **CORRECT:**
```bash
PS C:\cursor\collective-memory> cd collective-memory-app
PS C:\cursor\collective-memory\collective-memory-app> python src/main.py --interactive --data-path ../data
```

### **Basic Troubleshooting Checklist**

1. **Directory Location Check:**
   ```bash
   pwd                           # Shows the current directory
   ls -la                        # Lists files (Linux/Mac)
   dir                          # Lists files (Windows)
   ```

2. **Required File Check:**
   ```bash
   ls collective-memory-app/src/main.py    # Does the file exist?
   python --version                        # Python version (requires 3.9+)
   ```

3. **Directory Structure Check:**
   ```bash
   # Has Collective memory directory been created?
   ls -la [project-directory]/.collective-memory/
   
   # Does the database file exist?
   ls -la [project-directory]/.collective-memory/database/collective_memory.db
   ```

---

## 🔧 **INSTALLATION AND FIRST USE**

### **1. Basic Installation**
```bash
# Clone the project
git clone https://github.com/your-username/collective-memory.git
cd collective-memory

# Go to the main application
cd collective-memory-app

# Install dependencies
pip install -r requirements.txt
```

### **2. Initial Indexing**
```bash
# Index your own project folder
python src/main.py --index --data-path "C:\path\to\your\project"

# The system will automatically create the .collective-memory/ directory
```

### **3. Search and Query Usage**

#### **A. Basic Search**
```bash
# Simple text search
python src/main.py --search "Django settings" --data-path "C:\your\project"

# Displays results on screen
```

#### **B. Saving Search Results to File** ⭐ **NEW**
```bash
# Search and save results to a file
python src/main.py --search "error resolution" --save-to "error-solutions.md" --data-path "C:\your\project"

# Saved in .collective-memory/ directory
```

#### **C. Interactive Mode**
```bash
# Start interactive mode
python src/main.py --interactive --data-path "C:\your\project"

# Commands:
# help         - Show help
# stats        - Show statistics  
# search term  - Perform search
# quit         - Exit
```

#### **D. System Statistics**
```bash
# Show project statistics
python src/main.py --stats --data-path "C:\your\project"
```

---

## 📖 **USAGE EXAMPLES**

### **Example 1: Django Project Error Investigation**
```bash
# Search for Django errors and save
python src/main.py --search "NoReverseMatch error" --save-to "django-errors.md" --data-path "C:\projects\django-app"

# Output: .collective-memory/django-errors.md file
```

### **Example 2: API Documentation Search**
```bash
# Search for API endpoints
python src/main.py --search "API endpoint configuration" --data-path "C:\projects\api-docs"

# Interactive mode for detailed investigation
python src/main.py --interactive --data-path "C:\projects\api-docs"
```

### **Example 3: General Project Investigation**
```bash
# First, check project statistics
python src/main.py --stats --data-path "C:\projects\my-project"

# Perform general search
python src/main.py --search "authentication system" --save-to "auth-research.md" --data-path "C:\projects\my-project"
```

---

## 💻 **Basic Usage Commands**

### **1. Interactive Terminal Mode (Main Feature)**

```bash
cd collective-memory-app
# Use your own folder:
python src/main.py --interactive --data-path /path/to/your/documents
# OR for demo data:
python src/main.py --interactive --data-path ../data

# Commands available after terminal opens:
search keyword                    # Keyword search
search "multiple words"          # Multi-word search
search keyword --limit=20        # Limit results
search keyword --type=markdown   # File type filter
files                           # List all files
files --recent                  # Recently changed files
stats                          # System statistics
cursor_history                 # Cursor chat history
cursor_history --limit=20      # Last 20 chats
cursor_history --workspaces    # All workspaces
help                           # All commands
exit                           # Exit
```

### **2. One-time Queries**

```bash
# Direct search:
python src/main.py --search "react component" --data-path ../data

# Get file list:
python src/main.py --list-files --data-path ../data

# Check system status:
python src/main.py --status --data-path ../data
```

### **3. Cursor Chat History Access**

```bash
# Show cursor chat history:
python src/main.py --cursor-history --data-path ../data

# Show last 10 chats:
python src/main.py --cursor-history --limit=10 --data-path ../data

# List workspaces:
python src/main.py --cursor-workspaces --data-path ../data
```

---

## 🔧 **Advanced Usage Scenarios**

### **Scenario 1: Project Documentation Search**

```bash
# In terminal mode:
search "API documentation"           # API documentation
search "deployment guide"           # Deployment guides
search "database schema"            # Database schemas
search "test coverage" --type=md    # Test coverage information
```

### **Scenario 2: Error Resolution and Troubleshooting**

```bash
# Search for error patterns:
search "error" --limit=50           # All error reports
search "fix" --type=markdown        # Solution documents
search "resolution"                 # Problem resolutions
```

### **Scenario 3: Code References and Examples**

```bash
# Search for code examples:
search "javascript"                 # JS code examples
search "python function"           # Python functions
search "django model"              # Django model examples
```

### **Scenario 4: Cursor Context Collection**

```bash
# Collect context from Cursor and copy to clipboard:
# In code comments:
# @collect-memory: Implement React modal component

# Manual trigger:
python src/main.py --collect-context --request "React modal component" --data-path ../data
```

---

## 📊 **System Monitoring and Statistics**

### **Real-time System Status**

```bash
# In interactive mode:
stats                              # General system statistics
files --recent                     # Recently changed files
files --count                      # Total file count
```

### **Performance Metrics**

```bash
# System performance test:
python src/main.py --performance-test --data-path ../data

# Database status:
python src/main.py --db-status --data-path ../data

# Indexing status:
python src/main.py --index-status --data-path ../data
```

---

## 🛠️ **Configuration and Customization**

### **Config File (config/settings.json)**

```json
{
    "data_path": "../data",
    "database_path": "collective_memory.db",
    "log_level": "INFO",
    "max_search_results": 50,
    "file_types": [".md", ".txt", ".py", ".js"],
    "ignore_patterns": ["*.log", "*.tmp", ".git/*"],
    "cursor_integration": true,
    "auto_monitoring": true
}
```

### **Environment Variables**

```bash
# Windows:
set COLLECTIVE_MEMORY_DATA_PATH=C:\path\to\data
set COLLECTIVE_MEMORY_LOG_LEVEL=DEBUG

# Linux/Mac:
export COLLECTIVE_MEMORY_DATA_PATH=/path/to/data
export COLLECTIVE_MEMORY_LOG_LEVEL=DEBUG
```

---

## 🔍 **Search Tips and Best Practices**

### **Effective Search Techniques**

1. **Keyword Selection:**
   ```bash
   search "implementation"          # Broad search
   search "react implementation"    # Specific search
   search "react modal component"   # Very specific search
   ```

2. **Filter Usage:**
   ```bash
   search keyword --type=markdown   # Search only in .md files
   search keyword --limit=10        # Show first 10 results
   search keyword --recent          # Search in recently changed files
   ```

3. **Boolean Searches:**
   ```bash
   search "django AND model"        # Contains both words
   search "react OR vue"           # Contains either word
   search "NOT deprecated"         # Does not contain
   ```

### **Common Search Commands**

```bash
# Documentation search:
search "documentation" --type=md
search "README" --type=md
search "guide" --limit=20

# Code examples:
search "example" --type=py
search "sample" --type=js
search "template" --type=html

# Error resolution:
search "error" --recent
search "fix" --limit=30
search "solution" --type=md

# APIs and endpoints:
search "API" --type=md
search "endpoint" --type=py
search "route" --type=js
```

---

## 🐛 **Troubleshooting and Error Resolution**

### **Common Errors and Solutions**

#### **1. "FileNotFoundError: No such file or directory"**

**Problem:** main.py file not found  
**Solution:**
```bash
# Go to the correct directory:
cd collective-memory-app
ls src/main.py                     # Check if file exists
```

#### **2. "ModuleNotFoundError: No module named 'watchdog'"**

**Problem:** Dependencies not installed  
**Solution:**
```bash
pip install -r requirements.txt
# or
pip install watchdog colorama pathlib
```

#### **3. "Permission denied" or "Access denied"**

**Problem:** File permissions  
**Solution:**
```bash
# Linux/Mac:
chmod +x setup.sh
chmod 755 src/main.py

# Windows: Run PowerShell as Administrator
```

#### **4. "Database locked" error**

**Problem:** SQLite database locked  
**Solution:**
```bash
# Delete and recreate the database file:
rm collective_memory.db
python src/main.py --rebuild-db --data-path ../data
```

#### **5. Cursor chat history access error**

**Problem:** Cursor database access issue  
**Solution:**
```bash
# Ensure Cursor is open
# Run with administrator privileges
python src/main.py --test-cursor --data-path ../data
```

### **Debug Mode**

```bash
# For detailed log output:
python src/main.py --debug --interactive --data-path ../data

# Create log file:
python src/main.py --interactive --data-path ../data --log-file debug.log
```

---

## 📈 **Performance Optimization**

### **Improving System Performance**

1. **Database Optimization:**
   ```bash
   python src/main.py --optimize-db --data-path ../data
   ```

2. **Index Rebuilding:**
   ```bash
   python src/main.py --rebuild-index --data-path ../data
   ```

3. **Cache Clearing:**
   ```bash
   python src/main.py --clear-cache --data-path ../data
   ```

### **Memory Usage**

```bash
# Light mode (low memory usage):
python src/main.py --memory-efficient --interactive --data-path ../data

# Fast mode (high performance):
python src/main.py --high-performance --interactive --data-path ../data
```

---

## 🔐 **Security and Privacy**

### **Data Security**

- All data is stored locally on your machine
- No data is sent to the internet
- Cursor chat history is read-only, not modifiable
- SQLite encryption option is available

### **Security Settings**

```bash
# Enable database encryption:
python src/main.py --enable-encryption --data-path ../data

# Create backup:
python src/main.py --backup --data-path ../data
```

---

## 📚 **Advanced Features**

### **API Usage**

```python
# Usage from Python code:
from src.collective_memory import CollectiveMemory

cm = CollectiveMemory()
results = cm.search("react component")
print(results)
```

### **Custom Extensions**

```python
# Custom search filters:
def custom_filter(file_path, content):
    return "react" in content.lower()

cm.add_custom_filter("react_filter", custom_filter)
```

### **Batch Operations**

```bash
# Batch operations:
python src/main.py --batch-search queries.txt --data-path ../data
python src/main.py --batch-index folder/ --data-path ../data
```

---

## �� **Support and Help**

### **Help Commands**

```bash
python src/main.py --help              # General help
python src/main.py --version           # Version information
python src/main.py --system-info       # System information
```

### **Log Files**

```bash
# Check log files:
tail -f logs/collective-memory.log     # Real-time logs
cat logs/error.log                     # Error logs
```

### **System Health Check**

```bash
python src/main.py --health-check --data-path ../data
```

---

## 🎯 **Results and Best Practices**

### **Best Usage Practices:**

1. **Regular Interactive Usage:** Prefer the `--interactive` mode
2. **Specific Searches:** Use specific terms instead of general words
3. **Filter Usage:** Activate `--type` and `--limit` parameters
4. **Regular Maintenance:** Run `--optimize-db` weekly

### **Performance Tips:**

- For large projects, use `--memory-efficient` mode
- Create aliases for frequently used searches
- Regularly optimize your database

---

**This guide is continuously updated. Refer to the GitHub repository for the latest version.** 