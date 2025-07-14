# Context7 ERP – Template Naming Conventions

_Last updated: 18 Haziran 2025_

Bu doküman, `templates/erp/` altındaki tüm modül-özel HTML şablonları için standart isimlendirme kurallarını tanımlar. Amaç; tutarlı, okunabilir ve kolay bulunabilir bir dizin yapısı sağlamaktır.

## 🍱 Dizin Yapısı

```
templates/
└── erp/
    ├── products/
    │   ├── list.html          # Kayıt listesi
    │   ├── form.html          # Oluştur / Güncelle formu
    │   ├── detail.html        # Detay sayfası
    │   └── confirm_delete.html# Silme onayı (opsiyonel)
    ├── customers/
    │   ├── list.html
    │   ├── form.html
    │   ├── detail.html
    │   └── confirm_delete.html
    ├── suppliers/
    │   ├── list.html
    │   ├── form.html
    │   ├── detail.html
    │   └── confirm_delete.html
    └── ... (diğer modüller aynı düzeni izler)
```

## 📜 Dosya Adları

| Tür             | Dosya Adı         | Açıklama                                   |
|-----------------|-------------------|--------------------------------------------|
| Liste sayfası   | `list.html`       | Çoğul veri listesi (örn. ürün listesi)     |
| Form sayfası    | `form.html`       | Oluşturma / güncelleme formları            |
| Detay sayfası   | `detail.html`     | Tekil kaydın ayrıntılı görünümü            |
| Sil onay sayfası| `confirm_delete.html` | Silme işlemi öncesi onay diyaloğu     |

> **Not:** Özel alt işlemler (ör. `bom_manage.html`, `stock_movement.html`) modül klasöründe ek dosya olarak bırakılabilir, ancak çekirdek CRUD sayfaları yukarıdaki standart ismi kullanmalıdır.

## 🛠️ View Kullanımı

View'larda şablon yolu şu şablonu izler:

```python
return render(request, 'erp/<modül>/<dosya>.html', context)
```

Örneğin ürün listesi:

```python
return render(request, 'erp/products/list.html', {'products': products})
```

## ✅ Geçiş Durumu

* 18 Haziran 2025 itibarıyla `products`, `customers`, `materials` klasörleri yeni standardı kullanacak şekilde güncellenmiştir.
* Eski dosya adları (`product_list.html` vb.) depo içinde tutulmamalıdır; gereksiz olanlar kaldırılacaktır.

---

Daha fazla bilgi için _Design System Guidelines_ ve _Code Quality Rules_ belgelerine bakınız. 