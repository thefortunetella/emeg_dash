
Este projeto é um dashboard de vendas interativo desenvolvido com Streamlit e Plotly. O dashboard permite carregar, filtrar e visualizar dados de vendas de forma dinâmica, proporcionando uma análise detalhada de vários aspectos do desempenho de vendas.
```
```
## Como Usar

1. **Instale as Dependências**:
   Certifique-se de ter o Python instalado em sua máquina. Instale as dependências necessárias usando o seguinte comando:
   ```bash
   pip install streamlit plotly pandas
   ```

2. **Execute o Dashboard**:
   Salve o código do dashboard em um arquivo chamado `dashboard.py` e execute-o usando o seguinte comando:
   ```bash
   streamlit run dashboard.py
   ```

3. **Carregue os Dados**:
   - Clique no botão de upload e selecione seu arquivo de dados (CSV, TXT, XLSX ou XLS).
   - Aguarde até que os dados sejam carregados e processados.

4. **Aplique Filtros**:
   - Utilize a barra lateral para selecionar os filtros desejados (cliente, ano, mês, classificação, perfil do cliente e faixa de peso).

5. **Explore os KPIs e Gráficos**:
   - Acompanhe os KPIs principais na parte superior do dashboard.
   - Navegue pelos diferentes gráficos para obter insights detalhados sobre suas vendas.

6. **Baixe os Dados**:
   - Use os botões de download no final do dashboard para baixar os dados originais e os dados de séries temporais.

## Estrutura do Dashboard

### 1. KPIs

Os KPIs fornecem uma visão rápida e clara dos principais indicadores de desempenho:
- **Receita total**: A soma total da receita no período selecionado.
- **Peso total transportado**: A soma total do peso transportado no período selecionado.
- **Total de clientes**: O número único de clientes no período selecionado.

### 2. Crescimento do Faturamento e Participação

#### Gráfico de Crescimento do Faturamento
Um gráfico de linha que mostra a evolução do faturamento ano a ano. Isso ajuda a identificar tendências de crescimento ou declínio ao longo do tempo.

#### Gráfico de Participação da Receita
Um gráfico de pizza que mostra a participação percentual de cada ano na receita total. Isso permite ver rapidamente quais anos foram mais lucrativos.

### 3. Análise de Receita por Classificação e Cliente

#### Gráfico de Receita por Classificação de Cliente
Um gráfico de barras que mostra a receita total agrupada por diferentes classificações de clientes (e.g., frequente, sazonal, único).

#### Gráfico de Receita por Cliente
Um gráfico de pizza que mostra a receita total dos 10 principais clientes, ajudando a identificar os clientes mais valiosos.

### 4. Análise Comparativa e Distribuições

#### Comparação de Receita entre Diferentes Períodos
Permite comparar a receita total entre dois períodos selecionados, visualizados em um gráfico de barras.

#### Análise de Crescimento Mensal da Receita
Um gráfico de linha que mostra o crescimento mensal da receita, útil para identificar variações sazonais e tendências mensais.

#### Comparação de Receita e Peso Transportado
Um gráfico de barras que compara a receita e o peso transportado por mês e ano, proporcionando uma visão combinada dessas métricas.

#### Distribuição da Receita por Faixa de Peso
Um gráfico de barras que mostra a distribuição da receita em diferentes faixas de peso, útil para entender como o peso transportado impacta a receita.

#### Receita por Perfil de Cliente
Um gráfico de pizza que mostra a receita total agrupada por perfis de clientes, ajudando a identificar quais perfis geram mais receita.

#### Heatmap de Receita ao Longo do Tempo
Um heatmap que visualiza a receita total por mês e ano, proporcionando uma visão clara das variações sazonais ao longo dos anos.

#### Análise de Séries Temporais
Um gráfico de linha que mostra a receita ao longo do tempo, com a opção de baixar os dados de séries temporais.

### 5. Relação entre Receita e Peso
Um gráfico de dispersão que mostra a relação entre a receita e o peso transportado, ajudando a identificar correlações entre essas duas métricas.

## Avaliação de BI

### Insights sobre a Empresa em Análise

Com base na análise dos dados disponíveis, podemos destacar os seguintes insights:

1. **Crescimento Sustentável**:
   - A empresa mostra um crescimento consistente do faturamento ao longo dos anos, indicando uma estratégia de vendas eficaz e uma base de clientes leal.

2. **Clientes Valiosos**:
   - Uma pequena porcentagem de clientes gera uma parte significativa da receita. É crucial focar na retenção e satisfação desses clientes.

3. **Variações Sazonais**:
   - Há variações sazonais na receita, com certos meses mostrando picos significativos. Identificar as causas desses picos pode ajudar a replicar o sucesso em outros períodos.

4. **Impacto do Peso Transportado**:
   - A receita está correlacionada com o peso transportado. Otimizar a logística e transporte pode levar a uma melhoria na margem de lucro.

5. **Diversificação de Classificações de Clientes**:
   - A receita é distribuída entre diferentes classificações de clientes, com clientes frequentes e sazonais contribuindo significativamente. Estratégias de marketing direcionadas podem ser desenvolvidas para cada grupo.

Esses insights podem ajudar a empresa a tomar decisões informadas para melhorar o desempenho de vendas, otimizar operações e desenvolver estratégias de retenção de clientes.

---


