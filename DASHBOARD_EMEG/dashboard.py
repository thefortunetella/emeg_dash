import streamlit as st
import plotly.express as px
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Configuração inicial do Streamlit
st.set_page_config(page_title="DASHBOARD DE VENDAS", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

st.title(" :bar_chart: DASHBOARD DE VENDAS")
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
    h1, h2, h3, h4 {
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
    date1 = pd.to_datetime(st.date_input("DATA DE INÍCIO", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("DATA DE FIM", endDate))

df = df[(df["Data"] >= date1) & (df["Data"] <= date2)].copy()

# Filtros laterais
st.sidebar.header("ESCOLHA SEUS FILTROS:")
clientes = st.sidebar.multiselect("ESCOLHA O CLIENTE", df["CLIENTE"].unique())
anos = st.sidebar.multiselect("ESCOLHA O ANO", df["Ano"].unique())
meses = st.sidebar.multiselect("ESCOLHA O MÊS", df["Mês"].unique())
classificacoes = st.sidebar.multiselect("ESCOLHA A CLASSIFICAÇÃO", df["Classificação"].unique())
perfis = st.sidebar.multiselect("ESCOLHA O PERFIL CLIENTE", df["Perfil Cliente"].unique())
faixas_peso = st.sidebar.multiselect("ESCOLHA A FAIXA DE PESO", df['Faixa de Peso'].unique())

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

st.markdown("### KPIS")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="RECEITA TOTAL", value=f"R$ {total_revenue:,.2f}")
kpi2.metric(label="PESO TOTAL TRANSPORTADO", value=f"{total_weight:,.2f} kg")
kpi3.metric(label="TOTAL DE CLIENTES", value=total_customers)

# KPIs adicionais
st.markdown("### KPIS ADICIONAIS")
col1, col2, col3 = st.columns(3)

# Variação percentual da receita anual
annual_revenue_variation = df_filtered.groupby('Ano')['RECEITA'].sum().pct_change().fillna(0).iloc[-1] * 100
col1.metric(label="VARIAÇÃO PERCENTUAL DA RECEITA", value=f"{annual_revenue_variation:.2f}%")

# Média de Peso por Transporte
avg_weight_per_transport = df_filtered['PESO'].mean()
col2.metric(label="MÉDIA DE PESO POR TRANSPORTE", value=f"{avg_weight_per_transport:.2f} kg")

# Porcentagem de clientes retidos ao longo dos anos
frequent_customers = df_filtered[df_filtered['Perfil Cliente'] == 'Frequente']['CLIENTE'].nunique()
retained_customers_percentage = (frequent_customers / df_filtered['CLIENTE'].nunique()) * 100
col3.metric(label="PORCENTAGEM DE CLIENTES RETIDOS", value=f"{retained_customers_percentage:.2f}%")

# Gráficos e tabelas
col1, col2 = st.columns((2))

# Gráfico de receita por classificação de cliente
with col1:
    st.subheader("RECEITA POR CLASSIFICAÇÃO DE CLIENTE")
    classificacao_df = df_filtered.groupby(by=["Classificação"], as_index=False)["RECEITA"].sum()
    fig = px.bar(classificacao_df, x="Classificação", y="RECEITA", text=classificacao_df["RECEITA"].apply(lambda x: f'R$ {x:,.2f}'),
                 template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(
        title="RECEITA POR CLASSIFICAÇÃO DE CLIENTE",
        xaxis_title="CLASSIFICAÇÃO",
        yaxis_title="RECEITA (R$)",
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="white"),
        title_font=dict(size=24, color="white"),
        xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
        yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de receita por cliente
with col2:
    st.subheader("RECEITA POR CLIENTE")
    cliente_df = df_filtered.groupby(by=["CLIENTE"], as_index=False)["RECEITA"].sum().nlargest(10, 'RECEITA')
    fig = px.pie(cliente_df, values="RECEITA", names="CLIENTE", hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(
        title="RECEITA POR CLIENTE",
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color="white"),
        title_font=dict(size=24, color="white"),
        legend=dict(font=dict(size=12, color="white"))
    )
    st.plotly_chart(fig, use_container_width=True)

# Top Clientes por Receita
st.subheader("TOP CLIENTES POR RECEITA")
top_clients = df_filtered.groupby('CLIENTE')['RECEITA'].sum().reset_index().sort_values(by='RECEITA', ascending=False).head(10)
fig = px.bar(top_clients, x='CLIENTE', y='RECEITA', text=top_clients["RECEITA"].apply(lambda x: f'R$ {x:,.2f}'),
             template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    title="TOP CLIENTES POR RECEITA",
    xaxis_title="CLIENTE",
    yaxis_title="RECEITA (R$)",
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(fig, use_container_width=True)

# Comparar receita entre diferentes períodos
st.subheader("COMPARAR RECEITA ENTRE DIFERENTES PERÍODOS")

# Seleção de períodos
col1, col2 = st.columns(2)
with col1:
    period1_start = st.date_input("DATA DE INÍCIO DO PERÍODO 1", value=pd.to_datetime("2023-01-01"))
    period1_end = st.date_input("DATA DE FIM DO PERÍODO 1", value=pd.to_datetime("2023-12-31"))

with col2:
    period2_start = st.date_input("DATA DE INÍCIO DO PERÍODO 2", value=pd.to_datetime("2024-01-01"))
    period2_end = st.date_input("DATA DE FIM DO PERÍODO 2", value=pd.to_datetime("2024-12-31"))

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
                        title="COMPARAÇÃO DE RECEITA ENTRE PERÍODOS", labels={"Receita": "RECEITA TOTAL"}, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig_comparison.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict
        title_font=dict(size=24, color="white")),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(fig_comparison, use_container_width=True)

# Análise de Crescimento Mensal
st.subheader('ANÁLISE DE CRESCIMENTO MENSAL DA RECEITA')
growth_df = df_filtered.groupby(df_filtered['Data'].dt.to_period('M'))['RECEITA'].sum().reset_index()
growth_df['Data'] = growth_df['Data'].astype(str)  # Convertendo para string
fig = px.line(growth_df, x='Data', y='RECEITA', title='CRESCIMENTO MENSAL DA RECEITA', template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(fig, use_container_width=True)

# Comparação de Receita e Peso Transportado
st.subheader("COMPARAÇÃO DE RECEITA E PESO TRANSPORTADO")
comparison_df = df_filtered.groupby(by=["Ano", "Mês"], as_index=False).agg({"RECEITA": "sum", "PESO": "sum"})
comparison_df = comparison_df.sort_values(by=["Ano", "Mês"])
fig = px.bar(comparison_df, x="Mês", y=["RECEITA", "PESO"], barmode="group", facet_col="Ano",
             labels={"value": "VALOR", "variable": "MÉTRICA"}, title="COMPARAÇÃO DE RECEITA E PESO TRANSPORTADO POR MÊS E ANO", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(fig, use_container_width=True)

# Distribuição da Receita por Faixa de Peso
st.subheader("DISTRIBUIÇÃO DA RECEITA POR FAIXA DE PESO")
faixa_peso_df = df_filtered.groupby(by=["Faixa de Peso"], as_index=False)["RECEITA"].sum()
fig = px.bar(faixa_peso_df, x="Faixa de Peso", y="RECEITA", text=faixa_peso_df["RECEITA"].apply(lambda x: f'R$ {x:,.2f}'),
             title="DISTRIBUIÇÃO DA RECEITA POR FAIXA DE PESO", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(fig, use_container_width=True)

# Análise de Receita por Perfil de Cliente
st.subheader("RECEITA POR PERFIL DE CLIENTE")
perfil_df = df_filtered.groupby(by=["Perfil Cliente"], as_index=False)["RECEITA"].sum()
fig = px.pie(perfil_df, values="RECEITA", names="Perfil Cliente", hole=0.5, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_layout(
    title="RECEITA POR PERFIL DE CLIENTE",
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    legend=dict(font=dict(size=12, color="white"))
)
fig.update_traces(text=perfil_df["Perfil Cliente"], textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# Heatmap de Receita
st.subheader("HEATMAP DE RECEITA AO LONGO DO TEMPO")
heatmap_df = df_filtered.pivot_table(values='RECEITA', index=df_filtered['Data'].dt.year, columns=df_filtered['Data'].dt.month, aggfunc='sum', fill_value=0)
fig_heatmap = px.imshow(heatmap_df, labels={'color': 'Receita'}, x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        y=heatmap_df.index, title='HEATMAP DE RECEITA POR MÊS E ANO', template="plotly_dark", color_continuous_scale=px.colors.sequential.Plasma)
fig_heatmap.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Análise de séries temporais
st.subheader('ANÁLISE DE SÉRIES TEMPORAIS')
linechart = pd.DataFrame(df_filtered.groupby(df_filtered["month_year"].dt.strftime("%Y-%b"))["RECEITA"].sum()).reset_index()
fig2 = px.line(linechart, x="month_year", y="RECEITA", labels={"RECEITA": "Valor"}, height=500, width=1000, template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
fig2.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(fig2, use_container_width=True)

with st.expander("DADOS DE SÉRIES TEMPORAIS"):
    st.write(linechart.T.style.background_gradient(cmap="plasma"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Baixar Dados', data=csv, file_name="TimeSeries.csv", mime='text/csv')

# Gráfico de dispersão
st.subheader("RELAÇÃO ENTRE RECEITA E PESO USANDO SCATTER PLOT")
data1 = px.scatter(df_filtered, x="RECEITA", y="PESO", size="PESO", 
                   labels={"RECEITA": "Receita", "PESO": "Peso"},
                   title="RELAÇÃO ENTRE RECEITA E PESO", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plasma)
data1.update_layout(
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(color="white"),
    title_font=dict(size=24, color="white"),
    xaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white")),
    yaxis=dict(title_font=dict(size=18, color="white"), tickfont=dict(size=12, color="white"))
)
st.plotly_chart(data1, use_container_width=True)

# Download de dados originais
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Baixar Dados', data=csv, file_name="Dados.csv", mime='text/csv')

