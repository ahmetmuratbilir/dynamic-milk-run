"""
analitik_filo_hesabi.py
========================
Hafta 6 — Korosi & Duchon (2026) Analitik Filo Boyutlandırma Formülü

Kaynak: Körösi, G. & Duchoň, F. (2026). Analytical fleet-sizing method for the 
        Open Platform for Innovation in Logistics (OPIL). Scientific Reports, 
        16, 16797. Sayfa 3–4.

Uygulanan Kararlar:
  - K12: Araç hızı = 10 km/sa (166.67 m/dk), Klenk et al. (2012) s.5
  - K14: Yükleme süresi = 2 dk
  - K15: Boşaltma süresi = 3 dk  
  - K36: Darboğaz = Zaman/Filo Kısıtı (Hafta 5 bulgusu)

Formül (Körösi 2026, s.3-4):
  TC = T_L + L_d/v_c + T_U + L_e/v_c
  WL = w × TC
  AT = 60 × A × F_t × E_w
  AN = WL / AT → AN_final = ceil(AN)

Parametre Kaynakları:
  - A (kullanılabilirlik): Körösi s.6 SMARTENVELOPE (A=0.7), s.10 SMARTHam (A=0.99)
  - F_t (trafik faktörü): Körösi s.6 (Ft=0.5), s.10 (Ft=0.99)
  - E_w (operatör verimliliği): Körösi s.3 "set to 1.0 for fully autonomous agents"
"""

import os
import sys
import math
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader


def hesapla_analitik_filo(
    w: float,       # Saatlik sinyal/teslimat döngüsü sayısı
    T_L: float,     # Yükleme süresi (dk)
    T_U: float,     # Boşaltma süresi (dk) 
    L_d: float,     # Ortalama yüklü seyahat mesafesi (m)
    L_e: float,     # Boş dönüş mesafesi (m)
    v_c: float,     # Araç hızı (m/dk)
    A: float,       # Kullanılabilirlik faktörü (0,1]
    F_t: float,     # Trafik faktörü (0,1]
    E_w: float = 1.0  # Operatör verimliliği (tam otonom=1.0)
) -> dict:
    """
    Korosi & Duchon (2026) analitik filo boyutlandırma formülü.
    Scientific Reports / Nature, 16:16797, Sayfa 3-4.
    """
    TC = T_L + (L_d / v_c) + T_U + (L_e / v_c)  # Tek çevrim süresi (dk)
    WL = w * TC                                    # Saatlik toplam iş yükü (dk)
    AT = 60.0 * A * F_t * E_w                     # Saatlik efektif süre (dk)
    AN = WL / AT                                   # Gerekli araç (kesirli)
    AN_final = math.ceil(AN)                       # Gerekli araç (tam sayı)
    Phi = A * F_t * E_w                           # Bileşik operasyonel faktör (s.539)

    return {
        "TC_dk": round(TC, 2),
        "WL_dk_saat": round(WL, 2),
        "AT_dk_saat": round(AT, 2),
        "AN_kesirli": round(AN, 4),
        "AN_final": AN_final,
        "Phi": round(Phi, 4),
        "A": A,
        "F_t": F_t,
        "E_w": E_w,
        "w_saat": w
    }


def main():
    loader = DataLoader()

    # ── Parametreleri projemizden al ──
    vehicles_df = loader.get_vehicles()
    T_L = float(vehicles_df.iloc[0]["yukl_sure_dk"])       # K14: 2 dk
    T_U = float(vehicles_df.iloc[0]["bosalt_sure_dk"])     # K15: 3 dk
    hiz_km_sa = float(vehicles_df.iloc[0]["hiz_kmh"])      # K12: 10 km/sa
    v_c = float(vehicles_df.iloc[0]["hiz_m_dk"])           # 166.67 m/dk

    # Mesafe matrisinden L_d ve L_e hesapla
    distances_df = loader.get_distances()
    
    # L_d: Depot'tan (node=0) istasyonlara ortalama mesafe (yueklue seyahat)
    from_depot = distances_df[distances_df["from_node"] == 0]
    L_d = from_depot["mesafe_m"].mean()
    
    # L_e: Istasyonlardan depot'a (node=0) ortalama mesafe (bos doenuesue)
    to_depot = distances_df[distances_df["to_node"] == 0]
    L_e = to_depot["mesafe_m"].mean()

    # w: Saatlik sinyal sayısı (H4 bulgusu: 182 sinyal / 8 saat)
    signals_path = os.path.join(loader.base_dir, "data", "synthetic", "ekanban_signals.csv")
    if os.path.exists(signals_path):
        signals_df = pd.read_csv(signals_path)
        toplam_sinyal = len(signals_df)
        vardiya_saat = 8.0
        w = toplam_sinyal / vardiya_saat
    else:
        toplam_sinyal = 182
        w = 182 / 8.0

    print("=" * 70)
    print("HAFTA 6: ANALITIK FILO BOYUTLANDIRMA (Korosi & Duchon, 2026)")
    print("Kaynak: Scientific Reports / Nature, 16:16797, s.3-4")
    print("=" * 70)

    print(f"\n── PROJENIN PARAMETRELERI ──")
    print(f"  T_L (yükleme süresi)  : {T_L} dk  [K14]")
    print(f"  T_U (boşaltma süresi) : {T_U} dk  [K15]")
    print(f"  v_c (araç hızı)       : {v_c:.2f} m/dk = {hiz_km_sa} km/sa  [K12]")
    print(f"  L_d (ort. yüklü mesafe): {L_d:.1f} m  [mesafe matrisi]")
    print(f"  L_e (ort. boş dönüş)  : {L_e:.1f} m  [mesafe matrisi]")
    print(f"  w (saatlik sinyal)    : {w:.2f} sinyal/saat  [{toplam_sinyal} sinyal / {vardiya_saat} saat]")
    print(f"  E_w (operatör verimi) : 1.0 (tam otonom)  [Körösi s.3]")

    # ── Duyarlılık Analizi: 3 senaryo ──
    # Körösi s.6: SMARTENVELOPE A=0.7, Ft=0.5
    # Körösi s.10: SMARTHam A=0.99, Ft=0.99
    # Bizim baz: A=0.85, Ft=0.80 (ikisinin ortası, onaylandı)
    senaryolar = [
        {"ad": "MUHAFAZAKAR", "A": 0.70, "F_t": 0.60, "kaynak": "Körösi s.6 (SMARTENVELOPE baz) civarinda"},
        {"ad": "BAZ",         "A": 0.85, "F_t": 0.80, "kaynak": "Kullanici onaylanmis orta değer"},
        {"ad": "IYIMSER",     "A": 0.95, "F_t": 0.95, "kaynak": "Körösi s.10 (SMARTHam baz) civarinda"},
    ]

    print(f"\n── DUYARLILIK ANALIZI: A x F_t SENARYOLARI ──")
    print(f"{'Senaryo':<15} {'A':>5} {'F_t':>5} {'Φ':>6} {'TC(dk)':>7} {'WL(dk/sa)':>10} {'AT(dk/sa)':>10} {'AN':>7} {'AN_final':>9}")
    print("-" * 85)

    sonuclar = []
    for s in senaryolar:
        r = hesapla_analitik_filo(
            w=w, T_L=T_L, T_U=T_U, L_d=L_d, L_e=L_e,
            v_c=v_c, A=s["A"], F_t=s["F_t"], E_w=1.0
        )
        sonuclar.append({**s, **r})
        print(f"{s['ad']:<15} {s['A']:>5.2f} {s['F_t']:>5.2f} {r['Phi']:>6.3f} {r['TC_dk']:>7.2f} {r['WL_dk_saat']:>10.2f} {r['AT_dk_saat']:>10.2f} {r['AN_kesirli']:>7.2f} {r['AN_final']:>9d}")

    print(f"\n── YORUM ──")
    baz = [s for s in sonuclar if s["ad"] == "BAZ"][0]
    print(f"  Baz senaryoda ({baz['A']}, {baz['F_t']}): AN = {baz['AN_kesirli']:.2f} → {baz['AN_final']} araç gerekli.")
    print(f"  Mevcut filo: 2 araç (K03).")
    if baz["AN_final"] > 2:
        print(f"  ⚠️  ANALITIK SONUC: 2 araç YETERSİZ. En az {baz['AN_final']} araç gereklidir.")
        print(f"  Bu sonuç, H5 deneysel bulgusunu (%52.08 starvation) analitik olarak doğrulamaktadır.")
    else:
        print(f"  ✅ Analitik sonuca göre 2 araç yeterli görünüyor.")

    # Sonuçları CSV olarak kaydet
    out_dir = os.path.join(loader.base_dir, "data", "synthetic")
    pd.DataFrame(sonuclar).to_csv(
        os.path.join(out_dir, "analitik_filo_sonuclari.csv"),
        index=False, encoding="utf-8"
    )
    print(f"\n  Sonuclar kaydedildi: data/synthetic/analitik_filo_sonuclari.csv")


if __name__ == "__main__":
    main()
