import os
import glob
from pypdf import PdfReader
import re

files_zip1 = [
    r"Expert Systems - 2020 - Simić - Modelling material flow using the Milk run and Kanban systems in the automotive industry.pdf",
    r"Optimizing milk-run system and IT-based Kanban with artificial intelligence  an empirical study on multi-lines assembly shop floor.pdf",
    r"Simulation_Testing_of_the_E-Kanban_to_Increase_the.pdf",
    r"Supply_Chain_Efficiencies_Through_E-Kanban_A_Case_.pdf",
    r"Analysis of Parameters Influencing in-plant Milk Run Design for P.pdf"
]

files_zip2 = [
    r"Particle swarm optimization algorithm for design of an adaptive Kanban system based on optimization via simulation.pdf",
    r"In-plant_milk_run_decision_problems.pdf",
    r"IJSIMM19-2_513.pdf",
    r"text20-1_551.pdf",
    r"1-s2.0-S0360835215001187-main.pdf",
    r"1-s2.0-S0360835224002018-main.pdf",
    r"1-s2.0-S2405896318307894-main.pdf",
    r"1-s2.0-S2405896322018420-main.pdf",
    r"00207543.2020.pdf",
    r"aa-01-2019-0013.pdf",
    r"cirrelt-2010-04.pdf",
    r"logistics-06-00074.pdf"
]

paths = []
zip1_dir = r"C:\Users\ahmet murat bilir\Desktop\dynamic-milk-run\docs\papers\zip1\dynamic makaleleri"
zip2_dir = r"C:\Users\ahmet murat bilir\Desktop\dynamic-milk-run\docs\papers\zip2\dy makale2"

for f in files_zip1:
    p = os.path.join(zip1_dir, f)
    if os.path.exists(p):
        paths.append(p)

for f in files_zip2:
    p = os.path.join(zip2_dir, f)
    if os.path.exists(p):
        paths.append(p)
    else:
        # maybe it's in zip1?
        p2 = os.path.join(zip1_dir, f)
        if os.path.exists(p2):
            paths.append(p2)

# Keywords mapping
params = {
    "Hat sayısı": ["production line", "assembly line", "number of lines"],
    "İstasyon sayısı": ["station", "stop", "number of stations", "number of stops", "workstation"],
    "Araç sayısı": ["vehicle", "tow train", "tugger", "forklift", "number of vehicles"],
    "Araç kapasitesi": ["vehicle capacity", "train capacity", "boxes per vehicle"],
    "Simülasyon süresi": ["simulation time", "simulation run time", "warm-up period", "simulated time"],
    "Lead time": ["lead time", "replenishment time", "delivery time"],
    "Güvenlik katsayısı": ["safety factor", "alpha", "safety stock"],
    "Kanban kart sayısı": ["kanban cards", "number of kanbans", "kanban formula", "kanban size"],
    "Kutu kapasitesi": ["box capacity", "container capacity", "parts per box", "parts per container"],
    "Tüketim hızı": ["demand rate", "consumption rate", "usage rate", "parts per minute", "demand"],
    "Mesafe": ["distance", "meters", "length of route", "travel distance"],
    "Zaman penceresi": ["time window", "delivery window"],
    "Handling süresi": ["handling time", "loading time", "unloading time", "service time"],
    "Araç hızı": ["speed", "velocity", "m/s", "m/min", "km/h"]
}

out_md = []

for p in paths:
    filename = os.path.basename(p)
    out_md.append(f"---\n**[{filename}]**\n| Parametre | Değer | Sayfa |\n|-----------|-------|-------|")
    
    found_params = {k: "Belirtilmemiş" for k in params}
    pages_params = {k: "" for k in params}
    
    try:
        reader = PdfReader(p)
        for i, page in enumerate(reader.pages):
            text = page.extract_text().lower() if page.extract_text() else ""
            sentences = text.split('.')
            
            for k, keywords in params.items():
                if found_params[k] != "Belirtilmemiş":
                    continue
                for kw in keywords:
                    if kw in text:
                        # Extract the sentence
                        for s in sentences:
                            if kw in s:
                                # Look for a number in the sentence
                                nums = re.findall(r'\b\d+(?:\.\d+)?\b', s)
                                if nums:
                                    found_params[k] = nums[0] + " (tahmini)"
                                    pages_params[k] = f"s.{i+1}"
                                    break
                    if found_params[k] != "Belirtilmemiş":
                        break
    except Exception as e:
        print(f"Error reading {p}: {e}")
        
    for k in params:
        val = found_params[k]
        pg = pages_params[k] if val != "Belirtilmemiş" else "-"
        out_md.append(f"| {k} | {val} | {pg} |")
        
    out_md.append("**Notlar:** Otomatik script ile çıkarılmıştır, sayı değerleri tam cümleden çekilmiş olup doğruluğu kontrol gerektirir.\n---\n")

summary = "\n### Özet Karşılaştırma Tablosu\n| Parametre | Makale Sayısı (Bulunan) |\n|-----------|-------------------------|\n"
# Count found parameters across all
for k in params:
    summary += f"| {k} | - |\n"

out_md.append(summary)

with open(r"C:\Users\ahmet murat bilir\Desktop\dynamic-milk-run\docs\hafta1_makale_parametreleri.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out_md))

print("Done.")
