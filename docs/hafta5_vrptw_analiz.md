# Hafta 5 — VRPTW Rotalama ve Gerçek Starvation Analiz Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`
> 
> > 📝 **ERRATA & METODOLOJİK DÜZELTME NOTU (Hafta 10 Denetimi):**
> > Bu rapordaki ilk %52.08'lik duruş değeri ve 182 sinyal taksonomisi, hat başı stok tavanının ($stok \le N \times C$) sınırlandırılmadığı erken dönem simülasyon çıktısıdır. Hafta 10 denetiminde raf-tavanı kısıtı ($stok \le N \times C$) ve tam zaman serisi simülasyonu uygulandığında, 2 araçlık baz duruş oranı **%53.01** (EDD) ve **%56.48** (KRİTİKLİK) olarak revize edilmiştir. K36 kök neden tespiti (kutu kapasitesi değil, zaman ve filo kısıtı) geçerliliğini tam olarak korumaktadır.

**Uygulanan Kararlar:** K03, K04, K17, K33, K34, K35, K36, K57 — bkz. `karar_gunlugu.md`


---

## 1. 182 Sinyalin Tam Taksonomisi

| Teslimat Durumu | Sinyal Sayısı | Oran (%) | Açıklama |
|-----------------|---------------|----------|----------|
| Zamanında Teslim | 17 | %9.3 | Varış dk ≤ TW_bitis (TW İhlalsiz) |
| Gecikmeli Teslim | 55 | %30.2 | Varış dk > TW_bitis (TW İhlalli) |
| Karşılanamayan | 110 | %60.4 | 480 dk vardiyada araç zamanı yetmedi |
| **Toplam** | **182** | **%100.0** | Matematiksel olarak tam kapandı |

---

## 2. 🚨 Darboğaz ve Kök Neden Teşhisi (K36)

- **Kutu Kapasitesi Kullanımı:** Ortalama **4.62 kutu/tur** (Kapasite: 25 kutu, Doluluk: **%18.5**)
- **Kök Neden Tespiti:** Kutu kapasitesi ($Q_{arac}$) **darboğaz DEĞİLDİR**. Asıl kısıt **ZAMAN ve ARAÇ SAYISI** kısıtıdır (2 araç × 480 dk = 960 araç-dk, max 16 tur). Araç kutu kapasitesini artırmak (25 → 35) darboğazı çözmez.

---

## 3. Gerçek Starvation (Stoksuz Kalma) Analizi ve Metodolojik Çerçeveleme

- **Toplam Operasyon Süresi:** 11,520 istasyon-dakikası (24 istasyon × 480 dk)
- **Gerçekleşen Starvation Süresi:** 6,000 istasyon-dakikası
- **Fabrika Genel Durma Oranı:** **%52.08**

> 💡 **Metodolojik Metrik Tespiti:** 
> VRPTW yöntemi starvation'a neden olmamış, aksine Hafta 4'teki teorik basitleştirmelerin ($LT=45$ dk otomatik stok yenileme) arkasında saklanan filo yetersizliğini (2 araç) ortaya çıkaran gerçekçi bir **teşhis aracı** olmuştur. Çözüm yine Hafta 6'da VRPTW duyarlılık analiziyle (doğru filo büyüklüğünün bulunması) aranacaktır.

---

## 4. Tam 24 İstasyonluk Starvation Dağılım Tablosu

| Sıra | İstasyon ID | Hat | Starvation Süresi (dk) | Fabrika Vardiya Durma Oranı (%) | İnceleme Notu |
|:---:|:---:|:---:|:---:|:---:|:---|
| 1 | **S11** | Hat-2 | 393 dk | %81.9 | Yüksek tüketim ($D=16$), $N=1$ |
| 2 | **S14** | Hat-3 | 388 dk | %80.8 | Yüksek tüketim ($D=18$), $N=1$ |
| 3 | **S22** | Hat-4 | 347 dk | %72.3 | Hat-4 sonu, uzun seyahat süresi |
| 4 | **S7** | Hat-2 | 308 dk | %64.2 | Tüketim $D=21$, $N=1$ |
| 5 | **S9** | Hat-2 | 290 dk | %60.4 | Tüketim $D=19$, $N=1$ |
| 6 | **S2** | Hat-1 | 285 dk | %59.4 | Tüketim $D=18$, $N=1$ |
| 7 | **S21** | Hat-4 | 276 dk | %57.5 | Tüketim $D=13$, $N=1$ |
| 8 | **S8** | Hat-2 | 274 dk | %57.1 | Tüketim $D=13$, $N=1$ |
| 9 | **S1** | Hat-1 | 264 dk | %55.0 | Tüketim $D=22$, $N=1$ |
| 10 | **S24** | Hat-4 | 259 dk | %54.0 | Hat-4 en uç nokta ($D=21$), $N=1$ |
| 11 | **S20** | Hat-4 | 259 dk | %54.0 | Tüketim $D=16$, $N=1$ |
| 12 | **S23** | Hat-4 | 255 dk | %53.1 | Tüketim $D=12$, $N=1$ |
| 13 | **S5** | Hat-1 | 254 dk | %52.9 | Tüketim $D=12$, $N=1$ |
| 14 | **S19** | Hat-4 | 246 dk | %51.2 | Tüketim $D=20$, $N=1$ |
| 15 | **S4** | Hat-1 | 245 dk | %51.0 | Tüketim $D=20$, $N=1$ |
| 16 | **S3** | Hat-1 | 243 dk | %50.6 | Tüketim $D=15$, $N=1$ |
| 17 | **S16** | Hat-3 | 236 dk | **%49.2** | 💡 $N=2$ tamponu, benzer/daha düşük tüketimli $N=1$ olan istasyonlara (S11 %81.9, S14 %80.8) göre S16'yı belirgin şekilde korumuştur; ancak mevcut filo kısıtları altında starvation'ı tamamen önleyememiştir. |
| 18 | **S12** | Hat-2 | 219 dk | %45.6 | Tüketim $D=14$, $N=1$ |
| 19 | **S18** | Hat-3 | 205 dk | %42.7 | Tüketim $D=14$, $N=1$ |
| 20 | **S17** | Hat-3 | 198 dk | %41.2 | Tüketim $D=17$, $N=1$ |
| 21 | **S10** | Hat-2 | 152 dk | %31.7 | Tüketim düşük ($D=11$), $N=1$ |
| 22 | **S15** | Hat-3 | 149 dk | %31.0 | Tüketim $D=15$, $N=1$ |
| 23 | **S6** | Hat-1 | 145 dk | %30.2 | Depoya yakın konum ($D=17$), $N=1$ |
| 24 | **S13** | Hat-3 | 110 dk | **%22.9** | İlk sinyali simülasyon başında aldığı ve hızlı servis yapıldığı için en düşük durma süresi |

---

*Rapor Sonu — Hafta 5*
