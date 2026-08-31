/**
 * app.js - Dinamik Milk-Run & E-Kanban Karar Destek Dashboard Mantığı
 * ==================================================================
 * 1.920 Senaryoluk Çevrimdışı Veri Ambarını (data/dashboard_scenarios.json) Okur
 * 5 Sekmeli Mimari (Özet, What-If, İstasyon Haritası, Karşılaştırma, Veri Girişi)
 */

// ===== GLOBAL DEĞİŞKENLER VE GRAFİK NESNELERİ =====
let scenariosData = [];
window.chartInstances = {
    fleet: null,
    pareto: null,
    alpha: null
};

// Gerçek Fabrika İstasyon Verileri (stations.csv)
const STATIONS_DATA = [
    { id: 'S1', hat: 'Hat-1', d_saat: 22, c: 20, n: 1 },
    { id: 'S2', hat: 'Hat-1', d_saat: 18, c: 20, n: 1 },
    { id: 'S3', hat: 'Hat-1', d_saat: 15, c: 15, n: 1 },
    { id: 'S4', hat: 'Hat-1', d_saat: 20, c: 20, n: 1 },
    { id: 'S5', hat: 'Hat-1', d_saat: 12, c: 15, n: 1 },
    { id: 'S6', hat: 'Hat-1', d_saat: 17, c: 20, n: 1 },
    { id: 'S7', hat: 'Hat-2', d_saat: 21, c: 20, n: 1 },
    { id: 'S8', hat: 'Hat-2', d_saat: 13, c: 15, n: 1 },
    { id: 'S9', hat: 'Hat-2', d_saat: 19, c: 20, n: 1 },
    { id: 'S10', hat: 'Hat-2', d_saat: 11, c: 15, n: 1 },
    { id: 'S11', hat: 'Hat-2', d_saat: 16, c: 20, n: 1 },
    { id: 'S12', hat: 'Hat-2', d_saat: 14, c: 15, n: 1 },
    { id: 'S13', hat: 'Hat-3', d_saat: 23, c: 20, n: 1 },
    { id: 'S14', hat: 'Hat-3', d_saat: 18, c: 20, n: 1 },
    { id: 'S15', hat: 'Hat-3', d_saat: 15, c: 15, n: 1 },
    { id: 'S16', hat: 'Hat-3', d_saat: 24, c: 20, n: 2, fragile: true },
    { id: 'S17', hat: 'Hat-3', d_saat: 17, c: 20, n: 1 },
    { id: 'S18', hat: 'Hat-3', d_saat: 14, c: 15, n: 1 },
    { id: 'S19', hat: 'Hat-4', d_saat: 20, c: 20, n: 1 },
    { id: 'S20', hat: 'Hat-4', d_saat: 16, c: 20, n: 1 },
    { id: 'S21', hat: 'Hat-4', d_saat: 13, c: 15, n: 1 },
    { id: 'S22', hat: 'Hat-4', d_saat: 18, c: 20, n: 1 },
    { id: 'S23', hat: 'Hat-4', d_saat: 12, c: 15, n: 1 },
    { id: 'S24', hat: 'Hat-4', d_saat: 21, c: 20, n: 1 }
];

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
        
        initOzetCharts();
        updateOzetView();
    } catch (err) {
        console.error('Veri yükleme hatası:', err);
    }
});

// ===== SEKME 1 (ÖZET) GRAFİK BAŞLATMA =====
function initOzetCharts() {
    const canvasFleet = document.getElementById('chartFleet');
    if (!canvasFleet) return;

    const ctxFleet = canvasFleet.getContext('2d');
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

    // KPI 3: Statik vs Dinamik Farkı
    const staticBase = 19.31; // 4 Araç K58 statik baseline
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
