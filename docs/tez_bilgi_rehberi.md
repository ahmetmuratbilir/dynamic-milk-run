# DİNAMİK MİLK-RUN VE E-KANBAN KARAR DESTEK SİSTEMİ
## TEZ BİLGİ VE AKADEMİK METODOLOJİ REHBERİ (HAFTA 1 – 5)

> **Bu Dokümanın Amacı:** Bu dosya, projenin Hafta 1 ile Hafta 5 arasındaki tüm mühendislik, matematik, kodlama ve literatür birikimini yüksek lisans / doktora tez hiyerarşisine dönüştüren **yaşayan akademik rehberdir**. İlerleyen haftalarda (Hafta 6–17) yeni bulgular ve modüller bu yapıya eklenerek tezin nihai metni oluşturulacaktır.

---

## 1. ARAŞTIRMA SORULARI VE TEZİN AKADEMİK KATKISI

Bu tez çalışması, endüstriyel lojistikte ve fabrika içi malzeme beslemede şu **4 temel Araştırma Sorusuna (Research Questions - RQ)** cevap vermektedir:

- **RQ1 (Kanban Boyutlandırma):** Stok tüketim hızının dalgalandığı montaj hatlarında, oransal tamponlu ($\alpha$) Dinamik Kanban modeli ($N = \lceil D \cdot LT \cdot (1+\alpha) / C_{kutu} \rceil$) hat başı emniyetini nasıl etkiler?
- **RQ2 (Sinyal Mimarisi):** E-Kanban sistemlerinde eş zamanlı sinyallerin önceliklendirilmesinde Karma Kural (Kritiklik Skoru + FIFO) starvation riskini minimize etmede ne kadar etkilidir?
- **RQ3 (Teorik Basitleştirme vs. Gerçek VRPTW):** Dinamik Kanban hesaplamalarında yapılan "Sabit Lead Time ($LT=45$ dk) ile stok yenilenir" basitleştirmesi ile gerçek seyahat ve elleçleme sürelerini içeren **Zaman Pencereli Araç Rotalama (VRPTW)** kısıtları arasındaki performans farkı nedir?
- **RQ4 (Darboğaz Teşhisi):** Fabrika içi milk-run çekici-römork sistemlerinde asıl operasyonel darboğaz araç kutu kapasitesi ($Q_{arac}$) midir, yoksa seyahat/handling sürelerine dayalı filo büyüklüğü (zaman kısıtı) mıdır?

---

## 2. TEZ HİYERARŞİSİNE GÖRE HAFTA 1–5 HARİTASI

```
TEZ BÖLÜM YAPISI
├── Bölüm 1: Giriş ve Problem Tanımı (Hafta 1)
├── Bölüm 2: Literatür Taraması ve Parametre Soyutlama (Hafta 1-2)
├── Bölüm 3: Dinamik Kanban ve E-Kanban Sinyal Mimarisi Metodolojisi (Hafta 3-4)
├── Bölüm 4: Zaman Pencereli Araç Rotalama (VRPTW) Matematiksel Modeli (Hafta 5)
└── Bölüm 5: Ampirik Bulgular, Teşhis ve Darboğaz Analizi (Hafta 5)
```

### Bölüm 1: Giriş ve Problem Tanımı (Hafta 1)
- **Problem:** Tam Zamanında (JIT) üretim yapan 4 montaj hatlı, 24 istasyonlu bir otomotiv/beyaz eşya montaj fabrikasında, istasyonların stoksuz kalarak hattın durması (starvation) riski.
- **Yaklaşım:** Gerçek fabrika verilerini esnek olarak okuyabilen veya sentetik veri üretebilen modüler `DataLoader` ve `config.json` mimarisinin kurulması.

### Bölüm 2: Literatür Taraması ve Parametre Soyutlama (Hafta 1–2)
- **Akademik Sıkılık:** 32 adet uluslararası makale taranarak fabrika içi lojistik parametre aralıkları çıkarılmıştır.
- **Parametre İkiliği:**
  1. *Literatür Kaynaklı Parametreler:* Oransal Tampon ($\alpha=0.15$, Klenk 2012), Karma Öncelikleme (Facchini 2022, Simić 2020), vb.
  2. *Mühendislik Varsayımları:* Araç sayısı ($2$ adet), Araç kutu kapasitesi ($Q_{arac}=25$ kutu), Max tur süresi ($90$ dk). *Tüm atıflar şeffaflıkla doğrulanmıştır.*

### Bölüm 3: Dinamik Kanban ve Sinyal Mimarisi Metodolojisi (Hafta 3–4)
- **Dinamik Kanban Hesabı:** $N_s = \lceil (D_s \cdot LT \cdot (1+\alpha)) / C_{kutu} \rceil$
- **Reorder Point (ROP) Hesabı (K25):** $ROP_s = D_s^{dk} \cdot LT \cdot (1+\alpha)$
- **Dinamik Zaman Penceresi (K27/K30):** $TW_{bitis} = \max(\min(t_{starv} - 5, t_{sinyal} + 60), t_{sinyal} + LT)$
- **Isınma Periyodu Ayrımı (K32):** Sinyal engellenmeden ilk 45 dk `ISINMA` (23 sinyal), 45–480 dk arası `KARARLI HAL` (159 sinyal) olarak etiketlenmiştir.

### Bölüm 4: VRPTW Matematiksel Modeli ve Rotalama Motoru (Hafta 5)
- **Strateji:** Olay Bazlı Dinamik Sevk (Event-based Dynamic Dispatching, K33).
- **Algoritma:** Nearest Neighbor + 2-opt Heuristik (K34).
- **Amaç Fonksiyonu:** $\min \sum_{k} \sum_{i,j} t_{ij} \cdot x_{kij}$ (TW ihlalleri hard constraint, K35).
- **Multi-Trip Mimarisi:** 2 araç, günde 16 tur (tur başına ortalama 4.62 kutu).

### Bölüm 5: Ampirik Bulgular ve Teşhis Analizi (Hafta 5)
- **Büyük Akademik Bulgular:**
  1. **Teorik vs. Gerçek Starvation Sıçraması:** Hafta 4'teki teorik $LT=45$ dk otomatik yenileme varsayımı altında starvation **%0** iken; Hafta 5 VRPTW seyahat ve elleçleme süreleri eklendiğinde gerçek starvation **%52.08** (6,000 istasyon-dakikası) seviyesine çıkmıştır. VRPTW bir sorun değil, saklı filo yetersizliğini ortaya çıkaran bir **teşhis aracıdır**.
  2. **Kök Neden Tespiti (K36):** Araç doluluk oranı **%18.5**'tir. Darboğaz **kutu kapasitesi ($Q_{arac}$) DEĞİLDİR**. Asıl kısıt **ZAMAN ve ARAÇ SAYISI** kısıtıdır (2 araç × 480 dk = 960 araç-dk).
  3. **Tampon Stoğun Nüanslı Etkisi (S16 Analizi):** S16 en yüksek tüketimine ($D=24$) rağmen $N=2$ (40 kutu tampon) sayesinde durma oranını **%49.2**'de tutabilmiştir. $N=1$ ile başlayan S11 (%81.9) ve S14 (%80.8) gibi istasyonlara göre daha korunaklı kalmış, ancak yetersiz filo nedeniyle durmayı tamamen önleyememiştir.

---

## 3. DEĞİŞİKLİK GÜNLÜĞÜ VE PARAMETRE SOYBİLİMİ (K01 – K36)

| Karar No | İnceleme Konusu | Değer / İfade | Tür | Akademik / Mühendislik Dayanağı |
|:---:|:---|:---|:---:|:---|
| **K01** | Fabrika Düzeni | 4 Hat, 24 İstasyon | Mühendislik | Simetrik sentetik yerleşim |
| **K03** | Araç Sayısı | 2 milk-run aracı ($A_1, A_2$) | Mühendislik | Operasyonel sentetik varsayım |
| **K04** | Araç Kapasitesi | $Q_{arac} = 25$ kutu | Mühendislik | Operasyonel sentetik varsayım (Menanno $Q_{min}=45$) |
| **K07** | Lead Time | $LT = 45$ dakika | Literatür | Klenk et al. (2012) s.12 |
| **K08** | Tampon Oranı | $\alpha = 0.15$ (%15) | Literatür | Klenk et al. (2012) s.12 |
| **K17** | Max Tur Süresi | $90$ dakika / tur | Mühendislik | Lojistik vardiya kısıtı |
| **K25** | ROP Formülü | $ROP = D_{dk} \cdot LT \cdot (1+\alpha)$ | Literatür | Klenk et al. (2012) s.12 |
| **K26** | Sinyal Önceliği | Karma (Kritiklik + FIFO) | Literatür | Facchini (2022) Sayfa 2, Simić (2020) Sayfa 5 |
| **K27** | Dinamik TW | $TW_{bitis} = \min(t_{starv}-5, t+60)$ | Mühendislik | S16 pencere daralması düzeltmesi |
| **K30** | TW Guard | $TW_{bitis} \ge t + LT$ | Mühendislik | Pencere daralma alt sınırı |
| **K31** | S13 Sınır Durumu | Marj %0.8 ($ROP=19.84, N \cdot C=20$) | Matematik | Kanban boyutlandırma edge-case |
| **K32** | Isınma Dönemi | 0-45 dk `ISINMA`, 45-480 dk `KARARLI` | Metodoloji | Ayrık olay simülasyonu warm-up kuralı |
| **K33** | Rotalama Stratejisi | Olay Bazlı Dinamik Sevk | Literatür | Facchini et al. (2022) Sayfa 2 |
| **K34** | VRPTW Algoritması | Nearest Neighbor + 2-opt | Literatür | Facchini et al. (2022) Sayfa 4 |
| **K35** | Amaç Fonksiyonu | Hard TW + Toplam Süre Min | Literatür | Facchini (2022) s.2, CIRRELT (2010) s.2 |
| **K36** | Darboğaz Tespiti | Zaman ve Filo Kısıtı (%18.5 doluluk) | Analiz | Teşhis düzeltmesi |

---

## 4. KOD VE VERİ MİMARİSİ SÖZLÜĞÜ

- `src/data_loader.py`: Veri soyutlama katmanı (`config.json` ile `synthetic` / `real` veri geçişi).
- `src/generate_synthetic_data.py`: Tüketim, mesafe ve istasyon verilerini üreten sentetik veri jeneratörü.
- `src/kanban_hesap.py`: Hafta 3 Dinamik Kanban N hesabı ve LT/α/C duyarlılık analizi.
- `src/ekanban_signal.py`: Hafta 4 E-Kanban sinyal simülatörü (480 dk, 182 sinyal).
- `src/vrptw_solver.py`: Hafta 5 VRPTW rotalama motoru, 182 sinyal taksonomisi ve gerçek starvation hesaplayıcısı.

---

## 5. GELECEK HAFTALAR İÇİN GENİŞLETME PLANI (HAFTA 6 – 17)

- **Hafta 6:** VRPTW Araç Sayısı ve Tur Çizelgeleme Duyarlılık Analizi (K36 teşhisinin çözümü: 2 araç vs 3 araç vs 4 araç karşılaştırması).
- **Hafta 7–8:** Simülasyon Entegrasyonu ve Darboğaz Giderimi.
- **Hafta 9–10:** Geleneksel Sabit Kanban vs. Dinamik E-Kanban + VRPTW Karşılaştırmalı KPI Analizi.
- **Hafta 11–12:** Web Dashboard (Streamlit/Vite UI) Karar Destek Arayüzü.
- **Hafta 13–17:** Nihai Tez Metni Yazımı ve Savunma Hazırlığı.

---

*Bu rehber her yeni haftada elde edilen bulgu, kod ve kararlarla güncellenecektir.*
