"""
v2_toyota_bandi_duyarliligi.py
==============================
Hafta 15 — K93 bulgusunun Toyota formülü parametre bandında sağlamlığı (H6, K95)

Sorun
-----
K06 Kanban formülü Toyota formülüdür (K88):

    y = D (Tw + Tp)(1 + α) / a        — Sugimori, Kusunoki, Cho & Uchikawa (1977),
                                        aktaran Kundu, Rossini & Portioli-Staudacher
                                        (2019), IJIEC 10, s.422–423

Aynı kaynak iki sınır verir:
  · α (güvenlik katsayısı) "policy variable (although < 10%)"
  · a (konteyner kapasitesi) "not more than 10% of daily demand"

Projenin varsayılanları ikisinin de DIŞINDADIR:
  · α = 0,15
  · C / günlük talep = %10,4 … %17,0 (ortalama %13,6) — 24 istasyonun 24'ü sınırı aşar
    (K88 yalnızca S1'i not etmişti; günlük talep = saatlik × 8 saatlik vardiya)

Hakem sorusu: "K93'teki sıralama değişimi, Toyota bandı dışındaki parametrelerin
bir yan ürünü olabilir mi?" Bu betik K93 deneyini bu bant boyunca tekrarlar.

Deney
-----
  α  ∈ {0,00; 0,05; 0,10; 0,15; 0,20}         (0,15 = proje varsayılanı)
  C  ∈ MEVCUT                    : stations.csv kutu kapasiteleri
       TOYOTA_Q_SABIT            : C_i = ⌊0,10 · 8 · D_i⌋; araç kapasitesi Q kutu olarak aynı
       TOYOTA_Q_HACIM            : C_i aynı; Q, taşınan parça hacmi korunacak şekilde
                                   ölçeklenir (Q · ΣC_mevcut / ΣC_toyota)
  Talep : baz ve +%50 şok
  Kurgu : A (ortak iki kutulu tampon, Vojdani & Drechsler 2022 s.5) ve
          B (politika-tutarlı, K65) — K93 ile aynı geleneksel/dijital sistemler

Ölçüt: her (α, C, talep) hücresinde
  fark_A, fark_B  = dijital − geleneksel duruş (puan)
  kayma           = fark_B − fark_A   (boyutlandırma tasarımının sonuca etkisi)
  sıralama değişimi = sign(fark_A) ≠ sign(fark_B) ve |fark| > GA

⚠️ C'nin küçültülmesi yalnızca kutu boyutunu değiştirir; talep, ağ ve LT aynıdır.
"Q sabit" varyantı araç başına taşınan parça miktarını da düşürür (karıştırıcı);
bu yüzden hacim-eşdeğer varyant birlikte raporlanır.

Kullanım
--------
    python -X utf8 -m src.v2_toyota_bandi_duyarliligi
    python -X utf8 -m src.v2_toyota_bandi_duyarliligi --rep 20
"""

import argparse
import copy
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

from src.v2_entegre_simulasyon import V2Parametre, V2Veri
from src.v2_boyutlandirma_duyarliligi import GELENEKSEL, DIJITAL, KURGULAR, _ort
from src.v2_pareto_ve_figurler import _eksen_duzenle, INK, INK2, MUTED, YUZEY, KRITIK

ALFALAR = [0.00, 0.05, 0.10, 0.15, 0.20]
TALEPLER = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]
VARDIYA_SAAT = 8
TOYOTA_C_ORAN = 0.10          # Kundu vd. 2019 s.423: a ≤ günlük talebin %10'u
TOYOTA_ALFA_UST = 0.10        # Kundu vd. 2019 s.423: α < %10


def c_varyantlari(veri: V2Veri) -> dict:
    gunluk = veri.mu_saat * VARDIYA_SAAT
    c_toyota = np.maximum(1.0, np.floor(TOYOTA_C_ORAN * gunluk))
    q_hacim = int(round(veri.Q * veri.C.sum() / c_toyota.sum()))
    out = {"MEVCUT": veri}
    for ad, q in [("TOYOTA_Q_SABIT", veri.Q), ("TOYOTA_Q_HACIM", q_hacim)]:
        v = copy.copy(veri)
        v.C = c_toyota.copy()
        v.Q = q
        out[ad] = v
    return out


def deney(varyant: dict, rep: int, arac: int) -> pd.DataFrame:
    satir = []
    for c_ad, veri in varyant.items():
        for talep_ad, talep in TALEPLER:
            for alpha in ALFALAR:
                for kurgu_ad, mod in KURGULAR:
                    for sistem, kw in [("Geleneksel", GELENEKSEL), ("Dijital", DIJITAL)]:
                        p = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac,
                                        talep_carpani=talep, kanban_modu=mod,
                                        alpha=alpha, **kw)
                        r = _ort(veri, p, rep)
                        satir.append({"c_varyant": c_ad, "Q": veri.Q, "talep": talep_ad,
                                      "alpha": alpha, "kurgu": kurgu_ad[0], "sistem": sistem,
                                      **r})
            print(f"  ✓ {c_ad:15s} · {talep_ad}")
    return pd.DataFrame(satir)


def ozetle(df: pd.DataFrame) -> pd.DataFrame:
    satir = []
    for (c_ad, talep, alpha), g in df.groupby(["c_varyant", "talep", "alpha"], sort=False):
        def al(k, s):
            return g[(g["kurgu"] == k) & (g["sistem"] == s)].iloc[0]
        fark, ga = {}, {}
        for k in ("A", "B"):
            gel, dij = al(k, "Geleneksel"), al(k, "Dijital")
            fark[k] = dij["starv_pct"] - gel["starv_pct"]
            ga[k] = float(np.hypot(dij["starv_pct_ci95"], gel["starv_pct_ci95"]))
        anlamli = {k: abs(fark[k]) > ga[k] for k in fark}
        degisti = (np.sign(fark["A"]) != np.sign(fark["B"])) and anlamli["A"]
        satir.append({
            "c_varyant": c_ad, "talep": talep, "alpha": alpha,
            "toyota_bandinda": alpha <= TOYOTA_ALFA_UST and c_ad != "MEVCUT",
            "fark_A": fark["A"], "ga_A": ga["A"], "fark_B": fark["B"], "ga_B": ga["B"],
            "kayma": fark["B"] - fark["A"],
            "A_anlamli_dijital_lehine": fark["A"] < 0 and anlamli["A"],
            "B_anlamli": anlamli["B"],
            "siralama_degisti": bool(degisti),
            "kart_A_gel": int(al("A", "Geleneksel")["toplam_kart"]),
            "kart_B_gel": int(al("B", "Geleneksel")["toplam_kart"]),
            "kart_B_dij": int(al("B", "Dijital")["toplam_kart"]),
        })
    return pd.DataFrame(satir)


def rapor(oz: pd.DataFrame):
    for talep, _ in TALEPLER:
        print(f"\n{'═' * 92}\n{talep}  —  fark = dijital − geleneksel duruş (puan), ± %95 GA\n{'═' * 92}")
        print(f"  {'C varyantı':16s} {'α':>5s}  {'fark A':>13s}  {'fark B':>13s}  "
              f"{'kayma':>7s}  {'kart A→B(gel)':>13s}  sıralama")
        for _, r in oz[oz["talep"] == talep].iterrows():
            bant = "◆" if r["toyota_bandinda"] else " "
            print(f" {bant}{r['c_varyant']:16s} {r['alpha']:5.2f}  "
                  f"{r['fark_A']:+6.2f}±{r['ga_A']:5.2f}  {r['fark_B']:+6.2f}±{r['ga_B']:5.2f}  "
                  f"{r['kayma']:+7.2f}  {r['kart_A_gel']:5d}→{r['kart_B_gel']:<5d}    "
                  f"{'DEĞİŞTİ' if r['siralama_degisti'] else '—'}")
    print("\n  ◆ = Toyota bandı içinde (α ≤ 0,10 ve C ≤ günlük talebin %10'u)")

    print(f"\n{'═' * 92}\nSAĞLAMLIK ÖZETİ\n{'═' * 92}")
    for talep, _ in TALEPLER:
        t = oz[oz["talep"] == talep]
        b = t[t["toyota_bandinda"]]
        print(f"  {talep}:")
        print(f"    kayma > 0 (B, geleneksel sistemi A'ya göre iyileştirir): "
              f"{int((t['kayma'] > 0).sum())}/{len(t)} hücre · Toyota bandında "
              f"{int((b['kayma'] > 0).sum())}/{len(b)}")
        print(f"    kayma aralığı: tüm {t['kayma'].min():+.2f} … {t['kayma'].max():+.2f} · "
              f"bantta {b['kayma'].min():+.2f} … {b['kayma'].max():+.2f}")
        print(f"    A'da dijital anlamlı önde: {int(t['A_anlamli_dijital_lehine'].sum())}/{len(t)} · "
              f"B'de fark anlamlı: {int(t['B_anlamli'].sum())}/{len(t)} · "
              f"sıralama değişimi: {int(t['siralama_degisti'].sum())}/{len(t)} "
              f"(bantta {int(b['siralama_degisti'].sum())}/{len(b)})")


def sekil6(oz: pd.DataFrame, yol: str):
    """Kayma (fark_B − fark_A) α'ya karşı; C varyantı başına bir çizgi, talep başına bir panel."""
    # Q varyantları duruşta özdeştir (araç doluluğu ≤ %57, Q bağlayıcı değil) → tek çizgi
    RENK = {"MEVCUT": "#8a8f98", "TOYOTA_Q_SABIT": "#1baf7a"}
    ETIKET = {"MEVCUT": "Mevcut C (%10,4–17,0 günlük talep)",
              "TOYOTA_Q_SABIT": "Toyota C ≤ %10 günlük talep (Q sabit = Q hacim-eşdeğer)"}
    fig, axlar = plt.subplots(1, len(TALEPLER), figsize=(11.4, 5.0), facecolor=YUZEY)
    for k, (ax, (talep, _)) in enumerate(zip(axlar, TALEPLER)):
        _eksen_duzenle(ax, "Güvenlik katsayısı α",
                       "Kayma = fark(B) − fark(A)  [puan]" if k == 0 else "", talep)
        ax.axvspan(-0.01, TOYOTA_ALFA_UST + 0.005, color="#1baf7a", alpha=0.07, zorder=0)
        ax.axhline(0, color=MUTED, lw=0.8, zorder=1)
        d = oz[oz["talep"] == talep]
        for c_ad, renk in RENK.items():
            s = d[d["c_varyant"] == c_ad]
            ax.plot(s["alpha"], s["kayma"], "-o", color=renk, lw=2, ms=5, zorder=3,
                    label=ETIKET[c_ad] if k == 0 else None)
            dg = s[s["siralama_degisti"]]
            ax.scatter(dg["alpha"], dg["kayma"], s=110, facecolors="none",
                       edgecolors=KRITIK, lw=1.6, zorder=4)
        ax.axvline(0.15, color=MUTED, lw=0.8, ls=":", zorder=1)
        y0 = ax.get_ylim()[0]
        ax.text(0.153, y0, " proje α", color=MUTED, fontsize=8, va="bottom")
        ax.text(0.0, y0, " Toyota α < %10", color="#137a55", fontsize=8, va="bottom")
        ax.set_xticks(ALFALAR)
    axlar[0].legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="center right")
    fig.suptitle("Şekil 6 · Boyutlandırma tasarımının etkisi Toyota parametre bandında da "
                 "sürmektedir", color=INK, fontsize=12, x=0.012, ha="left", y=0.98)
    fig.text(0.012, 0.015, "Kayma > 0: politika-tutarlı boyutlandırma geleneksel sistemin "
                           "dezavantajını azaltır. Kırmızı halka: sıralama değişimi. "
                           "Yeşil bant: α < %10 (Sugimori vd. 1977, aktaran Kundu vd. 2019).",
             color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.045, 1, 0.945))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=12)
    ap.add_argument("--arac", type=int, default=3)
    args = ap.parse_args()

    veri = V2Veri()
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    varyant = c_varyantlari(veri)

    oran = veri.C / (veri.mu_saat * VARDIYA_SAAT)
    print("=" * 92)
    print("K93 BULGUSUNUN TOYOTA FORMÜLÜ BANDINDA SAĞLAMLIĞI (H6 / K95)")
    print("  Kaynak: Sugimori vd. (1977), aktaran Kundu vd. (2019) s.422–423")
    print(f"  Mevcut C/günlük talep: %{100 * oran.min():.1f} … %{100 * oran.max():.1f} "
          f"(ort. %{100 * oran.mean():.1f}); sınırı aşan istasyon: "
          f"{int((oran > TOYOTA_C_ORAN).sum())}/{veri.n}")
    t = varyant["TOYOTA_Q_SABIT"]
    print(f"  Toyota C: {int(t.C.min())}…{int(t.C.max())} adet/kutu "
          f"(mevcut {int(veri.C.min())}…{int(veri.C.max())}); "
          f"Q: sabit {veri.Q} · hacim-eşdeğer {varyant['TOYOTA_Q_HACIM'].Q} kutu")
    print(f"  Filo: {args.arac} araç · Replikasyon: {args.rep}")
    print("=" * 92)

    df = deney(varyant, args.rep, args.arac)
    oz = ozetle(df)
    rapor(oz)

    cikti = os.path.join(kok, "data", "synthetic")
    df.to_csv(os.path.join(cikti, "v2_toyota_bandi_ham.csv"), index=False, encoding="utf-8-sig")
    oz.to_csv(os.path.join(cikti, "v2_toyota_bandi_ozet.csv"), index=False, encoding="utf-8-sig")
    fig_yol = os.path.join(kok, "docs", "figurler", "sekil6_toyota_bandi_sagligi.png")
    sekil6(oz, fig_yol)
    print(f"\n  → data/synthetic/v2_toyota_bandi_{{ham,ozet}}.csv")
    print(f"  → docs/figurler/{os.path.basename(fig_yol)}")


if __name__ == "__main__":
    main()
