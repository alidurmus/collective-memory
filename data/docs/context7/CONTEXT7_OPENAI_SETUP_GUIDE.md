# 🤖 OpenAI API Key Kurulum Rehberi

## Hızlı Kurulum (5 dakika)

### 1. OpenAI API Key Edinme

1. **https://platform.openai.com/** adresine gidin
2. **Hesap oluşturun** veya giriş yapın
3. **API Keys** sekmesine tıklayın
4. **"Create new secret key"** butonuna tıklayın
5. Key'i **kopyalayın** (bir daha göremezsiniz!)

### 2. .env Dosyası Oluşturma

Proje ana dizininde `.env` dosyası oluşturun:

**Windows (PowerShell):**
```powershell
echo. > .env
```

**Windows (CMD):**
```cmd
type nul > .env
```

**Linux/Mac:**
```bash
touch .env
```

### 3. API Key'i .env Dosyasına Ekleyin

`.env` dosyasını açın ve aşağıdaki satırı ekleyin:

```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

**Örnek:**
```env
OPENAI_API_KEY=sk-proj-abcd1234xyz5678
```

### 4. Sistemin Çalıştığını Kontrol Edin

```bash
python manage.py context7_deploy_check --environment=development
```

**Başarı mesajı görmelisiniz:**
```
🤖 OpenAI API integration: ENABLED
🎯 AI Model: gpt-4o
```

## 🎯 AI Özelliklerini Test Etme

### Django Shell'de Test:

```bash
python manage.py shell
```

```python
from django.conf import settings
print(f"AI Enabled: {settings.AI_ENABLED}")
print(f"AI Model: {settings.AI_MODEL}")
```

### TODO Otomasyonu Test:

1. Admin panele girin: http://127.0.0.1:8000/admin/
2. Core → Todos bölümüne gidin
3. Bir TODO görevi oluşturun
4. "AI Analiz" butonunu kullanın

## 🔒 Güvenlik Notları

- ❌ API key'inizi **asla** Git'e commit etmeyin
- ✅ `.env` dosyası `.gitignore`'da olmalı
- ✅ Production'da farklı key kullanın
- ✅ Düzenli olarak key'leri yenileyin

## 💰 Maliyet Kontrolü

- OpenAI API'si **ücretlidir**
- **Usage** sayfasından kullanımınızı takip edin
- **Billing limits** ayarlayın
- Test için **düşük limit** belirleyin ($5-10)

## 🔧 Sorun Giderme

### "API key not found" hatası:
1. `.env` dosyasının doğru yerde olduğundan emin olun
2. Key'in `OPENAI_API_KEY=` ile başladığından emin olun
3. Key'de boşluk veya özel karakter olmadığından emin olun

### "Rate limit exceeded" hatası:
1. OpenAI dashboard'da kullanım limitinizi kontrol edin
2. Daha yavaş istek gönderin
3. Billing limitinizi artırın

### Import hatası:
```bash
pip install pydantic-ai openai httpx
```

---

## ✅ Kurulum Tamamlandı!

AI özellikleri artık aktif! Context7 görev otomasyonu kullanıma hazır.

📞 **Destek**: Sorunlar için GitHub Issues açın. 