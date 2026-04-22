import streamlit as st

st.markdown("<h1 style='color: #6a5acd;'>Análise Exploratória (EDA)</h1>", unsafe_allow_html=True)
st.divider()

st.markdown("### 🎯 Objetivo da Análise")

st.write("""
O painel analítico foi desenvolvido para explorar os dados históricos e responder às perguntas de negócio da Passos Mágicos. 
O objetivo é identificar padrões, correlações e tendências que possam guiar as decisões estratégicas da organização.
""")

st.markdown("### 🧩 Principais Insights Obtidos")

with st.container(border=True):
    st.write("""
    - **Defasagem (IAN) vs. Evolução:** A análise mostra que a defasagem é mais acentuada nos alunos ingressantes, mas o programa demonstra sucesso em reduzi-la progressivamente ao longo das fases (Quartzo → Topázio).
    
    - **Engajamento é Chave:** Há uma forte correlação positiva entre o Índice de Engajamento (IEG) e o Desempenho Acadêmico (IDA). Alunos mais engajados tendem a ter notas melhores.
    
    - **Sinais de Alerta:** Quedas no Índice Psicossocial (IPS) frequentemente antecedem uma queda no desempenho (IDA) no bimestre seguinte, tornando o IPS um importante preditor de risco.
    
    - **Autopercepção:** Em geral, a autoavaliação dos alunos (IAA) é coerente com seu desempenho (IDA), mas alunos em risco tendem a superestimar suas notas, indicando uma oportunidade para intervenção psicopedagógica.
    """)

st.divider()

st.markdown("### 📊 Acessar Painel Analítico")
st.write("link")
st.caption("O link acima é um placeholder para o dashboard gerencial desenvolvido para a Passos Mágicos.")