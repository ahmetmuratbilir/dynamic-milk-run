# Hafta 2 — Tüketim ve Stok Verileri Analiz Raporu

**Aktif Veri Kaynağı:** `synthetic`
**Tarih:** 2026-07-29

---

## 1. Genel İstatistikler

- **Toplam Simülasyon Süresi:** 480 dakika (8 saat / 1 vardiya)
- **Toplam İstasyon Sayısı:** 24 istasyon (4 hat × 6 istasyon)
- **Toplam Fabrika Tüketimi (8 saat):** 3268.8 adet
- **Ortalama Fabrika Tüketim Hızı:** 408.6 adet/saat

## 2. Hat Bazlı Tüketim Dağılımı

| Hat | İstasyon Sayısı | Toplam Tüketim (Adet) | Ortalama/İstasyon |
|-----|-----------------|------------------------|-------------------|
| Hat-1 | 6 | 828.9 | 138.1 |
| Hat-2 | 6 | 748.4 | 124.7 |
| Hat-3 | 6 | 893.3 | 148.9 |
| Hat-4 | 6 | 798.1 | 133.0 |

## 3. İstasyon Detay Tablosu ve Kanban Sayıları

| İstasyon | Hat | Hedef Tüketim (ad/sa) | Gerçekleşen (ad/sa) | Toplam Tüketim | Kutu Kapasitesi (C) | Hesaplanan Kanban (N) |
|----------|-----|-----------------------|---------------------|----------------|---------------------|-----------------------|
| S1 | Hat-1 | 22 | 21.87 | 175.0 | 20 | 1 |
| S2 | Hat-1 | 18 | 17.68 | 141.5 | 20 | 1 |
| S3 | Hat-1 | 15 | 14.95 | 119.6 | 15 | 1 |
| S4 | Hat-1 | 20 | 19.95 | 159.6 | 20 | 1 |
| S5 | Hat-1 | 12 | 11.96 | 95.7 | 15 | 1 |
| S6 | Hat-1 | 17 | 17.19 | 137.5 | 20 | 1 |
| S7 | Hat-2 | 21 | 20.79 | 166.3 | 20 | 1 |
| S8 | Hat-2 | 13 | 13.03 | 104.2 | 15 | 1 |
| S9 | Hat-2 | 19 | 18.96 | 151.7 | 20 | 1 |
| S10 | Hat-2 | 11 | 10.93 | 87.4 | 15 | 1 |
| S11 | Hat-2 | 16 | 15.79 | 126.3 | 20 | 1 |
| S12 | Hat-2 | 14 | 14.05 | 112.4 | 15 | 1 |
| S13 | Hat-3 | 23 | 23.45 | 187.6 | 20 | 1 |
| S14 | Hat-3 | 18 | 18.1 | 144.8 | 20 | 1 |
| S15 | Hat-3 | 15 | 15.05 | 120.4 | 15 | 1 |
| S16 | Hat-3 | 24 | 24.01 | 192.1 | 20 | 2 |
| S17 | Hat-3 | 17 | 17.01 | 136.1 | 20 | 1 |
| S18 | Hat-3 | 14 | 14.05 | 112.4 | 15 | 1 |
| S19 | Hat-4 | 20 | 19.91 | 159.3 | 20 | 1 |
| S20 | Hat-4 | 16 | 16.12 | 128.9 | 20 | 1 |
| S21 | Hat-4 | 13 | 13.05 | 104.4 | 15 | 1 |
| S22 | Hat-4 | 18 | 17.69 | 141.5 | 20 | 1 |
| S23 | Hat-4 | 12 | 11.9 | 95.2 | 15 | 1 |
| S24 | Hat-4 | 21 | 21.1 | 168.8 | 20 | 1 |

## 4. Değerlendirme ve Sonraki Adımlar

1. Sentetik tüketim verisi `Normal(μ, 0.20μ)` stokastik dağılımına uygun şekilde üretilmiştir.
2. Kanban kart sayıları $N = \lceil (D \times LT \times (1+\alpha)) / C \rceil$ formülüyle hesaplanmıştır.
3. Veri soyutlama katmanı (`DataLoader`) kurulmuştur. İleride gerçek fabrika verisi geldiğinde sadece `data/config.json` dosyasında `"data_source": "real"` yapılması yeterli olacaktır.
