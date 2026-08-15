import sys; sys.path.append('.')
from src.data_loader import DataLoader
from src.hafta8_kanban_karsilastirma import StaticMilkRunSimulator

loader = DataLoader()
sim = StaticMilkRunSimulator(loader)

print("=== K58 REGRESYON TESTI ===")
print()

# 60 dk - Hafta 8 orijinal
r60 = sim.run_static_simulation(arac_sayisi=2, tur_sikligi_dk=60)
print("60 dk, 2 arac: starv=" + str(round(r60['starv_pct_11520'],2)) + "% WIP=" + str(r60['ort_wip_stok']))
print("  Kalkis takvimi: " + str(r60['kalkis_dakikalari']))

r60_4 = sim.run_static_simulation(arac_sayisi=4, tur_sikligi_dk=60)
print("60 dk, 4 arac: starv=" + str(round(r60_4['starv_pct_11520'],2)) + "% WIP=" + str(r60_4['ort_wip_stok']))
print()

# 80 dk - Hafta 9 kanonik
r80 = sim.run_static_simulation(arac_sayisi=4, tur_sikligi_dk=80)
print("80 dk, 4 arac: starv=" + str(round(r80['starv_pct_11520'],2)) + "% WIP=" + str(r80['ort_wip_stok']))
print("  Kalkis takvimi: " + str(r80['kalkis_dakikalari']))
print("  Kanonik beklenti: %19.31 WIP=177.0")
print()

# Sonuc
if round(r80['starv_pct_11520'],2) == 19.31 and r80['ort_wip_stok'] == 177.0:
    print("REGRESYON: GECTI - 80dk kanonik deger tam eslesiyor")
else:
    print("REGRESYON: BASARISIZ - beklenti 19.31/177.0, elde edilen " + 
          str(round(r80['starv_pct_11520'],2)) + "/" + str(r80['ort_wip_stok']))

print()
print("GERI UYUMLULUK KONTROLU (varsayilan 60dk):")
r_default = sim.run_static_simulation(arac_sayisi=2)
print("Varsayilan (60dk), 2 arac: starv=" + str(round(r_default['starv_pct_11520'],2)) + "% WIP=" + str(r_default['ort_wip_stok']))
