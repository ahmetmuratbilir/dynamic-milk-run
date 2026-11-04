# Hat Besleme Literatür Açığı — Ara Özet (04.11.2026)

> Derin araştırmanın dört taramasından üçünün sonuçlarının özeti. Ayrıntı ve kaynaklar
> aynı klasördeki not dosyalarında. Tehdit taraması (`tehdit_calismalar.md`) tamamlanınca
> nihai rapor `reports/Hat besleme literatür açığı.md` olarak yazılacak.
> Sunumda kullanılabilir.

## Araştırma aşamaları

| # | Tarama | Dosya | Soru |
|---|---|---|---|
| 1 | Tehdit çalışmaları | `tehdit_calismalar.md` | Hat besleme yazınında bizim iddiayı zayıflatan çalışma var mı? |
| 2 | İlan edilmiş boşluklar | `ilan_edilmis_bosluklar.md` | Derlemelerin "gelecek çalışma" dediği, modelimizin kapatabileceği ikinci açık var mı? |
| 3 | Karşılaştırma tabanı yöntembilimi | `karsilastirma_tabani_metodolojisi.md` | "Karşılaştırma şekli sonucu değiştirir" türü katkılar nasıl yayımlanmış? |
| 4 | Dergi uygunluğu | `dergi_uygunlugu.md` | İddia TR Dizin / SCI-E için yeterli mi? |

## 1. Dergi uygunluğu (tarama 4)

- **TR Dizin için katkı yeterli görünüyor.** PAJES 2026'da (Sevim & Görkemli Aykut) varsayımsal
  sistem + sentetik veriyle milk-run simülasyonu yayımlandı → sentetik veri tek başına ret
  gerekçesi değil.
- **En düşük riskli hedef JTOM:** kapsamında simülasyon/lojistik var; kabul oranı %73–83
  (2022–2025); TR Dizin.
- **SCI-E için sınırda:** 2022–2025 milk-run simülasyon makalelerinin çoğu gerçek vaka/ölçüm
  kullanıyor. Gerçek veri olmadan en ucuz güçlendirme: **yayımlanmış bir vakayı yeniden kurup**
  bulguyu orada da göstermek (ör. Korytkowski & Karkoszka 2016'nın 10 istasyonu).
- Aynı soruyu soran 2020–2026 tarihli makale **bulunamadı**.

## 2. Yöntemsel emsaller (tarama 3)

- **En yakın emsal: Enns & Rogers (2008), WSC, s.1867–1872, doi:10.1109/WSC.2008.4736277**
  (tam metin okundu). CONWIP ↔ push; push'a "daha adil" sabit bırakma verilince **sıralama
  tersine dönüyor**; sonuç eğri üzerinde raporlanıyor. Sonuç cümlesi: *"comparison is not
  straightforward … it may not be possible to conclude that either system dominates"*.
  **Yalnızca 16 atıf** → "sonuç karşılaştırmaya bağlı" mesajı tek başına zayıf katkı.
- Üretim kontrolünde bilinen ilke, ama **tasarım kuralı** olarak kullanılıyor, başlık katkısı
  olarak değil: Bonvik vd. 1997 (249 atıf), Framinan vd. 2003 (159), Gstettner & Kuhn 1996 (151;
  kanban kart dağılımı optimize edilince ters sonuç), Muckstadt & Tayur 1995, Geraghty & Heavey
  2005 (44).
- **En güçlü yöntemsel dayanak: Hooker (1995), J. Heuristics 1:33–42 (440 atıf):** *"the parameter
  settings are among the factors one would investigate experimentally … the problem of fair
  comparison becomes a nonproblem"* → "parametreyi tara, eğriyi raporla" önerimizin dayanağı.
- Genel kılavuzlar: Barr vd. 1995, Rardin & Uzsoy 2001, STRESS (Monks vd. 2019).
- **Mekanizma önerisi (çıkarım):** eşit kart sayısı olay tabanlı sisteme avantaj sağlar; aynı
  tampon periyodik sistemde *çevrim + tedarik süresini*, olay tabanlıda yalnızca *tedarik
  süresini* karşılar. K93 bulgusuyla örtüşür.
- **Hat besleme/milk-run alanında bu tür bir makale bulunamadı** → "taranan yazında" diye
  yazılmalı.

**Düzeltmeler:**
- Kaynakça [43] Enns: ikinci yazar **Paul Rogers** ve sayfa aralığı (1867–1872) eklenmeli.
- **"Amos vd." doğrulanamadı** (MDPI Processes 2022 üzerinden aktarılmıştı) → doğrulanana kadar
  kullanılmayacak.

## 3. İlan edilmiş boşluklar (tarama 2)

### 🎯 İkinci açık (yazar tarafından kelimesi kelimesine ilan edilmiş)

**Ciemnoczolowski & Bozer (2013) Part 2, IJPR, s.579:** *"It should be possible in future research
to quantify the relative contributions of the number of Kanban and the tugger capacity to
starvation at each WS."* Onların "kapasite artınca duruş sıfırlanır" sonucu sabit tüketim
varsayımına dayanır; değişken tüketimde sıfır olmayan bir sınır beklerler.

Destek: **Alnahhal, Ridwan & Noche (2014) §VI:** *"lack of studies regarding fast response of the
system to any changes in material demand"*.

**Açık:** Stokastik talep ve talep şoku altında duruşun ne kadarının kart sayısından, ne kadarının
taşıma kapasitesinden geldiğini P2 ve P3 için ayrı ayrı ayrıştırmak; şok sonrası toparlanma
süresini ölçmek. **İlk açıktan (eşitleme kuralı) bağımsız**, ama aynı mesajı tamamlar: duruşu
politikadan çok tampon ve kapasite belirler.

**Model gereksinimi:** kart sayısı × kapasite × politika × şok tam faktöriyel; ANOVA η² ile
varyans ayrıştırma; toparlanma süresi göstergesi. ⚠️ C&B tek çekicinin fiziksel kapasitesini
kastediyor; filo boyutuyla birlikte vagon kapasitesi de taranmalı ya da eşleme açıkça yazılmalı.

### ⚠️ Tehdit: Lieb (2021), TUM doktora tezi

- **s.118–120:** teslim son tarihi istasyon stoku + yoldaki stok + tüketimden ("Bestandsreichweite")
  türetiliyor → **"Katkı 3" (stoktan türetilen zaman penceresi) yeni değil.**
  `literatur_boslugu_analizi.md`'deki "taranan literatürde rastlanmamıştır" ifadesi düzeltilmeli,
  Lieb'e atıf yapılmalı.
- 18 kontrol stratejisi DES ile karşılaştırılmış; WIP ve en az çekici sayısı ana çıktılar
  (10 çekiciye kadar, %59 tasarruf) → "olay tabanlı kontrolde filo boyutu" ve "dinamik statikten
  iyi" yeni iddia olamaz.
- **Destekleyici (s.224):** kalkış zamanı modülü tek anlamlı olmayan iyileştirme → bizim "sevk
  kuralları arasında fark yok" (K82) bulgumuzun dış doğrulaması.
- **Destekleyici (s.119):** en çok hat stoku planlamadan verili alınıyor → ilk açığı destekler.

### Diğer doğrulanmış ilanlar

- Moretti, Tappia & Melacini (2021, HICL) s.129–130, 145: gerçek zamanlı bilginin değeri hâlâ
  eksik; talep düzeyi ve yeniden sipariş politikalarına duyarlılık önerilir (AMR/kitting bağlamı).
- Kundu (2019) s.439: uyarlanabilir kanban gelecek çalışma → K98'i destekler.
- Bocewicz (2019) s.51: değişen talepte yeniden çizelgeleme.
- Alnahhal & Noche (2015) s.118: bilinen talep ve sabit rota sınırlılık.
- Schmidt (2016) s.5–6: "ideal çekici başlangıç aralıkları" açık soru.
- Facchini (2022) s.1126: teslim güvenilirliği (%8 gecikme).
- Emde & Gendreau (2017): döngüsel çizelgeler hat stokunu çoğunlukla iki katından fazla artırır.

## Ara sonuç tablosu

| Açık | Durum |
|---|---|
| 1. Eşitleme kuralı sonucu değiştirir (ana) | Hat besleme alanında yeni; genel ilke üretim kontrolünde biliniyor |
| 2. Duruşta kart sayısı ↔ taşıma kapasitesi payının ayrıştırılması | Ciemnoczolowski & Bozer 2013 tarafından ilan edilmiş; modelimiz kapatabilir |
| ~~3. Stoktan türetilen zaman penceresi~~ | Lieb 2021'de var; katkı olarak çıkarılmalı |

## İddiayı güçlendirecek eklemeler (öneri)

1. **Mekanizma:** sıralamanın neden tersine döndüğünü basit bir ifade + K93 verisiyle göstermek.
2. **Karar rehberi:** hangi karar sorusu için hangi eşitleme kuralı (Enns & Rogers'ta yoktu).
3. **İkinci açık deneyi:** kart sayısı × kapasite × politika × şok faktöriyel + toparlanma süresi.
4. **Yayımlanmış vakanın yeniden kurulması** (SCI-E için): Korytkowski 10 istasyon ya da Bae 2016
   tek araç.
