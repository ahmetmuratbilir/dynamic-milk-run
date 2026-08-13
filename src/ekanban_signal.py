"""
ekanban_signal.py
=================
Hafta 4 — E-Kanban Sinyal Mimarisi

⚠️ UYARI: Bu modül SENTETİK veriyle çalışır.
Gerçek veri için data/config.json → "real" yapın.

Uygulanan Kararlar (karar_gunlugu.md):
  K25: ROP = D_dk × LT × (1+α)            — oransal tampon, Klenk(2012) satır 1199
  K26: Karma öncelik: Kritiklik + FIFO     — Facchini(2022) satır 416, Simić(2020) satır 301
  K27: TW_bitis = min(t_starv-5, t+60)    — dinamik, starvation bazlı
  K28: Açık sinyal güncellenir, tekrar üretilmez
  K29: Stok yenileme = sinyal+LT(45dk) ⚠️ GEÇİCİ — Hafta 5-6'da VRPTW ile değişecek
"""

import math
import os
import sys
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader


class EKanbanSimulator:
    """
    480 dakikalık E-Kanban sinyal simülatörü.

    Her dakika:
      1. Tüketim uygula
      2. ROP kontrolü → sinyal üret (K25)
      3. Açık sinyalleri güncelle (K28)
      4. Stok yenileme: sinyal+LT sonra (K29 — GEÇİCİ)
      5. Starvation kaydı
    """

    def __init__(self, loader: DataLoader, alpha: float = 0.15):
        self.loader    = loader
        self.LT        = 45      # K07
        self.ALPHA     = alpha   # K08
        self.TW_MAX    = 60      # K16 — üst sınır
        self.TW_SAFETY = 5       # K27 — starvation'dan kaç dk önce pencere kapansın

        # Veriler
        stations_df       = loader.get_stations()
        self.consumption_df = loader.get_consumption()
        self.inventory_df   = loader.get_inventory()

        # İstasyon sözlükleri
        self.istasyonlar = {}
        for _, row in stations_df.iterrows():
            sid = row["istasyon_id"]
            D_dk = row["ort_tuketim_saat"] / 60
            # K25: ROP formülü
            rop  = D_dk * self.LT * (1 + self.ALPHA)
            self.istasyonlar[sid] = {
                "hat":         row["hat"],
                "D_dk":        D_dk,
                "C":           row["kutu_kapasitesi"],
                "N":           row["kanban_n"],
                "rop":         rop,
                "stok":        row["baslangic_stok_adet"],  # başlangıç stoku
                "acik_sinyal": False,   # K28: açık sinyal var mı?
                "sinyal_dk":   None,    # açık sinyalin başladığı dakika
                "sinyal_id":   None,    # açık sinyalin ID'si
                "yenileme_dk": None,    # K29: stok ne zaman yenilenecek
            }

        # Dakikalık tüketim tablosu → hızlı erişim için pivot
        self.tuketim_pivot = (
            self.consumption_df
            .pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")
        )

        # Çıktı listeleri
        self.sinyaller    = []   # tüm üretilen sinyaller
        self.starvations  = []   # stok=0 olayları
        self._sinyal_sayac = {}  # istasyon başına sinyal numaralandırma

    # ─────────────────────────────────────────────────────────
    def _sinyal_id_uret(self, istasyon_id: str) -> str:
        n = self._sinyal_sayac.get(istasyon_id, 0) + 1
        self._sinyal_sayac[istasyon_id] = n
        return f"{istasyon_id}_{n:03d}"

    def _starvation_suresi(self, istasyon_id: str, t: int) -> float:
        """K27: Şu anki stokla istasyon kaç dakikada stoka düşer?"""
        ist  = self.istasyonlar[istasyon_id]
        if ist["D_dk"] == 0:
            return float("inf")
        return t + ist["stok"] / ist["D_dk"]

    def _tw_bitis_hesapla(self, istasyon_id: str, t_sinyal: int) -> tuple:
        """
        K27: TW_bitis = min(t_starvation - TW_SAFETY, t_sinyal + TW_MAX)
        Dinamik — sabit +60 değil.

        Guard (K30): TW_bitis >= t_sinyal + LT
        Eğer starvation LT'den önce geliyorsa → KRİTİK_ACIL sinyali.
        Karar K30: karar_gunlugu.md
        """
        t_starv    = self._starvation_suresi(istasyon_id, t_sinyal)
        dinamik    = t_starv - self.TW_SAFETY
        sabit      = t_sinyal + self.TW_MAX
        tw_ham     = int(min(dinamik, sabit))
        # Guard: alt sınır = t_sinyal + LT (K29 yenilemenin pencereye sığması için)
        tw_guard   = t_sinyal + self.LT
        tw_bitis   = max(tw_ham, tw_guard)
        kritik     = (t_starv - t_sinyal) < self.LT  # starvation LT'den önce mi?
        return tw_bitis, kritik

    # ─────────────────────────────────────────────────────────
    def _sinyal_uret(self, istasyon_id: str, t: int):
        """Yeni E-Kanban sinyali üretir ve kaydeder."""
        ist       = self.istasyonlar[istasyon_id]
        sinyal_id = self._sinyal_id_uret(istasyon_id)
        t_starv   = self._starvation_suresi(istasyon_id, t)
        tw_bitis, kritik_acil = self._tw_bitis_hesapla(istasyon_id, t)

        # Kritiklik skoru (K26): düşükse daha acil
        kritiklik = ist["stok"] / ist["rop"] if ist["rop"] > 0 else 0

        # Durum: K30 guard — starvation LT'den önce geliyorsa KRİTİK_ACIL
        durum = "KRİTİK_ACIL" if kritik_acil else "ACIK"
        # K32: Isınma Periyodu Etiketi (0-45 dk)
        periyot = "ISINMA (0-45dk)" if t < self.LT else "KARARLI (45-480dk)"

        sinyal = {
            "sinyal_id":        sinyal_id,
            "istasyon_id":      istasyon_id,
            "hat":              ist["hat"],
            "sinyal_dk":        t,
            "periyot":          periyot,
            "stok_o_an":        round(ist["stok"], 3),
            "rop_esigi":        round(ist["rop"], 3),
            "kritiklik_skoru":  round(kritiklik, 4),
            "tw_baslangic":     t,
            "tw_bitis":         tw_bitis,
            "tw_genislik_dk":   tw_bitis - t,
            "starvation_riski": round(t_starv, 1),
            "lt_dk":            self.LT,
            "istenen_kutu":     ist["N"],
            "istenen_adet":     ist["N"] * ist["C"],
            "durum":            durum,
            "_son_guncelleme":  t,
        }

        self.sinyaller.append(sinyal)

        # İstasyona işaret koy (K28)
        ist["acik_sinyal"] = True
        ist["sinyal_dk"]   = t
        ist["sinyal_id"]   = sinyal_id
        # K29 (GEÇİCİ): LT dakika sonra stok yenilenecek
        ist["yenileme_dk"] = t + self.LT

    def _acik_sinyal_guncelle(self, istasyon_id: str, t: int):
        """
        K28: Açık sinyal varken kritiklik_skoru ve stok_o_an güncellenir.
        Yeni sinyal üretilmez.
        """
        ist = self.istasyonlar[istasyon_id]
        if not ist["acik_sinyal"]:
            return
        # Sinyali bul ve güncelle
        for sinyal in reversed(self.sinyaller):
            if sinyal["sinyal_id"] == ist["sinyal_id"]:
                kritiklik = ist["stok"] / ist["rop"] if ist["rop"] > 0 else 0
                sinyal["stok_o_an"]       = round(ist["stok"], 3)
                sinyal["kritiklik_skoru"] = round(kritiklik, 4)
                sinyal["_son_guncelleme"] = t
                break

    def _stok_yenile(self, istasyon_id: str, t: int):
        """
        K29 (GEÇİCİ BASITLEŞTİRME): sinyal+LT sonra stok yenilenir.
        Hafta 5-6'da VRPTW gerçek rota süresiyle değiştirilecek.
        """
        ist = self.istasyonlar[istasyon_id]
        if ist["yenileme_dk"] is None or t != ist["yenileme_dk"]:
            return
        if not ist["acik_sinyal"]:
            return

        # Stok yenile
        ist["stok"]       += ist["N"] * ist["C"]
        ist["acik_sinyal"] = False
        ist["sinyal_dk"]   = None
        ist["sinyal_id"]   = None
        ist["yenileme_dk"] = None

        # Sinyali "teslim edildi (varsayım)" olarak işaretle
        for sinyal in reversed(self.sinyaller):
            if sinyal["istasyon_id"] == istasyon_id and sinyal["durum"] in ("ACIK", "KRİTİK_ACIL"):
                sinyal["durum"] = "TESLİM(VARSAYIM)"
                break

    # ─────────────────────────────────────────────────────────
    def run(self) -> pd.DataFrame:
        """
        480 dakikalık simülasyonu çalıştırır.
        Döndürür: ekanban_signals DataFrame
        """
        print("⚠️  SENTETİK veri ile çalışılıyor (config.json: synthetic)")
        print(f"Simülasyon başlıyor: 480 dk, {len(self.istasyonlar)} istasyon...\n")

        for t in range(480):
            # 1. Her istasyon için tüketim ve ROP kontrolü
            for sid, ist in self.istasyonlar.items():

                # K29: Önce stok yenileme kontrolü
                self._stok_yenile(sid, t)

                # Tüketim uygula
                tuketim = self.tuketim_pivot.at[t, sid] if t in self.tuketim_pivot.index else 0
                ist["stok"] = max(0.0, ist["stok"] - tuketim)

                # Starvation kontrolü
                if ist["stok"] <= 0:
                    self.starvations.append({
                        "dakika":      t,
                        "istasyon_id": sid,
                        "hat":         ist["hat"],
                    })

                # K28: Açık sinyal varsa güncelle, yeni sinyal üretme
                if ist["acik_sinyal"]:
                    self._acik_sinyal_guncelle(sid, t)
                    continue

                # K25: ROP kontrolü — sinyal tetikleme
                if ist["stok"] <= ist["rop"]:
                    self._sinyal_uret(sid, t)

            # 2. K26: Aktif sinyalleri Karma kuralla sırala
            acik_sinyaller = [s for s in self.sinyaller if s["durum"] == "ACIK"]
            acik_sinyaller.sort(key=lambda s: (s["kritiklik_skoru"], s["sinyal_dk"]))
            for sira, sinyal in enumerate(acik_sinyaller, 1):
                sinyal["oncelik_sirasi"] = sira

        # ── Sonuçları temizle ──
        df = pd.DataFrame(self.sinyaller)
        if "_son_guncelleme" in df.columns:
            df.drop(columns=["_son_guncelleme"], inplace=True)
        # Kalan ACIK/KRİTİK_ACIL = simülasyon ufku kesilmesi (480.dk)
        # ⚠️ Gerçek başarısızlık değil — LT henüz dolmamış
        df.loc[df["durum"] == "ACIK", "durum"] = "ACIK(UFUK)"
        df.loc[df["durum"] == "KRİTİK_ACIL", "durum"] = "KRİTİK_ACIL(UFUK)"
        return df

    def starvation_raporu(self) -> pd.DataFrame:
        return pd.DataFrame(self.starvations)


# ─────────────────────────────────────────────────────────────
def main():
    loader = DataLoader()
    sim    = EKanbanSimulator(loader)
    df     = sim.run()
    starv  = sim.starvation_raporu()

    out_dir = os.path.join(loader.base_dir, "data", "synthetic")
    df.to_csv(os.path.join(out_dir, "ekanban_signals.csv"), index=False, encoding="utf-8")

    # ── Özet Rapor ──
    print("=" * 60)
    print("HAFTA 4: E-KANBAN SİMÜLASYON SONUÇLARI")
    print("⚠️  SENTETİK VERİ | config.json → 'real' ile gerçek veri kullanılır")
    print("=" * 60)

    isinma_df = df[df["periyot"] == "ISINMA (0-45dk)"]
    kararli_df = df[df["periyot"] == "KARARLI (45-480dk)"]

    isinma_teslim  = len(isinma_df[isinma_df["durum"] == "TESLİM(VARSAYIM)"])
    isinma_acik    = len(isinma_df[isinma_df["durum"].isin(["ACIK(UFUK)", "KRİTİK_ACIL(UFUK)"])])
    kararli_teslim = len(kararli_df[kararli_df["durum"] == "TESLİM(VARSAYIM)"])
    kararli_acik   = len(kararli_df[kararli_df["durum"].isin(["ACIK(UFUK)", "KRİTİK_ACIL(UFUK)"])])

    print(f"\nPERİYOT BAZLI DETAYLI DAĞILIM:")
    print("-" * 55)
    print(f"  Isınma (0-45 dk)    : {len(isinma_df)} sinyal -> {isinma_teslim} Teslim(Varsayım), {isinma_acik} Açık(Ufuk)")
    print(f"  Kararlı (45-480 dk) : {len(kararli_df)} sinyal -> {kararli_teslim} Teslim(Varsayım), {kararli_acik} Açık(Ufuk)")
    print("-" * 55)
    print(f"\nTeslim(Varsayım) Toplam : {len(df[df['durum'] == 'TESLİM(VARSAYIM)'])}")
    print(f"  ⚠️  Bu gerçek rota performansı DEĞİL ('sinyal+LT<=480' şartı)")
    print(f"  ⚠️  Gerçek teslim performansı Hafta 5-6 VRPTW ile ölçülecek")
    print(f"Hâlâ Açık (ufuk kesimi) : {len(df[df['durum'].isin(['ACIK(UFUK)', 'KRİTİK_ACIL(UFUK)'])])}")
    print(f"  ⚠️  480.dk kesilmesinden dolayı — gerçek başarısızlık değil")
    print(f"KRİTİK_ACIL Sinyal      : {len(df[df['durum'] == 'KRİTİK_ACIL'])}  (TW<LT, K30 guard devrede)")
    print(f"Starvation Olayı        : {len(starv)}")

    print("\nİSTASYON BAZLI SİNYAL DAĞILIMI (İlk 10):")
    print("-" * 50)
    ist_ozet = (df.groupby(["istasyon_id", "hat"])
                  .size()
                  .reset_index(name="sinyal_sayisi")
                  .sort_values("sinyal_sayisi", ascending=False))
    print(ist_ozet.to_string(index=False))

    print("\nDİNAMİK ZAMAN PENCERESİ ÖRNEKLERİ (İlk 5 sinyal):")
    print("-" * 70)
    cols = ["sinyal_id", "sinyal_dk", "stok_o_an", "rop_esigi",
            "tw_bitis", "tw_genislik_dk", "starvation_riski", "kritiklik_skoru"]
    print(df[cols].head(10).to_string(index=False))

    # S16 özel analizi (en kırılgan istasyon)
    s16 = df[df["istasyon_id"] == "S16"]
    print(f"\nS16 ÖZEL ANALİZİ (En Kırılgan İstasyon — D=24 adet/sa):")
    print("-" * 50)
    print(f"  Toplam sinyal   : {len(s16)}")
    if len(s16) > 0:
        print(f"  Ort. TW genişlik: {s16['tw_genislik_dk'].mean():.1f} dk")
        print(f"  Min TW genişlik : {s16['tw_genislik_dk'].min():.1f} dk")
        print(f"  Ort. kritiklik  : {s16['kritiklik_skoru'].mean():.4f}")

    if len(starv) > 0:
        print(f"\n⚠️  STARVATION DETAYI:")
        print(starv.groupby("istasyon_id").size().reset_index(name="starvation_sayisi")
                   .to_string(index=False))
    else:
        print("\n✅ Starvation yok — sistem tüm istasyonları stoksuz bırakmadı.")

    # Markdown rapor
    docs_dir  = os.path.join(loader.base_dir, "docs")
    rapor_yol = os.path.join(docs_dir, "hafta4_ekanban_analiz.md")
    with open(rapor_yol, "w", encoding="utf-8") as f:
        f.write("# Hafta 4 — E-Kanban Sinyal Simülasyonu Analiz Raporu\n\n")
        f.write("> ⚠️ **SENTETİK VERİ** — Gerçek veri için `data/config.json → \"real\"`\n\n")
        f.write("**Uygulanan Kararlar:** K25, K26, K27, K28, K29 — bkz. `karar_gunlugu.md`\n\n---\n\n")
        f.write("## 1. Genel Özet\n\n")
        f.write(f"| Metrik | Isınma (0-45dk) | Kararlı (45-480dk) | Toplam |\n")
        f.write(f"|--------|-----------------|--------------------|--------|\n")
        f.write(f"| Sinyal Sayısı | {len(isinma_df)} | {len(kararli_df)} | {len(df)} |\n")
        f.write(f"| Teslim (Varsayım) | {isinma_teslim} | {kararli_teslim} | {isinma_teslim+kararli_teslim} |\n")
        f.write(f"| Açık (Ufuk Kesimi) | {isinma_acik} | {kararli_acik} | {isinma_acik+kararli_acik} |\n")
        f.write(f"| Starvation | 0 | 0 | {len(starv)} |\n\n")
        f.write("## 2. İstasyon Bazlı Sinyal Dağılımı\n\n")
        f.write(ist_ozet.to_markdown(index=False))
        f.write("\n\n## 3. Dinamik TW Örnekleri (K27)\n\n")
        f.write(df[cols].head(20).to_markdown(index=False))
        f.write("\n\n## 4. S16 Özel Analizi\n\n")
        if len(s16) > 0:
            f.write(s16[cols].to_markdown(index=False))
        f.write("\n\n## 5. ⚠️ Geçici Basitleştirme Notu (K29)\n\n")
        f.write("Bu simülasyonda stok yenileme `sinyal anı + LT(45 dk)` ile yapılmaktadır.\n")
        f.write("Hafta 5-6'da VRPTW gerçek rota süresi hesaplandıktan sonra bu değer güncellenecektir.\n")

    print(f"\nSinyaller kaydedildi : data/synthetic/ekanban_signals.csv ({len(df)} satır)")
    print(f"Analiz raporu        : docs/hafta4_ekanban_analiz.md")


if __name__ == "__main__":
    main()
