"""
generate_synthetic_data.py
==========================
Onaylanan referans_veri.md parametrelerine gore sentetik veri seti uretir.
Cikti: data/synthetic/ klasorune 5 CSV dosyasi

KAYNAK: referans_veri.md (Hafta 1, kullanici onayladi 29.07.2026)
NOT: Bu tamamen ornek veridir. Gercek veriyle test edilmesi gerekiyor.
"""

import pandas as pd
import numpy as np
import os

# Rastgele sabit seed - ayni script calistirildiginda ayni veri uretilir
np.random.seed(42)

# ─────────────────────────────────────────────────────────
# ONAYLI PARAMETRELER (referans_veri.md'den)
# ─────────────────────────────────────────────────────────
SIM_SURE   = 480        # dakika (1 vardiya)
N_HAT      = 4          # uretim hatti sayisi
N_ISTASYON = 24         # toplam istasyon (hat basina 6)
N_ARAC     = 2          # milk-run araci
ARAC_KAP   = 25         # kutu/arac
ARAC_HIZ   = 10         # km/saat
LT_DK      = 45         # lead time (dakika)
ALPHA      = 0.15       # guvenlik katsayisi
MESAFE_M   = 180        # istasyonlar arasi ortalama mesafe (metre)
DEPO_ID    = 0          # depo node ID

# Her istasyonun ortalama saatlik tuketim hizi (onaylanan degerler)
# Kaynak: referans_veri.md - tuketim hizi: 11-24 adet/saat
ISTASYON_TUKETIM = {
    # Hat-1 (S1-S6)
    "S1":  {"hat": "Hat-1", "mu": 22, "C": 20},
    "S2":  {"hat": "Hat-1", "mu": 18, "C": 20},
    "S3":  {"hat": "Hat-1", "mu": 15, "C": 15},
    "S4":  {"hat": "Hat-1", "mu": 20, "C": 20},
    "S5":  {"hat": "Hat-1", "mu": 12, "C": 15},
    "S6":  {"hat": "Hat-1", "mu": 17, "C": 20},
    # Hat-2 (S7-S12)
    "S7":  {"hat": "Hat-2", "mu": 21, "C": 20},
    "S8":  {"hat": "Hat-2", "mu": 13, "C": 15},
    "S9":  {"hat": "Hat-2", "mu": 19, "C": 20},
    "S10": {"hat": "Hat-2", "mu": 11, "C": 15},
    "S11": {"hat": "Hat-2", "mu": 16, "C": 20},
    "S12": {"hat": "Hat-2", "mu": 14, "C": 15},
    # Hat-3 (S13-S18)
    "S13": {"hat": "Hat-3", "mu": 23, "C": 20},
    "S14": {"hat": "Hat-3", "mu": 18, "C": 20},
    "S15": {"hat": "Hat-3", "mu": 15, "C": 15},
    "S16": {"hat": "Hat-3", "mu": 24, "C": 20},
    "S17": {"hat": "Hat-3", "mu": 17, "C": 20},
    "S18": {"hat": "Hat-3", "mu": 14, "C": 15},
    # Hat-4 (S19-S24)
    "S19": {"hat": "Hat-4", "mu": 20, "C": 20},
    "S20": {"hat": "Hat-4", "mu": 16, "C": 20},
    "S21": {"hat": "Hat-4", "mu": 13, "C": 15},
    "S22": {"hat": "Hat-4", "mu": 18, "C": 20},
    "S23": {"hat": "Hat-4", "mu": 12, "C": 15},
    "S24": {"hat": "Hat-4", "mu": 21, "C": 20},
}

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic")
os.makedirs(OUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# 1. stations.csv — Istasyon tanim tablosu
# ─────────────────────────────────────────────────────────
print("Olusturuluyor: stations.csv ...")

istasyon_listesi = []
for idx, (istasyon_id, bilgi) in enumerate(ISTASYON_TUKETIM.items(), start=1):
    mu    = bilgi["mu"]
    sigma = round(0.20 * mu, 2)   # std = %20 * ortalama (referans_veri.md onaylandi)
    C     = bilgi["C"]
    # Kanban formulu: N = ceil((D_saat/60 * LT * (1+alpha)) / C)
    # D_dakika = mu / 60
    D_dk  = mu / 60
    N     = int(np.ceil((D_dk * LT_DK * (1 + ALPHA)) / C))
    # Baslangic stogu: N kutu (tam dolu basla)
    baslangic_kutu = N

    istasyon_listesi.append({
        "istasyon_id":          istasyon_id,
        "hat":                  bilgi["hat"],
        "sira_no":              idx,
        "ort_tuketim_saat":     mu,
        "std_tuketim_saat":     sigma,
        "ort_tuketim_dk":       round(D_dk, 4),
        "kutu_kapasitesi":      C,
        "kanban_n":             N,
        "baslangic_kutu":       baslangic_kutu,
        "baslangic_stok_adet":  baslangic_kutu * C,
        "reorder_point_kutu":   1,    # ROP: 1 kutu kaldiginda sinyal
    })

df_istasyon = pd.DataFrame(istasyon_listesi)
df_istasyon.to_csv(os.path.join(OUT_DIR, "stations.csv"), index=False, encoding="utf-8")
print(f"  -> {len(df_istasyon)} istasyon kaydedildi.")

# ─────────────────────────────────────────────────────────
# 2. consumption.csv — Dakiklik stokastik tuketim verisi
# ─────────────────────────────────────────────────────────
print("Olusturuluyor: consumption.csv ...")

# Her dakika, her istasyon icin tüketim uret
# Tuketim: Normal(mu/60, sigma/60), min=0 (negatif olamaz)
kayitlar = []
for dk in range(SIM_SURE):
    for istasyon_id, bilgi in ISTASYON_TUKETIM.items():
        mu_dk    = bilgi["mu"] / 60
        sigma_dk = (0.20 * bilgi["mu"]) / 60
        tuketim  = max(0.0, np.random.normal(mu_dk, sigma_dk))
        kayitlar.append({
            "dakika":       dk,
            "istasyon_id":  istasyon_id,
            "tuketim_adet": round(tuketim, 4),
        })

df_tuketim = pd.DataFrame(kayitlar)
df_tuketim.to_csv(os.path.join(OUT_DIR, "consumption.csv"), index=False, encoding="utf-8")
print(f"  -> {len(df_tuketim)} satir kaydedildi ({SIM_SURE} dk x {N_ISTASYON} istasyon).")

# ─────────────────────────────────────────────────────────
# 3. inventory.csv — Baslangic stok seviyeleri
# ─────────────────────────────────────────────────────────
print("Olusturuluyor: inventory.csv ...")

inv_kayitlar = []
for row in istasyon_listesi:
    inv_kayitlar.append({
        "istasyon_id":         row["istasyon_id"],
        "hat":                 row["hat"],
        "baslangic_kutu":      row["baslangic_kutu"],
        "baslangic_stok_adet": row["baslangic_stok_adet"],
        "kutu_kapasitesi":     row["kutu_kapasitesi"],
        "kanban_n":            row["kanban_n"],
        "reorder_point_kutu":  row["reorder_point_kutu"],
    })

df_inv = pd.DataFrame(inv_kayitlar)
df_inv.to_csv(os.path.join(OUT_DIR, "inventory.csv"), index=False, encoding="utf-8")
print(f"  -> {len(df_inv)} istasyon stok bilgisi kaydedildi.")

# ─────────────────────────────────────────────────────────
# 4. vehicles.csv — Arac tanim tablosu
# ─────────────────────────────────────────────────────────
print("Olusturuluyor: vehicles.csv ...")

araclar = []
for i in range(1, N_ARAC + 1):
    araclar.append({
        "arac_id":          f"A{i}",
        "kapasite_kutu":    ARAC_KAP,
        "hiz_kmh":          ARAC_HIZ,
        "hiz_m_dk":         round(ARAC_HIZ * 1000 / 60, 2),   # metre/dakika
        "yukl_sure_dk":     2,     # yükleme suresi (onaylandi)
        "bosalt_sure_dk":   3,     # bosaltma suresi (onaylandi)
        "handling_sure_dk": 5,     # toplam handling/istasyon (onaylandi)
        "max_tur_sure_dk":  90,    # maksimum tur suresi (onaylandi)
    })

df_arac = pd.DataFrame(araclar)
df_arac.to_csv(os.path.join(OUT_DIR, "vehicles.csv"), index=False, encoding="utf-8")
print(f"  -> {len(df_arac)} arac kaydedildi.")

# ─────────────────────────────────────────────────────────
# 5. distances.csv — Mesafe matrisi (depo + 24 istasyon)
# ─────────────────────────────────────────────────────────
print("Olusturuluyor: distances.csv ...")

# Node listesi: 0=Depo, 1..24 = istasyonlar
# Depo -> Hat-1 ilk istasyon: 90 m
# Depo -> Hat-2 ilk istasyon: 120 m
# Depo -> Hat-3 ilk istasyon: 180 m
# Depo -> Hat-4 ilk istasyon: 250 m
# Ayni hat icinde istasyonlar arasi: MESAFE_M = 180 m
# Farkli hat arasi: 250-420 m arasi

istasyon_id_listesi = list(ISTASYON_TUKETIM.keys())  # S1..S24
hat_listesi = [ISTASYON_TUKETIM[s]["hat"] for s in istasyon_id_listesi]

# Depo -> her hat ilk istasyonu mesafesi
depo_hat_mesafe = {
    "Hat-1": 90,
    "Hat-2": 120,
    "Hat-3": 180,
    "Hat-4": 250,
}

def get_mesafe(from_node, to_node):
    """Iki node arasindaki mesafeyi hesapla."""
    if from_node == to_node:
        return 0
    
    # Depo (node 0) iceriyorsa
    if from_node == 0:
        hat = hat_listesi[to_node - 1]
        return depo_hat_mesafe[hat]
    if to_node == 0:
        hat = hat_listesi[from_node - 1]
        return depo_hat_mesafe[hat]
    
    # Istasyon -> Istasyon
    hat_from = hat_listesi[from_node - 1]
    hat_to   = hat_listesi[to_node - 1]
    
    if hat_from == hat_to:
        # Ayni hat: fark * 180 m
        fark = abs(from_node - to_node)
        return fark * MESAFE_M
    else:
        # Farkli hat: sabit 300 m + kucuk rastgele
        np.random.seed(from_node * 100 + to_node)
        return 300 + int(np.random.uniform(-50, 120))

# Tum node ciftleri icin mesafe tablosu
n_nodes = N_ISTASYON + 1   # 0 (depo) + 24 istasyon
mesafe_kayitlari = []
for i in range(n_nodes):
    for j in range(n_nodes):
        if i == j:
            continue
        mesafe = get_mesafe(i, j)
        # Dakika cinsinden sure (hiz = 10 km/h = 166.67 m/dk)
        sure_dk = round(mesafe / (ARAC_HIZ * 1000 / 60), 2)
        
        from_label = "Depo" if i == 0 else istasyon_id_listesi[i - 1]
        to_label   = "Depo" if j == 0 else istasyon_id_listesi[j - 1]
        
        mesafe_kayitlari.append({
            "from_node":    i,
            "to_node":      j,
            "from_label":   from_label,
            "to_label":     to_label,
            "mesafe_m":     mesafe,
            "sure_dk":      sure_dk,
        })

df_mesafe = pd.DataFrame(mesafe_kayitlari)
df_mesafe.to_csv(os.path.join(OUT_DIR, "distances.csv"), index=False, encoding="utf-8")
print(f"  -> {len(df_mesafe)} node cifti kaydedildi ({n_nodes} node).")

# ─────────────────────────────────────────────────────────
# 6. production_plan.csv — Uretim programi (saatlik)
# ─────────────────────────────────────────────────────────
print("Olusturuluyor: production_plan.csv ...")

plan_kayitlar = []
saat_sayisi = SIM_SURE // 60  # 8 saat

for saat in range(saat_sayisi):
    for hat_id in [f"Hat-{i}" for i in range(1, N_HAT + 1)]:
        # Hat bazli planlanan uretim miktari (ornek: 50-100 adet/saat)
        plan_miktar = int(np.random.uniform(50, 100))
        plan_kayitlar.append({
            "saat":         saat,
            "hat":          hat_id,
            "plan_miktar":  plan_miktar,
        })

df_plan = pd.DataFrame(plan_kayitlar)
df_plan.to_csv(os.path.join(OUT_DIR, "production_plan.csv"), index=False, encoding="utf-8")
print(f"  -> {len(df_plan)} uretim plan satirı kaydedildi.")

# ─────────────────────────────────────────────────────────
# OZET RAPOR
# ─────────────────────────────────────────────────────────
print("\n" + "="*50)
print("SENTETIK VERI SETI OLUSTURULDU")
print("="*50)
print(f"Kaynak : referans_veri.md (Hafta 1 - onaylandi)")
print(f"Durum  : ORNEK VERI - gercek veriyle test edilmesi gerekiyor")
print()
print("Dosyalar:")
for f in ["stations.csv", "consumption.csv", "inventory.csv",
          "vehicles.csv", "distances.csv", "production_plan.csv"]:
    path = os.path.join(OUT_DIR, f)
    size = os.path.getsize(path)
    print(f"  data/synthetic/{f:<25} {size:>8} byte")

print()
print("Istasyon Kanban Ozeti:")
print(f"{'Istasyon':<10} {'Hat':<8} {'mu(sa)':<10} {'C':<6} {'N':<5} {'Bas.Kutu'}")
print("-" * 50)
for row in istasyon_listesi:
    print(f"  {row['istasyon_id']:<8} {row['hat']:<8} {row['ort_tuketim_saat']:<10} "
          f"{row['kutu_kapasitesi']:<6} {row['kanban_n']:<5} {row['baslangic_kutu']}")
