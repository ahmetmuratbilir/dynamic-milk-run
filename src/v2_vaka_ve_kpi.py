"""
v2_vaka_ve_kpi.py
=================
Hafta 14 — Vaka Çalışması, Dinamik Kanban Testi, Dinamiklik Derecesi ve KPI Uyumu

Dört analiz üretir:

  V1  VAKA ÇALIŞMASI (K83)
      TR Dizin dergileri, özellikle Endüstri Mühendisliği Dergisi, gerçek veya gerçekçi
      bir vaka içeren çalışmalara öncelik vermektedir. Gerçek fabrika verisi henüz
      bulunmadığından, **literatürden türetilmiş** ve bu şekilde açıkça etiketlenmiş bir
      vaka kurgulanır: bir otomotiv yan sanayi montaj atölyesinin tek vardiyası.
      Ölçek ve parametreler klasördeki üç vakadan alınmıştır:
        · Facchini vd. (2022) s.1125: otomotiv kaynak atölyesi, 3 vagonlu 4 çekici,
          vardiyada ~400 sefer; 25 dk üzeri "geç", 15 dk altı "erken" teslimat
        · Menanno vd. (2023) s.13-14: 11 hatlı pompa montajı, Q_min 35-55 birim
        · Sevim & Görkemli Aykut (2026) s.67: 10 istasyon, ROP 25-50 birim
      Vaka, üç politikanın normal vardiya ve iki bozucu senaryo altında karşılaştırılmasıdır.

  V2  KOŞU-İÇİ DİNAMİK KANBAN (K74/C4)
      Literatürde *adaptive Kanban*, kart sayısının işletme sırasında değiştiği sistemdir
      (Elloumi vd. 2025 s.613). Projede N yalnızca senaryolar arasında değişiyordu.
      Burada koşu-içi güncelleme (30 dk'da bir, son 60 dk tüketiminden) sabit N ile
      karşılaştırılır — özellikle talep kayması altında.

  V3  DİNAMİKLİK DERECESİ (K84/C5)
      Larsen vd. (2008), *Recent Developments in Dynamic Vehicle Routing Systems*,
      Bölüm 3.1: dod = n_imm / n_tot (anlık istek oranı) ve zaman pencereli uyarlaması.
      Projenin problem sınıfı bu ölçütle sayısallaştırılır.

  V4  LİTERATÜR KPI UYUMU (K85/C6)
      Sevim & Görkemli Aykut (2026) s.67, Denk. 5-9'daki dört performans ölçütü
      (ortalama doluluk, tur başına mesafe, tur sayısı, istasyon başına bekleme süresi)
      ile Menanno vd. (2023) s.16'daki starvation tanımı raporlanır.

Kullanım:
    python -X utf8 -m src.v2_vaka_ve_kpi
"""

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

REP = 12


def _ort(veri, p, rep=REP, seed0=8000):
    tek = [calistir(replace(p, seed=seed0 + r), veri) for r in range(rep)]
    cikti = {}
    for k in tek[0]:
        if k.startswith("_"):
            continue
        v = [t[k] for t in tek]
        if all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
            cikti[k] = float(np.mean(v))
            cikti[k + "_ci95"] = 1.96 * float(np.std(v, ddof=1)) / np.sqrt(rep)
        else:
            cikti[k] = v[0]
    return cikti


# ─────────────────────────────────────────────────────────────
def v1_vaka(veri: V2Veri) -> pd.DataFrame:
    print("\n" + "═" * 78)
    print("V1 · VAKA ÇALIŞMASI — Otomotiv yan sanayi montaj atölyesi (literatürden türetilmiş)")
    print("═" * 78)
    print("  Ölçek: 4 hat · 24 istasyon · 1 süpermarket · 480 dk vardiya")
    print("  Kaynak ölçekler: Facchini 2022 s.1125 (4 çekici) · Menanno 2023 s.13 (11 hat)")
    print("                   Sevim & Görkemli Aykut 2026 s.67 (10 istasyon, ROP 25-50)")
    print("  ⚠️ Gerçek fabrika verisi DEĞİLDİR; literatür parametreleriyle kurgulanmıştır.\n")

    senaryolar = [
        ("Normal vardiya", dict(talep_carpani=1.0, arac_sayisi=3)),
        ("Talep şoku +%50", dict(talep_carpani=1.5, arac_sayisi=3)),
        ("Araç arızası (3→2)", dict(talep_carpani=1.0, arac_sayisi=2)),
    ]
    politikalar = [("P1", dict(politika="P1", tur_araligi_dk=60)),
                   ("P2", dict(politika="P2", tur_araligi_dk=60)),
                   ("P3", dict(politika="P3", sevk="KONSOLIDASYON"))]

    satir = []
    for s_ad, s_kw in senaryolar:
        print(f"  ── {s_ad} ──")
        for p_ad, p_kw in politikalar:
            p = V2Parametre(talep_modeli="SAATLIK_REJIM", **{**s_kw, **p_kw})
            r = _ort(veri, p)
            satir.append({"senaryo": s_ad, "politika": p_ad, **{
                k: r[k] for k in ("starv_pct", "starv_pct_ci95", "ort_wip",
                                  "toplam_mesafe_km", "tur_sayisi", "doluluk_pct",
                                  "arac_kullanim_pct", "toplam_kart")}})
            print(f"     {p_ad}  duruş=%{r['starv_pct']:6.2f} ±{r['starv_pct_ci95']:.2f}  "
                  f"WIP={r['ort_wip']:6.1f}  mesafe={r['toplam_mesafe_km']:5.1f} km  "
                  f"tur={r['tur_sayisi']:5.1f}  doluluk=%{r['doluluk_pct']:5.1f}  "
                  f"kart={int(r['toplam_kart'])}")
    df = pd.DataFrame(satir)

    print("\n  ── VAKA ÖZETİ: P3'ün P1'e göre göreli farkı ──")
    for s_ad, _ in senaryolar:
        a = df[(df["senaryo"] == s_ad) & (df["politika"] == "P3")].iloc[0]
        b = df[(df["senaryo"] == s_ad) & (df["politika"] == "P1")].iloc[0]
        print(f"     {s_ad:22s} duruş {a['starv_pct'] - b['starv_pct']:+6.2f} puan · "
              f"WIP %{100 * (a['ort_wip'] / b['ort_wip'] - 1):+5.1f} · "
              f"mesafe %{100 * (a['toplam_mesafe_km'] / b['toplam_mesafe_km'] - 1):+5.1f} · "
              f"tur %{100 * (a['tur_sayisi'] / b['tur_sayisi'] - 1):+5.1f}")
    return df


# ─────────────────────────────────────────────────────────────
def v2_dinamik_kanban(veri: V2Veri) -> pd.DataFrame:
    print("\n" + "═" * 78)
    print("V2 · KOŞU-İÇİ DİNAMİK KANBAN (Elloumi vd. 2025 s.613)")
    print("═" * 78)
    satir = []
    for talep_ad, carpan in [("Baz talep", 1.0), ("Talep şoku +%50", 1.5),
                             ("Talep düşüşü −%30", 0.7)]:
        for mod_ad, dinamik in [("Sabit N (senaryo bazlı)", False),
                                ("Dinamik N (koşu-içi)", True)]:
            p = V2Parametre(politika="P3", sevk="KONSOLIDASYON", arac_sayisi=3,
                            talep_modeli="SAATLIK_REJIM", talep_carpani=carpan,
                            dinamik_n=dinamik)
            r = _ort(veri, p)
            satir.append({"talep": talep_ad, "mod": mod_ad,
                          **{k: r[k] for k in ("starv_pct", "ort_wip", "toplam_kart",
                                               "n_degisim", "tur_sayisi",
                                               "toplam_mesafe_km")}})
        a, b = satir[-1], satir[-2]
        print(f"  {talep_ad:20s} sabit N: duruş=%{b['starv_pct']:5.2f} WIP={b['ort_wip']:6.1f} "
              f"kart={int(b['toplam_kart'])}  →  dinamik N: duruş=%{a['starv_pct']:5.2f} "
              f"WIP={a['ort_wip']:6.1f} kart={int(a['toplam_kart'])} "
              f"({a['n_degisim']:.0f} kart değişimi)")
    print("\n  Yorum: kart sayısı koşu içinde güncellendiğinde sistem talep kaymasına")
    print("  uyum sağlar; sabit N'de raf boyutu tasarım anındaki talebe kilitlidir.")
    return pd.DataFrame(satir)


# ─────────────────────────────────────────────────────────────
def v3_dinamiklik(veri: V2Veri) -> dict:
    print("\n" + "═" * 78)
    print("V3 · DİNAMİKLİK DERECESİ (Larsen vd. 2008, Bölüm 3.1)")
    print("═" * 78)
    p = V2Parametre(politika="P3", sevk="KONSOLIDASYON", arac_sayisi=3,
                    talep_modeli="SAATLIK_REJIM")
    r = _ort(veri, p)
    siparis = r["siparis"]
    print(f"  Vardiya başına sipariş (anlık istek) : {siparis:.1f}")
    print(f"  Önceden bilinen (advance) istek      : 0")
    print(f"  dod = n_imm / n_tot                  : 1,00")
    print("\n  Yorum: Tüm ikmal istekleri vardiya içinde, gerçek stok tükenmesiyle doğar;")
    print("  hiçbiri planlama ufkunun başında bilinmez. Problem, Larsen vd.'nin")
    print("  sınıflandırmasında **tam dinamik (dod = 1)** uçtadır. Bu, statik VRPTW")
    print("  çözücülerinin doğrudan uygulanamamasının gerekçesidir ve P1/P2 (dod = 0,")
    print("  takvim tabanlı) ile P3 arasındaki yapısal farkı tanımlar.")
    print("\n  ⚠️ Sınırlılık: dod = 1 uç değeri, üretim programının hiç kullanılmamasından")
    print("  kaynaklanır. production_plan.csv talep modeline bağlanırsa kısmen önceden")
    print("  bilinen istekler doğar ve dod < 1 olur (gelecek çalışma).")
    return {"dod": 1.0, "siparis": siparis}


# ─────────────────────────────────────────────────────────────
def v4_kpi(veri: V2Veri) -> pd.DataFrame:
    print("\n" + "═" * 78)
    print("V4 · LİTERATÜR KPI UYUMU (Sevim & Görkemli Aykut 2026 s.67, Denk. 5-9)")
    print("═" * 78)
    satir = []
    for ad, kw in [("P1 · sabit takt, sabit miktar", dict(politika="P1", tur_araligi_dk=60)),
                   ("P2 · sabit takt, Kanban miktarı", dict(politika="P2", tur_araligi_dk=60)),
                   ("P3 · dinamik, anında sevk", dict(politika="P3", sevk="ANINDA")),
                   ("P3 · dinamik, konsolidasyonlu", dict(politika="P3", sevk="KONSOLIDASYON"))]:
        p = V2Parametre(arac_sayisi=3, talep_modeli="SAATLIK_REJIM", **kw)
        r = _ort(veri, p)
        tur = max(r["tur_sayisi"], 1e-9)
        satir.append({
            "politika": ad,
            "ort_doluluk_pct": r["doluluk_pct"],                    # Denk. 5-6
            "ort_tur_mesafe_km": r["toplam_mesafe_km"] / tur,       # Denk. 8
            "ort_tur_sayisi": r["tur_sayisi"],                      # Denk. 7
            "ort_bekleme_dk_ist": r.get("ort_ikmal_sure_dk") or np.nan,  # Denk. 9 benzeri
            "starv_pct": r["starv_pct"],                            # Menanno 2023 s.16
            "ort_wip": r["ort_wip"],
            "arac_kullanim_pct": r["arac_kullanim_pct"],
            "ort_tur_sure_dk": r["ort_tur_sure_dk"],
        })
    df = pd.DataFrame(satir)
    print(f"  {'Politika':32s} {'Doluluk':>8s} {'km/tur':>8s} {'Tur':>6s} "
          f"{'İkmal dk':>9s} {'Duruş%':>7s} {'WIP':>7s}")
    for _, r in df.iterrows():
        ikmal = "—" if pd.isna(r["ort_bekleme_dk_ist"]) else f"{r['ort_bekleme_dk_ist']:9.1f}"
        print(f"  {r['politika']:32s} {r['ort_doluluk_pct']:7.1f}% "
              f"{r['ort_tur_mesafe_km']:8.3f} {r['ort_tur_sayisi']:6.1f} {ikmal} "
              f"{r['starv_pct']:7.2f} {r['ort_wip']:7.1f}")
    print("\n  Karşılaştırma değerleri (literatür):")
    print("    Doluluk  — Urru 2018 s.408: 0,85-0,89 · Sevim 2026 s.67: %69-81 · "
          "Simić 2020 s.12: 3,51/5 römork")
    print("    İkmal LT — Klenk 2012 s.12: e-Kanban 102-113 dk (20 kutu/tur) · "
          "Facchini 2022: hedef ≤25 dk")
    print("  ⚠️ Not: Bu çalışmada tur başına taşınan kutu sayısı literatürdekinden düşüktür")
    print("  (istasyon başına 1-3 kutu); doluluk oranları bu nedenle doğrudan kıyaslanamaz.")
    return df


def main():
    veri = V2Veri()
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    os.makedirs(cikti, exist_ok=True)

    v1_vaka(veri).to_csv(os.path.join(cikti, "v2_vaka_calismasi.csv"),
                         index=False, encoding="utf-8")
    v2_dinamik_kanban(veri).to_csv(os.path.join(cikti, "v2_dinamik_kanban.csv"),
                                   index=False, encoding="utf-8")
    v3_dinamiklik(veri)
    v4_kpi(veri).to_csv(os.path.join(cikti, "v2_kpi_uyumu.csv"),
                        index=False, encoding="utf-8")
    print("\n  CSV: data/synthetic/v2_vaka_calismasi.csv, v2_dinamik_kanban.csv, "
          "v2_kpi_uyumu.csv")


if __name__ == "__main__":
    main()
