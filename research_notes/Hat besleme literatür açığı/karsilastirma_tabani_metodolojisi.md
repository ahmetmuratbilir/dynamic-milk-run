# Karşılaştırma tabanı metodolojisi: eşitleme kuralı hangi politikanın "kazandığını" değiştirir mi? (YA / üretim kontrolü / lojistik simülasyonu emsalleri)

> Hazırlanma: 04.11.2026. Atıf sayıları **OpenAlex** (`cited_by_count`, 04.11.2026'da sorgulandı); Google Scholar sayıları genellikle daha yüksektir, GS ayrıca alınamadı.
> İşaretler: **[DOĞRULANDI-TAM METİN]** = tam metin bu oturumda okundu; **[PROJE NOTU]** = kullanıcı tam metni daha önce okudu (docs/literatur_boslugu_analizi.md); **[İKİNCİL]** = yalnızca özet, katalog veya atıf yapan kaynaktan; **[ÇIKARIM]** = benim yorumum.

## S1. Üretim kontrolü: adil karşılaştırma hakkında tam olarak ne diyorlar?

### Takeaway
Eşitleme tabanı (eşit WIP, eşit çıktı veya eşit hizmet düzeyi; hangi parametre eniyilenmiş; push için hangi bırakma süreci) CONWIP/kanban/push sıralamasını değiştirebilir ve bu, üretim kontrolü yazınında en az 1995'ten beri açıkça biliniyor. Fakat bu bilgi çoğunlukla bir **tasarım ilkesi** olarak (her politikayı kendi en iyi ayarıyla, eşit hizmet düzeyinde veya ödünleşim eğrisi üzerinde karşılaştır) ya da **çelişkili bulguların açıklaması** olarak yer alır. Ana katkısı "sonuç karşılaştırma tasarımına bağlıdır" olan tek doğrudan emsal Enns & Rogers (2008, WSC) ve etkisi düşük kalmış (16 atıf).

### Cited Findings

**Enns & Rogers (2008), WSC: en doğrudan emsal** [DOĞRULANDI-TAM METİN]
- Künye düzeltmesi: makale **iki yazarlıdır**: S. T. Enns ve Paul Rogers, "Clarifying CONWIP versus push system behavior using simulation," *Proc. 2008 Winter Simulation Conference*, s. 1867–1872 (PDF sayfa numaraları 1867'den 1872'ye), DOI 10.1109/WSC.2008.4736277. Projedeki referans [43] yalnızca "S. T. Enns" yazıyor ve sayfa vermiyor; düzeltilmeli. — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf); DOI ve atıf: [OpenAlex](https://api.openalex.org/works?search=Clarifying%20CONWIP%20versus%20push%20system%20behavior)
- Özet: "Tradeoff curves based on inflating the inventory level for the CONWIP system and the arrival rate for the 'push' system are generated … Results show that, contrary to what some previous studies have indicated, CONWIP efficiency is not inherently superior to 'push' system efficiency. Instead, the release mechanism used for the 'push' system has a significant impact on which system will perform better." (s. 1867) — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)
- Giriş: "One of the problems in comparing the performance of a CONWIP system with any other system is the lack of a unified framework for comparison (Framinan et al. 2003). This leads to results that are difficult to generalize and may even be contradictory." Örnek olarak Gstettner & Kuhn (1996)'nın ters sonucu verilir (s. 1867). — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)
- Hedef alınan iddia: "Hopp and Spearman (2000) concluded that CONWIP will dominate a 'push' workload control system in a simple flowline. More specifically … a CONWIP system will yield more throughput for a given average inventory level." (s. 1867). Hopp & Spearman'ın sayısal örneği: aynı çıktıda (λ=0,6) CONWIP için L=6, Poisson girişli push için L=7,5 (s. 1868–1869). — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)
- Tersine dönme: push'ta Poisson giriş yerine sabit aralıklı bırakma kullanıldığında, *aynı çıktıda* push L=5,675 (GA 5,644–5,707) verir, yani CONWIP'in L=6'sından daha az. "It is therefore clear that CONWIP systems do not always dominate in terms of throughput versus inventory performance efficiency." (s. 1869–1870). Gerekçe: "assuming a 'push' system with constant interarrival times for comparison with a CONWIP system is more fair." (s. 1869) — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)
- Sonuç bölümü: "Preliminary results indicate that comparison is not straightforward and that it may not be possible to conclude that either system dominates, as has been suggested in some previous research." (s. 1872). Sonuçlar çıktı–envanter ödünleşim eğrileri olarak sunulur (Şekil 2–5). — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)
- Etki: OpenAlex'te **16 atıf**. — [OpenAlex](https://api.openalex.org/works?search=Clarifying%20CONWIP%20versus%20push%20system%20behavior)

**Hopp & Spearman, *Factory Physics*: eşit çıktıda envanter karşılaştırması**
- Yukarıda aktarıldığı gibi, Hopp & Spearman CONWIP ile push'u **aynı çıktıda ortalama WIP** üzerinden karşılaştırır ve CONWIP'in baskın olduğunu söyler. Bu, Enns & Rogers'ın aktarımından doğrulandı; kitabın kendisini ve sayfa numarasını görmedim. — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)

**Bonvik, Couch & Gershwin (1997), IJPR 35(3):789–804** [PROJE NOTU]
- Beş politika (kanban, minimal blocking, base stock, CONWIP, hibrit) "the tradeoff between service level and inventory" eğrisinde karşılaştırılır (Şekil 5, s.797). Ardından "Find a configuration that gives a 99.9% service level using the least possible total inventory" (s.797), yani her politika kendi en iyi ayarıyla ve eşit hizmet düzeyinde karşılaştırılır (Tablo 2, s.798). — proje notu: `docs/literatur_boslugu_analizi.md` §4.1.3c
- Etki: OpenAlex'te **249 atıf** ve bu küme içinde en çok atıf alan karşılaştırma makalesi. Katkısını bir metodoloji makalesi olarak değil, "hangi mekanizma daha iyi" sorusunun yanıtı olarak çerçeveler; adil karşılaştırma onda tasarımın bir parçasıdır. — [OpenAlex](https://api.openalex.org/works/doi:10.1080/002075497195713)

**Geraghty & Heavey (2005), OR Spectrum 27:435–457** [PROJE NOTU]
- Kontrol parametreleri kısmi sayımla taranır ve her strateji için "minimum WIP required by each PCS to achieve a targeted Service Level" karşılaştırılır (§5, s.448–454; Tablo 4, s.453). Ölçüt "Service Level vs. WIP trade-off"tur. — proje notu: `docs/literatur_boslugu_analizi.md` §4.1.3c
- Etki: OpenAlex'te **44 atıf**. — [OpenAlex](https://api.openalex.org/works/doi:10.1007/s00291-005-0204-z)

**Framinan, González & Ruiz-Usano (2003), *Production Planning & Control* 14(3):255–265** [İKİNCİL]
- Künye: PPC 14(3), s. 255–265, DOI 10.1080/0953728031000102595. CONWIP yazınını işleyiş, uygulama ve diğer sistemlerle karşılaştırma başlıkları altında derler. — [Bohrium kaydı](https://www.bohrium.com/paper-details/the-conwip-production-control-system-review-and-research-issues/812352579802497026-6150); [Taylor & Francis DOI](https://informahealthcare.com/doi/full/10.1080/0953728031000102595)
- Enns & Rogers derlemenin "lack of a unified framework for comparison" tespitini aktarır [DOĞRULANDI: Enns & Rogers metninde]. — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)
- Arama özetine göre derleme şunu da söyler: "Most of the comparisons of Conwip with other production control systems suffer the lack of a unified framework for comparison where each system is tested under optimal parameter setting". Bu cümleyi derlemenin kendi metninde görmedim; kelimesi kelimesine atıf yapmadan önce tam metinden kontrol edilmeli. — [Bohrium kaydı](https://www.bohrium.com/paper-details/the-conwip-production-control-system-review-and-research-issues/812352579802497026-6150)
- Atıf yapan kaynaklara göre derleme, base stock ile CONWIP hakkında çelişen bulguları not edip açıklığa kavuşturulmasını önerir [İKİNCİL]. — [Tsukuba tartışma metni](https://infoshako.sk.tsukuba.ac.jp/~databank/pdf/1202.pdf)
- Etki: OpenAlex'te **159 atıf**. — [OpenAlex](https://api.openalex.org/works/doi:10.1080/0953728031000102595)

**Gstettner & Kuhn (1996), IJPR 34(11):3253–3273 (bazı kaynaklarda 3274): "ters sonuç"** [İKİNCİL]
- IAOR özeti: belirli bir üretim hızında ortalama WIP kanban'da CONWIP'e göre daha düşüktür; optimum kart dağılımları "WIP bowl phenomenon" ortaya çıkarır. — [IAOR](https://iaorifors.com/paper/18888)
- Atıf yapan kaynaklar bunu "opposite conclusion" olarak sunar. Kanban istasyonlar arasında kart dağılımı **eniyilendiğinde** CONWIP'i yener; yani sonuç parametre eniyileme tasarımına bağlıdır. — [Tsukuba tartışma metni](https://infoshako.sk.tsukuba.ac.jp/~databank/pdf/1202.pdf)
- Etki: OpenAlex'te **151 atıf**. — [OpenAlex](https://api.openalex.org/works/doi:10.1080/00207549608905087)

**Muckstadt & Tayur (1995), IIE Transactions 27, Kısım I (s.140–150) ve Kısım II (s.151–161)** [İKİNCİL]
- Kısım I: CONWIP ve geleneksel kanban, uygulanabilir çekme kontrollerinden oluşan sonlu bir ailenin iki ucudur. — [Scilit, Kısım I](https://www.scilit.net/publications/f5a2b4b6dfb03b9c22886394c6fe159f)
- Kısım II: politikalar, sağlanması gereken bir **ortalama çıktı hedefi** altında **üç farklı amaçla** karşılaştırılır: en yüksek envanteri, ortalama envanteri veya çıktı varyansını en küçüklemek. Bu, eşitleme koşulunun ve amaç ölçütünün açıkça birer tasarım değişkeni yapıldığı erken bir örnektir. Bulguların amaca göre değiştiğini tam metinden doğrulamadım. — [Scilit, Kısım II](https://www.scilit.net/publications/62dfcdfe4f8a05ee0f25ae5bf507c08e)
- Etki: OpenAlex'te Kısım I için **82**, Kısım II için **44 atıf**. — [OpenAlex I](https://api.openalex.org/works/doi:10.1080/07408179508936726); [OpenAlex II](https://api.openalex.org/works/doi:10.1080/07408179508936727)

**Diğer "aynı çıktıda WIP" karşılaştırmaları** [İKİNCİL]
- Khojasteh-Ghamari (2009, J. Intelligent Manufacturing): kanban ile CONWIP'i aynı çıktıda ortalama WIP üzerinden karşılaştırır. Arama özetine göre önceki analitik çalışmalar, CONWIP'in seri hatta kanban'ı yalnızca "toplam kart sayısı uygun ayarlandığında" geçtiğini bildirmiştir. — [Springer kaydı](https://springerlink.bibliotecabuap.elogim.com/doi/10.1007/s10845-008-0174-5)
- Ang (2015, IJPME): base stock, geleneksel kanban ve genişletilmiş kanbanı karşılaştırır. Arama özetine göre tez sürümünde karşılaştırmadan önce S\* ve K\* eniyilenir. — [IJPME](https://polipapers.upv.es/index.php/IJPME/article/view/3038)

**Thürer vd. / Lödding: iş yükü kontrolü (WLC)**
- Thürer, Fernandes, Lödding & Stevenson (2024), "Material Flow Control in Make-to-Stock Production Systems…": yeniden sipariş noktası, iş yükü normları ve POLCA kart düzeyleri birkaç düzeyde taranır. Emniyet faktörü düzeyleri "to realize a fill rate that can be considered good while still maintaining performance differences" amacıyla seçilmiştir. Taradığım metinde açık bir "adil karşılaştırma" tartışması bulamadım. [DOĞRULANDI-TAM METİN, kabul edilmiş el yazması] — [Lancaster ePrints](https://eprints.lancs.ac.uk/213129/5/PURE_FSMJ_Thurer-et-al_2024.pdf)
- Lödding, *Handbook of Manufacturing Control*: "Fundamentals of Order Release" bölümü, bırakmanın WIP'i, WIP'e bağlı kullanım oranını ve geçiş süresini etkilediğini söyler (Nyhuis–Wiendahl lojistik işletim eğrileri geleneği). Karşılaştırma tabanı üzerine bir ifade bulamadım. — [Springer bölümü](https://link.springer.com/chapter/10.1007/978-3-642-24458-2_16)

### Inferences
- [ÇIKARIM] Yazında **dört ayrı eşitleme ekseni** zaten var: (i) eşit çıktıda WIP (Hopp & Spearman; Gstettner & Kuhn; Khojasteh-Ghamari), (ii) eşit hizmet düzeyinde envanter (Bonvik vd.; Geraghty & Heavey), (iii) her politika kendi eniyilenmiş parametresiyle (Gstettner & Kuhn kart dağılımı; Bonvik; Ang), (iv) push için bırakma süreci seçimi (Enns & Rogers). Tezdeki "eşit kart / politika-tutarlı boyutlandırma / eşit hizmet / eşit WIP" dörtlüsü bunlarla birebir örtüşüyor. Bu yüzden ilkenin kendisi yeni değil.
- [ÇIKARIM] Enns & Rogers tezin en yakın akrabasıdır: bir ders kitabının baskınlık iddiası, karşılaştırma tasarımındaki tek bir varsayım değiştirilince tersine dönüyor ve sonuç ödünleşim eğrileriyle raporlanıyor. Düşük etkisinin (16 atıf, WSC) muhtemel nedenleri: konferans bildirisi olması, tek ve basit bir hat incelemesi ve "preliminary" çerçevesi. Ders: "sonuç tabana bağlıdır" mesajı tek başına zayıf karşılanıyor. Hangi koşulda hangi politikanın neden kazandığına dair mekanizma açıklaması eklenmeli.
- [ÇIKARIM] En çok atıf alanlar (Bonvik 249, Framinan 159, Gstettner & Kuhn 151) adil karşılaştırmayı **araç** olarak kullanıp **içerik sonucu** (hangisi, ne zaman) veren çalışmalardır. Tez de katkısını "metodoloji uyarısı + alan içi içerik sonucu (statik/dinamik milk-run ne zaman kazanır)" ikilisi olarak sunmalı.

### Gaps
- Framinan vd. (2003) tam metni okunmadı. "optimal parameter setting" cümlesi ikincil kaynaktan; sayfa numarası yok.
- Gstettner & Kuhn (1996) ve Muckstadt & Tayur (1995) tam metinleri okunmadı. Kesin eşitleme kuralları ve Muckstadt & Tayur'da amaçlara göre sıralamanın değişip değişmediği doğrulanamadı.
- **"Amos vd."** (projede "aktaran MDPI Processes 2022, 10(1):5" olarak geçiyor) **doğrulanamadı**: MDPI sayfası 403 döndü ve hedefli aramada Amos adlı yazarın kanban/CONWIP karşılaştırma çalışması çıkmadı. Atıf zinciri tam metinden kontrol edilmeden makalede kullanılmamalı; olası bir yanlış atıf.
- Gaury & Kleijnen (ve Gaury, Pierreval & Kleijnen) çekme sistemi özelleştirme ve sağlamlık çalışmaları bu oturumda aranmadı.
- *Factory Physics*'in kendi "adil karşılaştırma" ifadesi ve sayfası görülmedi (yalnızca Enns & Rogers aktarımı var).
- Thürer/Land WLC yazınında sonuçların norm düzeyleri boyunca "performans eğrisi" olarak sunulması [ÇIKARIM, bilgi birikimime dayalı] bu oturumda kaynakla doğrulanmadı.

## S2. Envanter/yenileme: periyodik ve sürekli gözden geçirme karşılaştırmalarında "eşit hizmet düzeyi" geleneği var mı?

### Takeaway
Envanter yazınında politikalar standart olarak ya **toplam maliyet** üzerinden (her politika kendi en iyi parametreleriyle) ya da **sabit hedef hizmet düzeyinde (dolum oranı) gereken güvenlik stoğu ve envanter** üzerinden karşılaştırılır. Bu, eşit hizmet tabanının yerleşik bir gelenek olduğunu gösterir. Ancak bu oturumda bunu açık bir "adil karşılaştırma" kuralı olarak yazan birincil ders kitabı pasajını doğrulayamadım.

### Cited Findings
- Rao (2003), "Properties of the Periodic Review (R, T) Inventory Control Policy for Stationary, Stochastic Demand," *MSOM* 5(1). (R,T) politikasını sürekli gözden geçirmeli (Q,r) ile **maliyet** üzerinden karşılaştırır. Sürekli talepte (R,T) kullanmanın en kötü durumda maliyeti en fazla %41,42 artırdığını ve koordinasyon gerektiğinde (R,T)'nin tercih edilebileceğini gösterir. — [Scilit](https://www.scilit.net/publications/21be653d83c339bd40bdb47cc73f5ed3); [EconBiz](https://www.econbiz.de/Record/properties-of-the-periodic-review-r-t-inventory-control-policy-for-stationary-stochastic-demand-rao-uday/10006027642)
- Rao (2003) OpenAlex'te **119 atıf**. — [OpenAlex](https://api.openalex.org/works/doi:10.1287/msom.5.1.37.12761)
- MIT ders notlarına (Graves) göre gözden geçirme sıklığı değiştiğinde "to ensure the same fill rate" daha fazla güvenlik stoğu gerekir. Bu, politika ve parametre karşılaştırmasının eşit dolum oranında yapıldığını gösteren ders düzeyinde bir kanıt. — [MIT 15.762J notları](https://dspace.mit.edu/bitstream/handle/1721.1/71720/15-762j-spring-2005/contents/lecture-notes/inventory_notes.pdf)
- Thürer vd. (2024) üretim kontrolünde de yeniden sipariş noktası emniyet faktörünü bir dolum oranı düzeyine göre seçer (bkz. S1). — [Lancaster ePrints](https://eprints.lancs.ac.uk/213129/5/PURE_FSMJ_Thurer-et-al_2024.pdf)

### Inferences
- [ÇIKARIM] Envanter teorisinde (R,S) ile (s,Q) karşılaştırması **tanım gereği** ya maliyet eniyilemesi ya da hizmet kısıtlı envanter en küçüklemesi olarak kurulur: her politika kendi formülüyle boyutlandırılır. Tezdeki "politika-tutarlı boyutlandırma" (her politikanın tamponu kendi çevrim süresinden türetilir) bunun hat besleme karşılığıdır. Statik milk-run periyodik gözden geçirmeye (R,S), dinamik/kanban tetiklemeli besleme ise sürekli gözden geçirmeye (s,Q) karşılık geldiği için bu analoji makalede açıkça kurulabilir.
- [ÇIKARIM] "Eşit kart sayısı" tabanı envanter teorisi açısından kusurludur: aynı tampon, gözden geçirme aralığı R olan bir politikada R+L süresini, sürekli gözden geçirmede ise yalnızca L süresini korur. Bu, kalıcı bir sistematik yanlılık üretir.

### Gaps
- Silver, Pyke & Thomas (2017) ve Axsäter (*Inventory Control*) ders kitaplarında "karşılaştırma eşit hizmette yapılmalı" türü açık bir ifade ve sayfa numarası doğrulanamadı.
- (R,S) ile (s,Q)'nun **eşit dolum oranında** sayısal karşılaştırmasını açık bir yöntem tercihi olarak raporlayan birincil makale bulunamadı.

## S3. Genel simülasyon/YA metodolojisi: kıyaslama tuzakları üzerine makaleler ve nasıl karşılandıkları

### Takeaway
Sezgisel algoritma deneyleri üzerine 1995 tarihli iki *Journal of Heuristics* makalesi (Hooker; Barr vd.) ve 2001 tarihli Rardin & Uzsoy rehberi yüksek atıf alan metodoloji katkılarıdır. Hooker'ın ilkeleri derginin editoryal politikası haline gelmiştir. Simülasyon tarafında STRESS (Monks vd. 2019) raporlama standardıdır. Hooker'ın "parametre ayarını tek noktada sabitleme, deneysel faktör yap" önerisi, tezin "tek noktalı karşılaştırma yerine ödünleşim eğrisi raporla" önerisinin doğrudan metodolojik dayanağıdır.

### Cited Findings
- **Hooker (1995)**, "Testing heuristics: We have it all wrong," *J. Heuristics* 1:33–42 [DOĞRULANDI-TAM METİN, ön baskı]. "The most obvious difficulty of competitive testing is making the competition fair … More difficult to defeat are differences in coding skill, tuning and effort invested." Ayar konusu: "How much adjustment is legitimate? Should one also adjust the competing code? … the question of how much tuning is legitimate recurs, with no answer in sight." — [Hooker ön baskı PDF](https://www.cs.ubc.ca/~hutter/EARG.shtml/earg/papers08/testing-heuristics.pdf)
- Hooker'ın çözümü (tez için kilit pasaj): "The issue of how much to tune an algorithm becomes moot, because the parameter settings are among the factors one would investigate experimentally. That is, rather than agonize over what are the best parameter settings, one runs controlled experiments in which many different parameter settings are used, precisely in order to understand their effect on performance. … In short, the problem of fair comparison becomes a nonproblem." — [Hooker ön baskı PDF](https://www.cs.ubc.ca/~hutter/EARG.shtml/earg/papers08/testing-heuristics.pdf)
- Karşılanma: OpenAlex'te **440 atıf**. *Journal of Heuristics* politikası, yeni yöntemleri yalnızca "scientifically tested by following the principles outlined by Hooker (1995)" ise değerlendirdiğini belirtir. — [OpenAlex](https://api.openalex.org/works/doi:10.1007/BF02430364); [J. Heuristics politika sayfası](https://www.springer.com/journal/10732/updates/17199246)
- **Barr, Golden, Kelly, Resende & Stewart (1995)**, "Designing and reporting on computational experiments with heuristic methods," *J. Heuristics* 1(1):9–32, DOI 10.1007/BF02430363. Sezgisel yöntem deneylerinin tasarımı ve raporlanması için yönergeler sunar. OpenAlex'te **452 atıf**. Tam metni okumadım. — [Springer](https://link.springer.com/doi/10.1007/BF02430363); [OpenAlex](https://api.openalex.org/works/doi:10.1007/BF02430363)
- **Rardin & Uzsoy (2001)**, "Experimental Evaluation of Heuristic Optimization Algorithms: A Tutorial," *J. Heuristics*. OpenAlex'te **333 atıf**. Hooker'ı deneysel değerlendirme kaynakları arasında anar. — [Rardin & Uzsoy PDF](https://www.dca.fee.unicamp.br/~gomide/courses/EA044/Artigos/ExperimentalEvaluationHeuristicOptimizationAlgorithmsRardin2001.pdf); [OpenAlex](https://api.openalex.org/works/doi:10.1023/A:1011319115230)
- Csébfalvi & Csébfalvi (2012), "Fair Comparison of Population-based Heuristic Approaches – The Evils of Competitive Testing" (SciTePress): Hooker'a dönüp stokastik yöntemlerde yaygın "one problem – one result" sunumunun adil karşılaştırmadan son derece uzak olduğunu savunur [İKİNCİL]. — [SciTePress](https://www.scitepress.org/papers/2012/41684)
- **Monks vd. (2019)**, "Strengthening the reporting of empirical simulation studies: Introducing the STRESS guidelines," *J. Simulation* 13(1):55–67, DOI 10.1080/17477778.2018.1442155. DES, ABS ve SD için 20 maddelik kontrol listeleri sunar. Motivasyonu, eksik raporlama nedeniyle simülasyon çalışmalarının yeniden üretilememesidir. OpenAlex'te **250 atıf**. — [RePEc](https://econpapers.repec.org/RePEc:taf:tjsmxx:v:13:y:2019:i:1:p:55-67); [OpenAlex](https://api.openalex.org/works/doi:10.1080/17477778.2018.1442155)
- Johnson (2002), "A theoretician's guide to the experimental analysis of algorithms" (*Data Structures, Near Neighbor Searches, and Methodology* içinde; 1996 taslağının genişletilmiş hali): ekinde "Pitfalls" ve "Pet Peeves" listeleri vardır. Karşılaştırmaya ilişkin maddeleri tam metinden okuyamadım. — [Resende, DSJ anısına sunum](https://www.mauricio.resende.info/talks/tribute-to-DSJ.pdf)

### Inferences
- [ÇIKARIM] Bu metodoloji makaleleri yöntem odaklı dergilerde (J. Heuristics, J. Simulation) yayımlanıp yüksek atıf almış. Ancak bunlar genel rehberdir ve bir uygulama alanında "sonuç tersine döner" gösterimi içermez. Tezin katkısı türü olarak bunlarla değil, Enns & Rogers ile aynı sınıftadır: uygulama alanına özgü, sayısal bir duyarlılık gösterimi.
- [ÇIKARIM] Hooker'ın "parametre ayarı deneysel faktördür" ilkesi tezde doğrudan alıntılanabilir: tampon/kart sayısı tek bir eşitleme noktasında sabitlenmez, taranır ve sonuç duruş–WIP eğrisi olarak raporlanır. STRESS ise "eşitleme kuralının açıkça raporlanması" önerisini bir raporlama maddesine bağlamak için kullanılabilir (STRESS'in ilgili maddesini kontrol listesinden doğrulamak gerekir).

### Gaps
- Law & Kelton (*Simulation Modeling and Analysis*) içindeki alternatif karşılaştırma bölümü bu oturumda görülmedi. Bilinen içerik ortak rastgele sayılar ve eşli t testidir; eşitleme tabanını ele aldığını doğrulayamadım.
- Barr vd. (1995) ve Johnson (2002) içinde ayar eşitliği ve adil karşılaştırma maddelerinin tam ifadeleri doğrulanamadı.
- STRESS-DES kontrol listesinde "karşılaştırılan senaryoların parametrelendirmesi" maddesinin tam ifadesi görülmedi.
- Araç rotalama ve sevkiyat kıyaslamasında "fair comparison" yazını (ör. dinamik rotalama benchmark tartışmaları) bu oturumda aranmadı.

## S4. Ana katkısı "sonuçlar farklı karşılaştırma tabanlarında tersine döner" olan lojistik/malzeme taşıma makalesi var mı?

### Takeaway
Bulduğum en yakın örnek üretim kontrolünden: **Enns & Rogers (2008)**. Ana mesajı tam olarak budur: bir ders kitabı iddiası bırakma süreci değiştirilince tersine dönüyor ve sonuç ödünleşim eğrisiyle gösteriliyor. Fabrika içi lojistik/milk-run/hat besleme alanında ana katkısı bu olan bir makale **bulamadım**. Alandaki karşılaştırmalar sıralamanın koşullara (talep değişkenliği, tren kapasitesi) bağlı olduğunu raporluyor, eşitleme kuralına bağlı olduğunu değil.

### Cited Findings
- Fabrika içi milk-run ile push, klasik kanban ve e-kanbanı karşılaştıran bir çalışmanın (core.ac.uk 33797136; yazar ve künye bu oturumda doğrulanmadı) arama özetine göre: tüketim değişkenliği yüksek değilse push etkilidir, tren kapasitesi yeterliyse klasik kanban etkilidir, e-kanban ise daha düşük envanter verir. Sıralama koşula bağlıdır, ama eşitleme tabanı bir değişken olarak ele alınmamıştır [İKİNCİL]. — [CORE PDF](https://core.ac.uk/download/33797136.pdf)
- Aynı arama özetine göre geleneksel kanban tasarımında kart sayısı, hat yanı ortalama envanter ile yok olma olasılığı arasındaki ödünleşimden belirlenir [İKİNCİL]. — [CORE PDF](https://core.ac.uk/download/33797136.pdf)
- Enns & Rogers (2008): ayrıntılar S1'de. — [WSC08 PDF](https://www.informs-sim.org/wsc08papers/230.pdf)

### Inferences
- [ÇIKARIM] Bu boşluk, projede zaten yazılı olan konumlandırmayı (literatur_boslugu_analizi.md §4.1.3c) destekliyor: ilke üretim kontrolünde biliniyor ama fabrika içi hat besleme ve milk-run yazınına taşınmamış. Katkı "ilkeyi icat etmek" değil; ilkeyi alana taşımak, dört somut kuralı aynı sistemde sayısal olarak karşılaştırmak ve alandaki çelişkili bulguları (Bae vd. 2016; Vojdani & Drechsler 2022) bununla açıklamaktır.
- [ÇIKARIM] Önerilen çerçeve cümlesi: "Üretim kontrolü yazınında karşılaştırma sonucunun eşitleme kuralına ve parametre ayarına bağlı olduğu bilinmektedir (Gstettner & Kuhn 1996; Bonvik vd. 1997; Framinan vd. 2003; Geraghty & Heavey 2005; Enns & Rogers 2008). Algoritma deneyleri yazınında ise parametre ayarının tek noktada sabitlenmesi yerine deneysel faktör olarak taranması önerilmektedir (Hooker 1995). Bu çalışma, aynı ilkenin fabrika içi hat besleme politikalarının karşılaştırılmasında da geçerli olduğunu ve ihmal edildiğinde sonucun yönünü değiştirdiğini göstermektedir."
- [ÇIKARIM] Karşılanma riski: Enns & Rogers örneği, salt "it depends" mesajının düşük etki aldığını gösteriyor (16 atıf). Ret ve düşük etki riskini azaltmak için tez (a) hangi tabanın hangi karar sorusuna uygun olduğunu söyleyen bir **öneri** (ör. "hizmet hedefi verilmişse eşit hizmet; tasarım aşamasındaysa eğri") ve (b) tersine dönmenin **mekanizmasını** (periyodik ve sürekli tetiklemede korunan süre farkı, R+L'ye karşı L) sunmalı.

### Gaps
- Fabrika içi lojistik, AGV/tugger, sevkiyat veya araç rotalama alanında ana katkısı karşılaştırma tabanı duyarlılığı olan bir makale bulunamadı. Bu, aramanın sınırlı olmasından da kaynaklanabilir (yaklaşık 15 sorgu); "yok" iddiası makalede "bulabildiğimiz kadarıyla" kaydıyla kullanılmalı.
- core.ac.uk 33797136 çalışmasının yazarı, yılı ve dergisi doğrulanmadı.
- Google Scholar atıf sayıları alınamadı; yukarıdaki tüm sayılar OpenAlex'ten ve muhtemelen GS'den düşük.
