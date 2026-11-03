# Hafta 14 — Literatür Denetimi, Model Revizyonu ve Doğrulama Raporu

**Tarih:** 30.09.2026
**Kapsam:** Masaüstü `dinamik milk run` klasöründeki 45 PDF (41 özgün çalışma) ile projenin
27 parametre/kararının karşılaştırılması; tespit edilen sorunların v2 motorunda giderilmesi;
Solomon kıyaslaması, Pareto analizi ve faktöriyel deney tasarımı.

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`
> **v1 motoru korunmuştur.** Hafta 4–13 raporlarındaki tüm sayılar v1 ile üretilmiştir ve
> bu revizyonda **değiştirilmemiştir**. Düzeltmeler `src/v2_entegre_simulasyon.py` altındadır.
> Bu rapor, iki motorun farklarını ve farkların nereden geldiğini belgelemektedir.

---

## 1. Yönetici Özeti

Denetim, projenin parametre tabanının büyük ölçüde savunulabilir olduğunu; buna karşılık
üç yapısal sorunun ana bulguları doğrudan etkilediğini ortaya koymuştur.

| # | Bulgu | Ölçülen etki |
|---|---|---|
| 1 | **Raf eksik boyutlandırılmış** (24 istasyonun 23'ünde $N=1$); VDI 5586'nın zorunlu kıldığı "+1 değişim pozisyonu" yok | Duruş **−3,88 puan** (p<0,001) |
| 2 | **Hizmet süresi asimetrisi**: dinamik 8 dk/durak, statik 3 dk/durak | Duruş **−10,34 puan** (en büyük tek etken) |
| 3 | **Açık döngü**: sinyaller LT=45 dk varsayımıyla önceden üretiliyor, gerçek teslimlere bağlı değil | Duruş %24,58 → **%6,85** |

Bu üç düzeltme birlikte uygulandığında projenin iki temel sonucu değişmektedir:

- **"Statik sistem eşit WIP'te 3–5 puan üstündür" (K53) koşullu hâle gelmiştir.** Araç
  yetersizken statik hâlâ hafif önde; yeterli filoda duruş farkı 1 puanın altındadır ve
  dinamik sistemin üstünlüğü **stoktadır** (⚠️ K96 errata: önceki "13,6 puan" ifadesi
  güncel ızgarayla uyuşmuyor, bkz. 6.2). Ayrıca dinamik sistem aynı duruş oranını belirgin daha az stokla sağlar.
- **"KRİTİKLİK anlamlı biçimde kötüdür, EDD'ye geçilmeli" (K45) desteklenmemektedir.**
  v2'de dört sevk kuralı arasında istatistiksel fark yoktur (p=0,9997 ve p=0,3415).

Ek olarak iki metodolojik düzeltme yapılmıştır: **ısınma süresi 45 dk değil 90 dk**
(Welch yöntemiyle ilk kez ölçüldü) ve **rotalama sezgiseli Solomon kıyaslamasında
ilk kez doğrulandı**.

---

## 2. İncelenen Literatür

**41 özgün çalışma** (45 PDF; 4'ü kopya). Tam metin okunanlar: Klenk vd. (2012),
Droste & Deuse (2011), Urru vd. (2018), Simić vd. (2020), Facchini vd. (2022),
Vojdani & Drechsler (2022), Sevim & Görkemli Aykut (2026), Menanno vd. (2023),
Tissir vd. (2020). Kalan 32 çalışma yöntem, parametre, bulgu ve sonuç bölümlerinden
hedefli olarak tarandı.

**Katalog dışı iki tespit:**

1. `LOGISTIQUA_2020_paper_166.pdf` (Tissir, El Fezazi & Cherrafi, 2020 — *Industry 4.0
   impact on Lean Manufacturing*) proje deposunda **yoktu**; giriş/motivasyon bölümü için
   kullanılabilir (Tablo 1: e-Kanban'ın Endüstri 4.0 ile ilişkisi).
2. CARV 2011 bildiri kitabından (`978-3-642-23860-4.pdf`) yalnızca **içindekiler** metne
   çıkarılmıştı. Kitabın s.605–610'undaki **Droste & Deuse (2011)** bildirisi projeyle
   doğrudan ilgilidir (çevrim süresi–stok ilişkisi, iki kutu prensibi, MTM ile süre
   modelleme) ve bu denetimde ilk kez okunmuştur.
3. `BM2409-012_Updated.pdf` ("The Cognitive Costs of Multitasking") konuyla ilgisizdir;
   klasörden çıkarılması önerilir.

---

## 3. Parametre Denetimi — Özet

| Sonuç | Sayı | Kararlar |
|---|---|---|
| Doğrulandı | 7 | LT (kısmen), araç kapasitesi, hız, yükleme süresi, statik 60 dk tur, replikasyon sayısı, Körösi filo formülü |
| **Atıf hatalı** | 8 | K06, K09, K18, K24, K34, K44 (×2), S6 |
| **Literatürden sapma** | 6 | N=1 raf, mesafe, hizmet süresi, tur süresi, TW genişliği, TW türü |
| Kaynaksız mühendislik kararı | 5 | α, 80 dk kanonik tur, talep dağılımı, ısınma süresi, %5 eşiği |
| **Aktarım hatası** | 1 | K75 (stokastik üreticide S10/S23) |

Karar bazında tam liste ve düzeltilmiş dayanaklar: `docs/karar_gunlugu.md` → **D-GRUBU**
tablosu ve **K65–K82**.

### 3.1 Öne çıkan atıf düzeltmeleri

- **K18 tersine döndü.** "Makalelerimizde $z\sigma\sqrt{LT}$ formülü yok" ifadesi yanlıştı;
  Demiray Kırmızı vd. (2024) *Systems* 12:260, **s.9 Tablo 3** bu formülü açıkça verir
  ($SS = k\sigma_d\sqrt{L_t}$). İstatistiksel ROP'un kullanılmaması bir **tercihtir**,
  kaynak yokluğu değil — sınırlılık olarak yazılmalıdır.
- **K24'ün yönü tersti.** Jarupathirun vd. (2009) Tablo 1–2: 255 dk → 190 dk, yani
  e-Kanban ile **%25 kısalma**. Bu bir LT *uzaması* kanıtı değil, e-Kanban lehine
  **destekleyici** bulgudur.
- **K44'te var olmayan sayfalara atıf.** Wang vd. (2008) s.128'de başlar; "s.48/s.52"
  mevcut değildir ve makalede EDD/SLACK geçmez. Gerçek dayanak: Vojdani & Drechsler
  (2022) s.5 ("Aufträge nach ihren Bedarfszeitpunkten sortiert").
- **S6 kapatıldı.** Vojdani & Drechsler (2022) s.6 doğrulandı: *"im Stundentakt … auf einer
  festen Route"*; ayrıca dijitalleşmeyle %27 daha az sefer, %29,39 daha az yol, %38,5 daha
  az sürüş süresi.
- **FIFO erratası geri alındı.** Herrera-Vidal vd. (2026) s.8'de FIFO kuyruk disiplini
  açıkça geçmektedir; 03.09.2026 tarihli errata fazla ileri gitmişti.

---

## 4. v2 Motoru: Yapılan Düzeltmeler

`src/v2_entegre_simulasyon.py` — 1 dakikalık **sabit zaman adımlı** (fixed-increment)
simülasyon. *Not: metinde "ayrık olay simülasyonu" yerine bu terim kullanılmalıdır.*

| Karar | Düzeltme | Dayanak |
|---|---|---|
| K65 | Raf: $N = 1 + \lceil ROP/C\rceil$ (+1 değişim pozisyonu) | Urru s.406; Klenk s.11; Vojdani s.5; Droste & Deuse s.607 |
| K66 | Tek hizmet süresi modeli (tüm politikalar) | Urru s.408; K14/K15 |
| K67 | "5 durak/tur" sınırı kaldırıldı | Simić s.8 ve Urru s.408 yanlış yorumlanmıştı |
| K68 | Konsolidasyonlu sevk (en geç kalkış) | Vojdani s.5–6; Sevim s.66; Menanno s.13–14 |
| K69 | Kapalı döngü entegrasyon | Facchini s.1126; Sevim s.66 |
| K70 | Saatlik rejim talebi (CV=0,20 korunur) | K10'un amaçlanan anlamı |
| K71 | Floyd–Warshall metrik kapanış (286 çift kısaldı) | Üçgen eşitsizliği ihlali |
| K72 | VRP-RTW + tur süresi kısıtı + gerçek 2-opt | Fitrie 2025; Facchini s.1124 Denk.7; Gendreau & Tarantilis Böl.1.1 |
| K73 | Üç politikalı set (P1/P2/P3), her biri kendi formülüyle | Klenk s.6; Simić s.10–11; Vojdani s.6; Facchini s.1123 |
| K74 | Koşu-içi dinamik N seçeneği | Elloumi s.613 |
| K77 | Başlangıç stoku seçeneği | K78'in gereği |
| K78 | Isınma 90 dk (Welch ile ölçüldü) | Herrera-Vidal s.9 |

### 4.1 Düzeltmelerin ayrıştırılması (m=4, kümülatif)

v1 ayarlarından başlanarak düzeltmeler tek tek eklenmiştir
(`src/v2_dogrulama_ve_kalibrasyon.py`, D4/D5):

| Adım | Duruş (%) | Δ (puan) | WIP | Tur | Doluluk (%) |
|---|---:|---:|---:|---:|---:|
| v1 ayarları (kapalı döngü hariç her şey v1) | 6,85 | — | 238,7 | 43 | 19,0 |
| + K71 metrik mesafe | 5,99 | −0,86 | 242,8 | 43 | 19,0 |
| + K72 2-opt & tur süresi | 5,03 | −0,95 | 246,5 | 43 | 19,1 |
| + K67 durak sınırı kalktı | 10,80 | **+5,76** | 235,8 | 37 | 23,1 |
| + K66 tek hizmet süresi | 0,46 | **−10,34** | 322,0 | 91 | 17,1 |
| + K68 konsolidasyon | 0,00 | −0,46 | 291,2 | 27 | **40,3** |
| + K65 VDI raf | 0,00 | 0,00 | 399,5 | 18 | 35,1 |
| + K70 saatlik rejim talebi | 0,09 | +0,09 | 403,6 | 17 | 36,0 |

**Okuma notları:**

- v1'in kendi raporladığı değer **%24,58**'dir; tablonun ilk satırı **%6,85**'tir. Aradaki
  fark **kapalı döngüden (K69)** gelir: v2 sinyalleri gerçek stoktan üretir, v1 ise
  LT=45 dk varsayımıyla önceden üretilmiş sabit bir listeyi kullanır.
- **K67 tek başına duruşu artırır (+5,76)**: durak sınırı kalkınca araç bir turda daha çok
  durak alır, 8 dk/durak hizmet süresiyle tur uzar ve diğer istasyonlar bekler. K66 ile
  birlikte uygulandığında etki tersine döner.
- **K66 en büyük tek etkendir (−10,34 puan).** Hafta 8'deki "duruşun 7–13 dakikaya düşmesi
  yalnızca tampon genişlemesi sayesindedir" yorumu bu nedenle **eksiktir**; hizmet süresinin
  8 dk'dan 3 dk'ya inmesi de aynı anda etkilidir ve iki etki ayrıştırılmamıştır.
- **K68 duruşu değiştirmeden doluluğu %17'den %40'a çıkarır** ve tur sayısını 91'den 27'ye
  düşürür — Vojdani & Drechsler'in %27 daha az sefer bulgusuyla aynı yöndedir.

---

## 5. Doğrulama Sonuçları

### 5.1 Solomon VRPTW kıyaslaması (K76)

6 örnek × 2 boyut. Referans: OR-Tools (Balikos vd. 2025 s.435–437 yaklaşımı; SINTEF'in BKS
tabloları sayfada JavaScript ile yüklendiğinden programatik alınamamıştır).

| Ölçüt | NN (v1) | NN + 2-opt (v2) |
|---|---:|---:|
| Ortalama sapma ($e_d$) | %102,69 | %101,76 |
| Medyan | %89,47 | %88,86 |
| En kötü (C201, n=50) | %198,45 | %197,76 |
| 2-opt kazancı | — | %0,50 |

**Yorum.** Açık büyüktür, ancak kaynağı tur-**arası** atamadır: 2-Opt tur-**içi** bir
komşuluk yapısıdır (Gendreau & Tarantilis, Böl. 1.1). Fabrika içi problemde turlar
2–8 duraklıdır; tur-içi sıralama tam numaralamaya göre yalnızca **%0,62** sapar:

| Durak | NN sapma (ort.) | NN+2opt sapma (ort.) |
|---:|---:|---:|
| 2 | %0,39 | %0,00 |
| 4 | %1,54 | %0,48 |
| 6 | %2,41 | %1,01 |
| 8 | %2,18 | %1,01 |
| **Genel** | **%1,68** | **%0,62** |

2-opt turların %46,5'inde optimali bulmaktadır. **Sınırlılık:** tur-arası atama
(hangi siparişin hangi turda olacağı) sevk kuralıyla belirlenir ve optimize edilmez.

### 5.2 Isınma süresi (K78)

20 replikasyon, ±15 dk hareketli ortalama, kararlı WIP ≈ 367 adet:

| t (dk) | WIP hareketli ort. | Kararlıdan sapma |
|---:|---:|---:|
| 0 | 831,5 | +126,5% |
| **45** (v1 varsayımı) | 573,3 | **+56,2%** |
| **90** (v2, K78) | 369,2 | **+0,6%** |
| 180 | 368,5 | +0,4% |

**Sonuç.** 45 dk ısınma süresi yetersizdir. 480 dk'lık vardiyada etkin analiz penceresi
435 dk değil **390 dk**'dır. Katı ölçütle (60 dk kesintisiz ±%2 bandı) kalıcı giriş
246 dk'dır — bu durumda pencerenin yarısından azı kullanılabilir. **S2 sınırlılığı
(tek vardiya) düşünülenden ciddidir.** 1440 dk'lık koşularda kararlı değer doğrulanmıştır.

### 5.3 Replikasyon yeterliliği

Ortalama duruş sıfıra yakınken **bağıl ölçüt tanım gereği sağlanamaz** (n=60'ta bile
yarı-genişlik ortalamanın %12,2'si). Mutlak ölçütle (±0,05 puan) **n=9** yeterlidir;
kullanılan 30 replikasyon fazlasıyla yeterlidir. Bu, tez metodoloji bölümüne bir
metodolojik not olarak eklenmelidir.

---

## 6. Yeni Bulgular

### 6.1 Politikalar ancak talep şoku altında ayrışır (K81)

252 konfigürasyon × 8 replikasyon. %5 eşiği için gereken en küçük filo:

| Politika | Baz talep | Talep şoku +%50 |
|---|---|---|
| P1 sabit takt, sabit miktar | 2 araç (T=45 dk) → %0,04 | 3 araç (T=30 dk) → %0,42 |
| P2 sabit takt, Kanban miktarı | 2 araç (T=80 dk) → %0,15 | 2 araç (T=80 dk) → %4,85 |
| P3 olay tabanlı dinamik | 2 araç (α=0,30) → %0,01 | 3 araç (α=0,30) → %0,49 |

**Bu, v1'in "%5 eşiği için 8 araç gerekir" bulgusunun (H10 ERRATA) yerini alır.**
v1'deki yüksek filo ihtiyacı, fiziksel raf kısıtının kendisinden değil, **eksik raf
boyutlandırma + hizmet süresi asimetrisi + açık döngü** birleşiminden kaynaklanmaktadır.

### 6.2 Eşit WIP karşılaştırması: sonuç koşullu (K53 revizyonu)

> ⚠️ **ERRATA (K96, 27.10.2026).** Aşağıdaki tablonun ikinci satırı güncel politika
> ızgarasıyla (`data/synthetic/v2_politika_izgara.csv`) **uyuşmamaktadır**: ızgarada P1,
> T=60, 3 araç **%0,09 duruş / 834 WIP** verir (%13,78 / ≈404 değil). Eşit WIP
> karşılaştırması statik sistemin kartları azaltılarak kurulabilir: K97 D kuralında
> dijital baz talepte **10,88**, şokta **15,15 puan** öndedir — yani büyüklük eşit WIP
> kuralı altında makuldür, ancak **kurala bağlıdır**. Politika-tutarlı boyutlandırmada
> (K97 kural B) ise yeterli filoda tüm politikalar %0–0,6 duruştadır; P3
> konsolidasyon %0,18 duruşu 413 WIP ile, en yakın statik nokta (P2, T=45) %0,55'i 467,
> P2 T=60 %0,49'u 673 WIP ile sağlar. **Üstünlük duruşta değil stoktadır.** Tablo tarihsel
> kayıt olarak korunmuştur.

| Koşul | Dinamik (P3) | Statik | Fark |
|---|---|---|---|
| 1 araç, WIP≈285 (doyma altı) | %21,41 | %18,80 (P1, T=30) | **2,60 puan statik lehine** |
| 3+ araç, WIP≈404 | %0,21 | %13,78 (P1, T=60) | **13,57 puan dinamik lehine** |
| 1 araç + %50 şok | %44,00 | %43,79 | 0,21 puan statik lehine |

**Doğru ifade:** Sistem doyma noktasının altındayken (araç yetersiz) statik çevrimin
öngörülebilirliği hafif avantaj sağlar; **yeterli filoda dinamik sistem hem daha düşük
duruş hem daha az stokla belirgin biçimde üstündür.** Pareto cephesinde (Şekil 1)
P3 cephesi hem en solda hem en alttadır.

### 6.3 Faktöriyel tasarım (K82)

$2^5$ tam faktöriyel × 10 replikasyon = 320 koşu. Duruş oranı ana etkileri:

| Faktör | Düşük → Yüksek | Ana etki | Cohen d | p |
|---|---|---:|---:|---|
| Talep düzeyi | 1,0 → 1,5 | **+10,22** | +1,57 | <0,001 |
| Filo büyüklüğü | 2 → 4 araç | **−9,55** | −1,41 | <0,001 |
| Raf boyutlandırma | V1 → VDI | **−3,88** | −0,48 | <0,001 |
| Güvenlik katsayısı α | 0,05 → 0,30 | −1,35 | −0,16 | 0,145 (—) |
| Sevk politikası | ANINDA → KONS. | +0,93 | +0,11 | 0,317 (—) |

En güçlü etkileşim: **Filo × Talep = −6,79 puan** (filo artışının faydası şok altında
daha büyüktür). Araç doluluğunda en güçlü ana etki **sevk politikasıdır (+20,19 puan,
d=1,80)** — konsolidasyon hizmet düzeyini bozmadan taşıma verimliliğini artırır.

α'nın sabit N modunda zayıf kalması, **K55'in bulgusuyla uyumludur.**

### 6.4 Sevk kuralları: K45/K64 revizyonu

| Senaryo | ANOVA | Tukey HSD |
|---|---|---|
| Yeterli filo (4 araç, baz talep) | F=0,003, **p=0,9997** | Hiçbir ikili fark eşiği (0,124) aşmıyor |
| Kısıtlı filo (2 araç, +%50 şok) | F=1,152, **p=0,3415** | Hiçbir ikili fark eşiği (1,369) aşmıyor |

**K45'in "KRİTİKLİK anlamlı biçimde kötüdür (Δ≈1,33 puan, p<0,0001), EDD'ye geçilmeli"
tavsiyesi v2'de desteklenmemektedir.** Olası nedenler: (a) v1'de kritiklik skoru sinyal
üretildiği anda hesaplanıp donuyordu, v2'de canlı stok/ROP kullanılır; (b) v1'deki 5 durak
sınırı seçim uzayını daraltıyordu; (c) hatalı talep verisi (K75).

### 6.5 Vaka çalışması (K83)

Gerçek fabrika verisi henüz bulunmadığından **literatürden türetilmiş** ve bu şekilde
açıkça etiketlenmiş bir vaka kurgulanmıştır: otomotiv yan sanayi montaj atölyesi,
4 hat / 24 istasyon / 3 araç / 480 dk. Ölçek referansları: Facchini vd. (2022) s.1125
(4 çekici, ~400 sefer/vardiya), Menanno vd. (2023) s.13–14, Sevim & Görkemli Aykut
(2026) s.67. 12 replikasyon.

**P3'ün P1'e göre farkı:**

| Senaryo | Duruş | WIP | Mesafe | Tur sayısı |
|---|---:|---:|---:|---:|
| Normal vardiya | +0,01 puan | **−%50,5** | +%14,6 | −%10,7 |
| Talep şoku +%50 | **−9,77 puan** | −%3,3 | +%67,9 | +%35,3 |
| Araç arızası (3→2) | +0,21 puan | **−%50,5** | +%20,3 | +%28,0 |

**Yorum.** Normal koşulda dinamik sistem aynı hizmet düzeyini **yarı yarıya stokla**
sağlamaktadır — yalın üretim açısından temel kazanç budur. Talep şokunda üstünlük
hizmet düzeyine de yansır (9,77 puan). Bedeli taşıma mesafesindeki artıştır
(+%15…+%68); bu, Alnahhal & Noche (2015) s.118'deki tur sayısı–stok ödünleşiminin
beklenen yönüdür.

### 6.6 Koşu-içi dinamik Kanban (K74)

| Talep | Sabit N | Dinamik N | Kart (sabit → dinamik) |
|---|---:|---:|---|
| Baz | %0,15 | %0,37 | 49 → 50 |
| **Şok +%50** | %4,15 | **%1,98** | 49 → 67 |
| Düşüş −%30 | %0,00 | %0,21 | 49 → 48 |

**Yorum.** Koşu-içi güncelleme **yalnızca talep kaydığında** kazandırır (şokta duruş
yarıya iner, kart 49→67). Talep kararlıyken gereksiz dalgalanma yaratıp hafifçe
kötüleştirir. Dolayısıyla uyarlanabilir Kanban, talep değişkenliğinin yüksek olduğu
hatlar için önerilmelidir — koşulsuz bir iyileştirme değildir.

### 6.7 Dinamiklik derecesi (K84)

Larsen vd. (2008) Bölüm 3.1 ölçütüyle: vardiya başına ≈161 ikmal isteğinin tamamı
vardiya içinde, gerçek stok tükenmesiyle doğar; hiçbiri ufkun başında bilinmez →
**dod = 1,00 (tam dinamik)**. P1/P2 takvim tabanlı olduğundan dod = 0'dır. Bu ölçüt,
statik VRPTW çözücülerinin doğrudan uygulanamamasının ve P3'ün yapısal farkının
biçimsel gerekçesidir.
*Sınırlılık:* dod = 1 uç değeri üretim programının hiç kullanılmamasından kaynaklanır;
`production_plan.csv` talep modeline bağlanırsa dod < 1 olur (gelecek çalışma).

### 6.8 Literatür KPI uyumu (K85)

Sevim & Görkemli Aykut (2026) s.67, Denk. 5–9'daki dört ölçüt (3 araç, baz talep):

| Politika | Doluluk | km/tur | Tur sayısı | İkmal süresi | Duruş | WIP |
|---|---:|---:|---:|---:|---:|---:|
| P1 sabit takt, sabit miktar | %32,0 | 1,66 | 21,0 | — | %0,14 | 833 |
| P2 sabit takt, Kanban miktarı | %27,5 | 1,66 | 21,0 | — | %0,37 | 678 |
| P3 dinamik, **anında** sevk | %5,7 | 0,43 | 113,7 | **5,5 dk** | %0,00 | 554 |
| P3 dinamik, **konsolidasyonlu** | **%33,7** | 2,13 | 18,8 | 29,6 dk | %0,15 | **412** |

**Konsolidasyonun ödünleşimi nettir:** ikmal süresi 5,5 → 29,6 dk uzar, buna karşılık
doluluk %5,7 → %33,7'ye çıkar ve tur sayısı 113,7 → 18,8'e iner. 29,6 dk, Facchini vd.
(2022) s.1125'teki ≤25 dk hedefine yakındır ve Klenk vd. (2012) s.12'deki e-Kanban
ikmal süresi bandının (102–113 dk) çok altındadır.

**⚠️ Kıyaslama uyarısı.** Doluluk oranları literatürle doğrudan kıyaslanamaz: bu
çalışmada istasyon başına 1–3 kutu taşınırken Urru vd. (2018) s.408'de rota kapasite
kullanımı 0,85–0,89, Sevim'de %69–81'dir. Fark, sistemin talep yoğunluğu ve kutu
büyüklüğü tasarımından gelmektedir.

---

## 7. Figürler

`docs/figurler/` altında, makale için 200 dpi:

| Dosya | İçerik |
|---|---|
| `sekil1_pareto_wip_durus.png` | WIP × duruş ödünleşimi, politika-içi iki amaçlı Pareto cepheleri |
| `sekil2_filo_sinir_egrisi.png` | Filo sınır eğrisi; baz talep ve +%50 şok küçük çoklusu |
| `sekil3_duzeltme_ayristirma.png` | v1 → v2 düzeltmelerinin duruşa katkısı |
| `sekil4_welch_isinma.png` | Welch ısınma eğrisi; 45 dk / 90 dk karşılaştırması |

Sayısal karşılıkları `data/synthetic/v2_*.csv` dosyalarındadır.

---

## 8. Tezin Özgün Katkısının Yeniden Konumlandırılması

**Mevcut iddia** (H10 rehberi, Bölüm 4.2): *"E-Kanban + VRPTW + stok simülasyonunu
bütünleşik ele alan çalışma literatürde yok."* Klasördeki kaynaklar karşısında bu iddia
**fazla güçlüdür**:

| Çalışma | Neyi bütünleşik ele alıyor |
|---|---|
| Menanno vd. (2023) | IT tabanlı Kanban + milk-run; starvation ölçülüyor (%43 azalma) |
| Vojdani & Drechsler (2022) | e-Kanban + dinamik rota + simülasyon |
| Sevim & Görkemli Aykut (2026) | ROP tetiklemeli dinamik milk-run, ajan tabanlı |
| Zhou & Wen (2024) | Kanban sayısı + kutu kapasitesi + çizelgeleme, Pareto cephesi |

Raf tavanı kısıtı da yeni değildir (Zhou & Zhu 2020; Menanno kısıt (3); Sevim $L_j$).

**Savunulabilir katkılar (revize):**

1. **Politika-tutarlı boyutlandırma ilkesi (ANA KATKI).** Politikaları karşılaştıran
   çalışmalarda tamponun hangi çevrim süresine göre boyutlandırıldığı belirtilmemektedir;
   bu ihmalin karşılaştırma sonucunun **yönünü** değiştirdiği gösterilmiştir.
2. **Modelleme kararlarının ayrıştırılmış etkisi** (Bölüm 4.1): ölçülen etkiler
   (10+ puan) politikalar arasındaki gerçek farktan (≈1 puan) büyüktür.
3. **Tüketim hızından türetilen dinamik zaman penceresi** (K27/K30) — en dar katkı;
   "taranan literatürde rastlanmamıştır" biçiminde ihtiyatlı yazılmalıdır.
4. **Dürüst olumsuz/koşullu bulgu raporlaması.**

> ⚠️ **26.10.2026 güncellemesi.** Bu bölüm, kaynak klasörünün dışına çıkan ayrı bir
> literatür taramasıyla yeniden sınanmıştır. Taramada, projenin ana karşılaştırmasının
> doğrudan öncülü olan **Alnahhal, Ramadan & Noche (2016)** ve **Ciemnoczolowski & Bozer
> (2013)** dâhil altı kritik çalışmanın kaynak klasöründe **bulunmadığı** tespit
> edilmiştir. İkisi (Bocewicz 2019, Kundu 2019) açık erişimden edinilmiş ve okunmuştur.
>
> **Üç ek sonuç:**
> 1. **K06 formülünün gerçek kaynağı bulundu** — Toyota formülü, **Sugimori vd. (1977)**;
>    Kundu vd. (2019) s.422 üzerinden. Formül artık "mühendislik uyarlaması" değildir.
>    ⚠️ Aynı kaynak α < %10 önerir; projede α = 0,15'tir (K88).
> 2. **Boşluk literatürce ilan edilmiştir** — Kundu vd. (2019) s.423: *reorder point*
>    ile *periodic review* politikalarının karşılaştırılması açıkça "gelecek çalışma"
>    olarak gösterilmiştir (K89). Bu alıntı makalenin girişinde kullanılmalıdır.
> 3. **Katkının gücü dürüstçe değerlendirilmiştir (K91):** katkı **metodolojiktir**,
>    teknik değildir. Lisans/YL tasarım çalışması için fazlasıyla yeterli; **TR Dizin
>    için sınırda** (tek engel: gerçek veri yokluğu); SCI-E için yetersizdir.
>
> Tam gerekçe, kanıt tabloları, hakem yanıtları ve güçlendirme yol haritası:
> **`docs/literatur_boslugu_analizi.md`** (özellikle Bölüm 4.1 ve Bölüm 10).

---

## 9. Sınırlılıklar (Güncellenmiş)

| ID | Sınırlılık | Durum |
|---|---|---|
| S1 | Sentetik veri | Değişmedi (yüksek) |
| S2 | Tek vardiya | **Ağırlaştı** — ısınma 90 dk (K78); etkin pencere 390 dk |
| S3 | Tek rastgele gerçekleşim | **Hafifledi** — v2'de 8–30 replikasyon; mutlak ölçütle n=9 yeterli |
| S4 | Sabit kutu kapasitesi C | Değişmedi |
| S5 | Tek fabrika düzeni | **Ağırlaştı** — mesafe matrisi metrik değildi (K71); kalıcı çözüm koordinat tabanlı üretim |
| S6 | Vojdani doğrulanamadı | **KAPANDI** — s.6 doğrulandı |
| S7 | Statik model basitliği | **Giderildi** — P2 politikası eklendi (K73) |
| **S8** | **Tur-arası atama optimize edilmiyor** | **YENİ** — sevk kuralıyla belirleniyor; Solomon'da NN açığı %102,7 (K76) |
| **S9** | **İstatistiksel ROP kullanılmadı** | **YENİ** — literatürde mevcut (Demiray Kırmızı s.9); bu bir tercihtir |
| **S10** | **Mesafeler koordinattan üretilmiyor** | **YENİ** — Floyd–Warshall geçici çözüm; kalıcı çözüm gelecek çalışma |

---

## 10. Kalan İşler

1. Mesafe matrisinin koordinatlardan dikdörtgensel ölçüyle yeniden üretilmesi ve istasyon
   aralığının literatür bandına (25–53 m) çekilmesi (S10).
2. Çok vardiyalı koşuların baz alınması ya da başlangıç stokunun kararlı durumda
   başlatılması (S2).
3. Koşu-içi dinamik Kanban (K74) ile senaryo bazlı Kanban'ın karşılaştırılması.
4. Gerçek ERP verisiyle doğrulama (`config.json → "real"`).
5. Makale taslağı: hedef dergi Endüstri Mühendisliği Dergisi veya JTOM; gönderim öncesi
   derginin güncel dizin, benzerlik sınırı ve dil kuralları kendi sitesinden doğrulanmalıdır.

---

## 11. Üretilen Dosyalar

**Kod:** `src/v2_entegre_simulasyon.py` (motor), `src/solomon_dogrulama.py`,
`src/v2_dogrulama_ve_kalibrasyon.py`, `src/v2_pareto_ve_figurler.py`,
`src/v2_deney_tasarimi.py`, `src/v2_vaka_ve_kpi.py`,
`src/tum_analizleri_calistir.py` (orkestratör).
Düzeltme: `src/stokastik_replikasyon.py` (K75).

**Veri:** `data/synthetic/` altında `solomon_dogrulama_sonuclari.csv`,
`v2_d1_tur_ici_optimallik.csv`, `v2_d2_welch_isinma.csv`, `v2_d3_replikasyon.csv`,
`v2_d45_ayristirma.csv`, `v2_politika_izgara.csv`, `v2_e1_faktoriyel_ham.csv`,
`v2_e1_ana_etkiler.csv`, `v2_e1_etkilesimler.csv`, `v2_e2_sevk_anova.csv`,
`v2_vaka_calismasi.csv`, `v2_dinamik_kanban.csv`, `v2_kpi_uyumu.csv`.

**Belge:** bu rapor; `docs/karar_gunlugu.md` (D-grubu + K65–K85); `docs/figurler/*.png`;
`README.md`; `requirements.txt`; `.gitignore`.
Errata notu eklenen raporlar: `hafta5_vrptw_analiz.md`, `hafta7_dispatch_analiz_raporu.md`,
`hafta8_kanban_karsilastirma_raporu.md`, `hafta9_sentez_ve_pareto_raporu.md`,
`tez_bilgi_rehberi.md`.

**Tekrarlanabilirlik:** `python -X utf8 -m src.tum_analizleri_calistir`
(tam koşu ≈ 6 dk; `--hizli` ile ≈ 1 dk).
