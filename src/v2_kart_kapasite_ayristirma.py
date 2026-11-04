"""
v2_kart_kapasite_ayristirma.py
==============================
Hafta 15 — İkinci açık: duruşta kart sayısı ile taşıma kapasitesinin payları ve şok sonrası
toparlanma (K109)

Açık
----
Ciemnoczolowski & Bozer (2013, IJPR 51(2), s.579): *"It should be possible in future research to
quantify the relative contributions of the number of Kanban and the tugger capacity to starvation
at each WS."* Onların sonucu (kapasite artınca duruş sıfırlanır) sabit tüketim varsayımına
dayanır. Alnahhal, Ridwan & Noche (2014, §VI): *"lack of studies regarding fast response of the
system to any changes in material demand"*. Bocewicz vd. (2019, s.51): değişen talepte geçiş.

Deney (nihai ayar K105: koordinat ağı, 1440 dk, ısınma sonrası gösterge)
------
A · Ayrıştırma — tam faktöriyel:
      politika {P2 T=60, P3 konsolidasyon} × kart kaydırma k {−1, 0, +1, +2} (N = max(1, N^VDI + k))
      × araç sayısı {1, 2, 3, 4} × araç kapasitesi Q {15, 25, 35 kutu} × talep {baz, +%50 düzey}
      → duruş varyansının η² ayrıştırması (dengeli tasarım; ana etkiler ve iki yönlü etkileşimler),
        politika başına ayrı ayrı.
B · Toparlanma — 480. dakikada başlayan 120 dk'lık +%50 talep darbesi:
      politika × k {0, +1, +2} × araç {2, 3, 4}; Q = 25.
      Aynı tohumla darbesiz koşu referans alınır (ortak rastgele sayılar): fark yalnızca şokun etkisidir.
      ek_durus = darbeden itibaren net fazladan duruş (istasyon-dakika);
      toparlanma = darbe bittikten sonra net fazladan duruşun %95'inin biriktiği ana kadar geçen süre (dk).
C · Tek araç kurgusu (Bae, Evans & Summers 2016): araç = 1, baz talep; eşit kart (iki kutu) ve
      politika-tutarlı (VDI) kurallar altında P2 (T = 30, 60) ve P3 (anında, konsolidasyon).

Kullanım
--------
    python -X utf8 -m src.v2_kart_kapasite_ayristirma
    python -X utf8 -m src.v2_kart_kapasite_ayristirma --rep 6 --rep-b 20
"""

import argparse
import copy
import itertools
import os
import sys
import time
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

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir, kanban_boyutlandir
from src.v2_pareto_ve_figurler import _eksen_duzenle, INK, INK2, MUTED, YUZEY

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIHAI = dict(mesafe_modu="KOORDINAT", sim_sure=1440)
POLITIKA = {"P2 · T=60": dict(politika="P2", tur_araligi_dk=60),
            "P3 · konsolidasyon": dict(politika="P3", sevk="KONSOLIDASYON")}
RENK = {"P2 · T=60": "#2a78d6", "P3 · konsolidasyon": "#1baf7a"}


def _veri_q(temel, Q):
    if Q == temel.Q:
        return temel
    v = copy.copy(temel)
    v.Q = Q
    return v


def _n(veri, p, k):
    n, _ = kanban_boyutlandir(veri, replace(p, n_ozel=None))
    return tuple(int(x) for x in np.maximum(1, n + k))


# ─────────────────────────────────────────────────────────────
# A · Ayrıştırma
# ─────────────────────────────────────────────────────────────
def deney_a(temel, rep):
    K, ARAC, Q, TALEP = (-1, 0, 1, 2), (1, 2, 3, 4), (15, 25, 35), (1.0, 1.5)
    veriler = {q: _veri_q(temel, q) for q in Q}
    satir = []
    for pol, kw in POLITIKA.items():
        for k, m, q, d in itertools.product(K, ARAC, Q, TALEP):
            veri = veriler[q]
            p = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=m, talep_carpani=d,
                            kanban_modu="VDI", **kw, **NIHAI)
            p = replace(p, n_ozel=_n(veri, p, k))
            for r in range(rep):
                s = calistir(replace(p, seed=41000 + r), veri)
                satir.append({"politika": pol, "k": k, "arac": m, "Q": q, "talep": d, "tohum": r,
                              "durus": s["starv_pct_isinma_sonrasi"],
                              "wip": s["ort_wip_isinma_sonrasi"], "kart": s["toplam_kart"],
                              "doluluk": s["doluluk_pct"]})
        print(f"  ✓ A · {pol}")
    return pd.DataFrame(satir)


def eta_kare(df, y, faktorler):
    """Dengeli tam faktöriyel için η² (ana etkiler + iki yönlü etkileşimler)."""
    gm = df[y].mean()
    ss_top = float(((df[y] - gm) ** 2).sum())
    out = {}
    ana = {}
    for f in faktorler:
        m = df.groupby(f)[y].transform("mean")
        ana[f] = m
        out[f] = float(((m - gm) ** 2).sum()) / ss_top
    for a, b in itertools.combinations(faktorler, 2):
        mab = df.groupby([a, b])[y].transform("mean")
        out[f"{a} × {b}"] = float(((mab - ana[a] - ana[b] + gm) ** 2).sum()) / ss_top
    out["artık + yüksek dereceli"] = 1.0 - sum(out.values())
    return out


# ─────────────────────────────────────────────────────────────
# B · Toparlanma
# ─────────────────────────────────────────────────────────────
def deney_b(temel, rep, bas=480, sure=120):
    satir = []
    for pol, kw in POLITIKA.items():
        for k, m in itertools.product((0, 1, 2), (2, 3, 4)):
            p0 = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=m, kanban_modu="VDI",
                             **kw, **NIHAI)
            p0 = replace(p0, n_ozel=_n(temel, p0, k), zaman_serisi=True)
            for r in range(rep):
                ref = calistir(replace(p0, seed=51000 + r), temel)
                sok = calistir(replace(p0, seed=51000 + r, talep_carpani=1.5,
                                       sok_baslangic_dk=bas, sok_sure_dk=sure), temel)
                fark = np.asarray(sok["_starv_seri"][bas:]) - np.asarray(ref["_starv_seri"][bas:])
                # net fazladan duruş: şoktan sonra iki koşunun rastgele ayrışması artı ve eksi
                # yönde birbirini götürür; "son pozitif an" bu ayrışmaya duyarlı olduğu için
                # toparlanma, net fazladan duruşun %95'inin biriktiği an olarak tanımlanır
                net = float(fark.sum())
                if net > 0:
                    kum = np.cumsum(fark)
                    t95 = int(np.argmax(kum >= 0.95 * net)) + bas
                    topar = max(0, t95 - (bas + sure))
                else:
                    topar = 0
                satir.append({"politika": pol, "k": k, "arac": m, "tohum": r,
                              "kart": ref["toplam_kart"], "ek_durus": max(0.0, net),
                              "toparlanma_dk": topar, "wip_ref": ref["ort_wip_isinma_sonrasi"]})
        print(f"  ✓ B · {pol}")
    return pd.DataFrame(satir)


# ─────────────────────────────────────────────────────────────
# C · Tek araç (Bae vd. 2016)
# ─────────────────────────────────────────────────────────────
def deney_c(temel, rep):
    konf = {"P2 · T=30": dict(politika="P2", tur_araligi_dk=30),
            "P2 · T=60": dict(politika="P2", tur_araligi_dk=60),
            "P3 · anında": dict(politika="P3", sevk="ANINDA"),
            "P3 · konsolidasyon": dict(politika="P3", sevk="KONSOLIDASYON")}
    satir = []
    for kural, mod in (("A · eşit kart (iki kutu)", "IKI_KUTU"), ("B · politika-tutarlı", "VDI")):
        for ad, kw in konf.items():
            p = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=1, kanban_modu=mod, **kw, **NIHAI)
            d, w, kart = [], [], 0
            for r in range(rep):
                s = calistir(replace(p, seed=61000 + r), temel)
                d.append(s["starv_pct_isinma_sonrasi"])
                w.append(s["ort_wip_isinma_sonrasi"])
                kart = s["toplam_kart"]
            satir.append({"kural": kural, "sistem": ad, "durus": np.mean(d),
                          "durus_ga": 1.96 * np.std(d, ddof=1) / np.sqrt(rep),
                          "wip": np.mean(w), "kart": kart})
    print("  ✓ C · tek araç")
    return pd.DataFrame(satir)


def sekil9(etalar, b, yol):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.4, 5.0), facecolor=YUZEY,
                                   gridspec_kw={"width_ratios": [1.25, 1]})
    _eksen_duzenle(ax1, "Duruş varyansındaki pay (η²)", "", "Duruşun kaynağı")
    gruplar = ["k", "arac", "Q", "talep", "k × arac", "arac × talep", "k × talep"]
    etiket = {"k": "Kart sayısı", "arac": "Araç sayısı", "Q": "Araç kapasitesi",
              "talep": "Talep düzeyi", "k × arac": "Kart × araç", "arac × talep": "Araç × talep",
              "k × talep": "Kart × talep"}
    y = np.arange(len(gruplar))
    h = 0.38
    for i, (pol, e) in enumerate(etalar.items()):
        v = [e.get(g, 0) for g in gruplar]
        ax1.barh(y + (i - 0.5) * h, v, h * 0.92, color=RENK[pol], label=pol, zorder=3)
        for yy, vv in zip(y + (i - 0.5) * h, v):
            ax1.text(vv + 0.005, yy, f"{vv:.2f}", va="center", fontsize=8, color=INK2)
    ax1.set_yticks(y)
    ax1.set_yticklabels([etiket[g] for g in gruplar], fontsize=9)
    ax1.invert_yaxis()
    ax1.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="lower right")

    _eksen_duzenle(ax2, "Araç sayısı", "Net fazladan duruş (istasyon-dakika)", "+%50 talep darbesi, 120 dk")
    for pol in POLITIKA:
        for k, ls in ((0, "-"), (1, ":"), (2, "--")):
            s = b[(b["politika"] == pol) & (b["k"] == k)].groupby("arac")["ek_durus"].mean()
            ax2.plot(s.index, s.values, ls, marker="o", color=RENK[pol], lw=2,
                     label=f"{pol} · k={k:+d}")
    ax2.set_xticks([2, 3, 4])
    ax2.legend(frameon=False, fontsize=8, labelcolor=INK2)
    fig.suptitle("Şekil 9 · Duruşu kart sayısı mı, taşıma kapasitesi mi belirliyor?",
                 color=INK, fontsize=12, x=0.012, ha="left", y=0.98)
    fig.text(0.012, 0.015, "Nihai ayar: koordinat ağı, 1440 dk, ısınma sonrası. Sol: dengeli tam "
                           "faktöriyel η². Sağ: aynı tohumlu darbesiz koşuya göre net fazladan duruş "
                           "(k: istasyon başına ek kart).", color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.045, 1, 0.945))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=4, help="A ve C için tekrar")
    ap.add_argument("--rep-b", type=int, default=12, help="B için tekrar")
    args = ap.parse_args()
    t0 = time.perf_counter()
    temel = V2Veri()
    print("=" * 92)
    print("KART SAYISI ↔ TAŞIMA KAPASİTESİ AYRIŞTIRMASI VE TOPARLANMA (K109)")
    print("  Ciemnoczolowski & Bozer (2013) s.579 · nihai ayar (K105)")
    print("=" * 92)

    a = deney_a(temel, args.rep)
    faktor = ["k", "arac", "Q", "talep"]
    etalar = {pol: eta_kare(a[a["politika"] == pol], "durus", faktor) for pol in POLITIKA}
    etalar_tum = eta_kare(a, "durus", ["politika"] + faktor)
    b = deney_b(temel, args.rep_b)
    c = deney_c(temel, args.rep)

    print(f"\n{'═' * 92}\nA · Duruş varyansının ayrıştırılması (η²)\n{'═' * 92}")
    tum_anahtar = list(dict.fromkeys(list(etalar_tum) + [x for e in etalar.values() for x in e]))
    print(f"  {'Kaynak':28s} {'Tümü':>8s} " + " ".join(f"{p:>20s}" for p in POLITIKA))
    for kaynak in tum_anahtar:
        print(f"  {kaynak:28s} {etalar_tum.get(kaynak, float('nan')):8.3f} "
              + " ".join(f"{etalar[p].get(kaynak, float('nan')):20.3f}" for p in POLITIKA))
    for pol in POLITIKA:
        e = etalar[pol]
        kart = e["k"] + e.get("k × talep", 0)
        kap = e["arac"] + e["Q"] + e.get("arac × Q", 0) + e.get("arac × talep", 0) + e.get("Q × talep", 0)
        print(f"  {pol}: kart kaynaklı ≈ {kart:.2f} · taşıma kapasitesi kaynaklı ≈ {kap:.2f} · "
              f"kart × araç {e.get('k × arac', 0):.2f}")

    print(f"\n{'═' * 92}\nB · Toparlanma (ortalama, {args.rep_b} tekrar)\n{'═' * 92}")
    bo = (b.groupby(["politika", "k", "arac"])
           .agg(kart=("kart", "first"), ek_durus=("ek_durus", "mean"),
                toparlanma_dk=("toparlanma_dk", "mean"), wip=("wip_ref", "mean")).reset_index())
    print(bo.round(1).to_string(index=False))

    print(f"\n{'═' * 92}\nC · Tek araç (Bae vd. 2016 kurgusu), baz talep\n{'═' * 92}")
    print(c.round(2).to_string(index=False))

    cikti = os.path.join(KOK, "data", "synthetic")
    a.to_csv(os.path.join(cikti, "v2_kart_kapasite_a_ham.csv"), index=False, encoding="utf-8-sig")
    pd.DataFrame({"kaynak": tum_anahtar, "tumu": [etalar_tum.get(x) for x in tum_anahtar],
                  **{p: [etalar[p].get(x) for x in tum_anahtar] for p in POLITIKA}}
                 ).to_csv(os.path.join(cikti, "v2_kart_kapasite_a_eta.csv"), index=False, encoding="utf-8-sig")
    bo.to_csv(os.path.join(cikti, "v2_kart_kapasite_b_toparlanma.csv"), index=False, encoding="utf-8-sig")
    c.to_csv(os.path.join(cikti, "v2_kart_kapasite_c_tek_arac.csv"), index=False, encoding="utf-8-sig")
    sekil9(etalar, b, os.path.join(KOK, "docs", "figurler", "sekil9_kart_kapasite.png"))
    print(f"\n  → data/synthetic/v2_kart_kapasite_*.csv · docs/figurler/sekil9_kart_kapasite.png")
    print(f"  Toplam süre: {time.perf_counter() - t0:.0f} sn")


if __name__ == "__main__":
    main()
