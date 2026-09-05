# DİNAMİK MİLK-RUN VE E-KANBAN KARAR DESTEK SİSTEMİ
## TEZ BİLGİ VE AKADEMİK METODOLOJİ MASTER REHBERİ (HAFTA 1 – 13)

> **Bu Dokümanın Amacı:** Bu dosya, projenin başından sonuna kadar (Hafta 1–13) elde edilen tüm teorik, mühendislik, matematik ve yazılımsal çıktılardan tezin Giriş, Literatür, Metodoloji ve Bulgular bölümlerinin doğrudan yazılabilmesini sağlayan **yaşayan akademik master dokümandır**.  
> **Son güncelleme:** Eylül 2026 — Hafta 6-13 bulguları IMRaD formatında eklendi; gerçekleşmemiş planlar kaldırıldı.

---

## 1. PROBLEM DEFINITION (Problem Tanımı)

- **Endüstriyel Bağlam:** Tam Zamanında (JIT) ve Yalın Üretim prensipleriyle çalışan montaj fabrikalarında (otomotiv, beyaz eşya), hat başı parça tedariği kritik bir lojistik operasyondur.
- **Gerçek Fabrika Problemi:** Tüketim hızlarının sabit olmaması, hat başında hem aşırı stok birikmesine (WIP maliyeti) hem de stoksuz kalma (starvation) sonucu montaj hattının durmasına neden olmaktadır.
- **Lojistik Kısıtlar:** Malzeme taşıma araçları (çekici-römork / tugger train) sınırlı zaman, hız, seyahat mesafesi ve taşıma kapasitesine sahiptir. Statik sipariş verme sistemleri bu dinamik kısıtları yönetmede yetersiz kalmaktadır.

---

## 2. RESEARCH GAP (Literatürdeki Eksiklik ve Katkımız)

- **Literatürdeki Eksiklik:**
  1. Çoğu çalışma Kanban boyutlandırmasını ve sinyal mimarisini **sabit tüketim ve teorik Lead Time ($LT$)** varsayımlarıyla ele almaktadır.
  2. E-Kanban sinyal üretimi ile araçların fiziksel zaman pencereli rotalamasını (**VRPTW**) entegre eden dinamik ve çevrimiçi (online) simülasyon modelleri kısıtlıdır.
- **Bu Tezin Özgün Katkısı (Novelty):**
  1. Tüketim dalgalanmalarına duyarlı oransal tamponlu Dinamik Kanban ve Karma Önceliklendirmeli E-Kanban Sinyal Mimarisi geliştirilmiştir.
  2. Teorik sinyal modellerinin araç kısıtları (VRPTW) altına sokulduğunda saklı kalan hat durmalarını nasıl görünür kıldığını kanıtlayan bütünleşik bir Karar Destek Sistemi (KDS) sunulmaktadır.

---

## 3. RESEARCH QUESTIONS (Araştırma Soruları)

- **RQ1 (Kanban Boyutlandırma):** Stok tüketim hızının dalgalandığı montaj hatlarında, oransal tamponlu ($\alpha$) Dinamik Kanban modeli ($N = \lceil D \cdot LT \cdot (1+\alpha) / C_{kutu} \rceil$) hat başı emniyetini nasıl etkiler?
- **RQ2 (Sinyal Mimarisi):** E-Kanban sistemlerinde eş zamanlı sinyallerin önceliklendirilmesinde Karma Kural (Kritiklik Skoru + FIFO) starvation riskini minimize etmede ne kadar etkilidir?
- **RQ3 (Teorik Basitleştirme vs. VRPTW):** Dinamik Kanban hesaplamalarında yapılan "Sabit Lead Time ($LT=45$ dk) ile stok yenilenir" basitleştirmesi ile fiziksel VRPTW araç kısıtları arasındaki performans farkı nedir?
- **RQ4 (Darboğaz Teşhisi):** Fabrika içi milk-run çekici-römork sistemlerinde asıl operasyonel darboğaz araç kutu kapasitesi ($Q_{arac}$) midir, yoksa seyahat/handling sürelerine dayalı filo büyüklüğü (zaman kısıtı) mıdır?

---

## 4. OBJECTIVES AND CONTRIBUTIONS (Amaçlar ve Katkılar)

- **Ana Amaç:** Fabrika içi malzeme beslemede stoksuz kalma süresini ve toplam seyahat süresini eş zamanlı minimize eden E-Kanban + VRPTW tabanlı dinamik bir Karar Destek Sistemi geliştirmek.
- **Alt Amaçlar:**
  - 24 istasyon ve 4 montaj hattı için dinamik $N$ ve $ROP$ hesaplama modülü yazmak.
  - Sinyaller için dinamik Zaman Penceresi ($TW$) ve Karma Öncelikleme algoritması kurgulamak.
  - Nearest Neighbor + 2-opt tabanlı olay bazlı VRPTW rotalama motoru geliştirmek.
- **Beklenen Katkılar:** Teorik Kanban boyutlandırması ile sahada çalışan araç rotalaması arasındaki uçurumu kapatan akademik olarak izlenebilir ve sanayide uygulanabilir bir metodoloji sunmak.

---

## 5. SCOPE (Araştırma Kapsamı)

### Kapsam İçinde Olanlar (In-Scope):
- Fabrika içi (in-plant) milk-run lojistik ağı.
- 4 montaj hattı, 24 istasyon, 1 ana depo (depot).
- Dinamik tüketim verileri (Poisson/Normal dağılımlı sentetik ve gerçek ERP veri desteği).
- Çevrimiçi/Olay bazlı (event-based) VRPTW rotalama.

### Kapsam Dışında Olanlar (Out-of-Scope):
- Fabrika dışı (outbound/supplier) tedarik zinciri nakliyesi.
- Aşırı karmaşık Yapay Zeka / Digital Twin modelleri (Master prompt yasağı gereği).
- Otonom AGV engel aşma / fiziksel sensör seviyesi simülasyonlar.

---

## 6. ASSUMPTIONS (Mühendislik ve Model Varsayımları)

- **Sentetik Veri Düzeni:** 4 hat, 24 istasyon, 1 ana depo simetrik mesafe matrisi (`distances.csv`).
- **Filo Yapısı:** 2 adet milk-run aracı ($A_1, A_2$) — *Mühendislik Varsayımı (K03)*.
- **Araç Kapasitesi:** $Q_{arac} = 25$ kutu/araç — *Mühendislik Varsayımı (K04)* (Menanno 2023 gerçek değeri $Q_{min}=45$).
- **Operasyonel Süreler:** Lead Time $LT = 45$ dk, Max tur süresi = $90$ dk, Handling = $5$ dk/durak, Yükleme = $2$ dk, Boşaltma = $3$ dk.
- **Çalışma Ufku:** 1 vardiya = $480$ dakika.

---

## 7. MATHEMATICAL MODELS (Matematiksel Modeller ve Formülasyonlar)

### 7.1. Dinamik Kanban Kutu Sayısı ($N_s$)
$$N_s = \left\lceil \frac{D_s \cdot LT \cdot (1 + \alpha)}{C_{kutu}} \right\rceil$$

### 7.2. Reorder Point ($ROP_s$) — Oransal Tamponlu (K25)
$$ROP_s = D_s^{dk} \cdot LT \cdot (1 + \alpha)$$

### 7.3. Dinamik Zaman Penceresi Bitişi ($TW_{bitis}$) (K27 / K30 Guard)
$$t_{starv} = t_{sinyal} + \frac{Stok_{o\_an}}{D_s^{dk}}$$
$$TW_{bitis} = \max\left(\min(t_{starv} - 5, \quad t_{sinyal} + 60), \quad t_{sinyal} + LT\right)$$

### 7.4. VRPTW Amaç Fonksiyonu ve Kısıtlar (K35)
$$\min \sum_{k \in K} \sum_{i \in V} \sum_{j \in V} t_{ij} \cdot x_{kij}$$

**Kısıtlar:**
1. $\sum_{k} \sum_{j} x_{kij} = 1 \quad \forall i \in V \setminus \{0\}$ (Her sinyal 1 kez ziyaret edilir)
2. $\sum_{i} d_i \cdot y_{ki} \le Q_{arac} \quad \forall k \in K$ (Araç kutu kapasite kısıtı, $Q_{arac}=25$)
3. $a_i \le s_{ki} \le b_i \quad \forall i \in V$ (Zaman penceresi kısıtı: $a_i = TW_{baslangic}, b_i = TW_{bitis}$)
4. $T_k \le 90 \text{ dk} \quad \forall k \in K$ (Max tur süresi kısıtı)

---

## 8. SYSTEM ARCHITECTURE (Sistem Mimarisi)

```
[ ERP / Sentetik Tüketim Verisi (DataLoader) ]
                      │
                      ▼
[ Dinamik Kanban & ROP Hesaplama Engine (kanban_hesap.py) ]
                      │
                      ▼
[ E-Kanban Sinyal Simülatörü & Karma Öncelikleyici (ekanban_signal.py) ]
                      │
                      ▼
[ VRPTW Rotalama Motoru: NN + 2-opt (vrptw_solver.py) ]
                      │
                      ▼
[ Dakika Dakika Stok & Gerçek Starvation Simülasyonu ]
                      │
                      ▼
[ Gelecek: Karar Destek Arayüzü & KPI Dashboard (Streamlit/Vite) ]
```

---

## 9. VALIDATION STRATEGY (Doğrulama ve Test Stratejisi)

1. **Sentetik Doğrulama (Hafta 1-5):** Kontrollü değişkenlerle (24 istasyon, 182 sinyal) algoritma mantığının ve kısıtların sınanması.
2. **Gerçek Veri Geçişi:** `config.json -> "real"` ile ERP tüketim ve fabrika mesafe verilerinin modele aktarılması.
3. **Senaryo Analizi (What-If):** Araç sayısı (2 vs 3 vs 4), tampon oranı ($\alpha=0.05-0.30$) ve kutu kapasitesi değişikliklerinin sınanması.
4. **Duyarlılık Analizi (Sensitivity Analysis):** $LT$ ve tüketim hızı ($D$) değişimlerinin sistem starvation oranına etkisinin ölçülmesi.

---

## 10. RESEARCH DECISIONS LOG (Karar Soybilimi Matrisi: K01 – K36+)

| ID | Karar Konusu | Karar Değeri | Gerekçe / Açıklama | Kaynak / Dayanak | Hafta |
|:---:|:---|:---|:---|:---|:---:|
| **K01** | Fabrika Düzeni | 4 Hat, 24 İstasyon | Simetrik sentetik yerleşim | Mühendislik Varsayımı | H1 |
| **K02** | İstasyon Dağılımı | Hat başına 6 istasyon | Yönetilebilir ölçek | Mühendislik Varsayımı | H1 |
| **K03** | Araç Sayısı | 2 milk-run aracı ($A_1, A_2$) | Operasyonel sentetik varsayım | Mühendislik Varsayımı | H1 |
| **K04** | Araç Kapasitesi | $Q_{arac} = 25$ kutu | Operasyonel sentetik varsayım | Mühendislik Varsayımı (Menanno $Q_{min}=45$) | H1 |
| **K05** | Vardiya Süresi | 480 dakika (8 saat) | Standart tek vardiya ufku | Endüstri Standardı | H1 |
| **K06** | Kanban Formülü | $N = \lceil (D \cdot LT \cdot (1+\alpha))/C_{kutu} \rceil$ | Standart Kanban boyutlandırma | Elloumi (2025) / Simić (2020) | H3 |
| **K07** | Lead Time | $LT = 45$ dakika | Tedarik döngü süresi | Klenk et al. (2012) s.12 — tur süresi referansı, LT için yakın kaynak | H3 |
| **K08** | Tampon Oranı | $\alpha = 0.15$ (%15) | Güvenlik stoku payı | Klenk et al. (2012) s.12 — %30 tampon kullanmış; bizim %15 daha temkinli, aynı mantık | H3 |
| **K16** | TW Üst Sınır | Max +60 dakika | Zaman penceresi genişliği | Mühendislik Varsayımı | H4 |
| **K17** | Max Tur Süresi | 90 dakika / tur | Tur başı süre limiti | Mühendislik Varsayımı | H5 |
| **K25** | ROP Formülü | $ROP = D_{dk} \cdot LT \cdot (1+\alpha)$ | Oransal tamponlu eşik | **Mühendislik Tasarım Kararı** ⚠️ ERRATA: Klenk (2012) tur süresi tamponuna atıfta bulunur, ROP formülünü doğrudan desteklemez | H4 |
| **K26** | Sinyal Önceliği | Karma (Kritiklik + FIFO) | Starvation önleme | **Mühendislik Tasarım Kararı** ⚠️ ERRATA: Facchini/Simić genel öncelik kavramını destekler; Kritiklik+FIFO spesifik kuralı özgün tasarım | H4 |
| **K27** | Dinamik TW | $TW_{bitis} = \min(t_{starv}-5, t+60)$ | S16 pencere daralması düzeltmesi | Mühendislik Varsayımı | H4 |
| **K28** | Sinyal Güncelleme | Yeni sinyal üretme, kritikliği güncelle | Tekrarlayan sinyal engelleme | Mühendislik Varsayımı | H4 |
| **K29** | Otomatik Yenileme | Sinyal + 45 dk (Geçici) | VRPTW öncesi teorik varsayım | Geçici Varsayım | H4 |
| **K30** | TW Guard | $TW_{bitis} \ge t + LT$ | Pencere daralma alt sınırı | Mühendislik Varsayımı | H4 |
| **K31** | S13 Sınır Durumu | Marj %0.8 ($ROP=19.84, N \cdot C=20$) | Kanban edge-case belgelemesi | Matematiksel Analiz | H4 |
| **K32** | Isınma Periyodu | 0-45 dk `ISINMA`, 45-480 dk `KARARLI` | Warm-up ayrıştırması | Ayrık Olay Simülasyon Kuralı | H4 |
| **K33** | Rotalama Stratejisi | Olay Bazlı Dinamik Sevk | Çevrimiçi E-Kanban sevk | Facchini et al. (2022) Sayfa 2 | H5 |
| **K34** | VRPTW Algoritması | Nearest Neighbor + 2-opt | Yay bazlı greedy heuristik | Facchini et al. (2022) Sayfa 4 | H5 |
| **K35** | Amaç Fonksiyonu | Hard TW + Toplam Süre Min | Rota süresi minimizasyonu | Facchini (2022) s.2, CIRRELT (2010) s.2 | H5 |
| **K36** | Darboğaz Tespiti | Zaman ve Filo Kısıtı (%18.5 doluluk) | Kapasite değil zaman kısıtı | Mühendislik Teşhisi | H5 |

---

## 11. WEEKLY PROGRESS (Haftalık İlerleme Raporları — IMRaD Formatı)

### HAFTA 1–2: Veri Mimarisi ve Parametre Soyutlama
- **Amaç (Objective):** Fabrika veri yapısını soyutlamak ve literatür kaynaklı temel lojistik parametreleri tanımlamak.
- **Yöntem (Methodology):** `DataLoader` sınıfı ve `config.json` ile veri katmanı ayrıştırıldı. 32 makale taranarak sentetik veri üreteci (`generate_synthetic_data.py`) yazıldı.
- **Bulgular (Findings):** 24 istasyon, 4 hat ve 600 mesafeli matris oluşturuldu.
- **Tartışma (Discussion):** Esnek veri yapısı, ileride gerçek ERP verisine geçişi dertsiz hale getirmiştir.
- **Sonraki Haftaya Etkisi (Next Step):** Hafta 3 Kanban hesaplamaları için altyapı sağlandı.

### HAFTA 3: Dinamik Kanban Hesabı ve Duyarlılık Analizi
- **Amaç (Objective):** İstasyonlar için optimum Kanban kutu sayısını ($N$) hesaplamak ve parametre duyarlılığını test etmek.
- **Yöntem (Methodology):** $N = \lceil (D \cdot LT \cdot (1+\alpha)) / C_{kutu} \rceil$ formülü `kanban_hesap.py` ile kodlandı. $LT, \alpha, C_{kutu}$ üzerinde duyarlılık analizi yapıldı.
- **Bulgular (Findings):** Fabrika toplam stok kapasitesi 455 adet olarak bulundu. $LT \ge 60$ dk olduğunda stok ihtiyacının 2 katına çıktığı; S16 istasyonunun ($D=24$) sistemdeki en kırılgan nokta olduğu tespit edildi.
- **Tartışma (Discussion):** $LT=45$ dk eşiği sistemin katlanma noktasının hemen altındadır.
- **Sonraki Haftaya Etkisi (Next Step):** S16 vaka analizi ve ROP formülü için altyapı oluşturuldu.

### HAFTA 4: E-Kanban Sinyal Mimarisi
- **Amaç (Objective):** 480 dakikalık simülasyon boyunca stok takibi yapmak ve ROP eşiğinde E-Kanban sinyalleri üretmek.
- **Yöntem (Methodology):** Oransal ROP (K25) ve Karma Öncelikleme (K26) kurallarıyla `ekanban_signal.py` simülatörü kodlandı. Dinamik TW (K27/K30) eklendi.
- **Bulgular (Findings):** 480 dk'da 182 sinyal üretildi (23 Isınma, 159 Kararlı Hal). Teorik $LT=45$ dk otomatik yenileme varsayımı altında starvation **0** çıktı.
- **Tartışma (Discussion):** Teorik varsayım altında sistem kusursuz görünmektedir; ancak bu durum araç kısıtları dahil edilmediği içindir.
- **Sonraki Haftaya Etkisi (Next Step):** `ekanban_signals.csv` VRPTW motoruna girdi olarak aktarıldı.

### HAFTA 5: VRPTW Rotalama ve Gerçek Starvation Analizi
- **Amaç (Objective):** E-Kanban sinyallerini 2 araca Zaman Pencereli Araç Rotalama (VRPTW) ile atamak ve gerçek hat durmalarını ölçmek.
- **Yöntem (Methodology):** Olay bazlı (K33), Nearest Neighbor + 2-opt (K34) algoritmalarıyla `vrptw_solver.py` yazıldı. Araçların gerçek varış dakikalarına göre hat başı stok simüle edildi.
- **Bulgular (Findings):**
  - **Sinyal Taksonomisi:** 17 Zamanında Teslim (%9.3), 55 Gecikmeli Teslim (%30.2), 110 Karşılanamayan (%60.4) = Toplam 182.
  - **Araç Doluluk Oranı:** Tur başına ortalama 4.62 kutu ile **%18.5** doluluk.
  - **Gerçek Starvation:** **6,000 istasyon-dakikası (%52.08 fabrika durma oranı)**.
- **Akademik Tartışma (Discussion):**
  - *Metodolojik Teşhis:* VRPTW modeli doğrudan bir darboğaz üretmemiştir. Aksine, model fiziksel araç kapasitesi ve filo büyüklüğü gibi operasyonel kısıtların sistem performansına etkisini görünür hale getiren bir **karar destek ve analiz mekanizması** olarak görev yapmıştır.
  - *Darboğaz Tespiti (K36):* Darboğaz kutu kapasitesi ($Q_{arac}$) DEĞİLDİR (Doluluk %18.5). Asıl kısıt ZAMAN ve FİLO BÜYÜKLÜĞÜ (2 araç) kısıtıdır.
  - *S16 Nüansı:* $N=2$ tamponu, $N=1$ olan istasyonlara (S11 %81.9, S14 %80.8) göre S16'yı (%49.2) korumuş, ancak yetersiz filo nedeniyle durmayı tamamen önleyememiştir.
- **Sonraki Haftaya Etkisi (Next Step):** Hafta 6'da 2 araç kısıtının çözümü için filo büyüklüğü (2 vs 3 vs 4 araç) ve tur çizelgeleme duyarlılık analizi yapılacaktır.

---

### HAFTA 6: Filo Büyüklüğü Duyarlılık ve Analitik Karşılaştırma
- **Amaç (Objective):** %52.08 starvation oranını düşürmek için araç sayısını (2–8) analitik ve simülasyon temelli olarak test etmek.
- **Yöntem (Methodology):** Körösi & Duchoň (2026) analitik filo formülü ($AN = WL/AT$) ile kendi simülasyon sonuçları karşılaştırıldı. 2'den 8'e kadar her araç sayısı için simülasyon çalıştırıldı. ⚠️ Bu haftanın verileri fiziksel raf tavanı kısıtı uygulanmadan üretildi (Hafta 10 ERRATA'sına bakınız).
- **Bulgular (Findings):** Analitik model 4 araç önerirken simülasyon 4 araçta %19.46 starvation gösterdi — formülün deterministik alt sınır niteliğinde olduğu kanıtlandı. Araç sayısı arttıkça starvation düzenli azaldı (%52→%36→%19→%5.20→%0.97, tavansız).
- **Tartışma (Discussion):** Darboğaz kutu kapasitesi değil, zaman ve filo büyüklüğü kısıtıdır (K36). Analitik formül gerçek stokastik sistemi yetersiz tahmin etmektedir.
- **⚠️ ERRATA (Hafta 10):** Raf tavanı ($stok \le N \times C$) uygulandığında 5 araç %15.98, 6 araç %11.27 çıkmaktadır — "%5 eşiğine 5-6 araç yeterli" bulgusu geçersizdir. Düzeltilmiş veriler `hafta6_filo_analiz_raporu.md` Bölüm 3.2'dedir.

### HAFTA 7: Dispatch Kuralları Karşılaştırması — Stokastik Replikasyon
- **Amaç (Objective):** EDD, SLACK, FIFO ve KRİTİKLİK dispatch kurallarının 30 stokastik replikasyonla istatistiksel karşılaştırması (K44).
- **Yöntem (Methodology):** 30 bağımsız replikasyon (farklı seed), 45 dk ısınma, 435 dk etkin analiz penceresi (K42, K43). Kural sıralama kriterleri: EDD=`tw_bitis↑`, SLACK=`tw_bitis−t↑`, FIFO=`tw_baslangic↑`, KRİTİKLİK=`kritiklik_skoru↑`. Wang et al. (2008) kaynaklandırıldı. İki örnekli t-testi (two-sample t-test) uygulandı.
- **Bulgular (Findings):**
  - 4 araç, EDD: %26.503 ± 0.074, KRİTİKLİK: %27.828 ± 0.064
  - EDD/SLACK/FIFO vs KRİTİKLİK: Δ≈−1.33 puan, **p<0.0001** ✅ anlamlı
  - EDD vs SLACK: Δ=−0.006 puan, **p=0.913** → istatistiksel olarak eşdeğer
  - FIFO kaynak: Mühendislik tasarım kararı (K44 ERRATA: Herrera-Vidal L8-10 atfı yanlıştı)
- **Tartışma (Discussion):** KRİTİKLİK kuralı diğer üçünden anlamlı biçimde daha kötüdür. EDD, SLACK, FIFO herhangi biri seçilebilir; EDD teorik olarak daha sağlam (Wang 2008).

### HAFTA 8: Statik vs Dinamik Karşılaştırma — WIP-Starvation Trade-off
- **Amaç (Objective):** Sabit turlu statik Milk-Run sistemi ile dinamik E-Kanban sistemini eşit WIP koşulunda karşılaştırmak.
- **Yöntem (Methodology):** StaticMilkRunSimulator (80 dk tur sıklığı, kanonik seed=42) ile EkanbanSimulator karşılaştırıldı. 1–8 araç için her iki sistem ayrı ayrı simüle edildi.
- **Bulgular (Findings):**

  | Araç | Statik (%) | Dinamik (%) | Fark (puan) | Üstün |
  |:---:|:---:|:---:|:---:|:---:|
  | 1 | 25.77 | — | — | — |
  | 4 | 19.31 | 24.58 | −5.27 | **Statik** |
  | 5 | 19.10 | 15.98 | +3.12 | **Dinamik ⚡** |
  | 8 | 18.68 | 3.50 | +15.18 | **Dinamik** |

- **Tartışma (Discussion):** 1-4 araçta statik sistem daha iyi (dinamiğin sinyal-reaksiyon gecikmesi dezavantaj). **5 araçtan itibaren dinamik sistem üstün** — bu geçiş noktası tezin en güçlü bulgusu. 8 araçta dinamik sistemi %5 hedefinin altına (%3.50) getirirken statik %18.68'de kalıyor. WIP-Starvation trade-off: Statik daha fazla stok tutarak düşük starvation sağlar; dinamik daha az stokla daha iyi performans elde eder (5+ araç).
- **Sevim & Aykut Karşılaştırması:** 3 araçlı senaryo (%36.11 starvation) Sevim & Aykut (2023) çalışmasıyla kıyaslanabilir niteliktedir.

### HAFTA 9: Sentez ve Pareto Analizi
- **Amaç (Objective):** WIP-Starvation trade-off'unu Pareto perspektifinden değerlendirmek, filo eşiğini belirlemek.
- **Bulgular (Findings):** Deterministik simülasyonla WIP ve starvation arasında tutarlı bir azalan getiri ilişkisi gözlemlendi. ⚠️ Bu haftanın filo eşiği bulguları tavansız modele dayanıyordu; Hafta 10 ERRATA'sıyla güncellendi.

### HAFTA 10: Kapsamlı Denetim ve Kanonik Motor
- **Amaç (Objective):** Önceki 9 haftanın tüm hesaplarını yeniden doğrulamak; fiziksel raf tavanı kısıtını uygulamak.
- **Yöntem (Methodology):** Raf tavanı ($stok \le N \times C$) kanonik motora eklendi (K57). 1920 senaryo (8 araç × 8 dispatch × 30 rep) yeniden üretildi. K63 dinamik SLACK formülü düzeltildi. K64: EDD vs SLACK istatistiksel test.
- **Bulgular (Findings):** Tavan kısıtı uygulandığında filo ihtiyacı sistematik olarak artmakta, önceki "5-6 araç yeterli" bulgusu geçersizleşmektedir. **%5 starvation eşiğine inmek için 8 araç gerekmektedir (%3.50)**. Kademeli filo azaltma (4→3→2→1) stres testi yapılarak ani filo kaybının etkisi incelendi.

### HAFTA 11–12: Dashboard — Karar Destek Arayüzü
- **Amaç (Objective):** Tüm simülasyon bulgularını interaktif bir web arayüzüne taşımak.
- **Bulgular (Findings):** 5 sekmeli dashboard tamamlandı: (1) KPI Özet, (2) What-If Simülatörü (araç slider + dinamik yorum), (3) İstasyon Haritası 6×4, (4) Statik vs Dinamik karşılaştırma tablosu, (5) Veri Girişi formu. 1920 senaryoluk veri gömülü olarak çalışıyor. `node --check` ile syntax doğrulandı.

### HAFTA 13: Saha Validasyonu
- **Amaç (Objective):** Gerçek fabrika verisiyle sistemin doğrulanması.
- **Durum:** Devam etmekte — `data/config.json → "real"` değişikliğiyle gerçek ERP verisi entegre edilecek.

---

> [!NOTE]
> **Gerçekleşmemiş Planlar (Gelecek Çalışma):**  
> - Python SimPy tam entegrasyonu (düşünüldü, uygulanmadı — mevcut ayrık olay simülatörü yeterli bulundu)  
> - Efrilianda et al. (2018) ve Demiray Kırmızı et al. (2024) formüllerinin doğrudan karşılaştırması (literatür taramasında incelendi, sistemimize entegre edilmedi — gelecek çalışma önerisi olarak bırakıldı)

---

*Bu rehber Eylül 2026 itibarıyla Hafta 13'e kadar güncellenmiştir.*

