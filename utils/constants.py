# constants.py — couleurs de l'application et limites de volume d'entraînement

# --- Couleurs principales ---
COLOR_PRIMARY = "#B0B0B0"
COLOR_SECONDARY = "#93A5CF"  # Pantone 6099 C

# --- Style partagé pour les graphiques matplotlib ---
CHART_BG = "#E8E8E8"
CHART_LINE_ASCENT = "#D04D46"   # Pantone 6047 C
CHART_LINE_DESCENT = "#5A77B5"  # Pantone 6102 C
CHART_FILL_ASCENT = "#D04D46"
CHART_FILL_DESCENT = "#5A77B5"
CHART_HIGHLIGHT = "#D04D46"

# --- Limites de volume pic (km/semaine) par type de course et niveau ---
# Format : (min_pic, max_pic)
VOLUME_PIC_LIMITS = {
    ("5km", "Débutant"):                (10, 20),
    ("5km", "Intermédiaire"):           (20, 30),
    ("5km", "Avancé"):                  (30, 50),
    ("10km", "Débutant"):               (20, 30),
    ("10km", "Intermédiaire"):          (30, 45),
    ("10km", "Avancé"):                 (45, 70),
    ("Semi-marathon", "Débutant"):      (25, 40),
    ("Semi-marathon", "Intermédiaire"): (40, 60),
    ("Semi-marathon", "Avancé"):        (60, 80),
    ("Marathon", "Débutant"):           (40, 60),
    ("Marathon", "Intermédiaire"):      (60, 80),
    ("Marathon", "Avancé"):             (70, 80),
}
