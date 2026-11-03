# DEVAM NOTU — 03.11.2026

> Oturum kota nedeniyle durduruldu. Bu dosya kaldığımız yeri ve sıradaki adımı tutar.
> Devam ederken önce bunu okuyun.

---

## ✅ TEMEL HAZIR (03.11.2026) — sıradaki iş: makale metni

- **Makale sayıları:** yalnızca `docs/makale_tablolari.md` (nihai ayar: koordinat ağı, 1440 dk, ısınma sonrası — K105). Üretim: `python -X utf8 -m src.v2_makale_tablolari` (≈4 dk)
- **Ana bulgu (nihai):** dört eşitleme kuralı farkı −17,3 … +2,0 puan arasında değiştirir; Toyota kutularında B → geleneksel, A/C/D → dijital. ⚠️ Önceki "üç farklı kazanan" ifadesi nihai ayarda tutmadı.
- **Hazır metin parçaları:** `literatur_boslugu_analizi.md` §5 (giriş, katkılar, tartışma, sonuç) ve §8 (başlık: Öneri C)
- **Kaynaklar:** 8/9 okundu (K103, K104); yalnızca Alnahhal 2016 eksik — yazarın tezi: duepublico2.uni-due.de/receive/duepublico_mods_00039133
- **Rehber:** `docs/proje_rehberi.html` (eksikler, kritik sorular, belge sırası, ekranlar)
- **Dashboard:** nihai ayarla üretildi (`generate_dashboard_data_v2 --nihai`, ≈25 dk)

---

## ✅ TAMAMLANAN — H2: Boyutlandırma duyarlılığı (K93)

**Durum: bitti, çalışıyor, belgelendi.**

Vojdani & Drechsler (2022) s.5'in karşılaştırma tasarımı (iki sistem, aynı iki kutulu
Kanban) v2 motorunda yeniden kuruldu. **Ana katkı artık kendi modelimizin dışına çıktı.**

**Bulgu:**

| Talep | Kurgu A (ortak tampon) | Kurgu B (politika-tutarlı) | Kayma |
|---|---:|---:|---:|
| Baz | dijital 2,33 puan önde | dijital 0,14 puan önde | 2,19 |
| **Şok +%50** | dijital **9,03** puan önde | geleneksel 0,04 puan önde | **9,07 — sıralama değişti** |

Mekanizma: A'da iki sistem de 48 kart; B'de geleneksel 63, dijital 49 kart alır.

**Üretilenler:**
- `src/v2_boyutlandirma_duyarliligi.py`
- `data/synthetic/v2_boyutlandirma_duyarliligi.csv`
- `docs/figurler/sekil5_boyutlandirma_duyarliligi.png`
- `src/v2_entegre_simulasyon.py` → yeni `kanban_modu="IKI_KUTU"`
- `src/tum_analizleri_calistir.py` → 5/6. adım olarak eklendi
- Belgeler: `karar_gunlugu.md` K93 · `literatur_boslugu_analizi.md` Yol 3

---

## ✅ TAMAMLANAN — D1: Dashboard v2 veri ambarı (K94, 27.10.2026)

- `app.js` → `data/dashboard_scenarios_v2.json` (standalone'da `window.DASHBOARD_DATA_V2`)
- Statik referans `statik_baz`'dan türetiliyor (P2, T=60, VDI)
- Duruş KPI'larında ± %95 GA, altbilgide sürüm damgası
- Mod etiketleri: **Politika-tutarlı (VDI)** / **Eski boyutlandırma (V1)**
- Uyarı bandı kaldırıldı, K92 kapandı
- `make_standalone.py` yeniden yazıldı ve çalışıyor; `dashboard.html` yeniden üretildi
- Doğrulama: headless tarayıcıda 4 araç / α=0,15 / EDD → **%0,37 ± 0,12**

---

## ✅ TAMAMLANAN — H6: Toyota bandı sağlamlığı (K95, 27.10.2026)

- 24/24 istasyon C ≤ %10 günlük talep sınırını aşıyor (K88 yalnız S1 diyordu — düzeltildi)
- K93 kayması **30/30 hücrede pozitif**; Toyota bandında daha büyük (baz +10,2…+10,5, şok +15,8…+18,1), sıralama 12/12 bant hücresinde değişiyor
- ⚠️ Toyota C + şokta geleneksel önde ama **%67 daha fazla WIP** ile → trade-off olarak yazılmalı
- `src/v2_toyota_bandi_duyarliligi.py`, Şekil 6, orkestratör adım 6/8

---

## ✅ TAMAMLANAN — Ara denetim düzeltmeleri (K96) ve dört adalet kuralı (K97), 27.10.2026

- Denetim raporu: https://claude.ai/artifact/MC78BkVvUUvG6bn8hbcTKj
- "13,6 puan" ifadesi 5 belgede düzeltildi: sonuç **eşitleme kuralına bağlı** (B'de fark <1 puan, üstünlük stokta; D eşit WIP'te dinamik 10,9 puan önde)
- K06 formül atfı tez rehberinde Sugimori (1977) yapıldı
- Kaynakça: [1]–[11] dolduruldu, [15] düzeltildi, [24]–[38] eklendi ("doğrulanmalı" notlarına bak)
- **K97 (ana katkı adayı):** A eşit kart / B politika-tutarlı / C eşit hizmet / D eşit WIP. Toyota kutularında şokta 3 farklı kazanan. Şekil 7 (+ `_toyota`). `src/v2_adalet_kurallari.py`
- Motor: `V2Parametre.n_ozel` eklendi (varsayılan None, eski sonuçlar birebir)

---

## ✅ TAMAMLANAN — Y4, H4, H3, H5, Dashboard Kademe 2 ve 3 (27.10.2026)

| Karar | İş | Sonuç |
|---|---|---|
| K98 | Y4 uyarlanan ROP | Toyota kutularında şok kırılganlığı **gerçek** (uyarlama eğri boyunca kaydırır = kart eklemek); eğriler ≈350 WIP'te kesişir |
| K99 | H4 çok vardiya + ısınma | ⚠️ KPI'lar ısınmayı içeriyor (duruş −1,15 / WIP +%5–37 yanlı); kayma 16/16 pozitif; göreli sonuçlar aynı. **Tez tablolarında ısınma sonrası gösterge kullan** |
| K100 | H3 koordinat ağı | Kayma 6/6 pozitif; **Vojdani çelişkisi çözüldü** (koordinat ağında dijital −%21 sefer, −%6 yol). "25–53 m" bandının kaynağı yok → Urru 2018: 20,7 m |
| K101 | H5 OR-Tools referansı | Baz/konsolidasyonda sezgisel %62–69 fazla yol ama daha az gecikme; şokta referans 94–121 teslimi geciktirir (karşılaştırılamaz). Kanıtlanmış alt sınır değil; S8 daralır, kapanmaz |
| K102 | Dashboard Kademe 2 | Yeni sekme: P1/P2/P3, dört adalet kuralı, Pareto, ayrıştırma. ⚠️ K94'ten kalan gömülü v1 sayıları, uydurma doluluk formülü ve geçersiz JSON (NaN) düzeltildi |
| — | Dashboard Kademe 3 | 🔬 Doğrulama sekmesi (sağlamlık tablosu, Welch, replikasyon) + senaryo karşılaştırıcı. D9 (gerçek veri modu) H1'e bağlı |

**Açık kararlar (kullanıcının):**
1. Nihai koşular koordinat ağıyla (K100) ve ısınma sonrası göstergeyle (K99) yapılsın mı? Yapılırsa dashboard ambarı yeniden üretilmeli (`python -X utf8 -m src.generate_dashboard_data_v2`, ~8 dk).
2. Kaynakçadaki "doğrulanmalı" alanları tam metinden kontrol etmek.
3. Alnahhal 2016, Ciemnoczolowski & Bozer 2013, Sugimori 1977'yi kütüphaneden istemek.

**Kalan tek büyük iş:** H1 gerçek veri (dış bağımlı).

---

## 📋 KALAN YOL HARİTASI

Kaynak: `docs/akademik_degerlendirme_ve_yol_haritasi.md` Bölüm C.

| # | İş | Durum | Süre |
|---|---|---|---|
| 1 | Dashboard v2 verisi (D1) | ✅ **bitti (K94)** | — |
| 2 | H2 Vojdani duyarlılığı | ✅ **bitti** | — |
| 3 | H4 Çok vardiyalı kararlı durum (1440 dk) | ✅ **bitti (K99)** | — |
| 4 | H6 α/C Toyota bandı duyarlılığı (K88) | ✅ **bitti (K95)** | — |
| 5 | H3 Koordinat tabanlı mesafe ağı | ✅ **bitti (K100)** | — |
| 6 | Dashboard Kademe 2 (politika/ablation/Pareto panelleri) | ✅ **bitti (K102)** | — |
| 7 | H5 OR-Tools referansı | ✅ **bitti (K101)** | — |
| 8 | Dashboard Kademe 3 (doğrulama sekmesi vb.) | ✅ **D7, D8 bitti** · D9 H1'e bağlı | — |
| ∞ | **H1 Gerçek veri** (dış bağımlı, en yüksek etki) | ⬜ | — |

---

## ⚠️ AÇIK UYARILAR

1. **6 kaynak hâlâ edinilmedi** (K87/K90): Alnahhal 2016 🔴, Ciemnoczolowski & Bozer
   2013 🔴, Schmidt 2016, VDI 5586, Korytkowski 2016, **Sugimori 1977** (K06'nın asıl
   kaynağı). Denetim: `python -X utf8 -m src.kaynak_arsivi_denetimi`
2. **α = 0,15 ve C Toyota bandının dışında** — K95: sonuçlar bantta yön değiştirmiyor; tezde gerekçe olarak Şekil 6 kullanılmalı.

---

## 🔁 HIZLI KOMUTLAR

```bash
# Tüm analizleri yeniden üret (~6 dk; Solomon hariç ~2 dk)
python -X utf8 -m src.tum_analizleri_calistir
python -X utf8 -m src.tum_analizleri_calistir --hizli --atla solomon

# Dashboard v2 ambarını yeniden üret (~8 dk)
python -X utf8 -m src.generate_dashboard_data_v2 --rep 3

# Standalone dashboard.html'i yeniden kur (~1 sn)
python -X utf8 make_standalone.py

# Kaynak arşivi denetimi
python -X utf8 -m src.kaynak_arsivi_denetimi
```

**Ana belgeler:** `literatur_boslugu_analizi.md` (boşluk + hakem yanıtları) ·
`akademik_degerlendirme_ve_yol_haritasi.md` (yol haritası) ·
`karar_gunlugu.md` (K01–K105) · `hafta14_literatur_denetimi_ve_revizyon_raporu.md`
