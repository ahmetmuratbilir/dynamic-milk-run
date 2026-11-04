# Hat besleme / milk-run yazınında tampon eşitleme: iddiayı zayıflatabilecek çalışmalar (2015–2026)

Kapsam notu (04.11.2026): Bu not, şu iddiayı çürütebilecek çalışmaları arar: *"Hat besleme/milk-run yazınında periyodik ve olay tabanlı besleme politikaları tek ve çoğunlukla örtük bir tampon eşitleme noktasında karşılaştırılır, sıralamalar çelişir ve hiçbir çalışma eşitleme kurallarını sistematik olarak karşılaştırmaz ya da üretim kontrolündeki gibi hizmet düzeyi–envanter ödünleşim eğrileri kullanmaz."*
Doğrulama düzeyi her maddede belirtilmiştir: **[TM]** = bu oturumda tam metinden doğrulandı; **[TM-proje]** = projede daha önce tam metinden okunmuş (`docs/literatur_boslugu_analizi.md`), bu oturumda yeniden okunmadı; **[Ö]** = yalnızca özet/meta veri; **[İ]** = ikincil kaynak/arama özeti. Sayfa numarası yalnızca görülen yerlerde verilmiştir.

## S1 — Hat besleme derlemeleri karşılaştırma tabanını veya tampon eşitlemeyi tartışıyor mu?

### Takeaway
Erişilebilen derleme ve sınıflandırma çalışmalarının hiçbirinde (özet düzeyinde) karşılaştırma tabanı ya da tampon eşitleme tartışması bulunamadı. Bu derlemeler politika *türlerini*, amaçları ve çözüm yöntemlerini sınıflandırıyor. ALFP (assembly line feeding problem) çizgisi ise maliyet optimizasyonu yapıyor: envanter her politikanın kendi mantığıyla hesaplanıyor, simülasyonla karşılaştırma yapılmıyor. Tam metinlere erişilemediği için bu bulgu kesin değil, ihtimal düzeyinde.

### Cited Findings
- **Kılıç & Durmuşoğlu (2015), Assembly Automation 35(1)** [Ö]: Derleme, yazını "feeding policy types, objectives, solution methodologies and the application types" eksenlerinde sınıflandırıyor ve açık araştırma alanlarını vurguluyor. Özette karşılaştırma tabanı, tampon eşitleme veya adil karşılaştırmaya dair bir ifade yok. — [OpenAlex kaydı / DOI 10.1108/aa-05-2014-047](https://doi.org/10.1108/aa-05-2014-047)
- **Kundu, Rossini & Portioli-Staudacher (2019), IJIEC** [TM-proje]: s.423'te iki politika ailesini (reorder point = sabit miktar/değişken zaman; periodic review = sabit zaman/değişken miktar) tanımlıyor ve şunu yazıyor: *"does not investigate the differences with the other policy. This could however be the subject of future research."* Aynı sayfada *"The comparison of different feeding policies has been relatively well covered"* diyerek Limère vd. 2012, Golz vd. 2012, Sali vd. 2015, Faccio 2014 ve Caputo & Pelagagge 2011'i sayıyor. Bu çalışmalar besleme *modu* karşılaştırmasıdır (line stocking/kitting/sequencing). s.422: boyutlandırma *"often carried out without adopting a specific technique"*. — [DOI 10.5267/j.ijiec.2018.12.001](https://doi.org/10.5267/j.ijiec.2018.12.001)
- **Adenipekun, Limère & Schmid (2022), Omega 107** ve **Schmid, Montreuil & Limère (2024), IJPE** [Ö]: ALFP modelleri her parçayı bir besleme politikasına atıyor ve toplam maliyeti (taşıma modu, tesis boyutu dahil) MIP/Benders ayrıştırmasıyla en küçüklüyor. Stokastik duruş ile envanter arasındaki ödünleşimi simülasyonla incelemiyorlar. — [Omega DOI](https://doi.org/10.1016/j.omega.2021.102544); [IJPE DOI](https://doi.org/10.1016/j.ijpe.2024.109354); [Adenipekun vd. 2020 Gent özeti](https://biblio.ugent.be/)
- **Caputo, Pelagagge & Salini (2015), Assembly Automation 35(1):35–46** [Ö/İ]: Sürekli parça beslemede JIT teslimat ile hat yanı depolama (line storage) için analitik planlama modelleri. Kaynaklar (kanban kutusu dahil) her alternatif için **kendi mantığıyla boyutlandırılıyor**, ardından toplam maliyet karşılaştırılıyor. Model deterministik ve tek modelli hat içindir. Caputo & Pelagagge (2011) kanban kutu sayısını "tedarik temin süresi boyunca aç kalmamak" koşuluyla belirliyor. — [Emerald kaydı](https://www.emerald.com/insight/content/doi/10.1108/AA-05-2014-040/full/html); [2011 makalesi](https://unpaywall.org/10.1108%2F02635571111099749)
- **Thürer, Fernandes & Stevenson (2019)**, J. Ind. Prod. Eng. [TM], s.2 (makale el yazması): Yazarlar parça besleme yazınının *"typically assumes the full availability of parts at stock points"* varsayımını eleştiriyor. Bu bir metodolojik eleştiridir ama eşitleme kuralıyla ilgili değildir. — [Lancaster el yazması](https://eprints.lancs.ac.uk/id/eprint/139031/1/Manuscript.pdf)

### Inferences
- Derleme düzeyinde bilinen bir "karşılaştırma tabanı önemlidir" tespiti yok gibi görünüyor. Ancak Kılıç & Durmuşoğlu, Schmid & Limère (2019) ve Hanson/Medbo derlemelerinin tam metinleri okunmadan "hiçbir derleme tartışmıyor" denmemeli. Daha güvenli ifade: *"incelediğimiz derlemelerde rastlanmadı"*.
- ALFP çizgisi, envanteri her politikaya kendi kuralıyla hesapladığı için örtük olarak **politika-tutarlı boyutlandırma** kullanıyor. Hakem bu çizgiyi "politika-tutarlı kural zaten standart" diye gösterebilir. Yanıt: bunlar besleme *modları* arasında, deterministik maliyet modelleridir. Periyodik/olay tabanlı ikmal arasında duruş–envanter karşılaştırması yapmazlar ve kurala duyarlılığı ölçmezler.

### Gaps
- Kılıç & Durmuşoğlu (2015), Schmid & Limère (2019, EJOR sınıflandırması), Hanson & Medbo, Sali/Şahin/Patchong, Faccio vd. (2013/2014) ve Emde & Boysen tam metinleri bu oturumda **okunamadı**. Marmara açık erişim sayfası JS ile yükleniyor ve PDF bağlantısı alınamadı; Springer/Elsevier/Emerald kaynakları 403 döndü. Bu derlemelerden sayfa numaralı alıntı verilemiyor.
- Faccio, Gamberi, Persona, Regattieri & Sgarbossa (2013, J. Manag. Control 24:187–208): kanban sayısının çekici tren çevrim süresine bağlı boyutlandırıldığı biliniyor, ancak tam metin bu oturumda doğrulanamadı.

## S2 — 2018–2026 simülasyon çalışmaları: tamponu politikaya göre ayrı boyutlandıran, her politikayı optimize eden ya da ödünleşim/Pareto eğrisi çizen var mı?

### Takeaway
Doğrudan tehdit oluşturan (birden çok eşitleme kuralını karşılaştıran veya periyodik ile olay tabanlı politikaları duruş–envanter eğrisi üzerinde karşılaştıran) bir çalışma **bulunamadı**. En yakın tehditler üç tanedir:
- Alnahhal & Noche (2015) ve Alnahhal, Ramadan & Noche (2016): eşit hizmet düzeyi tabanı, envanter–duruş ödünleşimi.
- Thürer vd. (2019): eşit toplam stok açıkça "karşılaştırılabilirlik için" seçilmiş, ama konu kitting ile line stocking.
- Bocewicz vd. (2019) ve Alnahhal & Noche (2013): filo–tampon ödünleşim eğrileri, ama tek politika içinde.

TUM'un dinamik milk-run çizgisi (Klenk & Galka 2019; Hormes vd. 2020) hat yanı tamponu hiç modellemiyor ya da yalnızca örtük bırakıyor.

### Cited Findings
**A. Orta düzey tehdit: eşitleme tabanını açıkça kuran ya da ödünleşimi inceleyen çalışmalar**
- **Alnahhal & Noche (2015)** [TM-proje], s.117: talep odaklı, Kanban ve kendi yöntemleri karşılaştırılıyor. *"K values were chosen so that fill rate is greater than or equal to 99%"* → **açık, eşit hizmet düzeyi tabanı**. Ancak tek bir kural kullanılıyor ve kural duyarlılığı incelenmiyor. — (proje notu `docs/literatur_boslugu_analizi.md` §4.1, Kol B tablosu)
- **Alnahhal, Ramadan & Noche (2016)**, *Dynamics in Logistics* (LNL, Springer), "Static Versus Dynamic Control of Material Flow in In-Plant Milk Run System" [Ö/İ]:
  - Karşılaştırılanlar: push, geleneksel kanban, e-kanban ve AEK (RFID tabanlı ayarlanmış e-kanban).
  - Yöntem: analitik denklemler ve simülasyon; envanter maliyeti ile duruş karşılaştırılıyor.
  - Sonuçlar koşullu: kanban yeterli tren kapasitesinde etkili, e-kanban daha düşük envanter veriyor, push düşük değişkenlikte etkili, AEK ağır kapasite kıtlığında en iyi.
  - Kanban sayısının nasıl belirlendiği özetlerde **belirtilmiyor**. Alnahhal (2015) yönteminin devamı olduğu için muhtemelen yine fill rate ≥ %99 kullanılıyor, ama bu **doğrulanmadı**.
  — [DOI 10.1007/978-3-319-23512-7_70](https://doi.org/10.1007/978-3-319-23512-7_70); [ResearchGate kaydı](https://www.researchgate.net/publication/300122222_Static_Versus_Dynamic_Control_of_Material_Flow_in_In-Plant_Milk_Run_System); [Alnahhal tezi (core.ac.uk, 403)](https://core.ac.uk/download/33797136.pdf)
- **Thürer, Fernandes & Stevenson (2019)**, J. Ind. Prod. Eng. [TM], s.8 (el yazması):
  - Line stocking ve "classical" kitting karşılaştırılıyor. Her ikisinde ROP için 2, 3 ve 4 düzeyleri taranıyor; ROQ 12/8/6.
  - Eşitleme tabanı açıkça yazılmış: *"The total amount of stock for each setting is kept equal to 24 units to ensure comparability across settings."* Kitting için: *"the same three different levels for the reorder point and reorder quantity are considered and the total amount of stock is kept equal."* → **açık "eşit toplam stok (eşit WIP)" kuralı + parametre taraması**.
  - Sonuç (s.4.3): *"There is only limited impact of upstream stations in a to-stock system … if the parameters of the reorder point system are set appropriately."*
  - Konu besleme **modu**dur (kitting ve line stocking), periyodik/olay tabanlı ikmal değildir. Taşıma (milk-run) modellenmiyor.
  — [Lancaster el yazması](https://eprints.lancs.ac.uk/id/eprint/139031/1/Manuscript.pdf); [DOI](https://doi.org/10.1080/21681015.2019.1695152)
- **Chee, Chong & Chin (2012)** [TM-proje, 2015 öncesi], s.392–393: push ile milk-run Kanban karşılaştırılıyor. Her iki sisteme de {2,4,6} parametre taraması uygulanıyor ve push lehine bir "mükemmel push" senaryosu kuruluyor → adil karşılaştırma kaygısı var. — (proje notu §4.1.5)
- **Bocewicz vd. (2019)** [TM-proje], s.41–45: filo büyüklüğü K ile tampon kapasitesi S_B arasındaki ödünleşim noktaları hesaplanıyor (*"if fewer trains are used … necessary to increase buffer capacity"*). Bu bir **ödünleşim eğrisidir**, ama **tek periyodik politika** içinde kalıyor ve duruş ölçülmüyor. — [ResearchGate kaydı](https://www.researchgate.net/publication/335977002_Milk-run_routing_and_scheduling_subject_to_a_trade-off_between_vehicle_fleet_size_and_storage_capacity)
- **Alnahhal & Noche (2013), SpringerPlus** [TM, Europe PMC]: deterministik DP ve MIP ile rotalama, çizelgeleme ve yükleme çözülüyor. Tablo 6'da tren kapasitesi K ile maksimum hat yanı envanter (MLSI) değiştirilerek tren sayısı ve amaç değeri raporlanıyor. Alıntı: *"it is not very helpful to get tow trains with high capacities if the maximum line-side inventory cannot be increased"*. Tek politika (sabit periyot) içinde bir duyarlılık analizidir; politika karşılaştırması yok. — [Europe PMC tam metin](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC3766513/fullTextXML); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3766513/)
- **Ciemnoczolowski & Bozer (2013), IJPR 51(2):568–581** [Ö]: kanban sayısı için analitik yaklaşımlar türetiliyor ve duruş tahmin ediliyor. Alıntı: *"the number of Kanban and the physical capacity of the tugger have a bigger impact on workstation starvation than the prescribed cycle time"*. Tek politikadır (periyodik MR). Kanbanın politikanın çevrimine bağlı olduğunu destekler; politika karşılaştırması yok. — [DOI 10.1080/00207543.2012.656331](https://doi.org/10.1080/00207543.2012.656331)

**B. Düşük tehdit: politika karşılaştıran ama tamponu modellemeyen veya sabit tutan çalışmalar**
- **Klenk & Galka (2019), IFAC-PapersOnLine 52(13)** [Ö]: sabit aralıklı milk-run kalkışı ile gerçek zamanlı kalkış belirleyen üç strateji karşılaştırılıyor. Ölçütler *"delivery service levels, order lead times, systems utilization and necessary number of MR trains"*. Özette hat yanı tampon veya kanban boyutlandırmasından söz edilmiyor; hizmet düzeyi zamanında teslim olarak tanımlanmış görünüyor. — [DOI 10.1016/j.ifacol.2019.11.517](https://doi.org/10.1016/j.ifacol.2019.11.517)
- **Hormes, Siala, Lieb & Fottner (2020)**, Logistics Journal: Proceedings [TM]:
  - Statik ve dinamik rotalı MR karşılaştırılıyor. Filo boyutu VDI 5586'ya genetik algoritma eklenerek hesaplanıyor.
  - Sonuç: §4.3, s.6: *"the total distance travelled D per hour is reduced from 6779 to 4505 meters … the fleet size can be reduced from 3 to 2 MR vehicles."*
  - Hat yanı tampon yalnızca GA uygunluk fonksiyonundaki bir ceza terimi olarak geçiyor (§3.2: *"ensures a continuous supply of parts and low line-side inventories"*). Duruş ve envanter ölçülmüyor.
  - Bilgi notu: Hormes adına bir 2025 tezi **bulunamadı**. mediaTUM ve dblp'de yalnızca Keuntje, Hormes & Fottner (2018) ve Fottner vd. (2021) görünüyor.
  — [Logistics Journal PDF](https://proc.logistics-journal.de/article/download/977/953/6956)
- **TUM DFG projesi "Dynamic in-plant milk-run control for volatile transport demand"** (2015–2019) [İ]: hedefi rotaları, kalkış zamanlarını ve kaynakları anlık siparişlere göre belirlemek. Beklenen sonuç, statik planlamaya göre daha az kaynak. — [TUM fml proje sayfası](https://mec.ed.tum.de/en/fml/research/2019/dynamic-in-plant-milkrun-control-for-volatile-transport-demand); [DFG GEPRIS](https://gepris.dfg.de/gepris/projekt/280752532)
- **Staab, Röschinger, Dewitz & Günthner (2015)**, WAMS [TM]: BMW için çekici tren (TT) simülasyonu. Çağrı (call-off) tabanlı tek bir sistem modelleniyor: sıralı çağrılar, talep odaklı otomatik çağrılar ve kanban çağrıları. Her çağrıya bir hedef zaman veriliyor ve *"buffer times planned in advance"* ile tedarik güvencesi ölçülüyor (§5.1). Politika karşılaştırması yok; tampon zaman olarak tanımlanmış. — [WAMS 2015 PDF](http://www.msc-les.org/proceedings/wams/2015/WAMS2015_22.pdf)
- **Sevim & Görkemli Aykut (2025)**, PAJES [Ö]: dinamik talep altında ajan tabanlı milk-run modeli. Ölçütler doluluk, mesafe ve bekleme; öneri *"high number of trains with low train capacity"*. Özette hat yanı envanter veya statik temel karşılaştırma yok. — [DergiPark](https://dergipark.org.tr/tr/pub/pajes/article/1813322); [PDF](https://dergipark.org.tr/tr/download/article-file/5373787)
- **Pekarčíková vd. (2020, 2021, 2022, 2025)**, IJSIMM / Sustainability / MPER [TM-proje kısmen, diğerleri Ö]: mevcut durum ile e-Kanban/milk-run karşılaştırılıyor. KanbanBuffer min 10 / maks 50 / çekme 15 sabit. Eşitleme tartışması yok. — [IJSIMM 2020](https://doi.org/10.2507/ijsimm19-2-513); [IJSIMM 2022](https://doi.org/10.2507/ijsimm21-1-593); [MPER 2025](https://doi.org/10.24425/mper.2025.153929)
- **Korytkowski & Karkoszka (2016), IJAMT** [Ö, kesik]: 10 istasyonlu hatta milk-run operatörü. Bozucular (operasyon süresi ve tedarik çevrimi değişkenliği, gecikmeler) ve yönetim kararları inceleniyor. Politika karşılaştırması yapılıp yapılmadığı özetten anlaşılmıyor. — [DOI 10.1007/s00170-015-7442-2](https://doi.org/10.1007/s00170-015-7442-2)
- **Miqueo, Gracia-Cadarso, Torralba & Gil Vilda (2023)**, Machines 11(1):66 [Ö]: beyaz eşya vaka çalışması. Dört senaryoda model sayısı ve değişkenlik kaynakları değiştiriliyor; *"milkruns can protect…"*. Politika karşılaştırması değil, bozucu analizi. Tam metin 403 verdi. — [MDPI](https://www.mdpi.com/2075-1702/11/1/66)
- **Xia, Zhang, Gao & Yang (2023)**, Sustainability [Ö]: tek çekici trenin rotalama, çizelgeleme ve yüklemesi taşıma ile hat envanteri maliyetini en küçüklemek için yapılıyor. Optimizasyondur, politika karşılaştırması değil. — [DOI 10.3390/su151914567](https://doi.org/10.3390/su151914567)
- **Vojdani & Drechsler (2022)** ve **Bae, Evans & Summers (2016)** [TM-proje]: iddiadaki çelişkili sıralamaların kaynaklarıdır. Her ikisinde de aynı iki kutulu kanban veya aynı akış rafı kullanılıyor → örtük eşit kart. — (proje notu §4.1.3b)

### Inferences
- **"Örtük" sözcüğü kısmen zayıf.** Alnahhal & Noche (2015) eşit hizmet düzeyini (fill rate ≥ %99) *açıkça* kullanıyor. Thürer vd. (2019) eşit toplam stoku *"to ensure comparability"* gerekçesiyle açıkça seçiyor. İddia "çoğunlukla örtük" dediği için hâlâ savunulabilir, ama bu iki çalışma örnek olarak anılmalı. Önerilen ifade: *"Tek bir eşitleme noktası kullanılır; bu nokta bazen açıkça (eşit hizmet düzeyi: Alnahhal & Noche 2015; eşit toplam stok: Thürer vd. 2019), çoğunlukla örtük olarak (aynı kutu/raf: Bae vd. 2016; Vojdani & Drechsler 2022) seçilir."*
- **"Ödünleşim eğrisi kullanılmıyor" iddiası için dikkat.** Bocewicz vd. (2019) ve Alnahhal & Noche (2013) filo–tampon ödünleşimini inceliyor; Alnahhal vd. (2016) envanter maliyetini duruşla tartıyor. Ancak bulgulara göre hiçbiri iki politikayı aynı **duruş–envanter eğrisi** üzerinde karşılaştırmıyor. İddia "politikalar *arası* hizmet–envanter eğrisi" diye daraltılırsa güvenli kalır.
- **TUM dinamik milk-run çizgisi** (Klenk & Galka 2019; Hormes vd. 2020) dinamik kontrolün üstünlüğünü **taşıma ölçütlerinde** (mesafe, filo, zamanında teslim) gösteriyor; hat yanı tamponu ya modellemiyor ya örtük bırakıyor. Bu durum Vojdani & Drechsler (2022) ile aynı örüntüdür ve iddiayı **destekler**: dinamik üstünlük tamponun sabit/örtük olduğu bir tabanda raporlanıyor.
- Thürer vd. (2019) üretim kontrolü topluluğundan gelip parça beslemeye "eşit toplam stok" disiplinini taşıyor. Bu, "karşılaştırma tabanı fikri hat beslemeye hiç girmedi" şeklindeki aşırı bir iddiayı çürütür. "Periyodik ile olay tabanlı ikmal karşılaştırmasında eşitleme kuralları sistematik karşılaştırılmadı" iddiasını ise çürütmez.

### Gaps
- Alnahhal, Ramadan & Noche (2016) tam metni ve Alnahhal tezi (core.ac.uk 403; DuEPublico'da aranmadı) okunamadı. Kanban sayısının politika başına nasıl belirlendiği **doğrulanmadı**. Bu, en olası tehdittir ve tam metin edinilmelidir.
- Klenk & Galka (2019) ve Klenk, Galka & Günthner (2015, IFAC 48(3):1882–1887) tam metinleri (ScienceDirect 403) okunamadı. Tampon varsayımı özetten çıkarıldı.
- Hormes (2025) tezi bulunamadı (mediaTUM aramasında yok). Görevde verilen başlık doğrulanamadı.
- Semantic Scholar API hız sınırına takıldı; OpenAlex sorgularının bir kısmı 429 döndü. Arama kapsamı bu nedenle tam değil. Özellikle IJPR/IJPE/C&IE'de 2020–2026 arası "e-kanban vs milk-run" simülasyonları (ör. Bo Zhou'nun gerçek zamanlı malzeme dağıtım çalışmaları, Kousi vd. mobil robot besleme) taranamadı.

## S3 — Politika karşılaştırma sonuçlarının eşitleme/karşılaştırma tabanına bağlı olduğunu açıkça söyleyen bir hat besleme çalışması var mı?

### Takeaway
Hat besleme/milk-run yazınında bu ilkeyi **açıkça** ifade eden bir çalışma bulunamadı. En yakın ifadeler üç tanedir:
- Thürer vd. (2019): eşit stok "karşılaştırılabilirlik için", ancak tabanın sonucu değiştirdiği gösterilmiyor.
- Chee vd. (2012): mükemmel push senaryosu.
- Kundu vd. (2019): iki politika ailesinin farkı gelecek çalışma olarak öneriliyor.

İlke üretim kontrolü yazınında yerleşiktir (Bonvik vd. 1997; Geraghty & Heavey 2005; Framinan vd. 2003).

### Cited Findings
- Thürer vd. (2019), s.8: eşit stok *"to ensure comparability across settings"*. Taban gerekçelendiriliyor, ancak farklı tabanlarla sonucun değişip değişmediği test edilmiyor. — [el yazması](https://eprints.lancs.ac.uk/id/eprint/139031/1/Manuscript.pdf)
- Kundu vd. (2019), s.423: periyodik ile reorder-point politikaları arasındaki fark *"could however be the subject of future research"* → tabana duyarlılık değil, karşılaştırmanın kendisi eksik ilan ediliyor. — [DOI](https://doi.org/10.5267/j.ijiec.2018.12.001)
- Thürer vd. (2019), §4.3: *"if the parameters of the reorder point system are set appropriately"* farkın sınırlı kaldığı yazılıyor. Sonucun parametre ayarına bağlı olduğu dolaylı olarak kabul ediliyor. — [el yazması](https://eprints.lancs.ac.uk/id/eprint/139031/1/Manuscript.pdf)
- Ciemnoczolowski & Bozer (2013): duruşu belirleyen etkenin çevrim süresinden çok kanban sayısı ve tren kapasitesi olduğu. Bu, karşılaştırmalarda tampon seçiminin sonucu domine edebileceğine dair dolaylı bir dayanaktır. — [DOI](https://doi.org/10.1080/00207543.2012.656331)

### Inferences
- İddianın çekirdeği şu haliyle bu taramadan sağ çıkıyor: *periyodik ile olay tabanlı hat besleme karşılaştırmalarında birden çok eşitleme kuralını yan yana koyan ve politikalar arası duruş–envanter eğrisi raporlayan çalışma yok.*
- Revizyon önerileri:
  1. "Örtük" yerine "tek ve çoğunlukla örtük; açık olduğunda da tek kural" denmeli. Alnahhal & Noche 2015 ve Thürer vd. 2019 örnek olarak verilmeli.
  2. "Ödünleşim eğrisi yok" iddiası "politikalar arası" ile sınırlanmalı. Bocewicz vd. 2019 ve Alnahhal & Noche 2013 tek politika içi ödünleşim örneği olarak anılmalı.
  3. ALFP maliyet modellerinin (Caputo vd. 2015; Adenipekun vd. 2022) politika-tutarlı envanter hesabını örtük biçimde kullandığı not edilmeli.

### Gaps
- Kesin bir "yok" iddiası için şu tam metinler okunmalı: Alnahhal vd. (2016), Klenk & Galka (2019), Klenk vd. (2015), Faccio vd. (2013) ve Kılıç & Durmuşoğlu (2015).
- Almanca yazın (Routenzug "getaktet" ile "bedarfsorientiert" karşılaştırmaları, ör. Logistics Journal, ZWF, Productivity) bu oturumda yalnızca yüzeysel tarandı. Galka/Klenk/Lieb ekibinin Almanca tezlerinde (mediaTUM) tampon boyutlandırma varsayımları ayrıca kontrol edilmeli.
