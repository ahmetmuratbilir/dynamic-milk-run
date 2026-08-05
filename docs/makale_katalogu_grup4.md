# Akademik Makale Kataloğu — Grup 4 (11 Makale)
## Dinamik Milk-Run & E-Kanban Karar Destek Sistemi Literatür Analizi

> **Yöntem:** 11 `.txt` dosyası doğrudan taranmış ve makalelerdeki veriler eksiksiz çıkarılmıştır.  
> **Kural:** Sadece makalelerde GERÇEKTEN yer alan bilgiler yazılmıştır. Uydurma veri kullanılmamış, bulunmayan parametreler için **"Belirtilmemiş"** ifadesi yazılmıştır.  
> **Dosya Yolu:** `c:\Users\ahmet murat bilir\Desktop\dynamic-milk-run\docs\papers\extracted_text\`

---

## 1. VRPTW Distribution Route Determination with Rigid and Flexible Time Window and Assignment Based on Number of Demand

* **Dosya Adı:** `jsti,+17230.txt`
* **Başlık:** VRPTW Distribution Route Determination with Rigid and Flexible Time Window and Assignment Based on Number of Demand
* **Yazarlar:** Muhammad Zidanne, Fikri Keynobi, Eri Wirdianto
* **Yıl:** 2025 (Kabul: Aralık 2024, Yayın: Ocak 2025)
* **Dergi / Kaynak:** Jurnal Sistem Teknik Industri (JSTI), Vol. 27, No. 1, ss. 14–20
* **Ana Konu:** Bir dağıtım firmasının 15 müşteriye ürün teslimatında katı (rigid) ve esnek (flexible) zaman pencereleri ile gecikme cezalarını (penalty fee) dikkate alarak araç kapasitelerine uygun en düşük maliyetli VRPTW rotasının belirlenmesi.
* **Metodoloji:** Karma Tamsayılı Doğrusal Programlama (MILP - Mixed-Integer Linear Programming), LINGO yazılımı ile tam (exact) çözüm.

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | Belirtilmemiş |
| **İstasyon / Durak sayısı** | 1 Depo (Depot), 15 Müşteri |
| **Araç sayısı** | 2 Araç (Araç 1 ve Araç 2) |
| **Araç kapasitesi** | Araç 1 (talep $\le$ 10 kg alan müşterilere özel, kapasite $Q_1$), Araç 2 (kapasite $Q_2 > Q_1$) |
| **LT (Lead Time)** | Belirtilmemiş |
| **Güvenlik katsayısı ($\alpha$)** | Belirtilmemiş |
| **Tüketim hızı** | Müşteri bazlı talep $d_i$ (kg/birim) |
| **Mesafe** | $c_{ij}$ mesafe matrisi (km) |
| **Zaman penceresi** | Katı ($[a_i, b_i]$), Esnek (sınırsız gecikme) ve Hibrit Katı-Esnek zaman pencereleri |
| **Handling süresi** | $s_i$ (müşteri noktasındaki hizmet süresi, dk) |
| **Araç hızı** | Belirtilmemiş (seyahat süresi $t_{ij}$ doğrudan matris olarak tanımlı) |

* **Projemizle İlişkisi:** VRPTW esnek/katı zaman pencereleri yönetimi, gecikme cezası (penalty fee) entegrasyonu, heterojen araç kapasitesi kısıtları ve LINGO/MILP matematiksel modelleme yaklaşımı projemizin dynamic milk-run rotalama ve zaman penceresi kısıtları modülüne doğrudan katkı sağlar.

---

## 2. Application of Optimization Techniques in the Dairy Supply Chain: A Systematic Review

* **Dosya Adı:** `logistics-06-00074.txt`
* **Başlık:** Application of Optimization Techniques in the Dairy Supply Chain: A Systematic Review
* **Yazarlar:** Mohit Malik, Vijay Kumar Gahlawat, Rahul S Mor, Vijay Dahiya, Mukheshwar Yadav
* **Yıl:** 2022
* **Dergi / Kaynak:** Logistics (MDPI), Vol. 6, No. 4, Art. 74
* **Ana Konu:** Süt tedarik zincirinde (Dairy Supply Chain) kullanılan matematiksel modelleme, yapay zeka (AI) ve makine öğrenmesi (ML) tabanlı optimizasyon tekniklerinin PRISMA yöntemiyle sistematik olarak taranması ve incelenmesi.
* **Metodoloji:** PRISMA rehberine dayalı Sistematik Literatür Taraması (Systematic Literature Review) ve Betimsel İstatistiksel Analiz (%56 Matematiksel Modelleme, %44 AI/ML).

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | Belirtilmemiş |
| **İstasyon / Durak sayısı** | Belirtilmemiş |
| **Araç sayısı** | Belirtilmemiş |
| **Araç kapasitesi** | Belirtilmemiş |
| **LT (Lead Time)** | Belirtilmemiş |
| **Güvenlik katsayısı ($\alpha$)** | Belirtilmemiş |
| **Tüketim hızı** | Belirtilmemiş |
| **Mesafe** | Belirtilmemiş |
| **Zaman penceresi** | Belirtilmemiş |
| **Handling süresi** | Belirtilmemiş |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** Tedarik zinciri optimizasyon tekniklerinin (matematiksel modelleme, sezgisel yöntemler, yapay zeka/makine öğrenmesi) sınıflandırılması ve süt/bozulabilir ürün lojistiğinde rotalama/tedarik süreçlerinin literatür çerçevesini sunması bakımından teorik altyapımıza katkı sağlar.

---

## 3. Discrete Event Simulation as a Predictor for Factory Traffic Management

* **Dosya Adı:** `ramirezechavarria-estebanr-mba-mgt-2025-thesis.txt`
* **Başlık:** Discrete Event Simulation as a Predictor for Factory Traffic Management
* **Yazarlar:** Esteban Ramirez Echavarria
* **Yıl:** 2025 (Yüksek Lisans Tezi, Mayıs 2025)
* **Dergi / Kaynak:** Massachusetts Institute of Technology (MIT Sloan School of Management & EECS) Yüksek Lisans Tezi
* **Ana Konu:** Bir uçak imalatı (Boeing) fabrikasında malzeme akışını modellemek, AGV, vinç ve taşıma arabası hareketlerini tahmin etmek ve fabrika içi trafik kilitlenmelerini önlemek amacıyla SimPy tabanlı Kesikli Olay Simülasyonu (DES) ve Dijital İkiz (Digital Twin) geliştirilmesi.
* **Metodoloji:** Kesikli Olay Simülasyonu (DES), Python SimPy kütüphanesi, Dijkstra en kısa yol algoritması, Push-out algoritması, React.js web arayüzü ve API entegrasyonu.

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | Belirtilmemiş (Alpha, Beta, Gamma parça üretim hatları/alanları) |
| **İstasyon / Durak sayısı** | Belirtilmemiş (Crucible, Trim, Staging, Paint vb. istasyonlar) |
| **Araç sayısı** | Belirtilmemiş (AGV, vinç, taşıma arabaları/carts filosu) |
| **Araç kapasitesi** | Belirtilmemiş (Atlas tool: 2, 4 veya 6 parça kapasiteli) |
| **LT (Lead Time)** | Belirtilmemiş |
| **Güvenlik katsayısı ($\alpha$)** | Belirtilmemiş |
| **Tüketim hızı** | Belirtilmemiş |
| **Mesafe** | Düğümler (nodes) arası Dijkstra mesafeleri |
| **Zaman penceresi** | Belirtilmemiş (Simülasyon periyodu: 10 saatlik tahminler, 40 günlük doğrulama dönemi) |
| **Handling süresi** | Operasyon bazlı işleme/damga süreleri (stamp processing times) |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** SimPy ile Python tabanlı kesikli olay simülasyonu (DES) mimarisi kurma, fabrika içi AGV/taşıyıcı trafik tahmini, dijital ikiz ve React front-end ile canlı izleme/zamanlama sistemleri tasarımı konularında projemizin simülasyon ve sinyal mimarisi modülüne katkı sağlar.

---

## 4. Analytical Fleet-Sizing Method for the Open Platform for Innovation in Logistics (OPIL)

* **Dosya Adı:** `s41598-026-46148-y.txt`
* **Başlık:** Analytical fleet-sizing method for the Open Platform for Innovation in Logistics (OPIL)
* **Yazarlar:** Ladislav Körösi, František Duchoň
* **Yıl:** 2026
* **Dergi / Kaynak:** Scientific Reports (Nature Publishing Group), Vol. 16, Art. 16797
* **Ana Konu:** OPIL (Open Platform for Innovation in Logistics) çerçevesinde lojistik ajanlarının (AGV, forklift, insan operatör) sabit durum malzeme akış taleplerini karşılamak için gerekli filo büyüklüğünü belirleyen deterministik analitik yöntem ve Docker modülü.
* **Metodoloji:** Groover'ın analitik metodolojisinin matris tabanlı genişletilmesi (akış matrisi $F_{ij}$, mesafe matrisi $D_{ij}$, kullanılabilirlik $A$, trafik katsayısı $F_t$, operatör verimliliği $E_w$), Docker tabanlı mikroservis, MongoDB ve Java HMI, duyarlılık analizi.

### Anahtar Parametreler (SMARTENVELOPE Plast-Farb Örnek Olayı)

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | Belirtilmemiş (3 ana taşıma rotası: depodan makinelere, makinelerden streç sarmaya, depoya) |
| **İstasyon / Durak sayısı** | $N$ istasyon (matris tabanlı) |
| **Araç sayısı** | $AN = 2.025 \to 3$ forklift (2 aktif, 1 yedek) |
| **Araç kapasitesi** | $c = 1$ palet/sefer |
| **LT (Lead Time)** | Çevrim süresi $TC = 2.912$ dk |
| **Güvenlik katsayısı ($\alpha$)** | Kullanılabilirlik katsayısı $A = 0.70$, Trafik katsayısı $F_t = 0.50$, Operatör verimliliği $E_w = 0.70$ |
| **Tüketim hızı** | $w = 10.222$ palet/saat |
| **Mesafe** | Yüklü mesafe $L_d = 40.30$ m, Boş mesafe $L_e = 28.76$ m |
| **Zaman penceresi** | Belirtilmemiş (Saatlik ortalama talepler) |
| **Handling süresi** | Yükleme $T_L = 0.4$ dk, Boşaltma $T_U = 0.5$ dk |
| **Araç hızı** | $v_c = 35$ m/dk (~2.1 km/sa) |

* **Projemizle İlişkisi:** Milk-run ve AGV/filo boyutlandırmada (fleet sizing) trafik sıkışıklığı ($F_t$), kullanılabilirlik ($A$) ve operasyonel verimlilik ($E_w$) katsayılarının analitik olarak modellenmesi; duyarlılık analizi yöntemleri projemizin filo boyutu hesabı ve duyarlılık analizi bölümlerine doğrudan katkı sağlar.

---

## 5. Simulation Testing of the E-Kanban to Increase the Efficiency of Logistics Processes

* **Dosya Adı:** `simulation-testing-of-the-e-kanban-to-increase-the-1zqtp4mux.txt`
* **Başlık:** Simulation Testing of the E-Kanban to Increase the Efficiency of Logistics Processes
* **Yazarlar:** Miriam Pekarcikova, Peter Trebuna, Marek Kliment, Marek Mizerak, Stanislav Kral
* **Yıl:** 2021
* **Dergi / Kaynak:** International Journal of Simulation Modelling (IJSIMM), Vol. 20, No. 1, ss. 134–145
* **Ana Konu:** Çelik tel ve kablo üreten bir fabrikada lojistik süreçlerin ve malzeme akışının verimliliğini artırmak amacıyla e-Kanban sisteminin Tecnomatix Plant Simulation ile simülasyonu ve optimizasyonu.
* **Metodoloji:** Yalın Üretim Araçları (VSM, Gemba, Bottleneck Analysis, E-Kanban) ve Tecnomatix Plant Simulation (v15.2) ile 2D/3D kesikli olay simülasyonu.

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | 1 ana üretim hattı |
| **İstasyon / Durak sayısı** | 9 ana işlem istasyonu (Drumming, Extending, Control diameter, Cabling, Splicing, Packing spool, Control spool, Packing pallet, Expedition) |
| **Araç sayısı** | Belirtilmemiş |
| **Araç kapasitesi** | Belirtilmemiş (Kutu/Tampon kapasiteleri tanımlı) |
| **LT (Lead Time)** | Döngü süreleri: Drumming (1:15), Extending (4:40-4:55), Control (2:00), Cabling (3:10-3:20), Splicing (2:15-2:25), Packing spool (6:00), Control spool (11:00), Packing pallet (9:00), Expedition (15:00) |
| **Güvenlik katsayısı ($\alpha$)** | Kullanılabilirlik (Availability) %95 - %100 |
| **Tüketim hızı** | Sipariş/vardiya bazlı akış hızı |
| **Mesafe** | Belirtilmemiş (2D/3D yerleşim ve Sankey diyagramı) |
| **Zaman penceresi** | Simülasyon süresi = 12 saat (1 vardiya) |
| **Handling süresi** | Kurulum (Set-up) süresi = 10 dk (Extending, Cabling, Splicing), MTTR = 5 dk |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** E-Kanban sinyalizasyonu ve Tecnomatix Plant Simulation / dijital ikiz uygulamaları ile hatlarda tıkanıklık (bottleneck) tespiti, tampon seviyesi yönetimi ve vardiya bazlı performans simülasyonu konularında projemizin E-Kanban ve Simülasyon modüllerine katkı sağlar.

---

## 6. Enhancing Inventory Management through Safety-Stock Strategies—A Case Study

* **Dosya Adı:** `systems-12-00260.txt`
* **Başlık:** Enhancing Inventory Management through Safety-Stock Strategies—A Case Study
* **Yazarlar:** Sema Demiray Kırmızı, Zeynep Ceylan, Serol Bulkan
* **Yıl:** 2024
* **Dergi / Kaynak:** Systems (MDPI), Vol. 12, No. 7, Art. 260
* **Ana Konu:** Bir işletmenin (STAR) stok tutma ve kıtlık (shortage) maliyetlerini minimize etmek amacıyla 5 farklı güvenlik stoğu yönteminin (mevcut gün sayısı, TOC tamamlama, servis seviyesi ve ABC-XYZ matrisi entegreli 2 yeni hibrit model) karşılaştırılması.
* **Metodoloji:** ABC-XYZ Matris Analizi, Kısıtlar Teorisi (TOC) Tamamlama Modeli, Servis Seviyesi (Service-Level) Yaklaşımı ve Simul8 ile Monte Carlo / Kesikli Olay Simülasyonu.

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | Belirtilmemiş |
| **İstasyon / Durak sayısı** | Belirtilmemiş |
| **Araç sayısı** | Belirtilmemiş |
| **Araç kapasitesi** | Belirtilmemiş |
| **LT (Lead Time)** | Sabit LT = 1 ay (30 gün) |
| **Güvenlik katsayısı ($\alpha$)** | Servis Seviyesi $z \in [1.28, 1.65, 2.33]$ (%90, %95, %99 servis seviyeleri), TOC güvenlik stoğu = LT talebinin %50'si |
| **Tüketim hızı** | Aylık ürün talepleri (5 temsilci SKU için değişken talep ve standart sapma $\sigma_D$) |
| **Mesafe** | Belirtilmemiş |
| **Zaman penceresi** | Belirtilmemiş (Aylık/Yıllık periyotlar) |
| **Handling süresi** | Belirtilmemiş |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** ABC-XYZ analizi ile dinamik güvenlik stoğu (safety stock) ve Yeniden Sipariş Noktası (ROP) hesaplama, Kısıtlar Teorisi (TOC) tampon yönetimi, stok kıtlık/stoksuzluk (starvation/backorder) maliyeti analizi projemizin ROP, Güvenlik Stoğu ve Starvation Analizi modüllerine katkı sağlar.

---

## 7. Material Flow Optimization through E-Kanban System Simulation

* **Dosya Adı:** `text19-2_513.txt`
* **Başlık:** Material Flow Optimization through E-Kanban System Simulation
* **Yazarlar:** Miriam Pekarcikova, Peter Trebuna, Marek Kliment, Ladislav Rosocha
* **Yıl:** 2020
* **Dergi / Kaynak:** International Journal of Simulation Modelling (IJSIMM), Vol. 19, No. 2, ss. 243–254
* **Ana Konu:** Tıbbi cihaz (idrar toplama torbası) üreten bir fabrikada üretim ve montaj süreçlerinin E-Kanban mantığı ve Tecnomatix Plant Simulation ile modellenerek malzeme akışının ve üretim verimliliğinin optimizasyonu.
* **Metodoloji:** E-Kanban Çekme (Pull) Sistemi, Hiyerarşik Modeller (Frames), Tecnomatix Plant Simulation (v15.2) ve Experiment Manager ile varyant simülasyon testleri.

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | 1 ana üretim hattı |
| **İstasyon / Durak sayısı** | Belirtilmemiş (Pres makineleri, manuel valf istasyonu, paketleme montaj istasyonları) |
| **Araç sayısı** | Belirtilmemiş |
| **Araç kapasitesi** | Paketleme kapasitesi: 1 bağ = 25 torba, 1 kutu = 8 bağ (200 torba/kutu) |
| **LT (Lead Time)** | Kaynak/pres işlem süresi = 10 saniye; Paketleme = 5 dakika |
| **Güvenlik katsayısı ($\alpha$)** | Belirtilmemiş |
| **Tüketim hızı** | Sipariş/vardiya bazlı akış hızı (Çocuk, valfli, yatak, seyahat, tek kullanımlık torbalar) |
| **Mesafe** | Belirtilmemiş |
| **Zaman penceresi** | Simülasyon süresi = 12 saat (1 vardiya) |
| **Handling süresi** | Pres süresi = 10 sn, Paketleme = 5 dk |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** Elektronik Kanban (E-Kanban) sinyal mimarisi, barkod/QR kod tabanlı gerçek zamanlı sipariş tetikleme ve Plant Simulation ile çekme (pull) kontrol döngülerinin simülasyonu projemizin E-Kanban ve Sinyal Mimarisi modüllerine katkı sağlar.

---

## 8. Simulation Testing of the E-Kanban to Increase the Efficiency of Logistics Processes

* **Dosya Adı:** `text20-1_551.txt`
* **Başlık:** Simulation Testing of the E-Kanban to Increase the Efficiency of Logistics Processes
* **Yazarlar:** Miriam Pekarcikova, Peter Trebuna, Marek Kliment, Marek Mizerak, Stanislav Kral
* **Yıl:** 2021
* **Dergi / Kaynak:** International Journal of Simulation Modelling (IJSIMM), Vol. 20, No. 1, ss. 134–145
* **Ana Konu:** Çelik tel ve kablo üretimi yapan bir tesiste lojistik süreçlerin ve malzeme akışının verimliliğini artırmak amacıyla e-Kanban sisteminin Tecnomatix Plant Simulation ile simülasyonu ve optimizasyonu.
* **Metodoloji:** Yalın Üretim Araçları (VSM, Gemba, Bottleneck Analysis, E-Kanban) ve Tecnomatix Plant Simulation (v15.2) ile 2D/3D kesikli olay simülasyonu.

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | 1 ana üretim hattı |
| **İstasyon / Durak sayısı** | 9 ana işlem istasyonu (Drumming, Extending, Control diameter, Cabling, Splicing, Packing spool, Control spool, Packing pallet, Expedition) |
| **Araç sayısı** | Belirtilmemiş |
| **Araç kapasitesi** | Belirtilmemiş |
| **LT (Lead Time)** | Döngü süreleri: Drumming (1:15), Extending (4:40-4:55), Control (2:00), Cabling (3:10-3:20), Splicing (2:15-2:25), Packing spool (6:00), Control spool (11:00), Packing pallet (9:00), Expedition (15:00) |
| **Güvenlik katsayısı ($\alpha$)** | Kullanılabilirlik (Availability) %95 - %100 |
| **Tüketim hızı** | Sipariş/vardiya bazlı akış hızı |
| **Mesafe** | Belirtilmemiş |
| **Zaman penceresi** | Simülasyon süresi = 12 saat (1 vardiya) |
| **Handling süresi** | Setup süresi = 10 dk (Extending, Cabling, Splicing), MTTR = 5 dk |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** E-Kanban sinyalizasyonu ve Tecnomatix Plant Simulation / dijital ikiz uygulamaları ile hatlarda tıkanıklık (bottleneck) tespiti, tampon seviyesi yönetimi ve vardiya bazlı performans simülasyonu konularında projemizin E-Kanban ve Simülasyon modüllerine katkı sağlar.

---

## 9. Milk-run Kanban System for Raw Printed Circuit Board Withdrawal to Surface-Mounted Equipment

* **Dosya Adı:** `v05-i02-p382_352-3211-5-PB.txt`
* **Başlık:** Milk-run kanban system for raw printed circuit board withdrawal to surface-mounted equipment
* **Yazarlar:** Swee Li Chee, Mei Yong Chong, Jeng Feng Chin
* **Yıl:** 2012
* **Dergi / Kaynak:** Journal of Industrial Engineering and Management (JIEM), Vol. 5, No. 2, ss. 382–405
* **Ana Konu:** Elektronik montaj tesisinde ham baskılı devre kartlarının (PCB) depodan SMT/SME (Surface-Mounted Equipment) yüzey montaj makinelerine taşınmasında push sistemden Milk-run Kanban çekme sistemine geçiş ve simülasyon/RSM analizi.
* **Metodoloji:** Değer Akış Haritalama (VSM), Kesikli Olay Simülasyonu (Witness 2008), Tam Faktöriyel Deney Tasarımı, Varyans Analizi (ANOVA) ve Yanıt Yüzeyi Metodolojisi (RSM - Response Surface Methodology / VB6).

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | 6 SME (Surface-Mounted Equipment) makine hattı |
| **İstasyon / Durak sayısı** | Depo, Mal Kabul Verifikasyon, Lazer/Manuel Markalama, Azot Odası, 6 SME Makine Standby Alanı |
| **Araç sayısı** | 1 milk-run operatörü / malzeme taşıyıcısı |
| **Araç kapasitesi** | Rota başına maks 2-4 bin/kutu (güvenlik ağırlık sınırı 20 kg; kutu boyutları $292\times394\times166$ mm ve $394\times592\times166$ mm) |
| **LT (Lead Time)** | Depodan teslimat süresi ~3 saat (öncesinde 2 gün standby) |
| **Güvenlik katsayısı ($\alpha$)** | Belirtilmemiş |
| **Tüketim hızı** | Vardiya başına ortalama 8 sipariş, paket başı ~60 raw PCB, şarj başı 40 panel |
| **Mesafe** | Belirtilmemiş (Fabrika içi milk-run rotası) |
| **Zaman penceresi** | Günde 3 vardiya, haftada 6 gün çalışma |
| **Handling süresi** | Kurulum (C/O) ve markalama süreleri (VSM verileri) |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** Milk-run dağıtımı ile Kanban çekme mantığının entegrasyonu, tam faktöriyel deney tasarımı ve Yanıt Yüzeyi Metodolojisi (RSM) ile simülasyon çıktılarının (WIP, darboğaz/SME kullanımı, bekleme süreleri) optimizasyonu projemizin Milk-run Rotalama, Kanban ve Duyarlılık Analizi (RSM) bölümlerine katkı sağlar.

---

## 10. Planning and Dimensioning of a Milk-Run Transportation System Considering the Actual Line Consumption

* **Dosya Adı:** `1-s2.0-S2405896318307894-main (1).txt`
* **Başlık:** Planning and dimensioning of a milk-run transportation system considering the actual line consumption
* **Yazarlar:** Augusto Urru, Marco Bonini, Wolfgang Echelmeyer
* **Yıl:** 2018
* **Dergi / Kaynak:** IFAC-PapersOnLine, Vol. 51, No. 9, ss. 404–409
* **Ana Konu:** VDI 5586 standardındaki itme odaklı milk-run/tugger train planlama metodolojisini, gerçek hat tüketimini ve farklı sipariş tetikleme yöntemlerini (fiziksel Kanban kartı, e-Kanban barkod, hat içi buton/sensör) dikkate alan dinamik çekme odaklı tampon boyutlandırma modeli ile geliştirmek.
* **Metodoloji:** VDI 5586 Standardı genişletmesi, Dinamik Çekme (Pull) Tampon Boyutlandırma Formülasyonu, 3 Farklı Sipariş Tetikleme Senaryosu (Kanban Card, E-Kanban Barcode, Direct Order Sensor) ve En Kötü Durum (Worst-Case) Çevrim Süresi Analizi ($k$ katsayısı hesabı).

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | Belirtilmemiş (1 ana milk-run / tugger train rotası) |
| **İstasyon / Durak sayısı** | 5 durak (S1-S5) + 1 Supermarket / Depo |
| **Araç sayısı** | 1-2 çekici tren (tugger train) |
| **Araç kapasitesi** | 2-5 römork/tren, standart yük birimleri (Unit Load - UL) |
| **LT (Lead Time)** | Rota periyodu / Takt süresi $t_{takt} = 1/f_r$ |
| **Güvenlik katsayısı ($\alpha$)** | Tampon güvenlik çarpanı $k$ (worst-case katsayısı) |
| **Tüketim hızı** | $\lambda_{A,H}$ (Durak H'de ürün A için saatlik ortalama tüketim - UL/h) |
| **Mesafe** | Belirtilmemiş |
| **Zaman penceresi** | Belirtilmemiş |
| **Handling süresi** | Komisyonlama süresi $t_{comA}$, yükleme/boşaltma süreleri |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** VDI 5586 standardına göre milk-run / tugger train tampon ve tur boyutlandırma, e-Kanban barkod / sensör ile bilgi akış süresinin ($t_{inf}$) sıfırlanmasının hat başı stok tutma ve hat duruşlarını (starvation) önleme üzerindeki matematiksel etkisinin modellenmesi projemizin E-Kanban, Sinyal Mimarisi, ROP ve Starvation Analizi modüllerine katkı sağlar.

---

## 11. Material Flow Optimization through E-Kanban System Simulation

* **Dosya Adı:** `IJSIMM19-2_513 (1).txt`
* **Başlık:** Material Flow Optimization through E-Kanban System Simulation
* **Yazarlar:** Miriam Pekarcikova, Peter Trebuna, Marek Kliment, Ladislav Rosocha
* **Yıl:** 2020
* **Dergi / Kaynak:** International Journal of Simulation Modelling (IJSIMM), Vol. 19, No. 2, ss. 243–254
* **Ana Konu:** Tıbbi cihaz (idrar toplama torbası) üreten bir fabrikada üretim ve montaj süreçlerinin E-Kanban mantığı ve Tecnomatix Plant Simulation ile modellenerek malzeme akışının ve üretim verimliliğinin optimizasyonu.
* **Metodoloji:** E-Kanban Çekme (Pull) Sistemi, Hiyerarşik Modeller (Frames), Tecnomatix Plant Simulation (v15.2) ve Experiment Manager ile varyant simülasyon testleri.

### Anahtar Parametreler

| Parametre | Makaledeki Değer |
|---|---|
| **Hat sayısı** | 1 ana üretim hattı |
| **İstasyon / Durak sayısı** | Belirtilmemiş (Pres makineleri, manuel valf istasyonu, paketleme montaj istasyonları) |
| **Araç sayısı** | Belirtilmemiş |
| **Araç kapasitesi** | Paketleme kapasitesi: 1 bağ = 25 torba, 1 kutu = 8 bağ (200 torba/kutu) |
| **LT (Lead Time)** | Kaynak/pres işlem süresi = 10 saniye; Paketleme = 5 dakika |
| **Güvenlik katsayısı ($\alpha$)** | Belirtilmemiş |
| **Tüketim hızı** | Sipariş/vardiya bazlı akış hızı |
| **Mesafe** | Belirtilmemiş |
| **Zaman penceresi** | Simülasyon süresi = 12 saat (1 vardiya) |
| **Handling süresi** | Pres süresi = 10 sn, Paketleme = 5 dk |
| **Araç hızı** | Belirtilmemiş |

* **Projemizle İlişkisi:** Elektronik Kanban (E-Kanban) sinyal mimarisi, barkod/QR kod tabanlı gerçek zamanlı sipariş tetikleme ve Plant Simulation ile çekme (pull) kontrol döngülerinin simülasyonu projemizin E-Kanban ve Sinyal Mimarisi modüllerine katkı sağlar.
