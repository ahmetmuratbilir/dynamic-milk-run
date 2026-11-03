# Akademik Değerlendirme ve Geliştirme Yol Haritası

**Tarih:** 26.10.2026
**Kapsam:** Çalışmanın akademik olgunluk değerlendirmesi, kıymetini artıracak hamleler ve
karar destek arayüzünün (dashboard) geliştirme planı.
**Bağlam:** Makale henüz yazılmamıştır; zaman baskısı yoktur. Bu, temeli sağlamlaştırmak
için elverişli bir durumdur.

---

## BÖLÜM A — AKADEMİK DEĞERLENDİRME

### A.1 Bileşen bazında olgunluk haritası

| Bileşen | Durum | Not |
|---|---|---|
| Karar izlenebilirliği (K01–K91) | 🟢 **Çok güçlü** | 91 karar, kaynaklı; errata disiplini yazında nadir |
| Literatür taraması | 🟢 **Güçlü** | 47 özgün çalışma; sayfa+alıntı standardı |
| Doğrulama & geçerleme | 🟢 **Güçlü** | Solomon, tur-içi tam numaralama, Welch, replikasyon yeterliliği |
| Deney tasarımı | 🟢 **Güçlü** | $2^5$ faktöriyel + ANOVA + Tukey; çoklu karşılaştırma düzeltmeli |
| Tekrarlanabilirlik | 🟢 **Güçlü** | Tek komutla tüm sonuçlar (~6 dk); seed kontrollü |
| Dürüstlük / öz-eleştiri | 🟢 **Çok güçlü** | Kendi sonucunu çürütme; ayrıştırmayla ölçme |
| Özgün katkı | 🟡 **Orta** | Metodolojik; teknik yenilik yok (bkz. K91) |
| Model gerçekçiliği | 🟡 **Orta** | Metrik olmayan mesafe düzeltildi ama koordinat tabanlı değil |
| **Veri** | 🔴 **Zayıf** | **Sentetik; en büyük engel** |
| **Karar destek arayüzü** | 🔴 **Geçersiz** | **v1 verisiyle çalışıyor — yanlış sonuç gösteriyor (Bölüm B)** |
| Optimizasyon derinliği | 🟡 **Orta** | Tur-arası atama optimize edilmiyor (S8) |

### A.2 Akademik kıymetin özü

Çalışmanın değeri **yeni bir yöntem önermesinde değil**, şu üçlüde toplanmaktadır:

1. **Ölçülmüş metodolojik uyarı.** Model kurma kararlarının (tampon boyutlandırma,
   hizmet süresi simetrisi, döngü kapalılığı) etkisi **10+ puan**; politikalar
   arasındaki gerçek fark **≈1 puan**. Yani modelleme kararları politika seçiminden
   daha belirleyicidir. Bu, benzer karşılaştırmalar yapan çalışmalar için uyarıdır.
2. **Literatürce ilan edilmiş boşluğun doldurulması.** Kundu vd. (2019) s.423'ün
   açıkça "gelecek çalışma" dediği *reorder point ↔ periodic review* karşılaştırması.
3. **Yeniden üretilebilir dürüstlük.** Kendi v1 bulgularını çürütüp bunu ayrıştırarak
   belgelemek. Yazında bu tür öz-düzeltme nadirdir ve metodoloji dergilerinde değerlidir.

### A.3 Nereye kadar gider

| Hedef | Yeterlilik | Eksik olan |
|---|---|---|
| Lisans / YL tasarım çalışması | ✅ Fazlasıyla | — |
| **TR Dizin** (End. Müh. Dergisi, JTOM) | ⚠️ Sınırda | **Gerçek veri** |
| SCI-E (Gazi, IJPR) | ❌ Yetersiz | Yeni model/algoritma veya çok-vaka genellemesi |

### A.4 Akademik kıymeti artıracak altı hamle (öncelik sırasıyla)

#### H1 🔴 Gerçek veri — tek vardiya bile yeter
**Etki:** TR Dizin eşiğini aşırır; S1 sınırlılığını kapatır.
**Gerekli:** Bir fabrikadan tek vardiyalık istasyon bazlı tüketim kaydı + mesafe krokisi.
**Hazır:** `config.json → "real"`, `data/real/*.csv` şablonları.
**Not:** Veri bulunamazsa, en azından **gerçek bir fabrika yerleşimi** (koordinatlar)
alınıp sentetik talep onun üzerinde üretilmelidir — bu bile S5/S10'u hafifletir.

#### H2 🔴 Katkıyı kendi modelinin dışına taşı
**Sorun:** Düzeltilen hata kendi v1 modelimizdedir; hakem *"kendi hatasını düzeltmek
katkı mı?"* diyebilir.
**Çözüm:** Vojdani & Drechsler (2022) s.5 kurgusu (iki sistem, *identisches Layout*,
**aynı iki kutulu Kanban**) v2'de yeniden kurulsun; politika-tutarlı boyutlandırmayla
sonucun nasıl değiştiği gösterilsin.
**İş yükü:** ≈ yarım saat (P1/P2 kurulu).
**⚠️ Çerçeveleme:** Çürütme değil, **duyarlılık analizi**. Vojdani'nin kendi bulgusu
(%27 az sefer, %29,39 az yol) taşıma verimliliği üzerinedir ve etkilenmez.

#### H3 🟠 Mesafe matrisini koordinatlardan üret
**Sorun:** Floyd–Warshall geçici çözümdür; matris hâlâ bir yerleşimden türetilmemiştir (S10).
**Çözüm:** İstasyonlara (x, y) koordinatı atanıp dikdörtgensel ölçüyle matris üretilmeli
(Sevim & Görkemli Aykut 2026 s.67 deseni). İstasyon aralığı literatür bandına
(25–53 m) çekilmeli.
**Kazanç:** "Gerçekleşemeyecek bir ağ üzerinde çalışıyorsunuz" itirazı kapanır.

#### H4 🟠 Çok vardiyalı kararlı durum
**Sorun:** Isınma 90 dk ölçüldü; 480 dk'lık vardiyada etkin pencere 390 dk (S2).
**Çözüm:** Temel koşular 1440 dk (3 vardiya) üzerinden raporlansın; tek vardiya
yalnızca karşılaştırma için tutulsun. Motor destekliyor (`sim_sure=1440`).

#### H5 🟠 Tur-arası atamayı optimize et
**Sorun:** Solomon'da sezgisel OR-Tools'tan %102,7 geride; tur-arası atama sevk
kuralıyla belirleniyor, optimize edilmiyor (S8).
**Çözüm:** OR-Tools zaten kurulu. Fabrika senaryosunda bir "üst sınır" referansı olarak
çalıştırılıp sezgiselin açığı raporlanabilir. Sonuçları değiştirmez ama
**metodolojik açığı kapatır**.

#### H6 🟡 α ve C'yi Toyota bandına çek
**Sorun:** Toyota formülü α < %10 ve C ≤ günlük talebin %10'u önerir (K88); projede
α = 0,15 ve S1 için C %11,4'tür.
**Çözüm:** α = 0,10 ile bir duyarlılık koşusu eklenip farkın önemsizliği gösterilsin
(faktöriyel tasarımda α zaten anlamsızdı, p = 0,145).

### A.5 Önerilen sıra ve kazanç

| Sıra | Hamle | İş yükü | Akademik kazanç |
|---|---|---|---|
| 1 | H2 Vojdani duyarlılığı | yarım saat | **Yüksek** — katkı genellenebilirlik kazanır |
| 2 | H4 Çok vardiya | 1 saat | Orta — S2 kapanır |
| 3 | H6 α/C bandı | 1 saat | Düşük–orta — Toyota uyumu |
| 4 | H3 Koordinat tabanlı ağ | yarım gün | Orta–yüksek — S5/S10 kapanır |
| 5 | H5 OR-Tools üst sınırı | yarım gün | Orta — S8 kapanır |
| 6 | **H1 Gerçek veri** | dış bağımlı | **En yüksek** — TR Dizin eşiği |

**Not:** H2–H6'nın tamamı yaklaşık **iki günlük** iştir ve makale yazımından önce
tamamlanabilir. H1 dış bağımlıdır; paralel yürütülmelidir.

---

## BÖLÜM B — KARAR DESTEK ARAYÜZÜ (DASHBOARD)

### B.1 🔴 KRİTİK SORUN: Arayüz geçersiz sonuç gösteriyor

Dashboard'un veri ambarı (`data/dashboard_scenarios.csv/json`, 1920 senaryo) tamamen
**v1 motorundan** üretilmiştir. v2 düzeltmelerinden sonra bu değerler geçerliliğini
yitirmiştir:

| Konfigürasyon | Dashboard (v1) | v2 gerçek değer | Fark |
|---|---:|---:|---:|
| 4 araç, α=0,15, EDD, baz talep | **%24,58** | **%0,18** (konsolidasyonlu) | **24,4 puan** |
| | | %0,00 (anında sevk) | |
| %5 eşiği için filo | 8 araç | **2–3 araç** | 5–6 araç |
| Sevk kuralları | farklı performans | **istatistiksel olarak eşdeğer** | — |

**Sonuç:** Dashboard şu anda tez savunmasında veya sunumda gösterilirse **yanlış bilgi
verir**. Bu, diğer tüm geliştirmelerden önce çözülmelidir.

**Geçici önlem (bugün):** Arayüze görünür bir uyarı bandı eklenmeli —
*"Bu arayüz v1 motoru sonuçlarını göstermektedir; güncel sonuçlar için
`docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md`."*

### B.2 Arayüzün akademik işlevi ne olmalı

Dashboard **tek başına akademik katkı değildir**. Akademik değeri üç yerde doğar:

1. **Tezin "uygulama" bölümü** — tasarım çalışmasının somut çıktısı.
2. **TR Dizin'de "karar destek sistemi" vurgusu** — Endüstri Mühendisliği Dergisi'nin
   ilgi alanına girer.
3. **Bulguların iletişimi** — özellikle ana katkı olan **ayrıştırma** ve
   **politika-tutarlı boyutlandırma**, statik tablodan çok etkileşimli gösterimde anlaşılır.

Bu nedenle arayüz, "güzel görünen bir panel" değil, **makalenin argümanını gösteren bir
kanıt aracı** olarak yeniden tasarlanmalıdır.

### B.3 Geliştirme yol haritası

#### Kademe 1 — Geçerlilik (zorunlu) 🔴

| # | İş | Açıklama |
|---|---|---|
| D1 | **v2 veri ambarını üret** | `src/generate_dashboard_data.py` v2 motoruna bağlanmalı. Yeni ızgara: 3 politika × filo × α × talep × sevk. Mevcut 1920 senaryo yerine ~500 konfigürasyon yeterlidir (replikasyon ortalamalarıyla). |
| D2 | **Belirsizlik göster** | Her değer tek sayı olarak değil, **ortalama ± %95 GA** olarak gösterilmeli. Veri zaten var (`starv_ci95`). Akademik titizlik açısından kritik. |
| D3 | **Sürüm damgası** | Arayüzde motor sürümü, üretim tarihi ve replikasyon sayısı görünmeli. |

#### Kademe 2 — Ana katkıyı görünür kıl 🟠

| # | İş | Neden |
|---|---|---|
| D4 | **Politika karşılaştırma sekmesi (P1/P2/P3)** | Mevcut "Statik vs Dinamik" sekmesi ikili; üç politikaya genişletilmeli. Her politikanın **kendi kart sayısı** gösterilmeli — ana katkı budur. |
| D5 | **Ayrıştırma (ablation) paneli** | v1 → v2 adımlarının duruşa katkısı interaktif gösterilsin. Kullanıcı adımları açıp kapatabilsin: *"hizmet süresi simetrisini kapatırsam ne olur?"* Bu, makalenin ana argümanının en güçlü görselidir. |
| D6 | **Pareto cephesi (interaktif)** | WIP × duruş düzlemi; politika filtreli; nokta seçilince konfigürasyon ayrıntısı. Şekil 1'in etkileşimli hâli. |

#### Kademe 3 — Akademik tamlık 🟡

| # | İş | Neden |
|---|---|---|
| D7 | **Doğrulama sekmesi** | Solomon sapmaları, Welch ısınma eğrisi, replikasyon yeterliliği. Savunmada "modeliniz doğru mu?" sorusunun hazır cevabı. |
| D8 | **Senaryo karşılaştırıcı** | İki konfigürasyon yan yana; fark sütunu. |
| D9 | **Gerçek veri modu** | `config.json → "real"` seçildiğinde arayüz gerçek veriyle çalışsın (H1 ile birlikte anlamlı). |

### B.4 Teknik yaklaşım

**Mevcut mimari korunmalıdır.** Gömülü JSON + vanilla JS + tek dosya (`dashboard.html`)
yaklaşımı çift tıkla çalışır, sunucu gerektirmez ve savunma ortamı için idealdir.
Yeniden yazmaya gerek yoktur; **veri katmanı yenilenmeli**, iki yeni sekme eklenmelidir.

| Konu | Karar |
|---|---|
| Veri boyutu | v1'de 1920 senaryo / 532 KB. v2'de ~500 konfigürasyon yeterli → daha küçük |
| Grafik kütüphanesi | Mevcut yapı korunmalı; makale figürleriyle **aynı renk paleti** kullanılmalı (mavi/turuncu/aqua — CVD doğrulanmış) |
| Üretim | `src/generate_dashboard_data.py` yeniden yazılıp `tum_analizleri_calistir.py`'ye adım olarak eklenmeli (tekrarlanabilirlik) |
| Doğrulama | `node --check` disiplini sürdürülmeli |

### B.5 Tahmini iş yükü

| Kademe | İş yükü | Çıktı |
|---|---|---|
| Kademe 1 (D1–D3) | ≈ yarım gün | Arayüz **geçerli** hâle gelir |
| Kademe 2 (D4–D6) | ≈ 1 gün | Arayüz **ana katkıyı gösterir** |
| Kademe 3 (D7–D9) | ≈ 1 gün | Arayüz **savunmaya tam hazır** |

---

## BÖLÜM C — BİRLEŞİK ÖNCELİK SIRASI

Makale yazımına başlamadan önce önerilen sıra:

| # | İş | Grup | İş yükü |
|---|---|---|---|
| 1 | **Dashboard v2 verisi + uyarı bandı** | B / Kademe 1 | yarım gün |
| 2 | **H2 Vojdani duyarlılık analizi** | A | yarım saat |
| 3 | H4 Çok vardiyalı kararlı durum | A | 1 saat |
| 4 | H6 α/C Toyota bandı duyarlılığı | A | 1 saat |
| 5 | H3 Koordinat tabanlı mesafe ağı | A | yarım gün |
| 6 | Dashboard Kademe 2 (ana katkı panelleri) | B | 1 gün |
| 7 | H5 OR-Tools üst sınır referansı | A | yarım gün |
| 8 | Dashboard Kademe 3 | B | 1 gün |
| ∞ | **H1 Gerçek veri** (paralel, dış bağımlı) | A | — |

**Toplam:** yaklaşık **4–5 günlük** iş. Bu tamamlandığında çalışma, gerçek veri gelmese
bile TR Dizin'e gönderilebilir olgunluğa yaklaşır; gerçek veri gelirse eşiği rahatlıkla
aşar.

---

*İlgili belgeler: `literatur_boslugu_analizi.md` (Bölüm 10 — katkı gücü),
`karar_gunlugu.md` (K86–K91), `hafta14_literatur_denetimi_ve_revizyon_raporu.md`.*
