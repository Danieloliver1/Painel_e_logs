import numpy as np
import pandas as pd
from scipy import stats
import os
from estastistica import Statistic
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_curve, auc, precision_recall_curve



class Classification(Statistic):

    def __init__(self, y_real, y_pred, X_real):
        # Passa os argumentos para a classe pai
        super().__init__(y_real, y_pred)

        self.y_real = y_real
        self.y_pred = y_pred
        self.X_real = X_real

        self.metricas = {}
        self.metricas_classificacao = {}
        self.metricas_detalhada = {}

        # Inicializa um dicionário para armazenar resultados estastístico
        self.resultado = {}

        # Chama a função de cálculo das métricas de regressão
        self.calculo_metricas_classificacao()

        # np.array para transformar em uma array
        self.classes = list(np.unique(np.array(y_real)))

    def calculo_metricas_classificacao(self):

        # Confusion Matrix
        cm = confusion_matrix(self.y_real, self.y_pred)
        VP = cm[1, 1]  # Verdadeiros Positivos
        VN = cm[0, 0]  # Verdadeiros Negativos
        FP = cm[0, 1]  # Falsos Positivos
        FN = cm[1, 0]  # Falsos Negativos

        # Para binarios ou multiclasses
        valores_unicos = np.unique(self.y_real)

        if len(valores_unicos) > 2:
            # Calculando as métricas (com agregação)
            acuracia = accuracy_score(self.y_real, self.y_pred)  # Acurácia
            precision = precision_score(
                self.y_real, self.y_pred, average='macro')
            recall = recall_score(self.y_real, self.y_pred, average='macro')
            f1 = f1_score(self.y_real, self.y_pred, average='macro')
        elif len(valores_unicos) == 2:
            # Calculando as métricas
            acuracia = accuracy_score(self.y_real, self.y_pred)  # Acurácia
            precision = precision_score(
                self.y_real, self.y_pred, average='binary')  # Precisão
            recall = recall_score(self.y_real, self.y_pred,
                                  average='binary')  # Recall
            f1 = f1_score(self.y_real, self.y_pred,
                          average='binary')  # F1-Score

        # Calculando as métricas (com agregação)
        precision_macro = precision_score(
            self.y_real, self.y_pred, average='macro')
        recall_macro = recall_score(self.y_real, self.y_pred, average='macro')
        f1_macro = f1_score(self.y_real, self.y_pred, average='macro')

        precision_micro = precision_score(
            self.y_real, self.y_pred, average='micro')
        recall_micro = recall_score(self.y_real, self.y_pred, average='micro')
        f1_micro = f1_score(self.y_real, self.y_pred, average='micro')

        precision_weighted = precision_score(
            self.y_real, self.y_pred, average='weighted')
        recall_weighted = recall_score(
            self.y_real, self.y_pred, average='weighted')
        f1_weighted = f1_score(self.y_real, self.y_pred, average='weighted')

        # FDR - Taxa de falsa descoberta
        fdr = FP / (FP + VP) if (FP + VP) > 0 else 0

        # NPU - Valor preditivo negativo
        npu = VN / (VN + FN) if (VN + FN) > 0 else 0

        # Prevalência
        prevalencia = (VP + FP) / (VP + VN + FP +
                                   FN) if (VP + VN + FP + FN) > 0 else 0

        # Taxa de falsa Omissão
        For = FN / (FN + VN) if (FN + VN) > 0 else 0

        # TPR - Taxa de verdadeiro positivo (Sensibilidade)
        tpr = VP / (VP + FN) if (VP + FN) > 0 else 0

        # FNR - Taxa de falso negativo
        fnr = FN / (FN + VP) if (FN + VP) > 0 else 0

        # FPR - Taxa de falso positivo
        fpr = FP / (FP + VN) if (FP + VN) > 0 else 0

        # Especificidade (TNR - True Negative Rate)
        especificidade = VN / (VN + FP) if (VN + FP) > 0 else 0

        # LR+ - Teste da razão de verossimilhança positiva
        lr_positivo = tpr / (1 - especificidade) if (1 -
                                                     especificidade) > 0 else 0

        # LR- - Teste de razão de verossimilhança negativa
        lr_negativo = (1 - tpr) / especificidade if especificidade > 0 else 0

        # --------------------------métricas globais--------------------------------------------------

        # Lista com os nomes das métricas
        nomes_metricas = [
            'Acuracia',
            'Precision',
            'Recall',
            'Especificidade',
            'F1_score',
            'Taxa_falsa_descoberta(FDR)',
            'Valor_preditivo_negativo(NPU)',
            'Prevalencia',
            'Taxa_falsa_Omissao(for)',
            'Sensibilidade(TPR)',
            'Taxa_falso_negativo',
            'Taxa_falso_positivo',
            'Teste_razao_verossimilhanca_negativa(LR-)',
            'Teste_razao_verossimilhanca_positiva(LR+)'
        ]

        lista_metricas = [
            acuracia,
            precision,
            recall,
            especificidade,
            f1,
            fdr,
            npu,
            prevalencia,
            For,
            tpr,
            fnr,
            fpr,
            lr_negativo,
            lr_positivo,
        ]

        nomes_metricas_detalhada = [
            'Precisão (Macro)',
            'Recall (Macro)',
            'F1-Score (Macro)',
            'Precisão (Micro)',
            'Recall (Micro)',
            'F1-Score (Micro)',
            'Precisão (Ponderada)',
            'Recall (Ponderada)',
            'F1-Score (Ponderada)',
        ]

        lista_metricas_detalhada = [
            precision_macro,
            recall_macro,
            f1_macro,
            precision_micro,
            recall_micro,
            f1_micro,
            precision_weighted,
            recall_weighted,
            f1_weighted,

        ]

        # Loop para calcular cada métrica ponderada e adicionar ao dicionário
        for nome, valores in zip(nomes_metricas, lista_metricas):
            self.metricas[nome] = np.sum(np.array(valores))

        for nome_detalhada, valores_detalhada in zip(nomes_metricas_detalhada, lista_metricas_detalhada):
            self.metricas_detalhada[nome_detalhada] = np.sum(
                np.array(valores_detalhada))

        # Armazenando as métricas globais
        self.metricas_classificacao = {**self.metricas, **self.summary()}
        #self.

    @property
    def classification_result(self):
        """
        Método getter para acessar as métricas de classificação
        """
        return self.metricas_classificacao | self.metricas_detalhada  # Retorna o dicionário de métricas de classificação por classes

    def get_metric(self, metric_name):
        """
        Método para acessar uma métrica específica.
        """
        resultado = self.metricas_classificacao
        return resultado.get(metric_name, "Métrica não encontrada")

    def report(self):
        """
        Método para gerar um relatório das métricas de classificação, retorna um Dataframe.
        """
        dados = self.metricas_classificacao
        df = pd.DataFrame(list(dados.items()), columns=['Nome', 'Valor'])
        return df
    
    
