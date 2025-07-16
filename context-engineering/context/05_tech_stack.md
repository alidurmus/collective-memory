# 🛠️ Context Engineering Template - Tech Stack

## 🎯 Context Engineering Özellikleri

**Context Engineering Template** için özel teknoloji seçimleri ve entegrasyon standartları.

> **Ana Tech Stack**: Detaylı teknoloji bilgileri için [`../../docs/technical/architecture/TECHNOLOGY_STACK.md`](../../docs/technical/architecture/TECHNOLOGY_STACK.md) dosyasına bakın.

## 🏗️ Template-Specific Technologies

### 📁 Context Organization
- **MDC Format**: Metadata + Content yapısı
- **YAML Frontmatter**: Dosya metadata yönetimi
- **JSON Configuration**: Template ayarları

### 🔧 Development Standards
- **Turkish UI / English Code** [[memory:2176195]]
- **Context7 Framework** [[memory:592593]]  
- **Playwright Testing** [[memory:592592]]

### 🧠 AI Integration
- **Prompt Templates**: Standardized AI prompts
- **Context Collection**: Otomatik bağlam toplama
- **Memory Management**: Persistent context storage

### 📊 Project Structure Standards
```
context-engineering/
├── commands/           # Executable scripts
├── context/           # Project context files  
├── output/            # Generated outputs
└── prompts/           # AI templates
```

## 🎨 Context7 Framework Integration

### Core Components
- **Glassmorphism Effects**: Modern UI design
- **Responsive Grid**: Mobile-first approach
- **Turkish Localization**: UI/UX in Turkish

### Implementation
```css
.context7-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
}
```

## 🧪 Testing Standards

### Playwright Configuration [[memory:592592]]
```javascript
// playwright.config.js
export default {
  testDir: './tests',
  timeout: 30000,
  use: {
    locale: 'tr-TR',
    timezoneId: 'Europe/Istanbul'
  }
};
```

## 📋 Configuration Standards

### Template Configuration
```json
{
  "template_version": "1.0",
  "language": {
    "ui": "tr",
    "code": "en"
  },
  "frameworks": {
    "ui": "context7",
    "testing": "playwright",
    "documentation": "markdown"
  }
}
```

---

**📖 Detaylı Teknoloji Bilgileri**: [`../../docs/technical/architecture/TECHNOLOGY_STACK.md`](../../docs/technical/architecture/TECHNOLOGY_STACK.md) 