# utils/ — modules métier du projet plan-entrainement
#
# constants.py  → couleurs, constantes graphiques, limites de volume
# styles.py     → injection CSS Streamlit + style matplotlib
# gpx.py        → parsing et analyse des fichiers GPX
# vdot.py       → estimation VDOT, calcul d'allures, parsing chrono
# plan.py       → génération du plan d'entraînement personnalisé

from utils.constants import (
    COLOR_PRIMARY, COLOR_SECONDARY,
    CHART_BG, CHART_LINE_ASCENT, CHART_LINE_DESCENT,
    CHART_FILL_ASCENT, CHART_FILL_DESCENT, CHART_HIGHLIGHT,
    VOLUME_PIC_LIMITS,
)
from utils.styles import inject_css, style_ax
from utils.gpx import analyser_gpx
from utils.vdot import parse_chrono, estimer_vdot, allures_from_vdot, format_pace, deduire_niveau
from utils.plan import generer_plan_personnalise, get_volume_pic_range
