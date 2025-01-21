
import streamlit as st
import pandas as pd


# Carregando dados
link = r'E:\Repositorio_Git\12_logs\dados\bando_de_dados_classificacao_classe.csv'
df = pd.read_csv(link)


aba1, aba2, aba3 = st.tabs(['Painel', 'Métricas', 'Gráficos'])


with aba1:
    st.write("Ola mundo!")

with aba2:
    #st.title('Painel de classificação por classes')
    col1, col2 = st.columns(2)
    with col1:
        st.write("Ola mundo!")
    with col2:
        st.write("Ola mundo!")

with aba3:
    #st.title('Painel de regressão')
    col1, col2 = st.columns(2)
    with col1:
        st.write("Ola mundo!")
    with col2:
        st.write("Ola mundo!")