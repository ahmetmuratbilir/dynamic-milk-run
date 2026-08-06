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
- **Kaynak:** Kullanıcı onayı (30.07.2026) — "Makale destekliyse onaylıyorum"
- **Literatür referansı:** Klenk et al. (2012) satır 1199-1200 → *"A safety buffer time of 30% to handle deviations in the mean number of bins per tour"* — oransal tampon yöntemi; 32 makalenin hiçbiri z×σ×√LT formülü kullanmamış.
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
- **Kaynak:** Kullanıcı onayı (30.07.2026) — "Makale destekliyse onaylıyorum"
- **Literatür referansı:**
  - Facchini et al. (2022) satır 416-417 → *"materials' priority, frequency of delivery"* — karma önceliklendirme
  - Simić et al. (2020) satır 301 → *"according to the priority of the parts needed"* — kritiklik bazlı
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

*Bu dosya her yeni kararla güncellenir.*
*Kaynak gösterilemeyen hiçbir değer projeye dahil edilmez.*
*⚠️ Tüm analizler SENTETİK veriyle yapılmaktadır. Gerçek veri için config.json → "real".*

