import streamlit as st
import pandas as pd
import joblib

st.markdown("<h1 style='color: #6a5acd;'>Simulador Interativo</h1>", unsafe_allow_html=True)
st.divider()

st.write("""
Preencha o formulário abaixo com os indicadores mais recentes do aluno para obter uma predição 
sobre o risco de defasagem no próximo ciclo avaliativo.
""")

with st.form("form_predicao_risco"):
    st.subheader("📊 Indicadores do Aluno")
    col1, col2 = st.columns(2)
    
    with col1:
        ian_opts = {"Adequado": 0, "Defasagem Leve": 1, "Defasagem Moderada": 2, "Defasagem Severa": 3}
        ian = st.selectbox("Nível de Adequação (IAN)", options=list(ian_opts.keys()))
        
        ida = st.slider("Desempenho Acadêmico (IDA)", min_value=0.0, max_value=10.0, value=7.5, step=0.1)
        
        ieg_opts = {"Baixo": 0, "Médio": 1, "Alto": 2}
        ieg = st.selectbox("Engajamento Geral (IEG)", options=list(ieg_opts.keys()))

    with col2:
        ips = st.slider("Índice Psicossocial (IPS)", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
        ipp = st.slider("Índice Psicopedagógico (IPP)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
        iaa = st.slider("Autoavaliação (IAA)", min_value=0.0, max_value=10.0, value=6.5, step=0.1)

    submitted = st.form_submit_button("🔍 Analisar Risco do Aluno")

if submitted:
    data = {
        'IAN': [ian_opts[ian]],
        'IDA': [ida],
        'IEG': [ieg_opts[ieg]],
        'IPS': [ips],
        'IPP': [ipp],
        'IAA': [iaa]
    }
    df_input = pd.DataFrame(data)
    
    st.divider()
    st.markdown("### Resultado da Análise Preditiva")