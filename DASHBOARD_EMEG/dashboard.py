import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Configuração inicial do Streamlit
st.set_page_config(page_title="Dashboard de Vendas", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

st.title(" :bar_chart: Dashboard de Vendas")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Aplicando tema escuro
st.markdown(
    """
    <style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
    }
    div.stButton > button:hover {
        background-color: #45a049;
        color: white;
    }
    .stSidebar, .css-1d391kg {
        background-color: #1A1A1A;
        color: #FAFAFA;
    }
    .stTextInput>div>div>input {
        background-color: #333333;
        color: #FAFAFA;
    }
    .stDateInput>div>div>input {
        background-color: #333333;
        color: #FAFAFA;
    }
    .stSelectbox>div>div>div>div {
        background-color: #333333;
        color: #FAFAFA;
    }
    .stFileUploader>label>div {
        background-color: #333333;
        color: #FAFAFA;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Carregar o arquivo CSV
uploaded_file = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="latin1", delimiter=';')
else:
    st.stop()

# Processar dados
month_mapping = {
    'janeiro': '01',
    'fevereiro': '02',
    'março': '03',
    'abril': '04',
    'maio': '05',
    'junho': '06',
    'julho': '07',
    'agosto': '08',
    'setembro': '09',
    'outubro': '10',
    'novembro': '11',
    'dezembro': '12'
}

df['Mês_Num'] = df['Mês'].map(month_mapping)
df['Data'] = pd.to_datetime(df['Ano'].astype(str) + '-' + df['Mês_Num'], format='%Y-%m')
df["month_year"] = df["Data"].dt.to_period("M")

# Criar coluna 'Faixa de Peso'
df['Faixa de Peso'] = pd.cut(df['PESO'], bins=[0, 50, 100, 200, 500, 1000, float('inf')],
                             labels=['0-50', '50-100', '100-200', '200-500', '500-1000', '1000+'])

# Filtragem de dados por data
col1, col2 = st.columns((2))
startDate = pd.to_datetime(df["Data"]).min()
endDate = pd.to_datetime(df["Data"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Data de Início", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("Data de Fim", endDate))

df = df[(df["Data"] >= date1) & (df["Data"] <= date2)].copy()

# Filtros laterais
st.sidebar.header("Escolha seus filtros:")
clientes = st.sidebar.multiselect("Escolha o Cliente", df["CLIENTE"].unique())
anos = st.sidebar.multiselect("Escolha o Ano", df["Ano"].unique())
meses = st.sidebar.multiselect("Escolha o Mês", df["Mês"].unique())
classificacoes = st.sidebar.multiselect("Escolha a Classificação", df["Classificação"].unique())
perfis = st.sidebar.multiselect("Escolha o Perfil Cliente", df["Perfil Cliente"].unique())
faixas_peso = st.sidebar.multiselect("Escolha a Faixa de Peso", df['Faixa de Peso'].unique())

# Aplicação dos filtros
df_filtered = df.copy()
if clientes:
    df_filtered = df_filtered[df_filtered["CLIENTE"].isin(clientes)]
if anos:
    df_filtered = df_filtered[df_filtered["Ano"].isin(anos)]
if meses:
    df_filtered = df_filtered[df_filtered["Mês"].isin(meses)]
if classificacoes:
    df_filtered = df_filtered[df_filtered["Classificação"].isin(classificacoes)]
if perfis:
    df_filtered = df_filtered[df_filtered["Perfil Cliente"].isin(perfis)]
if faixas_peso:
    df_filtered = df_filtered[df_filtered['Faixa de Peso'].isin(faixas_peso)]

# KPIs
total_revenue = df_filtered['RECEITA'].sum()
total_weight = df_filtered['PESO'].sum()
total_customers = df_filtered['CLIENTE'].nunique()

st.markdown("### KPIs")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Receita Total", value=f"R$ {total_revenue:,.2f}")
kpi2.metric(label="Peso Total Transportado", value=f"{total_weight:,.2f} kg")
kpi3.metric(label="Total de Clientes", value=total_customers)

# Gráficos e tabelas
col1, col2 = st.columns((2))

with col1:
    st.subheader("Receita por Classificação de Cliente")
    classificacao_df = df_filtered.groupby(by=["Classificação"], as_index=False)["RECEITA"].sum()
    fig = px.bar(classificacao_df, x="Classificação", y="RECEITA", text=classificacao_df["RECEITA"].apply(lambda x: f'R$ {x:,.2f}'),
                 template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Receita por Cliente")
    cliente_df = df_filtered.groupby(by=["CLIENTE"], as_index=False)["RECEITA"].sum().nlargest(10, 'RECEITA')
    fig = px.pie(cliente_df, values="RECEITA", names="CLIENTE", hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
    )
    st.plotly_chart(fig, use_container_width=True)

# Top Clientes por Receita
st.subheader("Top Clientes por Receita")
top_clients = df_filtered.groupby('CLIENTE')['RECEITA'].sum().reset_index().sort_values(by='RECEITA', ascending=False).head(10)
fig = px.bar(top_clients, x='CLIENTE', y='RECEITA', text=top_clients["RECEITA"].apply(lambda x: f'R$ {x:,.2f}'),
             template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig, use_container_width=True)

# Comparar receita entre diferentes períodos
st.subheader("Comparar Receita entre Diferentes Períodos")

# Seleção de períodos
col1, col2 = st.columns(2)
with col1:
    period1_start = st.date_input("Data de Início do Período 1", value=pd.to_datetime("2023-01-01"))
    period1_end = st.date_input("Data de Fim do Período 1", value=pd.to_datetime("2023-12-31"))

with col2:
    period2_start = st.date_input("Data de Início do Período 2", value=pd.to_datetime("2024-01-01"))
    period2_end = st.date_input("Data de Fim do Período 2", value=pd.to_datetime("2024-12-31"))

# Filtragem dos dados para os períodos selecionados
period1_df = df[(df["Data"] >= pd.to_datetime(period1_start)) & (df["Data"] <= pd.to_datetime(period1_end))]
period2_df = df[(df["Data"] >= pd.to_datetime(period2_start)) & (df["Data"] <= pd.to_datetime(period2_end))]

# Cálculo das receitas para os períodos
period1_revenue = period1_df['RECEITA'].sum()
period2_revenue = period2_df['RECEITA'].sum()

# Gráfico de comparação
comparison_df = pd.DataFrame({
    "Período": ["Período 1", "Período 2"],
    "Receita": [period1_revenue, period2_revenue]
})

fig_comparison = px.bar(comparison_df, x="Período", y="Receita", text=comparison_df["Receita"].apply(lambda x: f'R$ {x:,.2f}'),
                        title="Comparação de Receita entre Períodos", labels={"Receita": "Receita Total"}, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig_comparison.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig_comparison, use_container_width=True)

# Análise de Crescimento Mensal
st.subheader('Análise de Crescimento Mensal da Receita')
growth_df = df_filtered.groupby(df_filtered['Data'].dt.to_period('M'))['RECEITA'].sum().reset_index()
growth_df['Data'] = growth_df['Data'].astype(str)  # Convertendo para string
fig = px.line(growth_df, x='Data', y='RECEITA', title='Crescimento Mensal da Receita', template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig, use_container_width=True)

# Comparação de Receita e Peso Transportado
st.subheader("Comparação de Receita e Peso Transportado")
comparison_df = df_filtered.groupby(by=["Ano", "Mês"], as_index=False).agg({"RECEITA": "sum", "PESO": "sum"})
comparison_df = comparison_df.sort_values(by=["Ano", "Mês"])
fig = px.bar(comparison_df, x="Mês", y=["RECEITA", "PESO"], barmode="group", facet_col="Ano",
             labels={"value": "Valor", "variable": "Métrica"}, title="Comparação de Receita e Peso Transportado por Mês e Ano", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig, use_container_width=True)

# Distribuição da Receita por Faixa de Peso
st.subheader("Distribuição da Receita por Faixa de Peso")
faixa_peso_df = df_filtered.groupby(by=["Faixa de Peso"], as_index=False)["RECEITA"].sum()
fig = px.bar(faixa_peso_df, x="Faixa de Peso", y="RECEITA", text=faixa_peso_df["RECEITA"].apply(lambda x: f'R$ {x:,.2f}'),
             title="Distribuição da Receita por Faixa de Peso", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig, use_container_width=True)

# Análise de Receita por Perfil de Cliente
st.subheader("Receita por Perfil de Cliente")
perfil_df = df_filtered.groupby(by=["Perfil Cliente"], as_index=False)["RECEITA"].sum()
fig = px.pie(perfil_df, values="RECEITA", names="Perfil Cliente", hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
fig.update_traces(text=perfil_df["Perfil Cliente"], textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# Heatmap de Receita
st.subheader("Heatmap de Receita ao Longo do Tempo")
heatmap_df = df_filtered.pivot_table(values='RECEITA', index=df_filtered['Data'].dt.year, columns=df_filtered['Data'].dt.month, aggfunc='sum', fill_value=0)
fig_heatmap = px.imshow(heatmap_df, labels={'color': 'Receita'}, x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        y=heatmap_df.index, title='Heatmap de Receita por Mês e Ano', template="plotly_dark", color_continuous_scale=px.colors.sequential.Plasma)
fig_heatmap.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Análise de séries temporais
st.subheader('Análise de Séries Temporais')
linechart = pd.DataFrame(df_filtered.groupby(df_filtered["month_year"].dt.strftime("%Y-%b"))["RECEITA"].sum()).reset_index()
fig2 = px.line(linechart, x="month_year", y="RECEITA", labels={"RECEITA": "Valor"}, height=500, width=1000, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig2.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig2, use_container_width=True)

with st.expander("Dados de Séries Temporais"):
    st.write(linechart.T.style.background_gradient(cmap="plasma"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Baixar Dados', data=csv, file_name="TimeSeries.csv", mime='text/csv')

# Sumário de vendas por Cliente
st.subheader(":point_right: Sumário de Vendas por Cliente Mensal")
with st.expander("Tabela de Sumário"):
    df_sample = df[0:5][["CLIENTE", "RECEITA", "PESO", "Classificação"]]
    fig = ff.create_table(df_sample, colorscale="plasma")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Tabela de Cliente Mensal")
    df["month"] = df["Data"].dt.month_name()
    cliente_Year = pd.pivot_table(data=df, values="RECEITA", index=["CLIENTE"], columns="month")
    st.write(cliente_Year.style.background_gradient(cmap="plasma"))

# Gráfico de dispersão
st.subheader("Relação entre Receita e Peso usando Scatter Plot")
data1 = px.scatter(df_filtered, x="RECEITA", y="PESO", size="Total de Compras", 
                   labels={"RECEITA": "Receita", "PESO": "Peso", "Total de Compras": "Compras"},
                   title="Relação entre Receita e Peso", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
data1.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(data1, use_container_width=True)

# Gráficos adicionais de comparação de porcentagens e crescimento

# Crescimento Percentual de Receita e Peso
st.subheader("Crescimento Percentual de Receita e Peso")
growth_percentage_df = df_filtered.groupby(['Ano', 'Mês'], as_index=False).agg({"RECEITA": "sum", "PESO": "sum"})
growth_percentage_df['Receita_Percentual'] = growth_percentage_df['RECEITA'].pct_change().fillna(0) * 100
growth_percentage_df['Peso_Percentual'] = growth_percentage_df['PESO'].pct_change().fillna(0) * 100
fig_growth_percentage = px.bar(growth_percentage_df, x='Mês', y=['Receita_Percentual', 'Peso_Percentual'], barmode='group', color='Ano',
                                labels={"value": "Crescimento Percentual", "variable": "Métrica"}, title="Crescimento Percentual de Receita e Peso", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig_growth_percentage.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig_growth_percentage, use_container_width=True)

# Comparação de Crescimento de Peso por Cliente ao Longo dos Anos
st.subheader("Comparação de Crescimento de Peso por Cliente ao Longo dos Anos")
client_weight_growth_df = df_filtered.groupby(['CLIENTE', 'Ano'], as_index=False).agg({"PESO": "sum"})
fig_client_weight_growth = px.bar(client_weight_growth_df, x='Ano', y='PESO', color='CLIENTE', 
                                   labels={"PESO": "Peso Total", "Ano": "Ano", "CLIENTE": "Cliente"},
                                   title="Comparação de Crescimento de Peso por Cliente ao Longo dos Anos", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig_client_weight_growth.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig_client_weight_growth, use_container_width=True)

# Crescimento Percentual de Receita por Cliente
st.subheader("Crescimento Percentual de Receita por Cliente")
client_revenue_growth_df = df_filtered.groupby(['CLIENTE', 'Ano'], as_index=False).agg({"RECEITA": "sum"})
client_revenue_growth_df['Receita_Percentual'] = client_revenue_growth_df.groupby('CLIENTE')['RECEITA'].pct_change().fillna(0) * 100
fig_client_revenue_growth = px.pie(client_revenue_growth_df, values='Receita_Percentual', names='CLIENTE', 
                                    labels={"Receita_Percentual": "Crescimento Percentual de Receita", "Ano": "Ano", "CLIENTE": "Cliente"},
                                    title="Crescimento Percentual de Receita por Cliente", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig_client_revenue_growth.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)
st.plotly_chart(fig_client_revenue_growth, use_container_width=True)

# Download de dados originais
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Baixar Dados', data=csv, file_name="Dados.csv", mime='text/csv')


