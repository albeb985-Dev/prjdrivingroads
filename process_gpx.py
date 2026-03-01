import gpxpy
import matplotlib.pyplot as plt
import reverse_geocoder as rg
import os
from geopy.distance import geodesic

# --- CONFIGURAZIONE ---
USER = "albeb985-Dev"
REPO = "prjdrivingroads"
BASE_DIR = "Gpx"  # La cartella principale che contiene le sottocartelle
OUTPUT_DIR = "output_data" # Dove verranno salvati i grafici

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_file(file_path):
    with open(file_path, 'r') as f:
        try:
            gpx = gpxpy.parse(f)
        except:
            return None # Salta file corrotti

    altitudes = []
    points = []
    total_dist = 0
    prev_p = None

    for track in gpx.tracks:
        for segment in track.segments:
            for p in segment.points:
                altitudes.append(p.elevation)
                points.append((p.latitude, p.longitude))
                if prev_p:
                    total_dist += geodesic((prev_p.latitude, prev_p.longitude), (p.latitude, p.longitude)).kilometers
                prev_p = p

    if not altitudes: return None

    # Analisi Geografica (Stato/Regione)
    # Usiamo il primo punto del tracciato per la località
    res = rg.search([points[0]])[0]
    
    # Generazione Grafico
    plt.figure(figsize=(8, 4))
    plt.fill_between(range(len(altitudes)), altitudes, color='skyblue', alpha=0.4)
    plt.plot(altitudes, color='royalblue', lw=2)
    plt.title(f"Profilo: {os.path.basename(file_path)}")
    
    # Nome file univoco per il grafico (sostituiamo / con _)
    graph_filename = file_path.replace(os.sep, "_").replace(".gpx", ".png")
    graph_path = os.path.join(OUTPUT_DIR, graph_filename)
    plt.savefig(graph_path)
    plt.close()

    # Composizione URL (Definita)
    gpx_url = f"https://github.com/{USER}/{REPO}/blob/main/{file_path}"
    img_url = f"https://raw.githubusercontent.com/{USER}/{REPO}/main/{graph_path}"

    return {
        "file": file_path,
        "max_alt": max(altitudes),
        "min_alt": min(altitudes),
        "dist": round(total_dist, 2),
        "stato": res['cc'],
        "regione": res['admin1'],
        "gpx_url": gpx_url,
        "img_url": img_url
    }

# --- ESECUZIONE RICORSIVA ---
all_results = []
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.lower().endswith(".gpx"):
            full_path = os.path.join(root, file)
            print(f"Elaborazione: {full_path}...")
            data = process_file(full_path)
            if data:
                all_results.append(data)

# Salvataggio Report Finale in Markdown (scansionabile da GitHub)
with open("REPORT_FINALE.md", "w") as f:
    f.write("# Report Automazione GPX\n\n")
    for r in all_results:
        f.write(f"## File: {r['file']}\n")
        f.write(f"- **Distanza:** {r['dist']} km\n")
        f.write(f"- **Altitudine:** Max {r['max_alt']}m / Min {r['min_alt']}m\n")
        f.write(f"- **Località:** {r['regione']}, {r['stato']}\n")
        f.write(f"- [Scarica GPX]({r['gpx_url']})\n\n")
        f.write(f"![Grafico]({r['img_url']})\n")
        f.write("---\n")
