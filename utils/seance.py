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
from utils.session_mix import EF, VMA, SEUIL, AS, SL, COTES, LABELS, PHASE_TAPER, PHASE_RACE_WEEK


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


# -------------------- Patterns adaptatifs par type de séance --------------------
#
# Principe : le volume annoncé dans le titre (km_total) doit correspondre au cumul
# réel échauffement + corps + retour au calme. Pour une séance de qualité (VMA /
# Seuil / AS / Côtes) on fixe :
#   - retour au calme = 0.5 km (constant)
#   - échauffement    = variable, absorbe le résidu pour atteindre km_total
#   - corps           = pattern choisi en fonction d'une cible body_target
#                       = km_total - 1.5 - 0.5 (plancher à 1.0 km).
# Les patterns renvoient le km réellement couvert par le corps afin que la fonction
# appelante calcule un échauffement cohérent (`ech_km = km_total - actual_body - 0.5`).

_COOLDOWN_KM = 0.5
_DEFAULT_WARMUP_KM = 1.5
_MIN_WARMUP_KM = 1.0


def _body_target(km):
    """Cible de volume pour le corps d'une séance de qualité (plancher 1.0 km)."""
    return max(1.0, round(km - _DEFAULT_WARMUP_KM - _COOLDOWN_KM, 1))


def _warmup_km(km, actual_body_km):
    """Échauffement absorbant le résidu, avec un plancher à 1.0 km."""
    return max(_MIN_WARMUP_KM, round(km - actual_body_km - _COOLDOWN_KM, 1))


def _pattern_vma(body_target):
    """
    Pattern VMA adapté au volume de corps visé. Retourne (label, detail, actual_km).
    Les tailles de répétition sont choisies pour rester physiologiquement pertinentes :
    200 m pour des séances très courtes, 1500 m pour les longues.
    """
    if body_target <= 2.0:
        n = max(6, round(body_target * 5))
        return (
            f"{n} × 200 m",
            "récup : 1 min trot entre les répétitions",
            round(n * 0.2, 1),
        )
    if body_target <= 4.0:
        n = max(5, round(body_target * 2.5))
        return (
            f"{n} × 400 m",
            "récup : 1 min trot entre les répétitions",
            round(n * 0.4, 1),
        )
    if body_target <= 7.5:
        n = max(4, round(body_target))
        return (
            f"{n} × 1000 m",
            "récup : 2 min trot entre les répétitions",
            round(n * 1.0, 1),
        )
    n = max(5, round(body_target / 1.5))
    return (
        f"{n} × 1500 m",
        "récup : 2 min 30 trot entre les répétitions",
        round(n * 1.5, 1),
    )


def _pattern_seuil(body_target):
    """
    Pattern Seuil/Tempo adapté au volume visé. Retourne
    (label, detail, zone_name, allure_display, actual_km).
    Le corps couvre exactement body_target (rep_km = body_target / nb_reps, arrondi).
    """
    if body_target <= 3.0:
        rep_km = round(body_target / 2, 1)
        actual = round(2 * rep_km, 1)
        return (
            f"2 × {rep_km:.1f} km à allure tempo",
            "récup : 2 min trot entre les blocs",
            ZONE_TEMPO,
            "Tempo",
            actual,
        )
    if body_target <= 6.0:
        rep_km = round(body_target / 3, 1)
        actual = round(3 * rep_km, 1)
        return (
            f"3 × {rep_km:.1f} km à allure seuil",
            "récup : 2 min trot entre les blocs",
            ZONE_SEUIL,
            LABELS[SEUIL],
            actual,
        )
    rep_km = round(body_target / 2, 1)
    actual = round(2 * rep_km, 1)
    return (
        f"2 × {rep_km:.1f} km à allure seuil",
        "récup : 3 min trot entre les blocs",
        ZONE_SEUIL,
        LABELS[SEUIL],
        actual,
    )


def _pattern_as(body_target, race_type):
    """
    Pattern allure spécifique adapté au volume visé et au type de course.
    Retourne (label, detail, actual_km).
    """
    if race_type == "5km":
        rep_km = round(body_target / 3, 1)
        actual = round(3 * rep_km, 1)
        return (
            f"3 × {rep_km:.1f} km à allure 5K",
            "récup : 1 min trot entre les blocs",
            actual,
        )
    if race_type == "10km":
        rep_km = round(body_target / 2, 1)
        actual = round(2 * rep_km, 1)
        return (
            f"2 × {rep_km:.1f} km à allure 10K",
            "récup : 2 min trot entre les blocs",
            actual,
        )
    if race_type == "Semi-marathon":
        rep_km = round(body_target / 2, 1)
        actual = round(2 * rep_km, 1)
        return (
            f"2 × {rep_km:.1f} km à allure semi",
            "récup : 3 min trot entre les blocs",
            actual,
        )
    # Marathon : bloc unique continu
    body_km = round(body_target, 1)
    return (
        f"1 × {body_km:.1f} km continus à allure marathon",
        "bloc unique, régularité du pacing",
        body_km,
    )


def _pattern_cotes(body_target):
    """
    Pattern côtes adapté au volume visé. Chaque répétition cumule ~0.3 km
    (montée 45 s + descente trottée/marchée). Plage de répétitions 6–12.
    Retourne (label, detail, actual_km).
    """
    n = max(6, min(12, round(body_target / 0.3)))
    return (
        f"{n} × 45 s en côte",
        "effort puissant, récup en descente trottée ou marchée",
        round(n * 0.3, 1),
    )


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
        return _seance_as(seance, km, race_type, allures, phase_group)
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
    retour_km = _COOLDOWN_KM

    # Race week : stimulus court et non traumatisant, quel que soit le volume.
    # On pad l'échauffement pour absorber le volume excédentaire (rien ne sert de raccourcir
    # le km total : le coureur garde une sortie complète, seul le corps de séance est court).
    if phase_group == PHASE_RACE_WEEK:
        body_label = "6 × 200 m"
        body_detail = "récup : 1 min marche/trot — effort vif mais non maximal"
        actual_body_km = 1.2
    else:
        body_target = _body_target(km)
        body_label, body_detail, actual_body_km = _pattern_vma(body_target)

    ech_km = _warmup_km(km, actual_body_km)

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
    retour_km = _COOLDOWN_KM
    body_target = _body_target(km)

    if phase_group == PHASE_TAPER:
        # En taper : un bloc tempo unique, effort contrôlé, corps = body_target complet.
        rep_km = round(body_target, 1)
        body_label = f"1 × {rep_km:.1f} km à allure tempo"
        body_detail = "effort contrôlé, pas de dernière accélération"
        zone = ZONE_TEMPO
        allure_display = "Tempo"
        actual_body_km = rep_km
    else:
        body_label, body_detail, zone, allure_display, actual_body_km = _pattern_seuil(body_target)

    ech_km = _warmup_km(km, actual_body_km)

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


def _seance_as(seance, km, race_type, allures, phase_group):
    retour_km = _COOLDOWN_KM

    # Race week : corps très court, juste un rappel d'allure cible.
    # L'échauffement absorbe le volume excédentaire (on garde une sortie "normale" en km).
    if phase_group == PHASE_RACE_WEEK:
        if race_type == "5km":
            body_label = "3 × 500 m à allure 5K"
            body_detail = "récup : 1 min trot — rappel d'allure"
            actual_body_km = 1.5
        elif race_type == "10km":
            body_label = "2 × 1 km à allure 10K"
            body_detail = "récup : 2 min trot — rappel d'allure"
            actual_body_km = 2.0
        elif race_type == "Semi-marathon":
            body_label = "2 × 1 km à allure semi"
            body_detail = "récup : 2 min trot — rappel d'allure"
            actual_body_km = 2.0
        else:  # Marathon
            body_label = "3 km continus à allure marathon"
            body_detail = "rappel d'allure, pas plus"
            actual_body_km = 3.0
    else:
        body_target = _body_target(km)
        body_label, body_detail, actual_body_km = _pattern_as(body_target, race_type)

    ech_km = _warmup_km(km, actual_body_km)

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
    retour_km = _COOLDOWN_KM
    body_target = _body_target(km)
    body_label, body_detail, actual_body_km = _pattern_cotes(body_target)
    ech_km = _warmup_km(km, actual_body_km)

    blocs = [
        {
            "label": "Échauffement",
            "detail": f"{ech_km:.1f} km progressifs sur terrain plat",
            "allure": LABELS[EF],
            "pace": _pace_range(allures, ZONE_EF),
        },
        {
            "label": f"Corps : {body_label}",
            "detail": body_detail,
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
        "summary": body_label + " + échauf.",
        "km_total": km,
        "blocs": blocs,
    }
