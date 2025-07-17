# 📤 Export Guide - Collective Memory

**Version:** v2.1  
**Date:** 14 July 2025  
**Category:** User Guides  

---

## 🎯 General Overview

Export guide for search results and data in various formats in the Collective Memory system.

## 📋 Supported Formats

### 1. **Markdown (.md)**
- Readable format
- GitHub compatible
- Links and images
- Code block support

### 2. **Plain Text (.txt)**
- Simple text format
- Universal compatibility
- Small file size
- Fast loading

### 3. **JSON (.json)**
- Programmatic access
- Structured data
- API integration
- Automatic processing

### 4. **CSV (.csv)**
- Spreadsheet compatibility
- Table format
- Excel/Sheets openable
- Data analysis

## 🔧 Export Commands

### Basic Export
```bash
# Markdown format
python src/main.py --search "Django" --save-to "django-docs.md" --data-path "C:\projects"

# Text format
python src/main.py --search "Python" --save-to "python-docs.txt" --data-path "C:\projects"

# JSON format
python src/main.py --search "API" --save-to "api-docs.json" --data-path "C:\projects"
```

### Advanced Export
```bash
# With filtering
python src/main.py --search "error" --type=py --save-to "python-errors.md" --data-path "C:\projects"

# With date range
python src/main.py --search "bug fix" --date-range="2025-01-01,2025-12-31" --save-to "bugs-2025.md" --data-path "C:\projects"

# With semantic search
python src/main.py --search "machine learning" --semantic --save-to "ml-docs.md" --data-path "C:\projects"
```

## 📊 Export Options

### File Structure
```
[Project Folder]/.collective-memory/
├── exports/
│   ├── search-results/
│   │   ├── django-docs.md
│   │   ├── python-docs.txt
│   │   └── api-docs.json
│   ├── reports/
│   │   ├── daily-report.md
│   │   └── weekly-report.csv
│   └── backups/
│       └── full-backup.json
```

### Automatic Naming
```bash
# Timestamped files
--save-to "search-results-{date}.md"
# Output: search-results-2025-07-14.md

# Query-based naming
--save-to "{query}-results.md"
# Output: Django-results.md
```

## 🚀 Advanced Features

### 1. **Batch Export**
```bash
# Multiple search results
python src/main.py --batch-export searches.txt --data-path "C:\projects"

# searches.txt content:
# Django models
# Python functions
# API endpoints
```

### 2. **Scheduled Export**
```bash
# Daily export
python src/main.py --schedule-export daily --format=md --data-path "C:\projects"

# Weekly export
python src/main.py --schedule-export weekly --format=csv --data-path "C:\projects"
```

### 3. **Template Based Export**
```bash
# Use custom template
python src/main.py --search "API" --template="api-report.template" --save-to "api-report.md" --data-path "C:\projects"
```

## 📝 Export Templates

### Markdown Template
```markdown
# {{title}}

**Search Query:** {{query}}  
**Date:** {{date}}  
**Result Count:** {{result_count}}

## Results

{{#results}}
### {{filename}}
- **Path:** {{path}}
- **Size:** {{size}}
- **Modification:** {{modified}}
- **Score:** {{score}}

{{snippet}}

---
{{/results}}
```

### JSON Template
```json
{
  "search_query": "{{query}}",
  "date": "{{date}}",
  "result_count": {{result_count}},
  "results": [
    {{#results}}
    {
      "filename": "{{filename}}",
      "path": "{{path}}",
      "size": "{{size}}",
      "modified": "{{modified}}",
      "score": {{score}},
      "snippet": "{{snippet}}"
    }{{#unless @last}},{{/unless}}
    {{/results}}
  ]
}
```

## 🔍 Console Integration

### Console Export
```bash
comprehensive> doc-export DOC_ID --format=md --output="exported-doc.md"
comprehensive> search-export "Django models" --format=json --output="django-models.json"
comprehensive> batch-export --query-file="searches.txt" --format=csv
```

### Automatic Export
```bash
# Automatic system report
comprehensive> auto-export --type=system-report --schedule=daily

# Automatic error report
comprehensive> auto-export --type=error-report --schedule=weekly
```

## 📈 Export Metrics

### File Size
- **Markdown:** Medium size, readable
- **JSON:** Small size, structured
- **CSV:** Very small, table format
- **TXT:** Smallest, simple text

### Performance
- **Fast:** TXT, CSV
- **Medium:** Markdown
- **Slow:** JSON (large data sets)

### Compatibility
- **Universal:** TXT
- **Developer:** JSON
- **Documentation:** Markdown
- **Analysis:** CSV

## 🛠️ Troubleshooting

### Common Issues

1. **File Not Created**
   ```bash
   # Solution: Check write permissions
   ls -la .collective-memory/exports/
   chmod 755 .collective-memory/exports/
   ```

2. **Large File Size**
   ```bash
   # Solution: Use filtering
   --limit=50 --type=md --date-range="2025-07-01,2025-07-31"
   ```

3. **Corrupted Format**
   ```bash
   # Solution: Check template
   --template="default.template" --validate
   ```

## 🎯 Usage Examples

### Project Documentation
```bash
# API documentation
python src/main.py --search "API endpoint" --save-to "api-docs.md" --data-path "C:\projects"

# Error documentation
python src/main.py --search "error solution" --save-to "error-fixes.md" --data-path "C:\projects"
```

### Report Generation
```bash
# Daily report
python src/main.py --daily-report --save-to "daily-report-{date}.md" --data-path "C:\projects"

# Weekly summary
python src/main.py --weekly-summary --save-to "weekly-summary.csv" --data-path "C:\projects"
```

### Backup
```bash
# Full backup
python src/main.py --full-backup --save-to "backup-{date}.json" --data-path "C:\projects"

# Selected backup
python src/main.py --backup-search "important" --save-to "important-backup.json" --data-path "C:\projects"
```

---

**📝 This guide covers all export features. It is updated when new formats are added.** 