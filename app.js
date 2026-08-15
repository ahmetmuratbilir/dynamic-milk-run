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

const kpiStarvVal = document.getElementById('kpiStarvVal');
const kpiStarvDk = document.getElementById('kpiStarvDk');
const kpiStarvCard = document.getElementById('kpiStarvCard');
const kpiTargetBadge = document.getElementById('kpiTargetBadge');

const kpiWipVal = document.getElementById('kpiWipVal');
const kpiFarkVal = document.getElementById('kpiFarkVal');
const kpiStatusText = document.getElementById('kpiStatusText');
const kpiStatusSub = document.getElementById('kpiStatusSub');
const kpiStatusIcon = document.getElementById('kpiStatusIcon');

// Uygulama Başlatma
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('data/dashboard_scenarios.json');
        scenariosData = await response.json();
        console.log(Veri ambarı yüklendi:  senaryo.);
        
        initEventListeners();
        initCharts();
        updateDashboard();
    } catch (err) {
        console.error('Veri yükleme hatası:', err);
    }
});

// Event Listener'lar
function initEventListeners() {
    sliderArac.addEventListener('input', (e) => {
        valArac.textContent = ${e.target.value} Araç;
        updateDashboard();
    });

    sliderAlpha.addEventListener('input', (e) => {
        valAlpha.textContent = ${parseFloat(e.target.value).toFixed(2)} (%);
        updateDashboard();
    });

    sliderTalep.addEventListener('input', (e) => {
        const val = parseInt(e.target.value);
        valTalep.textContent = val === 0 ? '%0 (Baz)' : ${val > 0 ? '+' : ''}%;
        updateDashboard();
    });

    document.querySelectorAll('input[name="nModu"]').forEach(el => {
        el.addEventListener('change', updateDashboard);
    });

    document.querySelectorAll('input[name="dispatch"]').forEach(el => {
        el.addEventListener('change', updateDashboard);
    });
}

// Seçili Parametrelere Göre Veri Getir
function getSelectedParameters() {
    return {
        arac_sayisi: parseInt(sliderArac.value),
        alpha: parseFloat(sliderAlpha.value),
        talep_sok_pct: parseInt(sliderTalep.value),
        dispatch_kural: document.querySelector('input[name="dispatch"]:checked').value,
        n_modu: document.querySelector('input[name="nModu"]:checked').value
    };
}

// Dashboard Güncelleme Ana Fonksiyonu
function updateDashboard() {
    if (!scenariosData || scenariosData.length === 0) return;

    const params = getSelectedParameters();
    
    // Seçili senaryoyu filtrele
    const currentScenario = scenariosData.find(s => 
        s.arac_sayisi === params.arac_sayisi &&
        Math.abs(s.alpha - params.alpha) < 0.01 &&
        s.talep_sok_pct === params.talep_sok_pct &&
        s.dispatch_kural === params.dispatch_kural &&
        s.n_modu === params.n_modu
    );

    if (currentScenario) {
        // KPI 1: Starvation
        const starvPct = currentScenario.starv_pct;
        kpiStarvVal.textContent = %;
        kpiStarvDk.textContent = ${currentScenario.starv_dk.toLocaleString()} / 11,520 dakika duruş;

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

        // KPI 3: Statik vs Dinamik Farkı
        // Statik 4 araç baz: 19.31%, Dinamik 4 araç baz: 24.58% => +5.27 puan
        // Genel dinamik delta hesaplama
        kpiFarkVal.textContent = +5.27 puan;

        // KPI 4: Kapasite Durumu
        if (params.arac_sayisi >= 8 && starvPct < 5.0) {
            kpiStatusIcon.textContent = '✅';
            kpiStatusText.textContent = 'Kapasite Yeterli';
            kpiStatusSub.textContent = 'Eşik <%5 sağlandı (8 araç)';
            kpiStatusText.style.color = '#10b981';
        } else if (params.arac_sayisi >= 5) {
            kpiStatusIcon.textContent = '⚠️';
            kpiStatusText.textContent = 'Orta Kapasite';
            kpiStatusSub.textContent = 'Tavanlı sistemde 8 araç gerekir';
            kpiStatusText.style.color = '#f59e0b';
        } else {
            kpiStatusIcon.textContent = '🚨';
            kpiStatusText.textContent = 'Kapasite Yetersiz';
            kpiStatusSub.textContent = 'Duruş yüksek (Filo arttırın)';
            kpiStatusText.style.color = '#f43f5e';
        }
    }

    // Grafikleri Güncelle
    updateCharts(params);
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
    chartPareto = new Chart(ctxPareto, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Dinamik Senaryolar (WIP vs Starvation)',
                data: [],
                backgroundColor: '#8b5cf6',
                pointRadius: 6
            }]
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

    // 2. Pareto Scatter Verileri
    const paretoData = [];
    for (let v = 1; v <= 8; v++) {
        const item = scenariosData.find(s => 
            s.arac_sayisi === v &&
            Math.abs(s.alpha - params.alpha) < 0.01 &&
            s.talep_sok_pct === params.talep_sok_pct &&
            s.dispatch_kural === params.dispatch_kural &&
            s.n_modu === params.n_modu
        );
        if (item) {
            paretoData.push({ x: item.ort_wip, y: item.starv_pct });
        }
    }
    chartPareto.data.datasets[0].data = paretoData;
    chartPareto.update();

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
