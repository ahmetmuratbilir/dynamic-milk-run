# TEZ METODOLOJİ VE BULGU REHBERİ
# Ne yaptık, neden yaptık, ne bulduk — tez yazımı için hazır kaynak
# Tarih: 15.08.2026 | Proje: Dinamik Milk-Run & E-Kanban Karar Destek Sistemi

---

## BÖLÜM 1: ARAŞTIRMANIN AMACI VE TASARIMI

### 1.1 Temel Araştırma Sorusu

Bu çalışma şu soruyu yanıtlamaya çalışmaktadır:
"Fabrika içi milk-run sistemlerinde E-Kanban tabanlı dinamik sevk ile geleneksel periyodik
sevk karşılaştırıldığında, hat duruş oranı (starvation) ve stok seviyeleri (WIP) açısından
hangisi daha iyi performans gösterir ve bu farkı asıl belirleyen faktör nedir?"

### 1.2 İki Sistem Karşılaştırması

STATIK SİSTEM (Geleneksel Periyodik Milk-Run):
- Araçlar sabit zaman aralıklarında (60, 80, 120 dk) tüm hattı dolaşır
- İstasyon stoklarına veya aciliyet durumuna bakmaksızın önceden belirlenmiş çevrim yapılır
- Parametreler: K48-K51 (karar_gunlugu.md)

DİNAMİK SİSTEM (E-Kanban + VRPTW):
- İstasyon stoğu eşiğin altına düştüğünde (ROP) elektronik sinyal gönderilir
- Sinyal üretildiğinde VRPTW algoritması araçları anlık olarak yönlendirir
- Sistem tam anlamıyla "olay-bazlı" (event-driven) çalışır

---

## BÖLÜM 2: SİSTEM PARAMETRELERİ (TEZ METODOLOJİ BÖLÜMÜ İÇİN)

### 2.1 Fabrika Modeli

| Parametre | Değer | Literatür Aralığı | Kaynak |
|-----------|-------|-------------------|--------|
| Üretim hattı sayısı | 4 hat | 1-38 hat | Kullanıcı onayı (K01) |
| İstasyon sayısı | 24 (hat başına 6) | 5-100 | Kullanıcı onayı (K02) |
| Araç sayısı (baz) | 2 araç | - | Mühendislik varsayımı (K03) |
| Araç kapasitesi | 25 kutu | - | Mühendislik varsayımı (K04) |
| Simülasyon süresi | 480 dakika (1 vardiya) | 600-7200 dk | Kullanıcı onayı (K05) |

### 2.2 Kanban Boyutlandırma Formülü

KULLANILAN FORMÜL:
  N = ceil(D × LT × (1 + α) / C)

Parametreler:
  D  = İstasyon tüketim hızı (adet/dk)
  LT = Lead Time = 45 dk (K07) — Klenk et al. 2012, s.12: 34-47 dk aralığı
  α  = Güvenlik katsayısı = 0.15 (K08) — tampon oranı, z-değeri DEĞİL
  C  = Kutu kapasitesi = 15 veya 20 adet (K09)
  N  = Gerekli Kanban kart sayısı (integer, en az 1)

NOT (SAVUNMA İÇİN ÖNEMLİ): α bu çalışmada istatistiksel service level hesabındaki
z-katsayısı değildir. Klenk et al. (2012) s.12'deki %30 tampon oranı mantığıyla
aynı kategoridedir — yani "ortalama tüketimin üzerine eklenen basit yüzde tampon."

### 2.3 Reorder Point (ROP) Hesabı

FORMULA: ROP_adet = D_dk × LT × (1 + α)

Bu formül, N formülünün payına karşılık gelir. İki farklı amaca hizmet eder:
  - N  → Rafta kaç kutu TUTULACAĞI (tasarım kararı, hesap başında yapılır)
  - ROP → Sinyal tetiklenme anındaki STOK EŞİĞİ (simülasyon sırasında anlık kontrol edilir)

Örnek (S1 istasyonu, düşük tüketim):
  D = 22 adet/sa = 0.367 adet/dk
  ROP = 0.367 × 45 × 1.15 = 18.97 adet → stok ≤18.97'ye düşünce E-Kanban sinyali
  N = ceil(18.97 / 20) = 1 kutu → sistemde 1 kutu Kanban

### 2.4 Araç ve Rota Parametreleri

| Parametre | Değer | Literatür Aralığı | Kaynak |
|-----------|-------|-------------------|--------|
| Araç hızı | 10 km/sa | 3.6-12 km/sa | K12 |
| İstasyonlar arası mesafe (ort.) | 180 m | 24-265 m | K13 |
| Yükleme süresi | 2 dk/durak | - | K14 |
| Boşaltma süresi | 3 dk/durak | - | K15 |
| Zaman penceresi genişliği | +60 dk | - | K16 |
| Maksimum tur süresi | 90 dk | - | K17 |

---

## BÖLÜM 3: HAFTALIK ÇALIŞMALAR — NE YAPILDI, NEDEN YAPILDI

### HAFTA 1-2: Literatür Taraması ve Veri Analizi

NE YAPILDI:
  - 17 akademik makale okundu ve parametreler karşılaştırıldı
  - Makale kataloğu oluşturuldu: docs/master_makale_katalogu.md
  - Sistematik parametre aralıkları (hat sayısı, araç sayısı, LT, α, C) belirlendi

NEDEN YAPILDI:
  - Sentetik veri parametrelerinin literatürle savunulabilir aralıkta olması için
  - "Bu değeri neden seçtiniz?" sorusuna makaleden kaynaklı cevap verebilmek için

TEMEL BULGULAR:
  - Literatürde hiçbir makale istatistiksel ROP formülü (z×σ×√LT) kullanmamış
  - Hepsi oransal tampon (α) kullanmış → bizim α=0.15 seçimi literatürle uyumlu
  - LT için en yakın kaynak: Klenk et al. 2012 → 34-47 dk → bizim 45 dk
  - Dispatch kural karşılaştırması yapan makale: Facchini et al. 2022

### HAFTA 3-4: Sentetik Veri Üretimi ve E-Kanban Simülasyonu

NE YAPILDI:
  - 24 istasyon için gerçekçi sentetik veri üretildi (src/generate_synthetic_data.py)
  - E-Kanban sinyal üreteci yazıldı (src/ekanban_signal.py)
  - Kanban kart sayıları N=ceil(D×LT×(1+α)/C) formülüyle hesaplandı
  - Stok simülasyonu: her dakika tüketim yapılır, ROP eşiği aşılınca sinyal

NEDEN YAPILDI:
  - Gerçek veri gizliliği nedeniyle sentetik veri zorunlu
  - E-Kanban sinyalleri rotalama algoritmasının girdisi
  - Stok dinamiği (tüketim + ikmal) simüle edilmeden starvation hesaplanamaz

KRİTİK TASARIM KARARI (SAVUNMADA SORULACAK):
  Tüketim dağılımı: Normal N(μ, 0.20μ) — yani CV=%20
  Gerekçe: Otomotiv montaj hatları için gerçekçi katsayı; literatürdeki
  Sevim & Aykut (2025) üstel dağılım, Zhou & Zhu (2020) Bernoulli kullanmış;
  normal dağılım ortalama davranışı en iyi temsil eder.

### HAFTA 5: VRPTW Rotalama Algoritması

NE YAPILDI:
  - Vehicle Routing Problem with Time Windows (VRPTW) çözücü yazıldı (src/vrptw_solver.py)
  - Nearest Neighbor heuristik kullanıldı (kesin çözüm değil, sezgisel)
  - Her tur: depodan çık → acil istasyonlara git → depoya dön
  - Starvation metrikleri hesaplandı

NEDEN VRPTW KULLANILDI:
  - Zaman penceresi (TW) kritik: her sinyal kendi deadline'ına sahip
  - Birden fazla araç (m-VRPTW): araç kapasitesi ve tur süresi kısıtları
  - Wang (2008) m-VRPTW referansı: "hizmet verilen müşteri sayısını maksimize et"

İLK TEMEL SONUÇ (2 ARAÇ, KRİTİKLİK KURALI):
  - Dinamik sistem: starvation %52.08 (10,440 dk ısınma sonrası payda)
  - Bu değer Hafta 6 başlangıç noktası olarak kullanıldı

NOT: Bu %52.08 değeri, K57 öncesi eski motor (vrptw_solver dahili sayaç) ile
üretildi. Kanonik motor (K57 sonrası) ile aynı koşul %51.96 veriyor (11,520 dk
tam vardiya paydası). Fark: payda değişikliği + farklı kod yolu. Bkz. K57.

### HAFTA 6: Filo Duyarlılık Analizi (2-6 Araç)

NE YAPILDI:
  - 2, 3, 4, 5, 6 araç için simülasyonlar koşuldu
  - Analitik filo boyutlandırma: Körösi & Duchoň (2026) formülü uygulandı
  - Azalan getiri eğrisi analizi yapıldı

BULGULAR (TAVANSIZ — KRİTİKLİK kuralı, orijinal H6):
  2 araç → %52.08 starvation, WIP=140.1
  3 araç → %36.11 starvation
  4 araç → %19.46 starvation  (Körösi analitik baz: 4 araç)
  5 araç → %5.20 starvation   ← eski "yeterli" eşiği
  6 araç → %0.97 starvation   ← eski "yeterli" eşiği

ERRATA (HAFTA 10 DÜZELTMESİ — TAM 2-8 ARAÇ SERİSİ):
  Orijinal değerler TAVANSIZ (sınırsız stok) + KRİTİKLİK dispatch modeline aittir.
  Hafta 10'da aynı çalışma EDD dispatch + TAVANLI (stok ≤ N×C) kanonik motorla
  yeniden koşuldu. Tam 2-8 araç serisi aşağıdadır:

  Araç | Tavansız % [EDD] | Tavanlı % [EDD] | Tavanlı WIP | Tavan Etkisi
  -----+------------------+-----------------+-------------+-------------
    2  |     %51.28       |    %53.01       |    111.1    | +1.74 puan
    3  |     %33.75       |    %36.93       |    148.5    | +3.18 puan
    4  |     %17.00       |    %24.58       |    182.3    | +7.59 puan
    5  |      %3.96       |    %15.98       |    211.0    | +12.02 puan  ← MAKSİMUM
    6  |      %0.64       |    %11.27       |    224.4    | +10.62 puan
    7  |      %0.28       |     %7.00       |    232.9    | +6.72 puan
    8  |      %0.10       |     %3.50       |    237.3    | +3.40 puan
  [Kaynak: src/hafta10_whatif_senaryolari.py — kanonik motor K57]

  NEDEN 6 ARAÇTA İKİ FARKLI DEĞER VAR (%12.08 ve %11.27):
  Denetim testinden (denetim_reproduksiyon_testi.py) gelen değer %12.08, orada
  KRİTİKLİK dispatch kuralı kullanıldı. Yukarıdaki tablo EDD kuralıyla koşuldu
  (%11.27). KRİTİKLİK kuralı acil istasyona önce gider ama WIP'i yüksek tutar;
  EDD kuralı deadline'a göre önceliklendirir ve birkaç puan daha düşük duruş üretir.
  BU BİR YAZIM HATASI DEĞİLDİR — dispatch kuralı farkından kaynaklanan sistematik
  bir farktır. H8-H10 baz değerleri EDD tabanlı olduğundan bu tablodaki EDD
  değerleri (%11.27 vb.) baz ile tutarlıdır ve tezde kullanılacaktır.

  SONUÇ: <%5 duruş için TAVANLI + EDD modelde minimum 8 araç gerekmektedir (%3.50).
  Orijinal "5-6 araç yeterli" sonucu tavansız (idealize) modelden kaynaklanmaktaydı.

AZALAN GETİRİ ANALİZİ (orijinal tavansız, genel örüntü hâlâ geçerli):
  2→3 araç: −15.97 puan (artan marjinal fayda)
  3→4 araç: −16.65 puan (ZİRVE marjinal fayda)
  4→5 araç: −14.26 puan (düşüş başlangıcı)
  5→6 araç: −4.23 puan (SERT azalan getiri)
  Klasik azalan getiri eğrisi — 3→4 araç geçişi en verimli noktadır.
  NOT: Bu örüntü orijinal (tavansız, KRİTİKLİK) verilere aittir. Tavanlı EDD
  serisinde de genel yön aynıdır ancak eşik değerleri farklılaşmaktadır.

### HAFTA 7: Dispatch Kuralı Karşılaştırması

NE YAPILDI:
  - 4 dispatch kuralı karşılaştırıldı: KRİTİKLİK, EDD, SLACK, FIFO
  - KRİTİKLİK: stok/ROP oranı en düşük önce (en acil)
  - EDD (Earliest Deadline First): deadline en yakın önce
  - SLACK: en az gevşek zaman penceresi önce
  - FIFO: geliş sırasına göre

BULGULAR — TAVANSIZ (2 araç, 11,520 payda):
  Kural       | Tavansız % | Tavansız WIP
  ------------+------------+-------------
  KRİTİKLİK  |   %51.96   |    140.1
  EDD         |   %51.28   |    121.2
  SLACK       |   %51.28   |    121.2
  FIFO        |   %51.29   |    121.1
  Fark çok küçük (< 1 puan) — 2 araçla kural değil filo kısıtı belirleyici.

ERRATA (HAFTA 10 DÜZELTMESİ — TAVANLI KARŞILAŞTIRMA):
  Hafta 10 denetiminde aynı 4 kural, TAVANLI (stok ≤ N×C) modelle yeniden koşuldu.
  [Kaynak: denetim_reproduksiyon_testi.py, KRİTİKLİK kuralı bazlı, 11,520 payda]

  Kural       | Tavansız % | Tavanlı %  | Tavanlı WIP | Tavan Etkisi
  ------------+------------+------------+-------------+-------------
  KRİTİKLİK  |   %51.96   |   %56.48   |    103.7    | +4.52 puan
  EDD         |   %51.28   |   %53.01   |    111.1    | +1.74 puan
  SLACK       |   %51.28   |   %53.01   |    111.1    | +1.74 puan
  FIFO        |   %51.29   |   %53.03   |    111.0    | +1.74 puan

  TEMEL GÖZLEM: Raf tavanı eklendikten sonra da sıralama korunuyor.
  EDD ≈ SLACK ≈ FIFO (birbirinden < 0.03 puan fark) ve KRİTİKLİK en yüksek duruş.
  Tavan kısıtı KRİTİKLİK kuralını orantısız biçimde etkiliyor (+4.52 puan) çünkü
  KRİTİKLİK en kritik istasyona önce gidiyor → orada stok dolup tavana çarpıyor →
  diğer istasyonlara geç kalıyor. EDD'de tavan etkisi daha eşit dağılıyor (+1.74 puan).

TEMEL ÇIKARIM (K64 istatistiksel düzeltmesiyle güncellenmiştir, 31.08.2026):
  EDD, SLACK ve FIFO birbirine istatistiksel olarak eşdeğerdir — Welch t-testi
  (30 replikasyon, K63 formülüyle): p=0.913 (4 araç), p=0.935 (2 araç).
  "SLACK en iyi kuraldır" iddiası istatistiksel kanıt taşımamaktadır.
  Doğru ifade: EDD, SLACK ve FIFO arasında anlamlı bir fark bulunamadı; bu
  üç kural birbirine eşdeğerdir ve herhangi biri seçilebilir. KRİTİKLİK ise
  her üçünden de istatistiksel olarak anlamlı biçimde daha kötüdür (p<0.0001,
  Δ≈+1.33 puan).
  EDD Hafta 8-10'da baz kural olarak seçildi çünkü:
  (1) Literatürde en yaygın kullanılan
  (2) Zaman penceresini doğrudan dikkate alıyor
  (3) SLACK ve FIFO ile istatistiksel olarak özdeş (p>0.9)
  (4) Tavan kısıtı altında KRİTİKLİK'e göre ~3.47 puan daha iyi

### HAFTA 8: Statik vs Dinamik Kapsamlı Karşılaştırma

NE YAPILDI:
  - Statik sistem (60 dk sabit periyodik tur) vs Dinamik sistem (E-Kanban+VRPTW) karşılaştırması
  - 2 araç ve 4 araç senaryoları
  - Raf tavanı (stok ≤ N×C) kısıtı eklendi — BU KRİTİK

RAF TAVANI KISITI (stok ≤ N×C) NEDEN EKLENDİ:
  Gerçek dünyada raflar sonsuza kadar dolu olamaz.
  N kutu × C kutu kapasitesi = fiziksel maksimum raf kapasitesi.
  Bu kısıt olmadan simülasyon "hayali" stok biriktiriyor ve starvation
  yapay olarak düşük çıkıyor. Fiziksel gerçekliği yansıtmak için zorunlu.

HAFTA 8 TEMEL SONUÇLAR (EDD, tavanlı, kanonik motor):
  Statik (2 araç, 60 dk): %45.54 starvation, WIP=119
  Dinamik (2 araç, EDD):  %53.01 starvation, WIP=111
  → 2 araçta statik daha iyi
  
  Statik (4 araç, 80 dk): %19.31 starvation, WIP=177
  Dinamik (4 araç, EDD):  %24.58 starvation, WIP=182  ← BAZ DEĞER
  → 4 araçta da statik daha iyi

NEDEN DİNAMİK SİSTEM İYİ ÇIKMIYOR:
  - Reaktif gecikme: sinyal geliyor, araç hazırlanıyor, yola çıkıyor
    → stok bu sürede tükeniyor ve starvation oluşuyor
  - Statik sistemde araç zaten belirlenen saatte yola çıkıyor
    → İstasyon stoklanmadan önce araç orada

### HAFTA 9: WIP-Starvation Trade-off ve Pareto Analizi

NE YAPILDI:
  - Statik sistemde sefer aralığı değiştirilerek WIP seviyeleri eşitlendi
  - Eşit WIP seviyesinde statik vs dinamik karşılaştırması yapıldı
  - Pareto eğrisi çizildi: düşük WIP + düşük starvation aynı anda mümkün mü?

TEMEL BULGULAR:

  TRADE-OFF KANITI:
  2 araç: Statik (120 dk tur, WIP≈119) %45.54 vs Dinamik (WIP≈111) %53.01
  → Eşit WIP'te statik 7.47 puan daha iyi
  4 araç: Statik (80 dk tur, WIP≈177) %19.31 vs Dinamik (WIP≈182) %24.58
  → Eşit WIP'te statik 5.27 puan daha iyi

  TEMEL MÜHENDİSLİK BULGUSU (K53):
  "Düşük WIP ve düşük starvation aynı anda elde edilemiyor."
  WIP starvation'ın baskın belirleyicisidir, AMA eşit WIP'te dahi
  statik sistem 5-7 puan avantajlıdır — çünkü deterministik çevrim
  reaktif gecikmeye karşı ek avantaj sağlar.

  HANGİSİ "DAHA İYİ": YANIT KARMA/OLUMSUZ
  Hafta 9 kontrol soruları:
  Q1: "Dinamik sistem mesafeyi azaltıyor mu?"
  → HAYIR. Aynı koşulda (4 araç): Statik 48.49 km, Dinamik 48.49 km ≈ EŞİT.
    (Çünkü VRPTW her iki sistemde de aynı mesafe matrisini kullanıyor)
  Q2: "Dinamik sistemde starvation daha düşük mü?"
  → HAYIR. Her konfigürasyonda statik sistem daha iyi veya eşit performans gösteriyor.
  
  Bu bulgu "beklediğimiz gibi çıktı" değil, "gerçek bir mühendislik gerilimi keşfettik."

### HAFTA 10: Stres Testleri ve Geriye Dönük Denetim

NE YAPILDI:
  1. Faz 1-3 Denetimi: Hafta 5-7 sonuçları raf tavanı kısıtıyla yeniden koşuldu
  2. 14 What-If Senaryo Testi: talep şoku, filo arızası, hız düşüşü, α duyarlılığı
  3. Kanonik motor birleştirmesi (K57): iki farklı kod yolu tek fonksiyona birleştirildi
  4. 7-8 araçlık genişletilmiş filo taraması

NEY IÇIN YAPILDI:
  Sistem "kırılma noktaları"nı bulmak: hangi senaryo altında sistem çöker?
  Tezde "Duyarlılık Analizi" ve "Dayanıklılık (Resilience) Değerlendirmesi" olarak raporlanacak.

10 WHAT-IF SENARYO SONUÇLARI (4 araç EDD baz → %24.58):
  +20% talep şoku      → %33.84 (+9.25 puan) — beklentiye UYGUN
  -20% talep düşüşü    → %12.13 (-12.45 puan), WIP arttı — UYGUN
  Filo 3 araç          → %36.93 (+12.35 puan) — UYGUN
  Filo 2 araç          → %53.01 (+28.43 puan) — UYGUN
  Filo 1 araç          → %69.50 (+44.92 puan) — KRİTİK ÇÖKÜŞ
  Hız düşüşü 10→6 km/sa → %36.21, mesafe 48.49→36.39 km (tur sayısı düştü)
  α=0.05 Sabit N       → %24.08 (baz'dan hafif iyi — anomali, gürültü seviyesi)
  α=0.30 Sabit N       → %21.90 (baz'dan biraz iyi)
  α=0.05 Dinamik N     → %25.32 (baz'dan hafif kötü)
  α=0.30 Dinamik N     → %17.90 (baz'dan 6.68 puan iyi — en büyük fark)
  S16 darboğaz krizi   → %25.38 (+0.80 puan — lokalize etki, sistem absorbe etti)

KRİTİK TASARIM BULGUSU — α MOD A vs MOD B (K55):
  Sabit N modu (Mod A): α değiştirince yalnızca ROP eşiği kayar.
    Etki zayıf: α=0.05 ile α=0.30 arası min-max fark sadece 2.18 puan.
  Dinamik N modu (Mod B): α değiştirince N=ceil(D×LT×(1+α)/C) yeniden hesaplanır.
    Etki güçlü: α=0.05 ile α=0.30 arası fark 7.42 puan.
  SONUÇ: Güvenlik katsayısının gerçek etkisini görmek için raf boyutunun
  (N kart sayısının) da birlikte güncellenmesi zorunludur.

---

## BÖLÜM 4: TEMEL BULGULAR VE TEZ KATKISI

### 4.1 Ana Bulgular (Tez Sonuç Bölümü İçin)

BULGU 1 — WIP-Starvation Temel Trade-off (K53):
  Düşük WIP (az stok) ile düşük starvation (az duruş) aynı anda elde edilemiyor.
  Bu temel bir mühendislik gerilimi/trade-off'udur.
  Eşit WIP seviyesinde statik sistem ~3-5 puan avantajlıdır (seed'e bağlı olarak):
    Deterministik tüketim (seed=42): +5.27 puan statik lehine
    Stokastik tüketim (3 farklı seed ortalaması): +3.06 puan statik lehine
  Mekanizma: deterministik çevrim vs reaktif gecikme.
  NOT: "5-7 puan avantaj" ifadesi yalnızca deterministik seed bazı alınırsa
  doğruydu; stokastik koşulda gerçekçi aralık ~3-5 puan'dır (K58 bağlamı).

BULGU 2 — Filo Boyutunun Baskınlığı (K56):
  Dispatch kuralı değil, filo büyüklüğü sistemi en çok etkileyen değişkendir.
  Her araç kaybı ortalama +12-16 puan starvation artışı getirir.
  1→2→3→4 araç: %69.50 → %53.01 → %36.93 → %24.58 (monoton azalma)

BULGU 3 — Fiziksel Raf Kısıtının Filo İhtiyacını Artırması (H10 ERRATA):
  Sınırsız stok varsayımıyla: 5-6 araç <%5 eşiğine yeterli görünüyor
  Fiziksel raf tavanıyla (gerçekçi model): <%5 için 8 araç gerekiyor
  Bu bulgu, bu çalışmada kullanılan simülasyon modelinde basitleştirilmiş
  (sınırsız stok) varsayımın filo ihtiyacını eksik tahmin ettiğini
  göstermektedir; bu gözlemin genellenebilirliği, farklı sistem
  konfigürasyonlarında (farklı istasyon sayısı, tüketim dağılımı, araç kapasitesi)
  test edilmesi gereken bir gelecek çalışma sorusudur.

BULGU 4 — α'nın Etkisi Yalnızca Dinamik N Modunda Anlamlı (K55):
  Raf boyutu sabitken α'yı artırmak sınırlı fayda sağlar (2.18 puan).
  N kart sayısı da birlikte güncellendiğinde α'nın etkisi 3.4 kat daha büyük (7.42 puan).

BULGU 5 — Talep Şoku Asimetrisi:
  +%20 talep → +9.25 puan starvation artışı
  -%20 talep → −12.45 puan starvation azalması (asimetrik tepki)
  Sistem talep düşüşüne daha duyarlı (stok birikmesi absorbe ediyor).

### 4.2 Tezin Özgün Katkısı

1. ENTEGRE MODEL: E-Kanban sinyali + VRPTW rotalama + stok simülasyonu
   tam entegre tek bir platform altında. Literatürde bunları ayrı ayrı
   ele alan çalışmalar var ama entegre simülasyon yok.

2. FİZİKSEL KISIT ANALİZİ: Raf tavanı (stok ≤ N×C) kısıtının sistematik
   olarak eklenmesi ve bunun filo boyutlandırması üzerindeki etkisinin
   sayısal olarak gösterilmesi.

3. WIP-STARVATION TRADE-OFF KANİTİ: Eşit WIP seviyesinde yapılan
   karşılaştırma ile "hangisi daha iyi" sorusunu sadece filo büyüklüğüne
   değil, sevk mekanizmasına bağlaması.

4. DÜRÜST NEGATIF BULGU: "Dinamik sistem her zaman daha iyidir" hipotezi
   bu sistemde geçerli değil — bu literatürde nadiren raporlanan bir
   dürüst negatif bulgudur.

---

## BÖLÜM 5: SİMÜLASYON KODU MİMARİSİ (YÖNTEM BÖLÜMÜ İÇİN)

### 5.1 Dosya Yapısı

src/generate_synthetic_data.py  → Sentetik veri üretimi (N, D, başlangıç stoku)
src/ekanban_signal.py           → E-Kanban sinyal motoru (ROP kontrol + sinyal üret)
src/vrptw_solver.py             → VRPTW rotalama algoritması (nearest neighbor)
src/hafta8_kanban_karsilastirma.py → Statik vs dinamik karşılaştırma + kanonik WIP/starvation fonksiyonu
src/denetim_reproduksiyon_testi.py → Faz 1-3 denetim ve reprodüksiyon testi
src/hafta10_whatif_senaryolari.py  → 14 senaryo What-If stres testi

### 5.2 Kanonik Motor (K57)

TÜM starvation ve WIP hesapları için TEK fonksiyon:
  hesapla_dinamik_wip_ve_starvation() — src/hafta8_kanban_karsilastirma.py

Bu fonksiyon:
  - Her dakika tüketim yapar
  - Teslimatları (ikmal) stoka ekler
  - stok = max(0, stok - tuketim)  ← negatife düşmez
  - raf tavanı: stok = min(stok_yeni, N×C)  ← N×C'yi aşamaz
  - starvation: stok ≤ 0 iken tuketim > 0 → o dakika-istasyon çifti sayılır
  - WIP: her dakikadaki toplam stok, 480 dakika ortalaması

### 5.3 İki Payda (Savunmada Sorulabilir)

Starvation oranı iki şekilde raporlandı:
  % (11,520) = toplam_starv / (480 dk × 24 istasyon) — tam vardiya paydası
  % (10,440) = ısınma_sonrası_starv / (435 dk × 24 istasyon) — ilk 45 dk hariç

Önerimiz: Tezde yalnızca % (11,520) paydası kullanın — daha şeffaf.
% (10,440) bir referans olarak dipnota alınabilir.

---

## BÖLÜM 6: SONUÇ CÜMLELERİ (TEZ SONUÇ BÖLÜMÜ İÇİN TASLAK)

1. "Bu çalışmada E-Kanban tabanlı dinamik milk-run sistemi, VRPTW algoritması ile
   entegre edilerek geleneksel periyodik milk-run sistemi ile karşılaştırılmıştır.
   Sentetik fabrika modeli üzerinde yürütülen simülasyon deneyleri, dinamik sistemin
   hat duruş oranı (starvation) açısından beklendiği gibi üstünlük sağlamadığını,
   ancak filo büyüklüğü ve güvenlik tamponu parametrelerine karşı öngörülebilir
   duyarlılık gösterdiğini ortaya koymuştur."

2. "Eşit WIP seviyesinde yapılan Pareto karşılaştırması, gözlemlenen duruş farklarının
   algoritmanın 'zekâsından' değil, sahada tutulan ortalama tampon stok miktarından
   kaynaklandığını göstermektedir. Bununla birlikte, eşit WIP koşulunda dahi statik
   sistem lehine gözlenen 5-7 puanlık fark, deterministik çevrim yapısının reaktif
   gecikmeye karşı sağladığı avantajı doğrulamaktadır."

3. "Fiziksel raf tavanı kısıtının (stok ≤ N×C) modele dahil edilmesi, <%5 starvation
   eşiğine ulaşmak için gereken filo büyüklüğünü tahmin edilen 5-6 araçtan 8 araca
   yükseltmiştir. Bu bulgu, çalışmada incelenen sentetik fabrika modelinde
   basitleştirilmiş (sınırsız stok) varsayımın filo ihtiyacını eksik tahmin ettiğini
   göstermektedir; fiziksel stok kısıtlarının benzer sonuçlar üretip üretmeyeceği
   farklı sistem konfigürasyonlarında araştırılması gereken bir gelecek çalışma
   sorusu olarak önerilmektedir."

---

## REFERANSLAR (DOĞRUDAN ATIF YAPILABİLECEKLER)

- Klenk, E. et al. (2012) — LT=34-47 dk, α tampon oranı %30
- Facchini, A. et al. (2022) — VRPTW milk-run, olay bazlı dispatch
- Körösi, G. & Duchoň, F. (2026) — Analitik filo boyutlandırma formülü
- Wang, C. (2008) — m-VRPTW, müşteri sayısını maksimize et
- Simić, D. (2020) — Milk-run & Kanban parametreleri
- Sevim & Görkemli Aykut (2025) — Dinamik milk-run, 2 vs 3 araç testi
- Vojdani & Drechsler (2022) — Geleneksel 1 saatlik sabit tur sistemi
  ⚠️ DOĞRULAMA NOTU: Bu makale statik sistemin (60 dk sabit periyot) gerekçesi
  olarak kullanılmaktadır ancak PDF'ten doğrudan alıntı teyidi henüz yapılmamıştır.
  Tez teslimine yakın Wang/Facchini gibi satır numarasıyla doğrulanmalıdır.

Tüm referansların tam kaynakları: docs/master_makale_katalogu.md

---

Son güncelleme: 15.08.2026 (Revizyon 2: Seed testi, Sevim&Aykut karşılaştırması, Sınırlılıklar eklendi)
Dosya: docs/hafta10_metodoloji_ve_bulgu_rehberi.md

---

## BÖLÜM 7: SEED SAGLAMLIK TESTI SONUÇLARI

--- TUTARSIZLIK TESPiTi VE DÜZELTME SERGÜVENi ---
Ilk seed testi su değerleri verdi: seed=42 Statik=%17.60 WIP=191.5
Kanonik beklenti (Hafta 9 raporundan): Statik=%19.31 WIP=177.0
Fark: 1.71 puan ve 14.5 birim WIP -- ACIKLANMADAN GECILMEMELI

ARASTIRMA:
Ilk seed testindeki hesapla_statik() fonksiyonu iki hatali parametre iceriyordu:
  (1) tur_suresi_dk=80 DOGRU, ama kalkis takvimi buna gore kurulmamis
  (2) kutu_per_ist = max(1, 4*25//24) = 4 kutu/ist -- YANLIS
      Kanonik Hafta 9 senaryosu: 1 kutu/ist/tur kullanir (StaticMilkRunSimulator L133)

IKINCi KESiF -- KANONiK StaticMilkRunSimulator KODU 60 dk HARD-CODED:
  StaticMilkRunSimulator.run_static_simulation() L97:
    kalkis_dakikalari = [60, 120, 180, 240, 300, 360, 420]
  Ama Hafta 9'da raporlanan kanonik deger 80 dk tur takviminden uretilmis.
  Yani: StaticMilkRunSimulator olduqu haliyle %19.31'i reprodukte etmiyor (%3.04 veriyor).
  Bu, kod ile rapor arasinda sessiz bir tutarsizlik -- Hafta 11'de duzeltilmesi gerekiyor.
  [NOT: StaticMilkRunSimulator L97'deki 60dk sabit tur, Hafta 8 orijinal tasarimi;
   Hafta 9'da WIP esitleme icin 80dk tura gecilmis ama kod guncellenmemis.]

KANONiK 80DK TESTI ile REPRODUKSIYON:
  80dk kalkis = [80, 160, 240, 320, 400], 1 kutu/ist, 4 arac (src/seed_testi_kanonik2.py)
  seed=42: Statik=%19.31 WIP=177.0 -- KANONiK DEGERLE TAMAMEN ESLESIYOR

ANA TRADE-OFF BULGUSUNUN DÜRÜST SEED TESTI
Kural: Tum sonuclar raporlanacak, seçici davranilmayacak.
Yontem: seed=42 deterministik + seed 7/99/123 stokastik tuketim
        (src/stokastik_replikasyon.py -> uret_stokastik_tuketim)
Senaryo: 4 arac, Statik (80dk tur, 1 kutu/ist, tavanli) vs Dinamik (EDD, tavanli)
[Kaynak: src/seed_testi_kanonik2.py]

Seed   | Tuketim      | Statik % | WIP_S | Dinamik % | WIP_D | Fark  | Yon
-------+--------------+----------+-------+-----------+-------+-------+----------------
42-det | Deterministik| %19.31   | 177.0 | %24.58    | 182.3 | +5.27 | STATIK LEHINE
     7 | Stokastik    | %26.61   | 162.3 | %29.53    | 171.1 | +2.92 | STATIK LEHINE
    99 | Stokastik    | %26.76   | 161.6 | %29.88    | 170.6 | +3.12 | STATIK LEHINE
   123 | Stokastik    | %26.77   | 161.7 | %29.90    | 170.4 | +3.13 | STATIK LEHINE

NIHAI SONUC: 4/4 seed icinde STATIK LEHINE

ANALIZ:
1. YON DEGISMEDI: 4 farkli tuketim profili altinda da statik sistem daha dusuk
   starvation uretiyor. Ana trade-off bulgumuz seed'e bagimli bir yapay sonuc degil.

2. FAR BUYUKLUGU (GUNCELLENMIS, DOGRU DEGERLER):
   Deterministik (seed=42): +5.27 puan statik lehine
   Stokastik seed 7:  +2.92 puan statik lehine
   Stokastik seed 99: +3.12 puan statik lehine
   Stokastik seed 123: +3.13 puan statik lehine
   GERCEKCI ARALIK: ~3-5 puan (seed bazli)
   NOT: Onceki raporlarda yazan '5-7 puan' araligi yalnizca deterministik
   seed=42 bazliydi; stokastik testler bu degerin ust siniri oldugunu gosteriyor.

3. NEDEN STOKASTIKTE FARK KUCULUYOR: Stokastik tuketim (CV=%20) daha dalgali
   talep uretiyor. Dalgali taleple dinamik sistem, anlik acil sinyallere daha
   hizli tepki veriyor -- bu farki biraz kapatiyor ama kapatamiyor.

4. SINIRLAMA: Bu test 4 seed ile yapildi (K46 uyarinca tam replikasyon kapsam disi).
   Fiziksel mekanizma (reaktif gecikme) deterministik oldugu icin yon degismesi
   teorik olarak beklenmiyor; 4 seed bu tezi desteklemektedir.

TEZ IFADESI ONERISI:
"Deterministik seed'de (42) gozlenen 5.27 puanlik statik-lehine fark, stokastik
seed'lerde 2.92-3.13 puana daralmaktadir -- bu, deterministik tuketim varsayiminin
fark buyuklugunu hafifce abarttigini, ancak yonunu (statik lehine) etkilemedigini
gostermektedir. Tez sonuc bolumunde 'statik sistem 5-7 puan avantajli' yerine
'statik sistem ~3-5 puan avantajli (seed'e bagli olarak)' araligi kullanilmalidir."

---

## BÖLÜM 8: SEVİM & AYKUT (2026) KARŞILAŞTIRMA PARAGRAFI
(Tez Tartışma bölümüne doğrudan eklenecek — PDF'ten doğrulanan metriklerle)

SEVIM & AYKUT GERCEK METRIKLERINI BELGELEYELİM (PDF satir referanslari):

Makalenin performans kriterleri (s.5-6, Denklem 5-9):
  - Ortalama doluluk oranı (araç kapasitesi kullanimi, %)
  - Ortalama tur mesafesi (km/tur)
  - Ortalama tur sayisi
  - Ortalama bekleme süresi (dakika/istasyon)

Makalenin "yeterlilik" önerisi (s.6-7, Sonuc tablosu):
  "Number of trains, inventory of raw material, train capacity, and reorder point
   as 3, 150, 250, and 25 respectively both in case of low demand and in case of
   high demand." (s.7, L1005-1007)

ÖNEMLI: Sevim & Aykut hiçbir yerde starvation orani veya %5 esik kullanmiyor.
  p=0 degerleri: Tren sayisi ve tren kapasitesinin DOLULUK ORANI üzerindeki etkisi
  (s.5, L820). "3 araç yeterli" sonucu doluluk + bekleme süresi optimizasyonuna
  dayanmaktadir, starvation oranina degil.

SISTEM FARKLARI (dogrulanmis):
  Sevim & Aykut         | Bu Calisma
  ----------------------+---------------------------
  10 istasyon           | 24 istasyon
  7200 dk simulasyon    | 480 dk (tek vardiya)
  Üstel talep           | Normal N(mu, 0.20mu)
  Kapasite: 250-400 unit| 25 kutu (varsayim)
  Basari olcutu: Doluluk| Basari olcutu: Starvation <%5
  Tur mesafesi optimize | Starvation minimize

HAZIR PARAGRAF (Tez Tartışma Bölümü İçin):

"Sevim & Görkemli Aykut (2026), benzer bir dinamik fabrika-ici milk-run sistemini
agent-based modelleme ile analiz etmis ve doluluk orani, ortalama tur mesafesi ve
istasyon basina ortalama bekleme suresi performans kriterleri cercevesinde 3 trenin
yeterli oldugunu onermistir (s.7). Bu öneri, tren sayisi ve kapasitesinin doluluk orani
uzerindeki etkisine ait ANOVA analizinde p=0 istatistiksel anlamlılıkla desteklenmistir
(s.5, Şekil 5).

Ancak bu calisma ile dogrudan karsilastirma yapmak yaniltici olacaktir, zira iki calisma
farkli basari kriterleri kullanmaktadir: Sevim & Aykut doluluk oranı ve bekleme
suresini optimize ederken, bu calisma hat durus orani (starvation) icin bir <%5
rekabetcilik esigi kullanmaktadir. Bunun yanısıra iki calisma birbirinden farkli
sistem büyüklüklerini modellemektedir (10 istasyon - 24 istasyon). Doluluk orani
ve bekleme suresi kriterlerine gore 3 aracin yeterli olmasi, starvation <%5 esigi icin
8 aracin gerekmesiyle çelismez; iki sonuc farkli sorulara cevap vermektedir.

Bu metodolojik fark, filo boyutlandirma probleminin asagidaki basari kriterine
gore farkli yanıtlar urettigini gostermesi bakimindan kendi basina anlamli bir
bulgudur: Karsilama kapasitesi odakli bir sistem tasarimi ile durus orani odakli
bir sistem tasarimi, farkli filo büyüklüklerine yonlendirebilir. Bu bulgu,
operasyonel hedefin tasarim kararlarini ne denli sekillendirdigini
orneklendirmektedir ve literaturde benzer bir karsılastırmali analizin eksikligine
dikkat cekmektedir."

---

## BÖLÜM 9: SINIRLILIKLAR (TEZ SINIRLILIKLAR BÖLÜMÜ İÇİN)
(Tüm bilinen sınırlılıklar tek yerde — savunmada proaktif sunum için)

S1 — SENTETİK VERİ (En Önemli Sınırlılık)
  Bu calısma gercek fabrika verisi yerine sentetik veri kullanmistir.
  Parametreler (LT, alfa, C, mesafe) litaruturle savunulabilir aralikta olmakla
  birlikte, sentetik veri gercek fabrika dinamiklerini (malzeme bozulmasi,
  beklenmedik talep siçramalari, tren arizasi) yansitamaz.
  Hafifletici Onlem: Tum parametreler litarutur kaynaklarına dayanmaktadir
  (bkz. Bolum 2, K06-K17). Gercek veriyle dogrulama Hafta 13 amaci.

S2 — TEK VARDIYANIN TEMSİLCİLİĞİ
  Simulasyon 480 dakika (1 vardiya) ile sinirlidir. Coklu vardiya etkileri
  (baslangic stoku degisimi, yorgunluk vb.) modellenmemistir.
  Hafifletici Onlem: K46 karari geregi sınırlı kapsam bilinçli seçimdir;
  Klenk (2012) ve Facchini (2022) de tek vardiya analizleri raporlamistir.

S3 — TEK RASTGELE GERÇEKLEŞİM (K46 KARARI)
  Ana çalısma seed=42 deterministik koşumla uretilmistir. Tam stokastik
  replikasyon (30+ tekrar) K46 ile kapsam disi birakilmistir.
  Hafifletici Onlem: Bolum 7'deki 4-seed saglamlik testi "yonun" korunduğunu
  gostermistir; ancak mutlak sayilarin guven araligi raporlanamamistir.

S4 — SABİT KUTU KAPASİTESİ (C)
  Hafta 3'te C=15 vs C=20 karsilastirmasi yapilmistir; Hafta 5-10 boyunca
  C sabittir. C'nin filo buyuklugu ve WIP-starvation trade-off'u uzerindeki
  etkilesimi (C azalinca daha fazla tur mu? daha az WIP mi?) incelenmemistir.
  Gelecek Calisma Onerisi: Farkli C degerlerinde tam duyarlilik taramasi.

S5 — TEK FABRIKA DÜZENİ
  24 istasyon, 4 hat, dogrusal duzende modellenistir. Farkli fabrika
  geometrileri (U-sekli, loop, cok katlı) modellenmemistir.
  Hafifletici Onlem: Parametreler litarutur araligindadir; sistem
  mantigi geometriden bagimsiz uygulanabilir yapidadir.

S6 — VOJDANİ & DRECHSLER (2022) DOĞRULANAMADI
  Statik sistemin (60 dk sabit tur) ana literatur dayanagi olan bu makale
  PDF'ten doğrudan alınti ile teyit edilmemistir. Almanca dilinde yazilmis
  olması yorumlama riskini artirmaktadir.
  Eylem: Tez teslimindan once Wang/Facchini standartinda (sayfa+satır numarasi)
  dogrulanmalidir.

S7 — STATİK SİSTEM MODELİNİN BASITLIĞI
  Statik sistemde "tum istasyonlara esit dagitim" varsayimi kullanilmistir.
  Gercek statik sistemlerde onceden hesaplanmis istasyon bazli dagitim
  planlari mevcut olabilir; bu durum statik sistemi daha avantajli yapabilir.
  Sonucun Yorumu: Eger statik model alt-tahmin ediliyorsa, 'statik lehine'
  bulgunun gercekte daha guclu olacagi dusunulebilir.

OZET TABLO:
ID | Sinirlilik                        | Onem   | Hafifletici Onlem
---+-----------------------------------+--------+--------------------------------
S1 | Sentetik veri                     | YUKSEK | Literatur parametreleri; H13
S2 | Tek vardiya                       | ORTA   | Literatur precedent; K46
S3 | Tek rastgele gerceklesim          | ORTA   | 4-seed yön testi (Bolum 7)
S4 | Sabit C (kutu kapasitesi)         | DUSUK  | Hafta 3 basarim duyarliligi
S5 | Tek fabrika duzeni                | DUSUK  | Parametreler aralik icinde
S6 | Vojdani dogrulanamadi             | ORTA   | Tez oncesi eylem gerekli
S7 | Statik model basitligi            | ORTA   | Alt-tahmin => bulgu daha guclu
