# 🤖 AI Templates

**Context Engineering Template - AI Assistant Templates**

Bu dosya, Cursor AI ve diğer AI araçlarıyla tutarlı geliştirme için şablon prompt'ları içerir.

## 🎯 Project Context Template

```markdown
# Collective Memory Project Context

**Project**: Collective Memory System v2.1.0
**Architecture**: Context Engineering Template  
**Framework**: Django + React + Context7
**Testing**: pytest (backend) + Playwright (UI) [[memory:592592]]
**Language**: Turkish (UI) + English (Code) [[memory:2176195]]
**Tools**: Context7 library tools [[memory:592593]]

## Current Task
[DESCRIBE_CURRENT_TASK]

## Requirements  
- Follow Context Engineering Template structure
- Maintain test coverage >80%
- Use Turkish for user-facing elements
- Apply Context7 design standards
- Test before commit

## Context
[ADDITIONAL_CONTEXT]
```

## 🔧 Code Generation Templates

### React Component Template
```jsx
// Context7 React Component Template
import React, { useState, useEffect } from 'react';
import './[ComponentName].css';

/**
 * [ComponentName] - [Brief Description]
 * Context7 Framework compatible component
 * 
 * @param {Object} props - Component props
 * @returns {JSX.Element} Rendered component
 */
const [ComponentName] = (props) => {
  const [state, setState] = useState(null);

  useEffect(() => {
    // Component initialization
  }, []);

  return (
    <div className="context7-[component-name]">
      {/* Turkish UI Text */}
      <h2>Başlık</h2>
      
      {/* Component content */}
      
    </div>
  );
};

export default [ComponentName];
```

### Django Model Template  
```python
# Context7 Django Model Template
import uuid
from django.db import models
from django.contrib.auth.models import User

class [ModelName](models.Model):
    """
    [ModelName] - [Brief Description]
    Context7 ERP System compatible model
    """
    
    # Context7 Standard Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    # Model-specific fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = '[table_name]'
        verbose_name = '[Verbose Name]'
        verbose_name_plural = '[Verbose Name Plural]'
        
    def __str__(self):
        return self.name
```

### Test Template
```python
# Context7 Test Template
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from [app_name].models import [ModelName]

class [ModelName]TestCase(TestCase):
    """
    [ModelName] test suite
    Coverage target: >80%
    """
    
    def setUp(self):
        """Test setup"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_[model_name]_creation(self):
        """Test model creation"""
        instance = [ModelName].objects.create(
            name='Test [ModelName]',
            created_by=self.user
        )
        
        self.assertEqual(instance.name, 'Test [ModelName]')
        self.assertEqual(instance.created_by, self.user)
        self.assertTrue(instance.is_active)
        self.assertFalse(instance.is_deleted)
        
    def test_[model_name]_str_method(self):
        """Test string representation"""
        instance = [ModelName].objects.create(
            name='Test Name',
            created_by=self.user
        )
        
        self.assertEqual(str(instance), 'Test Name')
```

## 🎨 UI/UX Templates

### CSS Context7 Template
```css
/* Context7 CSS Template */
.context7-[component-name] {
  /* Glassmorphism Base */
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  /* Layout */
  padding: 1.5rem;
  margin: 1rem 0;
  
  /* Animation */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.context7-[component-name]:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  .context7-[component-name] {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .context7-[component-name] {
    padding: 1rem;
    margin: 0.5rem 0;
  }
}
```

## 📋 Documentation Templates

### Feature Documentation Template
```markdown
# [Feature Name]

**Version**: 2.1.0
**Context**: Context Engineering Template  
**Status**: [Development/Testing/Complete]

## Genel Bakış
[Turkish description for users]

## Technical Overview  
[English technical description]

## Implementation
- **Frontend**: React + Context7
- **Backend**: Django
- **Database**: [Model relationships]
- **Tests**: pytest + Playwright [[memory:592592]]

## Usage
[Code examples and usage instructions]

## Testing
[Test scenarios and coverage information]

## Related
- Context: [Related context files]
- Commands: [Related command scripts]  
- Output: [Generated output files]
```

## 🚨 Quick Actions

### Commit Message Template
```
feat: [feature description in English]

- Turkish UI elements added [[memory:2176195]]
- Context7 framework integration [[memory:592593]]
- Playwright tests included [[memory:592592]]
- Follows Context Engineering Template structure

Closes: #[issue_number]
```

### Pull Request Template
```markdown
## 🎯 Context Engineering Template PR

**Feature**: [Feature name]
**Type**: [Feature/Bugfix/Enhancement/Documentation]

### ✅ Checklist
- [ ] Tests pass (pytest + Playwright)
- [ ] Turkish UI / English code separation maintained
- [ ] Context7 standards followed
- [ ] Context Engineering Template structure preserved
- [ ] Documentation updated

### 📋 Changes
[List of changes]

### 🧪 Testing
[Testing approach and coverage]

### 📸 Screenshots
[UI changes if applicable]
```

---

**🔧 Usage**: Bu template'lari `[PLACEHOLDER]` değerlerini değiştirerek kullanın.  
**📚 Context**: Her template Context Engineering Template prensiplerine uygun tasarlanmıştır.  
**🔄 Update**: Yeni pattern'ler keşfedildikçe template'ları güncelleyin. 