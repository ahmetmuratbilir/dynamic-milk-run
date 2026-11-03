"""
v2_cok_vardiya.py
=================
Hafta 15 — Ana bulguların kararlı durumda ve çok vardiyalı ufukta sağlamlığı (H4, K99)

Sorun
-----
(1) Motorun `starv_pct` ve `ort_wip` göstergeleri ısınma dönemini de içerir
    (starv_pct = toplam duruş / (T·n); WIP tüm dakikaların ortalaması). K78'de ısınma
    süresi Welch yöntemiyle 90 dk ölçülmüştür, ancak K93–K98 deneyleri bu 90 dk'yı
    göstergelerden çıkarmamıştır. Raflar dolu başladığı için ısınma dönemi duruşu
    düşük, WIP'i yüksek gösterir.
(2) Tüm deneyler 480 dk (tek vardiya) ufukla yapılmıştır; 90 dk ısınma ufkun %19'udur.
    Law (2015) kararlı durum analizinde ısınmanın ufka göre küçük kalmasını önerir.

Bu betik K93 karşılaştırmasını (kurgu A ortak iki kutulu tampon ↔ B politika-tutarlı;
geleneksel P2 T=60 ↔ dijital P3 konsolidasyon; 3 araç) şu koşullarda tekrarlar:
  · ufuk 480 dk ve 1440 dk (3 vardiya, saatlik rejim talebi kesintisiz sürer)
  · gösterge: tüm koşu  ↔  ısınma sonrası (t ≥ 90 dk)
  · kutu: mevcut ve Toyota (K95) · talep: baz ve +%50

Ölçüt: kayma = fark_B − fark_A (dijital − geleneksel duruş farkı) ve sıralama değişimi
dört gösterge/ufuk birleşiminde aynı mı?

Kullanım
--------
    python -X utf8 -m src.v2_cok_vardiya
"""

import argparse
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir
from src.v2_boyutlandirma_duyarliligi import GELENEKSEL, DIJITAL, KURGULAR
from src.v2_toyota_bandi_duyarliligi import c_varyantlari

UFUKLAR = [480, 1440]
TALEPLER = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]
SISTEMLER = [("Geleneksel", GELENEKSEL), ("Dijital", DIJITAL)]


def _ort(veri, p, rep, seed0=11000):
    """Tüm koşu ve ısınma sonrası duruş/WIP (ortalama ± %95 GA)."""
    deg = {"durus_tum": [], "durus_kd": [], "wip_tum": [], "wip_kd": []}
    for r in range(rep):
        s = calistir(replace(p, seed=seed0 + r, zaman_serisi=True), veri)
        w = np.asarray(s["_wip_seri"])
        deg["durus_tum"].append(s["starv_pct"])
        deg["durus_kd"].append(s["starv_pct_isinma_sonrasi"])
        deg["wip_tum"].append(float(w.mean()))
        deg["wip_kd"].append(float(w[p.isinma_dk:].mean()))
    out = {}
    for k, v in deg.items():
        out[k] = float(np.mean(v))
        out[k + "_ga"] = 1.96 * float(np.std(v, ddof=1)) / np.sqrt(rep)
    return out


def deney(veriler, rep, arac):
    satir = []
    for kutu, veri in veriler.items():
        for T in UFUKLAR:
            for talep_ad, talep in TALEPLER:
                for kurgu_ad, mod in KURGULAR:
                    for sistem, kw in SISTEMLER:
                        p = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac,
                                        talep_carpani=talep, kanban_modu=mod, sim_sure=T, **kw)
                        satir.append({"kutu": kutu, "ufuk_dk": T, "talep": talep_ad,
                                      "kurgu": kurgu_ad[0], "sistem": sistem,
                                      **_ort(veri, p, rep)})
                print(f"  ✓ {kutu:7s} · {T:4d} dk · {talep_ad}")
    return pd.DataFrame(satir)


def ozet(df):
    sat = []
    for (kutu, T, talep), g in df.groupby(["kutu", "ufuk_dk", "talep"], sort=False):
        for gost in ("tum", "kd"):
            def al(k, s):
                return g[(g["kurgu"] == k) & (g["sistem"] == s)].iloc[0]
            fark, ga = {}, {}
            for k in ("A", "B"):
                gl, dj = al(k, "Geleneksel"), al(k, "Dijital")
                fark[k] = dj[f"durus_{gost}"] - gl[f"durus_{gost}"]
                ga[k] = float(np.hypot(dj[f"durus_{gost}_ga"], gl[f"durus_{gost}_ga"]))
            yon = lambda f, e: 0 if abs(f) <= e else int(np.sign(f))
            sat.append({"kutu": kutu, "ufuk_dk": T, "talep": talep,
                        "gosterge": "tüm koşu" if gost == "tum" else "ısınma sonrası",
                        "fark_A": fark["A"], "ga_A": ga["A"], "fark_B": fark["B"], "ga_B": ga["B"],
                        "kayma": fark["B"] - fark["A"],
                        "yon_A": yon(fark["A"], ga["A"]), "yon_B": yon(fark["B"], ga["B"]),
                        "siralama_degisti": yon(fark["A"], ga["A"]) != yon(fark["B"], ga["B"])})
    return pd.DataFrame(sat)


def yanlilik(df):
    """Isınmanın göstergelere etkisi: tüm koşu − ısınma sonrası."""
    d = df.copy()
    d["durus_yanlilik"] = d["durus_tum"] - d["durus_kd"]
    d["wip_yanlilik_pct"] = 100 * (d["wip_tum"] / d["wip_kd"] - 1)
    return d


def rapor(oz, yan):
    YON = {-1: "dijital", 0: "eşit", 1: "geleneksel"}
    for kutu in oz["kutu"].unique():
        for talep, _ in TALEPLER:
            print(f"\n{'═' * 92}\n{kutu} kutular · {talep}\n{'═' * 92}")
            print(f"  {'Ufuk':>6s}  {'Gösterge':15s} {'fark A':>13s} {'fark B':>13s} {'kayma':>7s}  "
                  f"önde (A → B)")
            for _, r in oz[(oz["kutu"] == kutu) & (oz["talep"] == talep)].iterrows():
                print(f"  {r['ufuk_dk']:4d}dk  {r['gosterge']:15s} {r['fark_A']:+6.2f}±{r['ga_A']:5.2f} "
                      f"{r['fark_B']:+6.2f}±{r['ga_B']:5.2f} {r['kayma']:+7.2f}  "
                      f"{YON[r['yon_A']]} → {YON[r['yon_B']]}"
                      f"{'   ← sıralama değişti' if r['siralama_degisti'] else ''}")

    print(f"\n{'═' * 92}\nISINMA YANLILIĞI (tüm koşu − ısınma sonrası)\n{'═' * 92}")
    for T in UFUKLAR:
        y = yan[yan["ufuk_dk"] == T]
        print(f"  {T:4d} dk: duruş {y['durus_yanlilik'].min():+.2f} … {y['durus_yanlilik'].max():+.2f} puan "
              f"(ort. {y['durus_yanlilik'].mean():+.2f}) · WIP %{y['wip_yanlilik_pct'].min():+.1f} … "
              f"%{y['wip_yanlilik_pct'].max():+.1f}")

    print(f"\n{'═' * 92}\nSAĞLAMLIK: kayma ve sıralama dört gösterge/ufuk birleşiminde\n{'═' * 92}")
    for (kutu, talep), g in oz.groupby(["kutu", "talep"], sort=False):
        print(f"  {kutu:7s} · {talep:16s} kayma {g['kayma'].min():+6.2f} … {g['kayma'].max():+6.2f} · "
              f"kayma>0: {int((g['kayma'] > 0).sum())}/{len(g)} · "
              f"sıralama değişimi: {int(g['siralama_degisti'].sum())}/{len(g)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=12)
    ap.add_argument("--arac", type=int, default=3)
    args = ap.parse_args()

    temel = V2Veri()
    veriler = {"mevcut": temel, "toyota": c_varyantlari(temel)["TOYOTA_Q_SABIT"]}
    print("=" * 92)
    print("KARARLI DURUM VE ÇOK VARDİYALI UFUK (H4 / K99)")
    print(f"  Ufuk: {UFUKLAR} dk · ısınma 90 dk (K78) · {args.arac} araç · {args.rep} replikasyon")
    print("=" * 92)

    df = deney(veriler, args.rep, args.arac)
    oz = ozet(df)
    yan = yanlilik(df)
    rapor(oz, yan)

    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    yan.to_csv(os.path.join(cikti, "v2_cok_vardiya_ham.csv"), index=False, encoding="utf-8-sig")
    oz.to_csv(os.path.join(cikti, "v2_cok_vardiya_ozet.csv"), index=False, encoding="utf-8-sig")
    print("\n  → data/synthetic/v2_cok_vardiya_{ham,ozet}.csv")


if __name__ == "__main__":
    main()
