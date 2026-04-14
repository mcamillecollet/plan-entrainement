# plan.py — génération du plan d'entraînement personnalisé semaine par semaine

import pandas as pd
from utils.constants import VOLUME_PIC_LIMITS
from utils.session_mix import compute_sessions, get_phase_group


def get_volume_pic_range(type_course, niveau):
    """Retourne (min, max) du volume pic recommandé pour le type de course et le niveau donnés."""
    return VOLUME_PIC_LIMITS.get((type_course, niveau), (15, 80))


def deriver_volumes(type_course, niveau, sorties_par_semaine, sorties_options):
    """
    Dérive (volume_debut, volume_pic) en km/semaine à partir :
    - de la fourchette VOLUME_PIC_LIMITS[(type, niveau)]
    - de la position de `sorties_par_semaine` dans `sorties_options`.
      Le pic atteint au minimum 70 % de la fourchette [pic_min, pic_max] même avec peu
      de sorties, et atteint pic_max au nombre maximum de sorties. Le nombre de sorties
      garde donc un léger effet sur le plafond sans pour autant ramener au bas de la
      fourchette.
    - d'un volume de départ à 60 % du pic (plancher 5 km).
    """
    pic_min, pic_max = get_volume_pic_range(type_course, niveau)
    n_min, n_max = sorties_options[0], sorties_options[-1]
    if n_max > n_min:
        ratio = (sorties_par_semaine - n_min) / (n_max - n_min)
    else:
        ratio = 1.0
    # Interpolation entre 0.7*fourchette (min sorties) et 1.0*fourchette (max sorties).
    effective_ratio = 0.7 + 0.3 * ratio
    volume_pic = round(pic_min + effective_ratio * (pic_max - pic_min))
    volume_debut = max(5, round(volume_pic * 0.60))
    return volume_debut, volume_pic


def generer_plan_personnalise(niveau, type_course, volume_debut, volume_pic,
                              duree_semaine, sorties_par_semaine, D_plus):
    """
    Génère un plan d'entraînement personnalisé sous forme de DataFrame.

    Phases du plan :
    - Under progress : progression linéaire du volume
    - Cool down      : semaines allégées (~70%) pour la récupération
    - Peak           : semaine au volume maximum
    - Recovery       : descente progressive avant la course
    - Race Week      : semaine de course (~35% du volume pic)

    Chaque ligne du DataFrame expose une colonne 'Séances' : liste de dicts
    {type, label, km[, km_as]} produite par utils.session_mix.compute_sessions.
    Le mix dépend à la fois du type de course, du nombre de sorties/semaine
    et de la phase (base / specific / taper).
    """
    plan = []

    # Nombre de semaines de redescente avant la course
    semaines_redescente = 2 if duree_semaine >= 10 else 1
    semaines_build = duree_semaine - semaines_redescente - 1 - 1  # -1 pic, -1 course
    semaine_pic = semaines_build + 1

    # Placement des semaines allégées dans la phase de progression
    semaines_allegees = set()
    if duree_semaine > 14:
        t1 = round(semaine_pic / 3)
        t2 = round(2 * semaine_pic / 3)
        semaines_allegees = {t1, t2}
    elif duree_semaine >= 12:
        milieu = (semaine_pic + 1) // 2
        semaines_allegees = {milieu}

    nb_prog = sum(1 for s in range(1, semaines_build + 1) if s not in semaines_allegees)

    # Le build plafonne à 90% du pic
    volume_build_max = volume_pic * 0.90
    if nb_prog > 1 and volume_build_max > volume_debut:
        increment = (volume_build_max - volume_debut) / (nb_prog - 1)
    else:
        increment = 0

    current_volume = volume_debut
    prog_count = 0

    for semaine in range(1, duree_semaine + 1):
        if semaine <= semaines_build:
            if semaine in semaines_allegees:
                volume_total = current_volume * 0.70
                sem_type = 'Cool down'
            else:
                current_volume = min(volume_debut + prog_count * increment, volume_build_max)
                volume_total = current_volume
                prog_count += 1
                sem_type = 'Under progress'
        elif semaine == semaine_pic:
            volume_total = volume_pic
            sem_type = 'Peak'
        elif semaine < duree_semaine:
            step = semaine - semaine_pic
            coef = 0.70 if (semaines_redescente == 2 and step == 1) else 0.50
            volume_total = volume_pic * coef
            sem_type = 'Recovery'
        else:
            # Race Week plafonnée à 18 km pour éviter une dernière semaine
            # trop chargée lorsque le volume pic est élevé (ex. pic 80 km → 24 km sans cap).
            volume_total = min(volume_pic * 0.30, 18)
            sem_type = 'Race Week'

        phase_group = get_phase_group(sem_type, semaine, semaine_pic)
        seances = compute_sessions(
            volume_total, type_course, sorties_par_semaine, phase_group, semaine
        )

        plan.append({
            'Semaine': semaine,
            'Type': sem_type,
            'Phase': phase_group,
            'Volume total (km)': round(volume_total, 1),
            'Séances': seances,
        })

    return pd.DataFrame(plan)
