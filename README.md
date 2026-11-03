# Dinamik Milk-Run ve E-Kanban Karar Destek Sistemi

Fabrika içi malzeme beslemede **hat duruşunu (starvation)** ve **hat yanı stoku (WIP)**
eş zamanlı yönetmek için E-Kanban sinyal üretimi ile zaman pencereli araç rotalamasını
(VRPTW) tek bir simülasyon motorunda birleştiren karar destek sistemi.

Endüstri Mühendisliği tasarım çalışması · Sentetik veri · Python 3.11

---

## Hızlı başlangıç

```bash
python -m pip install -r requirements.txt

# Tüm analizleri yeniden üret (~15-30 dk)
python -X utf8 -m src.tum_analizleri_calistir

# Hızlı koşu (~5 dk)
python -X utf8 -m src.tum_analizleri_calistir --hizli
```

Çıktılar: `data/synthetic/v2_*.csv` ve `docs/figurler/*.png`.
Yorumları: `docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md`.

> **Windows notu.** Konsol varsayılan olarak cp1254 kullanır; Türkçe karakterler için
> betikleri `python -X utf8 -m ...` biçiminde çalıştırın.

---

## Sistem

| Öğe | Değer | Karar |
|---|---|---|
| Fabrika | 4 hat, 24 istasyon, 1 depo | K01, K02 |
| Araç | 25 kutu, 10 km/sa | K04, K12 |
| Lead time / güvenlik katsayısı | 45 dk / α = 0,15 | K07, K08 |
| Kutu kapasitesi | 15 veya 20 adet | K09 |
| Vardiya / ısınma | 480 dk / **90 dk** | K05, **K78** |
| Kanban | $N = 1 + \lceil D \cdot LT (1+\alpha) / C \rceil$ | **K65** |

Her parametrenin kaynağı ve gerekçesi: **`docs/karar_gunlugu.md`** (K01–K105).

**Makale tabloları (nihai ayar: koordinat ağı, 1440 dk, ısınma sonrası):** `docs/makale_tablolari.md` — üretim: `python -X utf8 -m src.v2_makale_tablolari` (≈4 dk, K105).
**Proje rehberi (eksikler, kritik sorular, belge sırası, ekranlar):** `docs/proje_rehberi.html`.

### Politikalar

| | Tanım | Dayanak |
|---|---|---|
| **P1** | Sabit takt, sabit miktar (her istasyona 1 kutu) | Klenk vd. 2012 s.6 |
| **P2** | Sabit takt, Kanban miktarı (1:1 boş kutu değişimi) | Simić 2020 s.10–11; Vojdani 2022 s.6 |
| **P3** | Olay tabanlı dinamik sevk (anında / konsolidasyonlu) | Facchini 2022 s.1123 |

---

## İki simülasyon motoru

Proje **iki motor** içerir. Bu ayrım bilinçlidir:

| | `v1` (Hafta 4–13) | `v2` (Hafta 14+) |
|---|---|---|
| Dosyalar | `ekanban_signal.py`, `vrptw_solver.py`, `hafta8_kanban_karsilastirma.py`, `variable_lt_solver.py` | `v2_entegre_simulasyon.py` |
| Yapı | Sinyaller önceden üretilir, rotalama hazır listeyi okur (açık döngü) | Tek olay döngüsü, sinyaller gerçek stoktan (kapalı döngü) |
| Durum | **Değiştirilmedi** — H4–H13 raporlarındaki sayıları üretir | Güncel; literatür denetimi düzeltmelerini içerir |

v1 **kasıtlı olarak korunmuştur**: yayımlanmış haftalık raporların sayıları yeniden
üretilebilir kalsın diye. Yeni analizler v2 ile yapılmalıdır.

**v2'de giderilen üç yapısal sorun** (ölçülen etkileriyle):

1. **Raf eksik boyutlandırılmıştı** — 24 istasyonun 23'ünde $N=1$; VDI 5586'nın zorunlu
   kıldığı "+1 değişim pozisyonu" (Urru vd. 2018 s.406) yoktu → **−3,88 puan duruş**
2. **Hizmet süresi asimetrisi** — statik 3 dk/durak, dinamik 8 dk/durak → **−10,34 puan**
3. **Açık döngü** — sinyaller LT=45 dk varsayımıyla önceden üretiliyordu → **%24,58 → %6,85**

Ayrıntı ve düzeltmelerin tek tek ayrıştırılması:
`docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md`, Bölüm 4.1.

---

## Depo düzeni

```
src/
  v2_entegre_simulasyon.py        Kanonik motor (v2) — P1/P2/P3, VRP-RTW, 2-opt
  v2_dogrulama_ve_kalibrasyon.py  Tur-içi optimallik, Welch ısınma, replikasyon, ayrıştırma
  v2_pareto_ve_figurler.py        Politika ızgarası, Pareto cephesi, makale figürleri
  v2_deney_tasarimi.py            2^5 faktöriyel, ANOVA, Tukey HSD
  v2_boyutlandirma_duyarliligi.py Vojdani tasarımı ↔ politika-tutarlı tampon (K93)
  v2_toyota_bandi_duyarliligi.py  Toyota α ve kutu bandında sağlamlık (K95)
  v2_adalet_kurallari.py          Dört eşitleme kuralı (K97; --kutu toyota)
  v2_uyarlanan_rop.py             Uyarlanan ROP (K98)
  v2_cok_vardiya.py               480/1440 dk, ısınma dahil/hariç (K99)
  v2_koordinat_agi.py             Koordinat tabanlı mesafe ağı (K100)
  v2_ortools_referansi.py         Çevrimdışı tam bilgi rotalama referansı (K101)
  v2_makale_tablolari.py          Nihai ayarla makale tabloları (K105)
  generate_dashboard_data_v2.py   Dashboard veri ambarı (K94, K102)
  solomon_dogrulama.py            Solomon VRPTW kıyaslaması (OR-Tools referanslı)
  tum_analizleri_calistir.py      Hepsini sırayla çalıştırır
  kaynak_arsivi_denetimi.py       Kaynak arşivi bütünlük denetimi (zip/kopya/eksik)
  generate_synthetic_data.py      Sentetik veri üretici (seed=42)
  data_loader.py                  Veri soyutlama katmanı (synthetic ↔ real)
  ekanban_signal.py …             v1 motoru ve haftalık analiz betikleri
data/
  config.json                     "synthetic" | "real" anahtarı
  synthetic/                      Üretilmiş veri ve tüm analiz çıktıları
  real/                           Gerçek veri şablonu (boş; yalnızca başlık satırları)
docs/
  karar_gunlugu.md                K01–K105: her kararın kaynağı ve gerekçesi
  makale_tablolari.md             ← makaleye girecek tablolar (K105)
  literatur_boslugu_analizi.md    Boşluk, katkılar, hazır cümleler, hakem cevapları
  proje_rehberi.html              Eksikler, kritik sorular, belge sırası, ekran rehberi
  hafta14_literatur_denetimi_ve_revizyon_raporu.md    ← güncel sonuçlar
  tez_bilgi_rehberi.md            Akademik master doküman (IMRaD)
  hafta1..10_*.md                 Haftalık raporlar (errata notlarıyla)
  figurler/                       Makale figürleri (200 dpi PNG)
  papers/                         Literatür kataloğu ve çıkarılmış metinler
dashboard.html, app.js, style.css Karar destek arayüzü: Özet, What-If, İstasyon,
                                  Politikalar & Ana Katkı, Doğrulama, Veri Girişi
```

> ⚠️ **Telif uyarısı.** `docs/papers/zip*/` altındaki makale PDF'leri telif hakkı
> korumalıdır ve kopyalı biçimde depoda tutulmaktadır. Depo herkese açılacaksa bu
> klasörler çıkarılmalı, yalnızca `docs/master_makale_katalogu.md` bırakılmalıdır.

---

## Gerçek veriye geçiş

`data/config.json` içindeki `data_source` değerini `"real"` yapın ve `data/real/`
altındaki altı CSV'yi doldurun (başlık satırları hazırdır). Kodun geri kalanında
değişiklik gerekmez — tüm okuma `src/data_loader.py` üzerinden yapılır.

---

## Doğrulama durumu

| Doğrulama | Sonuç |
|---|---|
| Solomon VRPTW (6 örnek × 2 boyut) | En yakın komşu, OR-Tools'tan **%102,7** daha uzun |
| Fabrika içi tur-içi optimallik (400 küme, tam numaralama) | NN+2opt sapması **%0,62** |
| Isınma süresi (Welch, 20 replikasyon) | **90 dk** (45 dk'da WIP kararlının %54 üzerinde) |
| Replikasyon yeterliliği | Mutlak ölçütle (±0,05 puan) **n = 9** |
| Sevk kuralları (ANOVA + Tukey) | Dört kural **eşdeğer** (p = 0,9997 / 0,3415) |

| Sağlamlık (K95, K99, K100) | Boyutlandırma kayması 52/52 koşulda pozitif |
| Rotalama, fabrika senaryosu (K101) | Çevrimdışı tam bilgi referansı daha kısa yol, daha çok gecikme |

**Bilinen sınırlılıklar:** sentetik veri; tek fabrika düzeni ve hatlar arası mesafe
varsayımı (K100); tur-arası atama optimize edilmiyor (K101); motor varsayılanları
ısınma dahil gösterge ve eski mesafe matrisiyle çalışır — makale sayıları nihai ayarla
üretilir (K99, K105). Tam liste: `docs/proje_rehberi.html` S11.
