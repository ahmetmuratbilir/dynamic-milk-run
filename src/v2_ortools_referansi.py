"""
v2_ortools_referansi.py
=======================
Hafta 15 — Fabrika senaryosunda rotalama sezgiselinin çevrimdışı tam bilgi referansına uzaklığı (H5, K101)

Sorun
-----
Solomon kıyaslamasında sezgisel (NN + 2-opt, sevk kuralıyla tur-arası atama) OR-Tools'tan
%102,7 geridedir (S8). Ancak Solomon 100 müşterili statik problemdir; fabrika içi turlar
2–8 duraklı ve çevrimiçidir. Hakem sorusu: "Fabrika senaryosunda rotalamanız ne kadar iyi?"

Yöntem — gevşetilmiş çevrimdışı problem (referans)
---------------------------------------------------
Bir P3 koşusunda oluşan tüm siparişler (istasyon, sinyal zamanı, son teslim, kutu)
kaydedilir ve OR-Tools ile ÇEVRİMDIŞI VRPTW olarak çözülür:
  · her sipariş bir düğümdür (istasyon konumunda), talep = kutu, Q = araç kapasitesi
  · zaman penceresi [t_sinyal + yükleme + depo→istasyon süresi, tw_bitis], yumuşak üst
    sınır (gecikme dakika başına ceza = motorla aynı, gecikme_ceza = 10)
  · servis süresi = durak başına boşaltma (3 dk); seyahat süresi = mesafe / hız

Gevşetmeler (çevrimiçi politikaya göre problemi KOLAYLAŞTIRIR):
  (1) siparişler önceden bilinir (çevrimiçi değil)
  (2) filo eşzamanlılığı kaldırılır: rota sayısı sınırsız sanal araçla temsil edilir
      (3 araçla aynı anda en fazla 3 tur kısıtı yoktur)
  (3) araç depodan siparişin sinyal zamanından önce çıkmış olabilir
Motorla aynı tur süresi kısıtı (max_tur_dk = 90, K72) korunur; bu olmadan sanal bir araç
bir istasyonda bekleyip ardışık siparişleri sıfır mesafeyle toplayabilir.
⚠️ OR-Tools GLS sezgiseldir ve süre sınırında yakınsamayabilir; sonuç KANITLANMIŞ bir
alt sınır değildir. Gevşetilmiş problemin gerçek optimumu raporlanan değerden de düşük
olabilir; bu yüzden raporlanan açık, sezgiselin çevrimdışı tam bilgiye göre geride
kaldığı miktarın gösterge niteliğindeki bir tahminidir. Referans mesafeyi gecikmeyle
takas edebileceği için mesafe ve gecikmeli teslim sayısı birlikte raporlanır. Not: sipariş akışı politikanın kendisine bağlıdır (sinyaller
stok düzeyinden doğar); sınır, gözlenen sipariş akışı sabit tutularak hesaplanır.

Kullanım
--------
    python -X utf8 -m src.v2_ortools_referansi
    python -X utf8 -m src.v2_ortools_referansi --sure 30 --rep 5
"""

import argparse
import os
import sys
import time
from dataclasses import replace

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir
from src.v2_koordinat_agi import aglar

TALEPLER = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]
SEVKLER = ["KONSOLIDASYON", "ANINDA"]
OL = 100   # tamsayı ölçekleme (OR-Tools)


def cevrimdisi_coz(sip, veri, p, sure_sn):
    from ortools.constraint_solver import pywrapcp, routing_enums_pb2
    mesafe = veri.mesafe_metrik if p.mesafe_modu == "METRIK" else veri.mesafe_ham
    hiz = veri.hiz_m_dk / p.hiz_carpani
    dugum = [0] + [int(veri.node[s["i"]]) for s in sip]          # 0 = depo
    n = len(dugum)
    D = mesafe[np.ix_(dugum, dugum)]
    S = D / hiz
    servis = np.array([0.0] + [p.durak_servis_dk] * (n - 1))
    talep = np.array([0] + [int(s["kutu"]) for s in sip])
    arac = n - 1                                                  # gevşetme (2): sınırsız rota
    yon = pywrapcp.RoutingIndexManager(n, arac, 0)
    model = pywrapcp.RoutingModel(yon)

    Di = np.rint(D * OL).astype(np.int64)
    Ti = np.rint((S + servis[:, None]) * OL).astype(np.int64)
    Ti[0, :] += int(round(p.yukleme_dk * OL))                     # depoda yükleme
    m_idx = model.RegisterTransitCallback(lambda i, j: int(Di[yon.IndexToNode(i), yon.IndexToNode(j)]))
    model.SetArcCostEvaluatorOfAllVehicles(m_idx)
    t_idx = model.RegisterTransitCallback(lambda i, j: int(Ti[yon.IndexToNode(i), yon.IndexToNode(j)]))
    ufuk = int((p.sim_sure + 600) * OL)
    model.AddDimension(t_idx, ufuk, ufuk, False, "Time")
    zaman = model.GetDimensionOrDie("Time")
    # gecikme cezası mesafe birimine çevrilir: motorun 2-opt maliyetindeki ağırlıkla aynı oran
    ceza = int(round(p.gecikme_ceza * hiz))                       # dk gecikme ↔ m
    for k in range(1, n):
        s = sip[k - 1]
        idx = yon.NodeToIndex(k)
        en_erken = s["t_sinyal"] + p.yukleme_dk + S[0, k]         # gevşetme (3)
        zaman.CumulVar(idx).SetMin(int(np.floor(en_erken * OL)))
        zaman.SetCumulVarSoftUpperBound(idx, int(np.ceil(s["tw_bitis"] * OL)), ceza)
    # K72 ile aynı tur süresi kısıtı: sınırsız sanal aracın bir istasyonda saatlerce bekleyip
    # ardışık siparişleri sıfır mesafeyle toplamasını engeller (aksi hâlde sınır anlamsızlaşır)
    if p.max_tur_dk is not None:
        for v in range(arac):
            zaman.SetSpanUpperBoundForVehicle(int(p.max_tur_dk * OL), v)
    k_idx = model.RegisterUnaryTransitCallback(lambda i: int(talep[yon.IndexToNode(i)]))
    model.AddDimensionWithVehicleCapacity(k_idx, 0, [int(veri.Q)] * arac, True, "Cap")

    par = pywrapcp.DefaultRoutingSearchParameters()
    par.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    par.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    par.time_limit.FromSeconds(sure_sn)
    coz = model.SolveWithParameters(par)
    if coz is None:
        return None
    toplam, rota, gec = 0.0, 0, 0
    for v in range(arac):
        idx = model.Start(v)
        if model.IsEnd(coz.Value(model.NextVar(idx))):
            continue
        rota += 1
        while not model.IsEnd(idx):
            nx = coz.Value(model.NextVar(idx))
            toplam += D[yon.IndexToNode(idx), yon.IndexToNode(nx)]
            idx = nx
    for k in range(1, n):
        varis = coz.Value(zaman.CumulVar(yon.NodeToIndex(k))) / OL
        gec += int(varis > sip[k - 1]["tw_bitis"] + 1e-6)
    return {"mesafe_km": toplam / 1000, "rota": rota, "gecikmeli": gec}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sure", type=int, default=30, help="OR-Tools süre sınırı (sn)")
    ap.add_argument("--rep", type=int, default=3)
    ap.add_argument("--arac", type=int, default=3)
    args = ap.parse_args()
    try:
        import ortools  # noqa: F401
    except ImportError:
        sys.exit("ortools kurulu değil: python -m pip install ortools")

    temel = V2Veri()
    ag, _ = aglar(temel)
    secili = {"MEVCUT_METRIK": ag["MEVCUT_METRIK"], "KOMPAKT": ag["KOMPAKT"]}
    print("=" * 96)
    print("FABRİKA SENARYOSUNDA ROTALAMA: ÇEVRİMDIŞI TAM BİLGİ REFERANSI (H5 / K101)")
    print(f"  Gevşetilmiş çevrimdışı VRPTW (OR-Tools GLS, {args.sure} sn) · P3 · "
          f"{args.arac} araç · {args.rep} tohum")
    print("=" * 96)

    satir = []
    for ag_ad, veri in secili.items():
        for talep_ad, talep in TALEPLER:
            for sevk in SEVKLER:
                for r in range(args.rep):
                    p = V2Parametre(politika="P3", sevk=sevk, arac_sayisi=args.arac,
                                    talep_carpani=talep, seed=11000 + r, zaman_serisi=True)
                    s = calistir(p, veri)
                    sip = s["_siparisler"]
                    t0 = time.perf_counter()
                    o = cevrimdisi_coz(sip, veri, p, args.sure)
                    if o is None:
                        print(f"  ✗ çözüm yok: {ag_ad} {talep_ad} {sevk} tohum {r}")
                        continue
                    satir.append({
                        "ag": ag_ad, "talep": talep_ad, "sevk": sevk, "tohum": r,
                        "siparis": len(sip), "sez_km": s["toplam_mesafe_km"],
                        "sez_tur": s["tur_sayisi"], "sez_gecikmeli": s["gecikmeli"],
                        "ort_km": o["mesafe_km"], "ort_rota": o["rota"],
                        "ort_gecikmeli": o["gecikmeli"], "cozum_sn": time.perf_counter() - t0,
                    })
                print(f"  ✓ {ag_ad:14s} · {talep_ad:16s} · {sevk}")

    df = pd.DataFrame(satir)
    df["acik_pct"] = 100 * (df["sez_km"] / df["ort_km"] - 1)
    oz = (df.groupby(["ag", "talep", "sevk"], sort=False)
            .agg(siparis=("siparis", "mean"), sez_km=("sez_km", "mean"), ort_km=("ort_km", "mean"),
                 acik_pct=("acik_pct", "mean"), acik_min=("acik_pct", "min"), acik_max=("acik_pct", "max"),
                 sez_tur=("sez_tur", "mean"), ort_rota=("ort_rota", "mean"),
                 sez_gec=("sez_gecikmeli", "mean"), ort_gec=("ort_gecikmeli", "mean"))
            .reset_index())

    print(f"\n{'═' * 96}")
    print(f"  {'Ağ':14s} {'Talep':16s} {'Sevk':14s} {'sipariş':>7s} {'sezgisel':>9s} {'referans':>9s} "
          f"{'açık %':>16s} {'tur/rota':>10s} {'gecikme':>9s}")
    for _, r in oz.iterrows():
        print(f"  {r['ag']:14s} {r['talep']:16s} {r['sevk']:14s} {r['siparis']:7.0f} "
              f"{r['sez_km']:8.1f}k {r['ort_km']:8.1f}k "
              f"{r['acik_pct']:+6.1f} ({r['acik_min']:+.0f}…{r['acik_max']:+.0f}) "
              f"{r['sez_tur']:4.0f}/{r['ort_rota']:<4.0f} {r['sez_gec']:4.1f}/{r['ort_gec']:<4.1f}")
    print("  açık % = sezgisel mesafesinin çevrimdışı tam bilgi referansına göre fazlası; "
          "gecikme = gecikmeli teslim sayısı (sezgisel/referans)")

    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    df.to_csv(os.path.join(cikti, "v2_ortools_referansi_ham.csv"), index=False, encoding="utf-8-sig")
    oz.to_csv(os.path.join(cikti, "v2_ortools_referansi_ozet.csv"), index=False, encoding="utf-8-sig")
    print("\n  → data/synthetic/v2_ortools_referansi_{ham,ozet}.csv")


if __name__ == "__main__":
    main()
