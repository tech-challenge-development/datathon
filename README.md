# datathon
datathon
# Datathon - Passos Mágicos (Análise de Risco de Defasagem)

Este projeto é uma aplicação interativa desenvolvida em Streamlit para análise e predição de risco de defasagem de alunos, conforme os requisitos do Datathon da Pós-Tech.

## 📋 Pré-requisitos

Para garantir a compatibilidade de todas as bibliotecas, é recomendado utilizar uma versão recente do Python.

*   **Python 3.10+**

## 🛠️ Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente virtual (`.venv`) e instalar as dependências.

### 1. Criar o Ambiente Virtual

```bash
# No Windows (usando o launcher 'py')
py -3.10 -m venv .venv

# Ou se o python 3.10 for seu padrão
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual
Escolha o comando de acordo com o seu terminal no Windows:

*   **PowerShell:**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
*   **Prompt de Comando (CMD):**
    ```cmd
    .\.venv\Scripts\activate.bat
    ```

### 3. Instalar Dependências
Com o ambiente ativado, instale todas as bibliotecas necessárias usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🚀 Como Rodar o Projeto

Após ativar o ambiente virtual, execute o comando abaixo na pasta raiz do projeto:

```bash
streamlit run home_datathon.py
```

O navegador abrirá automaticamente no endereço local do Streamlit.
