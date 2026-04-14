# utils/ — modules métier du projet plan-entrainement
#
# constants.py    → couleurs, constantes graphiques, limites de volume
# styles.py       → injection CSS Streamlit + style matplotlib
# gpx.py          → parsing et analyse des fichiers GPX
# vdot.py         → estimation VDOT, calcul d'allures, parsing chrono
# session_mix.py  → mix de séances (course × sorties × phase)
# plan.py         → génération du plan d'entraînement personnalisé
# seance.py       → programme détaillé par séance (échauffement / corps / retour)

from utils.constants import (
    COLOR_PRIMARY, COLOR_SECONDARY,
    CHART_BG, CHART_LINE_ASCENT, CHART_LINE_DESCENT,
    CHART_FILL_ASCENT, CHART_FILL_DESCENT, CHART_HIGHLIGHT,
    VOLUME_PIC_LIMITS,
)
from utils.styles import inject_css, style_ax
from utils.gpx import analyser_gpx
from utils.vdot import parse_chrono, estimer_vdot, allures_from_vdot, format_pace, deduire_niveau
from utils.session_mix import (
    compute_sessions, get_phase_group,
    EF, VMA, SEUIL, AS, SL, COTES, LABELS,
    PHASE_BASE, PHASE_SPECIFIC, PHASE_TAPER,
)
from utils.plan import generer_plan_personnalise, get_volume_pic_range, deriver_volumes
from utils.seance import generer_seance_detaillee
