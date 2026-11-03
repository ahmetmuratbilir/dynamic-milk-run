"""
v2_uyarlanan_rop.py
===================
Hafta 15 — Dijital sistemin şok kırılganlığı: model kısıtı mı, politika özelliği mi? (Y4, K98)

Sorun
-----
K95/K97: Toyota kutu boyunda (C ≤ günlük talebin %10'u), politika-tutarlı boyutlandırmada
ve +%50 talep şokunda dijital sistem (P3) %17,6 duruş verirken geleneksel sistem (P2,
T=60) %5,5 verir. Bu deneylerde P3'ün ROP'u tasarım talebiyle SABİTTİR; oysa e-Kanban'ın
bilgi avantajı tam olarak gerçekleşen tüketimi görebilmesidir. Uyarlanabilir Kanban
yazını (Elloumi vd. 2025 s.613) kart sayısının işletme sırasında güncellenmesini önerir.

Soru: ROP (ve N) gerçekleşen talebe uyarlanırsa kırılganlık kapanır mı? Kapanıyorsa
bu gerçek bir iyileşme midir, yoksa yalnızca daha fazla stok mu?

Deney (3 araç, 12 replikasyon, K74 mekanizması: 30 dk'da bir son 60 dk'dan D tahmini)
------
  Dijital · sabit           : P3, VDI, ROP tasarım talebiyle (K95/K97 kural B)
  Dijital · ROP uyarlanan   : N sabit (VDI), ROP gerçekleşen talebe göre güncellenir
  Dijital · N+ROP uyarlanan : K74 tam (N ve ROP birlikte güncellenir)
  Geleneksel                : P2, T=60, VDI (karşılaştırma)

Ayırt edici ölçüt — "eğri kazancı":
  K97'deki dijital kart taraması eğrisi (sabit ROP, N = VDI + k) aynı WIP'te hangi duruşu
  veriyorsa, uyarlanan nokta ondan ne kadar aşağıdadır?
    kazanç > GA  : uyarlama gerçek iyileşme (aynı stokla daha az duruş)
    |kazanç| ≤ GA: uyarlama yalnızca eğri boyunca kaydırır (= kart eklemekle eşdeğer)

⚠️ Uyarlama yalnızca dijital sisteme verilir; bu e-Kanban'ın gerçek zamanlı bilgisinin
doğal sonucudur, ama geleneksel sistemin de periyodik olarak yeniden boyutlandırılabileceği
not edilmelidir. Şok tüm koşu boyunca sürer (düzey kayması).

Ön koşul: v2_adalet_kurallari (iki kutu varyantı için de) çalıştırılmış olmalı.

Kullanım
--------
    python -X utf8 -m src.v2_uyarlanan_rop
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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, kanban_boyutlandir
from src.v2_boyutlandirma_duyarliligi import GELENEKSEL, DIJITAL, _ort
from src.v2_toyota_bandi_duyarliligi import c_varyantlari
from src.v2_pareto_ve_figurler import _eksen_duzenle, INK, INK2, MUTED, YUZEY

TALEPLER = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]
KUTULAR = [("Mevcut kutular", "mevcut", ""), ("Toyota kutuları", "toyota", "_toyota")]
VARYANT = ["Dijital · sabit", "Dijital · ROP uyarlanan", "Dijital · N+ROP uyarlanan", "Geleneksel"]
RENK = {"Dijital · sabit": "#1baf7a", "Dijital · ROP uyarlanan": "#8a5cd6",
        "Dijital · N+ROP uyarlanan": "#d6612a", "Geleneksel": "#2a78d6"}


def kos(veri, rep, arac, talep):
    satir = []
    p_d = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac, talep_carpani=talep,
                      kanban_modu="VDI", **DIJITAL)
    n_vdi, _ = kanban_boyutlandir(veri, p_d)
    ayar = {
        "Dijital · sabit": p_d,
        "Dijital · ROP uyarlanan": replace(p_d, dinamik_n=True, n_ozel=tuple(int(x) for x in n_vdi)),
        "Dijital · N+ROP uyarlanan": replace(p_d, dinamik_n=True),
        "Geleneksel": V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac,
                                  talep_carpani=talep, kanban_modu="VDI", **GELENEKSEL),
    }
    for ad in VARYANT:
        satir.append({"varyant": ad, **_ort(veri, ayar[ad], rep)})
    return pd.DataFrame(satir)


def egri_kazanci(df, egri):
    """Sabit-ROP dijital kart taraması eğrisine göre aynı WIP'teki duruş farkı."""
    s = egri[(egri["sistem"] == "Dijital") & (egri["nokta"] != "iki_kutu")].sort_values("ort_wip")
    w, y = s["ort_wip"].to_numpy(), s["starv_pct"].to_numpy()
    out = []
    for _, r in df.iterrows():
        if w.min() <= r["ort_wip"] <= w.max():
            ref = float(np.interp(r["ort_wip"], w, y))
            out.append(ref - r["starv_pct"])
        else:
            out.append(np.nan)
    return out


def rapor(baslik, df):
    print(f"\n{'═' * 92}\n{baslik}\n{'═' * 92}")
    print(f"  {'Varyant':28s} {'Duruş %':>12s} {'WIP':>7s} {'Kart':>6s} {'Eğri kazancı':>14s}  yorum")
    for _, r in df.iterrows():
        k = r["egri_kazanci"]
        if r["varyant"] == "Geleneksel" or r["varyant"] == "Dijital · sabit":
            yorum = ""
        elif np.isnan(k):
            yorum = "eğri aralığı dışında"
        elif k > r["starv_pct_ci95"]:
            yorum = "gerçek iyileşme (aynı stokla daha az duruş)"
        elif k < -r["starv_pct_ci95"]:
            yorum = "eğrinin üstünde (aynı stokla daha fazla duruş)"
        else:
            yorum = "eğri boyunca kayma (= kart eklemek)"
        ks = "" if np.isnan(k) else f"{k:+.2f}"
        print(f"  {r['varyant']:28s} {r['starv_pct']:6.2f}±{r['starv_pct_ci95']:4.2f} "
              f"{r['ort_wip']:7.0f} {r['toplam_kart']:6.0f} {ks:>14s}  {yorum}")
    gel = df[df["varyant"] == "Geleneksel"].iloc[0]
    for ad in VARYANT[:3]:
        d = df[df["varyant"] == ad].iloc[0]
        fark = d["starv_pct"] - gel["starv_pct"]
        ga = float(np.hypot(d["starv_pct_ci95"], gel["starv_pct_ci95"]))
        kim = "eşit" if abs(fark) <= ga else ("dijital önde" if fark < 0 else "geleneksel önde")
        print(f"    {ad:28s} − Geleneksel: duruş {fark:+6.2f} ({kim}), "
              f"WIP %{100 * (d['ort_wip'] / gel['ort_wip'] - 1):+.0f}")


def sekil8(tum, egriler, yol):
    fig, axlar = plt.subplots(len(KUTULAR), len(TALEPLER), figsize=(11.4, 8.6), facecolor=YUZEY)
    for i, (kutu_ad, _, ek) in enumerate(KUTULAR):
        for j, (talep, _) in enumerate(TALEPLER):
            ax = axlar[i, j]
            _eksen_duzenle(ax, "Ortalama WIP (adet)" if i == len(KUTULAR) - 1 else "",
                           "Hat duruş oranı (%)" if j == 0 else "", f"{kutu_ad} · {talep}")
            e = egriler[ek]
            e = e[(e["talep"] == talep) & (e["nokta"] != "iki_kutu")]
            d = tum[(tum["kutu"] == kutu_ad) & (tum["talep"] == talep)]
            for sistem, renk in (("Dijital", RENK["Dijital · sabit"]), ("Geleneksel", RENK["Geleneksel"])):
                s = e[e["sistem"] == sistem].sort_values("ort_wip")
                ax.plot(s["ort_wip"], s["starv_pct"], "-", color=renk, lw=1.4, alpha=0.45, zorder=2,
                        label=f"{sistem} · kart taraması (sabit ROP)" if (i, j) == (0, 0) else None)
            for _, r in d.iterrows():
                ax.errorbar(r["ort_wip"], r["starv_pct"], yerr=r["starv_pct_ci95"], fmt="o",
                            ms=7, color=RENK[r["varyant"]], mec=INK, mew=0.6, capsize=3, zorder=4,
                            label=r["varyant"] if (i, j) == (0, 1) else None)
            x_ust = 1.5 * d["ort_wip"].max()
            gor = e[e["ort_wip"] <= x_ust]["starv_pct"]
            y_ust = 1.15 * max(d["starv_pct"].max() + d["starv_pct_ci95"].max(), gor.max(), 2)
            ax.set_xlim(0, x_ust)
            ax.set_ylim(-0.03 * y_ust, y_ust)
    axlar[0, 0].legend(frameon=False, fontsize=8, labelcolor=INK2, loc="upper right")
    axlar[0, 1].legend(frameon=False, fontsize=8, labelcolor=INK2, loc="upper right")
    fig.suptitle("Şekil 8 · Uyarlanan ROP: dijital sistemin şok kırılganlığı stok mu, bilgi mi?",
                 color=INK, fontsize=12, x=0.012, ha="left", y=0.985)
    fig.text(0.012, 0.012, "Soluk eğriler: sabit ROP ile kart taraması (K97). Uyarlanan nokta "
                           "dijital eğrinin altındaysa iyileşme aynı stokla elde edilmiştir. "
                           "Hata çubukları: %95 GA, 12 replikasyon, 3 araç.", color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 0.955))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=12)
    ap.add_argument("--arac", type=int, default=3)
    args = ap.parse_args()

    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    egriler = {}
    for _, _, ek in KUTULAR:
        yol = os.path.join(cikti, f"v2_adalet_egriler{ek}.csv")
        if not os.path.exists(yol):
            sys.exit(f"Eksik: {yol} — önce: python -X utf8 -m src.v2_adalet_kurallari"
                     f"{' --kutu toyota' if ek else ''}")
        egriler[ek] = pd.read_csv(yol)

    temel = V2Veri()
    veriler = {"mevcut": temel, "toyota": c_varyantlari(temel)["TOYOTA_Q_SABIT"]}

    print("=" * 92)
    print("UYARLANAN ROP: DİJİTAL SİSTEMİN ŞOK KIRILGANLIĞI (Y4 / K98)")
    print(f"  Mekanizma: K74 — her 30 dk, son 60 dk tüketiminden D tahmini · "
          f"{args.arac} araç · {args.rep} replikasyon")
    print("=" * 92)

    tum = []
    for kutu_ad, anahtar, ek in KUTULAR:
        for talep, carpan in TALEPLER:
            df = kos(veriler[anahtar], args.rep, args.arac, carpan)
            df["egri_kazanci"] = egri_kazanci(df, egriler[ek][egriler[ek]["talep"] == talep])
            rapor(f"{kutu_ad} · {talep}", df)
            df.insert(0, "talep", talep)
            df.insert(0, "kutu", kutu_ad)
            tum.append(df)
    tum = pd.concat(tum, ignore_index=True)

    tum.to_csv(os.path.join(cikti, "v2_uyarlanan_rop.csv"), index=False, encoding="utf-8-sig")
    fig_yol = os.path.join(kok, "docs", "figurler", "sekil8_uyarlanan_rop.png")
    sekil8(tum, egriler, fig_yol)
    print("\n  → data/synthetic/v2_uyarlanan_rop.csv")
    print(f"  → docs/figurler/{os.path.basename(fig_yol)}")


if __name__ == "__main__":
    main()
