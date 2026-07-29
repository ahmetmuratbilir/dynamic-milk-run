# Hafta 1 — Literatür Özeti
## Dinamik Milk-Run & E-Kanban Karar Destek Sistemi

> **Not:** Aşağıdaki özetler, elimizde bulunan referanslara dayanarak hazırlanmıştır.
> Her makalenin okunması ve notların çıkarılması senin görevin; bu belge sadece
> bir başlangıç çerçevesi ve arama rehberi sunuyor.

---

## 1. E-Kanban / Dinamik Kanban Literatürü

### 1.1 Pekarcikova et al. — Material Flow Optimization through E-Kanban System Simulation

**Temel Katkı:**
Fiziksel Kanban kartlarını elektronik sisteme taşıyan bu çalışma, malzeme akışında
simülasyon tabanlı optimizasyonun nasıl uygulandığını gösteriyor.

**Bizim için önemli noktalar:**
- E-Kanban'da "sinyal" kavramı: fiziksel kart boşaldığında sistemin nasıl haberdar edildiği
- Malzeme akışındaki darboğazların tespitinde simülasyon kullanımı

**Proje bağlantısı:** Sinyal tetikleme mekanizması tasarımımıza (Hafta 4) doğrudan girdi sağlayacak.

---

### 1.2 Pekarcikova et al. — Simulation Testing of the E-Kanban to Increase Efficiency of Logistics Processes

**Temel Katkı:**
E-Kanban sisteminin verimlilik üzerindeki etkisini simülasyon testleriyle ölçen çalışma.
Önceki makalenin devamı niteliğinde.

**Bizim için önemli noktalar:**
- Lojistik verimliliği nasıl KPI'larla ölçülür?
- Simülasyon koşulları (parametreler, senaryo kurgusu) nasıl tasarlanır?

**Proje bağlantısı:** Hafta 9'daki Sabit vs Dinamik simülasyon kurgumuza metodoloji referansı.

---

### 1.3 Jarupathirun et al. — Supply Chain Efficiencies Through E-Kanban: A Case Study

**Temel Katkı:**
Gerçek bir tedarik zincirinde E-Kanban uygulaması. Teorinin sahaya nasıl taşındığını
somut verilerle gösteriyor.

**Bizim için önemli noktalar:**
- Kanban kart sayısı nasıl hesaplandı?
- Uygulama öncesi/sonrası KPI karşılaştırması nasıl yapıldı?
- Reorder point nasıl belirlendi?

**Proje bağlantısı:** KPI tanımlarımıza ve formül doğrulamasına referans.

---

### 1.4 Elloumi, Ammar & Benaissa — Particle Swarm Optimization for Adaptive Kanban System

**Temel Katkı:**
Kanban kart sayısını sabit tutmak yerine talebe göre dinamik olarak ayarlayan bir
adaptif sistem. PSO (Parçacık Sürü Optimizasyonu) algoritması kullanmış.

**Bizim için önemli noktalar:**
- "Adaptif" (dinamik) Kanban fikrinin teorik temeli bu makalede
- D parametresinin (tüketim hızı) dinamik güncellenmesi mantığı

**Proje bağlantısı:** Dinamik N formülümüzün akademik meşruiyeti için temel kaynak.
> ⚠️ Dikkat: Biz PSO kullanmıyoruz. Formülde D'yi periyodik olarak güncellemek yeterli.

---

### 1.5 Simić et al. — Modelling Material Flow Using Milk Run and Kanban Systems in Automotive Industry

**Temel Katkı:**
Otomotiv sanayiinde hem Milk-run hem Kanban sistemini birlikte modelleyen nadir çalışmalardan biri.
İki sistemi entegre eden mimariyi somut örnekle anlatıyor.

**Bizim için önemli noktalar:**
- Milk-run ve Kanban entegrasyonu nasıl kurgulanıyor?
- Otomotiv bağlamındaki süpermarket (hat yanı depo) yapısı

**Proje bağlantısı:** İki bileşeni (Kanban + Milk-run) birbirine bağlayan mimarinin referansı.
Bu makaleyi mutlaka oku — projenin genel iskeletine en yakın çalışma bu.

---

## 2. Milk-Run Literatürü

### 2.1 Sevim & Görkemli Aykut — A Dynamic In-Plant Milk-Run System via Agent-Based Modelling

**Temel Katkı:**
Fabrika içi milk-run sistemini ajan tabanlı modellemeyle dinamikleştiriyor.
Talep değişikliklerine gerçek zamanlı tepki veren bir sistem önerisi.

**Bizim için önemli noktalar:**
- "Dinamik" milk-run ne anlama geliyor? (sabit tur vs. talebe duyarlı tur farkı)
- Yeniden rotalama (re-routing) tetikleme koşulları

**Proje bağlantısı:** What-if senaryolarımızdaki (Hafta 10) re-routing mantığına referans.
> ⚠️ Biz ajan tabanlı modelleme yapmıyoruz, ama dinamik tur fikri doğrudan ilgili.

---

### 2.2 Menanno et al. — Optimizing Milk-Run System and IT-based Kanban with AI

**Temel Katkı:**
IT altyapısı ve yapay zeka ile desteklenmiş bir Kanban + Milk-run sistemi.

**Bizim için önemli noktalar:**
- IT tabanlı Kanban sisteminin bileşenleri
- Milk-run optimizasyonunda iyileştirme kriterleri (mesafe, zaman)

**Proje bağlantısı:** Dashboard tasarımımıza (Hafta 11) sistem mimarisi referansı.
> ⚠️ "AI" kısmını çalışmamıza ekleme — kapsam sınırları gereği.

---

### 2.3 dos Santos et al. — Supply Chain System Model Based on Kanban and Milk Run Methodologies

**Temel Katkı:**
Kanban ve Milk-run metodolojilerini birleştiren bir tedarik zinciri modeli.

**Bizim için önemli noktalar:**
- İki metodoloji nasıl entegre edilir?
- Model kurulum adımları

**Proje bağlantısı:** Metodoloji bölümü (Hafta 14, makale) için çerçeve referansı.

---

### 2.4 Droste & Deuse — A Planning Approach for In-Plant Milk Run Processes

**Temel Katkı:**
Montaj sistemlerinde malzeme tedariğini optimize etmek için milk-run planlama yaklaşımı.
Fabrika içi lojistiğe odaklanan pratik bir çerçeve sunuyor.

**Bizim için önemli noktalar:**
- Tur planlama kriterleri (hangi istasyonlar hangi sırayla?)
- Yükleme/boşaltma (handling) sürelerinin modele dahil edilmesi

**Proje bağlantısı:** Hafta 6'daki handling süresi kısıtlarının modellenmesine referans.

---

### 2.5 Alnahhal & Noche — Dynamic Material Flow Control in Mixed Model Assembly Lines

**Temel Katkı:**
Karma model montaj hatlarında dinamik malzeme akışı kontrolü.

**Bizim için önemli noktalar:**
- Karma (mixed) üretim ortamında Kanban sayısının dinamik ayarlanması
- Stok yönetimi ve hat besleme arasındaki denge

**Proje bağlantısı:** Farklı parça/kutu tiplerini (mixed load) içeren kapasite kısıtlarına referans.

---

### 2.6 Vojdani & Drechsler — Simulationsbasierte Analyse eines Milk Run Systems

**Temel Katkı:**
Dijitalleştirilmiş bir milk-run sisteminin simülasyon tabanlı analizi (Almanca kaynak).

**Bizim için önemli noktalar:**
- Dijital milk-run sistemi bileşenleri
- Simülasyon ile performans değerlendirme metodolojisi

**Proje bağlantısı:** Hafta 9 simülasyon kurgumuza metodoloji referansı.

---

## 3. VRPTW Literatürü

### 3.1 Solomon & Desrosiers (1988) — Time Window Constrained Routing and Scheduling Problems

**Temel Katkı:**
VRPTW'nin temel/kurucu makalesi. Zaman pencereli rotalama problemini ilk kez
sistematik biçimde tanımlayan çalışma. 37 yıllık ama hâlâ zorunlu referans.

**Bizim için önemli noktalar:**
- Zaman penceresi [a_i, b_i] tanımı — erken teslimat (a_i) ve geç teslimat (b_i)
- Problem formülasyonu: düğüm, kenar, araç, kapasite, zaman

**Proje bağlantısı:** VRPTW matematiksel modelimizin (Hafta 5) temel referansı.
Mutlaka oku — makale metodoloji bölümünde kesinlikle alıntılanacak.

---

### 3.2 Bräysy & Gendreau — Vehicle Routing Problem with Time Windows (Part I & II)

**Temel Katkı:**
VRPTW için geliştirilen çözüm algoritmalarını kapsamlı biçimde inceleyen survey makalesi.
Part I: Tam çözüm yöntemleri. Part II: Sezgisel ve meta-sezgisel yöntemler.

**Bizim için önemli noktalar:**
- OR-Tools'un içinde kullandığı Local Search algoritmalarının teorik arka planı
- Hangi algoritma hangi koşulda daha iyi?

**Proje bağlantısı:** Hafta 7'deki algoritma seçimimizi akademik olarak gerekçelendirmek için.

---

### 3.3 Larsen, Madsen & Solomon — Partially Dynamic Vehicle Routing

**Temel Katkı:**
Tamamen dinamik değil, kısmen dinamik araç rotalama. Siparişler başlangıçta değil,
sistem çalışırken gelir — bu bizim E-Kanban sinyal modelimize çok yakın.

**Bizim için önemli noktalar:**
- "Partially dynamic" kavramı: bazı siparişler önceden bilinir, bazıları gelir
- Yeni sipariş geldiğinde rotayı güncelleme mantığı

**Proje bağlantısı:** E-Kanban sinyali → VRPTW tetikleme zincirinin teorik temeli.
Bu kavram savunmada "neden dinamik?" sorusuna güçlü bir cevap verir.

---

## 4. Boşluk Analizi (Gap Analysis)

Literatürde ne var, bizim çalışmamız neyi birleştiriyor?

| Literatürde yaygın olan | Bizim çalışmamızda |
|------------------------|-------------------|
| E-Kanban veya Milk-run, ayrı ayrı | **İkisi entegre** — E-Kanban sinyali VRPTW'yi tetikliyor |
| Statik Kanban sayısı | **Dinamik N** — tüketim hızına göre periyodik güncelleme |
| Tek politika karşılaştırması yok | **Sabit vs Dinamik** politika karşılaştırması simülasyonla |
| Gerçek zamanlı dashboard nadir | **Karar destek arayüzü** — depo yöneticisi kullanabilir |

> **Not:** Bu boşluk analizi, makale Giriş ve Sonuç bölümlerinde doğrudan kullanılabilir.
> Ancak son cümleleri kendi dilinde yeniden yazacaksın (intihal riski).

---

## 5. Okuma Öncelik Sırası (Öneri)

Zamanın kısıtlıysa önce bunları oku:

1. 🔴 **Simić et al.** — İki sistemi birleştiriyor, projeye en yakın
2. 🔴 **Solomon & Desrosiers (1988)** — VRPTW'nin temeli, makale için zorunlu
3. 🟡 **Larsen, Madsen & Solomon** — Dinamik rotalama mantığı
4. 🟡 **Elloumi et al.** — Dinamik Kanban'ın teorik dayanağı
5. 🟢 **Diğerleri** — Zaman kalırsa

---

*Hazırlayan: AI (teknik proje ortağı) | Tarih: Hafta 1*
*Bu belge iskelet/başlangıç noktasıdır — okuma notlarını sen ekleyeceksin.*
