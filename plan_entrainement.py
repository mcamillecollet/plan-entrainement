import streamlit as st
import gpxpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import MultipleLocator
import datetime

# --- Page config ---
st.set_page_config(
    page_title="Plan d'entraînement",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS (minimalist editorial style) ---
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

  /* Radio buttons: option background matching other inputs */
  [data-testid="stRadio"] div[role="radiogroup"] label {
    background: #B0B0B0 !important;
    border-radius: 4px;
    padding: 0.2rem 0.4rem;
  }

  /* Radio button circle/dot in Pantone 6047 C */
  [data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"],
  [data-testid="stRadio"] div[role="radiogroup"] input[type="radio"] {
    accent-color: #D04D46 !important;
  }

  /* Input focus border in Pantone 6047 C — champ de saisie uniquement */
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

  /* Date picker popover: month/year text, arrows, and selection in anthracite */
  [data-testid="stDateInput"] div[data-baseweb="popover"] {
    background: #B0B0B0 !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] {
    background: #B0B0B0 !important;
  }

  /* Month/year header text */
  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[data-baseweb="calendar-header"] *,
  [data-testid="stDateInput"] div[data-baseweb="popover"] div[data-baseweb="calendar-header"] * {
    color: #2E2E2E !important;
  }

  /* Navigation arrows */
  [data-testid="stDateInput"] div[data-baseweb="calendar"] button svg,
  [data-testid="stDateInput"] div[data-baseweb="popover"] button svg {
    fill: #2E2E2E !important;
    color: #2E2E2E !important;
  }

  [data-testid="stDateInput"] div[data-baseweb="calendar"] button,
  [data-testid="stDateInput"] div[data-baseweb="popover"] button {
    color: #2E2E2E !important;
  }

  /* Selected day highlight in anthracite */
  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[role="gridcell"] div[data-highlighted="true"],
  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[role="gridcell"] div[aria-selected="true"] {
    background-color: #2E2E2E !important;
    color: #FFFFFF !important;
  }

  /* Day numbers in anthracite */
  [data-testid="stDateInput"] div[data-baseweb="calendar"] div[role="gridcell"] div {
    color: #2E2E2E !important;
  }

  /* Weekday headers */
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


# --- Parsing chrono et estimation VDOT ---
def parse_chrono(chrono_str):
    """Parse un chrono au format 1h45, 1h45m30, 45:30, 3h30m, 25m30, etc. Retourne le temps en minutes."""
    import re
    chrono_str = chrono_str.strip().lower()
    # Format HhMm ou HhMmSs
    m = re.match(r'^(\d+)h(\d+)(?:m(\d+)?(?:s)?)?$', chrono_str)
    if m:
        h, mn, s = int(m.group(1)), int(m.group(2)), int(m.group(3)) if m.group(3) else 0
        return h * 60 + mn + s / 60
    # Format Mm ou MmSs
    m = re.match(r'^(\d+)m(\d+)?(?:s)?$', chrono_str)
    if m:
        mn, s = int(m.group(1)), int(m.group(2)) if m.group(2) else 0
        return mn + s / 60
    # Format MM:SS ou H:MM:SS
    parts = chrono_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) + int(parts[1]) / 60
    if len(parts) == 3:
        return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60
    return None


def estimer_vdot(distance_km, temps_minutes):
    """Estime le VDOT à partir d'une performance (distance en km, temps en minutes).
    Utilise la formule simplifiée de Jack Daniels."""
    t = temps_minutes
    d = distance_km * 1000  # en mètres
    v = d / t  # vitesse en m/min

    # VO2 estimée pour la course
    vo2 = -4.60 + 0.182258 * v + 0.000104 * v ** 2

    # Fraction de VO2max utilisable sur la durée
    pct_max = 0.8 + 0.1894393 * np.exp(-0.012778 * t) + 0.2989558 * np.exp(-0.1932605 * t)

    vdot = vo2 / pct_max
    return round(vdot, 1)


def allures_from_vdot(vdot):
    """Calcule les allures d'entraînement à partir du VDOT.
    Retourne un dict avec les allures en min/km."""

    # VO2 correspondant à chaque intensité (% du VDOT)
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
    """Formatte une allure en min/km vers M'SS" """
    if pace_min_per_km is None:
        return "—"
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}'{seconds:02d}\""


# --- Couleurs de l'application ---
COLOR_PRIMARY = "#B0B0B0"
COLOR_SECONDARY = "#93A5CF"  # Pantone 6099 C

# --- Style partagé pour les graphiques matplotlib ---
CHART_BG = "#E8E8E8"
CHART_LINE_ASCENT = "#D04D46"   # Pantone 6047 C
CHART_LINE_DESCENT = "#93A5CF"  # Pantone 6099 C
CHART_FILL_ASCENT = "#D04D46"   # Pantone 6047 C
CHART_FILL_DESCENT = "#93A5CF"  # Pantone 6099 C
CHART_HIGHLIGHT = "#D04D46"     # Pantone 6047 C


def style_ax(ax, fig):
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


# --- Header ---
st.markdown("# Analyse GPX & Plan d'entraînement")
st.markdown('<p class="section-label">Analyse de parcours — Planification personnalisée</p>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Importer le fichier GPX de votre prochaine course", type=['gpx'])

if uploaded_file is not None:
    analyse = analyser_gpx(uploaded_file)

    if analyse:
        # --- Statistiques parcours ---
        st.markdown('<p class="section-label">Statistiques du parcours</p>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        stats = [
            (col1, "Distance", f"{analyse['distance_totale_km']:.2f}", "km"),
            (col2, "Altitude min", f"{analyse['altitude_min_m']:.0f}", "m"),
            (col3, "Altitude max", f"{analyse['altitude_max_m']:.0f}", "m"),
            (col4, "D+", f"{analyse['D_plus_m']:.0f}", "m"),
        ]
        for col, label, value, unit in stats:
            with col:
                st.markdown(f"""
                <div class="stat-card">
                  <span class="stat-label">{label}</span>
                  <span class="stat-value">{value} <span class="stat-unit">{unit}</span></span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

        # --- Graphique profil d'altitude (côtes) ---
        st.markdown('<p class="section-label">Profil d\'altitude — montées</p>', unsafe_allow_html=True)
        df = analyse['df']
        fig, ax = plt.subplots(figsize=(11, 3.5))
        style_ax(ax, fig)

        y_min_data, y_max_data = df['elevation'].min(), df['elevation'].max()
        data_range = y_max_data - y_min_data if y_max_data != y_min_data else 100

        min_gap_x = df['cum_distance'].iloc[-1] * 0.10
        label_step = data_range * 0.13
        label_base = data_range * 0.03
        label_positions = []
        cote_labels = []
        for cote in analyse['cotes']:
            mid = (cote['start_km'] + cote['end_km']) / 2
            h = df.loc[(df['cum_distance'] >= cote['start_km']) & (df['cum_distance'] <= cote['end_km']), 'elevation'].max()
            y_label = h + label_base
            for prev_x, prev_y in label_positions:
                if abs(mid - prev_x) < min_gap_x:
                    y_label = max(y_label, prev_y + label_step)
            label_positions.append((mid, y_label))
            cote_labels.append((cote, mid, h, y_label))

        max_y_label = max((y for _, y in label_positions), default=y_max_data)
        y_top = max_y_label + data_range * 0.10
        y_bottom = y_min_data - data_range * 0.05
        ax.set_ylim(y_bottom, y_top)

        ax.fill_between(df['cum_distance'], df['elevation'], y_bottom, color=CHART_FILL_ASCENT, alpha=0.06)

        for cote, mid, h, y_label in cote_labels:
            mask = (df['cum_distance'] >= cote['start_km']) & (df['cum_distance'] <= cote['end_km'])
            df_section = df[mask]
            if not df_section.empty:
                ax.fill_between(df_section['cum_distance'], df_section['elevation'], y_bottom,
                                color=CHART_HIGHLIGHT, alpha=0.15)

        ax.plot(df['cum_distance'], df['elevation'], color=CHART_LINE_ASCENT, linewidth=1.5)
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xlim(0, df['cum_distance'].iloc[-1])
        ax.set_xlabel("Distance (km)", fontsize=10)
        ax.set_ylabel("Altitude (m)", fontsize=10)
        ax.set_title("")

        for cote, mid, h, y_label in cote_labels:
            ax.text(mid, y_label, f"{cote['pente_pct']}%",
                    ha='center', va='bottom', color=CHART_HIGHLIGHT,
                    fontsize=8.5, fontweight='bold', zorder=6)

        fig.tight_layout()
        st.pyplot(fig)

        # --- Tableau des côtes ---
        if analyse['cotes']:
            st.markdown('<p class="section-label">Montées &gt; 200 m</p>', unsafe_allow_html=True)
            cotes_df = pd.DataFrame(analyse['cotes'])
            cotes_df = cotes_df[['start_km', 'end_km', 'longueur_km', 'pente_pct']]
            cotes_df = cotes_df.round({'start_km': 1, 'end_km': 1, 'longueur_km': 1})
            cotes_df.index = range(1, len(cotes_df) + 1)
            cotes_df.rename(columns={
                'start_km': 'Début (km)', 'end_km': 'Fin (km)',
                'longueur_km': 'Longueur (km)', 'pente_pct': 'Pente (%)'
            }, inplace=True)
            st.dataframe(cotes_df, use_container_width=True, column_config={
                'Pente (%)': st.column_config.NumberColumn(format="%.1f %%")
            })

        # --- Graphique descentes ---
        if analyse['descentes']:
            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown('<p class="section-label">Profil d\'altitude — descentes</p>', unsafe_allow_html=True)
            fig3, ax3 = plt.subplots(figsize=(11, 3.5))
            style_ax(ax3, fig3)

            y_min_d, y_max_d = df['elevation'].min(), df['elevation'].max()
            data_range_d = y_max_d - y_min_d if y_max_d != y_min_d else 100

            min_gap_x_d = df['cum_distance'].iloc[-1] * 0.10
            label_step_d = data_range_d * 0.13
            label_base_d = data_range_d * 0.03
            label_positions_d = []
            desc_labels = []
            for desc in analyse['descentes']:
                mid = (desc['start_km'] + desc['end_km']) / 2
                h = df.loc[(df['cum_distance'] >= desc['start_km']) & (df['cum_distance'] <= desc['end_km']), 'elevation'].max()
                y_label = h + label_base_d
                for prev_x, prev_y in label_positions_d:
                    if abs(mid - prev_x) < min_gap_x_d:
                        y_label = max(y_label, prev_y + label_step_d)
                label_positions_d.append((mid, y_label))
                desc_labels.append((desc, mid, h, y_label))

            max_y_label_d = max((y for _, y in label_positions_d), default=y_max_d)
            y_top_d = max_y_label_d + data_range_d * 0.10
            y_bottom_d = y_min_d - data_range_d * 0.05
            ax3.set_ylim(y_bottom_d, y_top_d)

            ax3.fill_between(df['cum_distance'], df['elevation'], y_bottom_d, color=CHART_FILL_DESCENT, alpha=0.06)

            for desc, mid, h, y_label in desc_labels:
                mask = (df['cum_distance'] >= desc['start_km']) & (df['cum_distance'] <= desc['end_km'])
                df_section = df[mask]
                if not df_section.empty:
                    ax3.fill_between(df_section['cum_distance'], df_section['elevation'], y_bottom_d,
                                     color=CHART_LINE_DESCENT, alpha=0.15)

            ax3.plot(df['cum_distance'], df['elevation'], color=CHART_LINE_DESCENT, linewidth=1.5)
            ax3.xaxis.set_major_locator(MultipleLocator(1))
            ax3.set_xlim(0, df['cum_distance'].iloc[-1])
            ax3.set_xlabel("Distance (km)", fontsize=10)
            ax3.set_ylabel("Altitude (m)", fontsize=10)
            ax3.set_title("")

            for desc, mid, h, y_label in desc_labels:
                ax3.text(mid, y_label, f"({desc['pente_pct']})%",
                         ha='center', va='bottom', color=CHART_LINE_DESCENT,
                         fontsize=8.5, fontweight='bold', zorder=6)

            fig3.tight_layout()
            st.pyplot(fig3)

            st.markdown('<p class="section-label">Descentes &gt; 200 m</p>', unsafe_allow_html=True)
            desc_df = pd.DataFrame(analyse['descentes'])
            desc_df = desc_df[['start_km', 'end_km', 'longueur_km', 'pente_pct']]
            desc_df = desc_df.round({'start_km': 1, 'end_km': 1, 'longueur_km': 1})
            desc_df.index = range(1, len(desc_df) + 1)
            desc_df.rename(columns={
                'start_km': 'Début (km)', 'end_km': 'Fin (km)',
                'longueur_km': 'Longueur (km)', 'pente_pct': 'Pente (%)'
            }, inplace=True)
            st.dataframe(desc_df, use_container_width=True, column_config={
                'Pente (%)': st.column_config.NumberColumn(format="(%.1f) %%")
            })

        # --- Paramètres pour le plan ---
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Paramètres du plan d\'entraînement</p>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            niveau = st.radio("Niveau", ["Débutant", "Intermédiaire", "Avancé"], horizontal=True)
            type_course = st.selectbox("Type de course", ["5km", "10km", "Semi-marathon", "Marathon"])
            chrono_actuel = st.text_input("Chrono actuel (ex: 1h45)")
            chrono_cible = st.text_input("Chrono cible (ex: 1h30)")
        with col_b:
            duree_semaine = st.selectbox("Durée du plan (semaines)", list(range(4, 21)), index=4)
            sorties_par_semaine = st.selectbox("Sorties par semaine", [2, 3, 4], index=1)
            volume_debut = st.selectbox("Volume de départ (km/semaine)", list(range(5, 21)), index=5)
            volume_pic = st.selectbox("Volume pic (km/semaine)", list(range(15, 105, 5)), index=5)

        date_course = st.date_input("Date de la course", value=None, format="DD/MM/YYYY")

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
                st.markdown('<p class="section-label">Estimation du niveau & allures d\'entraînement</p>', unsafe_allow_html=True)

                # Préparer les données pour chaque chrono disponible
                sections = []
                if temps_actuel:
                    vdot_actuel = estimer_vdot(dist_km, temps_actuel)
                    sections.append(("Niveau actuel", temps_actuel, vdot_actuel, COLOR_PRIMARY))
                if temps_cible:
                    vdot_cible = estimer_vdot(dist_km, temps_cible)
                    sections.append(("Niveau cible", temps_cible, vdot_cible, COLOR_SECONDARY))

                # Afficher les colonnes VDOT côte à côte si les deux sont présents
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
                            <span class="stat-label">VDOT estimé</span>
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

                # Zones d'allure côte à côte
                if temps_actuel and temps_cible:
                    col_z1, col_z2 = st.columns(2)
                    cols_zones = [col_z1, col_z2]
                else:
                    cols_zones = [st.container()]

                for idx, (label, temps, vdot, color) in enumerate(sections):
                    with cols_zones[idx]:
                        allures = allures_from_vdot(vdot)
                        st.markdown(f'<p class="section-label">Zones d\'allure – {label}</p>', unsafe_allow_html=True)

                        for nom, (pace_fast, pace_slow) in allures.items():
                            vitesse_fast = round(60 / pace_fast, 1) if pace_fast else None
                            vitesse_slow = round(60 / pace_slow, 1) if pace_slow else None
                            vitesse_str = f"{vitesse_slow} – {vitesse_fast}" if vitesse_slow and vitesse_fast else "—"
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
                                {format_pace(pace_fast)}–{format_pace(pace_slow)} /km
                              </span>
                              <span style="font-family: 'Geist Mono', monospace; color: #FFF; flex: 1;
                                          text-align: right; font-size: 0.78rem; white-space: nowrap;">
                                {vitesse_str} km/h
                              </span>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown("")

        st.markdown("")
        if st.button("Générer le plan d'entraînement"):
            plan_df = generer_plan_personnalise(
                niveau, type_course, volume_debut, volume_pic,
                duree_semaine, sorties_par_semaine, analyse['D_plus_m']
            )

            st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
            st.markdown('<p class="section-label">Plan d\'entraînement personnalisé</p>', unsafe_allow_html=True)
            st.dataframe(plan_df, use_container_width=True)

            st.markdown('<p class="section-label">Volume hebdomadaire</p>', unsafe_allow_html=True)
            fig2, ax2 = plt.subplots(figsize=(11, 3.5))
            style_ax(ax2, fig2)
            ax2.plot(plan_df['Semaine'], plan_df['Volume total (km)'],
                     color=CHART_LINE_ASCENT, linewidth=2, marker='o',
                     markersize=5, markerfacecolor='white', markeredgewidth=1.5)
            ax2.fill_between(plan_df['Semaine'], plan_df['Volume total (km)'],
                             alpha=0.06, color=CHART_LINE_ASCENT)
            ax2.set_xlabel("Semaine", fontsize=10)
            ax2.set_ylabel("Volume (km)", fontsize=10)
            ax2.xaxis.set_major_locator(MultipleLocator(1))
            fig2.tight_layout()
            st.pyplot(fig2)

    else:
        st.error("Impossible d'analyser le fichier GPX.")
