import pandas as pd

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
        print("✅ Todas as colunas comuns possuem os mesmos tipos de dados.")
    else:
        print("⚠️ Divergências de tipos encontradas:")
        for col, types in mismatches:
            print(f"  - Coluna '{col}': {types}")

dfs = {
    'PEDE2022': df2022,
    'PEDE2023': df2023,
    'PEDE2024': df2024
}

verify_structure(dfs)

def normalize_string(text):
    if text is None or text == '':
        return None
    
    text = text.upper()
    
    text = " ".join(text.split())
    
    text = text.strip()

    if text is None or text == '':
        return None

    return text

# Remover colunas
df2023 = df2023.drop('Pedra 23', axis=1)

# Renomear colunas
df2022 = df2022.rename(columns={'Ano nasc': 'Ano Nasc', 'Idade 22': 'Idade'})
df2023 = df2023.rename(columns={'Nome Anonimizado': 'Nome', 'Pedra 2023': 'Pedra 23'})
df2024 = df2024.rename(columns={'Nome Anonimizado': 'Nome', 'Pedra 2024': 'Pedra 24', 'INDE 2024': 'INDE 24'})

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

# Merge
print("\n" + "="*50)
print("Merge")
print("="*50)

columns_2022 = df2022[['RA', 'Fase', 'Turma', 'Nome', 'Data de Nasc', 'Ano Nasc', 'Idade', 'Gênero', 'Ano ingresso', 'Instituição de ensino', 'Pedra 20', 'Pedra 21', 'Pedra 22', 'INDE 22', 'Pedra 23', 'INDE 23', 'Pedra 24', 'INDE 24']].copy()
columns_2023 = df2023[['RA', 'Fase', 'Turma', 'Nome', 'Data de Nasc', 'Ano Nasc', 'Idade', 'Gênero', 'Ano ingresso', 'Instituição de ensino', 'Pedra 20', 'Pedra 21', 'Pedra 22', 'INDE 22', 'Pedra 23', 'INDE 23', 'Pedra 24', 'INDE 24']].copy()
columns_2024 = df2024[['RA', 'Fase', 'Turma', 'Nome', 'Data de Nasc', 'Ano Nasc', 'Idade', 'Gênero', 'Ano ingresso', 'Instituição de ensino', 'Pedra 20', 'Pedra 21', 'Pedra 22', 'INDE 22', 'Pedra 23', 'INDE 23', 'Pedra 24', 'INDE 24']].copy()

df = pd.concat([columns_2022, columns_2023, columns_2024], ignore_index=True)

cols_string = ['RA', 'Fase', 'Turma', 'Nome', 'Gênero', 'Instituição de ensino', 'Pedra 20', 'Pedra 21', 'Pedra 22', 'Pedra 23', 'Pedra 24']
df[cols_string] = df[cols_string].fillna('null').astype(str)
for col in cols_string:
    df[col] = df[col].apply(normalize_string)

df['Data de Nasc'] = pd.to_datetime(df['Data de Nasc'], errors='coerce')
df['Data de Nasc'] = df['Data de Nasc'].dt.normalize()

df['Ano Nasc'] = pd.to_numeric(df['Ano Nasc'], errors='coerce').astype('Int64')
df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce').astype('Int64')
df['Ano ingresso'] = pd.to_numeric(df['Ano ingresso'], errors='coerce').astype('Int64')
df['INDE 22'] = pd.to_numeric(df['INDE 22'], errors='coerce').astype('float')
df['INDE 23'] = pd.to_numeric(df['INDE 23'], errors='coerce').astype('float')
df['INDE 24'] = pd.to_numeric(df['INDE 24'], errors='coerce').astype('float')

# Exibe os primeiros RAs
print("\nPrimeiros 20 RAs do novo DataFrame:")
print(df.head(20))

print("\nÚltimos 20 RAs do novo DataFrame:")
print(df.tail(20))

print("\nTipos de dados:")
print(df.dtypes)