import streamlit as st
import pandas as pd
import joblib
import os

def load_model():
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, '..', 'modelo_risco_defasagem.pkl')
    return joblib.load(model_path)

model = load_model()

with st.sidebar:
    st.markdown("### ⚙️ Características do Modelo")
    st.markdown("- **Algoritmo:** Random Forest Classifier")
    st.markdown("- **AUC:** 76%")
    st.markdown("- **Recall (Classe Risco):** 75%")
    st.markdown("- **Acurácia:** 76%")

st.markdown("<h1 style='color: #6a5acd;'>📊 Simulador Interativo de Risco</h1>", unsafe_allow_html=True)
st.write("Ajuste os indicadores abaixo para simular o perfil de um aluno e prever a probabilidade de **defasagem escolar** no próximo ano letivo.")
st.divider()

aba_simulador, aba_info = st.tabs(["💻 Simulador", "ℹ️ Sobre o Simulador"])

with aba_simulador:
    st.markdown("### Perfil do Aluno")
    with st.container(border=True):
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            idade = st.number_input("Idade", min_value=5, max_value=25, value=15)
        with col_p2:
            genero = st.selectbox("Gênero", ["MENINA", "MENINO"])
        with col_p3:
            instituicao = st.selectbox("Instituição de Ensino", ["ESCOLA PÚBLICA", "REDE DECISÃO", "Outra"])

    st.markdown("### Indicadores de Desempenho (0 a 10)")
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
            if prob_risco_percentual >= 60:
                st.error(f"### ⚠️ Risco Alto de Defasagem: {prob_risco_percentual:.1f}%\n\n"
                         f"**Atenção recomendada:** Os indicadores inseridos apontam uma forte tendência à defasagem no próximo ano letivo. Sugere-se uma intervenção pedagógica imediata e acompanhamento psicossocial ativo.")
                st.progress(prob_risco, text="Probabilidade de entrar em defasagem")
            elif prob_risco_percentual >= 30:
                st.warning(f"### 🟡 Risco Moderado de Defasagem: {prob_risco_percentual:.1f}%")
                st.progress(prob_risco, text="Probabilidade de entrar em defasagem")
                st.write("**Sinal amarelo:** Monitore de perto a evolução dos indicadores do aluno, especialmente IDA e IEG.")
            else:
                st.success(f"### ✅ Risco Baixo de Defasagem: {prob_risco_percentual:.1f}%")
                st.progress(prob_risco, text="Probabilidade de entrar em defasagem")
                st.write("**Cenário positivo:** O aluno possui um perfil saudável em relação aos indicadores.")

    st.divider()
    st.info("**Uso Responsável:** Este simulador é uma ferramenta analítica de suporte à decisão baseada em dados históricos. As predições geradas estimam probabilidades, mas não substituem o julgamento humano, o acompanhamento humano e a avaliação pedagógica/psicológica individualizada de cada aluno.")

with aba_info:
    st.markdown("### Objetivo do Simulador e do Trabalho")
    st.info("O objetivo do Datathon e deste simulador é utilizar técnicas de Data Science e Machine Learning para prever precocemente a probabilidade de um aluno entrar em defasagem escolar. Dessa forma, a instituição pode adotar medidas preventivas e intervenções pedagógicas direcionadas, mitigando riscos e garantindo um melhor desenvolvimento do estudante.")

    st.markdown("### Variáveis Utilizadas (Features de Entrada)")
    st.write("O modelo utiliza as seguintes variáveis do perfil e do desempenho do aluno:")
    
    df_features = pd.DataFrame({
        "Categoria": ["Demográficas", "Desempenho Acadêmico", "Psicossociais e Comportamentais"],
        "Variáveis": [
            "Idade, Gênero, Instituição de Ensino", 
            "IDA (Indicador de Aprendizagem), Notas de Matemática e Português", 
            "IAA (Autoavaliação), IEG (Engajamento), IPS (Psicossocial), IPP (Psicopedagógico)"
        ]
    }).set_index("Categoria")
    st.table(df_features)

    st.markdown("### Variáveis Excluídas do Modelo")
    st.write("Algumas variáveis foram intencionalmente deixadas de fora do treinamento por diversos motivos, tais como:")
    
    df_excluidas = pd.DataFrame({
        "Variável Excluída": [
            "RA e Nome", 
            "IAN (Adequação ao Nível)",
            "Ing (Nota de Inglês)"
        ],
        "Motivo da Exclusão": [
            "São identificadores únicos e não possuem nenhum valor preditivo, visando também a prevenção de viés e manutenção da privacidade.",
            "Possui uma relação matemática direta e determinística com a variável alvo, o que inflaria a precisão artificialmente causando vazamento de dados (data leakage).",
            "Muitos valores ausentes/inconsistentes dependendo da fase escolar ou instituição, o que poderia comprometer o treinamento e a estabilidade do modelo."
        ]
    }).set_index("Variável Excluída")
    st.table(df_excluidas)

    st.markdown("### Interpretação dos Resultados")
    st.write("O simulador divide a probabilidade de risco em três níveis de atenção:")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.success("**🟢 < 30% (Risco Baixo)**\n\nO aluno está com indicadores muito saudáveis e dentro do esperado. Apenas manutenção da rotina de estudos é sugerida.")
    with col_res2:
        st.warning("**🟡 30% a 59% (Risco Moderado)**\n\nSinal de alerta. O aluno começa a demonstrar oscilações em indicadores chave. Requer monitoramento mais próximo por parte dos educadores.")
    with col_res3:
        st.error("**🔴 ≥ 60% (Risco Alto)**\n\nPerfil muito propício à defasagem. Indicadores acusam queda severa em pontos críticos. Necessária ação pedagógica ou apoio psicossocial imediato.")

    st.markdown("### Probabilidade de Risco *vs* Confiança do Modelo")
    st.write("É fundamental não confundir o **risco de defasagem do aluno** com a **acurácia do modelo**:")
    
    col_conf1, col_conf2 = st.columns(2)
    with col_conf1:
        st.info("**Probabilidade de Risco (ex: 75% de Risco Alto)**\n\nIndica que, dadas as características inseridas, o perfil deste aluno se assemelha a 75% dos casos históricos que *efetivamente* entraram em defasagem.")
    with col_conf2:
        st.info("**Acurácia / Confiança (ex: 85%)**\n\nSignifica que, de forma geral, quando o nosso modelo de IA prevê algo, ele acerta o diagnóstico histórico e real cerca de 85 vezes a cada 100 avaliações.")
        
    st.caption("*Ou seja: \"O aluno X tem 75% de risco de defasagem, e nós temos 85% de confiança de que a leitura geral do modelo está correta.\"*")