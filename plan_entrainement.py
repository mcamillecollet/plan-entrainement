import streamlit as st
import gpxpy
import pandas as pd
import numpy as np

# --- Fonction d'analyse GPX ---
def analyser_gpx(gpx_file):
    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time
                })
    df = pd.DataFrame(points)
    
    if df.empty:
        return None
    
    # Calcul distance entre points (approximation)
    df['distance'] = np.sqrt((df['latitude'].diff()**2) + (df['longitude'].diff()**2)).fillna(0) * 111  # km approx
    df['elevation_diff'] = df['elevation'].diff().fillna(0)
    
    # D+ total
    D_plus = df.loc[df['elevation_diff'] > 0, 'elevation_diff'].sum()
    
    # Identifier les côtes >1 km avec fusion si descente <1 km
    cotes = []
    cote_distance = 0
    cote_elevation = 0
    descente_courte = 0
    
    for d, e in zip(df['distance'], df['elevation_diff']):
        if e > 0:  # montée
            cote_distance += d + descente_courte  # ajouter descente courte précédente
            cote_elevation += e
            descente_courte = 0
        else:  # descente
            if cote_distance == 0:  # pas de côte en cours
                continue
            if d < 1.0:  # petite descente, on continue la côte
                descente_courte += d
            else:  # descente longue => clôturer côte si distance >1 km
                if cote_distance >= 1.0:
                    pente = (cote_elevation / (cote_distance * 1000)) * 100
                    cotes.append({'distance_km': round(cote_distance,2), 'pente_pct': round(pente,1)})
                cote_distance = 0
                cote_elevation = 0
                descente_courte = 0
    # dernière côte
    if cote_distance >= 1.0:
        pente = (cote_elevation / (cote_distance * 1000)) * 100
        cotes.append({'distance_km': round(cote_distance,2), 'pente_pct': round(pente,1)})
    
    analyse = {
        'distance_totale_km': df['distance'].sum(),
        'altitude_min_m': df['elevation'].min(),
        'altitude_max_m': df['elevation'].max(),
        'D_plus_m': D_plus,
        'cotes': cotes
    }
    
    return analyse

# --- Fonction de génération du plan d'entraînement ---
def generer_plan(distance, D_plus):
    base_semaine = distance / 5
    denivele_factor = 1 + (D_plus / 1000)
    
    plan = []
    for semaine in range(1, 9):
        plan.append({
            'Semaine': semaine,
            'Endurance': round(base_semaine * 2 * denivele_factor, 1),
            'Seuil': round(base_semaine * 1.2 * denivele_factor, 1),
            'Vitesse': round(base_semaine * 0.8 * denivele_factor, 1)
        })
    return pd.DataFrame(plan)

# --- Streamlit UI ---
st.title("Analyse GPX et Plan d'entraînement personnalisé")

uploaded_file = st.file_uploader("📁 Upload ton fichier GPX", type=['gpx'])

if uploaded_file is not None:
    analyse = analyser_gpx(uploaded_file)
    
    if analyse:
        st.subheader("📊 Analyse du parcours")
        st.write(f"Distance totale : {analyse['distance_totale_km']:.2f} km")
        st.write(f"Altitude min : {analyse['altitude_min_m']:.0f} m")
        st.write(f"Altitude max : {analyse['altitude_max_m']:.0f} m")
        st.write(f"D+ total : {analyse['D_plus_m']:.0f} m")
        
        if analyse['cotes']:
            st.write(f"Nombre de côtes > 1 km : {len(analyse['cotes'])}")
            for i, cote in enumerate(analyse['cotes'], 1):
                st.write(f"Côte {i} : {cote['distance_km']} km, pente {cote['pente_pct']} %")
        else:
            st.write("Pas de côte supérieure à 1 km détectée")
        
        st.subheader("🏃 Plan d'entraînement 8 semaines")
        plan_df = generer_plan(analyse['distance_totale_km'], analyse['D_plus_m'])
        st.dataframe(plan_df)
        
    else:
        st.error("Impossible d'analyser le fichier GPX.")