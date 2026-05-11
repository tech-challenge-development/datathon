import streamlit as st
import pandas as pd
import joblib
import os

def load_model():
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, '..', 'modelo_risco_defasagem.pkl')
    return joblib.load(model_path)

model = load_model()

st.markdown("<h1 style='color: #6a5acd;'>📊 Simulador Interativo de Risco</h1>", unsafe_allow_html=True)
st.write("Ajuste os indicadores abaixo para simular o perfil de um aluno e prever a probabilidade de **defasagem escolar** no próximo ano letivo.")
st.divider()

st.markdown("### 👤 Perfil do Aluno")
with st.container(border=True):
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        idade = st.number_input("Idade", min_value=5, max_value=25, value=15)
    with col_p2:
        genero = st.selectbox("Gênero", ["MENINA", "MENINO"])
    with col_p3:
        instituicao = st.selectbox("Instituição de Ensino", ["ESCOLA PÚBLICA", "REDE DECISÃO", "Outra"])

st.markdown("### 📈 Indicadores de Desempenho (0 a 10)")
with st.container(border=True):
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown("**🧠 Comportamental e Psicológico**")
        iaa = st.slider("IAA (Autoavaliação)", 0.0, 10.0, 7.0, 0.1, help="Percepção de desempenho")
        ieg = st.slider("IEG (Engajamento)", 0.0, 10.0, 7.0, 0.1, help="Participação e envolvimento")
        ips = st.slider("IPS (Psicossocial)", 0.0, 10.0, 7.0, 0.1, help="Emocional e social")
        ipp = st.slider("IPP (Psicopedagógico)", 0.0, 10.0, 7.0, 0.1, help="Dificuldades de aprendizagem")
    with col_i2:
        st.markdown("**📚 Acadêmico**")
        ida = st.slider("IDA (Aprendizagem)", 0.0, 10.0, 7.0, 0.1, help="Rendimento nas avaliações")
        mat = st.slider("Nota de Matemática", 0.0, 10.0, 7.0, 0.1)
        por = st.slider("Nota de Português", 0.0, 10.0, 7.0, 0.1)

st.divider()

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analisar = st.button("Gerar Análise de Risco", type="primary", use_container_width=True)

if analisar:
    dados_entrada = {
        'Idade': [idade],
        'IAA': [iaa],
        'IEG': [ieg],
        'IPS': [ips],
        'IPP': [ipp],
        'IDA': [ida],
        'Mat': [mat],
        'Por': [por],
        'Gênero': [genero],
        'Instituição de ensino': [instituicao]
    }
    
    df_novo_aluno = pd.DataFrame(dados_entrada)
    
    prob_risco = model.predict_proba(df_novo_aluno)[0, 1]
    prob_risco_percentual = prob_risco * 100

    st.markdown("### 🎯 Resultado da Simulação")
    with st.container(border=True):
        if prob_risco_percentual >= 50:
            st.error(f"### ⚠️ Risco Alto de Defasagem: {prob_risco_percentual:.1f}%")
            st.progress(prob_risco, text="Probabilidade de entrar em defasagem")
            st.write("**Atenção recomendada:** Os indicadores inseridos apontam uma forte tendência à defasagem no próximo ano.")
        elif prob_risco_percentual >= 30:
            st.warning(f"### 🟡 Risco Moderado de Defasagem: {prob_risco_percentual:.1f}%")
            st.progress(prob_risco, text="Probabilidade de entrar em defasagem")
            st.write("**Sinal amarelo:** Monitore de perto a evolução dos indicadores do aluno, especialmente IDA e IEG.")
        else:
            st.success(f"### ✅ Risco Baixo de Defasagem: {prob_risco_percentual:.1f}%")
            st.progress(prob_risco, text="Probabilidade de entrar em defasagem")
            st.write("**Cenário positivo:** O aluno possui um perfil saudável em relação aos indicadores.")