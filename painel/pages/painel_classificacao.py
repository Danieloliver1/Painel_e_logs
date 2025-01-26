

from conexao_com_banco import Consulta
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from graficos import Graficos
import ast
from streamlit_extras.switch_page_button import switch_page

import sys
import os

# Adiciona o diretório do arquivo atual ao sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# import sqlite3
dados = Consulta()

# ---------------------------DADOS
# Retorna informações como commit, id, endereço data hora...
df_filtro = dados.consultar_modelos_cl()
# data_metricas = dados.consultar_metricas() # Retonrna as metricas
# dataset =  consultar_valores()


graficos = Graficos()

st.set_page_config(layout="wide")


# Para filtro
df_filtro['id_combinado'] = df_filtro['commit_id'].astype(
    str) + ' - ' + df_filtro['controle_de_versao'].astype(str)


metricas_gerais = [
    'Acuracia', 'Precision', 'Recall', 'Especificidade', 'F1_score',
    'Taxa_falsa_descoberta(FDR)', 'Valor_preditivo_negativo(NPU)', 'Prevalencia',
    'Taxa_falsa_Omissao(for)', 'Sensibilidade(TPR)', 'Taxa_falso_negativo',
    'Taxa_falso_positivo', 'Teste_razao_verossimilhanca_negativa(LR-)',
    'Teste_razao_verossimilhanca_positiva(LR+)'
]

metricas_reais = [
    'media_real', 'mediana_real', 'moda_real', 'desvio_padrao_real',
    'Q1_real', 'Q2_real', 'Q3_real', 'skewness_real', 'kurtosis_real'
]

metricas_preditas = [
    'media_pred', 'mediana_pred', 'moda_pred', 'desvio_padrao_pred',
    'Q1_pred', 'Q2_pred', 'Q3_pred', 'skewness_pred', 'kurtosis_pred'
]

metricas_diferencas = [
    'media_diff', 'mediana_diff', 'moda_diff', 'desvio_padrao_diff',
    'skewness_diff', 'kurtosis_diff'
]


aba1, aba2, aba3 = st.tabs(['Painel', 'Métricas', 'Gráficos'])


with aba1:
    id_selecionado = st.selectbox('ID, Modelos', df_filtro['id_combinado'])
    query = """
    id_combinado in @id_selecionado
    """
    df_filtrado = df_filtro.query(query)
    st.dataframe(df_filtrado)

    st.page_link("./painel_principal.py",
                 label="Voltar para o Painel Principal")

# Garantindo que o DataFrame filtrado não está vazio antes de consultar métricas
if not df_filtrado.empty:
    endereco = df_filtrado.iloc[0, 2]  # Pegando o valor diretamente
    commit_id = df_filtrado.iloc[0, 1]  # Pegando o valor diretamente

df_metricas = dados.consultar_metricas_cl(
    # Retorna as metricas
    commit_id=str(df_filtrado.iloc[0, 1]), endereco=str(df_filtrado.iloc[0, 2]))

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
            row_mean = f"{df_metricas[x].astype(float).iloc[0]:.4f}"
            nome = x.replace('_', ' ')
            #st.metric(nome, row_mean)  # Passando métricas
            
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
            row_mean = f"{df_metricas[x].astype(float).iloc[0]:.4f}"
            nome = x.replace('_', ' ')
            #st.metric(nome, row_mean)  # Passando métricas
            
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
            row_mean = f"{df_metricas[x].astype(float).iloc[0]:.4f}"
            nome = x.replace('_', ' ')
            #st.metric(nome, row_mean)  # Passando métricas
            
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
            row_mean = f"{df_metricas[x].astype(float).iloc[0]:.4f}"
            nome = x.replace('_', ' ')
            #st.metric(nome, row_mean)  # Passando métricas
            
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

with aba3:
    # st.title('Painel de regressão')
    col1, col2 = st.columns(2)
    with col1:
        id_metrica01 = st.selectbox('Métricas', metricas_gerais)
        st.plotly_chart(graficos.grafico_rosca(
            id_metrica01, df_metricas[id_metrica01].mean(), '#67ace1'))
        st.write("Ola mundo!")
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
        nomes = ['Acuracia', 'Precision',
                 'Recall', 'Especificidade', 'F1_score']

        valores = pd.DataFrame(
            {
                'Metrica': nomes,
                'Valor': df_metricas[['Acuracia', 'Precision', 'Recall',
                                      'Especificidade', 'F1_score']].mean()
            }
        )
        teste = graficos.barra_gradiente(valores)
        st.pyplot(teste)
# ----------------------------------------------------------------
    id_unique = df_filtro['controle_de_versao'].unique()
    id_unique = pd.Series(id_unique)
    id_selecionado = st.selectbox('ID, Modelos', id_unique)

    id_metrica = st.selectbox('ID, Modelos', metricas_gerais)

    df_agrupado_metrica = dados.consultar_metricas_cl(endereco=id_selecionado)

    st.plotly_chart(graficos.grafico_linha_detalhada(
        id_metrica, df_agrupado_metrica.index, df_agrupado_metrica[id_metrica].values))

# ----------------------------------------------------------------

    df_valores = dados.consultar_valores_cl(
        # Retorna as metricas
        id_atual=int(df_filtrado.iloc[0, 0]), commit_id=str(df_filtrado.iloc[0, 1]))

    # Verificação se 'fpr' e 'tpr' estão presentes e não são nulos
    fpr = df_valores[0].get('fpr')
    tpr = df_valores[0].get('tpr')

    if fpr and tpr:  # Verifica se ambos não são None ou vazios
        try:
            # Convertendo a string para uma lista real
            fpr = ast.literal_eval(fpr)
            # Convertendo a string para uma lista real
            tpr = ast.literal_eval(tpr)
            st.plotly_chart(graficos.curva_roc(
                fpr, tpr))  # Exibe o gráfico
        except (ValueError, SyntaxError) as e:
            st.error(f"Erro ao converter valores para lista: {e}")
    else:
        st.error("Valores de fpr ou tpr estão ausentes.")

    precision = df_valores[0].get('precision')
    recall = df_valores[0].get('recall')
    avg_precision = df_valores[0].get('avg_precision')

    if precision and recall:  # Verifica se ambos não são None ou vazios
        try:
            # Convertendo a string para uma lista real
            precision = ast.literal_eval(precision)
            # Convertendo a string para uma lista real
            recall = ast.literal_eval(recall)
            # Convertendo a string para um tipo real
            avg_precision = ast.literal_eval(avg_precision)
            st.plotly_chart(graficos.curva_precision_recall(
                precision, recall, avg_precision))  # Exibe o gráfico
        except (ValueError, SyntaxError) as e:
            st.error(f"Erro ao converter valores para lista: {e}")
    else:
        st.error("Valores de precision ou recall estão ausentes.")
