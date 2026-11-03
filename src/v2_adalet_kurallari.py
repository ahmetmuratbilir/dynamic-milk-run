"""
v2_adalet_kurallari.py
======================
Hafta 15 — Politika karşılaştırmasında adalet (eşitleme) kuralları (Y1 + Y2, K97)

Soru
----
İki besleme politikası karşılaştırılırken tampon bir biçimde "eşit" kılınmak zorundadır.
Yazında dört farklı kural kullanılmaktadır ve hiçbir çalışma bunları yan yana koymaz:

  A · Eşit kart            : her iki sisteme aynı tampon
                             (Vojdani & Drechsler 2022 s.5 — iki kutulu Kanban)
  B · Politika-tutarlı     : her sistem kendi çevrim süresinden boyutlandırılır
                             (Urru vd. 2018 s.406; VDI 5586 — bu çalışmada K65)
  C · Eşit hizmet düzeyi   : her sistem hedef hizmet düzeyini sağlayan en küçük tampona
                             indirilir, sonra stok karşılaştırılır
                             (Alnahhal & Noche 2015 s.117: "fill rate ≥ %99")
  D · Eşit WIP             : sistemler aynı ortalama stokta karşılaştırılır (K53, K95)

Bu betik dört kuralı aynı sistemde uygular ve her kuralda "kazananı" belirler.
Y2: tek ölçütlü sıralama yerine duruş–WIP düzleminde Pareto baskınlığı da raporlanır.

Yöntem
------
Her sistem için kart sayısı tek bir kaydırma ile taranır: N_i = max(1, N_i^VDI + k),
k ∈ {−3 … +6}. Böylece her sistemin duruş–WIP eğrisi elde edilir; B kuralı k=0
noktasıdır, C ve D bu eğriler üzerinde aranır (D'de doğrusal ara değerleme).
Sistemler K93 ile aynıdır: geleneksel = P2, T=60 dk; dijital = P3, konsolidasyonlu sevk.

⚠️ Sınırlar: tüm istasyonlara aynı k uygulanır (istasyon bazında optimum aranmaz);
duruş ≤ %1, hizmet düzeyi %99'un vekili olarak alınır (zaman bazlı, adet bazlı değil).

Kullanım
--------
    python -X utf8 -m src.v2_adalet_kurallari
    python -X utf8 -m src.v2_adalet_kurallari --rep 20
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
from src.v2_pareto_ve_figurler import _eksen_duzenle, INK, INK2, MUTED, YUZEY

SISTEMLER = [("Geleneksel", GELENEKSEL), ("Dijital", DIJITAL)]
TALEPLER = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]
KAYDIRMA = list(range(-3, 7))
HEDEF_DURUS = 1.0           # % — hizmet düzeyi ≈ %99 vekili (Alnahhal & Noche 2015 s.117)
RENK = {"Geleneksel": "#2a78d6", "Dijital": "#1baf7a"}
KURAL_AD = {"A": "A · Eşit kart", "B": "B · Politika-tutarlı",
            "C": "C · Eşit hizmet düzeyi", "D": "D · Eşit WIP"}


def egri(veri, rep, arac, talep):
    """Her sistem için k taraması + iki kutulu (A) nokta."""
    satir = []
    for sistem, kw in SISTEMLER:
        p0 = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac,
                         talep_carpani=talep, kanban_modu="VDI", **kw)
        n_vdi, _ = kanban_boyutlandir(veri, p0)
        for k in KAYDIRMA:
            n = np.maximum(1, n_vdi + k)
            r = _ort(veri, replace(p0, n_ozel=tuple(int(x) for x in n)), rep)
            satir.append({"sistem": sistem, "nokta": f"k={k:+d}", "k": k, **r})
        r = _ort(veri, replace(p0, kanban_modu="IKI_KUTU"), rep)
        satir.append({"sistem": sistem, "nokta": "iki_kutu", "k": np.nan, **r})
    return pd.DataFrame(satir)


def kurallar(e: pd.DataFrame) -> pd.DataFrame:
    """Dört kuralın her biri için iki sistemin karşılaştırma noktası."""
    out = []
    tarama = e[e["nokta"] != "iki_kutu"]

    def ekle(kural, sistem, r, not_=""):
        out.append({"kural": kural, "sistem": sistem, "starv_pct": r["starv_pct"],
                    "starv_ci95": r["starv_pct_ci95"], "ort_wip": r["ort_wip"],
                    "toplam_kart": r["toplam_kart"], "not": not_})

    for sistem, _ in SISTEMLER:
        ekle("A", sistem, e[(e["sistem"] == sistem) & (e["nokta"] == "iki_kutu")].iloc[0])
        ekle("B", sistem, tarama[(tarama["sistem"] == sistem) & (tarama["k"] == 0)].iloc[0])
        s = tarama[tarama["sistem"] == sistem].sort_values("k")
        uygun = s[s["starv_pct"] <= HEDEF_DURUS]
        if len(uygun):
            ekle("C", sistem, uygun.iloc[0], f"k={int(uygun.iloc[0]['k']):+d}")
        else:
            ekle("C", sistem, s.iloc[-1], f"hedefe ulaşılamadı (k={int(s.iloc[-1]['k']):+d})")

    # D: ortak WIP = dijital sistemin politika-tutarlı WIP'i; geleneksel eğride ara değerleme
    w_hedef = tarama[(tarama["sistem"] == "Dijital") & (tarama["k"] == 0)].iloc[0]["ort_wip"]
    for sistem, _ in SISTEMLER:
        s = tarama[tarama["sistem"] == sistem].sort_values("ort_wip")
        w, y, g = s["ort_wip"].to_numpy(), s["starv_pct"].to_numpy(), s["starv_pct_ci95"].to_numpy()
        if w.min() <= w_hedef <= w.max():
            r = {"starv_pct": float(np.interp(w_hedef, w, y)),
                 "starv_pct_ci95": float(np.interp(w_hedef, w, g)),
                 "ort_wip": float(w_hedef), "toplam_kart": np.nan}
            ekle("D", sistem, r, "ara değerleme")
        else:
            j = int(np.argmin(np.abs(w - w_hedef)))
            r = {"starv_pct": y[j], "starv_pct_ci95": g[j], "ort_wip": w[j],
                 "toplam_kart": s.iloc[j]["toplam_kart"]}
            ekle("D", sistem, r, f"hedef WIP {w_hedef:.0f} erişilemedi")
    return pd.DataFrame(out)


def kazanan(k: pd.DataFrame) -> pd.DataFrame:
    sat = []
    for kural, g in k.groupby("kural", sort=False):
        gel = g[g["sistem"] == "Geleneksel"].iloc[0]
        dij = g[g["sistem"] == "Dijital"].iloc[0]
        fark = dij["starv_pct"] - gel["starv_pct"]
        ga = float(np.hypot(gel["starv_ci95"], dij["starv_ci95"]))
        wip_fark = 100 * (dij["ort_wip"] / gel["ort_wip"] - 1)
        if kural == "C":                      # eşit hizmet → stokta kazanan
            kim = "Dijital" if wip_fark < -5 else ("Geleneksel" if wip_fark > 5 else "eşit")
            olcut = "WIP (hizmet eşit)"
        else:                                 # A, B, D → duruşta kazanan
            kim = "eşit" if abs(fark) <= ga else ("Dijital" if fark < 0 else "Geleneksel")
            olcut = "duruş"
        # Y2: Pareto baskınlığı (duruş GA dahilinde eşit sayılır, WIP %5 tolerans)
        d_iyi = (fark <= ga) and (wip_fark <= 5) and (fark < -ga or wip_fark < -5)
        g_iyi = (fark >= -ga) and (wip_fark >= -5) and (fark > ga or wip_fark > 5)
        pareto = "Dijital baskın" if d_iyi else ("Geleneksel baskın" if g_iyi else "baskınlık yok (takas)")
        sat.append({"kural": kural, "fark_durus": fark, "ga": ga, "wip_fark_pct": wip_fark,
                    "olcut": olcut, "kazanan": kim, "pareto": pareto,
                    "not": "; ".join(x for x in (gel["not"], dij["not"]) if x)})
    return pd.DataFrame(sat)


def rapor(talep, k, kz):
    print(f"\n{'═' * 96}\n{talep}\n{'═' * 96}")
    print(f"  {'Kural':26s} {'Sistem':11s} {'Duruş %':>12s} {'WIP':>7s} {'Kart':>5s}  not")
    for _, r in k.iterrows():
        kart = "" if pd.isna(r["toplam_kart"]) else f"{int(r['toplam_kart'])}"
        print(f"  {KURAL_AD[r['kural']]:26s} {r['sistem']:11s} "
              f"{r['starv_pct']:6.2f}±{r['starv_ci95']:4.2f} {r['ort_wip']:7.0f} {kart:>5s}  {r['not']}")
    print(f"\n  {'Kural':26s} {'Ölçüt':18s} {'Kazanan':12s} {'Δduruş':>8s} {'ΔWIP':>7s}  Pareto (Y2)")
    for _, r in kz.iterrows():
        print(f"  {KURAL_AD[r['kural']]:26s} {r['olcut']:18s} {r['kazanan']:12s} "
              f"{r['fark_durus']:+8.2f} {r['wip_fark_pct']:+6.0f}%  {r['pareto']}")


def sekil7(tum_e, tum_k, yol):
    """Duruş–WIP eğrileri; dört kural aynı iki eğri üzerinde dört nokta."""
    isaret = {"A": "s", "B": "o", "C": "^", "D": "D"}
    fig, axlar = plt.subplots(1, len(TALEPLER), figsize=(11.4, 5.3), facecolor=YUZEY)
    for i, (ax, (talep, _)) in enumerate(zip(axlar, TALEPLER)):
        _eksen_duzenle(ax, "Ortalama WIP (adet)", "Hat duruş oranı (%)" if i == 0 else "", talep)
        e = tum_e[(tum_e["talep"] == talep) & (tum_e["nokta"] != "iki_kutu")]
        for sistem, _ in SISTEMLER:
            s = e[e["sistem"] == sistem].sort_values("ort_wip")
            ax.plot(s["ort_wip"], s["starv_pct"], "-", color=RENK[sistem], lw=1.8, alpha=0.55,
                    zorder=2, label=f"{sistem} · kart taraması" if i == 0 else None)
            ax.scatter(s["ort_wip"], s["starv_pct"], s=12, color=RENK[sistem], alpha=0.55, zorder=2)
        k = tum_k[tum_k["talep"] == talep]
        ax.axhline(HEDEF_DURUS, color=MUTED, lw=0.8, ls=":", zorder=1)
        # ilgi bölgesi: kural noktalarının çevresi (uzun kuyruk eğrinin şeklini ezmesin)
        x_ust = 1.35 * k["ort_wip"].max()
        gorunur = e[e["ort_wip"] <= x_ust]["starv_pct"]
        y_ust = 1.15 * max(k["starv_pct"].max(), gorunur.max(), 2 * HEDEF_DURUS)
        ax.set_xlim(0, x_ust)
        ax.set_ylim(-0.03 * y_ust, y_ust)
        # yakın düşen kural noktaları tek etikette birleşir ("B=D"); tolerans eksen ölçeğinin %3'ü
        for sistem in ("Geleneksel", "Dijital"):
            gruplar = []
            for _, r in k[k["sistem"] == sistem].iterrows():
                ax.scatter(r["ort_wip"], r["starv_pct"], marker=isaret[r["kural"]], s=70,
                           facecolor=RENK[sistem], edgecolor=INK, lw=0.8, zorder=4)
                for g in gruplar:
                    if abs(g["x"] - r["ort_wip"]) < 0.03 * x_ust and abs(g["y"] - r["starv_pct"]) < 0.03 * y_ust:
                        g["ad"].append(r["kural"])
                        break
                else:
                    gruplar.append({"x": r["ort_wip"], "y": r["starv_pct"], "ad": [r["kural"]]})
            for g in gruplar:
                # geleneksel etiketleri sağ üste, dijital sol alta: çakışmayı önler
                ofs = (7, 6) if sistem == "Geleneksel" else (-8 - 7 * len(g["ad"]), -14)
                ax.annotate("=".join(g["ad"]), (g["x"], g["y"]), xytext=ofs, textcoords="offset points",
                            fontsize=9, color=RENK[sistem], fontweight="bold")
    for kural, m in isaret.items():
        axlar[1].scatter([], [], marker=m, s=55, facecolor="none", edgecolor=INK, label=KURAL_AD[kural])
    axlar[0].legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="upper right")
    axlar[1].legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="upper right")
    fig.suptitle("Şekil 7 · Aynı iki sistem, dört adalet kuralı: kazanan kurala göre değişir",
                 color=INK, fontsize=12, x=0.012, ha="left", y=0.98)
    fig.text(0.012, 0.015, "Eğriler: N_i = max(1, N_i^VDI + k), k = −3…+6. Noktalı çizgi: "
                           "%1 duruş (C kuralının hizmet hedefi). Geleneksel: P2, T=60 dk; "
                           "dijital: P3, konsolidasyonlu sevk; 3 araç.", color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.045, 1, 0.945))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=12)
    ap.add_argument("--arac", type=int, default=3)
    ap.add_argument("--kutu", choices=["mevcut", "toyota"], default="mevcut",
                    help="toyota: C_i = ⌊0,10 · günlük talep⌋ (K95)")
    args = ap.parse_args()

    veri = V2Veri()
    if args.kutu == "toyota":
        from src.v2_toyota_bandi_duyarliligi import c_varyantlari
        veri = c_varyantlari(veri)["TOYOTA_Q_SABIT"]
    ek = "" if args.kutu == "mevcut" else "_toyota"
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 96)
    print("POLİTİKA KARŞILAŞTIRMASINDA ADALET KURALLARI (Y1 + Y2 / K97)")
    print(f"  Kutu: {args.kutu} · Filo: {args.arac} araç · Replikasyon: {args.rep} · Kart kaydırma k ∈ "
          f"{KAYDIRMA[0]}…{KAYDIRMA[-1]:+d} · Hizmet hedefi: duruş ≤ %{HEDEF_DURUS:.0f}")
    print("=" * 96)

    tum_e, tum_k, tum_z = [], [], []
    for talep, carpan in TALEPLER:
        e = egri(veri, args.rep, args.arac, carpan)
        k = kurallar(e)
        z = kazanan(k)
        rapor(talep, k, z)
        for df, hedef in ((e, tum_e), (k, tum_k), (z, tum_z)):
            df.insert(0, "talep", talep)
            hedef.append(df)
    tum_e, tum_k, tum_z = (pd.concat(x, ignore_index=True) for x in (tum_e, tum_k, tum_z))

    print(f"\n{'═' * 96}\nÖZET — kazanan kurala göre değişiyor mu?\n{'═' * 96}")
    for talep, _ in TALEPLER:
        z = tum_z[tum_z["talep"] == talep]
        kz = ", ".join(f"{r['kural']}→{r['kazanan']}" for _, r in z.iterrows())
        print(f"  {talep:18s} {kz}   ({z['kazanan'].nunique()} farklı sonuç)")

    cikti = os.path.join(kok, "data", "synthetic")
    tum_e.to_csv(os.path.join(cikti, f"v2_adalet_egriler{ek}.csv"), index=False, encoding="utf-8-sig")
    tum_k.to_csv(os.path.join(cikti, f"v2_adalet_kurallar{ek}.csv"), index=False, encoding="utf-8-sig")
    tum_z.to_csv(os.path.join(cikti, f"v2_adalet_kazanan{ek}.csv"), index=False, encoding="utf-8-sig")
    fig_yol = os.path.join(kok, "docs", "figurler", f"sekil7_adalet_kurallari{ek}.png")
    sekil7(tum_e, tum_k, fig_yol)
    print(f"\n  → data/synthetic/v2_adalet_{{egriler,kurallar,kazanan}}{ek}.csv")
    print(f"  → docs/figurler/{os.path.basename(fig_yol)}")


if __name__ == "__main__":
    main()
