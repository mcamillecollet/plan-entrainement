# plan.py — génération du plan d'entraînement personnalisé semaine par semaine

import pandas as pd
from utils.constants import VOLUME_PIC_LIMITS


def get_volume_pic_range(type_course, niveau):
    """Retourne (min, max) du volume pic recommandé pour le type de course et le niveau donnés."""
    return VOLUME_PIC_LIMITS.get((type_course, niveau), (15, 80))


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
            volume_total = volume_pic * 0.35
            sem_type = 'Race Week'

        is_long_run = (semaine % 2 == 1)
        row = _repartir_seances(volume_total, sem_type, semaine, sorties_par_semaine, is_long_run)
        plan.append(row)

    return pd.DataFrame(plan)


def _repartir_seances(volume_total, sem_type, semaine, sorties_par_semaine, is_long_run):
    """
    Répartit le volume total entre les séances selon le nombre de sorties par semaine.
    Retourne un dict représentant une ligne du plan.
    """
    if sorties_par_semaine == 2:
        quali_km = round(volume_total * 0.40, 1)
        sortie_longue_km = round(volume_total * 0.60, 1)
        if is_long_run:
            as_km = round(sortie_longue_km * 0.15, 1)
            detail = f"Long Run ({round(sortie_longue_km - as_km, 1)}) + AS ({as_km})"
        else:
            detail = f"EF ({sortie_longue_km})"
        return {
            'Semaine': semaine, 'Type': sem_type,
            'Qualitative seuil/VMA (km)': quali_km,
            'Sortie longue ou EF (km)': sortie_longue_km,
            'Détail sortie longue': detail,
            'Volume total (km)': round(volume_total, 1)
        }

    elif sorties_par_semaine == 3:
        ef_km = round(volume_total * 0.25, 1)
        quali_km = round(volume_total * 0.25, 1)
        sortie_longue_km = round(volume_total * 0.50, 1)
        as_km = round(sortie_longue_km * 0.15, 1)
        return {
            'Semaine': semaine, 'Type': sem_type,
            'EF (km)': ef_km,
            'Qualitative VMA/seuil/côtes (km)': quali_km,
            'Sortie longue (km)': sortie_longue_km,
            'dont AS (km)': as_km,
            'Volume total (km)': round(volume_total, 1)
        }

    else:  # 4 sorties
        ef_km = round(volume_total * 0.20, 1)
        quali1_km = round(volume_total * 0.15, 1)
        quali2_km = round(volume_total * 0.15, 1)
        sortie_longue_km = round(volume_total * 0.50, 1)
        as_km = round(sortie_longue_km * 0.15, 1)
        return {
            'Semaine': semaine, 'Type': sem_type,
            'EF (km)': ef_km,
            'Qualitative 1 VMA (km)': quali1_km,
            'Qualitative 2 seuil/côtes (km)': quali2_km,
            'Sortie longue (km)': sortie_longue_km,
            'dont AS (km)': as_km,
            'Volume total (km)': round(volume_total, 1)
        }
