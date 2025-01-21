import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.metrics import auc
import numpy as np


class Graficos:
    def __init__(self):
        pass

    def grafico_rosca(self, nome_metrica, valor_da_metrica, cor, exibir_nome_metrica=True):
        # Valor da métrica em porcentagem
        # Garante que o valor seja positivo
        valor = abs(valor_da_metrica) * 100

        # Calcule o tamanho da rosca
        rosca_size = valor  # A rosca vai representar o valor diretamente

        # Crie um DataFrame com os dados
        data = {'Categoria': [f'{nome_metrica}', ''],
                # O restante da rosca ficará vazio
                'Valor': [rosca_size, 100 - rosca_size]}

        df = pd.DataFrame(data)

        # Crie o gráfico de rosca manualmente usando plotly.graph_objects
        fig = go.Figure(go.Pie(
            labels=df['Categoria'],
            values=df['Valor'],
            hole=0.7,
            # Definindo manualmente as cores
            # Cor com transparência
            # rgba(169, 169, 169, 0.3)
            marker=dict(colors=[f'{cor}', 'rgba(0,0,0,0)']),
            textinfo='none',  # Remove os textos automáticos
            showlegend=False  # Remove a legenda
        ))

        # Atualizar layout para remoção de fundo e adicionar o valor no centro
        fig.update_layout(
            width=410,
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        # Adicionar o nome da métrica, se 'exibir_nome_metrica' for True
        if exibir_nome_metrica:
            fig.add_annotation(
                x=0.5, y=1.3, text=f'<b>{nome_metrica}</b>',
                font=dict(color=cor, size=29, family='Arial, sans-serif'), showarrow=False)

        # Adicionar o valor percentual no centro
        fig.add_annotation(
            x=0.5, y=0.5, text=f'<b>{valor:.1f}%</b>',
            font=dict(color=cor, size=32, family='Arial, sans-serif'), showarrow=False)

        return fig

    def roscas_empilhadas_v2(self, nomes, valores, cores):
        """
        Gera um gráfico de roscas empilhadas com cores consistentes e valores individuais.

        Parâmetros:
        - nomes (list): Lista de nomes das métricas.
        - valores (list): Lista de valores das métricas (em porcentagem, de 0 a 100).
        - cores (list): Lista de cores para cada rosca.

        Retorna:
        - Exibe o gráfico de roscas empilhadas.
        """
        # Validação de entrada
        if len(nomes) != len(valores) or len(nomes) != len(cores):
            raise ValueError(
                "Os parâmetros 'nomes', 'valores' e 'cores' devem ter o mesmo tamanho.")

        # Criando a figura
        fig = go.Figure()

        # Adicionando cada rosca individualmente
        for i, (nome, valor, cor) in enumerate(zip(nomes, valores, cores)):
            # Garante que o valor seja positivo e calculado em porcentagem
            rosca_size = abs(valor) * 100

            # Criação dos dados para a rosca
            data = {'Categoria': [f'{nome}', 'Restante'],
                    'Valor': [rosca_size, 100 - rosca_size]}
            df = pd.DataFrame(data)

            # Adicionando a rosca
            fig.add_trace(go.Pie(
                labels=df['Categoria'],
                values=df['Valor'],
                hole=0.4 + (i * 0.12),  # Buraco ajustado para cada camada
                # Cor principal e cinza para restante
                marker=dict(colors=[cor, 'rgba(0,0,0,0)']),
                textinfo='none',  # Remove textos automáticos
                showlegend=False  # Remove a legenda
            ))

            # Adicionando anotações para exibir os valores
            fig.add_annotation(
                # Ajusta posição vertical para cada camada
                x=0.99, y=0.9 - (i * 0.15),
                text=f"{nome}: {round(valor, 2)}%",  # Texto com o nome e valor
                font=dict(size=12, color=cor), showarrow=False
            )

        # Ajustando o layout
        fig.update_layout(
            title_text="Gráfico de Roscas Empilhadas com Cores Consistentes",
            showlegend=False,
            plot_bgcolor="white"
        )

        # Exibir o gráfico
        return fig

    def grafico_linha(self, dados, titulo):

        lista = list(range(1, dados.shape[0]+1))

        fig = px.line(dados,
                      x=lista,  # Índice do DataFrame como eixo x
                      y=dados.columns,  # Colunas do DataFrame como eixo y
                      color_discrete_sequence=px.colors.qualitative.Dark24,  # Sequência de cores
                      # Rótulos dos eixos
                      labels={'x': 'Índice', 'y': 'Valor'},
                      title=f'{titulo}')

        # Atualização do layout do gráfico
        fig.update_layout(xaxis_title='Coluna de entrada X',  # Título do eixo x
                          yaxis_title='Valor',  # Título do eixo y
                          legend_title='Comparativo',  # Título da legenda
                          # Define as margens
                          margin=dict(l=50, r=20, t=50, b=20),
                          # Exibir grade no eixo y
                          yaxis=dict(showgrid=True, zeroline=False),
                          width=1300,  # Largura do gráfico
                          height=400)  # Altura do gráfico
        return fig

    def grafico_linha_detalhada(self, titulo, categorias, valores, exibir=True):
        # Converter os valores para uma Série do pandas
        valores = pd.Series(valores)

        # Calcular estatísticas descritivas
        desvio_padrao = round(valores.std(), 2)
        media = round(valores.mean(), 2)
        mediana = round(valores.median(), 2)
        erro = round(valores.sem(), 2)  # Erro padrão médio

        # Definir o nível de confiança (95% neste caso)
        confidence_level = 0.95
        graus_de_liberdade = len(valores) - 1  # Graus de liberdade

        # Calcular o valor crítico para o nível de confiança
        t_critical = stats.t.ppf(
            q=(1 + confidence_level) / 2, df=graus_de_liberdade)

        # Calcular a margem de erro e o intervalo de confiança
        margin_of_error = t_critical * erro
        # confidence_interval = (media - margin_of_error), (media + margin_of_error)

        # Converter para float antes de arredondar
        margin_of_error = round(float(margin_of_error), 2)
        confidence_interval = (
            round(float(media - margin_of_error), 2),
            round(float(media + margin_of_error), 2)
        )

        # Criando o gráfico de linhas com Plotly Express
        fig = px.line(x=categorias, y=valores,
                      title=titulo, text=valores.round(2))

        # Adicionar marcadores e texto no gráfico
        fig.update_traces(mode='lines+markers+text', textposition='top center')

        # Personalizar o layout do gráfico
        fig.update_layout(
            xaxis_title='Categorias',  # Título do eixo X
            yaxis_title='Valores',     # Título do eixo Y
            hovermode='x',             # Configuração de hover
            template='plotly_white',   # Tema do gráfico
            width=1200,                # Largura do gráfico
            height=400,                # Altura do gráfico
            margin=dict(l=20, r=260, t=35, b=20),  # Margens do gráfico
            title_font=dict(size=20, color='white'),  # Cor e tamanho do título
            xaxis=dict(
                # Título do eixo X em branco
                title=dict(font=dict(size=14, color='white')),
                # Texto do eixo X em branco
                tickfont=dict(color='white')
            ),
            yaxis=dict(
                # Título do eixo Y em branco
                title=dict(font=dict(size=14, color='white')),
                # Texto do eixo Y em branco
                tickfont=dict(color='white')
            ),
            plot_bgcolor='rgba(0,0,0,0)',  # Fundo do gráfico transparente
            paper_bgcolor='rgba(0,0,0,0)'  # Fundo da área externa transparente
        )

        # Adicionar anotações de estatísticas ao lado do gráfico, se exibir=True
        if exibir:
            fig.add_annotation(
                text=f'<b>Resultados</b><br> Desvio Padrão: {
                    desvio_padrao}<br> Média: {media}<br> Mediana: {mediana}'
                f'<br> Erro padrão médio: {erro}<br> Margin de erro: {
                    margin_of_error}'
                f'<br> Intervalo de confiança: {confidence_interval}',
                xref='paper',  # Posicionamento em relação ao papel
                yref='paper',  # Posicionamento em relação ao papel
                x=1.30,        # Posição horizontal do texto
                y=0.85,        # Posição vertical do texto
                showarrow=False,  # Não exibir seta
                font=dict(size=14, color='white'),  # Texto em branco
                bgcolor='rgba(0,0,0,0)',            # Fundo transparente
                borderwidth=1,                      # Largura da borda
                align='left'                        # Alinhamento do texto à esquerda
            )

        return fig

    # curva ROC
    def curva_roc(self, fpr, tpr):

        roc_auc = auc(fpr, tpr)  # Área sob a curva ROC
        fig = px.area(
            x=fpr,  # Índice do DataFrame como eixo x
            y=tpr,  # Colunas do DataFrame como eixo y
            color_discrete_sequence=px.colors.qualitative.Dark24,  # Sequência de cores
            labels={'x': 'Índice', 'y': 'Valor'},  # Rótulos dos eixos
            title='<b>Curva ROC</b>',)

        # Adicionar a linha diagonal de referência
        fig.add_shape(
            type='line',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            line=dict(color='black', dash='dash'),)

        # Adicionar a linha da curva ROC
        fig.add_scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            # Incluindo a AUC na legenda
            name=f'ROC curve (área = {roc_auc:.2f})',
            line=dict(color='darkorange', width=2)
        )

        # Atualizar o layout do gráfico
        fig.update_layout(
            # Título do eixo x
            xaxis_title='Taxa de Falso Positivo (FPR)<br>(ou 1 — Especificidade)',
            # Título do eixo y
            yaxis_title='Taxa de Verdadeiros Positivos<br>(TPR) (ou Sensibilidade/Recall)',
            legend_title='Acurácia',  # Título da legenda
            margin=dict(l=50, r=200, t=50, b=20),  # Define as margens
            # Exibir grade no eixo y
            yaxis=dict(showgrid=True, zeroline=False),
            width=1300,  # Largura do gráfico
            height=500  # Altura do gráfico
        )

        # Mostrar o gráfico
        return fig

    def curva_precision_recall(self, precisao, revocacao, avg_precision):

        fig = px.area(
            x=revocacao,  # Valores da taxa de revocação
            y=precisao,   # Valores da precisão
            color_discrete_sequence=px.colors.qualitative.Dark24,  # Sequência de cores
            labels={'x': 'Revocação', 'y': 'Precisão'},  # Rótulos dos eixos
            title='<b>Curva Precision-Recall</b>'  # Título do gráfico
        )

        # Adicionar a linha da Curva Precision-Recall
        fig.add_scatter(
            x=revocacao,
            y=precisao,
            mode='lines',
            # Incluindo a AUC na legenda
            name=f'Precision-Recall curve (área = {avg_precision:.2f})',
            line=dict(color='darkorange', width=2)
        )

        # Atualizar o layout do gráfico
        fig.update_layout(
            xaxis_title='Revocação (Recall)',  # Título do eixo x
            yaxis_title='Precisão',  # Título do eixo y
            legend_title=f'Média da precisão',  # Título da legenda
            margin=dict(l=50, r=50, t=50, b=50),  # Definindo as margens
            # Exibir grade no eixo y
            yaxis=dict(showgrid=True, zeroline=False),
            width=1300,  # Largura do gráfico
            height=500  # Altura do gráfico
        )

        # Mostrar o gráfico
        return fig

    def barra_gradiente(self, dados):
        """
        Cria um gráfico de barras com gradiente de cores e personalizações.

        Parâmetros:
        - dados (pd.DataFrame): DataFrame com colunas 'Metrica' e 'Valor'.

        Retorna:
        - matplotlib.figure.Figure: A figura gerada pelo Seaborn.
        """
        # Configuração inicial
        fig, ax = plt.subplots(figsize=(12, 5))

        # Criação do gráfico de barras
        barras = sns.barplot(
            x='Metrica',
            y='Valor',
            data=dados,
            palette='GnBu_d',
            ax=ax
        )

        # Adicionar os valores e nomes acima das barras
        for i, (indice, valor) in enumerate(zip(dados['Metrica'], dados['Valor'])):
            # Texto combinado com nome da métrica e valor
            texto = f"{indice}: {valor:.2%}"  # Exemplo: "Acurácia: 89%"
            ax.text(
                i,  # Posição X
                valor + 0.02,  # Posição Y (levemente acima da barra)
                texto,  # Texto formatado
                ha='center',  # Alinhamento horizontal
                va='bottom',  # Alinhamento vertical
                fontsize=16,  # Tamanho da fonte
                color='#ff0119'  # Cor do texto
            )

        # Removendo as bordas, linhas verticais e horizontais
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.grid(False)  # Remove a grade
        ax.set_ylabel('')  # Remove o texto do eixo Y
        ax.set_xlabel('')  # Remove o texto do eixo X
        ax.set_xticks([])  # Remove os ticks do eixo X
        ax.set_yticks([])  # Remove os ticks do eixo Y
        fig.patch.set_alpha(0)  # Fundo da figura
        ax.patch.set_alpha(0)   # Fundo do gráfico (eixo)

        # Ajustando layout
        plt.tight_layout()

        return fig

    def barra_gradiente2(self, dados):
        """
        Cria um gráfico de barras com gradiente de cores e personalizações.

        Parâmetros:
        - dados (pd.DataFrame): DataFrame com colunas 'Metrica' e 'Valor'.

        Retorna:
        - matplotlib.figure.Figure: A figura gerada pelo Seaborn.
        """
        # Configuração inicial
        fig, ax = plt.subplots(figsize=(12, 5))

        # Criação do gráfico de barras
        barras = sns.barplot(
            x='Metrica',
            y='Valor',
            data=dados,
            palette='GnBu_d',
            ax=ax
        )

        # Adicionar os valores e nomes acima das barras
        for i, (indice, valor) in enumerate(zip(dados['Metrica'], dados['Valor'])):
            # Texto combinado com nome da métrica e valor
            texto = f"{indice}: {valor:.2f}"  # Exemplo: "Acurácia: 89%"
            ax.text(
                i,  # Posição X
                valor + 0.02,  # Posição Y (levemente acima da barra)
                texto,  # Texto formatado
                ha='center',  # Alinhamento horizontal
                va='bottom',  # Alinhamento vertical
                fontsize=16,  # Tamanho da fonte
                color='#ff0119'  # Cor do texto
            )

        # Removendo as bordas, linhas verticais e horizontais
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.grid(False)  # Remove a grade
        ax.set_ylabel('')  # Remove o texto do eixo Y
        ax.set_xlabel('')  # Remove o texto do eixo X
        ax.set_xticks([])  # Remove os ticks do eixo X
        ax.set_yticks([])  # Remove os ticks do eixo Y
        fig.patch.set_alpha(0)  # Fundo da figura
        ax.patch.set_alpha(0)   # Fundo do gráfico (eixo)

        # Ajustando layout
        plt.tight_layout()

        return fig

    def teia_de_aranha(self, categorias, valores1):

        # Criando o gráfico
        fig = go.Figure()

        # Primeiro conjunto de valores
        fig.add_trace(go.Scatterpolar(
            r=valores1,
            theta=categorias,
            fill='toself',
            name='Entidade 1',
            line=dict(color='rgba(30, 144, 255, 0.7)',
                      width=2),  # Azul translúcido
            # Azul mais claro para o preenchimento
            fillcolor='rgba(30, 144, 255, 0.3)'
        ))

        # # Segundo conjunto de valores
        # fig.add_trace(go.Scatterpolar(
        #     r=valores2,
        #     theta=categorias,
        #     fill='toself',
        #     name='Entidade 2',
        #     line=dict(color='rgba(255, 165, 0, 0.7)', width=2),  # Laranja translúcido
        #     fillcolor='rgba(255, 165, 0, 0.3)'  # Laranja mais claro para o preenchimento
        # ))

        # Personalizando o layout
        fig.update_layout(
            title=dict(
                text="Gráfico de Teia de Aranha - Comparação de Atributos",
                font=dict(size=20, color='darkblue'),
                x=0.5  # Centralizar título
            ),
            polar=dict(
                bgcolor='whitesmoke',
                angularaxis=dict(
                    tickfont=dict(size=14, color='black'),
                    linecolor='lightgrey'
                ),
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=12, color='black'),
                    gridcolor='lightgrey',
                    linecolor='lightgrey'
                )
            ),
            legend=dict(
                font=dict(size=14),
                bordercolor='gray',
                borderwidth=1,
                orientation="h",
                x=0.5,
                xanchor="center",
                y=-0.2
            ),
            showlegend=True,
        )

        # Exibindo o gráfico
        return fig

    def distribuicao_normal(self, titulo, errors):
        # Calculando os parâmetros da distribuição normal
        mu, sigma = np.mean(errors), np.std(errors)

        # Criando a faixa de valores para o eixo x
        xmin, xmax = min(errors), max(errors)
        x = np.linspace(xmin, xmax, 100)

        # Calculando a densidade normal
        p = (1 / (sigma * np.sqrt(2 * np.pi))) * \
            np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        # Criando o gráfico com Plotly
        fig = go.Figure()

        # Adicionando o histograma dos erros
        fig.add_trace(go.Histogram(
            x=errors,
            nbinsx=30,
            histnorm='probability density',
            name='Histograma dos Erros',
            marker=dict(color='#00bfff', opacity=0.6)
        ))

        # Adicionando a curva de densidade normal
        fig.add_trace(go.Scatter(
            x=x,
            y=p,
            mode='lines',
            name='Distribuição Normal Teórica',
            line=dict(color='#e00500', width=2)
        ))

        # Adicionando título e rótulos
        fig.update_layout(
            title=f'Distribuição dos ({titulo}) da {titulo}',
            xaxis_title=f'{titulo}',
            yaxis_title='Densidade de Probabilidade',
            template='plotly_white'
        )

        # Exibindo o gráfico
        return fig

    def calcular_porcentagens(self, values):
        # Calculando o IQR (Interquartile Range)
        Q1 = np.percentile(values, 25)
        Q3 = np.percentile(values, 75)
        IQR = Q3 - Q1

        # Calculando os limites para os outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Encontrando os outliers
        outliers = [x for x in values if x < lower_bound or x > upper_bound]
        in_range = [x for x in values if x >= lower_bound and x <= upper_bound]

        # Calculando as porcentagens
        outliers_percentage = (len(outliers) / len(values)) * 100
        in_range_percentage = (len(in_range) / len(values)) * 100

        return outliers_percentage, outliers

    def outline(self, y_test, y_pred):
        # Calculando as porcentagens e outliers para y_test e y_pred
        outliers_percentage_test, outliers_test = self.calcular_porcentagens(
            y_test)
        outliers_percentage_pred, outliers_pred = self.calcular_porcentagens(
            y_pred)

        # Criando o box plot com Plotly
        fig = go.Figure()

        # Adicionando box plot para y_test
        fig.add_trace(go.Box(
            y=y_test,
            name='y_test',
            marker=dict(color='royalblue'),
            boxmean=True,  # Mostrar a média
            jitter=0.3,  # Adicionando dispersão para os pontos
            whiskerwidth=0.7,  # Largura dos bigodes ajustada
        ))

        # Adicionando box plot para y_pred
        fig.add_trace(go.Box(
            y=y_pred,
            name='y_pred',
            marker=dict(color='orange'),
            boxmean=True,  # Mostrar a média
            jitter=0.3,
            whiskerwidth=0.7,  # Largura dos bigodes ajustada
        ))

        # Adicionando os outliers como pontos com valor ao lado para y_test
        for outlier in outliers_test:
            fig.add_trace(go.Scatter(
                x=['y_test'],
                y=[outlier],
                mode='markers+text',
                text=[f'{outlier:.2f}'],
                textposition='top right',
                marker=dict(color='red', size=12, symbol='circle'),
            ))

        # Adicionando os outliers como pontos com valor ao lado para y_pred
        for outlier in outliers_pred:
            fig.add_trace(go.Scatter(
                x=['y_pred'],
                y=[outlier],
                mode='markers+text',
                text=[f'{outlier:.2f}'],
                textposition='top right',
                marker=dict(color='red', size=12, symbol='circle'),
            ))

        # Adicionando título e rótulos
        fig.update_layout(
            title=f'Distribuição dos Valores: <br>y_test IQR: {100 - outliers_percentage_test:.2f}% | Outliers: {
                outliers_percentage_test:.2f}% <br>y_pred IQR: {100 - outliers_percentage_pred:.2f}% | Outliers: {outliers_percentage_pred:.2f}%',
            yaxis_title='Valor',
            xaxis_title='Tipos de Dados',
            template='plotly_white',
            showlegend=False,
        )

        # Exibindo o gráfico
        return fig

    def outline_residuo(self, y_test, y_pred):
        # Calculando os resíduos (diferença entre y_test e y_pred)
        residuos = np.array(y_test) - np.array(y_pred)

        # Calculando as porcentagens e outliers para os resíduos
        outliers_percentage, outliers = self.calcular_porcentagens(residuos)

        # Criando o box plot com Plotly
        fig = go.Figure()

        # Adicionando box plot para os resíduos
        fig.add_trace(go.Box(
            y=residuos,
            name='Resíduos (y_test - y_pred)',
            marker=dict(color='forestgreen'),
            boxmean=True,
            jitter=0.3,
            whiskerwidth=0.7,  # Largura dos bigodes ajustada
            width=False  # Ajustando a largura do box plot
        ))

        # Adicionando os outliers como pontos com valor ao lado
        for outlier in outliers:
            fig.add_trace(go.Scatter(
                x=['Resíduos (y_test - y_pred)'],
                y=[outlier],
                mode='markers+text',
                text=[f'{outlier:.2f}'],
                textposition='top right',
                marker=dict(color='#248889', size=12, symbol='circle'),
            ))

        # Adicionando título e rótulos
        fig.update_layout(
            title=f'Distribuição dos Resíduos: <br>Resíduos IQR: {
                100 - outliers_percentage:.2f}% | Outliers: {outliers_percentage:.2f}%',
            yaxis_title='Valor',
            xaxis_title='Tipos de Dados',
            template='plotly_white',
            showlegend=False,
        )

        # Exibindo o gráfico
        return fig
