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

> [!WARNING]
> **⚠️ ERRATA — Raf Tavanı Düzeltmesi (Hafta 10 Denetimi, 15.08.2026):**  
> Aşağıdaki orijinal tablo, istasyon stok düzeylerinin fiziksel raf kapasitesinin ($stok \le N \times C$) **ötesine çıkabildiği** basitleştirilmiş (tavansız) model üzerinden hesaplanmıştır. Bu durum, özellikle yüksek araç sayısında hayali stok birikimi oluşturarak starvation değerlerinin gerçekçi olmayan biçimde düşük çıkmasına yol açmıştır. Hafta 10 geriye dönük denetiminde tavan kısıtı uygulandığında, **5 araçta starvation %5.20'den %15.98'e, 6 araçta %0.97'den %11.27'ye çıkmıştır** (EDD kuralı). Düzeltilmiş veriler ve metodolojik açıklama bu bölümün sonunda verilmektedir.

| Metrik | 2 Araç | 3 Araç | 4 Araç | 5 Araç | 6 Araç |
|--------|:------:|:------:|:------:|:------:|:------:|
| Zamanında Teslim | 17 (%9.3) | 40 (%22.0) | 51 (%28.0) | 89 (%48.9) | 155 (%85.2) |
| Gecikmeli Teslim | 55 (%30.2) | 69 (%37.9) | 92 (%50.5) | 76 (%41.8) | 25 (%13.7) |
| Karşılanamayan | 110 (%60.4) | 73 (%40.1) | 39 (%21.4) | 17 (%9.3) | 2 (%1.1) |
| **Karşılama Oranı** | **%39.6** | **%59.9** | **%78.6** | **%90.7** | **%98.9** |
| **Starvation (ist-dk)** | **6,000** | **4,160** | **2,242** | **599** | **112** |
| **Starvation (%) — TAVANSIZ `[Orijinal]`** | **%52.08** | **%36.11** | **%19.46** | **%5.20** | **%0.97** |
| Toplam Tur Sayısı | 16 | 24 | 32 | 42 | 81 |
| Ort. Tur Başı Kutu | 4.62 | 4.62 | 4.56 | 4.02 | 2.28 |
| **Araç Doluluk (%)** | **%18.50** | **%18.50** | **%18.25** | **%16.10** | **%9.14** |

#### 📐 Düzeltilmiş Tablo — Tavanlı Model ($stok \le N \times C$, EDD Dispatch, Hafta 10 Denetimi)

| Araç | Tavansız Duruş `[Orijinal]` | **Tavanlı Duruş** `[Düzeltilmiş]` | Tavansız WIP | **Tavanlı WIP** | Fark |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **2** | %51.28 | **%53.01** | 121.2 | **111.1** | +1.74 puan |
| **3** | %33.75 | **%36.93** | 166.5 | **148.5** | +3.18 puan |
| **4** | %17.00 | **%24.58** | 229.8 | **182.3** | +7.59 puan |
| **5** | %3.96 | **%15.98** | 339.8 | **211.0** | +12.02 puan |
| **6** | %0.64 | **%11.27** | 426.1 | **224.4** | +10.62 puan |
| **7** | %0.28 | **%7.00** | 474.5 | **232.9** | +6.72 puan |
| **8** | %0.10 | **%3.50** | 501.8 | **237.3** | +3.40 puan |

> `[Kod çıktısı]` — `src/denetim_reproduksiyon_testi.py` + `src/hafta10_whatif_senaryolari.py` kanonik motoru (K57). EDD dispatch kuralı. Orijinal H6 tablosu KRİTİKLİK kuralıyla üretilmişti; EDD tabanlı tavansız değerler orijinalden hafif farklıdır.
>
> **Düzeltilmiş Bulgular:**  
> - Raf tavanı uygulandığında hiçbir filo büyüklüğü orijinaldeki %5 eşiğini koruyamaktadır.  
> - Tavanlı modelde **%5'in altına inmek için 8 araç gerekmektedir** (%3.50).  
> - Tavan etkisi araç sayısı arttıkça büyümekte (maksimum +12.02 puan, 5 araçta), ardından küçülmektedir — bu "azalan sıçrama" eğrisi, stokun sisteme geri beslemesinin filo büyüdükçe değiştiğini yansıtmaktadır.

### 3.3 Değişim ve Azalan Getiri (Diminishing Returns) Analizi

| Geçiş | Starvation Δ (puan) | Karşılama Δ (puan) | Marjinal Eğilim |
|--------|:---:|:---:|---|
| 2 → 3 araç | −15.97 | +20.3 | Artan marjinal fayda |
| **3 → 4 araç** | **−16.65** | **+18.7** | **Zirve marjinal fayda** |
| 4 → 5 araç | −14.26 | +12.1 | Düşüş başlangıcı |
| **5 → 6 araç** | **−4.23** | **+8.2** | **Sert azalan getiri** |

> **Gözlem:** Marjinal fayda 3→4 araç geçişinde zirve yapmakta (16.65 puan düşüş), 4. araçtan sonra azalmaya başlamakta, 5→6 geçişinde ise belirgin şekilde düşmektedir (4.23 puan) — **klasik azalan getiri eğrisi 4–5 araç bandında netleşmektedir.**
>
> *(Not: Bu analiz orijinal tavansız verilere dayanmaktadır. Tavanlı verilerle marjinal fayda örüntüsü farklılaşmaktadır; 5 araç geçişinde eğri kırılmamaktadır — bkz. düzeltilmiş tablo.)*

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

### 4.4 Araç Doluluk Oranının Seyri (Kapasite vs Atıl Filo)

2, 3 ve 4 araç senaryolarında araç doluluk oranı **%18.25–%18.50** bandında neredeyse sabittir (ort. ~4.6 kutu/tur). Bu durum, 4 araca kadar olan bantta araçların her seferde ellerindeki maksimum sinyali topladıklarını ve kısıtın kutu kapasitesi değil **araç zamanı/sayısı** olduğunu (K36) teyit eder. 
Ancak 5 araçta doluluk **%16.10**'a, 6 araçta ise **%9.14**'e (ort. 2.28 kutu/tur, 81 tur) gerilemektedir. 6 araçlı sistemde araçlar biriken sinyalleri beklemeden hemen yola çıktığı için starvation %0.97'ye inmekte, fakat araç kapasite kullanımı yarı yarıya düşerek **aşırı filo kapasitesi (atıl filo / israf)** oluşmaktadır.

### 4.5 Wang (2008) Perspektifi

Wang'ın m-VRPTW'de "hizmet verilen müşteri sayısını maksimize et" önceliği (s.48–55), bizim sonuçlarımızda net görülmektedir: 2 araçla %39.6, 6 araçla %98.9 karşılama oranı. Filo kısıtlı sistemlerde mesafe değil, karşılama kapasitesi birincil metriktir.

---

## 5. Sonuç ve Sonraki Adım

- **K03 kararı (2 araç) yetersizdir** — hem analitik (Körösi: AN=3.86→4) hem deneysel (%52.08 starvation) olarak kanıtlanmıştır.
- Araç sayısı arttıkça starvation düzenli azalmaktadır: %52.08 → %36.11 → %19.46 → %5.20 → %0.97 *(orijinal tavansız model)*.
- **Marjinal fayda 3→4 araç geçişinde zirve yapmakta (16.65 puan), 4. araçtan sonra azalmaya başlamakta, 5→6 geçişinde ise belirgin şekilde düşmektedir (4.23 puan) — klasik azalan getiri eğrisi 4–5 araç bandında netleşmektedir.**
- 4 araçla bile starvation %19.46 seviyesindedir; 6 araçla starvation %0.97'ye inerken doluluk %9.14'e düşmektedir. Bu durum, filoyu 6'ya çıkararak atıl kapasite yaratmak yerine **dispatch/çizelgeleme optimizasyonunun** potansiyel olarak daha sürdürülebilir bir alternatif olabileceğini düşündürmektedir; bu iki yaklaşımın maliyet-etkinlik karşılaştırması bu çalışmanın kapsamı dışındadır ve gelecek çalışma (Hafta 7–8) önerisi olarak bırakılmıştır.
- **Sonraki adım (Hafta 7–8):** SimPy entegrasyonu ile stokastik simülasyon altyapısının kurulması ve farklı dispatch/önceliklendirme stratejilerinin test edilmesi.

> [!IMPORTANT]
> **⚠️ ERRATA — Raf Tavanı Düzeltmesi (Hafta 10 Denetimi, 15.08.2026):**  
> Yukarıdaki Bölüm 5 sonuç cümleleri orijinal (tavansız) simülasyon verilerine dayanmaktadır. Hafta 10 denetiminde fiziksel raf tavanı ($stok \le N \times C$) uygulandığında "%5.20" ve "%0.97" değerleri sırasıyla **%15.98** ve **%11.27**'ye yükselmektedir. "5–6 araç <%5 duruş eşiğine yeterli" ifadesi bu durumda geçerli değildir; **tavanlı modelde %5 eşiğine inmek için 8 araç gerekmektedir (%3.50)**. Düzeltilmiş tam tablo Bölüm 3.2'deki Errata tablosunda verilmiştir. Tezin bu bölüme atıfta bulunan sonuç cümleleri güncellenmelidir.
