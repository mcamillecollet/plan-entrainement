import streamlit as st
import streamlit.components.v1 as components
from shared import inject_css


def render():
    inject_css()

    # Titre et sous-titre centrés
    st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center;
            text-align: center; padding: 3rem 2rem 0 2rem;">

  <h1 style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 2.8rem;
             letter-spacing: -0.03em; color: #F0F0F0; margin-bottom: 0.5rem;">
    Plan d'entra\u00eenement
  </h1>

  <p style="font-family: 'Geist Mono', monospace; font-size: 0.78rem; font-weight: 400;
            letter-spacing: 0.1em; text-transform: uppercase; color: #888; margin-bottom: 0;">
    Analyse de parcours \u2014 Planification personnalis\u00e9e
  </p>

</div>
""", unsafe_allow_html=True)

    # Animation de deux coureurs style icon (traits épais arrondis)
    runner_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    overflow: hidden;
    padding-top: 40px;
  }

  /* --- Bounce global des coureurs --- */
  .runner-front {
    animation: bounce-front 0.6s ease-in-out infinite;
  }
  .runner-back {
    animation: bounce-back 0.6s ease-in-out infinite;
    animation-delay: 0.3s;
  }
  @keyframes bounce-front {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-5px); }
  }
  @keyframes bounce-back {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-5px); }
  }

  /* --- Bras et jambes animés --- */
  .f-arm-l, .f-arm-r, .f-leg-l, .f-leg-r,
  .b-arm-l, .b-arm-r, .b-leg-l, .b-leg-r {
    transform-box: fill-box;
    transform-origin: top center;
  }

  /* Coureur de devant */
  .f-arm-l  { animation: f-swing-arm-l 0.6s ease-in-out infinite; }
  .f-arm-r  { animation: f-swing-arm-r 0.6s ease-in-out infinite; }
  .f-leg-l  { animation: f-swing-leg-l 0.6s ease-in-out infinite; }
  .f-leg-r  { animation: f-swing-leg-r 0.6s ease-in-out infinite; }

  @keyframes f-swing-arm-l {
    0%, 100% { transform: rotate(-40deg); }
    50%      { transform: rotate(40deg); }
  }
  @keyframes f-swing-arm-r {
    0%, 100% { transform: rotate(40deg); }
    50%      { transform: rotate(-40deg); }
  }
  @keyframes f-swing-leg-l {
    0%, 100% { transform: rotate(30deg); }
    50%      { transform: rotate(-30deg); }
  }
  @keyframes f-swing-leg-r {
    0%, 100% { transform: rotate(-30deg); }
    50%      { transform: rotate(30deg); }
  }

  /* Coureur de derrière (décalé) */
  .b-arm-l  { animation: b-swing-arm-l 0.6s ease-in-out infinite 0.3s; }
  .b-arm-r  { animation: b-swing-arm-r 0.6s ease-in-out infinite 0.3s; }
  .b-leg-l  { animation: b-swing-leg-l 0.6s ease-in-out infinite 0.3s; }
  .b-leg-r  { animation: b-swing-leg-r 0.6s ease-in-out infinite 0.3s; }

  @keyframes b-swing-arm-l {
    0%, 100% { transform: rotate(-35deg); }
    50%      { transform: rotate(35deg); }
  }
  @keyframes b-swing-arm-r {
    0%, 100% { transform: rotate(35deg); }
    50%      { transform: rotate(-35deg); }
  }
  @keyframes b-swing-leg-l {
    0%, 100% { transform: rotate(28deg); }
    50%      { transform: rotate(-28deg); }
  }
  @keyframes b-swing-leg-r {
    0%, 100% { transform: rotate(-28deg); }
    50%      { transform: rotate(28deg); }
  }

  /* --- Lignes de vitesse --- */
  .speed-line { animation: speed 0.8s ease-in-out infinite; }
  .sl-1 { animation-delay: 0s; }
  .sl-2 { animation-delay: 0.2s; }
  .sl-3 { animation-delay: 0.4s; }
  @keyframes speed {
    0%, 100% { opacity: 0.7; transform: translateX(0); }
    50%      { opacity: 0.1; transform: translateX(-10px); }
  }
</style>
</head>
<body>
  <svg viewBox="0 0 280 260" width="240" height="224" xmlns="http://www.w3.org/2000/svg"
       fill="none" stroke-linecap="round" stroke-linejoin="round">

    <!-- ==================== -->
    <!-- LIGNES DE VITESSE    -->
    <!-- ==================== -->
    <g>
      <line class="speed-line sl-1" x1="18" y1="62" x2="48" y2="62"
            stroke="#F0F0F0" stroke-width="7" opacity="0.7"/>
      <line class="speed-line sl-2" x1="10" y1="82" x2="40" y2="82"
            stroke="#F0F0F0" stroke-width="7" opacity="0.6"/>
      <line class="speed-line sl-3" x1="22" y1="102" x2="48" y2="102"
            stroke="#F0F0F0" stroke-width="7" opacity="0.5"/>
    </g>

    <!-- =============================== -->
    <!-- COUREUR ARRIERE (plus petit)     -->
    <!-- =============================== -->
    <g class="runner-back">
      <!-- Tête -->
      <circle cx="190" cy="42" r="14" stroke="#F0F0F0" stroke-width="7" fill="none"/>

      <!-- Corps (torse) -->
      <polyline points="182,58 168,110"
                stroke="#F0F0F0" stroke-width="7"/>

      <!-- Bras gauche (devant) -->
      <g class="b-arm-l">
        <polyline points="178,70 158,88 148,78"
                  stroke="#F0F0F0" stroke-width="7"/>
      </g>

      <!-- Bras droit (derrière) -->
      <g class="b-arm-r">
        <polyline points="178,70 196,90 204,82"
                  stroke="#F0F0F0" stroke-width="7"/>
      </g>

      <!-- Jambe gauche (devant) -->
      <g class="b-leg-l">
        <polyline points="168,110 148,145 132,138"
                  stroke="#F0F0F0" stroke-width="7"/>
      </g>

      <!-- Jambe droite (derrière) -->
      <g class="b-leg-r">
        <polyline points="168,110 186,148 198,142"
                  stroke="#F0F0F0" stroke-width="7"/>
      </g>
    </g>

    <!-- =============================== -->
    <!-- COUREUR DEVANT (plus grand)      -->
    <!-- =============================== -->
    <g class="runner-front">
      <!-- Tête -->
      <circle cx="128" cy="52" r="16" stroke="#F0F0F0" stroke-width="8" fill="none"/>

      <!-- Corps (torse) -->
      <polyline points="118,70 100,132"
                stroke="#F0F0F0" stroke-width="8"/>

      <!-- Bras gauche (devant, plié) -->
      <g class="f-arm-l">
        <polyline points="112,84 86,108 74,96"
                  stroke="#F0F0F0" stroke-width="8"/>
      </g>

      <!-- Bras droit (derrière, plié) -->
      <g class="f-arm-r">
        <polyline points="112,84 136,108 146,98"
                  stroke="#F0F0F0" stroke-width="8"/>
      </g>

      <!-- Jambe gauche (devant, pliée) -->
      <g class="f-leg-l">
        <polyline points="100,132 72,178 52,168"
                  stroke="#F0F0F0" stroke-width="8"/>
      </g>

      <!-- Jambe droite (derrière, pliée) -->
      <g class="f-leg-r">
        <polyline points="100,132 128,180 146,172"
                  stroke="#F0F0F0" stroke-width="8"/>
      </g>
    </g>

    <!-- ==================== -->
    <!-- LIGNES SOUS LES PIEDS -->
    <!-- ==================== -->
    <g>
      <line class="speed-line sl-1" x1="40" y1="210" x2="72" y2="210"
            stroke="#F0F0F0" stroke-width="6" opacity="0.5"/>
      <line class="speed-line sl-2" x1="90" y1="225" x2="130" y2="225"
            stroke="#F0F0F0" stroke-width="6" opacity="0.4"/>
      <line class="speed-line sl-3" x1="150" y1="215" x2="185" y2="215"
            stroke="#F0F0F0" stroke-width="6" opacity="0.3"/>
    </g>

  </svg>
</body>
</html>
"""
    components.html(runner_html, height=300)
