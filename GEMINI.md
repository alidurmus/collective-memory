# 🧠 GEMINI.md - Collective Memory Projesi Rehberi

Bu dosya, Gemini yapay zeka asistanının Collective Memory projesinde tutarlı ve verimli bir şekilde çalışması için gerekli olan temel kuralları, standartları ve mevcut durumu özetlemektedir.

---

## 🚨 **KRİTİK UYARI: SİSTEM ÇALIŞMIYOR** 🚨

**Mevcut Durum:** Proje şu anda 3 kritik hata nedeniyle **çalışmıyor**. Ana hedefim, başka bir göreve geçmeden önce bu hataları çözmektir.

1.  **❌ Backend API Hatası:** `ModuleNotFoundError: No module named 'query_engine'`
2.  **❌ Frontend Sunucu Hatası:** `ENOENT: no such file or directory, open 'package.json'`
3.  **❌ Enterprise Modül Hatası:** `ModuleNotFoundError: No module named 'enterprise_features'`

Bu hatalar çözülene kadar sistemin hiçbir bileşeninin (API, Frontend, Arama) çalışır durumda olduğunu varsaymamalıyım.

---

## 📜 **Temel Proje Kuralları (Altın Kurallar)**

Bu kurallar projedeki tüm çalışmalarım için geçerlidir ve her zaman önceliklidir.

1.  **Dil Standardı: Türkçe UI / İngilizce Kod [[memory:2176195]]**
    *   **Kullanıcı Arayüzü (UI):** Tüm metinler, etiketler, butonlar ve kullanıcıya dönük dokümantasyon **Türkçe** olmalıdır.
    *   **Kod ve Teknik Alanlar:** Tüm değişkenler, fonksiyon adları, sınıf adları, API endpoint'leri ve commit mesajları **İngilizce** olmalıdır.
    *   **Yorumlar:** Kod içi yorumlar, kullanıcıya yönelik açıklamalar için **Türkçe** olabilir.

2.  **Frontend Framework: Context7 [[memory:592593]]**
    *   Tüm frontend geliştirmeleri, projenin özel **Context7** framework'üne uygun olmalıdır.
    *   Bu, **glassmorphism** tasarım dilini, belirlenmiş renk paletini ve component yapılarını kullanmayı içerir.

3.  **Test Standardı: Playwright Zorunluluğu [[memory:592592]]**
    *   Tüm UI ve E2E (uçtan uca) testler **Playwright** kullanılarak yazılmalıdır.
    *   Backend testleri için **pytest** kullanılmalıdır.
    *   Test kapsamı (coverage) %80'in üzerinde tutulmalıdır.

4.  **Hafıza Odaklı Geliştirme [[memory:3235989]]**
    *   Her talimat öncesinde, konuyla ilgili hafıza kayıtlarımı (`[[memory:xxxx]]`) kontrol etmeliyim.
    *   Projenin kurallarını (`.cursor/rules/`) okumalı ve uygulamalıyım.
    *   Geliştirmelerimi bu hafıza ve kurallar çerçevesinde yapmalıyım.

---

## 🔄 **İş Akışı (Workflow) [[memory:3190909]]**

Tüm görevleri aşağıdaki adımları izleyerek gerçekleştireceğim:

1.  **Analiz:** Talebi anlamsal parçalara ayırırım.
2.  **Bilgi Toplama:** `search_file_content`, `read_file`, `list_directory` gibi araçlarla proje hakkında bağlam toplarım.
3.  **Pattern Uygulama:** Projenin mevcut kodlama desenlerini ve en iyi pratikleri uygularım.
4.  **Uygulama:** Kodu yazar veya değiştiririm. Mümkün olan işlemleri paralel yürütürüm.
5.  **Test:** Yaptığım değişiklikleri `pytest` ve `Playwright` ile test ederim.
6.  **Optimizasyon:** Performans ve hata yönetimi kurallarını uygularım.
7.  **Raporlama:** Yaptığım işlemler hakkında net ve kısa bir rapor sunarım.

---

## 💻 **Teknoloji Yığını Özeti**

-   **Backend:** Python, Django, Flask, SQLite
-   **Frontend:** React, TypeScript, Vite, Context7 Framework
-   **Test:** Pytest (Backend), Playwright (Frontend)
-   **Paket Yönetimi:** `pip` ve `requirements.txt` (Python), `npm` ve `package.json` (Node.js)
-   **CI/CD:** Docker, GitHub Actions

---

## 📁 **Önemli Dizinler**

-   `collective-memory-app/`: Ana uygulamanın bulunduğu yer. Tüm komutlar bu dizin içinden çalıştırılmalıdır.
-   `.cursor/rules/`: Benim için tanımlanmış, uyulması zorunlu kuralları içerir.
-   `docs/`: Projenin genel dokümantasyonu, raporları ve rehberleri.
-   `data/`: **Sadece** demo ve test amaçlı verileri içerir. Gerçek proje verisi değildir.
