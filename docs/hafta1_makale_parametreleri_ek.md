# Hafta 1 - Makale Parametreleri Ek Raporu

Bu raporda, verilen 15 adet akademik makale ve metin dosyasından elde edilen 14 temel lojistik ve üretim parametresi incelenmiş ve makalelerde geçen doğrudan değerler satır numaralarıyla raporlanmıştır. Makalelerde yer almayan parametreler için "Belirtilmemiş" ifadesi kullanılmıştır.

---

**1. aa-01-2019-0013.txt — Optimally scheduling and loading tow trains of in-plant milk-run delivery for mixed-model assembly lines — Binghai Zhou, Zhexin Zhu (2020)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | 1 karma modelli montaj hattı (MMAL) | L6, L128 |
| İstasyon / durak sayısı | Küçük ölçek: 5/10/15/20/25; Orta ölçek: 30/35/40/45/50; Büyük ölçek: 55/60/65/70/75 istasyon | L1537-1540 |
| Araç sayısı | Güzergah başına 1 çekici tren (tow train) | L34, L195-202, L221 |
| Araç kapasitesi | $A = \sum_{s=1}^{|S|} \sum_{c=1}^{C} d_{sc} / K + 1$ kutu (bin) | L61-63, L1516-1523 |
| Simülasyon süresi | Çalışma döngüleri (C): 9/18/27/36 (küçük), 45/54/63/72 (orta), 81/90/99/108 (büyük) | L1542-1546 |
| Lead time | Süpermarket yenileme süresi $d = 4, 8, 12$ döngü süresi; İstasyon seyahat süresi $p_s$ | L45-51, L1547-1551 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-3760 |
| Kanban formülü / kart sayısı | Belirtilmemiş (JIT envanter optimizasyonu / Matematiksel programlama) | L1-3760 |
| Kutu kapasitesi | Standart kutular (bins of uniform size), birim talep $d_{sc} \in \{0, 1\}$ kutu | L56-59, L597-599, L1524 |
| Tüketim hızı | İş döngüsü başına istasyon $s$ için talep $d_{sc} = 1$ (%45-%50 olasılık) veya 0 | L56-59, L1524-1525 |
| İstasyonlar arası mesafe | Normalize seyahat süreleri: $p_1 = \text{rand}(0.05, 0.2)$, $p_s = p_{s-1} + \text{rand}(0.05, 0.2)$, $R = \lceil p_{|S|} + \text{rand}(0.05, 0.2) \rceil$ | L36-39, L1507-1514 |
| Zaman penceresi | Belirtilmemiş | L1-3760 |
| Handling süresi | Süpermarkette yenileme süresi $d = 4, 8, 12$ döngü; $p_s$ süresi yükleme/boşaltmayı kapsar | L48-51, L1547-1551 |
| Araç hızı | Belirtilmemiş (Tüm zaman parametreleri iş döngüsü süresine normalize edilmiştir) | L625-626 |

**Notlar:** Bağışıklık Klon Seçim Algoritması (NSICSA) kullanılarak karma modelli montaj hatlarında hat yanı envanterini minimize eden çekici tren çizelgeleme ve yükleme optimizasyonu yapılmıştır.

---

**2. logistics-06-00074.txt — Application of Optimization Techniques in the Dairy Supply Chain: A Systematic Review — Mohit Malik, Vijay Kumar Gahlawat, Rahul S Mor, Vijay Dahiya, Mukheshwar Yadav (2022)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Belirtilmemiş | L1-1126 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-1126 |
| Araç sayısı | Belirtilmemiş | L1-1126 |
| Araç kapasitesi | Belirtilmemiş | L1-1126 |
| Simülasyon süresi | Belirtilmemiş | L1-1126 |
| Lead time | Belirtilmemiş | L1-1126 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-1126 |
| Kanban formülü / kart sayısı | Belirtilmemiş | L1-1126 |
| Kutu kapasitesi | Belirtilmemiş | L1-1126 |
| Tüketim hızı | Belirtilmemiş | L1-1126 |
| İstasyonlar arası mesafe | Belirtilmemiş | L1-1126 |
| Zaman penceresi | Belirtilmemiş | L1-1126 |
| Handling süresi | Belirtilmemiş | L1-1126 |
| Araç hızı | Belirtilmemiş | L1-1126 |

**Notlar:** Süt tedarik zincirinde (DSC) optimizasyon, yapay zeka (AI) ve makine öğrenmesi (ML) tekniklerini PRISMA metodolojisiyle inceleyen sistematik bir literatür taraması makalesidir.

---

**3. 1-s2.0-S2405896318307894-main.txt — Planning and dimensioning of a milk-run transportation system considering the actual line consumption — A. Urru, M. Bonini, W. Echelmeyer (2018)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | 1 montaj hattı | L14, L432 |
| İstasyon / durak sayısı | 5 durak (S1 - S5) | L74-75, L435 |
| Araç sayısı | 1 çekici tren (tugger train) | L436-446 |
| Araç kapasitesi | 3 römork, her biri 1 birim yük (UL) taşır = Toplam 3 birim yük (3 ULs) | L446-447 |
| Simülasyon süresi | Saatlik bazda analiz (saatte 5, 10, 12 ürün üretimi) | L452-453, L551 |
| Lead time | Süpermarket hazırlama süresi: 2 dak/UL (3 UL aynı anda 2 dakikada hazırlanır); Bilgi akış süresi: Kanban kart (10 dk), e-Kanban (1-2 dk), direkt sipariş (0 dk) | L449-451, L615-630 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-813 |
| Kanban formülü / kart sayısı | Manuel Kanban kartı, e-Kanban ve direkt sipariş karşılaştırmalı tampon boyutlandırma formülleri sunulmuştur | L61-63, L178-183, L470 |
| Kutu kapasitesi | Standart Birim Yük (unique type of Unit Load - UL) | L433-434 |
| Tüketim hızı | Hat çıktısı: 5, 10 veya 12 ürün/saat; Birim yük tüketimi: 16, 32, 38.4 UL/saat | L452-455, L581-593 |
| İstasyonlar arası mesafe | Toplam güzergah uzunluğu: 124 metre (5 durak eşit dağılmış) | L435-436 |
| Zaman penceresi | Belirtilmemiş | L1-813 |
| Handling süresi | Durak başı değişim süresi: 30 sn/UL; Durak ivmelenme/yavaşlama: 10 sn/durak; Koridor gecikmesi: 20 sn; Süpermarket toplama süresi: 2 dk | L439-446, L449-451 |
| Araç hızı | 1 m/s (3.6 km/s) | L437 |

**Notlar:** Alman Mühendisler Birliği (VDI 5586) standardının "push" yaklaşımı eleştirilerek gerçek hat tüketimine dayalı "pull" (Kanban, e-Kanban, sensör) tampon boyutlandırma metodolojisi geliştirilmiştir.

---

**4. 1-s2.0-S2405896322018420-main.txt — A Milk-run routing and Scheduling model for a Smart Manufacturing System — Francesco Facchini, Giorgio Mossa, Simona De Tullio (2022)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | 1 kaynak atölyesi (welding shop) | L459-460 |
| İstasyon / durak sayısı | Kaynak atölyesindeki çalışma istasyonları (spesifik sayısal adet verilmemiştir) | L459-460, L470 |
| Araç sayısı | 4 çekici tren (4 tugger trains) | L456-457, L460 |
| Araç kapasitesi | Çekici tren başına 3 vagon (3 wagons per tugger train) | L460-461 |
| Simülasyon süresi | Vardiya bazlı operasyon (vardiya başına ~400 sefer) | L461-462, L541 |
| Lead time | Optimize modelde siparişten teslimata maksimum 25 dakika (25 dk üzeri geç teslimat sayılır) | L476-477, L480-482, L508-510 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-708 |
| Kanban formülü / kart sayısı | Belirtilmemiş (Sensör/buton tabanlı dinamik sipariş ve VRPTW algoritması kullanılmıştır) | L462-463, L471, L487 |
| Kutu kapasitesi | Palet birimleri (pallets containing materials) | L458-459 |
| Tüketim hızı | İnsan performansına ve değişken hazırlık sürelerine bağlı stokastik dinamik siparişler | L461-467 |
| İstasyonlar arası mesafe | Mesafeler vardiya başına %23 azaltılmıştır (spesifik matris verilmemiştir) | L83, L540-541 |
| Zaman penceresi | Erken teslimat: < 15 dakika; Geç teslimat: > 25 dakika (Hedef zaman penceresi: 15 - 25 dakika) | L480-487 |
| Handling süresi | Belirtilmemiş (Erken teslimat kaynaklı yeniden taşıma / re-handling engellenmiştir) | L531-534 |
| Araç hızı | Belirtilmemiş | L1-708 |

**Notlar:** Küresel bir otomotiv fabrikasının kaynak atölyesinde Industry 4.0 IoT cihazları (GPS, RFID, tablet, buton) ve VRPTW modeli ile zaman pencereli dinamik milk-run rotalaması gerçekleştirilmiştir.

---

**5. 00207543.2020.txt — Information and digital technologies of Industry 4.0 and Lean supply chain management: a systematic literature review — Miguel Núñez-Merino, Juan Manuel Maqueira-Marín, José Moyano-Fuentes, Pedro José Martínez-Jurado (2020)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Belirtilmemiş | L1-1126 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-1126 |
| Araç sayısı | Belirtilmemiş | L1-1126 |
| Araç kapasitesi | Belirtilmemiş | L1-1126 |
| Simülasyon süresi | Belirtilmemiş | L1-1126 |
| Lead time | Belirtilmemiş | L1-1126 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-1126 |
| Kanban formülü / kart sayısı | Belirtilmemiş | L1-1126 |
| Kutu kapasitesi | Belirtilmemiş | L1-1126 |
| Tüketim hızı | Belirtilmemiş | L1-1126 |
| İstasyonlar arası mesafe | Belirtilmemiş | L1-1126 |
| Zaman penceresi | Belirtilmemiş | L1-1126 |
| Handling süresi | Belirtilmemiş | L1-1126 |
| Araç hızı | Belirtilmemiş | L1-1126 |

**Notlar:** Endüstri 4.0 bilgi ve dijital teknolojileri ile Yalın Tedarik Zinciri Yönetimi (LSCM) arasındaki 78 makaleyi kapsayan sistematik literatür taramasıdır.

---

**6. ec-12-2024-1056en.txt — Route optimization of simultaneous delivery and pick-up in automotive inbound logistics under the milk-run mode in a dual-carbon background — Weiwei Zhang (2024/2026)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | 1 OEM üretim tesisi (4 ana süreç: damgalama, kaynak, boyama, montaj) | L89-91, L1273 |
| İstasyon / durak sayısı | 2 dağıtım merkezi (R1, R2) ve 30 tedarikçi (S1 - S30) | L1272-1273, L1319-1334 |
| Araç sayısı | 3 farklı araç tipi filosu (6.8m, 9.6m, 13m kamyonlar) | L1575-1590 |
| Araç kapasitesi | 6.8m araç: 7t / 31 dolu kutu (124 boş kutu); 9.6m araç: 16t / 45 dolu kutu (180 boş kutu); 13m araç: 30t / 62 dolu kutu (248 boş kutu) | L1576-1590 |
| Simülasyon süresi | 1 günlük operasyon planı | L1271-1272 |
| Lead time | Belirtilmemiş | L1-1614 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-1614 |
| Kanban formülü / kart sayısı | Belirtilmemiş (2E-VRPSPDTW çok amaçlı tam sayı programlama modeli) | L1-1614 |
| Kutu kapasitesi | Standart katlanabilir kutular (boş kutular iç içe geçerek dolu kutunun 1/5'i hacim kaplar) | L120-123 |
| Tüketim hızı | 30 tedarikçiden toplam 650 dolu kutu ve 31.7t - 407.3t arası kargo talebi | L1312-1315 |
| İstasyonlar arası mesafe | Tedarikçiler ve Dağıtım Merkezlerinin (X, Y) koordinat matrisi verilmiştir | L1293-1574 |
| Zaman penceresi | Belirtilen zaman pencereleri (örn. 5:20–7:50, 6:20–8:50, 8:50–11:20, 9:50–12:20) ve Kabul edilebilir genişletilmiş zaman pencereleri (örn. 4:20–11:20, 5:20–12:20, 7:20–14:20) | L1340-1573 |
| Handling süresi | Yükleme/boşaltma hızı ($v_{swk}$): 120 kutu/saat | L1595-1598 |
| Araç hızı | 65 km/saat ($v_{twk} = 65\text{ km/h}$) | L1591-1594 |

**Notlar:** Çift karbon hedefi altında otomotiv girdi lojistiğinde eşzamanlı teslimat ve toplama yapılan 2 kademeli zaman pencereli araç rotalama problemi (2E-VRPSPDTW) geliştirilmiş NSGA-II algoritması ile çözülmüştür.

---

**7. editor_in_chief,+ejers_2569.txt — Supply Chain System Model of Components for Assembly Lines Based on Kanban and Milk Run Methodologies — Victor Hugo Oliveira dos Santos, Marcelo Albuquerque de Oliveira, Gabriela de Mattos Veroneze (2021)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Şirket F (Elektronik): 38 montaj hattı (34'ü aktif); Şirket H (Motosiklet): Montaj hatları | L61, L73, L395 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-693 |
| Araç sayısı | Belirtilmemiş (Besleme arabaları ve çekiciler) | L338, L513 |
| Araç kapasitesi | Belirtilmemiş | L1-693 |
| Simülasyon süresi | 3 üretim vardiyası / günlük operasyon | L59-60, L412 |
| Lead time | Belirtilmemiş | L1-693 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-693 |
| Kanban formülü / kart sayısı | Terazi/ağırlık tabanlı e-Kanban; Sipariş formülü: $E = (Q_m \times \sum I_m) - \text{Minimum stock}$ | L382-389, L430-448 |
| Kutu kapasitesi | Örnek: 1000 adetlik kaynak somunu sepeti (ağırlık $1.8 \pm 0.142\text{ kg}$) | L442-446 |
| Tüketim hızı | Şirket F: 30,000 modem/gün ve 50,000 uzaktan kumanda/gün; Şirket H: 10,000 motosiklet/gün | L59-61, L72-73 |
| İstasyonlar arası mesafe | Depo/besleme sektörü hatlara yaklaşık 2 km uzaklıktadır | L365 |
| Zaman penceresi | Belirtilmemiş | L1-693 |
| Handling süresi | Belirtilmemiş | L1-693 |
| Araç hızı | Belirtilmemiş | L1-693 |

**Notlar:** Manaus Serbest Bölgesi'ndeki Şirket F (Elektronik) ve Şirket H (Motosiklet) fabrikalarında ağırlık sensörlü terazi sistemi ile gerçek zamanlı Kanban ve Milk Run entegrasyonu önerilmiştir.

---

**8. v05-i02-p382_352-3211-5-PB.txt — Milk-run kanban system for raw printed circuit board withdrawal to surface-mounted equipment — Swee Li Chee, Mei Yong Chong, Jeng Feng Chin (2012)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | 3 operasyonel departman (D1: Ambar, D2: İşaretleme LM/MM, D3: 6 SME hattı) | L381-385 |
| İstasyon / durak sayısı | 6 Yüzey Montaj Ekipmanı (SME(1)-SME(6)) istasyonu, 2 işaretleme istasyonu (LM, MM), 1 Ambar (D1) | L382-385 |
| Araç sayısı | 1 - 3 operatör ($n_{op} = 1, 2, 3$) | L456, L470 |
| Araç kapasitesi | Sefer başına maksimum 500 PCB parçası | L503 |
| Simülasyon süresi | 15 gün (vardiya başına 8 saat, günde 3 vardiya, toplam 1,296,000 saniye; 1 gün ısınma) | L433-435 |
| Lead time | Ambar hammadde hazırlık süresi $T_p = 5$ saat; Geleneksel sistemde ambardan hatta teslimat lead time ~3 saat | L283-284, L500 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-978 |
| Kanban formülü / kart sayısı | Makineye özel Kanban kart sayısı ($n_k = 2, 4, 6$) ve toplanacak kart sayısı ($n_r = 2, 4, 6$) | L453-454, L465-468 |
| Kutu kapasitesi | Bir paket ~60 raw PCB; Standart lot boyutu $n_sL_s = 50, 100, 200$ adet; Kutu boyutları: $292\text{ mm} \times 394\text{ mm} \times 166\text{ mm}$ (küçük) ve $394\text{ mm} \times 592\text{ mm} \times 166\text{ mm}$ (büyük) | L286-289, L462-464 |
| Tüketim hızı | Vardiya başına (~8 saat) yaklaşık 3000 birim sipariş | L487-488 |
| İstasyonlar arası mesafe | Operatör yürüme süreleriyle ifade edilmiştir (D1'den B1'e 60 - 180 saniye) | L501-506 |
| Zaman penceresi | Belirtilmemiş | L1-978 |
| Handling süresi | Kanban kart gönderme $T_s = 60\text{ sn}$; Malzeme taşıma/transfer süresi $T_m = 60 - 180\text{ sn}$ | L501-506 |
| Araç hızı | Belirtilmemiş (Operatör yürüme süreleri $T_m$ verilmiştir) | L502-506 |

**Notlar:** Malezya'daki Şirket X elektronik montaj fabrikasında PCB'lerin yüzey montaj ekipmanlarına (SME) beslenmesi için Milk-Run Kanban Sistemi (MRKS) geliştirilmiş ve Witness yazılımıyla 15 günlük simülasyon yapılmıştır.

---

**9. document (1).txt — Simulationsbasierte Analyse eines innerbetrieblichen digitalisierten Milk Run Systems — Nina Vojdani, Patrick Drechsler (2022)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | 1 üretim alanı (3 çalışma alanına bölünmüş) | L648-650 |
| İstasyon / durak sayısı | 15 çalışma istasyonu (3 alana dağıtılmış) | L644, L648-650 |
| Araç sayısı | 1 çekici tren (1 Routenzug) | L631, L649, L715 |
| Araç kapasitesi | Belirtilmemiş (Kutu kapasitesi sınırlaması dinamik e-Kanban ve sefer başına taşınan kutu sayısı ile yönetilir) | L744-750 |
| Simülasyon süresi | 7 günlük simülasyon periyodu | L765, L785-786 |
| Lead time | Geleneksel sistemde saatlik döngü (1 saat); Ortalama Versorgungsfahrt döngü süresi: Geleneksel 8 dk 55 sn, Dijital 11 dk 29 sn | L678-679, L775-778 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-976 |
| Kanban formülü / kart sayısı | 2-Behälter-Kanban-System (İki kutulu Kanban sistemi); Dijital e-Kanban (elektronik bildirim) vs Geleneksel manuel kart toplama | L664-679 |
| Kutu kapasitesi | Standart Kanban kutuları (Kanban-Behälter) | L630, L668-669 |
| Tüketim hızı | Sipariş yüküne bağlı değişken tüketim | L644-646 |
| İstasyonlar arası mesafe | Dijital milk run ile toplam kat edilen mesafe %29.39 düşürülmüştür (kart toplama dahil edildiğinde geleneksel sistem 2.8 kat daha fazla yol kat eder) | L761-770 |
| Zaman penceresi | Belirtilmemiş (Malzeme tükenmeden önce varış şartı) | L715-717 |
| Handling süresi | Belirtilmemiş (Depoda komisyonlama ve yükleme süresi modele dahildir) | L629-631 |
| Araç hızı | Belirtilmemiş | L1-976 |

**Notlar:** Rostock Üniversitesi'nde gerçekleştirilen simülasyon çalışmasında, 15 istasyonlu bir üretim alanında geleneksel sabit turlu Kanban sistemi ile dinamik dijital e-Kanban Milk Run sistemi 7 günlük simülasyonla karşılaştırılmıştır.

---

**10. 10.5505-pajes.2025.39960-5373787.txt — Etmen tabanlı modelleme yöntemi ile tesis içi dinamik bir milk-run sistemi / A dynamic in-plant milk-run system via agent-based modelling — Yasemin Sevim, Latife Görkemli Aykut (2025/2026)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | 1 tesis içi üretim alanı | L715-753 |
| İstasyon / durak sayısı | 10 istasyon (İstasyon 1 - 10) ve 1 Ambar (depo koordinatı 50,0) | L712, L715-753 |
| Araç sayısı | 2 veya 3 tren (Deney faktörü: Number of trains = 2; 3) | L774-775 |
| Araç kapasitesi | 250 veya 400 birim (Deney faktörü: Train capacity = 250; 400 unit) | L778-779 |
| Simülasyon süresi | 7200 dakika (5 gün * 24 saat * 60 dakika) | L765 |
| Lead time | Belirtilmemiş (İstasyon ortalama bekleme süresi: 0.6 - 0.9 dakika) | L906-950 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-1351 |
| Kanban formülü / kart sayısı | Yeniden sipariş noktası (Reorder point): 25 veya 50 birim; İstasyon hammadde stok kapasitesi: 125 veya 150 birim | L776-781 |
| Kutu kapasitesi | Birim malzeme (unit) | L776-779 |
| Tüketim hızı | Üstel dağılımlı talep (Oran parametresi: 0.5 veya 1 birim/dk); İstasyon üretim süreleri: 1, 2, 3, 4, 5 dakika/parça | L721-753, L768-783 |
| İstasyonlar arası mesafe | Koordinat matrisi: Ambar (50,0), İstasyonlar (50,10) ile (50,55) arası metre cinsinden | L712, L718-753 |
| Zaman penceresi | Belirtilmemiş | L1-1351 |
| Handling süresi | İstasyon yükleme/boşaltma süresi $f = 0.6$ dakika | L710 |
| Araç hızı | 5 km/saat = 83.33 m/dakika | L706-708 |

**Notlar:** AnyLogic yazılımında Etmen Tabanlı Modelleme (Agent-Based Modelling) ile dinamik talep altında 5 faktörlü tam faktöriyel deney tasarımı uygulanarak tesis içi milk-run performans ölçütleri analiz edilmiştir.

---

**11. 14977-Article Text-24446-1-10-20250816.txt — Mathematical Modeling of the Vehicle Routing Problem with Relaxed Time Windows and Delay Penalties — Rosa Fitrie, Saib Suwilo, Herman Mawengkang (2025)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Belirtilmemiş | L1-675 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-675 |
| Araç sayısı | Belirtilmemiş | L1-675 |
| Araç kapasitesi | Belirtilmemiş | L1-675 |
| Simülasyon süresi | Belirtilmemiş | L1-675 |
| Lead time | Belirtilmemiş | L1-675 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-675 |
| Kanban formülü / kart sayısı | Belirtilmemiş | L1-675 |
| Kutu kapasitesi | Belirtilmemiş | L1-675 |
| Tüketim hızı | Belirtilmemiş | L1-675 |
| İstasyonlar arası mesafe | Belirtilmemiş | L1-675 |
| Zaman penceresi | Belirtilmemiş | L1-675 |
| Handling süresi | Belirtilmemiş | L1-675 |
| Araç hızı | Belirtilmemiş | L1-675 |

**Notlar:** Gevşetilmiş Zaman Pencereli Araç Rotalama Problemi (VRP-RTW) için ceza fonksiyonlu tam sayı matematiksel programlama modeli geliştirilmiştir. Makalede sayısal veri veya deneysel uygulama yapılmamıştır (L602-604).

---

**12. 978-0-387-77778-8_9.txt — Recent Developments in Dynamic Vehicle Routing Systems — Allan Larsen, Oli B.G. Madsen, Marius M. Solomon (2008)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Belirtilmemiş | L1-1071 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-1071 |
| Araç sayısı | Belirtilmemiş | L1-1071 |
| Araç kapasitesi | Belirtilmemiş | L1-1071 |
| Simülasyon süresi | Belirtilmemiş | L1-1071 |
| Lead time | Belirtilmemiş | L1-1071 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-1071 |
| Kanban formülü / kart sayısı | Belirtilmemiş | L1-1071 |
| Kutu kapasitesi | Belirtilmemiş | L1-1071 |
| Tüketim hızı | Belirtilmemiş | L1-1071 |
| İstasyonlar arası mesafe | Belirtilmemiş | L1-1071 |
| Zaman penceresi | Belirtilmemiş | L1-1071 |
| Handling süresi | Belirtilmemiş | L1-1071 |
| Araç hızı | Belirtilmemiş | L1-1071 |

**Notlar:** Dinamik Araç Rotalama Problemleri (DVRP), GPS/GIS iletişim teknolojileri ve dinamiklik derecesi (degree of dynamism) kavramlarını ele alan Springer kitap bölümüdür.

---

**13. cirrelt-2010-04.txt — Solving Large-Scale Vehicle Routing Problems with Time Windows: The State-of-the-Art — Michel Gendreau, Christos D. Tarantilis (2010)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Belirtilmemiş | L1-842 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-842 |
| Araç sayısı | Belirtilmemiş | L1-842 |
| Araç kapasitesi | Belirtilmemiş | L1-842 |
| Simülasyon süresi | Belirtilmemiş | L1-842 |
| Lead time | Belirtilmemiş | L1-842 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-842 |
| Kanban formülü / kart sayısı | Belirtilmemiş | L1-842 |
| Kutu kapasitesi | Belirtilmemiş | L1-842 |
| Tüketim hızı | Belirtilmemiş | L1-842 |
| İstasyonlar arası mesafe | Belirtilmemiş | L1-842 |
| Zaman penceresi | Belirtilmemiş | L1-842 |
| Handling süresi | Belirtilmemiş | L1-842 |
| Araç hızı | Belirtilmemiş | L1-842 |

**Notlar:** Büyük ölçekli Zaman Pencereli Araç Rotalama Problemleri (VRPTW) için geliştirilen gelişmiş sezgisel ve meta-sezgisel algoritmaları (Solomon ve Gehring & Homberger verisetleri) derleyen durum değerlendirme çalışmasıdır.

---

**14. 614b1f_79608d7857f1466db6b43408362e12b4.txt — Tedarik Zinciri Yönetiminde Milk-Run Modeli: Avantajlar ve Zorluklar — Ali İmran Tatlıbadem, Mesut Selamoğlu (2025)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Belirtilmemiş | L1-603 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-603 |
| Araç sayısı | Belirtilmemiş | L1-603 |
| Araç kapasitesi | Belirtilmemiş | L1-603 |
| Simülasyon süresi | Belirtilmemiş | L1-603 |
| Lead time | Belirtilmemiş | L1-603 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-603 |
| Kanban formülü / kart sayısı | Belirtilmemiş | L1-603 |
| Kutu kapasitesi | Belirtilmemiş | L1-603 |
| Tüketim hızı | Belirtilmemiş | L1-603 |
| İstasyonlar arası mesafe | Belirtilmemiş | L1-603 |
| Zaman penceresi | Belirtilmemiş | L1-603 |
| Handling süresi | Belirtilmemiş | L1-603 |
| Araç hızı | Belirtilmemiş | L1-603 |

**Notlar:** Tedarik zinciri yönetiminde Milk-Run lojistik modelinin teorik temellerini, uygulama alanlarını, avantaj ve dezavantajlarını açıklayan Türkçe kitap bölümüdür.

---

**15. In-plant_milk_run_decision_problems.txt — In-plant Milk Run Decision Problems — Mohammed Alnahhal, Asep Ridwan, Bernd Noche (2014)**

| Parametre | Deger | Satır |
|-----------|-------|-------|
| Hat sayısı | Belirtilmemiş | L1-1077 |
| İstasyon / durak sayısı | Belirtilmemiş | L1-1077 |
| Araç sayısı | Belirtilmemiş | L1-1077 |
| Araç kapasitesi | Belirtilmemiş | L1-1077 |
| Simülasyon süresi | Belirtilmemiş | L1-1077 |
| Lead time | Belirtilmemiş | L1-1077 |
| Güvenlik katsayısı (alpha) | Belirtilmemiş | L1-1077 |
| Kanban formülü / kart sayısı | Belirtilmemiş | L1-1077 |
| Kutu kapasitesi | Belirtilmemiş | L1-1077 |
| Tüketim hızı | Belirtilmemiş | L1-1077 |
| İstasyonlar arası mesafe | Belirtilmemiş | L1-1077 |
| Zaman penceresi | Belirtilmemiş | L1-1077 |
| Handling süresi | Belirtilmemiş | L1-1077 |
| Araç hızı | Belirtilmemiş | L1-1077 |

**Notlar:** Tesis içi milk run sistemlerindeki karar problemlerini (yerleşim, rotalama, çizelgeleme, yükleme, konteynerizasyon) ve Yalın üretim ilkelerini inceleyen IEEE bildirisidir.
