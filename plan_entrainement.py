import streamlit as st
import gpxpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

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
    
    distances = [0.0]
    for i in range(1, len(df)):
        d = gpxpy.geo.haversine_distance(
            df['latitude'].iloc[i-1], df['longitude'].iloc[i-1],
            df['latitude'].iloc[i], df['longitude'].iloc[i]
        ) / 1000  # mètres → km
        distances.append(d)
    df['distance'] = distances
    df['cum_distance'] = df['distance'].cumsum()
    df['elevation_diff'] = df['elevation'].diff().fillna(0)
    
    D_plus = df.loc[df['elevation_diff'] > 0, 'elevation_diff'].sum()
    
    # Identifier les côtes >0.5 km
    cotes = []
    cote_distance = 0
    cote_elevation = 0
    cum_d = 0
    for d, e, cum_d in zip(df['distance'], df['elevation_diff'], df['cum_distance']):
        if e > 0:
            cote_distance += d
            cote_elevation += e
        else:
            if cote_distance >= 0.5:
                pente = (cote_elevation / (cote_distance * 1000)) * 100
                cote_distance_start = cum_d - cote_distance
                cotes.append({
                    'start_km': cote_distance_start,
                    'end_km': cum_d,
                    'longueur_km': cote_distance,
                    'pente_pct': round(pente,1)
                })
            cote_distance = 0
            cote_elevation = 0
    if cote_distance >= 0.5:
        pente = (cote_elevation / (cote_distance * 1000)) * 100
        cote_distance_start = cum_d - cote_distance
        cotes.append({
            'start_km': cote_distance_start,
            'end_km': cum_d,
            'longueur_km': cote_distance,
            'pente_pct': round(pente,1)
        })
    
    analyse = {
        'distance_totale_km': df['cum_distance'].iloc[-1],
        'altitude_min_m': df['elevation'].min(),
        'altitude_max_m': df['elevation'].max(),
        'D_plus_m': D_plus,
        'df': df,
        'cotes': cotes
    }
    
    return analyse

# --- Fonction pour générer plan personnalisé ---
def generer_plan_personnalise(distance_course, D_plus, duree_semaine, sorties_par_semaine):
    plan = []
    volume_base = distance_course / 5
    coef_Dplus = 1 + (D_plus / 1000)
    
    for semaine in range(1, duree_semaine + 1):
        if semaine >= duree_semaine - 1:
            coef_progression = 0.7 + 0.15*(semaine - (duree_semaine - 2))
        else:
            coef_progression = 1 + 0.07*(semaine - 1)
        
        volume_total = volume_base * coef_Dplus * coef_progression
        
        easy_pct = 0.25
        seuil_pct = 0.30
        fraction_pct = 0.20
        long_pct = 0.25
        
        if D_plus > 500:
            fraction_pct += 0.1
            seuil_pct -= 0.05
            easy_pct -= 0.05
        
        easy_km = round(volume_total * easy_pct, 1)
        seuil_km = round(volume_total * seuil_pct, 1)
        fraction_km = round(volume_total * fraction_pct, 1)
        long_km = round(volume_total * long_pct, 1)
        
        plan.append({
            'Semaine': semaine,
            'Easy Run (km)': easy_km,
            'Seuil / Tempo (km)': seuil_km,
            'Fractionné / Côtes (km)': fraction_km,
            'Long Run (km)': long_km,
            'Volume total (km)': round(volume_total, 1)
        })
    
    return pd.DataFrame(plan)

# --- Streamlit UI ---
st.title("🏃 Analyse GPX et Plan d'entraînement personnalisé")

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
        ax.plot(df['cum_distance'], df['elevation'], color='red', linewidth=2)
        ax.set_facecolor('#f5f5f5')
        fig.patch.set_facecolor('#f5f5f5')
        ax.grid(True, color='black', linestyle='--', linewidth=0.7, alpha=0.3)
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Altitude (m)")
        ax.set_title("Profil d'altitude du parcours")
        
        for i, cote in enumerate(analyse['cotes'], 1):
            mid = (cote['start_km'] + cote['end_km']) / 2
            h = df.loc[(df['cum_distance']>=cote['start_km']) & (df['cum_distance']<=cote['end_km']), 'elevation'].max()
            ax.annotate(f"{cote['pente_pct']} %", xy=(mid, h), xytext=(0,10), textcoords='offset points',
                        ha='center', color='red', fontsize=9, fontweight='bold')
            ax.axvspan(cote['start_km'], cote['end_km'], color='red', alpha=0.1)
        
        st.pyplot(fig)
        
        # --- Tableau des côtes ---
        if analyse['cotes']:
            st.subheader("🗻 Tableau des côtes (>500m)")
            cotes_df = pd.DataFrame(analyse['cotes'])
            cotes_df = cotes_df[['start_km','end_km','longueur_km','pente_pct']]
            cotes_df = cotes_df.round({'start_km':1,'end_km':1,'longueur_km':1})
            cotes_df.rename(columns={'start_km':'Début (km)','end_km':'Fin (km)','longueur_km':'Longueur (km)','pente_pct':'% dénivelé'}, inplace=True)
            cotes_df['% dénivelé'] = cotes_df['% dénivelé'].astype(str) + ' %'
            st.dataframe(cotes_df, use_container_width=True)
        
        # --- Paramètres pour le plan ---
        st.subheader("⚙️ Paramètres du plan d'entraînement")
        objectif_temps = st.text_input("Durée cible du semi (ex: 1h50)", value="1h50")
        duree_semaine = st.selectbox("Durée du plan (semaines)", list(range(4,21)), index=4)
        sorties_par_semaine = st.selectbox("Nombre de sorties par semaine", [2,3,4], index=1)
        
        if st.button("Générer le plan d'entraînement"):
            plan_df = generer_plan_personnalise(analyse['distance_totale_km'], analyse['D_plus_m'], duree_semaine, sorties_par_semaine)
            
            st.subheader("📋 Plan d'entraînement personnalisé")
            st.dataframe(plan_df, use_container_width=True)
            
            # --- Graphique volume hebdo ---
            fig2, ax2 = plt.subplots(figsize=(10,4))
            ax2.plot(plan_df['Semaine'], plan_df['Volume total (km)'], color='#ff4b4b', linewidth=3, marker='o')
            ax2.set_facecolor('#f5f5f5')
            fig2.patch.set_facecolor('#f5f5f5')
            ax2.set_title("Évolution du volume hebdomadaire", fontsize=14, weight='bold')
            ax2.set_xlabel("Semaine", fontsize=12)
            ax2.set_ylabel("Volume total (km)", fontsize=12)
            ax2.grid(True, color='black', linestyle='--', linewidth=0.7, alpha=0.3)
            ax2.xaxis.set_major_locator(MultipleLocator(1))
            st.pyplot(fig2)
        
    else:
        st.error("Impossible d'analyser le fichier GPX.")
