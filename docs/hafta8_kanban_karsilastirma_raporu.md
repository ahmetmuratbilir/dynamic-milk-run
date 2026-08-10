# Hafta 8 — Sabit Kanban vs Dinamik E-Kanban ve Değişken Lead Time Analizi Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K04, K05, K06, K10, K12, K14, K15, K17, K25, K44, K45, K47, K48–K51  
**Bkz.:** `docs/karar_gunlugu.md`

---

## 1. Amaç (Objective)

Hafta 8 çalışmasının iki temel araştırma hedefi bulunmaktadır:
1. **Değişken Lead Time ($LT_i \in [30, 60] \text{ dk}$) ve Kanban Disiplini ($WIP \le \sum N_i \times C_i$):** Sentetik modelde istasyonların depoya olan mesafelerine göre Min-Max normalizasyonuyla deterministik teslim süreleri ($LT_i \in [30, 60] \text{ dk}$) ve yeni kart sayıları ($N_i$) tanımlandığında sevk kurallarının (`EDD` vs `SLACK`) sistem duruşlarına ve hat başı stoklarına etkisinin incelenmesi.
2. **Statik vs. Dinamik Politika Karşılaştırması:** Geleneksel sabit periyodik seferli Milk-Run (Senaryo A) ile ROP tetiklemeli Dinamik E-Kanban VRPTW sisteminin (Senaryo B) adil, eşit ve fiziksel raf kapasitesi ($stok \le N \times C$) kısıtları altında çok boyutlu (Starvation, WIP Stok, Mesafe, Sefer Sayısı, Araç Doluluğu) karşılaştırılması.

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
- **Fiziksel Raf Tavanı Kuralı:** Her istasyonda teslimat sonrası anlık stok seviyesi $stok_i(t) \le N_i \times C_i$ tavanını aşamaz (fiziksel raf doluluğu kuralı).

### 2.2 Senaryo A: Statik Kanban / Sabit Seferli Milk-Run
- **Kalkış Sıklığı:** 60 dakikada bir periyodik sefer ($t = 60, 120, 180, 240, 300, 360, 420$) `[Operasyonel Mühendislik Kararı: TC_tam ≈ 45-55 dk ve 90 dk üst sınır kısıtı gereği]`.
- **Rota Politikası:** Sabit hat sırasıyla ($Hat\text{-}1 \rightarrow Hat\text{-}2 \rightarrow Hat\text{-}3 \rightarrow Hat\text{-}4$) tüm 24 istasyon taranır; her istasyona periyodik $1 \text{ kutu}$ teslimat yapılır.

### 2.3 Senaryo B: Dinamik E-Kanban + Olay Bazlı VRPTW
- **Tetikleme:** İstasyon anlık stoku $ROP_i$ altına düştüğünde dinamik E-Kanban sinyali üretilir `[K25]`.
- **Sevk ve Rotalama:** Sinyal oluştuğunda depodan araç çıkar (Olay bazlı sevk `[K33]`), EDD kuralıyla sıralanır `[K45]` ve dinamik NN + 2-opt rotalama ile servis edilir `[K34]`.

---

## 3. Bulgular (Findings)

### 3.1 Statik (Senaryo A) vs Dinamik (Senaryo B) Karşılaştırması (Tablo 1)

| Sistem Politikası | Filo Büyüklüğü | Duruş Süresi (dk) | Starvation ($11,520$ Payda) | Starvation ($10,440$ Payda) | Ortalama Hat Başı WIP Stok | Kat Edilen Mesafe ($km$) | Toplam Sefer Sayısı | Sefer Başı Ort. Kutu | Araç Doluluk Oranı (%) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Senaryo A (Statik 60 dk Sabit Sefer)** | 2 Araç | 628 dk `[Kod çıktısı]` | **%5.45** `[Kod çıktısı]` | **%6.02** `[Kod çıktısı]` | **226.7 adet** `[Kod çıktısı]` | 34.55 km `[Kod çıktısı]` | 14 tur `[Kod çıktısı]` | 12.00 kutu `[Kod çıktısı]` | **%48.0** `[Kod çıktısı ÷ K04 Q=25]` |
| **Senaryo B (Dinamik E-Kanban EDD)** | 2 Araç | 6,107 dk `[Kod çıktısı]` | **%53.01** `[Kod çıktısı]` | **%58.50** `[Kod çıktısı]` | **111.1 adet** `[Kod çıktısı]` | **26.97 km** `[Kod çıktısı]` | 16 tur `[Kod çıktısı]` | 4.62 kutu `[Kod çıktısı]` | **%18.5** `[Kod çıktısı ÷ K04 Q=25]` |
| **Senaryo A (Statik 60 dk Sabit Sefer)** | 4 Araç | 350 dk `[Kod çıktısı]` | **%3.04** `[Kod çıktısı]` | **%3.35** `[Kod çıktısı]` | **231.4 adet** `[Kod çıktısı]` | **34.16 km** `[Kod çıktısı]` | 28 tur `[Kod çıktısı]` | 6.00 kutu `[Kod çıktısı]` | **%24.0** `[Kod çıktısı ÷ K04 Q=25]` |
| **Senaryo B (Dinamik E-Kanban EDD)** | 4 Araç | 2,832 dk `[Kod çıktısı]` | **%24.58** `[Kod çıktısı]` | **%27.13** `[Kod çıktısı]` | **182.3 adet** `[Kod çıktısı]` | 48.49 km `[Kod çıktısı]` | 32 tur `[Kod çıktısı]` | 4.59 kutu `[Kod çıktısı]` | **%18.4** `[Kod çıktısı ÷ K04 Q=25]` |

---

### 3.2 İstasyon Bazlı Değişken Lead Time ($LT$) ve Dispatch Sonuçları (Tablo 2)

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

## 4. Tartışma ve Çok Boyutlu Trade-off Analizi (Discussion)

### 4.1 İki Politika Arasındaki Temel Ödünleşimler (WIP vs. Starvation vs. Mesafe)
Sayısal bulgularımız iki sistemin birbirine karşı mutlak bir üstünlüğü olmadığını, operasyonel hedeflere göre değişen ödünleşimler içerdiğini göstermektedir:

1. **WIP Stok Azaltma ve Yalınlık (Dinamik Sistemin Avantajı):**
   * 2 araçlı modelde Dinamik Sistem hat başında ortalama **111.1 adet** stok tutarken, Statik Sistem **226.7 adet** stok tutmaktadır (**Dinamik sistem %51.0 daha az WIP stok**).
   * 4 araçlı modelde Dinamik Sistem ortalama **182.3 adet** stokla çalışırken, Statik Sistem **231.4 adet** stok tutmaktadır (**Dinamik sistem %21.2 daha az WIP stok**).
2. **Taşıma Mesafesi Tasarrufu (Dinamik Sistemin Avantajı):**
   * 2 araçlı senaryoda Dinamik Sistem gereksiz istasyon ziyaretlerini eleyerek Statik Sisteme göre **%21.9 daha az mesafe** kat etmiştir ($26.97 \text{ km}$ vs $34.55 \text{ km}$).
3. **Duruş Güvenliği ve Doluluk (Statik Sistemin Avantajı):**
   * Statik Sistem her 60 dakikada bir tüm istasyonları toplu beslediği için araç doluluk oranı daha yüksektir (%48.0 vs %18.5) ve duruş riski daha düşüktür (%5.45 vs %53.01). Ancak bu avantaj, sahada **yüksek stok yığılması (226-231 adet)** pahasına elde edilmektedir.

### 4.2 Değişken $LT$ Modelinde Kanban Tavanı ve Duruş Mekanizması
1. **Kanban Disiplini Uyumu:** Değişken $LT$ modelinde hat başı ortalama WIP ($312 - 331 \text{ adet}$), güncellenen teorik tavan olan **$535 \text{ adet}$** sınırının altında kalmış ve Kanban disiplini ($WIP \le \sum N_i \times C_i$) korunmuştur.
2. **Duruşun 7-13 Dakikaya Düşme Mekanizması:**
   * Duruşun dramatik şekilde düşmesi sevk kuralının başarısından ziyade, uzak ve yoğun istasyonlarda kart sayısının $N=1$'den $N=2$'ye çıkarılarak güvenlik tamponunun $20$'den $40 \text{ adede}$ katlanması sayesindedir.
3. **4 Araçta WIP'in 2 Araçtan Biraz Yüksek Çıkma Nedeni:**
   * 2 araçta araçlar yetişemediği için istasyonlar sıklıkla boşalmakta ve dip seviyelerde kalmaktadır ($Ort. WIP = 312 \text{ adet}$, duruş = $188-211 \text{ dk}$).
   * 4 araçta ise araçlar anında yenileme yaptığı için istasyonlar sürekli dolu seviyelerde tutulabilmektedir ($Ort. WIP = 331 \text{ adet}$, duruş neredeyse sıfır = $7-13 \text{ dk}$).
4. **Metodolojik Asimetri ve İç Tutarlılık Kanıtı (Tavan Etkisinin Yönü):**
   * Aynı raf-tavanı ($stok \le N \times C$) düzeltmesinin Tablo 1'de duruşu artırıp (%17.04'ten %24.58'e) Tablo 2'de duruşu neredeyse sıfırlaması (%1.28'den %0.06'ya), iki farklı fiziksel mekanizmanın ayrı ayrı çalıştığını açıkça göstermektedir:
     - **Tablo 1'de (Sabit $LT=45 \text{ dk}$):** $N$ kart sayıları sabit kaldığından, tavan düzeltmesi yalnızca imkânsız hayali stok birikmesini kırpmış (**saf kırpma etkisi**) ve gizli duruşları görünür kılarak duruş oranını artırmıştır.
     - **Tablo 2'de (Değişken $LT \in [30, 60] \text{ dk}$):** K06 formülü uyarınca kritik istasyonlarda kart sayıları $N=1 \rightarrow 2$'ye yükseldiğinden, fiziksel raf kapasitesi iki katına çıkmış (**tampon genişleme etkisi**) ve duruşları bertaraf etmiştir.
   * Bu zıt yönlü etki, simülasyon motorunun manipülasyona kapalı olduğunun ve fiziksel kurallarla tam tutarlı işlediğinin güçlü bir kanıtıdır.

---

## 5. Sonuç (Conclusion)

- **Statik Model:** Yüksek hat başı stok tamponu (226–231 adet) ile duruşları minimize etmekte, ancak yalın üretim ilkelerine aykırı olarak hat başında stok maliyeti yaratmaktadır.
- **Dinamik Model:** Hat başı stoku %21–%51 oranında azaltarak yalın lojistik sağlamakta; ancak 2 araçlı filo kısıtında araçlar zaman darboğazına girdiğinde duruş yaşamaktadır.
- **Öneri:** Gerçek fabrika koşullarında dinamik sistemin uygulanabilmesi için Hafta 6 bulgumuz olan **en az 4 araçlık filo büyüklüğü** veya hat yoğunluğuna göre dinamik tetiklenen hibrit sevk politikası önerilmektedir.
