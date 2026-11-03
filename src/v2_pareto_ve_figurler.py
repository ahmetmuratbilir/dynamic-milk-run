"""
v2_pareto_ve_figurler.py
========================
Hafta 14 — Politika Karşılaştırması, Pareto Cephesi ve Makale Figürleri

Üretilenler
-----------
  P-1  POLİTİKA IZGARA TARAMASI (K73, K79)
       Üç politika kendi boyutlandırma formülüyle taranır:
         P1  sabit takt + sabit miktar (her istasyona 1 kutu)          [Klenk 2012 s.6]
         P2  sabit takt + Kanban miktarı (1:1 boş kutu değişimi)       [Simić 2020 s.10-11;
                                                                        Vojdani 2022 s.6]
         P3  olay tabanlı dinamik sevk (ANINDA / KONSOLIDASYON)        [Facchini 2022 s.1123]
       Önceki karşılaştırmalar tek bir statik referans noktasına (80 dk tur) dayanıyordu;
       burada tur aralığı 30–120 dk bandında taranarak SINIR EĞRİSİ kurulur (Bulgu B2).

  P-2  PARETO CEPHESİ (C2 / K80)
       Amaçlar: ortalama hat yanı WIP ↓, duruş oranı ↓, toplam mesafe ↓.
       Analitik temel: stok çevrim süresiyle orantılıdır (Droste & Deuse 2011 s.607-608,
       Şekil 4); tampon rota frekansıyla ters orantılıdır (Urru vd. 2018 s.406).
       Tur sayısı ile stok arasındaki ödünleşim: Alnahhal & Noche 2015 s.118.
       Bu ölçekte metasezgisel gerekmez; tam ızgara taranıp baskın olmayan çözümler
       süzülür (Zhou & Wen 2024 NSGA-II ile aynı çıktı türünü üretir: Pareto cephesi).

  P-3  MAKALE FİGÜRLERİ  → docs/figurler/*.png
       Şekil 1  Pareto cephesi (WIP × duruş, politikaya göre)
       Şekil 2  Filo sınır eğrisi (araç sayısı × duruş, %5 eşik referansı)
       Şekil 3  Düzeltmelerin ayrıştırılması (v1 → v2 katkı şeması)
       Şekil 4  Welch ısınma eğrisi (K78 gerekçesi)

Görselleştirme kuralları: tek eksen, kategorik renk kimliğe göre sabit sıra
(mavi/turuncu/aqua — CVD doğrulaması yapılmış), ince işaretler, geri planda ızgara,
seçici doğrudan etiket, ≥2 seride her zaman gösterge. Figürler basılı makale için
açık tema üretilir; sayısal karşılıkları CSV olarak da yazılır (tablo görünümü).

Kullanım:
    python -X utf8 -m src.v2_pareto_ve_figurler            # tam tarama
    python -X utf8 -m src.v2_pareto_ve_figurler --rep 5    # hızlı tarama
"""

import argparse
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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.v2_entegre_simulasyon import V2Parametre, V2Veri, calistir

# ── Görsel kimlik (dataviz referans paleti; 3 slot all-pairs doğrulandı) ──
RENK = {"P1": "#2a78d6", "P2": "#eb6834", "P3": "#1baf7a"}
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
IZGARA, EKSEN, YUZEY = "#e1e0d9", "#c3c2b7", "#fcfcfb"
KRITIK = "#d03b3b"
POLITIKA_ADI = {"P1": "P1 · sabit takt, sabit miktar",
                "P2": "P2 · sabit takt, Kanban miktarı",
                "P3": "P3 · olay tabanlı dinamik"}

TUR_ARALIKLARI = [30, 45, 60, 80, 90, 120]
ARACLAR = [1, 2, 3, 4, 5, 6, 8]
ALFALAR = [0.05, 0.15, 0.30]
# Talep düzeyleri (K81): baz senaryoda literatüre uygun boyutlandırma ile üç politika da
# eşiğin çok altında kalır ve ayrışmaz; politikalar ancak talep şoku altında ayrışır.
# Şok büyüklükleri K22 (+%20) ve Klenk vd. 2012 s.14'teki "uneven demand" bozucu senaryosu.
TALEP_DUZEYLERI = [("Baz talep", 1.0), ("Talep şoku +%50", 1.5)]


def _eksen_duzenle(ax, xl, yl, baslik=None):
    ax.set_facecolor(YUZEY)
    ax.grid(True, color=IZGARA, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for k in ("top", "right"):
        ax.spines[k].set_visible(False)
    for k in ("left", "bottom"):
        ax.spines[k].set_color(EKSEN)
        ax.spines[k].set_linewidth(1.0)
    ax.tick_params(colors=MUTED, labelsize=9, length=0)
    ax.set_xlabel(xl, color=INK2, fontsize=10)
    ax.set_ylabel(yl, color=INK2, fontsize=10)
    if baslik:
        ax.set_title(baslik, color=INK, fontsize=12, loc="left", pad=12)


def izgara_tara(veri: V2Veri, rep: int) -> pd.DataFrame:
    """Politika ızgarasını rep replikasyonla tarar; ortalamaları döner."""
    isler = []
    for etiket, carpan in TALEP_DUZEYLERI:
        for T in TUR_ARALIKLARI:
            for m in ARACLAR:
                for pol in ("P1", "P2"):
                    isler.append(dict(politika=pol, tur_araligi_dk=T, arac_sayisi=m,
                                      alpha=0.15, talep_carpani=carpan, _talep=etiket))
        for m in ARACLAR:
            for sevk in ("ANINDA", "KONSOLIDASYON"):
                for a in ALFALAR:
                    isler.append(dict(politika="P3", sevk=sevk, arac_sayisi=m, alpha=a,
                                      talep_carpani=carpan, _talep=etiket))

    print(f"  {len(isler)} konfigürasyon × {rep} replikasyon = {len(isler) * rep} koşu")
    satir = []
    for i, kw in enumerate(isler, 1):
        talep_etiket = kw.pop("_talep")
        p = V2Parametre(talep_modeli="SAATLIK_REJIM", **kw)
        tek = [calistir(replace(p, seed=3000 + r), veri) for r in range(rep)]
        d = {k: kw.get(k) for k in ("politika", "sevk", "tur_araligi_dk", "arac_sayisi",
                                    "alpha", "talep_carpani")}
        d["talep_duzeyi"] = talep_etiket
        for alan in ("starv_pct", "ort_wip", "toplam_mesafe_km", "tur_sayisi",
                     "doluluk_pct", "toplam_kart", "max_tur_sure_dk", "arac_kullanim_pct"):
            v = [s[alan] for s in tek]
            d[alan] = float(np.mean(v))
            if alan == "starv_pct":
                d["starv_sd"] = float(np.std(v, ddof=1)) if rep > 1 else 0.0
                d["starv_ci95"] = 1.96 * d["starv_sd"] / np.sqrt(rep) if rep > 1 else 0.0
        d["sevk"] = kw.get("sevk", "TAKVIM")
        satir.append(d)
        if i % 20 == 0 or i == len(isler):
            print(f"    [{i}/{len(isler)}]")
    return pd.DataFrame(satir)


def baskin_olmayan(df: pd.DataFrame, amaclar=("ort_wip", "starv_pct", "toplam_mesafe_km")):
    """Üç amaçta (hepsi minimize) baskın olmayan (Pareto-optimal) satırları işaretler."""
    A = df[list(amaclar)].to_numpy()
    n = len(A)
    bayrak = np.ones(n, dtype=bool)
    for i in range(n):
        if not bayrak[i]:
            continue
        kucuk_esit = np.all(A <= A[i] + 1e-9, axis=1)
        kesin_kucuk = np.any(A < A[i] - 1e-9, axis=1)
        if np.any(kucuk_esit & kesin_kucuk):
            bayrak[i] = False
    return bayrak


def sekil1_pareto(df: pd.DataFrame, yol: str):
    """WIP × duruş düzleminde iki amaçlı cephe (merdiven). Üç amaçlı set CSV'dedir."""
    df = df[df["talep_duzeyi"] == TALEP_DUZEYLERI[0][0]]
    fig, ax = plt.subplots(figsize=(9.2, 5.6), facecolor=YUZEY)
    _eksen_duzenle(ax, "Ortalama hat yanı WIP stoku (adet)", "Hat duruş oranı (%)",
                   "Şekil 1 · WIP–duruş ödünleşimi ve iki amaçlı Pareto cephesi (baz talep)")
    for pol in ("P1", "P2", "P3"):
        alt = df[df["politika"] == pol]
        ax.scatter(alt["ort_wip"], alt["starv_pct"], s=26, color=RENK[pol],
                   alpha=0.40, linewidths=0, zorder=2, label=POLITIKA_ADI[pol])
        pf = alt[alt["pareto_2a"]].sort_values("ort_wip")
        if len(pf):
            ax.step(pf["ort_wip"], pf["starv_pct"], where="post",
                    color=RENK[pol], linewidth=2.0, zorder=3)
            ax.scatter(pf["ort_wip"], pf["starv_pct"], s=54, color=RENK[pol],
                       edgecolors=YUZEY, linewidths=2.0, zorder=4)
    ax.axhline(5.0, color=KRITIK, linewidth=1.4, linestyle=(0, (5, 3)), zorder=1)
    ax.set_yscale("symlog", linthresh=0.1, linscale=0.6)
    ax.set_ylim(bottom=0)
    ax.set_yticks([0, 0.1, 0.5, 1, 2, 5, 10, 20])
    ax.set_yticklabels(["0", "0,1", "0,5", "1", "2", "5", "10", "20"])
    ax.annotate("%5 duruş eşiği", xy=(ax.get_xlim()[1], 5.0), xytext=(-6, 5),
                textcoords="offset points", ha="right", color=KRITIK, fontsize=9)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK2, loc="upper right")
    fig.text(0.01, 0.015, "İçi dolu işaretler ve merdiven: WIP–duruş düzleminde baskın olmayan "
                          "çözümler · y ekseni %0,1 altında doğrusal", color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def sekil2_filo(df: pd.DataFrame, yol: str):
    """Küçük çoklu: baz talep ve talep şoku altında filo sınır eğrisi."""
    duzeyler = [e for e, _ in TALEP_DUZEYLERI]
    fig, axlar = plt.subplots(1, len(duzeyler), figsize=(11.4, 5.0),
                              facecolor=YUZEY, sharey=True)
    for k, (ax, duzey) in enumerate(zip(np.atleast_1d(axlar), duzeyler)):
        _eksen_duzenle(ax, "Filo büyüklüğü (araç)",
                       "Hat duruş oranı (%)" if k == 0 else "", duzey)
        son_noktalar = []
        for pol in ("P1", "P2", "P3"):
            alt = (df[(df["politika"] == pol) & (df["talep_duzeyi"] == duzey)]
                   .groupby("arac_sayisi")["starv_pct"].min().reset_index()
                   .sort_values("arac_sayisi"))
            ax.plot(alt["arac_sayisi"], alt["starv_pct"], color=RENK[pol], linewidth=2.0,
                    marker="o", markersize=6, markeredgecolor=YUZEY, markeredgewidth=1.6,
                    label=POLITIKA_ADI[pol] if k == 0 else None, zorder=3)
            son_noktalar.append((pol, alt.iloc[-1]["arac_sayisi"], alt.iloc[-1]["starv_pct"]))
        if k == len(duzeyler) - 1:          # doğrudan etiket yalnızca sağ panelde
            son_noktalar.sort(key=lambda z: z[2], reverse=True)
            kullanilan = []
            for pol, x, y in son_noktalar:
                dy = 0
                while any(abs(y + dy - yk) < 1e-9 for yk in kullanilan):
                    dy += 0.004                     # çakışan etiketleri dikeyde ayır
                kullanilan.append(y + dy)
                ax.annotate(pol, xy=(x, y), xytext=(9, 11 if dy else 0),
                            textcoords="offset points", color=RENK[pol],
                            fontsize=10, fontweight="bold", va="center")
        ax.axhline(5.0, color=KRITIK, linewidth=1.4, linestyle=(0, (5, 3)), zorder=1)
        ax.set_yscale("symlog", linthresh=0.01, linscale=0.5)
        ax.set_ylim(bottom=0)
        ax.set_xticks(ARACLAR)
        ax.set_xlim(0.6, ARACLAR[-1] + 0.9)
    ax0 = np.atleast_1d(axlar)[0]
    ax0.set_yticks([0, 0.01, 0.1, 1, 5, 20, 50])
    ax0.set_yticklabels(["0", "0,01", "0,1", "1", "5", "20", "50"])
    ax0.annotate("%5 duruş eşiği", xy=(0.7, 5.0), xytext=(0, 6),
                 textcoords="offset points", color=KRITIK, fontsize=9)
    ax0.legend(frameon=False, fontsize=9, labelcolor=INK2, loc="upper right",
               bbox_to_anchor=(1.0, 0.86))
    fig.suptitle("Şekil 2 · Filo sınır eğrisi: politikalar ancak talep şoku altında ayrışır",
                 color=INK, fontsize=12, x=0.012, ha="left", y=0.98)
    fig.text(0.012, 0.015, "Her nokta, o filo büyüklüğünde ilgili politikanın taranan "
                           "konfigürasyonları içindeki en düşük duruş oranıdır · "
                           "y ekseni %0,01 altında doğrusal", color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.045, 1, 0.945))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def sekil3_ayristirma(yol_csv: str, yol: str):
    if not os.path.exists(yol_csv):
        print("    (Şekil 3 atlandı: v2_d45_ayristirma.csv yok)")
        return
    df = pd.read_csv(yol_csv)
    fig, ax = plt.subplots(figsize=(9.2, 5.0), facecolor=YUZEY)
    _eksen_duzenle(ax, "Duruş oranı (%)", "",
                   "Şekil 3 · v1'den v2'ye düzeltmelerin duruş oranına katkısı")
    y = np.arange(len(df))[::-1]
    ax.barh(y, df["starv_pct"], height=0.6, color="#2a78d6", zorder=2)
    for yi, (_, r) in zip(y, df.iterrows()):
        ax.text(r["starv_pct"] + 0.15, yi, f"%{r['starv_pct']:.2f}"
                + ("" if pd.isna(r["d_starv_puan"]) else f"  ({r['d_starv_puan']:+.2f} puan)"),
                va="center", color=INK2, fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(df["adim"], fontsize=9, color=INK2)
    ax.set_xlim(0, max(df["starv_pct"]) * 1.45)
    fig.text(0.01, 0.015, "Kümülatif: her satır, üstündeki tüm düzeltmeleri içerir. "
                          "Parantez içi değer o adımın tek başına katkısıdır.",
             color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def sekil4_isinma(yol_csv: str, yol: str):
    if not os.path.exists(yol_csv):
        print("    (Şekil 4 atlandı: v2_d2_welch_isinma.csv yok)")
        return
    df = pd.read_csv(yol_csv)
    # 480 dk'lık koşu, 1440 dk'lık DOLU koşunun ilk 480 dakikasıyla özdeştir; çizimde
    # üst üste bineceği için yalnızca başlangıç stoku farkı gösterilir (K77/K78).
    gosterilecek = [k for k in df["konfig"].unique() if not k.startswith("480")]
    fig, ax = plt.subplots(figsize=(9.2, 5.2), facecolor=YUZEY)
    _eksen_duzenle(ax, "Simülasyon zamanı (dakika)", "Ortalama hat yanı WIP (adet)",
                   "Şekil 4 · Welch grafik yöntemiyle ısınma süresi")
    for konfig, c in zip(gosterilecek, ["#2a78d6", "#1baf7a"]):
        alt = df[df["konfig"] == konfig]
        ax.plot(alt["dakika"], alt["wip_ma"], color=c, linewidth=2.0,
                label=konfig, zorder=3)
    kararli = df["kararli_wip"].iloc[-1]
    ax.axhline(kararli, color=MUTED, linewidth=1.0, linestyle=(0, (2, 3)), zorder=1)
    ax.annotate(f"kararlı ≈ {kararli:.0f} adet", xy=(df["dakika"].max(), kararli),
                xytext=(-6, 8), textcoords="offset points", ha="right",
                color=MUTED, fontsize=9)
    ust = ax.get_ylim()[1]
    for t, etiket, c, dy in [(45, "v1: 45 dk", KRITIK, -14),
                             (90, "v2 (K78): 90 dk", "#006300", -32),
                             (480, "tek vardiya sonu", MUTED, -14)]:
        ax.axvline(t, color=c, linewidth=1.4, linestyle=(0, (5, 3)), zorder=2)
        ax.annotate(etiket, xy=(t, ust), xytext=(5, dy), textcoords="offset points",
                    color=c, fontsize=9)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK2, loc="upper right")
    fig.text(0.01, 0.015, "20 replikasyon ortalaması, ±15 dk hareketli ortalama. "
                          "45. dakikada WIP kararlı değerin %54 üzerindedir; %1 bandına "
                          "t≈90 dk'da girilir.", color=MUTED, fontsize=8)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(yol, dpi=200, facecolor=YUZEY)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rep", type=int, default=10, help="konfigürasyon başına replikasyon")
    args = ap.parse_args()

    veri = V2Veri()
    kok = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cikti = os.path.join(kok, "data", "synthetic")
    fig_dizin = os.path.join(kok, "docs", "figurler")
    os.makedirs(cikti, exist_ok=True)
    os.makedirs(fig_dizin, exist_ok=True)

    print("=" * 78)
    print("POLİTİKA IZGARASI, PARETO CEPHESİ VE FİGÜRLER")
    print("=" * 78)
    df = izgara_tara(veri, args.rep)
    # Cepheler her talep düzeyi içinde ayrı hesaplanır
    df["pareto_genel_3a"] = False
    df["pareto_2a"] = False
    for duzey in df["talep_duzeyi"].unique():
        md = df["talep_duzeyi"] == duzey
        df.loc[md, "pareto_genel_3a"] = baskin_olmayan(df[md].reset_index(drop=True))
        for pol in df["politika"].unique():
            m = md & (df["politika"] == pol)
            df.loc[m, "pareto_2a"] = baskin_olmayan(df[m].reset_index(drop=True),
                                                    amaclar=("ort_wip", "starv_pct"))
    df.to_csv(os.path.join(cikti, "v2_politika_izgara.csv"), index=False, encoding="utf-8")

    for duzey, _ in TALEP_DUZEYLERI:
        d = df[df["talep_duzeyi"] == duzey]
        print(f"\n{'═' * 78}\nTALEP DÜZEYİ: {duzey}\n{'═' * 78}")

        print("── %5 EŞİĞİ İÇİN GEREKEN EN KÜÇÜK FİLO ──")
        for pol in ("P1", "P2", "P3"):
            alt = d[(d["politika"] == pol) & (d["starv_pct"] < 5.0)]
            if len(alt):
                m = int(alt["arac_sayisi"].min())
                en = alt[alt["arac_sayisi"] == m].nsmallest(1, "starv_pct").iloc[0]
                ek = (f"T={int(en['tur_araligi_dk'])} dk" if pol != "P3"
                      else f"{en['sevk']}, α={en['alpha']}")
                print(f"  {pol}: {m} araç ({ek}) → %{en['starv_pct']:.2f}, "
                      f"WIP={en['ort_wip']:.0f}, mesafe={en['toplam_mesafe_km']:.1f} km")
            else:
                print(f"  {pol}: taranan bantta %5 altına inen konfigürasyon yok")

        print("── EŞİT WIP KOŞULUNDA KARŞILAŞTIRMA (±%5 bant) ──")
        p3 = d[d["politika"] == "P3"].sort_values("ort_wip")
        gosterildi = 0
        for _, r in p3.iterrows():
            w = r["ort_wip"]
            rakip = d[(d["politika"] != "P3") & (d["ort_wip"].between(w * 0.95, w * 1.05))]
            if not len(rakip) or gosterildi >= 3:
                continue
            en = rakip.nsmallest(1, "starv_pct").iloc[0]
            fark = r["starv_pct"] - en["starv_pct"]
            kim = "dinamik lehine" if fark < 0 else "statik lehine"
            print(f"  P3 m={int(r['arac_sayisi'])} {r['sevk'][:4]} α={r['alpha']}: "
                  f"WIP={w:.0f} → %{r['starv_pct']:.2f}  ||  "
                  f"{en['politika']} m={int(en['arac_sayisi'])} T={int(en['tur_araligi_dk'])}: "
                  f"WIP={en['ort_wip']:.0f} → %{en['starv_pct']:.2f}   "
                  f"[{abs(fark):.2f} puan {kim}]")
            gosterildi += 1

    print("\n── FİGÜRLER ──")
    sekil1_pareto(df, os.path.join(fig_dizin, "sekil1_pareto_wip_durus.png"))
    sekil2_filo(df, os.path.join(fig_dizin, "sekil2_filo_sinir_egrisi.png"))
    sekil3_ayristirma(os.path.join(cikti, "v2_d45_ayristirma.csv"),
                      os.path.join(fig_dizin, "sekil3_duzeltme_ayristirma.png"))
    sekil4_isinma(os.path.join(cikti, "v2_d2_welch_isinma.csv"),
                  os.path.join(fig_dizin, "sekil4_welch_isinma.png"))
    for f in sorted(os.listdir(fig_dizin)):
        print(f"    docs/figurler/{f}")
    print(f"\n  CSV: data/synthetic/v2_politika_izgara.csv ({len(df)} satır)")


if __name__ == "__main__":
    main()
