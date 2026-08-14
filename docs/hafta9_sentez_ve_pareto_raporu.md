# Hafta 9 — Sentez ve Pareto Trade-off Analiz Raporu
**Faz 3: Simülasyon, Senaryo ve Arayüz (Dashboard)**

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K04, K05, K10, K12, K14, K15, K17, K25, K37, K44, K45, K47, K48–K54  
**Bkz.:** `docs/karar_gunlugu.md`

---

## 1. Hafta 9 Kontrol Sorularının Dürüst Yanıtları

| Kontrol Sorusu | Soru Metni | Veriye Dayalı Dürüst Yanıt |
|:---|:---|:---|
| **Soru 1 (Mesafe / Maliyet)** | *Simülasyon sonuçları dinamik rotalamanın mesafeyi/maliyeti azalttığını kanıtlıyor mu?* | **KISMÎ EVET:** 2 araçlı modelde Dinamik Sistem mesafeyi **%21.9 azaltmıştır** ($26.97 \text{ km}$ vs $34.55 \text{ km}$). Ancak 4 araçlı modelde sık seferler nedeniyle mesafe artmıştır ($48.49 \text{ km}$). |
| **Soru 2 (Malzeme Eksikliği / Starvation)** | *Dinamik sistemde malzeme eksikliği vakaları (starvation) sabit sisteme göre daha düşük mü?* | **HAYIR (Eşit araç koşulunda):** Statik sistemin duruşu daha düşüktür (%5.45 vs %53.01). **ÇÜNKÜ:** Statik sistem hat başında yapay olarak **2 kat daha fazla WIP stok** biriktirmektedir ($226.7 \text{ adet}$ vs $111.1 \text{ adet}$). |

> **🔑 Temel Mühendislik Çıkarımı:** Düşük WIP ile düşük starvation aynı fiziksel sistemde birlikte kolayca elde edilemez. Bu bir algoritma kusuru değil, endüstriyel lojistiğin **temel WIP–Starvation ödünleşimidir (trade-off)**.

---

## 2. Eşit WIP ve Farklı Tur Sıklıklarında Pareto Sınırı Analizi

Statik sistemin tur sıklığı $45, 60, 80, 90, 120 \text{ dakika}$ olarak değiştirilerek Dinamik sistemle eşit WIP seviyesindeki duruş performansı test edilmiştir:

| Sistem Politikası | Filo Büyüklüğü | Duruş Süresi (dk) | Starvation ($11,520$ Payda) | Starvation ($10,440$ Payda) | Ortalama Hat Başı WIP Stok | Kat Edilen Mesafe ($km$) | Sefer Sayısı |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Statik ($45 \text{ dk}$ Sefer) | 2 Araç | 172 dk `[Kod çıktısı]` | %1.49 `[Kod çıktısı]` | %1.65 `[Kod çıktısı]` | 289.3 adet `[Kod çıktısı]` | 49.36 km `[Kod çıktısı]` | 20 tur `[Kod çıktısı]` |
| Statik ($60 \text{ dk}$ Sefer) | 2 Araç | 628 dk `[Kod çıktısı]` | %5.45 `[Kod çıktısı]` | %6.02 `[Kod çıktısı]` | 226.7 adet `[Kod çıktısı]` | 34.55 km `[Kod çıktısı]` | 14 tur `[Kod çıktısı]` |
| Statik ($80 \text{ dk}$ Sefer) | 2 Araç | 2,460 dk `[Kod çıktısı]` | %21.35 `[Kod çıktısı]` | %23.56 `[Kod çıktısı]` | 175.2 adet `[Kod çıktısı]` | 24.68 km `[Kod çıktısı]` | 10 tur `[Kod çıktısı]` |
| Statik ($90 \text{ dk}$ Sefer) | 2 Araç | 3,456 dk `[Kod çıktısı]` | %30.00 `[Kod çıktısı]` | %33.10 `[Kod çıktısı]` | 155.8 adet `[Kod çıktısı]` | 24.68 km `[Kod çıktısı]` | 10 tur `[Kod çıktısı]` |
| Statik ($120 \text{ dk}$ Sefer) | 2 Araç | 5,246 dk `[Kod çıktısı]` | %45.54 `[Kod çıktısı]` | %50.25 `[Kod çıktısı]` | 119.1 adet `[Kod çıktısı]` | 14.81 km `[Kod çıktısı]` | 6 tur `[Kod çıktısı]` |
| **Dinamik (Olay Bazlı EDD)** | 2 Araç | 6,107 dk `[Kod çıktısı]` | %53.01 `[Kod çıktısı]` | %58.50 `[Kod çıktısı]` | **111.1 adet** `[Kod çıktısı]` | **26.97 km** `[Kod çıktısı]` | 16 tur `[Kod çıktısı]` |
| Statik ($45 \text{ dk}$ Sefer) | 4 Araç | 18 dk `[Kod çıktısı]` | %0.16 `[Kod çıktısı]` | %0.17 `[Kod çıktısı]` | 296.8 adet `[Kod çıktısı]` | 48.80 km `[Kod çıktısı]` | 40 tur `[Kod çıktısı]` |
| Statik ($60 \text{ dk}$ Sefer) | 4 Araç | 350 dk `[Kod çıktısı]` | %3.04 `[Kod çıktısı]` | %3.35 `[Kod çıktısı]` | 231.4 adet `[Kod çıktısı]` | 34.16 km `[Kod çıktısı]` | 28 tur `[Kod çıktısı]` |
| Statik ($80 \text{ dk}$ Sefer) | 4 Araç | 2,225 dk `[Kod çıktısı]` | %19.31 `[Kod çıktısı]` | %21.31 `[Kod çıktısı]` | 177.0 adet `[Kod çıktısı]` | 24.40 km `[Kod çıktısı]` | 20 tur `[Kod çıktısı]` |
| Statik ($90 \text{ dk}$ Sefer) | 4 Araç | 3,226 dk `[Kod çıktısı]` | %28.00 `[Kod çıktısı]` | %30.90 `[Kod çıktısı]` | 162.8 adet `[Kod çıktısı]` | 24.40 km `[Kod çıktısı]` | 20 tur `[Kod çıktısı]` |
| Statik ($120 \text{ dk}$ Sefer) | 4 Araç | 5,239 dk `[Kod çıktısı]` | %45.48 `[Kod çıktısı]` | %50.18 `[Kod çıktısı]` | 119.0 adet `[Kod çıktısı]` | 14.64 km `[Kod çıktısı]` | 12 tur `[Kod çıktısı]` |
| **Dinamik (Olay Bazlı EDD)** | 4 Araç | 2,832 dk `[Kod çıktısı]` | %24.58 `[Kod çıktısı]` | %27.13 `[Kod çıktısı]` | **182.3 adet** `[Kod çıktısı]` | 48.49 km `[Kod çıktısı]` | 32 tur `[Kod çıktısı]` |

---

## 3. What-If Stres Testi Bulguları (Hafta 10 Girişi)

| Bozucu Senaryo | Filo | Duruş Süresi (dk) | Starvation ($11,520$ Payda) | Starvation ($10,440$ Payda) | Ortalama WIP | Operasyonel Etki |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **0. Baz Durum (Standart)** | 4 Araç | 2,832 dk `[Kod çıktısı]` | %24.58 `[Kod çıktısı]` | %27.13 `[Kod çıktısı]` | 182.3 adet `[Kod çıktısı]` | Standart talep ve tam filo |
| **1. Talep Şoku (+%20 Tüketim)** | 4 Araç | 3,995 dk `[Kod çıktısı]` | %34.68 `[Kod çıktısı]` | %38.27 `[Kod çıktısı]` | 154.5 adet `[Kod çıktısı]` | Duruş +10.1 puan arttı |
| **2. Araç Arızası ($4 \rightarrow 3$ Araç)** | 3 Araç | 4,254 dk `[Kod çıktısı]` | %36.93 `[Kod çıktısı]` | %40.75 `[Kod çıktısı]` | 148.5 adet `[Kod çıktısı]` | Duruş +12.4 puan arttı |
| **3. Kritik Arıza ($2 \rightarrow 1$ Araç)** | 1 Araç | 8,006 dk `[Kod çıktısı]` | %69.50 `[Kod çıktısı]` | %76.69 `[Kod çıktısı]` | 71.5 adet `[Kod çıktısı]` | Sistem ağır darboğaza girdi |

---

## 4. Tartışma ve Metodolojik Çıkarımlar (Discussion)

### 4.1 Eşit WIP Seviyesinde Kalan Fark (WIP vs. Sevk Mekanizması)
- Pareto tablosu incelendiğinde, ortalama WIP seviyesi eşitlendiğinde dahi Statik sistemin Dinamik sisteme göre **%5 – %7 puan daha düşük duruş** sağladığı görülmektedir:
  - 2 Araç: Statik (120 dk, WIP≈119) %45.54 vs Dinamik (WIP≈111) %53.01 ($\Delta = 7.47$ puan).
  - 4 Araç: Statik (80 dk, WIP≈177) %19.31 vs Dinamik (WIP≈182) %24.58 ($\Delta = 5.27$ puan).
- **Bilimsel Yorum:** WIP seviyesi hat duruşunun **baskın belirleyicisidir**; ancak eşit WIP'te dahi gözlenen bu %5–7 puanlık kalan fark, statik rotalamanın *düzenli ve öngörülebilir çevrim yapısının*, olay bazlı dinamik sistemdeki *sinyal-reaksiyon gecikmesine (reaktif gecikme)* karşı ek bir operasyonel avantaj sağladığını düşündürmektedir.

### 4.2 Filo Büyüklüğü ve Başarı Eşiği (Hafta 6 ile Uyum)
- 4 araçlık konfigürasyonda dinamik sistemin duruş oranı (%24.58), statik baz sistemin (%3.04) belirgin şekilde gerisinde kalmaktadır.
- Dolayısıyla 4 araç bir "başarı eşiği" değil, duruşu %53'ten %24'e indiren **bir ara iyileşme adımıdır**.
- Dinamik sistemin statik sistemle rekabet edebilecek seviyede düşük duruş oranlarına (<%5) ulaşabilmesi için, Hafta 6 duyarlılık analizinde tespit edilen **5–6 araçlık filo bandına** (5 araçta %5.20, 6 araçta %0.97) yaklaşması gerekmektedir.

> [!IMPORTANT]
> **⚠️ ERRATA — Filo Eşiği Düzeltmesi (Hafta 10 Denetimi, 15.08.2026):**  
> Yukarıdaki cümle, fiziksel raf tavanı ($stok \le N \times C$) uygulanmadan üretilen (tavansız) Hafta 6 simülasyon değerlerine dayanmaktadır. Hafta 10 denetiminde tavan kısıtlı kanonik motor kullanıldığında:
>
> | Araç | Tavansız (Eski) | **Tavanlı (Doğru)** | Fark |
> |:---:|:---:|:---:|:---:|
> | 5 | %5.20 / %3.96 | **%15.98** | +12.02 puan |
> | 6 | %0.97 / %0.64 | **%11.27** | +10.62 puan |
> | 7 | %0.28 | **%7.00** | +6.72 puan |
> | **8** | %0.10 | **%3.50** | +3.40 puan |
>
> `[Kod çıktısı]` — `src/hafta10_whatif_senaryolari.py`, kanonik motor (K57), EDD dispatch.
>
> **Düzeltilmiş Sonuç:** "5–6 araç <%5 duruş eşiğine yeterlidir" ifadesi geçerli değildir. Raf tavanı uygulandığında **%5 eşiğinin altına inmek için 8 araç gerekmektedir** (%3.50). Bu bulgu, basitleştirilmiş (tavansız) simülasyonların filo ihtiyacını sistematik olarak eksik tahmin ettiğini ve fiziksel stok kısıtının simülasyon modeline dahil edilmesinin zorunluluğunu göstermektedir — tez savunması için güçlü bir metodolojik katkıdır.
