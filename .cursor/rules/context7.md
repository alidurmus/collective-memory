---
description: Context7 glassmorphism framework kullanım kuralları
globs: ["frontend/**/*.jsx", "frontend/**/*.tsx", "frontend/**/*.css", "frontend/**/*.scss"]
alwaysApply: false
---

# 🎨 Context7 Framework Kuralları

Context7 glassmorphism framework kullanımı için zorunlu kurallar.

## 🌟 Glassmorphism Desing System

### Ana Renk Paleti
```css
:root {
  --context7-primary: #667eea;
  --context7-secondary: #764ba2;
  --context7-accent: #f093fb;
  --context7-glass: rgba(255, 255, 255, 0.1);
  --context7-border: rgba(255, 255, 255, 0.2);
  --context7-shadow: rgba(31, 38, 135, 0.37);
}
```

### Glassmorphism Effects
```css
.context7-card {
  background: var(--context7-glass);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid var(--context7-border);
  box-shadow: 0 8px 32px 0 var(--context7-shadow);
}

.context7-button {
  background: linear-gradient(135deg, var(--context7-primary), var(--context7-secondary));
  backdrop-filter: blur(10px);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.context7-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
}
```

## 🔧 Component Patterns

### Dashboard Component
```jsx
// ✅ Correct Context7 Component
import React from 'react';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="context7-dashboard">
      <div className="context7-card">
        <h2 className="context7-title">Akıllı Dashboard</h2>
        <p className="context7-subtitle">Sistem durumunu görüntüle</p>
      </div>
    </div>
  );
};

export default Dashboard;
```

### Search Interface
```jsx
// ✅ Context7 Search Component
const SearchInterface = ({ onSearch }) => {
  return (
    <div className="context7-search-container">
      <div className="context7-card">
        <input 
          type="text" 
          className="context7-input"
          placeholder="Akıllı arama yap..."
          onChange={(e) => onSearch(e.target.value)}
        />
        <button className="context7-button">
          <i className="fas fa-search"></i>
          Ara
        </button>
      </div>
    </div>
  );
};
```

## 🎯 Turkish UI Standards

### UI Text Patterns
```jsx
// ✅ Turkish UI Labels
const UI_LABELS = {
  dashboard: "Ana Panel",
  search: "Akıllı Arama", 
  analytics: "Analitikler",
  settings: "Ayarlar",
  profile: "Profil",
  logout: "Çıkış Yap",
  save: "Kaydet",
  cancel: "İptal",
  loading: "Yükleniyor...",
  error: "Hata oluştu",
  success: "Başarılı"
};
```

### Form Validations
```jsx
// ✅ Turkish Error Messages
const ERROR_MESSAGES = {
  required: "Bu alan zorunludur",
  email: "Geçerli bir email adresi giriniz",
  minLength: "En az {min} karakter olmalıdır",
  maxLength: "En fazla {max} karakter olabilir",
  numeric: "Sadece sayı giriniz",
  password: "Şifre en az 8 karakter, büyük harf, sayı içermelidir"
};
```

## 📱 Responsive Design

### Breakpoints
```css
/* Context7 Responsive Breakpoints */
@media (max-width: 768px) {
  .context7-card {
    margin: 8px;
    padding: 16px;
  }
  
  .context7-button {
    width: 100%;
    padding: 12px;
  }
}

@media (min-width: 1024px) {
  .context7-dashboard {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
  }
}
```

### Mobile-First Approach
```css
/* ✅ Mobile First */
.context7-container {
  /* Mobile styles */
  padding: 16px;
  
  /* Tablet styles */
  @media (min-width: 768px) {
    padding: 24px;
  }
  
  /* Desktop styles */
  @media (min-width: 1024px) {
    padding: 32px;
  }
}
```

## 🚀 Performance Optimizations

### CSS Optimizations
```css
/* ✅ Hardware Acceleration */
.context7-card {
  will-change: transform, opacity;
  transform: translateZ(0);
}

/* ✅ Efficient Animations */
.context7-button {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ✅ Backdrop Filter Fallback */
.context7-glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

@supports not (backdrop-filter: blur(10px)) {
  .context7-glass {
    background: rgba(255, 255, 255, 0.8);
  }
}
```

### React Performance
```jsx
// ✅ Memoization
import React, { memo, useMemo } from 'react';

const Dashboard = memo(({ data }) => {
  const processedData = useMemo(() => {
    return data.map(item => ({
      ...item,
      formatted: formatData(item)
    }));
  }, [data]);

  return (
    <div className="context7-dashboard">
      {processedData.map(item => (
        <div key={item.id} className="context7-card">
          {item.formatted}
        </div>
      ))}
    </div>
  );
});
```

## 🔍 Testing Requirements

### Component Testing
```jsx
// ✅ Context7 Component Test
import { render, screen } from '@testing-library/react';
import Dashboard from './Dashboard';

describe('Context7 Dashboard', () => {
  test('renders Turkish UI correctly', () => {
    render(<Dashboard />);
    expect(screen.getByText('Akıllı Dashboard')).toBeInTheDocument();
  });
  
  test('applies glassmorphism styles', () => {
    render(<Dashboard />);
    const card = screen.getByRole('main');
    expect(card).toHaveClass('context7-card');
  });
});
```

### Visual Testing
```javascript
// ✅ Playwright Visual Tests
test('Context7 glassmorphism effects', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.locator('.context7-card')).toHaveCSS('backdrop-filter', 'blur(10px)');
  await expect(page.locator('.context7-button')).toHaveCSS('background', /linear-gradient/);
});
```

## 🛡️ Accessibility (WCAG 2.1 AA)

### Color Contrast
```css
/* ✅ Sufficient Contrast */
.context7-text {
  color: #333333; /* 4.5:1 contrast ratio */
  background: rgba(255, 255, 255, 0.9);
}

.context7-button {
  color: #ffffff;
  background: linear-gradient(135deg, #667eea, #764ba2);
  /* Contrast ratio: 4.7:1 */
}
```

### Keyboard Navigation
```jsx
// ✅ Keyboard Accessibility
const Context7Button = ({ onClick, children }) => {
  return (
    <button 
      className="context7-button"
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          onClick();
        }
      }}
      aria-label="Arama yap"
      tabIndex={0}
    >
      {children}
    </button>
  );
};
```

@frontend/src/styles/context7.css
@frontend/src/components/Dashboard.jsx
@frontend/src/components/SearchInterface.jsx 