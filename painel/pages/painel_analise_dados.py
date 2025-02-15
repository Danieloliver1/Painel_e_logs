import streamlit as st
import pandas as pd
import numpy as np
import wfdb
import os
import glob
import time
import neurokit2 as nk
import plotly.express as px
import matplotlib.pyplot as plt

# Título do aplicativo
st.title("📊 Dados de Eletrocardiograma (ECG)")

# Definir caminho para os arquivos
path = r'D:\Projeto_Tese_mestrado\02_Dataset\dados_ECG\High-resolution_ECG\P0*'

# Usando glob para obter todos os arquivos correspondentes
arquivos = glob.glob(path)
arquivos = [os.path.splitext(arquivo)[0] for arquivo in arquivos]  # Removendo extensões

# Criar um DataFrame com os arquivos
df = pd.DataFrame(arquivos, columns=['caminho'])
df = df[df.duplicated()]
df['ultimo_nome'] = df['caminho'].apply(lambda x: os.path.basename(x))

# Selecionar ID do paciente
id_selecionado = st.selectbox('📌 **Selecione um Paciente:**', df['ultimo_nome'])

# Filtrar os dados
df_filtrado = df[df['ultimo_nome'] == id_selecionado]

# Carregar o arquivo selecionado
record = wfdb.rdrecord(df_filtrado.iloc[0, 0])

# Criando abas
aba1, aba2, aba3, aba4 = st.tabs(['📋 Informação', '📊 Dados X', '📊 Dados Y', '📊 Dados Z'])

# Aba de Informações
with aba1:
    col1, col2 = st.columns(2)
    with col1:
        st.write("📌 **Nome do Registro:** ", record.record_name)
        st.write("📌 **Nº de Sinais:** ", record.n_sig)
        st.write("📌 **Frequência de Amostragem:** ", record.fs)
        st.write("📌 **Comprimento do Sinal:** ", record.sig_len)
        st.write("📌 **Arquivo(s):** ", record.file_name)
        st.write("📌 **Unidade de Medida:** ", record.units)
        st.write("📌 **Resolução do ADC:** ", record.adc_res)
        st.write("📌 **Ponto Zero do ADC:** ", record.adc_zero)

# Botão para carregar os dados X
with aba2:
    if 'sinal_x' not in st.session_state:  # Verifica se os dados não estão armazenados
        if st.button("🔄 Carregar Dados X"):
            with st.spinner("Carregando os dados X... 🔍"):
                sinal_x = record.p_signal[:, 0]
                resultado_x, _ = nk.ecg_process(sinal_x, sampling_rate= record.fs , method='neurokit')
                st.plotly_chart(px.line(resultado_x[1000:2000], x=resultado_x.index[0:1000], y = 'ECG_Clean'))

                # Armazenar os dados no session_state para evitar recálculo
                st.session_state.sinal_x = sinal_x
                st.session_state.resultado_x = resultado_x
                st.session_state.ecg = sinal_x[0:98000].copy()

                signals = pd.DataFrame({
                    "ECG_Raw" : st.session_state.ecg,
                    "ECG_NeuroKit" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="neurokit"),
                    "ECG_BioSPPy" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="biosppy"),
                    "ECG_PanTompkins" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="pantompkins1985"),
                    "ECG_Hamilton" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="hamilton2002"),
                    "ECG_Elgendi" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="elgendi2010"),
                    "ECG_EngZeeMod" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="engzeemod2012"),
                    "ECG_VG" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="vg"),
                    "ECG_TC" : nk.ecg_clean(st.session_state.ecg, sampling_rate=1000, method="templateconvolution")
                })
                
                fig, ax = plt.subplots()
                signals.plot(subplots=True, ax=ax)  # Criar gráfico no Matplotlib
                st.pyplot(fig)  # Exibir no Streamlit

                #st.line_chart(signals.plot(subplots=True))
        else:
            st.warning("Clique no botão acima para carregar os dados X.")
    else:
        # Caso os dados já estejam no session_state, exibe o gráfico
        st.plotly_chart(px.line(st.session_state.resultado_x[0:1000], x=st.session_state.resultado_x.index[0:1000], y='ECG_Clean'))
        fig, ax = plt.subplots()
        signals.plot(subplots=True, ax=ax)  # Criar gráfico no Matplotlib
        st.pyplot(fig)  # Exibir no Streamlit

# Botão para carregar os dados Y (seguindo a mesma lógica do X)
with aba3:
    if 'sinal_y' not in st.session_state:
        if st.button("🔄 Carregar Dados Y"):
            with st.spinner("Carregando os dados Y... 🔍"):
                if record.n_sig > 1:
                    sinal_y = record.p_signal[:, 1]  # Extrai o sinal Y
                    
                    # Processa o sinal como no X
                    resultado_y, _ = nk.ecg_process(sinal_y, sampling_rate=record.fs, method='neurokit')
                    
                    # Exibe gráfico interativo
                    st.plotly_chart(px.line(resultado_y[1000:2000], x=resultado_y.index[0:1000], y='ECG_Clean'))
                    
                    # Armazena no session_state
                    st.session_state.sinal_y = sinal_y
                    st.session_state.resultado_y = resultado_y
                else:
                    st.error("Apenas um sinal disponível!")
        else:
            st.warning("Clique no botão acima para carregar os dados Y.")
    else:
        # Exibe gráfico se os dados já estiverem carregados
        st.plotly_chart(px.line(st.session_state.resultado_y[1000:2000], x=st.session_state.resultado_y.index[0:1000], y='ECG_Clean'))

# Botão para carregar os dados Z 
with aba4:
    if 'sinal_z' not in st.session_state:
        if st.button("🔄 Carregar Dados Z"):
            with st.spinner("Carregando os dados Z... 🔍"):
                if record.n_sig > 2:
                    sinal_z = record.p_signal[:, 2]  # Extrai o sinal Z
                    
                    # Processa o sinal como no X e Y
                    resultado_z, _ = nk.ecg_process(sinal_z, sampling_rate=record.fs, method='neurokit')
                    
                    # Exibe gráfico interativo
                    st.plotly_chart(px.line(resultado_z[1000:2000], x=resultado_z.index[0:1000], y='ECG_Clean'))
                    
                    # Armazena no session_state
                    st.session_state.sinal_z = sinal_z
                    st.session_state.resultado_z = resultado_z
                else:
                    st.error("Apenas dois sinais disponíveis!")
        else:
            st.warning("Clique no botão acima para carregar os dados Z.")              
    else:
        # Exibe gráfico se os dados já estiverem carregados
        st.plotly_chart(px.line(st.session_state.resultado_z[1000:2000], x=st.session_state.resultado_z.index[0:1000], y='ECG_Clean'))
