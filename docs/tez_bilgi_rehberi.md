# DİNAMİK MİLK-RUN VE E-KANBAN KARAR DESTEK SİSTEMİ
## TEZ BİLGİ VE AKADEMİK METODOLOJİ MASTER REHBERİ (HAFTA 1 – 5)

> **Bu Dokümanın Amacı:** Bu dosya, projenin başından sonuna kadar (Hafta 1 – 17) elde edilen tüm teorik, mühendislik, matematik ve yazılımsal çıktılardan tezin Giriş, Literatür, Metodoloji ve Bulgular bölümlerinin doğrudan yazılabilmesini sağlayan **yaşayan akademik master dokümandır**.

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
| **K07** | Lead Time | $LT = 45$ dakika | Tedarik döngü süresi | Klenk et al. (2012) s.12 | H3 |
| **K08** | Tampon Oranı | $\alpha = 0.15$ (%15) | Güvenlik stoku payı | Klenk et al. (2012) s.12 | H3 |
| **K16** | TW Üst Sınır | Max +60 dakika | Zaman penceresi genişliği | Mühendislik Varsayımı | H4 |
| **K17** | Max Tur Süresi | 90 dakika / tur | Tur başı süre limiti | Mühendislik Varsayımı | H5 |
| **K25** | ROP Formülü | $ROP = D_{dk} \cdot LT \cdot (1+\alpha)$ | Oransal tamponlu eşik | Klenk et al. (2012) s.12 | H4 |
| **K26** | Sinyal Önceliği | Karma (Kritiklik + FIFO) | Starvation önleme | Facchini (2022) s.2, Simić (2020) s.5 | H4 |
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

### HAFTA 6 (GELECEK PLAN): Araç Sayısı ve Duyarlılık Analizi
- **Amaç (Objective):** 2 araçlı sistemdeki %52.08 starvation oranını düşürmek için araç sayısını (2 vs 3 vs 4) ve tur parametrelerini analitik ve simülasyon temelli duyarlılık analizine tabi tutmak.
- **Akademik Formül & Yöntem (Körösi & Duchoň, 2026 - Nature):**
  - **Analitik Filo İhtiyacı Formülü:**
    $$WL = w \times TC = \left(\sum F_{ij}\right) \times \left( T_L + \frac{L_d}{v_c} + T_U + \frac{L_e}{v_c} \right)$$
    $$AT = 60 \times A \times F_t \times E_w$$
    $$AN = \frac{WL}{AT} \implies AN_{final} = \lceil AN \rceil$$
  - Burada $F_t$ (trafik kısıtı) ve $E_w$ (operatör verimliliği) parametreleri duyarlılık değişkeni olarak kullanılacaktır.
- **Beklenen Katkı:** 2 araç yetersizliğinin sadece deneysel değil, Nature (2026) analitik filo formülüyle teorik ispatı sağlanacaktır.

### HAFTA 7–8 (GELECEK PLAN): SimPy Simülasyonu ve Darboğaz Giderimi
- **Amaç (Objective):** VRPTW motorunu Python SimPy ortamına tam entegre etmek, ısınma (warm-up) ve replikasyon standartlarını oturtmak.
- **Akademik Referanslar:**
  - **Herrera-Vidal et al. (2026):** SimPy simülasyonlarında 50 replikasyon ve 30 dk Welch warm-up analizi (Bizim K32: 45 dk ısınma kararımızın doğrulaması).
  - **Wang (2008):** Filo kısıtlı m-VRPTW amaç fonksiyonu: $\min [ -\sum \text{Müşteri}, \sum \text{Mesafe}, \sum \text{Araç} ]$.

### HAFTA 9–10 (GELECEK PLAN): Sabit Kanban vs Dinamik E-Kanban Karşılaştırma Deneyleri
- **Amaç (Objective):** Geleneksel Sabit Kanban ROP modeli ile bizim Dinamik E-Kanban modelimizi kıyaslamak.
- **Akademik Referanslar & Formüller:**
  - **Sabit Kanban Referans Formülü (Efrilianda et al., 2018):**
    $$ROP_{sabit} = L_j \times \left( \frac{\sum D_t}{t} \right) + \left[ \sum B_t - (1 - SL) \sum D_t \right]$$
  - **Dinamik E-Kanban Formülü (Demiray Kırmızı et al., 2024 & Bizim K25):**
    $$SS = k \cdot \sigma_d \cdot \sqrt{Lt} + DOH_{ABC-XYZ} \cdot d_{daily}$$

---

*Bu rehber her yeni haftada elde edilen bulgu, kod ve kararlarla güncellenecektir.*
