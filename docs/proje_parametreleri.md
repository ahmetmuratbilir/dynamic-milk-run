# Proje Parametreleri Şablonu
## Dinamik Milk-Run & E-Kanban Karar Destek Sistemi

> **Durum:** Sentetik veri kullanılıyor.
> Aşağıdaki değerler önerilen başlangıç değerleridir — senin onayınla kesinleşecek.
> Onayladıktan sonra bu tablo tüm hesaplamaların referansı olacak.

---

## Bölüm A — Sistem Yapısı

| Parametre | Açıklama | Önerilen Değer | Senin Onayın |
|-----------|----------|----------------|--------------|
| Hat sayısı | Sisteme dahil üretim hattı | 3 hat | [ ] |
| İstasyon sayısı | Toplam hat yanı durak (node) | 6 istasyon | [ ] |
| Depo sayısı | Başlangıç ve bitiş noktası | 1 merkezi depo | [ ] |
| Araç sayısı | Milk-run aracı | 2 araç | [ ] |
| Araç kapasitesi (Q) | Her araç için maksimum taşıma kapasitesi | 20 kutu | [ ] |
| Simülasyon süresi | Toplam simülasyon uzunluğu | 480 dk (1 vardiya) | [ ] |

---

## Bölüm B — Dinamik Kanban Parametreleri

Formül: **N = ⌈ (D × LT × (1+α)) / C ⌉**

| Parametre | Sembol | Açıklama | Önerilen Değer (Sentetik) | Senin Onayın |
|-----------|--------|----------|--------------------------|--------------|
| Tüketim hızı | D | Birim zamanda tüketilen parça sayısı | Parçaya göre 5–20 adet/saat | [ ] |
| Tedarik süresi | LT | Sipariş verilmesinden teslimata kadar geçen süre | 0.5–1.0 saat | [ ] |
| Güvenlik payı | α | Talep dalgalanmasına karşı tampon | 0.15 (yani %15) | [ ] |
| Kutu kapasitesi | C | Standart kutudaki parça adedi | 10 adet/kutu | [ ] |
| Dinamik güncelleme periyodu | T_update | D'nin kaç dakikada bir yeniden hesaplandığı | 60 dk (saatlik) | [ ] |

---

## Bölüm C — Zaman Penceresi (VRPTW) Parametreleri

| Parametre | Açıklama | Önerilen Değer (Sentetik) | Senin Onayın |
|-----------|----------|--------------------------|--------------|
| Erken teslimat sınırı (a_i) | En erken kabul edilebilir teslimat anı | Sipariş anından 0 dk sonra | [ ] |
| Geç teslimat sınırı (b_i) | En geç kabul edilebilir teslimat anı | Sipariş anından 60 dk sonra | [ ] |
| Handling süresi | İstasyon başına yükleme/boşaltma süresi | 5 dk/istasyon | [ ] |
| Ortalama istasyonlar arası mesafe | | 200 m (fabrika içi) | [ ] |
| Ortalama seyahat hızı | | 10 km/saat (forklift/transpalet) | [ ] |

---

## Bölüm D — Simülasyon Parametreleri

| Parametre | Açıklama | Önerilen Değer | Senin Onayın |
|-----------|----------|----------------|--------------|
| Tüketim hızı dağılımı | Stokastik mi, deterministik mi? | Normal dağılım (μ=D, σ=0.2D) | [ ] |
| Başlangıç stok seviyesi | Simülasyon başında her istasyondaki stok | N × C (dolu başla) | [ ] |
| Reorder point (ROP) | Sinyal tetikleme eşiği | 1 kutu kaldığında | [ ] |

---

## Onay Talimatı

Bu tabloyu inceledikten sonra:
- Katıldığın satırlar için [x] işaretle (veya "hepsi tamam" de)
- Değiştirmek istediğin varsa yeni değeri söyle
- Emin olmadığın varsa sordur — birlikte karar verelim

> ⚠️ Bu değerler onaylanmadan Hafta 3'te Kanban hesabı yapılamaz.
> Onay beklenecek, kendi başıma kesinleştirmeyeceğim.

---

*Hazırlayan: AI | Durum: ONAY BEKLENİYOR | Güncelleme: Hafta 1*
