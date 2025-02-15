import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page


st.title('Menu principal')


# Criação de 3 colunas
col1, col2, col3 = st.columns(3)

# import time

# # CSS da animação de carregamento
# loader_css = """
#     <style>
#         .loader {
#             width: fit-content;
#             font-weight: bold;
#             font-family: sans-serif;
#             font-size: 30px;
#             padding-bottom: 8px;
#             background: linear-gradient(currentColor 0 0) 0 100%/0% 3px no-repeat;
#             animation: l2 2s linear infinite;
#         }
#         .loader:before {
#             content:"Loading..."
#         }
#         @keyframes l2 {to{background-size: 100% 3px}}

#         /* Ocultar a animação depois que a página carrega */
#         .hide-loader {
#             display: none;
#         }
#     </style>
# """

# # HTML para exibir a animação
# loader_html = '<div class="loader"></div>'

# # Exibe o CSS e HTML para a animação
# st.markdown(loader_css, unsafe_allow_html=True)
# st.markdown(loader_html, unsafe_allow_html=True)

# # Função que simula algum processo demorado
# def processo_demorado():
#     time.sleep(1)  # Simula o tempo de processamento

# Exibe o conteúdo após o carregamento
# with st.spinner('Carregando...'):
#     processo_demorado()


# Esconde a animação após o carregamento e exibe o conteúdo
# st.markdown('<style>.loader { display: none; }</style>', unsafe_allow_html=True)


# Adicionando links em cada coluna
with col1:
    st.page_link("pages/painel_classificacao.py", label="Classificação")
    # st.page_link("pages/painel_classificacao_modelos.py",label="Classificação de Modelos")
    st.page_link("pages/painel_regressao.py", label="Regressão")
    st.page_link("pages/painel_series_temporais.py", label="Séries Temporais")
    st.page_link("pages/painel_analise_dados.py", label="Análise de Dados")
    # st.page_link("pages/painel_regressao_modelos.py",label="Regressão de Modelos")

with col2:
    st.image("./imagens/download.png")

    # if st.button("Painel Classificação"):
    #     switch_page("painel_classificacao")

    # if st.button("Painel Regressão"):
    #     switch_page("painel_regressao")

# with col3:


# st.dataframe(dados)

# import streamlit as st
# import pandas as pd
# import numpy as np
# import time

# df = pd.DataFrame(np.random.randn(15, 3), columns=(["A", "B", "C"]))
# my_data_element = st.line_chart(df)

# for tick in range(10):
#     time.sleep(.5)
#     add_df = pd.DataFrame(np.random.randn(1, 3), columns=(["A", "B", "C"]))
#     my_data_element.add_rows(add_df)

# st.button("Regenerate")




# import streamlit as st

# st.title("Exibindo Texto no Streamlit")  # Título maior
# st.header("Este é um cabeçalho")  # Cabeçalho grande
# st.subheader("Este é um subcabeçalho")  # Cabeçalho menor
# st.text("Este é um texto simples.")  # Texto sem formatação
# st.write("Texto com `st.write()`, que aceita Markdown, variáveis e muito mais!")  
# st.markdown("**Texto em negrito**, _itálico_, e até [um link](https://www.streamlit.io)!")
