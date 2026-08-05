# Yeni Makale Çapraz Analiz (K01-K36 Kararları ile)

Yapılan literatür taraması sonucunda okunan 12 yeni makale, projemizin mevcut karar günlüğündeki (K01-K36) parametreler ve mimari tercihler ile karşılaştırılmış ve aşağıdaki 5 ana başlık altında analiz edilmiştir.

## 1. ÇELİŞEN VERİLER (Mevcut K01-K36 kararlarıyla çelişen)

- **Sabit Kapasite Yaklaşımı (K36):** Karar günlüğümüzde kapasite probleminin bir darboğaz olmadığı ve sistemin daha çok filo/zaman kısıtlı olduğu kabul edilmiştir. Ancak **Zidanne (2025)** tarafından yapılan VRPTW analizinde ceza (penalty) maliyetleri ile kapasite optimizasyonunun doğrudan ilişkili olduğu ve kapasite ihlallerinin zaman pencerelerinde katı gecikmelere sebep olabileceği belirtilmiştir (Satır: 111-125). Bu durum, araç kapasitelerinin tamamen göz ardı edilmemesi gerektiğini göstermektedir.
- **Emniyet Stoku ve Talep Değişkenliği (K08/K25):** Projede emniyet stoku sadece bir güvenlik tamponu (Alpha = 0.15 vb.) olarak ele alınmış olup, istatistiksel değişkenlik modeline (z-value vb.) dayandırılmamıştır. **Demiray Kırmızı (2024)**, emniyet stokunun belirlenmesinde doğrudan varyasyon katsayısının (COV) ve %99'luk servis seviyesi hesaplamalarının kullanılmasını savunur, bu da mevcut deterministik yaklaşımımızla çelişir (Satır: 62-67). 

## 2. YENİ BİLGİLER (Kararlarımızı güçlendiren)

- **Python ve SimPy Tabanlı Simülasyon Tercihi (K34):** Açık kaynaklı SimPy ve Python kullanımımız, **Byrne (2012)** ve **Dagkakis (2016 - ManPy)** makaleleri tarafından güçlü bir şekilde desteklenmektedir. Byrne (2012), SimPy'ın ticari ExtendSim yazılımına rakip olabilecek seviyede esneklik sunduğunu belirtirken; **Herrera-Vidal (2026)** çalışması SimPy kullanılarak yapılan ayrık olay simülasyonlarının (DES) geçerliliğini ve ANOVA testleri ile entegrasyon gücünü doğrulamaktadır.
- **M-VRPTW Sınırları:** **Wang (2008)**, araç sayısının sınırlı olduğu m-VRPTW modellemesinde en öncelikli hedefin minimum mesafe yerine hizmet verilen müşteri (istasyon) sayısının maksimize edilmesi olduğunu belirtmiştir (Satır: 48-55). Bu durum, sınırlı AGV filomuzda istasyonların "starvation" (açlık) durumunu engellemeye yönelik ana hedefimizle örtüşmektedir.

## 3. FİLO VE KAPASİTE ANALİZİ (Özellikle Körösi 2026 Nature ve Ramirez 2025 MIT)

- **Körösi & Duchoň (2026) Analitik Filo Boyutlandırma:** Bu makale, deterministik durumlar için analitik kapasite kestirim modeli sunmaktadır (Satır: 140-160). Araç sayısı kestirimi için sadece hız ve mesafe değil; erişilebilirlik (A), trafik (Ft) ve operatör verimliliği (Ew) faktörlerinin çarpımının kullanılması gerektiği ispatlanmıştır. Bizim sistemimizde trafik darboğazları K36 kararı uyarınca önemlidir; Körösi (2026) bu darboğazların filo sayısını doğrusal olmayan (inversely proportional) şekilde artırdığını formülize etmiştir.
- **Ramirez (2025) MIT - Trafik Yönetimi:** SimPy tabanlı dijital ikiz uygulaması ile AGV'lerin fabrika içi trafik yönetimi modellenmiştir. Çalışmada, deterministik hesaplamaların düşük veri ortamlarında kullanışlı olduğu (Satır: 322-327) vurgulanmış, modüler yapı ile AGV kuyruklarının engellenebileceği belirtilmiştir. Projemizde çekme/itme (push/pull) sistemleriyle kurulacak Kanban döngülerinde AGV trafik tıkanıklığı bu çalışmadaki yöntemlerle (SimPy) modellenebilir.

## 4. ALGORİTMA ve SİMÜLASYON KARŞILAŞTIRMASI (GA-VRPTW, OR-Tools vs NN+2opt)

- **Genetik Algoritma (GA) vs. NN+2opt:** K34 uyarınca projemizde Nearest Neighbor + 2-opt sezgiseli (heuristic) kullanılması hedeflenmektedir. **Wang (2008)**, kısıtlı filolar için Genetik Algoritma'nın kümeli atama (customer clustering) yöntemi ile entegre edildiğinde başarılı olduğunu gösterse de (Satır: 372-390), hesaplama maliyeti yüksektir. Dinamik bir E-Kanban sisteminde sürekli anlık (real-time) yönlendirme yapılması gerektiği için bizim NN+2opt veya Sweep tabanlı daha hızlı sezgiseller kullanma kararımız pratiktir.
- **Google OR-Tools Uygulanabilirliği:** **Balikos (2025)**, Google OR-Tools paketinin küçük (25 müşteri) ve orta (50 müşteri) ölçekli CVRPTW problemlerinde oldukça yüksek çözüm yüzdelerine (yaklaşık %80-100) ulaştığını göstermiştir (Satır: 645-650). Hata payı %10'un altındadır. Ancak gerçek zamanlı (online) rotalama senaryolarına geçildiğinde statik (offline) duruma kıyasla performansın ciddi oranda düştüğü (Satır: 788-792) saptanmıştır. Sinyal tabanlı E-Kanban yapımız dinamik olduğundan, OR-Tools gibi statik çözücülerin online adaptasyonları zor olabilir; bu da SimPy ile kendi dinamik kural motorumuzu yazmamızın ne kadar haklı bir strateji olduğunu kanıtlar.

## 5. ROP ve EMNİYET STOKU (Efrilianda 2018 ROP vs K25, Demiray 2024 vs K08)

- **Efrilianda (2018) ROP ve MMFE Karşılaştırması:** Efrilianda, yeniden sipariş noktasının (Reorder Point - ROP) belirlenmesinde talep tahminlerinin (MMFE modeli) ve tedarik süresinin (Lead Time) emniyet stokuyla matematiksel birleşimini modellemiştir (Satır: 410-431). Projemizdeki K25 kararımız ROP formülasyonunu LT * Ortalama Tüketim + Emniyet Stoku şeklinde kurgulamaktadır. Bu durum Efrilianda (2018) denklem (17) modeliyle tamamen tutarlıdır.
- **Demiray (2024) vs K08:** Demiray Kırmızı vd. (2024), envanter kontrolünde standart "gün sayısı" (K08 statik alpha katsayımız gibi) yaklaşımlarının, yüksek servis seviyesi ve talep değişkenliği (COV) gerektiren yerlerde yetersiz kalabileceğini iddia etmektedir. Kararlarımız (K08, K25) şu an deterministik, sabit emniyet stoklarını (Safety Stock) savunmaktadır. Dinamik varyasyon katsayılarını (Demiray 2024) modelimize dahil etmek, sistemimizin kıtlık maliyetlerini (backorder costs) azaltabilir.
