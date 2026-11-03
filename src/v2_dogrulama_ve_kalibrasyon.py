"""
v2_dogrulama_ve_kalibrasyon.py
==============================
Hafta 14 — v2 Motorunun Doğrulanması ve İstatistiksel Kalibrasyonu

Bu betik dört doğrulama üretir (tez "Doğrulama ve Geçerleme" bölümü için):

  D1  TUR-İÇİ OPTİMALLİK (K76 tamamlayıcısı)
      Solomon testinde (src/solomon_dogrulama.py) en yakın komşu sezgiselinin OR-Tools'a
      göre ortalama ~%103 daha uzun rotalar ürettiği, 2-opt kazancının ise ~%0.5'te
      kaldığı ölçülmüştür. 2-Opt tur-İÇİ bir komşuluk yapısıdır (Gendreau & Tarantilis
      2010, Bölüm 1.1); Solomon'daki açık esas olarak tur-ARASI atamadan doğar.
      Fabrika içi problemde bir turdaki durak sayısı küçüktür (2–8), dolayısıyla
      tur-içi sıralama TAM NUMARALAMA ile optimal olarak çözülebilir. Bu test,
      sezgiselin fabrika bağlamındaki optimallik açığını ölçer ve Solomon sonucunun
      doğrudan bu bağlama taşınıp taşınmadığını gösterir.

  D2  ISINMA SÜRESİ — Welch grafik yöntemi
      Herrera-Vidal vd. (2026, Applied Sci. 16:1701, s.9): ısınma süresi Welch'in
      grafik yöntemiyle belirlenir; anılan çalışmada sistem 25–30 dk'da kararlı hâle
      gelmiş, muhafazakâr 30 dk seçilmiştir. Projede 45 dk (K32/K43) varsayılmış ama
      yöntem hiç uygulanmamıştı. Burada hareketli ortalama ile uygulanır.

  D3  REPLİKASYON YETERLİLİĞİ
      Herrera-Vidal vd. (s.9–10): replikasyon sayısı, %95 GA yarı-genişliğinin
      ortalamanın %2'sinin altına inmesi ölçütüyle belirlenir (anılan çalışmada
      ~45 replikasyondan sonra). Aynı ölçüt v2 motoruna uygulanır.

  D4  v1 ↔ v2 KÖPRÜSÜ (regresyon)
      v2, v1 ayarlarına indirgendiğinde (kanban_modu="V1", mesafe "HAM", talep "CSV",
      max_durak=5, tur süresi kontrolü kapalı, 2-opt kapalı, ANINDA sevk) v1'in
      kanonik %24.58 / WIP=182.3 değerine ne kadar yaklaştığı ölçülür. Bu, v2'deki
      farkların hangi düzeltmeden geldiğini ayrıştırmak için gereken temeldir.

  D5  DÜZELTMELERİN AYRIŞTIRILMASI (ablation)
      v1 ayarlarından başlanarak düzeltmeler tek tek eklenir; her birinin duruş ve WIP
      üzerindeki katkısı ayrı ayrı raporlanır. Hafta 8 raporundaki "duruşun düşmesi
      yalnızca tampon genişlemesindendir" yorumunun sınanması için gereklidir.

Kullanım:
    python -X utf8 -m src.v2_dogrulama_ve_kalibrasyon
"""

import itertools
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir, _Rota


# ─────────────────────────────────────────────────────────────
# D1 — Tur-içi optimallik: sezgisel vs tam numaralama
# ─────────────────────────────────────────────────────────────
def d1_tur_ici_optimallik(veri: V2Veri, p: V2Parametre, tekrar: int = 400) -> pd.DataFrame:
    """Rastgele üretilen durak kümelerinde NN, NN+2opt ve tam numaralama kıyaslanır."""
    rng = np.random.default_rng(20260930)
    sure = (veri.mesafe_metrik / veri.hiz_m_dk)
    rota = _Rota(sure, p)
    kayit = []
    for _ in range(tekrar):
        k = int(rng.integers(2, 9))                       # 2–8 durak (gözlenen aralık)
        dug = [int(x) for x in rng.choice(veri.node, size=k, replace=False)]
        mik = [1] * k
        nn = rota.en_yakin_komsu(dug)
        nn_m = rota.maliyet(nn, dug, 0.0, mik, None)
        o2 = rota.iki_opt(list(nn), dug, 0.0, mik, None)
        o2_m = rota.maliyet(o2, dug, 0.0, mik, None)
        opt_m = min(rota.maliyet(list(pm), dug, 0.0, mik, None)
                    for pm in itertools.permutations(range(k)))
        kayit.append({"durak": k, "nn": nn_m, "nn2opt": o2_m, "opt": opt_m,
                      "nn_ed_pct": 100 * (nn_m - opt_m) / opt_m,
                      "nn2opt_ed_pct": 100 * (o2_m - opt_m) / opt_m})
    df = pd.DataFrame(kayit)
    print("\n── D1: TUR-İÇİ OPTİMALLİK (tam numaralamaya göre sapma) ──")
    ozet = df.groupby("durak")[["nn_ed_pct", "nn2opt_ed_pct"]].agg(["mean", "max"]).round(2)
    print(ozet.to_string())
    print(f"  GENEL: NN %{df['nn_ed_pct'].mean():.2f} (en kötü %{df['nn_ed_pct'].max():.2f}) | "
          f"NN+2opt %{df['nn2opt_ed_pct'].mean():.2f} (en kötü %{df['nn2opt_ed_pct'].max():.2f})")
    print(f"  NN+2opt optimali bulma oranı: %{100 * (df['nn2opt_ed_pct'] < 1e-6).mean():.1f}")
    return df


# ─────────────────────────────────────────────────────────────
# D2 — Welch grafik yöntemiyle ısınma süresi
# ─────────────────────────────────────────────────────────────
def _welch(veri, p, rep, pencere, ufuk, baslangic):
    """Tek konfigürasyon için Welch hareketli ortalamaları ve kararlılık dakikası."""
    wip, starv = [], []
    for r in range(rep):
        s = calistir(replace(p, seed=7000 + r, sim_sure=ufuk, baslangic_stok=baslangic,
                             zaman_serisi=True), veri)
        wip.append(s["_wip_seri"])
        starv.append(s["_starv_seri"])
    W, S = np.array(wip).mean(axis=0), np.array(starv).mean(axis=0)

    def hareketli(x, w):
        return np.array([x[max(0, i - w): i + w + 1].mean() for i in range(len(x))])

    Wh, Sh = hareketli(W, pencere), hareketli(S, pencere)
    son = Wh[-(ufuk // 4):].mean()
    esik = 0.02 * abs(son) if son else 1.0
    kararli = next((t for t in range(len(Wh) - 60)
                    if np.all(np.abs(Wh[t:t + 60] - son) <= esik)), None)
    return Wh, Sh, son, kararli


def d2_welch_isinma(veri: V2Veri, p: V2Parametre, rep: int = 20, pencere: int = 15):
    """
    Welch grafik yöntemi (Herrera-Vidal 2026 s.9). İki soruyu birlikte yanıtlar:
      (a) 480 dk'lık tek vardiyada sistem kararlı hâle geliyor mu?
      (b) Başlangıç stoku (K77) geçici rejim uzunluğunu nasıl etkiliyor?
    """
    print("\n── D2: ISINMA SÜRESİ (Welch grafik yöntemi; Herrera-Vidal 2026 s.9) ──")
    print(f"  {rep} replikasyon ortalaması, ±{pencere} dk hareketli ortalama")
    sonuc = {}
    for etiket, ufuk, bas in [("480 dk / DOLU raf (v1 varsayımı)", 480, "DOLU"),
                              ("1440 dk / DOLU raf (3 vardiya)", 1440, "DOLU"),
                              ("1440 dk / ROP seviyesi (K77)", 1440, "ROP")]:
        Wh, Sh, son, kararli = _welch(veri, p, rep, pencere, ufuk, bas)
        sonuc[etiket] = {"wip_ma": Wh, "starv_ma": Sh, "kararli_dk": kararli, "son": son}
        print(f"\n  · {etiket}")
        print(f"    kararlı WIP ≈ {son:.1f} adet | ±%2 bandına kalıcı giriş: "
              f"{kararli if kararli is not None else 'ufuk içinde yok'} dk")
        for t in (0, 45, 90, 180, 300, 480, 900, 1200):
            if t < len(Wh):
                print(f"      t={t:4d} dk  WIP_ma={Wh[t]:7.1f} ({100*(Wh[t]-son)/son:+7.2f}%)  "
                      f"starv_ma={Sh[t]:5.2f} istasyon/dk")
    return sonuc


# ─────────────────────────────────────────────────────────────
# D3 — Replikasyon yeterliliği
# ─────────────────────────────────────────────────────────────
def d3_replikasyon(veri: V2Veri, p: V2Parametre, en_fazla: int = 60,
                   mutlak_esik: float = 0.05):
    """
    İki ölçüt birlikte raporlanır:
      BAĞIL  : yarı-genişlik ≤ ortalamanın %2'si (Herrera-Vidal 2026 s.9-10)
      MUTLAK : yarı-genişlik ≤ mutlak_esik puan
    Ortalama duruş oranı sıfıra yakınsa bağıl ölçüt tanım gereği sağlanamaz; bu durumda
    mutlak ölçüt kullanılmalıdır (tez metodoloji notu).
    """
    x = np.array([calistir(replace(p, seed=9000 + r), veri)["starv_pct"]
                  for r in range(en_fazla)])
    print("\n── D3: REPLİKASYON YETERLİLİĞİ ──")
    print(f"  Bağıl ölçüt: ±%95 GA ≤ ortalamanın %2'si | Mutlak ölçüt: ≤ {mutlak_esik} puan")
    bagil = mutlak = None
    for n in range(5, en_fazla + 1):
        alt = x[:n]
        hw = 1.96 * alt.std(ddof=1) / np.sqrt(n)
        oran = 100 * hw / alt.mean() if alt.mean() else np.inf
        if n in (5, 10, 20, 30, 40, 50, 60):
            print(f"    n={n:3d}  ort=%{alt.mean():6.3f}  ±{hw:.4f} puan  "
                  f"(ortalamanın %{oran:.2f}'i)")
        if bagil is None and oran <= 2.0:
            bagil = n
        if mutlak is None and hw <= mutlak_esik:
            mutlak = n
    print(f"  Bağıl ölçütü sağlayan en küçük n : {bagil if bagil else 'ufuk içinde yok'}")
    print(f"  Mutlak ölçütü sağlayan en küçük n: {mutlak if mutlak else 'ufuk içinde yok'}")
    return {"bagil_n": bagil, "mutlak_n": mutlak, "degerler": x}


# ─────────────────────────────────────────────────────────────
# D4 / D5 — v1 köprüsü ve düzeltmelerin ayrıştırılması
# ─────────────────────────────────────────────────────────────
V1_AYAR = dict(politika="P3", sevk="ANINDA", dispatch_kural="EDD", kanban_modu="V1",
               mesafe_modu="HAM", talep_modeli="CSV", max_durak=5, max_tur_dk=None,
               iki_opt=False, durak_servis_dk=8.0, kutu_basi_servis_dk=0.0, seed=42)


def d4_d5_ayristirma(veri: V2Veri, arac: int = 4) -> pd.DataFrame:
    """v1 ayarlarından başlayıp düzeltmeleri tek tek ekler (kümülatif ablation)."""
    adimlar = [
        ("v1 ayarları (referans)", {}),
        ("+ K71 metrik mesafe", {"mesafe_modu": "METRIK"}),
        ("+ K72 2-opt & tur süresi", {"iki_opt": True, "max_tur_dk": 90.0}),
        ("+ K67 durak sınırı kalktı", {"max_durak": None}),
        ("+ K66 tek hizmet süresi", {"durak_servis_dk": 3.0}),
        ("+ K68 konsolidasyon", {"sevk": "KONSOLIDASYON"}),
        ("+ K65 VDI raf (+1 kutu)", {"kanban_modu": "VDI"}),
        ("+ K70 saatlik rejim talebi", {"talep_modeli": "SAATLIK_REJIM"}),
    ]
    ayar = dict(V1_AYAR)
    satir, onceki = [], None
    print("\n── D4/D5: v1 KÖPRÜSÜ VE DÜZELTMELERİN AYRIŞTIRILMASI (m=%d) ──" % arac)
    for ad, degisim in adimlar:
        ayar.update(degisim)
        s = calistir(V2Parametre(arac_sayisi=arac, **ayar), veri)
        d_starv = None if onceki is None else s["starv_pct"] - onceki["starv_pct"]
        d_wip = None if onceki is None else s["ort_wip"] - onceki["ort_wip"]
        satir.append({"adim": ad, "starv_pct": round(s["starv_pct"], 2),
                      "d_starv_puan": None if d_starv is None else round(d_starv, 2),
                      "ort_wip": round(s["ort_wip"], 1),
                      "d_wip": None if d_wip is None else round(d_wip, 1),
                      "tur": s["tur_sayisi"], "mesafe_km": round(s["toplam_mesafe_km"], 2),
                      "doluluk_pct": round(s["doluluk_pct"], 1),
                      "toplam_kart": s["toplam_kart"]})
        print(f"  {ad:30s} starv=%{s['starv_pct']:6.2f} "
              f"({'—' if d_starv is None else format(d_starv, '+6.2f')}) "
              f"WIP={s['ort_wip']:7.1f} tur={s['tur_sayisi']:4d} "
              f"kart={s['toplam_kart']:3d} doluluk=%{s['doluluk_pct']:5.1f}")
        onceki = s
    return pd.DataFrame(satir)


def main():
    veri = V2Veri()
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    os.makedirs(cikti, exist_ok=True)

    print("=" * 78)
    print("v2 DOĞRULAMA VE KALİBRASYON")
    print(f"  Metrik kapanış: {veri.metrik_duzeltilen_cift} yönlü düğüm çifti kısaltıldı (K71)")
    print("=" * 78)

    p_baz = V2Parametre(politika="P3", sevk="KONSOLIDASYON", arac_sayisi=4,
                        talep_modeli="SAATLIK_REJIM")

    d1 = d1_tur_ici_optimallik(veri, p_baz)
    d1.to_csv(os.path.join(cikti, "v2_d1_tur_ici_optimallik.csv"), index=False, encoding="utf-8")

    d2 = d2_welch_isinma(veri, p_baz)
    d2_satir = []
    for etiket, s in d2.items():
        for t, (w, st) in enumerate(zip(s["wip_ma"], s["starv_ma"])):
            d2_satir.append({"konfig": etiket, "dakika": t, "wip_ma": w, "starv_ma": st,
                             "kararli_dk": s["kararli_dk"], "kararli_wip": s["son"]})
    pd.DataFrame(d2_satir).to_csv(os.path.join(cikti, "v2_d2_welch_isinma.csv"),
                                  index=False, encoding="utf-8")

    d3 = d3_replikasyon(veri, p_baz)
    pd.DataFrame({"replikasyon": range(1, len(d3["degerler"]) + 1),
                  "starv_pct": d3["degerler"]}).to_csv(
        os.path.join(cikti, "v2_d3_replikasyon.csv"), index=False, encoding="utf-8")

    d45 = d4_d5_ayristirma(veri, arac=4)
    d45.to_csv(os.path.join(cikti, "v2_d45_ayristirma.csv"), index=False, encoding="utf-8")

    print("\n  CSV çıktıları: data/synthetic/v2_d1..d45_*.csv")


if __name__ == "__main__":
    main()
