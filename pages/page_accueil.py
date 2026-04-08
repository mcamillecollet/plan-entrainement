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

    # Animation du coureur via st.components.v1.html (supporte le SVG)
    runner_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; }
  body {
    background: transparent;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100%;
    overflow: hidden;
  }

  .runner-bounce {
    animation: bounce 0.35s ease-in-out infinite;
  }
  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-7px); }
  }

  .arm-l, .arm-r, .leg-l, .leg-r {
    transform-box: fill-box;
    transform-origin: top center;
  }

  .arm-l  { animation: swing-arm-l 0.7s ease-in-out infinite; }
  .arm-r  { animation: swing-arm-r 0.7s ease-in-out infinite; }
  .leg-l  { animation: swing-leg-l 0.7s ease-in-out infinite; }
  .leg-r  { animation: swing-leg-r 0.7s ease-in-out infinite; }

  @keyframes swing-arm-l {
    0%, 100% { transform: rotate(-35deg); }
    50%      { transform: rotate(35deg); }
  }
  @keyframes swing-arm-r {
    0%, 100% { transform: rotate(35deg); }
    50%      { transform: rotate(-35deg); }
  }
  @keyframes swing-leg-l {
    0%, 100% { transform: rotate(28deg); }
    50%      { transform: rotate(-28deg); }
  }
  @keyframes swing-leg-r {
    0%, 100% { transform: rotate(-28deg); }
    50%      { transform: rotate(28deg); }
  }

  .runner-shadow {
    animation: shadow-pulse 0.35s ease-in-out infinite;
  }
  @keyframes shadow-pulse {
    0%, 100% { opacity: 0.25; }
    50%      { opacity: 0.10; }
  }

  .speed-line { animation: speed 0.7s ease-in-out infinite; }
  .speed-line-1 { animation-delay: 0s; }
  .speed-line-2 { animation-delay: 0.18s; }
  .speed-line-3 { animation-delay: 0.36s; }
  @keyframes speed {
    0%, 100% { opacity: 0.6; transform: translateX(0); }
    50%      { opacity: 0.05; transform: translateX(-12px); }
  }

  .dust { animation: dust-particle 0.7s ease-out infinite; }
  .dust-1 { animation-delay: 0s; }
  .dust-2 { animation-delay: 0.25s; }
  .dust-3 { animation-delay: 0.5s; }
  @keyframes dust-particle {
    0%   { opacity: 0.4; transform: translate(0, 0) scale(1); }
    100% { opacity: 0; transform: translate(-18px, -8px) scale(0.3); }
  }
</style>
</head>
<body>
  <svg viewBox="0 0 160 185" width="160" height="185" xmlns="http://www.w3.org/2000/svg">

    <!-- Speed lines -->
    <line class="speed-line speed-line-1" x1="12" y1="48" x2="32" y2="48"
          stroke="#D04D46" stroke-width="2.2" stroke-linecap="round"/>
    <line class="speed-line speed-line-2" x1="8"  y1="66" x2="30" y2="66"
          stroke="#D04D46" stroke-width="1.8" stroke-linecap="round"/>
    <line class="speed-line speed-line-3" x1="16" y1="84" x2="34" y2="84"
          stroke="#D04D46" stroke-width="1.4" stroke-linecap="round"/>

    <g class="runner-bounce">
      <!-- Head -->
      <circle cx="82" cy="18" r="12" fill="#F0F0F0"/>

      <!-- Torso -->
      <line x1="80" y1="30" x2="74" y2="78"
            stroke="#F0F0F0" stroke-width="5.5" stroke-linecap="round"/>

      <!-- Left arm -->
      <g class="arm-l">
        <line x1="78" y1="38" x2="60" y2="62"
              stroke="#F0F0F0" stroke-width="3.8" stroke-linecap="round"/>
        <line x1="60" y1="62" x2="54" y2="72"
              stroke="#CCCCCC" stroke-width="3" stroke-linecap="round"/>
      </g>

      <!-- Right arm -->
      <g class="arm-r">
        <line x1="78" y1="38" x2="96" y2="62"
              stroke="#F0F0F0" stroke-width="3.8" stroke-linecap="round"/>
        <line x1="96" y1="62" x2="102" y2="72"
              stroke="#CCCCCC" stroke-width="3" stroke-linecap="round"/>
      </g>

      <!-- Left leg (thigh + calf with shoe) -->
      <g class="leg-l">
        <line x1="74" y1="78" x2="54" y2="118"
              stroke="#F0F0F0" stroke-width="5" stroke-linecap="round"/>
        <line x1="54" y1="118" x2="46" y2="148"
              stroke="#F0F0F0" stroke-width="4.2" stroke-linecap="round"/>
        <line x1="46" y1="148" x2="40" y2="155"
              stroke="#D04D46" stroke-width="5" stroke-linecap="round"/>
      </g>

      <!-- Right leg (thigh + calf with shoe) -->
      <g class="leg-r">
        <line x1="74" y1="78" x2="94" y2="118"
              stroke="#F0F0F0" stroke-width="5" stroke-linecap="round"/>
        <line x1="94" y1="118" x2="102" y2="148"
              stroke="#F0F0F0" stroke-width="4.2" stroke-linecap="round"/>
        <line x1="102" y1="148" x2="108" y2="155"
              stroke="#D04D46" stroke-width="5" stroke-linecap="round"/>
      </g>
    </g>

    <!-- Ground shadow -->
    <ellipse class="runner-shadow" cx="76" cy="172" rx="24" ry="4" fill="#D04D46" opacity="0.25"/>

    <!-- Dust particles behind feet -->
    <circle class="dust dust-1" cx="42" cy="162" r="2.5" fill="#888"/>
    <circle class="dust dust-2" cx="36" cy="158" r="2"   fill="#888"/>
    <circle class="dust dust-3" cx="46" cy="166" r="1.8" fill="#888"/>

  </svg>
</body>
</html>
"""
    components.html(runner_html, height=220)
