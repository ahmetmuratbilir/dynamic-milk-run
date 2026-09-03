import json

with open('data/dashboard_scenarios.json', 'r', encoding='utf-8') as f:
    scenarios_json = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html_template = f.read()

with open('style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# JS içindeki fetch kısmını SCENARIOS_DATA doğrudan gömülü olacak şekilde değiştir
js_standalone = js_content.replace(
    "let scenariosData = [];", 
    "let scenariosData = " + scenarios_json + ";"
)

js_standalone = js_standalone.replace(
    "document.addEventListener('DOMContentLoaded', async () => {\n    try {\n        const response = await fetch('data/dashboard_scenarios.json');\n        scenariosData = await response.json();\n        console.log(Veri ambarı yüklendi:  senaryo.);\n        \n        initEventListeners();\n        initCharts();\n        updateDashboard();\n    } catch (err) {\n        console.error('Veri yükleme hatası:', err);\n    }\n});",
    "document.addEventListener('DOMContentLoaded', () => {\n        console.log(Gömülü Veri Ambarı Yüklendi:  senaryo.);\n        initEventListeners();\n        initCharts();\n        renderStations();\n        updateDashboard();\n});"
)

# Station render script desteği ekle
station_js = """
function renderStations() {
    const grid = document.getElementById('stationsGrid');
    if (!grid) return;
    grid.innerHTML = '';

    for (let i = 1; i <= 24; i++) {
        const sid = S;
        const isFragile = (i === 16);
        
        const box = document.createElement('div');
        box.className = station-box ;
        box.id = st-box-;
        
        box.innerHTML = 
            <div class="station-header">
                <span></span>
                
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill status-green" id="st-bar-" style="width: 70%;"></div>
            </div>
            <div class="station-metrics">
                <span id="st-val-">Stok: 14</span>
                <span id="st-rop-">ROP: 10</span>
            </div>
        ;
        grid.appendChild(box);
    }
}

function updateStations(params) {
    for (let i = 1; i <= 24; i++) {
        const sid = S;
        const bar = document.getElementById(st-bar-);
        const valTxt = document.getElementById(st-val-);
        const ropTxt = document.getElementById(st-rop-);

        const baseRop = Math.round(10 * (1 + params.alpha));
        const cap = Math.round(baseRop * 1.8);
        
        let currentStok = i === 16 ? Math.round(baseRop * 0.7) : Math.round(baseRop * (1.1 + (i % 3) * 0.2));
        if (params.arac_sayisi < 3) currentStok = Math.max(0, currentStok - 5);
        if (params.talep_sok_pct > 0) currentStok = Math.max(0, currentStok - 3);

        const pct = Math.min(100, Math.max(0, (currentStok / cap) * 100));

        if (bar) {
            bar.style.width = ${pct}%;
            if (currentStok <= 0) {
                bar.className = 'progress-bar-fill status-red';
            } else if (currentStok <= baseRop) {
                bar.className = 'progress-bar-fill status-yellow';
            } else {
                bar.className = 'progress-bar-fill status-green';
            }
        }

        if (valTxt) valTxt.textContent = Stok: ;
        if (ropTxt) ropTxt.textContent = ROP: ;
    }
}
"""

js_standalone += "\n" + station_js
js_standalone = js_standalone.replace("updateCharts(params);", "updateCharts(params);\n    updateStations(params);")

# HTML'e CSS ve JS göm
full_html = html_template.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + css_content + '\n</style>')
full_html = full_html.replace('<script src="app.js"></script>', '<script>\n' + js_standalone + '\n</script>')

# 24 İstasyon görünümünü ekle
section5_html = """
                <div class="chart-card glass-card full-width">
                    <div class="chart-header">
                        <h3>Bölüm 5 — 24 İstasyon Bazlı Stok ve ROP Durum Takibi</h3>
                        <span class="chart-subtitle">🟢 Stok > ROP | 🟡 Stok &le; ROP (Sinyal) | 🔴 Kritik Stok | <strong style="color:var(--accent-rose);">S16 En Kırılgan İstasyon</strong></span>
                    </div>
                    <div class="stations-grid" id="stationsGrid">
                    </div>
                </div>
"""

full_html = full_html.replace('<div class="table-card glass-card">', section5_html + '\n<div class="table-card glass-card">')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("dashboard.html basariyla uretildi.")
