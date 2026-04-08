import streamlit as st

st.set_page_config(
    page_title="Plan d'entra\u00eenement",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Navigation via session state ---
PAGES = ["Accueil", "Analyse GPX", "Plan d'entra\u00eenement", "Explications"]

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Accueil"

current = st.session_state["current_page"]

# --- CSS global + navbar fixe ---
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Outfit:wght@300;400;500;600&display=swap');

  [data-testid="stSidebar"],
  [data-testid="stSidebarNav"],
  header[data-testid="stHeader"] {
    display: none !important;
  }

  [data-testid="stAppViewContainer"] > .main {
    padding-top: 4.5rem !important;
  }

  .glass-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2.5rem;
    height: 52px;
    background: rgba(30, 30, 30, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  }

  .glass-navbar .nav-brand {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #FFFFFF;
  }

  .glass-navbar .nav-buttons {
    display: flex;
    gap: 0.3rem;
    align-items: center;
  }

  /* Masquer la rangée de boutons Streamlit (sous la navbar) */
  .nav-btn-row {
    position: fixed;
    top: 0;
    right: 2.5rem;
    z-index: 10000;
    height: 52px;
    display: flex;
    align-items: center;
    gap: 0.3rem;
  }

  .nav-btn-row .stButton > button {
    background: transparent !important;
    color: #AAAAAA !important;
    border: none !important;
    font-family: 'Geist Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.2rem !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
    margin: 0 !important;
    white-space: nowrap !important;
  }

  .nav-btn-row .stButton > button:hover {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.08) !important;
  }

  .nav-btn-row .stButton > button[kind="primary"] {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.12) !important;
  }
</style>

<div class="glass-navbar">
  <span class="nav-brand">Plan d'entra\u00eenement</span>
</div>
""", unsafe_allow_html=True)

# --- Boutons de navigation fixés dans la navbar ---
with st.container():
    st.markdown('<div class="nav-btn-row">', unsafe_allow_html=True)
    cols = st.columns(len(PAGES))
    for i, page_name in enumerate(PAGES):
        with cols[i]:
            btn_type = "primary" if page_name == current else "secondary"
            if st.button(page_name, key=f"nav_{page_name}", type=btn_type):
                st.session_state["current_page"] = page_name
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Rendu de la page courante ---
if current == "Accueil":
    from pages.page_accueil import render
    render()
elif current == "Analyse GPX":
    from pages.page_analyse import render
    render()
elif current == "Plan d'entra\u00eenement":
    from pages.page_plan import render
    render()
elif current == "Explications":
    from pages.page_explications import render
    render()
