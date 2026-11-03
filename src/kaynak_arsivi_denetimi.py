"""
kaynak_arsivi_denetimi.py
=========================
Kaynak Arşivi Bütünlük Denetimi (K87)

Ne yapar
--------
1. Masaüstü `dinamik milk run` klasöründeki **zip dosyalarının** içeriğini listeler ve
   çıkarılmış klasörlerle karşılaştırır: zip'te olup çıkarılmamış dosya var mı?
2. Masaüstü arşivi ile proje arşivini (`docs/papers/`) karşılaştırır.
3. MD5 ile kopyaları tespit eder, **özgün çalışma sayısını** verir.
4. Metne çıkarılmamış (`docs/papers/extracted_text/` altında karşılığı olmayan)
   PDF'leri bildirir.
5. `docs/hafta1_referans_listesi.md` ve `docs/master_makale_katalogu.md` içinde kayıtlı
   **edinilmesi gereken** kaynakların hâlâ eksik olup olmadığını kontrol eder.

Neden gerekli
-------------
26.10.2026 denetiminde (K87), zip dosyalarının içeriğinin çıkarılmış klasörlerle özdeş
olduğu ve eksikliğin zip'lerde değil **hiç edinilmemiş kaynaklarda** olduğu tespit
edilmiştir. Bu betik, yeni makale eklendiğinde denetimin tekrarlanmasını sağlar.

Kullanım
--------
    python -X utf8 -m src.kaynak_arsivi_denetimi
    python -X utf8 -m src.kaynak_arsivi_denetimi --arsiv "D:/baska/klasor"
"""

import argparse
import hashlib
import os
import re
import sys
import zipfile
from collections import defaultdict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARSAYILAN_ARSIV = os.path.join(os.path.expanduser("~"), "Desktop", "dinamik milk run")

# K87'de belirlenen, edinilmesi gereken kaynaklar (dosya adında aranacak ipuçları)
BEKLENEN_EKSIKLER = [
    ("🔴", "Alnahhal, Ramadan & Noche (2016) — Static vs Dynamic Control",
     ["static", "versus", "dynamic control"]),
    ("🔴", "Ciemnoczolowski & Bozer (2013) — Number of Kanban and starvation",
     ["ciemnoczolowski", "small-batch container"]),
    ("🟠", "Bocewicz vd. (2019) — fleet size / storage capacity trade-off",
     ["bocewicz", "fleet size"]),
    ("🟠", "Schmidt vd. (2016) — New design guidelines",
     ["new design guidelines", "schmidt"]),
    ("🟡", "VDI 5586 Blatt 2 (2022)", ["vdi 5586", "vdi5586"]),
    ("🟡", "Kundu vd. (2019) — kanban line feeding, DES+PSO",
     ["kundu", "particle swarm optimization a study"]),
    ("🟡", "Korytkowski & Karkoszka (2016) — milk-run operator disturbances",
     ["korytkowski"]),
    ("🔴", "Sugimori vd. (1977) — Toyota formülü (K06'nın asıl kaynağı, K88)",
     ["sugimori", "toyota production system and kanban"]),
]


def md5(yol: str, blok: int = 1 << 20) -> str:
    h = hashlib.md5()
    with open(yol, "rb") as f:
        while (p := f.read(blok)):
            h.update(p)
    return h.hexdigest()


def pdf_topla(kok: str) -> list:
    return [os.path.join(k, d) for k, _, dl in os.walk(kok)
            for d in dl if d.lower().endswith(".pdf")]


def zip_denetimi(arsiv: str) -> dict:
    print("\n── 1) ZIP İÇERİK DENETİMİ ──")
    diskteki = {os.path.basename(p) for p in pdf_topla(arsiv)}
    cikarilmamis = defaultdict(list)
    zipler = [os.path.join(k, d) for k, _, dl in os.walk(arsiv)
              for d in dl if d.lower().endswith(".zip")]
    if not zipler:
        print("  (zip dosyası yok)")
    for z in zipler:
        ad = os.path.relpath(z, arsiv)
        try:
            with zipfile.ZipFile(z) as a:
                girdiler = [e for e in a.namelist() if not e.endswith("/")]
                pdfler = [e for e in girdiler if e.lower().endswith(".pdf")]
                print(f"  {ad}  ({os.path.getsize(z) / 1e6:.1f} MB) — "
                      f"{len(girdiler)} girdi, {len(pdfler)} PDF")
                if not girdiler:
                    print("     ⚠️ BOŞ ARŞİV")
                for e in pdfler:
                    if os.path.basename(e) not in diskteki:
                        cikarilmamis[ad].append(os.path.basename(e))
        except zipfile.BadZipFile:
            print(f"  {ad} — ⚠️ BOZUK ZIP")
    if cikarilmamis:
        print("\n  ⚠️ ZIP'TE OLUP ÇIKARILMAMIŞ DOSYALAR:")
        for z, dosyalar in cikarilmamis.items():
            for d in dosyalar:
                print(f"     {z} → {d}")
    else:
        print("\n  ✅ Zip içerikleri çıkarılmış klasörlerle örtüşüyor; "
              "çıkarılmamış PDF yok.")
    return cikarilmamis


def kopya_denetimi(arsiv: str) -> int:
    print("\n── 2) ÖZGÜN ÇALIŞMA SAYISI (MD5) ──")
    pdfler = pdf_topla(arsiv)
    gruplar = defaultdict(list)
    for p in pdfler:
        gruplar[md5(p)].append(os.path.relpath(p, arsiv))
    kopyalar = {h: g for h, g in gruplar.items() if len(g) > 1}
    print(f"  Toplam PDF: {len(pdfler)} | Özgün: {len(gruplar)} | "
          f"Kopya grubu: {len(kopyalar)}")
    for g in kopyalar.values():
        print(f"     kopya: {' == '.join(g)}")
    return len(gruplar)


def proje_karsilastirma(arsiv: str):
    print("\n── 3) MASAÜSTÜ ARŞİVİ ↔ PROJE ARŞİVİ ──")
    proje_papers = os.path.join(KOK, "docs", "papers")
    if not os.path.isdir(proje_papers):
        print("  (docs/papers yok)")
        return
    m_hash = {}
    for p in pdf_topla(arsiv):
        m_hash.setdefault(md5(p), os.path.relpath(p, arsiv))
    p_hash = {md5(p) for p in pdf_topla(proje_papers)}
    print(f"  Masaüstünde özgün: {len(m_hash)} | Projede özgün: {len(p_hash)}")
    yok = [ad for h, ad in m_hash.items() if h not in p_hash]
    if yok:
        print(f"  ⚠️ Masaüstünde olup projede OLMAYAN: {len(yok)} dosya")
        for ad in sorted(yok):
            print(f"     {ad}")
    else:
        print("  ✅ Masaüstündeki her PDF projede mevcut.")


def metin_denetimi(arsiv: str):
    print("\n── 4) METNE ÇIKARILMAMIŞ PDF'LER ──")
    metin_dizin = os.path.join(KOK, "docs", "papers", "extracted_text")
    if not os.path.isdir(metin_dizin):
        print("  (extracted_text yok)")
        return
    govdeler = {os.path.splitext(d)[0].lower()
                for d in os.listdir(metin_dizin) if d.endswith(".txt")}
    eksik = []
    for p in pdf_topla(arsiv):
        govde = os.path.splitext(os.path.basename(p))[0].lower()
        if not any(govde[:42] in g or g[:42] in govde for g in govdeler):
            eksik.append(os.path.basename(p))
    if eksik:
        print(f"  ⚠️ {len(eksik)} PDF metne çıkarılmamış:")
        for d in sorted(set(eksik)):
            print(f"     {d}")
    else:
        print("  ✅ Tüm PDF'lerin metin karşılığı var.")


def eksik_kaynak_denetimi(arsiv: str):
    print("\n── 5) EDİNİLMESİ GEREKEN KAYNAKLAR (K87) ──")
    adlar = " | ".join(os.path.basename(p).lower() for p in pdf_topla(arsiv))
    metin_dizin = os.path.join(KOK, "docs", "papers", "extracted_text")
    if os.path.isdir(metin_dizin):
        adlar += " | " + " | ".join(d.lower() for d in os.listdir(metin_dizin))
    hala_eksik = 0
    for oncelik, kunye, ipuclari in BEKLENEN_EKSIKLER:
        bulundu = any(re.search(re.escape(i), adlar) for i in ipuclari)
        if bulundu:
            print(f"  ✅ {oncelik} {kunye}  → arşivde bulundu")
        else:
            hala_eksik += 1
            print(f"  ❌ {oncelik} {kunye}")
    print(f"\n  Hâlâ eksik: {hala_eksik}/{len(BEKLENEN_EKSIKLER)}")
    if hala_eksik:
        print("  Künyeler: docs/hafta1_referans_listesi.md → EK bölümü")
        print("  Gerekçe : docs/literatur_boslugu_analizi.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arsiv", default=VARSAYILAN_ARSIV,
                    help="kaynak arşivi klasörü (varsayılan: masaüstü/dinamik milk run)")
    args = ap.parse_args()

    print("=" * 78)
    print("KAYNAK ARŞİVİ BÜTÜNLÜK DENETİMİ (K87)")
    print(f"  Arşiv: {args.arsiv}")
    print("=" * 78)
    if not os.path.isdir(args.arsiv):
        print("  ⚠️ Arşiv klasörü bulunamadı.")
        return

    zip_denetimi(args.arsiv)
    kopya_denetimi(args.arsiv)
    proje_karsilastirma(args.arsiv)
    metin_denetimi(args.arsiv)
    eksik_kaynak_denetimi(args.arsiv)


if __name__ == "__main__":
    main()
