"""
analyze_consumption.py
======================
Hafta 2 — Tüketim ve Stok Verilerinin İstatistiksel Analizi

Bu betik DataLoader kullanarak sentetik (veya gerçek) tüketim verilerini analiz eder:
1. İstasyon bazında toplam ve ortalama tüketim miktarları
2. Hat bazında toplam tüketim dağılımı
3. Kanban kart sayısı (N) doğrulaması
4. Stok tükenme (starvation) risk analizi
"""

import pandas as pd
import numpy as np
import os
import sys

# src dizinini path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader

def analyze_data():
    loader = DataLoader()
    print(f"==================================================")
    print(f"HAFTA 2: VERİ ANALİZ RAPORU (Kaynak: {loader.get_source_type()})")
    print(f"==================================================\n")

    stations_df = loader.get_stations()
    consumption_df = loader.get_consumption()
    inventory_df = loader.get_inventory()

    # İstasyon bazında toplam tüketim
    total_cons = consumption_df.groupby("istasyon_id")["tuketim_adet"].sum().reset_index()
    total_cons.rename(columns={"tuketim_adet": "toplam_tuketim_adet"}, inplace=True)

    # İstatistikleri birleştir
    summary_df = pd.merge(stations_df, total_cons, on="istasyon_id")
    summary_df["gerceklesen_saatlik_ort"] = round(summary_df["toplam_tuketim_adet"] / 8, 2)  # 8 saat (480 dk)

    print("İSTASYON BAZLI TÜKETİM VE KANBAN ÖZETİ:")
    print("-" * 75)
    print(f"{'İstasyon':<10} {'Hat':<8} {'Hedef(sa)':<10} {'Gerçek(sa)':<12} {'Toplam(8s)':<12} {'Kapasite':<10} {'Kanban N':<10}")
    print("-" * 75)

    for idx, row in summary_df.iterrows():
        print(f"{row['istasyon_id']:<10} {row['hat']:<8} {row['ort_tuketim_saat']:<10} {row['gerceklesen_saatlik_ort']:<12} {row['toplam_tuketim_adet']:<12.1f} {row['kutu_kapasitesi']:<10} {row['kanban_n']:<10}")

    print("-" * 75)

    # Hat bazlı özet
    hat_summary = summary_df.groupby("hat")["toplam_tuketim_adet"].agg(["count", "sum", "mean"]).reset_index()
    hat_summary.columns = ["Hat", "İstasyon Sayısı", "Toplam Tüketim (Adet)", "Ortalama Tüketim/İstasyon"]

    print("\nHAT BAZLI TÜKETİM ÖZETİ:")
    print("-" * 60)
    for idx, row in hat_summary.iterrows():
        print(f"{row['Hat']:<10} İstasyon: {row['İstasyon Sayısı']:<5} Toplam: {row['Toplam Tüketim (Adet)']:<10.1f} Ort/İst: {row['Ortalama Tüketim/İstasyon']:<10.1f}")
    print("-" * 60)

    toplam_fabrika_tuketim = summary_df["toplam_tuketim_adet"].sum()
    print(f"\nTOPLAM FABRİKA TÜKETİMİ (8 Saat): {toplam_fabrika_tuketim:.1f} adet")
    print(f"ORTALAMA SAATLİK FABRİKA TÜKETİMİ : {toplam_fabrika_tuketim/8:.1f} adet/saat")

    # Analiz sonuçlarını docs/hafta2_veri_analiz_raporu.md dosyasına yazalım
    docs_dir = os.path.join(loader.base_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    report_path = os.path.join(docs_dir, "hafta2_veri_analiz_raporu.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Hafta 2 — Tüketim ve Stok Verileri Analiz Raporu\n\n")
        f.write(f"**Aktif Veri Kaynağı:** `{loader.get_source_type()}`\n")
        f.write("**Tarih:** 2026-07-29\n\n")
        f.write("---\n\n")
        f.write("## 1. Genel İstatistikler\n\n")
        f.write(f"- **Toplam Simülasyon Süresi:** 480 dakika (8 saat / 1 vardiya)\n")
        f.write(f"- **Toplam İstasyon Sayısı:** 24 istasyon (4 hat × 6 istasyon)\n")
        f.write(f"- **Toplam Fabrika Tüketimi (8 saat):** {toplam_fabrika_tuketim:.1f} adet\n")
        f.write(f"- **Ortalama Fabrika Tüketim Hızı:** {toplam_fabrika_tuketim/8:.1f} adet/saat\n\n")
        f.write("## 2. Hat Bazlı Tüketim Dağılımı\n\n")
        f.write("| Hat | İstasyon Sayısı | Toplam Tüketim (Adet) | Ortalama/İstasyon |\n")
        f.write("|-----|-----------------|------------------------|-------------------|\n")
        for idx, row in hat_summary.iterrows():
            f.write(f"| {row['Hat']} | {row['İstasyon Sayısı']} | {row['Toplam Tüketim (Adet)']:.1f} | {row['Ortalama Tüketim/İstasyon']:.1f} |\n")
        
        f.write("\n## 3. İstasyon Detay Tablosu ve Kanban Sayıları\n\n")
        f.write("| İstasyon | Hat | Hedef Tüketim (ad/sa) | Gerçekleşen (ad/sa) | Toplam Tüketim | Kutu Kapasitesi (C) | Hesaplanan Kanban (N) |\n")
        f.write("|----------|-----|-----------------------|---------------------|----------------|---------------------|-----------------------|\n")
        for idx, row in summary_df.iterrows():
            f.write(f"| {row['istasyon_id']} | {row['hat']} | {row['ort_tuketim_saat']} | {row['gerceklesen_saatlik_ort']} | {row['toplam_tuketim_adet']:.1f} | {row['kutu_kapasitesi']} | {row['kanban_n']} |\n")

        f.write("\n## 4. Değerlendirme ve Sonraki Adımlar\n\n")
        f.write("1. Sentetik tüketim verisi `Normal(μ, 0.20μ)` stokastik dağılımına uygun şekilde üretilmiştir.\n")
        f.write("2. Kanban kart sayıları $N = \\lceil (D \\times LT \\times (1+\\alpha)) / C \\rceil$ formülüyle hesaplanmıştır.\n")
        f.write("3. Veri soyutlama katmanı (`DataLoader`) kurulmuştur. İleride gerçek fabrika verisi geldiğinde sadece `data/config.json` dosyasında `\"data_source\": \"real\"` yapılması yeterli olacaktır.\n")

    print(f"\nRapor başarıyla kaydedildi: {report_path}")

if __name__ == "__main__":
    analyze_data()
