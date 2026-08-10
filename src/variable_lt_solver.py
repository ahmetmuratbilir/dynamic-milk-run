"""
variable_lt_solver.py
======================
Hafta 8 -- İstasyon Bazlı Değişken Lead Time (LT) ve EDD vs. SLACK Ayrışma Analizi

Tasarım ve Mantık:
  - Sentetik veride sabit LT = 45 dk olduğunda EDD == SLACK == FIFO çıkmıştı (H7 bulgusu).
  - Hafta 8'de istasyonların depoya olan mesafesine dayalı deterministik değişken LT_i in [30, 60] dk tanımlanır.
  - Formül: LT_i = 30 + floor( (Mesafe(Depo, S_i) / Maks_Mesafe) * 30 )  [Mühendislik Kararı]
  - ROP_i = D_i,dk * LT_i * (1 + alpha)  [K25 oransal tampon formülü]

Test Edilen Hipotez:
  - Klasik Çizelgeleme Teorisi (Baker, 1974; Pinedo, 2016): Değişken teslim sürelerinde SLACK kuralının
    aciliyeti daha esnek yakaladığı kabul edilir (Genel çizelgeleme hipotezi, Wang 2008 teoremi değildir).
  - Bu hipotezin sentetik veri setimizdeki geçerliliği test edilir.

Kapsam ve Raporlama Standartları:
  - İkili Payda Raporlaması (K47): Hem 11,520 (tam vardiya) hem 10,440 (warm-up hariç) paydası gösterilir.
  - Deterministik Standart Koşum (K46): seed=42 tüketim verisi, 480 dk vardiya, Q_arac=25 kutu [K04].
"""

import os
import sys
import math
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader


class VariableLTSimulator:

    def __init__(self, loader: DataLoader):
        self.loader = loader
        self.stations_df = loader.get_stations()
        self.distances_df = loader.get_distances()
        self.consumption_df = loader.get_consumption()
        self.vehicles_df = loader.get_vehicles()

        self.Q_arac = int(self.vehicles_df.iloc[0]["kapasite_kutu"])  # 25 kutu [Mühendislik varsayımı - K04]
        self.max_tur_sure = float(self.vehicles_df.iloc[0]["max_tur_sure_dk"])  # 90 dk [K17]
        self.yukleme_sure = float(self.vehicles_df.iloc[0]["yukl_sure_dk"])  # 2 dk [K14]
        self.bosaltma_sure = float(self.vehicles_df.iloc[0]["bosalt_sure_dk"])  # 3 dk [K15]
        self.ALPHA = 0.15  # K08

        # Mesafe ve Süre sözlükleri
        self.dist_matrix = {}
        self.time_matrix = {}
        for _, row in self.distances_df.iterrows():
            f = str(row["from_node"])
            t = str(row["to_node"])
            self.dist_matrix[(f, t)] = float(row["mesafe_m"])
            self.time_matrix[(f, t)] = float(row["sure_dk"])

        # 1. İstasyon bazlı değişken LT_i hesaplama
        self.station_lt = self._hesapla_degisken_lt()

    def _hesapla_degisken_lt(self) -> dict:
        """
        Depo (Node 0) ile istasyonlar (Node 1..24) arasındaki mesafeye göre LT_i in [30, 60] dk belirler.
        Min-Max Normalizasyon Formülü: LT_i = 30 + round( ((Mesafe - Min_Mesafe) / (Maks_Mesafe - Min_Mesafe)) * 30 )
        Böylece en yakın istasyon (90m) tam 30 dk, en uzak istasyon (250m) tam 60 dk alır.
        """
        depot_distances = {}
        for sid in self.stations_df["istasyon_id"]:
            s_num = sid.replace("S", "")
            dist = self.dist_matrix.get(("0", s_num), self.dist_matrix.get(("DEPOT", sid), 150.0))
            depot_distances[sid] = dist

        min_dist = min(depot_distances.values()) if depot_distances else 90.0
        max_dist = max(depot_distances.values()) if depot_distances else 250.0

        station_lt = {}
        for sid, dist in depot_distances.items():
            if max_dist > min_dist:
                lt_val = 30 + int(round(((dist - min_dist) / (max_dist - min_dist)) * 30))
            else:
                lt_val = 45
            lt_val = max(30, min(60, lt_val))
            station_lt[sid] = {
                "mesafe_m": dist,
                "lt_dk": lt_val
            }
        return station_lt

    def get_travel_time(self, from_node: str, to_node: str) -> float:
        if from_node == to_node:
            return 0.0
        return self.time_matrix.get((from_node, to_node), 5.0)

    def uret_degisken_lt_sinyalleri(self) -> pd.DataFrame:
        """
        İstasyon bazlı ROP_i ve LT_i değerlerine göre 480 dakikalık E-Kanban sinyallerini üretir.
        K06 gereği N_i = ceil( D_i * LT_i * (1+alpha) / C_i ) formülüyle kart sayıları da güncellenir.
        Her istasyon için açık sinyal t + LT_i anında kapanır ve yeni döngüye izin verir (K28/K29).
        """
        tuketim_pivot = self.consumption_df.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")

        # İstasyon durumları
        ist_durum = {}
        for _, row in self.stations_df.iterrows():
            sid = row["istasyon_id"]
            D_dk = float(row["ort_tuketim_saat"]) / 60.0
            lt_i = self.station_lt[sid]["lt_dk"]
            C_val = float(row["kutu_kapasitesi"])
            rop_i = D_dk * lt_i * (1 + self.ALPHA)  # K25
            # K06: Değişken LT_i için yeni N_i hesaplaması
            n_i = math.ceil(rop_i / C_val)
            
            ist_durum[sid] = {
                "hat": row["hat"],
                "D_dk": D_dk,
                "C": C_val,
                "N": n_i,
                "lt_i": lt_i,
                "rop": rop_i,
                "stok": float(n_i * C_val),  # Başlangıç stoku = N_i * C_i
                "acik_sinyal": False,
                "yenileme_dk": None,
                "sinyal_id_sayac": 0
            }

        sinyaller = []

        for t in range(480):
            # 1. Stok yenileme (t == yenileme_dk)
            for sid, ist in ist_durum.items():
                if ist["acik_sinyal"] and ist["yenileme_dk"] == t:
                    # Kanban kuralı: Stok asla N * C tavanını aşamaz
                    ist["stok"] = min(float(ist["N"] * ist["C"]), ist["stok"] + ist["C"])
                    ist["acik_sinyal"] = False
                    ist["yenileme_dk"] = None

            # 2. Tüketim düş
            for sid in ist_durum:
                c_val = tuketim_pivot.loc[t, sid] if t in tuketim_pivot.index and sid in tuketim_pivot.columns else 0.0
                ist_durum[sid]["stok"] = max(0.0, ist_durum[sid]["stok"] - c_val)

            # 3. ROP kontrolü & Sinyal üretimi
            for sid, ist in ist_durum.items():
                if ist["stok"] <= ist["rop"] and not ist["acik_sinyal"]:
                    ist["acik_sinyal"] = True
                    ist["yenileme_dk"] = t + ist["lt_i"]
                    ist["sinyal_id_sayac"] += 1
                    sig_id = f"{sid}_{ist['sinyal_id_sayac']:03d}"

                    # Zaman pencereleri (K27 guard K30)
                    t_starv = t + (ist["stok"] / ist["D_dk"]) if ist["D_dk"] > 0 else t + 60
                    tw_bitis_ham = min(t_starv - 5.0, t + 60.0)
                    tw_bitis = max(tw_bitis_ham, t + ist["lt_i"])  # K30 guard

                    kritiklik = ist["rop"] / max(0.01, ist["stok"])  # K26

                    sinyaller.append({
                        "sinyal_id": sig_id,
                        "istasyon_id": sid,
                        "hat": ist["hat"],
                        "sinyal_dk": t,
                        "stok_o_an": round(ist["stok"], 3),
                        "rop_esigi": round(ist["rop"], 3),
                        "kritiklik_skoru": round(kritiklik, 4),
                        "tw_baslangic": t,
                        "tw_bitis": round(tw_bitis, 2),
                        "tw_genislik_dk": round(tw_bitis - t, 2),
                        "lt_dk": ist["lt_i"],
                        "istenen_kutu": 1,
                        "istenen_adet": int(ist["C"]),
                        "serviced": False,
                        "varis_dk": None,
                        "teslim_durumu": "KARŞILANAMADI"
                    })

        return pd.DataFrame(sinyaller)

    def solve_vrptw(self, signals_df: pd.DataFrame, arac_sayisi: int = 4, dispatch_kural: str = "EDD") -> tuple:
        """
        Değişken LT_i sinyalleri üzerinde VRPTW çözer.
        """
        vehicles = {
            f"A{i+1}": {"musait_dk": 0.0, "mevcut_konum": "0", "tur_sayisi": 0}
            for i in range(arac_sayisi)
        }

        pending_signals = signals_df.copy()
        rotalar = []
        rota_id_sayac = 1

        for t in range(481):
            active_mask = (pending_signals["tw_baslangic"] <= t) & (~pending_signals["serviced"])
            active_batch = pending_signals[active_mask]

            if active_batch.empty:
                continue

            available_v_id = None
            earliest_time = float("inf")
            for v_id, v_info in vehicles.items():
                if v_info["musait_dk"] <= t and v_info["musait_dk"] < earliest_time:
                    earliest_time = v_info["musait_dk"]
                    available_v_id = v_id

            if available_v_id is None:
                continue

            # Dispatch kuralına göre sıralama
            if dispatch_kural == "EDD":
                # Earliest Due Date: tw_bitis ↑
                sorted_batch = active_batch.sort_values(by=["tw_bitis"])
            elif dispatch_kural == "SLACK":
                # Minimum Slack: (tw_bitis - t - tahmini_yol) ↑
                active_batch = active_batch.copy()
                # Depodan istasyona tahmini seyahat süresi
                slack_vals = []
                for _, s_row in active_batch.iterrows():
                    s_node = s_row["istasyon_id"].replace("S", "")
                    tt = self.get_travel_time("0", s_node)
                    slack_vals.append(s_row["tw_bitis"] - t - tt)
                active_batch["_slack"] = slack_vals
                sorted_batch = active_batch.sort_values(by=["_slack"])
            elif dispatch_kural == "FIFO":
                sorted_batch = active_batch.sort_values(by=["tw_baslangic"])
            else:
                # KRITIKLIK
                sorted_batch = active_batch.sort_values(by=["kritiklik_skoru", "tw_bitis"], ascending=[False, True])

            selected_signals = []
            current_load = 0
            for idx, signal in sorted_batch.iterrows():
                demanded = int(signal["istenen_kutu"])
                if current_load + demanded <= self.Q_arac:
                    selected_signals.append(signal)
                    current_load += demanded
                    if len(selected_signals) >= 5:  # Max 5 durak/tur
                        break

            if not selected_signals:
                continue

            # Rota oluşturma: NN
            curr_node = "0"
            curr_time = float(t)
            unvisited = list(selected_signals)
            route_nodes = []

            while unvisited:
                best_next = None
                best_tt = float("inf")
                for candidate in unvisited:
                    cand_node = candidate["istasyon_id"].replace("S", "")
                    tt = self.get_travel_time(curr_node, cand_node)
                    if tt < best_tt:
                        best_tt = tt
                        best_next = candidate

                target_node = best_next["istasyon_id"].replace("S", "")
                arr_time = curr_time + best_tt
                dept_time = arr_time + self.bosaltma_sure

                sig_id = best_next["sinyal_id"]
                tw_end = best_next["tw_bitis"]
                teslim_durumu = "ZAMANINDA_TESLİM" if arr_time <= tw_end else "GECİKMELİ_TESLİM"

                pending_signals.loc[pending_signals["sinyal_id"] == sig_id, "serviced"] = True
                pending_signals.loc[pending_signals["sinyal_id"] == sig_id, "varis_dk"] = round(arr_time, 2)
                pending_signals.loc[pending_signals["sinyal_id"] == sig_id, "teslim_durumu"] = teslim_durumu

                route_nodes.append({
                    "rota_id": f"R{rota_id_sayac:03d}",
                    "arac_id": available_v_id,
                    "istasyon_id": best_next["istasyon_id"],
                    "node": target_node,
                    "istenen_kutu": best_next["istenen_kutu"],
                    "varis_dk": round(arr_time, 2),
                    "cikis_dk": round(dept_time, 2),
                    "teslim_durumu": teslim_durumu
                })

                unvisited = [s for s in unvisited if s["sinyal_id"] != sig_id]
                curr_node = target_node
                curr_time = dept_time

            return_tt = self.get_travel_time(curr_node, "0")
            tour_end = curr_time + return_tt
            vehicles[available_v_id]["musait_dk"] = tour_end
            vehicles[available_v_id]["tur_sayisi"] += 1
            rota_id_sayac += 1

            for rn in route_nodes:
                rotalar.append(rn)

        # Starvation hesabı
        starvations = self.simulate_starvation(pending_signals)
        return pd.DataFrame(rotalar), pending_signals, starvations

    def simulate_starvation(self, signals_df: pd.DataFrame) -> list:
        tuketim_pivot = self.consumption_df.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")
        
        stoklar = {}
        stoklar = {}
        ist_c = {}
        ist_cap = {}
        for _, row in self.stations_df.iterrows():
            sid = row["istasyon_id"]
            D_dk = float(row["ort_tuketim_saat"]) / 60.0
            lt_i = self.station_lt[sid]["lt_dk"]
            C_val = float(row["kutu_kapasitesi"])
            rop_i = D_dk * lt_i * (1 + self.ALPHA)
            n_i = math.ceil(rop_i / C_val)
            ist_c[sid] = C_val
            ist_cap[sid] = float(n_i * C_val)
            stoklar[sid] = float(n_i * C_val)  # Başlangıç stoku = N_i * C_i

        deliveries = {}
        serviced = signals_df[signals_df["serviced"] == True]
        for _, row in serviced.iterrows():
            if row["varis_dk"] is not None:
                arr_m = int(math.floor(row["varis_dk"]))
                deliveries.setdefault(arr_m, []).append((row["istasyon_id"], row["istenen_kutu"] * ist_c[row["istasyon_id"]]))

        starvation_events = []
        wip_records = []
        for m in range(480):
            # Teslimat ekle (Kanban kuralı: Stok asla N * C tavanını aşamaz)
            if m in deliveries:
                for sid, miktar in deliveries[m]:
                    stoklar[sid] = min(ist_cap[sid], stoklar[sid] + miktar)

            # Tüketim düş
            for sid in stoklar:
                c_val = tuketim_pivot.loc[m, sid] if m in tuketim_pivot.index and sid in tuketim_pivot.columns else 0.0
                stoklar[sid] -= c_val
                if stoklar[sid] <= 0:
                    starvation_events.append({"dakika": m, "istasyon_id": sid})
                    stoklar[sid] = 0.0

            wip_records.append(sum(stoklar.values()))

        avg_wip = np.mean(wip_records)
        return starvation_events, avg_wip


def main():
    loader = DataLoader()
    sim = VariableLTSimulator(loader)

    print("=" * 85)
    print("HAFTA 8: DEĞİŞKEN LEAD TIME (LT in [30, 60] dk) VE EDD vs SLACK ANALİZİ")
    print("=" * 85)

    # 1. İstasyon LT Dağılım Tablosu
    print("\n--- 1. İSTASYON BAZLI DEĞİŞKEN LT DAĞILIMI ---")
    lt_rows = []
    rop_toplam = 0.0
    for sid, info in sorted(sim.station_lt.items(), key=lambda x: int(x[0].replace("S", ""))):
        hat = sim.stations_df[sim.stations_df["istasyon_id"] == sid]["hat"].values[0]
        D_dk = float(sim.stations_df[sim.stations_df["istasyon_id"] == sid]["ort_tuketim_saat"].values[0]) / 60.0
        rop_val = D_dk * info["lt_dk"] * (1 + sim.ALPHA)
        rop_toplam += rop_val
        lt_rows.append({
            "İstasyon": sid, "Hat": hat, "Mesafe (m)": info["mesafe_m"], "Atanan LT (dk)": info["lt_dk"],
            "ROP (adet)": round(rop_val, 2), "Kaynak": "[Mühendislik Kararı - Min-Max Normalizasyon]"
        })
    lt_df = pd.DataFrame(lt_rows)
    print(lt_df.to_string(index=False))
    print(f"\nOrtalama İstasyon ROP Eşiği: {rop_toplam/24.0:.2f} adet (Sabit LT=45dk için 18.06 adetti) [Kod çıktısı]")

    # Sinyalleri üret
    signals = sim.uret_degisken_lt_sinyalleri()
    print(f"Toplam üretilen değişken LT sinyali: {len(signals)} adet [Kod çıktısı]")

    # 2. Kuralları Koş (2 ve 4 Araç)
    print("\n--- 2. DEĞİŞKEN LT ALTINDA DİSPATCH KURALLARI KARŞILAŞTIRMASI ---")
    results = []

    for arac in [2, 4]:
        for kural in ["KRITIKLIK", "FIFO", "EDD", "SLACK"]:
            rotalar, sig_out, (starvs, avg_wip) = sim.solve_vrptw(signals, arac_sayisi=arac, dispatch_kural=kural)
            
            toplam_starv_dk = len(starvs)
            warmup_starv_dk = len([s for s in starvs if s["dakika"] >= 45])
            
            # İkili payda hesabı (K47)
            pct_11520 = (toplam_starv_dk / 11520.0) * 100.0
            pct_10440 = (warmup_starv_dk / 10440.0) * 100.0
            
            zamaninda = len(sig_out[sig_out["teslim_durumu"] == "ZAMANINDA_TESLİM"])
            gecikmeli = len(sig_out[sig_out["teslim_durumu"] == "GECİKMELİ_TESLİM"])
            karsilanamayan = len(sig_out[sig_out["teslim_durumu"] == "KARŞILANAMADI"])
            karsilama_orani = ((zamaninda + gecikmeli) / len(sig_out)) * 100.0
            
            toplam_tur = rotalar["rota_id"].nunique() if len(rotalar) > 0 else 0

            results.append({
                "Araç Sayısı": f"{arac} Araç [K03/K37]",
                "Kural": kural,
                "Starv (dk)": toplam_starv_dk,
                "Starvation (11.520 Payda)": f"%{pct_11520:.2f} [Kod çıktısı]",
                "Starvation (10.440 Payda)": f"%{pct_10440:.2f} [Kod çıktısı]",
                "Ort WIP Stok (adet)": f"{avg_wip:.1f} [Kod çıktısı]",
                "Karşılama (%)": f"%{karsilama_orani:.1f} [Kod çıktısı]",
                "Zamanında": zamaninda,
                "Gecikmeli": gecikmeli,
                "Karşılanamayan": karsilanamayan,
                "Tur Sayısı": toplam_tur
            })

    res_df = pd.DataFrame(results)
    print(res_df.to_string(index=False))

    # CSV olarak kaydet
    out_path = os.path.join(loader.base_dir, "data", "synthetic", "hafta8_degisken_lt_sonuclari.csv")
    res_df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\nSonuçlar kaydedildi: {out_path}")


if __name__ == "__main__":
    main()
