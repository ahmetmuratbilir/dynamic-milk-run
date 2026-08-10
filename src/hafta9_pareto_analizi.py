"""
hafta9_pareto_analizi.py
========================
Hafta 9 -- Eşit WIP ve Eşit Duruş Seviyesinde Pareto Sınırı (Trade-off) Analizi

Amaç:
  - Statik sistem ile Dinamik sistemi sadece 'aynı araç sayısında' değil, 'aynı WIP seviyesinde'
    ve 'farklı tur sıklıklarında' karşılaştırarak gerçek Pareto sınırını çıkarmak.
  - Statik sistem tur periyodunu 60 dk, 80 dk, 90 dk, 120 dk yaparak WIP'i dinamik sistem seviyesine (~110-180 adet)
    düşürmek ve o noktada starvation'ı ölçmek.
"""

import os
import sys
import math
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.hafta8_kanban_karsilastirma import StaticMilkRunSimulator, hesapla_dinamik_wip_ve_starvation
from src.vrptw_solver import VRPTWSolver


class ParetoAnalyzer:

    def __init__(self, loader: DataLoader):
        self.loader = loader
        self.static_sim = StaticMilkRunSimulator(loader)
        self.dynamic_solver = VRPTWSolver(loader)
        self.stations_df = loader.get_stations()
        self.consumption_df = loader.get_consumption()

    def run_static_with_frequency(self, periyot_dk: int, arac_sayisi: int = 2) -> dict:
        """
        Farklı periyotlarla (örn. 60, 80, 90, 120 dk) statik milk-run çalıştırır.
        """
        tuketim_pivot = self.consumption_df.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")
        stoklar = {row["istasyon_id"]: float(row["baslangic_stok_adet"]) for _, row in self.stations_df.iterrows()}
        ist_cap = {row["istasyon_id"]: float(row["kanban_n"] * row["kutu_kapasitesi"]) for _, row in self.stations_df.iterrows()}
        ist_c = {row["istasyon_id"]: float(row["kutu_kapasitesi"]) for _, row in self.stations_df.iterrows()}

        kalkis_dakikalari = list(range(periyot_dk, 480, periyot_dk))
        sabit_istasyon_sirasi = [f"S{i}" for i in range(1, 25)]

        tur_kayitlari = []
        toplam_mesafe_m = 0.0
        toplam_tasinan_kutu = 0
        deliveries_by_min = {}

        tur_id = 1
        for t_kalkis in kalkis_dakikalari:
            istasyon_gruplari = np.array_split(sabit_istasyon_sirasi, arac_sayisi)

            for v_idx, grup in enumerate(istasyon_gruplari):
                v_id = f"A{v_idx + 1}"
                curr_node = "0"
                curr_time = float(t_kalkis)
                tur_kutu = 0
                tur_mesafe = 0.0

                for sid in grup:
                    target_node = sid.replace("S", "")
                    tt = self.static_sim.get_travel_time(curr_node, target_node)
                    dist = self.static_sim.get_travel_dist(curr_node, target_node)
                    
                    arr_time = curr_time + tt
                    dept_time = arr_time + self.static_sim.bosaltma_sure

                    kutu_sayisi = 1
                    if tur_kutu + kutu_sayisi <= self.static_sim.Q_arac:
                        tur_kutu += kutu_sayisi
                        arr_m = int(math.floor(arr_time))
                        deliveries_by_min.setdefault(arr_m, []).append((sid, kutu_sayisi * ist_c[sid]))

                    tur_mesafe += dist
                    curr_node = target_node
                    curr_time = dept_time

                ret_tt = self.static_sim.get_travel_time(curr_node, "0")
                ret_dist = self.static_sim.get_travel_dist(curr_node, "0")
                tur_mesafe += ret_dist
                toplam_mesafe_m += tur_mesafe
                toplam_tasinan_kutu += tur_kutu

                tur_kayitlari.append({
                    "tur_id": f"STAT_T{tur_id:03d}",
                    "arac_id": v_id,
                    "kalkis_dk": t_kalkis,
                    "bitis_dk": round(curr_time + ret_tt, 2),
                    "tasinan_kutu": tur_kutu,
                    "mesafe_m": tur_mesafe
                })
                tur_id += 1

        starvation_events = []
        wip_stok_kayitlari = []

        for m in range(480):
            if m in deliveries_by_min:
                for sid, miktar in deliveries_by_min[m]:
                    stoklar[sid] = min(ist_cap[sid], stoklar[sid] + miktar)

            for sid in stoklar:
                c_val = tuketim_pivot.loc[m, sid] if m in tuketim_pivot.index and sid in tuketim_pivot.columns else 0.0
                stoklar[sid] -= c_val
                if stoklar[sid] <= 0:
                    starvation_events.append({"dakika": m, "istasyon_id": sid})
                    stoklar[sid] = 0.0

            wip_stok_kayitlari.append(sum(stoklar.values()))

        toplam_starv_dk = len(starvation_events)
        warmup_starv_dk = len([s for s in starvation_events if s["dakika"] >= 45])
        pct_11520 = (toplam_starv_dk / 11520.0) * 100.0
        pct_10440 = (warmup_starv_dk / 10440.0) * 100.0
        ort_wip = np.mean(wip_stok_kayitlari)
        toplam_tur = len(tur_kayitlari)

        return {
            "politika": f"Statik ({periyot_dk} dk Sefer)",
            "arac_sayisi": arac_sayisi,
            "starv_dk": toplam_starv_dk,
            "starv_pct_11520": pct_11520,
            "starv_pct_10440": pct_10440,
            "ort_wip": round(ort_wip, 1),
            "mesafe_km": round(toplam_mesafe_m / 1000.0, 2),
            "toplam_tur": toplam_tur
        }


def main():
    loader = DataLoader()
    analyzer = ParetoAnalyzer(loader)

    print("=" * 90)
    print("HAFTA 9: PARETO VE EŞİT WIP SEVİYESİ KARŞILAŞTIRMA ANALİZİ")
    print("=" * 90)

    results = []

    # 1. Statik Sistem Farklı Frekanslar (2 Araç)
    for p in [45, 60, 80, 90, 120]:
        res = analyzer.run_static_with_frequency(periyot_dk=p, arac_sayisi=2)
        results.append(res)

    # 2. Dinamik Sistem (2 Araç - EDD)
    rot_d2, sig_d2, _ = analyzer.dynamic_solver.solve(arac_sayisi=2, dispatch_kural="EDD")
    wip_d2, starv_d2, starv_d2_w = hesapla_dinamik_wip_ve_starvation(sig_d2, loader.get_stations(), loader.get_consumption())
    
    # Mesafe hesabı
    dist_m_d2 = 0.0
    for rid, rgroup in rot_d2.groupby("rota_id"):
        nodes = ["0"] + [str(r["istasyon_id"]).replace("S", "") for _, r in rgroup.iterrows()] + ["0"]
        for i in range(len(nodes)-1):
            dist_m_d2 += analyzer.static_sim.get_travel_dist(nodes[i], nodes[i+1])

    results.append({
        "politika": "Dinamik E-Kanban (Olay Bazlı EDD)",
        "arac_sayisi": 2,
        "starv_dk": starv_d2,
        "starv_pct_11520": (starv_d2 / 11520.0) * 100.0,
        "starv_pct_10440": (starv_d2_w / 10440.0) * 100.0,
        "ort_wip": wip_d2,
        "mesafe_km": round(dist_m_d2 / 1000.0, 2),
        "toplam_tur": rot_d2["rota_id"].nunique()
    })

    # 3. Statik Sistem Farklı Frekanslar (4 Araç)
    for p in [45, 60, 80, 90, 120]:
        res = analyzer.run_static_with_frequency(periyot_dk=p, arac_sayisi=4)
        results.append(res)

    # 4. Dinamik Sistem (4 Araç - EDD)
    rot_d4, sig_d4, _ = analyzer.dynamic_solver.solve(arac_sayisi=4, dispatch_kural="EDD")
    wip_d4, starv_d4, starv_d4_w = hesapla_dinamik_wip_ve_starvation(sig_d4, loader.get_stations(), loader.get_consumption())
    
    dist_m_d4 = 0.0
    for rid, rgroup in rot_d4.groupby("rota_id"):
        nodes = ["0"] + [str(r["istasyon_id"]).replace("S", "") for _, r in rgroup.iterrows()] + ["0"]
        for i in range(len(nodes)-1):
            dist_m_d4 += analyzer.static_sim.get_travel_dist(nodes[i], nodes[i+1])

    results.append({
        "politika": "Dinamik E-Kanban (Olay Bazlı EDD)",
        "arac_sayisi": 4,
        "starv_dk": starv_d4,
        "starv_pct_11520": (starv_d4 / 11520.0) * 100.0,
        "starv_pct_10440": (starv_d4_w / 10440.0) * 100.0,
        "ort_wip": wip_d4,
        "mesafe_km": round(dist_m_d4 / 1000.0, 2),
        "toplam_tur": rot_d4["rota_id"].nunique()
    })

    # Tablo formatlama
    display_rows = []
    for r in results:
        display_rows.append({
            "Sistem Politikası": r["politika"],
            "Filo": f"{r['arac_sayisi']} Araç [K03/K37]",
            "Duruş (dk)": f"{r['starv_dk']} dk [Kod çıktısı]",
            "Starv (11.520)": f"%{r['starv_pct_11520']:.2f} [Kod çıktısı]",
            "Starv (10.440)": f"%{r['starv_pct_10440']:.2f} [Kod çıktısı]",
            "Ort. WIP Stok": f"{r['ort_wip']:.1f} adet [Kod çıktısı]",
            "Toplam Mesafe": f"{r['mesafe_km']:.2f} km [Kod çıktısı]",
            "Sefer": f"{r['toplam_tur']} tur [Kod çıktısı]"
        })

    df_pareto = pd.DataFrame(display_rows)
    print(df_pareto.to_string(index=False))

    out_path = os.path.join(loader.base_dir, "data", "synthetic", "hafta9_pareto_sonuclari.csv")
    pd.DataFrame(results).to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nPareto sonuçları kaydedildi: {out_path}")


if __name__ == "__main__":
    main()
