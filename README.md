# Dinamik Milk-Run ve E-Kanban Karar Destek Sistemi

Fabrika içi malzeme beslemede iki ikmal politikasını karşılaştıran bir benzetim (simülasyon) çalışması:
**periyodik milk-run** (tren sabit aralıkla tura çıkar) ve **olay tabanlı e-Kanban** (stok eşiğe
düşünce sinyal gider, tren çağrılır). Proje bir Python benzetim motoru, analiz betikleri, bir
karar destek arayüzü (dashboard) ve makale hazırlık belgelerinden oluşur.

Endüstri Mühendisliği tasarım/tez çalışması · Sentetik veri · Python 3.11 · Hedef: TR Dizin
(JTOM, Endüstri Mühendisliği Dergisi)

> **Tek cümlede:** Bu iki politikayı karşılaştırırken kazananı politika değil, **karşılaştırmanın
> nasıl eşitlendiği** ve **araç kapasitesi rejimi** belirliyor. Yazındaki iki ters sonucu
> (Bae vd. 2016: milk-run önde; Vojdani & Drechsler 2022: dijital önde) aynı modelde ürettik.

---

## İçindekiler

1. [Bu depoya ilk kez bakıyorsanız: okuma sırası](#1-bu-depoya-ilk-kez-bakıyorsanız-okuma-sırası)
2. [Problem ve araştırma açığı](#2-problem-ve-araştırma-açığı)
3. [Sistem ve politikalar](#3-sistem-ve-politikalar)
4. [Yöntem: neyi nasıl yaptık](#4-yöntem-neyi-nasıl-yaptık)
5. [Bulgular](#5-bulgular)
6. [Sağlamlık ve doğrulama](#6-sağlamlık-ve-doğrulama)
7. [Sınırlılıklar ve açık işler](#7-sınırlılıklar-ve-açık-işler)
8. [Kurulum ve çalıştırma](#8-kurulum-ve-çalıştırma)
9. [Dashboard (karar destek arayüzü)](#9-dashboard-karar-destek-arayüzü)
10. [Depo düzeni](#10-depo-düzeni)
11. [Makaleler ve kaynaklara erişim](#11-makaleler-ve-kaynaklara-erişim)
12. [Kısaltmalar](#12-kısaltmalar)

---

## 1. Bu depoya ilk kez bakıyorsanız: okuma sırası

Bir insan ya da yapay zekâ ajanı projeyi baştan anlamak istiyorsa bu sırayla okusun:

| Sıra | Belge | Ne verir |
|---|---|---|
| 1 | `README.md` (bu dosya) | Bütün resim |
| 2 | `docs/basit_anlatim.md` | Projenin sade dille anlatımı, tüm sayıların okunuşu, kısaltma sözlüğü |
| 3 | `docs/hocaya_anlatim.md` | Neden, hangi makale, ne yaptık, hangi açıklar, olası hakem/hoca soruları ve cevapları |
| 4 | `docs/makale_tablolari.md` | **Makaleye girecek sayıların tek kaynağı** (nihai ayar) |
| 5 | `docs/literatur_boslugu_analizi.md` | Literatür açığı, katkı maddeleri, rakip çalışmalar, hazır cümleler |
| 6 | `docs/karar_gunlugu.md` | K01–K110: her modelleme kararının kaynağı (sayfa numarasıyla) ve gerekçesi |
| 7 | `reports/*.md` | Derin literatür araştırmaları (açık doğrulaması; 2023–2026 yeni kaynaklar ve eklenebilecek özellikler) |
| 8 | `docs/hafta1_referans_listesi.md`, `docs/master_makale_katalogu.md` | Kaynakça ve makale kataloğu |

> **Önemli kural:** Makaledeki ve sunumdaki her sayı yalnızca `docs/makale_tablolari.md`'den
> alınmalıdır. Haftalık raporlardaki (hafta1…hafta14) eski sayılar farklı ayarlarla üretildi.

Sunum slaytları: `docs/sunum/` · Proje rehberi (ekranlar, eksikler): `docs/proje_rehberi.html`.

---

## 2. Problem ve araştırma açığı

**Problem.** Montaj hattındaki istasyonlara parça küçük bir çekici trenle (milk-run, tugger train)
taşınır. Kutu boşalırsa istasyon durur (**duruş**, starvation). Fazla kutu ise hat yanında
stok (**WIP**) biriktirir. Tren ya sabit aralıkla tur atar (periyodik) ya da stok eşiğe düşünce
çağrılır (e-Kanban). Hangisi daha iyi?

**Yazındaki çelişki.**
- Bae, Evans & Summers (2016, WSC, s.2865): tek trenle talep üzerine sistemde duruş milk-run'ın yaklaşık 4 katı → **milk-run önde**.
- Vojdani & Drechsler (2022): **dijital önde**.
- Alnahhal vd. (2016): sonuç **kapasiteye bağlı**.

**Açık 1 (ana açık).** Üretim kontrolünde karşılaştırmanın neye göre eşitlendiğinin sonucu
değiştirdiği biliniyor (Bonvik vd. 1997; Geraghty & Heavey 2005; Enns & Rogers 2008). Hat
besleme yazınında ise her çalışma **tek bir eşitleme tabanı** kullanıyor; bu taban bazen açık,
çoğunlukla örtük. Politikalar arası duruş–stok eğrisi çizen bir çalışma da yok. Kundu vd.
(2019, s.423) bu iki politika ailesinin karşılaştırılmasını açıkça "gelecek çalışma" olarak bırakıyor.

**Açık 2.** Ciemnoczolowski & Bozer (2013, IJPR, s.579): kart sayısı ile araç kapasitesinin
duruşa göreli katkısı nicelendirilmeli. Biz bunu stokastik talep altında η² ayrıştırmasıyla yaptık.

**Konumlandırma.** "Fikri biz bulduk" demiyoruz. Üretim kontrolünde bilinen adil karşılaştırma
ilkesini hat besleme alanına taşıyoruz ve alandaki çelişkiyi iki kaynağa bağlıyoruz: araç
kapasitesi rejimi ve eşitleme kuralı. 2023–2026 taramasında bu iddiayı çürüten bir çalışma
bulunmadı. En yakın çalışma Tappia vd. 2025 (IJCIM); ayrıştığımız noktalar
`reports/Hat besleme yeni kaynaklar ve özellikler.md` dosyasında.

---

## 3. Sistem ve politikalar

| Öğe | Değer | Karar |
|---|---|---|
| Fabrika | 4 hat, 24 istasyon, 1 depo (süpermarket) | K01, K02 |
| Araç | 25 kutu kapasiteli çekici tren, 10 km/sa; filo 1–8 araç (ana senaryo 3–4) | K04, K12 |
| Tedarik süresi / güvenlik katsayısı | 45 dk / α = 0,15 (Toyota bandında α < 0,10) | K07, K08, K95 |
| Kutu kapasitesi | 15 veya 20 adet ("mevcut"); Toyota kutuları: günlük talebin ≤ %10'u | K09, K95 |
| Mesafe | Koordinat ağı, dik açılı (rectilinear) mesafe, durak aralığı ≈ 20,7 m | K100 |
| Ufuk / ısınma | **1440 dk** (3 vardiya) / **90 dk** ısınma, göstergeler ısınma sonrası | K78, K99, K105 |
| Tekrar | 12 replikasyon, ortak rastgele sayılar (CRN) | K105 |

### Politikalar

| | Tanım | Dayanak |
|---|---|---|
| **P1** | Sabit takt, sabit miktar | Klenk vd. 2012 |
| **P2** · geleneksel | Sabit takt (ana senaryo T = 60 dk), Kanban miktarı (1:1 boş kutu değişimi) | Simić 2020; Vojdani 2022 |
| **P3** · dijital | Olay tabanlı e-Kanban: stok yeniden sipariş noktasına (ROP) düşünce sinyal; ANINDA veya KONSOLİDASYON sevk | Facchini 2022 |

### Kart sayısı (boyutlandırma)

- **Toyota formülü** (Sugimori vd. 1977, s.561): N ≈ D · L · (1 + α) / C
- **Politika-tutarlı (VDI):** "+1 değişim kutusu" (VDI 5586 Blatt 2, 2022; formül Urru vd. 2018, s.406'dan aktarılıyor)
  - P3: N = 1 + ⌈ROP / C⌉
  - P1/P2: N = 1 + ⌈D · T · (1 + α) / C⌉. Her politika kendi çevrim süresiyle boyutlandırılır (K65).
- **V1 (eski):** N = ⌈ROP / C⌉ · **İki kutu:** her istasyona 2 kart.

---

## 4. Yöntem: neyi nasıl yaptık

1. **Ayrık olaylı benzetim motoru** (`src/v2_entegre_simulasyon.py`): tek olay döngüsü, kapalı döngü (sinyaller gerçek stoktan doğar), zaman pencereli araç rotalama (VRP-RTW) + 2-opt, P1/P2/P3.
2. **Model düzeltme ve ayrıştırma (v1 → v2):** İlk sürümdeki üç yapısal hata tek tek düzeltildi, her birinin duruşa etkisi ayrı ölçüldü. Ayrıntı: `docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md` §4.1.
3. **Dört eşitleme kuralı** (`src/v2_adalet_kurallari.py`): kart sayısı N = max(1, N_VDI + k) taranır, duruş–stok eğrisi çizilir. Dört kural bu eğri üzerinde dört noktadır:
   - **A · Eşit kart:** iki sisteme aynı kart sayısı (Vojdani 2022).
   - **B · Politika-tutarlı:** her sistem kendi formülüyle (VDI 5586 / Urru 2018).
   - **C · Eşit hizmet:** iki sistemde de duruş ≤ %1; kazanan daha az stoklu olan (Alnahhal & Noche 2015).
   - **D · Eşit WIP:** aynı stokta daha az duran kazanır.
4. **Pareto analizi:** duruş × WIP cephesi.
5. **Yazın kurgularının yeniden üretimi:** tek araç (Bae) ve 3 araç ile eşit kart (Vojdani).
6. **Faktöriyel deney + η²** (`src/v2_kart_kapasite_ayristirma.py`, K109): politika × kart × araç sayısı × araç kapasitesi (Q) × talep; ayrıca geçici talep şoku (480. dk'da 120 dk boyunca +%50) ve şok sonrası toparlanma.
7. **Sağlamlık:** Toyota bandı (K95), uyarlanan ROP (K98), 480/1440 dk ve ısınma dahil/hariç (K99), koordinat ağı (K100), OR-Tools çevrimdışı rota referansı (K101).
8. **Makale tabloları:** nihai ayarla tek betikten (`src/v2_makale_tablolari.py`, K105).

Eksi işaretli fark (Δ duruş = dijital − geleneksel, puan) **dijital lehine** demektir.

---

## 5. Bulgular

Sayılar `docs/makale_tablolari.md`'den alındı (nihai ayar).

### Bulgu 1 · Önce model düzeltildi (K65–K72)
v1 modeli 4 araçta %24,6 duruş gösteriyor ve "statik sistem üstün" diyordu. Hizmet süresi
asimetrisi tek başına **10,3 puan**, eksik tampon (+1 kutu yokluğu) **3,9 puan** oynatıyordu.
Politikalar arasındaki gerçek fark ise yaklaşık 1 puandı. Yani yanlış kurulmuş bir model,
politika seçiminden daha çok şey değiştiriyor.

### Bulgu 2 · Kazanan, eşitleme kuralına göre değişiyor (ana bulgu, K97, K105)

Toyota kutuları, Δ duruş (puan, ± %95 GA):

| Kural | Baz talep | Talep şoku +%50 | Kazanan |
|---|---:|---:|---|
| A · Eşit kart | −11,27 ± 0,41 | −15,96 ± 0,60 | Dijital |
| B · Politika-tutarlı | +0,11 ± 0,04 | +1,97 ± 0,61 | **Geleneksel** |
| C · Eşit hizmet | +0,12 ± 0,06 (stok −%36) | +0,40 ± 0,05 (stok −%11) | Dijital (stokta) |
| D · Eşit WIP | −7,69 ± 0,29 | −12,76 ± 0,62 | Dijital |

Tüm koşullarda fark **−17,3 ile +2,0 puan** arasında. Mevcut (büyük) kutularda kazanan hep
dijital, ama fark 0,03 ile 17,3 puan arasında değişiyor.

### Bulgu 3 · Yazındaki iki ters sonuç aynı modelde (K106, K109)
- **Tek araç (Bae'nin kurgusu):** geleneksel %7,5–12,5, dijital %17,7–18,4 duruş → milk-run önde.
- **3 araç, eşit kart (Vojdani'nin kurgusu):** dijital %0,12, geleneksel %2,54 → dijital önde.
- Çelişkinin iki kaynağı: **kapasite rejimi** ve **eşitleme kuralı**.

### Bulgu 4 · Mekanizma (K103, K104, K108)
Periyodik sistemde tampon "çevrim + teslim süresini", e-Kanban'da yalnızca "teslim süresini"
karşılamak zorunda (Alnahhal vd. 2016, s.707–708; Ciemnoczolowski & Bozer 2013, s.570). Eşit kart
bu yüzden e-Kanban'ı kayırıyor. Politika-tutarlı formül ise geleneksel sisteme fazladan kart veriyor.

### Bulgu 5 · Duruşu araç sayısı ve kart sayısı belirliyor (Açık 2, K109)
Duruş varyansındaki pay (η²): **araç sayısı ≈ 0,33**, **kart sayısı 0,20–0,33**, **araç kapasitesi
0–0,06**. Uyarı: deneyde araç kapasitesi hiç bağlayıcı olmadı (doluluk ≤ %57). Dar kapasiteyle
tekrar önerilir (bkz. §7).

### Bulgu 6 · Talep şokunda ek kart ek araçtan etkili ama stoğa mal oluyor (K109)
İstasyon başına +1 kart: fazladan duruş **140 → 1 istasyon-dakika**, ama stok **+%69**.
Dijital sistemde 3 araçtan sonra araç eklemek bir şey değiştirmiyor.

---

## 6. Sağlamlık ve doğrulama

| Doğrulama | Sonuç |
|---|---|
| Sağlamlık (K95, K99, K100, K105) | Boyutlandırma kayması (fark_B − fark_A) **36 bağımsız koşulun 36'sında** pozitif (52 test hücresi). Örnek (Toyota, şok, α = 0,05): A −5,19 → B +12,37, kayma +17,56 puan |
| Solomon VRPTW (6 örnek × 2 boyut) | En yakın komşu, OR-Tools'tan %102,7 daha uzun |
| Fabrika içi tur-içi optimallik (400 küme, tam numaralama) | NN + 2-opt sapması %0,62 |
| Isınma süresi (Welch, 20 replikasyon) | 90 dk |
| Replikasyon yeterliliği | Mutlak ölçütle (±0,05 puan) n = 9; makalede 12 |
| Sevk kuralları (ANOVA + Tukey) | Dört kural eşdeğer (p = 0,9997 / 0,3415); "önemli karar" diye sunulmamalı |
| Rotalama referansı (K101) | OR-Tools çevrimdışı tam bilgi referansı daha kısa yol, ama daha çok gecikme (kanıtlanmış alt sınır değil) |

---

## 7. Sınırlılıklar ve açık işler

**Sınırlılıklar** (makalede yazılmalı):
- Veri sentetik; tek fabrika düzeni.
- VDI 5586 ücretli. Önizlemesiyle künye ve sembol gösterimi doğrulandı; "+1" formülü Urru vd. 2018 üzerinden aktarılıyor.
- Araç kapasitesi deneylerde bağlayıcı olmadı. η² faktöriyel deneyi 4 tekrarla koşuldu.
- Kart sayısı tüm istasyonlarda aynı miktarda değiştirildi; istasyon başına optimize edilmedi.
- Eşit hizmet kuralı zaman bazlı. Sevk kuralı ve α'nın etkisi anlamsız.
- Motor varsayılanları eski ayarla çalışır (ısınma dahil gösterge, eski mesafe matrisi). Makale sayıları `--nihai` / `v2_makale_tablolari` ile üretilir.
- `src/tum_analizleri_calistir.py` henüz uçtan uca tek seferde çalıştırılmadı; betikler ayrı ayrı çalıştırıldı.

**Önerilen sonraki adımlar** (öncelik sırasıyla, `reports/Hat besleme yeni kaynaklar ve özellikler.md`):
1. İkinci açığı dar araç kapasitesiyle (araç başına 5–10 kutu) ve daha çok tekrarla yinelemek.
2. Her politikayı kendi en iyi kart ayarında karşılaştırmak (Bonvik 1997 tarzı; beşinci kural). `n_ozel` parametresi bunun için hazır.
3. Araç arızası / geç kalkış (Zhou & Zhu 2020; Sevim & Görkemli Aykut 2026; Korytkowski 2016).
4. e-Kanban sinyal gecikmesi/kaybı (Facchini 2022).
5. Yayımlanmış bir vakanın yeniden üretimi (ör. Korytkowski 10 istasyon); gerçek veriyle doğrulama.
6. Eksik atıflar: Limère 2012, Golz 2012, Sali 2015, Faccio 2014, Caputo & Pelagagge 2011 (besleme *biçimi* karşılaştırmaları; biz ikmal *tetikleyicisini* karşılaştırıyoruz), Boysen vd. 2015, Kilic & Durmusoglu 2015, Hopp & Spearman 2004, Sargent 2013, Hoad vd. 2010, Tappia vd. 2025.
7. Vojdani & Drechsler 2022'nin DOI/URN'si doğrulanmalı.

---

## 8. Kurulum ve çalıştırma

```bash
python -m pip install -r requirements.txt

# Makale tabloları (nihai ayar, ≈4 dk)
python -X utf8 -m src.v2_makale_tablolari

# Tek tek analizler (örnekler)
python -X utf8 -m src.v2_adalet_kurallari --kutu toyota
python -X utf8 -m src.v2_kart_kapasite_ayristirma

# Tüm analizler (~15–30 dk; henüz uçtan uca denenmedi)
python -X utf8 -m src.tum_analizleri_calistir
python -X utf8 -m src.tum_analizleri_calistir --hizli

# Dashboard verisi ve tek dosyalık arayüz
python -X utf8 -m src.generate_dashboard_data_v2 --nihai
python -X utf8 make_standalone.py
```

Çıktılar: `data/synthetic/v2_*.csv`, `docs/figurler/*.png`, `data/dashboard_scenarios_v2.json`, `dashboard.html`.

> **Windows notu.** Konsol cp1254 kullanır; Türkçe karakterler için `python -X utf8 -m ...` biçiminde çalıştırın.

**Gerçek veriye geçiş.** `data/config.json` içindeki `data_source` değerini `"real"` yapın ve
`data/real/` altındaki altı CSV'yi doldurun (başlıklar hazır). Tüm okuma `src/data_loader.py`
üzerinden yapılır.

---

## 9. Dashboard (karar destek arayüzü)

`dashboard.html` dosyasını tarayıcıda açın. Tek dosyadır ve veri içine gömülüdür; sunucu gerekmez.
Kaynakları `index.html`, `app.js` ve `style.css`'tir.

| Sekme | Ne gösterir |
|---|---|
| **Bulgular** (açılış) | 8 bulgu kartı: neden, literatür, ne yaptık, ne bulduk, hangi açık. "Uygulamada göster" düğmesiyle ilgili grafiğe gider. Altta "dikkat edilmesi gerekenler" kutusu var |
| **Özet** | Baz senaryonun tek bakışta özeti |
| **Politikalar ve kurallar** | P1/P2/P3 tablosu (filo, talep, boyutlandırma seçilir), dört eşitleme kuralı grafiği, Pareto cephesi, v1 → v2 ayrıştırma |
| **Ne olursa?** | Önceden hesaplanmış 1920 senaryoda parametre gezintisi |
| **Doğrulama** | Welch ısınma, replikasyon serisi, karşılaştırıcı |
| Ek: İstasyonlar, Veri girişi | İstasyon görünümü (stok çubukları temsili, simülasyon çıktısı değil) ve veri şablonu |

Tablo okuma: P2 = geleneksel, P3 = dijital. Duruş ve WIP düşük, doluluk yüksek olan iyidir.

---

## 10. Depo düzeni

```
src/
  v2_entegre_simulasyon.py        Kanonik motor (v2): P1/P2/P3, VRP-RTW, 2-opt, şok, KOORDINAT mesafe
  v2_makale_tablolari.py          Nihai ayarla makale tabloları (K105)
  v2_adalet_kurallari.py          Dört eşitleme kuralı (K97; --kutu toyota)
  v2_kart_kapasite_ayristirma.py  η² ayrıştırma, şok toparlanma, tek araç (K109)
  v2_boyutlandirma_duyarliligi.py Vojdani tasarımı ↔ politika-tutarlı tampon (K93)
  v2_toyota_bandi_duyarliligi.py  Toyota α ve kutu bandı (K95)
  v2_uyarlanan_rop.py             Uyarlanan ROP (K98)
  v2_cok_vardiya.py               480/1440 dk, ısınma dahil/hariç (K99)
  v2_koordinat_agi.py             Koordinat tabanlı mesafe ağı (K100)
  v2_ortools_referansi.py         Çevrimdışı rotalama referansı (K101)
  v2_dogrulama_ve_kalibrasyon.py  Tur-içi optimallik, Welch, replikasyon, ayrıştırma
  v2_pareto_ve_figurler.py        Politika ızgarası, Pareto, figürler
  v2_deney_tasarimi.py            2^5 faktöriyel, ANOVA, Tukey
  generate_dashboard_data_v2.py   Dashboard veri ambarı (--nihai)
  tum_analizleri_calistir.py      Hepsini sırayla çalıştırır
  generate_synthetic_data.py      Sentetik veri (seed = 42)
  data_loader.py                  synthetic ↔ real veri katmanı
  ekanban_signal.py, vrptw_solver.py, …  v1 motoru (Hafta 4–13 raporlarının sayıları; değiştirilmedi)
data/
  config.json, synthetic/, real/, dashboard_scenarios_v2.json
docs/
  basit_anlatim.md / .html        Sade anlatım + kısaltma sözlüğü
  hocaya_anlatim.md               Danışmana kapsamlı anlatım, olası sorular
  makale_tablolari.md             ← makale sayılarının tek kaynağı
  literatur_boslugu_analizi.md    Açık, katkılar, rakip yazın, hazır cümleler
  karar_gunlugu.md                K01–K110
  hafta1_referans_listesi.md      Kaynakça [1]–[45], doğrulama durumlarıyla
  master_makale_katalogu.md       Makale kataloğu (ek kaynaklar: E1–E13; E14–E19 için bkz. referans listesi ve reports/)
  tez_bilgi_rehberi.md            Akademik master doküman (IMRaD)
  proje_rehberi.html              Ekran rehberi, eksikler, kritik sorular
  sunum/                          Kısa sunum slaytları
  hafta*_*.md                     Haftalık raporlar (eski ayarlar; errata notlu)
  figurler/                       Makale figürleri (PNG)
  papers/                         Makale PDF'leri ve metinleri (yerelde; git'e eklenmez)
reports/, research_notes/         Derin literatür araştırmaları ve notları
dashboard.html, index.html, app.js, style.css, make_standalone.py   Arayüz
```

**İki motor bilinçli olarak tutuluyor:** v1 (açık döngü, Hafta 4–13 raporlarını üretir, değiştirilmedi)
ve v2 (kapalı döngü, güncel). Yeni analizler v2 ile yapılmalı.

---

## 11. Makaleler ve kaynaklara erişim

Makale PDF'leri ve tam metinleri **telif hakkı nedeniyle bu depoda yoktur** (`.gitignore`:
`docs/papers/**/*.pdf`, `docs/papers/ek_kaynaklar/` ve çıkarılmış metinler). Depoda yalnızca katalog
ve kaynakça bulunur: `docs/master_makale_katalogu.md`, `docs/hafta1_referans_listesi.md`. Belgelerdeki
sayfa numaralı atıflar bu yerel PDF'lerden okunmuştur.

> **Makalelere erişemiyorsanız depo sahibinden isteyin** (GitHub: `ahmetmuratbilir`; depoda bir
> issue açabilirsiniz). Yerel arşiv tek bir zip dosyasında tutuluyor (61 PDF ve çıkarılmış metinler,
> içerik listesi `ICINDEKILER.md` ile birlikte).

---

## 12. Kısaltmalar

| Kısaltma | Anlamı |
|---|---|
| P1 / P2 / P3 | Sabit takt + sabit miktar / sabit takt + Kanban miktarı (geleneksel) / olay tabanlı e-Kanban (dijital) |
| Kanban, e-Kanban | Kutuya bağlı sipariş kartı / elektronik hali |
| ROP | Reorder Point, yeniden sipariş noktası |
| WIP | Work In Process, hat yanı stok |
| N, C, T, Q, D, α | Kart sayısı, kutu kapasitesi, takt, araç kapasitesi, talep, emniyet payı |
| VDI 5586 | Alman Mühendisler Birliği'nin fabrika içi çekici tren standardı (Blatt 2: Planlama ve boyutlandırma, 2022-07) |
| VRP(-TW / -RTW) | Araç rotalama problemi (zaman pencereli) |
| CRN | Common Random Numbers, ortak rastgele sayılar |
| η² | Eta-kare: bir faktörün sonuç varyansındaki payı |
| GA | %95 güven aralığı |
| Δ duruş | Dijital − geleneksel duruş farkı (puan); eksi dijital lehine |
| Kayma | fark_B − fark_A: kural A'dan B'ye geçince sonucun yer değiştirmesi |
| JTOM, TR Dizin, SCI-E | Journal of Turkish Operations Management; ulusal dizin; uluslararası atıf dizini |
