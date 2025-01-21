from scipy import stats
from datetime import date
from datetime import datetime
import random
import os
import pandas as pd
import numpy as np
from regressao import Regression
from classificacao import Classification
from series_temporais import Series_Temporais
import hashlib
import uuid
import sqlite3
import json


class ExperimentLogger():

    """
    Classe responsável por gerenciar a execução de experimentos de classificação e regressão.

    A classe calcula métricas, organiza os resultados e os salva em arquivos CSV. 
    Pode ser utilizada para experimentos de classificação ou regressão.
    """

    def __init__(self, tipo):
        """
        Inicializa a classe ExperimentLogger.

        Parâmetros:
        - tipo (str): Tipo do experimento ('Classificacao' ou 'Regressao').
        - y_real (array-like): Valores reais das saídas.
        - y_pred (array-like): Valores previstos pelo modelo.
        - X_real (array-like): Dados de entrada usados no experimento.

        Lança:
        - ValueError: Caso o tipo informado não seja 'Classificacao' ou 'Regressao'.

        Para salvar o relatorio em csv, precisa chamar a função salvando_relatorio(commit_id) o commit_id é para definir um historico de abordagem. 
        """

        # Definir o tipo logo no início
        self.tipo = tipo

        # self.endereco = str(uuid.uuid4())  # Gerando um identificador único
        # self.endereco = id(tipo)
        self.endereco = None

        # Inicializando o contador de IDs para classificação e regressão
        self.contador_id_classificacao = id(tipo)
        self.contador_id_regressao = id(tipo)
        self.contador_id_series_temporais = id(tipo)

        # Configuração inicial
        self.dados = pd.DataFrame()
        self.colunas = []

        # Data e hora atuais
        self.data_atual = date.today().strftime('%d/%m/%Y')
        self.hora_atual = datetime.now().strftime('%H:%M:%S')

        self.commit_id = None  # Inicia com None, que pode ser atribuído mais tarde

        #self._ajustar_contador_ids()

    def preparar_modelo(self, **kwargs):

        if self.tipo == 'Classificacao':
            # Instancia Classification
            self.modelo = Classification(
                kwargs.get('y_real'), kwargs.get(
                    'y_pred'), kwargs.get('X_real')
            )

        elif self.tipo == 'Regressao':
            # Instancia Regression
            self.modelo = Regression(
                kwargs.get('y_real'), kwargs.get(
                    'y_pred'), kwargs.get('X_real')
            )

        elif self.tipo == 'Series_Temporais':
            # Instancia Regression
            self.modelo = Series_Temporais(
                kwargs.get('y_real'), kwargs.get(
                    'y_pred')
            )
        else:
            raise ValueError(
                "Tipo inválido. Escolha entre 'Classificacao', 'Regressao',  ou 'Series_Temporais'."
            )

    # def _ajustar_contador_ids(self):
    #     """
    #     Ajusta os contadores de ID com base nos dados existentes no banco de dados SQLite.
    #     """
    #     # Caminho para o banco de dados SQLite
    #     db_path = './dados/banco_de_dados_classificacao/classificacao.db'

    #     # Conectando ao banco de dados
    #     conn = sqlite3.connect(db_path)
    #     cursor = conn.cursor()

    #     # Ajustando o contador para a tabela CLASSIFICACAO
    #     cursor.execute(
    #         "CREATE TABLE IF NOT EXISTS CLASSIFICACAO (id INTEGER PRIMARY KEY)")
    #     cursor.execute("SELECT MAX(id) FROM CLASSIFICACAO")
    #     # Obtém o valor máximo do ID
    #     max_id_classificacao = cursor.fetchone()[0]
    #     self.contador_id_classificacao = (
    #         max_id_classificacao + 1) if max_id_classificacao is not None else 1

    #     # Ajustando o contador para a tabela REGRESSAO
    #     cursor.execute(
    #         "CREATE TABLE IF NOT EXISTS REGRESSAO (id INTEGER PRIMARY KEY)")
    #     cursor.execute("SELECT MAX(id) FROM REGRESSAO")
    #     max_id_regressao = cursor.fetchone()[0]  # Obtém o valor máximo do ID
    #     self.contador_id_regressao = (
    #         max_id_regressao + 1) if max_id_regressao is not None else 1

    #     # Ajustando o contador para a tabela SERIES_TEMPORAIS
    #     cursor.execute(
    #         "CREATE TABLE IF NOT EXISTS SERIES_TEMPORAIS (id INTEGER PRIMARY KEY)")
    #     cursor.execute("SELECT MAX(id) FROM SERIES_TEMPORAIS")
    #     # Obtém o valor máximo do ID
    #     max_id_series_temporais = cursor.fetchone()[0]
    #     self.contador_id_series_temporais = (
    #         max_id_series_temporais + 1) if max_id_series_temporais is not None else 1

    #     # Fechando a conexão
    #     conn.close()



# ------------------------------------------------Classificação ou Regressão -------------------------------------------------------------

    def salvando_relatorio(self, commit_id, endereco, fpr=None, tpr=None, thresholds_roc=None, precision=None, recall=None, thresholds=None, avg_precision=None):
        """
            Salva as métricas e os relatórios de classificação ou regressão em 
            arquivos CSV, atualizando os IDs e associando os dados ao commit 
            especificado.

            PARÂMETROS:
            -----------
            commit_id : str
                O ID do commit associado ao relatório. Esse valor será utilizado 
                para identificar o commit ao qual os relatórios e métricas estão 
                associados.

            DESCRIÇÃO:
            -----------
            A função verifica o tipo do problema ('Classificacao' ou 'Regressao') 
            e, com base nesse tipo, executa diferentes ações para salvar as 
            métricas associadas.

            Para problemas de 'Classificação', a função realiza o seguinte:
            - Gera um ID sequencial para o relatório de classificação.
            - Recupera as métricas de classificação do modelo.
            - Salva as métricas em um arquivo CSV global de classificação.
            - Gera um relatório por classe e o salva em outro arquivo CSV.

            Para problemas de 'Regressão', a função realiza o seguinte:
            - Gera um ID sequencial para o relatório de regressão.
            - Recupera as métricas de regressão do modelo.
            - Salva as métricas em um arquivo CSV global de regressão.

            Ao final, a função imprime "Salvamento concluído" para indicar que o processo foi finalizado.

            EXEMPLO DE USO:
            ---------------
            # Salvar relatório para um commit específico
            relatorio.salvando_relatorio(commit_id="abc123")

            NOTAS:
            ------
            - Para problemas de classificação, dois arquivos CSV são salvos: 
            um para as métricas globais e outro por classe.
            - Para problemas de regressão, apenas um arquivo CSV é gerado.
            - O ID sequencial é gerado e incrementado com base no tipo de problema 
            (Classificação ou Regressão).
        """
        if self.tipo == 'Classificacao':
            id_atual = self.contador_id_classificacao
            #self.contador_id_classificacao += 1
            #dados = self.modelo.metricas_classificacao
            self.sqlite_classification(
                id_atual, commit_id, endereco, fpr, tpr, thresholds_roc, precision, recall, thresholds, avg_precision)

        elif self.tipo == 'Regressao':
            id_atual = self.contador_id_regressao
            #self.contador_id_regressao += 1
            #dados = self.modelo.metricas_regressao

            self.sqlite_regression(
                id_atual, commit_id, endereco)

        elif self.tipo == 'Series_Temporais':
            id_atual = self.contador_id_series_temporais
            #self.contador_id_series_temporais += 1
            #dados = self.modelo.decomposicao

            self.sqlite_seriestemporais(
                id_atual, commit_id, endereco)
        print("Salvamento concluído")


# ================================================ Parte Banco de dados ==================================================================

    # Função para verificar se uma coluna existe

    def coluna_existe(self, tabela, coluna, cursor):
        """
        Verifica se uma coluna existe em uma tabela no banco de dados.
        """
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = [info[1]
                   for info in cursor.fetchall()]  # Obtém os nomes das colunas
        return coluna in colunas
# -------------------------------------Salvando em um Banco de dados para classificação---------------------------------------------------

    def sqlite_classification(self, id_atual, commit_id, endereco, fpr, tpr, thresholds_roc, precision, recall, thresholds, avg_precision):

        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            './dados/banco_de_dados_classificacao/classificacao.db')
        cursor = conn.cursor()

        # Dados para salvar (exemplo: métrica de classificação)
        dados = self.modelo.metricas_classificacao
        y_test = self.modelo.y_real
        y_pred = self.modelo.y_pred

        # Convertendo os valores para tipos padrão (int ou float)
        dados_convertidos = {key: float(value) if isinstance(
            value, (np.int32, np.float32)) else value for key, value in dados.items()}

        metricas = json.dumps(dados_convertidos)  # Convertendo para JSON

        # Convertendo as métricas para JSON para armazenar no banco
        # parametros = json.dumps(dados)

        # Obtendo a data e hora atual para salvar
        data_atual = self.data_atual
        hora_atual = self.hora_atual

        # Verificando se fpr, tpr, e thresholds_roc são None e convertendo para JSON se não forem
        # Para curva roc
        fpr_str = json.dumps(fpr.tolist()) if fpr is not None else None
        tpr_str = json.dumps(tpr.tolist()) if tpr is not None else None
        thresholds_roc_str = json.dumps(
            thresholds_roc.tolist()) if thresholds_roc is not None else None
        # Para average Precision Score
        precision_str = json.dumps(
            precision.tolist()) if precision is not None else None
        recall_str = json.dumps(
            recall.tolist()) if recall is not None else None
        thresholds_str = json.dumps(
            thresholds.tolist()) if thresholds is not None else None

        # Excluindo a tabela "CLASSIFICACAO"
        # cursor.execute('DROP TABLE IF EXISTS CLASSIFICACAO')
        # Nome da tabela e coluna a adicionar
        # Verifica se a tabela CLASSIFICACAO existe
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='CLASSIFICACAO'")
        tabela_existe = cursor.fetchone() is not None

        # Se a tabela não existir, cria com todas as colunas
        if not tabela_existe:
            cursor.execute('''
                CREATE TABLE CLASSIFICACAO (
                    id INTEGER PRIMARY KEY,
                    id_commit TEXT,
                    controle_de_versao TEXT,
                    data DATETIME,
                    hora DATETIME,
                    dados TEXT,
                    y_test TEXT,
                    y_pred TEXT,
                    fpr TEXT,
                    tpr TEXT,
                    thresholds_roc TEXT,
                    precision TEXT,
                    recall TEXT,
                    thresholds TEXT,
                    avg_precision REAL
                    
                )
            ''')
        else:
            # Adiciona colunas extras se necessário
            for coluna in ["id_commit", "controle_de_versao", "data", "hora", "dados", "y_test", "y_pred", "fpr", "tpr", "thresholds_roc", "precision", "recall", "thresholds", "avg_precision"]:
                if not self.coluna_existe("CLASSIFICACAO", coluna, cursor):
                    cursor.execute(
                        f"ALTER TABLE CLASSIFICACAO ADD COLUMN {coluna} TEXT")

        # Inserindo dados do modelo
        cursor.execute('''
            INSERT INTO CLASSIFICACAO (id, id_commit, controle_de_versao, data, hora, dados, y_test, y_pred, fpr, tpr, thresholds_roc, precision, recall, thresholds, avg_precision)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            id_atual,                      # Exemplo de ID
            commit_id,                     # Exemplo de ID de commit
            endereco,                     # Controle de versão
            data_atual,                 # Data atual
            hora_atual,                 # Hora atual
            metricas,   # Dados do modelo, armazenados em formato JSON
            json.dumps(y_test.tolist()),  # y_test convertido para JSON
            json.dumps(y_pred.tolist()),  # y_pred convertido para JSON
            fpr_str,                     # fpr convertido para JSON ou None
            tpr_str,                     # tpr convertido para JSON ou None
            thresholds_roc_str,           # thresholds_roc convertido para JSON ou None
            precision_str,
            recall_str,
            thresholds_str,
            avg_precision

        ))

        # Comitando as mudanças
        conn.commit()

        # Fechando a conexão
        conn.close()
# -------------------------------------Salvando em um Banco de dados para Regressão-------------------------------------------------------

    def sqlite_regression(self, id_atual, commit_id, endereco):

        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            './dados/banco_de_dados_regressao/regressao.db')
        cursor = conn.cursor()

        # Dados para salvar (exemplo: métrica de classificação)
        dados = self.modelo.metricas_regressao
        y_test = self.modelo.y_real
        y_pred = self.modelo.y_pred

        # Convertendo os valores para tipos padrão (int ou float)
        dados_convertidos = {key: float(value) if isinstance(
            value, (np.int32, np.float32)) else value for key, value in dados.items()}

        metricas = json.dumps(dados_convertidos)  # Convertendo para JSON

        # Convertendo as métricas para JSON para armazenar no banco
        # parametros = json.dumps(dados)

        # Obtendo a data e hora atual para salvar
        data_atual = self.data_atual
        hora_atual = self.hora_atual

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='REGRESSAO'")
        tabela_existe = cursor.fetchone() is not None

        # Se a tabela não existir, cria com todas as colunas
        if not tabela_existe:
            cursor.execute('''
                CREATE TABLE REGRESSAO (
                    id INTEGER PRIMARY KEY,
                    id_commit TEXT,
                    controle_de_versao TEXT,
                    data DATETIME,
                    hora DATETIME,
                    dados TEXT,
                    y_test TEXT,
                    y_pred TEXT
                    
                )
            ''')
        else:
            # Adiciona colunas extras se necessário
            for coluna in ["id_commit", "controle_de_versao", "data", "hora", "dados", "y_test", "y_pred"]:
                if not self.coluna_existe("REGRESSAO", coluna, cursor):
                    cursor.execute(
                        f"ALTER TABLE REGRESSAO ADD COLUMN {coluna} TEXT")

        # Inserindo dados do modelo
        cursor.execute('''
            INSERT INTO REGRESSAO (id, id_commit, controle_de_versao, data, hora, dados, y_test, y_pred)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            id_atual,                      # Exemplo de ID
            commit_id,                     # Exemplo de ID de commit
            endereco,                     # Controle de versão
            data_atual,                 # Data atual
            hora_atual,                 # Hora atual
            metricas,   # Dados do modelo, armazenados em formato JSON
            json.dumps(y_test.tolist()),  # y_test convertido para JSON
            json.dumps(y_pred.tolist())  # y_pred convertido para JSON

        ))

        # Comitando as mudanças
        conn.commit()

        # Fechando a conexão
        conn.close()

# -------------------------------------Salvando em um Banco de dados para Séries temporais------------------------------------------------
    def sqlite_seriestemporais(self, id_atual, commit_id, endereco):

        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            './dados/banco_de_dados_seriestemporais/series_temporais.db')
        cursor = conn.cursor()

        # Dados para salvar (exemplo: métrica de classificação)
        dados = self.modelo.metricas_series_temporais
        y_test = self.modelo.y_real
        y_pred = self.modelo.y_pred

        # Convertendo os valores para tipos padrão (int ou float)
        dados_convertidos = {key: float(value) if isinstance(
            value, (np.int32, np.float32)) else value for key, value in dados.items()}

        decomposicao = json.dumps(dados_convertidos)  # Convertendo para JSON

        # Convertendo as métricas para JSON para armazenar no banco
        # parametros = json.dumps(dados)

        # Obtendo a data e hora atual para salvar
        data_atual = self.data_atual
        hora_atual = self.hora_atual

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='SERIES_TEMPORAIS'")
        tabela_existe = cursor.fetchone() is not None

        # Se a tabela não existir, cria com todas as colunas
        if not tabela_existe:
            cursor.execute('''
                CREATE TABLE SERIES_TEMPORAIS (
                    id INTEGER PRIMARY KEY,
                    id_commit TEXT,
                    controle_de_versao TEXT,
                    data DATETIME,
                    hora DATETIME,
                    dados TEXT,
                    y_test TEXT,
                    y_pred TEXT
                    
                )
            ''')
        else:
            # Adiciona colunas extras se necessário
            for coluna in ["id_commit", "controle_de_versao", "data", "hora", "dados", "y_test", "y_pred"]:
                if not self.coluna_existe("SERIES_TEMPORAIS", coluna, cursor):
                    cursor.execute(
                        f"ALTER TABLE SERIES_TEMPORAIS ADD COLUMN {coluna} TEXT")

        # Inserindo dados do modelo
        cursor.execute('''
            INSERT INTO SERIES_TEMPORAIS (id, id_commit, controle_de_versao, data, hora, dados, y_test, y_pred)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            id_atual,                      # Exemplo de ID
            commit_id,                     # Exemplo de ID de commit
            endereco,                     # Controle de versão
            data_atual,                 # Data atual
            hora_atual,                 # Hora atual
            decomposicao,   # Dados do modelo, armazenados em formato JSON
            json.dumps(y_test.tolist()),  # y_test convertido para JSON
            json.dumps(y_pred.tolist())  # y_pred convertido para JSON

        ))

        # Comitando as mudanças
        conn.commit()

        # Fechando a conexão
        conn.close()

    def consultar_modelos(self, id_atual=None, commit_id=None, endereco=None):
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            './dados/banco_de_dados_classificacao/classificacao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = 'SELECT * FROM CLASSIFICACAO WHERE 1=1'
        params = []

        if id_atual is not None:
            query += ' AND id = ?'
            params.append(id_atual)

        if commit_id is not None:
            query += ' AND id_commit = ?'
            params.append(commit_id)

        if endereco is not None:
            query += ' AND controle_de_versao = ?'
            params.append(endereco)

        # Executando a consulta com os parâmetros passados
        cursor.execute(query, params)

        # Recuperando os resultados
        modelos = cursor.fetchall()

        # Exibindo os dados
        for modelo in modelos:
            print(modelo)

        # Fechando a conexão
        conn.close()


# --------------------------------------------------------------------------------------------------------------------------------

    def report(self, detalhado=False):
        """
        Retorna o relatório gerado pelo modelo.

        Args:
            detalhado (bool): Se True, retorna um relatório mais completo.
        """
        if self.tipo == 'Classificacao':
            if detalhado:
                print("Relatório detalhado:")
                # Retorna o resultado de classificação
                return self.modelo.classification_result
            return self.modelo.report()  # Chamando a função report para outros tipos de modelos

        if self.tipo == 'Regressao':
            if detalhado:
                print("Relatório detalhado:")
                return self.modelo.regression_result  # Retorna o resultado de regressão
            return self.modelo.report()  # Chamando a função report para outros tipos de modelos
        
        if self.tipo == 'Series_Temporais':
            if detalhado:
                print("Relatório detalhado:")
                return self.modelo.series_result  # Retorna o resultado de regressão
            return self.modelo.report()  # Chamando a função report para outros tipos de modelos

    def get_metric(self, metric_name):
        return self.modelo.get_metric(metric_name)

# --------------------------------------------------------------------------------------------------------------------------------
