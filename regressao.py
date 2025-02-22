
from scipy import stats
import os
import pandas as pd
import numpy as np
from estastistica import Statistic


class Regression(Statistic):
    """
        Inicializa a classe Regression, que herda da classe Statistic.

        Parâmetros:
        - y_real: Valores reais das variáveis dependentes.
        - y_pred: Valores previstos pelo modelo de regressão.
        - X_real: Variáveis independentes (features) usadas no modelo.

        Métodos:
            __init__(self, y_real, y_pred, X_real):
                Inicializa a classe e executa o cálculo de métricas de regressão.
            calculo_metricas_classificacao(self):
                Calcula e armazena métricas de regressão gerais e por classe.
            report(self):
                Imprime um relatório com métricas de regressão gerais e por classe.
            get_metric(self, metric_name):
                Retorna o valor de uma métrica específica.
            classification_result:
                Retorna o dicionário de métricas de regressão.
    """

    def __init__(self, y_real, y_pred):

        # Passa os argumentos para a classe pai
        super().__init__(y_real, y_pred)

        self.y_real = y_real
        self.y_pred = y_pred

        # Inicializa um dicionário para armazenar as métricas
        self.metricas = {}
        self.metricas_regressao = {}
        # self.metricas_classificao = {}

        # Inicializa um dicionário para armazenar resultados estastístico
        self.resultado = {}

        # Chama a função de cálculo das métricas de regressão
        self._calculo_metricas_regressao()

    def _calculo_metricas_regressao(self):
        """
        Calcula métricas estatísticas para avaliação de modelos de regressão.

        MÉTRICAS CALCULADAS:
        --------------------
        - Mean Squared Error (MSE): Erro Quadrático Médio, que mede a média dos 
        quadrados das diferenças entre os valores reais e os previstos.
        - Root Mean Squared Error (RMSE): Raiz quadrada do MSE, proporcionando 
        uma métrica no mesmo domínio dos valores reais.
        - Mean Absolute Error (MAE): Erro Absoluto Médio, representando a média 
        das diferenças absolutas entre os valores reais e previstos.
        - Mean Relative Error (MRE): Erro Relativo Médio, expresso em 
        percentual, considerando a diferença relativa entre os valores reais 
        e previstos.
        - Mean Absolute Percentage Error (MAPE): Erro Percentual Absoluto Médio, 
        que mede o erro em termos percentuais de forma absoluta.
        - Explained Variance Score (EVS): Pontuação de Variância Explicada, que 
        avalia a proporção da variância dos valores reais explicada pelo modelo.
        - R-squared (R²): Coeficiente de Determinação, indicando a qualidade do 
        ajuste do modelo em relação aos dados reais.
        - Adjusted R-squared (R² Ajustado): Versão ajustada do R², considerando 
        o número de amostras e de características no modelo.

        COMO FUNCIONA:
        --------------
        Os valores reais (`y_real`) e previstos (`y_pred`) são utilizados para 
        calcular métricas padrão de avaliação em regressão. O método armazena os 
        resultados no dicionário `self.metricas` para uso posterior.

        EXEMPLO DE SAÍDA:
        -----------------
        {
            'mse': 0.0234,
            'rmse': 0.1529,
            'mae': 0.1347,
            'mre': 8.52,
            'mape': 8.52,
            'evs': 0.976,
            'r_squared': 0.975,
            'adj_r2': 0.973
        }

        NOTAS:
        ------
        - Pequenos valores de MSE, RMSE, MAE, MRE e MAPE indicam melhor desempenho.
        - EVS e R² variam de 0 a 1, sendo 1 o melhor valor possível.
        - R² Ajustado é útil em modelos com múltiplas variáveis independentes.

        Armazena os resultados no dicionário `self.metricas` e combina com 
        os resultados estatísticos do método `summary` no dicionário 
        `self.metricas_regressao`.
        """

        # Mean Squared Error (MSE) - Erro Quadrático Médio
        mse = np.mean((self.y_real - self.y_pred) ** 2)

        # Root Mean Squared Error (RMSE) - Raiz do Erro Quadrático Médio
        rmse = np.sqrt(np.mean((self.y_real - self.y_pred) ** 2))

        # Mean Absolute Error (MAE) - Erro Absoluto Médio
        mae = np.mean(np.abs(self.y_real - self.y_pred))

        # Erro Relativo Médio (MRE), que é uma métrica que expressa o erro médio em termos relativos, ou seja, em percentual, considerando a diferença entre os valores reais e previstos em relação aos valores reais.
        mre = np.mean(np.abs((self.y_real - self.y_pred) /
                      (self.y_real + 1e-10))) * 100

        # Mean Absolute Percentage Error (MAPE) - Erro Percentual Absoluto Médio
        mape = np.mean(np.abs((self.y_real - self.y_pred) /
                       (self.y_real + 1e-10))) * 100

        # Explained Variance Score - Pontuação de Variância Explicada
        mean_y_real = np.mean(self.y_real)
        total_variance = np.sum((self.y_real - mean_y_real) ** 2)
        error_variance = np.sum((self.y_real - self.y_pred) ** 2)
        evs = 1 - (error_variance / total_variance)

        # R-squared (R²) - Coeficiente de Determinação
        sst = np.sum((self.y_real - mean_y_real) ** 2)
        sse = np.sum((self.y_real - self.y_pred) ** 2)
        r_squared = 1 - (sse / sst)

        # Adjusted R-squared - R² Ajustado
        n = len(self.y_real)  # Número de amostras

        # Armazenar as métricas no dicionário
        self.metricas = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'mre': mre,
            'mape': mape,
            'evs': evs,
            'r_squared': r_squared,
        }

        resultado = self.summary()
        self.metricas_regressao = {**self.metricas, **resultado}

    @property
    def regression_result(self):
        """
        Método getter para acessar as métricas de regressão
        """
        return self.metricas_regressao  # Retorna o dicionário de métricas de regressao

    def get_metric(self, metric_name):
        """
        Método para acessar uma métrica específica.
        """
        return self.metricas_regressao.get(metric_name, "Métrica não encontrada")

    def report(self):
        """
        Método para gerar um relatório das métricas de regressão, retorna um Dataframe.
        """
        dados = self.metricas_regressao
        df = pd.DataFrame(list(dados.items()), columns=['Nome', 'Valor'])
        return df
