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

Her parametrenin kaynağı ve gerekçesi: **`docs/karar_gunlugu.md`** (K01–K82).

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
  karar_gunlugu.md                K01–K82: her kararın kaynağı ve gerekçesi
  hafta14_literatur_denetimi_ve_revizyon_raporu.md    ← güncel sonuçlar
  tez_bilgi_rehberi.md            Akademik master doküman (IMRaD)
  hafta1..10_*.md                 Haftalık raporlar (errata notlarıyla)
  figurler/                       Makale figürleri (200 dpi PNG)
  papers/                         Literatür kataloğu ve çıkarılmış metinler
dashboard.html, app.js, style.css Karar destek arayüzü (1920 senaryo gömülü)
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

**Bilinen sınırlılıklar:** sentetik veri; tek vardiya (ısınma sonrası etkin pencere
390 dk); tur-arası atama optimize edilmiyor; mesafe matrisi koordinatlardan
üretilmiyor (Floyd–Warshall geçici çözümü). Tam liste: revizyon raporu Bölüm 9.
