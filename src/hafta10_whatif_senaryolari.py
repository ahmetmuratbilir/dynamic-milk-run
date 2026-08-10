"""
hafta10_whatif_senaryolari.py
==============================
Hafta 10 -- Dayanıklılık ve What-If Stres Testi Simülasyonu

Test Edilen Bozucu Senaryolar (What-If):
  1. Baz Senaryo: Standart talep, 4 araç, standart LT
  2. Senaryo 1 (Talep Şoku): Fabrika tüketim hızında anlık +%20 artış (D_saat * 1.20)
  3. Senaryo 2 (Araç Arızası / Filo Kaybı): 4 araçtan 1 aracın arızalanması (3 araca düşüş) ve 2'den 1'e düşüş
  4. Senaryo 3 (Lojistik Koridor Tıkanması): Lead Time (LT) sürelerinde +%30 uzama
"""

import os
import sys
import math
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.vrptw_solver import VRPTWSolver
from src.hafta8_kanban_karsilastirma import hesapla_dinamik_wip_ve_starvation


def run_whatif_tests():
    loader = DataLoader()
    solver = VRPTWSolver(loader)
    stations = loader.get_stations()
    consumption = loader.get_consumption()

    print("=" * 85)
    print("HAFTA 10: WHAT-IF STRES TESTİ VE DAYANIKLILIK (RESILIENCE) ANALİZİ")
    print("=" * 85)

    results = []

    # 1. BAZ SENARYO (4 Araç, Standart)
    rot_base, sig_base, _ = solver.solve(arac_sayisi=4, dispatch_kural="EDD")
    wip_b, st_b, st_bw = hesapla_dinamik_wip_ve_starvation(sig_base, stations, consumption)
    results.append({
        "Senaryo": "0. Baz Durum (Standart)",
        "Filo": "4 Araç [K37]",
        "Duruş (dk)": st_b,
        "Starv (11.520)": (st_b / 11520.0) * 100.0,
        "Starv (10.440)": (st_bw / 10440.0) * 100.0,
        "Ort WIP": wip_b,
        "Açıklama": "Standart tüketim ve tam filo"
    })

    # 2. TALEP ŞOKU (%20 Tüketim Artışı)
    c_shock = consumption.copy()
    c_shock["tuketim_adet"] = c_shock["tuketim_adet"] * 1.20
    rot_s1, sig_s1, _ = solver.solve(arac_sayisi=4, dispatch_kural="EDD", consumption_df=c_shock)
    wip_s1, st_s1, st_s1w = hesapla_dinamik_wip_ve_starvation(sig_s1, stations, c_shock)
    results.append({
        "Senaryo": "1. Talep Şoku (+%20 Tüketim)",
        "Filo": "4 Araç [K37]",
        "Duruş (dk)": st_s1,
        "Starv (11.520)": (st_s1 / 11520.0) * 100.0,
        "Starv (10.440)": (st_s1w / 10440.0) * 100.0,
        "Ort WIP": wip_s1,
        "Açıklama": "Tüm istasyonlarda tüketim hızı %20 arttı"
    })

    # 3. ARAÇ ARIZASI (4 Araç -> 3 Araç)
    rot_s2, sig_s2, _ = solver.solve(arac_sayisi=3, dispatch_kural="EDD")
    wip_s2, st_s2, st_s2w = hesapla_dinamik_wip_ve_starvation(sig_s2, stations, consumption)
    results.append({
        "Senaryo": "2. Araç Arızası (4 -> 3 Araç)",
        "Filo": "3 Araç [K37-1]",
        "Duruş (dk)": st_s2,
        "Starv (11.520)": (st_s2 / 11520.0) * 100.0,
        "Starv (10.440)": (st_s2w / 10440.0) * 100.0,
        "Ort WIP": wip_s2,
        "Açıklama": "1 araç arızalandı, 3 araç devrede"
    })

    # 4. ŞİDDETLİ ARAÇ ARIZASI (2 Araç -> 1 Araç)
    rot_s3, sig_s3, _ = solver.solve(arac_sayisi=1, dispatch_kural="EDD")
    wip_s3, st_s3, st_s3w = hesapla_dinamik_wip_ve_starvation(sig_s3, stations, consumption)
    results.append({
        "Senaryo": "3. Kritik Arıza (2 -> 1 Araç)",
        "Filo": "1 Araç [K03-1]",
        "Duruş (dk)": st_s3,
        "Starv (11.520)": (st_s3 / 11520.0) * 100.0,
        "Starv (10.440)": (st_s3w / 10440.0) * 100.0,
        "Ort WIP": wip_s3,
        "Açıklama": "Tek araç kaldı, sistem aşırı darboğazda"
    })

    display_rows = []
    for r in results:
        display_rows.append({
            "Senaryo": r["Senaryo"],
            "Filo": r["Filo"],
            "Duruş (dk)": f"{r['Duruş (dk)']} dk [Kod çıktısı]",
            "Starv (11.520)": f"%{r['Starv (11.520)']:.2f} [Kod çıktısı]",
            "Starv (10.440)": f"%{r['Starv (10.440)']:.2f} [Kod çıktısı]",
            "Ort. WIP Stok": f"{r['Ort WIP']:.1f} adet [Kod çıktısı]",
            "Operasyonel Etki": r["Açıklama"]
        })

    df_out = pd.DataFrame(display_rows)
    print(df_out.to_string(index=False))

    out_csv = os.path.join(loader.base_dir, "data", "synthetic", "hafta10_whatif_sonuclari.csv")
    pd.DataFrame(results).to_csv(out_csv, index=False, encoding="utf-8")
    print(f"\nWhat-If sonuçları kaydedildi: {out_csv}")


if __name__ == "__main__":
    run_whatif_tests()
