# Hocaya Anlatım: Ne Yaptık, Neden Yaptık, Ne Bulduk

*Hazırlanma: 4 Kasım 2026 · Karar günlüğü K01–K110*

Bu belge, çalışmayı danışmana anlatmak için hazırlandı. Önce üç dakikalık kısa anlatım,
sonra projenin hikâyesi, kullanılan terimler, kapatılan açıklar, bulgular tek tek, sağlamlık
testlerinin ne olduğu (örnekle), danışmanın sorabileceği sorular ve cevapları, dashboard'la
on dakikalık bir sunum akışı ve dikkat edilecekler var.

Dashboard'u açmak için `dashboard.html` dosyasına çift tıklamak yeterli. Açılış sayfası olan
**Bulgular** bu belgenin uygulamadaki karşılığıdır; her bulgunun altındaki "Uygulamada
göster" düğmesi ilgili ekranı doğru ayarlarla açar.

---

## İçindekiler

1. Üç dakikada anlatım
2. Projenin hikâyesi: nereden nereye geldik
3. Terimler sözlüğü
4. Açıkları nasıl kapattık (tek tabloda)
5. Bulgular, tek tek
6. Sağlamlık testleri: "36 koşul" ne demek? (örnekli)
7. Danışmanın sorabileceği sorular ve cevaplar
8. Dashboard'la on dakikalık sunum akışı
9. Söylenmemesi gerekenler ve dikkat edilecekler
10. Sınırlılıklar ve gelecek çalışma
11. Dosyalar

---

## 1. Üç dakikada anlatım

> Fabrika içinde montaj hatlarına malzeme taşıyan araçların (milk-run) iki temel çalışma
> biçimi var: belirli aralıklarla tur atan **periyodik** sistem ve istasyon stoğu azalınca
> elektronik sinyalle çağrılan **e-Kanban** sistemi. Yazında hangisinin daha iyi olduğu
> konusunda birbirine ters sonuçlar var: Bae ve arkadaşları (2016) periyodik sistemi,
> Vojdani ve Drechsler (2022) e-Kanban'ı daha iyi buluyor.
>
> 24 istasyonlu bir simülasyon modeli kurduk ve şunu gösterdik: **kazananı politikanın
> kendisi değil, karşılaştırmanın nasıl kurulduğu ve araç kapasitesinin yeterli olup
> olmadığı belirliyor.** İki sisteme aynı rafı vermek (yazında en sık yapılan) e-Kanban'ı
> kayırıyor; çünkü periyodik sistemin rafı "tur aralığı + yol süresi" kadar, e-Kanban'ınki
> yalnızca "yol süresi" kadar süreyi karşılamak zorunda. Yazında kullanılan dört farklı
> eşitleme kuralını aynı modelde yan yana koyduk: küçük kutularda kurala göre kazanan
> değişiyor. Yazındaki iki ters sonucu da aynı modelde ürettik: tek araçta periyodik
> sistem, yeterli filoda ve eşit rafla e-Kanban önde.
>
> İkinci olarak, 2013'te Ciemnoczolowski ve Bozer'in açık bıraktığı bir soruyu
> cevapladık: duruşu asıl olarak **araç sayısı ve kart sayısı** belirliyor; aracın
> taşıyabildiği kutu sayısı neredeyse hiç etkili değil.
>
> Bulgular birbirinden bağımsız 36 farklı koşulda sınandı ve yönü hiçbirinde değişmedi.
> Bu fikrin genel hâli üretim kontrolü yazınında biliniyor (Bonvik 1997, Enns & Rogers
> 2008); bizim katkımız onu fabrika içi malzeme besleme alanına taşımak, bu alandaki
> çelişkiyi açıklamak ve 2013'ten beri açık duran ikinci bir soruyu cevaplamak.

---

## 2. Projenin hikâyesi: nereden nereye geldik

**Başlangıç (Hafta 1–13).** E-Kanban sinyalleri ile araç rotalamasını birleştiren bir karar
destek sistemi kurduk. İlk sürüm (v1), 4 araçla %24,6 duruş gösteriyor ve "periyodik sistem
dijitalden üstün" diyordu.

**Literatür denetimi (Hafta 14).** 41 makaleyi tek tek modelimizle karşılaştırdık ve
modelde üç yapısal sorun bulduk: raflar standarda göre bir kutu eksikti (VDI 5586'nın "+1
değişim kutusu"), iki sistemin durak başına hizmet süreleri farklıydı (3 dk ↔ 8 dk) ve
sinyaller gerçek stoktan değil önceden hesaplanıyordu. Düzelttiğimizde duruş %0,4'e indi ve
"periyodik üstün" sonucu ortadan kalktı. Buradan ilk ana fikir çıktı: **politikaları
karşılaştırırken rafın nasıl boyutlandırıldığı sonucu değiştiriyor.**

**Açığı kendi modelimizin dışına taşımak.** Danışman/hakem "kendi hatanızı düzeltmek katkı
mı?" diyebilirdi. Bu yüzden aynı sorunun bağımsız bir yayında da sonucu etkilediğini
gösterdik (Vojdani & Drechsler 2022'nin karşılaştırma tasarımı).

**Sağlamlık.** Parametrelerimiz Toyota'nın önerdiği sınırların dışındaydı, model tek
vardiya çalışıyordu, mesafe tablosu gerçekçi değildi. Hepsini tek tek test ettik; bulgu
değişmedi. Sonra makale tablolarını en gerçekçi ayarla (gerçekçi yerleşim, 3 vardiya,
ısınma dönemi hariç) yeniden ürettik.

**Rakip yazın.** Araştırırken "karşılaştırmanın nasıl kurulduğu sonucu değiştirir" fikrinin
üretim kontrolünde (kanban/CONWIP) bilindiğini bulduk. Bunu saklamak yerine konumlandırmayı
buna göre yaptık: fikri biz bulmadık, onu fabrika içi besleme alanına taşıdık.

**Yazındaki çelişki.** Bae (2016) ile Vojdani (2022) ters sonuçlar buluyor. İkisini de aynı
modelde ürettik ve çelişkinin iki kaynağını gösterdik.

**Derin araştırma.** Dört açıdan tarama yaptık: bizi çürüten çalışma var mı, başka açık var
mı, bu tür katkılar nasıl yayımlanmış, hangi dergiye uygun. Ana açığımızı çürüten çalışma
bulunmadı; bir katkımız düştü (zaman penceresi, Lieb 2021'de var); yerine yazarın kendisinin
"gelecek çalışma" dediği ikinci bir açık geldi.

**İkinci açık.** Ciemnoczolowski & Bozer'in (2013) sorusunu deneyle cevapladık.

**Bugün.** Bütün kaynaklar tam metinden okundu (tek eksik ücretli bir standart), makale
tabloları hazır, dashboard sadeleşti ve bulguları anlatan bir açılış sayfası eklendi.

---

## 3. Terimler sözlüğü

| Terim | Anlamı |
|---|---|
| **Milk-run** | Fabrika içinde belirli bir rota üzerinde istasyonlara malzeme taşıyan çekici/araç sistemi. |
| **Periyodik besleme (P2)** | Araç sabit aralıklarla (örn. her 60 dakikada) tur atar ve her istasyonun boşalan kutularını yerine koyar. Yazında "sabit zaman, değişken miktar" (Bozer & Ciemnoczolowski 2013, s.555). |
| **P1** | Sabit aralık, her istasyona sabit miktar (karşılaştırma için tutuldu). |
| **E-Kanban / olay tabanlı (P3)** | İstasyon stoğu yeniden sipariş noktasına düşünce elektronik sinyal gider, araç gerektiğinde çıkar. "Sabit miktar, değişken zaman". |
| **Konsolidasyon** | Dijital sistemde araç hemen çıkmaz, son teslim zamanını kaçırmadan birden fazla siparişi birleştirir. |
| **Kart (kanban) sayısı / tampon / raf** | Her istasyonun yanında tutulabilecek kutu sayısı. Toyota formülü: N = D·LT·(1+α)/C (Sugimori 1977, s.561). |
| **Politika-tutarlı boyutlandırma (VDI)** | Her politikanın rafını kendi tur aralığına göre hesaplamak; artı bir değişim kutusu (VDI 5586). |
| **Duruş (starvation)** | Parça olmadığı için istasyonun beklediği sürenin toplam süreye oranı (Korytkowski & Karkoszka 2016, s.834). |
| **WIP / hat yanı stok** | İstasyonların yanında ortalama bekleyen parça sayısı. |
| **Eşitleme kuralı** | İki sistemi "adil" karşılaştırmak için neyi eşit tuttuğun: A eşit kart, B kendi formülü, C eşit hizmet düzeyi, D eşit stok. |
| **Kayma** | Kural B'deki fark eksi kural A'daki fark. Pozitifse, eşit kart vermek dijitali olduğundan iyi göstermiş demektir. |
| **Toyota kutuları** | Kutu kapasitesi günlük talebin en fazla %10'u olacak şekilde küçültülmüş kutular (Sugimori 1977, s.561). |
| **η² (eta kare)** | Duruştaki toplam değişkenliğin ne kadarının bir faktörden kaynaklandığı (0–1 arası pay). |
| **Pareto / duruş–stok eğrisi** | Bir sistemin aynı duruşu ne kadar stokla sağlayabildiğini gösteren eğri; iki sistemi tek noktada değil bu eğri üzerinde karşılaştırmak. |
| **Nihai ayar** | Makale tablolarında kullanılan en gerçekçi ayar: gerçekçi yerleşim (durak aralığı 20,7 m, Urru 2018), 1440 dakika (3 vardiya), ilk 90 dakikalık ısınma dönemi ölçüme katılmadan. |

---

## 4. Açıkları nasıl kapattık (tek tabloda)

| Açık | Literatürde kim, ne demiş | Biz ne yaptık | Sonuç | Dashboard'da |
|---|---|---|---|---|
| **Ana açık:** Periyodik ve e-Kanban karşılaştırmasında rafın nasıl eşitlendiği sonucu belirler mi? | Kundu vd. (2019, s.423) iki politikanın karşılaştırılmasını "gelecek çalışma" bırakmış. Vojdani (2022) eşit raf, Alnahhal (2016, s.709) eşit hizmet kullanıyor; kimse kuralları karşılaştırmamış. Üretim kontrolünde ilke biliniyor (Bonvik 1997; Geraghty & Heavey 2005; Enns & Rogers 2008). | Dört eşitleme kuralını aynı modelde, duruş–stok eğrileri üzerinde karşılaştırdık. | Küçük kutularda kurala göre kazanan değişiyor; fark −17 ile +2 puan arasında oynuyor. | Politikalar ve kurallar → Dört adalet kuralı |
| **Çelişki:** Yazında neden ters sonuçlar var? | Bae (2016): milk-run önde; Vojdani (2022): dijital önde. | İki kurguyu aynı modelde kurduk. | Tek araçta periyodik, yeterli filoda eşit rafla dijital önde. Çelişkinin iki kaynağı: araç kapasitesi ve eşitleme kuralı. | Politikalar ve kurallar → Politika karşılaştırması, filo 1 |
| **Mekanizma:** Neden tersine dönüyor? | Alnahhal (2016, s.707–708): tampon ikmal süresiyle büyür; Ciemnoczolowski & Bozer (2013, s.570): kart alt sınırı çevrimle büyür. | Eski ve politika-tutarlı boyutlandırmayı karşılaştırdık. | Periyodik raf "tur + yol", e-Kanban rafı "yol" süresini karşılar; eşit kart e-Kanban'ı kayırır. | Politikalar ve kurallar → V1 ↔ VDI |
| **İkinci açık:** Duruşta kart mı, araç kapasitesi mi? | Ciemnoczolowski & Bozer (2013, s.579): *"quantify the relative contributions of the number of Kanban and the tugger capacity to starvation"* | Politika × kart × araç sayısı × araç kapasitesi × talep tam faktöriyel deney. | Araç sayısı ≈ %33, kart sayısı %20–33, aracın kutu kapasitesi %0–6. | Bulgular sayfası, 5. kart |
| **Hızlı tepki:** Şokta ne yapmalı? | Alnahhal, Ridwan & Noche (2014, §VI): talep değişimine hızlı tepki üzerine çalışma eksik. | 2 saatlik %50 talep darbesi; aynı rastgele sayılarla şoksuz koşuyla kıyas. | Periyodik sistemde +1 kart şoku neredeyse siliyor ama stok %70 artıyor; dijitalde 3 araçtan sonra araç eklemek işe yaramıyor. | Bulgular sayfası, 6. kart |

**Kapatmadığımız / katkı olarak sunmadığımız:** stoktan türetilen zaman penceresi (Lieb 2021,
s.118–120'de var), "dinamik kontrol statikten iyidir" (Lieb 2021'de 18 strateji
karşılaştırılmış), olay tabanlı kontrolde filo boyutu.

---

## 5. Bulgular, tek tek

Her bulgu için: neden yaptık, literatürde ne vardı, ne aldık, programda ne yaptık, ne bulduk,
hangi açığı kapatıyor, dashboard'da nerede.

### Bulgu 1 — Önce model düzeltildi: modelleme kararları politika farkından büyük

- **Neden yaptık?** İlk sürüm 4 araçta %24,6 duruş gösteriyor ve "periyodik sistem üstün"
  diyordu. Literatürle karşılaştırınca bunun model kurulumundan geldiğinden şüphelendik.
- **Literatürde ne vardı?** VDI 5586 standardı ve Urru ve arkadaşları (2018, s.406) her
  rafa bir "değişim kutusu" eklenmesini ister. Kart sayısı formülü Toyota'dan gelir
  (Sugimori ve arkadaşları 1977, s.561).
- **Ne aldık?** Toyota formülünü ve "+1 kutu" kuralını.
- **Programda ne yaptık?** Hataları tek tek düzeltip her adımın etkisini ayrı ayrı ölçtük
  (ayrıştırma).
- **Ne bulduk?** Hizmet süresi farkı tek başına 10,3 puan, eksik raf 3,9 puan oynatıyor;
  politikalar arasındaki gerçek fark ise yaklaşık 1 puan. Yanlış kurulan bir model,
  politika seçiminden daha çok şey değiştiriyor.
- **Hangi açık?** Hangi modelleme kararının sonucu ne kadar değiştirdiğini tek tek ölçen
  uygulama nadir.
- **Dashboard'da:** Politikalar ve kurallar → Ayrıştırma paneli (adımları açıp kapatarak).

### Bulgu 2 — Başka bir çalışmanın karşılaştırma tasarımı sonucu kaydırıyor

- **Neden yaptık?** "Kendi hatanızı düzeltmek katkı mı?" sorusuna karşı, sorunun bağımsız
  bir yayında da etkili olup olmadığını görmek için.
- **Literatürde ne vardı?** Vojdani ve Drechsler (2022, s.5) iki sistemi karşılaştırırken
  ikisine de aynı iki kutulu rafı veriyor. Oysa Droste ve Deuse (2011), Urru (2018) ve
  Ciemnoczolowski ve Bozer (2013, s.570) gereken rafın tur aralığıyla büyüdüğünü gösteriyor.
  Kundu ve arkadaşları (2019, s.423) bu iki politikanın karşılaştırılmasını açıkça "gelecek
  çalışma" olarak bırakıyor.
- **Ne aldık?** Vojdani'nin karşılaştırma tasarımını olduğu gibi.
- **Programda ne yaptık?** Aynı sistemde iki kurgu: A (eşit iki kutu, Vojdani) ve B (her
  politika kendi tur aralığına göre).
- **Ne bulduk?** Vojdani tasarımı dijitali 2,4–16 puan önde gösteriyor; doğru kurulan rafta
  fark küçülüyor, küçük kutularda yön değiştiriyor. Örnek (nihai ayar, mevcut kutular,
  talep şoku): A'da dijital 10,8 puan önde, B'de yalnızca 1,9 puan önde.
- **Hangi açık?** Raf boyutlandırma yazını ile politika karşılaştırma yazını birleşmemiş.
- **Dashboard'da:** Politikalar ve kurallar → Dört adalet kuralı (mevcut kutular, şok); A ve
  B noktaları.

### Bulgu 3 — Dört eşitleme kuralı: kazanan kurala göre değişiyor (ana bulgu)

- **Neden yaptık?** "Neden bu eşitleme? Başkası olsa ne olurdu?" sorusuna cevap vermek için.
- **Literatürde ne vardı?** Üretim kontrolünde bu ilke biliniyor: Bonvik ve arkadaşları
  (1997, s.797) yöntemleri "%99,9 hizmet düzeyini en az stokla sağlayan ayar" üzerinden,
  Geraghty ve Heavey (2005, s.448–454) hizmet–stok eğrisi üzerinden karşılaştırıyor; Enns ve
  Rogers (2008) adil bir kurguyla sıralamanın tersine döndüğünü gösteriyor. Fabrika içi
  beslemede ise her çalışma tek bir eşitleme kullanıyor: Vojdani eşit raf, Alnahhal ve Noche
  (2015) ile Alnahhal ve arkadaşları (2016, s.709) eşit hizmet düzeyi.
- **Ne aldık?** Üretim kontrolündeki "eğri üzerinde karşılaştır" yaklaşımını ve alandaki
  dört eşitleme kuralını.
- **Programda ne yaptık?** İki sistemin kart sayısını −3 ile +6 arasında tarayıp duruş–stok
  eğrilerini çizdik; dört kural bu eğriler üzerinde dört nokta oldu.
- **Ne bulduk?** Küçük (Toyota) kutularda politika-tutarlı kural periyodik sistemi, diğer
  üç kural e-Kanban'ı kazandırıyor. Duruş farkı kurala göre −17 ile +2 puan arasında
  oynuyor. Mevcut kutularda kazanan hep dijital, ama farkın büyüklüğü kurala göre çok
  değişiyor (0,03 puandan 17,3 puana).
- **Hangi açık?** Ana açık.
- **Dashboard'da:** Politikalar ve kurallar → Dört adalet kuralı (Toyota kutuları, şok).

### Bulgu 4 — Yazındaki iki ters sonucu aynı modelde ürettik

- **Neden yaptık?** Modelimizin yazındaki çelişkiyi açıklayıp açıklayamayacağını görmek için.
- **Literatürde ne vardı?** Bae, Evans ve Summers (2016) tek araçla periyodik sistemi önde
  buluyor (talep üzerine sistemde duruş yaklaşık 4 kat). Vojdani ve Drechsler (2022)
  e-Kanban'ı önde buluyor.
- **Ne aldık?** İki çalışmanın kurgusunu: Bae'den tek araç, Vojdani'den yeterli filo ve
  eşit raf.
- **Programda ne yaptık?** İki kurguyu aynı modelde kurduk.
- **Ne bulduk?** Tek araçta periyodik sistem her iki kuralda da önde (%7,5–12,5'e karşı
  %17,7–18,4); 3 araçta eşit rafla e-Kanban önde (%0,12'ye karşı %2,54). Çelişkinin iki
  kaynağı var: araç kapasitesinin yeterli olup olmadığı ve rafın nasıl eşitlendiği.
- **Hangi açık?** Alandaki çelişkili bulguları tek modelde açıklıyor; Alnahhal (2016)'nın
  "kapasiteye bağlı" sonucuyla da tutarlı.
- **Dashboard'da:** Politikalar ve kurallar → Politika karşılaştırması, filo 1 araç.

### Bulgu 5 — Duruşu kart sayısı ve araç sayısı belirliyor, aracın kapasitesi değil

- **Neden yaptık?** İkinci, bağımsız bir açık olduğu için.
- **Literatürde ne vardı?** Ciemnoczolowski ve Bozer (2013, s.579) bu soruyu açıkça
  cevapsız bırakmış. Onlar sabit tüketim varsayıp araç kapasitesi artınca duruşun
  sıfırlandığını buldu.
- **Ne aldık?** Sorunun kendisini.
- **Programda ne yaptık?** 2 politika × 4 kart düzeyi × 4 araç sayısı × 3 araç kapasitesi ×
  2 talep düzeyi = 192 kombinasyon, her biri 4 tekrar. Duruştaki değişkenliğin her faktöre
  düşen payını (η²) hesapladık.
- **Ne bulduk?** Değişken talepte duruşu araç sayısı (yaklaşık %33) ve kart sayısı
  (%20–33) belirliyor; aracın taşıyabildiği kutu sayısı %0–6. E-Kanban'da kart ve araç
  birbirini tamamlıyor (etkileşim %29): ek kart ancak yeterli araç varken işe yarıyor.
- **Hangi açık?** İkinci açık: 2013'ten beri açık duran soruya değişken talep altında cevap.
- **Dashboard'da:** Bulgular sayfasındaki çubuk grafik; Ne olursa? sayfasında filo
  değiştirilerek denenebilir.

### Bulgu 6 — Talep şokunda bir ek kart, ek araçtan daha etkili ama stoğa mal oluyor

- **Neden yaptık?** Fabrikada şok olduğunda ilk soru "araç mı ekleyelim, kart mı?" olur.
- **Literatürde ne vardı?** Alnahhal, Ridwan ve Noche (2014): sistemin talep değişimine
  hızlı tepkisi üzerine çalışma eksik. Bocewicz ve arkadaşları (2019, s.51): değişen
  talepte geçiş.
- **Programda ne yaptık?** 8. saatte 2 saatlik %50 talep artışı verdik ve aynı rastgele
  sayılarla şoksuz koşuya göre fazladan duruşu ölçtük.
- **Ne bulduk?** Periyodik sistemde, 2 araçla, istasyon başına tek ek kart fazladan duruşu
  140 istasyon-dakikadan 1'e indiriyor, ama ortalama stok 621'den 1051'e çıkıyor (%69).
  Araç sayısını 2'den 4'e çıkarmak ise 140'ı ancak 94'e indiriyor. Dijital sistemde 3
  araçtan sonra araç eklemek bir şey değiştirmiyor.
- **Dashboard'da:** Bulgular sayfasındaki şok tablosu.

### Bulgu 7 — Neden tersine dönüyor? (mekanizma)

- **Neden yaptık?** "Sonuç kurala bağlı" demek yetmez, hakem "neden?" diye sorar. Benzer
  bir makale (Enns & Rogers 2008) bunu açıklamadığı için az atıf almış (16).
- **Literatürde ne vardı?** Alnahhal ve arkadaşları (2016, s.707–708): raf ihtiyacı, parça
  gelene kadar geçen süreyle büyür; klasik kanbanda talep bilgisi ancak araç gelince
  iletilir. Ciemnoczolowski ve Bozer (2013, s.570): kart sayısının alt sınırı bir turdaki
  tüketimle büyür. Sugimori (1977, s.562): Toyota talep artınca kart sayısını değil tedarik
  süresini değiştirir.
- **Ne bulduk?** Periyodik sistemde raf "tur aralığı + yol süresi", e-Kanban'da yalnızca
  "yol süresi" kadar süreyi karşılamak zorunda. Bu yüzden eşit raf e-Kanban'ı kayırıyor;
  her politikaya kendi süresine göre raf verilince fark kapanıyor. Basit bir örnek: 60
  dakikalık tur aralığı ve 45 dakikalık yol süresiyle periyodik sistemin rafı 105 dakikalık,
  e-Kanban'ınki 45 dakikalık tüketimi karşılamalı. İkisine aynı rafı verirsen periyodik
  sistem aç kalır.
- **Dashboard'da:** Politikalar ve kurallar → Politika karşılaştırması, "Eski boyutlandırma
  (V1)" ile "Politika-tutarlı (VDI)" arasında geçiş.

### Bulgu 8 — Sonuçlar sağlam

- **Neden yaptık?** Bazı parametrelerimiz Toyota'nın önerdiği sınırların dışındaydı, model
  tek vardiya çalışıyordu ve mesafe tablosu gerçekçi değildi.
- **Ne yaptık?** Toyota sınırları içinde, 3 vardiyada, ısınma dönemi hariç ve gerçekçi bir
  yerleşimle tekrarladık (ayrıntı ve örnek 6. bölümde).
- **Ne bulduk?** Etkinin yönü birbirinden bağımsız 36 koşulun 36'sında aynı. Eski mesafe
  tablosu, Vojdani ile aramızdaki görünür bir çelişkinin de kaynağıymış.
- **Dashboard'da:** Doğrulama sayfası.

---

## 6. Sağlamlık testleri: "36 koşul" ne demek? (örnekli)

### Ne ölçüyoruz?

Her koşulda aynı soruyu soruyoruz: **"İki sisteme eşit raf vermek (kural A) ile her birine
kendi formülüyle raf vermek (kural B) arasında, dijital ile geleneksel arasındaki fark ne
kadar değişiyor?"** Bu değişime **kayma** diyoruz:

> kayma = (kural B'de dijital − geleneksel duruş) − (kural A'da dijital − geleneksel duruş)

Kayma pozitifse, eşit raf vermek dijitali olduğundan iyi göstermiş demektir. Bulgumuz
"kayma her zaman pozitif" iddiasıdır; test, bunun parametreler değişince bozulup
bozulmadığını sınar.

### Hesaplanmış bir örnek

Toyota kutuları, %50 talep şoku, güvenlik katsayısı α = 0,05 (K95):

| Kural | Geleneksel ↔ dijital farkı (dijital − geleneksel) | Okunuşu |
|---|---:|---|
| A · eşit raf (Vojdani'nin kurgusu) | −5,19 puan | Dijital 5,19 puan daha az duruşla önde |
| B · her biri kendi formülüyle | +12,37 puan | Geleneksel 12,37 puan daha az duruşla önde |
| **Kayma** = 12,37 − (−5,19) | **+17,56 puan** | Kural değişince sıralama tersine dönüyor |

Yani **aynı fabrika, aynı talep, aynı araçlar**: sadece rafı nasıl dağıttığınıza göre
"dijital çok iyi" ya da "geleneksel çok iyi" sonucu çıkabiliyor.

İkinci örnek (gerçekçi yerleşim, %50 şok, K100): kural A'da dijital 8,72 puan önde, kural
B'de yalnızca 0,93 puan önde. Kayma +7,79. Sıralama değişmiyor ama fark %89 küçülüyor.

### 36 koşul nereden geliyor?

| Test | Neyi değiştirdik | Hücre | Bağımsız | Kayma pozitif |
|---|---|---:|---:|---:|
| **K95 · Toyota formülü bandı** | Güvenlik katsayısı α (0; 0,05; 0,10; 0,15; 0,20) × kutu boyu (mevcut, Toyota; araç kapasitesi iki türlü) × talep (baz, şok) | 30 | 20 | 30/30 |
| **K99 · Ufuk ve ölçüm** | Süre (480 / 1440 dk) × ölçüm (ısınma dahil / hariç) × kutu boyu × talep | 16 | 12 | 16/16 |
| **K100 · Mesafe ağı** | Eski tablo / gerçekçi yerleşim / genişletilmiş yerleşim × talep | 6 | 4 | 6/6 |
| **Toplam** | | **52** | **36** | **52/52** |

**Neden 52 değil 36?** K95'te araç kapasitesinin iki türü (sabit / hacme göre ayarlı) birebir
aynı sonucu verdi, çünkü araç hiçbir koşulda dolmuyor (doluluk ≤ %57); bu 10 hücre kopya.
K99 ve K100'deki bazı hücreler de K95'teki koşulların aynısı. Danışmana "52 test hücresi,
36 bağımsız koşul" demek doğru olanı.

**Ayrıca:** Kaymanın büyüklüğü koşula göre +1,3 ile +19,0 puan arasında değişiyor. Toyota
kutularında ve şokta en büyük; yani parametreleri Toyota'nın önerdiği sınırlara çektikçe
etki küçülmüyor, büyüyor.

---

## 7. Danışmanın sorabileceği sorular ve cevaplar

**"Gerçek veri yok, sentetik veriyle ne gösterebilirsin?"**
Katkımız yöntemsel: eşitleme kuralının sonucu değiştirdiği, verinin gerçek olup olmamasından
bağımsız gösterilebilir. Parametreler literatürden: kart formülü Sugimori (1977), durak
aralığı Urru (2018), karşılaştırma tasarımı Vojdani (2022), hizmet hedefi Alnahhal & Noche
(2015). PAJES 2026'da (Sevim & Görkemli Aykut) varsayımsal sistemle bir milk-run makalesi
yayımlanmış. Gerçek veri gelirse altyapı hazır (dashboard'da Veri girişi sayfası).

**"Bu zaten bilinen bir şey değil mi?"**
Genel ilke üretim kontrolünde biliniyor (Bonvik 1997; Enns & Rogers 2008). Fabrika içi
malzeme beslemede kimse eşitleme kurallarını yan yana koymamış; bu alandaki çelişkili
sonuçları (Bae 2016 ↔ Vojdani 2022) açıklayan bir çalışma yok. Ayrıca Ciemnoczolowski &
Bozer'in 2013'te açık bıraktığı soruyu cevaplıyoruz.

**"Enns & Rogers (2008) aynı şeyi yapmamış mı?"**
Benzer fikir, farklı alan (CONWIP ↔ push). Onlar mekanizmayı açıklamıyor ve hangi kuralın
ne zaman kullanılacağını söylemiyor; biz ikisini de yapıyoruz. Sadece 16 atıf almaları, bu
mesajın tek başına zayıf kaldığını gösteriyor; bu yüzden mekanizma ve ikinci açığı ekledik.

**"Alnahhal (2016) karşılaştırmayı adil yapmış, sizin farkınız ne?"**
Evet, eşit hizmet düzeyinde (%3 duruş) karşılaştırmışlar ve sonuçları bizim C kuralımızla
tutarlı. Ama tek bir kural kullanmışlar; kural değişince sonucun nasıl değiştiğine
bakmamışlar. Ayrıca rotaları sabit, bizimki olay tabanlı.

**"Modelin doğru olduğunu nereden biliyorsun?"**
Isınma süresi Welch yöntemiyle 90 dakika ölçüldü. 9 tekrarda güven aralığı ±0,05 puanın
altına iniyor (tablolar 12 tekrar). Tur içi rota sıralaması tam aramaya göre ortalama %0,62
sapıyor. Duruş tanımı Korytkowski (2016) ile aynı. Rotalama genel kıyaslamada (Solomon)
OR-Tools'tan geride; bunu sınırlılık olarak yazıyoruz. Fabrika senaryosunda ise sezgisel,
gecikmeyi öncelikli tutuyor.

**"Neden simülasyon, neden matematiksel model değil?"**
Schmidt vd. (2016, s.1): milk-run tasarımı "sıradan bir optimizasyon problemi olarak çözücüye
verilemez". Stokastik talep altında kapalı döngü davranışı karşılaştırıyoruz; analitik
formüller bunu yakalamıyor.

**"Sonuçlar istatistiksel olarak anlamlı mı?"**
Her değer 12 tekrarın ortalaması ± %95 güven aralığı. Kazanan kararları, fark güven
aralığının dışındaysa veriliyor; içindeyse "eşit" yazılıyor. Sevk kuralları için ANOVA ve
Tukey yapıldı: fark yok (p = 0,9997 ve 0,3415).

**"Neden 24 istasyon, 4 hat?"**
Literatürdeki tipik hat besleme düzenine göre (Sevim 2026'da 10, Korytkowski 2016'da 10
istasyon). Tek fabrika düzeni bir sınırlılık; gelecekte yayımlanmış bir vakayı yeniden
kurmak öneriliyor.

**"α = 0,15 neden? Toyota %10'u geçmeyin diyor."**
Sugimori (1977, s.562) α'yı atölyenin iyileştirme yeteneğinin göstergesi sayıyor: yetersiz
atölyeler geçici olarak α'yı artırır. Ayrıca α'yı 0 ile 0,20 arasında tarayıp sonucun
değişmediğini gösterdik (K95).

**"Sevk kuralları arasında fark yoksa o kısım boşa mı?"**
Hayır, bilgilendirici bir olumsuz bulgu: duruşu sevk ayrıntısından çok kart ve araç sayısı
belirliyor. Lieb (2021) da kalkış kurallarında anlamlı fark bulamamış; bağımsız bir doğrulama.

**"52 test mi yaptın?"**
52 test hücresi, 36 bağımsız koşul (6. bölüm). Kayma hepsinde pozitif.

**"Hangi dergiye göndereceksin?"**
TR Dizin: Endüstri Mühendisliği Dergisi (ana hedef) veya Journal of Turkish Operations
Management (kabul oranı %73–83). SCI-E için (Journal of Simulation) yayımlanmış bir vakanın
yeniden kurulması gibi eklemeler gerekir.

**"Uygulamaya ne faydası var?"**
Fabrika yöneticisine iki net mesaj: (1) "Dijitale geçersek duruş düşer" hesabı yapılırken
iki sisteme aynı raf verilirse dijital olduğundan iyi görünür; doğru karşılaştırma stok
maliyetini de hesaba katmalı. (2) Duruş artınca ilk bakılacak yer araç sayısı ve kart
sayısı; araç büyütmek (daha çok kutu taşıyan araç) çoğu zaman işe yaramaz. Şokta tek ek
kart çok etkili ama stoğu %70 artırır.

**"En zayıf yerin ne?"**
Gerçek veri yok ve tek fabrika düzeni var. Ayrıca kart sayısını tüm istasyonlarda aynı
miktarda değiştirdik; Bonvik (1997) gibi her istasyonu ayrı optimize etmedik.

**"Bundan sonra ne yapacaksın?"**
Makaleyi yazmak. İsteğe bağlı güçlendirme: yayımlanmış bir vakayı (Korytkowski'nin 10
istasyonu) yeniden kurup bulguyu orada da göstermek; gerçek veri bulunursa onunla doğrulamak.

---

## 8. Dashboard'la on dakikalık sunum akışı

1. **Bulgular sayfası (açılış), 1 dk.** Üstteki "Tek cümlede" kutusunu oku; üç sayıyı göster.
2. **Bulgu 1 → "Uygulamada göster: ayrıştırma paneli", 1 dk.** Adımları açıp kapatarak
   modelleme kararlarının etkisini göster; "hizmet süresi asimetrisi" kutusunu kapatınca
   sonucun nasıl değiştiğine dikkat çek.
3. **Bulgu 2 → "kural A ve B noktaları", 1 dk.** Mevcut kutular, şok: A noktasında dijital
   çok önde, B noktasında fark küçük.
4. **Bulgu 3 → "dört kural, Toyota kutuları", 2 dk.** Ana bulgu. Grafikte mavi (geleneksel)
   ve yeşil (dijital) eğrileri, üzerlerindeki A, B, C, D noktalarını göster; tablodan
   "Kazanan" sütununun kurala göre değiştiğini oku.
5. **Bulgu 4 → "tek araçta politikalar", 1 dk.** Filo 1 araçken periyodik sistemin önde
   olduğunu göster; sonra filo kutusunu 3 yap, farkın kapandığını göster.
6. **Bulgu 5 ve 6, 2 dk.** Kartlardaki çubuk grafikle "araç sayısı ve kart sayısı belirliyor,
   aracın kapasitesi değil" mesajı; şok tablosuyla "+1 kart çok etkili ama stok artıyor".
7. **Bulgu 7 → "eski boyutlandırmayla politikalar", 1 dk.** V1 ile VDI arasında geçiş yapıp
   kart sayılarının nasıl değiştiğini göster; mekanizmayı (tur + yol ↔ yol) anlat.
8. **Doğrulama sayfası, 1 dk.** Sağlamlık tablosu ve ısınma grafiği; "36 bağımsız koşulun
   36'sında yön aynı".
9. **Bulgular sayfasının altındaki "Dikkat edilmesi gerekenler" kutusu.** Sınırlılıkları
   kendin söyle; danışman sormadan söylemek güven verir.

---

## 9. Söylenmemesi gerekenler ve dikkat edilecekler

| Söyleme | Bunun yerine |
|---|---|
| "Bu fikri ilk biz bulduk." | "Üretim kontrolünde bilinen ilkeyi fabrika içi beslemeye taşıdık ve buradaki çelişkiyi açıkladık." |
| "E-Kanban ile rotalamayı ilk biz birleştirdik." | Söylenmez; Menanno 2023, Vojdani 2022, Alnahhal 2016 yapmış. |
| "Kimse eşitlemeyi düşünmemiş." | "Her çalışma tek bir taban kullanmış; bazen açık, çoğunlukla örtük." |
| "Toyota kutularında üç farklı kazanan var." | "İki farklı kazanan var" (nihai ayarla). |
| "52 koşulda test ettik." | "36 bağımsız koşul (52 test hücresi)." |
| "Stoktan türetilen zaman penceresi bizim katkımız." | "Lieb (2021)'deki mantığı kullandık" (yöntem). |
| "Dijital sistem daha iyi." | "Hangisinin iyi olduğu karşılaştırmanın nasıl kurulduğuna ve araç kapasitesine bağlı." |
| "İstasyonlar ekranında anlık stok görülüyor." | "Bu ekran temsili; kart sayısı ve ROP gerçek formülle, stok çubukları temsili." |

**Sayılar:** Makaleye ve sunuma yalnızca `docs/makale_tablolari.md`'deki (nihai ayar) sayılar
girer. Eski haftalık raporlardaki sayılar farklı ayarla üretildi.

---

## 10. Sınırlılıklar ve gelecek çalışma

### Sınırlılıklar

- Sentetik veri; tek fabrika düzeni (24 istasyon, 4 hat); hatlar arası mesafe bir varsayım.
- Aracın kutu kapasitesi deneylerde hiç dolmadı; Ciemnoczolowski & Bozer'in "çekici
  kapasitesi" çok araçlı sistemimizde araç sayısıyla temsil edildi.
- Eşit hizmet kuralında hizmet düzeyi zaman bazlı duruşla temsil edildi (Alnahhal'da
  adet bazlı doluluk oranı).
- Kart sayısı tüm istasyonlarda aynı miktarda değiştirildi; istasyon bazında optimize
  edilmedi.
- Talep şoku ya koşu boyunca sabit bir artış ya da tek bir darbe; gerçek talep örüntüleri
  denenmedi.
- Rotalama sezgiseli genel kıyaslamada OR-Tools'tan geride.

### Gelecek çalışma

- Yayımlanmış bir vakanın (Korytkowski 2016, 10 istasyon) yeniden kurulması.
- Gerçek fabrika verisiyle doğrulama.
- Kart sayısının istasyon bazında optimize edildiği "her politika kendi en iyi ayarında"
  karşılaştırma (Bonvik 1997 yaklaşımı).
- Hangi karar sorusunda hangi eşitleme kuralının kullanılacağına dair bir rehber.

---

## 11. Dosyalar

| Ne | Nerede |
|---|---|
| Dashboard (açılış: Bulgular) | `dashboard.html` |
| Makale tabloları | `docs/makale_tablolari.md` |
| Hazır makale cümleleri | `docs/literatur_boslugu_analizi.md` §5, §8 |
| Derin araştırma raporu | `reports/Hat besleme literatür açığı.md` |
| Proje rehberi | `docs/proje_rehberi.html` |
| Tüm kararlar ve kaynakları | `docs/karar_gunlugu.md` (K01–K110) |
| Şekiller | `docs/figurler/` (ana figür: `sekil7_adalet_kurallari_nihai_toyota.png`; ikinci açık: `sekil9_kart_kapasite.png`) |
| Okunan makaleler (PDF) | `Desktop/dinamik milk run/ek_kaynaklar_kasim_2026/` (yerelde; GitHub'a gönderilmedi) |
