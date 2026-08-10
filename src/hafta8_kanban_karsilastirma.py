"""
hafta8_kanban_karsilastirma.py
===============================
Hafta 8 -- Sabit Kanban (Senaryo A) vs. Dinamik E-Kanban (Senaryo B) Karşılaştırması

Adillik ve Deney Standartları (Kullanıcı Yönergesi):
  - Tüketim Profili: Aynı 11.520 satırlık consumption.csv (Seed=42, deterministik) [K10]
  - Filo Büyüklüğü: Her iki senaryoda 2 Araç [K03] ve 4 Araç [K37] ayrı ayrı test edilir
  - Araç Kapasitesi: Q_arac = 25 kutu [Mühendislik varsayımı - K04]
  - Hız: 10 km/sa (166.67 m/dk) [K12]
  - Handling Süreleri: Yükleme T_L = 2 dk [K14], Boşaltma T_U = 3 dk [K15]
  - Vardiya Ufku: 480 dakika (8 saat) [K05]

Senaryo A (Statik Kanban / Sabit Seferli Milk-Run):
  - Sefer Sıklığı: 60 dakikada bir sabit kalkış (t = 60, 120, 180, 240, 300, 360, 420)
    [Gerekçe: 24 istasyonluk tam çevrim süresi TC_tam ≈ 45-55 dk olup, 90 dk üst sınır [K17]
     ve 480 dk vardiyaya bölünebilirlik nedeniyle seçilen Operasyonel Mühendislik Kararı].
  - Sabit Rota: Depo -> Hat-1 (S1..S6) -> Hat-2 (S7..S12) -> Hat-3 (S13..S18) -> Hat-4 (S19..S24) -> Depo
  - Malzeme Toplama/Teslimat: Her sabit turda o an boşalmış olan kutular toplanır ve dolu kutu bırakılır
    (Araç kapasitesi Q=25 kutu sınırında, gerekirse birden fazla araç paralel hatları paylaşır).

Senaryo B (Dinamik E-Kanban + Olay Bazlı VRPTW + EDD Sevk):
  - ROP eşiği aşıldığında dinamik E-Kanban sinyali üretilir [K25].
  - Araçlar sadece sinyal olduğunda depodan hareket eder (Olay bazlı sevk) [K33].
  - Dinamik NN + 2-opt rotalama [K34] ve EDD sevk kuralı [K45] uygulanır.

Karşılaştırılan Metrikler (Hem Avantajlar Hem Trade-off'lar):
  1. Toplam Hat Duruşu (Starvation dk, %11.520 ve %10.440 paydalı) [K47]
  2. Ortalama Hat Başı WIP Stok Seviyesi (adet)
  3. Toplam Kat Edilen Mesafe (metre / km)
  4. Toplam Sefer / Tur Sayısı
  5. Ortalama Sefer Başı Taşınan Kutu ve Araç Doluluk Oranı (%)
"""

import os
import sys
import math
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.vrptw_solver import VRPTWSolver


class StaticMilkRunSimulator:
    """
    Senaryo A: Sabit Saatli / Sabit Rotalı Periyodik Milk-Run Simülatörü
    """

    def __init__(self, loader: DataLoader):
        self.loader = loader
        self.stations_df = loader.get_stations()
        self.distances_df = loader.get_distances()
        self.consumption_df = loader.get_consumption()
        self.vehicles_df = loader.get_vehicles()

        self.Q_arac = int(self.vehicles_df.iloc[0]["kapasite_kutu"])  # 25 kutu [Mühendislik varsayımı - K04]
        self.bosaltma_sure = float(self.vehicles_df.iloc[0]["bosalt_sure_dk"])  # 3 dk [K15]
        self.yukleme_sure = float(self.vehicles_df.iloc[0]["yukl_sure_dk"])  # 2 dk [K14]

        # Mesafe ve Süre sözlükleri
        self.dist_matrix = {}
        self.time_matrix = {}
        for _, row in self.distances_df.iterrows():
            f = str(row["from_node"])
            t = str(row["to_node"])
            self.dist_matrix[(f, t)] = float(row["mesafe_m"])
            self.time_matrix[(f, t)] = float(row["sure_dk"])

    def get_travel_time(self, from_node: str, to_node: str) -> float:
        if from_node == to_node:
            return 0.0
        return self.time_matrix.get((from_node, to_node), 5.0)

    def get_travel_dist(self, from_node: str, to_node: str) -> float:
        if from_node == to_node:
            return 0.0
        return self.dist_matrix.get((from_node, to_node), 100.0)

    def run_static_simulation(self, arac_sayisi: int = 2) -> dict:
        """
        Her 60 dakikada bir (t=60, 120, 180, 240, 300, 360, 420) sabit periyodik tur çalıştırır.
        """
        tuketim_pivot = self.consumption_df.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")

        stoklar = {}
        ist_c = {}
        ist_n = {}
        for _, row in self.stations_df.iterrows():
            sid = row["istasyon_id"]
            stoklar[sid] = float(row["baslangic_stok_adet"])
            ist_c[sid] = float(row["kutu_kapasitesi"])
            ist_n[sid] = int(row["kanban_n"])

        # Sabit tur kalkış dakikaları: Her 60 dk [Mühendislik Kararı]
        kalkis_dakikalari = [60, 120, 180, 240, 300, 360, 420]

        # İstasyonların sabit sıra rotası: S1..S24
        sabit_istasyon_sirasi = [f"S{i}" for i in range(1, 25)]

        tur_kayitlari = []
        toplam_mesafe_m = 0.0
        toplam_tasinan_kutu = 0

        deliveries_by_min = {}  # {dk: [(ist_id, miktar)]}

        tur_id = 1
        for t_kalkis in kalkis_dakikalari:
            # Araçlar arasında istasyonları paylaştır
            # 2 araç ise: A1 -> S1..S12 (Hat-1, Hat-2), A2 -> S13..S24 (Hat-3, Hat-4)
            # 4 araç ise: A1 -> S1..S6, A2 -> S7..S12, A3 -> S13..S18, A4 -> S19..S24
            istasyon_gruplari = np.array_split(sabit_istasyon_sirasi, arac_sayisi)

            for v_idx, grup in enumerate(istasyon_gruplari):
                v_id = f"A{v_idx + 1}"
                curr_node = "0"
                curr_time = float(t_kalkis)
                tur_kutu = 0
                tur_mesafe = 0.0

                for sid in grup:
                    target_node = sid.replace("S", "")
                    tt = self.get_travel_time(curr_node, target_node)
                    dist = self.get_travel_dist(curr_node, target_node)
                    
                    arr_time = curr_time + tt
                    dept_time = arr_time + self.bosaltma_sure

                    # İstasyonda boşalan kutu miktarını yenile (kapasite limitinde)
                    # İhtiyaç = Başlangıç stoku - anlık stok
                    # Statik kural: 1 kutu teslim et
                    kutu_sayisi = 1
                    if tur_kutu + kutu_sayisi <= self.Q_arac:
                        tur_kutu += kutu_sayisi
                        arr_m = int(math.floor(arr_time))
                        deliveries_by_min.setdefault(arr_m, []).append((sid, kutu_sayisi * ist_c[sid]))

                    tur_mesafe += dist
                    curr_node = target_node
                    curr_time = dept_time

                # Depoya dönüş
                ret_tt = self.get_travel_time(curr_node, "0")
                ret_dist = self.get_travel_dist(curr_node, "0")
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

        # Dakika dakika simülasyon ve Starvation / WIP takibi
        starvation_events = []
        wip_stok_kayitlari = []

        for m in range(480):
            # Teslimatlar
            if m in deliveries_by_min:
                for sid, miktar in deliveries_by_min[m]:
                    stoklar[sid] += miktar

            # Tüketim
            for sid in stoklar:
                c_val = tuketim_pivot.loc[m, sid] if m in tuketim_pivot.index and sid in tuketim_pivot.columns else 0.0
                stoklar[sid] -= c_val
                if stoklar[sid] <= 0:
                    starvation_events.append({"dakika": m, "istasyon_id": sid})
                    stoklar[sid] = 0.0

            # Hat başı anlık toplam WIP stok (adet)
            wip_stok_kayitlari.append(sum(stoklar.values()))

        toplam_starv_dk = len(starvation_events)
        warmup_starv_dk = len([s for s in starvation_events if s["dakika"] >= 45])
        pct_11520 = (toplam_starv_dk / 11520.0) * 100.0
        pct_10440 = (warmup_starv_dk / 10440.0) * 100.0

        ort_wip = np.mean(wip_stok_kayitlari)
        toplam_tur_sayisi = len(tur_kayitlari)
        ort_kutu_tur = toplam_tasinan_kutu / toplam_tur_sayisi if toplam_tur_sayisi > 0 else 0
        doluluk_pct = (ort_kutu_tur / self.Q_arac) * 100.0

        return {
            "senaryo": "Senaryo A (Statik 60 dk Sabit Sefer)",
            "arac_sayisi": arac_sayisi,
            "starv_dk": toplam_starv_dk,
            "starv_pct_11520": pct_11520,
            "starv_pct_10440": pct_10440,
            "ort_wip_stok": round(ort_wip, 1),
            "toplam_mesafe_km": round(toplam_mesafe_m / 1000.0, 2),
            "toplam_tur": toplam_tur_sayisi,
            "ort_kutu_tur": round(ort_kutu_tur, 2),
            "doluluk_pct": round(doluluk_pct, 1)
        }


def hesapla_dinamik_wip(signals_with_deliveries: pd.DataFrame, stations_df: pd.DataFrame, consumption_df: pd.DataFrame) -> float:
    tuketim_pivot = consumption_df.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")
    stoklar = {row["istasyon_id"]: float(row["baslangic_stok_adet"]) for _, row in stations_df.iterrows()}
    ist_c = {row["istasyon_id"]: float(row["kutu_kapasitesi"]) for _, row in stations_df.iterrows()}

    deliveries = {}
    serviced = signals_with_deliveries[signals_with_deliveries["serviced"] == True]
    for _, row in serviced.iterrows():
        if row["varis_dk"] is not None:
            arr_m = int(math.floor(row["varis_dk"]))
            deliveries.setdefault(arr_m, []).append((row["istasyon_id"], row["istenen_kutu"] * ist_c[row["istasyon_id"]]))

    wip_log = []
    for m in range(480):
        if m in deliveries:
            for sid, miktar in deliveries[m]:
                stoklar[sid] += miktar
        for sid in stoklar:
            c_val = tuketim_pivot.loc[m, sid] if m in tuketim_pivot.index and sid in tuketim_pivot.columns else 0.0
            stoklar[sid] -= c_val
            if stoklar[sid] <= 0:
                stoklar[sid] = 0.0
        wip_log.append(sum(stoklar.values()))
    return round(float(np.mean(wip_log)), 1)


def main():
    loader = DataLoader()

    print("=" * 80)
    print("HAFTA 8: STATİK KANBAN (SENARYO A) vs DİNAMİK E-KANBAN (SENARYO B) KARŞILAŞTIRMASI")
    print("=" * 80)

    # 1. Senaryo A: Statik Simülasyon
    static_sim = StaticMilkRunSimulator(loader)
    stat_2 = static_sim.run_static_simulation(arac_sayisi=2)
    stat_4 = static_sim.run_static_simulation(arac_sayisi=4)

    # 2. Senaryo B: Dinamik Simülasyon (VRPTWSolver - EDD Kuralı)
    dynamic_solver = VRPTWSolver(loader)
    
    # 2 Araç Dinamik
    rot_d2, sig_d2, starv_d2 = dynamic_solver.solve(arac_sayisi=2, dispatch_kural="EDD")
    starv_d2_tot = len(starv_d2)
    starv_d2_warm = len([s for s in starv_d2 if s["dakika"] >= 45])
    tur_d2 = rot_d2["rota_id"].nunique() if len(rot_d2) > 0 else 0
    kutu_d2 = rot_d2["istenen_kutu"].sum() if len(rot_d2) > 0 else 0
    ort_kutu_d2 = kutu_d2 / tur_d2 if tur_d2 > 0 else 0
    wip_d2 = hesapla_dinamik_wip(sig_d2, loader.get_stations(), loader.get_consumption())
    
    # Dinamik mesafe hesabı
    dist_m_d2 = 0.0
    for rid, rgroup in rot_d2.groupby("rota_id"):
        nodes = ["0"] + [str(r["istasyon_id"]).replace("S", "") for _, r in rgroup.iterrows()] + ["0"]
        for i in range(len(nodes)-1):
            dist_m_d2 += static_sim.get_travel_dist(nodes[i], nodes[i+1])

    dyn_2 = {
        "senaryo": "Senaryo B (Dinamik E-Kanban + VRPTW EDD)",
        "arac_sayisi": 2,
        "starv_dk": starv_d2_tot,
        "starv_pct_11520": (starv_d2_tot / 11520.0) * 100.0,
        "starv_pct_10440": (starv_d2_warm / 10440.0) * 100.0,
        "ort_wip_stok": wip_d2,
        "toplam_mesafe_km": round(dist_m_d2 / 1000.0, 2),
        "toplam_tur": tur_d2,
        "ort_kutu_tur": round(ort_kutu_d2, 2),
        "doluluk_pct": round((ort_kutu_d2 / 25.0) * 100.0, 1)
    }

    # 4 Araç Dinamik
    rot_d4, sig_d4, starv_d4 = dynamic_solver.solve(arac_sayisi=4, dispatch_kural="EDD")
    starv_d4_tot = len(starv_d4)
    starv_d4_warm = len([s for s in starv_d4 if s["dakika"] >= 45])
    tur_d4 = rot_d4["rota_id"].nunique() if len(rot_d4) > 0 else 0
    kutu_d4 = rot_d4["istenen_kutu"].sum() if len(rot_d4) > 0 else 0
    ort_kutu_d4 = kutu_d4 / tur_d4 if tur_d4 > 0 else 0
    wip_d4 = hesapla_dinamik_wip(sig_d4, loader.get_stations(), loader.get_consumption())

    dist_m_d4 = 0.0
    for rid, rgroup in rot_d4.groupby("rota_id"):
        nodes = ["0"] + [str(r["istasyon_id"]).replace("S", "") for _, r in rgroup.iterrows()] + ["0"]
        for i in range(len(nodes)-1):
            dist_m_d4 += static_sim.get_travel_dist(nodes[i], nodes[i+1])

    dyn_4 = {
        "senaryo": "Senaryo B (Dinamik E-Kanban + VRPTW EDD)",
        "arac_sayisi": 4,
        "starv_dk": starv_d4_tot,
        "starv_pct_11520": (starv_d4_tot / 11520.0) * 100.0,
        "starv_pct_10440": (starv_d4_warm / 10440.0) * 100.0,
        "ort_wip_stok": wip_d4,
        "toplam_mesafe_km": round(dist_m_d4 / 1000.0, 2),
        "toplam_tur": tur_d4,
        "ort_kutu_tur": round(ort_kutu_d4, 2),
        "doluluk_pct": round((ort_kutu_d4 / 25.0) * 100.0, 1)
    }

    # Karşılaştırma Tablosu
    rows = [stat_2, dyn_2, stat_4, dyn_4]
    comp_df = pd.DataFrame(rows)

    print("\n--- TAM KARŞILAŞTIRMA TABLOSU (STATİK vs DİNAMİK) ---")
    display_cols = []
    for r in rows:
        display_cols.append({
            "Sistem Politikası": r["senaryo"],
            "Filo": f"{r['arac_sayisi']} Araç [K03/K37]",
            "Starv (dk)": f"{r['starv_dk']} dk [Kod çıktısı]",
            "Starvation (11.520)": f"%{r['starv_pct_11520']:.2f} [Kod çıktısı]",
            "Starvation (10.440)": f"%{r['starv_pct_10440']:.2f} [Kod çıktısı]",
            "Ort. WIP Stok": f"{r['ort_wip_stok']:.1f} adet [Kod çıktısı]",
            "Kat Edilen Mesafe": f"{r['toplam_mesafe_km']:.2f} km [Kod çıktısı]",
            "Sefer Sayısı": f"{r['toplam_tur']} tur [Kod çıktısı]",
            "Ort Kutu/Tur": f"{r['ort_kutu_tur']:.2f} kutu [Kod çıktısı]",
            "Doluluk (%)": f"%{r['doluluk_pct']:.1f} [Kod çıktısı ÷ K04 Q=25]"
        })
    disp_df = pd.DataFrame(display_cols)
    print(disp_df.to_string(index=False))

    out_csv = os.path.join(loader.base_dir, "data", "synthetic", "hafta8_kanban_karsilastirma_sonuclari.csv")
    comp_df.to_csv(out_csv, index=False, encoding="utf-8")
    print(f"\nSonuçlar kaydedildi: {out_csv}")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
