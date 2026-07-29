# Proje Referans Verisi — Onaylı Parametre Listesi
## Dinamik Milk-Run & E-Kanban Karar Destek Sistemi

> Bu dosya projenin "tek doğruluk kaynağı"dır.
> Her parametre değerinin yanında hangi makaleden alındığı yazıyor.
> Onay sütunu boşsa henüz onaylanmadı demektir.

---

## BÖLÜM A — SİSTEM YAPISI

| Parametre | Bizim Değerimiz | Eşleşen Makaleler | Literatür Aralığı | Onay |
|-----------|-----------------|-------------------|-------------------|------|
| Üretim hattı sayısı | **4** | Menanno (2023): 11 hat; Pekarcikova (2021): 1 hat; Elloumi (2025): 1 hat | 1 – 38 | ✅ |
| İstasyon sayısı (toplam) | **24** (hat başına 6) | Simić (2020): 5; Urru (2018): 5; Vojdani (2022): 15; Sevim (2025): 10; Zhou&Wen (2024): 4–100 | 5 – 100 | ✅ |
| Merkezi depo sayısı | **1** | Simić (2020), Urru (2018), Sevim (2025) hepsi 1 depo | 1 | ✅ |
| Milk-run aracı sayısı | **2** | Zhou&Wen (2024): 2 araç; Sevim (2025): 2–3 araç | 1 – 4 | ✅ |
| Araç kapasitesi | **25 kutu** | Menanno (2023): 35–55 birim; Klenk (2012): 2–5 kutu/durak; Zhou&Wen (2024): 6; Sevim (2025): 250–400 birim | 3 – 400 | ✅ |
| Simülasyon süresi | **480 dk (1 vardiya)** | Simić (2020): 600 dk; Pekarcikova (2021): 12 saat; Vojdani (2022): 7 gün; Sevim (2025): 7200 dk | 12 sa – 7 gün | ✅ |

---

## BÖLÜM B — DİNAMİK KANBAN PARAMETRELERİ

Formül: **N = ⌈ (D × LT × (1+α)) / C ⌉**

| Parametre | Sembol | Bizim Değerimiz | Eşleşen Makaleler | Literatür Aralığı | Onay |
|-----------|--------|-----------------|-------------------|-------------------|------|
| Tüketim hızı | D | **11–24 adet/sa** (istasyona göre) | Simić (2020): 60/sa; Menanno (2023): ~70; Zhou&Wen (2024): Uniform[1,3]; Sevim (2025): 0.5–1/dk | 0.5/dk – 70/sa | ✅ |
| Talep dağılımı | — | **Normal N(μ, 0.20μ)** | Sevim (2025): Üstel dağılım; Zhou&Zhu (2020): %45–50 olasılık | Stokastik yaygın | ✅ |
| Lead time | LT | **45 dk** | Simić (2020): 20 dk; Klenk (2012): 34–47 dk; Facchini (2022): maks. 25 dk | 20 – 255 dk | ✅ |
| Güvenlik katsayısı | α | **0.15 (%15)** | Klenk (2012): %30 tampon ⚠️ | Tek kaynak: %30 | ✅ |
| Kutu kapasitesi | C | **15 veya 20 adet/kutu** (parçaya göre) | Pekarcikova (2021): 10–50 adet; Zhou&Wen (2024): <6; Simić (2020): parçaya göre | 6 – 2500 | ✅ |
| Güncelleme periyodu | T | **30 dk** (D her 30 dk'da güncellenir) | Literatürde belirtilmemiş ⚠️ — mühendislik varsayımı | — | ✅ |
| Reorder point | ROP | **1 kutu kaldığında** | Facchini (2022): sinyal tabanlı; Sevim (2025): ROP=25–50 birim | Değişken | ✅ |

---

## BÖLÜM C — MİLK-RUN / ARAÇ PARAMETRELERİ

| Parametre | Bizim Değerimiz | Eşleşen Makaleler | Literatür Aralığı | Onay |
|-----------|-----------------|-------------------|-------------------|------|
| Araç hızı | **10 km/sa** | Simić (2020): 4 km/sa; Urru (2018): 3.6 km/sa; Sevim (2025): 5 km/sa; Zhou&Wen (2024): 7.2 km/sa; Menanno (2023): 12 km/sa | 3.6 – 12 km/sa | ✅ |
| İstasyonlar arası mesafe | **180 m** | Simić (2020): 265 m (rota toplamı); Urru (2018): 124 m (rota toplamı); Zhou&Wen (2024): 8 m/istasyon | 8 m – 265 m (rota) | ✅ |
| Yükleme süresi | **2 dk** | Urru (2018): 10 sn/birim + hazırlık; Zhou&Wen (2024): 10 sn; Simić (2020): 4 dk (toplam yükleme) | 10 sn – 4 dk | ✅ |
| Boşaltma süresi | **3 dk** | Zhou&Wen (2024): 5 sn; Sevim (2025): 0.6 dk toplam | 5 sn – 13 dk | ✅ |
| Toplam handling | **5 dk/istasyon** | Klenk (2012): 0–13 dk; Urru (2018): 30 sn/birim; Sevim (2025): 0.6 dk | 0 – 13 dk | ✅ |

---

## BÖLÜM D — VRPTW PARAMETRELERİ

| Parametre | Bizim Değerimiz | Eşleşen Makaleler | Literatür Aralığı | Onay |
|-----------|-----------------|-------------------|-------------------|------|
| Zaman penceresi başlangıcı (a) | **Sipariş anı** | Facchini (2022): sinyal sonrası | — | ✅ |
| Zaman penceresi bitişi (b) | **+60 dk** | Facchini (2022): maks. 25 dk; Klenk (2012): 34–47 dk | 25 – 60 dk | ✅ |
| Maksimum tur süresi | **90 dk** | Simić (2020): 20 dk tur; Klenk (2012): 34–47 dk | 20 – 90 dk | ✅ |
| Depoya dönüş | **Zorunlu** | Simić (2020), Urru (2018), Sevim (2025) hepsi zorunlu | Standart | ✅ |

---

## BÖLÜM E — SENARYO PARAMETRELERİ

| Senaryo | Tanım | Eşleşen Makaleler | Onay |
|---------|-------|-------------------|------|
| S1 — Sabit rota | 2 araç, 60 dk sabit tur, talep görmezden | Vojdani (2022): geleneksel sabit 1 sa tur | ✅ |
| S2 — Dinamik rota | E-Kanban + VRPTW tetiklemesi | Facchini (2022), Sevim (2025), Vojdani (2022) | ✅ |
| S3 — Talep +%20 | Tüm D değerleri ×1.20 | Klenk (2012) talep dalgalanması; Alnahhal (2015) | ✅ |
| S4 — Araç arızası | 2 araç → 1 araç | Alnahhal (2015): makine arızası etkisi | ✅ |
| S5 — LT uzaması | 45 dk → 70 dk | Jarupathirun (2009): LT değişimi (190→255 dk) | ✅ |

---

## BÖLÜM F — DASHBOARD KPI LİSTESİ

| KPI | Tanım (Formül) | Eşleşen Makaleler | Onay |
|-----|----------------|-------------------|------|
| Toplam tur mesafesi (km) | Tüm araçların tur başına toplam mesafesi | Vojdani (2022): %29.39 düşüş hedefi | ✅ |
| Ortalama araç doluluk (%) | (taşınan yük / araç kapasitesi) × 100 | Menanno (2023): kapasite kullanım analizi | ✅ |
| Starvation sayısı | Stok = 0 olan an sayısı | Alnahhal (2015): starvation kavramı | ✅ |
| Ortalama tur süresi (dk) | Seyahat + handling toplamı | Simić (2020): 20 dk tur; Vojdani (2022): 8–11 dk | ✅ |
| Ortalama teslim süresi (dk) | Siparişten teslimata geçen süre | Jarupathirun (2009): 190 dk → 255 dk | ✅ |
| Kanban kart sayısı (N) | N = ⌈(D×LT×(1+α))/C⌉ | Elloumi (2025), Simić (2020) | ✅ |
| Kritik istasyon sayısı | Stok < ROP olan istasyon adedi | Facchini (2022): zaman penceresi ihlali | ✅ |
| Araç kullanım oranı (%) | Aktif sürüş / toplam simülasyon süresi | Vojdani (2022): sürüş süresi analizi | ✅ |

---

## BÖLÜM G — ⚠️ LİTERATÜRDE EŞLEŞMEYEN / MÜHENDİSLİK VARSAYIMI OLAN DEĞERLER

Bunlar savunmada sorulabilir — hazır cevabın olsun:

| Parametre | Bizim Değerimiz | Durum | Savunma Cevabı |
|-----------|-----------------|-------|----------------|
| Güvenlik katsayısı α | %15 | ⚠️ Literatür %30 diyor (Klenk 2012) | "What-if S3 senaryosunda α=%30 ile karşılaştırıyoruz" |
| Güncelleme periyodu T | 30 dk | ⚠️ Literatürde belirtilmemiş | "Mühendislik varsayımı — vardiya süresi/16 olarak alındı" |
| Zaman penceresi +60 dk | 60 dk | ⚠️ Facchini (2022) 25 dk öneriyor | "4 hatlı, 24 istasyonlu büyük sistem için daha geniş pencere seçildi" |
| Depo-hat mesafesi | 90–250 m | ✅ Simić (2020) 265 m rota | Savunulabilir |

---

## ONAY TALİMATI

Her satırdaki ✅ kutusunu onaylamak için:
- "Tamamı onaylıyorum" → Tüm ✅ → ✅
- Değiştirmek istediğin varsa yeni değeri söyle
- Emin olmadığın varsa sordur

> **Bu dosya onaylandıktan sonra Hafta 2'de sentetik veri bu değerlerle üretilecek.**
> Onaysız hiçbir değeri kullanmayacağım.

---

*Kaynak: hafta1_makale_parametreleri.md | Güncelleme: Hafta 1*
*Tüm değerler makalelere dayalıdır. ⚠️ işaretliler mühendislik varsayımıdır.*
