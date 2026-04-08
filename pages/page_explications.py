import streamlit as st
from shared import inject_css


def render():
    inject_css()

    st.markdown("# Explications des types de séances")
    st.markdown('<p class="section-label">Comprendre les différents types d\'entraînement</p>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # --- Tableau récapitulatif ---
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

    # --- Style partagé pour les blocs d'explication ---
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

    # --- 1. Endurance fondamentale ---
    st.markdown(f"""
<div style="{card_style}">
  <p style="{title_style}">1. Endurance fondamentale (EF)</p>
  <p style="{subtitle_style}">Base aérobique</p>

  <p style="{question_style}">C'est quoi ?</p>
  <p style="{text_style}">
    Une course très confortable, où tu peux parler sans effort.<br>
    C'est l'allure la plus lente… et pourtant la plus importante.
  </p>

  <p style="{question_style}">Objectif de la séance</p>
  <ul style="{li_style}">
    <li>Construire la base aérobique, indispensable pour progresser</li>
    <li>Apprendre au corps à utiliser les graisses pour produire de l'énergie</li>
    <li>Renforcer le cœur et améliorer le souffle</li>
    <li>Favoriser la récupération entre les séances difficiles</li>
    <li>Prévenir les blessures (séance la moins traumatisante)</li>
  </ul>

  <p style="{question_style}">À quoi ça ressemble ?</p>
  <ul style="{example_style}">
    <li>30 à 60 min à allure "cool", parfois plus pour les sorties longues</li>
    <li>Conversation possible sans être essoufflé(e)</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # --- 2. Seuil / Tempo ---
    st.markdown(f"""
<div style="{card_style}">
  <p style="{title_style}">2. Seuil / Tempo</p>
  <p style="{subtitle_style}">Endurance haute intensité</p>

  <p style="{question_style}">C'est quoi ?</p>
  <p style="{text_style}">
    Une allure soutenue mais contrôlée.<br>
    Tu cours vite, mais tu ne sprintes pas.<br>
    Tu peux dire quelques mots, pas tenir une conversation.
  </p>

  <p style="{question_style}">Objectif de la séance</p>
  <ul style="{li_style}">
    <li>Repousser ton seuil lactique (supporter un effort plus intense sans exploser)</li>
    <li>Mieux gérer les efforts continus (10 km, semi…)</li>
    <li>Améliorer l'endurance à haute intensité</li>
    <li>Apprendre à stabiliser ton rythme et ta respiration sous stress</li>
  </ul>

  <p style="{question_style}">À quoi ça ressemble ?</p>
  <ul style="{example_style}">
    <li>2 × 10 min tempo</li>
    <li>3 × 8 min seuil</li>
    <li>Effort "dur mais gérable"</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # --- 3. VMA / Intervalles ---
    st.markdown(f"""
<div style="{card_style}">
  <p style="{title_style}">3. VMA / Intervalles</p>
  <p style="{subtitle_style}">Vitesse maximale aérobie</p>

  <p style="{question_style}">C'est quoi ?</p>
  <p style="{text_style}">
    Des efforts courts et rapides, souvent sous forme d'intervalles (ex : 1 min vite / 1 min lent).
  </p>

  <p style="{question_style}">Objectif de la séance</p>
  <ul style="{li_style}">
    <li>Augmenter la vitesse maximale aérobie (VMA)</li>
    <li>Améliorer la VO₂max, c'est-à-dire ta capacité à utiliser l'oxygène</li>
    <li>Rendre les allures plus rapides plus faciles à tenir</li>
    <li>Améliorer la coordination et la technique en vitesse</li>
    <li>Créer un "réservoir de vitesse" pour les autres allures</li>
  </ul>

  <p style="{question_style}">À quoi ça ressemble ?</p>
  <ul style="{example_style}">
    <li>10 × 30 sec rapides / 30 sec lentes</li>
    <li>8 × 400 m vifs</li>
    <li>Intensité élevée mais efforts courts</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # --- 4. Allure spécifique ---
    st.markdown(f"""
<div style="{card_style}">
  <p style="{title_style}">4. Allure spécifique (AS)</p>
  <p style="{subtitle_style}">Rythme cible de course</p>

  <p style="{question_style}">C'est quoi ?</p>
  <p style="{text_style}">
    C'est la vitesse que tu veux tenir le jour de ta course :<br>
    allure 10 km, allure semi, allure marathon.
  </p>

  <p style="{question_style}">Objectif de la séance</p>
  <ul style="{li_style}">
    <li>Apprendre à ton corps à tenir l'allure exacte de l'objectif</li>
    <li>Calibrer ton pacing (éviter de partir trop vite)</li>
    <li>Habituer ton mental et ton souffle au rythme cible</li>
    <li>Simuler la sensation de course</li>
    <li>Vérifier si ton objectif est réaliste</li>
  </ul>

  <p style="{question_style}">À quoi ça ressemble ?</p>
  <ul style="{example_style}">
    <li>3 × 2 km allure 10 km</li>
    <li>2 × 5 km allure semi</li>
    <li>Effort régulier, sans sprint</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # --- 5. Sortie longue ---
    st.markdown(f"""
<div style="{card_style}">
  <p style="{title_style}">5. Sortie longue (SL)</p>
  <p style="{subtitle_style}">Endurance totale</p>

  <p style="{question_style}">C'est quoi ?</p>
  <p style="{text_style}">
    La séance la plus longue de la semaine, courue à allure lente, parfois avec une petite portion plus rapide en fin.
  </p>

  <p style="{question_style}">Objectif de la séance</p>
  <ul style="{li_style}">
    <li>Construire l'endurance musculaire et mentale</li>
    <li>Apprendre à gérer l'effort dans la durée</li>
    <li>Préparer les articulations, tendons et muscles à la distance</li>
    <li>Améliorer la capacité à brûler les graisses</li>
    <li>Tester nutrition, hydratation et matériel (essentiel pour semi / marathon)</li>
  </ul>

  <p style="{question_style}">À quoi ça ressemble ?</p>
  <ul style="{example_style}">
    <li>1h15 à 2h en prépa semi</li>
    <li>1h30 à 2h30 en prépa marathon</li>
    <li>Souvent : 80–90 % lent + 10–20 % allure spécifique</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    # --- 6. Côtes ---
    st.markdown(f"""
<div style="{card_style}">
  <p style="{title_style}">6. Côtes</p>
  <p style="{subtitle_style}">Force et puissance</p>

  <p style="{question_style}">C'est quoi ?</p>
  <p style="{text_style}">
    Des répétitions de montées courtes ou longues, avec récup en descente.
  </p>

  <p style="{question_style}">Objectif de la séance</p>
  <ul style="{li_style}">
    <li>Développer la force des jambes (quadriceps, mollets, fessiers)</li>
    <li>Améliorer la puissance et la foulée</li>
    <li>Travailler la technique naturelle (levée de genou, posture droite, poussée)</li>
    <li>Faire du travail intense mais moins traumatisant que la VMA sur le plat</li>
    <li>Améliorer la stabilité et la coordination</li>
  </ul>

  <p style="{question_style}">À quoi ça ressemble ?</p>
  <ul style="{example_style}">
    <li>10 × 20–30 sec en côte</li>
    <li>6 × 1 min montée / récupération en marchant</li>
    <li>Puissant mais contrôlé</li>
  </ul>
</div>
""", unsafe_allow_html=True)
