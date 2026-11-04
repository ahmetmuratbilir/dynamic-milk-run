# DİNAMİK MİLK-RUN VE E-KANBAN KARAR DESTEK SİSTEMİ
## TEZ BİLGİ VE AKADEMİK METODOLOJİ MASTER REHBERİ (HAFTA 1 – 15)

> **Bu Dokümanın Amacı:** Bu dosya, projenin başından sonuna kadar (Hafta 1–14) elde edilen tüm teorik, mühendislik, matematik ve yazılımsal çıktılardan tezin Giriş, Literatür, Metodoloji ve Bulgular bölümlerinin doğrudan yazılabilmesini sağlayan **yaşayan akademik master dokümandır**.  
> **Son güncelleme:** 03.11.2026 — Hafta 15: dört adalet kuralı, sağlamlık testleri, nihai makale tabloları (K93–K105).
> **Makale sayıları yalnızca `docs/makale_tablolari.md`'den alınmalıdır (K105).**

> [!IMPORTANT]
> ## ⚠️ HAFTA 14 REVİZYONU — ÖNCE BUNU OKUYUN (30.09.2026)
>
> Masaüstündeki `dinamik milk run` klasöründeki 41 özgün çalışma tek tek incelenerek
> projenin 27 parametre/kararı kaynaklarıyla karşılaştırılmıştır. **Tezin iki temel sonucu
> revize edilmiştir.** Aşağıdaki bölümlerde H1–H13 metni **tarihsel kayıt olarak
> korunmuştur**; güncel sonuçlar için bu kutuya ve
> `docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md` dosyasına bakılmalıdır.
>
> | Konu | H1–H13 (v1) | Hafta 14 (v2) |
> |---|---|---|
> | Eşit WIP'te üstünlük | Statik 3–5 puan üstün (K53) | **Koşullu:** doyma altında statik hafif önde; sonuç **eşitleme kuralına bağlıdır** (K97): politika-tutarlı boyutlandırmada duruş farkı 1 puanın altında, üstünlük stokta (P3 %0,18 / 413 WIP ↔ P2 T=60 %0,49 / 673 WIP); eşit WIP'te dinamik **10,9 puan** önde |
> | %5 eşiği için filo | 8 araç (H10 ERRATA) | **Baz talepte 2, +%50 şokta 3 araç** |
> | Sevk kuralı | KRİTİKLİK anlamlı kötü, EDD öner (K45) | **Dört kural eşdeğer** (ANOVA p=0,9997 / 0,3415) |
> | Isınma süresi | 45 dk (varsayım) | **90 dk** (Welch ile ölçüldü, K78) |
> | Raf boyutlandırma | $N=\lceil ROP/C\rceil$ → 23/24 istasyonda $N=1$ | **$N = 1 + \lceil ROP/C\rceil$** (VDI 5586 "+1 değişim pozisyonu") |
> | Rotalama | "NN + 2-opt" (2-opt **kodda yoktu**) | Gerçek 2-opt; Solomon'da doğrulandı |
>
> **Üç yapısal sorunun ölçülen etkisi:** eksik raf boyutlandırma **−3,88 puan**,
> hizmet süresi asimetrisi (statik 3 dk / dinamik 8 dk per durak) **−10,34 puan**,
> açık döngü sinyal üretimi **%24,58 → %6,85**.

---

## 1. PROBLEM DEFINITION (Problem Tanımı)

- **Endüstriyel Bağlam:** Tam Zamanında (JIT) ve Yalın Üretim prensipleriyle çalışan montaj fabrikalarında (otomotiv, beyaz eşya), hat başı parça tedariği kritik bir lojistik operasyondur.
- **Gerçek Fabrika Problemi:** Tüketim hızlarının sabit olmaması, hat başında hem aşırı stok birikmesine (WIP maliyeti) hem de stoksuz kalma (starvation) sonucu montaj hattının durmasına neden olmaktadır.
- **Lojistik Kısıtlar:** Malzeme taşıma araçları (çekici-römork / tugger train) sınırlı zaman, hız, seyahat mesafesi ve taşıma kapasitesine sahiptir. Statik sipariş verme sistemleri bu dinamik kısıtları yönetmede yetersiz kalmaktadır.

---

## 2. RESEARCH GAP (Literatürdeki Eksiklik ve Katkımız)

> ⚠️ **26.10.2026'da tümüyle yeniden yazıldı.** Önceki metin *"E-Kanban sinyal üretimi ile
> VRPTW'yi entegre eden modeller kısıtlıdır"* diyordu. Yapılan genişletilmiş tarama bu
> iddianın **savunulamaz** olduğunu göstermiştir: Menanno vd. (2023), Vojdani & Drechsler
> (2022), Sevim & Görkemli Aykut (2026) ve Alnahhal vd. (2016) bu entegrasyonu zaten
> yapmıştır. Tam gerekçe, kanıt tablosu ve hakem yanıtları:
> **`docs/literatur_boslugu_analizi.md`**

### 2.1 Literatürdeki eksiklik: iki kol birleşmemiştir

Fabrika içi milk-run yazını bu konuda **iki ayrı kolda** gelişmiştir:

- **Kol A (boyutlandırma/planlama):** Gereken hat yanı tamponun ikmal politikasına bağlı
  olduğunu gösterir. Urru vd. (2018) s.407, *aynı veriyle* dört farklı yeniden sipariş
  yöntemi için planlamayı tekrarlamış ve tampon ihtiyacının 18'den 19/20/23'e çıktığını
  bulmuştur. Droste & Deuse (2011) s.607–608 gereken stokun çevrim süresiyle orantılı
  olduğunu; Schmidt vd. (2016) s.3–4 ve VDI 5586 Blatt 2 (2022) ise
  $q = 1 + \lceil n_{LT}\rceil$ formülünü verir. **Ancak bu kol politikaları performans
  açısından karşılaştırmaz.**
- **Kol B (politika karşılaştırma/simülasyon):** Politikaları duruş ve stok açısından
  karşılaştırır. Vojdani & Drechsler (2022) s.5 iki sistemi *"identisches Layout und
  identische Taktzeiten"* ve **aynı iki kutulu Kanban** ile karşılaştırır. Chee vd. (2012)
  s.392 push ve Kanban'a aynı {2,4,6} aralığını uygular. Alnahhal & Noche (2015) s.117
  Kanban sayısını *"fill rate ≥ %99"* ölçütüyle seçer. **Ancak bu kol tamponu politikanın
  kendi çevrim süresinden formülle türetmez.**

**Boşluk:** Tamponun politikaya bağlı olduğunu gösteren kol ile politikaları karşılaştıran
kol birleştirilmemiştir; bu birleşmemenin karşılaştırma sonuçlarını ne ölçüde etkilediği
ölçülmemiştir.

### 2.2 Bu tezin özgün katkısı (revize)

1. **Politika-tutarlı boyutlandırma ilkesi.** Her besleme politikasının hat yanı tamponu
   kendi çevrim süresinden türetilir. Bu yapılmadığında karşılaştırma sonucunun **yönünün**
   değiştiği gösterilmiştir: politika-tutarsız boyutlandırma ve asimetrik hizmet süreleri
   altında statik sistem üstün görünmektedir. Bağımsız bir çalışmanın karşılaştırma
   tasarımı (Vojdani & Drechsler 2022, ortak iki kutulu tampon) uygulandığında dijital
   sistem şokta **9,03 puan** önde görünürken, politika-tutarlı boyutlandırmada fark
   kapanır (K93); bu kayma Toyota parametre bandının 12 hücresinin tamamında sıralamayı
   değiştirir (K95). Düzeltme sonrası yeterli filoda politikalar arasındaki duruş farkı
   1 puanın altındadır; dinamik sistemin üstünlüğü stoktadır (K96). Dört eşitleme kuralı
   (eşit kart, politika-tutarlı, eşit hizmet düzeyi, eşit WIP) yan yana konduğunda
   kazanan kurala göre değişir (K97, Şekil 7).
2. **Modelleme kararlarının ayrıştırılmış etkisi.** Tampon boyutlandırma (−3,88 puan),
   hizmet süresi simetrisi (−10,34 puan), kapalı döngü sinyal üretimi (%24,58 → %6,85) ve
   metrik mesafe (−0,86 puan) katkıları tek tek ölçülmüştür. Bu etkiler, politikalar
   arasındaki gerçek farktan (≈1 puan) **büyüktür**.
3. **Tüketim hızından türetilen dinamik zaman penceresi** (K27/K30): teslim son tarihi
   istasyonun anlık stoku ve tüketim hızından hesaplanır; pencere istasyonun kırılganlığına
   göre kendiliğinden daralır. ⚠️ *K107: katkı değil, yöntem öğesidir — aynı mantık Lieb
   (2021, TUM doktora tezi, s.118–120)'de kullanılmıştır; atıf yapılmalıdır.*
4. **Koşullu ve dürüst raporlama:** üstünlük filo doygunluğuna bağlıdır; sevk kuralları
   arasında anlamlı fark bulunamamıştır (ANOVA p=0,9997 / 0,3415).

> **⚠️ İddia edilmeyecekler:** "E-Kanban + VRPTW entegrasyonu", "Kanban ↔ starvation
> ilişkisi", "filo ↔ stok ödünleşimi", "Pareto cephesi", "VDI +1 kuralı" ve
> **"$N = \lceil D\cdot LT(1+\alpha)/C\rceil$ formülü"** özgün katkı **değildir**;
> sırasıyla Menanno (2023), Ciemnoczolowski & Bozer (2013), Bocewicz vd. (2019),
> Zhou & Wen (2024), Urru vd. (2018) ve **Sugimori vd. (1977 — Toyota formülü, K88)**
> tarafından kapatılmıştır.

### 2.3 Boşluğun literatürce ilan edilmiş hâli (K89)

Kundu, Rossini & Portioli-Staudacher (2019) s.423, Monden (2011)'e dayanarak iki
politika ailesini tanımlar — *fixed quantity, variable time* = **reorder point**
(bu tezde **P3**) ve *fixed time, variable quantity* = **periodic review** (**P2**) —
ve şunu yazar:

> *"This research utilizes the fixed time, variable quantity solution and **does not
> investigate the differences with the other policy. This could however be the subject
> of future research.**"*

Bu alıntı **makalenin giriş bölümünde doğrudan kullanılmalıdır**: tezin doldurduğu
boşluk, literatürün kendisi tarafından açıkça ilan edilmiştir.

⚠️ Aynı sayfadaki karşı kanıt da dürüstçe aktarılmalıdır: *"The comparison of different
feeding policies has been relatively well covered"*. Dolayısıyla **"politika
karşılaştırması yapılmamıştır" denemez**; iddia yalnızca *boyutlandırmanın politikaya
göre türetilmesi ve etkisinin ölçülmesi* ile sınırlıdır.

### 2.4 ⚠️ Katkı gücünün dürüst değerlendirmesi (K91)

| Hedef | Yeterlilik |
|---|---|
| Lisans / YL tasarım çalışması | ✅ Fazlasıyla yeterli |
| **TR Dizin** (End. Müh. Dergisi, JTOM) | ⚠️ **Sınırda** — tek engel gerçek veri yokluğu |
| SCI-E | ❌ Katkı artımsaldır |

Katkı **metodolojiktir**, teknik değildir: yeni algoritma, yeni mimari veya yeni
ödünleşim keşfi yoktur. Güçlendirme yol haritası (etki sırasına göre):

1. 🔴 **Gerçek veri** — tek vardiya bile yeter; `config.json → "real"`. S1'i kapatır.
2. 🟠 **İddiayı küçült, kanıtı büyüt** — "entegre KDS geliştirdik" yerine
   *"boyutlandırma tutarsızlığı, politikalar arasındaki gerçek farktan büyük bir
   yanlılık üretir"* (10,34 vs ≈1 puan).
3. 🟠 **Katkıyı kendi modelinin dışına taşı** — Vojdani & Drechsler (2022) s.5'teki
   kurgu (aynı iki kutulu Kanban, farklı çevrim süreleri) v2'de yeniden kurulursa
   katkı genellenebilirlik kazanır. ≈ yarım saatlik iş; duyarlılık analizi olarak
   sunulmalı, çürütme olarak değil.

Ayrıntı: `docs/literatur_boslugu_analizi.md` Bölüm 10.

---

## 3. RESEARCH QUESTIONS (Araştırma Soruları)

> **Güncel araştırma soruları (Hafta 15, makale için):**
> - **AS1:** Periyodik (sabit takt) ve olay tabanlı (e-Kanban) besleme politikaları karşılaştırılırken hat yanı tamponun nasıl eşitlendiği, karşılaştırmanın sonucunu ne ölçüde belirler?
> - **AS2:** Yazında kullanılan dört eşitleme kuralı (eşit kart, politika-tutarlı formül, eşit hizmet düzeyi, eşit WIP) aynı sistemde hangi kazananları verir?
> - **AS3:** Bu etki Toyota formülünün parametre bandında, üç vardiyalık ufukta ve gerçekleşebilir bir mesafe ağında sürer mi?
> - **AS4:** Her politika kendi çevrim süresine göre boyutlandırıldığında politikalar duruş ve stokta nasıl ayrışır?
>
> Aşağıdaki RQ1–RQ4 v1 dönemine aittir ve tarihsel kayıt olarak korunmuştur.


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
| **K06** | Kanban Formülü | $N = \lceil (D \cdot LT \cdot (1+\alpha))/C_{kutu} \rceil$ | Standart Kanban boyutlandırma | Toyota formülü: Sugimori vd. (1977) s.561 (K88, K103) | H3 |
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

### HAFTA 14: Literatür Denetimi, v2 Motoru ve Doğrulama
- **Amaç (Objective):** Kaynak klasöründeki 41 özgün çalışmayla projenin tüm parametre ve
  kararlarını karşılaştırmak; tespit edilen yapısal sorunları gidermek; rotalama sezgiselini
  bağımsız bir kıyaslama setinde doğrulamak.
- **Yöntem (Methodology):** 45 PDF tarandı (9'u tam metin). 27 parametre/karar denetlendi.
  Düzeltmeler v1'i bozmadan `src/v2_entegre_simulasyon.py`'de toplandı (K65–K82).
  Doğrulama: Solomon VRPTW (OR-Tools referansı), tur-içi tam numaralama, Welch ısınma
  analizi, $2^5$ faktöriyel tasarım + ANOVA/Tukey.
- **Bulgular (Findings):**
  - Denetim: 7 doğrulandı, **8 atıf hatalı**, 6 literatürden sapma, 5 kaynaksız karar,
    **1 aktarım hatası** (K75: stokastik üreticide S10/S23 talepleri, toplam %9 fazla).
  - Düzeltmelerin ayrıştırılması: hizmet süresi asimetrisi **−10,34 puan**,
    kapalı döngü **%24,58 → %6,85**, raf boyutlandırma **−3,88 puan**, durak sınırı **+5,76**.
  - Faktöriyel ana etkiler (duruş): talep **+10,22** > filo **−9,55** > raf **−3,88** >
    α −1,35 (p=0,15) > sevk +0,93 (p=0,32). Doluluğa en güçlü etki: **sevk +20,19 puan**.
  - Solomon: en yakın komşu OR-Tools'tan **%102,7** daha uzun; fabrika içi tur-içi sapma
    yalnızca **%0,62** (turlar 2–8 duraklı olduğu için Solomon açığı bu bağlama taşınmaz).
  - Isınma süresi **90 dk** (45 dk'da WIP kararlı değerin %54 üzerindedir).
- **Tartışma (Discussion):** v1'deki yüksek duruş oranları (%24–53) ve yüksek filo ihtiyacı
  (8 araç), politika farkından değil **model kurma sorunlarından** kaynaklanmaktadır.
  Literatüre uygun boyutlandırmayla üç politika da baz talepte 2 araçla %5 eşiğinin
  altındadır; politikalar ancak **talep şoku altında ayrışır** (K81).
- **Sonraki Adım:** Mesafe matrisinin koordinatlardan üretilmesi (S10), çok vardiyalı
  koşular (S2), gerçek ERP verisi.

### HAFTA 15: Katkının Genelleştirilmesi, Sağlamlık ve Nihai Tablolar
- **Amaç (Objective):** Ana katkıyı kendi v1 modelimizin dışına taşımak, yazındaki
  eşitleme kurallarını karşılaştırmak, bulguyu farklı koşullarda sınamak ve makale
  tablolarını nihai ayarla üretmek.
- **Yöntem (Methodology):** Vojdani & Drechsler (2022) karşılaştırma tasarımının yeniden
  kurulması (K93); Toyota bandı α × kutu boyu ızgarası (K95); dört eşitleme kuralı ve
  kart taraması ile duruş–WIP eğrileri (K97); uyarlanan ROP (K98); 480/1440 dk ve ısınma
  dahil/hariç göstergeler (K99); koordinat tabanlı mesafe ağı (K100); OR-Tools çevrimdışı
  referansı (K101); nihai ayarla makale tabloları (K105).
- **Bulgular (Findings, nihai ayar — K105):**
  - Vojdani tasarımı (ortak iki kutulu tampon) dijital sistemi **2,4–16,0 puan** önde
    gösterir; politika-tutarlı boyutlandırmada fark %80–100 küçülür, Toyota kutularında
    yön döner. Kayma 36 bağımsız sağlamlık koşulunun 36'sında pozitiftir (52 test hücresi; K95'teki iki Q varyantı özdeş) (K95, K99, K100).
  - Dört eşitleme kuralı farkı **−17,3 ile +2,0 puan** arasında değiştirir; Toyota
    kutularında politika-tutarlı kural geleneksel sistemi, diğer üç kural dijital sistemi
    kazandırır; Pareto yargısı kurala göre değişir.
  - Politika-tutarlı tamponda P3 konsolidasyon, P2 (T=60 dk)'ye göre baz talepte 0,19,
    şokta 1,86 puan daha az duruş ve %37–41 daha az stokla çalışır.
  - Uyarlanan ROP küçük kutularda kart eklemekle eşdeğerdir (K98) — Sugimori vd. (1977,
    s.562)'nin "kanban sayısı sabit tutulur" ilkesiyle tutarlı.
  - Isınma dahil göstergeler duruşu ort. 1,15 puan düşük, WIP'i %5–37 yüksek gösterir (K99);
    mevcut mesafe matrisi yolu 2,5–3,5 kat şişirir ve Vojdani ile görünen çelişkinin
    kaynağıdır (K100).
- **Kaynaklar (K103, K104):** Sugimori (1977), Bozer & Ciemnoczolowski (2013) Part 1–2,
  Schmidt vd. (2016), Korytkowski & Karkoszka (2016) edinildi ve okundu; Kanban formülü
  asıl kaynağından doğrulandı. Alnahhal vd. (2016) edinilemedi.
- **Tartışma (Discussion):** Katkı yöntemseldir: karşılaştırma çalışmaları eşitleme kuralını
  açıkça belirtmeli ve sonuçlarını duruş–WIP düzleminde raporlamalıdır.
- **Sonraki Adım:** Makale metni; gerçek veri (H1).

---

> [!NOTE]
> **Gerçekleşmemiş Planlar (Gelecek Çalışma):**  
> - Python SimPy tam entegrasyonu (düşünüldü, uygulanmadı). ⚠️ **Terminoloji notu (H14):**
>   mevcut simülatör **1 dakikalık sabit zaman adımlı** (fixed-increment) bir modeldir;
>   metinde "ayrık olay simülasyonu" yerine bu terim kullanılmalıdır. SimPy'ye geçilecekse
>   klasördeki üç kaynak yöntem şablonu sunar: Pop vd. (2025), Dagkakis vd. (2015 — ManPy),
>   Ramirez Echavarria (2025 — 40 günlük veriyle doğrulanmış model).
> - Efrilianda et al. (2018) ve Demiray Kırmızı et al. (2024) formüllerinin doğrudan
>   karşılaştırması. ⚠️ **H14 düzeltmesi:** Demiray Kırmızı vd. **s.9 Tablo 3**'te
>   $SS = k\sigma_d\sqrt{L_t}$ formülü açıkça verilmektedir; K18'in "makalelerimizde bu
>   formül yok" ifadesi yanlıştır. İstatistiksel ROP'un kullanılmaması bir **tercihtir**
>   ve sınırlılık (S9) olarak yazılmalıdır.

---

*Bu rehber 03.11.2026 itibarıyla Hafta 15'e kadar güncellenmiştir (K01–K105).*
*Güncel sonuçlar için: `docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md`*

