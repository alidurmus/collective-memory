---
description: Collective Memory genel proje kuralları ve standartları
globs: []
alwaysApply: true
---

# 📋 Genel Proje Kuralları

Bu kurallar tüm Collective Memory projesinde geçerlidir.

## 🎯 Proje Kimliği

- **Turkish UI + English Code** standardı [[memory:2176195]]
- **Context7 Framework** kullanımı [[memory:592593]]
- **Playwright Testing** implementasyonu [[memory:592592]]
- **Memory-aware development** - Her işlem öncesi hafızayı kontrol et [[memory:3235989]]

## 📁 Dosya Adlandırma

### Python Dosyaları
```python
# ✅ Correct
database_manager.py
enhanced_query_engine.py
terminal_interface.py

# ❌ Incorrect
databaseManager.py
enhancedQueryEngine.py
TerminalInterface.py
```

### React Dosyaları  
```jsx
// ✅ Correct
Dashboard.jsx
SearchInterface.jsx
SystemStatus.jsx

// ❌ Incorrect
dashboard.jsx
searchInterface.jsx
system_status.jsx
```

## 🔧 Import Organizasyonu

### Python Imports
```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party
import django
from rest_framework import serializers

# 3. Local
from .models import User
from ..utils import helpers
```

### React Imports
```jsx
// 1. React/libs
import React, { useState, useEffect } from 'react';
import axios from 'axios';

// 2. Components
import Dashboard from './Dashboard';
import SearchPanel from './SearchPanel';

// 3. Styles
import './styles.css';
```

## 📊 Kod Kalitesi

- **Line length**: 88 karakter (Python), 100 karakter (JavaScript)
- **Naming**: snake_case (Python), camelCase (JavaScript)
- **Comments**: Türkçe açıklama, İngilizce technical terms
- **Documentation**: Docstrings zorunlu (Python), JSDoc önerilir (React)

## 🚀 Performance Standards

- **API Response**: <500ms
- **Search Response**: <100ms
- **Bundle Size**: <2MB
- **Memory Usage**: <512MB
- **Test Coverage**: >80%

@examples/code-standards.py
@examples/react-patterns.jsx 