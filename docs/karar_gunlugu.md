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

*Bu dosya her yeni kararla güncellenir.*
*Kaynak gösterilemeyen hiçbir değer projeye dahil edilmez.*
*⚠️ Tüm analizler SENTETİK veriyle yapılmaktadır. Gerçek veri için config.json → "real".*
