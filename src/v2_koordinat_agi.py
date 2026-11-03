"""
v2_koordinat_agi.py
===================
Hafta 15 — Koordinat tabanlı (gerçekleşebilir) mesafe ağında sağlamlık (H3, K100)

Sorun
-----
`distances.csv` hiçbir yerleşimden türetilmemiştir ve üçgen eşitsizliğini ihlal eder
(S1→S6 = 900 m iken Depo→S1 = Depo→S6 = 90 m). K71'de Floyd–Warshall kapanışıyla
geçici olarak metrikleştirilmiştir (S5, S10 sınırlılıkları).

Çözüm: istasyonlara (x, y) koordinatı atanır, mesafe dikdörtgensel ölçüyle üretilir
(Sevim & Görkemli Aykut 2026, Denk. 3: d = |Δx| + |Δy|).

Yerleşim
--------
  · Süpermarket (depo) (0, 0)'da; 4 montaj hattı paralel, her hatta 6 istasyon
    (stations.csv: hat, sira_no).
  · Durak aralığı s = 124 m / 6 ≈ 20,7 m — Urru, Bonini & Echelmeyer (2018) s.406:
    "a set of 5 stops ... equally distributed along the route. The route is 124 meters
    long" (5 durak + depo dönüşü = 6 eşit parça).
  · Hat aralığı w = 2·s — ⚠️ MÜHENDİSLİK VARSAYIMI (kaynak yok); duyarlılık için
    "geniş" ölçek ayrıca koşulur.

Ağlar
-----
  MEVCUT_METRIK : distances.csv + Floyd–Warshall (K71, şimdiye kadarki tüm sonuçlar)
  KOMPAKT       : yukarıdaki yerleşim (Urru ölçeği)
  GENIS         : aynı yerleşim, ortalama depo–istasyon mesafesi mevcut matrise
                  eşitlenecek biçimde ölçeklenmiş

Deney: K93 karşılaştırması (A ortak iki kutulu tampon ↔ B politika-tutarlı; geleneksel
P2 T=60 ↔ dijital P3 konsolidasyon; 3 araç, 12 replikasyon) her ağda; ayrıca Vojdani &
Drechsler (2022)'nin taşıma metrikleri (sefer, yol) yeniden karşılaştırılır.

Kullanım
--------
    python -X utf8 -m src.v2_koordinat_agi
"""

import argparse
import copy
import os
import sys

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.v2_entegre_simulasyon import V2Parametre, V2Veri
from src.v2_boyutlandirma_duyarliligi import GELENEKSEL, DIJITAL, KURGULAR, _ort

DURAK_ARALIGI = 124.0 / 6     # m — Urru vd. (2018) s.406
HAT_ARALIGI_KAT = 2.0         # w = 2·s — mühendislik varsayımı
TALEPLER = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]
SISTEMLER = [("Geleneksel", GELENEKSEL), ("Dijital", DIJITAL)]


def koordinatlar(veri: V2Veri, s: float, w: float) -> np.ndarray:
    """Düğüm 0 = depo, düğüm k = S_k. Döner: [n_node × 2] koordinat."""
    st = veri.loader.get_stations()
    hatlar = sorted(st["hat"].unique())
    n_node = veri.mesafe_ham.shape[0]
    xy = np.zeros((n_node, 2))
    orta = (len(hatlar) - 1) / 2
    # sira_no global numaralıdır (1–24); hat içi sıra, hat içindeki sıralamadan türetilir
    hat_ici = st.groupby("hat")["sira_no"].rank(method="first").astype(int)
    for (_, r), j in zip(st.iterrows(), hat_ici):
        k = int(str(r["istasyon_id"]).replace("S", ""))
        h = hatlar.index(r["hat"])
        xy[k] = (s * j, w * (h - orta))
    return xy


def dikdortgensel(xy: np.ndarray) -> np.ndarray:
    return np.abs(xy[:, None, 0] - xy[None, :, 0]) + np.abs(xy[:, None, 1] - xy[None, :, 1])


def aglar(temel: V2Veri) -> dict:
    s, w = DURAK_ARALIGI, HAT_ARALIGI_KAT * DURAK_ARALIGI
    m_kompakt = dikdortgensel(koordinatlar(temel, s, w))
    olcek = temel.mesafe_metrik[0, 1:].mean() / m_kompakt[0, 1:].mean()
    out = {"MEVCUT_METRIK": temel}
    for ad, m in (("KOMPAKT", m_kompakt), ("GENIS", m_kompakt * olcek)):
        v = copy.copy(temel)
        v.mesafe_ham = m
        v.mesafe_metrik = m
        out[ad] = v
    return out, olcek


def ucgen_ihlali(m: np.ndarray) -> int:
    d = m.copy()
    for k in range(d.shape[0]):
        d = np.minimum(d, d[:, [k]] + d[[k], :])
    return int(np.sum(d < m - 1e-9))


def deney(ag: dict, rep: int, arac: int) -> pd.DataFrame:
    satir = []
    for ag_ad, veri in ag.items():
        for talep_ad, talep in TALEPLER:
            for kurgu_ad, mod in KURGULAR:
                for sistem, kw in SISTEMLER:
                    p = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac,
                                    talep_carpani=talep, kanban_modu=mod, **kw)
                    satir.append({"ag": ag_ad, "talep": talep_ad, "kurgu": kurgu_ad[0],
                                  "sistem": sistem, **_ort(veri, p, rep)})
            print(f"  ✓ {ag_ad:14s} · {talep_ad}")
    return pd.DataFrame(satir)


def ozet(df: pd.DataFrame) -> pd.DataFrame:
    sat = []
    for (ag, talep), g in df.groupby(["ag", "talep"], sort=False):
        def al(k, s):
            return g[(g["kurgu"] == k) & (g["sistem"] == s)].iloc[0]
        r = {"ag": ag, "talep": talep}
        yon = {}
        for k in ("A", "B"):
            gl, dj = al(k, "Geleneksel"), al(k, "Dijital")
            f = dj["starv_pct"] - gl["starv_pct"]
            e = float(np.hypot(dj["starv_pct_ci95"], gl["starv_pct_ci95"]))
            r[f"fark_{k}"], r[f"ga_{k}"] = f, e
            yon[k] = 0 if abs(f) <= e else int(np.sign(f))
            r[f"sefer_{k}_pct"] = 100 * (dj["tur_sayisi"] / gl["tur_sayisi"] - 1)
            r[f"yol_{k}_pct"] = 100 * (dj["toplam_mesafe_km"] / gl["toplam_mesafe_km"] - 1)
            r[f"wip_{k}_pct"] = 100 * (dj["ort_wip"] / gl["ort_wip"] - 1)
            r[f"yol_gel_{k}_km"], r[f"yol_dij_{k}_km"] = gl["toplam_mesafe_km"], dj["toplam_mesafe_km"]
        r["kayma"] = r["fark_B"] - r["fark_A"]
        r["yon_A"], r["yon_B"] = yon["A"], yon["B"]
        r["siralama_degisti"] = yon["A"] != yon["B"]
        sat.append(r)
    return pd.DataFrame(sat)


def rapor(oz: pd.DataFrame):
    YON = {-1: "dijital", 0: "eşit", 1: "geleneksel"}
    for talep, _ in TALEPLER:
        print(f"\n{'═' * 96}\n{talep}\n{'═' * 96}")
        print(f"  {'Ağ':14s} {'fark A':>13s} {'fark B':>13s} {'kayma':>7s}  {'önde A → B':22s} "
              f"{'sefer B':>8s} {'yol B':>7s} {'WIP B':>7s}  yol gel/dij (km)")
        for _, r in oz[oz["talep"] == talep].iterrows():
            print(f"  {r['ag']:14s} {r['fark_A']:+6.2f}±{r['ga_A']:5.2f} {r['fark_B']:+6.2f}±{r['ga_B']:5.2f} "
                  f"{r['kayma']:+7.2f}  {YON[r['yon_A']] + ' → ' + YON[r['yon_B']]:22s} "
                  f"{r['sefer_B_pct']:+7.0f}% {r['yol_B_pct']:+6.0f}% {r['wip_B_pct']:+6.0f}%  "
                  f"{r['yol_gel_B_km']:.1f} / {r['yol_dij_B_km']:.1f}")
    print("\n  Vojdani & Drechsler (2022) s.6 referansı: dijital −%27 sefer, −%29,39 yol.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=12)
    ap.add_argument("--arac", type=int, default=3)
    args = ap.parse_args()

    temel = V2Veri()
    ag, olcek = aglar(temel)
    print("=" * 96)
    print("KOORDİNAT TABANLI MESAFE AĞI (H3 / K100)")
    print(f"  Dikdörtgensel ölçü (Sevim & Görkemli Aykut 2026, Denk. 3) · durak aralığı "
          f"{DURAK_ARALIGI:.1f} m (Urru vd. 2018 s.406) · hat aralığı {HAT_ARALIGI_KAT:.0f}·s (varsayım)")
    for ad, v in ag.items():
        m = v.mesafe_metrik
        print(f"  {ad:14s} depo→istasyon ort. {m[0, 1:].mean():6.1f} m · istasyonlar arası ort. "
              f"{m[1:, 1:][np.triu_indices(m.shape[0] - 1, 1)].mean():6.1f} m · üçgen ihlali (ham): "
              f"{ucgen_ihlali(v.mesafe_ham)}")
    print(f"  GENIS ölçek katsayısı: {olcek:.2f} · {args.arac} araç · {args.rep} replikasyon")
    print("=" * 96)

    df = deney(ag, args.rep, args.arac)
    oz = ozet(df)
    rapor(oz)

    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    df.to_csv(os.path.join(cikti, "v2_koordinat_agi_ham.csv"), index=False, encoding="utf-8-sig")
    oz.to_csv(os.path.join(cikti, "v2_koordinat_agi_ozet.csv"), index=False, encoding="utf-8-sig")
    print("\n  → data/synthetic/v2_koordinat_agi_{ham,ozet}.csv")


if __name__ == "__main__":
    main()
