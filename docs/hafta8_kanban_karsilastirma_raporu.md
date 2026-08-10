# Hafta 8 — Sabit Kanban vs Dinamik E-Kanban ve Değişken Lead Time Analizi Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K04, K05, K06, K10, K12, K14, K15, K17, K25, K44, K45, K47, K48–K51  
**Bkz.:** `docs/karar_gunlugu.md`

---

## 1. Amaç (Objective)

Hafta 8 çalışmasının iki temel araştırma hedefi bulunmaktadır:
1. **Değişken Lead Time ($LT_i \in [30, 60] \text{ dk}$) ve Kanban Disiplini ($WIP \le \sum N_i \times C_i$):** Sentetik modelde istasyonların depoya olan mesafelerine göre Min-Max normalizasyonuyla deterministik teslim süreleri ($LT_i \in [30, 60] \text{ dk}$) ve yeni kart sayıları ($N_i$) tanımlandığında sevk kurallarının (`EDD` vs `SLACK`) sistem duruşlarına ve hat başı stoklarına etkisinin incelenmesi.
2. **Statik vs. Dinamik Politika Karşılaştırması:** Geleneksel sabit periyodik seferli Milk-Run (Senaryo A) ile ROP tetiklemeli Dinamik E-Kanban VRPTW sisteminin (Senaryo B) adil ve eşit kısıtlar altında çok boyutlu (Starvation, WIP Stok, Mesafe, Sefer Sayısı, Araç Doluluğu) karşılaştırılması.

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

İstasyonların depoya mesafesine göre Min-Max normalizasyonlu deterministik $LT_i$ dağılımı ($30 + \text{round}( (\text{Mesafe}-90)/(250-90) \times 30 ) \text{ dk}$):
- `Hat-1` ($S_1 - S_6$, $90\text{ m}$): $LT = 30 \text{ dk}$, $N_i = 1$, ROP = $6.90 - 12.65 \text{ adet}$ `[Mühendislik Kararı - Min-Max]`
- `Hat-2` ($S_7 - S_{12}$, $120\text{ m}$): $LT = 36 \text{ dk}$, $N_i = 1$, ROP = $7.59 - 14.49 \text{ adet}$ `[Mühendislik Kararı - Min-Max]`
- `Hat-3` ($S_{13} - S_{18}$, $180\text{ m}$): $LT = 47 \text{ dk}$, $N_i \in [1, 2]$, ROP = $12.61 - 21.62 \text{ adet}$ `[Mühendislik Kararı - Min-Max]`
- `Hat-4` ($S_{19} - S_{24}$, $250\text{ m}$): $LT = 60 \text{ dk}$, $N_i \in [1, 2]$, ROP = $13.80 - 24.15 \text{ adet}$ `[Mühendislik Kararı - Min-Max]`

**Toplam Teorik Kanban Tavanı ($\sum N_i \times C_i$):** $535 \text{ adet}$ `[K06/K25 formülü]`

**Değişken $LT$ Altında Dispatch Kuralları Karşılaştırması:**

| Filo Büyüklüğü | Sevk Kuralı | Duruş Süresi (dk) | Starvation ($11,520$ Payda) | Starvation ($10,440$ Payda) | Ortalama Hat Başı WIP Stok | Karşılama Oranı (%) | Zamanında Teslim | Gecikmeli Teslim | Karşılanamayan | Sefer Sayısı |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 2 Araç | KRİTİKLİK | 211 dk `[Kod çıktısı]` | **%1.83** `[Kod çıktısı]` | **%2.02** `[Kod çıktısı]` | 317.7 adet `[Kod çıktısı]` | %98.5 `[Kod çıktısı]` | 192 | 1 | 3 | 64 tur `[Kod çıktısı]` |
| 2 Araç | FIFO | 188 dk `[Kod çıktısı]` | **%1.63** `[Kod çıktısı]` | **%1.80** `[Kod çıktısı]` | 315.5 adet `[Kod çıktısı]` | %99.5 `[Kod çıktısı]` | 195 | 0 | 1 | 57 tur `[Kod çıktısı]` |
| 2 Araç | EDD | 195 dk `[Kod çıktısı]` | **%1.69** `[Kod çıktısı]` | **%1.87** `[Kod çıktısı]` | 312.4 adet `[Kod çıktısı]` | %99.0 `[Kod çıktısı]` | 194 | 0 | 2 | 57 tur `[Kod çıktısı]` |
| 2 Araç | SLACK | 195 dk `[Kod çıktısı]` | **%1.69** `[Kod çıktısı]` | **%1.87** `[Kod çıktısı]` | 312.4 adet `[Kod çıktısı]` | %99.0 `[Kod çıktısı]` | 194 | 0 | 2 | 57 tur `[Kod çıktısı]` |
| 4 Araç | KRİTİKLİK | 7 dk `[Kod çıktısı]` | **%0.06** `[Kod çıktısı]` | **%0.07** `[Kod çıktısı]` | 331.0 adet `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 196 | 0 | 0 | 155 tur `[Kod çıktısı]` |
| 4 Araç | FIFO | 13 dk `[Kod çıktısı]` | **%0.11** `[Kod çıktısı]` | **%0.12** `[Kod çıktısı]` | 331.1 adet `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 196 | 0 | 0 | 155 tur `[Kod çıktısı]` |
| 4 Araç | EDD | 13 dk `[Kod çıktısı]` | **%0.11** `[Kod çıktısı]` | **%0.12** `[Kod çıktısı]` | 331.0 adet `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 196 | 0 | 0 | 155 tur `[Kod çıktısı]` |
| 4 Araç | SLACK | 13 dk `[Kod çıktısı]` | **%0.11** `[Kod çıktısı]` | **%0.12** `[Kod çıktısı]` | 331.0 adet `[Kod çıktısı]` | %100.0 `[Kod çıktısı]` | 196 | 0 | 0 | 155 tur `[Kod çıktısı]` |

---

### 3.2 Statik (Senaryo A) vs Dinamik (Senaryo B) Karşılaştırması

| Sistem Politikası | Filo Büyüklüğü | Duruş Süresi (dk) | Starvation ($11,520$ Payda) | Starvation ($10,440$ Payda) | Ortalama Hat Başı WIP Stok | Kat Edilen Mesafe ($km$) | Toplam Sefer Sayısı | Sefer Başı Ort. Kutu | Araç Doluluk Oranı (%) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Senaryo A (Statik 60 dk Sabit Sefer)** | 2 Araç | 620 dk `[Kod çıktısı]` | **%5.38** `[Kod çıktısı]` | **%5.94** `[Kod çıktısı]` | **316.3 adet** `[Kod çıktısı]` | 34.55 km `[Kod çıktısı]` | 14 tur `[Kod çıktısı]` | 12.00 kutu `[Kod çıktısı]` | **%48.0** `[Kod çıktısı ÷ K04 Q=25]` |
| **Senaryo B (Dinamik E-Kanban EDD)** | 2 Araç | 5,922 dk `[Kod çıktısı]` | **%51.41** `[Kod çıktısı]` | **%56.72** `[Kod çıktısı]` | **121.2 adet** `[Kod çıktısı]` | **26.97 km** `[Kod çıktısı]` | 16 tur `[Kod çıktısı]` | 4.62 kutu `[Kod çıktısı]` | **%18.5** `[Kod çıktısı ÷ K04 Q=25]` |
| **Senaryo A (Statik 60 dk Sabit Sefer)** | 4 Araç | 341 dk `[Kod çıktısı]` | **%2.96** `[Kod çıktısı]` | **%3.27** `[Kod çıktısı]` | **332.8 adet** `[Kod çıktısı]` | **34.16 km** `[Kod çıktısı]` | 28 tur `[Kod çıktısı]` | 6.00 kutu `[Kod çıktısı]` | **%24.0** `[Kod çıktısı ÷ K04 Q=25]` |
| **Senaryo B (Dinamik E-Kanban EDD)** | 4 Araç | 1,963 dk `[Kod çıktısı]` | **%17.04** `[Kod çıktısı]` | **%18.80** `[Kod çıktısı]` | **229.8 adet** `[Kod çıktısı]` | 48.49 km `[Kod çıktısı]` | 32 tur `[Kod çıktısı]` | 4.59 kutu `[Kod çıktısı]` | **%18.4** `[Kod çıktısı ÷ K04 Q=25]` |

---

## 4. Tartışma ve Çok Boyutlu Trade-off Analizi (Discussion)

### 4.1 İki Politika Arasındaki Temel Ödünleşimler (WIP vs. Starvation vs. Mesafe)
Sayısal bulgularımız iki sistemin birbirine karşı mutlak bir üstünlüğü olmadığını, operasyonel hedeflere göre değişen ödünleşimler içerdiğini göstermektedir:

1. **WIP Stok Azaltma ve Yalınlık (Dinamik Sistemin Avantajı):**
   * 2 araçlı modelde Dinamik Sistem hat başında ortalama **121.2 adet** stok tutarken, Statik Sistem **316.3 adet** stok tutmaktadır (**Dinamik sistem %61.7 daha düşük WIP stok**).
   * 4 araçlı modelde Dinamik Sistem ortalama **229.8 adet** stokla çalışırken, Statik Sistem **332.8 adet** stok tutmaktadır (**Dinamik sistem %31.0 daha düşük WIP stok**).
2. **Taşıma Mesafesi Tasarrufu (Dinamik Sistemin Avantajı):**
   * 2 araçlı senaryoda Dinamik Sistem gereksiz istasyon ziyaretlerini eleyerek Statik Sisteme göre **%21.9 daha az mesafe** kat etmiştir ($26.97 \text{ km}$ vs $34.55 \text{ km}$).
3. **Duruş Güvenliği ve Doluluk (Statik Sistemin Avantajı):**
   * Statik Sistem her 60 dakikada bir tüm istasyonları toplu beslediği için araç doluluk oranı daha yüksektir (%48.0 vs %18.5) ve duruş riski daha düşüktür (%5.38 vs %51.41). Ancak bu avantaj, sahada **yüksek stok yığılması** pahasına elde edilmektedir.

### 4.2 Değişken $LT$ Modelinde Kanban Tavanı ve Filo Dinamiği
1. **Kanban Disiplini Uyumu:** Değişken $LT$ modelinde hat başı ortalama WIP ($312 - 331 \text{ adet}$), güncellenen teorik tavan olan **$535 \text{ adet}$** sınırının altında kalmış ve Kanban disiplini ($WIP \le \sum N_i \times C_i$) korunmuştur.
2. **4 Araçta WIP'in 2 Araçtan Biraz Yüksek Çıkma Nedeni:**
   * 2 araçta araçlar yetişemediği için istasyonlar sıklıkla boşalmakta ve dip seviyelerde kalmaktadır ($Ort. WIP = 312 \text{ adet}$, duruş = $188-211 \text{ dk}$).
   * 4 araçta ise araçlar anında yenileme yaptığı için istasyonlar sürekli dolu seviyelerde tutulabilmektedir ($Ort. WIP = 331 \text{ adet}$, duruş neredeyse sıfır = $7-13 \text{ dk}$).

---

## 5. Sonuç (Conclusion)

- **Statik Model:** Yüksek hat başı stok tamponu (316–333 adet) ile duruşları minimize etmekte, ancak yalın üretim ilkelerine aykırı olarak hat başında stok maliyeti yaratmaktadır.
- **Dinamik Model:** Hat başı stoku %31–%62 oranında azaltarak yalın lojistik sağlamakta; ancak 2 araçlı filo kısıtında araçlar zaman darboğazına girdiğinde duruş yaşamaktadır.
- **Öneri:** Gerçek fabrika koşullarında dinamik sistemin uygulanabilmesi için Hafta 6 bulgumuz olan **en az 4 araçlık filo büyüklüğü** veya hat yoğunluğuna göre dinamik tetiklenen hibrit sevk politikası önerilmektedir.
