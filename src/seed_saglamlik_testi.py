import sys, numpy as np
sys.path.append('.')
from src.data_loader import DataLoader
from src.vrptw_solver import VRPTWSolver
from src.hafta8_kanban_karsilastirma import hesapla_dinamik_wip_ve_starvation
from src.stokastik_replikasyon import uret_stokastik_tuketim

def hesapla_statik(consumption_df, stations_df, arac_sayisi=4, tur_suresi_dk=80):
    tuketim_pivot = consumption_df.pivot(index='dakika', columns='istasyon_id', values='tuketim_adet')
    ist_ids = list(stations_df['istasyon_id'])
    ist_n   = {r['istasyon_id']: int(r['kanban_n'])             for _, r in stations_df.iterrows()}
    ist_c   = {r['istasyon_id']: float(r['kutu_kapasitesi'])     for _, r in stations_df.iterrows()}
    stoklar = {r['istasyon_id']: float(r['baslangic_stok_adet']) for _, r in stations_df.iterrows()}
    tavan   = {s: ist_n[s] * ist_c[s] for s in ist_ids}
    starv, wip_log = [], []
    for m in range(480):
        if m > 0 and m % tur_suresi_dk == 0:
            kutu_per_ist = max(1, (arac_sayisi * 25) // len(ist_ids))
            for sid in ist_ids:
                stoklar[sid] = min(stoklar[sid] + kutu_per_ist * ist_c[sid], tavan[sid])
        for sid in ist_ids:
            c_val = tuketim_pivot.loc[m, sid] if (m in tuketim_pivot.index and sid in tuketim_pivot.columns) else 0.0
            stoklar[sid] = max(0.0, stoklar[sid] - c_val)
            if stoklar[sid] <= 0 and c_val > 0:
                starv.append((m, sid))
        wip_log.append(sum(stoklar.values()))
    return round(float(np.mean(wip_log)), 1), len(starv)

loader = DataLoader()
st = loader.get_stations()
solver = VRPTWSolver(loader)

results = []
co_42 = loader.get_consumption()
_, sig_42, _ = solver.solve(arac_sayisi=4, dispatch_kural='EDD')
wip_d42, starv_d42, _ = hesapla_dinamik_wip_ve_starvation(sig_42, st, co_42)
wip_s42, starv_s42 = hesapla_statik(co_42, st)
pct_d42 = round(starv_d42/11520*100, 2)
pct_s42 = round(starv_s42/11520*100, 2)
fark42 = round(pct_d42-pct_s42, 2)
yon42 = "STATIK LEHINE" if pct_s42 < pct_d42 else "DINAMIK LEHINE"
results.append(yon42)
print(f"BAZ seed=42 deterministik: Statik={pct_s42}% WIP={wip_s42} | Dinamik={pct_d42}% WIP={wip_d42} | Fark={fark42:+.2f} | {yon42}")

for seed in [7, 99, 123]:
    co_s = uret_stokastik_tuketim(seed=seed)
    _, sig_s, _ = solver.solve(arac_sayisi=4, dispatch_kural='EDD', consumption_df=co_s)
    wip_d, starv_d, _ = hesapla_dinamik_wip_ve_starvation(sig_s, st, co_s)
    wip_s, starv_s = hesapla_statik(co_s, st)
    pct_d = round(starv_d/11520*100, 2)
    pct_s = round(starv_s/11520*100, 2)
    fark  = round(pct_d-pct_s, 2)
    yon   = "STATIK LEHINE" if pct_s < pct_d else "DINAMIK LEHINE"
    results.append(yon)
    print(f"seed={seed} stokastik: Statik={pct_s}% WIP={wip_s} | Dinamik={pct_d}% WIP={wip_d} | Fark={fark:+.2f} | {yon}")

statik_n = results.count("STATIK LEHINE")
print(f"NIHAI OZET: {statik_n}/{len(results)} seed icinde STATIK LEHINE")
