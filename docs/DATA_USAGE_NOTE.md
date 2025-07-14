# 📁 Data Klasörü Kullanım Açıklaması

**ÖNEMLİ NOT:** `/data` klasörü sadece örnek ve test amaçlıdır!

---

## 🚨 **Önemli Uyarı**

### **`/data` Klasörü:**
- ❌ **ANA PROGRAM DEĞİLDİR**
- ✅ **Sadece örnek/demo içerik**
- ✅ **Test ve deneme amaçlı**
- ✅ **Dokümantasyon örnekleri**

### **Ana Program:**
- ✅ **`collective-memory-app/` klasöründedir**
- ✅ **Asıl çalışan sistem budur**
- ✅ **Tüm komutlar burada çalıştırılır**

---

## 🎯 **Doğru Kullanım**

### **1. Kendi Verilerinizle Kullanım (Önerilen):**
```bash
cd collective-memory-app
python src/main.py --interactive --data-path /path/to/your/documents
```

### **2. Test/Demo Amaçlı Kullanım:**
```bash
cd collective-memory-app
python src/main.py --interactive --data-path ../data
```

---

## 📋 **Data Klasörü İçeriği**

`/data` klasöründeki tüm dosyalar sadece:
- **Örnektir** - Gerçek proje verisi değil
- **Test içindir** - Sistemin nasıl çalıştığını gösterir
- **Dokümantasyon örneğidir** - Format ve yapı referansı

---

## 💻 **Gerçek Kullanım Senaryoları**

### **Kendi Projeleriniz İçin:**
```bash
# Kendi proje klasörünüzü belirtin:
python src/main.py --interactive --data-path /home/user/my-project
python src/main.py --interactive --data-path C:\Users\Name\Documents\MyProject
python src/main.py --interactive --data-path ~/Desktop/work-docs
```

### **Test ve Öğrenme İçin:**
```bash
# Demo data ile test edin:
python src/main.py --interactive --data-path ../data
```

---

## 🔍 **Hangi Klasörü Kullanmalıyım?**

| Amaç | Kullanılacak Path | Açıklama |
|------|------------------|----------|
| **Gerçek çalışma** | `/path/to/your/docs` | Kendi dökümanlarınız |
| **Test/Demo** | `../data` | Örnek verilerle deneme |
| **Öğrenme** | `../data` | Sistemi anlamak için |
| **Geliştirme** | `../data` | Özellik testi için |

---

## 🎯 **Özet**

1. **Ana program:** `collective-memory-app/` klasöründe
2. **Data klasörü:** Sadece örnek/test içeriği
3. **Gerçek kullanım:** Kendi klasörünüzü belirtin
4. **Demo/Test:** `../data` kullanabilirsiniz

---

**⚡ Bu dosya `/data` klasörünün rolünü netleştirmek için oluşturulmuştur.** 