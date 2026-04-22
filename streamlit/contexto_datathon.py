import streamlit as st

st.markdown("<h1 style='color: #6a5acd;'>Contexto e Indicadores Chave</h1>", unsafe_allow_html=True)
st.divider()

st.markdown("""
Para analisar o desenvolvimento dos alunos e a efetividade do programa, a Passos Mágicos utiliza um conjunto de indicadores multidimensionais. 
Compreender cada um deles é fundamental para a nossa análise.
""")

st.header("💎 Fases do Programa")
st.write("O programa é estruturado em fases, cada uma com focos de desenvolvimento específicos: **Quartzo, Ágata, Ametista e Topázio**.")

st.header("📖 Dicionário de Indicadores")
with st.container(border=True):
    st.markdown("""
    - **IAN (Índice de Adequação de Nível)**
      - *O quê mede?* A defasagem do aluno em relação ao seu nível escolar esperado.
      - *Exemplo:* Se um aluno está "severamente defasado".

    - **IDA (Índice de Desempenho Acadêmico)**
      - *O quê mede?* O rendimento do aluno nas avaliações e atividades acadêmicas.

    - **IEG (Índice de Engajamento Geral)**
      - *O quê mede?* A participação e o envolvimento do aluno nas atividades propostas.

    - **IAA (Índice de Autoavaliação)**
      - *O quê mede?* A percepção que o aluno tem sobre seu próprio desempenho e engajamento.

    - **IPS (Índice Psicossocial)**
      - *O quê mede?* Aspectos emocionais e sociais do aluno, como bem-estar e relacionamento.

    - **IPP (Índice Psicopedagógico)**
      - *O quê mede?* Avaliações psicopedagógicas que identificam dificuldades de aprendizagem.

    - **IPV (Índice do Ponto de Virada)**
      - *O quê mede?* Comportamentos que indicam uma mudança positiva ou negativa na trajetória do aluno.

    - **INDE (Índice de Desenvolvimento Educacional)**
      - *O quê mede?* A nota global do aluno, combinando os demais indicadores.
    """)