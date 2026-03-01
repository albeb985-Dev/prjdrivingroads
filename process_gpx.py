import gpxpy
import matplotlib.pyplot as plt
import reverse_geocoder as rg
import os

def run_analysis():
    # Cerca il primo file .gpx nella cartella
    gpx_files = [f for f in os.listdir('.') if f.endswith('.gpx')]
    if not gpx_files: return
    
    file_path = gpx_files[0]
    with open(file_path, 'r') as f:
        gpx = gpxpy.parse(f)

    altitudes = []
    lats_lons = []
    
    for track in gpx.tracks:
        for segment in track.segments:
            for p in segment.points:
                altitudes.append(p.elevation)
                lats_lons.append((p.latitude, p.longitude))

    # Calcoli
    max_alt = max(altitudes)
    min_alt = min(altitudes)
    
    # Geolocalizzazione (Stato e Regione)
    res = rg.search([lats_lons[0], lats_lons[len(lats_lons)//2]])
    regione = res[0]['admin1']
    stato = res[0]['cc']

    # Creazione Grafico
    plt.figure(figsize=(8, 4))
    plt.plot(altitudes, color='blue')
    plt.fill_between(range(len(altitudes)), altitudes, color='skyblue', alpha=0.3)
    graph_name = "grafico_altitudine.png"
    plt.savefig(graph_name)

    # Composizione URL (Esempio GitHub Pages)
    user = "albeb985-Dev"
    repo = "prjdrivingroads"
    gpx_url = f"https://github.com/{user}/{repo}/blob/main/{file_path}"
    img_url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{graph_name}"

    # Salva report finale
    with open("report.txt", "w") as r:
        r.write(f"Max: {max_alt}m\nMin: {min_alt}m\nStato: {stato}\nRegione: {regione}\nGPX: {gpx_url}\nIMG: {img_url}")

if __name__ == "__main__":
    run_analysis()
