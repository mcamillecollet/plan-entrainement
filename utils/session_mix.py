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
        PHASE_SPECIFIC: [(AS,  0.40), (SL, 0.60)],
        PHASE_TAPER:    [(VMA, 0.35), (EF, 0.65)],
    },
    ("5km", 3): {
        PHASE_BASE:     [(EF, 0.30), (VMA, 0.30), (SL, 0.40)],
        PHASE_SPECIFIC: [(EF, 0.25), (AS,  0.30), (SL, 0.45)],
        PHASE_TAPER:    [(EF, 0.40), (VMA, 0.25), (EF, 0.35)],
    },
    ("5km", 4): {
        PHASE_BASE:     [(EF, 0.25), (VMA, 0.20), (SEUIL, 0.15), (SL, 0.40)],
        PHASE_SPECIFIC: [(EF, 0.20), (VMA, 0.15), (AS,    0.20), (SL, 0.45)],
        PHASE_TAPER:    [(EF, 0.35), (VMA, 0.20), (AS,    0.15), (EF, 0.30)],
    },
    ("5km", 5): {
        PHASE_BASE:     [(EF, 0.20), (EF, 0.15), (VMA, 0.20), (SEUIL, 0.15), (SL, 0.30)],
        PHASE_SPECIFIC: [(EF, 0.20), (EF, 0.15), (VMA, 0.15), (AS,    0.20), (SL, 0.30)],
        PHASE_TAPER:    [(EF, 0.30), (EF, 0.20), (VMA, 0.15), (AS,    0.15), (EF, 0.20)],
    },
    # ---------- 10 km ----------
    ("10km", 3): {
        PHASE_BASE:     [(EF, 0.25), (VMA, 0.25), (SL, 0.50)],
        PHASE_SPECIFIC: [(EF, 0.25), (AS,  0.25), (SL, 0.50)],
        PHASE_TAPER:    [(EF, 0.40), (AS,  0.25), (EF, 0.35)],
    },
    ("10km", 4): {
        PHASE_BASE:     [(EF, 0.25), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.45)],
        PHASE_SPECIFIC: [(EF, 0.20), (SEUIL, 0.15), (AS, 0.20), (SL, 0.45)],
        PHASE_TAPER:    [(EF, 0.30), (SEUIL, 0.15), (AS, 0.20), (EF, 0.35)],
    },
    ("10km", 5): {
        PHASE_BASE:     [(EF, 0.20), (EF, 0.15), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.35)],
        PHASE_SPECIFIC: [(EF, 0.15), (EF, 0.15), (SEUIL, 0.15), (AS, 0.20), (SL, 0.35)],
        PHASE_TAPER:    [(EF, 0.25), (EF, 0.20), (SEUIL, 0.15), (AS, 0.15), (EF, 0.25)],
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
        PHASE_BASE:     [(EF, 0.20), (EF, 0.15), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.35)],
        PHASE_SPECIFIC: [(EF, 0.15), (EF, 0.15), (SEUIL, 0.15), (AS, 0.15), (SL, 0.40)],
        PHASE_TAPER:    [(EF, 0.25), (EF, 0.20), (SEUIL, 0.15), (AS, 0.15), (EF, 0.25)],
    },
    # ---------- Marathon ----------
    ("Marathon", 3): {
        PHASE_BASE:     [(EF, 0.20), (SEUIL, 0.25), (SL, 0.55)],
        PHASE_SPECIFIC: [(EF, 0.15), (SEUIL, 0.20), (SL, 0.65)],
        PHASE_TAPER:    [(EF, 0.40), (AS, 0.15), (EF, 0.45)],
    },
    ("Marathon", 4): {
        PHASE_BASE:     [(EF, 0.20), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.50)],
        PHASE_SPECIFIC: [(EF, 0.20), (SEUIL, 0.15), (AS, 0.20), (SL, 0.45)],
        PHASE_TAPER:    [(EF, 0.35), (SEUIL, 0.15), (AS, 0.15), (EF, 0.35)],
    },
    ("Marathon", 5): {
        PHASE_BASE:     [(EF, 0.15), (EF, 0.15), (VMA, 0.15), (SEUIL, 0.15), (SL, 0.40)],
        PHASE_SPECIFIC: [(EF, 0.15), (EF, 0.15), (SEUIL, 0.15), (AS, 0.15), (SL, 0.40)],
        PHASE_TAPER:    [(EF, 0.25), (EF, 0.20), (SEUIL, 0.15), (AS, 0.15), (EF, 0.25)],
    },
}

# --- Plafonds absolus de sortie longue par type de course (en km) ---
# Au-delà, la SL est cappée et le surplus est réalloué sur l'EF la plus volumineuse
# du mix afin de conserver le volume hebdo total. Les valeurs visent à garder une
# SL cohérente avec la distance cible (pas plus de ~2x la distance course pour 5K/10K,
# ~1.2x pour le semi, ~0.75x pour le marathon).
SL_MAX_KM = {
    "5km":           12,
    "10km":          18,
    "Semi-marathon": 25,
    "Marathon":      35,
}

# --- Planchers physiologiques par type de séance (en km) ---
# En dessous de ces seuils, une séance perd l'essentiel de son intérêt
# (échauffement + récup consomment déjà ~3-4 km pour VMA/Seuil). Si le volume
# hebdo ne permet pas de tenir ces minimums pour toutes les séances du template,
# _enforce_session_minimums() réorganise la semaine (fusion / drop) en
# conservant le volume hebdo total.
MIN_SESSION_KM = {
    EF:    5.0,
    VMA:   6.0,
    SEUIL: 6.0,
    AS:    5.0,
    COTES: 6.0,
    SL:    None,  # borné séparément par SL_MAX_KM
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


def _absorb_overflow(sessions, overflow_km):
    """
    Redistribue un surplus de km (retiré d'une SL cappée) sur une séance non-SL.
    Priorité : la plus grosse EF, puis à défaut n'importe quelle autre séance
    (AS, Seuil, VMA, Côtes) dont le km est le plus grand. Préserve le volume total.
    Nécessaire pour les templates sans EF (ex. 5km 2 sorties = [AS, SL]).
    """
    if overflow_km <= 0:
        return
    ef_targets = [x for x in sessions if x["type"] == EF]
    if ef_targets:
        target = max(ef_targets, key=lambda x: x["km"])
    else:
        non_sl = [x for x in sessions if x["type"] != SL]
        if not non_sl:
            return
        target = max(non_sl, key=lambda x: x["km"])
    target["km"] = round(target["km"] + overflow_km, 1)


def _is_standard_label(label, base):
    """True si `label` est `base` ou `base N` (suffixe numérique). Exclut les
    libellés spéciaux ('Endurance fondamentale (longue)', 'EF détente',
    'Activation (...)') qu'il ne faut pas renommer."""
    if label == base:
        return True
    if label.startswith(f"{base} "):
        suffix = label[len(base) + 1:]
        return suffix.isdigit()
    return False


def _renumber_labels(sessions):
    """Renumérote les libellés standards après que _enforce_session_minimums a pu
    droper ou fusionner des séances, pour éviter d'afficher 'Endurance fondamentale 2'
    alors qu'une seule EF subsiste. Ne touche pas aux libellés spéciaux."""
    type_counts = {}
    for s in sessions:
        type_counts[s["type"]] = type_counts.get(s["type"], 0) + 1
    seen = {}
    for s in sessions:
        t = s["type"]
        base = LABELS.get(t)
        if base is None or not _is_standard_label(s["label"], base):
            continue
        if type_counts[t] > 1:
            idx = seen.get(t, 0) + 1
            seen[t] = idx
            s["label"] = f"{base} {idx}"
        else:
            s["label"] = base


def _enforce_session_minimums(sessions, race_type, phase_group):
    """
    Redistribue les km pour garantir que chaque séance respecte son plancher
    physiologique (voir MIN_SESSION_KM). Séquence par séance sous plancher :

    1. Prendre sur la SL (tant qu'elle reste ≥ SL_MAX_KM × 0.4, garde-fou).
    2. Prendre sur la plus grosse EF donneuse (qui reste ≥ MIN_SESSION_KM[EF]).
    3. Sinon : DROP la séance et rediriger ses km vers (a) une séance jumelle
       du même type si elle existe, (b) à défaut la plus grosse EF, (c) à
       défaut la SL.

    Invariant : `sum(s['km'] for s in sessions)` est préservé (à l'arrondi près).
    La longueur de `sessions` peut diminuer si des séances ont été fusionnées.
    """
    sl_max = SL_MAX_KM.get(race_type)
    sl_reserve = sl_max * 0.4 if sl_max else None

    max_iters = 6
    for _ in range(max_iters):
        changed = False
        for i, s in enumerate(sessions):
            t = s["type"]
            if t == SL:
                continue
            min_km = MIN_SESSION_KM.get(t)
            if min_km is None or s["km"] >= min_km:
                continue

            deficit = round(min_km - s["km"], 1)

            # 1) Prendre sur SL si elle est au-dessus de sa réserve
            if deficit > 0 and sl_reserve is not None:
                for sl in sessions:
                    if sl["type"] != SL:
                        continue
                    available = max(0.0, round(sl["km"] - sl_reserve, 1))
                    take = min(deficit, available)
                    if take > 0:
                        sl["km"] = round(sl["km"] - take, 1)
                        s["km"] = round(s["km"] + take, 1)
                        if "km_as" in sl:
                            sl["km_as"] = round(sl["km"] * 0.15, 1)
                        deficit = round(deficit - take, 1)
                        changed = True
                    break

            # 2) Prendre sur les EF donneuses (hors self) tant qu'il reste un surplus
            if deficit > 0:
                ef_min = MIN_SESSION_KM[EF]
                ef_donors = sorted(
                    [x for x in sessions
                     if x["type"] == EF and x is not s and x["km"] > ef_min],
                    key=lambda x: -x["km"],
                )
                for ef in ef_donors:
                    if deficit <= 0:
                        break
                    available = max(0.0, round(ef["km"] - ef_min, 1))
                    take = min(deficit, available)
                    if take > 0:
                        ef["km"] = round(ef["km"] - take, 1)
                        s["km"] = round(s["km"] + take, 1)
                        deficit = round(deficit - take, 1)
                        changed = True

            # 3) Drop si le déficit persiste — fusion avec un jumeau, sinon EF, sinon SL
            if deficit > 0 and s["km"] < min_km:
                dropped_km = s["km"]
                twin = next(
                    (x for x in sessions if x["type"] == t and x is not s),
                    None,
                )
                if twin is not None:
                    twin["km"] = round(twin["km"] + dropped_km, 1)
                else:
                    ef_targets = [x for x in sessions
                                  if x["type"] == EF and x is not s]
                    if ef_targets:
                        target = max(ef_targets, key=lambda x: x["km"])
                        target["km"] = round(target["km"] + dropped_km, 1)
                    else:
                        sl_targets = [x for x in sessions if x["type"] == SL]
                        if sl_targets:
                            sl_targets[0]["km"] = round(
                                sl_targets[0]["km"] + dropped_km, 1
                            )
                            if "km_as" in sl_targets[0]:
                                sl_targets[0]["km_as"] = round(
                                    sl_targets[0]["km"] * 0.15, 1
                                )
                sessions.pop(i)
                changed = True
                break  # repartir du début avec la liste modifiée

        if not changed:
            break

    _renumber_labels(sessions)

    # Si une fusion a poussé la SL au-dessus du cap, recapper proprement.
    if sl_max is not None:
        for s in sessions:
            if s["type"] == SL and s["km"] > sl_max:
                overflow = round(s["km"] - sl_max, 1)
                s["km"] = float(sl_max)
                if "km_as" in s:
                    s["km_as"] = round(sl_max * 0.15, 1)
                _absorb_overflow(sessions, overflow)

    return sessions


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
        return _enforce_session_minimums(sessions, race_type, phase_group)

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

    # --- Cap absolu de la sortie longue ---
    # Si la SL calculée dépasse le plafond pour ce type de course, on la borne et on
    # redistribue le surplus sur la plus grosse séance d'EF du mix (pour conserver
    # le volume total hebdo). Ne s'applique qu'aux séances encore de type SL
    # (exclut donc le cas 2 sorties/semaine converti en EF longue ci-dessus).
    sl_max = SL_MAX_KM.get(race_type)
    if sl_max is not None:
        for s in sessions:
            if s["type"] == SL and s["km"] > sl_max:
                overflow = round(s["km"] - sl_max, 1)
                s["km"] = float(sl_max)
                if "km_as" in s:
                    s["km_as"] = round(sl_max * 0.15, 1)
                _absorb_overflow(sessions, overflow)

    # --- Plancher minimum par séance ---
    # Garantit qu'aucune séance ne tombe sous son plancher physiologique (cf. MIN_SESSION_KM).
    # Peut fusionner / supprimer des séances si le volume hebdo ne permet pas de tenir toutes
    # les séances du template au-dessus de leur plancher — le volume total est préservé.
    sessions = _enforce_session_minimums(sessions, race_type, phase_group)

    # --- Cible minimale pour la SL en phase specific ---
    # Garantit que la SL peut atteindre SL_MAX_KM quel que soit le niveau et le
    # nombre de sorties, tant que le volume hebdo le permet. On puise le déficit
    # sur les séances EF du mix (de la plus grosse à la plus petite), sans
    # descendre sous MIN_SESSION_KM[EF]. Ainsi, un plan Débutant marathon
    # avec 5 sorties (pic 60 km, SL naturelle 30 km) peut quand même atteindre
    # une SL de 35 km en phase specific (dans la limite du surplus EF disponible).
    if sl_max is not None and phase_group == PHASE_SPECIFIC:
        min_ef_km = MIN_SESSION_KM[EF]
        for s in sessions:
            if s["type"] == SL and s["km"] < sl_max:
                deficit = round(sl_max - s["km"], 1)
                remaining = deficit
                ef_sessions = sorted(
                    [x for x in sessions if x["type"] == EF],
                    key=lambda x: -x["km"],
                )
                for ef in ef_sessions:
                    if remaining <= 0:
                        break
                    available = max(0.0, round(ef["km"] - min_ef_km, 1))
                    take = min(remaining, available)
                    if take > 0:
                        ef["km"] = round(ef["km"] - take, 1)
                        remaining = round(remaining - take, 1)
                total_boost = round(deficit - remaining, 1)
                if total_boost > 0:
                    s["km"] = round(s["km"] + total_boost, 1)
                    if "km_as" in s:
                        s["km_as"] = round(s["km"] * 0.15, 1)

    return sessions
