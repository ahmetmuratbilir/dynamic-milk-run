/**
 * app.js - Dinamik Milk-Run & E-Kanban Karar Destek Dashboard Mantığı
 * ==================================================================
 * 1.920 Senaryoluk Çevrimdışı Veri Ambarını (data/dashboard_scenarios.json) Okur
 * 5 Sekmeli Mimari:
 *   Sekme 1: Özet Ekranı (4 KPI, dinamik yorum, filo duyarlılık eğrisi)
 *   Sekme 2: What-If Simülatör (Slider kontrolleri, anlık KPI'lar, Pareto, K55 Alpha)
 *   Sekme 3: İstasyon Haritası (6x4 Kompakt Kart Izgarası, mini progress bar, ROP işareti)
 *   Sekme 4: Statik vs Dinamik Karşılaştırma (Detaylı metrik tablosu & 1-8 araç matrisi)
 *   Sekme 5: Veri Girişi & Gerçek Veri (Form, canlı ROP önizleme, localStorage & CSV dışa aktarma)
 */

// ===== GLOBAL DEĞİŞKENLER VE GRAFİK NESNELERİ =====
let scenariosData = [];
window.chartInstances = {
    fleet: null,
    pareto: null,
    alpha: null
};

// Gerçek StaticMilkRunSimulator (tur_sikligi_dk = 80 dk Kanonik K58) Çıktıları
const STATIC_BASELINE_MAP = {
    1: 25.77,
    2: 21.35,
    3: 19.70,
    4: 19.31,
    5: 19.10,
    6: 18.96,
    7: 18.83,
    8: 18.68
};

// Sentetik Baz İstasyon Verileri (stations.csv)
const BASE_STATIONS_DATA = [
    { id: 'S1', hat: 'Hat-1', d_saat: 22, std_saat: 5.5, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S2', hat: 'Hat-1', d_saat: 18, std_saat: 4.5, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S3', hat: 'Hat-1', d_saat: 15, std_saat: 3.8, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S4', hat: 'Hat-1', d_saat: 20, std_saat: 5.0, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S5', hat: 'Hat-1', d_saat: 12, std_saat: 3.0, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S6', hat: 'Hat-1', d_saat: 17, std_saat: 4.2, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S7', hat: 'Hat-2', d_saat: 21, std_saat: 5.2, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S8', hat: 'Hat-2', d_saat: 13, std_saat: 3.2, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S9', hat: 'Hat-2', d_saat: 19, std_saat: 4.8, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S10', hat: 'Hat-2', d_saat: 11, std_saat: 2.8, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S11', hat: 'Hat-2', d_saat: 16, std_saat: 4.0, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S12', hat: 'Hat-2', d_saat: 14, std_saat: 3.5, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S13', hat: 'Hat-3', d_saat: 23, std_saat: 5.8, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S14', hat: 'Hat-3', d_saat: 18, std_saat: 4.5, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S15', hat: 'Hat-3', d_saat: 15, std_saat: 3.8, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S16', hat: 'Hat-3', d_saat: 24, std_saat: 6.0, c: 20, n: 2, baslangic_kutu: 2, fragile: true },
    { id: 'S17', hat: 'Hat-3', d_saat: 17, std_saat: 4.2, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S18', hat: 'Hat-3', d_saat: 14, std_saat: 3.5, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S19', hat: 'Hat-4', d_saat: 20, std_saat: 5.0, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S20', hat: 'Hat-4', d_saat: 16, std_saat: 4.0, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S21', hat: 'Hat-4', d_saat: 13, std_saat: 3.2, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S22', hat: 'Hat-4', d_saat: 18, std_saat: 4.5, c: 20, n: 1, baslangic_kutu: 1 },
    { id: 'S23', hat: 'Hat-4', d_saat: 12, std_saat: 3.0, c: 15, n: 1, baslangic_kutu: 1 },
    { id: 'S24', hat: 'Hat-4', d_saat: 21, std_saat: 5.2, c: 20, n: 1, baslangic_kutu: 1 }
];

// Aktif İstasyon Veri Listesi (Düzenlenebilir)
let activeStationsData = JSON.parse(JSON.stringify(BASE_STATIONS_DATA));
let isPreviewMode = false;

// ===== HAZIR TEST EDİLMİŞ SEKME GEÇİŞ MEKANİZMASI =====
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => {
        el.style.display = 'none';
    });
    document.querySelectorAll('.tab-button').forEach(el => {
        el.classList.remove('active');
    });
    const target = document.getElementById(tabId);
    if (target) target.style.display = 'block';
    const btn = document.querySelector('[data-tab="' + tabId + '"]');
    if (btn) btn.classList.add('active');

    if (tabId === 'tab-istasyon') {
        updateStations();
    }

    Object.values(window.chartInstances || {}).forEach(chart => {
        if (chart && typeof chart.resize === 'function') chart.resize();
    });
}

// ===== localStorage YARDIMCI FONKSİYONLARI =====
const STORAGE_KEY = 'dashboard_gercek_veri_v1';

function saveRealDataToStorage(data) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        return true;
    } catch (e) {
        console.error('Kaydetme hatasi:', e);
        return false;
    }
}

function loadRealDataFromStorage() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch (e) {
        console.error('Yukleme hatasi:', e);
        return null;
    }
}

function clearRealDataStorage() {
    localStorage.removeItem(STORAGE_KEY);
}

// ===== CSV DIŞA AKTARMA (GENEL AMAÇLI) =====
function exportArrayToCSV(rows, headers, filename) {
    const headerLine = headers.join(',');
    const dataLines = rows.map(row =>
        headers.map(h => {
            const val = row[h] !== undefined ? row[h] : '';
            const s = String(val);
            return s.includes(',') ? '"' + s + '"' : s;
        }).join(',')
    );
    const csvContent = [headerLine, ...dataLines].join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ===== UYGULAMA BAŞLATMA =====
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data/dashboard_scenarios.json');
        scenariosData = await response.json();
        console.log('Veri ambarı yüklendi: ' + scenariosData.length + ' senaryo.');
        
        // localStorage'dan kayıtlı veri varsa yükle
        const savedData = loadRealDataFromStorage();
        if (savedData && Array.isArray(savedData) && savedData.length === 24) {
            activeStationsData = savedData;
        }

        initAllCharts();
        initWhatIfListeners();
        renderStations();
        renderDataEntryTable();
        initSampleStationSelect();
        initDefaultSampleRows();
        updateOzetView();
        updateWhatIfView();
    } catch (err) {
        console.error('Veri yükleme hatası:', err);
    }
});

// ===== GRAFİK BAŞLATMA (ÖZET + WHAT-IF) =====
function initAllCharts() {
    const chartConfigCommon = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#94a3b8', font: { family: 'Outfit' } } }
        },
        scales: {
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
        }
    };

    // 1. Filo Duyarlılık Eğrisi (Sekme 1)
    const canvasFleet = document.getElementById('chartFleet');
    if (canvasFleet) {
        const ctxFleet = canvasFleet.getContext('2d');
        window.chartInstances.fleet = new Chart(ctxFleet, {
            type: 'line',
            data: {
                labels: ['1 Araç', '2 Araç', '3 Araç', '4 Araç (Baz)', '5 Araç', '6 Araç', '7 Araç', '8 Araç'],
                datasets: [
                    {
                        label: 'Tavanlı Dinamik Sistem (Starvation %)',
                        data: [],
                        borderColor: '#06b6d4',
                        backgroundColor: 'rgba(6, 182, 212, 0.15)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 3,
                        pointBackgroundColor: '#06b6d4',
                        pointRadius: 4
                    },
                    {
                        label: 'Statik Milk-Run Baseline (%19.31 @ 4 Araç)',
                        data: [25.77, 21.35, 19.70, 19.31, 19.10, 18.96, 18.83, 18.68],
                        borderColor: '#f59e0b',
                        borderDash: [4, 4],
                        borderWidth: 2,
                        pointRadius: 0
                    },
                    {
                        label: 'Rekabetçilik Eşiği (<%5)',
                        data: [5, 5, 5, 5, 5, 5, 5, 5],
                        borderColor: '#10b981',
                        borderDash: [6, 6],
                        borderWidth: 2,
                        pointRadius: 0
                    }
                ]
            },
            options: chartConfigCommon
        });
    }

    // 2. Pareto Scatter (Sekme 2)
    const canvasPareto = document.getElementById('chartPareto');
    if (canvasPareto) {
        const ctxPareto = canvasPareto.getContext('2d');
        const bgScatterData = [];
        if (scenariosData && scenariosData.length > 0) {
            for (let i = 0; i < scenariosData.length; i += 4) {
                bgScatterData.push({ x: scenariosData[i].ort_wip, y: scenariosData[i].starv_pct });
            }
        }

        window.chartInstances.pareto = new Chart(ctxPareto, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Tüm 1.920 Senaryo Noktası',
                        data: bgScatterData,
                        backgroundColor: 'rgba(148, 163, 184, 0.25)',
                        pointRadius: 3
                    },
                    {
                        label: 'Seçili Senaryo',
                        data: [],
                        backgroundColor: '#f43f5e',
                        pointRadius: 9,
                        pointHoverRadius: 12
                    }
                ]
            },
            options: {
                ...chartConfigCommon,
                scales: {
                    x: { title: { display: true, text: 'Ortalama WIP Stok (adet)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    y: { title: { display: true, text: 'Starvation (%)', color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
                }
            }
        });
    }

    // 3. Alpha Mod A vs Mod B Bar (Sekme 2)
    const canvasAlpha = document.getElementById('chartAlpha');
    if (canvasAlpha) {
        const ctxAlpha = canvasAlpha.getContext('2d');
        window.chartInstances.alpha = new Chart(ctxAlpha, {
            type: 'bar',
            data: {
                labels: ['alpha=0.05', 'alpha=0.10', 'alpha=0.15', 'alpha=0.20', 'alpha=0.25', 'alpha=0.30'],
                datasets: [
                    {
                        label: 'Dinamik N (Mod B - 3.4 Kat Güçlü Etki)',
                        data: [],
                        backgroundColor: '#10b981'
                    },
                    {
                        label: 'Sabit N (Mod A - Zayıf Etki)',
                        data: [],
                        backgroundColor: '#3b82f6'
                    }
                ]
            },
            options: chartConfigCommon
        });
    }
}

// ===== WHAT-IF EVENT LISTENERS =====
function initWhatIfListeners() {
    const sliderArac = document.getElementById('sliderArac');
    const valArac = document.getElementById('valArac');
    const sliderAlpha = document.getElementById('sliderAlpha');
    const valAlpha = document.getElementById('valAlpha');
    const sliderTalep = document.getElementById('sliderTalep');
    const valTalep = document.getElementById('valTalep');

    if (sliderArac && valArac) {
        sliderArac.addEventListener('input', (e) => {
            valArac.textContent = e.target.value + ' Araç';
            updateWhatIfView();
        });
    }

    if (sliderAlpha && valAlpha) {
        sliderAlpha.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            valAlpha.textContent = val.toFixed(2) + ' (%' + Math.round(val * 100) + ')';
            updateWhatIfView();
        });
    }

    if (sliderTalep && valTalep) {
        sliderTalep.addEventListener('input', (e) => {
            const val = parseInt(e.target.value);
            valTalep.textContent = (val === 0 ? '%0 (Baz)' : (val > 0 ? '+' : '') + val + '%');
            updateWhatIfView();
        });
    }

    document.querySelectorAll('input[name="nModu"]').forEach(el => {
        el.addEventListener('change', updateWhatIfView);
    });

    document.querySelectorAll('input[name="dispatch"]').forEach(el => {
        el.addEventListener('change', updateWhatIfView);
    });
}

// ===== WHAT-IF SEÇİLİ PARAMETRELERİ AL =====
function getWhatIfParameters() {
    const sliderArac = document.getElementById('sliderArac');
    const sliderAlpha = document.getElementById('sliderAlpha');
    const sliderTalep = document.getElementById('sliderTalep');
    const checkedRadio = document.querySelector('input[name="nModu"]:checked');
    const checkedDisp = document.querySelector('input[name="dispatch"]:checked');

    return {
        arac_sayisi: sliderArac ? parseInt(sliderArac.value) : 4,
        alpha: sliderAlpha ? parseFloat(sliderAlpha.value) : 0.15,
        talep_sok_pct: sliderTalep ? parseInt(sliderTalep.value) : 0,
        dispatch_kural: checkedDisp ? checkedDisp.value : 'EDD',
        n_modu: checkedRadio ? checkedRadio.value : 'Dinamik_N'
    };
}

// ===== SEKME 1 (ÖZET) GÖRÜNÜMÜNÜ GÜNCELLEME =====
function updateOzetView() {
    if (!scenariosData || scenariosData.length === 0) return;

    // Baz Senaryo: Araç=4, alpha=0.15, talep=0, EDD, Dinamik_N
    const bazScenario = scenariosData.find(s => 
        s.arac_sayisi === 4 &&
        Math.abs(s.alpha - 0.15) < 0.01 &&
        s.talep_sok_pct === 0 &&
        s.dispatch_kural === 'EDD' &&
        s.n_modu === 'Dinamik_N'
    ) || scenariosData[0];

    if (!bazScenario) return;

    const starvPct = bazScenario.starv_pct;
    const ortWip = bazScenario.ort_wip;
    const starvDk = bazScenario.starv_dk;

    // KPI 1: Starvation
    const elStarv = document.getElementById('kpiStarvVal');
    const elStarvDk = document.getElementById('kpiStarvDk');
    const dotStarv = document.getElementById('dotStarv');
    if (elStarv) elStarv.textContent = '%' + starvPct.toFixed(2);
    if (elStarvDk) elStarvDk.textContent = starvDk.toLocaleString() + ' / 11,520 dakika duruş';

    if (dotStarv) {
        dotStarv.className = 'kpi-status-dot ' + (starvPct < 10 ? 'dot-green' : (starvPct <= 25 ? 'dot-yellow' : 'dot-red'));
    }

    // KPI 2: WIP
    const elWip = document.getElementById('kpiWipVal');
    const dotWip = document.getElementById('dotWip');
    if (elWip) elWip.textContent = ortWip.toFixed(1);
    if (dotWip) {
        dotWip.className = 'kpi-status-dot ' + (ortWip <= 200 ? 'dot-green' : (ortWip <= 250 ? 'dot-yellow' : 'dot-red'));
    }

    // KPI 3: Statik vs Dinamik Farkı (4 Araç İçin Doğru Statik Baseline: %19.31)
    const staticBase = STATIC_BASELINE_MAP[4] || 19.31;
    const diffPuan = (starvPct - staticBase).toFixed(2);
    const elFark = document.getElementById('kpiFarkVal');
    const dotFark = document.getElementById('dotFark');
    if (elFark) elFark.textContent = (diffPuan >= 0 ? '+' : '') + diffPuan + ' puan';
    if (dotFark) {
        dotFark.className = 'kpi-status-dot ' + (diffPuan <= 0 ? 'dot-green' : (diffPuan <= 5 ? 'dot-yellow' : 'dot-red'));
    }

    // KPI 4: Doluluk
    const elDoluluk = document.getElementById('kpiDolulukVal');
    const dotDoluluk = document.getElementById('dotDoluluk');
    const dolulukEst = Math.min(98.5, Math.max(35.0, (100 - starvPct * 0.8))).toFixed(1);
    if (elDoluluk) elDoluluk.textContent = '%' + dolulukEst;
    if (dotDoluluk) {
        dotDoluluk.className = 'kpi-status-dot ' + (dolulukEst >= 60 && dolulukEst <= 90 ? 'dot-green' : 'dot-yellow');
    }

    // Otomatik Dinamik Yorum Metni
    const commentEl = document.getElementById('dynamicCommentText');
    if (commentEl) {
        commentEl.innerHTML = 
            'Mevcut baz senaryoda (4 Araç, &alpha;=0.15, EDD) sistem <strong>%' + starvPct.toFixed(2) + '</strong> duruş oranıyla çalışmaktadır — ' +
            'bu, statik sistemin (%' + staticBase.toFixed(2) + ') <strong>+' + diffPuan + ' puan</strong> üzerindedir (30 replikasyon stokastik ortalamasında fark: +3.06 puandır). ' +
            'Sistemin <%5.0 rekabetçilik eşiğine ulaşması için filo büyüklüğünün <strong>8 araca</strong> çıkarılması gerekmektedir.';
    }

    // Filo Duyarlılık Eğrisini Çiz (1-8 Araç)
    if (window.chartInstances.fleet) {
        const fleetData = [];
        for (let v = 1; v <= 8; v++) {
            const item = scenariosData.find(s => 
                s.arac_sayisi === v &&
                Math.abs(s.alpha - 0.15) < 0.01 &&
                s.talep_sok_pct === 0 &&
                s.dispatch_kural === 'EDD' &&
                s.n_modu === 'Dinamik_N'
            );
            fleetData.push(item ? item.starv_pct : null);
        }
        window.chartInstances.fleet.data.datasets[0].data = fleetData;
        window.chartInstances.fleet.update();
    }
}

// ===== SEKME 2 (WHAT-IF) GÖRÜNÜMÜNÜ GÜNCELLEME =====
function updateWhatIfView() {
    if (!scenariosData || scenariosData.length === 0) return;

    const params = getWhatIfParameters();

    // Seçili senaryoyu filtrele
    const curScenario = scenariosData.find(s => 
        s.arac_sayisi === params.arac_sayisi &&
        Math.abs(s.alpha - params.alpha) < 0.01 &&
        s.talep_sok_pct === params.talep_sok_pct &&
        s.dispatch_kural === params.dispatch_kural &&
        s.n_modu === params.n_modu
    ) || scenariosData[0];

    if (!curScenario) return;

    const starvPct = curScenario.starv_pct;
    const ortWip = curScenario.ort_wip;
    const starvDk = curScenario.starv_dk;

    // What-If KPI 1: Starvation
    const wiStarvVal = document.getElementById('wiStarvVal');
    const wiStarvDk = document.getElementById('wiStarvDk');
    const wiTargetBadge = document.getElementById('wiTargetBadge');
    if (wiStarvVal) wiStarvVal.textContent = '%' + starvPct.toFixed(2);
    if (wiStarvDk) wiStarvDk.textContent = starvDk.toLocaleString() + ' / 11,520 dk';

    if (wiTargetBadge) {
        if (starvPct < 5.0) {
            wiTargetBadge.textContent = 'Eşik: <%5 (HEDEF ULAŞILDI ✅)';
            wiTargetBadge.style.background = 'rgba(16, 185, 129, 0.2)';
            wiTargetBadge.style.color = '#6ee7b7';
            wiTargetBadge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
        } else {
            wiTargetBadge.textContent = 'Eşik: <%5 (YETERSİZ 🚨)';
            wiTargetBadge.style.background = 'rgba(244, 63, 94, 0.2)';
            wiTargetBadge.style.color = '#fecdd3';
            wiTargetBadge.style.borderColor = 'rgba(244, 63, 94, 0.4)';
        }
    }

    // What-If KPI 2: WIP
    const wiWipVal = document.getElementById('wiWipVal');
    if (wiWipVal) wiWipVal.textContent = ortWip.toFixed(1);

    // What-If KPI 3: Statik vs Dinamik Farkı (DOĞRU STATIC_BASELINE_MAP KULLANIMI)
    const staticBase = STATIC_BASELINE_MAP[params.arac_sayisi] || 19.31;
    const diffPuan = (starvPct - staticBase).toFixed(2);
    const wiFarkVal = document.getElementById('wiFarkVal');
    const wiFarkSub = document.getElementById('wiFarkSub');
    const wiFarkNote = document.getElementById('wiFarkNote');

    if (wiFarkVal) {
        wiFarkVal.textContent = (diffPuan >= 0 ? '+' : '') + diffPuan + ' puan';
        wiFarkVal.style.color = diffPuan <= 0 ? '#10b981' : (diffPuan <= 5 ? '#f59e0b' : '#f43f5e');
    }
    if (wiFarkSub) {
        wiFarkSub.textContent = params.arac_sayisi + ' araç için statik referans: %' + staticBase.toFixed(2);
    }
    if (wiFarkNote) {
        wiFarkNote.textContent = diffPuan <= 0 ? 'Dinamik sistem daha başarılı' : 'Statik sistem avantajlı';
    }

    // What-If KPI 4: Doluluk
    const wiDolulukVal = document.getElementById('wiDolulukVal');
    if (wiDolulukVal) {
        const dolulukEst = Math.min(98.5, Math.max(35.0, (100 - starvPct * 0.8))).toFixed(1);
        wiDolulukVal.textContent = '%' + dolulukEst;
    }

    // Pareto Scatter Güncelleme (Kırmızı Seçili Nokta)
    if (window.chartInstances.pareto) {
        window.chartInstances.pareto.data.datasets[1].data = [{ x: ortWip, y: starvPct }];
        window.chartInstances.pareto.update();
    }

    // K55 Alpha Duyarlılığı Güncelleme (Seçili Araç Sayısı ve Parametreler İçin)
    if (window.chartInstances.alpha) {
        const alphaDinamik = [];
        const alphaSabit = [];
        const alphas = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30];

        alphas.forEach(a => {
            const itemD = scenariosData.find(s => 
                s.arac_sayisi === params.arac_sayisi &&
                Math.abs(s.alpha - a) < 0.01 &&
                s.talep_sok_pct === params.talep_sok_pct &&
                s.dispatch_kural === params.dispatch_kural &&
                s.n_modu === 'Dinamik_N'
            );
            const itemS = scenariosData.find(s => 
                s.arac_sayisi === params.arac_sayisi &&
                Math.abs(s.alpha - a) < 0.01 &&
                s.talep_sok_pct === params.talep_sok_pct &&
                s.dispatch_kural === params.dispatch_kural &&
                s.n_modu === 'Sabit_N'
            );

            alphaDinamik.push(itemD ? itemD.starv_pct : 0);
            alphaSabit.push(itemS ? itemS.starv_pct : 0);
        });

        window.chartInstances.alpha.data.datasets[0].data = alphaDinamik;
        window.chartInstances.alpha.data.datasets[1].data = alphaSabit;
        window.chartInstances.alpha.update();
    }

    // İstasyon haritasını da güncel parametrelerle güncelle
    updateStations(params);
}

// ===== SEKME 3 (İSTASYON HARİTASI) 6x4 KART IZGARASI RENDER =====
function renderStations() {
    const grid = document.getElementById('stationsGrid');
    if (!grid) return;
    grid.innerHTML = '';

    activeStationsData.forEach(st => {
        const sid = st.id;
        const isFragile = !!st.fragile;
        
        const card = document.createElement('div');
        card.className = 'station-card' + (isFragile ? ' card-fragile' : '');
        card.id = 'st-card-' + sid;
        card.title = sid + ' (' + st.hat + '): Tüketim=' + st.d_saat + ' kutu/saat, Kutu Kapasitesi C=' + st.c + ', Başlangıç N=' + st.n;
        
        card.innerHTML = 
            '<div class="station-card-header">' +
                '<span class="station-card-title">' + sid + 
                    (isFragile ? ' <span class="fragile-badge-icon" title="En Kırılgan İstasyon">⚠️</span>' : '') + 
                '</span>' +
                '<span class="station-card-hat">' + st.hat + '</span>' +
            '</div>' +
            '<div class="station-mini-bar-wrapper">' +
                '<div class="station-mini-bar-fill fill-green" id="st-bar-' + sid + '" style="width: 70%;"></div>' +
                '<div class="station-rop-marker" id="st-rop-mark-' + sid + '" style="left: 45%;" title="ROP Eşiği"></div>' +
            '</div>' +
            '<div class="station-card-metrics">' +
                '<span id="st-val-' + sid + '" style="font-weight:600; color:#e2e8f0;">Stok: ' + (st.n * st.c) + '</span>' +
                '<span id="st-rop-' + sid + '" style="color:#fde047;">ROP: ' + Math.ceil((st.d_saat/60)*45*1.15) + '</span>' +
            '</div>';
        
        grid.appendChild(card);
    });
}

function updateStations(params) {
    if (!params) params = getWhatIfParameters();
    const LT_dk = 45.0;
    const talepCarpan = 1.0 + (params.talep_sok_pct / 100.0);

    activeStationsData.forEach(st => {
        const sid = st.id;
        const card = document.getElementById('st-card-' + sid);
        const bar = document.getElementById('st-bar-' + sid);
        const ropMark = document.getElementById('st-rop-mark-' + sid);
        const valTxt = document.getElementById('st-val-' + sid);
        const ropTxt = document.getElementById('st-rop-' + sid);

        const d_dk = (st.d_saat / 60.0) * talepCarpan;
        const ropAdet = Math.ceil(d_dk * LT_dk * (1.0 + params.alpha));
        
        let nKart = st.n;
        if (params.n_modu === 'Dinamik_N') {
            nKart = Math.max(1, Math.ceil(ropAdet / st.c));
        }
        const cap = nKart * st.c;

        // Anlık simüle edilen stok seviyesi
        let currentStok = st.fragile ? Math.round(ropAdet * 0.75) : Math.round(cap * 0.85);
        if (params.arac_sayisi < 3) currentStok = Math.max(0, currentStok - Math.round(st.c * 0.4));
        if (params.talep_sok_pct > 0) currentStok = Math.max(0, currentStok - Math.round(st.c * 0.2));

        const pct = Math.min(100, Math.max(0, (currentStok / cap) * 100));
        const ropPct = Math.min(100, Math.max(0, (ropAdet / cap) * 100));

        if (bar) {
            bar.style.width = pct + '%';
            if (currentStok <= 0) {
                bar.className = 'station-mini-bar-fill fill-red';
            } else if (currentStok <= ropAdet) {
                bar.className = 'station-mini-bar-fill fill-yellow';
            } else {
                bar.className = 'station-mini-bar-fill fill-green';
            }
        }

        if (card) {
            card.classList.remove('card-status-green', 'card-status-yellow', 'card-status-red');
            if (currentStok <= 0) {
                card.classList.add('card-status-red');
            } else if (currentStok <= ropAdet) {
                card.classList.add('card-status-yellow');
            } else {
                card.classList.add('card-status-green');
            }
        }

        if (ropMark) {
            ropMark.style.left = ropPct + '%';
        }

        if (valTxt) valTxt.textContent = 'Stok: ' + currentStok + ' / ' + cap;
        if (ropTxt) ropTxt.textContent = 'ROP: ' + ropAdet;
    });
}

// ===== SEKME 5: VERİ GİRİŞİ MANTIĞI VE FONKSİYONLARI =====

// Alt-Sekme Değişimi (İstasyonlar vs Tüketim Örneklemi)
function switchDataSubtab(subtab) {
    const btnSt = document.getElementById('btnSubtabStations');
    const btnCo = document.getElementById('btnSubtabConsumption');
    const cntSt = document.getElementById('subtabContentStations');
    const cntCo = document.getElementById('subtabContentConsumption');

    if (subtab === 'stations') {
        if (btnSt) btnSt.className = 'subtab-btn active';
        if (btnCo) btnCo.className = 'subtab-btn';
        if (cntSt) cntSt.style.display = 'block';
        if (cntCo) cntCo.style.display = 'none';
    } else {
        if (btnSt) btnSt.className = 'subtab-btn';
        if (btnCo) btnCo.className = 'subtab-btn active';
        if (cntSt) cntSt.style.display = 'none';
        if (cntCo) cntCo.style.display = 'block';
    }
}

// 24 İstasyon Tablosunu Doldur
function renderDataEntryTable() {
    const tbody = document.getElementById('tbodyStationsInput');
    if (!tbody) return;
    tbody.innerHTML = '';

    activeStationsData.forEach((st, idx) => {
        const sid = st.id;
        const ropCalc = Math.ceil((st.d_saat / 60.0) * 45.0 * 1.15);
        const maxCap = st.n * st.c;

        const tr = document.createElement('tr');
        tr.id = 'row-input-' + sid;
        tr.innerHTML = 
            '<td><strong>' + sid + '</strong>' + (st.fragile ? ' <span style="color:#f43f5e;">⚠️</span>' : '') + '</td>' +
            '<td><span class="tag" style="background:rgba(255,255,255,0.05); color:#cbd5e1;">' + st.hat + '</span></td>' +
            '<td><input type="number" min="1" max="200" step="1" value="' + st.d_saat + '" onchange="onStationFieldChange(' + idx + ', \'d_saat\', this.value)"></td>' +
            '<td><input type="number" min="0" max="50" step="0.1" value="' + (st.std_saat || (st.d_saat * 0.25).toFixed(1)) + '" onchange="onStationFieldChange(' + idx + ', \'std_saat\', this.value)"></td>' +
            '<td><input type="number" min="1" max="100" step="1" value="' + st.c + '" onchange="onStationFieldChange(' + idx + ', \'c\', this.value)"></td>' +
            '<td><input type="number" min="1" max="20" step="1" value="' + st.n + '" onchange="onStationFieldChange(' + idx + ', \'n\', this.value)"></td>' +
            '<td><input type="number" min="0" max="20" step="1" value="' + (st.baslangic_kutu || st.n) + '" onchange="onStationFieldChange(' + idx + ', \'baslangic_kutu\', this.value)"></td>' +
            '<td id="calc-rop-' + sid + '" style="font-weight:600; color:#fde047;">' + ropCalc + ' adet</td>' +
            '<td id="calc-cap-' + sid + '" style="color:#a5f3fc;">' + maxCap + ' adet</td>';
        
        tbody.appendChild(tr);
    });
}

function onStationFieldChange(idx, field, val) {
    const num = parseFloat(val) || 0;
    activeStationsData[idx][field] = num;

    const st = activeStationsData[idx];
    const ropCalc = Math.ceil((st.d_saat / 60.0) * 45.0 * 1.15);
    const maxCap = st.n * st.c;

    const elRop = document.getElementById('calc-rop-' + st.id);
    const elCap = document.getElementById('calc-cap-' + st.id);
    if (elRop) elRop.textContent = ropCalc + ' adet';
    if (elCap) elCap.textContent = maxCap + ' adet';
}

// Sentetik Verileri Forma Doldur
function loadSyntheticDataToForm() {
    activeStationsData = JSON.parse(JSON.stringify(BASE_STATIONS_DATA));
    renderDataEntryTable();
    resetToSyntheticData();
    alert('Sentetik fabrika baz verileri (24 İstasyon) tabloya başarıyla yüklendi.');
}

// Tarayıcı Hafızasına (localStorage) Kaydet
function saveFormToLocalStorage() {
    const success = saveRealDataToStorage(activeStationsData);
    if (success) {
        alert('Girdiğiniz 24 istasyon verisi tarayıcı hafızasına (localStorage) başarıyla kaydedildi.');
    } else {
        alert('Kaydetme sırasında bir hata oluştu.');
    }
}

// Hafızayı Sıfırla
function clearFormStorage() {
    if (confirm('Tarayıcıda saklanan gerçek veri silinip sentetik değerlere dönülsün mü?')) {
        clearRealDataStorage();
        loadSyntheticDataToForm();
    }
}

// Gerçek Veriyi Hesapla ve Önizle
function previewRealData() {
    isPreviewMode = true;
    const banner = document.getElementById('previewModeBanner');
    if (banner) banner.style.display = 'flex';

    renderStations();
    updateStations();
    showTab('tab-istasyon');
}

// Sentetik Veriye Geri Dön
function resetToSyntheticData() {
    isPreviewMode = false;
    const banner = document.getElementById('previewModeBanner');
    if (banner) banner.style.display = 'none';

    renderStations();
    updateStations();
}

// ===== CSV DIŞA AKTARMA (data/real/ ŞABLONLARIYLA HARFİYEN BİREBİR) =====

// 1. stations.csv Dışa Aktarma
function exportStationsCSV() {
    const headers = [
        'istasyon_id',
        'hat',
        'sira_no',
        'ort_tuketim_saat',
        'std_tuketim_saat',
        'ort_tuketim_dk',
        'kutu_kapasitesi',
        'kanban_n',
        'baslangic_kutu',
        'baslangic_stok_adet',
        'reorder_point_kutu'
    ];

    const rows = activeStationsData.map((st, idx) => {
        const d_saat = Number(st.d_saat);
        const std_saat = Number(st.std_saat || (d_saat * 0.25).toFixed(2));
        const d_dk = Number((d_saat / 60.0).toFixed(4));
        const c = Number(st.c);
        const n = Number(st.n);
        const basl_kutu = Number(st.baslangic_kutu || n);
        const basl_adet = basl_kutu * c;
        const rop_adet = Math.ceil(d_dk * 45.0 * 1.15);
        const rop_kutu = Math.max(1, Math.ceil(rop_adet / c));

        return {
            istasyon_id: st.id,
            hat: st.hat,
            sira_no: idx + 1,
            ort_tuketim_saat: d_saat,
            std_tuketim_saat: std_saat,
            ort_tuketim_dk: d_dk,
            kutu_kapasitesi: c,
            kanban_n: n,
            baslangic_kutu: basl_kutu,
            baslangic_stok_adet: basl_adet,
            reorder_point_kutu: rop_kutu
        };
    });

    exportArrayToCSV(rows, headers, 'stations.csv');
}

// 2. consumption.csv Dışa Aktarma
function exportConsumptionCSV() {
    const headers = ['dakika', 'istasyon_id', 'tuketim_adet'];
    const rows = [];

    // Örneklem tablosundan satırları topla, eğer boşsa aktif istasyonlardan örnek 480 dakikalık zaman serisi üret
    const sampleTableRows = document.querySelectorAll('#tbodySampleInput tr');
    if (sampleTableRows.length > 0) {
        const selStation = document.getElementById('selectSampleStation') ? document.getElementById('selectSampleStation').value : 'S1';
        sampleTableRows.forEach(tr => {
            const minInput = tr.querySelector('.sample-min');
            const qtyInput = tr.querySelector('.sample-qty');
            if (minInput && qtyInput) {
                rows.push({
                    dakika: parseInt(minInput.value) || 1,
                    istasyon_id: selStation,
                    tuketim_adet: parseInt(qtyInput.value) || 0
                });
            }
        });
    }

    // Eğer kullanıcı örneklem tablosuna satır girmemişse tüm istasyonlar için 1..10 dk başlangıç serisi ver
    if (rows.length === 0) {
        for (let t = 1; t <= 15; t++) {
            activeStationsData.forEach(st => {
                const lambda = st.d_saat / 60.0;
                const qty = Math.max(0, Math.round(lambda + (Math.sin(t + parseInt(st.id.replace('S',''))) * 0.3)));
                rows.push({
                    dakika: t,
                    istasyon_id: st.id,
                    tuketim_adet: qty
                });
            });
        }
    }

    exportArrayToCSV(rows, headers, 'consumption.csv');
}

// ===== TÜKETİM ÖRNEKLEMİ GİRİŞ ARACI FONKSİYONLARI =====

function initSampleStationSelect() {
    const sel = document.getElementById('selectSampleStation');
    if (!sel) return;
    sel.innerHTML = '';
    activeStationsData.forEach(st => {
        const opt = document.createElement('option');
        opt.value = st.id;
        opt.textContent = st.id + ' (' + st.hat + ' - Mevcut D: ' + st.d_saat + ' adet/saat)';
        sel.appendChild(opt);
    });
}

function initDefaultSampleRows() {
    const tbody = document.getElementById('tbodySampleInput');
    if (!tbody) return;
    tbody.innerHTML = '';
    
    // Varsayılan 5 örnek satır
    const defaults = [
        { min: 5, qty: 2 },
        { min: 10, qty: 1 },
        { min: 15, qty: 3 },
        { min: 20, qty: 2 },
        { min: 25, qty: 1 }
    ];
    defaults.forEach(d => addSampleRow(d.min, d.qty));
}

function addSampleRow(minVal, qtyVal) {
    const tbody = document.getElementById('tbodySampleInput');
    if (!tbody) return;

    const rowIdx = tbody.children.length + 1;
    const tr = document.createElement('tr');
    tr.innerHTML = 
        '<td>' + rowIdx + '</td>' +
        '<td><input type="number" class="sample-min" min="1" max="480" value="' + (minVal !== undefined ? minVal : rowIdx * 5) + '"></td>' +
        '<td><input type="number" class="sample-qty" min="0" max="50" value="' + (qtyVal !== undefined ? qtyVal : 2) + '"></td>' +
        '<td><button class="action-btn btn-danger" style="padding:2px 8px; font-size:11px;" onclick="this.closest(\'tr\').remove()">Sil</button></td>';
    
    tbody.appendChild(tr);
}

function calculateSampleStats() {
    const rows = document.querySelectorAll('#tbodySampleInput tr');
    if (rows.length === 0) {
        alert('Lütfen en az 1 örneklem satırı ekleyin.');
        return;
    }

    const values = [];
    rows.forEach(tr => {
        const input = tr.querySelector('.sample-qty');
        if (input) values.push(parseFloat(input.value) || 0);
    });

    const n = values.length;
    const sum = values.reduce((a, b) => a + b, 0);
    const meanPerSample = sum / n;
    
    // Ortalama dakika aralığı
    const minInputs = document.querySelectorAll('.sample-min');
    let totalDk = 30;
    if (minInputs.length >= 2) {
        const lastMin = parseFloat(minInputs[minInputs.length - 1].value) || 30;
        const firstMin = parseFloat(minInputs[0].value) || 0;
        totalDk = Math.max(5, lastMin - firstMin);
    }
    
    // Saatlik tüketim hızı D hesabı: (Toplam Adet / Toplam Dakika) * 60
    const dSaatCalc = Math.max(1, Math.round((sum / totalDk) * 60));
    
    // Standart sapma hesabı
    let stdCalc = 1.0;
    if (n > 1) {
        const variance = values.reduce((acc, val) => acc + Math.pow(val - meanPerSample, 2), 0) / (n - 1);
        stdCalc = parseFloat((Math.sqrt(variance) * (60 / (totalDk / n))).toFixed(1));
    }

    const selStation = document.getElementById('selectSampleStation').value;
    const stIdx = activeStationsData.findIndex(s => s.id === selStation);

    if (stIdx !== -1) {
        activeStationsData[stIdx].d_saat = dSaatCalc;
        activeStationsData[stIdx].std_saat = stdCalc;
        renderDataEntryTable();

        const resBox = document.getElementById('sampleStatsResult');
        if (resBox) {
            resBox.style.display = 'block';
            resBox.innerHTML = 
                '✅ <strong>Hesaplama Başarılı:</strong> ' + selStation + ' için ' + n + ' örneklem noktasından ortalama saatlik tüketim <strong>D = ' + dSaatCalc + ' adet/saat</strong> ' +
                've standart sapma <strong>&sigma; = ' + stdCalc + ' adet/saat</strong> hesaplanarak 1. Bölümdeki tabloya aktarıldı.';
        }
    }
}
