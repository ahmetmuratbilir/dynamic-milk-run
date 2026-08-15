# 80dk kalkis takvimi testi - 19.31'i reprodukte etmeye calis
import sys, math, numpy as np, pandas as pd
sys.path.append('.')
from src.data_loader import DataLoader
from src.hafta8_kanban_karsilastirma import StaticMilkRunSimulator, hesapla_dinamik_wip_ve_starvation
from src.vrptw_solver import VRPTWSolver

loader = DataLoader()
sim = StaticMilkRunSimulator(loader)
st = loader.get_stations()
co = loader.get_consumption()

# 80dk kalkis takvimi
kalkis_80 = [80, 160, 240, 320, 400]

# Orjinal 60dk test
print("60dk tur:", sim.run_static_simulation(4)['starv_pct_11520'],
      "WIP:", sim.run_static_simulation(4)['ort_wip_stok'])

# 80dk takvimle el ile simulasyon
sim.kalkis_dakikalari = kalkis_80  # Bu ise yaramaz, metod ic degisken
# Fakat StaticMilkRunSimulator icindeki kalkis_dakikalari degistirerek test edelim
import types

def run_80dk(self, arac_sayisi=4):
    tuketim_pivot = self.consumption_df.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")
    stoklar = {}
    ist_c = {}
    ist_n = {}
    for _, row in self.stations_df.iterrows():
        sid = row["istasyon_id"]
        stoklar[sid] = float(row["baslangic_stok_adet"])
        ist_c[sid] = float(row["kutu_kapasitesi"])
        ist_n[sid] = int(row["kanban_n"])
    kalkis_dakikalari = [80, 160, 240, 320, 400]
    sabit_istasyon_sirasi = [f"S{i}" for i in range(1, 25)]
    deliveries_by_min = {}
    toplam_mesafe_m = 0.0
    toplam_tasinan_kutu = 0
    tur_kayitlari = []
    tur_id = 1
    for t_kalkis in kalkis_dakikalari:
        istasyon_gruplari = np.array_split(sabit_istasyon_sirasi, arac_sayisi)
        for v_idx, grup in enumerate(istasyon_gruplari):
            v_id = f"A{v_idx+1}"
            curr_node = "0"
            curr_time = float(t_kalkis)
            tur_kutu = 0
            tur_mesafe = 0.0
            for sid in grup:
                target_node = sid.replace("S", "")
                tt = self.get_travel_time(curr_node, target_node)
                dist = self.get_travel_dist(curr_node, target_node)
                arr_time = curr_time + tt
                kutu_sayisi = 1
                if tur_kutu + kutu_sayisi <= self.Q_arac:
                    tur_kutu += kutu_sayisi
                    arr_m = int(math.floor(arr_time))
                    deliveries_by_min.setdefault(arr_m, []).append((sid, kutu_sayisi * ist_c[sid]))
                tur_mesafe += dist
                curr_node = target_node
                curr_time = arr_time + self.bosaltma_sure
            ret_tt = self.get_travel_time(curr_node, "0")
            ret_dist = self.get_travel_dist(curr_node, "0")
            tur_mesafe += ret_dist
            toplam_mesafe_m += tur_mesafe
            toplam_tasinan_kutu += tur_kutu
            tur_kayitlari.append({"tur_id": f"STAT_T{tur_id:03d}", "arac_id": v_id, "kalkis_dk": t_kalkis})
            tur_id += 1
    ist_cap = {row["istasyon_id"]: float(row["kanban_n"] * row["kutu_kapasitesi"]) for _, row in self.stations_df.iterrows()}
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
    starv_pct = len(starvation_events)/11520*100
    wip = round(float(np.mean(wip_stok_kayitlari)),1)
    return starv_pct, wip

starv_80, wip_80 = run_80dk(sim, 4)
print("80dk tur (el ile, 1 kutu/ist):", round(starv_80,2), "WIP:", wip_80)
print("Kanonik beklenti: %19.31 WIP=177")
