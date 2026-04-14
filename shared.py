# Ce fichier est conservé pour rétrocompatibilité uniquement.
# Toute la logique a été déplacée dans utils/ :
#
#   utils/constants.py  — couleurs et limites de volume
#   utils/styles.py     — inject_css() et style_ax()
#   utils/gpx.py        — analyser_gpx()
#   utils/vdot.py       — parse_chrono(), estimer_vdot(), allures_from_vdot(), format_pace()
#   utils/plan.py       — generer_plan_personnalise(), get_volume_pic_range()
#
# Les pages importent désormais depuis utils directement.

from utils import (
    inject_css, style_ax, analyser_gpx,
    parse_chrono, estimer_vdot, allures_from_vdot, format_pace,
    generer_plan_personnalise, get_volume_pic_range,
    COLOR_PRIMARY, COLOR_SECONDARY,
    CHART_BG, CHART_LINE_ASCENT, CHART_LINE_DESCENT,
    CHART_FILL_ASCENT, CHART_FILL_DESCENT, CHART_HIGHLIGHT,
    VOLUME_PIC_LIMITS,
)
