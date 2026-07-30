# Hafta 5 — VRPTW Rotalama ve Gerçek Starvation Analiz Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K04, K17, K33, K34, K35, K36 — bkz. `karar_gunlugu.md`

---

## 1. 182 Sinyalin Tam Taksonomisi

| Teslimat Durumu | Sinyal Sayısı | Oran (%) | Açıklama |
|-----------------|---------------|----------|----------|
| Zamanında Teslim | 17 | %9.3 | Varış dk ≤ TW_bitis (TW İhlali Yok) |
| Gecikmeli Teslim | 55 | %30.2 | Varış dk > TW_bitis (TW İhlali Var) |
| Karşılanamayan | 110 | %60.4 | 480 dk vardiyada araç zamanı yetmedi |
| **Toplam** | **182** | **%100** | |

## 2. 🚨 Darboğaz ve Kök Neden Analizi (K36)

- **Kutu Kapasitesi Kullanımı:** Ortalama **4.62 kutu/tur** (Kapasite: 25 kutu, Doluluk: **%18.5**)
- **Kök Neden Tespiti:** Kutu kapasitesi ($Q_{arac}$) **darboğaz DEĞİLDİR**. Asıl kısıt **ZAMAN ve ARAÇ SAYISI** kısıtıdır (2 araç × 480 dk = 960 araç-dk, max 16 tur).

## 3. Gerçek Starvation (Stoksuz Kalma) Analizi ve İstasyon Dağılımı

- **Toplam Operasyon Süresi:** 11520 istasyon-dakikası (24 istasyon × 480 dk)
- **Gerçekleşen Starvation:** 6000 istasyon-dakikası
- **Fabrika Genel Durma Oranı:** **%52.08**

### İstasyon Bazlı Durma Dağılımı Tablosu:

| istasyon_id   |   starvation_dk |   durma_% |
|:--------------|----------------:|----------:|
| S11           |             393 |      81.9 |
| S14           |             388 |      80.8 |
| S22           |             347 |      72.3 |
| S7            |             308 |      64.2 |
| S9            |             290 |      60.4 |
| S2            |             285 |      59.4 |
| S21           |             276 |      57.5 |
| S8            |             274 |      57.1 |
| S1            |             264 |      55   |
| S24           |             259 |      54   |
| S20           |             259 |      54   |
| S23           |             255 |      53.1 |
| S5            |             254 |      52.9 |
| S19           |             246 |      51.2 |
| S4            |             245 |      51   |
| S3            |             243 |      50.6 |
| S16           |             236 |      49.2 |
| S12           |             219 |      45.6 |
| S18           |             205 |      42.7 |
| S17           |             198 |      41.2 |
| S10           |             152 |      31.7 |
| S15           |             149 |      31   |
| S6            |             145 |      30.2 |
| S13           |             110 |      22.9 |

*Not: S16 yüksek tüketimine ($D=24$) rağmen $N=2$ (40 kutu tampon stok) sayesinde durma oranını %49.2'de tutabilmiştir. S11 (%81.9) ve S14 (%80.8) $N=1$ ile başladıklarından daha fazla durma yaşamışlardır.*
