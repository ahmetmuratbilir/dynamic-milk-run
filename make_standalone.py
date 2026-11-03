"""
make_standalone.py — index.html + style.css + app.js + v2 veri ambarı → tek dosya dashboard.html

app.js veriyi `window.DASHBOARD_DATA_V2` varsa oradan, yoksa
data/dashboard_scenarios_v2.json'dan okur. Bu betik JSON'u bir <script> içinde
gömer; app.js'te metin değiştirme yapılmaz (eski sürümün backtick kaybı hatası
bu yüzden tekrarlanamaz — K94).

Kullanım:
    python -X utf8 make_standalone.py
"""

import json
import os

KOK = os.path.dirname(os.path.abspath(__file__))


def oku(ad):
    with open(os.path.join(KOK, ad), encoding="utf-8") as f:
        return f.read()


def main():
    html = oku("index.html")
    css = oku("style.css")
    js = oku("app.js")
    veri = json.loads(oku(os.path.join("data", "dashboard_scenarios_v2.json")))
    # </script> dizisi gömülü JSON'u erken kapatmasın
    veri_js = json.dumps(veri, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    css_etiket = '<link rel="stylesheet" href="style.css">'
    js_etiket = '<script src="app.js"></script>'
    assert html.count(css_etiket) == 1 and html.count(js_etiket) == 1

    html = html.replace(css_etiket, "<style>\n" + css + "\n</style>")
    html = html.replace(
        js_etiket,
        "<script>\nwindow.DASHBOARD_DATA_V2 = " + veri_js + ";\n</script>\n"
        "    <script>\n" + js + "\n</script>",
    )

    with open(os.path.join(KOK, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"dashboard.html yazıldı ({len(html.encode('utf-8')) / 1024:.0f} KB, "
          f"{veri['meta']['senaryo_sayisi']} senaryo)")


if __name__ == "__main__":
    main()
