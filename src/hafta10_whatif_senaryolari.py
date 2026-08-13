import os
import sys
import math
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.ekanban_signal import EKanbanSimulator
from src.vrptw_solver import VRPTWSolver
from src.hafta8_kanban_karsilastirma import hesapla_dinamik_wip_ve_starvation

class MockLoader(DataLoader):
    def __init__(self, c_df, s_df):
        super().__init__()
        self._c_df = c_df
        self._s_df = s_df
    
    def get_consumption(self):
        return self._c_df.copy()
    
    def get_stations(self):
        return self._s_df.copy()

def get_dist_matrix(loader):
    df = loader.get_distances()
    dist_matrix = {}
    for _, row in df.iterrows():
        dist_matrix[(str(row["from_node"]), str(row["to_node"]))] = float(row["mesafe_m"])
    return dist_matrix

def run_scenario(scenario, baz_c_df, baz_s_df, dist_matrix):
    c_df = baz_c_df.copy()
    s_df = baz_s_df.copy()

    if scenario["id"] == "TALEP_ART":
        c_df["tuketim_adet"] = c_df["tuketim_adet"] * 1.20
    elif scenario["id"] == "TALEP_DUS":
        c_df["tuketim_adet"] = c_df["tuketim_adet"] * 0.80
    elif scenario["id"] == "S16_KRIZ":
        c_df.loc[c_df["istasyon_id"] == "S16", "tuketim_adet"] *= 2.0
        s_df.loc[s_df["istasyon_id"] == "S16", "ort_tuketim_saat"] *= 2.0

    if scenario["mod"] == "Dinamik_N":
        # ROP = D_dk * LT * (1 + alpha)
        # N = ceil(ROP / C)
        lt = 45
        alpha = scenario["alpha"]
        for idx, row in s_df.iterrows():
            d_dk = row["ort_tuketim_saat"] / 60.0
            rop = d_dk * lt * (1 + alpha)
            n_yeni = math.ceil(rop / row["kutu_kapasitesi"])
            s_df.at[idx, "kanban_n"] = max(1, n_yeni) # En az 1

    # 1. E-Kanban Simülasyonu
    loader = MockLoader(c_df, s_df)
    sim = EKanbanSimulator(loader, alpha=scenario["alpha"])
    signals_df = sim.run()

    # 2. VRPTW Rotalama
    solver = VRPTWSolver(loader)
    solver.signals_df = signals_df # Ez
    # VRPTW loglamayı kapatmak için stdout'u yoksayabiliriz ama şimdilik kalsın
    rotalar_df, out_signals, starvations = solver.solve(
        arac_sayisi=scenario["arac"],
        dispatch_kural="EDD",
        consumption_df=c_df,
        hiz_carpani=scenario["hiz"]
    )

    # 3. Hesaplama (hafta 8 fonksiyonu ile)
    wip, st_tot, st_warm = hesapla_dinamik_wip_ve_starvation(out_signals, s_df, c_df)

    # Tur sayısı, mesafe
    tur_sayisi = rotalar_df["rota_id"].nunique() if len(rotalar_df) > 0 else 0
    toplam_mesafe_m = 0.0
    if len(rotalar_df) > 0:
        for rid, rgroup in rotalar_df.groupby("rota_id"):
            nodes = ["0"] + [str(r["istasyon_id"]).replace("S", "") for _, r in rgroup.iterrows()] + ["0"]
            for i in range(len(nodes)-1):
                toplam_mesafe_m += dist_matrix.get((nodes[i], nodes[i+1]), 100.0)

    toplam_mesafe_km = toplam_mesafe_m / 1000.0

    return {
        "Senaryo": scenario["name"],
        "Durus_dk": st_tot,
        "Starv_11520": (st_tot / 11520.0) * 100,
        "Starv_10440": (st_warm / 10440.0) * 100,
        "Ort_WIP": wip,
        "Mesafe_km": toplam_mesafe_km,
        "Tur_Sayisi": tur_sayisi
    }

def main():
    loader = DataLoader()
    baz_c_df = loader.get_consumption()
    baz_s_df = loader.get_stations()
    dist_matrix = get_dist_matrix(loader)

    print("=== BAZ REGRESYON TESTİ ===")
    baz_senaryo = {"id": "BAZ", "name": "Baz Senaryo", "alpha": 0.15, "arac": 4, "hiz": 1.0, "mod": "Sabit_N"}
    baz_sonuc = run_scenario(baz_senaryo, baz_c_df, baz_s_df, dist_matrix)
    
    beklenen_starv = 24.58
    beklenen_wip = 182.3
    gercek_starv = baz_sonuc["Starv_11520"]
    gercek_wip = baz_sonuc["Ort_WIP"]
    
    print(f"Beklenen: %{beklenen_starv:.2f} / {beklenen_wip:.1f} adet")
    print(f"Gerçekleşen: %{gercek_starv:.2f} / {gercek_wip:.1f} adet")
    
    # Tolerans
    if abs(gercek_starv - beklenen_starv) < 0.5 and abs(gercek_wip - beklenen_wip) < 1.0:
        print("SONUÇ: EŞLEŞME")
    else:
        print("SONUÇ: UYUMSUZLUK")
        print("DURDURULUYOR...")
        return
    
    scenarios = [
        baz_senaryo,
        {"id": "TALEP_ART", "name": "+20% Talep Şoku", "alpha": 0.15, "arac": 4, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "TALEP_DUS", "name": "-20% Talep Düşüşü", "alpha": 0.15, "arac": 4, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "FILO_4", "name": "Filo: 4 Araç", "alpha": 0.15, "arac": 4, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "FILO_3", "name": "Filo: 3 Araç", "alpha": 0.15, "arac": 3, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "FILO_2", "name": "Filo: 2 Araç", "alpha": 0.15, "arac": 2, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "FILO_1", "name": "Filo: 1 Araç", "alpha": 0.15, "arac": 1, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "HIZ_DUS", "name": "Hız Düşüşü", "alpha": 0.15, "arac": 4, "hiz": 10/6, "mod": "Sabit_N"},
        {"id": "ALPHA_05_A", "name": "Alpha 0.05 (Sabit N)", "alpha": 0.05, "arac": 4, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "ALPHA_30_A", "name": "Alpha 0.30 (Sabit N)", "alpha": 0.30, "arac": 4, "hiz": 1.0, "mod": "Sabit_N"},
        {"id": "ALPHA_05_B", "name": "Alpha 0.05 (Dinamik N)", "alpha": 0.05, "arac": 4, "hiz": 1.0, "mod": "Dinamik_N"},
        {"id": "ALPHA_15_B", "name": "Alpha 0.15 (Dinamik N)", "alpha": 0.15, "arac": 4, "hiz": 1.0, "mod": "Dinamik_N"},
        {"id": "ALPHA_30_B", "name": "Alpha 0.30 (Dinamik N)", "alpha": 0.30, "arac": 4, "hiz": 1.0, "mod": "Dinamik_N"},
        {"id": "S16_KRIZ", "name": "S16 Darboğaz Krizi", "alpha": 0.15, "arac": 4, "hiz": 1.0, "mod": "Sabit_N"},
    ]

    results = []
    print("\nSenaryolar çalıştırılıyor...")
    for sc in scenarios:
        if sc["id"] == "BAZ":
            res = baz_sonuc
        else:
            res = run_scenario(sc, baz_c_df, baz_s_df, dist_matrix)
        results.append(res)
    
    df_res = pd.DataFrame(results)
    out_dir = os.path.join(loader.base_dir, "data", "synthetic")
    os.makedirs(out_dir, exist_ok=True)
    df_res.to_csv(os.path.join(out_dir, "hafta10_whatif_sonuclari.csv"), index=False)
    
    print("\n=== SENARYO SONUÇLARI ===")
    print(df_res.to_string(index=False, float_format="%.2f"))

    print("\n=== BEKLENTİ MATRİSİ KARŞILAŞTIRMASI ===")
    
    baz = df_res[df_res["Senaryo"] == "Baz Senaryo"].iloc[0]
    
    # +20%
    t_art = df_res[df_res["Senaryo"] == "+20% Talep Şoku"].iloc[0]
    diff = t_art["Starv_11520"] - baz["Starv_11520"]
    durum = "UYARI" if (diff < 3 or diff > 20) else "UYGUN"
    print(f"[+20% Talep Şoku] Beklenti: Duruş +8-12 puan artmalı. Gerçekleşen Fark: {diff:.2f} -> {durum}")

    # -20%
    t_dus = df_res[df_res["Senaryo"] == "-20% Talep Düşüşü"].iloc[0]
    w_dus_arttimi = t_dus["Ort_WIP"] > baz["Ort_WIP"]
    s_dus_azaldimi = t_dus["Starv_11520"] < baz["Starv_11520"]
    durum2 = "HATA (İkisi aynı anda arttı)" if (w_dus_arttimi and not s_dus_azaldimi) else ("UYGUN" if s_dus_azaldimi else "UYARI")
    print(f"[-20% Talep Düşüşü] Beklenti: WIP artmalı, Starvation düşmeli. WIP artışı: {w_dus_arttimi}, Starv düşüşü: {s_dus_azaldimi} -> {durum2}")
    
    # Filo
    f4 = baz["Starv_11520"]  # Baz = 4 araç
    f3 = df_res[df_res["Senaryo"] == "Filo: 3 Araç"].iloc[0]["Starv_11520"]
    f2 = df_res[df_res["Senaryo"] == "Filo: 2 Araç"].iloc[0]["Starv_11520"]
    f1 = df_res[df_res["Senaryo"] == "Filo: 1 Araç"].iloc[0]["Starv_11520"]
    f_sirasi = f4 <= f3 <= f2 <= f1
    durum3 = "UYGUN" if f_sirasi else "HATA"
    print(f"[Filo Kademeli Düşüş] Beklenti: Starvation monoton artmalı. (4->3->2->1: {f4:.1f} -> {f3:.1f} -> {f2:.1f} -> {f1:.1f}) -> {durum3}")

    # Hız
    hiz = df_res[df_res["Senaryo"] == "Hız Düşüşü"].iloc[0]
    m_diff = abs(hiz["Mesafe_km"] - baz["Mesafe_km"])
    durum4 = "UYGUN" if m_diff < 0.1 else "HATA"
    print(f"[Hız Düşüşü] Beklenti: Mesafe DEĞİŞMEMELİ. Fark: {m_diff:.2f} km -> {durum4}")
    
    # Alpha Sabit N
    a05 = df_res[df_res["Senaryo"] == "Alpha 0.05 (Sabit N)"].iloc[0]["Starv_11520"]
    a15 = baz["Starv_11520"]
    a30 = df_res[df_res["Senaryo"] == "Alpha 0.30 (Sabit N)"].iloc[0]["Starv_11520"]
    a_sirasi = a30 <= a15 <= a05
    durum5 = "UYGUN" if a_sirasi else "HATA"
    print(f"[Alpha Duyarlılığı Sabit N] Beklenti: Starvation monoton azalmalı (0.05 > 0.15 > 0.30). ({a05:.1f} > {a15:.1f} > {a30:.1f}) -> {durum5}")
    
    # S16 Krizi
    s16 = df_res[df_res["Senaryo"] == "S16 Darboğaz Krizi"].iloc[0]
    s16_s = s16["Starv_11520"]
    diff_s16 = s16_s - baz["Starv_11520"]
    durum6 = "UYGUN" if diff_s16 > 0 and diff_s16 < 40 else "KAPSAM HATASI"
    print(f"[S16 Darboğaz Krizi] Beklenti: S16 ciddi etkilenmeli. Genel starvation farkı: {diff_s16:.2f} -> {durum6}")

if __name__ == "__main__":
    main()
