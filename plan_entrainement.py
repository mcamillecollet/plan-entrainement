import streamlit as st
import gpxpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    
    df['distance'] = np.sqrt((df['latitude'].diff()**2) + (df['longitude'].diff()**2)).fillna(0) * 111
    df['cum_distance'] = df['distance'].cumsum()
    df['elevation_diff'] = df['elevation'].diff().fillna(0)
    
    D_plus = df.loc[df['elevation_diff'] > 0, 'elevation_diff'].sum()
    
    cotes = []
    cote_distance = 0
    cote_elevation = 0
    
    for d, e, cum_d in zip(df['distance'], df['elevation_diff'], df['cum_distance']):
        if e > 0:
            cote_distance += d
            cote_elevation += e
        else:
            if cote_distance >= 1.0:
                pente = (cote_elevation / (cote_distance * 1000)) * 100
                cotes.append({'start_km': cum_d - cote_distance, 'end_km': cum_d, 'pente_pct': round(pente,1)})
            cote_distance = 0
            cote_elevation = 0

    if cote_distance >= 1.0:
        pente = (cote_elevation / (cote_distance * 1000)) * 100
        cotes.append({'start_km': cum_d - cote_distance, 'end_km': cum_d, 'pente_pct': round(pente,1)})
    
    analyse = {
        'distance_totale_km': df['cum_distance'].iloc[-1],
        'altitude_min_m': df['elevation'].min(),
        'altitude_max_m': df['elevation'].max(),
        'D_plus_m': D_plus,
        'df': df,
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
        
        # --- Graphique profil d'altitude ---
        df = analyse['df']
        fig, ax = plt.subplots(figsize=(10,4))

        # Ligne rouge
        ax.plot(df['cum_distance'], df['elevation'], color='red', linewidth=2)

        # Fond gris clair partout
        ax.set_facecolor('#d9d9d9')
        fig.patch.set_facecolor('#d9d9d9')

        # Police cohérente avec Streamlit
        font = {'family':'sans-serif','size':12}
        ax.set_xlabel("Distance (km)", fontdict=font)
        ax.set_ylabel("Altitude (m)", fontdict=font)
        ax.set_title("Profil d'altitude du parcours", fontdict={'family':'sans-serif','size':14,'weight':'bold'})

        # Quadrillage clair
        ax.grid(True, color='white', linestyle='--', linewidth=0.7, alpha=0.7)

        # Marquer les côtes >1 km
        for cote in analyse['cotes']:
            mid = (cote['start_km'] + cote['end_km']) / 2
            h = df.loc[(df['cum_distance']>=cote['start_km']) & (df['cum_distance']<=cote['end_km']), 'elevation'].max()
            ax.annotate(f"{cote['pente_pct']}%", xy=(mid, h), xytext=(0,10), textcoords='offset points',
                        ha='center', color='red', fontsize=10, fontweight='bold')
            ax.axvspan(cote['start_km'], cote['end_km'], color='red', alpha=0.1)

        st.pyplot(fig)
        
        st.subheader("🏃 Plan d'entraînement 8 semaines")
        plan_df = generer_plan(analyse['distance_totale_km'], analyse['D_plus_m'])
        st.dataframe(plan_df)
        
    else:
        st.error("Impossible d'analyser le fichier GPX.")