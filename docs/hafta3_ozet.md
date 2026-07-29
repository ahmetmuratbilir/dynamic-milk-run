# Hafta 3 Özeti
## Dinamik Milk-Run & E-Kanban Karar Destek Sistemi

**Dönem:** Hafta 3 — Dinamik Kanban Hesabı ve Duyarlılık Analizi
**Durum:** ✅ KAPATILDI — Kullanıcı onayı alındı (30.07.2026)

> ⚠️ Bu haftaki tüm analizler SENTETİK veriyle yapılmıştır.
> Gerçek fabrika verisi geldiğinde `data/config.json → "real"` yapılarak tekrar çalıştırılmalıdır.

---

## Bu Hafta Ne Yaptık?

### 1. Kanban Modülü Kuruldu — `src/kanban_hesap.py`
- 24 istasyon için $N = \lceil (D \times LT \times (1+\alpha)) / C \rceil$ formülü **adım adım** hesaplandı.
- Her istasyon için: temel ihtiyaç, güvenlik stoğu, toplam ihtiyaç, N, başlangıç stok tablosu üretildi.
- Toplam fabrika stok kapasitesi: **455 adet** (LT=45, α=0.15 ile)

### 2. Duyarlılık Analizi — 3 Parametre Test Edildi

**LT Duyarlılığı (en kritik bulgu):**
- LT ≤ 45 dk → sistem N=1 ile çalışıyor ✅
- LT = 60 dk → 18 istasyonda N=2'ye çıkıyor ⚠️
- LT = 75 dk → tüm istasyonlar N=2 ⚠️
- **Savunma argümanı:** *"LT=45 dk, sistemin ikiye katlanma eşiğinin tam altında. 5 dk daha uzasaydı sistem 2 katı stok tutmak zorunda kalırdı."*

**α Duyarlılığı:**
- α = 0.05–0.20 → büyük çoğunluk için N değişmiyor (yuvarlama etkisi)
- α = 0.30 (Klenk 2012'nin değeri) → S1, S7, S13, S16, S24'te N=2

**C Duyarlılığı:**
- C = 10 → S16'da N=3 gerekiyor ⚠️
- C = 15/20 → dengeli ✅
- C ≥ 25 → N=1 yeterli ama hat yanına fiziksel olarak sığmaz

### 3. Kritik İstasyon Belirlendi — S16 (Hat-3)
- D = 24 adet/sa (sistemdeki en yüksek tüketim)
- Her parametrede en kırılgan istasyon
- Tezde "en kırılgan nokta" vaka analizi olarak öne çıkarılacak (kullanıcı onayı ✅)

### 4. Açık Kalan Kararlar Onaylandı

| Karar | Değer | Makale Desteği |
|-------|-------|----------------|
| **K25 — ROP Formülü** | $ROP = D_{dk} \times LT \times (1+\alpha)$ | Klenk (2012) satır 1199–1200 |
| **K26 — Öncelik Kuralı** | Karma: Kritiklik + FIFO | Facchini (2022) satır 416-417, Simić (2020) satır 301 |

### 5. N ile ROP Arasındaki Fark Netleştirildi

| | N | ROP |
|--|---|-----|
| Soru | Kaç kutu? | Ne zaman sinyal? |
| Ne zaman | Kurulumda bir kez | Her dakika kontrol |
| Birim | Kutu (integer) | Adet (sürekli) |
| Aynı α | Evet — ama farklı amaç |

---

## Üretilen Dosyalar

| Dosya | İçerik |
|-------|--------|
| `src/kanban_hesap.py` | Kanban modülü + duyarlılık analizi kodu |
| `data/synthetic/kanban_hesap.csv` | 24 istasyon için tam hesap tablosu |
| `docs/hafta3_kanban_analiz.md` | Analiz raporu (3 duyarlılık tablosu) |
| `docs/karar_gunlugu.md` | K25, K26 eklendi; değişiklik geçmişi güncellendi |

---

## Bir Sonraki Adım — Hafta 4: E-Kanban Sinyal Mimarisi

K25 (ROP formülü) ve K26 (Karma öncelik) onaylandı.
Artık bu kararlarla `src/ekanban_signal.py` yazılabilir:
- Her dakika stok izleme
- ROP eşiği geçilince sinyal üretme
- Sinyal önceliklendirme (Karma: Kritiklik + FIFO)
- Zaman penceresi atama [t_sinyal, t_sinyal + 60 dk]
- 480 dk simülasyonda toplam sinyal sayısı ve dağılımı

---

*Hazırlayan: AI | Hafta 3 | Durum: ✅ Kapalı*
