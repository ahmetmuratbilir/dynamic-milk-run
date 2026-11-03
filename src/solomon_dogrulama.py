"""
solomon_dogrulama.py
====================
Hafta 14 — Rotalama Sezgiselinin Solomon VRPTW Kıyaslama Setiyle Doğrulanması (K76)

Amaç
----
Projede kullanılan rota kurma sezgiselinin (en yakın komşu; v2'de + 2-opt) çözüm
kalitesini bağımsız bir kıyaslama setinde ölçmek. Tez/makale metodoloji bölümünün
"modelin güvenilirliği" iddiası bu tabloya dayanır.

Neden gerekli
-------------
Gendreau & Tarantilis (2010, CIRRELT-2010-04, s.2–3): Solomon (1987) veri setleri
VRPTW yazınının standart orta ölçekli kıyaslama setidir; büyük ölçek için Gehring &
Homberger (1999) kullanılır. 2-Opt ve Or-Opt komşuluk yapıları aynı çalışmanın
Bölüm 1.1'inde tanımlanır (projede 2-opt atfı bu kaynağa düzeltilmiştir — K34 errata).

Referans çözücü seçimi
----------------------
SINTEF'in yayımladığı BKS tabloları sayfa içinde JavaScript ile yüklendiğinden
programatik olarak güvenilir biçimde alınamamıştır. BKS değerlerini ikincil
kaynaklardan elle aktarmak hata riski taşıdığı için bu çalışmada Balikos vd. (2025,
"Google's VRP Free Algorithm Evaluation Study", s.435–437) yaklaşımı izlenmiştir:
OR-Tools referans çözücü olarak kullanılır. Anılan çalışma OR-Tools'u Solomon'un 25,
50 ve 100 müşterili örneklerinde 60 sn süre sınırıyla test etmiş, sapmayı
    e_d = 100 · (v_c − v_k) / v_k
formülüyle ölçmüş ve ortalama sapmayı bilinen en iyi çözümlere göre %10'un altında
bulmuştur (s.437). Dolayısıyla OR-Tools'a göre ölçülen sapmaya bu mertebede bir
dolaylı BKS payı eklenmelidir; rapor metninde bu sınırlılık açıkça belirtilir.

Deney tasarımı
--------------
  Örnekler : C101, C201, R101, R201, RC101, RC201  (kümelenmiş / rastgele / karma)
  Boyutlar : 25 ve 50 müşteri (Solomon konvansiyonu: 100'lük dosyanın ilk n müşterisi)
  Çözücüler: NN (v1 mantığı) | NN+2opt (v2) | OR-Tools (referans, PATH_CHEAPEST_ARC
             + guided local search, 60 sn)
  Kısıtlar : kesin zaman penceresi, araç kapasitesi, servis süreleri
  Amaç     : önce araç sayısı, sonra toplam mesafe (Gendreau & Tarantilis s.3;
             Wang vd. 2008 s.355–358 amaç hiyerarşisi)

Kullanım
--------
    python -m src.solomon_dogrulama                 # indirir, çözer, CSV+MD yazar
    python -m src.solomon_dogrulama --sure 10       # OR-Tools süre sınırı (sn)
"""

import argparse
import io
import math
import os
import sys
import time
import urllib.request
import zipfile

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Windows konsolu varsayilan olarak cp1254 kullanir; Turkce ve ok karakterleri icin UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SOLOMON_URL = "https://www.sintef.no/globalassets/project/top/vrptw/solomon/solomon-100.zip"
ORNEKLER = ["C101", "C201", "R101", "R201", "RC101", "RC201"]
BOYUTLAR = [25, 50]


# ─────────────────────────────────────────────────────────────
# Örnek okuma
# ─────────────────────────────────────────────────────────────
def solomon_indir(klasor: str) -> str:
    """solomon-100.zip'i indirip açar; açılmış klasörü döner (bir kez indirir)."""
    hedef = os.path.join(klasor, "solomon")
    if os.path.isdir(hedef) and len(os.listdir(hedef)) > 0:
        return hedef
    os.makedirs(klasor, exist_ok=True)
    req = urllib.request.Request(SOLOMON_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        ham = r.read()
    with zipfile.ZipFile(io.BytesIO(ham)) as z:
        z.extractall(hedef)
    return hedef


def solomon_oku(klasor: str, ad: str, n_musteri: int) -> dict:
    """Solomon metin formatını okur; ilk n müşteriyi alır (0 = depo)."""
    yol = None
    for kok, _, dosyalar in os.walk(klasor):
        for d in dosyalar:
            if d.lower() == ad.lower() + ".txt":
                yol = os.path.join(kok, d)
    if yol is None:
        raise FileNotFoundError(f"Solomon örneği bulunamadı: {ad}")

    satirlar = [s.strip() for s in open(yol, encoding="utf-8", errors="replace")]
    i_arac = next(i for i, s in enumerate(satirlar) if s.upper().startswith("VEHICLE"))
    arac_sayisi, kapasite = (int(x) for x in satirlar[i_arac + 2].split()[:2])
    i_must = next(i for i, s in enumerate(satirlar) if s.upper().startswith("CUSTOMER"))

    kayit = []
    for s in satirlar[i_must + 2:]:
        p = s.split()
        if len(p) >= 7:
            kayit.append([float(x) for x in p[:7]])
        if len(kayit) > n_musteri:
            break
    a = np.array(kayit[:n_musteri + 1])
    return {"ad": ad, "n": n_musteri, "arac_ust_sinir": arac_sayisi, "Q": float(kapasite),
            "x": a[:, 1], "y": a[:, 2], "talep": a[:, 3],
            "tw_bas": a[:, 4], "tw_bit": a[:, 5], "servis": a[:, 6]}


def mesafe_matrisi(ins: dict) -> np.ndarray:
    dx = ins["x"][:, None] - ins["x"][None, :]
    dy = ins["y"][:, None] - ins["y"][None, :]
    return np.sqrt(dx ** 2 + dy ** 2)


# ─────────────────────────────────────────────────────────────
# Kendi sezgiselimiz (projedeki rota kurma mantığı)
# ─────────────────────────────────────────────────────────────
def _rota_uygun_mu(rota, D, ins):
    """Kesin TW + kapasite kontrolü. Döner: (uygun mu, toplam mesafe, dönüş zamanı)."""
    if sum(ins["talep"][i] for i in rota) > ins["Q"] + 1e-9:
        return False, 0.0, 0.0
    t, konum, mesafe = 0.0, 0, 0.0
    for i in rota:
        t += D[konum, i]
        mesafe += D[konum, i]
        if t > ins["tw_bit"][i] + 1e-9:
            return False, 0.0, 0.0
        t = max(t, ins["tw_bas"][i]) + ins["servis"][i]
        konum = i
    t += D[konum, 0]
    mesafe += D[konum, 0]
    if t > ins["tw_bit"][0] + 1e-9:          # depo kapanışı (tur süresi üst sınırı)
        return False, 0.0, 0.0
    return True, mesafe, t


def _iki_opt(rota, D, ins):
    """2-opt: yalnızca uygun ve mesafeyi kısaltan hamleler kabul edilir
    (Gendreau & Tarantilis 2010, Bölüm 1.1)."""
    uy, en_iyi_m, _ = _rota_uygun_mu(rota, D, ins)
    if not uy:
        return rota, None
    en_iyi = list(rota)
    iyilesti = True
    while iyilesti:
        iyilesti = False
        for i in range(len(en_iyi) - 1):
            for j in range(i + 1, len(en_iyi)):
                aday = en_iyi[:i] + en_iyi[i:j + 1][::-1] + en_iyi[j + 1:]
                uy2, m2, _ = _rota_uygun_mu(aday, D, ins)
                if uy2 and m2 < en_iyi_m - 1e-9:
                    en_iyi, en_iyi_m, iyilesti = aday, m2, True
    return en_iyi, en_iyi_m


def coz_en_yakin_komsu(ins: dict, D: np.ndarray, iki_opt: bool) -> dict:
    """
    Ardışık rota kurma (sequential route construction): boş rotadan başla, kesin TW ve
    kapasiteye uyan en yakın müşteriyi ekle; uyan kalmazsa yeni rota aç.
    Projedeki en yakın komşu mantığının Solomon kısıtlarına uyarlanmış hâli.
    """
    t0 = time.perf_counter()
    kalan = set(range(1, ins["n"] + 1))
    rotalar, toplam = [], 0.0
    while kalan:
        rota, konum, t, yuk = [], 0, 0.0, 0.0
        while True:
            aday, en_iyi = None, math.inf
            for j in kalan:
                if yuk + ins["talep"][j] > ins["Q"] + 1e-9:
                    continue
                varis = t + D[konum, j]
                if varis > ins["tw_bit"][j] + 1e-9:
                    continue
                if not _rota_uygun_mu(rota + [j], D, ins)[0]:
                    continue
                if D[konum, j] < en_iyi:
                    aday, en_iyi = j, D[konum, j]
            if aday is None:
                break
            rota.append(aday)
            kalan.remove(aday)
            t = max(t + D[konum, aday], ins["tw_bas"][aday]) + ins["servis"][aday]
            yuk += ins["talep"][aday]
            konum = aday
        if not rota:                       # hiçbir müşteri eklenemedi: kısıt ihlali
            return {"basarili": False, "sure_sn": time.perf_counter() - t0}
        if iki_opt and len(rota) > 2:
            rota, _ = _iki_opt(rota, D, ins)
        toplam += _rota_uygun_mu(rota, D, ins)[1]
        rotalar.append(rota)
    return {"basarili": True, "arac": len(rotalar), "mesafe": toplam,
            "sure_sn": time.perf_counter() - t0}


# ─────────────────────────────────────────────────────────────
# OR-Tools referansı
# ─────────────────────────────────────────────────────────────
def coz_ortools(ins: dict, D: np.ndarray, sure_sn: int, arac: int) -> dict:
    from ortools.constraint_solver import pywrapcp, routing_enums_pb2
    t0 = time.perf_counter()
    OL = 100  # tamsayı ölçekleme
    n = ins["n"] + 1
    yon = pywrapcp.RoutingIndexManager(n, arac, 0)
    model = pywrapcp.RoutingModel(yon)

    Di = np.rint(D * OL).astype(np.int64)
    servis = np.rint(ins["servis"] * OL).astype(np.int64)

    def mesafe_cb(i, j):
        return int(Di[yon.IndexToNode(i), yon.IndexToNode(j)])

    mesafe_idx = model.RegisterTransitCallback(mesafe_cb)
    model.SetArcCostEvaluatorOfAllVehicles(mesafe_idx)

    def sure_cb(i, j):
        a, b = yon.IndexToNode(i), yon.IndexToNode(j)
        return int(Di[a, b] + servis[a])

    sure_idx = model.RegisterTransitCallback(sure_cb)
    ufuk = int(round(ins["tw_bit"][0] * OL))
    model.AddDimension(sure_idx, ufuk, ufuk, False, "Time")
    zaman = model.GetDimensionOrDie("Time")
    for k in range(1, n):
        idx = yon.NodeToIndex(k)
        zaman.CumulVar(idx).SetRange(int(round(ins["tw_bas"][k] * OL)),
                                     int(round(ins["tw_bit"][k] * OL)))
    for v in range(arac):
        zaman.CumulVar(model.Start(v)).SetRange(0, ufuk)
        zaman.CumulVar(model.End(v)).SetRange(0, ufuk)
        model.AddVariableMinimizedByFinalizer(zaman.CumulVar(model.Start(v)))
        model.AddVariableMinimizedByFinalizer(zaman.CumulVar(model.End(v)))

    talep = np.rint(ins["talep"]).astype(np.int64)
    kap_idx = model.RegisterUnaryTransitCallback(lambda i: int(talep[yon.IndexToNode(i)]))
    model.AddDimensionWithVehicleCapacity(kap_idx, 0, [int(ins["Q"])] * arac, True, "Cap")

    par = pywrapcp.DefaultRoutingSearchParameters()
    par.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    par.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    par.time_limit.FromSeconds(sure_sn)
    coz = model.SolveWithParameters(par)
    if coz is None:
        return {"basarili": False, "sure_sn": time.perf_counter() - t0}

    mesafe, kullanilan = 0.0, 0
    for v in range(arac):
        idx = model.Start(v)
        if not model.IsEnd(coz.Value(model.NextVar(idx))):
            kullanilan += 1
        while not model.IsEnd(idx):
            n_idx = coz.Value(model.NextVar(idx))
            mesafe += D[yon.IndexToNode(idx), yon.IndexToNode(n_idx)]
            idx = n_idx
    return {"basarili": True, "arac": kullanilan, "mesafe": mesafe,
            "sure_sn": time.perf_counter() - t0}


# ─────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sure", type=int, default=30, help="OR-Tools süre sınırı (sn)")
    args = ap.parse_args()

    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    onbellek = os.path.join(kok, "data", "benchmark")
    print("=" * 78)
    print("SOLOMON VRPTW DOĞRULAMASI (K76)")
    print(f"  OR-Tools süre sınırı: {args.sure} sn | Referans: Balikos vd. 2025 s.435-437")
    print("=" * 78)
    klasor = solomon_indir(onbellek)

    satirlar = []
    for ad in ORNEKLER:
        for n in BOYUTLAR:
            ins = solomon_oku(klasor, ad, n)
            D = mesafe_matrisi(ins)
            nn = coz_en_yakin_komsu(ins, D, iki_opt=False)
            nn2 = coz_en_yakin_komsu(ins, D, iki_opt=True)
            arac = max(nn.get("arac", 0), nn2.get("arac", 0), 1)
            ot = coz_ortools(ins, D, args.sure, arac)

            r = {"ornek": ad, "musteri": n, "tip": ad[:2] if ad.startswith("RC") else ad[:1]}
            for etiket, s in [("NN", nn), ("NN2opt", nn2), ("ORTools", ot)]:
                r[f"{etiket}_arac"] = s.get("arac")
                r[f"{etiket}_mesafe"] = round(s["mesafe"], 2) if s["basarili"] else None
                r[f"{etiket}_sure_sn"] = round(s["sure_sn"], 2)
            if ot["basarili"]:
                for etiket in ("NN", "NN2opt"):
                    if r[f"{etiket}_mesafe"] is not None:
                        r[f"{etiket}_ed_pct"] = round(
                            100.0 * (r[f"{etiket}_mesafe"] - ot["mesafe"]) / ot["mesafe"], 2)
            if r["NN_mesafe"] and r["NN2opt_mesafe"]:
                r["iki_opt_kazanc_pct"] = round(
                    100.0 * (r["NN_mesafe"] - r["NN2opt_mesafe"]) / r["NN_mesafe"], 2)
            satirlar.append(r)
            print(f"  {ad:6s} n={n:3d} | NN {r['NN_mesafe']:>8} ({r['NN_arac']} araç) | "
                  f"NN+2opt {r['NN2opt_mesafe']:>8} ({r['NN2opt_arac']}) | "
                  f"OR-Tools {r['ORTools_mesafe']:>8} ({r['ORTools_arac']}) | "
                  f"e_d: NN {r.get('NN_ed_pct')}% → NN+2opt {r.get('NN2opt_ed_pct')}%")

    df = pd.DataFrame(satirlar)
    cikti_dizin = os.path.join(kok, "data", "synthetic")
    os.makedirs(cikti_dizin, exist_ok=True)
    csv_yol = os.path.join(cikti_dizin, "solomon_dogrulama_sonuclari.csv")
    df.to_csv(csv_yol, index=False, encoding="utf-8")

    print("\n--- ÖZET (OR-Tools referansına göre ortalama sapma) ---")
    for k in ("NN_ed_pct", "NN2opt_ed_pct"):
        if k in df:
            print(f"  {k:14s} ortalama %{df[k].mean():.2f} | medyan %{df[k].median():.2f} | "
                  f"en kötü %{df[k].max():.2f}")
    if "iki_opt_kazanc_pct" in df:
        print(f"  2-opt kazancı  ortalama %{df['iki_opt_kazanc_pct'].mean():.2f}")
    print(f"\n  CSV: data/synthetic/solomon_dogrulama_sonuclari.csv ({len(df)} satır)")
    return df


if __name__ == "__main__":
    main()
