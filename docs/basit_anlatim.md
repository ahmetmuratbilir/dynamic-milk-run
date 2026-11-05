# Projeyi Basitçe Anlatıyorum

Bu belge projeyi hiç bilmeyen birine anlatır gibi yazıldı. Sunumdaki her sayının ne dediği
ve her kısaltmanın anlamı aşağıda var.

---

## 1. Fabrikada ne oluyor?

Bir montaj hattı düşün: yan yana **24 masa** var, her birine **istasyon** diyoruz.
Her istasyonda bir işçi parça takıyor. Parçalar istasyonun yanındaki **kutularda** duruyor.

Kutu boşalırsa işçi bekler, hat durur. Buna **duruş** diyoruz. Duruş kötüdür.

Kutuları doldurmak için fabrikanın içinde küçük bir **tren** (çekici araç) dolaşıyor.
Depodan parçaları alıyor, istasyonları tek tek gezip boş kutuların yerine dolularını bırakıyor.
Sabahları kapı kapı süt dağıtan sütçüye benzediği için buna **milk-run** (sütçü turu) deniyor.

## 2. Tren ne zaman yola çıksın? İki yol var

**Geleneksel yol (P2): saat başı tur**
- Tren her **60 dakikada bir** yola çıkıyor, hiç beklemiyor.
- Hangi istasyon ne kadar parça istiyorsa onu götürüyor. İstek, kutudaki **kanban kartıyla** bildiriliyor.
- Tıpkı her saat başı geçen belediye otobüsü gibi.

**Dijital yol (P3): çağırınca gelen tren (e-Kanban)**
- Kutudaki parça belli bir seviyenin altına düşünce sistem anında elektronik bir sinyal gönderiyor.
- Tren bu sinyali alınca yola çıkıyor.
- **Konsolidasyon:** tren boş yere tek bir kutu için gitmesin diye birkaç çağrıyı toplayıp öyle çıkıyor.
- Taksi çağırmak gibi düşünebilirsin.

(Projede bir de P1 var: saat başı tur ve her seferinde hep aynı miktar. Ana karşılaştırma P2 ile P3 arasında.)

## 3. Kart ne demek? Neden önemli?

- **Kanban** Japonca "kart" demek. Her dolu kutunun bir kartı var.
- Kutu boşalınca kart depoya gidiyor ve "bana bir kutu daha getir" demiş oluyor.
- **e-Kanban** aynı işi yapan elektronik kart.
- **Kart sayısı (N)**, hatta en fazla kaç kutu bulunabileceğini belirliyor.
  - Kart çoksa hatta çok kutu birikir. Duruş azalır ama ortalık stokla dolar.
  - Kart azsa ortalık temiz kalır ama parça biter, hat durur.

Yani her zaman bir **takas** var: stok arttıkça duruş azalır.

## 4. Neyi ölçüyoruz?

| Ölçü | Ne demek | İyi olan |
|---|---|---|
| **Duruş (%)** | İstasyonların zamanının yüzde kaçında parça yokluğundan beklediği | Düşük |
| **WIP** (Work In Process, "süreçteki iş") | Hatta ortalama ne kadar parça bekliyor, yani stok | Düşük |

İkisini aynı anda düşürmek zor. Biri azalınca öbürü genelde artıyor.

## 5. Sorun ne? Neden bu çalışmayı yapıyoruz?

Daha önce yazılmış makaleler birbirini tutmuyor:
- **Bae vd. 2016:** "Saat başı tur (geleneksel) daha iyi" diyor.
- **Vojdani & Drechsler 2022:** "Çağırınca gelen (dijital) daha iyi" diyor.
- **Alnahhal vd. 2016:** "Duruma göre değişir" diyor.

Biz şunu fark ettik: Bu yarışlar **adil kurulmamış olabilir.**

Bir koşu düşün: bir koşucunun sırtında 10 kilo, öbürünün sırtında 2 kilo çanta var.
Kazananı söylemeden önce çantaları nasıl eşitlediğine bakman lazım.

Bizim konumuzda "çanta" **kart sayısı**. Makaleler iki sisteme kartı farklı yollarla dağıtmış.
- **Üretim planlamada** bu konu biliniyor: Bonvik 1997, Geraghty & Heavey 2005, Enns & Rogers 2008 "karşılaştırmayı neye göre eşitlediğin sonucu değiştirir" diyor.
- **Hat beslemede** (milk-run) kimse buna bakmamış. Herkes tek bir yolla eşitlemiş ve geçmiş.
- **Kundu vd. 2019** (s.423) "bu politikaları karşılaştırmak gelecekte yapılacak iş" diye yazmış.

**İşte boşluk (literatür açığı) bu.**

## 6. Biz ne yaptık?

Bilgisayarda sahte ama gerçekçi bir fabrika kurduk. Buna **benzetim** (simülasyon) diyoruz.
**Python** ile yazdık. Veriler **sentetik**, yani gerçek bir fabrikadan değil, gerçekçi
olsun diye bizim ürettiğimiz veriler.

- 24 istasyon, parçaları taşıyan 3 tren (bazı deneylerde 1, 2 veya 4).
- Bir gün = 1440 dakika boyunca çalıştırıyoruz.
- İlk 90 dakikayı saymıyoruz. Bu **ısınma süresi**; sistem yeni açıldığında her şey dolu olduğu için o kısım yanıltıcı.
- Her deneyi **12 kez** tekrarlıyoruz (**replikasyon**), çünkü talep rastgele. Tek seferlik şans olmasın.
- **Ortak rastgele sayılar (CRN, Common Random Numbers):** iki sistemi aynı müşteri talebiyle yarıştırıyoruz. Biri şanslı gün, öbürü şanssız gün yaşamasın.

Sonra yarışı **dört farklı adil kuralla** kurduk.

## 7. Dört eşitleme kuralı (A, B, C, D)

| Kural | Basit anlamı | Koşu benzetmesi | Kim kullanmış |
|---|---|---|---|
| **A · Eşit kart** | İki sisteme de aynı sayıda kart veriyoruz | İkisine de aynı çanta | Vojdani 2022 |
| **B · Politika-tutarlı** | Her sistem kendi kitabındaki formülle kart sayısını hesaplıyor | Herkes kendi antrenörünün dediği çantayı taşıyor | VDI 5586, Urru 2018 |
| **C · Eşit hizmet** | İkisinde de duruş en fazla %1 olsun; sonra hangisinin daha az stokla bunu yaptığına bakıyoruz | İkisi de aynı sürede bitirsin, hangisi daha az yorulmuş? | Alnahhal 2015 |
| **D · Eşit WIP** | İkisine aynı miktarda stok veriyoruz, hangisi daha az duruyor ona bakıyoruz | Aynı yükle kim daha hızlı? | (bizim eklediğimiz) |

## 8. Sonuçlar ve sayılar ne diyor?

### Önce sayıları okumayı öğrenelim

- **Δ duruş** (Δ "delta" okunur, "fark" demek) = dijitalin duruşu − geleneksel sistemin duruşu.
  - **Eksi** çıkarsa dijital daha az duruyor, yani **dijital iyi**.
  - **Artı** çıkarsa geleneksel daha az duruyor, yani **geleneksel iyi**.
- **Puan** = yüzde puanı. Örnek: dijital %2, geleneksel %13 durursa fark −11 puan olur.
- **± (artı-eksi)** = güven aralığı (%95). "Deneyi tekrar etsek sonuç büyük ihtimalle bu aralıkta çıkar" demek. ± küçükse sonuç sağlam.
- **Toyota kutuları:** her kutu bir günlük ihtiyacın en fazla %10'unu alıyor (küçük kutular). Toyota'nın kuralı bu (Sugimori 1977).
- **Mevcut kutular:** veri setindeki asıl kutular, daha büyükler.

### Bulgu 1: Kazanan, kurala göre değişiyor (sunum slayt 5)

Toyota kutularıyla, normal talepte:

| Kural | Δ duruş | Okunuşu |
|---|---|---|
| A · Eşit kart | −11,27 | Dijital 11 puan daha az duruyor → **dijital kazanır** |
| B · Politika-tutarlı | +0,11 | Geleneksel biraz daha az duruyor → **geleneksel kazanır** |
| C · Eşit hizmet | +0,12 | Duruşlar neredeyse eşit, ama dijital bunu **%36 daha az stokla** yapıyor → **dijital kazanır** |
| D · Eşit WIP | −7,69 | Aynı stokla dijital 7,7 puan daha az duruyor → **dijital kazanır** |

**Aynı fabrika, aynı tren, aynı talep. Sadece "adil" kuralını değiştirdik ve kazanan değişti.**
Fark −17,3 puan ile +2,0 puan arasında oynuyor.

**Talep şoku +%50:** gün ortasında talep birden yüzde 50 artıyor, yani sipariş patlaması.
Bu durumda da tablo aynı: B'de geleneksel kazanıyor (+1,97), diğer kurallarda dijital.

### Bulgu 2: İki kavgalı makalenin ikisini de haklı çıkardık (slayt 6)

- **Tek trenle** (tren kıt): geleneksel %7,5–12,5 duruyor, dijital %17,7–18,4 duruyor. **Geleneksel iyi**, Bae'nin dediği çıkıyor.
  - Neden? Herkes aynı anda çağırınca tek tren yetişemiyor, oysa saat başı tur düzenli.
- **3 trenle, eşit kartla:** dijital %0,12, geleneksel %2,54 duruyor. **Dijital iyi**, Vojdani'nin dediği çıkıyor.

Yani çelişkinin **iki sebebi** var:
1. **Kapasite rejimi:** tren sayısı yeterli mi, kıt mı?
2. **Eşitleme kuralı:** yarış nasıl kurulmuş?

### Neden böyle oluyor? (mekanizma, slayt 7)

- **Geleneksel:** Bir sonraki tur 60 dakika sonra. Kutu, "turun gelmesini bekleme süresi + yol süresi" boyunca yetecek kadar parça tutmak zorunda. Bu yüzden çok stok gerekiyor.
- **Dijital:** Çağırınca geliyor. Kutunun yalnızca "yol süresi" boyunca yetmesi yeterli. Daha az stok yetiyor.

Kural B'de formül geleneksel sisteme zaten **fazladan kart** veriyor. O yüzden orada geleneksel öne geçiyor.
(Bu açıklama Alnahhal 2016 s.707–708 ve Ciemnoczolowski & Bozer 2013 s.570 ile uyumlu.)

### Bulgu 3: İkinci açık, yani kart mı önemli tren mi? (slayt 8)

Ciemnoczolowski & Bozer 2013 (s.579) "kart sayısı mı, araç sayısı mı daha çok etkiler, bakılmalı" demiş. Biz baktık.

**η² (eta-kare):** duruştaki bütün iniş çıkışın yüzde kaçını bu etkenin açıkladığını gösteriyor. 0 ile 1 arasında.
- **Tren sayısı:** ≈ 0,33, yani duruş değişiminin **üçte biri** tren sayısından.
- **Kart sayısı:** 0,20–0,33, yani o da çok önemli.
- **Trenin taşıma kapasitesi (Q):** 0–0,06, yani **neredeyse hiç önemli değil.**

**Şok deneyi:** talep birden artınca her istasyona **1 kart fazla** verirsek fazladan duruş
140 istasyon-dakikadan **1'e** düşüyor. Ama stok **%69 artıyor**. Bedava değil, yine takas var.

**İstasyon-dakika:** 1 istasyon 1 dakika durdu demek. 10 istasyon 14'er dakika durursa 140 istasyon-dakika olur.

### Sağlamlık: Şans değil mi? (slayt 9)

- **Kayma** = (B kuralındaki fark) − (A kuralındaki fark). Kural değişince sonuç ne kadar kaydı, onu ölçüyor.
  - Örnek: Toyota kutuları, şok, α=0,05 → A'da −5,19, B'de +12,37 → **kayma +17,56 puan.**
- Bunu farklı ayarlarla **36 bağımsız koşulda** denedik (tabloda 52 hücre var ama bazıları birbirinin tekrarı). **36'nın 36'sında** kayma aynı yönde (pozitif) çıktı.
- **Welch testi:** iki grubun ortalaması gerçekten farklı mı, yoksa tesadüf mü, ona bakan istatistik testi.
- **OR-Tools:** Google'ın rota bulma kütüphanesi. Bizim trenin rotası çok mu kötü diye kıyas noktası olarak kullandık.

## 9. Kısaltmalar sözlüğü

| Kısaltma | Açılımı | Anlamı |
|---|---|---|
| **P1 / P2 / P3** | Politika 1/2/3 | P1 saat başı + sabit miktar; P2 saat başı + kart kadar; P3 çağırınca gelen (dijital) |
| **Kanban** | Japonca "kart" | Kutuya bağlı sipariş kartı |
| **e-Kanban** | Elektronik kanban | Kartın dijital hali, sinyal anında gidiyor |
| **ROP** | Reorder Point, yeniden sipariş noktası | "Kutu bu seviyeye düşünce çağır" eşiği |
| **N** | Kart sayısı | Hatta en çok kaç kutu bulunabileceği |
| **C** | Kutu kapasitesi | Bir kutuda kaç parça var |
| **T** | Takt / periyot | Geleneksel turun aralığı (60 dk) |
| **Q** | Araç kapasitesi | Trenin bir turda taşıyabileceği yük |
| **α (alfa)** | Emniyet payı | Formüle eklenen yedek oranı (Toyota: %10'dan az) |
| **D** | Talep | Bir istasyonun dakikada / günde kullandığı parça |
| **WIP** | Work In Process | Hatta bekleyen stok |
| **VDI** | Verein Deutscher Ingenieure (Alman Mühendisler Birliği) | Standart yayımlayan kurum |
| **VDI 5586** | Bu birliğin fabrika içi çekici tren standardı (Blatt 2, Temmuz 2022: "Planlama ve boyutlandırma") | Her rafa 1 yedek kutu ekleme (+1) kuralı bu standarttan; biz Urru 2018 üzerinden aktarıyoruz |
| **Toyota formülü** | Sugimori 1977 | Kart sayısı ≈ talep × süre × (1+α) / kutu kapasitesi |
| **η²** | Eta-kare | Bir etkenin sonuçtaki değişimin ne kadarını açıkladığı |
| **±** | Güven aralığı (%95) | Sonucun ne kadar oynayabileceği |
| **Δ** | Delta | Fark |
| **CRN** | Common Random Numbers | İki sistemi aynı rastgele talep ile yarıştırma |
| **Pareto** | — | Duruş–stok grafiğinde "ikisinde de daha iyi olan" sistemi bulma yöntemi |
| **VRP** | Vehicle Routing Problem | Trenin hangi sırayla istasyonları gezeceği problemi |
| **OR-Tools** | Google Operations Research Tools | Rota bulma yazılımı |
| **TR Dizin** | — | Türkiye'nin ulusal dergi dizini |
| **SCI-E** | Science Citation Index Expanded | Uluslararası, daha zor dergi listesi |
| **JTOM** | Journal of Turkish Operations Management | Hedef dergimiz (TR Dizin) |

## 10. Hocaya tek nefeste

> "Hat beslemede saat başı tur ile çağırınca gelen sistemi karşılaştıran makaleler zıt sonuçlar
> buluyor. Biz aynı sistemde dört farklı adil karşılaştırma kuralı denedik ve kazananın kurala göre
> değiştiğini gösterdik. Çelişkinin iki sebebi var: tren yeterli mi, kıt mı; ve yarış nasıl
> eşitlenmiş. Ayrıca kartın ve trenin duruştaki payını ayırdık: tren sayısı ve kart önemli, trenin
> kapasitesi neredeyse önemsiz."

**Zayıf yanlarımız (hoca sorarsa dürüstçe):**
- Veri sentetik, gerçek fabrika verisi değil.
- VDI 5586 ücretli bir standart. Önizlemesinden adını, tarihini (Temmuz 2022) ve sembollerini doğruladık. "+1 kutu" formülünü ise bu standardı aktaran Urru vd. 2018 (s.406) makalesinden aldık.
- Kart sayısını tüm istasyonlarda aynı miktarda değiştirdik. Daha ince ayar yapılabilir.
