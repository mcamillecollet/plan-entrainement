# seance.py — génération d'un programme détaillé pour chaque séance
#
# À partir d'une séance (type + km) produite par session_mix.compute_sessions
# et du VDOT actuel du coureur, on produit une structure standard :
#   {
#     "type": str, "label": str, "summary": str, "km_total": float,
#     "blocs": [ {"label", "detail", "allure", "pace"}, ... ]
#   }
# utilisée par la page Plan pour afficher un résumé inline + un détail dépliable.

from utils.vdot import allures_from_vdot, format_pace
from utils.session_mix import EF, VMA, SEUIL, AS, SL, COTES, LABELS, PHASE_TAPER


# --- Libellés de zones d'allure (doivent correspondre à allures_from_vdot) ---
ZONE_EF = "Endurance fondamentale (EF)"
ZONE_SEUIL = "Seuil (SL)"
ZONE_TEMPO = "Tempo"
ZONE_AS = "Allure spécifique (AS)"
ZONE_VMA = "Intervalles / VMA"


def _pace_range(allures, zone_name):
    """Retourne la fourchette d'allure formatée (ex: "4'50–5'20 /km") pour une zone."""
    if allures is None or zone_name not in allures:
        return "—"
    pace_fast, pace_slow = allures[zone_name]
    if pace_fast is None or pace_slow is None:
        return "—"
    return f"{format_pace(pace_fast)}–{format_pace(pace_slow)} /km"


def _median_pace(allures, zone_name):
    """Retourne l'allure médiane (min/km) d'une zone, ou None si indisponible."""
    if allures is None or zone_name not in allures:
        return None
    pace_fast, pace_slow = allures[zone_name]
    if pace_fast is None or pace_slow is None:
        return None
    return (pace_fast + pace_slow) / 2


def generer_seance_detaillee(seance, vdot, race_type, phase_group):
    """
    Point d'entrée principal : retourne la structure détaillée d'une séance.
    - seance : dict {type, label, km[, km_as]}
    - vdot   : float (VDOT actuel du coureur). Si None, les allures sont absentes.
    - race_type : '5km' | '10km' | 'Semi-marathon' | 'Marathon'
    - phase_group : 'base' | 'specific' | 'taper'
    """
    allures = allures_from_vdot(vdot) if vdot else None

    t = seance["type"]
    km = seance["km"]
    km_as = seance.get("km_as", 0) or 0

    if t == EF:
        return _seance_ef(seance, km, allures)
    if t == SL:
        return _seance_sl(seance, km, km_as, allures)
    if t == VMA:
        return _seance_vma(seance, km, allures, phase_group)
    if t == SEUIL:
        return _seance_seuil(seance, km, allures, phase_group)
    if t == AS:
        return _seance_as(seance, km, race_type, allures)
    if t == COTES:
        return _seance_cotes(seance, km, allures)

    # Fallback : séance inconnue, renvoyer un bloc unique EF
    return _seance_ef(seance, km, allures)


# -------------------- Séance par type --------------------

def _seance_ef(seance, km, allures):
    pace = _pace_range(allures, ZONE_EF)
    bloc = {
        "label": "Bloc continu",
        "detail": f"{km:.1f} km à allure EF",
        "allure": LABELS[EF],
        "pace": pace,
    }
    return {
        "type": seance["type"],
        "label": seance["label"],
        "summary": f"{km:.1f} km en endurance fondamentale",
        "km_total": km,
        "blocs": [bloc],
    }


def _seance_sl(seance, km, km_as, allures):
    blocs = []
    if km_as and km_as > 0:
        km_ef = round(km - km_as, 1)
        blocs.append({
            "label": "Partie EF",
            "detail": f"{km_ef:.1f} km à allure EF",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        })
        blocs.append({
            "label": "Partie AS (fin de sortie)",
            "detail": f"{km_as:.1f} km à allure spécifique",
            "allure": LABELS[AS],
            "pace": _pace_range(allures, ZONE_AS),
        })
        summary = f"{km:.1f} km dont {km_as:.1f} km en AS en fin de sortie"
    else:
        blocs.append({
            "label": "Sortie continue",
            "detail": f"{km:.1f} km à allure EF",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        })
        summary = f"Sortie longue de {km:.1f} km à allure EF"
    return {
        "type": seance["type"],
        "label": seance["label"],
        "summary": summary,
        "km_total": km,
        "blocs": blocs,
    }


def _seance_vma(seance, km, allures, phase_group):
    ech_km = 1.5
    retour_km = 0.5
    km_body = max(0.5, round(km - ech_km - retour_km, 1))

    # Choix du motif en fonction du volume de travail
    if km_body <= 2.0:
        pattern_reps = 8 if phase_group != PHASE_TAPER else 6
        body_label = f"{pattern_reps} × 30 s vite / 30 s trot"
        body_detail = "récup : trot actif, même durée que l'effort"
    elif km_body <= 3.5:
        pattern_reps = 10 if phase_group != PHASE_TAPER else 6
        body_label = f"{pattern_reps} × 400 m"
        body_detail = "récup : 1 min trot entre les répétitions"
    else:
        pattern_reps = 6 if phase_group != PHASE_TAPER else 4
        body_label = f"{pattern_reps} × 1000 m"
        body_detail = "récup : 2 min trot entre les répétitions"

    blocs = [
        {
            "label": "Échauffement",
            "detail": f"{ech_km:.1f} km progressifs",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
        {
            "label": f"Corps : {body_label}",
            "detail": body_detail,
            "allure": LABELS[VMA],
            "pace": _pace_range(allures, ZONE_VMA),
        },
        {
            "label": "Retour au calme",
            "detail": f"{retour_km:.1f} km",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
    ]
    return {
        "type": seance["type"],
        "label": seance["label"],
        "summary": body_label + " + échauf.",
        "km_total": km,
        "blocs": blocs,
    }


def _seance_seuil(seance, km, allures, phase_group):
    ech_km = 1.5
    retour_km = 1.0
    km_body = max(1.0, round(km - ech_km - retour_km, 1))

    if km_body <= 4:
        body_label = "2 × 10 min à allure tempo"
        body_detail = "récup : 2 min trot entre les blocs"
        zone = ZONE_TEMPO
        allure_display = "Tempo"
    elif km_body <= 7:
        body_label = "3 × 8 min à allure seuil"
        body_detail = "récup : 2 min trot entre les blocs"
        zone = ZONE_SEUIL
        allure_display = LABELS[SEUIL]
    else:
        body_label = "2 × 15 min à allure seuil"
        body_detail = "récup : 3 min trot entre les blocs"
        zone = ZONE_SEUIL
        allure_display = LABELS[SEUIL]

    if phase_group == PHASE_TAPER:
        # En taper : corps raccourci, 1 bloc unique.
        body_label = "1 × 10 min à allure tempo"
        body_detail = "effort contrôlé, pas de dernière accélération"
        zone = ZONE_TEMPO
        allure_display = "Tempo"

    blocs = [
        {
            "label": "Échauffement",
            "detail": f"{ech_km:.1f} km progressifs",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
        {
            "label": f"Corps : {body_label}",
            "detail": body_detail,
            "allure": allure_display,
            "pace": _pace_range(allures, zone),
        },
        {
            "label": "Retour au calme",
            "detail": f"{retour_km:.1f} km",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
    ]
    return {
        "type": seance["type"],
        "label": seance["label"],
        "summary": body_label + " + échauf.",
        "km_total": km,
        "blocs": blocs,
    }


def _seance_as(seance, km, race_type, allures):
    ech_km = 1.5
    retour_km = 1.0

    # Patterns AS par distance cible
    if race_type == "5km":
        body_label = "3 × 1 km à allure 5K"
        body_detail = "récup : 1 min trot"
    elif race_type == "10km":
        body_label = "3 × 2 km à allure 10K"
        body_detail = "récup : 2 min trot"
    elif race_type == "Semi-marathon":
        body_label = "2 × 5 km à allure semi"
        body_detail = "récup : 3 min trot"
    else:  # Marathon
        body_label = "1 × 8 km continus à allure marathon"
        body_detail = "bloc unique, régularité du pacing"

    blocs = [
        {
            "label": "Échauffement",
            "detail": f"{ech_km:.1f} km progressifs",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
        {
            "label": f"Corps : {body_label}",
            "detail": body_detail,
            "allure": LABELS[AS],
            "pace": _pace_range(allures, ZONE_AS),
        },
        {
            "label": "Retour au calme",
            "detail": f"{retour_km:.1f} km",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
    ]
    return {
        "type": seance["type"],
        "label": seance["label"],
        "summary": body_label,
        "km_total": km,
        "blocs": blocs,
    }


def _seance_cotes(seance, km, allures):
    ech_km = 1.5
    retour_km = 1.0
    blocs = [
        {
            "label": "Échauffement",
            "detail": f"{ech_km:.1f} km progressifs sur terrain plat",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
        {
            "label": "Corps : 8 × 45 s en côte",
            "detail": "effort puissant, récup en descente trottée ou marchée",
            "allure": "Effort contrôlé puissant",
            "pace": "—",
        },
        {
            "label": "Retour au calme",
            "detail": f"{retour_km:.1f} km sur plat",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
    ]
    return {
        "type": seance["type"],
        "label": seance["label"],
        "summary": "8 × 45 s en côte + échauf.",
        "km_total": km,
        "blocs": blocs,
    }
