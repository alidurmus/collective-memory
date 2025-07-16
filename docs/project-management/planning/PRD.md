# **Kapsamlı Ürün Gereksinimleri Dokümanı (PRD): Collective Memory v2.0**

* **Versiyon Geçmişi:**  
  * **v2.0 (13 Temmuz 2025):** Belge, standart PRD bölümlerini (hedefler, varsayımlar, yayın planı, başarı metrikleri vb.) içerecek şekilde genişletildi.  
  * **v1.1 (13 Temmuz 2025):** Harici projelerden alınan dersler doğrultusunda güncellendi.  
  * **v1.0 (13 Temmuz 2025):** İlk sürüm.

### **1\. Giriş ve Genel Bakış**

* **1.1. Proje Adı:** Collective Memory  
* **1.2. Problem Tanımı:** Yazılım geliştiriciler, Cursor gibi YZ destekli kodlama asistanlarını kullanırken, asistanın önceki konuşmaları, proje bağlamını ve belirlenen standartları unutması nedeniyle sık sık tekrara düşmektedir. Bu "amnezi" durumu, her yeni görevde bağlamı yeniden açıklama zorunluluğu getirerek bilişsel yükü artırır ve verimliliği düşürür.  
* **1.3. Çözüm (Vizyon):** "Collective Memory", bireysel geliştiricinin yerel makinesinde çalışan, akıllı bir bağlam orkestratörüdür. Geliştiricinin kod içerisinden basit bir komutla tetiklediği bu araç, proje kurallarını, geçmiş sohbetleri ve ilgili dokümanları analiz ederek, LLM'e gönderilecek olan sorguyu otomatik olarak zenginleştirir. Temel amacı, manuel bağlam sağlama yükünü ortadan kaldırarak geliştirme sürecini akıcı hale getirmektir.  
* **1.4. Hedef Kitle:** Cursor AI kullanarak kod geliştiren ve YZ asistanının hafıza sınırlamaları nedeniyle verimlilik kaybı yaşayan bireysel yazılım geliştiricileri.

### **2\. Stratejik Hedefler ve Amaçlar**

* **2.1. Kullanıcı Hedefleri:**  
  * **Bilişsel Yükü Azaltmak:** Geliştiriciyi, YZ'nin hafızasını yönetme görevinden kurtarmak.  
  * **Verimliliği Artırmak:** Manuel olarak bağlam arama ve ekleme (@ komutları) için harcanan zamanı ortadan kaldırmak.  
  * **Tutarlılığı Sağlamak:** Proje kurallarını ve standartlarını her sorguya otomatik olarak dahil ederek YZ çıktılarının kalitesini ve tutarlılığını artırmak.  
* **2.2. İş Hedefleri (v1.0 için):**  
  * **Problemi Doğrulamak:** YZ destekli kodlamada "kalıcı hafıza" eksikliğinin ne kadar kritik bir sorun olduğunu açık kaynak bir araçla kanıtlamak.  
  * **Topluluk Oluşturmak:** Proje etrafında, geri bildirim ve katkı sağlayan bir kullanıcı topluluğu oluşturmak.  
  * **Temel Oluşturmak:** Gelecekteki potansiyel bir "Pro" veya "Takım" sürümü için sağlam bir teknik temel ve konsept kanıtı (proof-of-concept) oluşturmak.

### **3\. Varsayımlar ve Bağımlılıklar**

* **3.1. Varsayımlar:**  
  * Kullanıcılar, Docker ve basit terminal betiklerini çalıştırabilecek teknik yeterliliğe sahiptir.  
  * Cursor'ın yerel veritabanı (SQLite) yapısı sık ve habersiz bir şekilde köklü değişikliklere uğramayacaktır.  
  * Geliştiriciler, // @collect-memory gibi yeni bir iş akışını benimsemeye açıktır.  
* **3.2. Bağımlılıklar:**  
  * **Yazılım:** Kullanıcının makinesinde Cursor ve Docker Desktop'ın kurulu olması gerekmektedir.  
  * **Platform:** Uygulama, Cursor'ın dosya ve veritabanı yapısına doğrudan bağımlıdır.

### **4\. Kapsam ve Özellikler**

* **4.1. Kapsam Dahilindeki Özellikler (v1.0):**  
  * **Özellik 1: Yorum Satırıyla Tetikleme**  
    * **Kullanıcı Hikayesi:** *Bir geliştirici olarak, kodumdan ayrılmadan basit bir yorum satırı ile bağlam toplama işlemini başlatmak istiyorum, böylece iş akışım kesintiye uğramaz.*  
  * **Özellik 2: Modüler Bağlam Toplama Motoru**  
    * **Kullanıcı Hikayesi:** *Bir geliştirici olarak, aracın proje kurallarını, geçmiş sohbetleri ve dokümanları otomatik olarak taramasını ve analiz etmesini istiyorum, böylece bu bilgileri manuel olarak aramak zorunda kalmam.*  
  * **Özellik 3: Kural Önceliklendirme**  
    * **Kullanıcı Hikayesi:** *Bir geliştirici olarak, aracın her zaman .cursor/rules içindeki kurallara öncelik vermesini istiyorum, böylece YZ'nin çıktıları projemin standartlarıyla her zaman tutarlı olur.*  
  * **Özellik 4: Yapılandırılmış Sorgu Oluşturma ve Panoya Kopyalama**  
    * **Kullanıcı Hikayesi:** *Bir geliştirici olarak, toplanan tüm bağlamın, YZ'nin anlayacağı yapılandırılmış bir formatta otomatik olarak panoya kopyalanmasını istiyorum, böylece tek yapmam gereken onu Cursor'a yapıştırmak olur.*  
* **4.2. Kapsam Dışı Olanlar (v1.0 için):**  
  * ❌ Takım özellikleri, paylaşılan hafıza ve bulut senkronizasyonu.  
  * ❌ Cursor arayüzüne gömülü bir grafik arayüz (GUI).  
  * ❌ Dosya sistemini anlık olarak izleyerek otomatik tetiklenme.  
  * ❌ Proje dosyalarına yazma veya kod değiştirme yetkisi.

### **5\. Kullanıcı Deneyimi ve Akışı (UX Flow)**

* **5.1. Kurulum Akışı:**  
  1. Kullanıcı, GitHub deposundan projeyi klonlar.  
  2. Terminalde setup.sh gibi basit bir kurulum betiği çalıştırır.  
  3. Betik, gerekli Docker imajını indirir ve collect-memory komutunu kullanıcının sistem yoluna (PATH) ekler.  
* **5.2. Günlük Kullanım Akışı:**  
  1. **Yazma:** Geliştirici, kod içine // @collect-memory: \[isteğim\] yorumunu ekler.  
  2. **Tetikleme:** Terminalden collect-memory komutunu çalıştırır.  
  3. **İşleme:** Arka planda Docker konteyneri çalışır, bağlamı toplar ve yapılandırılmış sorguyu hazırlar.  
  4. **Bildirim:** Terminalde ve/veya sistem bildirimiyle "✅ Sorgu panoya kopyalandı\!" mesajı gösterilir.  
  5. **Yapıştırma:** Geliştirici, sorguyu Cursor'a yapıştırır.  
* **5.3. Hata Yönetimi:**  
  * Cursor veritabanı bulunamazsa veya okunamıyorsa, kullanıcıya "Cursor veritabanı bulunamadı. Lütfen yolun doğru yapılandırıldığından emin olun." gibi açıklayıcı bir hata mesajı gösterilir.  
  * Tetikleyici komut bir proje klasörü içinde çalıştırılmazsa, kullanıcı uyarılır.

### **6\. Teknik Gereksinimler**

* **6.1. Teknoloji Yığını:**  
  * **Çekirdek Mantık:** Python (dosya okuma, SQLite erişimi, metin işleme için).  
  * **Konteynerleştirme:** Docker.  
  * **Tetikleyici:** Shell Script (Bash/Zsh uyumlu).  
* **6.2. Mimari:**  
  * Uygulama, PRD v1.1'de detaylandırıldığı gibi modüler bir yapıda (fetch\_\* fonksiyonları) ve geçici bir JSON veri yapısı kullanarak geliştirilecektir. Tüm mantık, yerel makinede çalışan bir Docker konteyneri içinde izole edilecektir.  
* **6.3. Performans:**  
  * Tetikleyici komutun çalıştırılmasından sorgunun panoya kopyalanmasına kadar geçen sürenin ortalama 3 saniyenin altında olması hedeflenmektedir.  
* **6.4. Güvenlik:**  
  * Uygulama, kullanıcının dosya sistemine yalnızca **salt okunur (read-only)** erişim talep edecektir.  
  * Hiçbir kullanıcı verisi, proje dosyası veya bağlam, harici bir sunucuya gönderilmeyecektir. Tüm işlemler yerel makinede gerçekleşir.

### **7\. Yayın Planı ve Kilometre Taşları**

* **Milestone 1 (Alpha \- İç Test):**  
  * Çekirdek fonksiyonlar tamamlandı: SQLite okuma, .rules ayrıştırma, temel sorgu birleştirme.  
  * Manuel olarak çalıştırılan Python betiği ile testler.  
* **Milestone 2 (Beta \- Kapalı Grup):**  
  * Docker konteyneri ve tetikleyici betik tamamlandı.  
  * Temel hata yönetimi eklendi.  
  * Seçilmiş bir grup geliştiriciye dağıtım ve geri bildirim toplama.  
* **Milestone 3 (v1.0 \- Herkese Açık):**  
  * GitHub'da projenin resmi olarak yayınlanması.  
  * Detaylı README.md dosyası, kurulum kılavuzu ve kullanım örnekleri.  
  * Docker Hub'da resmi imajın yayınlanması.

### **8\. Başarı Metrikleri**

* **8.1. Benimseme Metrikleri:**  
  * GitHub yıldız ve fork sayısı.  
  * Docker Hub'dan indirilen imaj sayısı.  
* **8.2. Etkileşim Metrikleri:**  
  * GitHub'da açılan "issue" ve "pull request" sayısı.  
  * Proje hakkında yazılan blog yazıları, yapılan sosyal medya paylaşımları.  
* **8.3. Kalitatif Metrikler:**  
  * Kullanıcılardan toplanan doğrudan geri bildirimler ve memnuniyet anketleri.

### **9\. Gelecek Çalışmalar ve Yol Haritası**

* **v1.1 Sonrası Fikirler:**  
  * **Git Entegrasyonu:** Bağlam kaynağı olarak git geçmişini (git log, git blame) kullanma.  
  * **Yapılandırma Dosyası:** Kullanıcının hangi kaynakların taranacağını (.collectivememoryrc gibi bir dosyayla) yönetmesine olanak tanıma.  
* **v2.0 ve Ötesi:**  
  * **Grafik Arayüz (GUI):** Kurulumu ve yapılandırmayı kolaylaştıran bir arayüz.  
  * **Gerçek Zamanlı İzleme:** Manuel tetikleyici yerine dosya sistemindeki değişiklikleri izleyerek otomatik bağlam güncelleme.  
* **Potansiyel "Pro" Sürüm:**  
  * Takımlar için paylaşılan ve senkronize edilen kolektif hafıza.  
  * Özel entegrasyonlar (Jira, Slack vb.).