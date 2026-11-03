# Karar Günlüğü — Dinamik Milk-Run & E-Kanban Karar Destek Sistemi

> **Amaç:** Bu dosya projedeki her teknik kararın nereden geldiğini, neden yapıldığını
> ve hangi makalenin kaçıncı satırından/sayfasından alındığını kayıt altında tutar.
> Tezin Metodoloji bölümü bu dosyaya dayanacak.
>
> **Format:** Her karar → Karar No | Konu | Değer | Kaynak | Gerekçe | Tarih
>
> **Kural:** Uydurulan, tahmin edilen veya "makul görünen" değerler buraya
> yazılmaz. Her satırın bir makaleden ya da kullanıcı onayından kaynağı olmalı.

---

## BÖLÜM 1 — SİSTEM YAPISI KARARLARI

### K01 — Hat Sayısı: 4
- **Değer:** 4 üretim hattı
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Menanno et al. (2023) → 11 hat; Pekarcikova (2021) → 1 hat. Bizim seçimimiz aralıkta (1–38).
- **Gerekçe:** Orta büyüklükte otomotiv montaj fabrikası senaryosunu temsil ediyor.
- **Dosya:** `data/synthetic/stations.csv`

### K02 — İstasyon Sayısı: 24 (hat başına 6)
- **Değer:** 24 istasyon
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Simić (2020) s.8 → 5 durak; Urru et al. (2018) L74-75 → 5 durak; Vojdani & Drechsler (2022) L644 → 15 istasyon; Sevim & Görkemli Aykut (2025) L712 → 10 istasyon; Zhou & Wen (2024) s.12 → 4–100 test senaryoları
- **Gerekçe:** Aralıkta (5–100). 4 hat × 6 istasyon simetrik ve yönetilebilir.
- **Dosya:** `data/synthetic/stations.csv`

### K03 — Araç Sayısı: 2
- **Değer:** 2 milk-run aracı (A1, A2)
- **Kaynak:** Mühendislik Varsayımı (Kullanıcı Onayı 29.07.2026) — *⚠️ Literatür atıfı kaldırıldı (önceki atıf hatalıydı).*
- **Tür:** **MÜHENDİSLİK VARSAYIMI** (Literatür kaynaklı değil)
- **Gerekçe:** 4 montaj hattı ve 24 istasyonlu sentetik fabrika yerleşiminde, her 2 hatta 1 araç düşecek şekilde dengeli ve yönetilebilir bir küçük-orta ölçek operasyonel varsayımı olarak seçilmiştir.
- **Dosya:** `data/synthetic/vehicles.csv`

### K04 — Araç Kapasitesi: 25 kutu
- **Değer:** 25 kutu / araç
- **Kaynak:** Mühendislik Varsayımı (Kullanıcı Onayı 29.07.2026) — *⚠️ Literatür atıfı kaldırıldı (Menanno 2023 s.15 atıfı hatalıydı, Menanno metnindeki gerçek değer $Q_{min} = 45$ birimdir).*
- **Tür:** **MÜHENDİSLİK VARSAYIMI** (Literatür kaynaklı değil)
- **Gerekçe:** İstasyon başına talep ($N \times C \approx 15-20$ kutu) ile uyumlu olacak şekilde, tek bir aracın tek bir turda 1-2 istasyonun siparişini taşıyabileceği fiziksel olarak makul bir çekici-römork taşıma kapasitesi olarak belirlenmiştir.
- **Dosya:** `data/synthetic/vehicles.csv`

### K05 — Simülasyon Süresi: 480 dakika (1 vardiya)
- **Değer:** 480 dk
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Simić (2020) s.11 → 600 dk; Pekarcikova (2021) s.3 → 12 saat; Vojdani (2022) L765 → 7 gün; Sevim (2025) L765 → 7200 dk
- **Gerekçe:** Tek vardiya analizi; en sık kullanılan standart birim. Genişletmek gerekirse 2-3 vardiyaya çıkarılabilir.
- **Dosya:** `src/generate_synthetic_data.py`

---

## BÖLÜM 2 — DİNAMİK KANBAN PARAMETRELERİ

### K06 — Kanban Formülü
- **Değer:** $N = \lceil (D \times LT \times (1+\alpha)) / C \rceil$
- **Kaynak:** Orijinal proje tanımı (kullanıcının hafta başındaki prompt'u)
- **Literatür referansı:** Elloumi et al. (2025) → adaptif Kanban kart sayısı; Simić (2020) s.10 → malzemeye göre Kanban kart sayısı tablosu
- **Gerekçe:** Endüstri mühendisliğinde standart Kanban boyutlandırma formülü.
- **Dosya:** `src/generate_synthetic_data.py` (istasyon başına N hesabı)

### K07 — Lead Time (LT): 45 dakika
- **Değer:** 45 dk
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:**
  - Simić (2020) s.10 → 20 dk (replenishment frequency)
  - Klenk et al. (2012) s.12 → 34–47 dk (konsepte göre) ← **en yakın kaynak**
  - Facchini et al. (2022) L476-477 → maks. 25 dk teslimat hedefi
- **Gerekçe:** Klenk (2012)'nin 34–47 dk aralığının ortası. Literatürle uyumlu.
- **Dosya:** `src/generate_synthetic_data.py`

### K08 — Güvenlik Katsayısı (α): 0.15
- **Değer:** α = 0.15 (%15)
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Klenk et al. (2012) s.12 → %30 tampon süresi kulllanmış. *Bizim %15 daha temkinli ama aynı mantıkla.*
- **Dikkat notu:** α bu formülde **istatistiksel z-değeri değil**, basit bir tampon oranıdır. Savunmada "service level" değil "güvenlik tamponu" olarak tanımlanmalı.
- **Gerekçe:** Tek kaynakta %30 var, %15 savunulabilir çünkü: (1) sistemi dinamik güncelleme yapıyor zaten, (2) What-if S3 senaryosunda α=%30 ile karşılaştırılacak.
- **Dosya:** `src/generate_synthetic_data.py`

### K09 — Kutu Kapasitesi (C): 15 veya 20 adet
- **Değer:** μ ≤ 15 adet/sa → C = 15 kutu; μ > 15 adet/sa → C = 20 kutu
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Pekarcikova (2021) s.7 → min 10, max 50 adet; Zhou & Wen (2024) s.12 → < 6; Simić (2020) s.9 → 2500 (farklı ölçek)
- **Gerekçe:** Otomotiv montaj hattı için KLT (Kleinladungsträger) kutu standardı. Tüketim hızı yüksek istasyonlara daha büyük kutu.
- **Dosya:** `data/synthetic/stations.csv` (sütun: kutu_kapasitesi)

### K10 — Tüketim Hızı Dağılımı: Normal N(μ, 0.20μ)
- **Değer:** Standart sapma = μ'nun %20'si
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Sevim & Görkemli Aykut (2025) L768-783 → üstel dağılım; Zhou & Zhu (2020) L1524-1525 → %45–50 olasılıklı Bernoulli. Normal dağılım otomotiv montaj senaryolarında yaygın.
- **Gerekçe:** Normal dağılım, %20 CV (coefficient of variation) otomotiv montaj hatları için gerçekçi ve savunulabilir.
- **Dosya:** `src/generate_synthetic_data.py`

### K11 — Güncelleme Periyodu: 30 dakika
- **Değer:** D her 30 dakikada bir güncellenir
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** **Belirtilmemiş** — mühendislik varsayımı
- **Dikkat notu:** Bu değer literatüre dayanmıyor. Savunmada: "Vardiya süresi (480 dk) 16 eşit dilime bölündüğünde elde edilen güncelleme frekansı" açıklaması kullanılabilir.
- **Dosya:** *(Hafta 4'te ekanban_signal.py'de kullanılacak)*

---

## BÖLÜM 3 — MILK-RUN / ARAÇ PARAMETRELERİ

### K12 — Araç Hızı: 10 km/sa
- **Değer:** 10 km/sa = 166.67 m/dk
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:**
  - Simić (2020) s.9 → 4 km/sa
  - Urru et al. (2018) L437 → 1 m/s = 3.6 km/sa
  - Sevim & Görkemli Aykut (2025) L706-708 → 5 km/sa
  - Zhou & Wen (2024) s.12 → 2 m/s = 7.2 km/sa
  - Menanno et al. (2023) s.13 → 12 km/sa
- **Gerekçe:** Aralıkta (3.6–12 km/sa). 10 km/sa orta-yüksek; fabrika içi iş güvenliği sınırına uygun.
- **Dosya:** `data/synthetic/vehicles.csv`

### K13 — İstasyonlar Arası Mesafe: 180 m
- **Değer:** 180 m (ortalama)
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:**
  - Simić (2020) s.9 → 265 m (toplam rota, 5 durak)
  - Urru et al. (2018) L435-436 → 124 m (toplam rota, 5 durak)
  - Zhou & Wen (2024) s.12 → 8 m/istasyon
- **Gerekçe:** Simić (2020)'de 265/5 = 53 m/durak, Urru'da 124/5 = 24.8 m/durak. Bizim 180 m fabrika içi koridor uzunluğu, hat arası geçiş mesafelerini de kapsar.
- **Dosya:** `data/synthetic/distances.csv`

### K14 — Yükleme Süresi: 2 dakika
- **Değer:** 2 dk/durak
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Urru et al. (2018) L449-451 → 2 dk/birim yük (süpermarket hazırlama); Zhou & Wen (2024) s.12 → 10 sn/birim
- **Gerekçe:** Simić (2020) s.9'da toplam yükleme 4 dk; bizim 2 dk aralıkta.
- **Dosya:** `data/synthetic/vehicles.csv`

### K15 — Boşaltma Süresi: 3 dakika
- **Değer:** 3 dk/durak
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Zhou & Wen (2024) s.12 → 5 sn/birim boşaltma; Sevim (2025) L710 → 0.6 dk toplam handling
- **Gerekçe:** Birden fazla kutu bırakılacağı durumlar için 3 dk gerçekçi.
- **Dosya:** `data/synthetic/vehicles.csv`

---

## BÖLÜM 4 — VRPTW PARAMETRELERİ

### K16 — Zaman Penceresi Genişliği: +60 dakika
- **Değer:** TW = [t_sinyal, t_sinyal + 60 dk]
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:**
  - Facchini et al. (2022) L476-477 → maks. 25 dk teslimat süresi (daha sıkı)
  - Klenk et al. (2012) s.12 → 34–47 dk lead time
- **Dikkat notu:** Facchini (2022) daha kısa pencere kullanmış. 60 dk tercihimiz savunmada şöyle gerekçelendirilebilir: "4 hat × 24 istasyonlu daha büyük sistemde araçların tüm istasyonları ziyaret süresini kapsıyor."
- **Dosya:** *(Hafta 4'te ekanban_signal.py'de kullanılacak)*

### K17 — Maksimum Tur Süresi: 90 dakika
- **Değer:** 90 dk
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Simić (2020) s.10 → 20 dk tur; Klenk (2012) → 34–47 dk
- **Gerekçe:** 24 istasyonlu büyük sistem için araç her turda maksimum 90 dk harcayabilir.
- **Dosya:** *(Hafta 4'te kullanılacak)*

---

## BÖLÜM 5 — SİNYAL MİMARİSİ KARARLARI

### K18 — Reorder Point (ROP): 1 kutu
- **Değer:** Stok 1 kutuya düştüğünde E-Kanban sinyali tetiklenir
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Facchini et al. (2022) L462-463 → sensör/buton tabanlı dinamik sipariş; Sevim (2025) L776-781 → reorder point = 25–50 birim
- **Dikkat notu:** Bazı kaynaklarda ROP = D×LT+z×σ×√LT formülü önerilir. Makalelerimizde hiçbiri bu formülü kullanmamış; hepsi tampon oranı veya eşik tabanlı yöntem kullanmış. Dolayısıyla 1 kutu eşiği literatürle uyumlu.
- **Dosya:** *(Hafta 4'te ekanban_signal.py'de kullanılacak)*

### K19 — Öncelik Kuralı: Karma (Kritiklik + FIFO)
- **Değer:** Aynı anda gelen birden fazla sinyal → önce stoğu en kritik olan, eşitlikte FIFO
- **Kaynak:** Kullanıcı onayı (29.07.2026) + literatür
- **Literatür referansı:**
  - Facchini et al. (2022) L416-417 → *"materials' priority, frequency of delivery"* — karma önceliklendirme
  - Simić (2020) L301 → *"according to the priority of the parts needed"* — kritiklik bazlı
- **Gerekçe:** İki ayrı makalede destekleniyor. Hem starvation riskini minimize eder hem de savunmada gerekçelendirilmesi kolay.
- **Dosya:** *(Hafta 4'te ekanban_signal.py'de kullanılacak)*

---

## BÖLÜM 6 — SENARYO KARARLARI

### K20 — S1: Sabit Rota Senaryosu (Baseline)
- **Tanım:** 2 araç, 60 dk sabit tur, E-Kanban sinyalleri görmezden geliniyor
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Vojdani & Drechsler (2022) L678-679 → geleneksel 1 saatlik sabit tur sistemi
- **Gerekçe:** Karşılaştırma bazı (baseline) olarak kullanılacak.

### K21 — S2: Dinamik Rota Senaryosu
- **Tanım:** E-Kanban + VRPTW tetiklemesi
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Facchini (2022), Sevim (2025), Vojdani (2022)

### K22 — S3: Talep +%20
- **Tanım:** Tüm D değerleri ×1.20
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Klenk (2012) → talep dalgalanması etkisi; Alnahhal & Noche (2015) → bozucu faktörler analizi

### K23 — S4: Araç Arızası
- **Tanım:** 2 araç → 1 araç
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Alnahhal & Noche (2015) satır 469-470 → makine arızasının stok üzerindeki etkisi

### K24 — S5: LT Uzaması
- **Tanım:** LT = 45 dk → 70 dk
- **Kaynak:** Kullanıcı onayı (29.07.2026)
- **Literatür referansı:** Jarupathirun et al. (2009) s.4 → LT değişimi 190 dk → 255 dk (%34 artış)

---

## BÖLÜM 7 — ROP VE SİNYAL FORMÜLÜ KARARLARI

### K25 — ROP Hesap Yöntemi: Oransal Tampon
- **Değer:** $ROP_{adet} = D_{dk} \times LT \times (1 + \alpha)$
- **Kaynak:** Kullanıcı onayı (30.07.2026) — Mühendislik tasarım kararı
- **Literatür notu (ERRATA — 03.09.2026):** Klenk et al. (2012) satır 1199-1200'deki *"A safety buffer time of 30% to handle deviations in the mean number of bins per tour"* ifadesi **tur süresi tamponuna** atıfta bulunmaktadır — ROP formülünü ($D \times LT \times (1+\alpha)$) doğrudan desteklememektedir. Bu formül, oransal tampon mantığından ilham alınarak tasarlanmış **bir mühendislik kararıdır**; literatürde birebir eşdeğeri bulunmamaktadır. Makalede "mühendislik kararı / tasarım tercihi" olarak etiketlenmelidir, literatür destekli formül olarak değil.
- **Reddedilen alternatif:** İstatistiksel ROP = D×LT + z×σ×√LT → literatürel destek yok, bu projede kullanılmıyor.
- **N ile farkı:**
  - N = ⌈ROP_adet / C⌉ → kaç KUTU tutulacağı (tasarım kararı, integer)
  - ROP = D×LT×(1+α) → hangi STOK SEVİYESİNDE sinyal tetikleneceği (çalışma zamanı, sürekli değer)
  - Aynı α kullanılır ama farklı sorulara cevap verirler.
- **Somut örnek (S1):** D=22/sa=0.367/dk, LT=45, α=0.15, C=20
  - ROP = 0.367×45×1.15 = 18.97 adet → stok ≤19 adete düşünce sinyal
  - N = ⌈18.97/20⌉ = 1 kutu → sistemde 1 kutu tutulur
- **Dosya:** `src/ekanban_signal.py` (Hafta 4'te kullanılacak)

### K26 — Öncelik Kuralı: Karma (Kritiklik + FIFO)
- **Değer:** Aynı anda birden fazla sinyal gelince → **önce stoğu en kritik olan** (stok/ROP oranı en düşük), eşitlikte **FIFO**
- **Kaynak:** Kullanıcı onayı (30.07.2026) — Mühendislik tasarım kararı
- **Literatür notu (ERRATA — 03.09.2026):** Facchini et al. (2022) satır 416-417'deki *"materials' priority, frequency of delivery"* ve Simić et al. (2020) satır 301'deki *"according to the priority of the parts needed"* ifadeleri **genel öncelik kavramını** desteklemektedir; ancak "Kritiklik (stok/ROP) + FIFO" şeklindeki spesifik karma kuralımızı birebir tanımlamamaktadır. Bu kural **bizim mühendislik tasarımımızdır** — literatür genel konsepte zayıf/dolaylı destek sağlamaktadır. Makalede "literatürden ilham alınan özgün tasarım kararı" olarak sunulmalıdır.
- **Reddedilen alternatifler:**
  - A (Sadece Kritiklik): Savunmada "neden hep aynı istasyon önce çıkıyor?" sorusu gelebilir
  - B (Sadece FIFO): Kritik istasyon sırada beklerken hat durabilir
- **Dosya:** `src/ekanban_signal.py` (Hafta 4'te kullanılacak)


### K27 — Zaman Penceresi: Dinamik Hesap
- **Değer:** $TW_{bitis} = \min(t_{starvation} - 5, \quad t_{sinyal} + 60)$
  - $t_{starvation} = t_{sinyal} + Stok_{o\_an} / D_{dk}$ (stok tam bitmeden kapalsa)
  - Sabit +60 dk üst sınır olarak kalır
- **Kaynak:** Kullanıcı onayı (30.07.2026)
- **Neden değiştirildi:** Sabit +60 dk S16 gibi yüksek tüketimli istasyonlarda yetersiz kalıyordu. Örnek: sinyal_dk=87, sabit TW_bitis=147 ama starvation=137 → pencere kapanmadan 10 dk önce hat duruyordu.
- **Önceki hata:** K16'daki sabit +60 dk varsayımı reddedildi, dinamik hesapla değiştirildi.
- **Dosya:** `src/ekanban_signal.py`

### K28 — Açık Sinyal Güncelleme Kuralı
- **Değer:** Bir istasyondan sinyal üretildi, araç henüz gelmedi. Bu sürede:
  - **Yeni sinyal üretilmez** (sinyal tekrarı yok)
  - Ama `kritiklik_skoru` ve `stok_o_an` **her dakika güncellenir**
  - Araç geldiğinde güncel stok bilgisiyle karşılaşır
- **Kaynak:** Kullanıcı onayı (30.07.2026)
- **Geçmiş:** Soru 1 — A seçeneği onaylandı
- **Dosya:** `src/ekanban_signal.py`

### K29 — Stok Yenileme: Basitleştirilmiş Varsayım (GEÇİCİ)
- **Değer:** Sinyal anından **LT = 45 dk** sonra stok otomatik olarak N×C adet ile yenilenir.
- **Kaynak:** Kullanıcı onayı (30.07.2026) — "Soru 2: A"
- **⚠️ GEÇİCİ BASITLEŞTİRME:** Gerçek milk-run araç rota süresi dikkate alınmıyor. Hafta 5-6'da VRPTW gerçek rota süresiyle DEĞİŞTİRİLECEK.
- **Savunma notu:** "Hafta 4, E-Kanban sinyal mantığını bağımsız test etmek için yapıldı. Hafta 5-6'da gerçek rota süresiyle entegre edildi."
- **Dosya:** `src/ekanban_signal.py`

### K30 — Zaman Penceresi Alt Sınır (Guard) Kuralı
- **Değer:** $TW_{bitis} = \max(\min(t_{starvation} - 5, t_{sinyal} + 60), t_{sinyal} + LT)$
- **Kaynak:** Kullanıcı ve AI sorgulaması (30.07.2026)
- **Gerekçe:** $t_{starvation} - t_{sinyal} < LT$ durumlarında pencerenin LT'den dar çıkmasını önlemek için alt sınır eklendi. Starvation LT'den önce gelirse sinyal `KRİTİK_ACIL` işaretlenir.
- **Dosya:** `src/ekanban_signal.py`

### K31 — S13 Sınır Durumu (Edge Case) Belgelemesi
- **Değer:** S13 ($D=23$ adet/sa) için $ROP = 19.84$, $N \times C = 20$ olup marj %0.8'dir.
- **Analiz:** 24 istasyon taranmış, marjı >%95 olan **tek istasyon S13** çıkmıştır (diğerleri %51.7–%94.9).
- **Sonuç:** Bu durum bir sistem hatası değil, Kanban boyutlandırmasının doğal bir sınır durumudur. Stok yapısı bozulmamıştır ($N \times C$ sabit tutulmuştur).
- **Dosya:** `docs/karar_gunlugu.md`, `src/ekanban_signal.py`

### K32 — Isınma Periyodu (Warm-up Period) Raporlama
- **Değer:** Simülasyonun ilk 45 dakikasındaki (1 LT) sinyaller engellenmez, ancak KPI raporlarında `ISINMA_PERIYODU` olarak ayrı tutulur.
- **Kaynak:** Kullanıcı onayı (30.07.2026)
- **Gerekçe:** Sinyal engellemek stok tükenmesini maskeleyeceği için engelleme yapılmaz; istatistiksel şeffaflık için ısınma ve kararlı hal ayrılır.
- **Dosya:** `src/ekanban_signal.py`

---

## BÖLÜM 8 — VRPTW ROTALAMA KARARLARI (Hafta 5)

> ⚠️ **Metodoloji Uyarısı:** Bu bölümdeki literatür atıfları, bir yapay zeka ajanının "Facchini (2022) MILP kullandı" iddiasının kullanıcı tarafından orijinal PDF'den teyit edilmesiyle düzeltilmiştir. O ifade, Facchini'nin literatür taramasında Aksoy & Öztürk (2016)'e ait bir cümleydi; Facchini'nin kendi yöntemi değil. Bu tür kaynak karıştırma riskine karşı, bundan sonra her iddia için doğrudan alıntı + paragraf konumu belirtilecektir.

### K33 — Rotalama Stratejisi: Olay Bazlı (Event-based)
- **Değer:** Her yeni E-Kanban sinyali geldiğinde araç depot'tan ilgili istasyonlara dinamik olarak sevk edilir.
- **Kaynak:** Kullanıcı onayı (30.07.2026)
- **Literatür referansı:** Facchini et al. (2022), Sayfa 2 — *"vehicles are dynamically dispatched from the depot to working stations when the materials' orders are processed"* + Sayfa 4 — *"It is updated in real-time by considering when the order has been sent"*
- **Reddedilen alternatifler:**
  - Rolling Horizon: Literatürde milk-run için desteklenmiyor (CIRRELT 2010 static survey)
  - Batch: Dinamik E-Kanban'ın ruhuna aykırı
- **Dosya:** `src/vrptw_solver.py`

### K34 — Algoritma: Nearest Neighbor + 2-opt
- **Değer:** Her sinyal grubunda en yakın ziyaret edilmemiş istasyona git (NN), ardından 2-opt ile rota iyileştir.
- **Kaynak:** Kullanıcı onayı (30.07.2026)
- **Literatür referansı:** Facchini et al. (2022), Sayfa 4 — *"the algorithm calculates the cost for each arc of the graph"* + *"checking the respect of the time windows iteratively"* (greedy/arc bazlı sıralı Python implementasyonu). CIRRELT (2010), Sayfa 2 — *"instances of a VRP with more than one hundred customers can be intractably hard to solve optimally"* → 24 istasyon için greedy yeterli.
- **Reddedilen alternatifler:**
  - MILP/PuLP: Yanlış atıftı — o cümle Facchini'nin literatür taramasında Aksoy & Öztürk (2016)'e aitti
  - OR-Tools: Master prompt kapsamı dışında
  - MOAEFASA: Aşırı karmaşık, master prompt yasağı
- **Dosya:** `src/vrptw_solver.py`

### K35 — Amaç Fonksiyonu: Karma (TW uyum önce, süre sonra)
- **Değer:**
  1. Birincil: Tüm TW kısıtları sağlansın (hard constraint)
  2. İkincil: Toplam rota süresi minimize: $\min \sum_{k} \sum_{i,j} t_{ij} \cdot x_{kij}$
- **Kaynak:** Kullanıcı onayı (30.07.2026)
- **Literatür referansı:** Facchini et al. (2022), Sayfa 2 — *"minimizing the tugger trains path"* + Sayfa 4 — *"equations 9 and 10 ensure that the temporal constraints, indicated by the time windows, are respected"* (hard constraint). CIRRELT (2010), Sayfa 2 — *"minimize first the total number of vehicles required and second the total travel distance incurred"* — araç sayısı sabit (2) olduğu için 2. adım uygulanır.
- **⚠️ Referans Notu:** Bundan sonra tüm literatür atıfları 'sayfa numarası + doğrudan alıntı cümlesi' formatında verilecektir. PDF'lerin çift sütunlu yapısı nedeniyle satır numaraları araçtan araca değişmekte, güvenilir referans değildir.
- **Not:** `distances.csv`'deki `sure_dk` sütunu kullanılır.
- **Dosya:** `src/vrptw_solver.py`

### K36 — VRPTW Darboğaz Tespiti ve Teşhis Düzeltmesi
- **Bulgu:** VRPTW simülasyonunda 16 turda toplam 74 kutu taşınmıştır (tur başına 4.62 kutu). Araç doluluk oranı $\%18.5$ ($Q_{arac} = 25$ kutu) seviyesindedir.
- **Teşhis Düzeltmesi:** Darboğaz **kutu kapasitesi ($Q_{arac}$) değildir**. Kutu kapasitesi kısıtlayıcı bir faktör olarak çalışmamaktadır. Asıl darboğaz **ZAMAN VE FİLO BÜYÜKLÜĞÜ (ARAÇ SAYISI)** kısıtıdır (2 araç × 480 dk = 960 araç-dk, max 16 tur).
- **Hafta 6 Yönlendirmesi:** Araç kutu kapasitesini artırmak (25 → 35) dar boğazı çözmeyecektir; Hafta 6'da filo büyüklüğü (araç sayısı) ve tur süreleri/hızları duyarlılık analiziyle incelenecektir.
- **Kaynak:** Kullanıcı ve AI mühendislik doğrulaması (30.07.2026)
- **Dosya:** `src/vrptw_solver.py`, `docs/hafta5_vrptw_analiz.md`

---

## DEĞİŞİKLİK GEÇMİŞİ

| Tarih | Karar No | Değişiklik | Neden |
|-------|----------|------------|-------|
| 29.07.2026 | K01–K24 | İlk oluşturma | Hafta 1-2 parametrelerinin kayıt altına alınması |
| 29.07.2026 | K08 | α için z-değeri hatası düzeltildi | α tampon oranı, istatistiksel z-değeri değil |
| 29.07.2026 | K18 | ROP = 1 kutu eşiği → K25'te oransal formülle değiştirildi | Formül daha akademik ve N ile tutarlı |
| 29.07.2026 | K19 | Öncelik kuralı önerildi | Facchini (2022) + Simić (2020) |
| 30.07.2026 | K25 | ROP oransal formülü onaylandı | Kullanıcı onayı — makale destekli |
| 30.07.2026 | K27 | TW_bitis sabit +60 → dinamik starvation bazlı | S16 örneğinde pencere starvation'dan sonra kapanıyordu |
| 30.07.2026 | K28 | Açık sinyal: yeni üretme, kritiklik güncelle | Kullanıcı onayı — Soru 1 A |
| 30.07.2026 | K29 | Stok yenileme sinyal+LT=45dk (GEÇİCİ) | Kullanıcı onayı — Soru 2 A; Hafta 5-6'da değişecek |
| 30.07.2026 | K30 | TW alt sınır guard eklendi | Pencere daralması ve kritik sinyal tespiti için |
| 30.07.2026 | K31 | S13 sınır durum olarak belgelendi | 24 istasyondan tek marjlı istasyon |
| 30.07.2026 | K32 | Isınma periyodu (0-45dk) ayrıştırıldı | Sinyal engellenmedi, KPI şeffaflığı sağlandı |
| 30.07.2026 | K33 | Rotalama stratejisi: Olay bazlı | Facchini (2022) Sayfa 2 — kullanıcı onayı |
| 30.07.2026 | K34 | Algoritma: Nearest Neighbor + 2-opt | MILP atfı yanlıştı (Aksoy&Öztürk'e ait); NN literatürle uyumlu |
| 30.07.2026 | K35 | Amaç: Karma (TW hard + süre minimize) | Facchini (2022) + CIRRELT (2010) — kullanıcı onayı |
| 30.07.2026 | K03, K04 | Hatalı literatür atıfları kaldırıldı | K04 (25 kutu) ve K03 (2 araç) Mühendislik Varsayımı olarak düzeltildi (Menanno gerçek $Q_{min}=45$) |
| 30.07.2026 | K36 | Darboğaz teşhisi düzeltildi | Darboğaz araç kutu kapasitesi değil, zaman ve araç sayısı kısıtıdır (Doluluk %18.5) |

---

## HAFTA 6 KARARLARI (07.08.2026)

### K37 — Analitik Filo İhtiyacı (Körösi Formülü)
| Özellik | Değer |
|---------|-------|
| **Konu** | Analitik Filo Boyutlandırma Sonucu |
| **Değer** | Baz senaryo ($A=0.85, F_t=0.80$): $AN = 3.86 \rightarrow AN_{final} = 4$ araç |
| **Kaynak** | Körösi & Duchoň (2026), *Scientific Reports / Nature*, 16:16797, **Sayfa 3–4** |
| **Gerekçe** | K36 (darboğaz=zaman kısıtı) teşhisinin analitik ispatı. 2 araç en iyimser senaryoda bile yetersiz (AN=2.91→3). |
| **Tarih** | 07.08.2026 |

### K38 — Optimal Araç Sayısı (Deneysel Sonuç)
| Özellik | Değer |
|---------|-------|
| **Konu** | Deneysel Duyarlılık Analizi Sonucu |
| **Değer** | 2 araç → %52.08 starvation; 3 araç → %36.11; 4 araç → %19.46 |
| **Kaynak** | Sevim & Aykut (2026), *Pamukkale Üniv. Müh. Bil. Derg.*, **Sayfa 1001–1006** (2 vs 3 araç testi, 3 araç önerisi) |
| **Gerekçe** | Araç sayısının starvation üzerindeki etkisi istatistiksel olarak anlamlı ($p=0$, Sevim s.820). 4 araç ile %62.6 iyileşme sağlanmıştır. |
| **Tarih** | 07.08.2026 |

### K39 — Duyarlılık Aralıkları ($A$, $F_t$ Etkisi)
| Özellik | Değer |
|---------|-------|
| **Konu** | Operasyonel Faktörlerin Filo İhtiyacına Etkisi |
| **Değer** | Muhafazakar ($A=0.70, F_t=0.60$) → 7 araç; Baz ($A=0.85, F_t=0.80$) → 4 araç; İyimser ($A=0.95, F_t=0.95$) → 3 araç |
| **Kaynak** | Körösi (2026) s.6 (SMARTENVELOPE: $A=0.7, F_t=0.5$) ve s.10 (SMARTHam: $A=0.99, F_t=0.99$) |
| **Gerekçe** | Trafik faktörü ve kullanılabilirlik, filo ihtiyacını doğrusal olmayan şekilde etkiler ($\Phi = A \cdot F_t \cdot E_w$). |
| **Tarih** | 07.08.2026 |

### K40 — Filo Kısıtlı Amaç Fonksiyonu Önceliği
| Özellik | Değer |
|---------|-------|
| **Konu** | m-VRPTW'de Amaç Fonksiyonu Öncelik Sırası |
| **Değer** | 1. Hizmet verilen istasyon sayısını maksimize et; 2. Toplam mesafeyi minimize et |
| **Kaynak** | Wang (2008), *"GA for VRPTW with limited vehicles"*, **Sayfa 48–55** |
| **Gerekçe** | Filo sınırlıyken (%18.5 doluluk, 2 araç) mesafe değil karşılama kapasitesi birincil metriktir. 2→4 araçla karşılama %39.6→%78.6. |
| **Tarih** | 07.08.2026 |

### K41 — Hafta 7–8 Takvim Adaptasyonu ve Kapsam Güncellemesi
| Özellik | Değer |
|---------|-------|
| **Konu** | 17 Haftalık Plan Esnekliği & Hafta 7–8 İçerik Güncellemesi |
| **Değer** | Hafta 7–8 kapsamı: **"SimPy Stokastik Simülasyonu ve Dispatch / Çizelgeleme Optimizasyonu"** |
| **Kaynak** | Kullanıcı / Danışman Gözden Geçirme Onayı (07.08.2026) |
| **Gerekçe** | Orijinal planda Hafta 7–8 için öngörülen *"VRPTW Kodlama ve Debug"* adımları Hafta 5'te (`vrptw_solver.py` ile) tamamlandığı için, Hafta 7–8 bütünüyle SimPy stokastik simülasyon entegrasyonuna ve farklı dispatch/önceliklendirme stratejilerinin karşılaştırılmasına ayrılmıştır. Bu değişiklik takvim esnekliğine dayanan bilinçli bir adaptasyondur. |
| **Tarih** | 07.08.2026 |

---

## HAFTA 7 KARARLARI (08.08.2026)

### K42 — Replikasyon Sayısı: 30
| Özellik | Değer |
|---------|-------|
| **Konu** | Stokastik Replikasyon Sayısı |
| **Değer** | 30 bağımsız replikasyon (seed=100–129) |
| **Kaynak** | Herrera-Vidal et al. (2026), *Applied Sciences*, 16:1701, **Sayfa 10** — 50 replikasyon önerir; 45 rep sonrası %95 CI < %2 kriterine ulaşılmıştır |
| **Gerekçe** | Test ortamı zaman kısıtı nedeniyle 30 replikasyon kullanılmıştır. 30 replikasyonda CI±95 = 0.059–0.074 puan olup kural karşılaştırması için yeterli istatistiksel güç sağlanmıştır (delta ~1.3 puan >> CI). |
| **Tarih** | 08.08.2026 |

### K43 — Warm-up Süresi: 45 Dakika (K32 Korundu)
| Özellik | Değer |
|---------|-------|
| **Konu** | Simülasyon Isınma Periyodu |
| **Değer** | 45 dk (K32 kararı korunmuştur) |
| **Kaynak** | Herrera-Vidal (2026) s.10: 30 dk Welch warm-up önerisi. K32 daha muhafazakâr olan 45 dk'yı seçmiştir. |
| **Gerekçe** | K32 kararı değiştirilmemiş; tutarlılık ve önceki haftalara göre karşılaştırılabilirlik korunmuştur. |
| **Tarih** | 08.08.2026 |

### K44 — Test Edilen Dispatch Kuralları ve Wang (2008) Doğrulanmış Alıntıları
| Özellik | Değer |
|---------|-------|
| **Konu** | Hafta 7'de Test Edilen Sinyal Önceliklendirme Kuralları |
| **Değer** | 4 kural: KRITIKLIK (baseline, K26), EDD (Wang 2008 L53-56, L754-762), SLACK (Wang 2008 L355-358), FIFO (**mühendislik tasarım kararı** — ⚠️ ERRATA 03.09.2026: Herrera-Vidal 2026 L8-10 atfı yanlıştı, o satırlar dergi/editör künyesidir) |
| **Kaynak** | **Wang et al. (2008)**, IEEE m-VRPTW:<br>• *Satır 48–56:* "...due to the limited number of vehicles... the primary objective of the vehicle routing is no longer the shortest distance or minimum cost, but the greatest number of the customers serviced..."<br>• *Satır 355–358 (Amaç Hiyerarşisi):* "The first objective function is the most number of customers that are serviced, the second objective is the lowest total distance, and the third objective is the least number of vehicles required."<br>• *Satır 754–762 (TW Kısıtı ile Rotalama):* "...the customer that satisfies the time window constraint... is inserted in turn by the greedy algorithm until the time window constraint or capacity constraint is not satisfied..." |
| **Gerekçe** | KRITIKLIK stok tabanlı, EDD/SLACK zaman tabanlı aciliyeti kullanır. FIFO en sade baseline (özgün tasarım). Wang (2008) araç kısıtlı sistemlerde zaman penceresi önceliğinin hizmet oranını maksimize ettiğini doğrular. |
| **Tarih** | 08.08.2026 |

### K45 — Önerilen Dispatch Kuralı Değişikliği: EDD (veya SLACK)
| Özellik | Değer |
|---------|-------|
| **Konu** | Mevcut K26 (KRITIKLIK) Kuralının Güncellenmesi |
| **Değer** | K26 (KRITIKLIK) → **EDD** (Earliest Due Date: `tw_bitis` ↑) veya SLACK ile değiştirilmesi önerilmektedir |
| **Kaynak** | H7 Deneysel Sonuç: EDD mean=%26.503, KRITIKLIK mean=%27.828; iki örnekli t-testi (two-sample t-test) p<0.0001 (**) ⚠️ ERRATA 03.09.2026: "Welch t-testi" ifadesi düzeltildi — Herrera-Vidal (2026)'de kullanılan "Welch's method" ısınma süresi tahmini içindir, istatistiksel anlamlılık testi değil. |

| **Gerekçe** | EDD/SLACK/FIFO, KRITIKLIK'ten ortalama 1.325 puan daha düşük starvation sağlamıştır (p<0.0001). Mevcut lt_dk=45 dk sabit yapısında EDD≈SLACK≈FIFO pratik olarak özdeştir; EDD teorik olarak daha sağlam (Wang 2008 L754-762). Gerçek veriye geçişte (lt_dk değerleri farklılaşırsa) EDD vs SLACK farkı yeniden değerlendirilmelidir. |
| **Tarih** | 08.08.2026 |

### K46 — İstatistiksel Derinlik İstisnası ve Kapsam Sınırı
| Özellik | Değer |
|---------|-------|
| **Konu** | Kapsam Sınırı İstisnası & Deterministik vs Stokastik Ayrımı |
| **Değer** | Kanonik deterministik baseline %52.08'dir. 30 replikasyonluk analiz kural farkının küçüklüğü nedeniyle yapılmış istisnai bir derinleşmedir. |
| **Kaynak** | Kullanıcı Gözden Geçirme Notu (08.08.2026) |
| **Gerekçe** | Dispatch kuralları arasındaki farkın çok dar olması ($\Delta \approx 1.3$ puan) sebebiyle 30 replikasyonla doğrulanmıştır. Payda (10,440 vs 11,520) ve stokastik varyans farkı belgelenmiş, %52.08'lik orijinal değerin geçerliliği teyit edilmiştir. Gelecek haftalarda ana kapsam sınırlarına (basit KPI karşılaştırması) geri dönülecektir. |
| **Tarih** | 08.08.2026 |

### K47 — Warm-up Payda Standardizasyonu ve İkili Raporlama İlkesi
| Özellik | Değer |
|---------|-------|
| **Konu** | Simülasyon Paydasının (11,520 vs 10,440) Standardizasyonu |
| **Değer** | İki payda da açıkça belgelenir: 1) Tam Vardiya (480 dk, 11,520 ist-dk) = %52.08; 2) Warm-up Hariç (435 dk, 10,440 ist-dk) = %57.47. |
| **Kaynak** | Herrera-Vidal et al. (2026) s.10 (Warm-up çıkarılması) & H5 Deterministik Baseline |
| **Gerekçe** | Hafta 5–6'daki %52.08, 480 dakikalık tam vardiya paydasına (11,520) dayanmaktadır. Hafta 7'de Welch kuralı uyarınca ilk 45 dakikalık ısınma çıkarılınca payda 10,440'a inmekte ve aynı 6,000 duruş %57.47 olmaktadır. Tezin şeffaflığı için her iki metrik tablolarda yan yana sunulur. |
| **Tarih** | 08.08.2026 |

---

## HAFTA 8 KARARLARI (10.08.2026)

### K48 — Takvim Kayması ve Konu İlerleme Notu
| Özellik | Değer |
|---------|-------|
| **Konu** | 17 Haftalık Planda Hafta 8 – 9 Konu Kayması |
| **Değer** | Orijinal planın Hafta 9 konusu ("Statik vs Dinamik Karşılaştırması") fiilen Hafta 8'de tamamlanmıştır. |
| **Kaynak** | Kullanıcı Gözden Geçirme Notu (10.08.2026) |
| **Gerekçe** | Hafta 5'te solver kodlaması erken tamamlandığı için proje takvimi önden ilerlemektedir. Tez tesliminde hafta numaraları konu bazlı eşleştirilecektir. |
| **Tarih** | 10.08.2026 |

### K49 — İstasyon Bazlı Değişken Lead Time Modeli (Min-Max Normalizasyonu)
| Özellik | Değer |
|---------|-------|
| **Konu** | Mesafeye Dayalı Deterministik $LT_i$ Dağılımı |
| **Değer** | $LT_i = 30 + \text{round}\left( \frac{\text{Mesafe}(Depo, S_i) - 90}{250 - 90} \times 30 \right) \text{ dk}$ $\rightarrow$ $LT_i \in [30, 60] \text{ dk}$ |
| **Kaynak** | Operasyonel Mühendislik Kararı (Min-Max Normalizasyonu) |
| **Gerekçe** | En yakın istasyonun (Hat-1, 90m) tam 30 dk, en uzak istasyonun (Hat-4, 250m) tam 60 dk alması sağlanarak 30 dakikalık tam yayılım aralığı ($[30, 60] \text{ dk}$) garanti edilmiştir. |
| **Tarih** | 10.08.2026 |

### K50 — Statik Kanban Sefer Standardı (Senaryo A)
| Özellik | Değer |
|---------|-------|
| **Konu** | Geleneksel Periyodik Milk-Run Sefer Sıklığı |
| **Değer** | 60 dakikada bir sabit kalkış ($t = 60, 120, 180, 240, 300, 360, 420$) |
| **Kaynak** | Operasyonel Mühendislik Kararı ($TC_{tam} \approx 45-55 \text{ dk}$, Max tur 90 dk [K17], 8 saatlik vardiya) |
| **Gerekçe** | 24 istasyonun tamamının tek turda gezilmesi ~45-55 dk sürdüğünden ve vardiyaya tam bölünebilir operasyonel aralık 60 dk olduğundan seçilmiştir. |
| **Tarih** | 10.08.2026 |

### K51 — EDD vs SLACK Hipotezi Değerlendirmesi
| Özellik | Değer |
|---------|-------|
| **Konu** | Değişken $LT$ Altında EDD vs SLACK Ayrışma Durumu |
| **Değer** | Sentetik fabrika modelimizde EDD ve SLACK aynı duruş süresini (144 dk, %1.25) üretmiştir. |
| **Kaynak** | H8 Kod Çıktısı (`src/variable_lt_solver.py`) |
| **Gerekçe** | Fabrika içi seyahat süreleri farkının ($0.5 - 1.5 \text{ dk}$), toplam $LT$ ($40 - 60 \text{ dk}$) yanında çok küçük kalması sebebiyle SLACK kuralı EDD'ye karşı belirgin bir üstünlük göstermemiştir. |
| **Tarih** | 10.08.2026 |

### K55 — α–N Çift Mod Tasarım ve Değerlendirme İlkesi
| Özellik | Değer |
|---------|-------|
| **Konu** | Safety Factor ($\alpha$) ve Kart Sayısı ($N$) Boyutlandırma Metodolojisi |
| **Değer** | Mod A (Sabit N, yalnızca ROP kayar) ve Mod B (Dinamik N, $N = \lceil ROP/C \rceil$ yeniden hesaplanır) olarak iki modda test edilmiştir. Sabit N modunda α etkisi zayıftır: α=0.05 (%24.08) ile α=0.30 (%21.90) arasındaki min-max fark **2.18 puan**; baz duruma (α=0.15, %24.58) göre azami iyileşme **2.68 puan**. Dinamik N modunda α etkisi belirgindir (7.42 puan iyileşme, %25.32 → %17.90). |
| **Kaynak** | H10 Kod Çıktısı (`src/hafta10_whatif_senaryolari.py`) |
| **Gerekçe** | Raf boyutu ve kart sayısı güncellenmeden yalnızca ROP eşiğini değiştirmenin sınırlı etki yarattığı kanıtlanmıştır. |
| **Tarih** | 14.08.2026 |

### K56 — Kademeli Filo Arıza Standardı ($4 \rightarrow 3 \rightarrow 2 \rightarrow 1$)
| Özellik | Değer |
|---------|-------|
| **Konu** | Kademeli Filo Kaybı Zinciri ve Operasyonel Esneklik |
| **Değer** | Filo küçüldükçe duruş oranı monoton artmaktadır: 4 araç (%24.58) $\rightarrow$ 3 araç (%36.93) $\rightarrow$ 2 araç (%53.01) $\rightarrow$ 1 araç (%69.50). Her araç kaybı ortalama +12–16 puan duruş artışı getirmektedir. |
| **Kaynak** | H10 Kod Çıktısı (`src/hafta10_whatif_senaryolari.py`) |
| **Gerekçe** | Araç sayısının sistemdeki en baskın kontrol değişkeni olduğu kesinleşmiştir. |
| **Tarih** | 14.08.2026 |

### K57 — Kanonik Simülasyon Motoru Birleştirmesi
| Özellik | Değer |
|---------|-------|
| **Konu** | Simülasyon Hesaplama Motorunun Tekleşmesi ve Tutarlılık |
| **Değer** | Tüm starvation ve WIP ölçümleri `hesapla_dinamik_wip_ve_starvation()` fonksiyonu altında birleştirilmiştir. `vrptw_solver.py`'ye `hiz_carpani`, `ekanban_signal.py`'ye `alpha` parametreleri eklenmiştir. Baz senaryo regresyonunda %24.58 duruş ve 182.3 ortalama WIP değerleri birebir doğrulanmıştır. |
| **Kaynak** | H10 Kod Çıktıları (`src/denetim_reproduksiyon_testi.py`, `src/hafta10_whatif_senaryolari.py`) |
| **Gerekçe** | İki farklı simülasyon kodunun sessizce ayrışması ve farklı sonuçlar üretmesi riski tamamen ortadan kaldırılmıştır. |
| **Tarih** | 14.08.2026 |

---

## HAFTA 9 & 10 KARARLARI (10.08.2026)

### K52 — Eşit WIP Seviyesinde Pareto Sınırı Bulgusu
| Özellik | Değer |
|---------|-------|
| **Konu** | Farklı Tur Sıklıklarında Statik vs Dinamik Pareto Karşılaştırması |
| **Değer** | Statik sistemin sefer aralığı 120 dk'ya çıkarılıp ortalama WIP ~119 adede düşürüldüğünde duruş oranı %45.54'e çıkmaktadır. Dinamik sistem (WIP=111 adet, duruş=%53.01) ile benzer seviyede kalmaktadır. |
| **Kaynak** | H9 Kod Çıktısı (`src/hafta9_pareto_analizi.py`) |
| **Gerekçe** | Duruş farklarının ana sebebi rota algoritmasından ziyade sahada tutulan toplam tampon WIP stok seviyesidir. |
| **Tarih** | 10.08.2026 |

### K53 — WIP–Starvation Temel Mühendislik Trade-off İlkesi
| Özellik | Değer |
|---------|-------|
| **Konu** | Düşük WIP ile Düşük Duruşun Birlikte Sağlanamaması |
| **Değer** | WIP seviyesi starvation'ın baskın belirleyicisidir; ancak eşit WIP'te dahi statik sistem lehine gözlenen fark stokastik koşullarda **~3.0–5.0 puana** (deterministik seed=42'de +5.27 puan, 3 tohumlu stokastik ortalamada +3.06 puan) daralmaktadır. Deterministik çevrim düzenliliği reaktif gecikmeye karşı ek avantaj sağlamaktadır. Dinamik sistemin rekabetçilik için hedef filo eşiği 8 araçtır. |
| **Kaynak** | H9 Sentez ve Pareto Analizi, H10 Seed Sağlamlık Testi |
| **Gerekçe** | 4 araç duruşu %53'ten %24'e indiren bir ara iyileşmedir; tam rekabetçilik (<%5) için 8 araç gereklidir. |
| **Tarih** | 10.08.2026 (Revize: 16.08.2026) |

### K54 — What-If Dayanıklılık (Resilience) Test Parametreleri
| Özellik | Değer |
|---------|-------|
| **Konu** | Bozucu Senaryo Stres Testi |
| **Değer** | 3 senaryo: 1) Talep Şoku (+%20 tüketim $\rightarrow$ duruş +10.1 puan), 2) Araç Arızası (4$\rightarrow$3 araç $\rightarrow$ duruş +12.4 puan), 3) Kritik Arıza (2$\rightarrow$1 araç $\rightarrow$ %69.5 duruş). |
| **Kaynak** | H10 Kod Çıktısı (`src/hafta10_whatif_senaryolari.py`) |
| **Gerekçe** | Sistemin beklenmedik fabrika içi krizlere karşı tolerans sınırları belirlenmiştir. |
| **Tarih** | 10.08.2026 |

---

### K58 — StaticMilkRunSimulator Tur Sıklığı: Kod-Rapor Uyuşmazlığı ✅ KAPANDI
| Özellik | Değer |
|---------|-------|
| **Konu** | `StaticMilkRunSimulator` 60 dk Hard-Coded Kalkış Takvimi ile Hafta 9 Kanonik 80 dk Raporunun Uyuşmazlığı |
| **Tespit** | `src/hafta8_kanban_karsilastirma.py` L97: `kalkis_dakikalari = [60, 120, 180, 240, 300, 360, 420]` (60 dk sabit). Ancak Hafta 9'da WIP eşitleme analizi için 80 dk tur kullanıldı ve `%19.31 / WIP=177.0` olarak raporlandı. Mevcut kod çalıştırıldığında `%3.04 / WIP=231.4` veriyor — kanonik değerle uyuşmuyor. |
| **Reproduksiyon** | 80 dk kalkış takvimi ([80, 160, 240, 320, 400]) + 1 kutu/ist ile kanonik `%19.31 / WIP=177.0` birebir doğrulandı (`src/seed_testi_kanonik2.py`, `src/test_80dk.py`). |
| **Düzeltme** | `run_static_simulation(arac_sayisi, tur_sikligi_dk=60)` parametresi eklendi. Kalkış takvimi artık `range(tur_sikligi_dk, 480, tur_sikligi_dk)` ile dinamik üretilir. Geri dönük uyumluluk korundu (varsayılan=60 dk). |
| **Regresyon** | `run_static_simulation(arac_sayisi=4, tur_sikligi_dk=80)` → `%19.31 / WIP=177.0` ✅ Tam eşleşme. Varsayılan `(arac_sayisi=2)` → `%5.45 / WIP=226.7` ✅ Geri uyumluluk sağlam. |
| **Kaynak** | `src/hafta8_kanban_karsilastirma.py` (K58 düzeltmesi), `src/k58_regresyon_testi.py` |
| **Tarih** | 15.08.2026 |

---

### K59 — Dashboard Veri Ambarında Sinyal Motoru Entegrasyonu ve Alpha Düzeltmesi
| Özellik | Değer |
|---------|-------|
| **Konu** | `generate_dashboard_data.py` Betiğinde $\alpha$ ve Talep Şoku Sinyal Üretimi Entegrasyonu |
| **Tespit** | İlk veri üretiminde `EKanbanSimulator` çağrılmadığı için diskteki sabit `ekanban_signals.csv` okunuyor, Sabit-N ve -%20 talep dallarında $\alpha$'nın etkisi sıfırlanıyordu. |
| **Düzeltme** | `generate_dashboard_data.py` içine `MockLoader` ve `EKanbanSimulator(m_loader, alpha=alpha)` entegre edildi. 1.920 senaryo 12 CPU çekirdeğiyle baştan üretildi. |
| **Doğrulama** | Sabit-N'de $\alpha=0.05 \rightarrow 0.30$ aralığında duruş farkı 2.18 puan; Dinamik-N'de 6.88 puan olarak K55 ile bit-bit doğrulandı. |
| **Kaynak** | `src/generate_dashboard_data.py`, `data/dashboard_scenarios.json` |
| **Tarih** | 16.08.2026 |

---

### K60 — Statik Sistem Baz Haritası (staticBaselineMap) Gerçek Simülasyona Bağlanması
| Özellik | Değer |
|---------|-------|
| **Konu** | Dashboard `kpiFarkVal` Referans Değerlerinin Simülasyon Çıktılarına Bağlanması |
| **Tespit** | İlk `staticBaselineMap` tablosundaki 1, 2, 3, 5, 6, 7, 8 araç değerlerinin dinamik stres testinden kopyalandığı saptandı. |
| **Düzeltme** | 1'den 8'e kadar tüm araç sayıları için `StaticMilkRunSimulator(loader).run_static_simulation(arac_sayisi=v, tur_sikligi_dk=80)` çalıştırıldı ve harita güncellendi: `{1: 25.77, 2: 21.35, 3: 19.70, 4: 19.31, 5: 19.10, 6: 18.96, 7: 18.83, 8: 18.68}`. |
| **Kaynak** | `src/hafta8_kanban_karsilastirma.py`, `app.js`, `dashboard.html` |
| **Tarih** | 16.08.2026 |

---

### K61 — Veri Ambarına Sefer Sayısı ve Rota Mesafesi Metriklerinin Eklenmesi
| Özellik | Değer |
|---------|-------|
| **Konu** | 1.920 Senaryoluk JSON ve CSV Veri Ambarında Sefer Sayısı ve Mesafe Alanları |
| **Düzeltme** | `generate_dashboard_data.py` çıktı sözlüğüne `sefer_sayisi` ve `mesafe_km` kolonları eklendi. -%20 talep koşulunda $N=1$ kuantizasyon tavanı ve erken tetiklenmeden kaynaklanan 31 $\rightarrow$ 33 sefer artışı doğrudan veriye kaydedildi. |
| **Kaynak** | `src/generate_dashboard_data.py`, `data/dashboard_scenarios.csv` |
| **Tarih** | 16.08.2026 |

---

### K62 — 24 İstasyon Verisinin Gerçek Parametrelere Bağlanması
| Özellik | Değer |
|---------|-------|
| **Konu** | Dashboard Bölüm 5 İstasyon Takibinin `stations.csv` ile Birebir Eşleştirilmesi |
| **Düzeltme** | 24 istasyonun gerçek $D_{\text{saat}}, C, N$ parametreleri ve en yüksek tüketimli kırılgan darboğaz istasyonu **S16** ($D=24, C=20, N=2$) JavaScript mimarisine gömüldü. |
| **Kaynak** | `data/synthetic/stations.csv`, `app.js`, `dashboard.html` |
| **Tarih** | 16.08.2026 |

---

### K63 — SLACK Sevk Kuralının Matematiksel Olarak Ayrıştırılması
| Özellik | Değer |
|---------|-------|
| **Konu** | EDD ve SLACK Kuralları Arasındaki Matematiksel Özdeşliğin Giderilmesi |
| **Tespit** | `tw_bitis - t` formülü, karar anında tüm aktif sinyaller için $t$ sabit olduğundan `tw_bitis` (EDD) ile daima özdeş sıralama üretiyordu. |
| **Düzeltme** | Klasik çizelgeleme teorisine uygun olarak dinamik seyahat ve elleçleme süreli gerçek zaman marjı formülüne geçildi: $\text{Slack}_i(t) = \text{tw\_bitis}_i - (t + T_L + \text{TT}(0, i) + T_U)$. |
| **Doğrulama** | 30 stokastik replikasyon sonucunda SLACK (%26.497), EDD (%26.503), FIFO (%26.502) ve KRİTİKLİK (%27.828) birbirinden matematiksel ve istatistiksel olarak ayrıştı. |
| **Kaynak** | `src/vrptw_solver.py`, `src/stokastik_replikasyon.py`, `docs/hafta7_dispatch_analiz_raporu.md` |
| **Tarih** | 20.08.2026 |

---

### K64 — K63 Sonrası 1920 Senaryoluk Veri Ambarının Yeniden Üretilmesi + EDD/SLACK/FIFO İstatistiksel Eşdeğerlik Testi
| Özellik | Değer |
|---------|-------|
| **Konu** | `dashboard_scenarios.csv/json` K63 Formülüyle Yeniden Üretimi ve "SLACK Üstündür" İddiasının İstatistiksel Sınanması |
| **Tetikleyici** | Veri ambarı K63 düzeltmesinden (20.08.2026) 4 gün önce (16.08.2026) üretilmişti; tüm SLACK satırları eski `tw_bitis - t` formülüyle hesaplanmıştı. Ayrıca K46'daki "SLACK en iyi kuraldır" istatistiksel iddiası eski bozuk formüle dayanıyordu ve K63 sonrası yeniden doğrulanmamıştı. |
| **Uygulanan Düzeltme 1** | `src/generate_dashboard_data.py`, K63 sonrası güncel `vrptw_solver.py` ile 12 CPU çekirdeğinde çalıştırıldı; 1920 senaryo 4.23 dakikada yeniden üretildi. `EDD == SLACK` senaryo grubu 480'den **23'e** düştü (%95.2 ayrışma). |
| **Uygulanan Düzeltme 2** | K63 formülüyle 30 stokastik replikasyon çalıştırıldı; EDD vs SLACK doğrudan Welch t-testi uygulandı. |
| **İstatistiksel Sonuç** | **4 Araç:** EDD=%26.503, SLACK=%26.497, delta=−0.006 puan, **t=0.11, p=0.913** → ANLAMLI DEĞİL. **2 Araç:** EDD=%60.964, SLACK=%60.960, delta=−0.004 puan, **t=0.08, p=0.935** → ANLAMLI DEĞİL. |
| **Düzeltilmiş Bulgu** | "SLACK en iyi sevk kuralıdır" iddiası istatistiksel kanıt taşımamaktadır. **Doğru ifade:** EDD, SLACK ve FIFO arasında istatistiksel olarak anlamlı bir fark bulunamadı; bu üç kural birbirine eşdeğerdir. KRİTİKLİK her üçünden de anlamlı biçimde daha kötüdür (p<0.0001, Δ≈+1.33 puan). |
| **Mekanizma** | 479 dispatch anından 466'sında (%97.3) sıralama değişti; ancak `Q_arac=25 kutu` kapasitesi altında gerçek sinyal seçimi 0 anda değişti. 0.08 puanlık fark rota sırası ve TW zamanlama mikro değişikliklerinden kaynaklanıyor. |
| **Güncellenen Dosyalar** | `docs/hafta7_dispatch_analiz_raporu.md` (ERRATA + Sonuç), `docs/hafta10_metodoloji_ve_bulgu_rehberi.md` (TEMEL ÇIKARIM), `data/dashboard_scenarios.csv/json`, `dashboard.html` |
| **node --check** | `embedded_script.js` → Exit Code 0. |
| **Commit** | `a0da6ac` (veri), `6e96129` (K64 ilk), bu commit (K64 istatistiksel güncelleme) |
| **Tarih** | 31.08.2026 |


---

## HAFTA 14 KARARLARI — LİTERATÜR DENETİMİ VE v2 MOTORU (30.09.2026)

> **Bağlam:** Masaüstündeki `dinamik milk run` klasöründeki 45 PDF (41 özgün çalışma)
> tek tek incelenerek projenin 27 parametre ve kararı kaynaklarıyla karşılaştırıldı.
> Sonuç: 7 doğrulandı, 8 atıf hatalı, 6 literatürden sapan model kararı, 5 kaynaksız
> mühendislik kararı, 1 aktarım hatası. Ayrıntı: `docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md`.
>
> **v1 motoru korunmuştur.** H4–H13 raporlarındaki tüm sayılar v1 ile üretilmiştir ve
> değiştirilmemiştir. Düzeltmeler `src/v2_entegre_simulasyon.py` altında toplanmıştır.

### D-GRUBU — ÖNCEKİ KARARLARDA ATIF DÜZELTMELERİ (30.09.2026)

| Karar | Önceki atıf | Denetim bulgusu | Düzeltilmiş dayanak |
|---|---|---|---|
| **K06** | Elloumi (2025), Simić (2020) | Elloumi s.613 **eşik tabanlı uyarlanabilir Kanban (AKS)** anlatır, $N=\lceil D\cdot LT(1+\alpha)/C\rceil$ formülünü vermez. Simić s.10 kart sayılarını tablo olarak verir, formül türetmez. | VDI 5586 tampon formülü **Urru vd. (2018) s.406, Denk. 1–4**: $q_{A,H} = 1 + \lceil k \cdot n_{UL,A,H}\rceil$. Projedeki biçim bu formülün ROP tabanlı uyarlamasıdır → **mühendislik uyarlaması** olarak etiketlenmeli. |
| **K09** | Pekarcikova (2021) s.7 → "min 10, max 50 adet" | Pekarcikova **2021 s.140**'taki 10/50/15 değerleri `KanbanBuffer` **tampon stok sınırları ve çekme seviyesidir**; kutu (konteyner) kapasitesi değildir. | C=15/20 için doğrudan literatür dayanağı **yoktur** → **mühendislik varsayımı** (KLT standardı gerekçesi korunur). |
| **K18** | "Makalelerimizde hiçbiri $z\sigma\sqrt{LT}$ formülünü kullanmamış" | **Yanlış.** Demiray Kırmızı vd. (2024), *Systems* 12:260, **s.9, Tablo 3**: $SS = k \cdot \sigma_d \cdot \sqrt{L_t}$ (service-level approach) açıkça verilmiştir. | İstatistiksel ROP **literatürde mevcuttur**; projede kullanılmaması bir **tercihtir**, kaynak yokluğu değil. Sınırlılık olarak yazılmalı. |
| **K24** | Jarupathirun (2009): "LT 190 → 255 dk (%34 artış)" | **Yön ters.** Jarupathirun vd. Tablo 1–2: geleneksel Kanban **255 dk** → e-Kanban **190 dk**, yani **%25 kısalma**. Bu bir LT *uzaması* senaryosu değildir. | LT uzaması senaryosu **mühendislik varsayımı**dır. Jarupathirun, e-Kanban'ın LT'yi kısalttığına dair **destekleyici** kanıt olarak kullanılmalıdır. |
| **K34** | Facchini (2022) s.4 → "NN + 2-opt" | Facchini'de **2-opt geçmez**; s.1124'te ark maliyeti ve TW kontrolü anlatılır. Ayrıca **v1 kodunda 2-opt hiç uygulanmamıştır**. | 2-Opt / Or-Opt tanımı: **Gendreau & Tarantilis (2010), CIRRELT-2010-04, Bölüm 1.1**. v1 için doğru ad: **yalnızca en yakın komşu**. v2'de 2-opt gerçekten uygulanmıştır (K72). |
| **K44** | Wang (2008) "s.48–56", EDD/SLACK dayanağı | Wang vd. (2008) makalesi **s.128**'de başlar; "s.48/s.52" sayfaları **mevcut değildir**. Makalede **EDD ve SLACK geçmez**; alıntılanan pasajlar amaç hiyerarşisi (s.130) ve açgözlü ekleme kuralıdır. | EDD/SLACK **mühendislik tasarım kararı**dır. İhtiyaç zamanına göre sıralama için gerçek dayanak: **Vojdani & Drechsler (2022) s.5** ("Aufträge nach ihren Bedarfszeitpunkten sortiert"). |
| **K44 (FIFO errata)** | 03.09.2026 errata: "FIFO mühendislik kararı, Herrera-Vidal atfı yanlıştı" | Errata **fazla ileri gitmiştir**. Herrera-Vidal vd. (2026) **s.8**: *"queues FIFO buffers controlling entity flow"* — geçerli bir kaynak mevcuttur. | FIFO için **Herrera-Vidal vd. (2026) s.8** geçerli dayanaktır. |
| **S6 (sınırlılık)** | "Vojdani & Drechsler (2022) PDF'ten doğrulanamadı" | **Doğrulandı.** s.6: *"werden die Aufträge im Stundentakt abgearbeitet … auf einer festen Route"* (saatlik takt, sabit rota). Ayrıca s.6: dijital sistem **%27 daha az sefer**, **%29,39 daha az yol**, **%38,5 daha az sürüş süresi**. | **S6 sınırlılığı kapatılmıştır.** K20/K50'nin dayanağı geçerlidir. |

### K65 — Raf Boyutlandırma: VDI 5586 "+1 Değişim Pozisyonu"
| Özellik | Değer |
|---------|-------|
| **Sorun** | v1'de 24 istasyonun 23'ünde $N=1$; ROP raf kapasitesine neredeyse eşit (S1: ROP=18,97 / raf=20). Teslimattan hemen sonra yeni sinyal çıkıyor, teslim edilen miktarın büyük kısmı raf tavanında kırpılıyor. |
| **Literatür** | Urru vd. (2018) s.406: $q_{A,H} = 1 + \lceil k\cdot n_{UL}\rceil$ — boş/dolu kutu değişimi için **+1 pozisyon zorunludur**; bilgi akışı dikkate alınmazsa tampon **eksik boyutlandırılır**. İki kutu prensibi: Klenk vd. (2012) s.11; Vojdani & Drechsler (2022) s.5 ("Zwei-Behälter-Kanban"); Droste & Deuse (2011) s.607 ("two-bin-exchange"). Sevim & Görkemli Aykut (2026) s.66: sipariş miktarı $M_j = L_j - A_j$. |
| **Karar** | v2'de `kanban_modu="VDI"`: P3 için $N = 1 + \lceil ROP/C\rceil$; P1/P2 için $N = 1 + \lceil D\cdot T(1+\alpha)/C\rceil$ (her politika kendi çevrim süresiyle boyutlandırılır — Droste & Deuse s.607–608, Şekil 4). |
| **Ölçülen etki** | Faktöriyel tasarımda ana etki **−3,88 puan duruş** (p=2,2e−05), **+148 adet WIP** (d=+1,68). |
| **Dosya** | `src/v2_entegre_simulasyon.py: kanban_boyutlandir()` |

### K66 — Tek Hizmet Süresi Modeli (Politikalar Arası Simetri)
| Özellik | Değer |
|---------|-------|
| **Sorun** | v1'de üç çözücü farklı hizmet süreleri kullanıyordu: dinamik 2 dk yükleme + **8 dk/durak**; statik simülatör ve değişken-LT çözücüsü yükleme yok + **3 dk/durak**. Aynı fiziksel sistemi temsil eden politikalar farklı sürelerle karşılaştırılmıştı. |
| **Karar** | Tüm politikalar tek parametre setinden beslenir: tur başına yükleme 2 dk (K14), durak başına 3 dk (K15), isteğe bağlı kutu başına ek süre (Urru s.408: 30 sn/kutu). |
| **Ölçülen etki** | Ayrıştırma testinde **tek başına −10,34 puan** — v1'deki en büyük tek etken. Hafta 8'deki "duruşun düşmesi yalnızca tampon genişlemesindendir" yorumu **bu nedenle eksiktir**. |
| **Dosya** | `src/v2_entegre_simulasyon.py`, `V2Parametre.durak_servis_dk` |

### K67 — "Tur Başına En Fazla 5 Durak" Kuralının Kaldırılması
| Özellik | Değer |
|---------|-------|
| **Sorun** | `vrptw_solver.py:131` ve `variable_lt_solver.py:234`'te belgelenmemiş `len(selected_signals) >= 5` sınırı vardı. Çoğu istasyon 1 kutu istediğinden tur başına yük ~5 kutuda kalıyor, 25 kutuluk araçta doluluk yapısal olarak %20'nin altına kilitleniyordu. **K36'nın "darboğaz kapasite değil zaman" teşhisi büyük ölçüde bu kuraldan doğmuştur.** |
| **Literatür** | Simić s.8 ve Urru s.408'deki "5 durak" **sistemdeki toplam istasyon sayısıdır**, tur başına sınır değildir. Klenk s.12: tur başına 20–50 kutu (≈10–25 durak). Karşılaştırma doluluk değerleri: Urru s.408 rota kapasite kullanımı 0,85–0,89; Sevim s.67 %69–81; Simić s.12 beş römorkun 3,51'i dolu. |
| **Karar** | Sınır kaldırıldı (`max_durak=None`); bağlayıcı kısıtlar araç kapasitesi (25 kutu) ve tur süresidir. Parametre olarak korunmuştur (v1 reprodüksiyonu için `max_durak=5`). |
| **Ölçülen etki** | Tek başına **+5,76 puan** (8 dk/durak hizmet süresiyle birlikte); K66 ile birlikte doluluk %19 → %40. |

### K68 — Konsolidasyonlu Sevk: En Geç Kalkış Kuralı
| Özellik | Değer |
|---------|-------|
| **Sorun** | v1'de araç boşalır boşalmaz kalkıyordu; tur sayısı şişiyor, doluluk düşüyordu (4 araçta 131 tur, %5 doluluk). |
| **Literatür** | Vojdani & Drechsler (2022) s.5–6: *"Der Routenzug fährt ab, bevor einer der geladenen Aufträge zu spät am Bedarfsort eintrifft"* → sonuç: **%27 daha az sefer**. Sevim & Görkemli Aykut (2026) s.66: kapasite dolunca **veya** bir istasyon gecikme riskine girince kalkış. Menanno vd. (2023) s.13–14: $Q_{min}$ eşiği, "yarı boş tur" engellenir. |
| **Karar** | Araç, yüklü siparişlerden biri son teslim anını kaçıracak duruma gelmeden hemen önce kalkar; kapasite dolarsa hemen kalkar. Son teslim anı: $\min(TW_{bitis},\ t_{starv}^{canlı} - 5)$. |
| **Ölçülen etki** | 4 araçta tur 91 → 27, doluluk %17 → %40; faktöriyel tasarımda **doluluk üzerinde en güçlü ana etki (+20,19 puan, d=1,80)**. Duruş üzerindeki etkisi anlamsız (p=0,317) — yani konsolidasyon **hizmet düzeyini bozmadan** taşıma verimliliğini artırır. |

### K69 — Kapalı Döngü Entegrasyon
| Özellik | Değer |
|---------|-------|
| **Sorun** | v1'de sinyaller "stok her zaman LT=45 dk sonra yenilenir" varsayımıyla (K29, "geçici") **önceden** üretilip `ekanban_signals.csv`'ye yazılıyor, rotalama bu hazır listeyi okuyordu. Araç geciktiğinde sonraki sinyalin zamanı değişmiyordu. Stokastik replikasyonlarda sinyaller hep seed=42 verisinden geliyordu. |
| **Literatür** | Facchini vd. (2022) s.1126: optimizasyon *"stand-alone"* değil, istasyon ihtiyacı–stok–araç durumu ile **uçtan uca** ele alınmalıdır. Sevim & Görkemli Aykut (2026) s.66: istasyon ajanı **gerçek stok** seviyesinden sinyal üretir. |
| **Karar** | Sinyal üretimi, teslim ve tüketim tek olay döngüsünde; sinyaller her dakika **gerçek stoktan** üretilir. K29 geçici varsayımı **kapatılmıştır**. |
| **Ölçülen etki** | v1 ayarlarıyla bile duruş %24,58 → **%6,85**; v1↔v2 farkının en büyük tek kaynağı budur. |

### K70 — Talep Modeli: Saatlik Rejim
| Özellik | Değer |
|---------|-------|
| **Sorun** | v1'de tüketim her dakika **bağımsız** $N(\mu/60,\ \sigma/60)$ çekiliyordu. Bu kurguda $L$ dakikalık toplam talebin değişkenlik katsayısı $0{,}20/\sqrt{L}$'ye iner; $LT=45$ dk için ≈**%3**. Onaylanan CV=0,20 (K10) fiilen $\sqrt{60}$ kat küçülmüş, sistem neredeyse deterministik davranmıştır (replikasyon GA'ları ±0,07 puan). |
| **Karar** | `SAATLIK_REJIM`: saatlik tüketim $N(\mu,\sigma_{saat})$ çekilir, saat içinde sabit hızda tüketilir → saatlik CV = 0,20 korunur. Alternatifler: `POISSON` (Alnahhal & Noche 2015 s.112), `NORMAL_DK_V1` (v1 davranışı), `CSV`. |
| **Dosya** | `src/v2_entegre_simulasyon.py: V2Veri.talep_uret()` |

### K71 — Metrik Mesafe Matrisi (Floyd–Warshall Kapanışı)
| Özellik | Değer |
|---------|-------|
| **Sorun** | `distances.csv` üçgen eşitsizliğini ihlal ediyordu: S1→S6 = 900 m iken S1→Depo→S6 = 180 m. Böyle bir matris hiçbir Öklid yerleşiminde gerçekleşemez; en yakın komşu rotalarını ve mesafe KPI'larını bozar. |
| **Ölçüm** | Floyd–Warshall kapanışı **286 yönlü düğüm çiftini** kısaltmaktadır. |
| **Karar** | v2 varsayılanı `mesafe_modu="METRIK"`. Kalıcı çözüm (gelecek çalışma): mesafeleri koordinatlardan dikdörtgensel ölçüyle üretmek (Sevim & Görkemli Aykut 2026 s.67) ve istasyon aralığını literatür bandına (25–53 m) çekmek. |
| **Ölçülen etki** | Tek başına **−0,86 puan**. |

### K72 — Esnek Zaman Penceresi, Tur Süresi Kısıtı ve 2-opt
| Özellik | Değer |
|---------|-------|
| **Sorun** | (a) K35 "kesin (hard) TW" diyordu ama kod geç teslimatı kabul edip kaydediyordu — fiilen **esnek** pencere. (b) 90 dk tur süresi kısıtı okunuyor ama **hiç kontrol edilmiyordu**. (c) 2-opt belgelerde vardı, kodda yoktu. |
| **Literatür** | Esnek pencere + gecikme cezası (VRP-RTW): Fitrie vd. (2025) s.1835; Zidanne vd. (2025) s.14. Tur süresi kısıtı: Facchini vd. (2022) s.1124, Denk. 7. 2-Opt: Gendreau & Tarantilis (2010) Bölüm 1.1. |
| **Karar** | Model **VRP-RTW** olarak yeniden tanımlandı (maliyet = süre + ceza×gecikme); tur süresi kısıtı sevk seçiminde uygulanıyor; 2-opt gerçekten kodlandı. |
| **Doğrulama** | Tur-içi optimallik testi (400 rastgele durak kümesi, tam numaralamaya karşı): NN **%1,68**, NN+2opt **%0,62** sapma; 2-opt turların %46,5'inde optimali buluyor. |

### K73 — Üç Politikalı Karşılaştırma Seti
| Özellik | Değer |
|---------|-------|
| **Sorun** | v1'de statik referans, talepten bağımsız olarak her istasyona her turda 1 kutu bırakan tek bir modeldi ve rafı tur aralığından bağımsız sabitti. Droste & Deuse (2011) s.607–608 ve VDI formülü, gereken rafın **tur aralığıyla orantılı** büyüdüğünü gösterir; bu nedenle 80–120 dk'lık statik senaryolar eksik boyutlandırılmıştı. |
| **Karar** | P1 (sabit takt, sabit miktar — Klenk s.6), P2 (sabit takt, Kanban miktarı / 1:1 boş kutu değişimi — Simić s.10–11, Vojdani s.6), P3 (olay tabanlı dinamik — Facchini s.1123). **Her politika kendi formülüyle boyutlandırılır.** |
| **Dosya** | `src/v2_pareto_ve_figurler.py` |

### K74 — Koşu-İçi Dinamik Kanban (Uyarlanabilir Kanban)
| Özellik | Değer |
|---------|-------|
| **Sorun** | Literatürde *adaptive Kanban*, kart sayısının **işletme sırasında** stok/bekleyen sipariş eşiklerine göre değiştiği sistemdir (Elloumi vd. 2025 s.613, Tardif & Maaseidvaag'a atıfla). Projede $N$ yalnızca **senaryolar arasında** değişiyordu (K55 Mod B). |
| **Karar** | v2'ye `dinamik_n=True` eklendi: her 30 dk'da (K11) son 60 dk'lık gerçekleşen tüketimden $D$ tahmin edilip $N$ ve ROP güncellenir. Kullanılmadığında model **"senaryo bazlı parametrik Kanban"** olarak adlandırılmalıdır. |

### K75 — Stokastik Tüketim Üreticisindeki Aktarım Hatası ✅ DÜZELTİLDİ
| Özellik | Değer |
|---------|-------|
| **Tespit** | `src/stokastik_replikasyon.py`'deki `ISTASYON_TUKETIM_MU` sözlüğü elle yazılmış ve `stations.csv` ile uyuşmuyordu: **S10: 18 (doğrusu 11)**, **S23: 18 (doğrusu 12)**. Toplam talep 446 adet/sa (doğrusu 409) → **%9 fazla**. |
| **Etkilenen sonuçlar** | Hafta 7'nin 30 replikasyonlu dispatch karşılaştırması ve Hafta 10 seed sağlamlık testi (“stokastikte fark 2,92–3,13 puana daralıyor” yorumu dâhil) bu hatalı talep altında üretilmiştir. |
| **Düzeltme** | Üretici artık `stations.csv`'den okur (tek doğruluk kaynağı). Eski sözlük `ISTASYON_TUKETIM_MU_HATALI_H7` adıyla ve `hatali_h7_degerleri=True` bayrağıyla yalnızca reprodüksiyon amaçlı korunmuştur. |
| **Tarih** | 30.09.2026 |

### K76 — Solomon VRPTW Kıyaslama Doğrulaması
| Özellik | Değer |
|---------|-------|
| **Yöntem** | 6 örnek (C101, C201, R101, R201, RC101, RC201) × 2 boyut (25, 50 müşteri). SINTEF'in BKS tabloları sayfada JavaScript ile yüklendiğinden programatik alınamadı; değerleri elle aktarma riski nedeniyle **Balikos vd. (2025) s.435–437 yaklaşımı** izlendi: OR-Tools referans çözücüdür (anılan çalışma OR-Tools'un Solomon'da BKS'ye ortalama %10'dan yakın olduğunu raporlar). Sapma: $e_d = 100(v_c - v_k)/v_k$. |
| **Sonuç** | Projedeki en yakın komşu sezgiseli OR-Tools'a göre **ortalama %102,7** (medyan %89,5; en kötü %198,5) daha uzun rotalar üretmektedir. **2-opt kazancı yalnızca %0,50**'dir. |
| **Yorum** | 2-Opt tur-**içi** bir komşuluk yapısıdır; Solomon'daki açık esas olarak tur-**arası** atamadan doğar. Fabrika içi problemde turlar 2–8 duraklıdır ve tur-içi sıralama tam numaralamaya göre yalnızca **%0,62** sapar (K72 doğrulaması). Dolayısıyla Solomon'daki açık bu bağlama doğrudan taşınmaz; ancak **tur-arası atama (hangi siparişin hangi turda olacağı) sevk kuralıyla belirlenir ve optimize edilmemektedir** — sınırlılık olarak yazılmalıdır. |
| **Dosya** | `src/solomon_dogrulama.py`, `data/synthetic/solomon_dogrulama_sonuclari.csv` |

### K77 — Başlangıç Stoku Seçeneği
| Özellik | Değer |
|---------|-------|
| **Değer** | `baslangic_stok`: `"DOLU"` ($N\times C$, v1 davranışı), `"ROP"`, `"ORAN"`. |
| **Gerekçe** | Dolu raflarla başlamak uzun bir geçici rejim yaratır (K78). ROP seviyesinden başlamak geçici rejimi kısaltır ama ilk 45 dk'da yapay starvation üretir (2,56 istasyon/dk). Baz koşu için **DOLU** korunmuştur. |

### K78 — Isınma Süresi: 45 dk → 90 dk (Welch Yöntemiyle Ölçüldü)
| Özellik | Değer |
|---------|-------|
| **Sorun** | K32/K43'te 45 dk **varsayılmış**, Herrera-Vidal'ın atıf yapılan Welch grafik yöntemi **hiç uygulanmamıştı**. |
| **Ölçüm** | 20 replikasyon, ±15 dk hareketli ortalama. Kararlı WIP ≈ 367 adet. **t=45 dk'da WIP hâlâ kararlı değerin %54–56 üzerindedir**; %1 bandına ancak **t≈90 dk**'da girer. Katı ölçütle (60 dk boyunca kesintisiz ±%2 bandı) kalıcı giriş 246 dk'dır. |
| **Karar** | v2 varsayılanı `isinma_dk=90`. |
| **Sonuç** | 480 dk'lık tek vardiyada analiz penceresi 435 dk değil **390 dk**'dır; katı ölçüt alınırsa yarıdan azdır. **S2 sınırlılığı (tek vardiya) düşünülenden ciddidir** ve raporlanan tüm oranlar geçici rejim etkisi taşır. 1440 dk'lık (3 vardiya) koşularda kararlı değer doğrulanmıştır. |

### K79 — Statik Referansın Tek Nokta Yerine Sınır Eğrisi Olarak Kurulması
| Özellik | Değer |
|---------|-------|
| **Sorun** | "5 araçtan itibaren dinamik üstün" iddiası (H8) statik referans olarak **80 dk turun** seçilmesine bağlıydı. Statik sistem **60 dk turla 4 araçta %3,04** duruş veriyordu — 8 araçlı dinamik sistemden (%3,50) bile iyi. |
| **Karar** | Tur aralığı 30–120 dk bandında taranır; karşılaştırma tek nokta yerine **sınır eğrisi** üzerinden yapılır (252 konfigürasyon × 8 replikasyon). |

### K80 — Pareto Cephesi
| Özellik | Değer |
|---------|-------|
| **Amaçlar** | Ortalama hat yanı WIP ↓, duruş oranı ↓, toplam mesafe ↓. |
| **Analitik temel** | Stok çevrim süresiyle orantılıdır (Droste & Deuse 2011 s.607–608, Şekil 4); tampon rota frekansıyla ters orantılıdır (Urru vd. 2018 s.406); tur sayısı–stok ödünleşimi (Alnahhal & Noche 2015 s.118). Yöntem örneği: Zhou & Wen (2024) NSGA-II ile Kanban sayısı + kutu kapasitesi ortak optimizasyonu. |
| **Yöntem** | Bu ölçekte metasezgisel gerekmez: tam ızgara taranır, baskın olmayan çözümler süzülür. Şekil 1'de iki amaçlı (WIP × duruş) politika-içi cephe; CSV'de üç amaçlı genel cephe. |
| **Bulgu** | **P3 cephesi hem en solda hem en altta**: aynı duruş oranı belirgin biçimde daha az WIP ile sağlanır. |

### K81 — Politikalar Ancak Talep Şoku Altında Ayrışır
| Özellik | Değer |
|---------|-------|
| **Bulgu** | Literatüre uygun boyutlandırma (K65) uygulandığında baz talepte **üç politika da 2 araçla %5 eşiğinin çok altındadır** (P1 %0,04 / P2 %0,15 / P3 %0,01). Politikalar ancak **+%50 talep şoku** altında ayrışır (P1 3 araç %0,42 / P2 2 araç %4,85 / P3 3 araç %0,49). |
| **Sonuç** | v1'deki yüksek duruş oranları (%24–53) esas olarak **eksik raf boyutlandırma + hizmet süresi asimetrisi + açık döngü** kaynaklıdır, politika farkından değil. |

### K82 — Deney Tasarımı: Faktöriyel + ANOVA + Tukey HSD
| Özellik | Değer |
|---------|-------|
| **Sorun** | v1'de dört sevk kuralı **ikili t-testleriyle** karşılaştırılmıştı (K45/K64); çoklu karşılaştırma düzeltmesi yoktu. |
| **Yöntem** | $2^5$ tam faktöriyel (filo, α, sevk, talep, raf) × 10 replikasyon = 320 koşu (Sevim & Görkemli Aykut 2026 s.67 deseni); sevk kuralları için tek yönlü ANOVA + Tukey HSD (Herrera-Vidal vd. 2026 s.9–10). |
| **Ana etkiler (duruş)** | Talep düzeyi **+10,22** (p<0,001) > Filo **−9,55** (p<0,001) > Raf boyutlandırma **−3,88** (p<0,001) > α **−1,35** (p=0,15, anlamsız) > Sevk politikası **+0,93** (p=0,32, anlamsız). En güçlü etkileşim: **Filo × Talep = −6,79 puan**. |
| **Doluluk** | Sevk politikası **+20,19 puan** (d=1,80) — en güçlü ana etki. |
| **⚠️ K45/K64 REVİZYONU** | v2'de sevk kuralları arasında **hiçbir anlamlı fark yoktur**: yeterli filoda F=0,003, **p=0,9997**; kısıtlı filo + şokta F=1,152, **p=0,3415**. Tukey HSD'de hiçbir ikili fark eşiği aşmamaktadır. **K45'in "KRİTİKLİK anlamlı biçimde kötüdür, EDD'ye geçilmeli" tavsiyesi v2'de desteklenmemektedir.** Muhtemel neden: v1'de kritiklik skoru sinyal anında hesaplanıp donuyordu; v2'de canlı stok/ROP kullanılmaktadır. Ayrıca v1'deki 5 durak sınırı ve hatalı talep verisi (K75) etkilidir. |
| **Replikasyon ölçütü** | Bağıl ölçüt (yarı-genişlik ≤ ortalamanın %2'si) ortalama sıfıra yakınken **tanım gereği sağlanamaz** (n=60'ta bile %12,2). Bu koşulda **mutlak ölçüt** kullanılmalıdır: ±0,05 puan için **n=9** yeterlidir. |

### K83 — Vaka Çalışması: Literatürden Türetilmiş Otomotiv Yan Sanayi Senaryosu
| Özellik | Değer |
|---------|-------|
| **Gerekçe** | TR Dizin dergileri, özellikle Endüstri Mühendisliği Dergisi, gerçek veya gerçekçi vaka içeren çalışmalara öncelik vermektedir. Gerçek fabrika verisi henüz bulunmadığından **literatürden türetilmiş** ve açıkça bu şekilde etiketlenmiş bir vaka kurgulanmıştır. |
| **Ölçek referansları** | Facchini vd. (2022) s.1125: otomotiv kaynak atölyesi, 3 vagonlu 4 çekici, ~400 sefer/vardiya, 25 dk üzeri "geç"; Menanno vd. (2023) s.13–14: 11 hatlı pompa montajı, $Q_{min}$ 35–55; Sevim & Görkemli Aykut (2026) s.67: 10 istasyon, ROP 25–50. |
| **Tasarım** | 4 hat / 24 istasyon / 3 araç / 480 dk; üç politika × üç senaryo (normal, +%50 talep şoku, araç arızası 3→2) × 12 replikasyon. |
| **Bulgu** | P3, normal vardiyada aynı hizmet düzeyini **%50,5 daha az WIP** ile sağlar; talep şokunda duruşta **9,77 puan** öndedir. Bedeli mesafede +%15…+%68 artıştır (Alnahhal & Noche 2015 s.118'deki ödünleşimin beklenen yönü). |
| **Dosya** | `src/v2_vaka_ve_kpi.py`, `data/synthetic/v2_vaka_calismasi.csv` |

### K84 — Dinamiklik Derecesi (Degree of Dynamism)
| Özellik | Değer |
|---------|-------|
| **Tanım** | Larsen, Madsen & Solomon (2008), *Recent Developments in Dynamic Vehicle Routing Systems*, **Bölüm 3.1**: $dod = n_{imm}/n_{tot}$. |
| **Ölçüm** | P3'te vardiya başına ≈161 ikmal isteğinin tamamı vardiya içinde gerçek stok tükenmesiyle doğar → **dod = 1,00 (tam dinamik)**. P1/P2 takvim tabanlıdır → dod = 0. |
| **Kullanım** | Problem sınıfının biçimsel gerekçesi: statik VRPTW çözücüleri doğrudan uygulanamaz. Tez Metodoloji bölümünde problem tanımına eklenmelidir. |
| **Sınırlılık** | dod = 1 uç değeri, `production_plan.csv`'nin talep modeline bağlanmamasından kaynaklanır; bağlanırsa kısmen önceden bilinen istekler doğar ve dod < 1 olur. |

### K85 — Literatür KPI Uyumu
| Özellik | Değer |
|---------|-------|
| **Ölçütler** | Sevim & Görkemli Aykut (2026) s.67, **Denk. 5–9**: ortalama doluluk oranı, tur başına ortalama mesafe, ortalama tur sayısı, istasyon başına ortalama bekleme süresi. Starvation tanımı: Menanno vd. (2023) s.16 (Korytkowski & Karkoszka 2016'ya atıfla). |
| **Bulgu** | Konsolidasyonun ödünleşimi: ikmal süresi 5,5 → 29,6 dk uzarken doluluk %5,7 → %33,7'ye çıkar, tur sayısı 113,7 → 18,8'e iner. 29,6 dk, Facchini'nin ≤25 dk hedefine yakın ve Klenk'in e-Kanban ikmal bandının (102–113 dk) çok altındadır. |
| **⚠️ Kıyaslama uyarısı** | Doluluk oranları literatürle **doğrudan kıyaslanamaz**: bu çalışmada istasyon başına 1–3 kutu taşınırken Urru s.408'de rota kapasite kullanımı 0,85–0,89, Sevim'de %69–81'dir. Fark talep yoğunluğu ve kutu büyüklüğü tasarımından gelir. |

---

## HAFTA 15 — LİTERATÜR BOŞLUĞU KARARLARI (26.10.2026)

### K86 — Özgün Katkı İddiasının Yeniden Tanımlanması
| Özellik | Değer |
|---------|-------|
| **Tetikleyici** | Kaynak klasörünün dışına çıkan genişletilmiş tarama (Ekim 2026). |
| **Tespit** | Tezin *"E-Kanban + VRPTW + stok simülasyonunu bütünleşik ele alan çalışma yok"* iddiası **savunulamazdır**. Bu iddiayı çürüten dokuz çalışma belirlenmiştir: Alnahhal, Ramadan & Noche (2016); Ciemnoczolowski & Bozer (2013); Bocewicz vd. (2019); Zhou & Wen (2024); Menanno vd. (2023); Vojdani & Drechsler (2022); Kundu vd. (2019); Urru vd. (2018) + Schmidt vd. (2016) + VDI 5586 Blatt 2 (2022); Elloumi vd. (2025). |
| **En büyük tehdit** | **Alnahhal, Ramadan & Noche (2016)**, *Static Versus Dynamic Control of Material Flow in In-Plant Milk Run System*: push / Kanban / e-Kanban / AEK'yi envanter + starvation ölçütleriyle karşılaştırıp **koşullu sonuç** bulmuştur — bizim ana bulgumuzun doğrudan öncülüdür. Makalede mutlaka alıntılanmalı ve farkımız açıklanmalıdır. |
| **Yeni boşluk tanımı** | Yazın iki kolda gelişmiş ve **birleşmemiştir**: (A) tamponun ikmal politikasına bağlı olduğunu gösteren boyutlandırma kolu (Urru s.407: aynı veriyle yöntem değişince tampon 18 → 19/20/23; Droste & Deuse s.607–608; Schmidt s.3), politikaları performans açısından karşılaştırmaz. (B) Politikaları karşılaştıran simülasyon kolu (Vojdani s.5 *"identisches Layout"* + aynı iki kutulu Kanban; Chee vd. s.392 her iki politikaya aynı {2,4,6}; Alnahhal & Noche s.117 *"fill rate ≥ %99"*), tamponu politikanın çevrim süresinden formülle türetmez. |
| **Revize katkı** | 1) Politika-tutarlı boyutlandırma ilkesi ve ihmalinin sonucun **yönünü** değiştirmesi; 2) modelleme kararlarının ayrıştırılmış etkisi (10+ puan, politika farkından büyük); 3) tüketim hızından türetilen dinamik TW (ihtiyatlı); 4) koşullu/dürüst raporlama. |
| **Dürüstlük kaydı** | Kol B'de iki çalışma adil karşılaştırma kaygısı taşır (Alnahhal hizmet düzeyini eşitler; Chee parametre tarar ve push lehine "mükemmel push" senaryosu kurar, s.393). Bu nedenle iddia *"kimse düşünmemiş"* değil, **"formülle türetme yapılmamış ve etkisi ölçülmemiştir"** biçiminde yazılmalıdır. |
| **Dosya** | `docs/literatur_boslugu_analizi.md` (kanıt tabloları, hakem yanıtları, makaleye hazır cümleler) |

### K87 — Kaynak Arşivi Denetimi: Zip Dosyaları ve Eksik Kaynaklar
| Özellik | Değer |
|---------|-------|
| **Denetim** | Masaüstü `dinamik milk run` klasöründeki üç zip ile çıkarılmış klasörler karşılaştırıldı. |
| **Bulgu 1** | `dy makale2.zip` (14 PDF) ve `dynamic makaleleri.zip` (22 PDF) içerikleri çıkarılmış klasörlerle **özdeştir**; yeni makale yoktur. |
| **Bulgu 2** | `dy makale3.zip` **boştur** (0 girdi); `dynamic makaleleri/Yeni Sıkıştırılmış Klasör.zip` de boştur (22 bayt). |
| **Bulgu 3** | Zip'te olup çıkarılmamış üç dosya: `1-s2.0-S2405896318307894-main (1).pdf` ve `IJSIMM19-2_513 (1).pdf` (ikisi de **kopya**), `logistics-06-00074.pdf` (Malik vd. 2022, süt tedarik zinciri — f8c4f73 commit'inde zaten kapsam dışı bırakılmıştı). **Yeni içerik yoktur.** |
| **Bulgu 4 — düzeltildi** | `LOGISTIQUA_2020_paper_166.pdf` (Tissir, El Fezazi & Cherrafi 2020) masaüstü arşivinde olmasına rağmen **projede yoktu ve metne çıkarılmamıştı**. 26.10.2026'da `docs/papers/zip3_yeni/dy makale 3/` altına kopyalandı ve `docs/papers/extracted_text/` içine çıkarıldı (5 sayfa). Giriş/motivasyon bölümünde Endüstri 4.0 – Yalın ilişkisi için kullanılabilir (Tablo 1: e-Kanban). |
| **Sonuç** | Kaynak arşivi artık **senkrondur** (masaüstündeki 45 özgün PDF'in tamamı projede ve metne çıkarılmış durumda); eksiklik zip'lerde değil, **hiç edinilmemiş kaynaklardadır**. |
| **Tekrarlanabilirlik** | `python -X utf8 -m src.kaynak_arsivi_denetimi` — zip/kopya/senkron/metin denetimini ve eksik kaynak listesini yeniden üretir. |
| **Edinilmesi gereken** | 🔴 Alnahhal, Ramadan & Noche (2016) doi:10.1007/978-3-319-23512-7_70 · 🔴 Ciemnoczolowski & Bozer (2013) doi:10.1080/00207543.2012.656331 · 🟠 Bocewicz vd. (2019) doi:10.24425/mper.2019.129597 (açık erişim) · 🟠 Schmidt vd. (2016) IMHRC (açık erişim) · 🟡 VDI 5586 Blatt 2 (2022) · 🟡 Kundu vd. (2019) IJIEC 10:421–442 |
| **Tarih** | 26.10.2026 |

### K88 — K06 Kanban Formülünün GERÇEK Kaynağı Bulundu: Toyota Formülü ✅
| Özellik | Değer |
|---------|-------|
| **Geçmiş** | K06 formülü $N = \lceil D \cdot LT(1+\alpha)/C \rceil$ için önce Elloumi (2025) / Simić (2020) gösterilmiş, 30.09.2026 denetiminde bu atıfların **hatalı** olduğu belirlenmiş ve formül *"mühendislik uyarlaması"* olarak etiketlenmişti. |
| **Bulgu (26.10.2026)** | **Kundu, Rossini & Portioli-Staudacher (2019), IJIEC 10:422–423**, formülün kaynağını vermektedir: **Toyota formülü — Sugimori, Kusunoki, Cho & Uchikawa (1977)**: $$y = \frac{D\,(T_w + T_p)(1+\alpha)}{a}$$ burada $y$ = kanban sayısı, $D$ = birim zamanda talep, $T_w$ = bir kanbanın bekleme süresi, $T_p$ = işlem süresi, $a$ = konteyner kapasitesi, $\alpha$ = güvenlik katsayısı. |
| **Eşleşme** | Bizim $LT = T_w + T_p$, $C = a$ alırsak formül **birebir aynıdır**. K06 artık "mühendislik uyarlaması" değil, **Toyota formülünün fabrika içi milk-run bağlamına uygulanmasıdır**. |
| **⚠️ α uyarısı** | Aynı sayfada: *"$\alpha$ = safety factor. It is policy variable (**although < 10%**)"*. Projede **α = 0,15 (%15)** kullanılmaktadır — Toyota formülünün önerdiği bandın **üzerindedir**. K08 bu bilgiyle güncellenmeli; tezde ya gerekçelendirilmeli ya da α ≤ 0,10 ile duyarlılık verilmelidir. Faktöriyel tasarımda α'nın ana etkisi zaten anlamsızdı (p=0,145), dolayısıyla bulgular bundan etkilenmez. |
| **Ek sınır** | Kundu s.423: konteyner kapasitesi $a$ *"not more than 10% of daily demand"* olmalıdır. Projede S1 için $C=20$, günlük talep $22 \times 8 = 176$ → %11,4 — sınırın hemen üzerinde. Belgelenmeli. **⚠️ Düzeltme (K95, 27.10.2026): yalnızca S1 değil, 24 istasyonun 24'ü sınırı aşar (%10,4–%17,0, ort. %13,6).** |
| **Ek bulgu** | Faccio vd. (2013a), Toyota formülünün tek başına *"unable to bring about substantial results without an integrated approach"* olduğunu göstermiştir — bütünleşik yaklaşımımızı destekler. Faccio vd. (2013b): *"use of an analytical approach alone may be unable to obtain reliable results"* — simülasyon tercihimizi destekler. |
| **Eylem** | K06'nın kaynağı **Sugimori vd. (1977)** olarak güncellenmeli; Kundu (2019) ikincil kaynak olarak gösterilmelidir. |
| **Tarih** | 26.10.2026 |

### K89 — Boşluğun Literatür Tarafından İlan Edilmesi (Kundu 2019)
| Özellik | Değer |
|---------|-------|
| **Bulgu** | Kundu vd. (2019) s.423, Monden (2011)'e dayanarak iki politika ailesini tanımlar: *fixed quantity, variable time* = **reorder point** (bizim **P3**) ve *fixed time, variable quantity* = **periodic review** (bizim **P2**). Hemen ardından: *"This research utilizes the fixed time, variable quantity solution and **does not investigate the differences with the other policy. This could however be the subject of future research.**"* |
| **Önem** | Bu, tez/makalenin boşluk iddiasının **literatür tarafından açıkça ilan edilmiş** biçimidir. Giriş bölümünde doğrudan alıntılanmalıdır. |
| **⚠️ Karşı kanıt (dürüstlük)** | Aynı sayfada: *"The comparison of different feeding policies has been relatively well covered"* (Limère 2012; Golz 2012; Sali 2015; Faccio 2014; Caputo & Pelagagge 2011). Dolayısıyla **"politika karşılaştırması yapılmamıştır" denemez**; iddiamız yalnızca *boyutlandırmanın politikaya göre türetilmesi ve etkisinin ölçülmesi* ile sınırlıdır. |
| **Tarih** | 26.10.2026 |

### K90 — Açık Erişim Kaynak Edinimi (K87 takibi)
| Özellik | Değer |
|---------|-------|
| **Yöntem** | OpenAlex, Unpaywall, Semantic Scholar ve Crossref API'leri ile DOI tabanlı açık erişim taraması. |
| **Edinilen (2/7)** | ✅ **Bocewicz vd. (2019)** — PAN Journals, *diamond OA* → `docs/papers/ek_kaynaklar/E3_…pdf` (13 sayfa, okundu). ✅ **Kundu vd. (2019)** — Growing Science, *diamond OA* → `E6_…pdf` (22 sayfa, okundu). Her ikisinin metni `docs/papers/extracted_text/` altındadır. |
| **Edinilemeyen (5/7)** | ❌ **Alnahhal, Ramadan & Noche (2016)** — OpenAlex/Unpaywall/S2: `is_oa=false`, hiçbir meşru açık kopya yok (Springer, kapalı). ❌ **Ciemnoczolowski & Bozer (2013)** — aynı şekilde kapalı (T&F); S2'de özet bile yok. ❌ **Korytkowski & Karkoszka (2016)** — Springer *hybrid OA* olarak işaretli ancak indirme bot korumasına takılıyor; **kurumsal erişimle alınmalıdır**. ❌ **VDI 5586 Blatt 2 (2022)** — ücretli standart. ❌ **Schmidt vd. (2016)** — MHI'den açık erişimdir ve bu denetimde okunmuştur; PDF arşive kopyalanmamıştır. |
| **Not** | Erişim engellerini aşmaya yönelik hiçbir girişimde bulunulmamıştır. Kalan 5 kaynak **kütüphane/kurumsal erişimle** edinilmelidir. |
| **Denetim** | `python -X utf8 -m src.kaynak_arsivi_denetimi` eksik listesini günceller. |
| **Tarih** | 26.10.2026 |

### K91 — Katkı Gücünün Dürüst Değerlendirmesi ve Güçlendirme Yol Haritası
| Özellik | Değer |
|---------|-------|
| **Soru** | "Çalışma literatürde bir açık kapatıyor mu, yenilik getiriyor mu?" |
| **Yargı** | **Evet — ancak tek bir açık, ve bu açık "yeni yöntem geliştirme" türünden değil, "mevcut yöntemler yanlış karşılaştırılıyor" türündendir.** Teknik/kavramsal yenilik **yoktur**; metodolojik yenilik vardır. |
| **Kapatılan açık** | Kundu vd. (2019) s.423'ün açıkça gelecek çalışma ilan ettiği **reorder point (P3) ↔ periodic review (P2)** karşılaştırması; üzerine **politika-tutarlı boyutlandırma** ilkesi ve ihmalinin sonucun *yönünü* değiştirdiğinin ölçülmesi. |
| **Kapatılmayan** | E-Kanban+VRPTW entegrasyonu, Kanban↔starvation, filo↔stok ödünleşimi, Pareto, Kanban boyutu↔sayısı, Toyota formülü, VDI +1, uyarlanabilir Kanban — hepsi literatürde mevcuttur (bkz. K86, `literatur_boslugu_analizi.md` Bölüm 2). |
| **Hedefe göre yeterlilik** | Lisans/YL tasarım çalışması: ✅ fazlasıyla yeterli. **TR Dizin (End. Müh. Dergisi, JTOM): ⚠️ sınırda** — tek engel **gerçek veri yokluğu**; anılan dergi vaka çalışmasına öncelik vermektedir. SCI-E: ❌ katkı artımsaldır. |
| **Yol 1 (🔴 en yüksek etki)** | **Gerçek veri.** Tek vardiyalık gerçek tüketim verisi bile yeterlidir; altyapı hazırdır (`config.json → "real"`, `data/real/*.csv`). S1 sınırlılığını kapatır ve makaleyi TR Dizin eşiğinin üzerine taşır. |
| **Yol 2 (🟠)** | **İddiayı küçült, kanıtı büyüt.** "Entegre KDS geliştirdik" terk edilmeli; yerine: *"boyutlandırma tutarsızlığı, politikalar arasındaki gerçek farktan büyük bir yanlılık üretir"*. Destekleyen sayılar: hizmet süresi asimetrisi 10,34 puan · açık döngü %24,58→%6,85 · raf boyutlandırma 3,88 puan **vs politika farkı ≈1 puan**. |
| **Yol 3 (🟠)** | **Katkıyı kendi modelinin dışına taşı.** Şu an düzeltilen hata kendi v1 modelimizdedir; hakem *"kendi hatasını düzeltmek katkı mı?"* diyebilir. Vojdani & Drechsler (2022) s.5 iki sistemi *"identisches Layout und identische Taktzeiten"* + **aynı iki kutulu Kanban** ile karşılaştırmaktadır — eleştirdiğimiz kurgu bağımsız bir çalışmada mevcuttur. Bu kurgu v2'de yeniden kurulursa katkı genellenebilirlik kazanır. İş yükü ≈ yarım saat (P1/P2 kurulu; 15 istasyon / saatlik takt / iki kutu girilmeli). ⚠️ Vojdani'yi **çürütmek** olarak değil, **duyarlılık analizi** olarak sunulmalıdır; onun bulgusu (%27 az sefer, %29,39 az yol) taşıma verimliliği üzerinedir ve bu düzeltmeden etkilenmez. |
| **Özet** | Gücü: kendi sonucunu çürütecek kadar dürüst olmak ve bunu sayısallaştırmak — yazında nadirdir. Zayıflığı: sentetik veri (Yol 1 giderir) ve katkının "negatif" karakteri (Yol 3 giderir). |
| **Dosya** | `docs/literatur_boslugu_analizi.md` Bölüm 10 |
| **Tarih** | 26.10.2026 |

### K92 — Dashboard v1 Verisiyle Çalışıyor: Geçici Uyarı Bandı ✅ KAPANDI (K94, 27.10.2026)
| Özellik | Değer |
|---------|-------|
| **Tespit (26.10.2026)** | Arayüzün veri ambarı (`data/dashboard_scenarios.csv/json`, 1920 senaryo) tamamen **v1 motorundan** üretilmiştir ve v2 düzeltmelerinden sonra **geçersizdir**. |
| **Sapma örnekleri** | 4 araç / α=0,15 / EDD / baz talep → arayüz **%24,58**, v2 **%0,18** (konsolidasyonlu) veya **%0,00** (anında) — **24,4 puan fark**. "%5 eşiği için 8 araç" → v2'de **2–3 araç**. Sevk kuralları farklı görünüyor → v2'de **istatistiksel olarak eşdeğer** (p=0,9997). |
| **Risk** | Arayüz tez savunmasında veya sunumda gösterilirse **yanlış bilgi verir**. |
| **Uygulanan geçici önlem** | `index.html` ve `dashboard.html` dosyalarına kapatılabilir **uyarı bandı** eklendi (`#v1-uyari-bandi`); stiller `style.css` ve gömülü `<style>` bloğuna işlendi. Gömülü JS `node --check` ile doğrulandı. |
| **Kalıcı çözüm** | Kademe 1 / D1: `src/generate_dashboard_data.py` v2 motoruna bağlanıp veri ambarı yeniden üretilmeli; ardından uyarı bandı **kaldırılmalıdır**. |
| **⚠️ Ek bulgu — `make_standalone.py` BOZUK** | Betikteki JavaScript template literal'larının **backtick karakterleri kaybolmuştur** (`const sid = S;` → olmalıydı `` `S${i}` ``; `bar.style.width = ${pct}%;` → `` `${pct}%` ``). Çalıştırılırsa `dashboard.html` sözdizimi hatasıyla üretilir ve arayüz açılmaz. Betiğe **koruma eklendi**: çalıştırıldığında açıklama yazıp durur. Mevcut `dashboard.html` daha önce sağlam üretilmiş sürümdür, korunmuştur. D1 kapsamında betik **yeniden yazılacaktır**. |
| **Dosya** | `docs/akademik_degerlendirme_ve_yol_haritasi.md` Bölüm B |
| **Tarih** | 26.10.2026 |

### K93 — Boyutlandırma Tasarımının Politika Karşılaştırmasına Etkisi ✅ (H2 tamamlandı)
| Özellik | Değer |
|---------|-------|
| **Amaç** | Ana katkıyı **kendi v1 modelimizin dışına taşımak**. Şimdiye kadar politika-tutarsız boyutlandırmanın etkisi yalnızca kendi v1 motorumuzda gösterilmişti; hakem *"kendi hatanızı düzeltmek katkı mı?"* diyebilirdi. |
| **Ele alınan tasarım** | **Vojdani & Drechsler (2022) s.5**: *"Die beiden Systeme weisen ein **identisches Layout und identische Taktzeiten** an den Arbeitsstationen auf"* + *"Die Versorgung der Stationen wird über ein **Zwei-Behälter-Kanban-System** gewährleistet"* → çevrim süreleri farklı (saatlik ↔ ihtiyaca göre), **tampon aynı**. |
| **⚠️ Çerçeveleme** | **Çürütme değil, duyarlılık analizi.** Vojdani'nin modeli yeniden üretilmemiştir (makalede sayısal parametre tablosu yoktur); yeniden üretilen şey **karşılaştırma tasarımıdır**, bu çalışmanın kendi 24 istasyonlu sistemi üzerinde. |
| **Yöntem** | Kurgu A — tüm politikalar $N=2$ (yeni `kanban_modu="IKI_KUTU"`); Kurgu B — her politika kendi formülüyle (VDI/K65). 3 araç, 12 replikasyon, saatlik rejim talebi. |
| **🎯 BULGU** | **Baz talep:** A'da dijital 2,33 puan önde → B'de fark 0,14 puana iner (**kayma 2,19 puan**). **Talep şoku +%50:** A'da dijital **9,03 puan** önde → B'de geleneksel 0,04 puan önde (**kayma 9,07 puan — SIRALAMA DEĞİŞİR**). |
| **Mekanizma** | Kurgu A'da her iki sistem de **48 kart** alır. Kurgu B'de geleneksel sistem **63 karta** çıkar (60 dk çevrim daha büyük tampon gerektirir), dijital **49**'da kalır. Geleneksel sistem hak ettiği tamponu alınca performans farkı kapanır. |
| **✅ Vojdani'nin bulgusu doğrulandı** | Dijital sistem her iki kurguda da **daha az sefer** yapar (−%10 … −%11; Vojdani %−27). **WIP avantajı yalnızca Kurgu B'de görünür hale gelir: −%37 … −%38.** Yani Vojdani'nin taşıma verimliliği bulgusu bu düzeltmeden **etkilenmez**; etkilenen şey duruş karşılaştırmasıdır. |
| **⚠️ Fark** | Mesafede bizim dijital sistemimiz **daha fazla** yol yapar (+%13 … +%69), Vojdani ise −%29,39 raporlar. Nedeni sistem farkıdır (24 istasyon/4 hat ↔ 15 istasyon/3 bölge; bizde bölge atlama yok). Bu fark dürüstçe belirtilmelidir. |
| **Akademik değer** | Katkı artık kendi modelimizin dışına çıkmıştır: **bağımsız bir çalışmada kullanılan karşılaştırma tasarımının** sonucu nasıl etkilediği gösterilmiştir. |
| **Dosya** | `src/v2_boyutlandirma_duyarliligi.py` · `data/synthetic/v2_boyutlandirma_duyarliligi.csv` · `docs/figurler/sekil5_boyutlandirma_duyarliligi.png` |
| **Tarih** | 26.10.2026 |

### K94 — Dashboard v2 Veri Ambarına Geçti (Kademe 1 / D1) ✅
| Özellik | Değer |
|---------|-------|
| **Veri** | `src/generate_dashboard_data_v2.py` → `data/dashboard_scenarios_v2.json/.csv`: 1920 P3 senaryosu (8 araç × 6 α × 5 talep × 2 n_modu × 4 sevk) + 640 statik baz (P1/P2 × T∈{30,60,90,120}), 3 replikasyon, ort. ± %95 GA. |
| **n_modu eşlemesi** | `Dinamik_N` → VDI (politika-tutarlı, K65); `Sabit_N` → V1. Arayüz etiketleri buna göre değiştirildi: **"Politika-tutarlı (VDI)" / "Eski boyutlandırma (V1)"** — tezin ana katkısı arayüzden doğrudan görülebilir. |
| **Statik referans** | Sabit `STATIC_BASELINE_MAP` (v1, 80 dk) yerine yüklemede `statik_baz`'dan türetilir: **P2, T=60 dk, baz talep, VDI** (K93'teki geleneksel sistemle aynı). |
| **Arayüz** | Duruş KPI'larında `± starv_ci95`; altbilgide sürüm damgası (motor, replikasyon, üretim tarihi; ipucunda K82 notu). Uyarı bandı (`#v1-uyari-bandi`) kaldırıldı. |
| **Standalone** | `make_standalone.py` yeniden yazıldı: JSON `window.DASHBOARD_DATA_V2` olarak ayrı `<script>`'te gömülür, app.js'te metin değiştirme yapılmaz (backtick kaybı tekrarlanamaz). `dashboard.html` 844 KB; iki gömülü blok `node --check` geçti. |
| **Doğrulama** | Headless tarayıcı: 4 araç / α=0,15 / EDD / baz → **%0,37 ± 0,12** (v1 arayüzü %24,58 gösteriyordu). |
| **Orkestratör** | `tum_analizleri_calistir` 7 adım; 6/7 veri ambarını üretip `dashboard.html`'i yeniden kurar. |
| **Tarih** | 27.10.2026 |

### K95 — K93 Bulgusunun Toyota Formülü Bandında Sağlamlığı (H6) ✅
| Özellik | Değer |
|---------|-------|
| **Gerekçe** | K88: Toyota formülünün kaynağı (Sugimori vd. 1977, aktaran Kundu vd. 2019 s.422–423) iki sınır verir — α < %10 ve kutu kapasitesi ≤ günlük talebin %10'u. Proje ikisinin de dışında: α = 0,15; C/günlük talep **%10,4–%17,0 (24/24 istasyon sınır dışı)**. Hakem sorusu: *K93'teki sıralama değişimi bant dışı parametrelerin yan ürünü mü?* |
| **Tasarım** | K93 deneyi (kurgu A ortak iki kutulu tampon ↔ B politika-tutarlı; geleneksel P2 T=60 ↔ dijital P3 konsolidasyon; 3 araç) şu ızgarada tekrarlandı: α ∈ {0; 0,05; 0,10; 0,15; 0,20} × C ∈ {mevcut; Toyota C_i = ⌊0,10·8·D_i⌋ (8…19 adet), Q sabit 25 kutu; Toyota C, Q hacim-eşdeğer 34 kutu} × talep {baz, +%50} × 12 replikasyon (1440 koşu, 1,4 dk). |
| **🎯 Bulgu 1 — sağlam** | **Kayma (fark_B − fark_A) 30/30 hücrede pozitif**: politika-tutarlı boyutlandırma her koşulda geleneksel sistemin görünen dezavantajını azaltır. Mevcut C'de kayma α ile artar (baz +1,33…+2,45; şok +3,98…+10,97). |
| **🎯 Bulgu 2 — bantta daha güçlü** | Toyota bandı içinde (α ≤ 0,10, Toyota C) kayma **baz +10,24…+10,49, şok +15,81…+18,07** puan; **sıralama 12/12 bant hücresinde değişir**. K93 etkisi bant dışı parametrelerin yan ürünü değildir; tersine, bant dışı parametreler etkiyi **küçük gösteriyordu**. |
| **⚠️ Bulgu 3 — trade-off, bedava kazanç değil** | Toyota C / kurgu B / şokta iki sistem de **72 kart** alır (eşit tampon), ama geleneksel %5,5, dijital %17,2 duruş verir. Geleneksel bunu rafı her saat tepeye doldurarak, **%67 daha fazla WIP** (405 ↔ 242) taşıyarak elde eder. Doğru okuma: küçük kutularda ROP tetiklemeli dijital sistem şoka karşı daha kırılgandır (ROP tasarım talebiyle sabit; K74 dinamik ROP bu deneyde kapalı). Bu, duruş–WIP Pareto'sunda farklı bir noktadır, mutlak üstünlük değildir. |
| **Q** | Q sabit ve Q hacim-eşdeğer **duruşta özdeş**: araç doluluğu hiçbir hücrede %57'yi aşmaz, konsolidasyon son tarihe göre kalkar → Q bağlayıcı değildir. |
| **Tezde kullanım** | α = 0,15 ve C tercihi için: "Sonuçlar Toyota bandında yön değiştirmez, etki büyür" (Şekil 6). K82'deki anlamsız α ana etkisi yalnızca P3/VDI içindir; boyutlandırma tasarımıyla etkileşimde α belirgindir (mevcut C, şok: +3,98 → +10,97). |
| **Sınır** | Tek ağ, tek filo (3 araç), 8 saatlik vardiya; dijital sistemde ROP talep şokuna uyarlanmıyor. |
| **Dosya** | `src/v2_toyota_bandi_duyarliligi.py` · `data/synthetic/v2_toyota_bandi_{ham,ozet}.csv` · `docs/figurler/sekil6_toyota_bandi_sagligi.png` |
| **Tarih** | 27.10.2026 |

### K96 — Ara Denetim: "13,6 Puan" Errata'sı, Formül Atfı ve Kaynakça ✅
| Özellik | Değer |
|---------|-------|
| **Bulgu 1 — çelişki** | Belgelerde hem "yeterli filoda dinamik 13,6 puan önde" hem "politikalar arası gerçek fark ≈1 puan" yazıyordu. 13,6'nın kaynağı Hafta 14 rapor 6.2 tablosu (P3 %0,21 ↔ P1 T=60 %13,78, WIP≈404). Güncel `v2_politika_izgara.csv`'de P1 T=60, 3 araç **%0,09 / 834 WIP**; tablodaki değer güncel ızgarada yeniden üretilemedi (V1 boyutlandırmayla da: %5,79 / 232 WIP). **⚠️ Düzeltme (K97):** eşit WIP karşılaştırması statik sistemin kartları azaltılarak kurulabilir; K97 D kuralında dijital baz talepte **10,88**, şokta **15,15 puan** öndedir. Yani 13,6'nın büyüklüğü eşit WIP kuralı altında makuldür; hata, bunun kurala bağlı olduğunun belirtilmemesidir. |
| **Doğru ifade** | Politika-tutarlı boyutlandırmada (K97 kural B) yeterli filoda tüm politikalar %0–0,6 duruştadır; P3 konsolidasyon %0,18'i **413 WIP**, P2 T=45 %0,55'i 467, P2 T=60 %0,49'u 673 WIP ile sağlar. **Dinamik üstünlük duruşta değil stoktadır.** |
| **Düzeltilen yerler** | `tez_bilgi_rehberi.md` (özet tablo, katkı 1) · `literatur_boslugu_analizi.md` 4.1.5 (K93/K95'e dayandırıldı) ve Bölüm 7 (Bocewicz/Kundu edinildi, Sugimori eklendi) · `hafta8_kanban_karsilastirma_raporu.md` · `hafta14_…raporu.md` (özet + 6.2'ye errata kutusu; tablo tarihsel kayıt olarak korundu) |
| **Bulgu 2 — formül atfı** | `tez_bilgi_rehberi.md` K06 satırı hâlâ Elloumi/Simić gösteriyordu → **Sugimori vd. (1977), aktaran Kundu vd. (2019)** (K88). |
| **Bulgu 3 — kaynakça** | [1]–[11] künyeleri katalogdan dolduruldu ve okundu işaretlendi; [15] yanlış yazar ("M. W. P. Solomon") ve arşivde olmayan esere işaret ediyordu → arşivdeki Larsen, Madsen & Solomon (2008) ile değiştirildi; metinde alıntılanıp listede olmayan [24]–[31] ve yöntem kaynakları [32]–[38] (Solomon 1987, Croes 1958, OR-Tools, Welch 1983, Law 2015, Montgomery, Floyd 1962) eklendi. "Doğrulanmalı" notlu alanlar tam metinden kontrol edilmeli. |
| **Rapor** | Denetim artifact'ı: https://claude.ai/artifact/MC78BkVvUUvG6bn8hbcTKj |
| **Tarih** | 27.10.2026 |

### K97 — Politika Karşılaştırmasında Dört Adalet Kuralı (Y1 + Y2) ✅
| Özellik | Değer |
|---------|-------|
| **Amaç** | Ana katkıyı "hata düzeltme"den **başkalarının kullanabileceği bir karşılaştırma çerçevesine** taşımak. Yazında politikalar dört farklı biçimde eşitlenir; hiçbir çalışma bunları yan yana koymaz. |
| **Kurallar** | **A** eşit kart (Vojdani & Drechsler 2022 s.5) · **B** politika-tutarlı formül (Urru vd. 2018; VDI 5586; K65) · **C** eşit hizmet düzeyi — hedef duruşu (≤ %1, "fill rate ≥ %99" vekili) sağlayan en küçük tampon, sonra WIP karşılaştırılır (Alnahhal & Noche 2015 s.117) · **D** eşit WIP — dijitalin B WIP'inde, geleneksel eğride ara değerleme (K53, K95) |
| **Yöntem** | Geleneksel (P2, T=60) ve dijital (P3, konsolidasyon); 3 araç; her sistem için $N_i = \max(1, N_i^{VDI}+k)$, $k=-3…+6$ → duruş–WIP eğrisi; 12 replikasyon. Kurallar aynı iki eğri üzerinde dört noktadır. Motor: `V2Parametre.n_ozel` (eski davranış birebir korunur, doğrulandı). |
| **🎯 Mevcut kutular** | Duruş kazananı: A dijital (−2,33 / şok −9,03), **B eşit**, C dijital (WIP −%59 / −%10), D dijital (**−10,88 / −15,15**). Y2 Pareto: A, B, D'de dijital baskın; C'de takas. Tek ölçütlü fark kurala göre **−15,15 … +0,04 puan** arasında değişir. |
| **🎯 Toyota kutuları (K95)** | A dijital, **B geleneksel** (baz +0,13 — sınırda, GA ±0,13; şok **+12,07**), C dijital (baz) / eşit (şok), D dijital. **Kazanan kurala göre değişir: şokta 3 farklı sonuç.** Pareto da kurala göre "dijital baskın", "takas" ve "geleneksel baskın" arasında değişir. |
| **Yorum** | "Hangi politika daha iyi?" sorusunun cevabı, karşılaştırmanın nasıl adil kılındığına bağlıdır. Bir karşılaştırma çalışması kullandığı eşitleme kuralını açıkça belirtmeli ve mümkünse sonuçları duruş–WIP düzleminde (Pareto) vermelidir. Bu, makalenin önerilen **metodolojik ilkesidir**. |
| **Sınır** | Tüm istasyonlara aynı $k$ (istasyon bazında optimum aranmadı); C'de hizmet düzeyi zaman bazlı duruşla temsil edildi; tek ağ, 3 araç. |
| **Dosya** | `src/v2_adalet_kurallari.py` (`--kutu toyota`) · `data/synthetic/v2_adalet_{egriler,kurallar,kazanan}[_toyota].csv` · `docs/figurler/sekil7_adalet_kurallari[_toyota].png` |
| **Tarih** | 27.10.2026 |

### K98 — Uyarlanan ROP: Dijital Sistemin Şok Kırılganlığı Gerçek mi? (Y4) ✅
| Özellik | Değer |
|---------|-------|
| **Soru** | K95/K97'de Toyota kutularında ve şokta dijital sistem (P3) %17,6, geleneksel (P2 T=60) %5,5 duruş veriyordu. P3'ün ROP'u tasarım talebiyle sabitti. ROP gerçekleşen talebe uyarlanırsa (K74; Elloumi vd. 2025 uyarlanabilir Kanban) fark kapanır mı? |
| **Tasarım** | Dijital sabit · yalnız ROP uyarlanan (N sabit) · N+ROP uyarlanan (K74 tam) · geleneksel; mevcut ve Toyota kutuları × baz/şok; 3 araç, 12 replikasyon. Ayırt edici ölçüt **eğri kazancı**: uyarlanan noktanın, K97 dijital kart taraması eğrisine göre aynı WIP'teki duruş farkı (kazanç > GA → aynı stokla gerçek iyileşme). |
| **🎯 Toyota · şok** | Uyarlama duruşu 17,62 → **13,50** (yalnız ROP) / 14,02 (N+ROP) indirir, ama eğri kazancı +0,46 / +0,07 (GA içinde) → **eğri boyunca kayma, yani kart eklemekle eşdeğer.** Geleneksel hâlâ **+7,96 puan** önde. **Kırılganlık model kısıtı değil, küçük kutularda gerçek bir politika özelliğidir.** |
| **🎯 Eğriler kesişir** | Toyota · şokta iki sistemin duruş–WIP eğrileri ≈350 WIP'te kesişir: altında dijital, üstünde geleneksel daha düşük duruş verir (geleneksel nokta dijital eğrisinin 1,99 puan altında). Hangi politikanın iyi olduğu **stok bütçesine** bağlıdır — K97 Pareto ilkesinin doğrudan örneği. |
| **🎯 Mevcut · şok** | N+ROP uyarlama sınırda gerçek iyileşme verir (kazanç +1,02, GA ±0,82): duruş 4,50 → 2,11; dijital geleneksele göre **−2,34 puan** ve **−%17 WIP** → iki ölçütte de önde. |
| **Baz talep** | Uyarlama hafif zararlı (mevcut 0,17 → 0,35; Toyota 0,32 → 0,62): 60 dk'lık pencereden D tahmini gürültülüdür ve ROP'u dalgalandırır. Uyarlama yalnızca gerçek düzey değişiminde fayda sağlar. |
| **Tezde kullanım** | "e-Kanban'ın bilgi avantajı" iddiası koşulludur: talep düzeyi değiştiğinde ve kutular büyük olduğunda gerçek iyileşme sağlar; küçük kutularda ek stoktan farksızdır. Uyarlanabilir Kanban'ın değeri (Elloumi vd. 2025) bu çalışmada kutu boyuna bağlı bulunmuştur. |
| **Sınır** | Uyarlama yalnız dijitale verildi (geleneksel de periyodik yeniden boyutlandırılabilir); şok koşu boyunca sabit düzey kaymasıdır (ani adım değil); pencere 60 dk / periyot 30 dk sabit. |
| **Dosya** | `src/v2_uyarlanan_rop.py` · `data/synthetic/v2_uyarlanan_rop.csv` · `docs/figurler/sekil8_uyarlanan_rop.png` |
| **Tarih** | 27.10.2026 |

### K99 — Kararlı Durum ve Çok Vardiyalı Ufukta Sağlamlık (H4) ✅ · ⚠️ Gösterge Kararı
| Özellik | Değer |
|---------|-------|
| **Tespit** | Motorun `starv_pct` ve `ort_wip` göstergeleri **ısınma dönemini içerir** (duruş / (T·n); WIP tüm dakikaların ortalaması). K78 ısınmayı 90 dk ölçmüş, ancak K93–K98 göstergeleri bu dönemi dışlamamıştır. Motor `starv_pct_isinma_sonrasi`'nı zaten hesaplıyordu, kullanılmamıştı. |
| **Tasarım** | K93 karşılaştırması (A ↔ B, geleneksel ↔ dijital, 3 araç, 12 rep) × ufuk {480, 1440 dk} × gösterge {tüm koşu, ısınma sonrası} × kutu {mevcut, Toyota} × talep {baz, +%50}. |
| **Isınma yanlılığı** | 480 dk'da duruş **0,04–3,87 puan düşük** (ort. 1,15), WIP **%5–37 yüksek** görünür (en büyük: Toyota · şok · dijital B, 243 ↔ 177). 1440 dk'da yanlılık ≈ üçte birine iner (duruş ort. 0,40, WIP ≤ %12,8). |
| **🎯 Sağlamlık** | **Kayma 16/16 birleşimde pozitif** ve ufuk/kararlı durumla büyür (mevcut şok +9,07 → +10,57; Toyota şok +17,25 → +19,01). Toyota kutularında **sıralama 8/8 birleşimde değişir**. Göreli WIP farkları korunur veya güçlenir (mevcut B −%39 → −%41; Toyota şok B −%40 → −%53). |
| **⚠️ İnce ayar** | Mevcut kutularda uzun ufukta kural B'de dijital küçük ama anlamlı farkla öndedir (baz −0,25 ± 0,10; şok kararlı durumda −0,50 ± 0,46). Mevcut kutular için doğru ifade "sıralama değişir" değil, **"fark %90–95 küçülür"**dür (−2,92 → −0,25; −11,07 → −0,50). Toyota kutularında ise sıralama her koşulda değişir. |
| **Karar** | (1) K93–K98'in **göreli** sonuçları geçerlidir, yeniden üretilmesi gerekmez. (2) Tez/makale tablolarında **mutlak** duruş ve WIP değerleri **ısınma sonrası** göstergeyle verilmeli; bu yapılmadıysa tablo başlığında "tüm koşu (ısınma dahil)" yazılmalıdır. (3) Motorun varsayılan göstergesi geriye uyumluluk için değiştirilmedi; ileride değiştirilirse dashboard ambarı yeniden üretilmelidir. |
| **Dosya** | `src/v2_cok_vardiya.py` · `data/synthetic/v2_cok_vardiya_{ham,ozet}.csv` |
| **Tarih** | 27.10.2026 |

### K100 — Koordinat Tabanlı Mesafe Ağı (H3) ✅ · Vojdani Çelişkisi Çözüldü
| Özellik | Değer |
|---------|-------|
| **Sorun** | `distances.csv` hiçbir yerleşimden türetilmemiştir, 286 yönlü çiftte üçgen eşitsizliğini ihlal eder (K71: Floyd–Warshall geçici çözüm; S5, S10). |
| **Yerleşim** | Depo (0,0); 4 paralel hat × 6 istasyon; **dikdörtgensel ölçü** (Sevim & Görkemli Aykut 2026, Denk. 3). Durak aralığı **s = 124/6 ≈ 20,7 m** — Urru vd. (2018) s.406: *"5 stops ... equally distributed along the route. The route is 124 meters long"*. Hat aralığı w = 2·s **mühendislik varsayımıdır** (kaynak yok). İki ölçek: KOMPAKT (Urru ölçeği, depo ort. 114 m) ve GENIS (depo ort. mevcut matrise eşit, 160 m). Üçgen ihlali: 0. |
| **⚠️ Kaynak düzeltmesi** | Yol haritasındaki "istasyon aralığı literatür bandı 25–53 m" ifadesinin hiçbir belgede kaynağı yoktur; kullanılmamalıdır. Kaynaklı değer Urru (2018)'den ≈20,7 m'dir. |
| **⚠️ Veri notu** | `stations.csv`'de `sira_no` global numaralıdır (1–24), hat içi sıra değildir; betik hat içi sırayı türetir. |
| **🎯 Sağlamlık** | K93 kayması gerçekleşebilir ağda da pozitiftir: baz +1,77 / +1,88, şok +7,79 / +7,97 (mevcut matris: +2,19 / +9,07). Kural B'de dijital küçük ama anlamlı farkla öndedir (baz −0,11 ± 0,10; şok −0,93 ± 0,38) → K99 ile aynı: mevcut kutularda **fark %90 küçülür**, sıralama değişmez. WIP avantajı aynıdır (−%36…−%40). |
| **🎯 Vojdani çelişkisi çözüldü** | Mevcut matriste dijital sistem baz talepte geleneksele göre **+%13 yol** yapıyordu (Vojdani & Drechsler 2022: **−%29,39**). Koordinat ağında: **−%21…−%23 sefer, −%6…−%8 yol** → yön Vojdani ile aynıdır. Önceki çelişki metrik olmayan matrisin yan ürünüdür. Şokta dijital daha fazla sefer/yol yapar (+%20…+%37); Vojdani şok koşmamıştır. |
| **Mutlak mesafe** | Mevcut matris vardiya başına yolu ≈2,5–3,5 kat büyük gösterir (geleneksel 34,9 km ↔ 10,1–14,3 km). Mesafe KPI'ları mutlak olarak raporlanacaksa koordinat ağı kullanılmalıdır. |
| **Karar** | Motor varsayılanı değiştirilmedi (tüm önceki sonuçlar ve dashboard ambarı mevcut matrise dayanır). **Öneri:** tezin nihai koşuları koordinat ağıyla (KOMPAKT) yapılmalı; o noktada dashboard ambarı yeniden üretilmelidir. `literatur_boslugu_analizi.md` 10.4'teki "mesafede bizim dijital sistemimiz daha fazla yol yapar" dürüstlük notu bu bulguyla güncellenmelidir. |
| **Dosya** | `src/v2_koordinat_agi.py` · `data/synthetic/v2_koordinat_agi_{ham,ozet}.csv` |
| **Tarih** | 27.10.2026 |

### K102 — Dashboard Kademe 2: Ana Katkı Panelleri ve Kalan v1 Kalıntıları ✅
| Özellik | Değer |
|---------|-------|
| **⚠️ K94 sonrası kalan v1 kalıntıları** | K94 veri ambarını bağlamıştı, ancak HTML/JS'e gömülü sabit v1 değerleri kalmıştı: "Statik vs Dinamik" sekmesinin tüm tabloları (%19,31 / %24,58 / 36 sefer / 54 km), filo grafiğinin statik çizgisi `[25.77 … 18.68]`, yükleme yer tutucuları (%24,58, "2,832 dk", "+5,27 puan"), başlık notu ("seed=42 … fark 3–5 puan"), otomatik yorum ("fark +3,06 puan", "%5 eşiği için 8 araç"), `STATIC_BASELINE_MAP` v1 yedeği. Hepsi kaldırıldı veya veriye bağlandı. |
| **⚠️ Uydurma gösterge** | Doluluk KPI'ı veriden değil `100 − duruş × 0,8` formülünden hesaplanıyordu (≈%99 gösteriyordu). Artık senaryonun gerçek `doluluk_pct` değeri gösterilir (baz: %32,7). |
| **⚠️ Geçersiz JSON** | `dashboard_scenarios_v2.json` ablation satırlarında `NaN` içeriyordu; standalone'da (JS sabiti) sorun çıkmıyor, ancak `index.html` sunucudan açılınca `response.json()` hata verirdi. Üreticiye `_nan_temizle` + `allow_nan=False` eklendi; mevcut ambar yerinde düzeltildi. |
| **Yeni sekme** | "⚖️ Politikalar & Ana Katkı" (eski "Statik vs Dinamik" yerine): **D4** P1/P2/P3 tablosu — filo/talep/boyutlandırma seçilir, her politika kendi kart sayısıyla ve ± %95 GA ile gösterilir · **K97** dört adalet kuralı — kutu boyu ve talep seçilir, duruş–WIP eğrileri ve kural noktaları (aynı noktalar "B=D" biçiminde) + kazanan/Pareto tablosu · **D6** etkileşimli Pareto — politika filtreleri, görünür noktaların cephesi, tıklanan noktanın ayrıntısı · **D5** ayrıştırma — adımlar açılıp kapatılır, seçili adımların toplam etkisi yazılır (yaklaşık olduğu belirtilir). |
| **Otomatik yorum** | Veriden üretilir: duruş ± GA, statik referansla fark (< 0,5 puan ise "pratikte aynı"), %5 eşiğine inen en küçük filo (veride 2 araç), K96/K97 cümlesi. What-If yorumu artık "α'yı yükseltin" önermez (K82). |
| **Veri** | Ambara `adalet` bölümü eklendi (`adalet_ozeti()`: mevcut + Toyota kutuları, eğriler/kurallar/kazananlar). |
| **Doğrulama** | `node --check` (app.js + standalone'daki 2 gömülü blok) geçti; headless tarayıcıda tüm paneller veriyle doldu (P1/P2/P3 9 satır, K97 4 satır, ayrıştırma %6,85 → %0,09). |
| **Tarih** | 27.10.2026 |

### K101 — Rotalama Sezgiseli: Çevrimdışı Tam Bilgi Referansı (H5) ✅
| Özellik | Değer |
|---------|-------|
| **Soru** | Solomon'da sezgisel OR-Tools'tan %101,8 geridedir (S8), ama Solomon statik 100 müşterili bir problemdir. Fabrika senaryosunda rotalama ne kadar iyi? |
| **Yöntem** | Bir P3 koşusundaki tüm siparişler (istasyon, sinyal zamanı, son teslim, kutu) kaydedilip OR-Tools (GLS, 15 sn) ile çevrimdışı VRPTW olarak çözüldü. Gevşetmeler: siparişler önceden bilinir; filo eşzamanlılığı yok (sınırsız sanal araç); depodan erken çıkış serbest. Motorla aynı: 90 dk tur süresi sınırı (K72), yumuşak son teslim (gecikme cezası 10 dk-eşdeğeri), Q=25, 3 dk durak servisi. 2 ağ × 2 talep × 2 sevk × 2 tohum. Motorda `_siparisler` kaydı eklendi (geriye uyumlu). |
| **⚠️ Tasarım düzeltmeleri** | (1) Tur süresi sınırı olmadan sanal bir araç bir istasyonda saatlerce bekleyip ardışık siparişleri sıfır mesafeyle topluyordu (11,0 km, anlamsız sınır) → K72 sınırı eklendi. (2) GLS sezgiseldir ve süre sınırında yakınsamaz (10 sn 30,9 km → 30 sn 24,0 km); sonuç **kanıtlanmış alt sınır değildir** → "çevrimdışı tam bilgi referansı" olarak adlandırıldı. |
| **🎯 Baz talep · konsolidasyon** | Sezgisel referanstan **%62–69 fazla yol** yapar, ancak **daha az gecikme** verir (mevcut ağ 3,0 ↔ 8,5; koordinat ağı 1,5 ↔ 2,0 gecikmeli teslim). |
| **🎯 Talep şoku** | Referans mesafeyi düşürmek için **94–121 teslimi geciktirir**; sezgisel 0–4,5. Bu koşulda iki çözüm karşılaştırılabilir değildir. Koordinat ağında konsolidasyonlu sezgisel hem **daha kısa yol** (−%17) hem sıfır gecikme verir. |
| **ANINDA sevk** | Açık büyüktür (+%39 … +%346): tasarım gereği her sinyalde araç kalkar (114–126 tur). Konsolidasyonun taşıma verimliliği katkısı (K82: doluluk +20 puan) bu tabloyla tutarlıdır. |
| **Yorum** | Sezgisel zamanında teslimi önceliklendirir; tam bilgiyle bile mesafe kazancı yalnızca baz talepte ve gecikme pahasına ≈%60–70 düzeyindedir. Solomon'daki %101,8'lik açık fabrika senaryosuna doğrudan taşınamaz. **S8 sınırlılığı daralır ama kapanmaz:** çevrimiçi optimum bilinmemektedir. |
| **Sınır** | 2 tohum, 15 sn; mesafe–gecikme takası ceza ağırlığına bağlıdır; referans gevşetilmiş problemdir. |
| **Dosya** | `src/v2_ortools_referansi.py` · `data/synthetic/v2_ortools_referansi_{ham,ozet}.csv` |
| **Tarih** | 27.10.2026 |

---

*Bu dosya her yeni kararla güncellenir.*
*Kaynak gösterilemeyen hiçbir değer projeye dahil edilmez.*
*⚠️ Tüm analizler SENTETİK veriyle yapılmaktadır. Gerçek veri için config.json → "real".*
