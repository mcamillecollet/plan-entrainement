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

# --- CSS global + navbar ---
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Outfit:wght@300;400;500;600&display=swap');

  [data-testid="stSidebar"],
  [data-testid="stSidebarNav"],
  header[data-testid="stHeader"] {
    display: none !important;
  }

  [data-testid="stAppViewContainer"] > .main {
    padding-top: 1rem !important;
  }

  .glass-nav {
    display: flex;
    align-items: center;
    padding: 0 1.5rem;
    height: 52px;
    background: rgba(30, 30, 30, 0.75);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    margin-bottom: 0.5rem;
  }

  .glass-nav .nav-brand {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #FFFFFF;
  }

  /* Restyle des boutons nav en glass */
  .nav-row .stButton > button {
    background: transparent !important;
    color: #AAAAAA !important;
    border: none !important;
    font-family: 'Geist Mono', monospace !important;
    font-size: 0.70rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1rem !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
    margin: 0 !important;
  }

  .nav-row .stButton > button:hover {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.08) !important;
  }

  .nav-row .stButton > button[kind="primary"],
  .nav-row .stButton > button:disabled {
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.12) !important;
  }
</style>
""", unsafe_allow_html=True)

# --- Barre de navigation ---
st.markdown('<div class="glass-nav"><span class="nav-brand">Plan d\'entra\u00eenement</span></div>', unsafe_allow_html=True)

st.markdown('<div class="nav-row">', unsafe_allow_html=True)
cols = st.columns([1] * len(PAGES))
for i, page_name in enumerate(PAGES):
    with cols[i]:
        btn_type = "primary" if page_name == current else "secondary"
        if st.button(page_name, key=f"nav_{page_name}", type=btn_type, use_container_width=True):
            st.session_state["current_page"] = page_name
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr style="border: none; border-top: 1px solid #4A4A4A; margin: 1rem 0 2rem 0;">', unsafe_allow_html=True)

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
