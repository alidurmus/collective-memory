# ERP Sistemi Veri Alanları Listesi

## 1. MÜŞTERİ YÖNETİMİ

### Temel Müşteri Bilgileri
- **Müşteri Kodu** (Otomatik/Manuel)
- **Müşteri Ana Kategori** (Kurumsal/Bireysel)
- **Müşteri Alt Kategori** (Bayi, Distribütör, Son Kullanıcı vb.)
- **Müşteri Tipi** (Yurtiçi/Yurtdışı)
- **Müşteri Durumu** (Aktif/Pasif/Blokeli)

### Kimlik ve Yasal Bilgiler
- **Ticaret Unvanı**
- **Vergi Dairesi**
- **Vergi/TC Kimlik No**
- **Ticaret Sicil No**
- **MERSIS No**
- **Faaliyet Belgesi No**
- **İmza Sirküleri**
- **Yetki Belgesi**

### İletişim Bilgileri
- **Posta Adresi** (Cadde, Sokak, No, Kat, Daire)
- **İl/İlçe/Mahalle/Posta Kodu**
- **Ülke**
- **Telefon No** (Birden fazla)
- **Faks No**
- **E-posta** (Birden fazla)
- **Web Sitesi**
- **Sosyal Medya Hesapları**

### Sevkiyat Adresleri
- **Sevkiyat Adres Kodu**
- **Sevkiyat Adres Tanımı**
- **Tam Adres Bilgileri**
- **İletişim Kişisi**
- **Özel Talimatlar**

### Finansal Bilgiler
- **Para Birimi**
- **Ödeme Vade Süresi**
- **Ödeme Şekli** (Nakit, Çek, Senet, Havale vb.)
- **Kredi Limiti**
- **Kredi Bloke Durumu**
- **Fiyat Listesi**
- **İskonto Oranı**
- **KDV Durumu** 
- **Banka Bilgileri** (IBAN, Banka Adı, Şube)

### Ticari Bilgiler
- **Müşteri Temsilcisi**
- **Müşteri Segmenti**
- **Sektör**
- **Müşteri Büyüklüğü**
- **Yıllık Ciro**
- **Çalışan Sayısı**
- **Kuruluş Tarihi**

### CRM Bilgileri
- **İletişim Geçmişi**
- **Satış Fırsatları**
- **Müşteri Notları**
- **Özel Günler** (Doğum günü, Kuruluş günü)
- **İlgi Alanları**
- **Tercihler**

## 2. TEDARİKÇİ YÖNETİMİ

### Temel Tedarikçi Bilgileri
- **Tedarikçi Kodu**
- **Tedarikçi Adı**
- **Tedarikçi Kategorisi** (Ana/Alt kategoriler)
- **Tedarikçi Tipi** (Yurtiçi/Yurtdışı)
- **Tedarikçi Durumu** (Aktif/Pasif/Onay Bekliyor)
- **Kritiklik Seviyesi** (A/B/C sınıfı)

### Yasal ve Finansal Bilgiler
- **Vergi Dairesi/TC Kimlik No**
- **Ticaret Sicil No**
- **Para Birimi**
- **Ödeme Vade Süresi**
- **Ödeme Şekli**
- **Banka Bilgileri**

### Performans Bilgileri
- **Kalite Puanı**
- **Teslimat Performansı**
- **Fiyat Rekabetçiliği**
- **Güvenilirlik Skoru**
- **Son Değerlendirme Tarihi**

### Belgeler ve Sertifikalar
- **ISO Sertifikaları**
- **Kalite Belgeleri**
- **Mali Mükemmellik Belgeleri**
- **Sigorta Poliçeleri**
- **Yetki Belgesi**

## 3. ÜRÜN YÖNETİMİ

### Temel Ürün Bilgileri
- **Ürün Kodu** (Ana kod + Varyant kodları)
- **Ürün Adı**
- **Ürün Açıklaması**
- **Ürün Kategorisi** (Ana/Alt kategoriler)
- **Ürün Grubu**
- **Marka**
- **Model**
- **Seri No**

### Teknik Özellikler
- **Ürün Tipi** (Hammadde, Yarı Mamul, Mamul, Hizmet)
- **Ürün Durumu** (Aktif/Pasif/Geliştirilmekte)
- **Birim** (Adet, Kg, Litre, Metre vb.)
- **Boyutlar** (En/Boy/Yükseklik)
- **Ağırlık**
- **Renk**
- **Materyal**
- **Teknik Özellikler** (JSON formatında)

### Stok Bilgileri
- **Stok Takip Durumu**
- **Minimum Stok Seviyesi**
- **Maksimum Stok Seviyesi**
- **Güvenlik Stok Seviyesi**
- **Yeniden Sipariş Noktası**
- **Optimum Sipariş Miktarı**
- **Raf Ömrü**
- **Seri/Lot Takibi**

### Fiyat Bilgileri
- **Maliyet Fiyatı**
- **Standart Satış Fiyatı**
- **Para Birimi**
- **KDV Oranı**
- **Özel Tüketim Vergisi**
- **Fiyat Geçerlilik Tarihi**

### Yasal ve Uyumluluk Bilgileri
- **GTIP Kodu**
- **Barkod/GTIN**
- **CE Belgesi**
- **TSE Standardı**
- **Çevre Dostu Sertifika**
- **REACH Uyumluluk**

## 4. STOK YÖNETİMİ

### Depo Bilgileri
- **Depo Kodu**
- **Depo Adı**
- **Depo Tipi** (Ana depo, Transfer depo, Karantina vb.)
- **Depo Adresi**
- **Depo Kapasitesi**
- **Sorumlu Kişi**

### Raf ve Lokasyon Bilgileri
- **Raf Kodu**
- **Koridor/Blok**
- **Seviye**
- **Raf Kapasitesi**
- **Raf Tipi** (Normal, Soğuk, Özel vb.)

### Stok Hareket Bilgileri
- **Hareket Tarihi**
- **Hareket Tipi** (Giriş/Çıkış/Transfer/Sayım/Düzeltme)
- **Hareket Nedeni**
- **Belge No**
- **Miktar**
- **Birim**
- **Birim Fiyat**
- **Toplam Tutar**
- **Seri/Lot No**
- **Son Kullanma Tarihi**

### Sayım Bilgileri
- **Sayım Tarihi**
- **Sayım Tipi** (Tam/Kısmi/Dönemsel/Ani)
- **Sayım Yapan Kişi**
- **Sistem Stoku**
- **Fiili Stok**
- **Fark Miktarı**
- **Fark Nedeni**

## 5. SATIŞ YÖNETİMİ

### Teklif Bilgileri
- **Teklif No**
- **Teklif Tarihi**
- **Geçerlilik Tarihi**
- **Teklif Durumu** (Hazırlanıyor/Gönderildi/Onaylandı/Reddedildi)
- **Müşteri Referans No**
- **Teslim Şartları**
- **Ödeme Şartları**
- **Özel Şartlar**

### Sipariş Bilgileri
- **Sipariş No**
- **Sipariş Tarihi**
- **Teslimat Tarihi**
- **Sipariş Durumu** (Onay Bekliyor/Onaylandı/Üretimde/Sevk Edildi/Teslim Edildi)
- **Sipariş Tipi** (Normal/Acil/İhracat)
- **Müşteri Sipariş No**
- **Kargo Firması**
- **Takip No**

### Sipariş Kalem Bilgileri
- **Kalem No**
- **Ürün Kodu**
- **Sipariş Miktarı**
- **Teslim Edilen Miktar**
- **Kalan Miktar**
- **Birim Fiyat**
- **İskonto Oranı**
- **KDV Oranı**
- **Toplam Tutar**

### Fatura Bilgileri
- **Fatura No**
- **Fatura Tarihi**
- **Fatura Tipi** (Satış/İade/İhracat)
- **E-Fatura UUID**
- **E-Arşiv No**
- **Matbu Seri/Sıra No**
- **Fatura Durumu**
- **Tahsilat Durumu**

## 6. SATIN ALMA YÖNETİMİ

### Satın Alma Talebi
- **Talep No**
- **Talep Tarihi**
- **Talep Eden Departman**
- **Talep Eden Kişi**
- **Talep Nedeni**
- **Aciliyet Durumu**
- **Talep Durumu**

### Teklif İsteme (RFQ)
- **RFQ No**
- **RFQ Tarihi**
- **Teklif Son Tarihi**
- **Davet Edilen Tedarikçiler**
- **Teknik Şartname**
- **Değerlendirme Kriterleri**

### Satın Alma Siparişi
- **Sipariş No**
- **Sipariş Tarihi**
- **Teslim Tarihi**
- **Sipariş Durumu**
- **Onay Durumu**
- **İncoterms**
- **Nakliye Şartları**

### Mal Kabul
- **İrsaliye No**
- **Giriş Tarihi**
- **Teslim Alan Kişi**
- **Kalite Kontrol Durumu**
- **Kabul Edilen Miktar**
- **Red Edilen Miktar**
- **Red Nedeni**

## 7. ÜRETİM YÖNETİMİ

### Üretim Emri
- **Üretim Emri No**
- **Üretim Planı Referansı**
- **Ürün Kodu**
- **Üretim Miktarı**
- **Başlangıç Tarihi**
- **Bitiş Tarihi**
- **Üretim Durumu**
- **Öncelik Seviyesi**

### Reçete (BOM)
- **Reçete Kodu**
- **Reçete Versiyonu**
- **Ana Ürün**
- **Bileşen Ürün**
- **Miktar**
- **Birim**
- **Fire Oranı**
- **Alternatif Bileşenler**

### İş Emri
- **İş Emri No**
- **Operasyon Kodu**
- **Operasyon Adı**
- **İş Merkezi**
- **Planlanan Süre**
- **Gerçekleşen Süre**
- **Başlangıç/Bitiş Zamanı**
- **Operatör**

### Kalite Kontrol
- **Kontrol No**
- **Kontrol Tarihi**
- **Kontrol Noktası**
- **Kontrol Edilecek Özellik**
- **Standart Değer**
- **Ölçülen Değer**
- **Tolerans**
- **Sonuç** (Uygun/Uygunsuz)
- **Kontrol Eden Kişi**

## 8. İNSAN KAYNAKLARI

### Personel Bilgileri
- **Sicil No**
- **TC Kimlik No**
- **Ad/Soyad**
- **Doğum Tarihi/Yeri**
- **Cinsiyet**
- **Medeni Durum**
- **Adres Bilgileri**
- **İletişim Bilgileri**
- **Acil Durum Kişisi**

### İstihdam Bilgileri
- **İşe Giriş Tarihi**
- **İş Çıkış Tarihi**
- **Departman**
- **Pozisyon**
- **Ünvan**
- **Çalışma Şekli** (Tam zamanlı/Yarı zamanlı/Proje bazlı)
- **İş Sözleşmesi Tipi**
- **Maaş Bilgileri**
- **SGK Bilgileri**

### İzin ve Devamsızlık
- **İzin Tipi**
- **İzin Başlangıç/Bitiş Tarihi**
- **İzin Gün Sayısı**
- **İzin Nedeni**
- **Onay Durumu**
- **Yıllık İzin Hakkı**
- **Kullanılan İzin**
- **Kalan İzin**

### Eğitim ve Sertifikalar
- **Eğitim Adı**
- **Eğitim Tarihi**
- **Eğitim Süresi**
- **Eğitim Veren Kurum**
- **Sertifika No**
- **Geçerlilik Tarihi**
- **Yenileme Tarihi**

## 9. FİNANS YÖNETİMİ

### Fatura Detayları
- **Fatura No**
- **Fatura Tarihi**
- **Vade Tarihi**
- **Fatura Tutarı**
- **KDV Tutarı**
- **Toplam Tutar**
- **Ödenen Tutar**
- **Kalan Tutar**
- **Para Birimi**
- **Döviz Kuru**

### Tahsilat/Ödeme
- **İşlem No**
- **İşlem Tarihi**
- **İşlem Tipi** (Tahsilat/Ödeme)
- **Ödeme Şekli**
- **Banka/Kasa**
- **Referans No**
- **Tutar**
- **Açıklama**

### Çek/Senet Takibi
- **Çek/Senet No**
- **Vade Tarihi**
- **Tutar**
- **Banka/Hesap**
- **Durumu** (Portföyde/Bankada/Tahsil Edildi/İade)
- **Ciro Bilgileri**

### Maliyet Muhasebesi
- **Maliyet Merkezi**
- **Maliyet Unsuru**
- **Direkt Malzeme Maliyeti**
- **Direkt İşçilik Maliyeti**
- **Genel Üretim Maliyeti**
- **Toplam Maliyet**
- **Birim Maliyet**

## 10. RAPORLAMA ve ANALİTİK

### Rapor Tanımları
- **Rapor Kodu**
- **Rapor Adı**
- **Rapor Kategorisi**
- **Rapor Tipi** (Tablo/Grafik/Dashboard)
- **Veri Kaynağı**
- **Filtre Parametreleri**
- **Güncelleme Sıklığı**

### Dashboard Widget'ları
- **Widget Adı**
- **Widget Tipi**
- **Veri Sorgusu**
- **Yenileme Periyodu**
- **Görünüm Ayarları**
- **Yetki Seviyeleri**

## 11. SİSTEM YÖNETİMİ

### Kullanıcı Hesapları
- **Kullanıcı Adı**
- **Şifre** (Hash'lenmiş)
- **E-posta**
- **Tam Ad**
- **Durum** (Aktif/Pasif/Blokeli)
- **Son Giriş Tarihi**
- **Şifre Son Değişim Tarihi**
- **İki Faktörlü Doğrulama**

### Roller ve Yetkiler
- **Rol Adı**
- **Rol Açıklaması**
- **Modül Yetkileri**
- **Okuma/Yazma/Silme Yetkileri**
- **Veri Filtreleme Kuralları**

### Sistem Ayarları
- **Şirket Bilgileri**
- **Para Birimi Ayarları**
- **Vergi Ayarları**
- **Dönem Ayarları**
- **Sıra No Formatları**
- **E-posta Sunucu Ayarları**
- **Yedekleme Ayarları**

### Log ve İzleme
- **İşlem Logları**
- **Hata Logları**
- **Kullanıcı Aktivite Logları**
- **Sistem Performans Logları**
- **Değişiklik Geçmişi**

## 12. ENTEGRASYON VE API

### E-Fatura/E-Arşiv
- **Entegratör Bilgileri**
- **Gönderim Durumu**
- **UUID Bilgileri**
- **Hata Kodları**
- **Yanıt Mesajları**

### Dış Sistem Entegrasyonları
- **API Anahtarları**
- **Endpoint Bilgileri**
- **Senkronizasyon Durumu**
- **Son Senkronizasyon Tarihi**
- **Hata Durumları**

### Veri İçe/Dışa Aktarma
- **İmport/Export Şablonları**
- **Veri Haritalama Kuralları**
- **Doğrulama Kuralları**
- **İşlem Logları**

## 13. DOKÜMAN YÖNETİMİ

### Doküman Bilgileri
- **Doküman Kodu**
- **Doküman Adı**
- **Doküman Tipi**
- **Versiyon No**
- **Oluşturma Tarihi**
- **Son Değişiklik Tarihi**
- **Durum** (Taslak/Onaylandı/Arşivlendi)
- **Dosya Yolu**
- **Dosya Boyutu**

### Onay Süreci
- **Onay Akış Şeması**
- **Onaylayan Kişiler**
- **Onay Tarihleri**
- **Onay Durumu**
- **Red Nedenleri**

Bu veri alanları listesi, modern bir ERP sisteminin temel ihtiyaçlarını karşılayacak şekilde tasarlanmıştır. Her modül için gerekli olan temel ve detay alanları içermekte, aynı zamanda Türkiye'deki yasal gereklilikleri de gözetmektedir.