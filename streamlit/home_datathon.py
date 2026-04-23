import streamlit as st

st.set_page_config(page_title="Datathon - Passos Mágicos - Turma 10DTAT - Grupo 55", layout="wide")

pg = st.navigation([
    st.Page("introducao_datathon.py", title="Introdução", icon="📖"),
    st.Page("contexto_datathon.py", title="Contexto e Indicadores", icon="🧩"),
    st.Page("analise_exploratoria_datathon.py", title="Análise Exploratória (EDA)", icon="📊"),
    st.Page("modelo_preditivo_datathon.py", title="Modelo Preditivo", icon="🤖"),
    st.Page("simulador_risco_datathon.py", title="Simulador Interativo", icon="💻"),
    st.Page("conclusao_datathon.py", title="Conclusão", icon="🎯")
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