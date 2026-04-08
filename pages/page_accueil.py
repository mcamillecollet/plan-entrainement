import streamlit as st
from shared import inject_css


def render():
    inject_css()

    st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center;
            min-height: 55vh; text-align: center; padding: 2rem;">

  <h1 style="font-family: 'Outfit', sans-serif; font-weight: 600; font-size: 2.8rem;
             letter-spacing: -0.03em; color: #F0F0F0; margin-bottom: 0.5rem;">
    Plan d'entra\u00eenement
  </h1>

  <p style="font-family: 'Geist Mono', monospace; font-size: 0.78rem; font-weight: 400;
            letter-spacing: 0.1em; text-transform: uppercase; color: #888; margin-bottom: 3rem;">
    Analyse de parcours \u2014 Planification personnalis\u00e9e
  </p>

  <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; justify-content: center;">

    <div style="background: rgba(255,255,255,0.06); backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.10);
                border-radius: 12px; padding: 2rem 2.5rem; min-width: 240px;">
      <p style="font-family: 'Geist Mono', monospace; font-size: 0.65rem; font-weight: 500;
                letter-spacing: 0.12em; text-transform: uppercase; color: #D04D46; margin-bottom: 0.5rem;">
        01
      </p>
      <p style="font-family: 'Outfit', sans-serif; font-weight: 500; font-size: 1.15rem;
                color: #F0F0F0; margin-bottom: 0.3rem;">
        Analyse GPX
      </p>
      <p style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; color: #888;">
        Importez votre parcours et analysez le profil d'altitude
      </p>
    </div>

    <div style="background: rgba(255,255,255,0.06); backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.10);
                border-radius: 12px; padding: 2rem 2.5rem; min-width: 240px;">
      <p style="font-family: 'Geist Mono', monospace; font-size: 0.65rem; font-weight: 500;
                letter-spacing: 0.12em; text-transform: uppercase; color: #5A77B5; margin-bottom: 0.5rem;">
        02
      </p>
      <p style="font-family: 'Outfit', sans-serif; font-weight: 500; font-size: 1.15rem;
                color: #F0F0F0; margin-bottom: 0.3rem;">
        Plan d'entra\u00eenement
      </p>
      <p style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; color: #888;">
        G\u00e9n\u00e9rez votre plan personnalis\u00e9 avec VDOT et allures
      </p>
    </div>

    <div style="background: rgba(255,255,255,0.06); backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.10);
                border-radius: 12px; padding: 2rem 2.5rem; min-width: 240px;">
      <p style="font-family: 'Geist Mono', monospace; font-size: 0.65rem; font-weight: 500;
                letter-spacing: 0.12em; text-transform: uppercase; color: #93A5CF; margin-bottom: 0.5rem;">
        03
      </p>
      <p style="font-family: 'Outfit', sans-serif; font-weight: 500; font-size: 1.15rem;
                color: #F0F0F0; margin-bottom: 0.3rem;">
        Explications
      </p>
      <p style="font-family: 'Outfit', sans-serif; font-size: 0.82rem; color: #888;">
        D\u00e9couvrez les diff\u00e9rents types de s\u00e9ances
      </p>
    </div>

  </div>
</div>
""", unsafe_allow_html=True)
