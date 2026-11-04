# Literatür Boşluğu Analizi — "Biz Neyi Kapatıyoruz?"

**Tarih:** 26.10.2026
**Amaç:** Makalenin/tezin en kritik savunma noktasını kanıta dayandırmak: literatürde
hangi boşluğu kapattığımızı, hangi iddiaları **kuramayacağımızı** ve hakem itirazlarına
nasıl yanıt vereceğimizi belirlemek.
**Yöntem:** Kaynak klasöründeki 41 özgün çalışmanın yeniden taranması + bu çalışmaların
atıf ağındaki 9 ek çalışmanın web üzerinden araştırılması (Ekim 2026).

---

## 1. Tek Cümlelik Cevap

> **Kapattığımız boşluk, "E-Kanban ile milk-run'ı birleştirmek" değildir — o yapılmıştır.
> Kapattığımız boşluk, bu iki sistemi karşılaştıran çalışmalarda hat yanı tamponun
> hangi politikanın çevrim süresine göre boyutlandırıldığının belirsiz bırakılması ve
> bu belirsizliğin karşılaştırma sonucunun *yönünü* değiştirebilmesidir.**

Bunu destekleyen üç alt katkı Bölüm 4'tedir.

---

## 2. ⚠️ Önce Kötü Haber: Kuramayacağımız İddialar

Mevcut tez metnindeki *"E-Kanban + VRPTW + stok simülasyonunu bütünleşik ele alan çalışma
literatürde yok"* iddiası **savunulamaz**. Aşağıdaki çalışmalar bu iddiayı doğrudan çürütür.
Hakem bunlardan birini bilirse makale reddedilir.

| # | Çalışma | Ne yapmış | Bizim hangi iddiamızı kapatıyor |
|---|---|---|---|
| 1 | **Alnahhal, Ramadan & Noche (2016)**, *Static Versus Dynamic Control of Material Flow in In-Plant Milk Run System*, Dynamics in Logistics, Springer | Push, geleneksel Kanban, e-Kanban ve önerdikleri "adjusted e-Kanban"ı **envanter maliyeti + starvation** ölçütleriyle analitik + simülasyonla karşılaştırmış. Sonuç **koşulludur**: düşük değişkenlikte push, yeterli tren kapasitesinde geleneksel Kanban, kapasite kıtlığında AEK en iyi. | **"Statik vs dinamik koşullu karşılaştırma"** ⚠️ **EN BÜYÜK TEHDİT** |
| 2 | **Ciemnoczolowski & Bozer (2013)**, IJPR 51(2):568–581, *Performance evaluation… Part 2: Number of Kanban and workstation starvation* | Kanban sayısı, araç kapasitesi ve çevrim süresinin **starvation** üzerindeki etkisini modellemiş; deterministik koşulda Kanban sayısı için **alt sınır** türetmiş. | "Kanban sayısı ↔ starvation ilişkisi" |
| 3 | **Bocewicz, Bożejko, Wójcik & Banaszak (2019)**, MPER 10(3):41–53, *Milk-run routing and scheduling subject to a trade-off between vehicle fleet size and storage capacity* | Başlığı birebir bizim ödünleşimimiz: **filo büyüklüğü ↔ depolama kapasitesi**. Anahtar kelimelerinde "trade-off point" var. | "Filo ↔ stok ödünleşimi" |
| 4 | **Zhou & Wen (2024)**, C&IE 190:110080 | **Kanban sayısı ve kutu kapasitesini birlikte** optimize etmiş; hat yanı stok + enerji amaçlarıyla NSGA-II kullanarak **Pareto cepheleri** üretmiş. | "Kanban + kapasite ortak optimizasyonu", "Pareto cephesi" |
| 5 | **Menanno, Savino & Shafiq (2023)**, P&MR 11:2179123 | IT tabanlı Kanban + milk-run; ACO+GA ile dinamik rota; **starvation %43 azalma** raporlamış. | "E-Kanban + dinamik rota entegrasyonu" |
| 6 | **Vojdani & Drechsler (2022)**, Logistics Journal | e-Kanban + esnek rota + simülasyon; %27 az sefer, %29,39 az yol. | "e-Kanban + dinamik rota + simülasyon" |
| 7 | **Kundu, Rossini & Portioli-Staudacher (2019)**, IJIEC 10:421–442 | DES + PSO; açıkça **"kanban boyutu ↔ kanban sayısı ödünleşimi"**ni kendi özgün katkısı ilan etmiş. | "Kanban boyutlandırma ödünleşimi" |
| 8 | **Urru, Bonini & Echelmeyer (2018)** s.406 + **Schmidt, Meinhardt & Schulze (2016)** s.3–4 + **VDI 5586 Blatt 2 (2022)** | Tampon formülü $q_{A,H} = 1 + \lceil n_{LT,A,H}\rceil$ — "+1 değişim pozisyonu" **yerleşik standarttır**. | "VDI +1 kuralı" — bu bizim **bulgumuz değil**, uyguladığımız standarttır |
| 9 | **Elloumi, Ammar & Benaissa (2025)**, JIPE 42(6) | Koşu-içi uyarlanabilir Kanban (AKS), PSO ile. | "Dinamik Kanban" |

**Sonuç:** Yukarıdaki dokuz başlığın hiçbiri bizim özgün katkımız olarak sunulamaz.

---

## 3. İyi Haber: Üç Çalışmanın Kendi Sınırı Bizim Alanımız

| Çalışma | Kendi sınırı | Bize açtığı alan |
|---|---|---|
| **Alnahhal vd. (2016)** | Rotalar **sabittir**; karşılaştırma tampon boyutlandırmasının politikaya göre nasıl değiştiğini tartışmaz | Rotanın da dinamik olduğu ve tamponun politikaya göre boyutlandığı durum |
| **Facchini vd. (2022)** s.1125 | Zaman penceresi **sabit eşiktir** (25 dk geç / 15 dk erken); istasyonun tüketim hızından bağımsız | Pencerenin istasyonun gerçek stok tükenme anından türetilmesi |
| **Schmidt vd. (2016)** s.1 | *"It is not feasible to formulate the design task as an ordinary optimization problem which can be handled by a solver without any further interaction"* | Tasarımın simülasyon tabanlı taramayla ele alınmasının gerekçesi — **bizim yöntemimizi meşrulaştırır** |

---

## 4. Gerçek Boşluk: Üç Savunulabilir Katkı

### Katkı 1 — Politika-tutarlı boyutlandırma ilkesi (ANA KATKI)

#### 4.1.1 Yazındaki iki kol birbirinden kopuktur

Kaynak klasöründeki 41 çalışma bu açıdan tarandığında, konunun **iki ayrı kolda**
geliştiği ve bu kolların birleşmediği görülmektedir.

**Kol A — Boyutlandırma/planlama yazını.** Gereken tamponun ikmal politikasına bağlı
olduğunu *gösterir*, ancak politikaları performans açısından karşılaştırmaz.

- **Urru, Bonini & Echelmeyer (2018)** s.407: *"with exactly the same data in input, the
  planning has been repeated applying the method proposed in this paper for three
  different reordering methods: Kanban card, e-Kanban and direct order."*
  Tablo 2'deki sonuç belirleyicidir: **aynı sistem, aynı talep, farklı yeniden sipariş
  yöntemi → farklı tampon ihtiyacı.** Hat çıktısı arttıkça push (forecast-driven)
  yönteminde tampon sabit 18 kalırken, Kanban kartında 23'e, e-Kanban'da 20'ye, doğrudan
  siparişte 19'a çıkmaktadır. Aynı sayfada yöntem farkının ihmal edilmesinin tamponun
  **eksik boyutlandırılmasına** yol açacağı belirtilir.
- **Droste & Deuse (2011)** s.607–608, Şekil 4: 120 dk'lık çevrim 120 birim stok
  gerektirirken, çevrim 60 veya 30 dk'ya indiğinde gereken stok orantılı olarak düşer.
- **Schmidt, Meinhardt & Schulze (2016)** s.3–4: $q_{A,H} = 1 + \lceil n_{LT,A,H}\rceil$ —
  VDI formülünün ikinci bağımsız teyidi.
- **Ciemnoczolowski & Bozer (2013) Part 2** s.570, Denk. 2–3: kanban alt sınırı
  $k_i^{LB} = \lceil 2r_i - 1/(2n_i)\rceil$, pratikte $\lceil 2r_i\rceil$; $r_i$ bir çevrimde
  tüketilen kutu sayısıdır → gereken kart sayısı **çevrim süresiyle büyür** (üçüncü bağımsız
  dayanak). Özet (s.568): *"the number of Kanban and the physical capacity of the tugger have
  a bigger impact on workstation starvation than the prescribed cycle time"* — boyutlandırmanın
  duruşu politika parametresinden daha çok belirlediği bulgumuzla aynı yöndedir (K104).

**Kol B — Politika karşılaştırma/simülasyon yazını.** Politikaları performans açısından
karşılaştırır, ancak tamponu politikanın çevrim süresinden **türetmez**.

| Çalışma | Neyi karşılaştırıyor | Tampon/Kanban nasıl belirlenmiş | Politika-tutarlı mı? |
|---|---|---|---|
| **Vojdani & Drechsler (2022)** s.5 | Geleneksel (saatlik sabit tur) ↔ dijitalleşmiş dinamik | *"ein identisches Layout und identische Taktzeiten"*; her iki sistemde de **aynı iki kutulu Kanban** | **HAYIR** — çevrim süreleri farklı, tampon aynı |
| **Chee, Chong & Chin (2012)** s.392 | Push ↔ milk-run Kanban (MRKS) | *"nr and nk are applied to MRKS only, whereas nbf is applied to the push system only"*; her ikisine de aynı aralık {2, 4, 6} | **KISMEN** — parametre taraması var, formülle türetme yok |
| **Alnahhal & Noche (2015)** s.117 | Talep-odaklı ↔ Kanban ↔ kendi yöntemleri | *"K values were chosen so that fill rate is greater than or equal to 99%"* | **KISMEN** — eşitleme ölçütü *hizmet düzeyi*, çevrim süresi değil |
| **Pekarcikova vd. (2020, 2021)** | Mevcut durum ↔ e-Kanban | `KanbanBuffer` min 10 / maks 50 / çekme 15 — sabit | **HAYIR** |
| **Menanno vd. (2023)** s.14 | Geleneksel Kanban ↔ IT tabanlı Kanban + MRS | $Q_{min}$ 35–55 aralığı taranmış | **HAYIR** — tek sistemin optimizasyonu |
| **Alnahhal, Ramadan & Noche (2016)** | Push ↔ Kanban ↔ e-Kanban ↔ AEK | Erişilemedi (klasörde yok); özette boyutlandırma ölçütü belirtilmiyor | **BİLİNMİYOR** ⚠️ |

#### 4.1.2 Kol A'ya eklenen iki kaynak (26.10.2026'da edinildi ve okundu)

- **Bocewicz vd. (2019)** s.45 — ilkenin en güçlü matematiksel ifadesi:
  *"if fewer trains are used, then delivery periods $T_P$ become longer, making it
  necessary to increase buffer capacity $S_B$. And conversely, a reduction of the
  admissible capacity of the buffers $S_B$ necessitates the use of a larger number of
  tugger trains $K$."*
  Çalışma, filo büyüklüğü ↔ depolama kapasitesi $(K, S_B)$ ödünleşim noktalarını
  belirler ve takt süresi ile ikmal partisi arasındaki ilişkinin **doğrusal olmadığını**
  gösterir (s.41, özet). **Ancak tek politika içindedir** (periyodik, sabit rota, sabit
  takt); politikalar arası karşılaştırma yoktur ve duruş ölçülmez — uygun teslim planı
  kısıtı duruşu zaten yasaklar.
- **Kundu, Rossini & Portioli-Staudacher (2019)** s.422 — boşluğun literatürdeki
  doğrudan itirafı: *"The dimensioning of this kind of refilling system, **albeit often
  carried out without adopting a specific technique**, has recently attracted the
  attention of several researchers."*

#### 4.1.3 🎯 Boşluğun literatür tarafından açıkça ilan edilmesi

Kundu vd. (2019) s.423, Monden (2011)'e dayanarak iki politika ailesini tanımlar:

| Politika | Literatürdeki adı | Bu çalışmadaki karşılığı |
|---|---|---|
| Sabit miktar, değişken zaman | **reorder point policy** | **P3** (olay tabanlı, ROP tetiklemeli) |
| Sabit zaman, değişken miktar | **periodic review policy** | **P2** (sabit takt, Kanban miktarı) |

Hemen ardından şunu yazarlar:

> *"This research utilizes the fixed time, variable quantity solution and **does not
> investigate the differences with the other policy. This could however be the subject
> of future research.**"*

**Bu, tam olarak bu çalışmanın yaptığı şeydir.** Literatürün kendisi, iki politika
ailesinin karşılaştırılmasını açık bir gelecek çalışma konusu olarak ilan etmektedir.
Bu alıntı makalenin giriş bölümünde **doğrudan kullanılmalıdır**.

#### 4.1.3b 🎯 Yazında çelişen sonuçlar (04.11.2026)

Periyodik (milk-run) ile olay tabanlı (talep üzerine / e-Kanban) beslemeyi karşılaştıran
çalışmalar **birbirine ters sıralamalar** raporlamaktadır:

| Çalışma | Tampon nasıl eşitlenmiş | Sonuç |
|---|---|---|
| **Bae, Evans & Summers (2016)**, WSC, s.2860–2867 | Her iki sistemde **aynı akış raf**; duruş "teslimler arası > 45 dk" olarak politikadan bağımsız tanımlı → örtük **eşit kart** | Tek araçla talep üzerine sistemde duruş milk-run'ın **≈4 katı**; iki araçla fark yok → **milk-run önde** |
| **Vojdani & Drechsler (2022)** s.5–6 | Her iki sistemde **aynı iki kutulu Kanban** → eşit kart | Dijital %27 daha az sefer, %29 daha az yol → **dijital önde** (taşıma ölçütlerinde) |
| **Alnahhal vd. (2016)** (özetten) | Bilinmiyor | **Koşullu** (araç kapasitesine bağlı) |
| **Bu çalışma (K97/K105)** | Dört kural yan yana | Aynı sistemde kurala göre **iki yönde de** sonuç üretilebilir (Toyota kutularında B → geleneksel, A/C/D → dijital) |

→ **Konumlandırma cümlesi:** Yazındaki çelişkili sıralamaların bir kısmı, karşılaştırmada
kullanılan (çoğunlukla örtük) tampon eşitleme kuralıyla açıklanabilir.

#### 4.1.3c ⚠️ Rakip yazın: "adil karşılaştırma" üretim kontrolünde biliniyor (04.11.2026)

Karşılaştırma tabanının sonucu etkilediği fikri **üretim kontrolü (kanban/CONWIP)
yazınında bilinmektedir**; makalede mutlaka atıf yapılmalı ve katkı buna göre
konumlandırılmalıdır:

- **Bonvik, Couch & Gershwin (1997)**, IJPR: mekanizmaları **eşit hizmet düzeyinde**
  (%99,9 için gereken en az envanter) karşılaştırır.
- Kanban–CONWIP karşılaştırmalarının bir kısmı **eşit WIP**, bir kısmı **eşit çıktı** tabanını
  kullanır ve sonuçlar çelişir; ayrıca kanban/CONWIP yalnızca **en çok** WIP'i kontrol eder,
  ortalama WIP sonuçtur (Framinan, Gonzalez & Ruiz-Usano 2003 derlemesi ve atıf yapanlar).
- **Geraghty & Heavey (2005)**, OR Spectrum 27:435–457 ✅ *okundu (04.11.2026)*: beş stratejinin
  kontrol parametreleri kısmi sayımla taranır, her biri için *"minimum WIP required by each PCS
  to achieve a targeted Service Level"* karşılaştırılır (§5, s.448–454; Tablo 4, s.453); ölçüt
  *"Service Level vs. WIP trade-off"*. → Her stratejinin **kendi en iyi eğrisi** üzerinde
  karşılaştırma — bizim "duruş–WIP düzleminde raporla" önerimizin üretim kontrolündeki
  **yerleşik karşılığı** (önerimizi destekler; fikrin bize ait olmadığını da doğrular).
- **Enns (2008)**, WSC: push–CONWIP karşılaştırmasının adil kurulması (eşit bırakma hızı).
- Amos vd. (aktaran MDPI Processes 2022, 10(1):5): her mekanizma **önce kendi en iyi ayarına**
  getirilip öyle karşılaştırılmalı.

**Sonuç:** "Karşılaştırma tabanı önemlidir" genel ilkesi **bizim katkımız değildir**. Katkı,
(a) bu ilkenin **fabrika içi hat besleme / milk-run** yazınına taşınması, (b) bu alanda
kullanılan **dört somut kuralın** (eşit kart, politika-tutarlı formül, eşit hizmet, eşit WIP)
aynı sistemde **sayısal olarak** karşılaştırılması ve (c) alandaki **çelişkili bulguların**
bununla açıklanabileceğinin gösterilmesidir. ⚠️ Bonvik (1997) ve Geraghty & Heavey (2005) tam
metinleri edinilip okunmalıdır (kapalı erişim). — Geraghty & Heavey (2005) 04.11.2026'da
edinildi ve okundu; Bonvik vd. (1997) hâlâ eksik.

**Makale cümlesi (Tartışma):** Üretim kontrolü yazınında stratejiler hizmet düzeyi–envanter
eğrisi üzerinden, her strateji kendi en iyi parametreleriyle karşılaştırılmaktadır (Geraghty
& Heavey 2005). Fabrika içi hat besleme yazınında ise karşılaştırmalar çoğunlukla tek bir
eşitleme noktasında yapılmakta ve çelişkili sonuçlar vermektedir (Bae vd. 2016; Vojdani &
Drechsler 2022). Bu çalışma, tek noktalı karşılaştırmaların eşitleme kuralına duyarlılığını
sayısal olarak göstermekte ve eğri tabanlı karşılaştırmanın bu alana da uygulanmasını
önermektedir.

#### 4.1.4 Boşluğun formülasyonu

> Tamponun politikaya bağlı olduğunu gösteren çalışmalar (Kol A) politikaları performans
> açısından karşılaştırmamakta; politikaları karşılaştıran çalışmalar (Kol B) ise tamponu
> politikanın çevrim süresinden türetmemektedir. **İki kol birleştirilmemiştir** — ve
> Kundu vd. (2019) s.423 bu birleştirmeyi açıkça gelecek çalışma olarak önermektedir.

#### 4.1.5 ⚠️ Karşı kanıt: dürüstlük payı

Kundu vd. (2019) s.423 aynı sayfada şunu da yazar: *"The comparison of different feeding
policies has been relatively well covered"* ve Limère vd. (2012), Golz vd. (2012),
Sali vd. (2015), Faccio (2014), Caputo & Pelagagge (2011) çalışmalarını sayar.
Dolayısıyla **"politika karşılaştırması yapılmamıştır" denemez.** İddiamız yalnızca
şudur: karşılaştırmalarda *tamponun politikaya göre türetilmesi* ve bu seçimin
sonuca etkisinin ölçülmesi yapılmamıştır.

Dürüstlük notu: Kol B'deki iki çalışma adil karşılaştırma kaygısı taşımaktadır — Alnahhal
& Noche (2015) hizmet düzeyini eşitler, Chee vd. (2012) parametre taraması yapar ve hatta
push lehine kısıtları gevşeten bir "mükemmel push" senaryosu kurar (s.393). Dolayısıyla
iddiamız *"kimse düşünmemiş"* değil, **"tampon, politikanın kendi çevrim süresinden
formülle türetilmemiş ve bu seçimin sonucu nasıl değiştirdiği ölçülmemiştir"** olmalıdır.

**Katkımız.** Bu ihmalin sonucu **yönünü değiştirdiğini** sayısal olarak gösteriyoruz.
Vojdani & Drechsler (2022)'nin karşılaştırma tasarımı (her iki sistemde aynı iki kutulu
tampon) uygulandığında dijital sistem talep şokunda **9,03 puan** önde görünürken, her
politika kendi formülüyle boyutlandırıldığında fark kapanmaktadır (K93). Bu kayma, Toyota
formülünün önerdiği parametre bandının **12 hücresinin tamamında sıralamayı
değiştirmektedir** (K95). Yeterli filoda politikalar arasındaki duruş farkı 1 puanın
altında kalır; dinamik sistemin üstünlüğü duruşta değil **stoktadır** (K96).

**Katkının genelleştirilmesi (K97, nihai ayar K105).** Yazında kullanılan dört eşitleme
kuralı — eşit kart (Vojdani & Drechsler 2022), politika-tutarlı formül (Urru vd. 2018; VDI
5586), eşit hizmet düzeyi (Alnahhal & Noche 2015) ve eşit WIP — aynı sistemde
uygulandığında: (a) dijital ile geleneksel arasındaki duruş farkı kurala göre **−17,3 ile
+2,0 puan** arasında değişmektedir; (b) Toyota kutu boyunda politika-tutarlı kural
geleneksel sistemi, diğer üç kural dijital sistemi kazandırmaktadır; (c) duruş–WIP
düzlemindeki Pareto yargısı kurala göre "baskın" ile "takas" arasında değişmektedir.
Önerilen ilke: karşılaştırma çalışmaları eşitleme kuralını açıkça belirtmeli ve
sonuçlarını duruş–WIP düzleminde (Pareto) raporlamalıdır.

**Neden güçlü.** Olumlu bir metodolojik ilke önerir ("politika-tutarlı boyutlandırma"),
yalnızca hata düzeltmez. Kendi önceki sonucumuz üzerinde gösterildiği için etik olarak
da sağlamdır — başkasının çalışmasını değil, kendi v1 modelimizi eleştiriyoruz.

### Katkı 2 — Model kurma hatalarının ayrıştırılmış etkisi

**Boşluk.** Simülasyon yazınında doğrulama/geçerleme (verification & validation) yaygındır;
ancak **hangi modelleme kararının sonucu ne kadar değiştirdiğini tek tek ayrıştıran**
(ablation benzeri) bir uygulamaya rastlanmamıştır. Herrera-Vidal vd. (2026) s.9–10 bile
yalnızca replikasyon ve ısınma yeterliliğini ele alır.

**Katkımız.** Sekiz adımlı kümülatif ayrıştırma (revizyon raporu Bölüm 4.1):

| Modelleme kararı | Duruş oranına etkisi |
|---|---|
| Hizmet süresi asimetrisi (statik 3 dk / dinamik 8 dk per durak) | **−10,34 puan** |
| Açık döngü sinyal üretimi (sinyaller önceden, LT varsayımıyla) | **%24,58 → %6,85** |
| Durak sınırının kaldırılması | +5,76 puan |
| Eksik raf boyutlandırma (VDI "+1" yok) | −3,88 puan (p<0,001) |
| Metrik olmayan mesafe matrisi | −0,86 puan |

**Neden güçlü.** Pratik bir uyarı üretir: bu büyüklükteki etkiler, iki politika arasındaki
gerçek farktan (≈1 puan) büyüktür. Yani modelleme kararları, politika seçiminden daha
belirleyici olabilmektedir.

### Katkı 3 — Tüketim hızından türetilen dinamik zaman penceresi

**Boşluk.** Facchini vd. (2022) s.1125 sabit eşik kullanır (25 dk geç / 15 dk erken).
Taramamızda, teslim son tarihini **istasyonun anlık stokundan ve tüketim hızından**
hesaplayan bir formülasyona rastlanmamıştır:

$$t_{starv} = t + \frac{Stok(t)}{D_{dk}}, \qquad
TW_{bitis} = \max\Big(\min\big(t_{starv} - \tau,\; t + TW_{max}\big),\; t + LT\Big)$$

**Katkımız.** Pencere, istasyonun kırılganlığına göre kendiliğinden daralır; yüksek
tüketimli istasyon otomatik olarak daha sıkı pencere alır.

**⚠️ Dikkat.** Bu en dar katkıdır ve "bulunamadı ≠ yoktur". Makalede **"taranan
literatürde rastlanmamıştır"** biçiminde ihtiyatlı yazılmalı, ana katkı olarak
sunulmamalıdır.

---

## 5. Makalede Savunulacak Cümleler (Kullanıma Hazır)

### Giriş — literatür boşluğu paragrafı

> Yalın üretimde fabrika içi malzeme besleme iki politika ailesiyle yürütülür: sabit
> zamanlı, değişken miktarlı periyodik sevk (milk run) ve sabit miktarlı, değişken
> zamanlı çağrı sistemi (Bozer & Ciemnoczolowski 2013; Kundu vd. 2019). Bu iki aile
> sıkça karşılaştırılmıştır: Alnahhal vd. (2016) push, geleneksel Kanban ve e-Kanban'ı
> envanter maliyeti ve hat duruşu ölçütleriyle karşılaştırmış ve sonucun koşullara bağlı
> olduğunu göstermiştir; Menanno vd. (2023) ve Vojdani & Drechsler (2022) e-Kanban ile
> dinamik rotalamayı bütünleştirmiştir. Öte yandan boyutlandırma yazını, hat yanı
> tamponun politikanın çevrim süresine bağlı olduğunu göstermektedir: gereken stok
> çevrim süresiyle orantılıdır (Droste & Deuse 2011), VDI 5586 tampon katsayısı yeniden
> sipariş yöntemine göre değişir (Urru vd. 2018) ve gereken kanban sayısının alt sınırı
> çevrimde tüketilen kutu sayısıyla büyür (Ciemnoczolowski & Bozer 2013). Ciemnoczolowski
> & Bozer (2013) ayrıca duruşu çevrim süresinden çok kanban sayısının belirlediğini
> bulmuştur. Buna karşılık politika karşılaştırmalarında tamponun nasıl eşitlendiği
> çoğunlukla açıkça tartışılmamaktadır: Vojdani & Drechsler (2022) iki sisteme aynı iki
> kutulu tamponu verir, Alnahhal & Noche (2015) tamponu eşit hizmet düzeyine göre seçer.
> Kundu vd. (2019) iki politika ailesinin karşılaştırılmasını açıkça gelecek çalışma
> olarak bırakmıştır. Bu çalışma, yazındaki dört eşitleme kuralını aynı sistemde yan yana
> koyarak karşılaştırma sonucunun bu seçime ne ölçüde bağlı olduğunu göstermektedir.

### Giriş — katkı maddeleri

> Bu çalışmanın katkıları şunlardır:
> 1. Malzeme besleme politikalarının karşılaştırılmasında kullanılan **dört eşitleme
>    kuralı** (eşit kart, politika-tutarlı formül, eşit hizmet düzeyi, eşit WIP) aynı
>    sistemde karşılaştırılmakta; kuralın farkın büyüklüğünü yaklaşık 20 puanlık bir
>    aralıkta, küçük kutu boyunda ise kazananı değiştirdiği gösterilmektedir. Buradan,
>    karşılaştırma çalışmalarının eşitleme kuralını açıkça belirtmesi ve sonuçları
>    duruş–WIP düzleminde raporlaması gerektiği ilkesi çıkarılmaktadır.
> 2. Bağımsız bir çalışmanın karşılaştırma tasarımı (Vojdani & Drechsler 2022, ortak iki
>    kutulu tampon) uygulandığında dijital sistemin 2,4–16,0 puan önde göründüğü, her
>    politika kendi çevrim süresine göre boyutlandırıldığında bu farkın %80–100 küçüldüğü
>    ya da tersine döndüğü gösterilmekte; bulgu Toyota formülü parametre bandında, üç
>    vardiyalık ufukta ve gerçekleşebilir bir mesafe ağında sınanmaktadır (52 koşul).
> 3. Modelleme kararlarının (tampon boyutlandırma, hizmet süresi simetrisi, kapalı döngü
>    sinyal üretimi, metrik mesafe) sonuç üzerindeki etkileri **tek tek ayrıştırılarak**
>    ölçülmekte; bu etkilerin politikalar arasındaki farktan büyük olabildiği
>    gösterilmektedir.
> 4. E-Kanban sinyalinin zaman penceresi istasyonun anlık stokundan ve tüketim hızından
>    türetilerek rotalamaya bağlanmaktadır (taranan yazında bu biçimde rastlanmamıştır).

### Tartışma — Alnahhal vd. (2016) ile ilişkilendirme (ZORUNLU)

> ⚠️ Alnahhal vd. (2016) tam metnine erişilememiştir; aşağıdaki paragraf yalnızca
> çalışmanın özetine dayanır. Yazarın doktora tezi (Duisburg-Essen) edinilirse
> eşitleme yöntemi kontrol edilip paragraf güncellenmelidir.

> Bulgularımız Alnahhal vd. (2016) ile aynı yöndedir: her iki çalışmada da politikalar
> arasındaki üstünlük koşullara bağlıdır. İki çalışma farklı mekanizmalara işaret
> etmektedir: Alnahhal vd. üstünlüğü bilgi akışının hızına (RFID ile ayarlanmış
> e-Kanban) ve araç kapasitesine bağlarken, bu çalışma karşılaştırmanın nasıl adil
> kılındığının sonucu tek başına değiştirebildiğini göstermektedir. Ayrıca Alnahhal vd.
> sabit rota varsayarken, bu çalışmada rota olay tabanlı olarak yeniden kurulmaktadır.

### Tartışma — Sugimori vd. (1977) ve uyarlanan ROP

> Uyarlanan ROP, küçük kutularda dijital sistemin şok altındaki duruşunu azaltmış, ancak
> bunu duruş–WIP eğrisi boyunca, yani kart eklemekle eşdeğer biçimde yapmıştır (K98).
> Bu, Sugimori vd. (1977, s.562)'nin ilkesiyle tutarlıdır: kanban sayısı talep
> değişse de sabit tutulur ve talep artışına tedarik süresi kısaltılarak yanıt verilir.

### Sonuç — ana cümle

> Bu çalışmanın temel bulgusu, fabrika içi besleme politikalarının karşılaştırılmasında
> **sonucun, karşılaştırmanın nasıl adil kılındığına bağlı olduğudur**: aynı iki sistem
> arasındaki duruş farkı, yazında kullanılan dört eşitleme kuralına göre −17 ile +2 puan
> arasında değişmekte, küçük kutu boyunda kazanan tersine dönmektedir. Her politika kendi
> çevrim süresine göre boyutlandırıldığında dijital sistem yeterli filoda geleneksel
> sisteme göre 0,2–1,9 puan daha az duruş ve %37–41 daha az stokla çalışmaktadır.

---

## 6. Hakem İtirazları ve Hazır Yanıtlar

| İtiraz | Yanıt |
|---|---|
| *"Bu zaten Alnahhal vd. (2016)'da var."* | Yön olarak tutarlıyız ve bunu açıkça yazıyoruz. Fark: (a) onlarda rota sabit, bizde olay tabanlı; (b) onlar mekanizmayı bilgi akışı hızına bağlıyor, biz boyutlandırmaya; (c) biz etkiyi ayrıştırarak ölçüyoruz. |
| *"VDI +1 kuralı yeni değil."* | Doğru, ve bunu kendi katkımız olarak sunmuyoruz. Katkımız kuralın **ihmal edilmesinin karşılaştırmalı sonuçları nasıl etkilediğini** ölçmektir. |
| *"Pareto analizi Zhou & Wen (2024)'te var."* | Onlar metasezgisel (NSGA-II) ile hat yanı stok + enerji amaçlarını optimize ediyor. Biz 24 istasyonluk ölçekte tam ızgara tarıyoruz ve amaçlarımız WIP + duruş + mesafe. Pareto'yu katkı olarak değil, **yöntem** olarak sunuyoruz. |
| *"Sentetik veri kullanmışsınız."* | Kabul ediyoruz (S1). Ancak katkımız **metodolojiktir**: boyutlandırma tutarsızlığının etkisi, verinin gerçek olup olmamasından bağımsız olarak gösterilebilir. Parametreler literatür bandındadır. |
| *"Rotalama sezgiseliniz zayıf."* | Açıkça raporluyoruz: Solomon'da OR-Tools'tan %102,7 geride. Ancak fabrika içi turlar 2–8 duraklı ve tur-içi sapmamız tam numaralamaya göre %0,62. Bunu sınırlılık (S8) olarak yazdık. |
| *"Sevk kuralları arasında fark yoksa katkı ne?"* | Bu **olumsuz ama bilgilendirici** bir bulgudur: çoklu karşılaştırma düzeltmesiyle (ANOVA + Tukey) sevk kuralı seçiminin, boyutlandırma kararları yanında önemsiz kaldığını gösteriyoruz. Önceki kendi bulgumuzu da bu yolla düzeltiyoruz. |

---

## 7. Kaynak Durumu (03.11.2026)

Konunun merkezindeki kaynakların durumu. Ayrıntılı notlar: `master_makale_katalogu.md` EK
bölümü; denetim: `python -X utf8 -m src.kaynak_arsivi_denetimi`.

| Durum | Çalışma | Ne kattı |
|---|---|---|
| 🔴 **Edinilemedi** | **Alnahhal, Ramadan & Noche (2016)**, *Static Versus Dynamic Control of Material Flow in In-Plant Milk Run System*, Dynamics in Logistics, Springer, doi:10.1007/978-3-319-23512-7_70 | Ana karşılaştırmanın en yakın öncülü. Yalnızca özetten atıf yapılır; yazarın açık erişimli doktora tezi (Duisburg-Essen, DuEPublico) aynı çalışmayı içerir |
| ✅ Okundu | **Ciemnoczolowski & Bozer (2013) Part 2**, IJPR 51(2):568–581 | Kanban alt sınırı çevrim süresiyle büyür (s.570); duruşu çevrim süresinden çok kanban sayısı belirler (s.568) — K104 |
| ✅ Okundu | **Bozer & Ciemnoczolowski (2013) Part 1**, IJPR 51(2):555–567 | P2/P3 sınıflandırmasının ikinci dayanağı (s.555) — K103 |
| ✅ Okundu | **Bocewicz vd. (2019)**, MPER 10(3):41–53 | Filo ↔ tampon ilkesi (s.45) — 4.1.2 |
| ✅ Okundu | **Schmidt, Meinhardt & Schulze (2016)**, IMHRC | VDI tampon formülü (s.3–4), simülasyon gerekçesi (s.1) — K104 |
| ✅ Okundu | **Kundu, Rossini & Portioli-Staudacher (2019)**, IJIEC 10:421–442 | Boşluk ilanı (s.423) — 4.1.3 |
| ✅ Okundu | **Sugimori, Kusunoki, Cho & Uchikawa (1977)**, IJPR 15(6):553–564 | Kanban formülü (s.561), kart sayısı sabit ilkesi (s.562) — K103 |
| ✅ Okundu | **Korytkowski & Karkoszka (2016)**, IJAMT 82:827–837 | Duruş tanımı (s.834), periyodik beslemenin dayanıklılığı |
| 🟡 Gerekmez | **VDI 5586 Blatt 2 (2022-07)** | Ücretli standart; yılı doğrulandı, Urru ve Schmidt üzerinden atıf |

---

## 8. Önerilen Başlık Revizyonu

Mevcut başlık entegrasyonu vurguluyor; oysa entegrasyon artık yeni değil. Boyutlandırma
vurgusu öne çıkarılmalıdır.

| | Başlık |
|---|---|
| Mevcut | Dinamik Milk-Run Rota ve E-Kanban Karar Destek Sistemi |
| **Öneri A** | **Fabrika İçi Milk-Run Politikalarının Karşılaştırılmasında Politika-Tutarlı Tampon Boyutlandırmanın Etkisi: Bir Simülasyon Çalışması** |
| **Öneri B** | **Statik ve Dinamik Milk-Run Besleme Politikalarının Adil Karşılaştırılması: Boyutlandırma Varsayımlarının Sonuçlar Üzerindeki Etkisi** |
| **✅ Öneri C (K105 sonrası, önerilen)** | **Fabrika İçi Milk-Run Besleme Politikalarının Karşılaştırılmasında Eşitleme Kurallarının Etkisi: Bir Simülasyon Çalışması** |

---

## 9. Özet Konumlandırma

**Ne diyoruz:** "Entegre bir sistem kurduk" değil → **"Bu karşılaştırmaların nasıl
yapılması gerektiğini gösteriyoruz."**

**Neden önemli:** Ölçtüğümüz modelleme etkileri (10+ puan), politikalar arasındaki gerçek
farktan (≈1 puan) büyüktür. Bu, yazındaki benzer karşılaştırmaların bir kısmının
boyutlandırma yanlılığı taşıyabileceği anlamına gelir.

**Hangi dergi:** Endüstri Mühendisliği Dergisi (TMMOB) veya JTOM. Metodolojik katkı
niteliği, uygulamalı bir vaka çalışmasından çok bir yöntem tartışmasına uygundur; bu
nedenle "Materyal ve Yöntem" bölümü ağırlıklı yazılmalı ve ayrıştırma tablosu (Bölüm 4.1)
makalenin merkezine konmalıdır.

---

## 10. Özdeğerlendirme — Yenilik Ne Kadar Güçlü? (26.10.2026)

> Bu bölüm, danışman ve hakem karşısına çıkmadan önce yapılan **dürüst iç
> değerlendirmedir**. Amaç, savunulamayacak bir iddiayla sunuma girmeyi önlemektir.

### 10.1 Tek cümlelik yargı

> **Çalışma literatürde bir açık kapatmaktadır — ancak tek bir tane, ve bu açık
> "yeni yöntem geliştirme" türünden değil, "mevcut yöntemler yanlış karşılaştırılıyor"
> türündendir. Teknik/kavramsal yenilik yoktur; metodolojik yenilik vardır.**

### 10.2 Katkı türünün doğru adlandırılması

| Katkı türü | Var mı? | Açıklama |
|---|---|---|
| Yeni algoritma / model sınıfı | ❌ | NN+2opt yerleşik; Kanban formülü Toyota (1977) |
| Yeni sistem mimarisi | ❌ | E-Kanban + VRPTW entegrasyonu yapılmış (Menanno, Vojdani, Alnahhal) |
| Yeni ödünleşim keşfi | ❌ | Filo ↔ stok (Bocewicz 2019), Kanban boyutu ↔ sayısı (Kundu 2019) |
| **Metodolojik uyarı + ölçüm** | ✅ | Boyutlandırma tutarsızlığının karşılaştırmayı yanlı hale getirmesi |
| **Literatürce ilan edilmiş boşluğun doldurulması** | ✅ | Kundu vd. (2019) s.423: P2 ↔ P3 karşılaştırması "gelecek çalışma" |
| **Dürüst olumsuz/koşullu bulgu** | ✅ | Yazında nadir; kendi önceki sonucunu çürütmek |

### 10.3 Katkının gücü: hedefe göre gerçekçi değerlendirme

| Hedef | Yeterlilik | Gerekçe |
|---|---|---|
| Lisans / YL tasarım çalışması | ✅ **Fazlasıyla yeterli** | Kapsam, doğrulama ve karar izlenebilirliği beklentinin üzerinde |
| **TR Dizin** (End. Müh. Dergisi, JTOM) | ⚠️ **Sınırda** | Metodolojik katkı yeterli; **gerçek veri yokluğu** ana engel. Endüstri Mühendisliği Dergisi vaka çalışmasına öncelik vermektedir |
| SCI-E (Gazi, IJPR vb.) | ❌ **Yetersiz** | Katkı artımsaldır (incremental); yeni model/algoritma yoktur |

**Sınırda kalmanın tek sebebi:** gerçek fabrika verisi yoktur. Hakemin doğal sorusu
*"sentetik veride ölçülen bu yanlılık gerçek sistemde de bu büyüklükte midir?"*
olacaktır ve mevcut hâliyle bu soruya veri temelli yanıt verilememektedir.

### 10.4 Katkıyı güçlendirmenin üç yolu (etki sırasına göre)

#### Yol 1 — Gerçek veri (en yüksek etki) 🔴

Tek vardiyalık gerçek tüketim verisi bile yeterlidir. Altyapı hazırdır:
`data/config.json → "real"` ve `data/real/*.csv` şablonları beklemektedir.
Bu tek adım makaleyi TR Dizin eşiğinin **üzerine** taşır ve S1 sınırlılığını kapatır.

#### Yol 2 — İddiayı küçült, kanıtı büyüt 🟠

*"Entegre bir KDS geliştirdik"* iddiası **terk edilmelidir**. Yerine konacak cümle:

> Besleme politikası karşılaştırmalarında tampon boyutlandırma tutarsızlığı,
> politikalar arasındaki gerçek farktan büyük bir yanlılık üretmektedir.

Bu iddianın ardındaki sayı çarpıcıdır ve elimizdedir:

| Kaynak | Duruş oranına etkisi |
|---|---|
| Hizmet süresi asimetrisi | **10,34 puan** |
| Açık döngü sinyal üretimi | %24,58 → %6,85 |
| Eksik raf boyutlandırma | 3,88 puan |
| **Politikalar arasındaki gerçek fark** | **≈ 1 puan** |

#### Yol 3 — Katkıyı kendi modelinin dışına taşı ✅ **TAMAMLANDI (26.10.2026)**

**Neydi:** Düzeltilen hata **kendi v1 modelimizdeydi**; hakem *"kendi hatasını düzeltmek
katkı mıdır?"* diye sorabilirdi.

**Yapılan:** Vojdani & Drechsler (2022) s.5'in karşılaştırma tasarımı — *"identisches
Layout und identische Taktzeiten"* + **aynı iki kutulu Kanban** — v2 motorunda yeniden
kuruldu (`src/v2_boyutlandirma_duyarliligi.py`, K93). İki kurgu karşılaştırıldı:
**A** = tüm politikalar $N=2$ (ortak tampon), **B** = her politika kendi formülüyle.

**🎯 Sonuç (3 araç, 12 replikasyon):**

| Talep | Kurgu A (ortak tampon) | Kurgu B (politika-tutarlı) | Tasarım kayması |
|---|---:|---:|---:|
| Baz | dijital **2,33 puan** önde | dijital 0,14 puan önde | 2,19 puan |
| **Şok +%50** | dijital **9,03 puan** önde | geleneksel 0,04 puan önde | **9,07 puan — sıralama değişti** |

**Mekanizma:** Kurgu A'da her iki sistem **48 kart** alır. Kurgu B'de geleneksel sistem
**63 karta** çıkar (60 dk çevrim daha büyük tampon gerektirir), dijital **49**'da kalır.
Geleneksel sistem hak ettiği tamponu alınca fark kapanır.

**✅ Vojdani'nin kendi bulgusu doğrulandı:** dijital sistem her iki kurguda da daha az
sefer yapar (−%10…−%11; Vojdani %−27) ve **WIP avantajı yalnızca Kurgu B'de görünür
hale gelir (−%37…−%38)**. Yani taşıma verimliliği bulgusu etkilenmez; etkilenen yalnızca
**duruş karşılaştırmasıdır**. Bu, çalışmanın Vojdani'yi çürütmediğini, onun tasarımının
farklı bir soruya (duruş) taşınması durumundaki sınırını gösterdiğini kanıtlar.

**⚠️ Dürüstlük notu (K100 ile güncellendi):** Eski mesafe matrisinde dijital sistem
**daha fazla** yol yapıyordu (+%13…+%69), Vojdani ise −%29,39 raporlar. Koordinat tabanlı
(dikdörtgensel, Urru 2018 durak aralığı) ağda baz talepte dijital **−%21…−%23 sefer ve
−%6…−%8 yol** yapar — yön Vojdani ile aynıdır; çelişki metrik olmayan matrisin yan
ürünüdür. Talep şokunda dijital daha fazla yol yapar (+%34…+%37); Vojdani şok koşmamıştır.

**Figür:** `docs/figurler/sekil5_boyutlandirma_duyarliligi.png`

### 10.5 Sonuç

Çalışmanın gücü **yeni bir şey icat etmesinde değil**, kendi sonucunu çürütecek kadar
dürüst olmasında ve bunu sayısallaştırmasındadır. Yazında bu nadirdir.

Zayıflığı ise ikilidir: **sentetik veri** ve katkının **"negatif" karakteri** (bir şeyin
nasıl yapılmaması gerektiğini göstermek). Yol 1 birinciyi, Yol 3 ikinciyi giderir.
