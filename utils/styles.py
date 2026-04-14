# styles.py — injection CSS Streamlit et style partagé pour les graphiques matplotlib

import streamlit as st
from utils.constants import CHART_BG


def inject_css():
    """Injecte le CSS global dans la page Streamlit courante."""
    st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Outfit:wght@300;400;500;600&display=swap');

  html, body, [data-testid="stAppViewContainer"] {
    background-color: #2E2E2E;
    font-family: 'Outfit', sans-serif;
    color: #E0E0E0;
  }

  [data-testid="stAppViewContainer"] > .main {
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1100px;
    margin: 0 auto;
    background-color: #2E2E2E;
  }

  [data-testid="stSidebar"] { background-color: #2E2E2E; }

  [data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    font-family: 'Outfit', sans-serif;
    color: #E0E0E0 !important;
  }

  [data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    color: #FFFFFF !important;
  }

  h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    font-size: 1.75rem;
    letter-spacing: -0.03em;
    color: #F0F0F0;
    margin-bottom: 0.25rem;
  }

  h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    letter-spacing: -0.02em;
    color: #E0E0E0;
  }

  .stat-card {
    background: #B0B0B0;
    border: 1px solid #999999;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  .stat-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #FFFFFF;
  }

  .stat-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.03em;
  }

  .stat-unit {
    font-family: 'Geist Mono', monospace;
    font-size: 0.75rem;
    color: #FFFFFF;
  }

  .section-divider {
    border: none;
    border-top: 1px solid #4A4A4A;
    margin: 2rem 0;
  }

  .section-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #AAA;
    margin-bottom: 1rem;
  }

  [data-testid="stFileUploader"] {
    background: #555;
    border: 1px solid #666;
    border-radius: 8px;
    padding: 0.5rem;
  }

  [data-testid="stFileUploader"] label {
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 1.4rem;
    letter-spacing: 0.01em;
    color: #F0F0F0;
  }

  [data-testid="stFileUploader"] section {
    background: #B0B0B0 !important;
    border: 1px solid #999999 !important;
    border-radius: 6px;
    padding: 0.5rem;
  }

  [data-testid="stFileUploader"] section button {
    background: #B0B0B0 !important;
    color: #FFFFFF !important;
  }

  [data-testid="stDataFrame"] {
    background: #2E2E2E;
    border: none;
    border-radius: 8px;
    overflow: hidden;
    font-family: 'Geist Mono', monospace;
    font-size: 0.8rem;
  }

  [data-testid="stDataFrame"] th,
  [data-testid="stDataFrame"] td,
  [data-testid="stDataFrame"] [role="gridcell"],
  [data-testid="stDataFrame"] [role="columnheader"] {
    background-color: #E8E8E8 !important;
    color: #2E2E2E !important;
  }

  .stButton > button {
    background: #555;
    color: #F0F0F0;
    border: none;
    border-radius: 6px;
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
    padding: 0.6rem 1.5rem;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: background 0.15s;
  }

  .stButton > button:hover { background: #666; }

  [data-testid="stRadio"] label,
  [data-testid="stSelectbox"] label,
  [data-testid="stTextInput"] label,
  [data-testid="stDateInput"] label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: #FFFFFF;
  }

  [data-testid="stRadio"],
  [data-testid="stSelectbox"],
  [data-testid="stTextInput"],
  [data-testid="stDateInput"] {
    background: #B0B0B0;
    border: 1px solid #999999;
    border-radius: 8px;
    padding: 0.5rem;
  }

  [data-testid="stRadio"] div[role="radiogroup"] label span,
  [data-testid="stSelectbox"] div[data-baseweb="select"] span,
  [data-testid="stSelectbox"] div[data-baseweb="select"] div,
  [data-testid="stTextInput"] input,
  [data-testid="stDateInput"] input {
    color: #FFFFFF !important;
  }

  [data-testid="stTextInput"] input:focus,
  [data-testid="stDateInput"] input:focus {
    border-color: #D04D46 !important;
    box-shadow: 0 0 0 1px #D04D46 !important;
    outline: none !important;
  }

  div[data-baseweb="popover"] *,
  div[data-baseweb="calendar"] * { color: #FFFFFF !important; }

  div[data-baseweb="popover"] svg,
  div[data-baseweb="calendar"] svg { fill: #FFFFFF !important; }

  [data-testid="stAlert"] {
    border-radius: 8px;
    border: 1px solid #4A4A4A;
    font-family: 'Outfit', sans-serif;
  }
</style>
""", unsafe_allow_html=True)


def style_ax(ax, fig):
    """Applique le style partagé à un axe matplotlib."""
    ax.set_facecolor(CHART_BG)
    fig.patch.set_facecolor(CHART_BG)
    ax.grid(True, color='#C8C5BE', linestyle='-', linewidth=0.5, alpha=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#C8C5BE')
    ax.spines['bottom'].set_color('#C8C5BE')
    ax.tick_params(colors='#555', labelsize=9)
    ax.xaxis.label.set_color('#444')
    ax.yaxis.label.set_color('#444')
    ax.title.set_color('#222')
