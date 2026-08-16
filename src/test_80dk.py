import json
import os

def build():
    with open('data/dashboard_scenarios.json', 'r', encoding='utf-8') as f:
        scenarios_json = f.read()

    with open('style.css', 'r', encoding='utf-8') as f:
        css_content = f.read()

    with open('index.html', 'r', encoding='utf-8') as f:
        html_template = f.read()

    with open('app.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Replace fetch call in app.js with embedded data
    js_embedded = js_content.replace(
        'let scenariosData = [];',
        'let scenariosData = ' + scenarios_json + ';'
    )

    fetch_block = """document.addEventListener('DOMContentLoaded', async () => {
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
});"""

    standalone_init = """document.addEventListener('DOMContentLoaded', () => {
    console.log('Gömülü Veri Ambarı Yüklendi: ' + scenariosData.length + ' senaryo.');
    initEventListeners();
    initCharts();
    renderStations();
    updateDashboard();
});"""

    js_embedded = js_embedded.replace(fetch_block, standalone_init)

    # Save embedded JS separately for node --check validation
    with open('embedded_script.js', 'w', encoding='utf-8') as f:
        f.write(js_embedded)

    # Combine into dashboard.html
    clean_html = html_template.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + css_content + '\n</style>')
    clean_html = clean_html.replace('<script src="app.js"></script>', '<script>\n' + js_embedded + '\n</script>')

    if 'id="stationsGrid"' not in clean_html:
        sec5 = """
                <div class="chart-card glass-card full-width">
                    <div class="chart-header">
                        <h3>Bölüm 5 — 24 İstasyon Bazlı Stok ve ROP Durum Takibi</h3>
                        <span class="chart-subtitle">🟢 Stok > ROP | 🟡 Stok &le; ROP (Sinyal) | 🔴 Kritik Stok | <strong style="color:var(--accent-rose);">S16 En Kırılgan İstasyon</strong></span>
                    </div>
                    <div class="stations-grid" id="stationsGrid">
                    </div>
                </div>
        """
        clean_html = clean_html.replace('<div class="table-card glass-card">', sec5 + '\n<div class="table-card glass-card">')

    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(clean_html)

    print(f"dashboard.html ve embedded_script.js basariyla uretildi. Boyut: {os.path.getsize('dashboard.html')} bytes")

if __name__ == '__main__':
    build()

