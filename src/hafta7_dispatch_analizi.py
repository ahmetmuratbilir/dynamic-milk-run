"""
hafta7_dispatch_analizi.py
===========================
Hafta 7 -- 30 Replikasyon Sonuclarinin Istatistiksel Analizi

Kaynak: Herrera-Vidal et al. (2026), Applied Sciences 16:1701, Sayfa 10
  -> %95 guven araligi ile replikasyon karsilastirmasi
  -> Welch t-testi (esit varyans varsayimi olmaksizin)

Yapilan Analizler:
  1. Her (dispatch_kural, arac_sayisi) kombinasyonu icin: mean +/- %95 CI
  2. Welch t-testi: KRITIKLIK vs en iyi alternatif -- fark anlamli mi?
  3. Karsilastirma tablosu: hangi kural hangi arac sayisiyla en iyi?
  4. "4 arac + en iyi dispatch" vs "5 arac + KRITIKLIK" karsilastirmasi
     (H6 verisinden: 5 arac = %5.20 -- bu eşiği geçebilir miyiz?)
"""

import os
import sys
import math
import numpy as np
import pandas as pd
from scipy import stats

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader

N_REPLIKASYON = 30  # K42

def welch_t_test(grup1: np.ndarray, grup2: np.ndarray) -> dict:
    """Welch t-testi (esit varyans varsayimi yok, Herrera-Vidal 2026 s.10)"""
    t_stat, p_val = stats.ttest_ind(grup1, grup2, equal_var=False)
    n1, n2 = len(grup1), len(grup2)
    se = math.sqrt(grup1.std()**2/n1 + grup2.std()**2/n2)
    return {
        "t_stat":  round(t_stat, 4),
        "p_value": round(p_val, 6),
        "anlamli": p_val < 0.05,
        "etki_yonu": "grup1 daha iyi" if grup1.mean() < grup2.mean() else "grup2 daha iyi",
    }


def ci95(arr: np.ndarray) -> float:
    """Herrera-Vidal (2026) s.10: %95 guven araligi yari genisligi"""
    return 1.96 * arr.std() / math.sqrt(len(arr))


def main():
    loader = DataLoader()
    csv_path = os.path.join(loader.base_dir, "data", "synthetic",
                            "hafta7_replikasyon_sonuclari.csv")
    if not os.path.exists(csv_path):
        print("HATA: Once stokastik_replikasyon.py calistirin!")
        sys.exit(1)

    df = pd.read_csv(csv_path)
    print("=" * 70)
    print("HAFTA 7: DISPATCH STRATEJISI ISTATISTIKSEL ANALIZI")
    print(f"  Replikasyon: {N_REPLIKASYON}, Veri: {len(df)} satir")
    print("=" * 70)

    # ── 1. Ozet Tablo: mean +/- 95CI ─────────────────────────────────────────
    print("\n--- 1. OZET TABLO: Starvation (%) mean +/- %95 CI ---")
    print(f"{'Arac':<6} {'Kural':<12} {'Mean%':>7} {'Std':>7} {'CI95':>7} {'Min%':>7} {'Max%':>7}")
    print("-" * 55)

    ozet_kayitlar = []
    for arac in sorted(df["arac_sayisi"].unique()):
        for kural in ["KRITIKLIK", "EDD", "SLACK", "FIFO"]:
            alt = df[(df["arac_sayisi"] == arac) & (df["dispatch_kural"] == kural)]["starvation_pct"]
            m   = alt.mean()
            s   = alt.std()
            ci  = ci95(alt.values)
            print(f"{arac:<6} {kural:<12} {m:>7.3f} {s:>7.3f} {ci:>7.3f} {alt.min():>7.3f} {alt.max():>7.3f}")
            ozet_kayitlar.append({
                "arac_sayisi": arac, "dispatch_kural": kural,
                "mean_starv":  round(m, 4),
                "std_starv":   round(s, 4),
                "ci95_starv":  round(ci, 4),
                "min_starv":   round(alt.min(), 4),
                "max_starv":   round(alt.max(), 4),
            })

    # ── 2. Welch t-testi: KRITIKLIK vs digerler (4 arac) ─────────────────────
    print("\n--- 2. WELCH T-TEST: KRITIKLIK vs Alternatif (4 Arac) ---")
    baseline = df[(df["arac_sayisi"] == 4) & (df["dispatch_kural"] == "KRITIKLIK")]["starvation_pct"].values
    print(f"  KRITIKLIK baseline: mean={baseline.mean():.3f}% +/- {ci95(baseline):.3f}")

    for kural in ["EDD", "SLACK", "FIFO"]:
        alt = df[(df["arac_sayisi"] == 4) & (df["dispatch_kural"] == kural)]["starvation_pct"].values
        res = welch_t_test(alt, baseline)
        yildiz = "**" if res["p_value"] < 0.01 else ("*" if res["anlamli"] else "  ")
        fark = alt.mean() - baseline.mean()
        print(f"  {kural} vs KRITIKLIK: mean={alt.mean():.3f}%, delta={fark:+.3f}%, "
              f"p={res['p_value']:.4f} {yildiz} -> {'Anlamli' if res['anlamli'] else 'Anlamli degil'}")

    # ── 3. En iyi dispatch kurali ─────────────────────────────────────────────
    print("\n--- 3. EN IYI DISPATCH KURALI (4 Arac) ---")
    en_iyi = None
    en_iyi_mean = float("inf")
    for kural in ["KRITIKLIK", "EDD", "SLACK", "FIFO"]:
        m = df[(df["arac_sayisi"] == 4) & (df["dispatch_kural"] == kural)]["starvation_pct"].mean()
        if m < en_iyi_mean:
            en_iyi_mean = m
            en_iyi = kural
    print(f"  En iyi kural: {en_iyi} (mean starvation = {en_iyi_mean:.3f}%)")

    # ── 4. "4 arac + en iyi kural" vs H6 referanslari ────────────────────────
    print("\n--- 4. DISPATCH OPTIMIZASYONU vs FILO ARTIRIMI (H6 Referans) ---")
    h6_ref = {
        "4 arac KRITIKLIK (H6 deterministik)": 19.46,
        "5 arac KRITIKLIK (H6 deterministik)": 5.20,
        "6 arac KRITIKLIK (H6 deterministik)": 0.97,
    }
    en_iyi_mean_4 = df[(df["arac_sayisi"] == 4) & (df["dispatch_kural"] == en_iyi)]["starvation_pct"].mean()
    print(f"  4 arac + {en_iyi} dispatch (30 rep mean): %{en_iyi_mean_4:.3f}")
    for etiket, deger in h6_ref.items():
        fark = en_iyi_mean_4 - deger
        print(f"  {etiket}: %{deger:.2f}  (fark: {fark:+.2f} puan)")

    # Kaydet
    ozet_df = pd.DataFrame(ozet_kayitlar)
    out_path = os.path.join(loader.base_dir, "data", "synthetic",
                            "hafta7_dispatch_ozet.csv")
    ozet_df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\n  Ozet kaydedildi: data/synthetic/hafta7_dispatch_ozet.csv")
    print("\n  * p<0.05  ** p<0.01  (Welch t-testi, Herrera-Vidal 2026 s.10)")


if __name__ == "__main__":
    main()
