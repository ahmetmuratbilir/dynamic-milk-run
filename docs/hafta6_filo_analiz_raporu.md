# Hafta 6 — Filo Duyarlılık Analizi Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K12–K17, K33–K36 — bkz. `karar_gunlugu.md`

---

## 1. Amaç (Objective)

Hafta 5'te 2 araçlı VRPTW simülasyonu %52.08 starvation oranı ve %18.5 araç doluluk oranı vermiştir. K36 kararında darboğazın kutu kapasitesi değil, **zaman ve filo kısıtı** olduğu tespit edilmiştir.

Bu haftanın amacı:
1. **Analitik olarak** kaç araç gerektiğini Körösi & Duchoň (2026, Nature) formülüyle hesaplamak
2. **Deneysel olarak** 2, 3 ve 4 araç senaryolarını VRPTW simülasyonuyla karşılaştırmak
3. İki yöntemin sonuçlarının tutarlılığını doğrulamak (cross-validation)

---

## 2. Yöntem (Methodology)

### 2.1 Analitik Filo Boyutlandırma

**Kaynak:** Körösi, G. & Duchoň, F. (2026). Analytical fleet-sizing method for OPIL. *Scientific Reports*, 16, 16797. **Sayfa 3–4.**

$$AN_{final} = \left\lceil \frac{WL}{AT} \right\rceil = \left\lceil \frac{w \times TC}{60 \times A \times F_t \times E_w} \right\rceil$$

**Parametreler:**

| Parametre | Değer | Kaynak |
|-----------|-------|--------|
| $T_L$ | 2 dk | K14 |
| $T_U$ | 3 dk | K15 |
| $v_c$ | 166.67 m/dk | K12 |
| $L_d$ | 160 m | Mesafe matrisi (depot→istasyonlar ortalaması) |
| $L_e$ | 160 m | Mesafe matrisi (istasyonlar→depot ortalaması) |
| $w$ | 22.75 sinyal/saat | H4: 182 sinyal / 8 saat |
| $E_w$ | 1.0 | Körösi s.3: *"set to 1.0 for fully autonomous agents"* |

**Duyarlılık Senaryoları:**

| Senaryo | $A$ | $F_t$ | Kaynak |
|---------|-----|-------|--------|
| Muhafazakar | 0.70 | 0.60 | Körösi s.6 SMARTENVELOPE ($A=0.7, F_t=0.5$) civarı |
| Baz | 0.85 | 0.80 | Kullanıcı onaylı orta değer |
| İyimser | 0.95 | 0.95 | Körösi s.10 SMARTHam ($A=0.99, F_t=0.99$) civarı |

### 2.2 Deneysel Duyarlılık Analizi

**Referans:** Sevim & Aykut (2026). A dynamic in-plant milk-run system via agent-based modelling. *Pamukkale Üniv. Müh. Bil. Derg.* **Sayfa 1001–1006** (2 vs 3 araç testi, 3 araç önerisi).

Aynı 182 sinyal verisi (H4 çıktısı) 3 farklı filo boyutuyla çalıştırılmıştır:
- Senaryo 1: **2 araç** (mevcut K03 kararı)
- Senaryo 2: **3 araç** (Sevim & Aykut önerisi)
- Senaryo 3: **4 araç** (Körösi analitik baz sonucu)

**KPI tanımları:**
- **Starvation:** İstasyon stoğunun sıfıra düştüğü dakika sayısı (Wang 2008, m-VRPTW: s.48–55)
- **Karşılama oranı:** Zamanında + Gecikmeli teslim edilen sinyal / toplam sinyal

---

## 3. Bulgular (Findings)

### 3.1 Analitik Filo Hesabı Sonuçları

| Senaryo | $A$ | $F_t$ | $\Phi$ | TC (dk) | WL (dk/sa) | AT (dk/sa) | AN | $AN_{final}$ |
|---------|-----|-------|--------|---------|------------|------------|-----|-------------|
| Muhafazakar | 0.70 | 0.60 | 0.420 | 6.92 | 157.43 | 25.20 | 6.25 | **7** |
| **Baz** | **0.85** | **0.80** | **0.680** | **6.92** | **157.43** | **40.80** | **3.86** | **4** |
| İyimser | 0.95 | 0.95 | 0.902 | 6.92 | 157.43 | 54.15 | 2.91 | **3** |

> **Sonuç:** Baz senaryoda **en az 4 araç** gereklidir. Mevcut 2 araç, en iyimser senaryoda bile yetersizdir (AN=2.91 → 3 araç).

### 3.2 Deneysel Karşılaştırma Tablosu

| Metrik | 2 Araç | 3 Araç | 4 Araç | 5 Araç | 6 Araç |
|--------|:------:|:------:|:------:|:------:|:------:|
| Zamanında Teslim | 17 (%9.3) | 40 (%22.0) | 51 (%28.0) | 89 (%48.9) | 155 (%85.2) |
| Gecikmeli Teslim | 55 (%30.2) | 69 (%37.9) | 92 (%50.5) | 76 (%41.8) | 25 (%13.7) |
| Karşılanamayan | 110 (%60.4) | 73 (%40.1) | 39 (%21.4) | 17 (%9.3) | 2 (%1.1) |
| **Karşılama Oranı** | **%39.6** | **%59.9** | **%78.6** | **%90.7** | **%98.9** |
| **Starvation (ist-dk)** | **6,000** | **4,160** | **2,242** | **599** | **112** |
| **Starvation (%)** | **%52.08** | **%36.11** | **%19.46** | **%5.20** | **%0.97** |
| Toplam Tur | 16 | 24 | 32 | 42 | 81 |
| Araç Doluluk | %18.5 | %18.5 | %18.2 | ~%18 | ~%18 |

### 3.3 Değişim ve Azalan Getiri (Diminishing Returns) Analizi

| Geçiş | Starvation Δ (puan) | Karşılama Δ (puan) |
|--------|:---:|:---:|
| 2 → 3 araç | −15.97 | +20.3 |
| 3 → 4 araç | −16.65 | +18.7 |
| 4 → 5 araç | −14.26 | +12.1 |
| **5 → 6 araç** | **−4.23** | **+8.2** |

> **Gözlem:** 2→5 arası her ek araç ortalama ~15 puan starvation düşürüyor. Ancak 5→6 geçişinde marjinal iyileşme yalnızca 4.23 puana düşüyor — **azalan getiri (diminishing returns) etkisi 5. araçtan sonra belirginleşmektedir.**

---

## 4. Tartışma (Discussion)

### 4.1 Analitik ve Deneysel Tutarlılık

Körösi formülü baz senaryoda **4 araç** önerirken, deneysel simülasyonda 4 araçla starvation %19.46'ya düşmüştür (sıfır değil). Bu tutarlıdır çünkü:
- Körösi formülü **kararlı durum (steady-state)** varsayımına dayanır (s.4) — stokastik talep dalgalanmalarını modellemez
- Simülasyondaki stokastik tüketim ($\mathcal{N}(\mu, 0.20\mu)$, K10) ek starvation yaratır
- 4 araçla bile %19.46 starvation, formülün "alt sınır" niteliğinde olduğunu doğrular

### 4.2 Analitik vs Deneysel Farkın Metodolojik Önemi

Körösi'nin analitik modeli ile bizim stokastik simülasyonumuz arasındaki fark, bir çelişki değil, **metodolojik bir bulgudur.** Analitik yöntemler ortalama (steady-state) davranışı tahmin eder; ancak dinamik ve patlamalı (bursty) talep koşullarında yetersiz kalabilir. Bizim sistemimizde talep stokastik olup ($CV = 0.20$, K10), sinyal zamanlamaları eşit aralıklı değildir — bazı zaman dilimlerinde sinyal yoğunluğu ortalamanın çok üstüne çıkmaktadır. Bu durum, analitik "yeterli" sayıdaki aracın (4) gerçek dinamik ortamda hâlâ %19.46 starvation üretmesini açıklamaktadır. Bu bulgu, analitik boyutlandırmanın tek başına yeterli olmadığını ve simülasyon doğrulamasının zorunlu olduğunu göstermektedir.

### 4.3 Sevim & Aykut (2026) ile Karşılaştırma

Sevim & Aykut, benzer bir fabrika-içi milk-run sisteminde 2→3 araca geçişin istatistiksel olarak anlamlı etki yarattığını ve **3 araç önerildiğini** raporlamıştır (s.1001–1006). Bizim sonuçlarımız bunu destekler: 3 araçla karşılanamayan sinyal 110'dan 73'e düşmüştür (%33.6 iyileşme). Ancak bizim sistemimizde 3 araç yeterli değildir — bu fark, istasyon sayısı (bizde 24, Sevim'de daha az) ve talep yapısından kaynaklanmaktadır.

### 4.4 Araç Doluluk Oranının Sabitliği

Tüm senaryolarda araç doluluk oranı %18.2–%18.5 arasında kalmıştır. Bu K36 teşhisini güçlü şekilde doğrular: **darboğaz kutu kapasitesi değil, araç zamanıdır**. Araç sayısı artırıldığında doluluk değişmez, ama daha fazla tur yapılabilir.

### 4.5 Wang (2008) Perspektifi

Wang'ın m-VRPTW'de "hizmet verilen müşteri sayısını maksimize et" önceliği (s.48–55), bizim sonuçlarımızda net görülmektedir: 2 araçla %39.6, 6 araçla %98.9 karşılama oranı. Filo kısıtlı sistemlerde mesafe değil, karşılama kapasitesi birincil metriktir.

---

## 5. Sonuç ve Sonraki Adım

- **K03 kararı (2 araç) yetersizdir** — hem analitik (Körösi: AN=3.86→4) hem deneysel (%52.08 starvation) olarak kanıtlanmıştır.
- Araç sayısı arttıkça starvation **düzenli ve monoton** azalmaktadır: %52→%36→%19→%5→%1.
- 5. araçtan sonra **azalan getiri (diminishing returns)** etkisi başlamaktadır (Δ 15 puan → 4 puan).
- 4 araçla bile starvation sıfırlanmıyor (%19.46). Bu, ya daha fazla araç gerektiğini ya da dispatch/çizelgeleme optimizasyonunun ek katkı sağlayabileceğini göstermektedir — **hangisinin maliyet-etkinlik açısından daha verimli olduğu, gelecek çalışma konusudur.**
- **Sonraki adım (Hafta 7–8):** SimPy entegrasyonu ile stokastik simülasyon altyapısının kurulması ve farklı dispatch stratejilerinin test edilmesi.

