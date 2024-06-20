import pandas as pd

# Função para limpar e converter os valores de receita
def clean_revenue(revenue):
    if isinstance(revenue, str):
        return float(revenue.replace('R$', '').replace('.', '').replace(',', '.').strip())
    return revenue

# Carregar dados
input_file = 'data.csv'
df = pd.read_csv(input_file, delimiter=';', encoding='latin1', names=['Ano', 'Mês', 'CLIENTE', 'RECEITA', 'PESO', 'Classificação'], skiprows=1)

# Tratar valores nulos
df.fillna({'RECEITA': 0, 'PESO': 0}, inplace=True)

# Aplicar função de limpeza na coluna de receita
df['RECEITA'] = df['RECEITA'].apply(clean_revenue)

# Corrigir nomes de clientes
df['CLIENTE'] = df['CLIENTE'].str.replace('Clinte', 'Cliente')

# Verificar tipos de dados
df['RECEITA'] = pd.to_numeric(df['RECEITA'], errors='coerce')
df['PESO'] = pd.to_numeric(df['PESO'], errors='coerce')

# Tratar possíveis valores nulos resultantes da conversão para numérico
df.fillna({'RECEITA': 0, 'PESO': 0}, inplace=True)

# Verificar se há valores duplicados e removê-los
df.drop_duplicates(inplace=True)

# Adicionar colunas de data e semestre
df['Data'] = pd.to_datetime(df['Ano'].astype(str) + '-' + df['Mês'].astype(str), format='%Y-%B', errors='coerce')
df['Semestre'] = df['Data'].dt.to_period('6M')

# Transporte de Peso Total por Semestre
peso_semestre = df.groupby('Semestre')['PESO'].sum().reset_index()
peso_semestre.columns = ['Semestre', 'Peso Total por Semestre']
df = df.merge(peso_semestre, on='Semestre', how='left')

# Receita Total por Semestre
receita_semestre = df.groupby('Semestre')['RECEITA'].sum().reset_index()
receita_semestre.columns = ['Semestre', 'Receita Total por Semestre']
df = df.merge(receita_semestre, on='Semestre', how='left')

# Total de Compras por Cliente
total_compras_cliente = df['CLIENTE'].value_counts().reset_index()
total_compras_cliente.columns = ['CLIENTE', 'Total de Compras']
df = df.merge(total_compras_cliente, on='CLIENTE', how='left')

# Cliente que Mais Comprou
cliente_mais_compras = df.groupby('CLIENTE')['RECEITA'].sum().reset_index().sort_values(by='RECEITA', ascending=False).iloc[0]
df['Cliente que Mais Comprou'] = cliente_mais_compras['CLIENTE']

# Peso Total Transportado por Cliente
peso_total_cliente = df.groupby('CLIENTE')['PESO'].sum().reset_index()
peso_total_cliente.columns = ['CLIENTE', 'Peso Total Transportado']
df = df.merge(peso_total_cliente, on='CLIENTE', how='left')

# Classificar clientes
purchase_counts = df['CLIENTE'].value_counts()
df['Perfil Cliente'] = df['CLIENTE'].map(lambda x: 'Frequente' if purchase_counts[x] > 20 else 'Único' if purchase_counts[x] == 1 else 'Sazonal')

# Variação Percentual da Receita Anual
receita_anual = df.groupby('Ano')['RECEITA'].sum().reset_index()
receita_anual['Variação Receita'] = receita_anual['RECEITA'].pct_change() * 100
df = df.merge(receita_anual[['Ano', 'Variação Receita']], on='Ano', how='left')

# Identificação de Clientes Retidos
df['Cliente Retido'] = df['Perfil Cliente'].apply(lambda x: 1 if x == 'Frequente' else 0)

# Salvar dados tratados em um novo arquivo CSV
df.to_csv('data_tratado.csv', index=False, sep=';', encoding='latin1')
