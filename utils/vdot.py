# vdot.py — estimation VDOT (Jack Daniels), calcul des zones d'allure, parsing de chrono

import numpy as np
import re


def parse_chrono(chrono_str):
    """
    Parse un chrono textuel vers des minutes (float).
    Formats acceptés : 1h45, 1h45m30, 45:30, 3h30m, 25m30, 1:45:30
    Retourne None si le format n'est pas reconnu.
    """
    chrono_str = chrono_str.strip().lower()

    # Format : 1h45, 1h45m30, 1h45m
    m = re.match(r'^(\d+)h(\d+)(?:m(\d+)?(?:s)?)?$', chrono_str)
    if m:
        h, mn, s = int(m.group(1)), int(m.group(2)), int(m.group(3)) if m.group(3) else 0
        return h * 60 + mn + s / 60

    # Format : 25m30, 45m
    m = re.match(r'^(\d+)m(\d+)?(?:s)?$', chrono_str)
    if m:
        mn, s = int(m.group(1)), int(m.group(2)) if m.group(2) else 0
        return mn + s / 60

    # Format : 45:30 ou 1:45:30
    parts = chrono_str.split(':')
    if len(parts) == 2:
        return int(parts[0]) + int(parts[1]) / 60
    if len(parts) == 3:
        return int(parts[0]) * 60 + int(parts[1]) + int(parts[2]) / 60

    return None


def estimer_vdot(distance_km, temps_minutes):
    """
    Estime le VDOT selon la méthode Jack Daniels.
    distance_km : distance de la course
    temps_minutes : temps de course en minutes
    """
    t = temps_minutes
    d = distance_km * 1000
    v = d / t
    vo2 = -4.60 + 0.182258 * v + 0.000104 * v ** 2
    pct_max = 0.8 + 0.1894393 * np.exp(-0.012778 * t) + 0.2989558 * np.exp(-0.1932605 * t)
    vdot = vo2 / pct_max
    return round(vdot, 1)


def allures_from_vdot(vdot):
    """
    Calcule les zones d'allure d'entraînement (min/km) à partir d'un VDOT.
    Retourne un dict {nom_zone: (pace_rapide, pace_lente)} en min/km.
    """
    zones = {
        'Endurance fondamentale (EF)': (0.59, 0.74),
        'Seuil (SL)':                  (0.83, 0.88),
        'Tempo':                        (0.88, 0.92),
        'Allure spécifique (AS)':       (0.92, 0.96),
        'Intervalles / VMA':            (0.97, 1.00),
    }
    allures = {}
    for nom, (pct_low, pct_high) in zones.items():
        vo2_low = vdot * pct_low
        vo2_high = vdot * pct_high
        allures[nom] = (_vo2_to_pace(vo2_high), _vo2_to_pace(vo2_low))
    return allures


def _vo2_to_pace(vo2_val):
    """Convertit une valeur VO2 en allure (min/km). Retourne None si impossible."""
    import numpy as np
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


def format_pace(pace_min_per_km):
    """
    Formate une allure en min/km vers la notation M'SS".
    Ex: 4.5 → "4'30\""
    """
    if pace_min_per_km is None:
        return "\u2014"
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}'{seconds:02d}\""
