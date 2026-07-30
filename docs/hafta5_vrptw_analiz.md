# Hafta 5 — VRPTW Rotalama ve Optimizasyon Analiz Raporu

> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → "real"`

**Uygulanan Kararlar:** K03, K04, K17, K33, K34, K35 — bkz. `karar_gunlugu.md`

---

## 1. Genel Rotalama Özeti

| Metrik | Değer |
|--------|-------|
| Servis Yapılan Sinyal | 72 / 182 |
| Toplam Tur Sayısı | 16 |
| Gerçek TW İhlal Sayısı | 55 |

## 2. Araç Bazlı Performans

| arac_id   |   toplam_tur |   tasinan_kutu |   ihlal_sayisi |
|:----------|-------------:|---------------:|---------------:|
| A1        |            8 |             38 |             27 |
| A2        |            8 |             36 |             28 |

## 3. Rota Örnekleri (İlk 15 Durak)

| rota_id   | arac_id   |   tur_no | istasyon_id   |   istenen_kutu |   tw_baslangic |   tw_bitis |   varis_dk | tw_ihlal   |
|:----------|:----------|---------:|:--------------|---------------:|---------------:|-----------:|-----------:|:-----------|
| ROTA_001  | A1        |        1 | S13           |              1 |              0 |         46 |          7 | False      |
| ROTA_002  | A2        |        1 | S1            |              1 |              2 |         48 |          9 | False      |
| ROTA_003  | A1        |        2 | S7            |              1 |              5 |         50 |         27 | False      |
| ROTA_003  | A1        |        2 | S6            |              1 |             18 |         64 |         40 | False      |
| ROTA_003  | A1        |        2 | S4            |              1 |              8 |         54 |         53 | False      |
| ROTA_003  | A1        |        2 | S12           |              1 |             12 |         57 |         66 | True       |
| ROTA_003  | A1        |        2 | S3            |              1 |              8 |         54 |         79 | True       |
| ROTA_004  | A2        |        2 | S19           |              1 |              7 |         53 |         29 | False      |
| ROTA_004  | A2        |        2 | S15           |              1 |              9 |         55 |         42 | False      |
| ROTA_004  | A2        |        2 | S21           |              1 |             17 |         63 |         55 | False      |
| ROTA_004  | A2        |        2 | S18           |              1 |             10 |         56 |         68 | True       |
| ROTA_004  | A2        |        2 | S17           |              1 |             18 |         64 |         81 | True       |
| ROTA_005  | A1        |        3 | S18           |              1 |             73 |        119 |         99 | False      |
| ROTA_005  | A1        |        3 | S20           |              1 |             23 |         69 |        112 | True       |
| ROTA_005  | A1        |        3 | S16           |              2 |             47 |         92 |        125 | True       |

## 4. ⚠️ Gerçek TW İhlalleri (K27 Varsayımı Testi)

| rota_id   | arac_id   | istasyon_id   |   tw_bitis |   varis_dk |   gercek_gecikme_dk |
|:----------|:----------|:--------------|-----------:|-----------:|--------------------:|
| ROTA_003  | A1        | S12           |         57 |         66 |                   9 |
| ROTA_003  | A1        | S3            |         54 |         79 |                  25 |
| ROTA_004  | A2        | S18           |         56 |         68 |                  12 |
| ROTA_004  | A2        | S17           |         64 |         81 |                  17 |
| ROTA_005  | A1        | S20           |         69 |        112 |                  43 |
| ROTA_005  | A1        | S16           |         92 |        125 |                  33 |
| ROTA_005  | A1        | S8            |        134 |        138 |                   4 |
| ROTA_005  | A1        | S6            |        132 |        151 |                  19 |
| ROTA_006  | A2        | S23           |         70 |        101 |                  31 |
| ROTA_006  | A2        | S24           |        109 |        114 |                   5 |
| ROTA_006  | A2        | S9            |        120 |        127 |                   7 |
| ROTA_006  | A2        | S10           |         74 |        140 |                  66 |
| ROTA_006  | A2        | S2            |        127 |        153 |                  26 |
| ROTA_007  | A1        | S24           |        166 |        171 |                   5 |
| ROTA_007  | A1        | S15           |        173 |        184 |                  11 |
| ROTA_007  | A1        | S13           |        149 |        205 |                  56 |
| ROTA_007  | A1        | S5            |        144 |        218 |                  74 |
| ROTA_008  | A2        | S7            |        163 |        173 |                  10 |
| ROTA_008  | A2        | S23           |        144 |        186 |                  42 |
| ROTA_008  | A2        | S19           |        111 |        199 |                  88 |
| ROTA_008  | A2        | S13           |         96 |        212 |                 116 |
| ROTA_008  | A2        | S17           |        207 |        225 |                  18 |
| ROTA_009  | A1        | S24           |        219 |        238 |                  19 |
| ROTA_009  | A1        | S9            |        246 |        264 |                  18 |
| ROTA_009  | A1        | S10           |        240 |        277 |                  37 |
| ROTA_009  | A1        | S13           |        250 |        290 |                  40 |
| ROTA_010  | A2        | S12           |        184 |        258 |                  74 |
| ROTA_010  | A2        | S1            |        157 |        271 |                 114 |
| ROTA_010  | A2        | S22           |        198 |        284 |                  86 |
| ROTA_010  | A2        | S5            |         69 |        297 |                 228 |
| ROTA_011  | A1        | S3            |        297 |        323 |                  26 |
| ROTA_011  | A1        | S13           |        301 |        336 |                  35 |
| ROTA_011  | A1        | S10           |        322 |        349 |                  27 |
| ROTA_011  | A1        | S1            |        323 |        362 |                  39 |
| ROTA_012  | A2        | S15           |        292 |        330 |                  38 |
| ROTA_012  | A2        | S6            |        341 |        351 |                  10 |
| ROTA_012  | A2        | S4            |        297 |        364 |                  67 |
| ROTA_013  | A1        | S4            |        357 |        382 |                  25 |
| ROTA_013  | A1        | S20           |        369 |        395 |                  26 |
| ROTA_013  | A1        | S12           |        378 |        408 |                  30 |
| ROTA_013  | A1        | S2            |        399 |        421 |                  22 |
| ROTA_013  | A1        | S16           |        393 |        434 |                  41 |
| ROTA_014  | A2        | S18           |        378 |        384 |                   6 |
| ROTA_014  | A2        | S19           |        355 |        397 |                  42 |
| ROTA_014  | A2        | S15           |        410 |        423 |                  13 |
| ROTA_014  | A2        | S12           |        315 |        436 |                 121 |
| ROTA_015  | A1        | S13           |        455 |        467 |                  12 |
| ROTA_015  | A1        | S12           |        443 |        480 |                  37 |
| ROTA_015  | A1        | S4            |        476 |        493 |                  17 |
| ROTA_015  | A1        | S7            |        455 |        506 |                  51 |
| ROTA_016  | A2        | S18           |        440 |        456 |                  16 |
| ROTA_016  | A2        | S11           |        375 |        469 |                  94 |
| ROTA_016  | A2        | S20           |        292 |        482 |                 190 |
| ROTA_016  | A2        | S14           |        394 |        495 |                 101 |
| ROTA_016  | A2        | S22           |        333 |        508 |                 175 |