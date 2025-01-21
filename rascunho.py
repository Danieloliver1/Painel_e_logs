import numpy as np
import pandas as pd
import plotly.graph_objects as go

def plot_limite_decisao(y_probabilidade_final, limite_decisao=0.5):
    """
    Cria um gráfico interativo com limite de decisão usando Plotly.
    
    Args:
        y_probabilidade_final (array-like): Lista ou array de probabilidades finais.
        limite_decisao (float): Valor do limite de decisão. Padrão é 0.5.
    """
    # Preparar os dados
    x = np.arange(len(y_probabilidade_final))
    y = y_probabilidade_final

    # Criar DataFrame para manipulação mais fácil
    df = pd.DataFrame({
        'X': x,
        'Probabilidade': y,
        'Classe': ['Classe 1' if p > limite_decisao else 'Classe 0' for p in y]
    })

    # Criar o gráfico
    fig = go.Figure()

    # Adicionar preenchimento para Classe 1 (acima do limite)
    fig.add_trace(go.Scatter(
        x=x,
        y=np.where(y > limite_decisao, y, limite_decisao),
        mode='lines',
        fill='tonexty',
        line=dict(width=0),
        fillcolor='rgba(0, 255, 0, 0.3)',
        name='Classe 1 (Área Verde)'
    ))

    # Adicionar preenchimento para Classe 0 (abaixo do limite)
    fig.add_trace(go.Scatter(
        x=x,
        y=np.where(y <= limite_decisao, y, limite_decisao),
        mode='lines',
        fill='tonexty',
        line=dict(width=0),
        fillcolor='rgba(255, 0, 0, 0.3)',
        name='Classe 0 (Área Vermelha)'
    ))

    # Adicionar linha do limite de decisão
    fig.add_trace(go.Scatter(
        x=x,
        y=[limite_decisao] * len(x),
        mode='lines',
        line=dict(color='black', dash='dash'),
        name='Limite de Decisão'
    ))

    # Adicionar pontos dos dados observados
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(color='blue', size=8),
        name='Dados Observados'
    ))

    # Personalizar layout
    fig.update_layout(
        title='Limite de Decisão',
        xaxis_title='X',
        yaxis_title='Probabilidade Final',
        legend_title='Legenda',
        template='plotly_white'
    )

    # Exibir gráfico
    fig.show()

# Exemplo de uso
y_probabilidade_final = np.random.rand(50)  # Probabilidades simuladas
plot_limite_decisao(y_probabilidade_final)











# import streamlit as st
# import pandas as pd

# # Exemplo de DataFrame
# dados = {
#     "Coluna 1": [1, 2, 3],
#     "Coluna 2": [4, 5, 6],
#     "Coluna 3": [7, 8, 9],
# }
# df = pd.DataFrame(dados)

# # Estilos personalizados para a tabela
# cabecalho = {
#     'selector': 'th',
#     'props': 'font-family: Helvetica; color: #dddd55; background-color: #34495E; text-align: center;'
# }

# celulas = {
#     'selector': 'td',
#     'props': 'font-family: Helvetica; color: white; background-color: #34495E; text-align: left;'
# }

# # Aplicar estilos ao DataFrame
# styled_df = df.style.format("{:.2f}").set_table_styles([cabecalho, celulas])

# # Renderizar o DataFrame estilizado como HTML
# styled_html = styled_df.render()

# # Exibir no Streamlit
# st.markdown(styled_html, unsafe_allow_html=True)
