"""
stokastik_replikasyon.py
=========================
Hafta 7 -- Dispatch Stratejisi Karsilastirmasi: 30 Replikasyon Orkestratorü

Akademik Referanslar:
  - Wang (2008), GA for m-VRPTW, Sayfa 48-55
    -> EDD ve SLACK dispatch kurallarinin teorik dayanaği
  - Herrera-Vidal et al. (2026), Applied Sciences 16:1701, Sayfa 8-10
    -> 50 replikasyon ve 30 dk Welch warm-up onerisi
    -> K42: Biz 30 replikasyon kullaniyoruz (test ortami siniri)
    -> K43: Warm-up = 45 dk (K32 karari korundu, Welch 30 dk'ya gore muhafazakar)
  - Herrera-Vidal (2026) Sayfa 8: FIFO kuyruk disiplini baseline
  - K26 (mevcut baseline): kritiklik_skoru + tw_bitis sirasi

Uygulanan Kararlar:
  - K26: KRITIKLIK kurali (mevcut baseline, ROP/stok orani)
  - K33: Olay bazli sevk (event-based dispatch)
  - K42: 30 replikasyon (Herrera-Vidal 50 onerisi, biz test ortami icin 30)
  - K43: Warm-up = 45 dk (K32 korundu)
  - K44: Test edilen 4 dispatch kurali: KRITIKLIK, EDD, SLACK, FIFO

Stokastiklik Kaynaği:
  - Mevcut consumption.csv seed=42 ile deterministik (generate_synthetic_data.py L16)
  - Her replikasyonda: farkli random seed ile N(mu/60, sigma/60) tuketim yeniden uretiliyor
  - Sinyal verisi (ekanban_signals.csv) degismez -- dispatch stratejisi sinyalleri
    seciyor ama sinyallerin kendisi sabit (K04, K06-K11 dogrulanmis parametreler)

Calistirilacak Kombinasyonlar:
  30 replikasyon x 4 dispatch kurali x 2 arac sayisi (2, 4) = 240 simulasyon
  Neden 2 ve 4 arac?
    - 2 arac: H5 baseline dogrulamasi (%52.08 starvation bekleniyor +/- stokastik varyans)
    - 4 arac: H6 optimal analitik sonucu (Korosi AN_final=4)
"""

import os
import sys
import math
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.vrptw_solver import VRPTWSolver


# ─── Parametreler ────────────────────────────────────────────────────────────
N_REPLIKASYON = 30        # K42: 30 rep (Herrera-Vidal 2026 s.10 -- 50 onerir, biz 30)
WARM_UP_DK    = 45        # K43: 45 dk warm-up (K32 korundu, Welch 30 dk'ya gore muhafazakar)
SIM_SURE      = 480       # Vardiya suresi (K05)
ARAC_SAYILARI = [2, 4]    # 2: H5 baseline, 4: Korosi AN_final (K37)
DISPATCH_KURALLARI = ["KRITIKLIK", "EDD", "SLACK", "FIFO"]  # K44

# Istasyon tuketim parametreleri (generate_synthetic_data.py'den alinmistir, K09-K10)
# mu_saat: Her istasyonun ortalama saatlik tuketimi (onaylanan degerler, referans_veri.md)
# sigma = 0.20 * mu (K10: CV=0.20)
ISTASYON_TUKETIM_MU = {
    "S1":  20, "S2":  20, "S3":  15, "S4":  20, "S5":  15, "S6":  20,
    "S7":  18, "S8":  16, "S9":  20, "S10": 18, "S11": 20, "S12": 15,
    "S13": 24, "S14": 20, "S15": 18, "S16": 24, "S17": 20, "S18": 16,
    "S19": 20, "S20": 18, "S21": 15, "S22": 20, "S23": 18, "S24": 16,
}


def uret_stokastik_tuketim(seed: int, sim_sure: int = SIM_SURE) -> pd.DataFrame:
    """
    Verilen seed ile stokastik tuketim tablosu uretir.
    Dagilis: N(mu/60, sigma/60), negatif degerler 0'a clip edilir.
    Kaynak: K10 (CV=0.20), generate_synthetic_data.py L109-L115
    """
    rng = np.random.default_rng(seed)
    kayitlar = []
    for dakika in range(sim_sure):
        for istasyon_id, mu_saat in ISTASYON_TUKETIM_MU.items():
            mu_dk    = mu_saat / 60.0
            sigma_dk = 0.20 * mu_dk  # K10: CV=0.20
            tuketim  = max(0.0, rng.normal(mu_dk, sigma_dk))
            kayitlar.append({
                "dakika":       dakika,
                "istasyon_id":  istasyon_id,
                "tuketim_adet": round(tuketim, 4),
            })
    return pd.DataFrame(kayitlar)


def run_single(solver: VRPTWSolver, arac_sayisi: int,
               dispatch_kural: str, consumption_df: pd.DataFrame) -> dict:
    """Tek bir (arac, kural, replikasyon) kombinasyonunu calistir."""
    routes_df, signals_df, starvations = solver.solve(
        arac_sayisi=arac_sayisi,
        dispatch_kural=dispatch_kural,
        consumption_df=consumption_df
    )
    toplam_sinyal = len(signals_df)
    zamaninda  = len(signals_df[signals_df["teslim_durumu"] == "ZAMANINDA_TESLİM"])
    gecikmeli  = len(signals_df[signals_df["teslim_durumu"] == "GECİKMELİ_TESLİM"])
    karsila    = len(signals_df[signals_df["teslim_durumu"] == "KARŞILANAMADI"])

    # Warm-up (K43: 45 dk) sonrasindaki starvation'lari say
    # Herrera-Vidal (2026) s.10: gecici hal etkilerini elemek icin
    starvation_warmup_sonrasi = [
        s for s in starvations if s["dakika"] >= WARM_UP_DK
    ]

    toplam_ist_dk = len(ISTASYON_TUKETIM_MU) * (SIM_SURE - WARM_UP_DK)
    starv_dk  = len(starvation_warmup_sonrasi)
    starv_pct = (starv_dk / toplam_ist_dk) * 100 if toplam_ist_dk > 0 else 0

    toplam_tur  = routes_df["rota_id"].nunique() if len(routes_df) > 0 else 0
    toplam_kutu = routes_df["istenen_kutu"].sum() if len(routes_df) > 0 else 0
    ort_kutu    = toplam_kutu / toplam_tur if toplam_tur > 0 else 0
    doluluk_pct = (ort_kutu / solver.Q_arac) * 100

    return {
        "arac_sayisi":    arac_sayisi,
        "dispatch_kural": dispatch_kural,
        "zamaninda":      zamaninda,
        "gecikmeli":      gecikmeli,
        "karsilanamayan": karsila,
        "karsilama_pct":  round((zamaninda + gecikmeli) / toplam_sinyal * 100, 2),
        "starvation_dk":  starv_dk,
        "starvation_pct": round(starv_pct, 4),
        "toplam_tur":     toplam_tur,
        "ort_kutu_tur":   round(ort_kutu, 2),
        "doluluk_pct":    round(doluluk_pct, 1),
    }


def main():
    loader = DataLoader()
    solver = VRPTWSolver(loader)

    print("=" * 70)
    print("HAFTA 7: DISPATCH STRATEJISI KARSILASTIRMASI -- STOKASTIK REPLIKASYON")
    print(f"  Replikasyon sayisi : {N_REPLIKASYON}  (K42 -- Herrera-Vidal 2026 s.10)")
    print(f"  Warm-up            : {WARM_UP_DK} dk  (K43 -- K32 korundu)")
    print(f"  Arac sayilari      : {ARAC_SAYILARI}")
    print(f"  Dispatch kurallari : {DISPATCH_KURALLARI}")
    print(f"  Toplam simulasyon  : {N_REPLIKASYON * len(DISPATCH_KURALLARI) * len(ARAC_SAYILARI)}")
    print("=" * 70)

    sonuclar = []
    toplam = N_REPLIKASYON * len(DISPATCH_KURALLARI) * len(ARAC_SAYILARI)
    sayac = 0

    for rep in range(N_REPLIKASYON):
        seed = 100 + rep  # Seed 100'den basla (42 deterministik baseline'dan ayri)
        consumption_df = uret_stokastik_tuketim(seed=seed)

        for arac in ARAC_SAYILARI:
            for kural in DISPATCH_KURALLARI:
                sayac += 1
                if sayac % 20 == 0 or sayac == toplam:
                    print(f"  [{sayac}/{toplam}] Rep={rep+1}, Arac={arac}, Kural={kural}")

                sonuc = run_single(solver, arac, kural, consumption_df)
                sonuc["replikasyon"] = rep + 1
                sonuc["seed"]        = seed
                sonuclar.append(sonuc)

    df = pd.DataFrame(sonuclar)

    # Kaydet
    out_dir = os.path.join(loader.base_dir, "data", "synthetic")
    out_path = os.path.join(out_dir, "hafta7_replikasyon_sonuclari.csv")
    df.to_csv(out_path, index=False, encoding="utf-8")

    print(f"\n  {len(df)} satir kaydedildi: data/synthetic/hafta7_replikasyon_sonuclari.csv")

    # Hizli ozet
    print("\n--- HIZLI OZET (mean starvation_pct) ---")
    ozet = df.groupby(["arac_sayisi", "dispatch_kural"])["starvation_pct"].agg(["mean", "std"])
    ozet["ci95"] = 1.96 * ozet["std"] / np.sqrt(N_REPLIKASYON)
    ozet = ozet.round(3)
    print(ozet.to_string())


if __name__ == "__main__":
    main()
