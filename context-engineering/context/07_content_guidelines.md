# 📝 Collective Memory - İçerik Yönergeleri

## 🎯 İçerik Stratejisi

**Collective Memory** projesi için tutarlı, anlaşılır ve kullanıcı dostu içerik oluşturma standartları. Türkçe UI ve İngilizce kod yaklaşımı [[memory:2176195]] temel alınarak hazırlanmıştır.

## 🌐 Dil Kullanım Kuralları

### 📱 Kullanıcı Arayüzü (Türkçe)
- **Menü ve Butonlar**: Net, kısa Türkçe terimler
- **Mesajlar**: Kullanıcı dostu, samimi dil
- **Hata Mesajları**: Açıklayıcı, çözüm odaklı
- **Yardım Metinleri**: Basit, anlaşılır açıklamalar

```javascript
// ✅ Doğru Türkçe UI örnekleri
const uiTexts = {
  buttons: {
    save: "Kaydet",
    cancel: "İptal",
    search: "Ara",
    upload: "Yükle"
  },
  messages: {
    success: "İşlem başarıyla tamamlandı!",
    error: "Bir hata oluştu. Lütfen tekrar deneyin.",
    loading: "Yükleniyor...",
    empty: "Henüz veri bulunamadı."
  },
  placeholders: {
    search: "Arama yapın...",
    email: "E-posta adresinizi girin",
    password: "Şifrenizi girin"
  }
};
```

### 💻 Kod ve Dokümantasyon (İngilizce)
- **Değişken İsimleri**: İngilizce, camelCase/snake_case
- **Fonksiyon İsimleri**: Açıklayıcı İngilizce
- **Yorumlar**: Türkçe açıklama + İngilizce kod
- **API Dokümantasyonu**: İngilizce

```python
# ✅ Doğru kod+yorum örneği
def get_user_context(user_id: int) -> Dict[str, Any]:
    """
    Kullanıcı bağlam bilgilerini getirir.
    
    Args:
        user_id: Kullanıcının benzersiz ID'si
        
    Returns:
        Kullanıcı bağlam verilerini içeren sözlük
    """
    # Kullanıcı verilerini veritabanından çek
    user_data = database.get_user(user_id)
    
    # Bağlam verilerini hazırla
    context_data = {
        "user_info": user_data,
        "recent_activity": get_recent_activity(user_id),
        "preferences": get_user_preferences(user_id)
    }
    
    return context_data
```

## 📚 Dokümantasyon Standartları

### 📖 README Dosyaları
- **Yapı**: Problem → Çözüm → Kurulum → Kullanım
- **Dil**: Türkçe (kullanıcı odaklı bölümler) + İngilizce (teknik bölümler)
- **Örnekler**: Gerçek kullanım senaryoları
- **Screenshots**: Turkish UI görselleri

### 🔧 API Dokümantasyonu
- **Format**: OpenAPI/Swagger standardı
- **Dil**: İngilizce (endpoint isimleri, parametreler)
- **Açıklamalar**: Net, kısa, örnekli
- **Error Codes**: Standart HTTP kodları + açıklama

```yaml
# ✅ API dokümantasyon örneği
/api/search:
  post:
    summary: "Search content in project files"
    description: "Performs intelligent search across indexed project files"
    parameters:
      - name: query
        in: body
        required: true
        description: "Search query string"
        example: "Django models"
    responses:
      200:
        description: "Search completed successfully"
        example:
          success: true
          results: [...]
          count: 25
      400:
        description: "Invalid search query"
```

### 📝 Kod İçi Dokümantasyon
- **Docstrings**: Google style, İngilizce
- **Inline Comments**: Türkçe, açıklayıcı
- **Type Hints**: Zorunlu, net tipler
- **Examples**: Kullanım örnekleri dahil

## 🎨 UI Metinleri Yazım Kuralları

### ✅ Yapılacaklar
- **Kısa ve net**: 2-5 kelime arası buton metinleri
- **Eylem odaklı**: "Kaydet", "Gönder", "İptal"
- **Kullanıcı merkezli**: "Dosyanızı seçin" (sen dili)
- **Tutarlı terminoloji**: Aynı kavram için aynı kelime
- **Pozitif dil**: "Başarılı" yerine "Tamamlandı"

### ❌ Yapılmayacaklar
- **Teknik jargon**: Kullanıcı arayüzünde teknik terimler
- **Belirsizlik**: "Bir şeyler oluştu" gibi belirsiz mesajlar
- **Uzun metinler**: Paragraf halinde buton metinleri
- **İngilizce karışımı**: "Save et", "Update yap"
- **Olumsuz tonlama**: "Başarısız oldu" yerine "Tekrar deneyin"

```javascript
// ✅ İyi UI metinleri
const goodUITexts = {
  buttons: {
    save: "Kaydet",
    delete: "Sil", 
    edit: "Düzenle",
    share: "Paylaş"
  },
  confirmations: {
    delete: "Bu öğeyi silmek istediğinizden emin misiniz?",
    save: "Değişiklikleriniz kaydedildi.",
    upload: "Dosya başarıyla yüklendi."
  }
};

// ❌ Kötü UI metinleri
const badUITexts = {
  buttons: {
    save: "Kayıt İşlemini Gerçekleştir", // Çok uzun
    delete: "Delete", // İngilizce
    edit: "Düzenleme yapın", // Belirsiz
    share: "Share et" // Karışık dil
  },
  confirmations: {
    delete: "Operation failed", // İngilizce + olumsuz
    save: "Bir şeyler oldu", // Belirsiz
    upload: "File upload process completed successfully" // İngilizce + uzun
  }
};
```

## 📊 Hata Mesajları Yazım Kuralları

### 🎯 Hata Mesajı Anatomisi
1. **Durum Açıklaması**: Ne oldu?
2. **Sebep**: Neden oldu? (opsiyonel)
3. **Çözüm**: Ne yapmalı?
4. **Alternatif**: Başka seçenekler

```javascript
// ✅ İyi hata mesajları
const errorMessages = {
  fileUpload: {
    title: "Dosya yüklenemedi",
    description: "Dosya boyutu 10MB'dan büyük olamaz.",
    action: "Daha küçük bir dosya seçin veya dosyayı sıkıştırın."
  },
  networkError: {
    title: "Bağlantı sorunu",
    description: "İnternet bağlantınızı kontrol edin.",
    action: "Tekrar deneyin veya daha sonra tekrar gelin."
  },
  validation: {
    title: "Eksik bilgi",
    description: "E-posta adresi gerekli.",
    action: "Lütfen geçerli bir e-posta adresi girin."
  }
};
```

## 🔍 Arama ve Etiketleme

### 🏷️ Keyword Strategy
- **Turkish Keywords**: UI ve kullanıcı odaklı içerik için
- **English Keywords**: Teknik dokümantasyon için  
- **Mixed Approach**: README ve genel dokümantasyon için

```markdown
<!-- ✅ İyi keyword örneği -->
# Collective Memory - Akıllı Bağlam Yönetimi

**Keywords**: bağlam yönetimi, AI asistan, Cursor entegrasyonu, context management, AI assistant, smart indexing

## Özellikler
- 🧠 **Akıllı Bağlam Toplama** (Smart Context Collection)
- 🔍 **Hızlı Arama** (Fast Search)
- 🤖 **AI Entegrasyonu** (AI Integration)
```

### 📝 Meta Descriptions
- **Türkçe**: Ana sayfa, kullanıcı kılavuzları
- **İngilizce**: API dokümantasyonu, teknik specs
- **Length**: 150-160 karakter arası
- **Value Proposition**: Net fayda vurgusu

## 🎭 Ton ve Stil Kuralları

### 😊 Kullanıcı Arayüzü Tonu
- **Samimi**: "sen" dili kullanımı
- **Yardımcı**: Destekleyici, rehber tarzı
- **Pozitif**: Çözüm odaklı yaklaşım
- **Net**: Karmaşık açıklamalardan kaçınma

```javascript
// ✅ Doğru ton örnekleri
const uiTone = {
  welcome: "Hoş geldin! Hemen başlayalım.",
  help: "Size nasıl yardımcı olabiliriz?",
  success: "Harika! İşleminiz tamamlandı.",
  guidance: "Sonraki adımda dosyanızı seçebilirsiniz."
};

// ❌ Yanlış ton örnekleri  
const wrongTone = {
  welcome: "Sistemimize giriş yapmış bulunmaktasınız.", // Resmi
  help: "Destek talebi oluşturun.", // Soğuk
  success: "İşlem başarı ile execute edilmiştir.", // Teknik
  guidance: "İlerleyen süreçte data upload gerçekleştirebilirsiniz." // Karışık
};
```

### 📚 Dokümantasyon Tonu
- **Profesyonel**: Resmi ama anlaşılır
- **Eğitici**: Öğretici, adım adım
- **Kapsamlı**: Detaylı ama karmaşık değil
- **Güncel**: En son bilgiler

## 📱 Platform-Specific Content

### 💻 Desktop UI
- **Detaylı açıklamalar**: Daha fazla yer var
- **Keyboard shortcuts**: Klavye kısayolları belirt
- **Advanced features**: Gelişmiş özellikleri göster

### 📱 Mobile/Responsive
- **Kısa metinler**: Ekran alanı sınırlı
- **Touch-friendly**: Dokunma dostu terimler
- **Essential info**: Sadece temel bilgiler

## ✅ İçerik Kalite Kontrol

### 📋 İçerik Review Checklist
- [ ] Türkçe UI metinleri doğru mu?
- [ ] İngilizce kod/API dokümantasyonu doğru mu?
- [ ] Ton tutarlı mı?
- [ ] Kullanıcı dostu mu?
- [ ] Teknik doğruluk var mı?
- [ ] Yazım kurallarına uygun mu?
- [ ] Keywords doğru yerleştirilmiş mi?
- [ ] Call-to-action net mi?

### 🔄 İçerik Güncelleme Süreci
1. **Quarterly Review**: 3 ayda bir genel gözden geçirme
2. **Feature Updates**: Yeni özellik eklendiğinde
3. **User Feedback**: Kullanıcı geri bildirimlerine göre
4. **A/B Testing**: UI metinleri için test yapma
5. **Analytics Review**: Kullanım verilerine göre optimizasyon

Bu içerik yönergeleri, Collective Memory projesinin tüm platformlarda tutarlı, kullanıcı dostu ve etkili iletişim kurmasını sağlar. 