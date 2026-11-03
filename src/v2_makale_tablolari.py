"""
v2_makale_tablolari.py
======================
Hafta 15 — Makale tablolarının nihai ayarla üretilmesi (K105)

Nihai ayar
----------
Önceki deneyler (K93–K98) motorun varsayılanlarıyla koşuldu: mevcut mesafe matrisi
(Floyd–Warshall ile metrikleştirilmiş, K71), 480 dk ufuk ve ısınmayı içeren göstergeler.
Sağlamlık testleri iki iyileştirmenin göreli sonuçları değiştirmediğini, ancak mutlak
değerleri kaydırdığını gösterdi:
  · K99  — göstergeler ısınma dönemini (90 dk) içeriyor; 1440 dk'da yanlılık üçte birine iner
  · K100 — mevcut matris gerçekleşemeyecek bir yerleşim tarif ediyor; koordinat ağı gerçekçi

Makale tabloları bu yüzden şu ayarla üretilir:
  · mesafe_modu = "KOORDINAT"   (Urru vd. 2018 durak aralığı, dikdörtgensel ölçü)
  · sim_sure    = 1440 dk        (3 vardiya)
  · gösterge    = ısınma sonrası (starv_pct_isinma_sonrasi, ort_wip_isinma_sonrasi)
Motorun varsayılanları değiştirilmedi; önceki betikler aynı sonuçları üretmeye devam eder.

Tablolar
--------
  Tablo 1 — Politika karşılaştırması: P1/P2 (T = 30, 60, 90, 120 dk) ve P3 (konsolidasyon,
            anında); her politika kendi formülüyle boyutlandırılmış (VDI, K65)
  Tablo 2 — Boyutlandırma tasarımının etkisi (K93): ortak iki kutulu tampon ↔ politika-tutarlı
  Tablo 3 — Dört adalet kuralı (K97): mevcut ve Toyota kutuları
Hepsi 3 araç, 12 replikasyon, baz talep ve +%50 talep şoku.

Çıktılar
--------
  data/synthetic/makale_tablo1_politikalar.csv
  data/synthetic/makale_tablo2_boyutlandirma.csv
  data/synthetic/makale_tablo3_adalet{,_egriler}.csv
  docs/makale_tablolari.md                        ← makaleye kopyalanacak tablolar
  docs/figurler/sekil7_adalet_kurallari_nihai{,_toyota}.png

Kullanım
--------
    python -X utf8 -m src.v2_makale_tablolari
    python -X utf8 -m src.v2_makale_tablolari --rep 20
"""

import argparse
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

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir
from src.v2_toyota_bandi_duyarliligi import c_varyantlari
import src.v2_boyutlandirma_duyarliligi as bd
import src.v2_adalet_kurallari as ak

NIHAI = dict(mesafe_modu="KOORDINAT", sim_sure=1440)
TALEPLER = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _ort_nihai(veri, p, rep, seed0=11000):
    """bd._ort ile aynı anahtarlar; duruş ve WIP ısınma sonrası, nihai ayarla."""
    tek = [calistir(replace(p, seed=seed0 + r, **NIHAI), veri) for r in range(rep)]
    kaynak = {"starv_pct": "starv_pct_isinma_sonrasi", "ort_wip": "ort_wip_isinma_sonrasi"}
    out = {}
    for k in ("starv_pct", "ort_wip", "toplam_mesafe_km", "tur_sayisi",
              "doluluk_pct", "toplam_kart", "ort_tur_sure_dk", "arac_kullanim_pct"):
        v = [t[kaynak.get(k, k)] for t in tek]
        out[k] = float(np.mean(v))
        out[k + "_ci95"] = 1.96 * float(np.std(v, ddof=1)) / np.sqrt(rep) if rep > 1 else 0.0
    return out


# Mevcut deney betikleri aynen kullanılır; yalnızca ortalama alma fonksiyonu nihai ayarla değiştirilir
bd._ort = _ort_nihai
ak._ort = _ort_nihai


def tablo1(veri, rep, arac):
    satir = []
    for talep_ad, talep in TALEPLER:
        konf = [("P1", T, None) for T in (30, 60, 90, 120)] + \
               [("P2", T, None) for T in (30, 60, 90, 120)] + \
               [("P3", None, "KONSOLIDASYON"), ("P3", None, "ANINDA")]
        for pol, T, sevk in konf:
            kw = dict(politika=pol)
            if T:
                kw["tur_araligi_dk"] = T
            if sevk:
                kw["sevk"] = sevk
            p = V2Parametre(talep_modeli="SAATLIK_REJIM", arac_sayisi=arac, talep_carpani=talep,
                            kanban_modu="VDI", **kw)
            satir.append({"talep": talep_ad, "politika": pol,
                          "takt": f"{T} dk" if T else ("sinyal · konsolidasyon" if sevk == "KONSOLIDASYON"
                                                       else "sinyal · anında"),
                          **_ort_nihai(veri, p, rep)})
    return pd.DataFrame(satir)


def tablo2(veriler, rep, arac):
    parcalar = []
    for kutu, veri in veriler.items():
        for talep_ad, talep in TALEPLER:
            d = bd.deney(veri, rep, arac, talep, talep_ad)
            d.insert(0, "kutu", kutu)
            parcalar.append(d)
    return pd.concat(parcalar, ignore_index=True)


def tablo3(veriler, rep, arac):
    egri_l, kural_l, kaz_l = [], [], []
    for kutu, veri in veriler.items():
        for talep_ad, talep in TALEPLER:
            e = ak.egri(veri, rep, arac, talep)
            k = ak.kurallar(e)
            z = ak.kazanan(k)
            for df, hedef in ((e, egri_l), (k, kural_l), (z, kaz_l)):
                df.insert(0, "talep", talep_ad)
                df.insert(0, "kutu", kutu)
                hedef.append(df)
    return tuple(pd.concat(x, ignore_index=True) for x in (egri_l, kural_l, kaz_l))


# ─────────────────────────────────────────────────────────────
# Markdown (Türkçe ondalık)
# ─────────────────────────────────────────────────────────────
def _s(x, b=2):
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{b}f}".replace(".", ",")


def _isaretli(x, b=2):
    return ("+" if x >= 0 else "−") + _s(abs(x), b)


def md_tablo1(t1):
    L = ["## Tablo 1 · Politika karşılaştırması",
         "",
         "Her politika kendi formülüyle boyutlandırılmıştır (P1/P2: $N = 1 + \\lceil D\\,T(1+\\alpha)/C \\rceil$, "
         "P3: $N = 1 + \\lceil ROP/C \\rceil$). 3 araç, 12 replikasyon, ortalama ± %95 GA.", ""]
    for talep, _ in TALEPLER:
        d = t1[t1["talep"] == talep]
        L += [f"**{talep}**", "",
              "| Politika | Takt | Duruş (%) | Ort. WIP (adet) | Kart | Sefer | Yol (km) | Araç doluluğu (%) |",
              "|---|---|---:|---:|---:|---:|---:|---:|"]
        for _, r in d.iterrows():
            L.append(f"| {r['politika']} | {r['takt']} | {_s(r['starv_pct'])} ± {_s(r['starv_pct_ci95'])} | "
                     f"{_s(r['ort_wip'], 0)} | {int(round(r['toplam_kart']))} | {_s(r['tur_sayisi'], 1)} | "
                     f"{_s(r['toplam_mesafe_km'], 1)} | {_s(r['doluluk_pct'], 1)} |")
        L.append("")
    return L


def md_tablo2(t2):
    L = ["## Tablo 2 · Boyutlandırma tasarımının karşılaştırmaya etkisi",
         "",
         "Geleneksel: P2, T = 60 dk. Dijital: P3, konsolidasyonlu sevk. Kurgu A: her iki sistemde "
         "aynı iki kutulu tampon (Vojdani & Drechsler 2022 s.5). Kurgu B: her sistem kendi formülüyle. "
         "Fark = dijital − geleneksel duruş (puan).", "",
         "| Kutu | Talep | Kurgu | Kart (gel./dij.) | Duruş gel. (%) | Duruş dij. (%) | Fark | WIP farkı | Önde |",
         "|---|---|---|---|---:|---:|---:|---:|---|"]
    ozet = []
    for (kutu, talep, kurgu), g in t2.groupby(["kutu", "talep", "kurgu"], sort=False):
        gl = g[g["sistem"].str.startswith("Geleneksel")].iloc[0]
        dj = g[g["sistem"].str.startswith("Dijital")].iloc[0]
        f = dj["starv_pct"] - gl["starv_pct"]
        ga = float(np.hypot(dj["starv_pct_ci95"], gl["starv_pct_ci95"]))
        kim = "eşit" if abs(f) <= ga else ("dijital" if f < 0 else "geleneksel")
        L.append(f"| {kutu} | {talep} | {kurgu[0]} | {int(gl['toplam_kart'])}/{int(dj['toplam_kart'])} | "
                 f"{_s(gl['starv_pct'])} | {_s(dj['starv_pct'])} | {_isaretli(f)} ± {_s(ga)} | "
                 f"%{_isaretli(100 * (dj['ort_wip'] / gl['ort_wip'] - 1), 0)} | {kim} |")
        ozet.append({"kutu": kutu, "talep": talep, "kurgu": kurgu[0], "fark": f, "ga": ga, "kim": kim})
    L.append("")
    oz = pd.DataFrame(ozet)
    for (kutu, talep), g in oz.groupby(["kutu", "talep"], sort=False):
        a, b = g[g["kurgu"] == "A"].iloc[0], g[g["kurgu"] == "B"].iloc[0]
        L.append(f"- {kutu} kutular, {talep.lower()}: kayma {_isaretli(b['fark'] - a['fark'])} puan; "
                 f"önde olan {a['kim']} → {b['kim']}.")
    L.append("")
    return L


def md_tablo3(t3k, t3z):
    L = ["## Tablo 3 · Dört adalet kuralı",
         "",
         "A eşit kart (Vojdani & Drechsler 2022) · B politika-tutarlı formül (Urru vd. 2018; VDI 5586) · "
         "C eşit hizmet düzeyi, duruş ≤ %1 (Alnahhal & Noche 2015) · D eşit WIP. "
         "C'de kazanan WIP'e, diğerlerinde duruşa göre belirlenir; Pareto sütunu iki ölçütü birlikte değerlendirir.", ""]
    for kutu in t3z["kutu"].unique():
        L += [f"**{'Toyota kutuları (C ≤ günlük talebin %10’u)' if kutu == 'toyota' else 'Mevcut kutular'}**", "",
              "| Talep | Kural | Kazanan | Δ duruş (puan) | Δ WIP | Pareto |",
              "|---|---|---|---:|---:|---|"]
        for _, r in t3z[t3z["kutu"] == kutu].iterrows():
            L.append(f"| {r['talep']} | {ak.KURAL_AD[r['kural']]} | **{r['kazanan']}** | "
                     f"{_isaretli(r['fark_durus'])} ± {_s(r['ga'])} | %{_isaretli(r['wip_fark_pct'], 0)} | {r['pareto']} |")
        L.append("")
        for talep, _ in TALEPLER:
            z = t3z[(t3z["kutu"] == kutu) & (t3z["talep"] == talep)]
            L.append(f"- {talep}: {z['kazanan'].nunique()} farklı sonuç ("
                     + ", ".join(f"{r['kural']} → {r['kazanan']}" for _, r in z.iterrows()) + ").")
        L.append("")
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=12)
    ap.add_argument("--arac", type=int, default=3)
    args = ap.parse_args()

    t0 = time.perf_counter()
    temel = V2Veri()
    veriler = {"mevcut": temel, "toyota": c_varyantlari(temel)["TOYOTA_Q_SABIT"]}
    print("=" * 92)
    print("MAKALE TABLOLARI — NİHAİ AYAR (K105)")
    print(f"  Koordinat ağı · {NIHAI['sim_sure']} dk · ısınma sonrası gösterge · "
          f"{args.arac} araç · {args.rep} replikasyon")
    print("=" * 92)

    t1 = tablo1(temel, args.rep, args.arac)
    print(f"  ✓ Tablo 1 ({time.perf_counter() - t0:.0f} sn)")
    t2 = tablo2(veriler, args.rep, args.arac)
    print(f"  ✓ Tablo 2 ({time.perf_counter() - t0:.0f} sn)")
    t3e, t3k, t3z = tablo3(veriler, args.rep, args.arac)
    print(f"  ✓ Tablo 3 ({time.perf_counter() - t0:.0f} sn)")

    cikti = os.path.join(KOK, "data", "synthetic")
    t1.to_csv(os.path.join(cikti, "makale_tablo1_politikalar.csv"), index=False, encoding="utf-8-sig")
    t2.to_csv(os.path.join(cikti, "makale_tablo2_boyutlandirma.csv"), index=False, encoding="utf-8-sig")
    t3k.to_csv(os.path.join(cikti, "makale_tablo3_adalet.csv"), index=False, encoding="utf-8-sig")
    t3z.to_csv(os.path.join(cikti, "makale_tablo3_adalet_kazanan.csv"), index=False, encoding="utf-8-sig")
    t3e.to_csv(os.path.join(cikti, "makale_tablo3_adalet_egriler.csv"), index=False, encoding="utf-8-sig")

    for kutu, ek in (("mevcut", ""), ("toyota", "_toyota")):
        e = t3e[t3e["kutu"] == kutu].drop(columns="kutu")
        k = t3k[t3k["kutu"] == kutu].drop(columns="kutu")
        ak.sekil7(e, k, os.path.join(KOK, "docs", "figurler", f"sekil7_adalet_kurallari_nihai{ek}.png"))

    md = ["# Makale Tabloları — Nihai Ayar",
          "",
          f"> Üretim: `python -X utf8 -m src.v2_makale_tablolari` · {time.strftime('%d.%m.%Y')} · K105",
          "> Ayar: koordinat tabanlı mesafe ağı (Urru vd. 2018 durak aralığı, K100), 1440 dk (3 vardiya), "
          "duruş ve WIP ısınma sonrası (90 dk, K78/K99). 3 araç, "
          f"{args.rep} replikasyon. Sayılar sentetik veriyle elde edilmiştir.",
          "> Önceki betiklerin (K93–K98) sayıları motor varsayılanlarıyla üretilmiştir; göreli sonuçlar "
          "aynıdır, mutlak değerler bu tablolardan alınmalıdır.",
          ""]
    md += md_tablo1(t1) + md_tablo2(t2) + md_tablo3(t3k, t3z)
    md += ["## Şekiller", "",
           "- `docs/figurler/sekil7_adalet_kurallari_nihai_toyota.png` — ana figür (Tablo 3, Toyota kutuları)",
           "- `docs/figurler/sekil7_adalet_kurallari_nihai.png` — mevcut kutular", ""]
    with open(os.path.join(KOK, "docs", "makale_tablolari.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("\n".join(md))
    print(f"\n  Toplam süre: {time.perf_counter() - t0:.0f} sn")


if __name__ == "__main__":
    main()
