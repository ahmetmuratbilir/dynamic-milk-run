# Hocaya Anlatım: Ne Yaptık, Neden Yaptık, Ne Bulduk

*Hazırlanma: 4 Kasım 2026 · Karar günlüğü K93–K110*

Bu metin, son çalışmalarda konuşulanların hocaya anlatılabilecek biçimde bir arada yazılmış
hâlidir. Her bulgu için aynı beş soru cevaplanır: neden yaptık, literatürde ne vardı, ne
aldık, programda ne yaptık, hangi açığı kapatıyor. Her bulgunun dashboard'da nerede
gösterileceği de yazılıdır. Dashboard'u açmak için `dashboard.html` dosyasına çift tıklamak
yeterli; açılış sayfası olan **Bulgular** sayfası bu metnin uygulamadaki karşılığıdır.

---

## 1. Üç dakikada anlatım

> Fabrika içinde montaj hatlarına malzeme taşıyan araçların (milk-run) iki temel çalışma
> biçimi var: belirli aralıklarla tur atan **periyodik** sistem ve istasyon stoğu azalınca
> elektronik sinyalle çağrılan **e-Kanban** sistemi. Yazında hangisinin daha iyi olduğu
> konusunda birbirine ters sonuçlar var: Bae ve arkadaşları (2016) periyodik sistemi,
> Vojdani ve Drechsler (2022) e-Kanban'ı daha iyi buluyor.
>
> Biz 24 istasyonlu bir simülasyon modeli kurduk ve şunu gösterdik: **kazananı politikanın
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
> Bulgular 52 farklı koşulda sınandı ve yönü değişmedi. Bu fikrin genel hâli üretim
> kontrolü yazınında biliniyor (Bonvik 1997, Enns & Rogers 2008); bizim katkımız onu
> fabrika içi malzeme besleme alanına taşımak ve bu alandaki çelişkiyi açıklamak.

---

## 2. Bugün adım adım ne yaptık

1. **Dashboard'u makaleyle aynı ayara getirdik.** Makale tablolarında kullandığımız nihai
   ayar (gerçekçi mesafe ağı, 3 vardiya, ısınma dönemi hariç ölçüm) dashboard'un verisine
   de uygulandı. Böylece ekranda gösterilen sayılar makaledekilerle aynı.
2. **Makale yazım araçlarını ve dergi kurallarını araştırdık.** Hedef dergi Endüstri
   Mühendisliği Dergisi: en fazla 8.000 kelime, 200'er kelimelik Türkçe ve İngilizce özet,
   Word. Simülasyon makaleleri için STRESS-DES kontrol listesini kullanacağız.
3. **Literatür açığımızı sorguladık ve rakip yazını bulduk.** "Karşılaştırmanın nasıl
   kurulduğu sonucu değiştirir" fikrinin üretim kontrolünde bilindiğini gördük (Bonvik
   1997; Geraghty & Heavey 2005). İkisini de indirip okuduk.
4. **Yazındaki çelişkiyi bulduk.** Bae ve arkadaşları (2016) ile Vojdani ve Drechsler
   (2022) ters sonuçlar buluyor; ikisi de iki sisteme aynı rafı veriyor.
5. **Dört ayrı açıdan derin araştırma yaptık:** bizi çürüten çalışma var mı, yazında ilan
   edilmiş başka boşluk var mı, bu tür yöntemsel katkılar nasıl yayımlanmış, hangi dergiye
   uygun. Sonuçlar `reports/Hat besleme literatür açığı.md` dosyasında.
6. **Alnahhal ve arkadaşlarının (2016) makalesini okuduk.** Bizi çürütmüyor; tersine
   mekanizmamıza dayanak veriyor.
7. **İkinci açığın deneyini yaptık:** kart sayısı mı, araç kapasitesi mi? Ayrıca talep
   şoku sonrası toparlanma ve tek araç kurgusu.
8. **Dashboard'u sadeleştirdik:** yazılı menü, her sayfada "bu sayfada ne var" açıklaması,
   ve açılışta bulguları anlatan yeni Bulgular sayfası.

---

## 3. Bulgular, tek tek

### Bulgu 1 — Önce model düzeltildi: modelleme kararları politika farkından büyük

- **Neden yaptık?** İlk sürüm 4 araçta %24,6 duruş gösteriyor ve "periyodik sistem üstün"
  diyordu. Literatürle karşılaştırınca bunun model kurulumundan geldiğinden şüphelendik.
- **Literatürde ne vardı?** VDI 5586 standardı ve Urru ve arkadaşları (2018, s.406) her
  rafa bir "değişim kutusu" eklenmesini ister. Kart sayısı formülü Toyota'dan gelir
  (Sugimori ve arkadaşları 1977, s.561).
- **Ne aldık?** Toyota formülünü ve "+1 kutu" kuralını.
- **Programda ne yaptık?** Hataları tek tek düzeltip her adımın etkisini ayrı ayrı ölçtük.
- **Ne bulduk?** Hizmet süresi farkı tek başına 10,3 puan, eksik raf 3,9 puan oynatıyor;
  politikalar arasındaki gerçek fark ise yaklaşık 1 puan. Yanlış kurulan bir model,
  politika seçiminden daha çok şey değiştiriyor.
- **Hangi açık?** Hangi modelleme kararının sonucu ne kadar değiştirdiğini tek tek ölçen
  uygulama nadir.
- **Dashboard'da:** Politikalar ve kurallar → Ayrıştırma paneli.

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
  fark küçülüyor, küçük kutularda yön değiştiriyor.
- **Hangi açık?** Raf boyutlandırma yazını ile politika karşılaştırma yazını birleşmemiş.
- **Dashboard'da:** Politikalar ve kurallar → Dört adalet kuralı (mevcut kutular, şok);
  A ve B noktaları.

### Bulgu 3 — Dört eşitleme kuralı: kazanan kurala göre değişiyor (ana bulgu)

- **Neden yaptık?** "Neden bu eşitleme? Başkası olsa ne olurdu?" sorusuna cevap vermek
  için.
- **Literatürde ne vardı?** Üretim kontrolünde bu ilke biliniyor: Bonvik ve arkadaşları
  (1997, s.797) yöntemleri "%99,9 hizmet düzeyini en az stokla sağlayan ayar" üzerinden,
  Geraghty ve Heavey (2005) hizmet–stok eğrisi üzerinden karşılaştırıyor; Enns ve Rogers
  (2008) adil bir kurguyla sıralamanın tersine döndüğünü gösteriyor. Fabrika içi beslemede
  ise her çalışma tek bir eşitleme kullanıyor: Vojdani eşit raf, Alnahhal ve Noche (2015)
  ile Alnahhal ve arkadaşları (2016, s.709) eşit hizmet düzeyi.
- **Ne aldık?** Üretim kontrolündeki "eğri üzerinde karşılaştır" yaklaşımını ve alandaki
  dört eşitleme kuralını.
- **Programda ne yaptık?** İki sistemin kart sayısını tarayıp duruş–stok eğrilerini çizdik;
  dört kural bu eğriler üzerinde dört nokta oldu.
- **Ne bulduk?** Küçük (Toyota) kutularda politika-tutarlı kural periyodik sistemi, diğer
  üç kural e-Kanban'ı kazandırıyor. Duruş farkı kurala göre −17 ile +2 puan arasında
  oynuyor.
- **Hangi açık?** Ana açık: üretim kontrolünde bilinen adil karşılaştırma ilkesini fabrika
  içi besleme alanına taşıyoruz ve tek noktalı karşılaştırmanın neden yanıltabileceğini
  sayıyla gösteriyoruz.
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
  %17,7–18,4); 3 araçta eşit rafla e-Kanban önde. Çelişkinin iki kaynağı var: araç
  kapasitesinin yeterli olup olmadığı ve rafın nasıl eşitlendiği.
- **Hangi açık?** Alandaki çelişkili bulguları tek modelde açıklıyor.
- **Dashboard'da:** Politikalar ve kurallar → Politika karşılaştırması, filo 1 araç.

### Bulgu 5 — Duruşu kart sayısı ve araç sayısı belirliyor, aracın kapasitesi değil

- **Neden yaptık?** İkinci, bağımsız bir açık olduğu için.
- **Literatürde ne vardı?** Ciemnoczolowski ve Bozer (2013, s.579) bu soruyu açıkça
  cevapsız bırakmış: kart sayısı ile aracın kapasitesinin duruşa katkıları ayrı ayrı
  ölçülmeli. Onlar sabit tüketim varsayıp araç kapasitesi artınca duruşun sıfırlandığını
  buldu.
- **Ne aldık?** Sorunun kendisini.
- **Programda ne yaptık?** Politika, kart sayısı, araç sayısı, araç kapasitesi ve talep
  düzeyinin tüm kombinasyonlarını koşturup duruştaki değişkenliğin her birine düşen payını
  hesapladık.
- **Ne bulduk?** Değişken talepte duruşu araç sayısı (yaklaşık %33) ve kart sayısı
  (%20–33) belirliyor; aracın taşıyabildiği kutu sayısı %0–6. E-Kanban'da kart ve araç
  birbirini tamamlıyor: ek kart ancak yeterli araç varken işe yarıyor.
- **Hangi açık?** İkinci açık: 2013'ten beri açık duran soruya değişken talep altında
  cevap.
- **Dashboard'da:** Bulgular sayfasındaki çubuk grafik; Ne olursa? sayfasında filo
  değiştirilerek denenebilir.

### Bulgu 6 — Talep şokunda bir ek kart, ek araçtan daha etkili ama stoğa mal oluyor

- **Neden yaptık?** Fabrikada şok olduğunda ilk soru "araç mı ekleyelim, kart mı?" olur.
- **Literatürde ne vardı?** Alnahhal, Ridwan ve Noche (2014): sistemin talep değişimine
  hızlı tepkisi üzerine çalışma eksik. Bocewicz ve arkadaşları (2019, s.51): değişen
  talepte geçiş.
- **Programda ne yaptık?** 8. saatte 2 saatlik %50 talep artışı verdik ve aynı rastgele
  sayılarla şoksuz koşuya göre fazladan duruşu ölçtük.
- **Ne bulduk?** Periyodik sistemde istasyon başına tek ek kart şokun etkisini neredeyse
  siliyor, ama stok yaklaşık %70 artıyor. E-Kanban'da 3 araçtan sonra araç eklemek bir şey
  değiştirmiyor.
- **Dashboard'da:** Bulgular sayfasındaki şok tablosu.

### Bulgu 7 — Neden tersine dönüyor? (mekanizma)

- **Neden yaptık?** "Sonuç kurala bağlı" demek yetmez, hakem "neden?" diye sorar. Benzer
  bir makale (Enns & Rogers 2008) bunu açıklamadığı için az atıf almış.
- **Literatürde ne vardı?** Alnahhal ve arkadaşları (2016, s.707–708): raf ihtiyacı, parça
  gelene kadar geçen süreyle büyür; klasik kanbanda talep bilgisi ancak araç gelince
  iletilir. Ciemnoczolowski ve Bozer (2013, s.570): kart sayısının alt sınırı bir turdaki
  tüketimle büyür. Sugimori (1977, s.562): Toyota talep artınca kart sayısını değil tedarik
  süresini değiştirir.
- **Ne bulduk?** Periyodik sistemde raf "tur aralığı + yol süresi", e-Kanban'da yalnızca
  "yol süresi" kadar süreyi karşılamak zorunda. Bu yüzden eşit raf e-Kanban'ı kayırıyor;
  her politikaya kendi süresine göre raf verilince fark kapanıyor.
- **Dashboard'da:** Politikalar ve kurallar → Politika karşılaştırması, "Eski
  boyutlandırma (V1)" ile "Politika-tutarlı (VDI)" arasında geçiş.

### Bulgu 8 — Sonuçlar sağlam

- **Neden yaptık?** Bazı parametrelerimiz Toyota'nın önerdiği sınırların dışındaydı, model
  tek vardiya çalışıyordu ve mesafe tablosu gerçekçi değildi.
- **Ne yaptık?** Toyota sınırları içinde, 3 vardiyada, ısınma dönemi hariç ve gerçekçi bir
  yerleşimle tekrarladık.
- **Ne bulduk?** Etkinin yönü 52 koşulun 52'sinde aynı. Eski mesafe tablosu, Vojdani ile
  aramızdaki görünür bir çelişkinin de kaynağıymış.
- **Dashboard'da:** Doğrulama sayfası.

---

## 4. Literatür açığımız, tek cümlede

> Üretim kontrolünde sonucun eşitleme tabanına bağlı olduğu bilinmesine karşın, fabrika içi
> malzeme besleme yazını periyodik ve e-Kanban beslemeyi tek bir tampon tabanında (bazen
> açık, çoğunlukla örtük) karşılaştırmaktadır. Bu çalışma dört kuralı yan yana koyarak
> kazananın değiştiğini gösterir, bunu iki politikanın tamponunun farklı süreleri
> karşılamasıyla açıklar, yazındaki iki ters sonucu aynı modelde üretir ve politikalar
> arası duruş–stok eğrisine dayalı bir karşılaştırma önerir.

**İkinci açık:** Ciemnoczolowski ve Bozer'in (2013) açık bıraktığı "duruşta kart sayısı
mı, araç kapasitesi mi?" sorusuna değişken talep altında cevap.

**Hangi dergi?** TR Dizin için yeterli; en düşük riskli hedef Journal of Turkish Operations
Management, ana hedef Endüstri Mühendisliği Dergisi. SCI-E için yayımlanmış bir vakanın
yeniden kurulması gibi eklemeler gerekir; en uygun dergi Journal of Simulation.

---

## 5. Dikkat edilecekler (hocaya da söylenmeli)

- **Fikri biz bulmadık.** Adil karşılaştırma ilkesi üretim kontrolünde biliniyor. Bizim
  katkımız onu bu alana taşımak ve buradaki çelişkiyi açıklamak.
- **Bir bulgu daraldı.** Önceki ayarda Toyota kutularında "üç farklı kazanan" çıkmıştı;
  gerçekçi ayarda iki çıktı. Makaleye yalnızca `docs/makale_tablolari.md`'deki sayılar
  girecek.
- **Bir katkı düştü.** Stoktan türetilen zaman penceresi Lieb'in (2021) doktora tezinde
  zaten var; bunu katkı değil, yöntem olarak ve atıfla yazacağız.
- **Önemsiz çıkan şeyler.** Sevk kuralı ve güvenlik katsayısı α arasında anlamlı fark yok.
- **Temsili ekran.** Dashboard'daki İstasyonlar ekranında stok çubukları temsili, gerçek
  simülasyon çıktısı değil.
- **Sınırlılıklar.** Sentetik veri; tek fabrika düzeni; aracın kutu kapasitesi deneylerde
  hiç dolmadı; kart sayısı tüm istasyonlarda aynı miktarda değiştirildi.

---

## 6. Dosyalar

| Ne | Nerede |
|---|---|
| Dashboard (açılış: Bulgular) | `dashboard.html` |
| Makale tabloları | `docs/makale_tablolari.md` |
| Hazır makale cümleleri | `docs/literatur_boslugu_analizi.md` §5, §8 |
| Derin araştırma raporu | `reports/Hat besleme literatür açığı.md` |
| Proje rehberi | `docs/proje_rehberi.html` |
| Tüm kararlar ve kaynakları | `docs/karar_gunlugu.md` (K01–K110) |
| Şekiller | `docs/figurler/` (ana figür: `sekil7_adalet_kurallari_nihai_toyota.png`; ikinci açık: `sekil9_kart_kapasite.png`) |
