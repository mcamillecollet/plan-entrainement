import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Plan Entraînement", layout="wide")

# Titre et introduction
st.title("💪 Plan d'Entraînement Personnalisé")
st.write("""
Bienvenue dans votre application de planification d'entraînement !  
Sélectionnez la semaine et découvrez vos séances de course et de renforcement.
""")

# Slider pour sélectionner la semaine
semaine = st.slider("Choisissez la semaine", 1, 12, 1)

# Exemple de plan sur 12 semaines (jour par jour)
plan = {
    1: {"Lundi":"Course 3x10 min","Mercredi":"Renfo 2x15 min","Vendredi":"Course 20 min"},
    2: {"Lundi":"Course 4x10 min","Mercredi":"Renfo 2x20 min","Vendredi":"Course 25 min"},
    3: {"Lundi":"Course 3x15 min","Mercredi":"Renfo 3x15 min","Vendredi":"Repos actif"},
    4: {"Lundi":"Course 25 min","Mercredi":"Renfo 3x20 min","Vendredi":"Course 30 min"},
    5: {"Lundi":"Course 30 min","Mercredi":"Renfo 3x20 min","Vendredi":"Course fractionné"},
    6: {"Lundi":"Course 35 min","Mercredi":"Renfo 3x25 min","Vendredi":"Repos actif"},
    7: {"Lundi":"Course 40 min","Mercredi":"Renfo 3x25 min","Vendredi":"Course 30 min"},
    8: {"Lundi":"Course fractionné","Mercredi":"Renfo 4x20 min","Vendredi":"Course 35 min"},
    9: {"Lundi":"Course 45 min","Mercredi":"Renfo 4x25 min","Vendredi":"Repos actif"},
    10: {"Lundi":"Course 50 min","Mercredi":"Renfo 4x25 min","Vendredi":"Course fractionné"},
    11: {"Lundi":"Course 55 min","Mercredi":"Renfo 3x30 min","Vendredi":"Course 40 min"},
    12: {"Lundi":"Course 60 min","Mercredi":"Renfo 3x30 min","Vendredi":"Repos actif"},
}

# Créer un DataFrame pour afficher joliment
df_semaine = pd.DataFrame(plan[semaine].items(), columns=["Jour", "Séance"])
st.subheader(f"Semaine {semaine} : Détails des séances")
st.table(df_semaine)

# Visualisation simple du volume d'entraînement
volumes = []
for jour in plan[semaine].values():
    # extraire minutes approximatives
    import re
    minutes = re.findall(r'\d+', jour)
    volumes.append(sum(int(m) for m in minutes) if minutes else 0)

plt.figure(figsize=(6,3))
plt.bar(df_semaine["Jour"], volumes, color='skyblue')
plt.title(f"Volume approximatif en minutes - Semaine {semaine}")
plt.ylabel("Minutes")
st.pyplot(plt)