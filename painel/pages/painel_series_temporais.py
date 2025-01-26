from conexao_com_banco import Consulta
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graficos import Graficos
import ast
from streamlit_extras.switch_page_button import switch_page
import numpy as np

import sys
import os

# Adiciona o diretório do arquivo atual ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# import sqlite3
dados = Consulta()

# ---------------------------DADOS
# Retorna informações como commit, id, endereço data hora...
df_filtro = dados.consultar_modelos_st()
# data_metricas = dados.consultar_metricas() # Retonrna as metricas
# dataset =  consultar_valores()

graficos = Graficos()

st.set_page_config(layout="wide")

# Para filtro
df_filtro['id_combinado'] = df_filtro['commit_id'].astype(
    str) + ' - ' + df_filtro['controle_de_versao'].astype(str)

aba1, aba2, aba3 = st.tabs(['Painel', 'Métricas', 'Gráficos'])


with aba1:
    id_selecionado = st.selectbox('ID, Modelos', df_filtro['id_combinado'])
    query = """
    id_combinado in @id_selecionado
    """
    df_filtrado = df_filtro.query(query)
    st.dataframe(df_filtrado)

    # Consulta os valores usando a primeira linha do DataFrame filtrado
    id_atual = int(df_filtrado.iloc[0, 0])
    commit_id = str(df_filtrado.iloc[0, 1])

    st.page_link("./painel_principal.py",
                 label="Voltar para o Painel Principal")

# Garantindo que o DataFrame filtrado não está vazio antes de consultar métricas
if not df_filtrado.empty:
    endereco = df_filtrado.iloc[0, 2]  # Pegando o valor diretamente
    commit_id = df_filtrado.iloc[0, 1]  # Pegando o valor diretamente

# df_metricas = dados.consultar_metricas_re(
#     # Retorna as metricas
#     commit_id=str(df_filtrado.iloc[0, 1]), endereco=str(df_filtrado.iloc[0, 2]))

with aba2:
    st.title('Ola mundo!')

with aba3:
    df_decomposicao = dados.consultar_decomposicao_st(
        # Retorna as metricas
        commit_id=str(df_filtrado.iloc[0, 1]), endereco=str(df_filtrado.iloc[0, 2]))

    st.dataframe(df_decomposicao)
    
    st.plotly_chart(graficos.plot_decomposicao(df_decomposicao,'titulo'))
