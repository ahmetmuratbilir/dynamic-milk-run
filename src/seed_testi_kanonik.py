import sys; sys.path.append('.')
from src.data_loader import DataLoader
from src.vrptw_solver import VRPTWSolver
from src.hafta8_kanban_karsilastirma import StaticMilkRunSimulator, hesapla_dinamik_wip_ve_starvation
from src.stokastik_replikasyon import uret_stokastik_tuketim

loader = DataLoader()
st = loader.get_stations()
co = loader.get_consumption()
solver = VRPTWSolver(loader)
sim_statik = StaticMilkRunSimulator(loader)

# BAZ seed=42: kanonik statik (60dk tur, 1 kutu/ist)
res_s = sim_statik.run_static_simulation(arac_sayisi=4)
_, sig_d, _ = solver.solve(arac_sayisi=4, dispatch_kural='EDD')
wip_d, starv_d, _ = hesapla_dinamik_wip_ve_starvation(sig_d, st, co)
pct_s = round(res_s['starv_pct_11520'], 2)
pct_d = round(starv_d/11520*100, 2)

print("=== KANONIK BAZ REPRODUKSIYONU (seed=42, 60dk tur, 1 kutu/ist) ===")
print(f"Statik:  {pct_s}%  WIP={res_s['ort_wip_stok']}  (kanonik beklenti: %19.31 WIP=177)")
print(f"Dinamik: {pct_d}%  WIP={wip_d}  (kanonik beklenti: %24.58 WIP=182.3)")
print()

# STOKASTIK SEEDLER - kanonik StaticMilkRunSimulator (consumption_df degistirilerek)
print("=== GERCEK SEED TESTI (kanonik StaticMilkRunSimulator + stokastik tuketim) ===")
print("seed | Statik% | WIP_S | Dinamik% | WIP_D | Fark   | Yon")

results = [("STATIK LEHINE" if pct_s < pct_d else "DINAMIK LEHINE")]
print(f" 42  | {pct_s:6.2f}% | {res_s['ort_wip_stok']} | {pct_d:7.2f}%  | {wip_d} | {round(pct_d-pct_s,2):+.2f}  | {'STATIK LEHINE' if pct_s < pct_d else 'DINAMIK LEHINE'}")

for seed in [7, 99, 123]:
    co_s = uret_stokastik_tuketim(seed=seed)
    sim_statik.consumption_df = co_s
    res_s2 = sim_statik.run_static_simulation(arac_sayisi=4)
    _, sig_s, _ = solver.solve(arac_sayisi=4, dispatch_kural='EDD', consumption_df=co_s)
    wip_d2, starv_d2, _ = hesapla_dinamik_wip_ve_starvation(sig_s, st, co_s)
    ps = round(res_s2['starv_pct_11520'], 2)
    pd2 = round(starv_d2/11520*100, 2)
    yon = "STATIK LEHINE" if ps < pd2 else "DINAMIK LEHINE"
    results.append(yon)
    print(f"{seed:4d}  | {ps:6.2f}% | {res_s2['ort_wip_stok']} | {pd2:7.2f}%  | {wip_d2} | {round(pd2-ps,2):+.2f}  | {yon}")

statik_n = results.count("STATIK LEHINE")
print()
print(f"NIHAI OZET: {statik_n}/{len(results)} seed icinde STATIK LEHINE")
