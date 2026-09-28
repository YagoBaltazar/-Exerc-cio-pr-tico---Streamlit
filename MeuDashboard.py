from pathlib import Path

import streamlit as st
import pandas as pd

CAMINHO_CSV = Path(__file__).parent / 'vendas.csv'

st.title('Dashboard de Vendas')


@st.cache_data
def carregar_dados():
    df = pd.read_csv(CAMINHO_CSV, parse_dates=['data'])
    return df


df = carregar_dados()

st.sidebar.title('Filtros')

categorias_disponiveis = df['categoria'].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias',
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

df_filtrado = df[df['categoria'].isin(categorias_selecionadas)]

col1, col2 = st.columns([1, 1])

receita_total = df_filtrado['valor_venda'].sum()
total_pedidos = df_filtrado['pedido_id'].nunique()

with col1:
    st.metric(label='Receita Total', value=f'R$ {receita_total:,.2f}')

with col2:
    st.metric(label='Total de Pedidos', value=total_pedidos)

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

with aba1:
    receita_mensal = df_filtrado.set_index('data')['valor_venda'].resample('ME').sum()
    st.area_chart(receita_mensal)

with aba2:
    st.dataframe(df_filtrado)

    csv_para_download = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='Baixar dados filtrados (CSV)',
        data=csv_para_download,
        file_name='vendas_filtradas.csv',
        mime='text/csv',
    )
