"""
hafta6_duyarlilik_analizi.py
=============================
Hafta 6 — Araç Sayısı Duyarlılık Analizi (2 vs 3 vs 4 Araç)

Akademik Referanslar:
  - Sevim & Aykut (2026). "A dynamic in-plant milk-run system via agent-based 
    modelling". Pamukkale Üniv. Müh. Bil. Derg. 
    → 2 vs 3 araç faktöriyel deney, 3 araç önerisi (s.1001-1006)
  - Wang (2008). "GA for VRPTW with limited vehicles". 
    → m-VRPTW'de öncelik: max servis edilen istasyon sayısı (s.48-55)
  - Körösi & Duchoň (2026). Nature Scientific Reports, 16:16797.
    → Analitik filo formülü (s.3-4)

Uygulanan Kararlar:
  - K03 (2 araç) → 2, 3, 4 araç senaryoları test edilecek
  - K34: Nearest Neighbor + 2-opt sezgiseli korunuyor
  - K35: Hard TW + Toplam Süre Min amaç fonksiyonu korunuyor
  - K36: Darboğaz = Zaman/Filo kısıtı (doğrulama)

KPI'lar (ölçülecek metrikler):
  1. Starvation oranı (istasyon-dk, %) — H5 ile karşılaştırma
  2. Sinyal taksonomisi (zamanında / gecikmeli / karşılanamayan)
  3. Araç doluluk oranı (%)
  4. Karşılanma oranı (Wang 2008: servis edilen istasyon / toplam)
"""

import os
import sys
import math
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.vrptw_solver import VRPTWSolver


def run_scenario(solver: VRPTWSolver, arac_sayisi: int) -> dict:
    """Tek bir filo senaryosunu çalıştır ve KPI'ları döndür."""
    routes_df, signals_df, starvations = solver.solve(arac_sayisi=arac_sayisi)

    toplam_sinyal = len(signals_df)
    t_zamaninda = len(signals_df[signals_df["teslim_durumu"] == "ZAMANINDA_TESLİM"])
    t_gecikmeli = len(signals_df[signals_df["teslim_durumu"] == "GECİKMELİ_TESLİM"])
    t_karsilanamayan = len(signals_df[signals_df["teslim_durumu"] == "KARŞILANAMADI"])

    toplam_istasyon_dk = 24 * 480  # 11,520
    starvation_dk = len(starvations)
    starvation_pct = (starvation_dk / toplam_istasyon_dk) * 100

    # Tur ve doluluk metrikleri
    if len(routes_df) > 0:
        toplam_tur = routes_df["rota_id"].nunique()
        toplam_kutu = routes_df["istenen_kutu"].sum()
        ort_kutu_tur = toplam_kutu / toplam_tur if toplam_tur > 0 else 0
        doluluk_pct = (ort_kutu_tur / solver.Q_arac) * 100
    else:
        toplam_tur = 0
        toplam_kutu = 0
        ort_kutu_tur = 0
        doluluk_pct = 0

    # Wang (2008): Servis edilen istasyon sayısı
    servis_edilen = t_zamaninda + t_gecikmeli
    karsilama_orani = (servis_edilen / toplam_sinyal) * 100 if toplam_sinyal > 0 else 0

    return {
        "arac_sayisi": arac_sayisi,
        "toplam_sinyal": toplam_sinyal,
        "zamaninda_teslim": t_zamaninda,
        "gecikmeli_teslim": t_gecikmeli,
        "karsilanamayan": t_karsilanamayan,
        "karsilama_orani_pct": round(karsilama_orani, 2),
        "starvation_dk": starvation_dk,
        "starvation_pct": round(starvation_pct, 2),
        "toplam_tur": toplam_tur,
        "toplam_kutu": int(toplam_kutu),
        "ort_kutu_tur": round(ort_kutu_tur, 2),
        "doluluk_pct": round(doluluk_pct, 1),
        "routes_df": routes_df,
        "signals_df": signals_df,
        "starvations": starvations
    }


def main():
    loader = DataLoader()
    solver = VRPTWSolver(loader)

    print("=" * 75)
    print("HAFTA 6: ARAÇ SAYISI DUYARLILIK ANALİZİ (2 vs 3 vs 4 ARAÇ)")
    print("Referans: Sevim & Aykut (2026) — 2 vs 3 araç faktöriyel deney")
    print("          Wang (2008) — m-VRPTW servis edilen istasyon önceliği")
    print("=" * 75)

    senaryolar = [2, 3, 4]
    sonuclar = []

    for n in senaryolar:
        print(f"\n{'─' * 60}")
        print(f"SENARYO: {n} ARAÇ")
        print(f"{'─' * 60}")

        result = run_scenario(solver, n)
        sonuclar.append(result)

        print(f"  Sinyal Taksonomisi:")
        print(f"    Zamanında  : {result['zamaninda_teslim']:>3d} sinyal (%{result['zamaninda_teslim']/result['toplam_sinyal']*100:.1f})")
        print(f"    Gecikmeli  : {result['gecikmeli_teslim']:>3d} sinyal (%{result['gecikmeli_teslim']/result['toplam_sinyal']*100:.1f})")
        print(f"    Karşılana. : {result['karsilanamayan']:>3d} sinyal (%{result['karsilanamayan']/result['toplam_sinyal']*100:.1f})")
        print(f"  Karşılama Oranı (Wang 2008): %{result['karsilama_orani_pct']:.1f}")
        print(f"  Tur Sayısı / Kutu: {result['toplam_tur']} tur, {result['toplam_kutu']} kutu, ort {result['ort_kutu_tur']} kutu/tur")
        print(f"  Araç Doluluk: %{result['doluluk_pct']:.1f}")
        print(f"  🚨 Starvation: {result['starvation_dk']} ist-dk (%{result['starvation_pct']:.2f})")

    # ── Karşılaştırma Tablosu ──
    print(f"\n{'=' * 75}")
    print("KARŞILAŞTIRMA TABLOSU")
    print(f"{'=' * 75}")
    print(f"{'Metrik':<30} {'2 Araç':>12} {'3 Araç':>12} {'4 Araç':>12}")
    print("-" * 70)

    metrikler = [
        ("Zamanında Teslim", "zamaninda_teslim", "d"),
        ("Gecikmeli Teslim", "gecikmeli_teslim", "d"),
        ("Karşılanamayan", "karsilanamayan", "d"),
        ("Karşılama Oranı (%)", "karsilama_orani_pct", ".1f"),
        ("Starvation (ist-dk)", "starvation_dk", "d"),
        ("Starvation (%)", "starvation_pct", ".2f"),
        ("Toplam Tur", "toplam_tur", "d"),
        ("Araç Doluluk (%)", "doluluk_pct", ".1f"),
    ]

    for label, key, fmt in metrikler:
        vals = [s[key] for s in sonuclar]
        line = f"  {label:<28}"
        for v in vals:
            line += f" {v:>12{fmt}}"
        print(line)

    # ── Değişim Analizi ──
    s2 = sonuclar[0]
    s3 = sonuclar[1]
    s4 = sonuclar[2]

    print(f"\n── DEĞİŞİM ANALİZİ ──")
    if s2["starvation_pct"] > 0:
        delta_2_3 = s2["starvation_pct"] - s3["starvation_pct"]
        delta_2_4 = s2["starvation_pct"] - s4["starvation_pct"]
        print(f"  2→3 araç: Starvation {s2['starvation_pct']:.2f}% → {s3['starvation_pct']:.2f}% (Δ = {delta_2_3:.2f} puan düşüş)")
        print(f"  2→4 araç: Starvation {s2['starvation_pct']:.2f}% → {s4['starvation_pct']:.2f}% (Δ = {delta_2_4:.2f} puan düşüş)")
        
        if s3["starvation_pct"] < s2["starvation_pct"] * 0.5:
            print(f"  📊 3 araç ile starvation %50'den fazla düştü → Sevim & Aykut (2026) önerisiyle tutarlı")

    # ── CSV kaydet ──
    out_dir = os.path.join(loader.base_dir, "data", "synthetic")
    summary_data = [{
        "arac_sayisi": s["arac_sayisi"],
        "zamaninda_teslim": s["zamaninda_teslim"],
        "gecikmeli_teslim": s["gecikmeli_teslim"],
        "karsilanamayan": s["karsilanamayan"],
        "karsilama_orani_pct": s["karsilama_orani_pct"],
        "starvation_dk": s["starvation_dk"],
        "starvation_pct": s["starvation_pct"],
        "toplam_tur": s["toplam_tur"],
        "toplam_kutu": s["toplam_kutu"],
        "ort_kutu_tur": s["ort_kutu_tur"],
        "doluluk_pct": s["doluluk_pct"],
    } for s in sonuclar]

    pd.DataFrame(summary_data).to_csv(
        os.path.join(out_dir, "hafta6_duyarlilik_sonuclari.csv"),
        index=False, encoding="utf-8"
    )

    # Her senaryo için rotaları ayrı kaydet
    for s in sonuclar:
        s["routes_df"].to_csv(
            os.path.join(out_dir, f"rotalar_{s['arac_sayisi']}arac.csv"),
            index=False, encoding="utf-8"
        )

    print(f"\n  Sonuçlar kaydedildi:")
    print(f"    data/synthetic/hafta6_duyarlilik_sonuclari.csv")
    print(f"    data/synthetic/rotalar_2arac.csv")
    print(f"    data/synthetic/rotalar_3arac.csv")
    print(f"    data/synthetic/rotalar_4arac.csv")


if __name__ == "__main__":
    main()
