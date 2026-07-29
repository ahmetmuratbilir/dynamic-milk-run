# Hafta 2 Özeti
## Dinamik Milk-Run & E-Kanban Karar Destek Sistemi

**Dönem:** Hafta 2 — Hat İçi Tüketim ve Stok Verilerinin Analizi
**Durum:** ⏳ Kontrol Onayı Bekliyor (29.07.2026)

---

## Bu Hafta Ne Yaptık? (Teknik Olmayan Dil)

1. **Veri Soyutlama Katmanı Kuruldu (`config.json` + `DataLoader`):**
   - Sistem mimarisine `data/config.json` yapılandırma dosyası ve Python `DataLoader` sınıfı eklendi.
   - Şu an `"data_source": "synthetic"` aktif. İleride gerçek fabrika verisi geldiğinde sadece config dosyasındaki değeri `"real"` yapmak yeterli olacak, hiçbir kod değişmeyecek.

2. **Sentetik Veri Seti Üretildi (Onaylı Referans Verilerine Göre):**
   - `referans_veri.md` içerisindeki onaylanan parametrelere tam sadık kalınarak 480 dakikalık (1 vardiya / 8 saat) stokastik tüketim verisi üretildi.
   - `stations.csv`: 24 istasyonun (4 hat × 6 istasyon) hedef tüketim hızları, kutu kapasiteleri ($C$) ve hesaplanan Kanban kart sayıları ($N$).
   - `consumption.csv`: 480 dakika × 24 istasyon = 11.520 satırlık dakikalık stokastik `Normal(μ, 0.20μ)` tüketim matrisi.
   - `inventory.csv`: İstasyonların başlangıç stok ve Reorder Point (ROP) ayarları.
   - `vehicles.csv`: 2 adet Milk-Run aracının kapasite (25 kutu), hız (10 km/sa = 166.67 m/dk) ve handling (5 dk/istasyon) parametreleri.
   - `distances.csv`: Depo (Node 0) ve 24 istasyon arasındaki 600 node çiftinin mesafe (metre) ve seyahat süreleri (dakika).
   - `production_plan.csv`: 8 saatlik hat bazlı üretim programı.

3. **İstatistiksel Veri Analizi Gerçekleştirildi:**
   - Toplam fabrika tüketimi 8 saatte **3.268,8 adet** (saatte ortalama **408,6 adet**) olarak hesaplandı.
   - Hat bazlı tüketim dağılımı: Hat-1 (828.9 adet), Hat-2 (748.4 adet), Hat-3 (893.3 adet), Hat-4 (798.1 adet).
   - Kanban formülüne $N = \lceil (D \times LT \times (1+\alpha)) / C \rceil$ göre $N$ değerleri doğrulandı.

---

## Üretilen Dosyalar ve Betikler

| Dosya / Betik | Konum | Tanım |
|---------------|-------|-------|
| Yapılandırma | `data/config.json` | Veri kaynağı seçimi (`synthetic`/`real`) |
| Veri Yükleyici | `src/data_loader.py` | Esnek veri okuma katmanı |
| Üretim Betiği | `src/generate_synthetic_data.py` | Sentetik CSV dosyalarını üreten kod |
| Analiz Betiği | `src/analyze_consumption.py` | Tüketim analizini çalıştıran kod |
| Sentetik Veri Klasörü | `data/synthetic/` | 6 adet CSV veri dosyası |
| Analiz Raporu | `docs/hafta2_veri_analiz_raporu.md` | İstatistiksel sonuç dokümanı |

---

## Bir Sonraki Adım (Hafta 3 — Onaydan Sonra)

- **E-Kanban Sinyal Mimarisi & Karar Mantığı Kurulumu:**
  - Reorder Point (ROP) tabanlı e-Kanban tetikleme mekanizmasının kodlanması
  - Stok seviyelerinin anlık takibi ve dinamik sinyal üretimi
  - E-Kanban sinyal önceliklendirme ve zaman penceresi (TW) ataması

---

## Kontrol Soruları (Hafta Kapanışı için)

- [ ] **Kontrol 1:** Üretilen sentetik tüketim ve stok verilerinin istatistiksel dağılımı inceledin mi? Beklentilerine uygun mu?
- [ ] **Kontrol 2:** `DataLoader` katmanı ve `config.json` mimarisini onaylıyor musun? (Gerçek veri entegrasyonu için hazır).

---

*Hazırlayan: AI | Hafta 2 | Durum: Kontrol onayı bekleniyor*
