
import pandas as pd
import numpy as np
from scipy import stats


class Statistic:

    def __init__(self, y_real, y_pred):
        self.y_real = y_real
        self.y_pred = y_pred
        #self.X_real = X_real

    def summary(self):
        """
        Gera um resumo estatístico abrangente para os valores reais (`y_real`), valores previstos (`y_pred`) 
        e a diferença entre eles (`y_real - y_pred`). O resumo inclui estatísticas descritivas como média, 
        mediana, moda, desvio padrão, quartis (Q1, Q2, Q3), skewness (assimetria) e kurtosis.

        Returns:
            dict: Um dicionário contendo os seguintes valores estatísticos para os dados reais, previstos 
                e as diferenças:
                
                - `media_real` (float): Média dos valores reais.
                - `mediana_real` (float): Mediana dos valores reais.
                - `moda_real` (array): Moda dos valores reais (valor mais frequente).
                - `desvio_padrao_real` (float): Desvio padrão dos valores reais.
                - `Q1_real` (float): Primeiro quartil dos valores reais (25%).
                - `Q2_real` (float): Segundo quartil (mediana, 50%) dos valores reais.
                - `Q3_real` (float): Terceiro quartil dos valores reais (75%).
                - `skewness_real` (float): Assimetria dos valores reais.
                - `kurtosis_real` (float): Curtose dos valores reais.
                
                - `media_pred` (float): Média dos valores previstos.
                - `mediana_pred` (float): Mediana dos valores previstos.
                - `moda_pred` (array): Moda dos valores previstos.
                - `desvio_padrao_pred` (float): Desvio padrão dos valores previstos.
                - `Q1_pred` (float): Primeiro quartil dos valores previstos (25%).
                - `Q2_pred` (float): Segundo quartil (mediana, 50%) dos valores previstos.
                - `Q3_pred` (float): Terceiro quartil dos valores previstos (75%).
                - `skewness_pred` (float): Assimetria dos valores previstos.
                - `kurtosis_pred` (float): Curtose dos valores previstos.
                
                - `media_diff` (float): Média das diferenças (`y_real - y_pred`).
                - `mediana_diff` (float): Mediana das diferenças (`y_real - y_pred`).
                - `moda_diff` (array): Moda das diferenças (`y_real - y_pred`).
                - `desvio_padrao_diff` (float): Desvio padrão das diferenças (`y_real - y_pred`).
                - `Q1_diff` (float): Primeiro quartil das diferenças (25%).
                - `Q2_diff` (float): Segundo quartil (mediana, 50%) das diferenças.
                - `Q3_diff` (float): Terceiro quartil das diferenças (75%).
                - `skewness_diff` (float): Assimetria das diferenças (`y_real - y_pred`).
                - `kurtosis_diff` (float): Curtose das diferenças (`y_real - y_pred`).

        Observações:
            - A função utiliza bibliotecas do NumPy e SciPy para cálculos estatísticos.
            - A moda retorna um array com o(s) valor(es) mais frequente(s). Caso haja múltiplos valores 
            com a mesma frequência, todos serão retornados.
            - As diferenças (`diff`) são calculadas como `y_real - y_pred`.

        Exemplo de Uso:
            >>> y_real = np.array([10, 20, 30, 40, 50])
            >>> y_pred = np.array([12, 18, 33, 37, 52])
            >>> obj = ClasseExemplo(y_real, y_pred)
            >>> resumo = obj.summary()
            >>> print(resumo['media_real'])  # Exibe a média dos valores reais.
            30.0
            >>> print(resumo['media_diff'])  # Exibe a média das diferenças.
            -0.4
        """


        # valores
        # Valores real
        media_real = np.mean(self.y_real)  # 1. Média
        mediana_real = np.median(self.y_real)  # 2. Mediana
        # O valor mais frequente # 3. Moda
        moda_real = stats.mode(self.y_real)[0]
        desvio_padrao_real = np.std(self.y_real)  # 4. Desvio Padrão
        # 5. Quartis (Q1, Q2, Q3)
        Q1_real = np.percentile(self.y_real, 25)  # 25% (primeiro quartil)
        # 50% (mediana, ou segundo quartil)
        Q2_real = np.percentile(self.y_real, 50)
        Q3_real = np.percentile(self.y_real, 75)  # 75% (terceiro quartil)
        skewness_real = stats.skew(self.y_real)  # 6. Skewness (Assimetria)
        kurtosis_real = stats.kurtosis(self.y_real)  # 7. Kurtosis

        # Valores Previstos
        media_pred = np.mean(self.y_pred)  # 1. Média
        mediana_pred = np.median(self.y_pred)  # 2. Mediana
        # O valor mais frequente # 3. Moda
        moda_pred = stats.mode(self.y_pred)[0]
        desvio_padrao_pred = np.std(self.y_pred)  # 4. Desvio Padrão
        # 5. Quartis (Q1, Q2, Q3)
        Q1_pred = np.percentile(self.y_pred, 25)  # 25% (primeiro quartil)
        # 50% (mediana, ou segundo quartil)
        Q2_pred = np.percentile(self.y_pred, 50)
        Q3_pred = np.percentile(self.y_pred, 75)  # 75% (terceiro quartil)
        skewness_pred = stats.skew(self.y_pred)  # 6. Skewness (Assimetria)
        kurtosis_pred = stats.kurtosis(self.y_pred)  # 7. Kurtosis

        # Valores da diferenças
        media_diff = media_real - media_pred  # 1. Média
        mediana_diff = mediana_real - mediana_pred  # 2. Mediana
        moda_diff = moda_real - moda_pred  # O valor mais frequente # 3. Moda
        desvio_padrao_diff = desvio_padrao_real - desvio_padrao_pred  # 4. Desvio Padrão
        # 5. Quartis (Q1, Q2, Q3)
        #Q1_diff = Q1_real - Q1_pred  # 25% (primeiro quartil)
        #Q2_diff = Q2_real - Q2_pred  # 50% (mediana, ou segundo quartil)
        #Q3_diff = Q3_real - Q3_pred  # 75% (terceiro quartil)
        skewness_diff = skewness_real - skewness_pred  # 6. Skewness (Assimetria)
        kurtosis_diff = kurtosis_real - kurtosis_pred  # 7. Kurtosis

        resultado = {'media_real': media_real,
                     'mediana_real': mediana_real,
                     'moda_real': moda_real,
                     'desvio_padrao_real': desvio_padrao_real,
                     'Q1_real': Q1_real,
                     'Q2_real': Q2_real,
                     'Q3_real': Q3_real,
                     'skewness_real': skewness_real,
                     'kurtosis_real': kurtosis_real,
                     'media_pred': media_pred,
                     'mediana_pred': mediana_pred,
                     'moda_pred': moda_pred,
                     'desvio_padrao_pred': desvio_padrao_pred,
                     'Q1_pred': Q1_pred,
                     'Q2_pred': Q2_pred,
                     'Q3_pred': Q3_pred,
                     'skewness_pred': skewness_pred,
                     'kurtosis_pred': kurtosis_pred,
                     'media_diff': media_diff,
                     'mediana_diff': mediana_diff,
                     'moda_diff': moda_diff,
                     'desvio_padrao_diff': desvio_padrao_diff,
                     #'Q1_diff': Q1_diff,
                     #'Q2_diff': Q2_diff,
                     #'Q3_diff': Q3_diff,
                     'skewness_diff': skewness_diff,
                     'kurtosis_diff': kurtosis_diff}

        return resultado
