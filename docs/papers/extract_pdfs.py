import fitz  # pymupdf
import os
import re

# Tüm PDF dosyalarının tam yolları
papers_root = r"C:\Users\ahmet murat bilir\Desktop\dynamic-milk-run\docs\papers"

pdf_files = []
for root, dirs, files in os.walk(papers_root):
    for f in files:
        if f.endswith(".pdf"):
            pdf_files.append(os.path.join(root, f))

# Mükerrer dosyaları isimle filtrele (sadece benzersiz isimler)
seen_names = set()
unique_pdfs = []
for p in pdf_files:
    name = os.path.basename(p)
    if name not in seen_names:
        seen_names.add(name)
        unique_pdfs.append(p)

print(f"Toplam benzersiz PDF sayisi: {len(unique_pdfs)}\n")

# Her PDF'den ilk 15 sayfa metnini çıkar
output_dir = r"C:\Users\ahmet murat bilir\Desktop\dynamic-milk-run\docs\papers\extracted_text"
os.makedirs(output_dir, exist_ok=True)

for pdf_path in unique_pdfs:
    name = os.path.basename(pdf_path).replace(".pdf", "")
    out_file = os.path.join(output_dir, name[:60] + ".txt")
    
    try:
        doc = fitz.open(pdf_path)
        text = ""
        max_pages = min(len(doc), 20)  # İlk 20 sayfa
        for i in range(max_pages):
            text += f"\n\n--- SAYFA {i+1} ---\n"
            text += doc[i].get_text()
        doc.close()
        
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"OK: {name[:60]}".encode("ascii", errors="replace").decode())
    except Exception as e:
        print(f"HATA: {name[:60]}".encode("ascii", errors="replace").decode())

print("\nTamamlandi!")
