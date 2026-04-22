import streamlit as st

st.markdown("<h1 style='color: #6a5acd;'>Conclusão e Recomendações</h1>", unsafe_allow_html=True)
st.divider()

st.markdown("### 🎯 Objetivo Atingido")

st.write("""
O projeto cumpriu seu objetivo de transformar dados brutos em inteligência acionável para a Passos Mágicos. 
Desenvolvemos uma solução analítica completa, desde a exploração de dados até a implementação de um modelo preditivo, 
para apoiar a equipe na identificação e mitigação do risco de defasagem dos alunos.
""")

st.markdown("### 🤖 Principais Entregas")

st.write("""
- **Análise Exploratória (EDA):** Revelou que o bem-estar psicossocial (IPS) e o engajamento (IEG) são cruciais para o sucesso acadêmico, validando a abordagem multidimensional da instituição.
- **Modelo Preditivo (?):** Alcançou uma acurácia de **?%**, provando ser uma ferramenta eficaz para a detecção precoce de alunos em risco.
- **Simulador Interativo:** Disponibiliza o poder do modelo preditivo para a equipe da Passos Mágicos, permitindo triagens rápidas e decisões baseadas em dados no dia a dia.
""")

st.markdown("### 🚀 Recomendações Estratégicas")

with st.container(border=True):
    st.write("""
    1.  **Implementar o Monitoramento do IPS:** Utilizar o Índice Psicossocial como um "sinal vital". Quedas neste indicador devem acionar um protocolo de acompanhamento imediato, mesmo que o desempenho acadêmico ainda não tenha sido afetado.
    
    2.  **Fomentar o Engajamento (IEG):** Criar programas e iniciativas focadas em aumentar o engajamento dos alunos, especialmente aqueles com IEG baixo ou médio, dado seu forte impacto no desempenho acadêmico.
    
    3.  **Utilizar o Simulador para Planejamento:** Integrar o simulador de risco no processo de planejamento pedagógico trimestral para alocar recursos de apoio (psicólogos, tutores) de forma mais eficiente para os alunos que mais precisam.
    """)

st.divider()
st.success("""
**Missão Cumprida:** Transformamos dados em diagnósticos e insights em estratégias, fornecendo à Passos Mágicos uma ferramenta poderosa para continuar sua mágica transformadora na vida de milhares de jovens.
""")