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
    
    df['distance'] = np.sqrt(
        (df['latitude'].diff()**2) + 
        (df['longitude'].diff()**2)
    ).fillna(0)
    df['duree'] = df['time'].diff().dt.total_seconds().fillna(0)
    df['vitesse'] = df['distance'] / df['duree'].replace(0, np.nan)
    
    analyse = {
        'distance_totale_km': df['distance'].sum() * 111,  # approx conversion deg -> km
        'denivele_total_m': df['elevation'].diff().abs().sum(),
        'vitesse_moyenne_kmh': df['vitesse'].mean() * 3.6,
        'point_max_elevation_m': df['elevation'].max(),
        'point_min_elevation_m': df['elevation'].min()
    }
    return analyse

# --- Fonction de génération du plan d'entraînement ---
def generer_plan(distance, denivele):
    """
    Génère un plan simple 8 semaines selon la distance et D+ du GPX.
    """
    base_semaine = distance / 5  # km de base pour chaque séance
    denivele_factor = 1 + (denivele / 1000)  # ajuste selon le D+
    
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
        st.write(f"Dénivelé total : {analyse['denivele_total_m']:.0f} m")
        st.write(f"Vitesse moyenne : {analyse['vitesse_moyenne_kmh']:.2f} km/h")
        st.write(f"Altitude max : {analyse['point_max_elevation_m']:.0f} m")
        st.write(f"Altitude min : {analyse['point_min_elevation_m']:.0f} m")
        
        st.subheader("🏃 Plan d'entraînement 8 semaines")
        plan_df = generer_plan(analyse['distance_totale_km'], analyse['denivele_total_m'])
        st.dataframe(plan_df)
        
    else:
        st.error("Impossible d'analyser le fichier GPX.")