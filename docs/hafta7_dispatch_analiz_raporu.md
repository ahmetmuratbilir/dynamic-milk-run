# Hafta 7 — Dispatch Stratejisi Karşılaştırması: Stokastik Replikasyon Analizi

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K26, K33, K34, K42, K43, K44  
**Bkz.:** `karar_gunlugu.md`, `hafta6_filo_analiz_raporu.md`

---

## 1. Amaç (Objective)

Hafta 6 sonunda (K41 kararı) şu soru açık bırakıldı: *"4 araçla dispatch stratejisini değiştirerek starvation daha fazla azaltılabilir mi — ve bu, araç eklemekten daha maliyet-etkin bir alternatif olabilir mi?"*

Hafta 7'de bu soruyu 30 stokastik replikasyon × 4 dispatch kuralı × 2 araç sayısı = **240 simülasyon** ile yanıtlamak hedeflenmiştir.

---

## 2. Yöntem (Methodology)

### 2.1 Stokastik Replikasyon Tasarımı

**Kaynak:** Herrera-Vidal et al. (2026), *Applied Sciences*, 16:1701, **Sayfa 8–10**  
→ 50 bağımsız replikasyon ve 30 dk Welch warm-up önerisi. K42 kararıyla test ortamı kısıtı nedeniyle **30 replikasyon** kullanılmıştır.  
→ K43: Warm-up = **45 dk** (K32 kararı korunmuştur; Welch'ın 30 dk önerisine göre muhafazakâr).

| Parametre | Değer | Kaynak |
|-----------|-------|--------|
| Replikasyon sayısı | 30 | K42 (Herrera-Vidal 2026 s.10) |
| Warm-up süresi | 45 dk | K43 (K32 korundu) |
| Efektif analiz penceresi | 435 dk (480-45) | Herrera-Vidal s.10 |
| Efektif denominator | 24 × 435 = 10.440 ist-dk | Warm-up sonrası |
| Random seed aralığı | 100–129 | Deterministik baseline (seed=42)'den ayrı |

### 2.2 Stokastiklik Kaynağı

Her replikasyonda tüketim profili `N(μ/60, 0.20×μ/60)` dağılımından farklı seed ile yeniden örneklendi (K10: CV=0.20). Kanban sinyalleri (`ekanban_signals.csv`) sabit tutuldu; dispatch stratejisi sinyalleri *seçiyor*, sinyallerin kendisi değişmiyor (K04, K06-K11).

### 2.3 Test Edilen Dispatch Kuralları (K44)

| Kural | Sıralama Kriteri | Akademik Dayanak |
|-------|-----------------|-----------------|
| **KRITIKLIK** | `kritiklik_skoru` ↑ (ROP/stok oranı) | K26 — mevcut baseline |
| **EDD** | `tw_bitis` ↑ (küçükten büyüğe) | Wang (2008) s.48: TW kısıtı önceliği |
| **SLACK** | `tw_bitis − t` ↑ (aciliyet skoru) | Wang (2008) s.52: minimum slack |
| **FIFO** | `tw_baslangic` ↑ (sinyal oluşma sırası) | Herrera-Vidal (2026) s.8: kuyruk baseline |

### 2.4 Metodolojik Not: H7 Stokastik vs H6 Deterministik Karşılaştırması

> [!IMPORTANT]
> **Kanonik Baseline Doğrulaması:**
> - Hafta 5–6'da kullanılan kanonik deterministik değer **%52.08**'dir ($6,000 / 11,520 \text{ ist-dk}$, 480 dk tam vardiya).
> - Hafta 7'deki 30 replikasyon ortalaması **%61.69** çıkmaktadır. Bu sıçramanın iki nedeni vardır:
>   1. **Payda Farkı (Warm-up Kesintisi):** H7'de 45 dk warm-up çıkarıldığı için payda $10,440 \text{ ist-dk}$'ya düşmektedir ($6,000 / 10,440 = \%57.47$).
>   2. **Stokastik Varyans:** Dakikalık bağımsız rastgele tüketim dalgalanmaları duruş süresini ortalama $6,440 \text{ dk}$'ya çıkarmıştır ($6,440 / 10,440 = \%61.69$).
> 
> Dolayısıyla %52.08 deterministik referans değerimiz geçerliliğini korumaktadır; %61.69 ise stokastik ortamdaki dinamik karşılığıdır.

---

## 3. Bulgular (Findings)

### 3.1 Ozet Tablo: mean ± %95 CI

| Araç | Kural | Mean (%) | Std | CI±95 | Min (%) | Max (%) |
|:----:|-------|:--------:|:---:|:-----:|:-------:|:-------:|
| 2 | KRITIKLIK | 61.693 | 0.167 | 0.059 | 61.351 | 62.117 |
| 2 | EDD | 60.964 | 0.164 | 0.058 | 60.575 | 61.245 |
| 2 | SLACK | 60.964 | 0.164 | 0.058 | 60.575 | 61.245 |
| 2 | FIFO | 60.962 | 0.162 | 0.057 | 60.575 | 61.255 |
| **4** | **KRITIKLIK** | **27.828** | **0.182** | **0.064** | **27.529** | **28.199** |
| **4** | **EDD** | **26.503** | **0.210** | **0.074** | **26.054** | **26.858** |
| **4** | **SLACK** | **26.503** | **0.210** | **0.074** | **26.054** | **26.858** |
| **4** | **FIFO** | **26.502** | **0.205** | **0.072** | **26.044** | **26.849** |

### 3.2 Welch t-testi: KRITIKLIK vs Alternatifler (4 Araç)

**Kaynak:** Herrera-Vidal (2026) s.10 — %95 güven aralığı ve Welch t-testi (eşit varyans varsayımı yok)

| Karşılaştırma | Δ (puan) | p-değeri | Anlamlı? |
|---------------|:--------:|:--------:|:--------:|
| EDD vs KRITIKLIK | **−1.325** | **< 0.0001** | ✅ ** |
| SLACK vs KRITIKLIK | **−1.325** | **< 0.0001** | ✅ ** |
| FIFO vs KRITIKLIK | **−1.326** | **< 0.0001** | ✅ ** |

> **p < 0.0001 (** — son derece anlamlı)**: Üç alternatif kural da KRITIKLIK'ten istatistiksel olarak anlamlı biçimde daha iyi performans göstermektedir.

### 3.3 EDD / SLACK / FIFO Özdeşliği

Üç alternatif kural arasındaki fark ihmal edilebilir düzeydedir (< 0.002 puan). Bunun nedeni:

- `tw_bitis = tw_baslangic + lt_dk` — `lt_dk` tüm istasyonlarda **45 dk** sabittir (K15, K08)
- Dolayısıyla EDD (`tw_bitis` ↑) ≈ FIFO (`tw_baslangic` ↑) — aynı sıralamayı üretirler
- SLACK = `tw_bitis − t` — her t anında `t` sabit olduğundan sıralama EDD ile özdeşleşir

Bu yapısal nedenle üç kural pratik olarak **tek bir kural gibi davranmaktadır.**

---

## 4. Tartışma (Discussion)

### 4.1 Dispatch Kuralının Etkisi: İstatistiksel Anlamlılık vs Pratik Büyüklük

Üç alternatif kural, KRITIKLIK'ten **~1.3 puan** daha iyi sonuç vermiş ve bu fark p<0.0001 düzeyinde istatistiksel olarak son derece anlamlıdır. Ancak etki büyüklüğü önemli bir bağlam gerektirmektedir:

H6'da filo büyüklüğü artırımının marjinal etkisi (aynı KRITIKLIK kuralıyla, deterministik):

| Geçiş | Δ Starvation |
|-------|:------------:|
| 2→3 araç | −15.97 puan |
| 3→4 araç | −16.65 puan |
| 4→5 araç | −14.26 puan |

Dispatch kural değişiminin etkisi (~1.3 puan), araç eklemenin marjinal etkisinin (14–17 puan) **yaklaşık 1/12'si** kadardır. Dispatch optimizasyonu gerçek ve anlamlı bir iyileşme sağlamaktadır, fakat filo büyüklüğünün baskın belirleyici olmaya devam ettiği görülmektedir.

### 4.2 Neden KRITIKLIK En Kötü?

KRITIKLIK skoru (K26), stokun ROP'a oranını kullanır — bu bir *stok tabanlı aciliyet* ölçüsüdür. Ancak bu ölçüt, zaman penceresi (TW) kısıtıyla doğrudan hizalanmamaktadır. EDD/SLACK ise *zaman tabanlı aciliyet* ölçütü kullanmaktadır. Wang (2008) s.48'de belirtildiği gibi, TW kısıtlı sistemlerde zaman tabanlı önceliklendirme daha etkin hizmet sağlamaktadır. Bulgumuz bu teorik beklentiyle tamamen örtüşmektedir.

### 4.3 Yapısal Kısıt: Mevcut Sinyal Altyapısı EDD/SLACK'ı Avantajlı Kılıyor

H7'de tüm istasyonlar aynı `lt_dk=45 dk` değerine sahip olduğundan EDD≈SLACK≈FIFO özdeşleşmiştir. Gerçek veri senaryosunda istasyonlara göre farklı `lt_dk` değerleri varsa, EDD ve SLACK birbirinden ayrışacak ve SLACK'in zirveye çıkması beklenir (Wang 2008 s.52). Bu, gerçek veriye geçişte test edilmelidir.

### 4.4 H6 ile Çapraz Metodolojik Bulgu

H6'da analitik model (Körösi 2026) 4 araç önerirken simülasyon %19.46 starvation gösterdi — formülün deterministik alt sınır niteliğinde olduğu kanıtlandı. H7'de aynı 4 araçla stokastik replikasyonlar %27.83 (KRITIKLIK) verdi. Bu, **stokastik talep dalgalanmalarının starvation'ı deterministik tahminden sistematik olarak daha yüksek tuttuğunu** doğrulamaktadır; bu durum Herrera-Vidal (2026) s.10'da belirtilen "steady-state dışı dönemlerin sistemi etkileyen geçici yüklere yol açması" ile tutarlıdır.

---

## 5. Sonuç ve Sonraki Adım

- **Dispatch kuralı istatistiksel olarak anlamlı etkiye sahiptir** (p<0.0001): EDD/SLACK/FIFO, KRITIKLIK'ten ~1.3 puan daha iyi starvation sağlamaktadır.
- Ancak **etki büyüklüğü nispeten küçüktür** (~1.3 puan); filo artırımının marjinal etkisinin (14–17 puan) yaklaşık 1/12'si kadardır.
- Mevcut sinyal altyapısında (`lt_dk=45 dk` sabit) EDD, SLACK ve FIFO **pratik olarak özdeş** performans sergilemektedir.
- KRITIKLIK'in (K26) yerini EDD veya SLACK alabilir — bu değişikliğin projede uygulanması için K45 kararı gereklidir.
- **Sonraki adım (Hafta 8):** Gerçek veri entegrasyonu (`config.json → "real"`) ve parametrelerin gerçek veriyle yeniden kalibrasyonu; gerçek `lt_dk` dağılımıyla EDD vs SLACK farkının gözlemlenmesi.
