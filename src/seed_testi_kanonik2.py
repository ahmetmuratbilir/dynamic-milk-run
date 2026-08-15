import sys, math, numpy as np
sys.path.append('.')
from src.data_loader import DataLoader
from src.vrptw_solver import VRPTWSolver
from src.hafta8_kanban_karsilastirma import StaticMilkRunSimulator, hesapla_dinamik_wip_ve_starvation
from src.stokastik_replikasyon import uret_stokastik_tuketim

def run_statik_80dk(sim, consumption_df, arac_sayisi=4):
    tuketim_pivot = consumption_df.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")
    stoklar = {row["istasyon_id"]: float(row["baslangic_stok_adet"]) for _, row in sim.stations_df.iterrows()}
    ist_c = {row["istasyon_id"]: float(row["kutu_kapasitesi"]) for _, row in sim.stations_df.iterrows()}
    ist_n = {row["istasyon_id"]: int(row["kanban_n"]) for _, row in sim.stations_df.iterrows()}
    ist_cap = {sid: ist_n[sid]*ist_c[sid] for sid in stoklar}
    kalkislar = [80, 160, 240, 320, 400]
    istasyon_sirasi = [f"S{i}" for i in range(1, 25)]
    deliveries_by_min = {}
    for t_k in kalkislar:
        gruplari = np.array_split(istasyon_sirasi, arac_sayisi)
        for grup in gruplari:
            curr_node = "0"
            curr_time = float(t_k)
            tur_kutu = 0
            for sid in grup:
                target_node = sid.replace("S", "")
                tt = sim.get_travel_time(curr_node, target_node)
                arr_time = curr_time + tt
                if tur_kutu + 1 <= sim.Q_arac:
                    tur_kutu += 1
                    arr_m = int(math.floor(arr_time))
                    deliveries_by_min.setdefault(arr_m, []).append((sid, ist_c[sid]))
                curr_node = target_node
                curr_time = arr_time + sim.bosaltma_sure
    starvation_events = []
    wip_log = []
    for m in range(480):
        if m in deliveries_by_min:
            for sid, miktar in deliveries_by_min[m]:
                stoklar[sid] = min(ist_cap[sid], stoklar[sid] + miktar)
        for sid in stoklar:
            c_val = tuketim_pivot.loc[m, sid] if m in tuketim_pivot.index and sid in tuketim_pivot.columns else 0.0
            stoklar[sid] -= c_val
            if stoklar[sid] <= 0:
                starvation_events.append(1)
                stoklar[sid] = 0.0
        wip_log.append(sum(stoklar.values()))
    return round(len(starvation_events)/11520*100, 2), round(float(np.mean(wip_log)), 1)

loader = DataLoader()
st = loader.get_stations()
solver = VRPTWSolver(loader)
sim = StaticMilkRunSimulator(loader)

print("=== KANONIK SEED SAGLAMLIK TESTI (80dk tur, 1 kutu/ist - Hafta 9 senaryosu) ===")
print("seed | Statik% | WIP_S | Dinamik% | WIP_D | Fark    | Yon")
results = []
for seed_label, co in [("42-det", loader.get_consumption())] + [(str(s), uret_stokastik_tuketim(seed=s)) for s in [7, 99, 123]]:
    ps, ws = run_statik_80dk(sim, co, arac_sayisi=4)
    sim_tmp = StaticMilkRunSimulator(loader)
    _, sig, _ = solver.solve(arac_sayisi=4, dispatch_kural='EDD', consumption_df=co)
    wip_d, starv_d, _ = hesapla_dinamik_wip_ve_starvation(sig, st, co)
    pd2 = round(starv_d/11520*100, 2)
    yon = "STATIK LEHINE" if ps < pd2 else "DINAMIK LEHINE"
    results.append(yon)
    print(seed_label, "| "+str(ps)+"% | "+str(ws)+" | "+str(pd2)+"% | "+str(wip_d)+" | "+str(round(pd2-ps,2))+" | "+yon)

statik_n = results.count("STATIK LEHINE")
print()
print("NIHAI OZET: "+str(statik_n)+"/"+str(len(results))+" seed icinde STATIK LEHINE")
print()
print("TUTARLILIK KONTROLU:")
print("seed=42-det Statik beklenti: %19.31 WIP=177.0 (Hafta 9 kanonik)")
