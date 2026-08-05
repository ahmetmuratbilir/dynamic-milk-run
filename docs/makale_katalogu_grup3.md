# Dynamic Milk-Run & E-Kanban Akademik Makale Kataloğu (Grup 3)

Bu katalog, Dynamic Milk-Run & E-Kanban projesi kapsamında incelenen 11 akademik makalenin özetlerini, metriklerini, kullanılan metodolojileri ve projemizle ilişkilerini içermektedir.

---

## 1. Particle Swarm Optimization Algorithm for Design of an Adaptive Kanban System Based on Optimization via Simulation

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Particle swarm optimization algorithm for design of an adaptive Kanban system based on optimization via simulation |
| **Yazarlar** | Khouloud Elloumi, Achraf Ammar, Mounir Benaissa |
| **Yıl** | 2025 |
| **Dergi / Kaynak** | Journal of Industrial and Production Engineering (Vol. 42, No. 6, pp. 612–624) |
| **Ana Konu** | Dalgalı ve stokastik müşteri talebi altında adaptif kanban sistemlerinin (AKS) parametrelerinin (kanban sayısı, ek kanban sayısı, serbest bırakma ve yakalama eşikleri) simülasyon ve Parçacık Sürü Optimizasyonu (PSO) entegrasyonu ile dinamik olarak optimize edilmesidir. |
| **Metodoloji** | Simülasyon Temelli Optimizasyon (Optimization via Simulation / SimOpt) — Rockwell Arena (v14) Kesikli Olay Simülasyonu ve Python tabanlı Parçacık Sürü Optimizasyonu (PSO) entegrasyonu. |
| **Projemizle İlişkisi** | Adaptif Kanban / E-Kanban mekanizması, Simülasyon Optimizasyonu (Arena-Python entegrasyonu), Değişken talep altında ROP/Kanban kartı ve stok/backorder ceza maliyeti optimizasyonu. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (1 aşamalı / single-stage imalat sistemi) |
| **İstasyon Sayısı** | 10 paralel sunucu (10 parallel servers) |
| **Araç Sayısı** | Belirtilmemiş |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Lead Time (LT)** | İşlem süreleri üstel dağılımlı, ortalama = 6 zaman birimi ($\mu = 1/6$) |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | Poisson süreci; Case 1: $\lambda_d = 1/7$, Case 2: $\lambda_d = 0.2$ (ortalama 5), Case 3: 3'ten 7'ye doğrusal artan/azalan üçgen talep, Case 4: 3, 5, 7 döngüsel (cyclical) talep |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş |
| **Diğer Parametreler** | Karar değişkenleri $X = [K, E, R, C]$ (Kanban sayısı, Ek kanban, Serbest bırakma eşiği, Yakalama eşiği), Backorder ceza maliyeti $b = 500 / 1000$, $K_{max} = 15$, $E_{max} = 10$, Replikasyon uzunluğu: 1.000.000 zaman birimi, Replikasyon sayısı: 30 |

---

## 2. Simulation Testing of the E-Kanban to Increase the Efficiency of Logistics Processes

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Simulation Testing of the E-Kanban to Increase the Efficiency of Logistics Processes |
| **Yazarlar** | Pekarcikova, M.; Trebuna, P.; Kliment, M.; Mizerak, M.; Kral, S. |
| **Yıl** | 2021 |
| **Dergi / Kaynak** | International Journal of Simulation Modelling (IJSIMM, Vol. 20, No. 1, pp. 134–145) |
| **Ana Konu** | Çelik tel/kablo üretimi yapan bir fabrikanın lojistik ve üretim süreçlerindeki darboğazları ve işmiktarlarını azaltmak amacıyla e-Kanban sisteminin Tecnomatix Plant Simulation yazılımı ile modellenmesi ve simülasyon testlerinin yapılmasıdır. |
| **Metodoloji** | Kesikli Olay Simülasyonu (Discrete Event Simulation - DES) ve Yalın Üretim Araçları (Value Stream Mapping - VSM, e-Kanban) — Tecnomatix Plant Simulation 15.2 yazılımı. |
| **Projemizle İlişkisi** | E-Kanban Sinyal Mimarisi, Simülasyon Ortamı (Plant Simulation), Tampon/Buffer yönetimi, WIP azaltma ve fabrika içi lojistik akışının dijitalleştirilmesi. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (Tek bir üretim hattı/akışı) |
| **İstasyon Sayısı** | 9 temel süreç/istasyon (Drumming, Extending, Control diameter, Cabling, Splicing, Packing spool, Control spool, Packing pallet, Expedition) + Frame yapıları |
| **Araç Sayısı** | Belirtilmemiş |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Lead Time (LT)** | Drumming (1:15:00), Extending (4:40:00 - 4:55:00), Control diameter (0:02:00), Cabling (3:10:00 - 3:20:00), Splicing (2:15:00 - 2:25:00), Packing spool (0:06:00), Control spool (0:11:00), Packing pallet (0:09:00), Expedition (0:15:00). Simülasyon süresi: 12 saat (1 vardiya) |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | Müşteri siparişine göre değişken; A_30 ürünü için KanbanBuffer min kapasite 10, max 50, reorder/pull seviyesi 15 adet |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş |

---

## 3. ManPy: An Open-Source Software Tool for Building Discrete Event Simulation Models of Manufacturing Systems

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | ManPy: an open-source software tool for building discrete event simulation models of manufacturing systems |
| **Yazarlar** | Georgios Dagkakis, Ioannis Papagiannopoulos, Cathal Heavey |
| **Yıl** | 2016 |
| **Dergi / Kaynak** | Software: Practice and Experience (Wiley, Vol. 46, No. 7, pp. 955–981) |
| **Ana Konu** | İmalat ve lojistik sistemlerinin kesikli olay simülasyonu (DES) modellerini oluşturmak için Python ve SimPy tabanlı, nesne yönelimli ve açık kaynaklı "ManPy" kütüphanesinin mimarisi, tasarımı ve endüstriyel uygulama alanlarının sunulmasıdır. |
| **Metodoloji** | Nesne Yönelimli Simülasyon Kütüphanesi (Object-Oriented DES Framework) — Python, SimPy ve DREAM platformu entegrasyonu; birim testleri (unit testing) ve optimizasyon rutinleri (ör. PuLP ile LP) entegrasyonu. |
| **Projemizle İlişkisi** | Simülasyon Mimarisi (Python tabanlı açık kaynaklı kesikli olay simülasyonu SimPy/ManPy altyapısı), Python ortamında simülasyon-optimizasyon entegrasyonu ve dynamic milk-run simülatörü geliştirme süreçleri. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (Kütüphane genel amaçlıdır; tıbbi cihaz imalat hattı, kalıp üretim job-shop ve tekstil makinesi imalatı olmak üzere 3 endüstriyel vaka ele alınmıştır) |
| **İstasyon Sayısı** | Belirtilmemiş (Generic nesneler: Source, Queue, Machine, Exit, Conveyer, Assembly vb.) |
| **Araç Sayısı** | Belirtilmemiş |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Lead Time (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | Belirtilmemiş |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş (Conveyer nesnesinde taşıma hızı parametrik tanımlıdır) |

---

## 4. Supply Chain Efficiencies Through E-Kanban: A Case Study

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Supply Chain Efficiencies Through E-Kanban: A Case Study |
| **Yazarlar** | Suprasith Jarupathirun, Andrew P. Ciganek, Thaloengsak Chotiwankaewmanee, Chayanun Kerdpitak |
| **Yıl** | 2009 |
| **Dergi / Kaynak** | International Journal of the Computer, the Internet and Management (Vol. 17, No. SP1, pp. 55.1–55.4) / International Conference on IT |
| **Ana Konu** | Otomotiv yan sanayinde Kokpit Modülü (CPM) üreten bir tedarikçide e-Kanban ve EDI sisteminin uygulanması ve geleneksel Kanban ile karşılaştırmalı performans ve maliyet analizidir. |
| **Metodoloji** | Vaka Çalışması (Case Study) — Gözlem, derinlemesine mülakatlar ve belge incelemesi. |
| **Projemizle İlişkisi** | E-Kanban & EDI Sinyal Mimarisi, Barkod/RFID entegrasyonu, Temin Süresi (Lead Time) ve Stok Maliyeti Azaltımı, Kanban Sirkülasyon Kart Sayısı optimizasyonu. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş |
| **İstasyon Sayısı** | Belirtilmemiş (Lojistik ve üretim adımları 7 adımdan 5 adıma düşürülmüştür) |
| **Araç Sayısı** | Belirtilmemiş (3PL lojistik sağlayıcı araçları) |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Lead Time (LT)** | Geleneksel Kanban'da 255 dk, E-Kanban ile 190 dk'ya düşmüştür (65 dk iyileşme) |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | 52 farklı malzeme parçası, günlük 26,226 kalemden (traditional) 24,479 kaleme (e-Kanban) düşüş. Kanban kart sirkülasyonu 700 karttan 530 karta düşmüştür |
| **Mesafe** | Belirtilmemiş (Depo alanı 220 m²'den 170 m²'ye düşmüştür) |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling Süresi** | Geleneksel Kanban adım adım süreleri: 40, 15, 35, 15, 50, 30, 70 dk; E-Kanban adımları: 40, 0, 50, 30, 70 dk |
| **Araç Hızı** | Belirtilmemiş |

---

## 5. The Potential Role of Open Source Discrete Event Simulation Software in the Manufacturing Sector

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | THE POTENTIAL ROLE OF OPEN SOURCE DISCRETE EVENT SIMULATION SOFTWARE IN THE MANUFACTURING SECTOR |
| **Yazarlar** | Néill Byrne, Paul Liston, John Geraghty, Paul Young |
| **Yıl** | 2012 |
| **Dergi / Kaynak** | Proceedings of the Operational Research Society Simulation Workshop 2012 (SW12, pp. 118–125) |
| **Ana Konu** | İmalat sektöründe açık kaynak kodlu kesikli olay simülasyonu (DES) yazılımlarının (özellikle SimPy) potansiyel rolü, ticari/mülkiyetli simülasyon yazılımları (ExtendSim vb.) ile vaka karşılaştırmaları ve avantaj/dezavantajlarının incelenmesidir. |
| **Metodoloji** | Vaka Çalışması & Karşılaştırmalı Analiz (Case Study & Benchmarking) — Açık kaynaklı SimPy (Python) ile ticari ExtendSim karşılaştırması; 2 vaka (Kapasite Planlama ve Yarı İletken Üretimi / Sematech minifab veriseti). |
| **Projemizle İlişkisi** | Simülasyon Mimarisi (Python/SimPy açık kaynak mimarisinin avantajları), Lisans kısıtı olmadan taşınabilir ve hızlı simülasyon araçları geliştirme, Darboğaz (bottleneck) ve kapasite planlama analizi. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (10 aylık üretim çizelgesi vaka çalışması ve Sematech minifab veriseti) |
| **İstasyon Sayısı** | Belirtilmemiş |
| **Araç Sayısı** | Belirtilmemiş |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Lead Time (LT)** | 10 aylık üretim planlama dönemi (Case I) |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | Belirtilmemiş |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş (Çalışma hızı oranı SimPy:ExtendSim 5:1 hız üstünlüğü gösterilmiştir) |

---

## 6. Optimally Scheduling and Loading Tow Trains of In-Plant Milk-Run Delivery for Mixed-Model Assembly Lines

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Optimally scheduling and loading tow trains of in-plant milk-run delivery for mixed-model assembly lines |
| **Yazarlar** | Binghai Zhou, Zhexin Zhu |
| **Yıl** | 2020 |
| **Dergi / Kaynak** | Assembly Automation (Vol. 40, No. 3, pp. 511–530) |
| **Ana Konu** | Karışık modelli montaj hatları (MMAL) için fabrika içi milk-run çekici trenlerinin (tow trains) hat kenarı stok maliyetini en aza indirecek şekilde kalkış zamanlarının ve yükleme planlarının optimize edilmesidir. |
| **Metodoloji** | Meta-sezgisel Optimizasyon — Komşuluk Araması ve Tavlama Benzetimi ile Birleştirilmiş Bağışıklık Klon Seçim Algoritması (NSICSA: Neighborhood Search + Simulated Annealing + Immune Clonal Selection Algorithm) ve Matematiksel Modelleme (MATLAB R2016a). |
| **Projemizle İlişkisi** | Milk-Run Çizelgeleme ve Yükleme Optimizasyonu (Tow train scheduling & loading), Hat kenarı stok seviyelerinin kontrolü (Line-side inventory minimization), Tampon/Kutu kapasite kısıtları altında stoksuz kalmama (no stock-out) garantisi. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Karışık modelli montaj hattı (MMAL) |
| **İstasyon Sayısı ($|S|$)** | Küçük ölçek (5–25 istasyon), Orta ölçek (30–50 istasyon), Büyük ölçek (55–75 istasyon) |
| **Araç Sayısı** | Çekici trenler (tow trains, tur sayısı $K$ ve no-wait politikası ile belirlenir) |
| **Araç Kapasitesi ($A$)** | Kutu/bin cinsinden maksimum yük kapasitesi ($A = \lceil \sum d_{sc} / K \rceil + 1$) |
| **Lead Time (LT)** | Süpermarket dolum süresi $d = 4, 8, 12$ döngü; seyahat ve yükleme/boşaltma süresi $p_s = p_{s-1} + \text{rand}(0.05, 0.2)$; toplam tur süresi $R = \lceil p_{|S|} + \text{rand}(0.05, 0.2) \rceil$ |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı ($d_{sc}$)** | İş döngüsü $c$ bazında $d_{sc} \in \{0, 1\}$ (talep olma olasılığı %45–50). İş döngüsü sayısı $C$: Küçük (9–36), Orta (45–72), Büyük (81–108) |
| **Mesafe** | İstasyonlar arası sürüş süreleri ($p_s$) ile temsil edilmiştir |
| **Zaman Penceresi** | Belirtilmemiş (Teslimatlar döngü bazlı tam sayı zaman noktalarında yapılmaktadır) |
| **Handling Süresi** | Yükleme ve boşaltma süresi $p_s$ seyahat süresi parametresinin içine dahil edilmiştir |
| **Araç Hızı** | Belirtilmemiş (Seyahat süreleri $p_s$ cinsinden ifade edilmiş) |
| **Diğer Parametreler** | İstasyon stok kapasitesi $B_s = 3$ kutu, Başlangıç stoku $IL(s,0) = 1$ kutu |

---

## 7. Discrete-Event Simulation for Waste Minimization and Productivity Enhancement in Coupling Manufacturing

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Discrete-Event Simulation for Waste Minimization and Productivity Enhancement in Coupling Manufacturing |
| **Yazarlar** | Germán Herrera-Vidal, David Martinez Sierra, Harold Cohen Padilla, Jairo R. Coronado-Hernandez |
| **Yıl** | 2026 |
| **Dergi / Kaynak** | Applied Sciences (MDPI, Vol. 16, Art. 1701) |
| **Ana Konu** | Petrol boru hatları bağlantı elemanları (coupling) imalatında kesikli olay simülasyonu (DES) kullanarak çelik atığını (scrap) azaltmak ve verimliliği/OEE'yi artırmak için senaryo bazlı süreç optimizasyonudur. |
| **Metodoloji** | Kesikli Olay Simülasyonu (Discrete Event Simulation - DES) — Python (v3.11, SimPy, NumPy, Pandas, SciPy) ile 6 aşamalı metodoloji (istatistiksel veri uydurma MLE, Kolmogorov-Smirnov, ANOVA, Tukey HSD, Welch warm-up analizi, 50 replikasyon). |
| **Projemizle İlişkisi** | Python/SimPy tabanlı Simülasyon Mimarisi, İstatistiksel Veri Dağılımı ve Doğrulama (Verification & Validation / Welch warm-up metodu), Duyarlılık ve Senaryo Analizi (ANOVA / OEE / Bottleneck tespiti). |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | 1 kesme ve işleme hattı (Cutting & machining line) |
| **İstasyon Sayısı** | 4 temel istasyon/süreç (Cutting, Rough machining, Threading, Inspection) + Finishing / Scrap |
| **Araç Sayısı** | Belirtilmemiş |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Lead Time (LT)** | Cutting (Lognormal $\mu=1.02, \sigma=0.25$ min), Rough machining (Lognormal $\mu=1.35, \sigma=0.40$ min), Threading (Triangular 2.8-3.4-4.2 min), Inspection (Triangular 0.7-1.0-1.2 min). Arıza MTBF (Exponential mean = 10.5 h), Tamir MTTR (Weibull $\alpha=1.8, \beta=0.9$ h). Vardiya süresi: 8 saat, warm-up: 30 dk |
| **Alpha ($\alpha$)** | Weibull tamir ölçek/şekil parametresi $\alpha = 1.8$ |
| **Tüketim Hızı (Talep)** | Taban modelde 8 saatlik vardiyada üretilen parça sayısı (S4 senaryosu ile throughput %14.5 artmış, scrap %35.4 azalmış, lead time %11.5 kısalmıştır) |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş |

---

## 8. Solving Large-Scale Vehicle Routing Problems with Time Windows: The State-of-the-Art

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Solving Large-Scale Vehicle Routing Problems with Time Windows: The State-of-the-Art |
| **Yazarlar** | Michel Gendreau, Christos D. Tarantilis |
| **Yıl** | 2010 |
| **Dergi / Kaynak** | CIRRELT Working Paper (CIRRELT-2010-04) / State-of-the-Art Survey |
| **Ana Konu** | Zaman Pencereli Araç Rotalama Problemleri (VRPTW) için büyük ölçekli (200 - 1000 ve 10.000 müşteriye kadar) en gelişmiş sezgisel, meta-sezgisel ve komşuluk arama yöntemlerinin literatür taraması ve analitik değerlendirmesidir. |
| **Metodoloji** | Derleme ve Karşılaştırmalı Literatür Analizi (State-of-the-Art Literature Survey & Taxonomic Classification) — Komşuluk Yapıları (2-Opt*, CROSS-exchange, $\lambda$-interchange, Large Neighborhood Search / LNS, ALNS), Hızlandırma Teknikleri (Lexicographic/Sequential search, Candidate lists, Macronodes) ve Meta-sezgisel Algoritmalar (Tabu Search, SA, GA, LNS). |
| **Projemizle İlişkisi** | VRPTW (Zaman Pencereli Araç Rotalama) Teorik ve Algoritmik Altyapısı, Dynamic Milk-Run rotalama algoritmaları için komşuluk arama (LNS/ALNS) ve zaman penceresi fizibilite kontrol teknikleri. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş |
| **İstasyon / Müşteri Sayısı** | 200 ile 1,000 müşteri arası (Gehring & Homberger test seti), 10,000 müşteriye kadar çok büyük ölçekli örnekler; Solomon test seti (100 müşteri) |
| **Araç Sayısı** | Filo boyutu (hiyerarşik amaç: önce araç sayısını minimize etmek, sonra seyahat mesafesini/süresini minimize etmek) |
| **Araç Kapasitesi** | Kapasite kısıtlı araçlar (Capacitated VRPTW) |
| **Lead Time (LT)** | Müşteri bazında servis süreleri ve seyahat süreleri; sert zaman pencereleri $[a_i, b_i]$ |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | Müşterilerin bilinen talepleri |
| **Mesafe** | Rotaların toplam seyahat mesafesi |
| **Zaman Penceresi** | Sert zaman pencereleri (Hard time windows - $[a_i, b_i]$). Erken varışta bekleme süresi, geç varışa izin verilmez |
| **Handling Süresi** | Müşteri servis süreleri (Service time) |
| **Araç Hızı** | Belirtilmemiş (Seyahat matrisleri/zamanları) |

---

## 9. Simulation-Based Analysis of an In-Plant Digitized Milk Run System

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Simulationsbasierte Analyse eines innerbetrieblichen digitalisierten Milk Run Systems (Simulation-based analysis of an in-plant digitized milk run system) |
| **Yazarlar** | Nina Vojdani, Patrick Drechsler |
| **Yıl** | 2022 |
| **Dergi / Kaynak** | Logistics Journal: Proceedings (ISSN 2192-9084) |
| **Ana Konu** | Fabrika içi e-Kanban ve RFID sensörleri ile dijitalleştirilmiş, esnek rotalı ve dinamik kalkış zamanlı bir Milk-Run sisteminin geliştirilmesi ve geleneksel sabitleştirilmiş Kanban milk-run sistemi ile simülasyon temelli karşılaştırılmasıdır. |
| **Metodoloji** | Simülasyon Temelli Karşılaştırmalı Analiz (Simulation-based Analysis) — Kesikli Olay Simülasyon Modeli (Ereignisdiskretes Simulationsmodell), Esnek Rota & Dinamik Kalkış Zamanı Algoritması vs. Sabit Saatlik Kontrol ve Sabit Rota. |
| **Projemizle İlişkisi** | Dynamic Milk-Run & E-Kanban Mimarisinin Doğrudan Özü — RFID/e-Kanban entegrasyonu, Stoksuz kalmama kısıtı altında dinamik kalkış zamanı hesaplama (demand-driven release scheduling), Esnek rotalama ve 2-Kutu Kanban mantığı. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | 3 üretim çalışma alanı (Arbeitsbereiche) |
| **İstasyon Sayısı** | 15 çalışma istasyonu (Arbeitsstationen) |
| **Araç Sayısı** | 1 Çekici tren (Routenzug / Tugger train) |
| **Araç Kapasitesi** | Belirtilmemiş (Çekici tren ve römorklar - Tugger train with trailers) |
| **Lead Time (LT)** | Geleneksel sistemde 1 saatlik (stündlich) kontrol; Dijitalleştirilmiş sistemde ortalama sürüş döngü süresi 11 dk 29 sn (gelenekselde 8 dk 55 sn fakat toplam sürüş süresinde %38.5 tasarruf sağlanmıştır). Benzetim süresi: 7 gün |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | Müşteri sipariş yüküne bağlı tüketim; 2-Kutu Kanban (Zwei-Behälter-Kanban) sistemi |
| **Mesafe** | Dijital Milk-run ile seyahat mesafesinde %29.39 tasarruf sağlanmış (kontroller dahil edildiğinde geleneksel sistem 2.8 kat fazla yol kat etmektedir) |
| **Zaman Penceresi** | İstasyonların malzeme tükenme (bedarfszeitpunkte) zaman noktalarına göre dinamik hesaplanan zaman penceresi kısıtı |
| **Handling Süresi** | Belirtilmemiş (Depoda ön komisyonlama ve yükleme) |
| **Araç Hızı** | Belirtilmemiş |

---

## 10. Route Optimization of Simultaneous Delivery and Pick-up in Automotive Inbound Logistics Under the Milk-Run Mode in a Dual-Carbon Background

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Route optimization of simultaneous delivery and pick-up in automotive inbound logistics under the milk-run mode in a dual-carbon background |
| **Yazarlar** | Weiwei Zhang |
| **Yıl** | 2026 |
| **Dergi / Kaynak** | Engineering Computations (Emerald) |
| **Ana Konu** | Çift karbon (dual-carbon) hedefi altında otomotiv tedarik lojistiğinde 2 kademeli, zaman pencereli, eşzamanlı teslimat ve toplamalı (2E-VRPSPDTW) milk-run rota optimizasyonu ve karbon emisyonu / maliyet minimizasyonudur. |
| **Metodoloji** | Çok Amaçlı Karma Karışık Tam Sayılı Programlama (MIP) ve Geliştirilmiş NSGA-II Algoritması (INSGA-II / INSGA2: elit kontrol stratejisi ile). |
| **Projemizle İlişkisi** | VRPTW & Milk-Run Rotalama Optimizasyonu, İki Kademeli (2-Echelon) Dağıtım ve Boş Konteyner Toplama / İade Sistemleri, Zaman Penceresi ve Hizmet Seviyesi (Service level) Kısıtları. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (2 kademeli tedarik ağı: 30 Tedarikçi -> 2 Dağıtım Merkezi (DC) -> 1 Ana Üretici OEM M) |
| **İstasyon / Düğüm Sayısı** | 30 Tedarikçi ($S_1 - S_{30}$), 2 Dağıtım Merkezi ($R_1, R_2$), 1 Ana Fabrika/OEM ($M$) |
| **Araç Sayısı** | Dağıtım merkezlerinde 3 tip araç (6.8 m, 9.6 m, 13 m filosu) |
| **Araç Kapasitesi** | Hacim ve ağırlık limitli ($Q_{wk}$). Boş konteynerler katlanabilir/içe içe geçebilir (nested empty containers, 1/5 hacim kaplar) |
| **Lead Time (LT)** | Düğümler arası seyahat süreleri $T_{jiwk}, T_{iewk}$, yükleme/boşaltma süresi $T_{iwk} = (EN_i + N_i) / v_{swk}$, DC işleme süresi $T_j$ |
| **Alpha ($\alpha$)** | Pareto elit indirgeme oranı $r \in [0, 1)$ ve çaprazlama katsayısı $\alpha \in [0, 1]$ |
| **Tüketim Hızı (Talep)** | 30 tedarikçiden toplam 650 dolu konteyner ve boş konteyner talepleri (örn. S1: 3 dolu, 5 boş; S3: 11 dolu, 20 boş vb.) |
| **Mesafe** | Öklid / seyahat mesafesi matrisi ($d_{ji}, d_{ie}$) |
| **Zaman Penceresi** | Belirtilen ve kabul edilebilir zaman pencereleri (Specified & Acceptable Time Windows, örn. S1: 6:20–8:50 / 5:20–12:20, S10: 9:50–12:20) |
| **Handling Süresi** | DC elleçleme hızı $v_j$ ve tedarikçi yükleme/boşaltma hızı $v_{swk}$ |
| **Araç Hızı** | $v_{twk}$ (araç seyahat hızı) |

---

## 11. Supply Chain System Model of Components for Assembly Lines Based on Kanban and Milk Run Methodologies

| Alan / Metrik | Detay / Değer |
| :--- | :--- |
| **Başlık** | Supply Chain System Model of Components for Assembly Lines Based on Kanban and Milk Run Methodologies |
| **Yazarlar** | Victor Hugo Oliveira dos Santos, Marcelo Albuquerque de Oliveira, Gabriela de Mattos Veroneze |
| **Yıl** | 2021 |
| **Dergi / Kaynak** | European Journal of Engineering and Technology Research (EJERS, Vol. 6, Issue 6, pp. 139–144) |
| **Ana Konu** | Otomotiv (motosiklet/4x4) ve elektronik tesislerindeki montaj hatlarına malzeme besleme süreçlerinin incelenmesi ve ağırlık sensörlü (terazi) e-Kanban ve Milk-Run entegrasyonu ile gerçek zamanlı stok takibi ve besleme sistem önerisidir. |
| **Metodoloji** | Vaka Çalışması & Konsept Sistem Tasarımı (Case Study & Conceptual System Design) — İki fabrika (Şirket F: Elektronik / 38-34 montaj hattı, Şirket H: Motosiklet / günlük 10,000 üretim) üzerinde doğrudan gözlem ve ağırlık sensörlü (terazi) gerçek zamanlı Kanban-Milk Run sistem modeli. |
| **Projemizle İlişkisi** | E-Kanban & Gerçek Zamanlı Sinyal Mimarisi (Ağırlık/Terazi sensörlü stok takibi), ROP ve Kritik Stok seviyelerinin belirlenmesi, Milk-Run ile montaj hatlarının gerçek zamanlı beslenmesi ve personel/taşıma israfının (Lean Waste) önlenmesi. |

### Anahtar Parametreler Tablosu

| Parametre | Değer / Açıklama |
| :--- | :--- |
| **Hat Sayısı** | Şirket F (38 veya 34 montaj hattı, 3 vardiya), Şirket H (motosiklet ve 4x4 montaj hatları) |
| **İstasyon Sayısı** | Belirtilmemiş (Hat üzerindeki montaj istasyonları) |
| **Araç Sayısı** | Belirtilmemiş (Teslimat kamyonları, sepetli arabalar, havalı taşıyıcılar) |
| **Araç Kapasitesi** | Belirtilmemiş (Kamyon ve sepet taşıma kapasiteleri) |
| **Lead Time (LT)** | Şirket H'de besleme sektörü hattın 2 km uzağındadır. Şirket F'de 306 personel besleme/taşıma yaparken, yeni sistemle personel ihtiyacı %67 azalacaktır |
| **Alpha ($\alpha$)** | Belirtilmemiş |
| **Tüketim Hızı (Talep)** | Şirket F: Günlük 30,000 modem ve 50,000 uzaktan kumanda. Şirket H: Günlük 10,000 motosiklet. Ağırlık hassasiyeti örn. 1000 adet somun sepeti $1.8 \pm 0.142$ kg |
| **Mesafe** | Besleme deposu - montaj hattı arası 2 km (Şirket H) |
| **Zaman Penceresi** | Gerçek zamanlı 3 stok durumu (OK, Yeniden Sipariş İsteği / Reposition Request, Kritik Stok / Critical Stock) |
| **Handling Süresi** | Belirtilmemiş (Gerçek zamanlı terazi okunarak elleçleme/yeniden sipariş kararı alınıyor) |
| **Araç Hızı** | Belirtilmemiş |

---
