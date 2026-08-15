import sys; sys.path.append('.')
from src.data_loader import DataLoader
from src.hafta8_kanban_karsilastirma import StaticMilkRunSimulator
loader = DataLoader()
sim = StaticMilkRunSimulator(loader)
for n in [2, 4]:
    r = sim.run_static_simulation(arac_sayisi=n)
    s = r['starv_pct_11520']
    w = r['ort_wip_stok']
    m = r['toplam_mesafe_km']
    print(n, 'arac: starv='+str(round(s,2))+'%  WIP='+str(w)+'  mesafe='+str(m)+'km')
    print('  kanonik beklenti 4 arac: %19.31 WIP=177')
