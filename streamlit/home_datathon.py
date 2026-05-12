import streamlit as st

st.set_page_config(page_title="Datathon - Passos Mágicos - Turma 10DTAT - Grupo 55", layout="wide")

pg = st.navigation([
    st.Page("simulador_risco_datathon.py", title="Simulador Interativo", icon="💻"),
])

with st.sidebar:
    st.markdown("<h3 style='margin-bottom: 0px; padding-bottom: 0px;'>Data Analytics - Turma 10DTAT - Grupo 55 - Datathon</h3>", unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    *Evandro Anholeto*  
    *Pedro Alencar*  
    *Renan Ribas*
    """)

pg.run()