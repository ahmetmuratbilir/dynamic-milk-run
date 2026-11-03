/**
 * app.js - Dinamik Milk-Run & E-Kanban Karar Destek Dashboard Mantığı (2026 Refactor)
 * =================================================================================
 * v2 Veri Ambarını (data/dashboard_scenarios_v2.json) Okur — 1.920 P3 senaryosu + 640 statik baz
 * Üretici: src/generate_dashboard_data_v2.py (K94). Standalone sürümde window.DASHBOARD_DATA_V2 gömülüdür.
 * 64px Sol Sidebar Navigasyonu + 5 Sekmeli Mimari
 */

// ===== GLOBAL DEĞİŞKENLER VE GRAFİK NESNELERİ =====
let scenariosData = [];
let dashboardMeta = null;
let statikBaz = [];
window.chartInstances = {
    fleet: null,
    pareto: null,
    alpha: null
};

// Statik referans: yüklemede v2 statik_baz'dan türetilir (P2, T=60 dk, baz talep, VDI).
let STATIC_BASELINE_MAP = {};

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

// ===== SIDEBAR SEKME GEÇİŞ MEKANİZMASI =====
function showTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(el => {
        el.style.display = 'none';
    });
    document.querySelectorAll('.sidebar-btn').forEach(el => {
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

// ===== v2 YARDIMCILARI (K94) =====
function ciMetni(s) {
    return (s && s.starv_ci95 != null) ? ' ±' + s.starv_ci95.toFixed(2) : '';
}

function renderSurumDamgasi() {
    const el = document.getElementById('surumDamgasi');
    if (!el || !dashboardMeta) return;
    el.textContent = 'Motor: ' + dashboardMeta.motor + ' · ' + dashboardMeta.replikasyon +
        ' replikasyon · üretim ' + dashboardMeta.uretim_tarihi + ' · değerler ort. ± %95 GA';
    el.title = dashboardMeta.not || '';
}

// ===== UYGULAMA BAŞLATMA =====
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const d = window.DASHBOARD_DATA_V2 ||
            await (await fetch('data/dashboard_scenarios_v2.json')).json();
        scenariosData = d.senaryolar.filter(s => s.politika === 'P3');
        dashboardMeta = d.meta;
        window.DASHBOARD_DATA_V2_YUKLU = d;
        statikBaz = d.statik_baz || [];
        const yeniBaz = {};
        statikBaz.forEach(s => {
            if (s.politika === 'P2' && s.tur_araligi_dk === 60 &&
                s.talep_sok_pct === 0 && s.n_modu === 'Dinamik_N') {
                yeniBaz[s.arac_sayisi] = s.starv_pct;
            }
        });
        if (Object.keys(yeniBaz).length) STATIC_BASELINE_MAP = yeniBaz;
        renderSurumDamgasi();
        console.log('Veri ambarı yüklendi: ' + scenariosData.length + ' senaryo (' + dashboardMeta.motor + ').');
        
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
        initKatkiPaneli();
        initDogrulamaPaneli();

        // Hash tab destegi
        if (window.location.hash) {
            const hashTab = window.location.hash.replace('#', '');
            if (document.getElementById(hashTab)) {
                showTab(hashTab);
            }
        }
        window.addEventListener('hashchange', () => {
            if (window.location.hash) {
                const h = window.location.hash.replace('#', '');
                if (document.getElementById(h)) showTab(h);
            }
        });
    } catch (err) {
        console.error('Veri yükleme hatası:', err);
    }
});

// ===== GRAFİK BAŞLATMA =====
function initAllCharts() {
    const chartConfigCommon = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#475569', font: { family: 'Outfit', size: 11, weight: '500' } } }
        },
        scales: {
            x: { grid: { color: 'rgba(0, 0, 0, 0.05)' }, ticks: { color: '#64748B', font: { size: 11 } } },
            y: { grid: { color: 'rgba(0, 0, 0, 0.05)' }, ticks: { color: '#64748B', font: { size: 11 } } }
        }
    };

// ===== KÖPRÜ NAVİGASYON (GRAFİK / TABLO -> WHAT-IF) =====
function navigateToWhatIf(fleetCount) {
    fleetCount = parseInt(fleetCount, 10);
    const sliderArac = document.getElementById('sliderArac');
    const valArac = document.getElementById('valArac');
    if (sliderArac && valArac && fleetCount >= 1 && fleetCount <= 8) {
        sliderArac.value = fleetCount;
        valArac.textContent = fleetCount + (fleetCount === 4 ? ' Araç (Baz)' : ' Araç');
        updateWhatIfView();
    }
    showTab('tab-whatif');
}

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
                        label: 'Dinamik E-Kanban (Starvation %)',
                        data: [],
                        borderColor: '#2563EB',
                        backgroundColor: 'rgba(37, 99, 235, 0.08)',
                        fill: true,
                        tension: 0.25,
                        borderWidth: 2.5,
                        pointBackgroundColor: '#2563EB',
                        pointRadius: 5,
                        pointHoverRadius: 8
                    },
                    {
                        label: 'Statik referans (P2, T=60 dk, VDI)',
                        data: [],
                        borderColor: '#D97706',
                        borderDash: [4, 4],
                        borderWidth: 1.8,
                        pointRadius: 0
                    },
                    {
                        label: 'Rekabetçilik Eşiği (<%5)',
                        data: [5, 5, 5, 5, 5, 5, 5, 5],
                        borderColor: '#059669',
                        borderDash: [6, 6],
                        borderWidth: 1.5,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                ...chartConfigCommon,
                onClick: (evt, elements) => {
                    if (elements && elements.length > 0) {
                        const idx = elements[0].index;
                        navigateToWhatIf(idx + 1);
                    }
                },
                onHover: (evt, elements) => {
                    const target = evt.native ? evt.native.target : (evt.target || evt);
                    if (target && target.style) {
                        target.style.cursor = (elements && elements.length > 0) ? 'pointer' : 'default';
                    }
                }
            }
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
                        label: 'Tüm Senaryolar',
                        data: bgScatterData,
                        backgroundColor: 'rgba(148, 163, 184, 0.5)',
                        pointRadius: 3
                    },
                    {
                        label: 'Seçili Senaryo',
                        data: [],
                        backgroundColor: '#E11D48',
                        borderColor: '#FFFFFF',
                        borderWidth: 2,
                        pointRadius: 8,
                        pointHoverRadius: 10
                    }
                ]
            },
            options: {
                ...chartConfigCommon,
                scales: {
                    x: { title: { display: true, text: 'Ortalama WIP Stok (adet)', color: '#475569', font: { size: 11, weight: '600' } }, grid: { color: 'rgba(0, 0, 0, 0.05)' }, ticks: { color: '#64748B' } },
                    y: { title: { display: true, text: 'Starvation (%)', color: '#475569', font: { size: 11, weight: '600' } }, grid: { color: 'rgba(0, 0, 0, 0.05)' }, ticks: { color: '#64748B' } }
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
                labels: ['α=0.05', 'α=0.10', 'α=0.15', 'α=0.20', 'α=0.25', 'α=0.30'],
                datasets: [
                    {
                        label: 'Dinamik N (Mod B)',
                        data: [],
                        backgroundColor: '#059669',
                        borderRadius: 4
                    },
                    {
                        label: 'Sabit N (Mod A)',
                        data: [],
                        backgroundColor: '#3B82F6',
                        borderRadius: 4
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
    const cardStarv = document.getElementById('kpiCardStarv');

    if (elStarv) elStarv.textContent = '%' + starvPct.toFixed(2) + ciMetni(bazScenario);
    if (elStarvDk) elStarvDk.textContent = starvDk.toLocaleString() + ' / 11,520 dakika kümülatif duruş';

    if (dotStarv && cardStarv) {
        if (starvPct < 10) {
            dotStarv.className = 'status-dot dot-good';
            cardStarv.className = 'kpi-card status-good';
        } else if (starvPct <= 25) {
            dotStarv.className = 'status-dot dot-warning';
            cardStarv.className = 'kpi-card status-warning';
        } else {
            dotStarv.className = 'status-dot dot-critical';
            cardStarv.className = 'kpi-card status-critical';
        }
    }

    // KPI 2: WIP
    const elWip = document.getElementById('kpiWipVal');
    if (elWip) elWip.textContent = ortWip.toFixed(1);

    // KPI 3: Statik vs Dinamik Farkı
    const staticBase = STATIC_BASELINE_MAP[4];
    const diffPuan = staticBase != null ? (starvPct - staticBase).toFixed(2) : null;
    const elFark = document.getElementById('kpiFarkVal');
    if (elFark) elFark.textContent = diffPuan == null ? '—' : (diffPuan >= 0 ? '+' : '') + diffPuan + ' puan';

    // KPI 4: Doluluk
    const elDoluluk = document.getElementById('kpiDolulukVal');
    if (elDoluluk) elDoluluk.textContent = bazScenario.doluluk_pct != null ? '%' + bazScenario.doluluk_pct.toFixed(1) : '—';

    // Otomatik Dinamik Yorum
    const commentEl = document.getElementById('dynamicCommentText');
    if (commentEl) {
        // %5 eşiğine inen en küçük filo veriden bulunur
        let esikFilo = null;
        for (let v = 1; v <= 8 && esikFilo === null; v++) {
            const it = scenariosData.find(s => s.arac_sayisi === v && Math.abs(s.alpha - 0.15) < 0.01 &&
                s.talep_sok_pct === 0 && s.dispatch_kural === 'EDD' && s.n_modu === 'Dinamik_N');
            if (it && it.starv_pct < 5) esikFilo = v;
        }
        let farkCumle = '';
        if (diffPuan != null) {
            const f = parseFloat(diffPuan);
            farkCumle = 'Bu değer aynı filodaki statik referansla (P2, T=60 dk: %' + staticBase.toFixed(2) + ') ' +
                (Math.abs(f) < 0.5 ? 'pratikte aynıdır (fark ' + diffPuan + ' puan). '
                    : 'karşılaştırıldığında <strong>' + Math.abs(f).toFixed(2) + ' puan</strong> ' + (f > 0 ? 'yüksektir. ' : 'düşüktür. '));
        }
        commentEl.innerHTML =
            'Baz senaryoda (4 araç, α=0,15, EDD, politika-tutarlı boyutlandırma) dinamik sistem <strong>%' +
            starvPct.toFixed(2) + ciMetni(bazScenario) + '</strong> duruşla çalışmaktadır. ' + farkCumle +
            (esikFilo ? '%5 duruş eşiğine <strong>' + esikFilo + ' araç</strong>la inilmektedir. ' : '') +
            'Yeterli filoda politikalar arasındaki fark duruşta değil stoktadır (K96, K97).';
    }

    // Filo Duyarlılık Eğrisini Çiz
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
        window.chartInstances.fleet.data.datasets[1].data =
            [1, 2, 3, 4, 5, 6, 7, 8].map(v => STATIC_BASELINE_MAP[v] != null ? STATIC_BASELINE_MAP[v] : null);
        window.chartInstances.fleet.update();
    }
}

// 1) WHAT-IF DINAMIK YORUM CUMLESI FONKSIYONU (HAZIR METIN SABLONU)
function getYorumCumlesi(starvPct, staticBase) {
    let anaYorum = '';
    if (starvPct < 5) {
        anaYorum = '🎯 Hedefe ulaşıldı — bu senaryoda sistem rekabetçi eşiğin (%5) altında çalışıyor.';
    } else if (starvPct < 15) {
        anaYorum = '🟡 Sistem hedefe yaklaşıyor ama henüz ulaşmadı. Filo büyüklüğünü artırmak en etkili müdahaledir (güvenlik katsayısı α anlamlı etki göstermemiştir, K82).';
    } else if (starvPct < 30) {
        anaYorum = '🟠 Sistem hedefin belirgin şekilde üzerinde. Filo büyüklüğü, bu senaryodaki en etkili müdahale noktasıdır (bkz. Filo Duyarlılık Eğrisi).';
    } else {
        anaYorum = '🔴 Kritik seviye — mevcut ayarlarda sistem ciddi tedarik riski taşıyor.';
    }

    let karsilastirma = '';
    if (staticBase == null) {
        karsilastirma = '';
    } else if (Math.abs(starvPct - staticBase) < 0.5) {
        karsilastirma = ' Statik referansla (%' + staticBase.toFixed(2) + ') duruş pratikte aynı; fark stokta aranmalı.';
    } else if (starvPct > staticBase) {
        karsilastirma = ' Bu senaryoda statik sistem (%' + staticBase.toFixed(2) + ') hâlâ daha avantajlı.';
    } else {
        karsilastirma = ' Bu senaryoda dinamik sistem, statik sistemi (%' + staticBase.toFixed(2) + ') geride bırakmış durumda ⚡.';
    }

    return anaYorum + karsilastirma;
}

// 2) ISTASYON POPUP METNI FONKSIYONU (HAZIR METIN SABLONU)
function getIstasyonPopupMetni(st) {
    const fabrikaOrtalamasi = 17.5; // 24 istasyonun ortalama D değeri (yaklaşık)
    const sapmaYuzde = Math.round(((st.d_saat - fabrikaOrtalamasi) / fabrikaOrtalamasi) * 100);
    const yonIfadesi = sapmaYuzde >= 0 ? 'üzerinde' : 'altında';

    let metin = st.id + ' (' + st.hat + '): Saatlik tüketim ' + st.d_saat +
        ' adet — fabrika ortalamasının %' + Math.abs(sapmaYuzde) + ' ' + yonIfadesi + '. ' +
        'Kutu kapasitesi ' + st.c + ', ' + st.n + ' Kanban kartıyla toplam ' + (st.n * st.c) +
        ' adetlik tampon stok kapasitesine sahip.';

    if (st.fragile) {
        metin += ' ⚠️ Bu, fabrikadaki en kırılgan istasyondur — yüksek tüketime rağmen ' +
                  'sınırlı tampon kapasitesi, onu izlemeye en çok ihtiyaç duyulan nokta yapar.';
    }
    return metin;
}

// ===== SEKME 2 (WHAT-IF) GÖRÜNÜMÜNÜ GÜNCELLEME =====
function updateWhatIfView() {
    if (!scenariosData || scenariosData.length === 0) return;

    const params = getWhatIfParameters();

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

    const wiStarvVal = document.getElementById('wiStarvVal');
    const wiStarvDk = document.getElementById('wiStarvDk');
    if (wiStarvVal) wiStarvVal.textContent = '%' + starvPct.toFixed(2) + ciMetni(curScenario);
    if (wiStarvDk) wiStarvDk.textContent = starvDk.toLocaleString() + ' / 11,520 dk';

    const wiWipVal = document.getElementById('wiWipVal');
    if (wiWipVal) wiWipVal.textContent = ortWip.toFixed(1);

    const staticBase = STATIC_BASELINE_MAP[params.arac_sayisi];
    const diffPuan = staticBase != null ? (starvPct - staticBase).toFixed(2) : null;
    const wiFarkVal = document.getElementById('wiFarkVal');
    const wiFarkSub = document.getElementById('wiFarkSub');

    if (wiFarkVal) {
        wiFarkVal.textContent = diffPuan == null ? '—' : (diffPuan >= 0 ? '+' : '') + diffPuan + ' puan';
        wiFarkVal.style.color = diffPuan <= 0 ? '#059669' : (diffPuan <= 5 ? '#D97706' : '#E11D48');
    }
    if (wiFarkSub) {
        wiFarkSub.textContent = params.arac_sayisi + ' araç statik ref: %' + staticBase.toFixed(2);
    }

    // 1) What-If Yorum Cümlesini Güncelle
    const wiCommentEl = document.getElementById('whatifCommentText');
    if (wiCommentEl) {
        wiCommentEl.textContent = getYorumCumlesi(starvPct, staticBase);
    }

    const wiDolulukVal = document.getElementById('wiDolulukVal');
    if (wiDolulukVal) {
        wiDolulukVal.textContent = curScenario.doluluk_pct != null ? '%' + curScenario.doluluk_pct.toFixed(1) : '—';
    }

    if (window.chartInstances.pareto) {
        window.chartInstances.pareto.data.datasets[1].data = [{ x: ortWip, y: starvPct }];
        window.chartInstances.pareto.update();
    }

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
        const popupText = getIstasyonPopupMetni(st);
        
        const card = document.createElement('div');
        card.className = 'st-card' + (isFragile ? ' is-fragile' : '');
        card.id = 'st-card-' + sid;
        
        card.innerHTML = 
            '<div class="st-card-top">' +
                '<span class="st-card-id">' + sid + 
                    (isFragile ? ' <span style="color:#E11D48; font-size:12px;" title="Kırılgan İstasyon">⚠️</span>' : '') + 
                '</span>' +
                '<span class="st-card-hat">' + st.hat + '</span>' +
            '</div>' +
            '<div class="st-bar-wrap">' +
                '<div class="st-bar-fill fill-good" id="st-bar-' + sid + '" style="width: 70%;"></div>' +
                '<div class="st-rop-line" id="st-rop-mark-' + sid + '" style="left: 45%;"></div>' +
            '</div>' +
            '<div class="st-card-bottom">' +
                '<span id="st-val-' + sid + '" style="font-weight:600; color:#0F172A;">Stok: ' + (st.n * st.c) + '</span>' +
                '<span id="st-rop-' + sid + '" style="font-weight:600; color:#D97706;">ROP: ' + Math.ceil((st.d_saat/60)*45*1.15) + '</span>' +
            '</div>' +
            '<div class="st-card-popup" id="st-popup-' + sid + '">' + popupText + '</div>';
        
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
        
        // Motorla aynı (kanban_boyutlandir, P3): VDI N = 1 + ⌈ROP/C⌉ (K65); V1 N = max(1, ⌈ROP/C⌉)
        const nKart = params.n_modu === 'Dinamik_N'
            ? 1 + Math.ceil(ropAdet / st.c - 1e-9)
            : Math.max(1, Math.ceil(ropAdet / st.c - 1e-9));
        const cap = nKart * st.c;

        let currentStok = st.fragile ? Math.round(ropAdet * 0.75) : Math.round(cap * 0.85);
        if (params.arac_sayisi < 3) currentStok = Math.max(0, currentStok - Math.round(st.c * 0.4));
        if (params.talep_sok_pct > 0) currentStok = Math.max(0, currentStok - Math.round(st.c * 0.2));

        const pct = Math.min(100, Math.max(0, (currentStok / cap) * 100));
        const ropPct = Math.min(100, Math.max(0, (ropAdet / cap) * 100));

        if (bar) {
            bar.style.width = pct + '%';
            if (currentStok <= 0) {
                bar.className = 'st-bar-fill fill-critical';
            } else if (currentStok <= ropAdet) {
                bar.className = 'st-bar-fill fill-warning';
            } else {
                bar.className = 'st-bar-fill fill-good';
            }
        }

        if (card) {
            card.classList.remove('border-good', 'border-warning', 'border-critical');
            if (currentStok <= 0) {
                card.classList.add('border-critical');
            } else if (currentStok <= ropAdet) {
                card.classList.add('border-warning');
            } else {
                card.classList.add('border-good');
            }
        }

        if (ropMark) {
            ropMark.style.left = ropPct + '%';
        }

        if (valTxt) valTxt.textContent = 'Stok: ' + currentStok + ' / ' + cap;
        if (ropTxt) ropTxt.textContent = 'ROP: ' + ropAdet;
    });

    applyStationFilter();
}

// ===== 2) İSTASYON AKILLI HIZLI FİLTRELEME MANTIĞI =====
let currentStationFilter = 'all';

function filterStations(filterType) {
    currentStationFilter = filterType;
    ['btnFilterAll', 'btnFilterAlert', 'btnFilterFragile'].forEach(id => {
        const btn = document.getElementById(id);
        if (btn) btn.className = 'btn-action btn-subtle';
    });
    if (filterType === 'all') {
        const b = document.getElementById('btnFilterAll');
        if (b) b.className = 'btn-action btn-accent';
    } else if (filterType === 'alert') {
        const b = document.getElementById('btnFilterAlert');
        if (b) b.className = 'btn-action btn-accent';
    } else if (filterType === 'fragile') {
        const b = document.getElementById('btnFilterFragile');
        if (b) b.className = 'btn-action btn-accent';
    }
    applyStationFilter();
}

function applyStationFilter() {
    activeStationsData.forEach(st => {
        const sid = st.id;
        const card = document.getElementById('st-card-' + sid);
        if (!card) return;

        if (currentStationFilter === 'all') {
            card.style.display = 'flex';
        } else if (currentStationFilter === 'fragile') {
            card.style.display = st.fragile ? 'flex' : 'none';
        } else if (currentStationFilter === 'alert') {
            const isWarningOrCrit = card.classList.contains('border-warning') || 
                                    card.classList.contains('border-critical') || 
                                    st.fragile;
            card.style.display = isWarningOrCrit ? 'flex' : 'none';
        }
    });
}


// ===== SEKME 5: VERİ GİRİŞİ MANTIĞI =====
function switchDataSubtab(subtab) {
    const btnSt = document.getElementById('btnSubtabStations');
    const btnCo = document.getElementById('btnSubtabConsumption');
    const cntSt = document.getElementById('subtabContentStations');
    const cntCo = document.getElementById('subtabContentConsumption');

    if (subtab === 'stations') {
        if (btnSt) btnSt.className = 'btn-action btn-accent';
        if (btnCo) btnCo.className = 'btn-action btn-subtle';
        if (cntSt) cntSt.style.display = 'block';
        if (cntCo) cntCo.style.display = 'none';
    } else {
        if (btnSt) btnSt.className = 'btn-action btn-subtle';
        if (btnCo) btnCo.className = 'btn-action btn-accent';
        if (cntSt) cntSt.style.display = 'none';
        if (cntCo) cntCo.style.display = 'block';
    }
}

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
            '<td><strong>' + sid + '</strong>' + (st.fragile ? ' <span style="color:#E11D48;">⚠️</span>' : '') + '</td>' +
            '<td><span style="background:#F1F5F9; padding:2px 6px; border-radius:4px; font-size:11px; color:#475569; font-weight:600;">' + st.hat + '</span></td>' +
            '<td><input type="number" min="1" max="200" step="1" value="' + st.d_saat + '" onchange="onStationFieldChange(' + idx + ', \'d_saat\', this.value)" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; padding:4px 8px; color:#0F172A; width:80px; text-align:center; font-weight:500;"></td>' +
            '<td><input type="number" min="0" max="50" step="0.1" value="' + (st.std_saat || (st.d_saat * 0.25).toFixed(1)) + '" onchange="onStationFieldChange(' + idx + ', \'std_saat\', this.value)" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; padding:4px 8px; color:#0F172A; width:70px; text-align:center; font-weight:500;"></td>' +
            '<td><input type="number" min="1" max="100" step="1" value="' + st.c + '" onchange="onStationFieldChange(' + idx + ', \'c\', this.value)" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; padding:4px 8px; color:#0F172A; width:70px; text-align:center; font-weight:500;"></td>' +
            '<td><input type="number" min="1" max="20" step="1" value="' + st.n + '" onchange="onStationFieldChange(' + idx + ', \'n\', this.value)" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; padding:4px 8px; color:#0F172A; width:70px; text-align:center; font-weight:500;"></td>' +
            '<td><input type="number" min="0" max="20" step="1" value="' + (st.baslangic_kutu || st.n) + '" onchange="onStationFieldChange(' + idx + ', \'baslangic_kutu\', this.value)" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; padding:4px 8px; color:#0F172A; width:70px; text-align:center; font-weight:500;"></td>' +
            '<td id="calc-rop-' + sid + '" style="font-weight:700; color:#D97706;">' + ropCalc + ' adet</td>' +
            '<td id="calc-cap-' + sid + '" style="font-weight:700; color:#2563EB;">' + maxCap + ' adet</td>';
        
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

function loadSyntheticDataToForm() {
    activeStationsData = JSON.parse(JSON.stringify(BASE_STATIONS_DATA));
    renderDataEntryTable();
    resetToSyntheticData();
    alert('Sentetik fabrika baz verileri (24 İstasyon) tabloya başarıyla yüklendi.');
}

function saveFormToLocalStorage() {
    const success = saveRealDataToStorage(activeStationsData);
    if (success) {
        alert('Girdiğiniz 24 istasyon verisi tarayıcı hafızasına (localStorage) başarıyla kaydedildi.');
    } else {
        alert('Kaydetme sırasında bir hata oluştu.');
    }
}

function clearFormStorage() {
    if (confirm('Tarayıcıda saklanan gerçek veri silinip sentetik değerlere dönülsün mü?')) {
        clearRealDataStorage();
        loadSyntheticDataToForm();
    }
}

function previewRealData() {
    isPreviewMode = true;
    const banner = document.getElementById('previewModeBanner');
    if (banner) banner.style.display = 'flex';

    renderStations();
    updateStations();
    showTab('tab-istasyon');
}

function resetToSyntheticData() {
    isPreviewMode = false;
    const banner = document.getElementById('previewModeBanner');
    if (banner) banner.style.display = 'none';

    renderStations();
    updateStations();
}

// ===== CSV DIŞA AKTARMA (data/real/ ŞABLONLARIYLA HARFİYEN BİREBİR) =====
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

function exportConsumptionCSV() {
    const headers = ['dakika', 'istasyon_id', 'tuketim_adet'];
    const rows = [];

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
        '<td><input type="number" class="sample-min" min="1" max="480" value="' + (minVal !== undefined ? minVal : rowIdx * 5) + '" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; padding:4px 8px; color:#0F172A; width:80px; text-align:center; font-weight:500;"></td>' +
        '<td><input type="number" class="sample-qty" min="0" max="50" value="' + (qtyVal !== undefined ? qtyVal : 2) + '" style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:6px; padding:4px 8px; color:#0F172A; width:80px; text-align:center; font-weight:500;"></td>' +
        '<td><button class="btn-action btn-subtle" style="height:26px; padding:0 8px; font-size:11px; color:#E11D48;" onclick="this.closest(\'tr\').remove()">Sil</button></td>';
    
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
    
    const minInputs = document.querySelectorAll('.sample-min');
    let totalDk = 30;
    if (minInputs.length >= 2) {
        const lastMin = parseFloat(minInputs[minInputs.length - 1].value) || 30;
        const firstMin = parseFloat(minInputs[0].value) || 0;
        totalDk = Math.max(5, lastMin - firstMin);
    }
    
    const dSaatCalc = Math.max(1, Math.round((sum / totalDk) * 60));
    
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
                've standart sapma <strong>σ = ' + stdCalc + ' adet/saat</strong> hesaplanarak 1. Bölümdeki tabloya aktarıldı.';
        }
    }
}


// ===== KADEME 2 · ANA KATKI PANELLERİ (D4, D5, D6, K97) =====
const KATKI_RENK = { gel: '#2a78d6', dij: '#1baf7a', p1: '#8a5cd6', v1: '#d6612a' };
const KURAL_AD = { A: 'A · Eşit kart', B: 'B · Politika-tutarlı', C: 'C · Eşit hizmet', D: 'D · Eşit WIP' };
// Veri ambarındaki talep düzeyleri (generate_dashboard_data_v2: TALEP_SOK)
const TALEP_DUZEYLERI = [-20, -10, 0, 10, 20];
const TALEP_ETIKET = { '-20': '−%20', '-10': '−%10', '0': 'Baz', '10': '+%10', '20': '+%20' };

function _secenekDoldur(id, degerler, etiket, varsayilan) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = degerler.map(v => '<option value="' + v + '"' + (String(v) === String(varsayilan) ? ' selected' : '') +
        '>' + etiket(v) + '</option>').join('');
}

function _sayi(v, b) { return v == null ? '—' : Number(v).toFixed(b); }

function initKatkiPaneli() {
    if (!window.DASHBOARD_DATA_V2_YUKLU) return;
    _secenekDoldur('polArac', [1, 2, 3, 4, 5, 6, 7, 8], v => v + ' araç', 3);
    _secenekDoldur('polTalep', TALEP_DUZEYLERI, v => TALEP_ETIKET[v], 0);
    _secenekDoldur('parTalep', TALEP_DUZEYLERI, v => TALEP_ETIKET[v], 0);
    const bagla = (idler, fn) => idler.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', fn);
    });
    bagla(['polArac', 'polTalep', 'polNModu'], renderPolitikaTablosu);
    bagla(['adaletKutu', 'adaletTalep'], renderAdalet);
    bagla(['parTalep', 'parP3VDI', 'parP3V1', 'parP1', 'parP2'], renderParetoTum);
    renderPolitikaTablosu();
    renderAdalet();
    renderParetoTum();
    renderAblation();
}

// D4 · P1/P2/P3 karşılaştırması: her politika kendi kart sayısıyla
function renderPolitikaTablosu() {
    const tb = document.getElementById('polTablo');
    if (!tb) return;
    const arac = parseInt(document.getElementById('polArac').value, 10);
    const talep = parseInt(document.getElementById('polTalep').value, 10);
    const nModu = document.getElementById('polNModu').value;
    const satirlar = statikBaz
        .filter(s => s.arac_sayisi === arac && s.talep_sok_pct === talep && s.n_modu === nModu)
        .sort((a, b) => a.politika.localeCompare(b.politika) || a.tur_araligi_dk - b.tur_araligi_dk)
        .map(s => ({
            ad: s.politika === 'P1' ? 'P1 · sabit takt, sabit miktar' : 'P2 · sabit takt, Kanban miktarı',
            takt: s.tur_araligi_dk + ' dk', s
        }));
    const p3 = scenariosData.find(s => s.arac_sayisi === arac && s.talep_sok_pct === talep && s.n_modu === nModu &&
        Math.abs(s.alpha - 0.15) < 0.01 && s.dispatch_kural === 'EDD');
    if (p3) satirlar.push({ ad: 'P3 · olay tabanlı (e-Kanban)', takt: 'sinyalle', s: p3 });
    if (!satirlar.length) { tb.innerHTML = ''; return; }
    const enIyi = Math.min(...satirlar.map(r => r.s.starv_pct));
    tb.innerHTML = satirlar.map(r => {
        const s = r.s;
        const iyi = s.starv_pct - enIyi < 0.5;
        return '<tr' + (r.ad.startsWith('P3') ? ' class="katki-p3"' : '') + '><td><strong>' + r.ad + '</strong></td><td>' +
            r.takt + '</td><td><span style="font-weight:700;color:' + (iyi ? 'var(--status-good)' : 'inherit') + '">%' +
            _sayi(s.starv_pct, 2) + '</span> <span class="katki-ga">± ' + _sayi(s.starv_ci95, 2) + '</span></td><td>' +
            _sayi(s.ort_wip, 0) + '</td><td>' + _sayi(s.toplam_kart, 0) + '</td><td>' + _sayi(s.sefer_sayisi, 1) +
            '</td><td>' + _sayi(s.mesafe_km, 1) + '</td><td>' + _sayi(s.doluluk_pct, 1) + '</td></tr>';
    }).join('');
    const notEl = document.getElementById('polNot');
    if (notEl) notEl.textContent = nModu === 'Dinamik_N'
        ? 'Politika-tutarlı boyutlandırmada her politikanın kart sayısı kendi çevrim süresinden türetilir; T büyüdükçe P1/P2 daha fazla kart alır. Yeşil: en düşük duruşa 0,5 puan içinde olanlar. P3: α=0,15, EDD.'
        : 'Eski boyutlandırmada (V1) kart sayısı politikadan bağımsızdır; sabit taktlı politikalar çevrim sürelerinin gerektirdiği tamponu alamaz. Düzeltilen hata budur (K65).';
}

// K97 · Dört adalet kuralı
function renderAdalet() {
    const ad = (window.DASHBOARD_DATA_V2_YUKLU || {}).adalet || {};
    const kutu = document.getElementById('adaletKutu').value;
    const talep = document.getElementById('adaletTalep').value;
    const k = ad[kutu];
    const tb = document.getElementById('adaletTablo');
    if (!k) {
        if (tb) tb.innerHTML = '<tr><td colspan="6">Adalet verisi yok. Önce <code>python -X utf8 -m src.v2_adalet_kurallari</code> çalıştırılmalı.</td></tr>';
        return;
    }
    const egri = sistem => k.egriler.filter(r => r.talep === talep && r.sistem === sistem)
        .sort((a, b) => a.ort_wip - b.ort_wip).map(r => ({ x: r.ort_wip, y: r.starv_pct }));
    const kural = sistem => k.kurallar.filter(r => r.talep === talep && r.sistem === sistem)
        .map(r => ({ x: r.ort_wip, y: r.starv_pct, kural: r.kural }));
    const setler = [
        { label: 'Geleneksel · kart taraması', data: egri('Geleneksel'), showLine: true, borderColor: KATKI_RENK.gel + '88', backgroundColor: KATKI_RENK.gel, pointRadius: 2, borderWidth: 2 },
        { label: 'Dijital · kart taraması', data: egri('Dijital'), showLine: true, borderColor: KATKI_RENK.dij + '88', backgroundColor: KATKI_RENK.dij, pointRadius: 2, borderWidth: 2 },
        { label: 'Geleneksel · kural', data: kural('Geleneksel'), pointRadius: 8, pointStyle: 'rectRot', backgroundColor: KATKI_RENK.gel, borderColor: '#0F172A', borderWidth: 1 },
        { label: 'Dijital · kural', data: kural('Dijital'), pointRadius: 8, pointStyle: 'circle', backgroundColor: KATKI_RENK.dij, borderColor: '#0F172A', borderWidth: 1 }
    ];
    const noktalar = setler[2].data.concat(setler[3].data);
    const xUst = 1.35 * Math.max(...noktalar.map(p => p.x));
    const gorunur = setler[0].data.concat(setler[1].data).filter(p => p.x <= xUst).map(p => p.y);
    const yUst = 1.15 * Math.max(2, ...noktalar.map(p => p.y), ...gorunur);
    // Aynı noktaya düşen kurallar tek etiketle yazılır ("B=D")
    const etiketEklentisi = {
        id: 'kuralEtiket',
        afterDatasetsDraw(chart) {
            const ctx = chart.ctx;
            [2, 3].forEach(di => {
                const gruplar = {};
                chart.data.datasets[di].data.forEach(r => {
                    const anahtar = Math.round(r.x) + '|' + r.y.toFixed(2);
                    if (!gruplar[anahtar]) gruplar[anahtar] = { r, metin: r.kural };
                    else gruplar[anahtar].metin += '=' + r.kural;
                });
                Object.values(gruplar).forEach(({ r, metin }) => {
                    const x = chart.scales.x.getPixelForValue(r.x);
                    const y = chart.scales.y.getPixelForValue(r.y);
                    ctx.save();
                    ctx.font = '700 11px Outfit, sans-serif';
                    ctx.fillStyle = di === 2 ? KATKI_RENK.gel : KATKI_RENK.dij;
                    ctx.fillText(metin, di === 2 ? x + 9 : x - 10 - 7 * metin.length, di === 2 ? y - 8 : y + 16);
                    ctx.restore();
                });
            });
        }
    };
    if (window.chartInstances.adalet) window.chartInstances.adalet.destroy();
    const cv = document.getElementById('chartAdalet');
    if (cv) {
        window.chartInstances.adalet = new Chart(cv.getContext('2d'), {
            type: 'scatter',
            data: { datasets: setler },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                plugins: {
                    legend: { labels: { color: '#475569', font: { family: 'Outfit', size: 11 } } },
                    tooltip: { callbacks: { label: c => (c.raw.kural ? KURAL_AD[c.raw.kural] + ' · ' : '') + 'WIP ' + c.raw.x.toFixed(0) + ', duruş %' + c.raw.y.toFixed(2) } }
                },
                scales: {
                    x: { min: 0, max: xUst, title: { display: true, text: 'Ortalama WIP (adet)', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } },
                    y: { min: 0, max: yUst, title: { display: true, text: 'Hat duruş oranı (%)', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } }
                }
            },
            plugins: [etiketEklentisi]
        });
    }
    const renk = kim => kim === 'Dijital' ? KATKI_RENK.dij : (kim === 'Geleneksel' ? KATKI_RENK.gel : '#64748B');
    if (tb) tb.innerHTML = k.kazanan.filter(r => r.talep === talep).map(r =>
        '<tr><td><strong>' + KURAL_AD[r.kural] + '</strong></td><td>' + r.olcut + '</td><td><span class="katki-cip" style="background:' +
        renk(r.kazanan) + '1f;color:' + renk(r.kazanan) + '">' + r.kazanan + '</span></td><td>' + (r.fark_durus >= 0 ? '+' : '') +
        _sayi(r.fark_durus, 2) + ' <span class="katki-ga">± ' + _sayi(r.ga, 2) + '</span></td><td>' + (r.wip_fark_pct >= 0 ? '+' : '') +
        _sayi(r.wip_fark_pct, 0) + '%</td><td>' + r.pareto + '</td></tr>').join('');
}

// D6 · Etkileşimli Pareto cephesi
function renderParetoTum() {
    const talep = parseInt(document.getElementById('parTalep').value, 10);
    const acik = id => { const el = document.getElementById(id); return !!(el && el.checked); };
    const nokta = (s, etiket) => ({ x: s.ort_wip, y: s.starv_pct, s, etiket });
    const setler = [];
    if (acik('parP3VDI')) setler.push({ label: 'P3 · VDI', data: scenariosData.filter(s => s.talep_sok_pct === talep && s.n_modu === 'Dinamik_N').map(s => nokta(s, 'P3')), backgroundColor: KATKI_RENK.dij + 'aa', pointRadius: 3 });
    if (acik('parP3V1')) setler.push({ label: 'P3 · V1', data: scenariosData.filter(s => s.talep_sok_pct === talep && s.n_modu === 'Sabit_N').map(s => nokta(s, 'P3')), backgroundColor: KATKI_RENK.v1 + '88', pointRadius: 3 });
    if (acik('parP1')) setler.push({ label: 'P1', data: statikBaz.filter(s => s.talep_sok_pct === talep && s.politika === 'P1').map(s => nokta(s, 'P1')), backgroundColor: KATKI_RENK.p1, pointRadius: 5, pointStyle: 'triangle' });
    if (acik('parP2')) setler.push({ label: 'P2', data: statikBaz.filter(s => s.talep_sok_pct === talep && s.politika === 'P2').map(s => nokta(s, 'P2')), backgroundColor: KATKI_RENK.gel, pointRadius: 5, pointStyle: 'rectRot' });
    // Görünür noktaların Pareto cephesi: daha az WIP ile daha az duruş
    const hepsi = setler.flatMap(d => d.data).sort((a, b) => a.x - b.x || a.y - b.y);
    const cephe = [];
    let enAz = Infinity;
    hepsi.forEach(p => { if (p.y < enAz - 1e-9) { cephe.push({ x: p.x, y: p.y }); enAz = p.y; } });
    setler.push({ label: 'Pareto cephesi', data: cephe, showLine: true, borderColor: '#0F172A', borderWidth: 1.5, pointRadius: 0, stepped: 'before' });
    if (window.chartInstances.paretoTum) window.chartInstances.paretoTum.destroy();
    const cv = document.getElementById('chartParetoTum');
    if (!cv) return;
    window.chartInstances.paretoTum = new Chart(cv.getContext('2d'), {
        type: 'scatter',
        data: { datasets: setler },
        options: {
            responsive: true, maintainAspectRatio: false, animation: false,
            plugins: {
                legend: { labels: { color: '#475569', font: { family: 'Outfit', size: 11 } } },
                tooltip: { callbacks: { label: c => c.raw.s ? _paretoMetin(c.raw) : 'Pareto cephesi' } }
            },
            scales: {
                x: { title: { display: true, text: 'Ortalama WIP (adet)', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } },
                y: { min: 0, title: { display: true, text: 'Hat duruş oranı (%)', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } }
            },
            onClick: (evt, el) => {
                if (!el.length) return;
                const r = setler[el[0].datasetIndex].data[el[0].index];
                const d = document.getElementById('parDetay');
                if (d && r.s) d.textContent = _paretoMetin(r);
            }
        }
    });
}

function _paretoMetin(r) {
    const s = r.s;
    const mod = s.n_modu === 'Dinamik_N' ? 'VDI' : 'V1';
    const ayar = r.etiket === 'P3'
        ? 'P3 · ' + s.arac_sayisi + ' araç · α=' + s.alpha.toFixed(2) + ' · ' + s.dispatch_kural + ' · ' + mod
        : r.etiket + ' · T=' + s.tur_araligi_dk + ' dk · ' + s.arac_sayisi + ' araç · ' + mod;
    return ayar + ' → duruş %' + _sayi(s.starv_pct, 2) + ' ± ' + _sayi(s.starv_ci95, 2) + ', WIP ' + _sayi(s.ort_wip, 0) +
        ', ' + _sayi(s.toplam_kart, 0) + ' kart, ' + _sayi(s.mesafe_km, 1) + ' km';
}

// D5 · Ayrıştırma: adımlar açılıp kapatılabilir
function renderAblation() {
    const tumu = (window.DASHBOARD_DATA_V2_YUKLU || {}).ablation || [];
    const ab = tumu.filter(r => r.d_starv_puan != null);
    const liste = document.getElementById('ablationListe');
    const cv = document.getElementById('chartAblation');
    if (!ab.length || !liste || !cv) return;
    const temizAd = r => r.adim.replace(/^\+ /, '');
    liste.innerHTML = ab.map((r, i) => '<label class="katki-onay"><input type="checkbox" id="abl' + i + '" checked> ' +
        temizAd(r) + ' <span class="katki-ga">(' + (r.d_starv_puan >= 0 ? '+' : '') + r.d_starv_puan.toFixed(2) + ')</span></label>').join('');
    if (window.chartInstances.ablation) window.chartInstances.ablation.destroy();
    window.chartInstances.ablation = new Chart(cv.getContext('2d'), {
        type: 'bar',
        data: { labels: ab.map(temizAd), datasets: [{ label: 'Duruş değişimi (puan)', data: ab.map(r => r.d_starv_puan), backgroundColor: [] }] },
        options: {
            indexAxis: 'y', responsive: true, maintainAspectRatio: false, animation: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { title: { display: true, text: 'Duruş oranına etkisi (puan)', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } },
                y: { grid: { display: false }, ticks: { color: '#334155', font: { size: 11 } } }
            }
        }
    });
    const ciz = () => {
        const secili = ab.map((r, i) => document.getElementById('abl' + i).checked);
        const toplam = ab.reduce((t, r, i) => t + (secili[i] ? r.d_starv_puan : 0), 0);
        const ozet = document.getElementById('ablationToplam');
        const bas = tumu[0];
        if (ozet) ozet.innerHTML = 'Seçili adımların toplam etkisi: <strong>' + (toplam >= 0 ? '+' : '') + toplam.toFixed(2) +
            ' puan</strong>' + (bas ? ' (v1 referansı %' + bas.starv_pct.toFixed(2) + ' → yaklaşık %' +
            Math.max(0, bas.starv_pct + toplam).toFixed(2) + ')' : '') + '.';
        const ch = window.chartInstances.ablation;
        ch.data.datasets[0].backgroundColor = ab.map((r, i) => !secili[i] ? '#E2E8F0' : (r.d_starv_puan < 0 ? KATKI_RENK.dij : '#E11D48'));
        ch.update();
    };
    ab.forEach((r, i) => document.getElementById('abl' + i).addEventListener('change', ciz));
    ciz();
}


// ===== KADEME 3 · DOĞRULAMA (D7) VE SENARYO KARŞILAŞTIRICI (D8) =====
function initDogrulamaPaneli() {
    const d = window.DASHBOARD_DATA_V2_YUKLU;
    if (!d) return;
    const dg = d.dogrulama || {};

    const tb = document.getElementById('saglamlikTablo');
    if (tb) tb.innerHTML = (d.saglamlik || []).map(r =>
        '<tr><td><strong>' + r.kod + '</strong></td><td>' + r.test + '</td><td>' + r.kosul + '</td><td>' +
        (r.kayma_pozitif == null ? '—' : r.kayma_pozitif + '/' + r.kosul) + '</td><td>' +
        (r.kayma_min == null ? '—' : '+' + _sayi(r.kayma_min, 2) + ' … +' + _sayi(r.kayma_max, 2)) + '</td><td>' +
        (r.siralama_degisti == null ? '—' : r.siralama_degisti + '/' + r.kosul) + '</td><td>' + (r.not || '') + '</td></tr>').join('');

    const ozet = document.getElementById('dogrulamaOzet');
    if (ozet) ozet.textContent = 'Isınma ' + (dg.isinma_dk || 90) + ' dk · ' + (dg.isinma_yontemi || '');
    const not = document.getElementById('dogrulamaNot');
    if (not) {
        const sol = dg.solomon || {}, tio = dg.tur_ici_optimallik || {};
        not.innerHTML = 'Welch: WIP hareketli ortalaması ±%1 bandına ≈90 dk\'da girer; katı ölçütle (60 dk kesintisiz ±%2) kalıcı giriş daha geçtir (noktalı çizgiler). ' +
            'Göstergeler ısınma dönemini içerir; 480 dk\'da duruş ort. 1,15 puan düşük, WIP %5–37 yüksek görünür, göreli sonuçlar değişmez (K99). ' +
            'Rotalama: tur içi sıralama tam numaralamaya göre ort. %' + _sayi(tio.nn2opt_sapma_ort, 2) + ' sapma (' + (tio.orneklem || '—') + ' örnek); ' +
            'Solomon kıyaslamasında OR-Tools\'a göre %' + _sayi(sol.nn2opt_ed_ort, 1) + ' geride (' + (sol.ornek_sayisi || '—') + ' örnek).';
    }

    const w = dg.welch || [];
    const cvW = document.getElementById('chartWelch');
    if (cvW && w.length) {
        const konfigler = [...new Set(w.map(r => r.konfig))];
        const renkler = ['#2a78d6', '#1baf7a', '#d6612a'];
        const setler = konfigler.map((k, i) => ({
            label: k, data: w.filter(r => r.konfig === k).map(r => ({ x: r.dakika, y: r.wip_ma })),
            borderColor: renkler[i % 3], backgroundColor: renkler[i % 3], pointRadius: 0, borderWidth: 1.8, showLine: true
        }));
        konfigler.forEach((k, i) => {
            const r = w.find(x => x.konfig === k);
            setler.push({ label: '', data: [{ x: r.kararli_dk, y: 0 }, { x: r.kararli_dk, y: 1000 }], borderColor: renkler[i % 3],
                borderDash: [4, 4], borderWidth: 1, pointRadius: 0, showLine: true });
        });
        setler.push({ label: 'Isınma 90 dk', data: [{ x: 90, y: 0 }, { x: 90, y: 1000 }], borderColor: '#0F172A', borderWidth: 1.5, pointRadius: 0, showLine: true });
        if (window.chartInstances.welch) window.chartInstances.welch.destroy();
        const yUst = 1.08 * Math.max(...w.map(r => r.wip_ma));
        window.chartInstances.welch = new Chart(cvW.getContext('2d'), {
            type: 'scatter', data: { datasets: setler },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                plugins: { legend: { labels: { color: '#475569', font: { family: 'Outfit', size: 10 }, filter: i => !!i.text } } },
                scales: {
                    x: { min: 0, max: 600, title: { display: true, text: 'Dakika', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } },
                    y: { min: 0, max: yUst, title: { display: true, text: 'WIP hareketli ortalaması (adet)', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } }
                }
            }
        });
    }

    const rs = dg.replikasyon_seri || [];
    const cvR = document.getElementById('chartReplikasyon');
    if (cvR && rs.length) {
        // kümülatif ortalama ve %95 GA yarı genişliği (t yaklaşımı yerine 1,96)
        const ort = [], ga = [];
        let top = 0, top2 = 0;
        rs.forEach((r, i) => {
            top += r.starv_pct; top2 += r.starv_pct * r.starv_pct;
            const n = i + 1, m = top / n;
            const sd = n > 1 ? Math.sqrt(Math.max(0, (top2 - n * m * m) / (n - 1))) : 0;
            ort.push({ x: n, y: m }); ga.push({ x: n, y: n > 1 ? 1.96 * sd / Math.sqrt(n) : null });
        });
        if (window.chartInstances.replikasyon) window.chartInstances.replikasyon.destroy();
        window.chartInstances.replikasyon = new Chart(cvR.getContext('2d'), {
            type: 'scatter',
            data: { datasets: [
                { label: 'Kümülatif ortalama duruş %', data: ort, borderColor: '#2a78d6', backgroundColor: '#2a78d6', showLine: true, pointRadius: 0, borderWidth: 2 },
                { label: '%95 GA yarı genişliği', data: ga, borderColor: '#d6612a', backgroundColor: '#d6612a', showLine: true, pointRadius: 0, borderWidth: 1.5, borderDash: [5, 3] },
                { label: 'Mutlak eşik 0,05 puan', data: [{ x: 1, y: 0.05 }, { x: rs.length, y: 0.05 }], borderColor: '#94A3B8', showLine: true, pointRadius: 0, borderWidth: 1 }
            ] },
            options: {
                responsive: true, maintainAspectRatio: false, animation: false,
                plugins: { legend: { labels: { color: '#475569', font: { family: 'Outfit', size: 10 } } } },
                scales: {
                    x: { min: 1, max: rs.length, title: { display: true, text: 'Replikasyon sayısı', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } },
                    y: { min: 0, title: { display: true, text: 'Duruş (%)', color: '#64748B' }, grid: { color: 'rgba(0,0,0,0.05)' } }
                }
            }
        });
    }

    _karsilastiriciKur('karsA', { arac: 3, alpha: 0.15, talep: 0, kural: 'EDD', mod: 'Dinamik_N' });
    _karsilastiriciKur('karsB', { arac: 3, alpha: 0.15, talep: 0, kural: 'EDD', mod: 'Sabit_N' });
    renderKarsilastirici();
}

function _karsilastiriciKur(kapId, v) {
    const kap = document.getElementById(kapId);
    if (!kap) return;
    const ek = kapId.slice(-1);
    const sec = (ad, degerler, etiket, varsayilan) => '<label for="' + kapId + ad + '">' + (ad === 'Arac' ? ek + ' · Filo' : ad === 'Alpha' ? 'α' : ad === 'Talep' ? 'Talep' : ad === 'Kural' ? 'Sevk' : 'Boyutlandırma') +
        '</label><select id="' + kapId + ad + '">' + degerler.map(x => '<option value="' + x + '"' + (String(x) === String(varsayilan) ? ' selected' : '') + '>' + etiket(x) + '</option>').join('') + '</select>';
    kap.innerHTML =
        sec('Arac', [1, 2, 3, 4, 5, 6, 7, 8], x => x + ' araç', v.arac) +
        sec('Alpha', [0.05, 0.10, 0.15, 0.20, 0.25, 0.30], x => x.toFixed(2), v.alpha) +
        sec('Talep', TALEP_DUZEYLERI, x => TALEP_ETIKET[x], v.talep) +
        sec('Kural', ['EDD', 'SLACK', 'FIFO', 'KRITIKLIK'], x => x, v.kural) +
        sec('Mod', ['Dinamik_N', 'Sabit_N'], x => x === 'Dinamik_N' ? 'VDI' : 'V1', v.mod);
    kap.querySelectorAll('select').forEach(el => el.addEventListener('change', renderKarsilastirici));
}

function _karsSenaryo(kapId) {
    const g = ad => document.getElementById(kapId + ad).value;
    return scenariosData.find(s => s.arac_sayisi === parseInt(g('Arac'), 10) && Math.abs(s.alpha - parseFloat(g('Alpha'))) < 0.01 &&
        s.talep_sok_pct === parseInt(g('Talep'), 10) && s.dispatch_kural === g('Kural') && s.n_modu === g('Mod'));
}

function renderKarsilastirici() {
    const tb = document.getElementById('karsTablo');
    if (!tb || !document.getElementById('karsAArac')) return;
    const A = _karsSenaryo('karsA'), B = _karsSenaryo('karsB');
    if (!A || !B) { tb.innerHTML = '<tr><td colspan="4">Bu konfigürasyon veri ambarında yok.</td></tr>'; return; }
    const gostergeler = [
        ['Duruş (%)', 'starv_pct', 2], ['Ortalama WIP (adet)', 'ort_wip', 0], ['Kart sayısı', 'toplam_kart', 0],
        ['Sefer', 'sefer_sayisi', 1], ['Mesafe (km)', 'mesafe_km', 1], ['Araç doluluğu (%)', 'doluluk_pct', 1], ['Araç kullanımı (%)', 'arac_kullanim_pct', 1]
    ];
    tb.innerHTML = gostergeler.map(([ad, k, b]) => {
        const fark = (B[k] != null && A[k] != null) ? B[k] - A[k] : null;
        let ek = '';
        if (k === 'starv_pct' && fark != null) {
            const ga = Math.hypot(A.starv_ci95 || 0, B.starv_ci95 || 0);
            ek = Math.abs(fark) <= ga ? ' <span class="katki-ga">(anlamlı değil, ± ' + ga.toFixed(2) + ')</span>' : ' <span class="katki-ga">(± ' + ga.toFixed(2) + ')</span>';
        }
        const ab = (x, s) => _sayi(x[k], b) + (k === 'starv_pct' ? ' <span class="katki-ga">± ' + _sayi(x.starv_ci95, 2) + '</span>' : '');
        return '<tr><td><strong>' + ad + '</strong></td><td>' + ab(A) + '</td><td>' + ab(B) + '</td><td>' +
            (fark == null ? '—' : (fark >= 0 ? '+' : '') + fark.toFixed(b)) + ek + '</td></tr>';
    }).join('');
}
