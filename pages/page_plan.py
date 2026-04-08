import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from shared import (inject_css, style_ax, parse_chrono, estimer_vdot,
                    allures_from_vdot, format_pace, generer_plan_personnalise,
                    COLOR_PRIMARY, COLOR_SECONDARY,
                    CHART_LINE_ASCENT, CHART_LINE_DESCENT)


def render():
    inject_css()

    st.markdown("# Plan d'entra\u00eenement")
    st.markdown('<p class="section-label">Param\u00e8tres et g\u00e9n\u00e9ration du plan personnalis\u00e9</p>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    analyse = st.session_state.get('analyse')

    if analyse:
        st.markdown('<p class="section-label">Parcours charg\u00e9</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
              <span class="stat-label">Distance</span>
              <span class="stat-value">{analyse['distance_totale_km']:.2f} <span class="stat-unit">km</span></span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
              <span class="stat-label">D+</span>
              <span class="stat-value">{analyse['D_plus_m']:.0f} <span class="stat-unit">m</span></span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    else:
        st.info("Aucun parcours GPX charg\u00e9. Vous pouvez g\u00e9n\u00e9rer un plan sans analyse de parcours, ou importer un GPX sur la page **Analyse GPX**.")

    st.markdown('<p class="section-label">Param\u00e8tres du plan d\'entra\u00eenement</p>', unsafe_allow_html=True)

    # Initialiser les valeurs par défaut en session state
    defaults = {
        'p_niveau': 0, 'p_type_course': 0, 'p_chrono_actuel': '',
        'p_chrono_cible': '', 'p_duree_semaine': 4, 'p_sorties': 1,
        'p_volume_debut': 5, 'p_volume_pic': 5, 'p_date_course': None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    niveaux = ["D\u00e9butant", "Interm\u00e9diaire", "Avanc\u00e9"]
    types_course = ["5km", "10km", "Semi-marathon", "Marathon"]
    durees = list(range(4, 21))
    sorties_options = [2, 3, 4]
    volumes_debut = list(range(5, 21))
    volumes_pic = list(range(15, 105, 5))

    col_a, col_b = st.columns(2)
    with col_a:
        niveau = st.radio("Niveau", niveaux, horizontal=True, key="p_niveau")
        type_course = st.selectbox("Type de course", types_course, key="p_type_course")
        chrono_actuel = st.text_input("Chrono actuel (ex: 1h45)", key="p_chrono_actuel")
        chrono_cible = st.text_input("Chrono cible (ex: 1h30)", key="p_chrono_cible")
    with col_b:
        duree_semaine = st.selectbox("Dur\u00e9e du plan (semaines)", durees, key="p_duree_semaine")
        sorties_par_semaine = st.selectbox("Sorties par semaine", sorties_options, key="p_sorties")
        volume_debut = st.selectbox("Volume de d\u00e9part (km/semaine)", volumes_debut, key="p_volume_debut")
        volume_pic = st.selectbox("Volume pic (km/semaine)", volumes_pic, key="p_volume_pic")

    date_course = st.date_input("Date de la course", value=None, format="DD/MM/YYYY", key="p_date_course")

    # --- Estimation VDOT et allures ---
    if chrono_actuel or chrono_cible:
        distances_map = {"5km": 5, "10km": 10, "Semi-marathon": 21.0975, "Marathon": 42.195}
        dist_km = distances_map[type_course]

        temps_actuel = parse_chrono(chrono_actuel) if chrono_actuel else None
        temps_cible = parse_chrono(chrono_cible) if chrono_cible else None

        if chrono_actuel and not temps_actuel:
            st.warning("Format du chrono actuel non reconnu. Exemples : 1h45, 45:30, 3h30m, 25m30")
        if chrono_cible and not temps_cible:
            st.warning("Format du chrono cible non reconnu. Exemples : 1h45, 45:30, 3h30m, 25m30")

        if temps_actuel or temps_cible:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown('<p class="section-label">Estimation du niveau & allures d\'entra\u00eenement</p>', unsafe_allow_html=True)

            sections = []
            if temps_actuel:
                vdot_actuel = estimer_vdot(dist_km, temps_actuel)
                sections.append(("Niveau actuel", temps_actuel, vdot_actuel, COLOR_PRIMARY))
            if temps_cible:
                vdot_cible = estimer_vdot(dist_km, temps_cible)
                sections.append(("Niveau cible", temps_cible, vdot_cible, COLOR_SECONDARY))

            if temps_actuel and temps_cible:
                col_actuel, col_cible = st.columns(2)
                cols = [col_actuel, col_cible]
            else:
                cols = [st.container()]

            for idx, (label, temps, vdot, color) in enumerate(sections):
                with cols[idx]:
                    vitesse_kmh = round(dist_km / (temps / 60), 1)
                    allure_moy = format_pace(temps / dist_km)
                    st.markdown(f"""
                    <p style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 1.05rem;
                              color: {color}; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">
                      {label}
                    </p>
                    <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                      <div class="stat-card" style="flex: 1; min-width: 120px;">
                        <span class="stat-label">VDOT estim\u00e9</span>
                        <span class="stat-value">{vdot}</span>
                      </div>
                      <div class="stat-card" style="flex: 1; min-width: 120px;">
                        <span class="stat-label">Vitesse moy.</span>
                        <span class="stat-value">{vitesse_kmh} <span class="stat-unit">km/h</span></span>
                      </div>
                      <div class="stat-card" style="flex: 1; min-width: 120px;">
                        <span class="stat-label">Allure moy.</span>
                        <span class="stat-value">{allure_moy} <span class="stat-unit">/km</span></span>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

            if temps_actuel and temps_cible:
                col_z1, col_z2 = st.columns(2)
                cols_zones = [col_z1, col_z2]
            else:
                cols_zones = [st.container()]

            for idx, (label, temps, vdot, color) in enumerate(sections):
                with cols_zones[idx]:
                    allures = allures_from_vdot(vdot)
                    st.markdown(f'<p class="section-label">Zones d\'allure \u2013 {label}</p>', unsafe_allow_html=True)

                    for nom, (pace_fast, pace_slow) in allures.items():
                        vitesse_fast = round(60 / pace_fast, 1) if pace_fast else None
                        vitesse_slow = round(60 / pace_slow, 1) if pace_slow else None
                        vitesse_str = f"{vitesse_slow} \u2013 {vitesse_fast}" if vitesse_slow and vitesse_fast else "\u2014"
                        st.markdown(f"""
                        <div style="background: {color}; border: 1px solid #999; border-radius: 8px;
                                    padding: 0.5rem 0.8rem; margin-bottom: 0.5rem;
                                    display: flex; justify-content: space-between; align-items: center;
                                    flex-wrap: nowrap; gap: 0.3rem;">
                          <span style="font-family: 'Outfit', sans-serif; font-weight: 500; color: #FFF; flex: 2;
                                      font-size: 0.82rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                            {nom}
                          </span>
                          <span style="font-family: 'Geist Mono', monospace; color: #FFF; flex: 1;
                                      text-align: center; font-size: 0.78rem; white-space: nowrap;">
                            {format_pace(pace_fast)}\u2013{format_pace(pace_slow)} /km
                          </span>
                          <span style="font-family: 'Geist Mono', monospace; color: #FFF; flex: 1;
                                      text-align: right; font-size: 0.78rem; white-space: nowrap;">
                            {vitesse_str} km/h
                          </span>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("")

    # --- Génération du plan ---
    st.markdown("")
    if st.button("G\u00e9n\u00e9rer le plan d'entra\u00eenement"):
        d_plus = analyse['D_plus_m'] if analyse else 0
        plan_df = generer_plan_personnalise(
            niveau, type_course, volume_debut, volume_pic,
            duree_semaine, sorties_par_semaine, d_plus
        )

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Plan d\'entra\u00eenement personnalis\u00e9</p>', unsafe_allow_html=True)
        st.dataframe(plan_df, use_container_width=True)

        st.markdown('<p class="section-label">Volume hebdomadaire</p>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(11, 3.5))
        style_ax(ax2, fig2)
        ax2.plot(plan_df['Semaine'], plan_df['Volume total (km)'],
                 color=CHART_LINE_ASCENT, linewidth=2, zorder=3)
        ax2.fill_between(plan_df['Semaine'], plan_df['Volume total (km)'],
                         alpha=0.06, color=CHART_LINE_ASCENT)

        colors_type = {'Progression': CHART_LINE_ASCENT, 'All\u00e9g\u00e9e': '#B0B0B0', 'Taper': CHART_LINE_DESCENT}
        for t, color in colors_type.items():
            mask = plan_df['Type'] == t
            if mask.any():
                ax2.scatter(plan_df.loc[mask, 'Semaine'], plan_df.loc[mask, 'Volume total (km)'],
                            color=color, s=40, zorder=5, edgecolors='white', linewidths=1.2, label=t)

        ax2.legend(fontsize=8, loc='upper left', framealpha=0.8)
        ax2.set_xlabel("Semaine", fontsize=10)
        ax2.set_ylabel("Volume (km)", fontsize=10)
        ax2.xaxis.set_major_locator(MultipleLocator(1))
        fig2.tight_layout()
        st.pyplot(fig2)
