# Hafta 5 — VRPTW Rotalama ve Gerçek Starvation Analiz Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K04, K17, K33, K34, K35, K36 — bkz. `karar_gunlugu.md`

---

## 1. 182 Sinyalin Tam Taksonomisi

| Teslimat Durumu | Sinyal Sayısı | Oran (%) | Açıklama |
|-----------------|---------------|----------|----------|
| Zamanında Teslim | 17 | %9.3 | Varış dk ≤ TW_bitis (TW İhlali Yok) |
| Gecikmeli Teslim | 55 | %30.2 | Varış dk > TW_bitis (TW İhlali Var) |
| Karşılanamayan | 110 | %60.4 | 480 dk vardiya süresinde araç zamanı yetmedi |
| **Toplam** | **182** | **%100** | |

## 2. 🚨 Darboğaz ve Kök Neden Analizi (Düzeltilmiş - K36)

- **Kutu Kapasitesi Kullanımı:** Ortalama **4.62 kutu/tur** (Kapasite: 25 kutu, Doluluk: **%18.5**)
- **Kök Neden Tespiti:** Kutu kapasitesi ($Q_{arac}$) **darboğaz DEĞİLDİR**. Asıl kısıt **ZAMAN ve ARAÇ SAYISI** kısıtıdır (2 araç × 480 dk = 960 araç-dk, max 16 tur).

## 3. Gerçek Starvation (Stoksuz Kalma) Analizi

Araçların gerçek varış zamanlarına göre dakika dakika stok takibi yapıldığında **toplam 6000 olay (dakika/istasyon)** starvation tespit edilmiştir.

