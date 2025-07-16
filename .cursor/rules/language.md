# 🌐 Dil Standartları [[memory:2176195]]

## Ana Dil Kuralları
- **Kullanıcı Arayüzü**: Türkçe (frontend, dokümantasyon, mesajlar)
- **Kod**: İngilizce (değişkenler, fonksiyonlar, class isimleri)
- **Yorumlar**: Türkçe (kullanıcı dostu açıklamalar)
- **Commit Mesajları**: İngilizce (uluslararası standart)

## Dokümantasyon Dil Kuralları
- **README**: Türkçe + İngilizce paralel
- **API Dokümantasyonu**: İngilizce
- **Kullanıcı Kılavuzu**: Türkçe
- **Kod İçi Dokümantasyon**: İngilizce docstring + Türkçe açıklama

## Kod Yazma Örnekleri

### Python Örnek
```python
# ✅ Doğru örnek
def kullanici_bilgisi_getir(user_id: int) -> Dict[str, Any]:
    """
    Kullanıcı bilgilerini veritabanından getirir.
    
    Args:
        user_id: Kullanıcının benzersiz ID'si
        
    Returns:
        Kullanıcı bilgilerini içeren sözlük
        
    Raises:
        UserNotFoundError: Kullanıcı bulunamadığında
    """
    # Türkçe yorum - kullanıcı ID'si kontrolü
    if not user_id:
        raise ValueError("Kullanıcı ID'si gerekli")
    
    # İngilizce variable name, Turkish comment
    user_data = get_user_from_database(user_id)
    return {"id": user_id, "name": user_data.name}
```

### React/TypeScript Örnek
```tsx
// ✅ Doğru örnek
interface KullaniciKartProps {
  kullaniciId: number;
  isActive: boolean;
  onKullaniciClick: (id: number) => void;
}

const KullaniciKart: React.FC<KullaniciKartProps> = ({ 
  kullaniciId, 
  isActive, 
  onKullaniciClick 
}) => {
  // Türkçe state isimleri UI için
  const [kullaniciDetay, setKullaniciDetay] = useState<UserDetail | null>(null);
  
  return (
    <div className="kullanici-kart">
      <h2>Kullanıcı Bilgileri</h2>
      {/* Turkish UI labels, English variable names */}
      <p>Aktif: {isActive ? "Evet" : "Hayır"}</p>
      <button onClick={() => onKullaniciClick(kullaniciId)}>
        Detayları Gör
      </button>
    </div>
  );
};
```

## UI Metin Kuralları
- **Butonlar**: Türkçe (Kaydet, İptal, Sil)
- **Formlar**: Türkçe label'lar (Ad, Soyad, E-posta)
- **Mesajlar**: Türkçe (Başarıyla kaydedildi, Hata oluştu)
- **Navigasyon**: Türkçe (Ana Sayfa, Ayarlar, Profil)

## Hata Mesajı Kuralları
- **Kullanıcı Hatası**: Türkçe mesaj
- **Geliştirici Hatası**: İngilizce log
- **API Hatası**: İngilizce response, Türkçe display

```python
# ✅ Hata mesajı örneği
try:
    user = User.objects.get(id=user_id)
except User.DoesNotExist:
    # İngilizce log
    logger.error(f"User not found with id: {user_id}")
    # Türkçe kullanıcı mesajı
    raise UserNotFoundError("Kullanıcı bulunamadı")
``` 