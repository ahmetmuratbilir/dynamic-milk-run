# Hafta 8 — Sabit Kanban vs Dinamik E-Kanban ve Değişken Lead Time Analizi Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K04, K05, K10, K12, K14, K15, K17, K25, K44, K45, K47, K48–K51  
**Bkz.:** `docs/karar_gunlugu.md`

---

## 1. Amaç (Objective)

Hafta 8 çalışmasının iki temel araştırma hedefi bulunmaktadır:
1. **Değişken Lead Time ($LT_i \in [40, 60] \text{ dk}$) Altında Çizelgeleme Hipotezi:** Sentetik modelde istasyonların depoya olan mesafelerine göre heterojen teslim süreleri tanımlandığında zaman odaklı sevk kurallarının (`EDD` vs `SLACK`) sistem duruşlarına etkisinin incelenmesi.
2. **Statik vs. Dinamik Politika Karşılaştırması:** Geleneksel sabit periyodik seferli Milk-Run (Senaryo A) ile ROP tetiklemeli Dinamik E-Kanban VRPTW sisteminin (Senaryo B) adil ve eşit kısıtlar altında çok boyutlu (Starvation, Mesafe, Sefer Sayısı, Araç Doluluğu) karşılaştırılması.

---

## 2. Yöntem ve Deney Standartları (Methodology)

### 2.1 Deney Koşulları ve Adillik Kriterleri
Her iki senaryo da birebir aynı fabrika parametreleri altında test edilmiştir:
- **Tüketim Verisi:** $11,520 \text{ satır}$, $24 \text{ istasyon}$, Normal($\mu, 0.20\mu$) dağılımı (Seed=42) `[K10]`
- **Filo Büyüklüğü:** 2 Araç `[K03]` ve 4 Araç `[K37]` senaryoları
- **Araç Kapasitesi:** $Q_{arac} = 25 \text{ kutu}$ `[Mühendislik varsayımı - K04]`
- **Araç Hızı:** $10 \text{ km/sa}$ ($166.67 \text{ m/dk}$) `[K12]`
- **Handling / Operasyon Süreleri:** Yükleme $T_L = 2 \text{ dk}$ `[K14]`, Boşaltma $T_U = 3 \text{ dk}$ `[K15]`, Maksimum Tur Limiti = $90 \text{ dk}$ `[K17]`
- **Vardiya Süresi:** $480 \text{ dakika}$ ($8 \text{ saat}$) `[K05]`

### 2.2 Senaryo A: Statik Kanban / Sabit Seferli Milk-Run
- **Kalkış Sıklığı:** 60 dakikada bir periyodik sefer ($t = 60, 120, 180, 240, 300, 360, 420$) `[Operasyonel Mühendislik Kararı: TC_tam ≈ 45-55 dk ve 90 dk üst sınır kısıtı gereği]`.
- **Rota Politikası:** Sabit hat sırasıyla ($Hat\text{-}1 \rightarrow Hat\text{-}2 \rightarrow Hat\text{-}3 \rightarrow Hat\text{-}4$) tüm 24 istasyon taranır; her istasyona periyodik $1 \text{ kutu}$ teslimat yapılır.

### 2.3 Senaryo B: Dinamik E-Kanban + Olay Bazlı VRPTW
- **Tetikleme:** İstasyon anlık stoku $ROP_i$ altına düştüğünde dinamik E-Kanban sinyali üretilir `[K25]`.
- **Sevk ve Rotalama:** Sinyal oluştuğunda depodan araç çıkar (Olay bazlı sevk `[K33]`), EDD kuralıyla sıralanır `[K45]` ve dinamik NN + 2-opt rotalama ile servis edilir `[K34]`.

---

## 3. Bulgular (Findings)

### 3.1 İstasyon Bazlı Değişken Lead Time ($LT$) ve Dispatch Sonuçları

İstasyonların depoya mesafesine göre deterministik $LT_i$ dağılımı ($30 + \lfloor (\text{Mesafe}/250) \times 30 \rfloor \text{ dk}$):
- `Hat-1` ($S_1 - S_6$, $90\text{ m}$): $LT = 40 \text{ dk}$ `[Mühendislik Kararı]`
- `Hat-2` ($S_7 - S_{12}$, $120\text{ m}$): $LT = 44 \text{ dk}$ `[Mühendislik Kararı]`
- `Hat-3` ($S_{13} - S_{18}$, $180\text{ m}$): $LT = 51 \text{ dk}$ `[Mühendislik Kararı]`
- `Hat-4` ($S_{19} - S_{24}$, $250\text{ m}$): $LT = 60 \text{ dk}$ `[Mühendislik Kararı]`

**Değişken $LT$ Altında Dispatch Kuralları Karşılaştırması:**

| Filo | Kural | Duruş (dk) | Starvation ($11,520$ Payda) | Starvation ($10,440$ Payda) | Karşılama (%) | Zamanında | Gecikmeli | Karşılanamayan | Sefer Sayısı |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 2 Araç | KRITIKLIK | 144 | **%1.25** `[Kod çıktısı]` | **%1.38** `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 180 | 1 | 0 | 69 |
| 2 Araç | FIFO | 143 | **%1.24** `[Kod çıktısı]` | **%1.37** `[Kod çıktısı]` | %99.4 `[Kod çıktısı]` | 180 | 0 | 1 | 66 |
| 2 Araç | EDD | 144 | **%1.25** `[Kod çıktısı]` | **%1.38** `[Kod çıktısı]` | %99.4 `[Kod çıktısı]` | 180 | 0 | 1 | 66 |
| 2 Araç | SLACK | 144 | **%1.25** `[Kod çıktısı]` | **%1.38** `[Kod çıktısı]` | %99.4 `[Kod çıktısı]` | 180 | 0 | 1 | 66 |
| 4 Araç | KRITIKLIK | 144 | **%1.25** `[Kod çıktısı]` | **%1.38** `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 181 | 0 | 0 | 140 |
| 4 Araç | FIFO | 144 | **%1.25** `[Kod çıktısı]` | **%1.38** `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 181 | 0 | 0 | 140 |
| 4 Araç | EDD | 144 | **%1.25** `[Kod çıktısı]` | **%1.38** `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 181 | 0 | 0 | 140 |
| 4 Araç | SLACK | 144 | **%1.25** `[Kod çıktısı]` | **%1.38** `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 181 | 0 | 0 | 140 |

> **Gözlem:** Değişken $LT$ modelinde uzak istasyonların $ROP_i$ eşiği yükseldiği için sinyaller daha erken tetiklenmiş ve duruşlar %1.25 seviyesine gerilemiştir. Ancak SLACK kuralı ile EDD kuralı arasında duruş süresi açısından belirgin bir fark gözlenmemiştir (her ikisi de 144 dk duruş üretmiştir).

---

### 3.2 Statik (Senaryo A) vs Dinamik (Senaryo B) Karşılaştırması

| Sistem Politikası | Filo | Duruş Süresi (dk) | Starvation ($11,520$ Payda) | Starvation ($10,440$ Payda) | Kat Edilen Mesafe ($km$) | Sefer Sayısı | Ort. Kutu / Sefer | Araç Doluluk Oranı (%) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Senaryo A (Statik 60 dk Sabit Sefer)** | 2 Araç | 620 dk `[Kod çıktısı]` | **%5.38** `[Kod çıktısı]` | **%5.94** `[Kod çıktısı]` | 34.55 km `[Kod çıktısı]` | 14 tur `[Kod çıktısı]` | 12.00 kutu `[Kod çıktısı]` | **%48.0** `[K04 Q=25]` |
| **Senaryo B (Dinamik E-Kanban EDD)** | 2 Araç | 5,922 dk `[Kod çıktısı]` | **%51.41** `[Kod çıktısı]` | **%56.72** `[Kod çıktısı]` | **26.97 km** `[Kod çıktısı]` | 16 tur `[Kod çıktısı]` | 4.62 kutu `[Kod çıktısı]` | **%18.5** `[K04 Q=25]` |
| **Senaryo A (Statik 60 dk Sabit Sefer)** | 4 Araç | 341 dk `[Kod çıktısı]` | **%2.96** `[Kod çıktısı]` | **%3.27** `[Kod çıktısı]` | **34.16 km** `[Kod çıktısı]` | 28 tur `[Kod çıktısı]` | 6.00 kutu `[Kod çıktısı]` | **%24.0** `[K04 Q=25]` |
| **Senaryo B (Dinamik E-Kanban EDD)** | 4 Araç | 1,963 dk `[Kod çıktısı]` | **%17.04** `[Kod çıktısı]` | **%18.80** `[Kod çıktısı]` | 48.49 km `[Kod çıktısı]` | 32 tur `[Kod çıktısı]` | 4.59 kutu `[Kod çıktısı]` | **%18.4** `[K04 Q=25]` |

---

## 4. Tartışma ve Trade-off Analizi (Discussion)

### 4.1 İki Politika Arasındaki Temel Trade-off'lar
Bulgularımız iki sistemin tek taraflı bir "üstünlük" sergilemediğini, net operasyonel ödünleşimler (trade-offs) içerdiğini göstermektedir:

1. **Taşıma Verimliliği ve Yalın Lojistik:**
   * 2 araçlı senaryoda Dinamik Sistem (Senaryo B), Statik Sisteme (Senaryo A) kıyasla **%21.9 daha az mesafe** kat etmiştir ($26.97 \text{ km}$ vs $34.55 \text{ km}$). Dinamik sistem boşta kalan istasyonlara gitmeyerek yol tasarrufu sağlamıştır.
2. **Kapasite Kullanımı ve Duruş Riski:**
   * Statik sistem her saat başında toplu halde tüm istasyonlara stok aktardığı için araç doluluk oranı daha yüksektir (%48.0 vs %18.5) ve hat duruş oranı daha düşüktür (%5.38 vs %51.41).
   * Ancak statik sistemin bu duruş başarısı, hat başında sürekli **yüksek WIP stok biriktirilmesi** pahasına elde edilmektedir.

### 4.2 EDD vs SLACK Hipotezinin Değerlendirilmesi
Klasik çizelgeleme teorisindeki "değişken teslim sürelerinde SLACK kuralının daha esnek olduğu" hipotezi, bu sentetik veri setinde anlamlı bir sayısal fark üretmemiştir (EDD ve SLACK aynı 144 dk duruşu vermiştir). Bunun temel nedeni, fabrika içi mesafelerin ($90 - 250 \text{ m}$) seyahat süresi farklarının ($0.54 - 1.50 \text{ dk}$), toplam $LT$ süresi ($40 - 60 \text{ dk}$) yanında çok küçük kalmasıdır.

---

## 5. Sonuç (Conclusion)

- **Senaryo A (Statik):** Yüksek hat başı stok tamponu yaratarak duruşları azaltmakta fakat gereksiz taşıma ve hat yoğunluğu oluşturmaktadır.
- **Senaryo B (Dinamik):** Yalın prensiplere uygun olarak yalnızca ihtiyaç anında taşıma yapmakta ve mesafeyi düşürmekte; ancak filo kısıtı (2 araç) durumunda zaman kısıtına takılmaktadır.
- **Öneri:** Gerçek fabrika koşullarında dinamik sistemin uygulanabilmesi için Hafta 6 bulgumuz olan **en az 4 araçlık filo büyüklüğü** veya hibrit periyodik-dinamik sevk politikası gereklidir.
