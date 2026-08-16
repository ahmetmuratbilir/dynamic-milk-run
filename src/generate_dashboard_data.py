"""
generate_dashboard_data.py
===========================
Dashboard için tüm Ne-Olursa-Ne-Olur (What-If) senaryo kombinasyonlarını 
çevrimdışı (offline) olarak Multiprocessing ile hesaplar ve 
data/dashboard_scenarios.json dosyasına kaydeder.
"""

import os
import sys
import math
import time
import json
import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader
from src.ekanban_signal import EKanbanSimulator
from src.vrptw_solver import VRPTWSolver
from src.hafta8_kanban_karsilastirma import hesapla_dinamik_wip_ve_starvation

class MockLoader:
    def __init__(self, c_df, s_df):
        self.c_df = c_df
        self.s_df = s_df
        self.base_loader = DataLoader()
        self.base_dir = self.base_loader.base_dir
    def get_consumption(self): return self.c_df.copy()
    def get_stations(self): return self.s_df.copy()
    def get_inventory(self): return self.base_loader.get_inventory()
    def get_distances(self): return self.base_loader.get_distances()
    def get_vehicles(self): return self.base_loader.get_vehicles()

def tek_senaryo_hesapla(args):
    arac_sayisi, alpha, talep_faktor, dispatch_kural, n_modu = args
    
    loader_base = DataLoader()
    stations_df = loader_base.get_stations().copy()
    consumption_df = loader_base.get_consumption().copy()
    
    # 1. Talep Ölçekleme (Talep Şoku)
    if talep_faktor != 1.0:
        consumption_df['tuketim_adet'] = consumption_df['tuketim_adet'] * talep_faktor
        stations_df['ort_tuketim_saat'] = stations_df['ort_tuketim_saat'] * talep_faktor
        stations_df['ort_tuketim_dk'] = stations_df['ort_tuketim_dk'] * talep_faktor

    # 2. Alpha & N Modu Güncellemesi (K55)
    LT_dk = 45.0
    if n_modu == 'Dinamik_N':
        for idx, row in stations_df.iterrows():
            D_dk = row['ort_tuketim_saat'] / 60.0
            C = row['kutu_kapasitesi']
            rop_adet = D_dk * LT_dk * (1.0 + alpha)
            n_kart = max(1, math.ceil(rop_adet / C))
            stations_df.at[idx, 'kanban_n'] = n_kart
            stations_df.at[idx, 'baslangic_stok_adet'] = n_kart * C

    # 3. E-Kanban Sinyal Üretimi (Doğru Alpha ve Talep ile)
    m_loader = MockLoader(consumption_df, stations_df)
    sim = EKanbanSimulator(m_loader, alpha=alpha)
    signals_df = sim.run()
    
    # 4. VRPTW Çözümü
    solver = VRPTWSolver(m_loader)
    solver.signals_df = signals_df
    
    _, out_signals, _ = solver.solve(
        arac_sayisi=arac_sayisi,
        dispatch_kural=dispatch_kural,
        consumption_df=consumption_df
    )
    
    wip_d, starv_tot, starv_warm = hesapla_dinamik_wip_ve_starvation(
        out_signals, stations_df, consumption_df
    )
    
    starv_pct = round((starv_tot / 11520.0) * 100.0, 2)
    
    return {
        "arac_sayisi": arac_sayisi,
        "alpha": alpha,
        "talep_faktor": talep_faktor,
        "talep_sok_pct": int(round((talep_faktor - 1.0) * 100)),
        "dispatch_kural": dispatch_kural,
        "n_modu": n_modu,
        "starv_pct": starv_pct,
        "starv_dk": starv_tot,
        "ort_wip": wip_d
    }


def main():
    print("=" * 80)
    print("DASHBOARD SENARYO VERİ AMBARI ÜRETİCİSİ (MULTIPROCESSING)")
    print("=" * 80)
    
    arac_list = [1, 2, 3, 4, 5, 6, 7, 8]
    alpha_list = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    talep_list = [0.80, 0.90, 1.00, 1.10, 1.20]
    dispatch_list = ['EDD', 'SLACK', 'FIFO', 'KRITIKLIK']
    n_modu_list = ['Dinamik_N', 'Sabit_N']
    
    param_list = []
    for n_mod in n_modu_list:
        for disp in dispatch_list:
            for tf in talep_list:
                for a in alpha_list:
                    for v in arac_list:
                        param_list.append((v, a, tf, disp, n_mod))
                        
    total_tasks = len(param_list)
    cores = cpu_count()
    print(f"Toplam Parametre Kombinasyonu: {total_tasks}")
    print(f"Kullanılabilir CPU Çekirdek Sayısı (12 Çekirdek): {cores}")
    print("Hesaplama başlatılıyor...")
    
    t0 = time.time()
    
    with Pool(processes=cores) as pool:
        results = pool.map(tek_senaryo_hesapla, param_list)
        
    elapsed = time.time() - t0
    print(f"\nİşlem Tamamlandı! Toplam Süre: {elapsed:.2f} saniye ({elapsed/60:.2f} dakika)")
    
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(out_dir, exist_ok=True)
    
    json_path = os.path.join(out_dir, "dashboard_scenarios.json")
    csv_path = os.path.join(out_dir, "dashboard_scenarios.csv")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"Veriler başarıyla kaydedildi:\n - {json_path}\n - {csv_path}")

if __name__ == "__main__":
    main()
