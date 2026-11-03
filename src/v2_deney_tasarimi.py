"""
v2_deney_tasarimi.py
====================
Hafta 14 — Faktöriyel Deney Tasarımı, ANOVA ve Tukey HSD (K82)

Neden
-----
v1'de dört sevk kuralı ikili t-testleriyle karşılaştırılmıştı (K44/K45). Aynı veri
üzerinde çok sayıda ikili test yapmak I. tip hata oranını şişirir. Klasördeki iki
kaynak doğru yöntemi tanımlıyor:

  · Herrera-Vidal vd. (2026, Applied Sci. 16:1701, s.9-10): senaryo karşılaştırması
    ANOVA + Tukey HSD ile, senaryo başına 30 replikasyon, p<0.05 ölçütüyle yapılır.
  · Sevim & Görkemli Aykut (2026, Pamukkale Üniv. Müh. Bil. Derg., s.67): beş faktör,
    iki düzey, tam faktöriyel tasarım; ana etki ve etkileşim grafikleriyle yorumlanır.

Bu betik iki analiz üretir:

  E1  TAM FAKTÖRİYEL TASARIM (2^5) — Sevim & Görkemli Aykut s.67 deseni
      Faktörler (düşük / yüksek):
        A filo büyüklüğü        2 / 4 araç
        B güvenlik katsayısı α  0.05 / 0.30
        C sevk politikası       ANINDA / KONSOLIDASYON
        D talep düzeyi          baz / +%50 şok
        E raf boyutlandırma     V1 (N=⌈ROP/C⌉) / VDI (N=1+⌈ROP/C⌉)
      Yanıt değişkenleri: duruş oranı, ortalama WIP, toplam mesafe, araç doluluğu.
      Ana etkiler ve iki faktörlü etkileşimler, etki büyüklükleriyle raporlanır.

  E2  SEVK KURALI KARŞILAŞTIRMASI — tek yönlü ANOVA + Tukey HSD
      EDD / SLACK / FIFO / KRİTİKLİK, K44'ün yeniden değerlendirmesi.
      v1'deki ikili t-testleri yerine çoklu karşılaştırma düzeltmeli test.

Tukey HSD ve ANOVA scipy ile hesaplanır (statsmodels bağımlılığı eklenmez).

Kullanım:
    python -X utf8 -m src.v2_deney_tasarimi              # rep=10
    python -X utf8 -m src.v2_deney_tasarimi --rep 30     # Herrera-Vidal ölçütü
"""

import argparse
import itertools
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd
from scipy import stats

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir

FAKTORLER = {
    "A_filo":   ("Filo büyüklüğü (araç)",        {"-": 2,        "+": 4}),
    "B_alpha":  ("Güvenlik katsayısı α",         {"-": 0.05,     "+": 0.30}),
    "C_sevk":   ("Sevk politikası",              {"-": "ANINDA", "+": "KONSOLIDASYON"}),
    "D_talep":  ("Talep düzeyi",                 {"-": 1.0,      "+": 1.5}),
    "E_raf":    ("Raf boyutlandırma",            {"-": "V1",     "+": "VDI"}),
}
YANITLAR = [("starv_pct", "Duruş oranı (%)"), ("ort_wip", "Ortalama WIP (adet)"),
            ("toplam_mesafe_km", "Mesafe (km)"), ("doluluk_pct", "Araç doluluğu (%)")]


def e1_faktoriyel(veri: V2Veri, rep: int) -> pd.DataFrame:
    kombinasyonlar = list(itertools.product("-+", repeat=len(FAKTORLER)))
    print(f"── E1: TAM FAKTÖRİYEL 2^{len(FAKTORLER)} = {len(kombinasyonlar)} koşul "
          f"× {rep} replikasyon ──")
    satir = []
    for i, kombin in enumerate(kombinasyonlar, 1):
        d = dict(zip(FAKTORLER.keys(), kombin))
        p = V2Parametre(politika="P3", talep_modeli="SAATLIK_REJIM",
                        arac_sayisi=FAKTORLER["A_filo"][1][d["A_filo"]],
                        alpha=FAKTORLER["B_alpha"][1][d["B_alpha"]],
                        sevk=FAKTORLER["C_sevk"][1][d["C_sevk"]],
                        talep_carpani=FAKTORLER["D_talep"][1][d["D_talep"]],
                        kanban_modu=FAKTORLER["E_raf"][1][d["E_raf"]])
        for r in range(rep):
            s = calistir(replace(p, seed=5000 + r), veri)
            satir.append({**d, "rep": r, **{k: s[k] for k, _ in YANITLAR}})
        if i % 8 == 0 or i == len(kombinasyonlar):
            print(f"    [{i}/{len(kombinasyonlar)}]")
    return pd.DataFrame(satir)


def ana_etkiler(df: pd.DataFrame) -> pd.DataFrame:
    """Her faktörün her yanıt üzerindeki ana etkisi = ortalama(+) − ortalama(−)."""
    satir = []
    for f, (ad, duzey) in FAKTORLER.items():
        for y, y_ad in YANITLAR:
            arti, eksi = df[df[f] == "+"][y], df[df[f] == "-"][y]
            t, pdeg = stats.ttest_ind(arti, eksi, equal_var=False)
            birlesik = np.sqrt((arti.var(ddof=1) + eksi.var(ddof=1)) / 2)
            satir.append({"faktor": ad, "yanit": y_ad,
                          "dusuk": f"{duzey['-']}", "yuksek": f"{duzey['+']}",
                          "ort_dusuk": eksi.mean(), "ort_yuksek": arti.mean(),
                          "ana_etki": arti.mean() - eksi.mean(),
                          "cohen_d": (arti.mean() - eksi.mean()) / birlesik if birlesik else 0.0,
                          "p": pdeg})
    return pd.DataFrame(satir)


def etkilesimler(df: pd.DataFrame, yanit: str = "starv_pct") -> pd.DataFrame:
    """İki faktörlü etkileşim = [(++ ) − (+−)] − [(−+) − (−−)], hepsi / 2."""
    satir = []
    for f1, f2 in itertools.combinations(FAKTORLER.keys(), 2):
        def ort(a, b):
            m = (df[f1] == a) & (df[f2] == b)
            return df.loc[m, yanit].mean()
        etki = ((ort("+", "+") - ort("+", "-")) - (ort("-", "+") - ort("-", "-"))) / 2
        satir.append({"faktor_1": FAKTORLER[f1][0], "faktor_2": FAKTORLER[f2][0],
                      "etkilesim": etki})
    return pd.DataFrame(satir).sort_values("etkilesim", key=abs, ascending=False)


def _tukey(gruplar: dict, alfa: float = 0.05) -> pd.DataFrame:
    """Dengeli tasarım için Tukey HSD; q kritik değeri F dağılımından yaklaşıklanır."""
    adlar = list(gruplar)
    k = len(adlar)
    n = len(next(iter(gruplar.values())))
    N = k * n
    ortalamalar = {a: np.mean(v) for a, v in gruplar.items()}
    hata_kt = sum(((np.array(v) - ortalamalar[a]) ** 2).sum() for a, v in gruplar.items())
    mse = hata_kt / (N - k)
    # q_{alfa,k,N-k} ≈ sqrt(2·(k−1)·F_{alfa,k−1,N−k})  (dengeli tasarımda yaygın yaklaşıklama)
    q_krit = np.sqrt(2 * (k - 1) * stats.f.ppf(1 - alfa, k - 1, N - k))
    hsd = q_krit * np.sqrt(mse / n)
    satir = []
    for a, b in itertools.combinations(adlar, 2):
        fark = ortalamalar[a] - ortalamalar[b]
        satir.append({"grup_1": a, "grup_2": b, "fark": fark, "HSD": hsd,
                      "anlamli": abs(fark) > hsd})
    return pd.DataFrame(satir)


def e2_sevk_kurallari(veri: V2Veri, rep: int, arac: int, talep: float) -> tuple:
    kurallar = ["EDD", "SLACK", "FIFO", "KRITIKLIK"]
    gruplar = {}
    for kural in kurallar:
        p = V2Parametre(politika="P3", sevk="KONSOLIDASYON", dispatch_kural=kural,
                        arac_sayisi=arac, talep_carpani=talep,
                        talep_modeli="SAATLIK_REJIM")
        gruplar[kural] = [calistir(replace(p, seed=6000 + r), veri)["starv_pct"]
                          for r in range(rep)]
    F, pdeg = stats.f_oneway(*gruplar.values())
    return gruplar, F, pdeg, _tukey(gruplar)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=10)
    args = ap.parse_args()

    veri = V2Veri()
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    os.makedirs(cikti, exist_ok=True)

    print("=" * 78)
    print("FAKTÖRİYEL DENEY TASARIMI, ANOVA VE TUKEY HSD")
    print("=" * 78)

    ham = e1_faktoriyel(veri, args.rep)
    ham.to_csv(os.path.join(cikti, "v2_e1_faktoriyel_ham.csv"), index=False, encoding="utf-8")

    ae = ana_etkiler(ham)
    ae.to_csv(os.path.join(cikti, "v2_e1_ana_etkiler.csv"), index=False, encoding="utf-8")
    print("\n── ANA ETKİLER (duruş oranı, etki büyüklüğüne göre) ──")
    alt = ae[ae["yanit"] == "Duruş oranı (%)"].sort_values("ana_etki", key=abs, ascending=False)
    for _, r in alt.iterrows():
        yildiz = "***" if r["p"] < 0.001 else ("**" if r["p"] < 0.01
                                               else ("*" if r["p"] < 0.05 else "—"))
        print(f"  {r['faktor']:26s} {r['dusuk']:>14s} → {r['yuksek']:<14s} "
              f"{r['ana_etki']:+7.2f} puan  d={r['cohen_d']:+5.2f}  p={r['p']:.2e} {yildiz}")

    print("\n── ANA ETKİLER (diğer yanıtlar) ──")
    for y, y_ad in YANITLAR[1:]:
        alt = ae[ae["yanit"] == y_ad].sort_values("ana_etki", key=abs, ascending=False).head(3)
        print(f"  {y_ad}:")
        for _, r in alt.iterrows():
            print(f"    {r['faktor']:26s} {r['ana_etki']:+9.2f}   (d={r['cohen_d']:+5.2f})")

    ek = etkilesimler(ham)
    ek.to_csv(os.path.join(cikti, "v2_e1_etkilesimler.csv"), index=False, encoding="utf-8")
    print("\n── EN GÜÇLÜ İKİ FAKTÖRLÜ ETKİLEŞİMLER (duruş oranı) ──")
    for _, r in ek.head(4).iterrows():
        print(f"  {r['faktor_1']:26s} × {r['faktor_2']:26s} {r['etkilesim']:+7.2f} puan")

    print("\n── E2: SEVK KURALI — TEK YÖNLÜ ANOVA + TUKEY HSD ──")
    e2_satir = []
    for etiket, arac, talep in [("Yeterli filo (4 araç, baz talep)", 4, 1.0),
                                ("Kısıtlı filo (2 araç, +%50 şok)", 2, 1.5)]:
        gruplar, F, pdeg, tukey = e2_sevk_kurallari(veri, args.rep, arac, talep)
        print(f"\n  · {etiket}")
        for k, v in gruplar.items():
            ci = 1.96 * np.std(v, ddof=1) / np.sqrt(len(v))
            print(f"      {k:10s} ort=%{np.mean(v):6.3f} ± {ci:.3f}")
        print(f"      ANOVA: F={F:.3f}, p={pdeg:.4f} → "
              f"{'gruplar arasında anlamlı fark VAR' if pdeg < 0.05 else 'anlamlı fark YOK'}")
        anlamli = tukey[tukey["anlamli"]]
        if len(anlamli):
            for _, r in anlamli.iterrows():
                print(f"      Tukey: {r['grup_1']} vs {r['grup_2']}  "
                      f"fark={r['fark']:+.3f} puan (HSD={r['HSD']:.3f}) ✓")
        else:
            print(f"      Tukey: hiçbir ikili fark HSD={tukey['HSD'].iloc[0]:.3f} puanı aşmıyor")
        for k, v in gruplar.items():
            for r_i, deger in enumerate(v):
                e2_satir.append({"senaryo": etiket, "kural": k, "rep": r_i,
                                 "starv_pct": deger, "anova_F": F, "anova_p": pdeg})
    pd.DataFrame(e2_satir).to_csv(os.path.join(cikti, "v2_e2_sevk_anova.csv"),
                                  index=False, encoding="utf-8")
    print("\n  CSV: data/synthetic/v2_e1_*.csv, v2_e2_sevk_anova.csv")


if __name__ == "__main__":
    main()
