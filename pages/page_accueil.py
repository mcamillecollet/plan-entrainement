import streamlit as st
import streamlit.components.v1 as components
from utils import inject_css


def render():
    inject_css()

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
    padding-top: 50px;
  }
  .runner-front { animation: bounce-front 0.7s ease-in-out infinite; }
  @keyframes bounce-front {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-4px); }
  }
  .runner-back { animation: bounce-back 0.7s ease-in-out infinite 0.35s; }
  @keyframes bounce-back {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-4px); }
  }
  .speed-line { animation: speed 0.9s ease-in-out infinite; }
  .sl-1 { animation-delay: 0s; }
  .sl-2 { animation-delay: 0.22s; }
  .sl-3 { animation-delay: 0.44s; }
  @keyframes speed {
    0%, 100% { opacity: 0.7; transform: translateX(0); }
    50%      { opacity: 0.08; transform: translateX(-14px); }
  }
  .ground-line { animation: ground 1s ease-in-out infinite; }
  .gl-1 { animation-delay: 0s; }
  .gl-2 { animation-delay: 0.3s; }
  .gl-3 { animation-delay: 0.6s; }
  @keyframes ground {
    0%, 100% { opacity: 0.5; transform: translateX(0); }
    50%      { opacity: 0.08; transform: translateX(-12px); }
  }
</style>
</head>
<body>
  <svg viewBox="0 0 300 280" width="260" height="242" xmlns="http://www.w3.org/2000/svg"
       fill="none" stroke="#F0F0F0" stroke-linecap="round" stroke-linejoin="round">
    <line class="speed-line sl-1" x1="16" y1="60" x2="50" y2="60" stroke-width="7.5"/>
    <line class="speed-line sl-2" x1="8"  y1="82" x2="42" y2="82" stroke-width="7.5"/>
    <line class="speed-line sl-3" x1="20" y1="104" x2="50" y2="104" stroke-width="7.5"/>
    <g class="runner-back">
      <circle cx="198" cy="38" r="13" stroke-width="7"/>
      <path d="M 192,53 L 178,105" stroke-width="7"/>
      <path d="M 188,68 L 166,86 L 156,76" stroke-width="7"/>
      <path d="M 188,68 L 208,88 L 218,78" stroke-width="7"/>
      <path d="M 178,105 L 156,140 L 140,132" stroke-width="7"/>
      <path d="M 178,105 L 198,142 L 212,134" stroke-width="7"/>
    </g>
    <g class="runner-front">
      <circle cx="136" cy="52" r="16" stroke-width="8.5"/>
      <path d="M 128,70 L 110,136" stroke-width="8.5"/>
      <path d="M 122,88 L 94,112 L 80,100" stroke-width="8.5"/>
      <path d="M 122,88 L 148,114 L 162,102" stroke-width="8.5"/>
      <path d="M 110,136 L 78,182 L 58,170" stroke-width="8.5"/>
      <path d="M 110,136 L 140,184 L 160,174" stroke-width="8.5"/>
    </g>
    <line class="ground-line gl-1" x1="42" y1="218" x2="80" y2="218" stroke-width="6"/>
    <line class="ground-line gl-2" x1="98" y1="234" x2="142" y2="234" stroke-width="6"/>
    <line class="ground-line gl-3" x1="160" y1="224" x2="196" y2="224" stroke-width="6"/>
  </svg>
</body>
</html>
"""
    components.html(runner_html, height=320)
