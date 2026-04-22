import streamlit as st

st.markdown("<h1 style='color: #6a5acd;'>Introdução ao Desafio</h1>", unsafe_allow_html=True)
st.divider()

st.markdown("### 🪄 A Missão da Passos Mágicos")

st.write("""
A **Associação Passos Mágicos** tem uma trajetória de 35 anos transformando a vida de crianças e jovens de baixa renda por meio da educação. 
Atuando como um projeto social e educacional, a associação instrumentaliza o uso da educação como ferramenta para a mudança das condições de vida de jovens em vulnerabilidade social.
""")

st.markdown("### 🎯 O Desafio de Dados")

st.write("""
Neste Datathon, nosso desafio é utilizar estratégias de **Data Analytics** para gerar um impacto real na vida dessas crianças. 
Com base em um dataset extensivo de desenvolvimento educacional (2022-2024), nossa missão é responder a dores de negócio críticas, 
contar uma história com os dados e desenvolver um modelo preditivo para identificar alunos em risco.
""")

st.markdown("### ❓ Perguntas de Negócio a Serem Respondidas")
st.info("""
1.  Qual o perfil de **defasagem (IAN)** dos alunos e sua evolução?
2.  O **desempenho acadêmico (IDA)** está melhorando ao longo do tempo?
3.  Qual a relação entre **engajamento (IEG)** e desempenho?
4.  Quais padrões nos indicadores permitem prever **alunos em risco**?
5.  O programa da Passos Mágicos demonstra **efetividade** ao longo das fases?
""")