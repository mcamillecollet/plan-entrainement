import streamlit as st
from shared import inject_css

inject_css()

st.markdown("# Explications des types de s\u00e9ances")
st.markdown('<p class="section-label">Comprendre les diff\u00e9rents types d\'entra\u00eenement</p>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.markdown("""
<div style="background: #3A3A3A; border: 1px solid #4A4A4A; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem;">
  <p style="font-family: 'Outfit', sans-serif; color: #E0E0E0; font-size: 1rem;">
    Cette page sera compl\u00e9t\u00e9e prochainement avec les explications d\u00e9taill\u00e9es de chaque type de s\u00e9ance :
  </p>
  <ul style="font-family: 'Outfit', sans-serif; color: #E0E0E0; font-size: 0.95rem; margin-top: 0.5rem;">
    <li>Endurance fondamentale (EF)</li>
    <li>Seuil / Tempo</li>
    <li>Fractionn\u00e9 / VMA</li>
    <li>Allure sp\u00e9cifique (AS)</li>
    <li>Sortie longue (Long Run)</li>
    <li>S\u00e9ance c\u00f4tes</li>
  </ul>
</div>
""", unsafe_allow_html=True)
