# Plan d'entraînement

Application Streamlit de génération de plans d'entraînement personnalisés pour la course à pied, avec analyse de parcours GPX.

## Fonctionnalités

- **Analyse GPX** : import d'un fichier GPX, visualisation du profil d'altitude, détection automatique des côtes et descentes > 200 m
- **Plan personnalisé** : génération d'un plan semaine par semaine selon le niveau, le type de course, le volume et la durée de préparation
- **Estimation VDOT** : calcul des zones d'allure d'entraînement à partir d'un chrono actuel ou cible (méthode Jack Daniels)
- **Explications** : guide des différents types de séances (EF, seuil, VMA, allure spécifique, sortie longue, côtes)

## Lancer l'application

```bash
pip install -r requirements.txt
streamlit run plan_entrainement.py
```

L'application tourne sur [localhost:8501](http://localhost:8501) par défaut.

## Structure du projet

```
plan_entrainement.py       # Point d'entrée — navigation et layout global
requirements.txt
README.md

pages/
  page_accueil.py          # Page d'accueil avec animation
  page_analyse.py          # Import GPX et visualisation du parcours
  page_plan.py             # Formulaire et génération du plan
  page_explications.py     # Guide des types de séances

utils/
  constants.py             # Couleurs, constantes graphiques, limites de volume
  styles.py                # CSS Streamlit et style matplotlib partagés
  gpx.py                   # Parsing et analyse des fichiers GPX
  vdot.py                  # Estimation VDOT, zones d'allure, parsing chrono
  plan.py                  # Génération du plan d'entraînement

.streamlit/
  config.toml              # Thème sombre

.devcontainer/
  devcontainer.json        # Config GitHub Codespaces
```

## Dépendances

- [Streamlit](https://streamlit.io/) — interface web
- [gpxpy](https://github.com/tkrajina/gpxpy) — parsing GPX
- [pandas](https://pandas.pydata.org/) / [numpy](https://numpy.org/) — traitement des données
- [matplotlib](https://matplotlib.org/) — graphiques
