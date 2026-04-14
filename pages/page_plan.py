from datetime import date
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from utils import (
    inject_css, style_ax, parse_chrono, estimer_vdot,
    allures_from_vdot, format_pace, generer_plan_personnalise,
    deduire_niveau, deriver_volumes, generer_seance_detaillee,
    COLOR_PRIMARY, COLOR_SECONDARY,
    CHART_LINE_ASCENT, CHART_LINE_DESCENT
)

DISTANCES_MAP = {"5km": 5, "10km": 10, "Semi-marathon": 21.0975, "Marathon": 42.195}
DUREE_PAR_DEFAUT = 12
SORTIES_PAR_DISTANCE = {
    "5km":           ([2, 3, 4, 5], 3),
    "10km":          ([3, 4, 5],    4),
    "Semi-marathon": ([3, 4, 5],    4),
    "Marathon":      ([3, 4, 5],    4),
}


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

    defaults = {
        'p_type_course': 0, 'p_chrono_actuel': '', 'p_chrono_cible': '',
        'p_date_course': None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    types_course = list(DISTANCES_MAP.keys())

    col_a, col_b = st.columns(2)
    with col_a:
        type_course = st.selectbox("Distance cible", types_course, key="p_type_course")
        chrono_actuel = st.text_input("Chrono actuel (ex: 1h45)", key="p_chrono_actuel")
        chrono_cible = st.text_input("Chrono vis\u00e9 (ex: 1h30)", key="p_chrono_cible")
    with col_b:
        sorties_options, sorties_default = SORTIES_PAR_DISTANCE[type_course]
        if st.session_state.get("p_sorties") not in sorties_options:
            st.session_state["p_sorties"] = sorties_default
        sorties_par_semaine = st.selectbox("Sorties par semaine", sorties_options, key="p_sorties")
        date_course = st.date_input("Date de la course (optionnelle)", value=None, format="DD/MM/YYYY", key="p_date_course")

    # --- Dérivation auto : VDOT → niveau → volumes + durée à partir de la date ---
    dist_km = DISTANCES_MAP[type_course]
    temps_actuel = parse_chrono(chrono_actuel) if chrono_actuel else None
    temps_cible = parse_chrono(chrono_cible) if chrono_cible else None

    if chrono_actuel and not temps_actuel:
        st.warning("Format du chrono actuel non reconnu. Exemples : 1h45, 45:30, 3h30m, 25m30")
    if chrono_cible and not temps_cible:
        st.warning("Format du chrono vis\u00e9 non reconnu. Exemples : 1h45, 45:30, 3h30m, 25m30")

    vdot_actuel = estimer_vdot(dist_km, temps_actuel) if temps_actuel else None
    niveau = deduire_niveau(vdot_actuel) if vdot_actuel else None

    if niveau:
        volume_debut, volume_pic = deriver_volumes(
            type_course, niveau, sorties_par_semaine, sorties_options
        )
    else:
        volume_debut = volume_pic = None

    if date_course:
        jours_restants = (date_course - date.today()).days
        if jours_restants <= 0:
            st.warning("La date de course est pass\u00e9e ou aujourd'hui : plan par d\u00e9faut de 12 semaines.")
            duree_semaine = DUREE_PAR_DEFAUT
        else:
            duree_semaine = max(6, min(18, jours_restants // 7))
    else:
        duree_semaine = DUREE_PAR_DEFAUT

    # --- Récapitulatif des paramètres dérivés ---
    if niveau:
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Param\u00e8tres d\u00e9duits automatiquement</p>', unsafe_allow_html=True)
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.markdown(f"""
            <div class="stat-card">
              <span class="stat-label">Niveau estim\u00e9</span>
              <span class="stat-value">{niveau}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_r2:
            st.markdown(f"""
            <div class="stat-card">
              <span class="stat-label">Plan sur</span>
              <span class="stat-value">{duree_semaine} <span class="stat-unit">semaines</span></span>
            </div>
            """, unsafe_allow_html=True)
        with col_r3:
            st.markdown(f"""
            <div class="stat-card">
              <span class="stat-label">Volume pic</span>
              <span class="stat-value">{volume_pic} <span class="stat-unit">km/sem</span></span>
            </div>
            """, unsafe_allow_html=True)

    # --- Estimation VDOT et allures ---
    if temps_actuel or temps_cible:
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">VDOT & allures d\'entra\u00eenement</p>', unsafe_allow_html=True)

        sections = []
        if temps_actuel:
            sections.append(("Niveau actuel", temps_actuel, vdot_actuel, COLOR_PRIMARY))
        if temps_cible:
            vdot_cible = estimer_vdot(dist_km, temps_cible)
            sections.append(("Niveau vis\u00e9", temps_cible, vdot_cible, COLOR_SECONDARY))

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
    can_generate = niveau is not None
    if not can_generate:
        st.info("Renseigne ton **chrono actuel** pour activer la g\u00e9n\u00e9ration du plan.")
    if st.button("G\u00e9n\u00e9rer le plan d'entra\u00eenement", disabled=not can_generate):
        d_plus = analyse['D_plus_m'] if analyse else 0
        plan_df = generer_plan_personnalise(
            niveau, type_course, volume_debut, volume_pic,
            duree_semaine, sorties_par_semaine, d_plus
        )

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Volume hebdomadaire</p>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(11, 3.5))
        style_ax(ax2, fig2)
        ax2.plot(plan_df['Semaine'], plan_df['Volume total (km)'],
                 color='#3C3C3C', linewidth=2, zorder=3)
        ax2.fill_between(plan_df['Semaine'], plan_df['Volume total (km)'],
                         alpha=0.06, color='#3C3C3C')

        colors_type = {
            'Under progress': CHART_LINE_ASCENT,
            'Cool down': '#B0B0B0',
            'Peak': '#CE0058',
            'Recovery': COLOR_SECONDARY,
            'Race Week': '#7AC4B7'
        }
        for t, color in colors_type.items():
            mask = plan_df['Type'] == t
            if mask.any():
                ax2.scatter(plan_df.loc[mask, 'Semaine'], plan_df.loc[mask, 'Volume total (km)'],
                            color=color, s=50, zorder=5, edgecolors='none', label=t)

        y_min = ax2.get_ylim()[0]
        bar_height = (ax2.get_ylim()[1] - y_min) * 0.04
        for _, row in plan_df.iterrows():
            sem = row['Semaine']
            t = row['Type']
            if t in colors_type:
                ax2.bar(sem, bar_height, bottom=y_min, width=0.8, color=colors_type[t], alpha=0.5, zorder=2)

        ax2.legend(fontsize=8, loc='upper left', framealpha=0.8)
        ax2.set_xlabel("Semaine", fontsize=10)
        ax2.set_ylabel("Volume (km)", fontsize=10)
        ax2.xaxis.set_major_locator(MultipleLocator(1))
        fig2.tight_layout()
        st.pyplot(fig2)

        # --- Cartes par semaine ---
        st.markdown('<p class="section-label">D\u00e9tail par semaine</p>', unsafe_allow_html=True)

        name_style = "font-family:'Outfit',sans-serif; font-size:0.9rem; font-weight:500; color:#F0F0F0;"
        summary_style = "font-family:'Outfit',sans-serif; font-size:0.76rem; color:#A8A8A8; margin-top:0.1rem;"
        km_style = "font-family:'Geist Mono',monospace; font-size:0.85rem; font-weight:500; color:#F0F0F0; white-space:nowrap;"

        rows_iter = list(plan_df.iterrows())
        # Deux semaines par ligne pour garder la grille 2 colonnes actuelle
        for i in range(0, len(rows_iter), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j >= len(rows_iter):
                    continue
                _, row = rows_iter[i + j]
                sem = int(row['Semaine'])
                sem_type = row['Type']
                phase_group = row.get('Phase', 'base')
                vol = row['Volume total (km)']
                color = colors_type.get(sem_type, '#B0B0B0')
                seances = row['S\u00e9ances'] or []

                # Badge optionnel quand le nombre de séances est réduit par le
                # post-traitement (volume hebdo trop bas pour tenir toutes les séances
                # au-dessus de leur plancher physiologique). La Race Week a toujours
                # 2 séances par design, on ne l'annote pas.
                reduced_badge = ""
                if sem_type != 'Race Week' and len(seances) < sorties_par_semaine:
                    reduced_badge = (
                        f'<span style="font-family:\'Outfit\',sans-serif; font-weight:500; '
                        f'font-size:0.72rem; color:#C8C8C8; background:rgba(255,255,255,0.08); '
                        f'border-radius:4px; padding:0.1rem 0.4rem; margin-left:0.5rem;">'
                        f'{len(seances)} s\u00e9ances (volume r\u00e9duit)</span>'
                    )

                with col:
                    with st.container(border=True):
                        # En-tête de la carte : semaine + phase + volume
                        st.markdown(
                            f"""<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem; border-left:4px solid {color}; padding-left:0.6rem;">
<span style="font-family:'Outfit',sans-serif; font-weight:600; font-size:1rem; color:#F0F0F0;">Semaine {sem}
<span style="font-weight:400; font-size:0.78rem; color:{color}; margin-left:0.5rem; text-transform:uppercase; letter-spacing:0.06em;">{sem_type}</span>{reduced_badge}
</span>
<span style="font-family:'Geist Mono',monospace; font-size:0.85rem; font-weight:500; color:#F0F0F0;">{vol} km</span>
</div>""",
                            unsafe_allow_html=True,
                        )

                        # Une ligne + expander par séance
                        for s_idx, seance in enumerate(seances):
                            detail = generer_seance_detaillee(
                                seance, vdot_actuel, type_course, phase_group
                            )
                            km_txt = f"{seance['km']:.1f} km"
                            summary_txt = detail['summary']

                            st.markdown(
                                f"""<div style="display:flex; justify-content:space-between; align-items:flex-start; padding:0.25rem 0;">
<div style="flex:1; min-width:0;">
<div style="{name_style}">{seance['label']}</div>
<div style="{summary_style}">{summary_txt}</div>
</div>
<div style="{km_style}; margin-left:0.8rem;">{km_txt}</div>
</div>""",
                                unsafe_allow_html=True,
                            )

                            with st.expander("Voir le d\u00e9tail de la s\u00e9ance", expanded=False):
                                for bloc in detail['blocs']:
                                    st.markdown(
                                        f"""<div style="padding:0.35rem 0; border-bottom:1px solid rgba(255,255,255,0.06);">
<div style="font-family:'Outfit',sans-serif; font-weight:500; font-size:0.88rem; color:#F0F0F0;">{bloc['label']}</div>
<div style="font-family:'Outfit',sans-serif; font-size:0.8rem; color:#C8C8C8; margin-top:0.1rem;">{bloc['detail']}</div>
<div style="display:flex; gap:1rem; margin-top:0.25rem; font-family:'Geist Mono',monospace; font-size:0.76rem; color:#9AA5BC;">
<span>Allure : {bloc['allure']}</span>
<span>Pace : {bloc['pace']}</span>
</div>
</div>""",
                                        unsafe_allow_html=True,
                                    )
