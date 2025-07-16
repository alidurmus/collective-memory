# 🏛️ Collective Memory - Yazılım Mimarisi

## 🎯 Mimari Genel Bakış

**Collective Memory** sistemi, **Context Engineering Template** üzerine inşa edilmiş, **hibrit monolitik-mikroservis** mimarisini benimser. AI-destekli bağlam yönetimi için optimize edilmiş, modüler ve ölçeklenebilir yapı sunar.

### 🏗️ Mimari Prensipler

1. **🔀 Separation of Concerns**: Her modül tek sorumluluğa sahip
2. **🔄 Loose Coupling**: Modüller arası minimal bağımlılık
3. **📈 High Cohesion**: İlgili fonksiyonlar aynı modülde
4. **🚀 Scalability**: Yatay ve dikey ölçeklendirme desteği
5. **🛡️ Security by Design**: Her katmanda güvenlik önlemleri
6. **🎨 Context7 Integration**: Modern UI framework entegrasyonu [[memory:592593]]

## 🌐 Sistem Mimarisi

### 📁 Context Engineering Template Yapısı
```
collective-memory/
├── context-engineering/     # 🏗️ Yeni mimari yapı
│   ├── commands/           # 🔧 Betikler ve araçlar
│   ├── context/           # 🧠 Proje bağlamı
│   ├── output/            # 📤 Üretilen çıktılar
│   └── prompts/           # 💬 AI şablonları
├── collective-memory-app/  # 🚀 Ana uygulama
├── data/                  # 🧪 Demo/test verileri
└── docs/                  # 📚 Dokümantasyon
```

## 🚀 Ana Uygulama Mimarisi

### 🎨 Frontend Mimarisi (React + Context7)

```typescript
// Component hiyerarşi yapısı - Türkçe UI + İngilizce kod [[memory:2176195]]
const KullaniciPaneli: React.FC<KullaniciPaneliProps> = ({ 
  userId, 
  isActive,
  onUserClick 
}) => {
  const { kullaniciData, isLoading } = useKullaniciData(userId);
  
  return (
    <div className="kullanici-paneli context7-card">
      <h2>Kullanıcı Bilgileri</h2>
      {/* Turkish UI labels, English variable names */}
    </div>
  );
};
```

### 🧠 Business Logic Katmanı

```python
class ContextEngine:
    """
    Ana bağlam yönetim motoru - Collective Memory'nin çekirdek bileşeni
    """
    
    def __init__(self):
        self.file_monitor = FileMonitor()
        self.content_indexer = ContentIndexer()
        self.search_engine = SearchEngine()
        self.cursor_reader = CursorReader()
        self.query_builder = QueryBuilder()
    
    async def collect_context(self, trigger_comment: str) -> ContextData:
        """
        Bağlam toplama ana işlevi
        
        Args:
            trigger_comment: Tetikleyici yorum satırı (// @collect-memory)
            
        Returns:
            ContextData: Toplanan ve işlenmiş bağlam verisi
        """
        
        # 1. Trigger analizi
        trigger_data = self.parse_trigger(trigger_comment)
        
        # 2. İlgili dosyaları bulma
        relevant_files = await self.find_relevant_files(trigger_data)
        
        # 3. Chat geçmişini analiz etme
        chat_history = await self.cursor_reader.get_recent_chats()
        
        # 4. Proje kurallarını getirme
        project_rules = await self.get_project_rules()
        
        # 5. Bağlam sentezi
        context = await self.synthesize_context(
            files=relevant_files,
            chat_history=chat_history,
            rules=project_rules,
            trigger_data=trigger_data
        )
        
        return context
```

### 💾 Database Schema Design

```sql
-- Ana veritabanı schema'sı - SQLite tabanlı, normalize edilmiş yapı

-- 📁 Files tablosu - Dosya metadata'sı
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT UNIQUE NOT NULL,
    content_hash TEXT NOT NULL,
    file_type TEXT NOT NULL,
    size_bytes INTEGER NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    indexed_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 🔍 Search index - FTS5 virtual table
CREATE VIRTUAL TABLE search_fts USING fts5(
    title,
    content,
    keywords,
    file_path,
    content='search_index',
    content_rowid='id'
);

-- 💬 Chat history tablosu
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    message_content TEXT NOT NULL,
    message_type TEXT NOT NULL CHECK (message_type IN ('user', 'assistant', 'system')),
    timestamp TIMESTAMP NOT NULL,
    context_data TEXT, -- JSON format
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Test Mimarisi

### 🐍 Backend Testing [[memory:592592]]
```python
# pytest kullanımı - AAA pattern
def test_kullanici_bilgisi_getir_basarili():
    # Arrange (Hazırlık)
    user_id = 123
    expected_data = {"id": 123, "name": "Test User"}
    
    # Act (İşlem)
    result = kullanici_bilgisi_getir(user_id)
    
    # Assert (Doğrulama)
    assert result == expected_data
    assert result["id"] == user_id
```

### 🎭 Frontend Testing (Playwright) [[memory:592592]]
```javascript
// Playwright test örneği - Turkish UI testing
import { test, expect } from '@playwright/test';

test('arama funcionality çalışır', async ({ page }) => {
  await page.goto('http://localhost:3003');
  
  await page.fill('[data-testid="arama-input"]', 'test arama');
  await page.click('[data-testid="ara-button"]');
  
  await expect(page.locator('.arama-sonuclari')).toBeVisible();
  await expect(page.locator('.sonuc-item')).toBeGreaterThanOrEqual(1);
});
```

## 🐳 Deployment Architecture

### 🐳 Container Architecture
```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    volumes:
      - ./data:/app/data
    depends_on:
      - redis
      
  frontend:
    build: ./frontend
    ports:
      - "3003:3003"
    depends_on:
      - backend
      
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
```

## 📊 Monitoring ve Observability

```python
class SystemHealthMonitor:
    """
    Sistem sağlığı ve performans izleme
    """
    
    async def monitor_system_health(self):
        """
        Sürekli sistem sağlığı izleme
        """
        health_metrics = {
            'database': await self.check_database_health(),
            'redis': await self.check_redis_health(),
            'disk_space': await self.check_disk_space(),
            'memory_usage': await self.check_memory_usage(),
            'api_response_time': await self.check_api_performance(),
            'search_performance': await self.check_search_performance()
        }
        
        # Kritik metrikleri kontrol et
        critical_issues = self.identify_critical_issues(health_metrics)
        
        if critical_issues:
            await self.alerting_system.send_alerts(critical_issues)
        
        return health_metrics
```

## ⚙️ Configuration Management

```python
class ConfigurationManager:
    """
    Çok katmanlı konfigürasyon yönetimi
    """
    
    def __init__(self):
        self.layers = [
            DefaultConfig(),      # 1. Varsayılan ayarlar
            EnvironmentConfig(),  # 2. Environment variables
            FileConfig(),         # 3. config.json dosyası
            DatabaseConfig(),     # 4. Veritabanı ayarları
            RuntimeConfig()       # 5. Runtime değişiklikleri
        ]
    
    def get_config(self, key: str, default=None):
        """
        Katman önceliğine göre konfigürasyon değeri getirme
        """
        for layer in reversed(self.layers):  # Runtime -> Default
            if layer.has_key(key):
                return layer.get(key)
        return default
```

Bu mimari dokümantasyonu, sistemin ana bileşenlerini ve yapısını özetleyerek, geliştiricilerin hızla proje mimarisini anlayabilmesini sağlar. 