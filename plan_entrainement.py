import streamlit as st

st.set_page_config(
    page_title="Plan d'entraînement",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

pages = [
    st.Page("pages/1_Analyse_GPX.py", title="Analyse GPX", default=True),
    st.Page("pages/2_Plan_Entrainement.py", title="Plan d'entraînement"),
    st.Page("pages/3_Explications.py", title="Explications des séances"),
]

pg = st.navigation(pages)
pg.run()
