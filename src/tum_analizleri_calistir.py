"""
tum_analizleri_calistir.py
==========================
Tüm Hafta 14 analizlerini sırayla çalıştırır ve çıktıları yeniden üretir.

Sıra
----
  1. Doğrulama ve kalibrasyon  (D1 tur-içi optimallik, D2 Welch ısınma,
                                D3 replikasyon, D4/D5 v1→v2 ayrıştırma)
  2. Politika ızgarası, Pareto cephesi ve figürler
  3. Faktöriyel tasarım, ANOVA ve Tukey HSD
  4. Vaka çalışması, dinamik Kanban, dinamiklik derecesi ve KPI uyumu
  5. Boyutlandırma tasarımı duyarlılığı (K93)
  6. Toyota bandı sağlamlığı (K95)
  7. Dört adalet kuralı (K97, mevcut + Toyota kutuları) uyarlanan ROP (K98), çok vardiya (K99), koordinat ağı (K100)
  8. Dashboard v2 veri ambarı + dashboard.html (K94)
  9. Solomon VRPTW doğrulaması        (ortools + vrplib gerekir; yoksa atlanır)

Kullanım
--------
    python -X utf8 -m src.tum_analizleri_calistir                # tam koşu
    python -X utf8 -m src.tum_analizleri_calistir --hizli        # az replikasyon
    python -X utf8 -m src.tum_analizleri_calistir --atla solomon

Çıktılar: data/synthetic/v2_*.csv, data/synthetic/solomon_*.csv, docs/figurler/*.png
"""

import argparse
import os
import subprocess
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def calistir(ad: str, modul: str, argumanlar: list) -> tuple:
    print("\n" + "█" * 78)
    print(f"█  {ad}")
    print("█" * 78)
    t0 = time.perf_counter()
    ortam = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    sonuc = subprocess.run([sys.executable, "-X", "utf8", "-m", modul] + argumanlar,
                           cwd=KOK, env=ortam)
    sure = time.perf_counter() - t0
    print(f"\n  → {ad}: {'TAMAM' if sonuc.returncode == 0 else 'HATA'} ({sure:.1f} sn)")
    return sonuc.returncode == 0, sure


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hizli", action="store_true", help="az replikasyonla hızlı koşu")
    ap.add_argument("--atla", nargs="*", default=[],
                    help="atlanacak adımlar: dogrulama, pareto, deney, vaka, boyutlandirma, toyota, adalet, dashboard, solomon")
    args = ap.parse_args()

    rep_izgara = "4" if args.hizli else "8"
    rep_deney = "5" if args.hizli else "10"
    rep_dash = "2" if args.hizli else "3"
    sure_solomon = "5" if args.hizli else "20"

    adimlar = [
        ("dogrulama", "1/9 · Doğrulama ve kalibrasyon",
         "src.v2_dogrulama_ve_kalibrasyon", []),
        ("pareto", "2/9 · Politika ızgarası, Pareto cephesi ve figürler",
         "src.v2_pareto_ve_figurler", ["--rep", rep_izgara]),
        ("deney", "3/9 · Faktöriyel tasarım, ANOVA ve Tukey HSD",
         "src.v2_deney_tasarimi", ["--rep", rep_deney]),
        ("vaka", "4/9 · Vaka çalışması, dinamik Kanban, dod ve KPI uyumu",
         "src.v2_vaka_ve_kpi", []),
        ("boyutlandirma", "5/9 · Boyutlandırma tasarımı duyarlılığı (K93)",
         "src.v2_boyutlandirma_duyarliligi", ["--rep", rep_deney]),
        ("toyota", "6/9 · Toyota formülü bandında sağlamlık (K95)",
         "src.v2_toyota_bandi_duyarliligi", ["--rep", rep_deney]),
        ("adalet", "7/9 · Dört adalet kuralı (K97)",
         "src.v2_adalet_kurallari", ["--rep", rep_deney]),
        ("adalet", "7/9 · Dört adalet kuralı, Toyota kutuları (K97)",
         "src.v2_adalet_kurallari", ["--rep", rep_deney, "--kutu", "toyota"]),
        ("adalet", "7/9 · Uyarlanan ROP (K98)",
         "src.v2_uyarlanan_rop", ["--rep", rep_deney]),
        ("adalet", "7/9 · Kararlı durum ve çok vardiya (K99)",
         "src.v2_cok_vardiya", ["--rep", rep_deney]),
        ("adalet", "7/9 · Koordinat tabanlı mesafe ağı (K100)",
         "src.v2_koordinat_agi", ["--rep", rep_deney]),
        ("solomon", "7/9 · Rotalama: OR-Tools çevrimdışı referansı (K101)",
         "src.v2_ortools_referansi", ["--sure", "5" if args.hizli else "15", "--rep", "2"]),
        ("dashboard", "8/9 · Dashboard v2 veri ambarı (K94)",
         "src.generate_dashboard_data_v2", ["--rep", rep_dash]),
        ("solomon", "9/9 · Solomon VRPTW doğrulaması",
         "src.solomon_dogrulama", ["--sure", sure_solomon]),
    ]

    print("=" * 78)
    print("DİNAMİK MİLK-RUN & E-KANBAN — TÜM ANALİZLER")
    print(f"  Mod: {'HIZLI' if args.hizli else 'TAM'}")
    print("=" * 78)

    ozet, toplam = [], 0.0
    for anahtar, ad, modul, ek in adimlar:
        if anahtar in args.atla:
            print(f"\n  ⏭  {ad} — atlandı")
            ozet.append((ad, "atlandı", 0.0))
            continue
        if anahtar == "solomon":
            try:
                import ortools  # noqa: F401
            except ImportError:
                print(f"\n  ⏭  {ad} — ortools kurulu değil, atlandı "
                      f"(python -m pip install ortools vrplib)")
                ozet.append((ad, "ortools yok", 0.0))
                continue
        basarili, sure = calistir(ad, modul, ek)
        if anahtar == "dashboard" and basarili:
            subprocess.run([sys.executable, "-X", "utf8", "make_standalone.py"], cwd=KOK)
        ozet.append((ad, "TAMAM" if basarili else "HATA", sure))
        toplam += sure

    print("\n" + "=" * 78)
    print("ÖZET")
    print("=" * 78)
    for ad, durum, sure in ozet:
        print(f"  {durum:12s} {sure:7.1f} sn   {ad}")
    print(f"\n  Toplam süre: {toplam / 60:.1f} dakika")
    print("\n  Çıktılar:")
    print("    data/synthetic/v2_*.csv, solomon_dogrulama_sonuclari.csv")
    print("    docs/figurler/*.png")
    print("    Yorumlar: docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md")


if __name__ == "__main__":
    main()
