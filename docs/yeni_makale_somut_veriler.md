# Yeni Makale Somut Veriler (Hafta 6-17 için)

## 1. Körösi 2026 Nature - Filo Boyutlandırma
- **Soru:** Analitik filo boyutlandırma formülü nedir? Bizim 24 istasyon/2 araç için uygulanabilir mi?
- **Çıkarılan Veri (Formüller):**
  - $w = \sum_{i,j | F_{ij}>0} F_{ij}$ (Toplam gerekli teslimat çevrimi)
  - $TC = T_L + \frac{L_d}{v_c} + T_U + \frac{L_e}{v_c}$ (Ortalama bir teslimat çevrim süresi)
  - $WL = w \times TC$ (Saatlik toplam iş yükü)
  - $AT = 60 \times A \times F_t \times E_w$ (Bir aracın saatlik efektif kullanılabilir süresi)
  - $AN = \frac{WL}{AT}$ ve $AN_{final} = \lceil AN \rceil$ (Gerekli araç sayısı)
- **Projemizle İlişkisi:** Evet, uygulanabilir. Hafta 6 filo duyarlılık analizinde (2 vs 3 vs 4 araç senaryoları) trafik sıkışıklığı ($F_t$), kullanılabilirlik ($A$) ve verimlilik ($E_w$) faktörlerini baz alarak kesin araç ihtiyacını belirlemek için **kesinlikle kullanılır**.

## 2. Ramirez 2025 - MIT Tezi
- **Soru:** SimPy ile fabrika içi AGV simülasyonunda hangi KPI'lar kullanılmış? Replikasyon sayısı? Isınma süresi?
- **Çıkarılan Veri:** 
  - Simülasyon Metrikleri (KPI): Çizelgeleme doğruluğu (scheduling accuracy), AGV bekleme süresindeki azalma (AGV idle time reduction) ve trafik sıkışıklığındaki iyileşme (congestion improvement). Ayrıca 40 günlük testte %89.6 doğruluk (accuracy) ve %80.2 hassasiyet (TPR) kullanılmış.
  - Replikasyon Sayısı ve Isınma Süresi: **Bulunamadı.**
- **Projemizle İlişkisi:** Hafta 7-8'deki darboğaz giderimi simülasyonlarında başarıyı ölçmek için KPI referansı olarak **kesinlikle kullanılır**.

## 3. Balikos 2025 - OR-Tools
- **Soru:** Solomon benchmark sonuçlarında 25 müşterili problemlerde NN vs GA vs OR-Tools performans karşılaştırma tablosu var mı? SOMUT sonuç yüzdeleri?
- **Çıkarılan Veri:** 
  - NN (Nearest Neighbor) vs GA (Genetic Algorithm) karşılaştırması: **Bulunamadı.**
  - OR-Tools 25 müşteri (bizim 24 istasyonumuza denk) performansı ve sapma (deviation) oranları (optimal sonuca göre):
    - R1 Tipi: %91.67 başarı, %3.11 sapma
    - R2 Tipi: %100 başarı, %2.7 sapma
    - RC1 Tipi: %75 başarı, %4.64 sapma
    - RC2 Tipi: %100 başarı, %1.87 sapma
    - C1 Tipi: %55.56 başarı, %0.31 sapma
    - C2 Tipi: %100 başarı, %1.52 sapma
- **Projemizle İlişkisi:** Hafta 7-8 darboğaz gideriminde Google OR-Tools kullanılacaksa, kapasite kısıtlı VRPTW için ne kadarlık bir hata payı (ort. %1.5-4.5) bırakmamız gerektiğini hesaplamak için **kesinlikle kullanılır**.

## 4. Wang 2008
- **Soru:** m-VRPTW'de araç sayısı sınırlıyken amaç fonksiyonu nasıl değişiyor? SOMUT formül var mı?
- **Çıkarılan Veri (Formül):**
  - $$ \min \left[ - \sum_{k \in V} \sum_{i \in C} \sum_{j \in N} x_{ijk}, \sum_{k \in V} \sum_{i \in N} \sum_{j \in N} c_{ij} \cdot x_{ijk}, \sum_{k \in V} \sum_{j \in C} x_{0jk} \right] $$
  - (Sırasıyla: 1. Hizmet verilen müşteri sayısını maksimize etme (eksi ile minimize edilir), 2. Toplam mesafeyi minimize etme, 3. Kullanılan araç sayısını minimize etme.)
- **Projemizle İlişkisi:** %18.5 düşük araç doluluğuna rağmen %52 starvation yaşanan projemizde araç kısıtını (2 araç) modellediğimiz için, Hafta 7-8'de istasyon rotalama önceliğini (hizmet verilen istasyon sayısını maksimize etmek) belirlemede **kesinlikle kullanılır**.

## 5. Herrera-Vidal 2026 - SimPy
- **Soru:** Welch warm-up analizi nasıl yapılmış? Kaç replikasyon? Isınma süresi kaç dakika bulunmuş?
- **Çıkarılan Veri:** 
  - Replikasyon Sayısı: 50.
  - Isınma (Warm-up) Süresi: Welch grafiksel stabilizasyon analizi kullanılarak ortalama üretim/bekleme sürelerinin 25-30. dakikalarda stabilize olduğu gözlemlenmiş. Muhafazakar bir yaklaşımla **30 dakika** olarak belirlenmiş.
- **Projemizle İlişkisi:** Hafta 7-8 simülasyon entegrasyonunda kendi belirlediğimiz K32 (45 dk) ısınma süresi kararımızı, akademik geçerliliği olan 50 replikasyon ve benzer bir ısınma süresiyle savunmak için **kesinlikle kullanılır**.

## 6. Efrilianda 2018
- **Soru:** ROP ve SS formüllerinin TAM matematiksel yazılışını çıkar.
- **Çıkarılan Veri (Formüller):**
  - Emniyet Stoku (SS): $$ SS = \sum B_t - (1 - SL) \sum D_t $$ 
    *(B_t: Backorder/Yok satma, SL: Service Level, D_t: Talep)*
  - Sipariş Noktası (ROP): $$ ROP = L_j \times \left( \frac{\sum D_t}{t} \right) + SS $$
    *(L_j: Lead Time, t: Periyot)*
- **Projemizle İlişkisi:** Dinamik tüketim hızı kullanan K25 formülümüze kıyasla oldukça statik (geçmiş talep ortalaması ve hizmet seviyesi hedefine dayalı) bir formüldür. Hafta 9-10'da "Sabit Kanban vs Dinamik E-Kanban karşılaştırması" yapılırken Sabit Kanban'ın referans modeli olarak **kesinlikle kullanılır**.

## 7. Demiray 2024
- **Soru:** COV bazlı emniyet stoku formülü nedir? Bizim sabit alpha=0.15 yerine kullanabilir miyiz?
- **Çıkarılan Veri (Formül):**
  - Melez Model Formülü: $$ SS = k \cdot \sigma_d \cdot \sqrt{Lt} + DOH_{ABC-XYZ} \cdot d_{daily} $$
  - *(Burada COV (Talep Varyasyon Katsayısı) bağımsız bir değişken değil, ürünleri ABC-XYZ sınıflarına ayırıp $DOH_{ABC-XYZ}$ (Elde tutulması gereken gün sayısı) katsayısını belirlemek için kullanılmıştır.)*
- **Projemizle İlişkisi:** Evet, sabit $\alpha = 0.15$ yerine kullanılabilir. Hafta 9-10'daki e-Kanban modelimizde her istasyonun kendi talep dalgalanmasına (COV değerine) göre dinamik $DOH$ (dinamik tampon) belirlenmesini sağlayarak starvation'ı azaltmak için **kesinlikle kullanılır**.
