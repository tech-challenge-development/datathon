import streamlit as st
import pandas as pd
import joblib

# 1. Carregando o Modelo Treinado
def load_model():
    return joblib.load('../modelo_risco_defasagem.pkl')

model = load_model()

# 2. Interface do Simulador
st.title("📊 Simulador de Risco de Defasagem")
st.markdown("Insira os dados do aluno abaixo para calcular a probabilidade de entrar em defasagem escolar.")

# Organizando os inputs em colunas para ficar visualmente bonito
col1, col2 = st.columns(2)

with col1:
    st.subheader("Perfil do Aluno")
    idade = st.number_input("Idade", min_value=5, max_value=25, value=15)
    genero = st.selectbox("Gênero", ["MENINA", "MENINO"])
    # Nota: O OneHotEncoder está com 'handle_unknown="ignore"', então mesmo se digitar
    # algo que não estava no treino, o modelo não vai quebrar.
    instituicao = st.selectbox("Instituição de Ensino", ["ESCOLA PÚBLICA", "REDE DECISÃO", "Outra"])

with col2:
    st.subheader("Indicadores de Desempenho")
    iaa = st.number_input("IAA (Autoavaliação)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    ieg = st.number_input("IEG (Engajamento)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    ips = st.number_input("IPS (Psicossocial)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    ipp = st.number_input("IPP (Psicopedagógico)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    ida = st.number_input("IDA (Aprendizagem)", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    mat = st.number_input("Nota Matemática", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
    por = st.number_input("Nota Português", min_value=0.0, max_value=10.0, value=7.0, step=0.1)

st.divider()

# 3. O Botão Mágico
if st.button("Gerar Análise de Risco", type="primary"):
    
    # Montando o "dicionário" exatamente com as mesmas colunas do treinamento
    # As chaves DEVEM ter os mesmos nomes que as colunas do seu df original
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
    
    # Transformando em um DataFrame do Pandas
    df_novo_aluno = pd.DataFrame(dados_entrada)
    
    # Calculando a Probabilidade! (Usando o [0, 1] para pegar a % de risco da única linha testada)
    prob_risco = model.predict_proba(df_novo_aluno)[0, 1]
    prob_risco_percentual = prob_risco * 100
    
    # 4. Exibindo o Resultado Visualmente
    st.subheader("Resultado do Modelo:")
    
    if prob_risco_percentual >= 50:
        st.error(f"⚠️ Risco Alto de Defasagem: {prob_risco_percentual:.1f}%")
        st.progress(prob_risco)
        st.write("Atenção recomendada: Os indicadores inseridos apontam uma forte tendência à defasagem no próximo ano.")
    elif prob_risco_percentual >= 30:
        st.warning(f"🟡 Risco Moderado de Defasagem: {prob_risco_percentual:.1f}%")
        st.progress(prob_risco)
        st.write("Sinal amarelo: Monitore de perto a evolução dos indicadores do aluno, especialmente IDA e IEG.")
    else:
        st.success(f"✅ Risco Baixo de Defasagem: {prob_risco_percentual:.1f}%")
        st.progress(prob_risco)
        st.write("Cenário positivo: O aluno possui um perfil saudável em relação aos indicadores.")