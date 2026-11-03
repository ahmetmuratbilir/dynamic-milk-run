"""
v2_entegre_simulasyon.py
========================
Hafta 14 — Kanonik Simülasyon Motoru v2 (Kapalı Döngü Entegre Milk-Run / E-Kanban)

Neden v2? (Hafta 14 literatür denetimi — docs/hafta14_literatur_denetimi_ve_revizyon_raporu.md)
  v1 motoru (ekanban_signal.py + vrptw_solver.py + hafta8_kanban_karsilastirma.py) raporlanan
  tüm H4–H13 sayılarını üretir ve DEĞİŞTİRİLMEDEN korunur. v2, denetimde tespit edilen
  yapısal sorunları tek motorda giderir:

  K65  Raf boyutlandırma: VDI 5586 "+1 değişim pozisyonu" (Urru vd. 2018 s.406; iki kutu
       prensibi: Klenk vd. 2012 s.11, Vojdani & Drechsler 2022 s.5, Droste & Deuse 2011 s.607)
  K66  Tek hizmet süresi modeli: tur başına yükleme + durak başına boşaltma; statik ve
       dinamik politikalar AYNI süreleri kullanır (v1'de 3 dk vs 5+3 dk asimetrisi vardı)
  K67  "Tur başına en fazla 5 durak" kuralı kaldırıldı (parametre olarak kaldı); araç
       kapasitesi (25 kutu) ve tur süresi (90 dk) bağlayıcıdır
  K68  Konsolidasyonlu sevk: en geç kalkış kuralı (Vojdani & Drechsler 2022 s.5–6;
       Sevim & Görkemli Aykut 2026 s.66; Menanno vd. 2023 s.13–14)
  K69  Kapalı döngü: sinyaller gerçek stoktan, gerçek teslimlerden sonra üretilir
       (Facchini vd. 2022 s.1126 — "stand-alone değil, uçtan uca")
  K70  Talep modeli: saatlik tüketim ~ N(μ, 0.20μ) doğrudan (saatlik rejim) — v1'de σ/60
       dakikalık gürültü, onaylı CV'yi √60 kat küçültüyordu; alternatif: Poisson
  K71  Metrik mesafe: ham matris üçgen eşitsizliğini ihlal ettiği için Floyd–Warshall
       en kısa yol kapanışı uygulanır (araç yol ağında en kısa yolu kullanır)
  K72  Esnek zaman penceresi (VRP-RTW; Fitrie vd. 2025, Zidanne vd. 2025) + tur süresi
       kısıtı (Facchini vd. 2022 s.1124, Denk. 7) + 2-opt iyileştirme
       (Gendreau & Tarantilis 2010, Bölüm 1.1)
  K73  Politika seti: P1 sabit takt–sabit miktar, P2 sabit takt–Kanban miktarı
       (Klenk s.6, Simić s.10–11, Vojdani s.6), P3 olay tabanlı dinamik
  K74  Opsiyonel koşu-içi dinamik N (Uyarlanabilir Kanban; Elloumi vd. 2025 s.613)

Zaman ilerletme: 1 dakikalık SABİT ZAMAN ADIMI (fixed-increment time advance). v1 ile
aynı yapı; metinde "ayrık olay simülasyonu" değil "sabit zaman adımlı simülasyon" denmelidir.

Dakika içi olay sırası (v1 ile aynı):
  1) o dakikaya düşen teslimler stoka eklenir (raf tavanı N×C)
  2) tüketim uygulanır, stok ≤ 0 ise istasyon-dakikası starvation sayılır
  3) (P3) ROP kontrolü ile sinyal üretimi
  4) sevk kararı (P3: boştaki araçlar; P1/P2: takvim)

Kullanım:
    from src.v2_entegre_simulasyon import V2Parametre, simule_et
    sonuc = simule_et(V2Parametre(politika="P3", sevk="KONSOLIDASYON", arac_sayisi=4, seed=1001))
"""

import os
import sys
import math
from dataclasses import dataclass, replace
from typing import Optional

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import DataLoader


# ─────────────────────────────────────────────────────────────
# Parametreler
# ─────────────────────────────────────────────────────────────
@dataclass
class V2Parametre:
    # Politika (K73)
    politika: str = "P3"                 # "P1" | "P2" | "P3"
    sevk: str = "KONSOLIDASYON"          # P3 için: "ANINDA" | "KONSOLIDASYON" (K68)
    dispatch_kural: str = "EDD"          # "EDD" | "SLACK" | "FIFO" | "KRITIKLIK"
    arac_sayisi: int = 4
    tur_araligi_dk: int = 60             # P1/P2 sabit takt (Vojdani & Drechsler 2022 s.6: saatlik)

    # Kanban / ROP (K06, K07, K08, K25, K65)
    alpha: float = 0.15
    lt_dk: float = 45.0
    # "V1"      : N = ⌈ROP/C⌉                     (v1 davranışı)
    # "VDI"     : N = 1 + ⌈ROP/C⌉                 (K65 — politika-tutarlı)
    # "IKI_KUTU": N = 2, tüm politikalarda sabit  (K93 — Vojdani & Drechsler 2022 s.5
    #             "Zwei-Behälter-Kanban"; politikadan bağımsız tampon)
    kanban_modu: str = "VDI"
    # K97: istasyon başına açık kart sayısı (adalet kuralı deneyleri); verilirse
    # kanban_modu'nun N'ini geçersiz kılar, ROP formülü değişmez
    n_ozel: Optional[tuple] = None
    dinamik_n: bool = False              # K74
    dinamik_n_periyot_dk: int = 30       # K11
    dinamik_n_pencere_dk: int = 60

    # Zaman penceresi (K16, K27, K30)
    tw_max_dk: float = 60.0
    tw_guvenlik_dk: float = 5.0

    # Hizmet süreleri (K14, K15, K66) — "toplam handling 5 dk = yükleme 2 + boşaltma 3"
    yukleme_dk: float = 2.0              # tur başına, depoda
    durak_servis_dk: float = 3.0         # durak başına sabit
    kutu_basi_servis_dk: float = 0.0     # kutu başına ek (literatür senaryosu: Urru 30 sn)

    # Rota kısıtları (K17, K67, K72)
    max_durak: Optional[int] = None      # v1: 5
    max_tur_dk: Optional[float] = 90.0   # None: kontrol yok (v1 davranışı)
    iki_opt: bool = True
    gecikme_ceza: float = 10.0           # 2-opt maliyetinde dk gecikme başına ağırlık

    # Ağ ve talep (K10, K70, K71)
    mesafe_modu: str = "METRIK"          # "HAM" | "METRIK" | "KOORDINAT" (K100, K105)
    talep_modeli: str = "SAATLIK_REJIM"  # "CSV" | "NORMAL_DK_V1" | "SAATLIK_REJIM" | "POISSON"
    talep_carpani: float = 1.0           # talep şoku (tasarım D'si değişmez)
    hiz_carpani: float = 1.0             # >1: süreler uzar

    # Simülasyon
    sim_sure: int = 480
    # K78: Welch grafik yöntemiyle ölçülen ısınma süresi = 90 dk (v1'de 45 dk varsayılmıştı).
    # Dolu raflarla başlayan sistemde WIP ortalaması 45. dk'da kararlı değerin ~%54 üzerinde,
    # 90. dk'da ~%1 içindedir (bkz. src/v2_dogrulama_ve_kalibrasyon.py, D2).
    isinma_dk: int = 90
    seed: int = 42
    zaman_serisi: bool = False
    # Başlangıç stoku (K77): "DOLU" = N×C (v1 davranışı; uzun geçici rejim yaratır),
    # "ROP" = ROP seviyesi, "ORAN" = baslangic_oran × N×C
    baslangic_stok: str = "DOLU"
    baslangic_oran: float = 0.5


# ─────────────────────────────────────────────────────────────
# Veri hazırlığı (bir kez okunur, tüm koşularda paylaşılır)
# ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
# Koordinat tabanlı mesafe ağı (K100, K105)
# ─────────────────────────────────────────────────────────────
# Durak aralığı: Urru, Bonini & Echelmeyer (2018) s.406 — "5 stops ... equally distributed
# along the route. The route is 124 meters long" (5 durak + depo dönüşü = 6 eşit parça).
# Hat aralığı w = 2·s mühendislik varsayımıdır (kaynak yok).
KOORDINAT_DURAK_ARALIGI_M = 124.0 / 6
KOORDINAT_HAT_ARALIGI_KAT = 2.0


def koordinat_mesafe(st: pd.DataFrame, n_node: int, s: float = KOORDINAT_DURAK_ARALIGI_M,
                     w: Optional[float] = None) -> np.ndarray:
    """Depo (0,0); hatlar paralel, istasyonlar hat içinde s aralıklı; dikdörtgensel ölçü
    (Sevim & Görkemli Aykut 2026, Denk. 3). Düğüm 0 = depo, düğüm k = S_k.
    stations.csv'deki sira_no global numaralıdır; hat içi sıra ondan türetilir."""
    w = KOORDINAT_HAT_ARALIGI_KAT * s if w is None else w
    hatlar = sorted(st["hat"].unique())
    orta = (len(hatlar) - 1) / 2
    hat_ici = st.groupby("hat")["sira_no"].rank(method="first").astype(int)
    xy = np.zeros((n_node, 2))
    for (_, r), j in zip(st.iterrows(), hat_ici):
        k = int(str(r["istasyon_id"]).replace("S", ""))
        xy[k] = (s * j, w * (hatlar.index(r["hat"]) - orta))
    return (np.abs(xy[:, None, 0] - xy[None, :, 0]) +
            np.abs(xy[:, None, 1] - xy[None, :, 1]))


class V2Veri:
    def __init__(self, loader: Optional[DataLoader] = None):
        self.loader = loader or DataLoader()
        st = self.loader.get_stations()
        self.istasyon_id = list(st["istasyon_id"])
        self.n = len(self.istasyon_id)
        self.node = np.array([int(s.replace("S", "")) for s in self.istasyon_id])
        self.mu_saat = st["ort_tuketim_saat"].to_numpy(dtype=float)
        self.sigma_saat = st["std_tuketim_saat"].to_numpy(dtype=float)
        self.C = st["kutu_kapasitesi"].to_numpy(dtype=float)
        self.n_v1 = st["kanban_n"].to_numpy(dtype=int)

        veh = self.loader.get_vehicles().iloc[0]
        self.Q = int(veh["kapasite_kutu"])
        self.hiz_m_dk = float(veh["hiz_m_dk"])

        dist = self.loader.get_distances()
        n_node = int(max(dist["from_node"].max(), dist["to_node"].max())) + 1
        ham = np.zeros((n_node, n_node))
        for f, t, m in zip(dist["from_node"], dist["to_node"], dist["mesafe_m"]):
            ham[int(f), int(t)] = float(m)
        self.mesafe_ham = ham
        self.mesafe_metrik, self.metrik_duzeltilen_cift = self._floyd_warshall(ham)
        self.mesafe_koordinat = koordinat_mesafe(st, n_node)

        cons = self.loader.get_consumption()
        piv = cons.pivot(index="dakika", columns="istasyon_id", values="tuketim_adet")
        self.tuketim_csv = piv[self.istasyon_id].to_numpy(dtype=float)

    @staticmethod
    def _floyd_warshall(m):
        """K71: en kısa yol kapanışı. Döner: (metrik matris, düzeltilen yönlü çift sayısı)."""
        d = m.copy()
        for k in range(d.shape[0]):
            d = np.minimum(d, d[:, [k]] + d[[k], :])
        return d, int(np.sum(d < m - 1e-9))

    def talep_uret(self, p: V2Parametre) -> np.ndarray:
        """Dakikalık tüketim matrisi [sim_sure × n] (K70)."""
        T = p.sim_sure
        rng = np.random.default_rng(p.seed)
        mu_dk = self.mu_saat / 60.0
        if p.talep_modeli == "CSV":
            # v1 deterministik baz (seed=42). Not: σ/60 ölçeklemesiyle üretilmiştir.
            # T > 480 ise CSV vardiya olarak tekrarlanır (çok vardiyalı ufuk için).
            tekrar = math.ceil(T / self.tuketim_csv.shape[0])
            tuk = np.tile(self.tuketim_csv, (tekrar, 1))[:T].copy()
        elif p.talep_modeli == "NORMAL_DK_V1":
            # v1 stokastik modeli (dakikalık N(μ/60, σ/60)), ancak μ stations.csv'den (K75)
            tuk = np.maximum(0.0, rng.normal(mu_dk, self.sigma_saat / 60.0, size=(T, self.n)))
        elif p.talep_modeli == "SAATLIK_REJIM":
            # Saatlik tüketim ~ N(μ, σ_saat); saat içinde sabit hız → saatlik CV = onaylı 0.20
            saat_sayisi = math.ceil(T / 60)
            oran = np.maximum(0.0, rng.normal(self.mu_saat, self.sigma_saat, size=(saat_sayisi, self.n)))
            tuk = np.repeat(oran / 60.0, 60, axis=0)[:T]
        elif p.talep_modeli == "POISSON":
            # Birim geliş: dakikada Poisson(μ/60) (Alnahhal & Noche 2015 s.112; Sevim 2026 s.67 üstel)
            tuk = rng.poisson(mu_dk, size=(T, self.n)).astype(float)
        else:
            raise ValueError(f"Bilinmeyen talep modeli: {p.talep_modeli}")
        return tuk * p.talep_carpani


# ─────────────────────────────────────────────────────────────
# Kanban boyutlandırma (K65)
# ─────────────────────────────────────────────────────────────
def kanban_boyutlandir(veri: V2Veri, p: V2Parametre, d_saat: Optional[np.ndarray] = None):
    """
    Döner: (N [kart], ROP [adet]).
      P3 (çekme):  ROP = D·LT·(1+α)          (K25)
                   V1 : N = ⌈ROP/C⌉           (K06)
                   VDI: N = 1 + ⌈ROP/C⌉       (Urru vd. 2018 s.406; +1 değişim pozisyonu)
      P1/P2 (sabit takt T): VDI 5586 q = 1 + ⌈D·T·(1+α)/C⌉ (Urru s.406, Denk. 1–2;
                   Droste & Deuse 2011 s.607–608: gerekli stok çevrim süresiyle orantılı)
                   V1 : P3'ün V1 N değeri (v1 karşılaştırmalarındaki gibi aynı raf)
    """
    d_dk = (veri.mu_saat if d_saat is None else d_saat) / 60.0
    rop = d_dk * p.lt_dk * (1.0 + p.alpha)
    if p.n_ozel is not None:
        return np.asarray(p.n_ozel, dtype=int), rop
    if p.kanban_modu == "IKI_KUTU":
        # K93: Politikadan BAĞIMSIZ sabit tampon (iki kutulu Kanban).
        # Vojdani & Drechsler (2022) s.5: her iki sistem de aynı iki kutulu Kanban ile
        # karşılaştırılır ("Zwei-Behälter-Kanban", "identische Taktzeiten").
        # Bu, politika-tutarlı boyutlandırmanın UYGULANMADIĞI durumu temsil eder.
        return np.full(veri.n, 2, dtype=int), rop
    if p.politika == "P3":
        if p.kanban_modu == "V1":
            n = np.maximum(1, np.ceil(rop / veri.C - 1e-9)).astype(int)
        else:
            n = 1 + np.ceil(rop / veri.C - 1e-9).astype(int)
    else:
        if p.kanban_modu == "V1":
            n = np.maximum(1, np.ceil(rop / veri.C - 1e-9)).astype(int)
        else:
            n = 1 + np.ceil(d_dk * p.tur_araligi_dk * (1.0 + p.alpha) / veri.C - 1e-9).astype(int)
    return n, rop


# ─────────────────────────────────────────────────────────────
# Rota yardımcıları (K72)
# ─────────────────────────────────────────────────────────────
class _Rota:
    def __init__(self, sure_mat, p: V2Parametre):
        self.S = sure_mat
        self.p = p

    def zamanla(self, sira, t0, miktar, tw):
        """Sıra için varış zamanları, dönüş zamanı ve toplam gecikme."""
        p = self.p
        t = t0 + p.yukleme_dk
        konum = 0
        varis = []
        gecikme = 0.0
        for i, nd in enumerate(sira):
            t += self.S[konum, nd]
            varis.append(t)
            if tw is not None:
                gecikme += max(0.0, t - tw[i])
            t += p.durak_servis_dk + p.kutu_basi_servis_dk * miktar[i]
            konum = nd
        t += self.S[konum, 0]
        return varis, t, gecikme

    def en_yakin_komsu(self, dugumler):
        kalan = list(range(len(dugumler)))
        sira_idx = []
        konum = 0
        while kalan:
            j = min(kalan, key=lambda k: self.S[konum, dugumler[k]])
            sira_idx.append(j)
            konum = dugumler[j]
            kalan.remove(j)
        return sira_idx

    def maliyet(self, idx, dugumler, t0, miktar, tw):
        sira = [dugumler[i] for i in idx]
        _, donus, gec = self.zamanla(sira, t0, [miktar[i] for i in idx],
                                     None if tw is None else [tw[i] for i in idx])
        return (donus - t0) + self.p.gecikme_ceza * gec

    def iki_opt(self, idx, dugumler, t0, miktar, tw):
        """2-opt (Gendreau & Tarantilis 2010, Bölüm 1.1); maliyet = süre + ceza·gecikme (VRP-RTW)."""
        en_iyi = list(idx)
        en_iyi_m = self.maliyet(en_iyi, dugumler, t0, miktar, tw)
        iyilesti = True
        while iyilesti:
            iyilesti = False
            for i in range(len(en_iyi) - 1):
                for j in range(i + 1, len(en_iyi)):
                    aday = en_iyi[:i] + en_iyi[i:j + 1][::-1] + en_iyi[j + 1:]
                    m = self.maliyet(aday, dugumler, t0, miktar, tw)
                    if m < en_iyi_m - 1e-9:
                        en_iyi, en_iyi_m, iyilesti = aday, m, True
        return en_iyi

    def kur(self, dugumler, t0, miktar, tw):
        idx = self.en_yakin_komsu(dugumler)
        if self.p.iki_opt and len(idx) > 2:
            idx = self.iki_opt(idx, dugumler, t0, miktar, tw)
        return idx


# ─────────────────────────────────────────────────────────────
# Ana simülasyon
# ─────────────────────────────────────────────────────────────
def simule_et(p: V2Parametre, veri: Optional[V2Veri] = None) -> dict:
    veri = veri or V2Veri()
    n, T = veri.n, p.sim_sure
    C = veri.C
    tuk = veri.talep_uret(p)

    mesafe = {"METRIK": veri.mesafe_metrik, "KOORDINAT": veri.mesafe_koordinat}.get(
        p.mesafe_modu, veri.mesafe_ham)
    sure = mesafe / veri.hiz_m_dk * p.hiz_carpani
    rota = _Rota(sure, p)

    N, rop = kanban_boyutlandir(veri, p)
    cap = N * C
    if p.baslangic_stok == "ROP":            # K77
        stok = np.minimum(cap, rop).astype(float).copy()
    elif p.baslangic_stok == "ORAN":
        stok = (p.baslangic_oran * cap).astype(float).copy()
    else:
        stok = cap.astype(float).copy()       # "DOLU": v1 davranışı
    d_plan_dk = veri.mu_saat / 60.0          # tasarım tüketim hızı (TW hesabı)

    teslim = {}                              # dakika -> [(istasyon_idx, adet)]
    starv = np.zeros(n, dtype=int)
    starv_isinma_sonrasi = 0
    wip_seri, starv_seri = [], []

    turlar = []                              # tur kayıtları
    arac_musait = np.zeros(p.arac_sayisi)

    # P3 sipariş yapıları
    acik = np.zeros(n, dtype=bool)           # istasyonun açık siparişi var mı (K28)
    atanmis = np.zeros(n, dtype=bool)        # sipariş bir araca atandı mı
    sip = {}                                 # istasyon_idx -> sipariş sözlüğü
    siparis_kaydi = []
    n_degisim = 0

    def teslim_ekle(dk, i, adet):
        teslim.setdefault(dk, []).append((i, adet))

    # ── P1/P2: sabit takt takvimi (K50, K58, K73)
    if p.politika in ("P1", "P2"):
        gruplar = np.array_split(np.arange(n), p.arac_sayisi)
        kalkislar = list(range(p.tur_araligi_dk, T, p.tur_araligi_dk))
        planli = [(tk, v) for tk in kalkislar for v in range(p.arac_sayisi)]
        bekleyen_takvim = sorted(planli)
    else:
        gruplar, bekleyen_takvim = None, []

    for t in range(T):
        # 1) Teslimler (raf tavanı N×C — K57)
        for i, adet in teslim.pop(t, []):
            stok[i] = min(cap[i], stok[i] + adet)

        # 2) Tüketim ve starvation
        stok -= tuk[t]
        bos = stok <= 0
        if bos.any():
            starv += bos
            if t >= p.isinma_dk:
                starv_isinma_sonrasi += int(bos.sum())
            stok[bos] = 0.0
        if p.zaman_serisi:
            wip_seri.append(float(stok.sum()))
            starv_seri.append(int(bos.sum()))

        # K74: koşu içi dinamik N (yalnızca P3)
        if p.politika == "P3" and p.dinamik_n and t > 0 and t % p.dinamik_n_periyot_dk == 0:
            bas = max(0, t - p.dinamik_n_pencere_dk)
            d_tahmin_saat = tuk[bas:t].mean(axis=0) * 60.0
            N_yeni, rop_yeni = kanban_boyutlandir(veri, p, d_saat=d_tahmin_saat)
            n_degisim += int(np.sum(N_yeni != N))
            N, rop = N_yeni, rop_yeni
            cap = N * C
            d_plan_dk = d_tahmin_saat / 60.0

        if p.politika == "P3":
            # 3) Sinyal üretimi — kapalı döngü (K69): gerçek stok, gerçek teslimlerden sonra
            for i in range(n):
                if not acik[i] and stok[i] <= rop[i]:
                    d = max(d_plan_dk[i], 1e-9)
                    t_starv = t + stok[i] / d
                    tw_bitis = max(min(t_starv - p.tw_guvenlik_dk, t + p.tw_max_dk), t + p.lt_dk)  # K27, K30
                    if p.kanban_modu == "V1":
                        kutu = int(N[i])                                   # v1: istenen_kutu = N
                    else:
                        kutu = max(1, int(math.floor((cap[i] - rop[i]) / C[i] + 1e-9)))  # M = L − A (Sevim s.66)
                    sip[i] = {"i": i, "t_sinyal": t, "tw_bitis": tw_bitis, "kutu": kutu,
                              "kritik": t_starv - t < p.lt_dk}
                    acik[i] = True
                    atanmis[i] = False

            # 4) Sevk kararı
            for v in range(p.arac_sayisi):
                if arac_musait[v] > t:
                    continue
                bekleyen = [sip[i] for i in range(n) if acik[i] and not atanmis[i]]
                if not bekleyen:
                    break
                secim = _siparis_sec(bekleyen, t, p, veri, rota, stok, rop, d_plan_dk)
                if not secim:
                    continue
                dugum = [int(veri.node[s["i"]]) for s in secim]
                miktar = [s["kutu"] for s in secim]
                tw = [s["tw_bitis"] for s in secim]
                idx = rota.kur(dugum, t, miktar, tw)
                sira = [dugum[k] for k in idx]
                varis, donus, _ = rota.zamanla(sira, t, [miktar[k] for k in idx], [tw[k] for k in idx])

                if p.sevk == "KONSOLIDASYON" and sum(miktar) < veri.Q:
                    # K68: en geç kalkış — bir dakika daha beklemek herhangi bir teslimi
                    # son tarihinden (min(tw_bitis, canlı t_starv − güvenlik)) sonraya itiyorsa kalk
                    en_gec = math.inf
                    for k, a in zip(idx, varis):
                        s = secim[k]
                        i = s["i"]
                        t_starv_canli = t + stok[i] / max(d_plan_dk[i], 1e-9)
                        son = min(s["tw_bitis"], t_starv_canli - p.tw_guvenlik_dk)
                        en_gec = min(en_gec, t + (son - a))
                    if t + 1 <= en_gec:
                        break   # bu dakika kimse kalkmaz; sipariş birikmeye devam eder

                for k, a in zip(idx, varis):
                    s = secim[k]
                    atanmis[s["i"]] = True
                    s["varis"] = a
                    if a < T:
                        teslim_ekle(int(math.floor(a)), s["i"], s["kutu"] * C[s["i"]])
                arac_musait[v] = donus
                turlar.append(_tur_kaydi(t, donus, sira, [miktar[k] for k in idx], mesafe,
                                         [secim[k]["tw_bitis"] for k in idx], varis))

            # Teslim edilen siparişleri kapat (varış dakikası geçtiyse)
            for i in range(n):
                if acik[i] and atanmis[i] and sip[i]["varis"] <= t + 1:
                    s = sip[i]
                    siparis_kaydi.append({"i": i, "t_sinyal": s["t_sinyal"], "varis": s["varis"],
                                          "tw_bitis": s["tw_bitis"], "kutu": s["kutu"],
                                          "kritik": s["kritik"]})
                    acik[i] = False
                    atanmis[i] = False

        else:
            # P1/P2 sabit takt: aracı meşgulse bir sonraki boş dakikada kalkar
            yeni = []
            for tk, v in bekleyen_takvim:
                if tk <= t and arac_musait[v] <= t:
                    grup = gruplar[v]
                    miktar_all = []
                    yuk = 0
                    for i in grup:
                        if p.politika == "P1":
                            q = 1                                          # K50: her istasyona 1 kutu
                        else:
                            q = int(math.floor((cap[i] - stok[i]) / C[i] + 1e-9))  # 1:1 boş kutu değişimi
                        q = max(0, min(q, veri.Q - yuk))
                        yuk += q
                        miktar_all.append(q)
                    # Sabit rota: tüm grup sırayla gezilir, yalnızca teslim olan duraklarda durulur
                    tt = t + p.yukleme_dk
                    konum = 0
                    varis_l, sira_l, mik_l = [], [], []
                    for i, q in zip(grup, miktar_all):
                        nd = int(veri.node[i])
                        tt += sure[konum, nd]
                        konum = nd
                        if q > 0:
                            varis_l.append(tt)
                            sira_l.append(nd)
                            mik_l.append(q)
                            if tt < T:
                                teslim_ekle(int(math.floor(tt)), i, q * C[i])
                            tt += p.durak_servis_dk + p.kutu_basi_servis_dk * q
                    tt += sure[konum, 0]
                    arac_musait[v] = tt
                    tam_rota = [int(veri.node[i]) for i in grup]
                    turlar.append(_tur_kaydi(t, tt, tam_rota, mik_l, mesafe, None, varis_l,
                                             durak_sayisi=len(sira_l)))
                else:
                    yeni.append((tk, v))
            bekleyen_takvim = yeni

    return _ozet(p, veri, starv, starv_isinma_sonrasi, turlar, siparis_kaydi, sip, acik,
                 N, cap, n_degisim, wip_seri, starv_seri, tuk)


def _siparis_sec(bekleyen, t, p, veri, rota, stok, rop, d_plan_dk):
    """Dispatch kuralına göre sırala; kapasite, durak sınırı ve tur süresi (K72) ile seç."""
    if p.dispatch_kural == "EDD":
        bekleyen.sort(key=lambda s: (s["tw_bitis"], s["t_sinyal"]))
    elif p.dispatch_kural == "SLACK":
        bekleyen.sort(key=lambda s: (s["tw_bitis"] - (t + p.yukleme_dk + rota.S[0, int(veri.node[s["i"]])]
                                                        + p.durak_servis_dk), s["tw_bitis"]))
    elif p.dispatch_kural == "FIFO":
        bekleyen.sort(key=lambda s: (s["t_sinyal"], s["tw_bitis"]))
    else:  # KRITIKLIK (K26): canlı stok/ROP
        bekleyen.sort(key=lambda s: (stok[s["i"]] / max(rop[s["i"]], 1e-9), s["tw_bitis"]))

    secim, yuk = [], 0
    for s in bekleyen:
        if yuk + s["kutu"] > veri.Q:
            continue
        if p.max_durak is not None and len(secim) >= p.max_durak:
            break
        aday = secim + [s]
        if p.max_tur_dk is not None and len(aday) > 1:
            dug = [int(veri.node[x["i"]]) for x in aday]
            idx = rota.en_yakin_komsu(dug)
            _, donus, _ = rota.zamanla([dug[k] for k in idx], t, [aday[k]["kutu"] for k in idx], None)
            if donus - t > p.max_tur_dk:
                continue
        secim, yuk = aday, yuk + s["kutu"]
    return secim


def _tur_kaydi(t0, donus, sira, miktar, mesafe, tw, varis, durak_sayisi=None):
    m, konum = 0.0, 0
    for nd in sira:
        m += mesafe[konum, nd]
        konum = nd
    m += mesafe[konum, 0]
    gec = 0
    if tw is not None:
        gec = sum(1 for a, b in zip(varis, tw) if a > b)
    return {"kalkis": t0, "donus": donus, "sure": donus - t0, "mesafe_m": m,
            "kutu": int(sum(miktar)), "durak": len(sira) if durak_sayisi is None else durak_sayisi,
            "gecikmeli_durak": gec}


def _ozet(p, veri, starv, starv_is, turlar, siparis_kaydi, sip, acik, N, cap, n_degisim,
          wip_seri, starv_seri, tuk):
    n, T = veri.n, p.sim_sure
    toplam_starv = int(starv.sum())
    tur_df = pd.DataFrame(turlar)
    tur_sayisi = len(tur_df)
    toplam_kutu = int(tur_df["kutu"].sum()) if tur_sayisi else 0
    sonuc = {
        "politika": p.politika, "sevk": p.sevk if p.politika == "P3" else "TAKVIM",
        "dispatch_kural": p.dispatch_kural if p.politika == "P3" else "-",
        "arac_sayisi": p.arac_sayisi, "tur_araligi_dk": p.tur_araligi_dk if p.politika != "P3" else None,
        "alpha": p.alpha, "kanban_modu": p.kanban_modu, "seed": p.seed, "talep_modeli": p.talep_modeli,
        "starv_dk": toplam_starv,
        "starv_pct": 100.0 * toplam_starv / (T * n),
        "starv_pct_isinma_sonrasi": 100.0 * starv_is / ((T - p.isinma_dk) * n),
        "ort_wip": float(np.mean(wip_seri)) if wip_seri else None,
        # K99: ısınma dönemi hariç WIP (tez tablolarında kullanılır)
        "ort_wip_isinma_sonrasi": float(np.mean(wip_seri[p.isinma_dk:])) if len(wip_seri) > p.isinma_dk else None,
        "toplam_mesafe_km": float(tur_df["mesafe_m"].sum() / 1000.0) if tur_sayisi else 0.0,
        "tur_sayisi": tur_sayisi,
        "ort_kutu_tur": toplam_kutu / tur_sayisi if tur_sayisi else 0.0,
        "doluluk_pct": 100.0 * toplam_kutu / (veri.Q * tur_sayisi) if tur_sayisi else 0.0,
        "ort_durak_tur": float(tur_df["durak"].mean()) if tur_sayisi else 0.0,
        "ort_tur_sure_dk": float(tur_df["sure"].mean()) if tur_sayisi else 0.0,
        "max_tur_sure_dk": float(tur_df["sure"].max()) if tur_sayisi else 0.0,
        "arac_kullanim_pct": 100.0 * float(np.minimum(tur_df["donus"], T).sub(tur_df["kalkis"]).clip(lower=0).sum())
                             / (p.arac_sayisi * T) if tur_sayisi else 0.0,
        "toplam_kart": int(N.sum()), "toplam_raf_adet": float(cap.sum()),
        "talep_adet": float(tuk.sum()),
        "dod": 1.0 if p.politika == "P3" else 0.0,   # Larsen vd. 2008: tüm istekler anlık
        "n_degisim": n_degisim,
    }
    if p.politika == "P3":
        sk = pd.DataFrame(siparis_kaydi)
        acik_kalan = int(acik.sum())
        sonuc["_siparisler"] = siparis_kaydi    # K101: OR-Tools çevrimdışı referansı için
        sonuc.update({
            "siparis": len(sk) + acik_kalan,
            "teslim_edilen": len(sk),
            "zamaninda": int((sk["varis"] <= sk["tw_bitis"]).sum()) if len(sk) else 0,
            "gecikmeli": int((sk["varis"] > sk["tw_bitis"]).sum()) if len(sk) else 0,
            "acik_kalan": acik_kalan,
            "ort_ikmal_sure_dk": float((sk["varis"] - sk["t_sinyal"]).mean()) if len(sk) else None,
            "ort_gecikme_dk": float((sk["varis"] - sk["tw_bitis"]).clip(lower=0).mean()) if len(sk) else None,
        })
    # ort_wip zaman serisi tutulmadıysa ayrıca hesaplanmadı; aşağıdaki sarmalayıcı her zaman tutar
    sonuc["_starv_istasyon"] = {veri.istasyon_id[i]: int(starv[i]) for i in range(n)}
    if p.zaman_serisi:
        sonuc["_wip_seri"] = wip_seri
        sonuc["_starv_seri"] = starv_seri
    return sonuc


def calistir(p: V2Parametre, veri: Optional[V2Veri] = None) -> dict:
    """WIP her zaman hesaplanır; zaman serileri yalnızca istenirse döner."""
    istendi = p.zaman_serisi
    s = simule_et(replace(p, zaman_serisi=True), veri)
    if not istendi:
        s.pop("_wip_seri", None)
        s.pop("_starv_seri", None)
        s.pop("_siparisler", None)
    return s


def main():
    veri = V2Veri()
    print("=" * 72)
    print("v2 KANONİK MOTOR — HIZLI KONTROL (seed=1001, saatlik rejim talebi)")
    print(f"  Metrik kapanış: {veri.metrik_duzeltilen_cift} yönlü düğüm çifti kısaltıldı (K71)")
    print("=" * 72)
    for pol, sevk, T in [("P1", "-", 60), ("P2", "-", 60), ("P3", "ANINDA", None), ("P3", "KONSOLIDASYON", None)]:
        for m in (2, 4):
            prm = V2Parametre(politika=pol, sevk=sevk if pol == "P3" else "KONSOLIDASYON",
                              arac_sayisi=m, tur_araligi_dk=T or 60, seed=1001)
            s = calistir(prm, veri)
            print(f"  {pol:2s} {sevk:13s} m={m}  starv=%{s['starv_pct']:6.2f}  WIP={s['ort_wip']:6.1f}  "
                  f"mesafe={s['toplam_mesafe_km']:6.2f} km  tur={s['tur_sayisi']:3d}  "
                  f"doluluk=%{s['doluluk_pct']:5.1f}  maxTur={s['max_tur_sure_dk']:5.1f} dk")


if __name__ == "__main__":
    main()
