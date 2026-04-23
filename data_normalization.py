import pandas as pd
import os

file_path = 'BASE DE DADOS PEDE 2024 - DATATHON.xlsx'

excel_file = pd.ExcelFile(file_path)

print(f"Abas encontradas: {excel_file.sheet_names}")

sheets = excel_file.sheet_names

df2022 = pd.read_excel(file_path, sheet_name=sheets[0])
df2023 = pd.read_excel(file_path, sheet_name=sheets[1])
df2024 = pd.read_excel(file_path, sheet_name=sheets[2])

# --- Comparação de Estrutura ---
def verify_structure(dfs_dict):
    """
    Compara nomes de colunas e tipos de dados entre vários DataFrames.
    """
    all_columns = {}
    for name, df in dfs_dict.items():
        all_columns[name] = set(df.columns)
    
    # 1. Verificar colunas comuns e exclusivas
    names = list(dfs_dict.keys())
    common_cols = all_columns[names[0]].intersection(*[all_columns[n] for n in names[1:]])
    union_cols = all_columns[names[0]].union(*[all_columns[n] for n in names[1:]])
    
    print("\n" + "="*50)
    print("ANÁLISE DE ESTRUTURA COMPARATIVA")
    print("="*50)
    print(f"Total de colunas únicas (união): {len(union_cols)}")
    print(f"Colunas comuns a todos: {len(common_cols)}")
    
    for name in names:
        exclusive = all_columns[name] - set().union(*[all_columns[n] for n in names if n != name])
        print(f"- {name}: {len(all_columns[name])} colunas ({len(exclusive)} exclusivas)")
        if len(exclusive) > 0:
            print(f"  Exclusivas: {sorted(list(exclusive))[:10]}... (listando top 10)")

    # 2. Verificar tipos de dados nas colunas comuns
    print("\n--- Verificação de Tipos (Dtypes) nas colunas comuns ---")
    mismatches = []
    for col in sorted(list(common_cols)):
        types = {name: str(dfs_dict[name][col].dtype) for name in names}
        if len(set(types.values())) > 1:
            mismatches.append((col, types))
            
    if not mismatches:
        print("OK: Todas as colunas comuns possuem os mesmos tipos de dados.")
    else:
        print("AVISO: Divergencias de tipos encontradas:")
        for col, types in mismatches:
            print(f"  - Coluna '{col}': {types}")

dfs = {
    'PEDE2022': df2022,
    'PEDE2023': df2023,
    'PEDE2024': df2024
}

verify_structure(dfs)

# --- Funções para a normalização dos dados ---
def normalize_string(text):
    if text is None:
        return None
    
    # Converte para maiúsculo
    text = text.upper()
    
    # Troca ';' por ' '
    text = text.replace(';', ' ')

    # Remove espaços duplos e transforma em espaços simples
    text = " ".join(text.split())
    
    # Remove espaços nas extremidades (trim)
    text = text.strip()

    # Verificação final para garantir que não restou uma string vazia
    if text == '':
        return None

    return text

# --- Remover colunas ---
df2023 = df2023.drop('Pedra 23', axis=1)

# --- Renomear colunas ---
df2022 = df2022.rename(columns={
    'Ano nasc': 'Ano Nasc',
    'Idade 22': 'Idade', 
    'Matem': 'Mat',
    'Portug': 'Por',
    'Inglês': 'Ing',
    'Fase ideal': 'Fase Ideal',
    'Defas': 'Defasagem'
})

df2023 = df2023.rename(columns={
    'Nome Anonimizado': 'Nome',
    'Pedra 2023': 'Pedra 23'
})

df2024 = df2024.rename(columns={
    'Nome Anonimizado': 'Nome',
    'Pedra 2024': 'Pedra 24',
    'INDE 2024': 'INDE 24'
})

# --- Tipagem e preenchimento de dados ausentes ---
# Data de Nasc
df2022['Data de Nasc'] = pd.Series([None] * len(df2022), dtype='datetime64[ns]')

# Ano Nasc
df2023['Data de Nasc'] = pd.to_datetime(df2023['Data de Nasc'], errors='coerce')
df2023['Ano Nasc'] = df2023['Data de Nasc'].dt.year.astype('Int64')

df2024['Data de Nasc'] = pd.to_datetime(df2024['Data de Nasc'], errors='coerce')
df2024['Ano Nasc'] = df2024['Data de Nasc'].dt.year.astype('Int64')

# Idade
df2022['Idade'] = pd.to_numeric(df2022['Idade'], errors='coerce')
df2022['Idade'] = df2022['Idade'].astype('Int64')

df2023['Idade'] = pd.to_numeric(df2023['Idade'], errors='coerce')
df2023['Idade'] = df2023['Idade'].astype('Int64')

df2024['Idade'] = pd.to_numeric(df2024['Idade'], errors='coerce')
df2024['Idade'] = df2024['Idade'].astype('Int64')

# Ano ingresso
df2022['Ano ingresso'] = pd.to_numeric(df2022['Ano ingresso'], errors='coerce')
df2022['Ano ingresso'] = df2022['Ano ingresso'].astype('Int64')

df2023['Ano ingresso'] = pd.to_numeric(df2023['Ano ingresso'], errors='coerce')
df2023['Ano ingresso'] = df2023['Ano ingresso'].astype('Int64')

df2024['Ano ingresso'] = pd.to_numeric(df2024['Ano ingresso'], errors='coerce')
df2024['Ano ingresso'] = df2024['Ano ingresso'].astype('Int64')

# INDE 22
df2022['INDE 22'] = pd.to_numeric(df2022['INDE 22'], errors='coerce')
df2022['INDE 22'] = df2022['INDE 22'].astype(float)

df2023['INDE 22'] = pd.to_numeric(df2023['INDE 22'], errors='coerce')
df2023['INDE 22'] = df2023['INDE 22'].astype(float)

df2024['INDE 22'] = pd.to_numeric(df2024['INDE 22'], errors='coerce')
df2024['INDE 22'] = df2024['INDE 22'].astype(float)

# Pedra 23
df2022['Pedra 23'] = None
df2022['Pedra 23'] = df2022['Pedra 23'].astype(str).replace('None', None)

# INDE 23
df2022['INDE 23'] = None
df2022['INDE 23'] = df2022['INDE 23'].astype(float)

df2023['INDE 23'] = pd.to_numeric(df2023['INDE 23'], errors='coerce')
df2023['INDE 23'] = df2023['INDE 23'].astype(float)

df2024['INDE 23'] = pd.to_numeric(df2024['INDE 23'], errors='coerce')
df2024['INDE 23'] = df2024['INDE 23'].astype(float)

# Pedra 24
df2022['Pedra 24'] = None
df2022['Pedra 24'] = df2022['Pedra 24'].astype(str).replace('None', None)

df2023['Pedra 24'] = None
df2023['Pedra 24'] = df2023['Pedra 24'].astype(str).replace('None', None)

# INDE 2024
df2022['INDE 24'] = None
df2022['INDE 24'] = df2022['INDE 24'].astype(float)

df2023['INDE 24'] = None
df2023['INDE 24'] = df2023['INDE 24'].astype(float)

df2024['INDE 24'] = pd.to_numeric(df2024['INDE 24'], errors='coerce')
df2024['INDE 24'] = df2024['INDE 24'].astype(float)

# Cg
df2022['Cg'] = pd.to_numeric(df2022['Cg'], errors='coerce')
df2022['Cg'] = df2022['Cg'].astype(float)

df2023['Cg'] = pd.to_numeric(df2023['Cg'], errors='coerce')
df2023['Cg'] = df2023['Cg'].astype(float)

df2024['Cg'] = pd.to_numeric(df2024['Cg'], errors='coerce')
df2024['Cg'] = df2024['Cg'].astype(float)

# Cf
df2022['Cf'] = pd.to_numeric(df2022['Cf'], errors='coerce')
df2022['Cf'] = df2022['Cf'].astype('Int64')

df2023['Cf'] = pd.to_numeric(df2023['Cf'], errors='coerce')
df2023['Cf'] = df2023['Cf'].astype('Int64')

df2024['Cf'] = pd.to_numeric(df2024['Cf'], errors='coerce')
df2024['Cf'] = df2024['Cf'].astype('Int64')

# Ct
df2022['Ct'] = pd.to_numeric(df2022['Ct'], errors='coerce')
df2022['Ct'] = df2022['Ct'].astype('Int64')

df2023['Ct'] = pd.to_numeric(df2023['Ct'], errors='coerce')
df2023['Ct'] = df2023['Ct'].astype('Int64')

df2024['Ct'] = pd.to_numeric(df2024['Ct'], errors='coerce')
df2024['Ct'] = df2024['Ct'].astype('Int64')

# Nº Av
df2022['Nº Av'] = pd.to_numeric(df2022['Nº Av'], errors='coerce')
df2022['Nº Av'] = df2022['Nº Av'].astype('Int64')

df2023['Nº Av'] = pd.to_numeric(df2023['Nº Av'], errors='coerce')
df2023['Nº Av'] = df2023['Nº Av'].astype('Int64')

df2024['Nº Av'] = pd.to_numeric(df2024['Nº Av'], errors='coerce')
df2024['Nº Av'] = df2024['Nº Av'].astype('Int64')

# Rec Av3
df2024['Rec Av3'] = None
df2024['Rec Av3'] = df2024['Rec Av3'].astype(str).replace('None', None)

# Rec Av4
df2024['Rec Av4'] = None
df2024['Rec Av4'] = df2024['Rec Av4'].astype(str).replace('None', None)

# Avaliador5
df2022['Avaliador5'] = None
df2022['Avaliador5'] = df2022['Avaliador5'].astype(str).replace('None', None)

df2023['Avaliador5'] = None
df2023['Avaliador5'] = df2023['Avaliador5'].astype(str).replace('None', None)

# Avaliador6
df2022['Avaliador6'] = None
df2022['Avaliador6'] = df2022['Avaliador6'].astype(str).replace('None', None)

df2023['Avaliador6'] = None
df2023['Avaliador6'] = df2023['Avaliador6'].astype(str).replace('None', None)

# IAA
df2022['IAA'] = pd.to_numeric(df2022['IAA'], errors='coerce')
df2022['IAA'] = df2022['IAA'].astype(float)

df2023['IAA'] = pd.to_numeric(df2023['IAA'], errors='coerce')
df2023['IAA'] = df2023['IAA'].astype(float)

df2024['IAA'] = pd.to_numeric(df2024['IAA'], errors='coerce')
df2024['IAA'] = df2024['IAA'].astype(float)

# IEG
df2022['IEG'] = pd.to_numeric(df2022['IEG'], errors='coerce')
df2022['IEG'] = df2022['IEG'].astype(float)

df2023['IEG'] = pd.to_numeric(df2023['IEG'], errors='coerce')
df2023['IEG'] = df2023['IEG'].astype(float)

df2024['IEG'] = pd.to_numeric(df2024['IEG'], errors='coerce')
df2024['IEG'] = df2024['IEG'].astype(float)

# IPS
df2022['IPS'] = pd.to_numeric(df2022['IPS'], errors='coerce')
df2022['IPS'] = df2022['IPS'].astype(float)

df2023['IPS'] = pd.to_numeric(df2023['IPS'], errors='coerce')
df2023['IPS'] = df2023['IPS'].astype(float)

df2024['IPS'] = pd.to_numeric(df2024['IPS'], errors='coerce')
df2024['IPS'] = df2024['IPS'].astype(float)

# IPP
df2022['IPP'] = None
df2022['IPP'] = df2022['IPP'].astype(float)

df2023['IPP'] = pd.to_numeric(df2023['IPP'], errors='coerce')
df2023['IPP'] = df2023['IPP'].astype(float)

df2024['IPP'] = pd.to_numeric(df2024['IPP'], errors='coerce')
df2024['IPP'] = df2024['IPP'].astype(float)

# IDA
df2022['IDA'] = pd.to_numeric(df2022['IDA'], errors='coerce')
df2022['IDA'] = df2022['IDA'].astype(float)

df2023['IDA'] = pd.to_numeric(df2023['IDA'], errors='coerce')
df2023['IDA'] = df2023['IDA'].astype(float)

df2024['IDA'] = pd.to_numeric(df2024['IDA'], errors='coerce')
df2024['IDA'] = df2024['IDA'].astype(float)

# Mat
df2022['Mat'] = pd.to_numeric(df2022['Mat'], errors='coerce')
df2022['Mat'] = df2022['Mat'].astype(float)

df2023['Mat'] = pd.to_numeric(df2023['Mat'], errors='coerce')
df2023['Mat'] = df2023['Mat'].astype(float)

df2024['Mat'] = pd.to_numeric(df2024['Mat'], errors='coerce')
df2024['Mat'] = df2024['Mat'].astype(float)

# Por
df2022['Por'] = pd.to_numeric(df2022['Por'], errors='coerce')
df2022['Por'] = df2022['Por'].astype(float)

df2023['Por'] = pd.to_numeric(df2023['Por'], errors='coerce')
df2023['Por'] = df2023['Por'].astype(float)

df2024['Por'] = pd.to_numeric(df2024['Por'], errors='coerce')
df2024['Por'] = df2024['Por'].astype(float)

# Ing
df2022['Ing'] = pd.to_numeric(df2022['Ing'], errors='coerce')
df2022['Ing'] = df2022['Ing'].astype(float)

df2023['Ing'] = pd.to_numeric(df2023['Ing'], errors='coerce')
df2023['Ing'] = df2023['Ing'].astype(float)

df2024['Ing'] = pd.to_numeric(df2024['Ing'], errors='coerce')
df2024['Ing'] = df2024['Ing'].astype(float)

# IPV
df2022['IPV'] = pd.to_numeric(df2022['IPV'], errors='coerce')
df2022['IPV'] = df2022['IPV'].astype(float)

df2023['IPV'] = pd.to_numeric(df2023['IPV'], errors='coerce')
df2023['IPV'] = df2023['IPV'].astype(float)

df2024['IPV'] = pd.to_numeric(df2024['IPV'], errors='coerce')
df2024['IPV'] = df2024['IPV'].astype(float)

# IAN
df2022['IAN'] = pd.to_numeric(df2022['IAN'], errors='coerce')
df2022['IAN'] = df2022['IAN'].astype(float)

df2023['IAN'] = pd.to_numeric(df2023['IAN'], errors='coerce')
df2023['IAN'] = df2023['IAN'].astype(float)

df2024['IAN'] = pd.to_numeric(df2024['IAN'], errors='coerce')
df2024['IAN'] = df2024['IAN'].astype(float)

# Defasagem
df2022['Defasagem'] = pd.to_numeric(df2022['Defasagem'], errors='coerce')
df2022['Defasagem'] = df2022['Defasagem'].astype('Int64')

df2023['Defasagem'] = pd.to_numeric(df2023['Defasagem'], errors='coerce')
df2023['Defasagem'] = df2023['Defasagem'].astype('Int64')

df2024['Defasagem'] = pd.to_numeric(df2024['Defasagem'], errors='coerce')
df2024['Defasagem'] = df2024['Defasagem'].astype('Int64')

# Escola
df2022['Escola'] = None
df2022['Escola'] = df2022['Escola'].astype(str).replace('None', None)

df2023['Escola'] = None
df2023['Escola'] = df2023['Escola'].astype(str).replace('None', None)

# Ativo/ Inativo
df2022['Ativo/ Inativo'] = None
df2022['Ativo/ Inativo'] = df2022['Ativo/ Inativo'].astype(str).replace('None', None)

df2023['Ativo/ Inativo'] = None
df2023['Ativo/ Inativo'] = df2023['Ativo/ Inativo'].astype(str).replace('None', None)

# Origem
df2022['Origem'] = 'PEDE2022'
df2022['Origem'] = df2022['Origem'].astype(str).replace('None', None)

df2023['Origem'] = 'PEDE2023'
df2023['Origem'] = df2023['Origem'].astype(str).replace('None', None)

df2024['Origem'] = 'PEDE2024'
df2024['Origem'] = df2024['Origem'].astype(str).replace('None', None)

# --- Unir os DataFrames ---
print("\n" + "="*50)
print("Merge")
print("="*50)

columns_2022 = df2022[['RA', 'Fase', 'Turma', 'Nome', 'Data de Nasc', 'Ano Nasc', 'Idade', 'Gênero',
'Ano ingresso', 'Instituição de ensino', 'Pedra 20', 'Pedra 21', 'Pedra 22', 'INDE 22', 'Pedra 23',
'INDE 23', 'Pedra 24', 'INDE 24', 'Cg', 'Cf', 'Ct', 'Nº Av', 'Avaliador1', 'Rec Av1', 'Avaliador2',
'Rec Av2', 'Avaliador3', 'Rec Av3', 'Avaliador4', 'Rec Av4', 'Avaliador5', 'Avaliador6', 'IAA', 'IEG',
'IPS', 'IPP', 'Rec Psicologia', 'IDA', 'Mat', 'Por', 'Ing', 'Indicado', 'Atingiu PV', 'IPV', 'IAN',
'Fase Ideal', 'Defasagem', 'Destaque IEG', 'Destaque IDA', 'Destaque IPV', 'Escola', 'Ativo/ Inativo',
'Origem']].copy()

columns_2023 = df2023[['RA', 'Fase', 'Turma', 'Nome', 'Data de Nasc', 'Ano Nasc', 'Idade', 'Gênero',
'Ano ingresso', 'Instituição de ensino', 'Pedra 20', 'Pedra 21', 'Pedra 22', 'INDE 22', 'Pedra 23',
'INDE 23', 'Pedra 24', 'INDE 24', 'Cg', 'Cf', 'Ct', 'Nº Av', 'Avaliador1', 'Rec Av1', 'Avaliador2',
'Rec Av2', 'Avaliador3', 'Rec Av3', 'Avaliador4', 'Rec Av4', 'Avaliador5', 'Avaliador6', 'IAA', 'IEG',
'IPS', 'IPP', 'Rec Psicologia', 'IDA', 'Mat', 'Por', 'Ing', 'Indicado', 'Atingiu PV', 'IPV', 'IAN',
'Fase Ideal', 'Defasagem', 'Destaque IEG', 'Destaque IDA', 'Destaque IPV', 'Escola', 'Ativo/ Inativo',
'Origem']].copy()

columns_2024 = df2024[['RA', 'Fase', 'Turma', 'Nome', 'Data de Nasc', 'Ano Nasc', 'Idade', 'Gênero',
'Ano ingresso', 'Instituição de ensino', 'Pedra 20', 'Pedra 21', 'Pedra 22', 'INDE 22', 'Pedra 23',
'INDE 23', 'Pedra 24', 'INDE 24', 'Cg', 'Cf', 'Ct', 'Nº Av', 'Avaliador1', 'Rec Av1', 'Avaliador2',
'Rec Av2', 'Avaliador3', 'Rec Av3', 'Avaliador4', 'Rec Av4', 'Avaliador5', 'Avaliador6', 'IAA', 'IEG',
'IPS', 'IPP', 'Rec Psicologia', 'IDA', 'Mat', 'Por', 'Ing', 'Indicado', 'Atingiu PV', 'IPV', 'IAN',
'Fase Ideal', 'Defasagem', 'Destaque IEG', 'Destaque IDA', 'Destaque IPV', 'Escola', 'Ativo/ Inativo',
'Origem']].copy()

df = pd.concat([columns_2022, columns_2023, columns_2024], ignore_index=True)

cols_string = ['RA', 'Fase', 'Turma', 'Nome', 'Gênero', 'Instituição de ensino', 'Pedra 20',
'Pedra 21', 'Pedra 22', 'Pedra 23', 'Pedra 24', 'Avaliador1', 'Rec Av1', 'Avaliador2', 'Rec Av2',
'Avaliador3', 'Rec Av3', 'Avaliador4', 'Rec Av4', 'Avaliador5', 'Avaliador6', 'Rec Psicologia',
'Indicado', 'Atingiu PV', 'Fase Ideal', 'Destaque IEG', 'Destaque IDA', 'Destaque IPV', 'Escola',
'Ativo/ Inativo', 'Origem']
df[cols_string] = df[cols_string].fillna('null').astype(str)
for col in cols_string:
    df[col] = df[col].apply(normalize_string)

df['Data de Nasc'] = pd.to_datetime(df['Data de Nasc'], errors='coerce')
df['Data de Nasc'] = df['Data de Nasc'].dt.normalize()

df['Ano Nasc'] = pd.to_numeric(df['Ano Nasc'], errors='coerce').astype('Int64')
df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce').astype('Int64')
df['Ano ingresso'] = pd.to_numeric(df['Ano ingresso'], errors='coerce').astype('Int64')
df['Cf'] = pd.to_numeric(df['Cf'], errors='coerce').astype('Int64')
df['Ct'] = pd.to_numeric(df['Ct'], errors='coerce').astype('Int64')
df['Nº Av'] = pd.to_numeric(df['Nº Av'], errors='coerce').astype('Int64')
df['Defasagem'] = pd.to_numeric(df['Defasagem'], errors='coerce').astype('Int64')

df['INDE 22'] = pd.to_numeric(df['INDE 22'], errors='coerce').astype(float)
df['INDE 23'] = pd.to_numeric(df['INDE 23'], errors='coerce').astype(float)
df['INDE 24'] = pd.to_numeric(df['INDE 24'], errors='coerce').astype(float)
df['Cg'] = pd.to_numeric(df['Cg'], errors='coerce').astype(float)
df['IAA'] = pd.to_numeric(df['IAA'], errors='coerce').astype(float)
df['IEG'] = pd.to_numeric(df['IEG'], errors='coerce').astype(float)
df['IPS'] = pd.to_numeric(df['IPS'], errors='coerce').astype(float)
df['IPP'] = pd.to_numeric(df['IPP'], errors='coerce').astype(float)
df['IDA'] = pd.to_numeric(df['IDA'], errors='coerce').astype(float)
df['Mat'] = pd.to_numeric(df['Mat'], errors='coerce').astype(float)
df['Por'] = pd.to_numeric(df['Por'], errors='coerce').astype(float)
df['Ing'] = pd.to_numeric(df['Ing'], errors='coerce').astype(float)
df['IPV'] = pd.to_numeric(df['IPV'], errors='coerce').astype(float)
df['IAN'] = pd.to_numeric(df['IAN'], errors='coerce').astype(float)

# --- Exibe os primeiros RAs ---
print("\nPrimeiros 20 RAs do novo DataFrame:")
print(df.head(20))

print("\nÚltimos 20 RAs do novo DataFrame:")
print(df.tail(20))

# --- Tipos de dados ---
print("\nTipos de dados:")
print(df.dtypes)

# --- Exportação dos Dados ---
output_file = 'BASE DE DADOS PEDE 2024 - DATATHON - NORMALIZADA.txt'

if os.path.exists(output_file):
    os.remove(output_file)
    print(f"\nArquivo '{output_file}' existente removido.")

df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
print(f"Arquivo '{output_file}' criado com sucesso.")