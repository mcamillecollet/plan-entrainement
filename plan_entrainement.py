import streamlit as st

st.set_page_config(
    page_title="Plan d'entraînement",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Navigation via query params ---
PAGES = {
    "accueil": "Accueil",
    "analyse": "Analyse GPX",
    "plan": "Plan d'entraînement",
    "explications": "Explications",
}

current = st.query_params.get("page", "accueil")
if current not in PAGES:
    current = "accueil"

st.session_state["current_page"] = current

# --- Navbar glassmorphism ---
nav_links = ""
for key, label in PAGES.items():
    active_style = "color: #FFFFFF; background: rgba(255,255,255,0.12);" if key == current else "color: #AAAAAA;"
    nav_links += f'''<a href="?page={key}" target="_self" style="
        font-family: 'Geist Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        text-decoration: none;
        {active_style}
        padding: 0.5rem 1.2rem;
        border-radius: 6px;
        transition: all 0.2s ease;
    ">{label}</a>'''

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Outfit:wght@300;400;500;600&display=swap');

  [data-testid="stSidebar"],
  [data-testid="stSidebarNav"],
  header[data-testid="stHeader"] {{
    display: none !important;
  }}

  .glass-navbar {{
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
  }}

  .glass-navbar .nav-brand {{
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #FFFFFF;
  }}

  .glass-navbar .nav-links {{
    display: flex;
    gap: 0.3rem;
    align-items: center;
  }}

  .glass-navbar .nav-links a:hover {{
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.08) !important;
  }}

  [data-testid="stAppViewContainer"] > .main {{
    padding-top: 4.5rem !important;
  }}
</style>

<div class="glass-navbar">
  <span class="nav-brand">Plan d'entraînement</span>
  <div class="nav-links">
    {nav_links}
  </div>
</div>
""", unsafe_allow_html=True)

# --- Séparateur ---
st.markdown('<hr style="border: none; border-top: 1px solid #4A4A4A; margin: 0.5rem 0 2rem 0;">', unsafe_allow_html=True)

# --- Rendu de la page courante ---
if current == "accueil":
    from pages.page_accueil import render
    render()
elif current == "analyse":
    from pages.page_analyse import render
    render()
elif current == "plan":
    from pages.page_plan import render
    render()
elif current == "explications":
    from pages.page_explications import render
    render()
