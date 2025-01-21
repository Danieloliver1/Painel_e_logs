

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
df_filtro = dados.consultar_modelos_re()
# data_metricas = dados.consultar_metricas() # Retonrna as metricas
# dataset =  consultar_valores()


graficos = Graficos()

st.set_page_config(layout="wide")

# Carregando dados
# link = '../dados/bando_de_dados_classificacao.csv'
# df = pd.read_csv(link)


# df = pd.concat([dataset, dataset_metricas], axis=1, ignore_index=False)


# Para filtro
df_filtro['id_combinado'] = df_filtro['id'].astype(
    str) + ' - ' + df_filtro['commit_id']


metricas_gerais = [
    "mse", "rmse", "mae", "mre", "mape", "evs", "r_squared", "adj_r2"
]

metricas_reais = [
    "media_real", "mediana_real", "moda_real",
    "desvio_padrao_real", "Q1_real", "Q2_real", "Q3_real",
    "skewness_real", "kurtosis_real"
]

metricas_preditas = [
    "media_pred", "mediana_pred", "moda_pred",
    "desvio_padrao_pred", "Q1_pred", "Q2_pred", "Q3_pred",
    "skewness_pred", "kurtosis_pred"
]

metricas_diferencas = [
    "media_diff", "mediana_diff", "moda_diff",
    "desvio_padrao_diff", "skewness_diff", "kurtosis_diff"
]


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

    valores = dados.consultar_valores_re(
        id_atual=id_atual, commit_id=commit_id)

    # Convertendo a string para uma lista real
    y_test = ast.literal_eval(valores[0]['y_test'])
    # Convertendo a string para uma lista real
    y_pred = ast.literal_eval(valores[0]['y_pred'])

    df = pd.DataFrame({
        'y_test': y_test,
        'y_pred': y_pred
    })

    st.plotly_chart(graficos.grafico_linha(
        df, 'Comparação entre Valores Reais e Previstos'))

    st.page_link("./painel_principal.py",
                 label="Voltar para o Painel Principal")

# Garantindo que o DataFrame filtrado não está vazio antes de consultar métricas
if not df_filtrado.empty:
    id_atual = df_filtrado.iloc[0, 0]  # Pegando o valor diretamente
    commit_id = df_filtrado.iloc[0, 1]  # Pegando o valor diretamente

df_metricas = dados.consultar_metricas_re(
    # Retorna as metricas
    id_atual=int(df_filtrado.iloc[0, 0]), commit_id=str(df_filtrado.iloc[0, 1]))

with aba2:
    id_metric = df_filtrado['commit_id'].iloc[0]  # Obtendo o valor desejado
    id_data = df_filtrado['data'].iloc[0]

    st.markdown(
        f"""
        <style>
            .metric-id-commit, .metric-id-data {{
                font-size: 14px; /* Tamanho específico */
            }}
        </style>
        <div class="metric-id-commit">Inf: {id_metric}</div>
        <div class="metric-id-data">Data da atualização: {id_data}</div>
        """,
        unsafe_allow_html=True
    )

    # st.title('Painel de classificação por classes')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Métricas", divider=True)
        for x in metricas_gerais:
            row_mean = float(df_metricas[x].round(4))
            nome = x.replace('_', ' ')
            # st.metric(nome, row_mean)  # Passando métricas
            st.text(nome)

            # HTML do card
            html_content = f"""
            <div
            style="
                position: relative;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 200px;
                height: 60px;
                overflow: hidden;
                border-radius: 0.25rem;
                background-color: #3d3c3d;
                margin-bottom: 15px;
            "
            >
            <div
                style="
                position: absolute;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                z-index: 1;
                opacity: 0.9;
                border-radius: 0.25rem;
                inset: 0.10rem;
                background-color: #101720;
                "
            >
                <div style="font-size: 20px; font-weight: bold; font-family: Arial;">{row_mean}</div>
            </div>
            <div
                style="
                position: absolute;
                width: 240px;
                height: 80px;
                background-color: white;
                filter: blur(20px);
                left: -70%;
                top: -30%;
                "
            ></div>
            </div>
            """

            # Exibindo o HTML no Streamlit
            st.markdown(
                html_content,
                unsafe_allow_html=True
            )

    with col2:
        st.subheader("Target Real", divider=True)
        for x in metricas_reais:
            row_mean = float(df_metricas[x].round(4))
            nome = x.replace('_', ' ')
            # st.metric(nome, row_mean)  # Passando métricas
            st.text(nome)

            # HTML do card
            html_content = f"""
            <div
            style="
                position: relative;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 200px;
                height: 60px;
                overflow: hidden;
                border-radius: 0.25rem;
                background-color: #3d3c3d;
                margin-bottom: 15px;
            "
            >
            <div
                style="
                position: absolute;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                z-index: 1;
                opacity: 0.9;
                border-radius: 0.25rem;
                inset: 0.10rem;
                background-color: #101720;
                "
            >
                <div style="font-size: 20px; font-weight: bold; font-family: Arial;">{row_mean}</div>
            </div>
            <div
                style="
                position: absolute;
                width: 240px;
                height: 80px;
                background-color: white;
                filter: blur(20px);
                left: -70%;
                top: -30%;
                "
            ></div>
            </div>
            """

            # Exibindo o HTML no Streamlit
            st.markdown(
                html_content,
                unsafe_allow_html=True
            )

    with col3:

        st.subheader("Target Previsto", divider=True)
        for x in metricas_preditas:
            row_mean = float(df_metricas[x].round(4))
            nome = x.replace('_', ' ')
            # st.metric(nome, row_mean)  # Passando métricas

            st.text(nome)

            # HTML do card
            html_content = f"""
            <div
            style="
                position: relative;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 200px;
                height: 60px;
                overflow: hidden;
                border-radius: 0.25rem;
                background-color: #3d3c3d;
                margin-bottom: 15px;
            "
            >
            <div
                style="
                position: absolute;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                z-index: 1;
                opacity: 0.9;
                border-radius: 0.25rem;
                inset: 0.10rem;
                background-color: #101720;
                "
            >
                <div style="font-size: 20px; font-weight: bold; font-family: Arial;">{row_mean}</div>
            </div>
            <div
                style="
                position: absolute;
                width: 240px;
                height: 80px;
                background-color: white;
                filter: blur(20px);
                left: -70%;
                top: -30%;
                "
            ></div>
            </div>
            """

            # Exibindo o HTML no Streamlit
            st.markdown(
                html_content,
                unsafe_allow_html=True
            )

    with col4:
        st.subheader("Direfença entre o real e o previsto", divider=True)
        for x in metricas_diferencas:
            row_mean = float(df_metricas[x].round(4))
            nome = x.replace('_', ' ')
            # st.metric(nome, row_mean)  # Passando métricas
            # Construindo os cards para cada métrica

            st.text(nome)

            # HTML do card
            html_content = f"""
            <div
            style="
                position: relative;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 200px;
                height: 60px;
                overflow: hidden;
                border-radius: 0.25rem;
                background-color: #3d3c3d;
                margin-bottom: 15px;
            "
            >
            <div
                style="
                position: absolute;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                z-index: 1;
                opacity: 0.9;
                border-radius: 0.25rem;
                inset: 0.10rem;
                background-color: #101720;
                "
            >
                <div style="font-size: 20px; font-weight: bold; font-family: Arial;">{row_mean}</div>
            </div>
            <div
                style="
                position: absolute;
                width: 240px;
                height: 80px;
                background-color: white;
                filter: blur(20px);
                left: -70%;
                top: -30%;
                "
            ></div>
            </div>
            """

            # Exibindo o HTML no Streamlit
            st.markdown(
                html_content,
                unsafe_allow_html=True
            )

            # ------------------------------

with aba3:
    # st.title('Painel de regressão')
    col1, col2 = st.columns(2)
    with col1:
        id_metrica01 = st.selectbox('Métricas', metricas_gerais)
        # st.plotly_chart(graficos.grafico_rosca(
        # id_metrica01, df_metricas[id_metrica01].mean(), '#67ace1'))

        # HTML com estilos inline para o card
        html_card_with_text = f"""
        <div
        style="
            width: 190px;
            height: 200px;
            border-radius: 30px;
            background: #212121;
            box-shadow: 15px 15px 30px rgb(25, 25, 25), -15px -15px 30px rgb(60, 60, 60);
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
        "
        >
        {df_metricas[id_metrica01].mean()}
        </div>
        """

        # Exibindo o card com texto no Streamlit
        st.markdown(html_card_with_text, unsafe_allow_html=True)

    with col2:
        # Obtendo o valor desejado
        id_metric = df_filtrado['commit_id'].iloc[0]
        id_data = df_filtrado['data'].iloc[0]

        st.markdown(
            f"""
            <style>
                .metric-id-commit, .metric-id-data {{
                    font-size: 14px; /* Tamanho específico */
                }}
            </style>
            <div class="metric-id-commit">Inf: {id_metric}</div>
            <div class="metric-id-data">Data da atualização: {id_data}</div>
            """,
            unsafe_allow_html=True
        )
        nomes = ["rmse", "mae", "mre", "mape", "EVS", "R squared", "Adj R2"]

        metricas = pd.DataFrame(
            {
                'Metrica': nomes,
                'Valor': df_metricas[["rmse", "mae", "mre", "mape", "evs", "r_squared", "adj_r2"]].mean()
            }
        )

        teste = graficos.barra_gradiente2(metricas)
        st.pyplot(teste)
# ----------------------------------------------------------------
    id_unique = df_filtro['controle_de_versao'].unique()
    id_unique = pd.Series(id_unique)
    id_selecionado = st.selectbox('ID, Modelos', id_unique)

    id_metrica = st.selectbox('ID, Modelos', metricas_gerais)

    df_agrupado_metrica = dados.consultar_metricas_re(endereco=id_selecionado)

    st.plotly_chart(graficos.grafico_linha_detalhada(
        id_metrica, df_agrupado_metrica.index, df_agrupado_metrica[id_metrica].values))

# ----------------------------------------------------------------
    listas = ['y_test', 'y_pred', 'Resíduos']

    classificar_lista = st.selectbox('Escolha o tipo', listas)

    if 'y_test' in classificar_lista or 'y_pred' in classificar_lista:
        valores_da_lista = ast.literal_eval(valores[0][classificar_lista])
    else:
        # Calculando os erros (resíduos)
        y_test = ast.literal_eval(valores[0]['y_test'])
        y_pred = ast.literal_eval(valores[0]['y_pred'])
        # Calculando os erros (resíduos)
        valores_da_lista = np.array(y_test) - np.array(y_pred)

    st.plotly_chart(graficos.distribuicao_normal(
        classificar_lista, valores_da_lista))

    y_test = ast.literal_eval(valores[0]['y_test'])
    y_pred = ast.literal_eval(valores[0]['y_pred'])
    st.plotly_chart(graficos.outline(y_test, y_pred))  # Gráfico

    st.plotly_chart(graficos.outline_residuo(y_test, y_pred))  # Gráfico
