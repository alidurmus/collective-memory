# 💬 JSON Konuşma Sistemi - Kullanım Rehberi

**Collective Memory v2.2 - JSON Chat Storage System**  
**Tarih:** 14 Ocak 2025  
**Versiyon:** 1.0  

---

## 🎯 **Genel Bakış**

JSON Konuşma Sistemi, Collective Memory projesi için geliştirilmiş, konuşmaları human-readable JSON dosyalarında saklayan modern bir hafıza yönetim çözümüdür. Bu sistem, Cursor AI chat geçmişini organize eder ve geliştiricilere güçlü arama ve analiz yetenekleri sunar.

### ✨ **Ana Özellikler**

- ✅ **JSON Formatında Depolama** - Human readable, version control friendly
- ✅ **Otomatik Organizasyon** - Günlük ve proje bazlı klasörleme
- ✅ **Güçlü Arama** - Full-text search ve filtreleme
- ✅ **Export/Import** - Çoklu format desteği (JSON, Markdown)
- ✅ **Cursor Entegrasyonu** - Otomatik Cursor chat import
- ✅ **REST API** - Web uygulamaları için API desteği
- ✅ **CLI Interface** - Terminal tabanlı yönetim
- ✅ **Tag Sistemi** - Konuşma etiketleme ve filtreleme

---

## 🏗️ **Sistem Mimarisi**

### 📁 **Dizin Yapısı**
```
.collective-memory/
├── conversations/              # 💬 JSON konuşma dosyaları
│   ├── index.json             # 📋 Merkezi indeks dosyası
│   ├── daily/                 # 📅 Günlük organizasyon
│   │   ├── 2025-01-14/        # Bugünkü konuşmalar
│   │   └── 2025-01-13/        # Dünkü konuşmalar
│   ├── projects/              # 📁 Proje bazlı konuşmalar
│   ├── archived/              # 📦 Arşivlenmiş konuşmalar
│   └── exports/               # 📤 Export edilen dosyalar
├── database/                  # 🗄️ SQLite veritabanları
├── cache/                     # ⚡ Cache dosyaları
├── logs/                      # 📝 Log dosyaları
└── config/                    # ⚙️ Konfigürasyon
```

### 🔗 **JSON Konuşma Formatı**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Context7 ERP Modül Geliştirme",
  "project_path": "/path/to/project",
  "created_at": "2025-01-14T10:30:00Z",
  "updated_at": "2025-01-14T11:45:00Z",
  "tags": ["context7", "erp", "development"],
  "metadata": {
    "project_type": "django",
    "framework": "context7",
    "priority": "high"
  },
  "messages": [
    {
      "id": "msg-001",
      "role": "user",
      "content": "Konuşma içeriği...",
      "timestamp": "2025-01-14T10:30:00Z",
      "metadata": {
        "query_type": "feature_request"
      }
    }
  ]
}
```

---

## 🚀 **Hızlı Başlangıç**

### 1. **Sistem Başlatma**
```python
from json_chat_manager import JSONChatManager

# Chat manager'ı başlat
chat_manager = JSONChatManager("/path/to/your/project")

# İlk konuşmayı oluştur
conversation_id = chat_manager.create_conversation(
    title="İlk Konuşmam",
    project_path="/path/to/project",
    initial_message="Merhaba, nasıl yardımcı olabilirim?"
)
```

### 2. **CLI Kullanımı**
```bash
# Yeni konuşma oluştur
python src/chat_cli.py create "Yeni Proje Planı" --project "/path/to/project"

# Konuşmaları listele
python src/chat_cli.py list --limit 10

# Konuşma detaylarını göster
python src/chat_cli.py show CONVERSATION_ID

# Arama yap
python src/chat_cli.py search "Context7 ERP"
```

### 3. **REST API Kullanımı**
```bash
# API server'ı başlat
python api_server.py --data-folder "/path/to/project"

# Yeni konuşma oluştur
curl -X POST http://localhost:8000/api/v1/chat/conversations \
  -H "Content-Type: application/json" \
  -d '{"title": "API Test", "project_path": "/path/to/project"}'

# Konuşmaları listele
curl http://localhost:8000/api/v1/chat/conversations?limit=10
```

---

## 📋 **Detaylı Kullanım**

### 💬 **Konuşma Yönetimi**

#### Yeni Konuşma Oluşturma
```python
conversation_id = chat_manager.create_conversation(
    title="Context7 ERP Geliştirme",
    project_path="/path/to/context7-project",
    initial_message="Context7 ERP için yeni özellik geliştirelim"
)
```

#### Mesaj Ekleme
```python
message_id = chat_manager.add_message(
    conversation_id=conversation_id,
    role="user",  # "user", "assistant", "system"
    content="Satış modülüne yeni özellik ekle",
    metadata={
        "feature": "sales",
        "priority": "high"
    }
)
```

#### Konuşma Yükleme
```python
conversation = chat_manager.load_conversation(conversation_id)
print(f"Başlık: {conversation.title}")
print(f"Mesaj Sayısı: {len(conversation.messages)}")
```

### 🔍 **Arama ve Filtreleme**

#### Temel Arama
```python
results = chat_manager.search_conversations(
    query="Context7 ERP",
    limit=20
)
```

#### Gelişmiş Filtreleme
```python
results = chat_manager.search_conversations(
    query="satış modülü",
    project_path="/path/to/specific/project",
    tags=["erp", "sales"],
    limit=50
)
```

#### CLI ile Arama
```bash
# Basit arama
python src/chat_cli.py search "Context7"

# Proje filtrelemeli arama
python src/chat_cli.py list --project "/path/to/project" --limit 20
```

### 📤 **Export ve Import**

#### Export İşlemleri
```python
# JSON export
json_path = chat_manager.export_conversation(conversation_id, "json")

# Markdown export
md_path = chat_manager.export_conversation(conversation_id, "markdown")
```

#### Cursor Chat Import
```python
from cursor_reader import EnhancedCursorDatabaseReader
cursor_reader = EnhancedCursorDatabaseReader()

# Cursor chat'lerini otomatik import et
imported_count = chat_manager.import_from_cursor(cursor_reader)
print(f"{imported_count} konuşma import edildi")
```

#### CLI ile Export/Import
```bash
# Konuşma export et
python src/chat_cli.py export CONVERSATION_ID --format markdown --output "my_chat.md"

# Cursor'dan import et
python src/chat_cli.py import-cursor
```

---

## 🛠️ **API Referansı**

### REST API Endpoints

#### GET `/api/v1/chat/conversations`
Konuşmaları listele
```bash
curl "http://localhost:8000/api/v1/chat/conversations?query=Context7&limit=10"
```

#### POST `/api/v1/chat/conversations`
Yeni konuşma oluştur
```bash
curl -X POST http://localhost:8000/api/v1/chat/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Yeni Konuşma",
    "project_path": "/path/to/project",
    "initial_message": "Merhaba!"
  }'
```

#### GET `/api/v1/chat/conversations/{id}`
Konuşma detaylarını getir
```bash
curl http://localhost:8000/api/v1/chat/conversations/550e8400-e29b-41d4-a716-446655440000
```

#### POST `/api/v1/chat/conversations/{id}/messages`
Konuşmaya mesaj ekle
```bash
curl -X POST http://localhost:8000/api/v1/chat/conversations/CONV_ID/messages \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "Yeni mesaj içeriği"
  }'
```

#### GET `/api/v1/chat/stats`
Sistem istatistikleri
```bash
curl http://localhost:8000/api/v1/chat/stats
```

### Python API

#### JSONChatManager Sınıfı
```python
class JSONChatManager:
    def __init__(self, data_folder: str = None)
    def create_conversation(self, title: str, project_path: str = None, initial_message: str = None) -> str
    def add_message(self, conversation_id: str, role: str, content: str, metadata: Dict = None) -> str
    def load_conversation(self, conversation_id: str) -> Optional[ChatConversation]
    def search_conversations(self, query: str = None, project_path: str = None, tags: List[str] = None, limit: int = 50) -> List[Dict]
    def export_conversation(self, conversation_id: str, format: str = "json") -> Optional[str]
    def import_from_cursor(self, cursor_reader) -> int
    def get_conversation_stats(self) -> Dict[str, Any]
```

---

## ⚙️ **Konfigürasyon**

### Config.json Ayarları
```json
{
  "json_chat_settings": {
    "enabled": true,
    "storage_path": ".collective-memory/conversations",
    "auto_save": true,
    "backup_interval_hours": 24,
    "max_conversations_per_project": 1000,
    "export_formats": ["json", "markdown", "txt"],
    "indexing": {
      "enabled": true,
      "full_text_search": true,
      "rebuild_interval_hours": 6
    },
    "import_settings": {
      "cursor_auto_import": true,
      "cursor_import_limit": 100,
      "merge_duplicates": true
    }
  }
}
```

### Environment Variables
```bash
export COLLECTIVE_MEMORY_DATA_FOLDER="/path/to/your/project"
export COLLECTIVE_MEMORY_CHAT_BACKUP_ENABLED=true
export COLLECTIVE_MEMORY_AUTO_IMPORT_CURSOR=true
```

---

## 📊 **İstatistikler ve Monitoring**

### Sistem İstatistikleri
```python
stats = chat_manager.get_conversation_stats()

print(f"Toplam Konuşma: {stats['total_conversations']}")
print(f"Toplam Mesaj: {stats['total_messages']}")
print(f"Storage Boyutu: {stats['storage_size']}")
print(f"Son Aktivite: {stats['last_activity']}")

# Proje bazlı istatistikler
for project, count in stats['projects'].items():
    print(f"{project}: {count} konuşma")

# Tag istatistikleri
for tag, count in stats['tags'].items():
    print(f"#{tag}: {count} konuşma")
```

### CLI ile İstatistikler
```bash
python src/chat_cli.py stats
```

---

## 🔧 **Troubleshooting**

### Yaygın Sorunlar

#### 1. **Dosya İzin Hatası**
```bash
# Çözüm: İzinleri düzelt
chmod -R 755 .collective-memory/
```

#### 2. **JSON Parse Hatası**
```python
# Bozuk JSON dosyalarını kontrol et
import json
with open("conversation_file.json", 'r') as f:
    json.load(f)  # Hata burada görünür
```

#### 3. **Disk Alanı Sorunu**
```bash
# Storage boyutunu kontrol et
du -sh .collective-memory/conversations/
```

#### 4. **Index Rebuild**
```python
# Index'i yeniden oluştur
chat_manager._save_index()
```

### Debug Modu
```bash
# Debug modunda çalıştır
export DEBUG=true
python src/chat_cli.py list
```

---

## 🚀 **Gelişmiş Özellikler**

### 1. **Otomatik Backup**
```python
# Günlük otomatik backup
chat_manager.create_daily_backup()
```

### 2. **Batch İşlemler**
```python
# Toplu mesaj ekleme
messages = [
    {"role": "user", "content": "Mesaj 1"},
    {"role": "assistant", "content": "Yanıt 1"},
    {"role": "user", "content": "Mesaj 2"}
]

for msg in messages:
    chat_manager.add_message(conversation_id, **msg)
```

### 3. **Tag Yönetimi**
```python
# Konuşmaya tag ekle
conversation = chat_manager.load_conversation(conversation_id)
conversation.tags.extend(["new-tag", "important"])
chat_manager._save_conversation(conversation)
```

### 4. **Metadata Filtreleme**
```python
# Metadata bazlı arama
results = chat_manager.search_conversations(
    query="Django",
    project_path="/django-project"
)

# Sadece yüksek öncelikli konuşmalar
high_priority = [
    conv for conv in results 
    if conv.get('metadata', {}).get('priority') == 'high'
]
```

---

## 📚 **Entegrasyon Örnekleri**

### VS Code Extension ile Entegrasyon
```javascript
// VS Code extension'da JSON chat kullanımı
const { exec } = require('child_process');

function createConversation(title, projectPath) {
    const command = `python src/chat_cli.py create "${title}" --project "${projectPath}"`;
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error}`);
            return;
        }
        console.log(`Conversation created: ${stdout}`);
    });
}
```

### Web Dashboard Entegrasyonu
```javascript
// React component'ta API kullanımı
import React, { useState, useEffect } from 'react';

const ConversationsList = () => {
    const [conversations, setConversations] = useState([]);
    
    useEffect(() => {
        fetch('/api/v1/chat/conversations')
            .then(response => response.json())
            .then(data => setConversations(data.data));
    }, []);
    
    return (
        <div className="conversations-list">
            {conversations.map(conv => (
                <div key={conv.id} className="conversation-item">
                    <h3>{conv.title}</h3>
                    <p>{conv.message_count} mesaj</p>
                </div>
            ))}
        </div>
    );
};
```

---

## 📞 **Destek ve Katkı**

### Dokümantasyon
- **[Ana README](../../README.md)** - Proje genel bakışı
- **[API Referansı](../technical/api/API_REFERENCE.md)** - Detaylı API dokümantasyonu
- **[Sistem Mimarisi](../technical/architecture/ARCHITECTURE.md)** - Teknik mimari

### Katkı Sağlama
```bash
# Development branch'ı oluştur
git checkout -b feature/json-chat-enhancement

# Değişikliklerinizi commit edin
git commit -m "feat: JSON chat yeni özellik"

# Pull request gönderin
git push origin feature/json-chat-enhancement
```

### İletişim
- **GitHub Issues**: Hata bildirimi ve özellik istekleri
- **GitHub Discussions**: Genel tartışmalar
- **Documentation**: Dokümantasyon iyileştirmeleri

---

**🎯 JSON Konuşma Sistemi ile konuşmalarınız artık organize, aranabilir ve yedeklenebilir! 💬✨** 