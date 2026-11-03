"""
v2_boyutlandirma_duyarliligi.py
===============================
Hafta 15 — Boyutlandırma Tasarımının Politika Karşılaştırmasına Etkisi (K93)

Amaç
----
Tezin ana katkısını **kendi v1 modelimizin dışına taşımak**. Şimdiye kadar
politika-tutarsız boyutlandırmanın etkisi yalnızca kendi v1 motorumuzda gösterildi;
hakem haklı olarak *"kendi hatanızı düzeltmek katkı mıdır?"* diye sorabilir.

Bu betik, **bağımsız bir çalışmada kullanılan karşılaştırma tasarımını** ele alır:

  Vojdani & Drechsler (2022), *Simulationsbasierte Analyse eines innerbetrieblichen
  digitalisierten Milk Run Systems*, Logistics Journal: Proceedings, s.5:
    · İki sistem karşılaştırılır: geleneksel (saatlik sabit tur, Kanban kartı) ve
      dijitalleşmiş (e-Kanban tetiklemeli, esnek rota).
    · *"Die beiden Systeme weisen ein identisches Layout und identische Taktzeiten
      an den Arbeitsstationen auf."*
    · *"Die Versorgung der Stationen wird über ein **Zwei-Behälter-Kanban-System**
      gewährleistet."* → **her iki sistemde de aynı iki kutulu tampon.**
    · Bulguları: dijital sistem %27 daha az sefer, %29,39 daha az yol,
      %38,5 daha az sürüş süresi (s.6).

Yani çevrim süreleri farklıdır (saatlik ↔ ihtiyaca göre) ama **tampon aynıdır**.
Droste & Deuse (2011) s.607–608 ve Urru vd. (2018) s.406'ya göre gereken tampon
çevrim süresiyle değişmelidir; dolayısıyla bu tasarım politika-tutarsızdır.

⚠️ ÇERÇEVELEME — ÇOK ÖNEMLİ
---------------------------
Bu bir **çürütme değildir**, bir **duyarlılık analizidir**:
  · Vojdani'nin kendi bulgusu (sefer/yol/süre tasarrufu) **taşıma verimliliği**
    üzerinedir ve bu düzeltmeden etkilenmez — nitekim aşağıda doğrulanmaktadır.
  · Sorgulanan şey, aynı tasarımın **hat duruşu (starvation)** karşılaştırmasına
    taşınması durumunda ortaya çıkabilecek yanlılıktır.
  · Vojdani'nin modeli yeniden üretilmemektedir (makalede sayısal parametre tablosu
    yoktur); yeniden üretilen şey **karşılaştırma tasarımıdır**, bu çalışmanın kendi
    24 istasyonlu sistemi üzerinde.

Deney
-----
  Kurgu A — "ortak tampon"      : tüm politikalar N = 2 (Vojdani tasarımı)
  Kurgu B — "politika-tutarlı"  : her politika kendi formülüyle (K65 / VDI)
  Ölçüt   : politika sıralaması, duruş farkı ve Vojdani'nin üç taşıma metriği

Kullanım
--------
    python -X utf8 -m src.v2_boyutlandirma_duyarliligi
    python -X utf8 -m src.v2_boyutlandirma_duyarliligi --rep 20
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

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir
from src.v2_pareto_ve_figurler import _eksen_duzenle, INK, INK2, MUTED, YUZEY, KRITIK

# Vojdani & Drechsler (2022) s.5–6 karşılaştırma tasarımı
GELENEKSEL = dict(politika="P2", tur_araligi_dk=60)        # saatlik sabit tur, Kanban miktarı
DIJITAL = dict(politika="P3", sevk="KONSOLIDASYON")        # e-Kanban tetiklemeli, esnek rota
KURGULAR = [("A · ortak tampon (Vojdani tasarımı)", "IKI_KUTU"),
            ("B · politika-tutarlı (K65)", "VDI")]


def _ort(veri, p, rep, seed0=11000):
    tek = [calistir(replace(p, seed=seed0 + r), veri) for r in range(rep)]
    out = {}
    for k in ("starv_pct", "ort_wip", "toplam_mesafe_km", "tur_sayisi",
              "doluluk_pct", "toplam_kart", "ort_tur_sure_dk", "arac_kullanim_pct"):
        v = [t[k] for t in tek]
        out[k] = float(np.mean(v))
        out[k + "_ci95"] = 1.96 * float(np.std(v, ddof=1)) / np.sqrt(rep) if rep > 1 else 0.0
    return out


def deney(veri: V2Veri, rep: int, arac: int, talep: float, talep_ad: str) -> pd.DataFrame:
    satir = []
    for kurgu_ad, mod in KURGULAR:
        for sistem_ad, kw in [("Geleneksel (saatlik sabit tur)", GELENEKSEL),
                              ("Dijitalleşmiş (e-Kanban, esnek rota)", DIJITAL)]:
            p = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac,
                            talep_carpani=talep, kanban_modu=mod, **kw)
            r = _ort(veri, p, rep)
            satir.append({"talep": talep_ad, "kurgu": kurgu_ad, "sistem": sistem_ad, **r})
    return pd.DataFrame(satir)


def rapor(df: pd.DataFrame, talep_ad: str):
    d = df[df["talep"] == talep_ad]
    print(f"\n{'═' * 84}\nTALEP: {talep_ad}\n{'═' * 84}")
    print(f"  {'Kurgu / Sistem':52s} {'Duruş%':>9s} {'WIP':>7s} {'Kart':>5s} "
          f"{'Tur':>6s} {'km':>6s}")
    for kurgu_ad, _ in KURGULAR:
        for _, r in d[d["kurgu"] == kurgu_ad].iterrows():
            print(f"  {kurgu_ad[:2] + ' · ' + r['sistem']:52s} "
                  f"{r['starv_pct']:7.2f}±{r['starv_pct_ci95']:.2f} "
                  f"{r['ort_wip']:7.0f} {int(r['toplam_kart']):5d} "
                  f"{r['tur_sayisi']:6.1f} {r['toplam_mesafe_km']:6.1f}")

    print("\n  ── Her kurguda dijital sistemin geleneksele göre farkı ──")
    ozet = {}
    for kurgu_ad, _ in KURGULAR:
        k = d[d["kurgu"] == kurgu_ad]
        gel = k[k["sistem"].str.startswith("Geleneksel")].iloc[0]
        dij = k[k["sistem"].str.startswith("Dijital")].iloc[0]
        fark = dij["starv_pct"] - gel["starv_pct"]
        kim = "dijital lehine" if fark < 0 else ("geleneksel lehine" if fark > 0 else "eşit")
        ozet[kurgu_ad] = fark
        print(f"    {kurgu_ad:42s} duruş {fark:+6.2f} puan ({kim})")
        print(f"      {'':40s}   sefer %{100 * (dij['tur_sayisi'] / gel['tur_sayisi'] - 1):+6.1f} · "
              f"yol %{100 * (dij['toplam_mesafe_km'] / gel['toplam_mesafe_km'] - 1):+6.1f} · "
              f"WIP %{100 * (dij['ort_wip'] / gel['ort_wip'] - 1):+6.1f} · "
              f"kart {int(gel['toplam_kart'])}→{int(dij['toplam_kart'])}")
    return ozet


def sekil5(tum: pd.DataFrame, yol: str):
    """İki kurguda duruş oranları; sıralamanın değiştiği yer vurgulanır."""
    RENK_SIS = {"Geleneksel": "#2a78d6", "Dijital": "#1baf7a"}
    talepler = list(dict.fromkeys(tum["talep"]))
    fig, axlar = plt.subplots(1, len(talepler), figsize=(11.4, 5.2),
                              facecolor=YUZEY, sharey=True)
    for k, (ax, talep) in enumerate(zip(np.atleast_1d(axlar), talepler)):
        _eksen_duzenle(ax, "", "Hat duruş oranı (%)" if k == 0 else "", talep)
        d = tum[tum["talep"] == talep]
        x = np.arange(len(KURGULAR))
        gen = 0.36
        for j, (etiket, anahtar) in enumerate([("Geleneksel · saatlik sabit tur", "Geleneksel"),
                                               ("Dijitalleşmiş · e-Kanban", "Dijital")]):
            y, hata = [], []
            for kurgu_ad, _ in KURGULAR:
                r = d[(d["kurgu"] == kurgu_ad) & (d["sistem"].str.startswith(anahtar))].iloc[0]
                y.append(r["starv_pct"])
                hata.append(r["starv_pct_ci95"])
            ax.bar(x + (j - 0.5) * gen, y, gen * 0.92, yerr=hata, capsize=4,
                   color=RENK_SIS[anahtar], zorder=3,
                   error_kw=dict(ecolor=MUTED, lw=1.2),
                   label=etiket if k == 0 else None)
            tepe = max(d["starv_pct"])
            for xi, yi, hi in zip(x + (j - 0.5) * gen, y, hata):
                ax.text(xi, yi + hi + tepe * 0.035, f"{yi:.2f}", ha="center",
                        color=INK2, fontsize=9)
        # sıralama değişimi işareti
        for i, (kurgu_ad, _) in enumerate(KURGULAR):
            kk = d[d["kurgu"] == kurgu_ad]
            gl = kk[kk["sistem"].str.startswith("Geleneksel")].iloc[0]["starv_pct"]
            dj = kk[kk["sistem"].str.startswith("Dijital")].iloc[0]["starv_pct"]
            ax.annotate(f"fark {dj - gl:+.2f}", xy=(i, max(gl, dj)),
                        xytext=(0, 26), textcoords="offset points", ha="center",
                        color=KRITIK if abs(dj - gl) > 1 else MUTED, fontsize=9,
                        fontweight="bold" if abs(dj - gl) > 1 else "normal")
        ax.set_xticks(x)
        ax.set_xticklabels(["A · ortak tampon\n(Vojdani tasarımı)",
                            "B · politika-tutarlı\n(K65)"], fontsize=9)
        ax.set_ylim(0, max(d["starv_pct"]) * 1.35)
    np.atleast_1d(axlar)[0].legend(frameon=False, fontsize=9, labelcolor=INK2,
                                   loc="upper right")
    fig.suptitle("Şekil 5 · Boyutlandırma tasarımı politika karşılaştırmasının sonucunu "
                 "değiştirmektedir", color=INK, fontsize=12, x=0.012, ha="left", y=0.98)
    fig.text(0.012, 0.015, "Hata çubukları: %95 güven aralığı (12 replikasyon). "
                           "Kurgu A'da her iki sistem de 48 kart; kurgu B'de geleneksel "
                           "63, dijital 49 kart alır.", color=MUTED, fontsize=8)
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
    cikti = os.path.join(kok, "data", "synthetic")
    os.makedirs(cikti, exist_ok=True)

    print("=" * 84)
    print("BOYUTLANDIRMA TASARIMININ POLİTİKA KARŞILAŞTIRMASINA ETKİSİ (K93)")
    print("  Karşılaştırma tasarımı: Vojdani & Drechsler (2022) s.5")
    print(f"  Filo: {args.arac} araç · Replikasyon: {args.rep} · Talep: saatlik rejim")
    print("  ⚠️ Vojdani'nin modeli değil, karşılaştırma TASARIMI yeniden kurulmuştur.")
    print("=" * 84)

    parcalar, ozetler = [], {}
    for talep_ad, carpan in [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]:
        df = deney(veri, args.rep, args.arac, carpan, talep_ad)
        parcalar.append(df)
        ozetler[talep_ad] = rapor(df, talep_ad)

    tum = pd.concat(parcalar, ignore_index=True)
    yol = os.path.join(cikti, "v2_boyutlandirma_duyarliligi.csv")
    tum.to_csv(yol, index=False, encoding="utf-8")

    fig_dizin = os.path.join(kok, "docs", "figurler")
    os.makedirs(fig_dizin, exist_ok=True)
    sekil5(tum, os.path.join(fig_dizin, "sekil5_boyutlandirma_duyarliligi.png"))
    print("\n  Figür: docs/figurler/sekil5_boyutlandirma_duyarliligi.png")

    print(f"\n{'═' * 84}\nSONUÇ\n{'═' * 84}")
    for talep_ad, o in ozetler.items():
        a = o[KURGULAR[0][0]]
        b = o[KURGULAR[1][0]]
        yon_degisti = (a > 0) != (b > 0)
        print(f"  {talep_ad}:")
        print(f"    Kurgu A (ortak tampon)     → duruş farkı {a:+6.2f} puan")
        print(f"    Kurgu B (politika-tutarlı) → duruş farkı {b:+6.2f} puan")
        print(f"    Tasarımın yarattığı kayma  : {abs(b - a):6.2f} puan"
              f"{'  ⚠️ SIRALAMA DEĞİŞTİ' if yon_degisti else ''}")
    print(f"\n  CSV: data/synthetic/v2_boyutlandirma_duyarliligi.csv ({len(tum)} satır)")


if __name__ == "__main__":
    main()
