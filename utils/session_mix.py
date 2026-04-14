# session_mix.py — répartition des types de séances selon (type de course, sorties/semaine, phase)
#
# Objectif : remplacer la logique figée de _repartir_seances (ex-utils/plan.py) par un mix
# de séances qui dépend à la fois de la distance cible, du nombre de sorties hebdomadaires
# et de la phase du plan (base / specific / taper).

# --- Constantes de types de séance ---
EF = "EF"         # Endurance fondamentale
VMA = "VMA"       # VMA / Intervalles
SEUIL = "Seuil"   # Seuil / Tempo
AS = "AS"         # Allure spécifique
SL = "SL"         # Sortie longue
COTES = "Côtes"   # Côtes (souvent en substitution de VMA)

# --- Libellés d'affichage associés aux types ---
LABELS = {
    EF:    "Endurance fondamentale",
    VMA:   "VMA / Intervalles",
    SEUIL: "Seuil / Tempo",
    AS:    "Allure spécifique",
    SL:    "Sortie longue",
    COTES: "Côtes",
}

# --- Phases macro : regroupent les phases fines de plan.py ---
# 'base'       → construction aérobie, peu d'allure spécifique
# 'specific'   → préparation spécifique, AS et qualité dominantes
# 'taper'      → affûtage, volume réduit, dernier rappel d'AS
# 'race_week'  → semaine de course : 2 séances seulement (activation + EF détente)
PHASE_BASE = "base"
PHASE_SPECIFIC = "specific"
PHASE_TAPER = "taper"
PHASE_RACE_WEEK = "race_week"


# --- Templates de répartition : pct du volume hebdo par type de séance ---
# Structure : {(race_type, n_sessions): {phase: [(type, pct), ...]}}
# Contraintes : somme des pct par phase == 1.0 ; 1 tuple = 1 séance dans la semaine.
SESSION_MIX_TEMPLATES = {
    # ---------- 5 km ----------
    ("5km", 2): {
        PHASE_BASE:     [(VMA, 0.40), (SL, 0.60)],
        PHASE_SPECIFIC: [(VMA, 0.40), (SL, 0.60)],
        PHASE_TAPER:    [(VMA, 0.35), (EF, 0.65)],
    },
    ("5km", 3): {
        PHASE_BASE:     [(EF, 0.30), (VMA, 0.25), (SL, 0.45)],
        PHASE_SPECIFIC: [(EF, 0.25), (VMA, 0.25), (SL, 0.50)],
        PHASE_TAPER:    [(EF, 0.40), (VMA, 0.25), (EF, 0.35)],
    },
    ("5km", 4): {
        PHASE_BASE:     [(EF, 0.25), (VMA, 0.20), (SEUIL, 0.15), (SL, 0.40)],
        PHASE_SPECIFIC: [(EF, 0.20), (VMA, 0.20), (SEUIL, 0.15), (SL, 0.45)],
        PHASE_TAPER:    [(EF, 0.35), (VMA, 0.20), (AS, 0.10), (EF, 0.35)],
    },
    ("5km", 5): {
        PHASE_BASE:     [(EF, 0.20), (EF, 0.15), (VMA, 0.20), (SEUIL, 0.15), (SL, 0.30)],
        PHASE_SPECIFIC: [(EF, 0.20), (EF, 0.15), (VMA, 0.20), (SEUIL, 0.15), (SL, 0.30)],
        PHASE_TAPER:    [(EF, 0.30), (EF, 0.20), (VMA, 0.15), (AS, 0.10), (EF, 0.25)],
    },
    # ---------- 10 km ----------
    ("10km", 3): {
        PHASE_BASE:     [(EF, 0.25), (VMA, 0.25), (SL, 0.50)],
        PHASE_SPECIFIC: [(EF, 0.20), (SEUIL, 0.25), (SL, 0.55)],
        PHASE_TAPER:    [(EF, 0.40), (VMA, 0.20), (EF, 0.40)],
    },
    ("10km", 4): {
        PHASE_BASE:     [(EF, 0.25), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.45)],
        PHASE_SPECIFIC: [(EF, 0.20), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.50)],
        PHASE_TAPER:    [(EF, 0.35), (VMA, 0.15), (AS, 0.15), (EF, 0.35)],
    },
    ("10km", 5): {
        PHASE_BASE:     [(EF, 0.20), (EF, 0.15), (VMA, 0.12), (SEUIL, 0.13), (SL, 0.40)],
        PHASE_SPECIFIC: [(EF, 0.15), (EF, 0.15), (VMA, 0.12), (SEUIL, 0.13), (SL, 0.45)],
        PHASE_TAPER:    [(EF, 0.30), (EF, 0.20), (VMA, 0.10), (AS, 0.15), (EF, 0.25)],
    },
    # ---------- Semi-marathon ----------
    ("Semi-marathon", 3): {
        PHASE_BASE:     [(EF, 0.25), (SEUIL, 0.25), (SL, 0.50)],
        PHASE_SPECIFIC: [(EF, 0.20), (SEUIL, 0.25), (SL, 0.55)],
        PHASE_TAPER:    [(EF, 0.40), (AS, 0.20), (EF, 0.40)],
    },
    ("Semi-marathon", 4): {
        PHASE_BASE:     [(EF, 0.25), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.45)],
        PHASE_SPECIFIC: [(EF, 0.20), (SEUIL, 0.15), (AS, 0.15), (SL, 0.50)],
        PHASE_TAPER:    [(EF, 0.35), (SEUIL, 0.15), (AS, 0.15), (EF, 0.35)],
    },
    ("Semi-marathon", 5): {
        PHASE_BASE:     [(EF, 0.20), (EF, 0.15), (VMA, 0.12), (SEUIL, 0.13), (SL, 0.40)],
        PHASE_SPECIFIC: [(EF, 0.15), (EF, 0.15), (SEUIL, 0.13), (AS, 0.12), (SL, 0.45)],
        PHASE_TAPER:    [(EF, 0.30), (EF, 0.20), (SEUIL, 0.10), (AS, 0.15), (EF, 0.25)],
    },
    # ---------- Marathon ----------
    ("Marathon", 3): {
        PHASE_BASE:     [(EF, 0.20), (SEUIL, 0.25), (SL, 0.55)],
        PHASE_SPECIFIC: [(EF, 0.15), (SEUIL, 0.20), (SL, 0.65)],
        PHASE_TAPER:    [(EF, 0.40), (AS, 0.15), (EF, 0.45)],
    },
    ("Marathon", 4): {
        PHASE_BASE:     [(EF, 0.20), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.50)],
        PHASE_SPECIFIC: [(EF, 0.15), (SEUIL, 0.15), (AS, 0.15), (SL, 0.55)],
        PHASE_TAPER:    [(EF, 0.35), (SEUIL, 0.15), (AS, 0.15), (EF, 0.35)],
    },
    ("Marathon", 5): {
        PHASE_BASE:     [(EF, 0.15), (EF, 0.15), (VMA, 0.10), (SEUIL, 0.15), (SL, 0.45)],
        PHASE_SPECIFIC: [(EF, 0.15), (EF, 0.15), (SEUIL, 0.10), (AS, 0.10), (SL, 0.50)],
        PHASE_TAPER:    [(EF, 0.25), (EF, 0.20), (SEUIL, 0.10), (AS, 0.20), (EF, 0.25)],
    },
}

# --- Template dédié à la semaine de course : 2 séances max quel que soit n_sessions ---
# Activation (AS/VMA courte) + EF détente. Ne dépend que du type de course.
RACE_WEEK_TEMPLATES = {
    "5km":           [(VMA, 0.40), (EF, 0.60)],
    "10km":          [(AS,  0.40), (EF, 0.60)],
    "Semi-marathon": [(AS,  0.40), (EF, 0.60)],
    "Marathon":      [(AS,  0.40), (EF, 0.60)],
}

# --- Sanity-check à l'import : somme des pct == 1.0 par (course, sorties, phase) ---
for _key, _phases in SESSION_MIX_TEMPLATES.items():
    for _phase, _mix in _phases.items():
        _total = sum(p for _, p in _mix)
        assert abs(_total - 1.0) < 0.01, f"SESSION_MIX_TEMPLATES{_key}[{_phase}] sum={_total}"

for _rt, _mix in RACE_WEEK_TEMPLATES.items():
    _total = sum(p for _, p in _mix)
    assert abs(_total - 1.0) < 0.01, f"RACE_WEEK_TEMPLATES[{_rt}] sum={_total}"


def get_phase_group(sem_type, semaine, semaine_pic):
    """
    Regroupe les phases fines de plan.py en 4 phases macro qui pilotent le mix de séances.

    - Race Week                         → 'race_week' (template dédié 2 séances)
    - Recovery                          → 'taper'
    - Peak                              → 'specific'
    - Under progress / Cool down        → 'base' sur les 2 premiers tiers des semaines de build
                                          puis 'specific' sur le dernier tiers (pré-peak).
    """
    if sem_type == "Race Week":
        return PHASE_RACE_WEEK
    if sem_type == "Recovery":
        return PHASE_TAPER
    if sem_type == "Peak":
        return PHASE_SPECIFIC
    # Under progress ou Cool down : spécifique sur le dernier tiers des semaines de build
    build_end = max(1, semaine_pic - 1)
    threshold = max(1, int(build_end * 2 / 3))
    if semaine > threshold:
        return PHASE_SPECIFIC
    return PHASE_BASE


def _should_substitute_cotes(race_type, phase_group, is_odd_week):
    """
    Indique si la séance VMA d'une semaine doit être remplacée par une séance de Côtes.
    - Marathon : alternance VMA/Côtes (renforcement) hors taper.
    - 5K / 10K / Semi : pas de substitution (la qualité reste axée VMA/Seuil).
    """
    if race_type == "Marathon" and phase_group != PHASE_TAPER and is_odd_week:
        return True
    return False


def compute_sessions(volume_total, race_type, n_sessions, phase_group, semaine):
    """
    À partir d'un volume hebdo et du template (course, sorties, phase), renvoie la liste
    de séances de la semaine.

    Chaque séance est un dict :
        {"type": str, "label": str, "km": float, ["km_as": float]}

    - Pour une séance SL en phase 'specific', on réserve 15 % du kilométrage en AS (km_as).
    - Pour une semaine paire sur Marathon (hors taper), VMA est substituée par Côtes.
    - Pour 2 sorties/semaine, la SL est remplacée par une sortie EF une semaine sur deux
      (alternance historique du plan).
    """
    # --- Race week : template dédié (2 séances, indépendant de n_sessions) ---
    if phase_group == PHASE_RACE_WEEK:
        mix = RACE_WEEK_TEMPLATES.get(race_type)
        if mix is None:
            return []
        sessions = []
        # Labels fixes : "Activation" pour la séance de qualité, "EF détente" pour la récup.
        for idx, (t, pct) in enumerate(mix):
            km = round(volume_total * pct, 1)
            if idx == 0:
                label = f"Activation ({LABELS[t]})"
            else:
                label = "EF détente"
            sessions.append({"type": t, "label": label, "km": km})
        return sessions

    template = SESSION_MIX_TEMPLATES.get((race_type, n_sessions))
    if template is None:
        # Fallback : au cas où une combinaison ne serait pas couverte, on renvoie une liste vide.
        # Les appelants doivent garantir une combinaison valide via SORTIES_PAR_DISTANCE.
        return []

    mix = template.get(phase_group, template[PHASE_BASE])
    is_odd_week = bool(semaine % 2)
    is_long_run_week = is_odd_week  # convention historique : SL les semaines impaires pour 2 sorties

    # Compter les occurrences par type pour numéroter les doublons (EF 1 / EF 2)
    type_counts_total = {}
    for t, _ in mix:
        type_counts_total[t] = type_counts_total.get(t, 0) + 1
    type_counts_seen = {}

    sessions = []
    for (t, pct) in mix:
        km = round(volume_total * pct, 1)

        # Substitution VMA → Côtes pour le Marathon, semaines paires, hors taper
        if t == VMA and _should_substitute_cotes(race_type, phase_group, is_odd_week):
            t_effective = COTES
        else:
            t_effective = t

        # Libellé : suffixe numérique si le type apparaît plusieurs fois dans le mix
        seen = type_counts_seen.get(t, 0) + 1
        type_counts_seen[t] = seen
        if type_counts_total[t] > 1:
            label = f"{LABELS[t_effective]} {seen}"
        else:
            label = LABELS[t_effective]

        session = {"type": t_effective, "label": label, "km": km}

        # Sortie longue avec portion d'allure spécifique en phase 'specific'
        if t_effective == SL and phase_group == PHASE_SPECIFIC:
            session["km_as"] = round(km * 0.15, 1)

        # Cas 2 sorties/semaine : alterner SL ↔ EF long pour les semaines paires
        if n_sessions == 2 and t_effective == SL and not is_long_run_week:
            session["type"] = EF
            session["label"] = "Endurance fondamentale (longue)"
            session.pop("km_as", None)

        sessions.append(session)

    return sessions
