"""
generate_dashboard_data_v2.py
=============================
Hafta 15 — Dashboard Veri Ambarının v2 Motoruyla Yeniden Üretilmesi (K92 / Kademe 1-D1)

Neden
-----
Mevcut `data/dashboard_scenarios.json` tamamen **v1 motorundan** üretilmiştir ve v2
düzeltmelerinden sonra geçersizdir (4 araç/α=0,15 için arayüz %24,58 gösterirken v2'de
%0,18'dir — 24,4 puan sapma). Bu betik ambarı v2 motoruyla yeniden üretir.

Arayüz uyumu
------------
`index.html` kontrollerinin aralıkları birebir karşılanır:
  sliderArac   1–8 (step 1)            → 8 değer
  sliderAlpha  0,05–0,30 (step 0,05)   → 6 değer
  sliderTalep  −20…+20 (step 10)       → 5 değer
  nModu        2 seçenek               → **yeni anlamı aşağıda**
  dispatch     EDD/SLACK/FIFO/KRİTİKLİK → 4 değer
Toplam 8×6×5×2×4 = 1920 konfigürasyon (v1 ile aynı sayıda, farklı anlamda).

⚠️ `n_modu` ALANININ YENİ ANLAMI (K92)
--------------------------------------
v1'de bu alan "Sabit N ↔ Dinamik N" (α'nın N'i güncelleyip güncellemediği) demekti.
v2'de **boyutlandırma yöntemini** gösterir ve tezin ana katkısını arayüze taşır:

    "Sabit_N"   → kanban_modu="V1"   : N = ⌈ROP/C⌉          (politika-tutarsız, eski)
    "Dinamik_N" → kanban_modu="VDI"  : N = 1 + ⌈ROP/C⌉      (politika-tutarlı, K65)

Böylece kullanıcı arayüzde iki boyutlandırma yöntemi arasında geçiş yapıp farkı
doğrudan görebilir.

Ek veri setleri
---------------
  statik_baz : P1 ve P2 politikaları (sabit takt) — karşılaştırma sekmesi için
  ablation   : v1→v2 düzeltmelerinin katkısı (v2_d45_ayristirma.csv)
  boyutlandirma : K93 duyarlılık deneyi
  adalet     : K97 dört adalet kuralı (mevcut + Toyota kutuları)
  saglamlik  : K95–K101 sağlamlık testleri özeti
  dogrulama  : Solomon, Welch ısınma, replikasyon yeterliliği özetleri
  meta       : motor sürümü, üretim tarihi, replikasyon sayısı

Kullanım
--------
    python -X utf8 -m src.generate_dashboard_data_v2
    python -X utf8 -m src.generate_dashboard_data_v2 --rep 5
"""

import argparse
import json
import math
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

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARACLAR = [1, 2, 3, 4, 5, 6, 7, 8]
ALFALAR = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
TALEP_SOK = [-20, -10, 0, 10, 20]
N_MODLARI = [("Dinamik_N", "VDI"), ("Sabit_N", "V1")]
DISPATCH = ["EDD", "SLACK", "FIFO", "KRITIKLIK"]
TUR_ARALIKLARI = [30, 60, 90, 120]


def _ort(veri, p, rep, seed0):
    tek = [calistir(replace(p, seed=seed0 + r), veri) for r in range(rep)]
    out = {}
    for k in ("starv_pct", "ort_wip", "toplam_mesafe_km", "tur_sayisi",
              "doluluk_pct", "toplam_kart", "arac_kullanim_pct", "ort_tur_sure_dk"):
        v = [t[k] for t in tek]
        out[k] = float(np.mean(v))
    sv = [t["starv_pct"] for t in tek]
    out["starv_ci95"] = (1.96 * float(np.std(sv, ddof=1)) / np.sqrt(rep)) if rep > 1 else 0.0
    out["starv_dk"] = float(np.mean([t["starv_dk"] for t in tek]))
    return out


def uret_senaryolar(veri: V2Veri, rep: int) -> list:
    """Ana ızgara — P3 (olay tabanlı dinamik, konsolidasyonlu sevk)."""
    toplam = len(ARACLAR) * len(ALFALAR) * len(TALEP_SOK) * len(N_MODLARI) * len(DISPATCH)
    print(f"  Ana ızgara (P3): {toplam} konfigürasyon × {rep} replikasyon "
          f"= {toplam * rep} koşu")
    kayit, i, t0 = [], 0, time.perf_counter()
    for m in ARACLAR:
        for a in ALFALAR:
            for sok in TALEP_SOK:
                for n_etiket, mod in N_MODLARI:
                    for disp in DISPATCH:
                        p = V2Parametre(politika="P3", sevk="KONSOLIDASYON",
                                        dispatch_kural=disp, arac_sayisi=m, alpha=a,
                                        talep_carpani=1.0 + sok / 100.0,
                                        kanban_modu=mod, talep_modeli="SAATLIK_REJIM")
                        r = _ort(veri, p, rep, seed0=21000)
                        kayit.append({
                            "politika": "P3", "arac_sayisi": m, "alpha": a,
                            "talep_sok_pct": sok, "talep_faktor": round(1 + sok / 100, 2),
                            "dispatch_kural": disp, "n_modu": n_etiket,
                            "kanban_modu": mod,
                            "starv_pct": round(r["starv_pct"], 3),
                            "starv_ci95": round(r["starv_ci95"], 3),
                            "starv_dk": round(r["starv_dk"], 1),
                            "ort_wip": round(r["ort_wip"], 1),
                            "sefer_sayisi": round(r["tur_sayisi"], 1),
                            "mesafe_km": round(r["toplam_mesafe_km"], 2),
                            "doluluk_pct": round(r["doluluk_pct"], 1),
                            "toplam_kart": int(round(r["toplam_kart"])),
                            "arac_kullanim_pct": round(r["arac_kullanim_pct"], 1),
                        })
                        i += 1
                        if i % 240 == 0:
                            hiz = i / (time.perf_counter() - t0)
                            print(f"    [{i}/{toplam}]  {hiz:.0f} konf/sn  "
                                  f"kalan ≈ {(toplam - i) / hiz / 60:.1f} dk")
    return kayit


def uret_statik_baz(veri: V2Veri, rep: int) -> list:
    """P1 ve P2 (sabit takt) — karşılaştırma sekmesi için."""
    toplam = 2 * len(TUR_ARALIKLARI) * len(ARACLAR) * len(TALEP_SOK) * len(N_MODLARI)
    print(f"  Statik baz (P1/P2): {toplam} konfigürasyon × {rep} replikasyon")
    kayit, i = [], 0
    for pol in ("P1", "P2"):
        for T in TUR_ARALIKLARI:
            for m in ARACLAR:
                for sok in TALEP_SOK:
                    for n_etiket, mod in N_MODLARI:
                        p = V2Parametre(politika=pol, tur_araligi_dk=T, arac_sayisi=m,
                                        alpha=0.15, talep_carpani=1.0 + sok / 100.0,
                                        kanban_modu=mod, talep_modeli="SAATLIK_REJIM")
                        r = _ort(veri, p, rep, seed0=31000)
                        kayit.append({
                            "politika": pol, "tur_araligi_dk": T, "arac_sayisi": m,
                            "talep_sok_pct": sok, "n_modu": n_etiket,
                            "starv_pct": round(r["starv_pct"], 3),
                            "starv_ci95": round(r["starv_ci95"], 3),
                            "ort_wip": round(r["ort_wip"], 1),
                            "sefer_sayisi": round(r["tur_sayisi"], 1),
                            "mesafe_km": round(r["toplam_mesafe_km"], 2),
                            "doluluk_pct": round(r["doluluk_pct"], 1),
                            "toplam_kart": int(round(r["toplam_kart"])),
                        })
                        i += 1
                        if i % 160 == 0:
                            print(f"    [{i}/{toplam}]")
    return kayit


def _csv_oku(ad: str):
    yol = os.path.join(KOK, "data", "synthetic", ad)
    if not os.path.exists(yol):
        return None
    return pd.read_csv(yol).to_dict(orient="records")


def dogrulama_ozeti() -> dict:
    out = {}
    sol = _csv_oku("solomon_dogrulama_sonuclari.csv")
    if sol:
        df = pd.DataFrame(sol)
        out["solomon"] = {
            "ornek_sayisi": len(df),
            "nn_ed_ort": round(float(df["NN_ed_pct"].mean()), 2),
            "nn2opt_ed_ort": round(float(df["NN2opt_ed_pct"].mean()), 2),
            "referans": "OR-Tools (Balikos vd. 2025 s.435-437 yaklaşımı)",
        }
    d1 = _csv_oku("v2_d1_tur_ici_optimallik.csv")
    if d1:
        df = pd.DataFrame(d1)
        out["tur_ici_optimallik"] = {
            "nn_sapma_ort": round(float(df["nn_ed_pct"].mean()), 2),
            "nn2opt_sapma_ort": round(float(df["nn2opt_ed_pct"].mean()), 2),
            "orneklem": len(df),
        }
    d3 = _csv_oku("v2_d3_replikasyon.csv")
    if d3:
        out["replikasyon"] = {"mutlak_olcut_n": 9, "esik_puan": 0.05}
    out["isinma_dk"] = 90
    out["isinma_yontemi"] = "Welch grafik yöntemi (Herrera-Vidal vd. 2026 s.9)"
    w = _csv_oku("v2_d2_welch_isinma.csv")
    if w:
        df = pd.DataFrame(w)
        df = df[df["dakika"] % 5 == 0]
        out["welch"] = [{"konfig": r["konfig"], "dakika": int(r["dakika"]), "wip_ma": round(float(r["wip_ma"]), 1),
                         "kararli_dk": int(r["kararli_dk"]), "kararli_wip": round(float(r["kararli_wip"]), 1)}
                        for _, r in df.iterrows()]
    if d3:
        out["replikasyon_seri"] = [{"replikasyon": int(r["replikasyon"]), "starv_pct": round(float(r["starv_pct"]), 4)}
                                   for r in d3]
    return out


def saglamlik_ozeti() -> list:
    """Hafta 15 sağlamlık testleri: K93 kayması ve sıralama değişimi koşullar boyunca (K95–K101)."""
    out = []

    def ekle(kod, ad, df_satir, kayma_alan="kayma", sira_alan="siralama_degisti", not_=""):
        if not df_satir:
            return
        df = pd.DataFrame(df_satir)
        out.append({
            "kod": kod, "test": ad, "kosul": len(df),
            "kayma_pozitif": int((df[kayma_alan] > 0).sum()),
            "kayma_min": round(float(df[kayma_alan].min()), 2),
            "kayma_max": round(float(df[kayma_alan].max()), 2),
            "siralama_degisti": int(df[sira_alan].astype(str).str.lower().isin(["true", "1"]).sum()),
            "not": not_,
        })

    ekle("K95", "Toyota formülü bandı (α × kutu boyu × talep)", _csv_oku("v2_toyota_bandi_ozet.csv"),
         not_="Toyota bandında etki büyür; sıralama 12/12 bant hücresinde değişir")
    ekle("K99", "Ufuk (480 / 1440 dk) × gösterge (ısınma dahil / hariç)", _csv_oku("v2_cok_vardiya_ozet.csv"),
         not_="Mevcut kutularda fark %90–95 küçülür; Toyota kutularında sıralama her koşulda değişir")
    ekle("K100", "Mesafe ağı (mevcut matris / koordinat tabanlı)", _csv_oku("v2_koordinat_agi_ozet.csv"),
         not_="Koordinat ağında Vojdani ile aynı yön: dijital daha az sefer ve yol")
    oz = _csv_oku("v2_ortools_referansi_ozet.csv")
    if oz:
        df = pd.DataFrame(oz)
        out.append({"kod": "K101", "test": "Rotalama: çevrimdışı tam bilgi referansı (OR-Tools)",
                    "kosul": len(df), "kayma_pozitif": None, "kayma_min": None, "kayma_max": None,
                    "siralama_degisti": None,
                    "not": "Baz/konsolidasyon: sezgisel %62–69 fazla yol, daha az gecikme; şokta referans "
                           "94–121 teslimi geciktirir. Kanıtlanmış alt sınır değildir."})
    return out


def adalet_ozeti() -> dict:
    """K97 dört adalet kuralı: eğriler, kural noktaları ve kazananlar (mevcut + Toyota kutuları)."""
    out = {}
    for ek, kutu in (("", "mevcut"), ("_toyota", "toyota")):
        e = _csv_oku(f"v2_adalet_egriler{ek}.csv")
        k = _csv_oku(f"v2_adalet_kurallar{ek}.csv")
        z = _csv_oku(f"v2_adalet_kazanan{ek}.csv")
        if not (e and k and z):
            continue
        alan = ("talep", "sistem", "k", "starv_pct", "starv_pct_ci95", "ort_wip", "toplam_kart")
        out[kutu] = {
            "egriler": [{a: r[a] for a in alan} for r in e if r["nokta"] != "iki_kutu"],
            "kurallar": k,
            "kazanan": z,
        }
    return out


def _nan_temizle(o):
    """NaN/inf → None: json.dump bunları geçersiz JSON olarak yazar ve fetch().json() kırılır."""
    if isinstance(o, float):
        return None if (math.isnan(o) or math.isinf(o)) else o
    if isinstance(o, dict):
        return {k: _nan_temizle(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_nan_temizle(v) for v in o]
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=3,
                    help="konfigürasyon başına replikasyon (varsayılan 3)")
    args = ap.parse_args()

    veri = V2Veri()
    print("=" * 78)
    print("DASHBOARD VERİ AMBARI — v2 MOTORU (K92 / Kademe 1-D1)")
    print(f"  Replikasyon: {args.rep} · Talep modeli: saatlik rejim · Isınma: 90 dk")
    print("=" * 78)

    t0 = time.perf_counter()
    senaryolar = uret_senaryolar(veri, args.rep)
    statik = uret_statik_baz(veri, args.rep)
    sure = time.perf_counter() - t0

    ambar = {
        "meta": {
            "motor": "v2 (src/v2_entegre_simulasyon.py)",
            "uretim_tarihi": time.strftime("%Y-%m-%d"),
            "replikasyon": args.rep,
            "isinma_dk": 90,
            "talep_modeli": "SAATLIK_REJIM (CV=0.20 saatlik düzeyde)",
            "mesafe_modu": "METRIK (Floyd-Warshall kapanışı, K71)",
            "n_modu_anlami": {
                "Dinamik_N": "VDI — politika-tutarlı boyutlandırma: N = 1 + ⌈ROP/C⌉ (K65)",
                "Sabit_N": "V1 — eski boyutlandırma: N = ⌈ROP/C⌉",
            },
            "not": ("Değerler ortalama ± %95 güven aralığıdır. Sevk kuralları arasında "
                    "istatistiksel fark bulunamamıştır (ANOVA p=0,9997 / 0,3415 — K82)."),
            "senaryo_sayisi": len(senaryolar),
            "statik_baz_sayisi": len(statik),
            "uretim_suresi_sn": round(sure, 1),
        },
        "senaryolar": senaryolar,
        "statik_baz": statik,
        "ablation": _csv_oku("v2_d45_ayristirma.csv") or [],
        "boyutlandirma": _csv_oku("v2_boyutlandirma_duyarliligi.csv") or [],
        "kpi_uyumu": _csv_oku("v2_kpi_uyumu.csv") or [],
        "vaka": _csv_oku("v2_vaka_calismasi.csv") or [],
        "dogrulama": dogrulama_ozeti(),
        "adalet": adalet_ozeti(),
        "saglamlik": saglamlik_ozeti(),
    }
    ambar = _nan_temizle(ambar)

    cikti_dizin = os.path.join(KOK, "data")
    json_yol = os.path.join(cikti_dizin, "dashboard_scenarios_v2.json")
    with open(json_yol, "w", encoding="utf-8") as f:
        json.dump(ambar, f, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    pd.DataFrame(senaryolar).to_csv(
        os.path.join(cikti_dizin, "dashboard_scenarios_v2.csv"),
        index=False, encoding="utf-8")

    boyut = os.path.getsize(json_yol) / 1024
    print(f"\n  ✅ {len(senaryolar)} senaryo + {len(statik)} statik baz")
    print(f"     data/dashboard_scenarios_v2.json  ({boyut:.0f} KB)")
    print(f"     data/dashboard_scenarios_v2.csv")
    print(f"     Üretim süresi: {sure / 60:.1f} dakika")

    df = pd.DataFrame(senaryolar)
    print("\n  ── ÖRNEK: 4 araç, α=0,15, baz talep, EDD ──")
    for n_etiket, mod in N_MODLARI:
        r = df[(df.arac_sayisi == 4) & (df.alpha == 0.15) & (df.talep_sok_pct == 0)
               & (df.dispatch_kural == "EDD") & (df.n_modu == n_etiket)].iloc[0]
        print(f"     {n_etiket:10s} ({mod:3s}) → duruş %{r['starv_pct']:5.2f} "
              f"± {r['starv_ci95']:.2f} | WIP {r['ort_wip']:6.1f} | "
              f"kart {r['toplam_kart']:3d} | sefer {r['sefer_sayisi']:5.1f}")
    print("     (v1 ambarı aynı konfigürasyon için %24,58 gösteriyordu)")


if __name__ == "__main__":
    main()
