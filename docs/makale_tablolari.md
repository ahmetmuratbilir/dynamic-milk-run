# Makale Tabloları — Nihai Ayar

> Üretim: `python -X utf8 -m src.v2_makale_tablolari` · 03.11.2026 · K105
> Ayar: koordinat tabanlı mesafe ağı (Urru vd. 2018 durak aralığı, K100), 1440 dk (3 vardiya), duruş ve WIP ısınma sonrası (90 dk, K78/K99). 3 araç, 12 replikasyon. Sayılar sentetik veriyle elde edilmiştir.
> Önceki betiklerin (K93–K98) sayıları motor varsayılanlarıyla üretilmiştir; göreli sonuçlar aynıdır, mutlak değerler bu tablolardan alınmalıdır.

## Tablo 1 · Politika karşılaştırması

Her politika kendi formülüyle boyutlandırılmıştır (P1/P2: $N = 1 + \lceil D\,T(1+\alpha)/C \rceil$, P3: $N = 1 + \lceil ROP/C \rceil$). 3 araç, 12 replikasyon, ortalama ± %95 GA.

**Baz talep**

| Politika | Takt | Duruş (%) | Ort. WIP (adet) | Kart | Sefer | Yol (km) | Araç doluluğu (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| P1 | 30 dk | 0,00 ± 0,00 | 764 | 48 | 141,0 | 68,0 | 32,0 |
| P1 | 60 dk | 1,02 ± 0,17 | 775 | 63 | 69,0 | 33,3 | 32,0 |
| P1 | 90 dk | 19,28 ± 0,51 | 297 | 73 | 45,0 | 21,7 | 32,0 |
| P1 | 120 dk | 35,72 ± 0,41 | 221 | 87 | 33,0 | 15,9 | 32,0 |
| P2 | 30 dk | 0,02 ± 0,01 | 501 | 48 | 141,0 | 68,0 | 14,6 |
| P2 | 60 dk | 0,30 ± 0,07 | 648 | 63 | 69,0 | 33,3 | 29,2 |
| P2 | 90 dk | 0,13 ± 0,03 | 716 | 73 | 45,0 | 21,7 | 43,7 |
| P2 | 120 dk | 0,14 ± 0,04 | 872 | 87 | 33,0 | 15,9 | 58,4 |
| P3 | sinyal · konsolidasyon | 0,11 ± 0,02 | 379 | 49 | 53,9 | 30,8 | 38,3 |
| P3 | sinyal · anında | 0,00 ± 0,00 | 545 | 49 | 387,5 | 98,0 | 5,4 |

**Talep şoku +%50**

| Politika | Takt | Duruş (%) | Ort. WIP (adet) | Kart | Sefer | Yol (km) | Araç doluluğu (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| P1 | 30 dk | 0,01 ± 0,01 | 704 | 48 | 141,0 | 68,0 | 32,0 |
| P1 | 60 dk | 23,81 ± 0,47 | 195 | 63 | 69,0 | 33,3 | 32,0 |
| P1 | 90 dk | 47,86 ± 0,37 | 125 | 73 | 45,0 | 21,7 | 32,0 |
| P1 | 120 dk | 59,14 ± 0,29 | 104 | 87 | 33,0 | 15,9 | 32,0 |
| P2 | 30 dk | 0,99 ± 0,09 | 409 | 48 | 141,0 | 68,0 | 21,9 |
| P2 | 60 dk | 4,64 ± 0,22 | 524 | 63 | 69,0 | 33,3 | 42,3 |
| P2 | 90 dk | 4,47 ± 0,21 | 565 | 73 | 45,0 | 21,7 | 63,1 |
| P2 | 120 dk | 5,39 ± 0,20 | 699 | 87 | 33,0 | 15,9 | 83,8 |
| P3 | sinyal · konsolidasyon | 2,78 ± 0,09 | 331 | 49 | 80,3 | 43,3 | 37,9 |
| P3 | sinyal · anında | 0,00 ± 0,00 | 502 | 49 | 380,1 | 113,8 | 8,3 |

## Tablo 2 · Boyutlandırma tasarımının karşılaştırmaya etkisi

Geleneksel: P2, T = 60 dk. Dijital: P3, konsolidasyonlu sevk. Kurgu A: her iki sistemde aynı iki kutulu tampon (Vojdani & Drechsler 2022 s.5). Kurgu B: her sistem kendi formülüyle. Fark = dijital − geleneksel duruş (puan).

| Kutu | Talep | Kurgu | Kart (gel./dij.) | Duruş gel. (%) | Duruş dij. (%) | Fark | WIP farkı | Önde |
|---|---|---|---|---:|---:|---:|---:|---|
| mevcut | Baz talep | A | 48/48 | 2,54 | 0,12 | −2,42 ± 0,22 | %+1 | dijital |
| mevcut | Baz talep | B | 63/49 | 0,30 | 0,11 | −0,20 ± 0,08 | %−41 | dijital |
| mevcut | Talep şoku +%50 | A | 48/48 | 13,60 | 2,78 | −10,82 ± 0,38 | %+1 | dijital |
| mevcut | Talep şoku +%50 | B | 63/49 | 4,64 | 2,78 | −1,86 ± 0,24 | %−37 | dijital |
| toyota | Baz talep | A | 48/48 | 11,51 | 0,25 | −11,27 ± 0,41 | %+35 | dijital |
| toyota | Baz talep | B | 72/72 | 0,13 | 0,23 | +0,11 ± 0,04 | %−36 | geleneksel |
| toyota | Talep şoku +%50 | A | 48/48 | 23,52 | 7,56 | −15,96 ± 0,60 | %+14 | dijital |
| toyota | Talep şoku +%50 | B | 72/72 | 4,88 | 6,85 | +1,97 ± 0,61 | %−36 | geleneksel |

- mevcut kutular, baz talep: kayma +2,23 puan; önde olan dijital → dijital.
- mevcut kutular, talep şoku +%50: kayma +8,96 puan; önde olan dijital → dijital.
- toyota kutular, baz talep: kayma +11,37 puan; önde olan dijital → geleneksel.
- toyota kutular, talep şoku +%50: kayma +17,93 puan; önde olan dijital → geleneksel.

## Tablo 3 · Dört adalet kuralı

A eşit kart (Vojdani & Drechsler 2022) · B politika-tutarlı formül (Urru vd. 2018; VDI 5586) · C eşit hizmet düzeyi, duruş ≤ %1 (Alnahhal & Noche 2015) · D eşit WIP. C'de kazanan WIP'e, diğerlerinde duruşa göre belirlenir; Pareto sütunu iki ölçütü birlikte değerlendirir.

**Mevcut kutular**

| Talep | Kural | Kazanan | Δ duruş (puan) | Δ WIP | Pareto |
|---|---|---|---:|---:|---|
| Baz talep | A · Eşit kart | **Dijital** | −2,42 ± 0,22 | %+1 | Dijital baskın |
| Baz talep | B · Politika-tutarlı | **Dijital** | −0,20 ± 0,08 | %−41 | Dijital baskın |
| Baz talep | C · Eşit hizmet düzeyi | **Dijital** | −0,03 ± 0,08 | %−56 | Dijital baskın |
| Baz talep | D · Eşit WIP | **Dijital** | −12,13 ± 0,19 | %+0 | Dijital baskın |
| Talep şoku +%50 | A · Eşit kart | **Dijital** | −10,82 ± 0,38 | %+1 | Dijital baskın |
| Talep şoku +%50 | B · Politika-tutarlı | **Dijital** | −1,86 ± 0,24 | %−37 | Dijital baskın |
| Talep şoku +%50 | C · Eşit hizmet düzeyi | **Dijital** | +0,77 ± 0,06 | %−40 | baskınlık yok (takas) |
| Talep şoku +%50 | D · Eşit WIP | **Dijital** | −17,34 ± 0,32 | %+0 | Dijital baskın |

- Baz talep: 1 farklı sonuç (A → Dijital, B → Dijital, C → Dijital, D → Dijital).
- Talep şoku +%50: 1 farklı sonuç (A → Dijital, B → Dijital, C → Dijital, D → Dijital).

**Toyota kutuları (C ≤ günlük talebin %10’u)**

| Talep | Kural | Kazanan | Δ duruş (puan) | Δ WIP | Pareto |
|---|---|---|---:|---:|---|
| Baz talep | A · Eşit kart | **Dijital** | −11,27 ± 0,41 | %+35 | baskınlık yok (takas) |
| Baz talep | B · Politika-tutarlı | **Geleneksel** | +0,11 ± 0,04 | %−36 | baskınlık yok (takas) |
| Baz talep | C · Eşit hizmet düzeyi | **Dijital** | +0,12 ± 0,06 | %−36 | baskınlık yok (takas) |
| Baz talep | D · Eşit WIP | **Dijital** | −7,69 ± 0,29 | %+0 | Dijital baskın |
| Talep şoku +%50 | A · Eşit kart | **Dijital** | −15,96 ± 0,60 | %+14 | baskınlık yok (takas) |
| Talep şoku +%50 | B · Politika-tutarlı | **Geleneksel** | +1,97 ± 0,61 | %−36 | baskınlık yok (takas) |
| Talep şoku +%50 | C · Eşit hizmet düzeyi | **Dijital** | +0,40 ± 0,05 | %−11 | baskınlık yok (takas) |
| Talep şoku +%50 | D · Eşit WIP | **Dijital** | −12,76 ± 0,62 | %+0 | Dijital baskın |

- Baz talep: 2 farklı sonuç (A → Dijital, B → Geleneksel, C → Dijital, D → Dijital).
- Talep şoku +%50: 2 farklı sonuç (A → Dijital, B → Geleneksel, C → Dijital, D → Dijital).

## Şekiller

- `docs/figurler/sekil7_adalet_kurallari_nihai_toyota.png` — ana figür (Tablo 3, Toyota kutuları)
- `docs/figurler/sekil7_adalet_kurallari_nihai.png` — mevcut kutular
