# 🔍 Search Guide - Collective Memory

**Version:** v2.1  
**Date:** 14 July 2025  
**Category:** User Guides  

---

## 🎯 General Overview

This guide is prepared to effectively utilize the powerful search features of the Collective Memory system.

## 📋 Search Types

### 1. **Basic Search**
```bash
python src/main.py --search "Django model" --data-path "C:\projects"
```

### 2. **Semantic Search**
```bash
python src/main.py --search "Python error resolution" --semantic --data-path "C:\projects"
```

### 3. **Saving Results**
```bash
python src/main.py --search "API documentation" --save-to "api-docs.md" --data-path "C:\projects"
```

## 🔧 Search Filters

### File Type Filters
- `.md` - Markdown files
- `.py` - Python files
- `.js` - JavaScript files
- `.txt` - Text files

### Date Filters
- Last 24 hours
- Last week
- Last month
- Custom date range

### Size Filters
- Small files (< 10KB)
- Medium files (10KB - 1MB)
- Large files (> 1MB)

## 🎯 Search Tips

### 1. **Efficient Keywords**
- Use specific terms
- Avoid abbreviations, use full words
- Mixed Turkish and English search

### 2. **Boolean Operators**
- `AND` - Contains both words
- `OR` - Contains any of them
- `NOT` - Does not contain

### 3. **Wildcard Usage**
- `*` - Any character sequence
- `?` - Single character
- `[abc]` - One of the specified characters

## 📊 Search Results

### Relevance Score
- **0.9-1.0:** Perfect match
- **0.7-0.9:** High relevance
- **0.5-0.7:** Medium relevance
- **0.3-0.5:** Low relevance

### Result Format
```
File: path/to/file.md
Score: 0.95
Snippet: "Search result preview..."
Size: 2.3 KB
Last Modified: 2 hours ago
```

## 🚀 Advanced Features

### 1. **Interactive Search**
```bash
python src/main.py --interactive --data-path "C:\projects"
> search "machine learning"
> search "Django settings" --type=py
```

### 2. **Search History**
```bash
> history
> search-history --limit=10
```

### 3. **Saved Searches**
```bash
> save-search "API docs" "API endpoint documentation"
> list-saved-searches
```

## 🔍 Search Strategies

### Code Search
```bash
search "class definition" --type=py
search "function implementation" --type=js
search "import statement" --type=py
```

### Documentation Search
```bash
search "installation guide" --type=md
search "API reference" --type=md
search "troubleshooting" --type=md
```

### Error Search
```bash
search "error" --type=log
search "exception" --type=py
search "bug fix" --type=md
```

## 📈 Performance Tips

### 1. **Fast Search**
- Short keywords
- File type filters
- Size limit

### 2. **Comprehensive Search**
- Long keywords
- Semantic search
- Wide date range

### 3. **Memory Optimization**
- Small project folders
- Frequently used terms
- Cache usage

## 🛠️ Troubleshooting

### Common Issues
1. **No Results Found**
   - Check keywords
   - Expand file type filters
   - Try semantic search

2. **Slow Search**
   - More specific terms
   - File type filters
   - Smaller folders

3. **Incorrect Results**
   - Longer keywords
   - Boolean operators
   - Exact match mode

## 🎯 Examples

### Project Development
```bash
# Django project
search "Django model" --type=py --save-to "django-models.md"

# React component
search "React component" --type=js --save-to "react-components.md"

# API documentation
search "API endpoint" --type=md --save-to "api-endpoints.md"
```

### Error Resolution
```bash
# Python errors
search "Python error" --type=py --save-to "python-errors.md"

# JavaScript errors
search "JavaScript error" --type=js --save-to "js-errors.md"

# System errors
search "system error" --type=log --save-to "system-errors.md"
```

---

**📝 This guide is continuously updated. When new features are added, the documentation will be updated.** 