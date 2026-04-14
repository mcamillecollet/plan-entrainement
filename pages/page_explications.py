import streamlit as st
from utils import inject_css


def render():
    inject_css()

    st.markdown("# Explications des types de séances")
    st.markdown('<p class="section-label">Comprendre les différents types d\'entraînement</p>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    st.markdown("""
<div style="overflow-x: auto; margin-bottom: 2.5rem;">
<table style="width: 100%; border-collapse: separate; border-spacing: 0;
              border-radius: 10px; overflow: hidden;
              font-family: 'Outfit', sans-serif; font-size: 0.92rem;">
  <thead>
    <tr style="background: #4A4A4A;">
      <th style="padding: 0.85rem 1.2rem; text-align: left; color: #F0F0F0;
                 font-weight: 600; letter-spacing: 0.02em; border-bottom: 2px solid #D04D46;">Séance</th>
      <th style="padding: 0.85rem 1.2rem; text-align: left; color: #F0F0F0;
                 font-weight: 600; letter-spacing: 0.02em; border-bottom: 2px solid #D04D46;">Objectif principal</th>
      <th style="padding: 0.85rem 1.2rem; text-align: left; color: #F0F0F0;
                 font-weight: 600; letter-spacing: 0.02em; border-bottom: 2px solid #D04D46;">Objectifs secondaires</th>
    </tr>
  </thead>
  <tbody>
    <tr style="background: #3A3A3A;">
      <td style="padding: 0.7rem 1.2rem; color: #E0E0E0; border-bottom: 1px solid #4A4A4A;"><strong>Endurance fondamentale</strong></td>
      <td style="padding: 0.7rem 1.2rem; color: #CCCCCC; border-bottom: 1px solid #4A4A4A;">Construire la base</td>
      <td style="padding: 0.7rem 1.2rem; color: #AAAAAA; border-bottom: 1px solid #4A4A4A;">Récup, prévention blessures</td>
    </tr>
    <tr style="background: #353535;">
      <td style="padding: 0.7rem 1.2rem; color: #E0E0E0; border-bottom: 1px solid #4A4A4A;"><strong>Seuil / Tempo</strong></td>
      <td style="padding: 0.7rem 1.2rem; color: #CCCCCC; border-bottom: 1px solid #4A4A4A;">Tenir un rythme soutenu</td>
      <td style="padding: 0.7rem 1.2rem; color: #AAAAAA; border-bottom: 1px solid #4A4A4A;">Seuil lactique, régulation</td>
    </tr>
    <tr style="background: #3A3A3A;">
      <td style="padding: 0.7rem 1.2rem; color: #E0E0E0; border-bottom: 1px solid #4A4A4A;"><strong>VMA / Intervalles</strong></td>
      <td style="padding: 0.7rem 1.2rem; color: #CCCCCC; border-bottom: 1px solid #4A4A4A;">Développer la vitesse</td>
      <td style="padding: 0.7rem 1.2rem; color: #AAAAAA; border-bottom: 1px solid #4A4A4A;">VO₂max, coordination</td>
    </tr>
    <tr style="background: #353535;">
      <td style="padding: 0.7rem 1.2rem; color: #E0E0E0; border-bottom: 1px solid #4A4A4A;"><strong>Allure spécifique</strong></td>
      <td style="padding: 0.7rem 1.2rem; color: #CCCCCC; border-bottom: 1px solid #4A4A4A;">Habituer au rythme de course</td>
      <td style="padding: 0.7rem 1.2rem; color: #AAAAAA; border-bottom: 1px solid #4A4A4A;">Pacing, confiance</td>
    </tr>
    <tr style="background: #3A3A3A;">
      <td style="padding: 0.7rem 1.2rem; color: #E0E0E0; border-bottom: 1px solid #4A4A4A;"><strong>Sortie longue</strong></td>
      <td style="padding: 0.7rem 1.2rem; color: #CCCCCC; border-bottom: 1px solid #4A4A4A;">Endurance totale</td>
      <td style="padding: 0.7rem 1.2rem; color: #AAAAAA; border-bottom: 1px solid #4A4A4A;">Nutrition, mental</td>
    </tr>
    <tr style="background: #353535;">
      <td style="padding: 0.7rem 1.2rem; color: #E0E0E0;"><strong>Côtes</strong></td>
      <td style="padding: 0.7rem 1.2rem; color: #CCCCCC;">Force et puissance</td>
      <td style="padding: 0.7rem 1.2rem; color: #AAAAAA;">Technique, stabilité</td>
    </tr>
  </tbody>
</table>
</div>
""", unsafe_allow_html=True)

    card_style = (
        "background: #3A3A3A; border: 1px solid #4A4A4A; border-radius: 10px; "
        "padding: 1.8rem 2rem; margin-bottom: 1.5rem;"
    )
    title_style = (
        "font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 1.25rem; "
        "color: #F0F0F0; margin: 0 0 0.2rem 0;"
    )
    subtitle_style = (
        "font-family: 'Geist Mono', monospace; font-size: 0.7rem; font-weight: 500; "
        "letter-spacing: 0.08em; text-transform: uppercase; color: #D04D46; margin: 0 0 1rem 0;"
    )
    question_style = (
        "font-family: 'Outfit', sans-serif; font-weight: 500; font-size: 1rem; "
        "color: #E0E0E0; margin: 1.2rem 0 0.4rem 0;"
    )
    text_style = (
        "font-family: 'Outfit', sans-serif; font-size: 0.92rem; color: #CCCCCC; "
        "line-height: 1.6; margin: 0 0 0.3rem 0;"
    )
    li_style = (
        "font-family: 'Outfit', sans-serif; font-size: 0.92rem; color: #CCCCCC; "
        "line-height: 1.8; margin-left: 0.5rem;"
    )
    example_style = (
        "font-family: 'Geist Mono', monospace; font-size: 0.82rem; color: #AAAAAA; "
        "line-height: 1.7; margin-left: 0.5rem;"
    )

    seances = [
        {
            "titre": "1. Endurance fondamentale (EF)",
            "sous_titre": "Base aérobique",
            "quoi": "Une course très confortable, où tu peux parler sans effort.<br>C'est l'allure la plus lente… et pourtant la plus importante.",
            "objectifs": [
                "Construire la base aérobique, indispensable pour progresser",
                "Apprendre au corps à utiliser les graisses pour produire de l'énergie",
                "Renforcer le cœur et améliorer le souffle",
                "Favoriser la récupération entre les séances difficiles",
                "Prévenir les blessures (séance la moins traumatisante)",
            ],
            "exemples": [
                "30 à 60 min à allure &laquo; cool &raquo;, parfois plus pour les sorties longues",
                "Conversation possible sans être essoufflé(e)",
            ],
        },
        {
            "titre": "2. Seuil / Tempo",
            "sous_titre": "Endurance haute intensité",
            "quoi": "Une allure soutenue mais contrôlée.<br>Tu cours vite, mais tu ne sprintes pas.<br>Tu peux dire quelques mots, pas tenir une conversation.",
            "objectifs": [
                "Repousser ton seuil lactique (supporter un effort plus intense sans exploser)",
                "Mieux gérer les efforts continus (10 km, semi…)",
                "Améliorer l'endurance à haute intensité",
                "Apprendre à stabiliser ton rythme et ta respiration sous stress",
            ],
            "exemples": ["2 × 10 min tempo", "3 × 8 min seuil", "Effort &laquo; dur mais gérable &raquo;"],
        },
        {
            "titre": "3. VMA / Intervalles",
            "sous_titre": "Vitesse maximale aérobie",
            "quoi": "Des efforts courts et rapides, souvent sous forme d'intervalles (ex : 1 min vite / 1 min lent).",
            "objectifs": [
                "Augmenter la vitesse maximale aérobie (VMA)",
                "Améliorer la VO₂max, c'est-à-dire ta capacité à utiliser l'oxygène",
                "Rendre les allures plus rapides plus faciles à tenir",
                "Améliorer la coordination et la technique en vitesse",
                "Créer un &laquo; réservoir de vitesse &raquo; pour les autres allures",
            ],
            "exemples": ["10 × 30 sec rapides / 30 sec lentes", "8 × 400 m vifs", "Intensité élevée mais efforts courts"],
        },
        {
            "titre": "4. Allure spécifique (AS)",
            "sous_titre": "Rythme cible de course",
            "quoi": "C'est la vitesse que tu veux tenir le jour de ta course :<br>allure 10 km, allure semi, allure marathon.",
            "objectifs": [
                "Apprendre à ton corps à tenir l'allure exacte de l'objectif",
                "Calibrer ton pacing (éviter de partir trop vite)",
                "Habituer ton mental et ton souffle au rythme cible",
                "Simuler la sensation de course",
                "Vérifier si ton objectif est réaliste",
            ],
            "exemples": ["3 × 2 km allure 10 km", "2 × 5 km allure semi", "Effort régulier, sans sprint"],
        },
        {
            "titre": "5. Sortie longue (SL)",
            "sous_titre": "Endurance totale",
            "quoi": "La séance la plus longue de la semaine, courue à allure lente, parfois avec une petite portion plus rapide en fin.",
            "objectifs": [
                "Construire l'endurance musculaire et mentale",
                "Apprendre à gérer l'effort dans la durée",
                "Préparer les articulations, tendons et muscles à la distance",
                "Améliorer la capacité à brûler les graisses",
                "Tester nutrition, hydratation et matériel (essentiel pour semi / marathon)",
            ],
            "exemples": [
                "1h15 à 2h en prépa semi",
                "1h30 à 2h30 en prépa marathon",
                "Souvent : 80–90 % lent + 10–20 % allure spécifique",
            ],
        },
        {
            "titre": "6. Côtes",
            "sous_titre": "Force et puissance",
            "quoi": "Des répétitions de montées courtes ou longues, avec récup en descente.",
            "objectifs": [
                "Développer la force des jambes (quadriceps, mollets, fessiers)",
                "Améliorer la puissance et la foulée",
                "Travailler la technique naturelle (levée de genou, posture droite, poussée)",
                "Faire du travail intense mais moins traumatisant que la VMA sur le plat",
                "Améliorer la stabilité et la coordination",
            ],
            "exemples": [
                "10 × 20–30 sec en côte",
                "6 × 1 min montée / récupération en marchant",
                "Puissant mais contrôlé",
            ],
        },
    ]

    for seance in seances:
        objectifs_html = "\n".join(f'<li style="{li_style}">{o}</li>' for o in seance["objectifs"])
        exemples_html = "\n".join(f'<li style="{example_style}">{e}</li>' for e in seance["exemples"])
        st.markdown(f"""
<div style="{card_style}">
  <p style="{title_style}">{seance['titre']}</p>
  <p style="{subtitle_style}">{seance['sous_titre']}</p>
  <p style="{question_style}">C'est quoi ?</p>
  <p style="{text_style}">{seance['quoi']}</p>
  <p style="{question_style}">Objectif de la séance</p>
  <ul>{objectifs_html}</ul>
  <p style="{question_style}">À quoi ça ressemble ?</p>
  <ul>{exemples_html}</ul>
</div>
""", unsafe_allow_html=True)
