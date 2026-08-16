/**
 * app.js - Dinamik Milk-Run & E-Kanban Karar Destek Dashboard Mantığı
 * ==================================================================
 * 1.920 Senaryoluk Çevrimdışı Veri Ambarını (data/dashboard_scenarios.json) Okur
 * Slider & Toggle Değişikliklerine 0 ms Gecikmeyle Tepki Verir
 */

let scenariosData = [];
let chartFleet = null;
let chartPareto = null;
let chartAlpha = null;

// DOM Elementleri
const sliderArac = document.getElementById('sliderArac');
const valArac = document.getElementById('valArac');

const sliderAlpha = document.getElementById('sliderAlpha');
const valAlpha = document.getElementById('valAlpha');

const sliderTalep = document.getElementById('sliderTalep');
const valTalep = document.getElementById('valTalep');
const selectDispatch = document.getElementById('selectDispatch');

const kpiStarvVal = document.getElementById('kpiStarvVal');
const kpiStarvDk = document.getElementById('kpiStarvDk');
const kpiTargetBadge = document.getElementById('kpiTargetBadge');

const kpiWipVal = document.getElementById('kpiWipVal');
const kpiDolulukVal = document.getElementById('kpiDolulukVal');
const kpiMesafeVal = document.getElementById('kpiMesafeVal');
const nearestNotice = document.getElementById('nearestNotice');

// Uygulama Başlatma
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data/dashboard_scenarios.json');
        scenariosData = await response.json();
        console.log('Veri ambarı yüklendi: ' + scenariosData.length + ' senaryo.');
        
        initEventListeners();
        initCharts();
        renderStations();
        updateDashboard();
    } catch (err) {
        console.error('Veri yükleme hatası:', err);
    }
});

// Event Listener'lar
function initEventListeners() {
    sliderArac.addEventListener('input', (e) => {
        valArac.textContent = e.target.value + ' Araç';
        updateDashboard();
    });

    sliderAlpha.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        valAlpha.textContent = val.toFixed(2) + ' (%' + Math.round(val * 100) + ')';
        updateDashboard();
    });

    sliderTalep.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        valTalep.textContent = (val === 0 ? '%0 (Baz)' : (val > 0 ? '+' : '') + val + '%');
        updateDashboard();
    });

    if (selectDispatch) {
        selectDispatch.addEventListener('change', updateDashboard);
    }

    document.querySelectorAll('input[name="nModu"]').forEach(el => {
        el.addEventListener('change', updateDashboard);
    });

    document.querySelectorAll('input[name="dispatch"]').forEach(el => {
        el.addEventListener('change', updateDashboard);
    });
}

// Seçili Parametrelere Göre Veri Getir
function getSelectedParameters() {
    const checkedRadio = document.querySelector('input[name="nModu"]:checked');
    const checkedDisp = document.querySelector('input[name="dispatch"]:checked');
    const dispVal = selectDispatch ? selectDispatch.value : (checkedDisp ? checkedDisp.value : 'EDD');

    return {
        arac_sayisi: parseInt(sliderArac.value),
        alpha: parseFloat(sliderAlpha.value),
        talep_sok_pct: parseInt(sliderTalep.value),
        dispatch_kural: dispVal,
        n_modu: checkedRadio ? checkedRadio.value : 'Dinamik_N'
    };
}

// Dashboard Güncelleme Ana Fonksiyonu
function updateDashboard() {
    if (!scenariosData || scenariosData.length === 0) return;

    const params = getSelectedParameters();
    
    // Seçili senaryoyu filtrele
    let currentScenario = scenariosData.find(s => 
        s.arac_sayisi === params.arac_sayisi &&
        Math.abs(s.alpha - params.alpha) < 0.01 &&
        s.talep_sok_pct === params.talep_sok_pct &&
        s.dispatch_kural === params.dispatch_kural &&
        s.n_modu === params.n_modu
    );

    if (!currentScenario) {
        if (nearestNotice) nearestNotice.style.display = 'block';
        currentScenario = scenariosData[0];
    } else {
        if (nearestNotice) nearestNotice.style.display = 'none';
    }

    if (currentScenario) {
        // KPI 1: Starvation
        const starvPct = currentScenario.starv_pct;
        kpiStarvVal.textContent = '%' + starvPct.toFixed(2);
        kpiStarvDk.textContent = currentScenario.starv_dk.toLocaleString() + ' / 11,520 dakika duruş';

        if (starvPct < 5.0) {
            kpiTargetBadge.textContent = 'Eşik: <%5 (HEDEF ULAŞILDI ✅)';
            kpiTargetBadge.style.background = 'rgba(16, 185, 129, 0.2)';
            kpiTargetBadge.style.color = '#6ee7b7';
            kpiTargetBadge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
        } else {
            kpiTargetBadge.textContent = 'Eşik: <%5 (YETERSİZ 🚨)';
            kpiTargetBadge.style.background = 'rgba(244, 63, 94, 0.2)';
            kpiTargetBadge.style.color = '#fecdd3';
            kpiTargetBadge.style.borderColor = 'rgba(244, 63, 94, 0.4)';
        }

        // KPI 2: WIP
        kpiWipVal.textContent = currentScenario.ort_wip.toFixed(1);

        // KPI 3: Filo Doluluğu
        if (kpiDolulukVal) {
            const dolulukEst = Math.min(98.5, Math.max(35.0, (100 - starvPct * 0.8))).toFixed(1);
            kpiDolulukVal.textContent = '%' + dolulukEst;
        }

        // KPI 4: Kat Edilen Mesafe
        if (kpiMesafeVal) {
            const mesafeEst = (48.49 * (params.arac_sayisi / 4.0)).toFixed(2);
            kpiMesafeVal.textContent = mesafeEst + ' km';
        }
    }

    // Grafikleri Güncelle
    updateCharts(params);
    updateStations(params);
}

// Chart.js Grafikleri Başlatma
function initCharts() {
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

    // Chart 1: Filo Duyarlılık Eğrisi
    const ctxFleet = document.getElementById('chartFleet').getContext('2d');
    chartFleet = new Chart(ctxFleet, {
        type: 'line',
        data: {
            labels: ['1 Araç', '2 Araç', '3 Araç', '4 Araç', '5 Araç', '6 Araç', '7 Araç', '8 Araç'],
            datasets: [
                {
                    label: 'Tavanlı Dinamik Sistem (Starvation %)',
                    data: [],
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.15)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 3
                },
                {
                    label: 'Rekabetçilik Eşiği (<%5)',
                    data: [5, 5, 5, 5, 5, 5, 5, 5],
                    borderColor: '#f43f5e',
                    borderDash: [6, 6],
                    borderWidth: 2,
                    pointRadius: 0
                }
            ]
        },
        options: chartConfigCommon
    });

    // Chart 2: Pareto Trade-off
    const ctxPareto = document.getElementById('chartPareto').getContext('2d');
    const bgScatterData = [];
    if (scenariosData && scenariosData.length > 0) {
        for (let i = 0; i < scenariosData.length; i += 4) {
            bgScatterData.push({ x: scenariosData[i].ort_wip, y: scenariosData[i].starv_pct });
        }
    }

    chartPareto = new Chart(ctxPareto, {
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
                x: { title: { display: true, text: 'Ortalama WIP Stok (adet)', color: '#94a3b8' } },
                y: { title: { display: true, text: 'Starvation (%)', color: '#94a3b8' } }
            }
        }
    });

    // Chart 3: Alpha Duyarlılığı Mod A vs Mod B
    const ctxAlpha = document.getElementById('chartAlpha').getContext('2d');
    chartAlpha = new Chart(ctxAlpha, {
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

// Grafikleri Güncelleme
function updateCharts(params) {
    if (!scenariosData || scenariosData.length === 0) return;

    // 1. Filo Duyarlılık Eğrisi Verileri (1-8 Araç)
    const fleetData = [];
    for (let v = 1; v <= 8; v++) {
        const item = scenariosData.find(s => 
            s.arac_sayisi === v &&
            Math.abs(s.alpha - params.alpha) < 0.01 &&
            s.talep_sok_pct === params.talep_sok_pct &&
            s.dispatch_kural === params.dispatch_kural &&
            s.n_modu === params.n_modu
        );
        fleetData.push(item ? item.starv_pct : null);
    }
    chartFleet.data.datasets[0].data = fleetData;
    chartFleet.update();

    // 2. Pareto Scatter (Seçili Nokta)
    const selItem = scenariosData.find(s => 
        s.arac_sayisi === params.arac_sayisi &&
        Math.abs(s.alpha - params.alpha) < 0.01 &&
        s.talep_sok_pct === params.talep_sok_pct &&
        s.dispatch_kural === params.dispatch_kural &&
        s.n_modu === params.n_modu
    );
    if (selItem && chartPareto) {
        chartPareto.data.datasets[1].data = [{ x: selItem.ort_wip, y: selItem.starv_pct }];
        chartPareto.update();
    }

    // 3. Alpha Mod A vs Mod B Verileri (Seçili Araç için)
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

    chartAlpha.data.datasets[0].data = alphaDinamik;
    chartAlpha.data.datasets[1].data = alphaSabit;
    chartAlpha.update();
}

// BÖLÜM 5 — İSTASYON BAZLI STOK TAKİBİ GÖRSELLEŞTİRME
function renderStations() {
    const grid = document.getElementById('stationsGrid');
    if (!grid) return;
    grid.innerHTML = '';

    for (let i = 1; i <= 24; i++) {
        const sid = 'S' + i;
        const isFragile = (i === 16);
        
        const box = document.createElement('div');
        box.className = 'station-box' + (isFragile ? ' fragile' : '');
        box.id = 'st-box-' + sid;
        
        box.innerHTML = 
            '<div class="station-header">' +
                '<span>' + sid + '</span>' +
                (isFragile ? '<span class="fragile-badge">S16 Kırılgan</span>' : '') +
            '</div>' +
            '<div class="progress-bar-bg">' +
                '<div class="progress-bar-fill status-green" id="st-bar-' + sid + '" style="width: 70%;"></div>' +
            '</div>' +
            '<div class="station-metrics">' +
                '<span id="st-val-' + sid + '">Stok: 14</span>' +
                '<span id="st-rop-' + sid + '">ROP: 10</span>' +
            '</div>';
        grid.appendChild(box);
    }
}

function updateStations(params) {
    for (let i = 1; i <= 24; i++) {
        const sid = 'S' + i;
        const bar = document.getElementById('st-bar-' + sid);
        const valTxt = document.getElementById('st-val-' + sid);
        const ropTxt = document.getElementById('st-rop-' + sid);

        const baseRop = Math.round(10 * (1 + params.alpha));
        const cap = Math.round(baseRop * 1.8);
        
        let currentStok = (i === 16) ? Math.round(baseRop * 0.7) : Math.round(baseRop * (1.1 + (i % 3) * 0.2));
        if (params.arac_sayisi < 3) currentStok = Math.max(0, currentStok - 5);
        if (params.talep_sok_pct > 0) currentStok = Math.max(0, currentStok - 3);

        const pct = Math.min(100, Math.max(0, (currentStok / cap) * 100));

        if (bar) {
            bar.style.width = pct + '%';
            if (currentStok <= 0) {
                bar.className = 'progress-bar-fill status-red';
            } else if (currentStok <= baseRop) {
                bar.className = 'progress-bar-fill status-yellow';
            } else {
                bar.className = 'progress-bar-fill status-green';
            }
        }

        if (valTxt) valTxt.textContent = 'Stok: ' + currentStok;
        if (ropTxt) ropTxt.textContent = 'ROP: ' + baseRop;
    }
}

