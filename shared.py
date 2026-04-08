import streamlit as st
import numpy as np
import pandas as pd
import re
from matplotlib.ticker import MultipleLocator


# --- Couleurs de l'application ---
COLOR_PRIMARY = "#B0B0B0"
COLOR_SECONDARY = "#93A5CF"  # Pantone 6099 C

# --- Style partagé pour les graphiques matplotlib ---
CHART_BG = "#E8E8E8"
CHART_LINE_ASCENT = "#D04D46"   # Pantone 6047 C
CHART_LINE_DESCENT = "#5A77B5"  # Pantone 6102 C
CHART_FILL_ASCENT = "#D04D46"   # Pantone 6047 C
CHART_FILL_DESCENT = "#5A77B5"  # Pantone 6102 C
CHART_HIGHLIGHT = "#D04D46"     # Pantone 6047 C


def inject_css():
    """Injecte le CSS partagé dans la page courante."""
    st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Outfit:wght@300;400;500;600&display=swap');

  html, body, [data-testid="stAppViewContainer"] {
    background-color: #2E2E2E;
    font-family: 'Outfit', sans-serif;
    color: #E0E0E0;
  }

  [data-testid="stAppViewContainer"] > .main {
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1100px;
    margin: 0 auto;
    background-color: #2E2E2E;
  }

  /* Sidebar navigation styling */
  [data-testid="stSidebar"] {
    background-color: #2E2E2E;
  }

  [data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    font-family: 'Outfit', sans-serif;
    color: #E0E0E0 !important;
  }

  [data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    color: #FFFFFF !important;
  }

  h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 1.75rem;
    letter-spacing: -0.03em;
    color: #F0F0F0;
    margin-bottom: 0.25rem;
  }

  h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    letter-spacing: -0.02em;
    color: #E0E0E0;
  }

  .stat-card {
    background: #B0B0B0;
    border: 1px solid #999999;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .stat-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #FFFFFF;
  }

  .stat-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.03em;
  }

  .stat-unit {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    color: #FFFFFF;
  }

  .section-divider {
    border: none;
    border-top: 1px solid #4A4A4A;
    margin: 2rem 0;
  }

  .section-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #AAA;
    margin-bottom: 1rem;
  }

  [data-testid="stFileUploader"] {
    background: #555;
    border: 1px solid #666;
    border-radius: 8px;
    padding: 0.5rem;
  }

  [data-testid="stFileUploader"] label {
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 1.4rem;
    letter-spacing: 0.01em;
    color: #F0F0F0;
  }

  [data-testid="stFileUploader"] section {
    background: #B0B0B0 !important;
    border: 1px solid #999999 !important;
    border-radius: 6px;
    padding: 0.5rem;
  }

  [data-testid="stFileUploader"] section button {
    background: #B0B0B0 !important;
    color: #FFFFFF !important;
  }

  [data-testid="stDataFrame"] {
    background: #2E2E2E;
    border: none;
    border-radius: 8px;
    overflow: hidden;
    font-family: 'Geist Mono', monospace;
    font-size: 0.8rem;
    color: #2E2E2E;
  }

  [data-testid="stDataFrame"] [data-testid="stDataFrameResizable"],
  [data-testid="stDataFrame"] .stDataFrame,
  [data-testid="stDataFrame"] iframe {
    background: #2E2E2E !important;
  }

  [data-testid="stDataFrame"] th,
  [data-testid="stDataFrame"] td,
  [data-testid="stDataFrame"] .col_heading,
  [data-testid="stDataFrame"] .row_heading,
  [data-testid="stDataFrame"] .data,
  [data-testid="stDataFrame"] [role="gridcell"],
  [data-testid="stDataFrame"] [role="columnheader"] {
    background-color: #E8E8E8 !important;
    color: #2E2E2E !important;
  }

  .stButton > button {
    background: #555;
    color: #F0F0F0;
    border: none;
    border-radius: 6px;
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.6rem 1.5rem;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: background 0.15s;
  }

  .stButton > button:hover {
    background: #666;
  }

  [data-testid="stRadio"] label,
  [data-testid="stSelectbox"] label,
  [data-testid="stTextInput"] label,
  [data-testid="stDateInput"] label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #FFFFFF;
  }

  [data-testid="stRadio"],
  [data-testid="stSelectbox"],
  [data-testid="stTextInput"],
  [data-testid="stDateInput"] {
    background: #B0B0B0;
    border: 1px solid #999999;
    border-radius: 8px;
    padding: 0.5rem;
  }

  [data-testid="stRadio"] div[role="radiogroup"] label span,
  [data-testid="stRadio"] div[role="radiogroup"] label p,
  [data-testid="stSelectbox"] div[data-baseweb="select"] span,
  [data-testid="stSelectbox"] div[data-baseweb="select"] div,
  [data-testid="stTextInput"] input,
  [data-testid="stDateInput"] input {
    color: #2E2E2E !important;
  }

  [data-testid="stRadio"] div[role="radiogroup"] label {
    background: #B0B0B0 !important;
    border-radius: 4px;
    padding: 0.2rem 0.4rem;
  }

  [data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"],
  [data-testid="stRadio"] div[role="radiogroup"] input[type="radio"] {
    accent-color: #D04D46 !important;
  }

  [data-testid="stTextInput"] input:focus,
  [data-testid="stDateInput"] input:focus {
    border-color: #D04D46 !important;
    box-shadow: 0 0 0 1px #D04D46 !important;
    outline: none !important;
  }

  [data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
    border-color: #D04D46 !important;
    box-shadow: none !important;
    outline: none !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="popover"] {
    background: #B0B0B0 !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] {
    background: #B0B0B0 !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[data-baseweb="calendar-header"] *,
  [data-testid="stDateInput"] div[data-baseweb="popover"] div[data-baseweb="calendar-header"] * {
    color: #2E2E2E !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] button svg,
  [data-testid="stDateInput"] div[data-baseweb="popover"] button svg {
    fill: #2E2E2E !important;
    color: #2E2E2E !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] button,
  [data-testid="stDateInput"] div[data-baseweb="popover"] button {
    color: #2E2E2E !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[role="gridcell"] div[data-highlighted="true"],
  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[role="gridcell"] div[aria-selected="true"] {
    background-color: #2E2E2E !important;
    color: #FFFFFF !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[role="gridcell"] div {
    color: #2E2E2E !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[role="row"] div {
    color: #2E2E2E !important;
  }

  [data-testid="stAlert"] {
    border-radius: 8px;
    border: 1px solid #4A4A4A;
    font-family: 'Outfit', sans-serif;
  }
</style>
""", unsafe_allow_html=True)


def style_ax(ax, fig):
    """Style partagé pour les graphiques matplotlib."""
    ax.set_facecolor(CHART_BG)
    fig.patch.set_facecolor(CHART_BG)
    ax.grid(True, color='#C8C5BE', linestyle='-', linewidth=0.5, alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#C8C5BE')
    ax.spines['bottom'].set_color('#C8C5BE')
    ax.tick_params(colors='#555', labelsize=9)
    ax.xaxis.label.set_color('#444')
    ax.yaxis.label.set_color('#444')
    ax.title.set_color('#222')


# --- Fonction d'analyse GPX ---
def analyser_gpx(gpx_file):
    import gpxpy
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
        ) / 1000
        distances.append(d)
    df['distance'] = distances
    df['cum_distance'] = df['distance'].cumsum()
    df['elevation_diff'] = df['elevation'].diff().fillna(0)

    D_plus = df.loc[df['elevation_diff'] > 0, 'elevation_diff'].sum()

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
                    'pente_pct': round(pente, 1)
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
            'pente_pct': round(pente, 1)
        })

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
                    'pente_pct': round(pente, 1)
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
            'pente_pct': round(pente, 1)
        })

    return {
        'distance_totale_km': df['cum_distance'].iloc[-1],
        'altitude_min_m': df['elevation'].min(),
        'altitude_max_m': df['elevation'].max(),
        'D_plus_m': D_plus,
        'df': df,
        'cotes': cotes,
        'descentes': descentes
    }


# --- Parsing chrono et estimation VDOT ---
def parse_chrono(chrono_str):
    """Parse un chrono au format 1h45, 1h45m30, 45:30, 3h30m, 25m30, etc. Retourne le temps en minutes."""
    chrono_str = chrono_str.strip().lower()
    m = re.match(r'^(\d+)h(\d+)(?:m(\d+)?(?:s)?)?$', chrono_str)
    if m:
        h, mn, s = int(m.group(1)), int(m.group(2)), int(m.group(3)) if m.group(3) else 0
        return h * 60 + mn + s / 60
    m = re.match(r'^(\d+)m(\d+)?(?:s)?$', chrono_str)
    if m:
        mn, s = int(m.group(1)), int(m.group(2)) if m.group(2) else 0
        return mn + s / 60
    parts = chrono_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) + int(parts[1]) / 60
    if len(parts) == 3:
        return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
    return None


def estimer_vdot(distance_km, temps_minutes):
    """Estime le VDOT (Jack Daniels)."""
    t = temps_minutes
    d = distance_km * 1000
    v = d / t
    vo2 = -4.60 + 0.182258 * v + 0.000104 * v ** 2
    pct_max = 0.8 + 0.1894393 * np.exp(-0.012778 * t) + 0.2989558 * np.exp(-0.1932605 * t)
    vdot = vo2 / pct_max
    return round(vdot, 1)


def allures_from_vdot(vdot):
    """Calcule les allures d'entraînement à partir du VDOT."""
    zones = {
        'Endurance fondamentale (EF)': (0.59, 0.74),
        'Seuil (SL)': (0.83, 0.88),
        'Tempo': (0.88, 0.92),
        'Allure spécifique (AS)': (0.92, 0.96),
        'Intervalles / VMA': (0.97, 1.00),
    }
    allures = {}
    for nom, (pct_low, pct_high) in zones.items():
        vo2_low = vdot * pct_low
        vo2_high = vdot * pct_high
        def vo2_to_pace(vo2_val):
            a = 0.000104
            b = 0.182258
            c = -(vo2_val + 4.60)
            discriminant = b ** 2 - 4 * a * c
            if discriminant < 0:
                return None
            v = (-b + np.sqrt(discriminant)) / (2 * a)
            if v <= 0:
                return None
            return 1000 / v
        pace_slow = vo2_to_pace(vo2_low)
        pace_fast = vo2_to_pace(vo2_high)
        allures[nom] = (pace_fast, pace_slow)
    return allures


def format_pace(pace_min_per_km):
    """Formatte une allure en min/km vers M'SS\"."""
    if pace_min_per_km is None:
        return "\u2014"
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}'{seconds:02d}\""


# --- Génération du plan personnalisé ---
def generer_plan_personnalise(niveau, type_course, volume_debut, volume_pic, duree_semaine, sorties_par_semaine, D_plus):
    plan = []

    # Redescente + dernière semaine = course (taper)
    # < 10 sem : 1 redescente
    # 10-14 sem : 2 redescentes (tous types)
    # > 14 sem : 3 redescentes (semi/marathon), 2 sinon
    course_longue = type_course in ('Semi-marathon', 'Marathon')
    if duree_semaine > 14:
        semaines_redescente = 3 if course_longue else 2
    elif duree_semaine >= 10:
        semaines_redescente = 2
    else:
        semaines_redescente = 1
    semaines_build = duree_semaine - semaines_redescente - 1  # -1 pour la semaine course

    # Déterminer les semaines allégées selon la durée du plan
    # < 10 sem : aucune
    # 10-14 sem : 1 allégée au milieu de la phase build
    # > 14 sem : 2 allégées à intervalle régulier dans la phase build
    semaines_allegees = set()
    if duree_semaine > 14:
        tiers = semaines_build // 3
        semaines_allegees = {tiers, 2 * tiers}
    elif duree_semaine >= 10:
        milieu = semaines_build // 2
        semaines_allegees = {milieu}
    # Moins de 10 semaines : aucune allégée

    nb_prog = sum(1 for s in range(1, semaines_build + 1) if s not in semaines_allegees)

    if nb_prog > 1 and volume_pic > volume_debut:
        rate = (volume_pic / volume_debut) ** (1 / (nb_prog - 1)) - 1
        rate = max(0.05, min(0.10, rate))
    else:
        rate = 0.07

    current_volume = volume_debut
    prog_count = 0

    for semaine in range(1, duree_semaine + 1):
        if semaine <= semaines_build:
            # Phase de préparation
            if semaine in semaines_allegees:
                volume_total = current_volume * 0.70
            else:
                if prog_count > 0:
                    current_volume = min(current_volume * (1 + rate), volume_pic)
                volume_total = current_volume
                prog_count += 1
        elif semaine < duree_semaine:
            # Phase de redescente (avant la semaine course)
            step = semaine - semaines_build
            if semaines_redescente == 3:
                coef = {1: 0.75, 2: 0.60, 3: 0.45}[step]
            elif semaines_redescente == 2:
                coef = 0.70 if step == 1 else 0.50
            else:
                coef = 0.60
            volume_total = volume_pic * coef
        else:
            # Dernière semaine = semaine de course (taper)
            volume_total = volume_pic * 0.35

        if semaine <= semaines_build:
            sem_type = 'Allégée' if semaine in semaines_allegees else 'Progression'
        elif semaine < duree_semaine:
            sem_type = 'Redescente'
        else:
            sem_type = 'Course'

        is_long_run = (semaine % 2 == 1)

        if sorties_par_semaine == 2:
            quali_km = round(volume_total * 0.40, 1)
            sortie_longue_km = round(volume_total * 0.60, 1)
            if is_long_run:
                as_km = round(sortie_longue_km * 0.15, 1)
                detail = f"Long Run ({round(sortie_longue_km - as_km, 1)}) + AS ({as_km})"
            else:
                detail = f"EF ({sortie_longue_km})"
            plan.append({
                'Semaine': semaine, 'Type': sem_type,
                'Qualitative seuil/VMA (km)': quali_km,
                'Sortie longue ou EF (km)': sortie_longue_km,
                'D\u00e9tail sortie longue': detail,
                'Volume total (km)': round(volume_total, 1)
            })
        elif sorties_par_semaine == 3:
            ef_km = round(volume_total * 0.25, 1)
            quali_km = round(volume_total * 0.25, 1)
            sortie_longue_km = round(volume_total * 0.50, 1)
            as_km = round(sortie_longue_km * 0.15, 1)
            plan.append({
                'Semaine': semaine, 'Type': sem_type,
                'EF (km)': ef_km,
                'Qualitative VMA/seuil/c\u00f4tes (km)': quali_km,
                'Sortie longue (km)': sortie_longue_km,
                'dont AS (km)': as_km,
                'Volume total (km)': round(volume_total, 1)
            })
        else:
            ef_km = round(volume_total * 0.20, 1)
            quali1_km = round(volume_total * 0.15, 1)
            quali2_km = round(volume_total * 0.15, 1)
            sortie_longue_km = round(volume_total * 0.50, 1)
            as_km = round(sortie_longue_km * 0.15, 1)
            plan.append({
                'Semaine': semaine, 'Type': sem_type,
                'EF (km)': ef_km,
                'Qualitative 1 VMA (km)': quali1_km,
                'Qualitative 2 seuil/c\u00f4tes (km)': quali2_km,
                'Sortie longue (km)': sortie_longue_km,
                'dont AS (km)': as_km,
                'Volume total (km)': round(volume_total, 1)
            })

    return pd.DataFrame(plan)
