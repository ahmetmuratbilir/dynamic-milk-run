# Dynamic Milk-Run & E-Kanban Projesi - Makale Kataloğu (Grup 1)

Bu doküman, **Dynamic Milk-Run & E-Kanban** projesi kapsamında incelenen 11 akademik makalenin künye bilgilerini, ana konularını, metodolojilerini, makalelerdeki sayısal/operasyonel parametreleri ve projemizin ilgili modülleriyle olan ilişkilerini içermektedir.

---

## 1. 00207543.2020.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | Information and digital technologies of Industry 4.0 and Lean supply chain management: a systematic literature review |
| **Yazarlar** | Miguel Núñez-Merino, Juan Manuel Maqueira-Marín, José Moyano-Fuentes, Pedro José Martínez-Jurado |
| **Yıl** | 2020 |
| **Dergi / Kaynak** | International Journal of Production Research, Vol. 58, No. 16, ss. 5034–5061 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Endüstri 4.0 Bilgi ve Dijital Teknolojileri (BDTI) ile Yalın Tedarik Zinciri Yönetimi (YTZY / LSCM) arasındaki etkileşimi, sinerjiyi ve literatürdeki temel eğilimleri inceleyen kapsamlı bir literatür taramasıdır. |
| **Metodoloji** | Sistematik Literatür Taraması (Systematic Literature Review - SLR) (1996-2019 yılları arasında yayımlanmış 78 makale incelenmiştir). |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş |
| **İstasyon Sayısı** | Belirtilmemiş |
| **Araç Sayısı** | Belirtilmemiş |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Teslimat Süresi (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş |
| **Tüketim Hızı** | Belirtilmemiş |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling (Hazırlama/Yükleme) Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş |

### Projemizle İlişkisi
Projemizin **Sinyal Mimarisi**, IoT/E-Kanban entegrasyonu, Yalın (Kanban/Milk-Run) ilkeleri ile Endüstri 4.0 dijital teknolojilerinin sinerjisinin kavramsal ve teorik çerçevesinin oluşturulmasına katkı sağlar.

---

## 2. 1-s2.0-S0360835215001187-main.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | Dynamic material flow control in mixed model assembly lines |
| **Yazarlar** | Mohammed Alnahhal, Bernd Noche |
| **Yıl** | 2015 |
| **Dergi / Kaynak** | Computers & Industrial Engineering, Vol. 85, ss. 110–119 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Karışık modelli montaj hatlarında (MMAL) makine arızası, hat durması, hatalı parça ve ürün yeniden sıralaması (resequencing) gibi kesintilere (disturbances) karşı tugger tren (milk-run) ile dinamik malzeme akış kontrolü ve emniyet stoğu yönetimidir. |
| **Metodoloji** | Analitik modelleme (rotalama için) ve Tam Sayılı Programlama (Integer Programming - IP) (çizelgeleme ve yükleme problemleri için); E-Kanban ve talep odaklı (demand-oriented) hibrit yaklaşım. |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (Karışık Modelli Montaj Hattı / MMAL) |
| **İstasyon Sayısı** | Matematiksel model değişkeni (Örnek problemde 9 durak / hücre yapısı) |
| **Araç Sayısı** | Formülasyonda dinamik (Tugger tren filosu) |
| **Araç Kapasitesi** | $K$ (Tren başına kutu/bin kapasitesi) |
| **Teslimat Süresi (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | $b_i$ (ideal emniyet stoğu seviyesi) ve doluluk/hizmet oranı ($\delta$) |
| **Tüketim Hızı** | Poisson dağılımı ile modellenen değişken parça talebi ($d_{ik}$) |
| **Mesafe** | Rotalama mesafe ve zaman parametreleri |
| **Zaman Penceresi** | Tren Döngü Süresi (Train Cycle Time - TCT), İstasyon Döngü Süresi (Station Cycle Time - SCT) |
| **Handling (Hazırlama/Yükleme) Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş |

### Projemizle İlişkisi
Dynamic Milk-Run ve E-Kanban entegrasyonu, kesintiler (disturbances), resequencing (yeniden sıralama), starvation (istasyon açlığı) önleme ve dinamik çizelgeleme/yükleme optimizasyonu ile doğrudan projemizin **çekirdek algoritmalarına** katkı sağlar.

---

## 3. 1-s2.0-S0360835224002018-main.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | A multi-objective artificial electric field algorithm with reinforcement learning for milk-run assembly line feeding and scheduling problem |
| **Yazarlar** | Binghai Zhou, Mingda Wen |
| **Yıl** | 2024 |
| **Dergi / Kaynak** | Computers & Industrial Engineering, Vol. 190, Article 110080 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Karışık modelli montaj hatlarında heterojen AGV'lerle milk-run malzeme dağıtımında hat yanı stok (TLI) ve toplam enerji tüketimini (TEC) eşzamanlı minimize etmek için Kanban sayısı ve malzeme kutusu (bin) kapasitesinin ortak optimizasyonudur. |
| **Metodoloji** | Çok amaçlı Yapay Elektrik Alan Algoritması ve SARSA Pekiştirmeli Öğrenme mekanizması (MOAEFASA - Multi-Objective Artificial Electric Field Algorithm with SARSA); Epsilon-Kısıt yöntemi (matematiksel model doğrulaması için). |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (MMAL ortamı) |
| **İstasyon Sayısı** | Matematiksel model düğümleri / istasyonlar |
| **Araç Sayısı** | Heterojen AGV filosu ($m$) |
| **Araç Kapasitesi** | AGV taşıma kapasitesi $D$ / Kutuların fiziki kapasitesi ($C_k$) |
| **Teslimat Süresi (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Emniyet katsayısı / Kanban sayısı ($K_k$) |
| **Tüketim Hızı** | Ürün BOM yapısına göre değişken parça tüketim hızı |
| **Mesafe** | Kat edilen seyahat mesafesi ($c_{ij}$) |
| **Zaman Penceresi** | Teslimat zaman penceresi / çizelgeleme zaman aralığı |
| **Handling (Hazırlama/Yükleme) Süresi** | Yükleme ve boşaltma süreleri ($t_{k,j}$) |
| **Araç Hızı** | AGV hızı (enerji tüketim fonksiyonunda değişken) |

### Projemizle İlişkisi
Kanban sayısı, bin kapasitesi, hat yanı stok minimizasyonu ve AGV/Milk-Run çizelgelemesinin hibrit optimizasyonu; **Kanban & ROP Parametre Hesabı** ve **Simülasyon/Çizelgeleme Modellerimize** katkı sağlar.

---

## 4. 1-s2.0-S2405896318307894-main.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | Planning and dimensioning of a milk-run transportation system considering the actual line consumption |
| **Yazarlar** | Augusto Urru, Marco Bonini, Wolfgang Echelmeyer |
| **Yıl** | 2018 |
| **Dergi / Kaynak** | IFAC-PapersOnLine, Vol. 51, No. 9, ss. 404–409 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | VDI 5586 standardının "push" (itme) bazlı varsayımlarının yetersizliğini ele alarak, gerçek hat tüketimini (pull/çekme) dikkate alan tugger tren milk-run sistemi boyutlandırma ve hat yanı tampon stok (buffer) hesaplama metodolojisidir. |
| **Metodoloji** | Analitik boyutlandırma modeli, VDI 5586 standardını Kanban, e-Kanban ve sensör/buton bazlı bilgi akışı ve teslimat süresi gecikmeleri ile genişleten analitik formülasyon. |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş |
| **İstasyon Sayısı** | Rota üzerindeki durak sayısı (Örnek senaryoda 5 durak: S1-S5) |
| **Araç Sayısı** | Tren sayısı ($n_{trains}$) |
| **Araç Kapasitesi** | Vagon (trailer) sayısı (2-5 vagon) / Taşıma birimi kapasitesi (Unit Load - UL) |
| **Teslimat Süresi (LT)** | Bilgi iletim süresi, sipariş toplama (commissioning) süresi ve taşıma süresi bileşenleri |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Tampon stok güvenlik marjı ($q_{A,H}$) |
| **Tüketim Hızı** | $\lambda_{A,H}$ (Birim yük/saat cinsinden hat tüketim hızı) |
| **Mesafe** | Rota uzunluğu |
| **Zaman Penceresi** | Döngü süresi ($t_{cycle}$), Rota frekansı ($f_r$) |
| **Handling (Hazırlama/Yükleme) Süresi** | Süpermarkette sipariş toplama ve yükleme/boşaltma süresi |
| **Araç Hızı** | Belirtilmemiş |

### Projemizle İlişkisi
VDI 5586 standardı uzantısı olarak E-Kanban sinyal iletim süresi (Lead Time) ve gerçek hat tüketimine dayalı **Hat Yanı Tampon Stok (Buffer Size) Boyutlandırması** ve **Kanban Hesaplamalarında** temel formülasyon sağlar.

---

## 5. 1-s2.0-S2405896322018420-main.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | A Milk-run routing and Scheduling model for a Smart Manufacturing System |
| **Yazarlar** | Francesco Facchini, Giorgio Mossa, Simona De Tullio |
| **Yıl** | 2022 |
| **Dergi / Kaynak** | IFAC-PapersOnLine, Vol. 55, No. 10, ss. 1122–1127 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Akıllı imalat sistemlerinde Fabrika İçi (In-plant) Milk-Run tugger tren teslimatları için Zaman Pencereli Araç Rotalama Problemi (VRPTW) tabanlı dinamik rotalama ve çizelgeleme modelidir. |
| **Metodoloji** | Zaman Pencereli Araç Rotalama Problemi (VRPTW) matematiksel modellemesi (Karma Tam Sayılı Doğrusal Programlama / MILP); Gerçek otomotiv vaka çalışması. |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (Otomotiv montaj tesisi) |
| **İstasyon Sayısı** | Düğüm (node)/müşteri sayısı $n$ (Vaka çalışmasında tanımlı duraklar) |
| **Araç Sayısı** | Filo araç sayısı $m$ (Vaka çalışmasında 3 tugger train) |
| **Araç Kapasitesi** | Araç taşıma kapasitesi $D$ |
| **Teslimat Süresi (LT)** | Zaman pencereleri $[a_j, b_j]$ ve seyahat süreleri |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş |
| **Tüketim Hızı** | İstasyona/düğüme özel malzeme talebi $d_j$ |
| **Mesafe** | Düğümler arası mesafe $c_{ij}$ (Vaka çalışmasında %23 mesafe tasarrufu elde edilmiştir) |
| **Zaman Penceresi** | Zaman penceresi kısıtları $[a_j, b_j]$, izin verilen maksimum rota süresi $T_{k, route}$ |
| **Handling (Hazırlama/Yükleme) Süresi** | Yükleme/boşaltma süresi $t_{k,j}$ |
| **Araç Hızı** | Araç seyir süresi $t_{k,ij}$ üzerinden bağıntılı |

### Projemizle İlişkisi
VRPTW yaklaşımı ile dinamik Milk-Run rotalama, zaman pencereli teslimat çizelgelemesi ve mesafe/maliyet optimizasyonu sağlayarak projemizin **VRPTW & Dinamik Rotalama Modülüne** doğrudan girdi sunar.

---

## 6. 10.5505-pajes.2025.39960-5373787.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | A dynamic in-plant milk-run system via agent-based modelling (Etmen tabanlı modelleme yöntemi ile tesis içi dinamik bir milk-run sistemi) |
| **Yazarlar** | Yasemin Sevim, Latife Görkemli Aykut |
| **Yıl** | 2026 (Kabul: 2025, Yayın: Pamukkale Univ Muh Bilim Derg 32(1), 62-71, 2026) |
| **Dergi / Kaynak** | Pamukkale Üniversitesi Mühendislik Bilimleri Dergisi, Vol. 32, No. 1, ss. 62–71 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Dinamik talep altında tesis içi (in-plant) milk-run taşıma sisteminin etmen tabanlı modelleme (Agent-Based Modelling - ABM) yöntemi ile modellenmesi ve rotalama, çizelgeleme, yükleme süreçlerinin eşzamanlı analizi. |
| **Metodoloji** | Etmen Tabanlı Modelleme (Agent-Based Modelling - ABM) (AnyLogic simülasyon ortamı) ve senaryo analizi. |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (Montaj hattı besleme ortamı) |
| **İstasyon Sayısı** | Örnek uygulamada 6 istasyon |
| **Araç Sayısı** | Tren sayısı (1, 2, 3 ve 4 trenli senaryolar) |
| **Araç Kapasitesi** | Tren kapasitesi (Düşük ve yüksek kapasiteli vagon senaryoları) |
| **Teslimat Süresi (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş |
| **Tüketim Hızı** | Dinamik talep varışları (Poisson / rastgele talep) |
| **Mesafe** | Ortalama kat edilen seyahat mesafesi |
| **Zaman Penceresi** | Rota ve durak zamanları |
| **Handling (Hazırlama/Yükleme) Süresi** | Yükleme ve boşaltma bekleme süreleri |
| **Araç Hızı** | Tren seyir hızı (sabit / değişken) |

### Projemizle İlişkisi
Etmen tabanlı simülasyon (Agent-Based Simulation) yaklaşımı, dinamik talep altında tren/araç sayısı ve kapasitesinin performans ölçütlerine (doluluk oranı, mesafe, bekleme süresi) etkisini değerlendirmede ve **Simülasyon Modülümüze** katkı sağlar.

---

## 7. 14977-Article Text-24446-1-10-20250816.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | Mathematical Modeling of the Vehicle Routing Problem with Relaxed Time Windows and Delay Penalties |
| **Yazarlar** | Rosa Fitrie, Saib Suwilo, Herman Mawengkang |
| **Yıl** | 2025 |
| **Dergi / Kaynak** | Sinkron: Jurnal dan Penelitian Teknik Informatika, Volume 9, Number 3, July 2025, ss. 1835–1842 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Esnetilmiş zaman pencereleri ve gecikme cezaları içeren Araç Rotalama Problemi (VRP-RTW) için toplam seyahat maliyeti ve gecikme cezalarını minimize eden matematiksel modellemedir. |
| **Metodoloji** | Karma Tam Sayılı Programlama (Mixed Integer Linear Programming - MILP) / Matematiksel Formülasyon. |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş |
| **İstasyon Sayısı** | Müşteri/düğüm kümesi $N$ ($i, j \in N$) |
| **Araç Sayısı** | Filo araç kümesi $V$ ($k \in V$) |
| **Araç Kapasitesi** | Araç kapasitesi $q_k$ |
| **Teslimat Süresi (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş |
| **Tüketim Hızı** | Müşteri talebi $d_i$ |
| **Mesafe** | Düğümler arası seyahat maliyeti/mesafesi $c_{ij}$ |
| **Zaman Penceresi** | Esnetilmiş zaman penceresi $[a_i, b_i]$ ve izin verilen esneklik marjı/gecikme süresi $w_{ik}$ |
| **Handling (Hazırlama/Yükleme) Süresi** | Servis süresi $t_{ij}$ |
| **Araç Hızı** | Belirtilmemiş |

### Projemizle İlişkisi
Sert zaman pencerelerinin esnetilmesi (Relaxed Time Windows) ve hat durmasını/gecikmesini cezalandıran maliyet fonksiyonu (Delay Penalties) ile projemizin **VRPTW** ve **Ceza Fonksiyonlu Çizelgeleme Modüllerine** teorik/matematiksel altyapı sunar.

---

## 8. 2837-4713-1-SM.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | IMPROVING THE PERFORMANCE OF MANUFACTURING SYSTEMS BY MODELING WITH SPECIFIC ELEMENTS FROM SIMPY LIBRARY |
| **Yazarlar** | Alin Florin POP, Claudiu INDRE, Florin BLAGA, Voichița HULE, Lajos VEREȘ, Traian BUIDOȘ |
| **Yıl** | 2025 |
| **Dergi / Kaynak** | ACTA TECHNICA NAPOCENSIS - Series: Applied Mathematics, Mechanics, and Engineering, Vol. 68, Special Issue II, July 2025, ss. 571–576 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | İmalat sistemlerinin performansını artırmak amacıyla Python SimPy kütüphanesi kullanılarak Kesikli Olay Simülasyonu (Discrete Event Simulation - DES) ile işleme süreçlerinin ve kaynak kullanımının modellenmesidir. |
| **Metodoloji** | Kesikli Olay Simülasyonu (Discrete Event Simulation - DES) (Python SimPy kütüphanesi). |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (Döküm parça işleme hattı) |
| **İstasyon Sayısı** | 3 temel işleme istasyonu (Torna/CNC Lathe, Taşlama/Grinding, Muayene/Inspection) |
| **Araç Sayısı** | Belirtilmemiş (İstasyon içi kaynaklar ve operatörler) |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Teslimat Süresi (LT)** | İşlem süreleri (Processing Times: Ortalama 15 dk torna, 10 dk taşlama) |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş |
| **Tüketim Hızı** | Parça varış hızı / gelişler arası süre (Üstel dağılım, örn. $\lambda=12$ dk) |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Toplam simülasyon süresi (örn. 480 dk / 8 saatlik vardiya) |
| **Handling (Hazırlama/Yükleme) Süresi** | Bekleme ve hazırlık süreleri |
| **Araç Hızı** | Belirtilmemiş |

### Projemizle İlişkisi
Python SimPy tabanlı kesikli olay simülasyonu mimarisini inceleyerek projemizin **Python Simülasyon Motoru (DES / SimPy)** ve **Stok/Üretim Akış Simülasyonu Modülüne** metodolojik ve kodlama düzeyinde doğrudan altyapı sağlar.

---

## 9. 614b1f_79608d7857f1466db6b43408362e12b4.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | TEDARİK ZİNCİRİ YÖNETİMİNDE MİLK-RUN MODELİ: AVANTAJLAR VE ZORLUKLAR (Bölüm 5, "Disiplinlerarası Sosyal Bilim Çalışmaları: Kavramlar, Modeller ve Uygulamalar" kitabı içinde) |
| **Yazarlar** | Ali İmran Tatlıbadem, Öğr. Gör. Mesut Selamoğlu |
| **Yıl** | 2025 |
| **Dergi / Kaynak** | UBAK Uluslararası Bilimler Akademisi Derneği Yayınevi (Kitap Bölümü, ISBN: 978-625-5923-50-9), Ankara, Mayıs 2025, ss. 144–156 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Tedarik zinciri yönetiminde Milk-Run modelinin operasyonel avantajları, zorlukları, temel ilkeleri, uygulama alanları (otomotiv, gıda, e-ticaret) ve sürdürülebilirliğe katkılarının incelenmesidir. |
| **Metodoloji** | Derleme / Literatür Taraması ve Kavramsal İnceleme. |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş |
| **İstasyon Sayısı** | Belirtilmemiş |
| **Araç Sayısı** | Belirtilmemiş |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Teslimat Süresi (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş |
| **Tüketim Hızı** | Belirtilmemiş |
| **Mesafe** | Belirtilmemiş |
| **Zaman Penceresi** | Belirtilmemiş |
| **Handling (Hazırlama/Yükleme) Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş |

*(Kavramsal derleme çalışması olduğu için sayısal operasyonel parametre içermemektedir).*

### Projemizle İlişkisi
Milk-Run kavramsal altyapısı, Tam Zamanında (JIT) malzeme akışı, stok maliyeti azaltımı, taşıma doluluk oranları ve çevresel sürdürülebilirlik konularında projemizin **Genel Teorik ve Literatür Özetleme Bölümlerine** katkı sağlar.

---

## 10. 978-0-387-77778-8_9.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | Recent Developments in Dynamic Vehicle Routing Systems (Bölüm 9, "The Vehicle Routing Problem" kitabı içinde) |
| **Yazarlar** | Allan Larsen, Oli B.G. Madsen, Marius M. Solomon |
| **Yıl** | 2008 |
| **Dergi / Kaynak** | Springer Science+Business Media / Operations Research/Computer Science Interfaces Series, Vol. 43, ss. 199–218 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Dinamik Araç Rotalama Problemleri (DVRP) üzerindeki literatür gelişimi, dinamizm derecesi (degree of dynamism), gerçek zamanlı bilgi kullanımı (GPS, GIS, GSM) ve dinamik rotalama algoritmalarının değerlendirilmesidir. |
| **Metodoloji** | Literatür Taraması / Derleme ve Takviyeli Yargılama Framework'ü (Degree of Dynamism - DoD metriği formülasyonu). |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş |
| **İstasyon Sayısı** | Dinamik müşteri istekleri sayısı |
| **Araç Sayısı** | Filodaki araç sayısı |
| **Araç Kapasitesi** | Belirtilmemiş (VRP kapasite kısıtı) |
| **Teslimat Süresi (LT)** | Belirtilmemiş |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş |
| **Tüketim Hızı** | Dinamik müşteri çağrı/sipariş geliş hızı |
| **Mesafe** | Rota mesafeleri (GIS tabanlı) |
| **Zaman Penceresi** | Statik ve dinamik zaman pencereleri |
| **Handling (Hazırlama/Yükleme) Süresi** | Servis süreleri |
| **Araç Hızı** | Belirtilmemiş |

*(İnceleme ve kavramsal çerçeve makalesidir).*

### Projemizle İlişkisi
Dinamik Araç Rotalama (DVRP) kavramsal temelleri, **"Degree of Dynamism (DoD)" Metriği** ve gerçek zamanlı sinyal/bilgi akışı (E-Kanban / IoT sinyalleri) altında **Dinamik Yeniden Rotalama (Re-routing) Stratejilerimiz** için teorik taban oluşturur.

---

## 11. 978-3-642-23860-4.txt

### Genel Bilgiler

| Parametre / Alan | Detay |
| :--- | :--- |
| **Başlık** | Change in Manufacturing – Research and Industrial Challenges (Özel Bildiri / Konferans Kitabı: Enabling Manufacturing Competitiveness and Economic Sustainability - CARV2011 Proceedings) <br> *(Not: Kitap İçeriğinde ayrıca "A Planning Approach for In plant Milk Run Processes to Optimize Material Provision in Assembly Systems" - Markus Droste & Jochen Deuse bildirisi yer almaktadır).* |
| **Yazarlar** | H. ElMaraghy, T. AlGeddawy, A. Azab, W. ElMaraghy *(Konferans Kitabı Editörü: Hoda A. ElMaraghy; Droste & Deuse makalesi yazarları: Markus Droste, Jochen Deuse)* |
| **Yıl** | 2012 (Konferans: CARV2011 - Ekim 2011; Springer Yayın Yılı: 2012) |
| **Dergi / Kaynak** | Enabling Manufacturing Competitiveness and Economic Sustainability (Proceedings of the 4th International Conference on Changeable, Agile, Reconfigurable and Virtual Production - CARV2011), Springer, e-ISBN: 978-3-642-23860-4, DOI: 10.1007/978-3-642-23860-4, ss. 2–9 & ss. 605–610 |

### İçerik ve Metodoloji

| Alan | Açıklama |
| :--- | :--- |
| **Ana Konu** | Değişebilir ve yeniden yapılandırılabilir imalat sistemlerinde araştırma zorlukları, evrimsel ürün/sistem platformları, ölçeklenebilir kapasite ve tesis içi milk-run süreçleriyle malzeme besleme optimizasyonudur. |
| **Metodoloji** | Kavramsal Çerçeve, Sistem Dinamikleri (System Dynamics) & İmalat Ortaklık/Değişebilirlik Analizi (Droste & Deuse için analitik milk-run planlama yaklaşımı). |

### Anahtar Parametreler

| Parametre | Değer / Durum |
| :--- | :--- |
| **Hat Sayısı** | Belirtilmemiş (Montaj sistemleri) |
| **İstasyon Sayısı** | Belirtilmemiş / Montaj durakları |
| **Araç Sayısı** | Belirtilmemiş (Milk-run çekicileri/vagonları) |
| **Araç Kapasitesi** | Belirtilmemiş |
| **Teslimat Süresi (LT)** | Süreç planlama ve teslimat süreleri |
| **Alpha ($\alpha$) / Emniyet Katsayısı** | Belirtilmemiş (Tampon stok kısıtları) |
| **Tüketim Hızı** | Ürün çeşidine bağlı malzeme tüketim hızı |
| **Mesafe** | Tesis içi rota mesafeleri |
| **Zaman Penceresi** | Üretim/besleme periyotları |
| **Handling (Hazırlama/Yükleme) Süresi** | Belirtilmemiş |
| **Araç Hızı** | Belirtilmemiş |

### Projemizle İlişkisi
Değişken imalat ortamlarında esnek ve yeniden yapılandırılabilir Milk-Run besleme stratejileri, ürün varyasyonları yönetimi ve stok/kapasite dinamikleri konularında projemizin **Sistem Mimarisi** ve **Esnek Milk-Run Tasarımı** bileşenlerine katkı sağlar.
