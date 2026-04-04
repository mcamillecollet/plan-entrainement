import streamlit as st
import gpxpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import datetime

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
    
    # Identifier les côtes >0.2 km
    cotes = []
    cote_distance = 0
    cote_elevation = 0
    cum_d = 0
    for d, e, cum_d in zip(df['distance'], df['elevation_diff'], df['cum_distance']):
        if e > 0:
            cote_distance += d
            cote_elevation += e
        else:
            if cote_distance >= 0.2:
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
    if cote_distance >= 0.2:
        pente = (cote_elevation / (cote_distance * 1000)) * 100
        cote_distance_start = cum_d - cote_distance
        cotes.append({
            'start_km': cote_distance_start,
            'end_km': cum_d,
            'longueur_km': cote_distance,
            'pente_pct': round(pente,1)
        })

    # Identifier les descentes >0.2 km
    descentes = []
    desc_distance = 0
    desc_elevation = 0
    cum_d = 0
    for d, e, cum_d in zip(df['distance'], df['elevation_diff'], df['cum_distance']):
        if e < 0:
            desc_distance += d
            desc_elevation += e
        else:
            if desc_distance >= 0.2:
                pente = (abs(desc_elevation) / (desc_distance * 1000)) * 100
                desc_distance_start = cum_d - desc_distance
                descentes.append({
                    'start_km': desc_distance_start,
                    'end_km': cum_d,
                    'longueur_km': desc_distance,
                    'pente_pct': round(pente,1)
                })
            desc_distance = 0
            desc_elevation = 0
    if desc_distance >= 0.2:
        pente = (abs(desc_elevation) / (desc_distance * 1000)) * 100
        desc_distance_start = cum_d - desc_distance
        descentes.append({
            'start_km': desc_distance_start,
            'end_km': cum_d,
            'longueur_km': desc_distance,
            'pente_pct': round(pente,1)
        })
    
    analyse = {
        'distance_totale_km': df['cum_distance'].iloc[-1],
        'altitude_min_m': df['elevation'].min(),
        'altitude_max_m': df['elevation'].max(),
        'D_plus_m': D_plus,
        'df': df,
        'cotes': cotes,
        'descentes': descentes
    }
    
    return analyse

# --- Fonction pour générer plan personnalisé ---
def generer_plan_personnalise(niveau, type_course, volume_debut, volume_pic, duree_semaine, sorties_par_semaine, D_plus):
    plan = []

    if niveau == "Débutant":
        easy_pct, seuil_pct, fraction_pct, long_pct = 0.45, 0.15, 0.10, 0.30
    elif niveau == "Intermédiaire":
        easy_pct, seuil_pct, fraction_pct, long_pct = 0.30, 0.25, 0.20, 0.25
    else:
        easy_pct, seuil_pct, fraction_pct, long_pct = 0.25, 0.25, 0.25, 0.25

    if type_course == "5km":
        fraction_pct += 0.10; long_pct -= 0.10
    elif type_course == "10km":
        fraction_pct += 0.05; seuil_pct += 0.05; easy_pct -= 0.05; long_pct -= 0.05
    elif type_course == "Semi-marathon":
        seuil_pct += 0.05; easy_pct -= 0.05
    elif type_course == "Marathon":
        long_pct += 0.10; fraction_pct -= 0.10

    if D_plus > 500:
        fraction_pct += 0.05; seuil_pct -= 0.05

    if sorties_par_semaine == 2:
        easy_pct += seuil_pct + fraction_pct
        seuil_pct, fraction_pct = 0, 0
    elif sorties_par_semaine == 3:
        seuil_pct += fraction_pct
        fraction_pct = 0

    total = easy_pct + seuil_pct + fraction_pct + long_pct
    easy_pct /= total; seuil_pct /= total; fraction_pct /= total; long_pct /= total

    semaines_taper = 3 if duree_semaine >= 12 else 2
    semaines_build = duree_semaine - semaines_taper

    for semaine in range(1, duree_semaine + 1):
        if semaine <= semaines_build:
            progress = (semaine - 1) / max(semaines_build - 1, 1)
            volume_total = volume_debut + (volume_pic - volume_debut) * progress
            if semaine % 4 == 0 and semaine < semaines_build:
                volume_total *= 0.75
        else:
            taper_step = semaine - semaines_build
            coef = 0.70 - 0.15 * (taper_step - 1)
            volume_total = volume_pic * max(coef, 0.30)

        plan.append({
            'Semaine': semaine,
            'Easy Run (km)': round(volume_total * easy_pct, 1),
            'Seuil / Tempo (km)': round(volume_total * seuil_pct, 1),
            'Fractionné / Côtes (km)': round(volume_total * fraction_pct, 1),
            'Long Run (km)': round(volume_total * long_pct, 1),
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
        
        # --- Graphique profil d'altitude (côtes) ---
        df = analyse['df']
        fig, ax = plt.subplots(figsize=(10,4))
        y_min_data, y_max_data = df['elevation'].min(), df['elevation'].max()
        data_range = y_max_data - y_min_data if y_max_data != y_min_data else 100

        min_gap_x = df['cum_distance'].iloc[-1] * 0.06
        label_positions = []
        cote_labels = []
        for cote in analyse['cotes']:
            mid = (cote['start_km'] + cote['end_km']) / 2
            h = df.loc[(df['cum_distance']>=cote['start_km']) & (df['cum_distance']<=cote['end_km']), 'elevation'].max()
            y_offset = 10
            for prev_x, prev_offset in label_positions:
                if abs(mid - prev_x) < min_gap_x:
                    y_offset = max(y_offset, prev_offset + 16)
            label_positions.append((mid, y_offset))
            cote_labels.append((cote, mid, h, y_offset))

        max_offset = max((off for _, off in label_positions), default=10)
        fig_height_pts = fig.get_size_inches()[1] * fig.dpi
        top_padding = (max_offset / fig_height_pts) * data_range * 1.8
        y_top = y_max_data + top_padding + data_range * 0.08
        y_bottom = y_min_data - data_range * 0.05
        ax.set_ylim(y_bottom, y_top)

        ax.fill_between(df['cum_distance'], df['elevation'], y_bottom, color='#cccccc', alpha=0.5)

        for cote, mid, h, y_offset in cote_labels:
            mask = (df['cum_distance'] >= cote['start_km']) & (df['cum_distance'] <= cote['end_km'])
            df_section = df[mask]
            if not df_section.empty:
                ax.fill_between(df_section['cum_distance'], df_section['elevation'],
                                y_top, color='#7B2D42', alpha=0.1)

        ax.plot(df['cum_distance'], df['elevation'], color='#7B2D42', linewidth=2)
        ax.set_facecolor('#f5f5f5')
        fig.patch.set_facecolor('#f5f5f5')
        ax.grid(True, color='black', linestyle='--', linewidth=0.7, alpha=0.3)
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xlim(0, df['cum_distance'].iloc[-1])
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Altitude (m)")
        ax.set_title("Profil d'altitude du parcours")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        for cote, mid, h, y_offset in cote_labels:
            ax.annotate(f"{cote['pente_pct']}%", xy=(mid, h),
                        xytext=(0, y_offset), textcoords='offset points',
                        ha='center', color='#7B2D42', fontsize=9, fontweight='bold')

        st.pyplot(fig)
        
        # --- Tableau des côtes ---
        if analyse['cotes']:
            st.subheader("🗻 Tableau des côtes (>200m)")
            cotes_df = pd.DataFrame(analyse['cotes'])
            cotes_df = cotes_df[['start_km','end_km','longueur_km','pente_pct']]
            cotes_df = cotes_df.round({'start_km':1,'end_km':1,'longueur_km':1})
            cotes_df.rename(columns={'start_km':'Début (km)','end_km':'Fin (km)','longueur_km':'Longueur (km)','pente_pct':'% dénivelé'}, inplace=True)
            st.dataframe(cotes_df, use_container_width=True, column_config={
                '% dénivelé': st.column_config.NumberColumn(format="%.1f %%")
            })

        # --- Graphique descentes ---
        if analyse['descentes']:
            st.subheader("📉 Profil des descentes (>200m)")
            fig3, ax3 = plt.subplots(figsize=(10,4))
            y_min_d, y_max_d = df['elevation'].min(), df['elevation'].max()
            data_range_d = y_max_d - y_min_d if y_max_d != y_min_d else 100

            min_gap_x_d = df['cum_distance'].iloc[-1] * 0.06
            label_positions_d = []
            desc_labels = []
            for desc in analyse['descentes']:
                mid = (desc['start_km'] + desc['end_km']) / 2
                h = df.loc[(df['cum_distance']>=desc['start_km']) & (df['cum_distance']<=desc['end_km']), 'elevation'].max()
                y_offset = 10
                for prev_x, prev_offset in label_positions_d:
                    if abs(mid - prev_x) < min_gap_x_d:
                        y_offset = max(y_offset, prev_offset + 16)
                label_positions_d.append((mid, y_offset))
                desc_labels.append((desc, mid, h, y_offset))

            max_offset_d = max((off for _, off in label_positions_d), default=10)
            fig_height_pts_d = fig3.get_size_inches()[1] * fig3.dpi
            top_padding_d = (max_offset_d / fig_height_pts_d) * data_range_d * 1.8
            y_top_d = y_max_d + top_padding_d + data_range_d * 0.08
            y_bottom_d = y_min_d - data_range_d * 0.05
            ax3.set_ylim(y_bottom_d, y_top_d)

            ax3.fill_between(df['cum_distance'], df['elevation'], y_bottom_d, color='#cccccc', alpha=0.5)

            for desc, mid, h, y_offset in desc_labels:
                mask = (df['cum_distance'] >= desc['start_km']) & (df['cum_distance'] <= desc['end_km'])
                df_section = df[mask]
                if not df_section.empty:
                    ax3.fill_between(df_section['cum_distance'], df_section['elevation'],
                                     y_top_d, color='#4A90C4', alpha=0.1)

            ax3.plot(df['cum_distance'], df['elevation'], color='#4A90C4', linewidth=2)
            ax3.set_facecolor('#f5f5f5')
            fig3.patch.set_facecolor('#f5f5f5')
            ax3.grid(True, color='black', linestyle='--', linewidth=0.7, alpha=0.3)
            ax3.xaxis.set_major_locator(MultipleLocator(1))
            ax3.set_xlim(0, df['cum_distance'].iloc[-1])
            ax3.set_xlabel("Distance (km)")
            ax3.set_ylabel("Altitude (m)")
            ax3.set_title("Profil des descentes")
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.spines['left'].set_visible(False)

            for desc, mid, h, y_offset in desc_labels:
                ax3.annotate(f"-{desc['pente_pct']}%", xy=(mid, h),
                             xytext=(0, y_offset), textcoords='offset points',
                             ha='center', color='#4A90C4', fontsize=9, fontweight='bold')

            st.pyplot(fig3)

            st.subheader("📋 Tableau des descentes (>200m)")
            desc_df = pd.DataFrame(analyse['descentes'])
            desc_df = desc_df[['start_km','end_km','longueur_km','pente_pct']]
            desc_df = desc_df.round({'start_km':1,'end_km':1,'longueur_km':1})
            desc_df.rename(columns={'start_km':'Début (km)','end_km':'Fin (km)','longueur_km':'Longueur (km)','pente_pct':'% dénivelé'}, inplace=True)
            st.dataframe(desc_df, use_container_width=True, column_config={
                '% dénivelé': st.column_config.NumberColumn(format="%.1f %%")
            })
        
        # --- Paramètres pour le plan ---
        st.subheader("⚙️ Paramètres du plan d'entraînement")
        niveau = st.radio("Niveau", ["Débutant", "Intermédiaire", "Avancé"], horizontal=True)
        type_course = st.selectbox("Type de course", ["5km", "10km", "Semi-marathon", "Marathon"])
        chrono_actuel = st.text_input("Chrono actuel (ex: 1h45)")
        chrono_cible = st.text_input("Chrono cible (ex: 1h30)")
        duree_semaine = st.selectbox("Durée du plan (semaines)", list(range(4, 21)), index=4)
        sorties_par_semaine = st.selectbox("Nombre de sorties par semaine", [2, 3, 4], index=1)
        volume_debut = st.selectbox("Volume hebdomadaire pour commencer (km)", list(range(5, 21)), index=5)
        volume_pic = st.selectbox("Volume hebdomadaire pic de préparation (km)", list(range(15, 105, 5)), index=5)
        date_course = st.date_input("Date de la course", value=None, format="DD/MM/YYYY")
        
        if st.button("Générer le plan d'entraînement"):
            plan_df = generer_plan_personnalise(niveau, type_course, volume_debut, volume_pic, duree_semaine, sorties_par_semaine, analyse['D_plus_m'])
            
            st.subheader("📋 Plan d'entraînement personnalisé")
            st.dataframe(plan_df, use_container_width=True)
            
            # --- Graphique volume hebdo ---
            fig2, ax2 = plt.subplots(figsize=(10,4))
            ax2.plot(plan_df['Semaine'], plan_df['Volume total (km)'], color='#7B2D42', linewidth=3, marker='o')
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
