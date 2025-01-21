import pandas as pd
import sqlite3
import json


class Consulta:
    def __init__(self):
        pass

    def consultar_metricas_cl(self, id_atual=None, commit_id=None, endereco=None):
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_classificacao/classificacao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = 'SELECT dados FROM CLASSIFICACAO WHERE 1=1'
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

        # Convertendo os resultados para um DataFrame
        if modelos:
            # Como 'dados' é retornado como texto JSON, vamos carregar e expandir
            # Converte a string JSON em um dicionário e cria um DataFrame com esses dados
            # Convertendo JSON para dicionário
            dados_json = [json.loads(modelo[0]) for modelo in modelos]
            # Criando DataFrame com as chaves como colunas
            df = pd.DataFrame(dados_json)
            # print(df)  # Exibindo o DataFrame
        else:
            print("Nenhum modelo encontrado.")

        # Fechando a conexão
        conn.close()

        return df  # Retornando o DataFrame

    def consultar_modelos_cl(self, id_atual=None, commit_id=None, endereco=None):
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_classificacao/classificacao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = '''
            SELECT id, id_commit, controle_de_versao, data, hora
            FROM CLASSIFICACAO 
            WHERE 1=1
        '''
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

        # Convertendo os resultados para um DataFrame
        if modelos:
            # Criando um DataFrame a partir dos dados retornados
            df = pd.DataFrame(modelos, columns=[
                              "id", "commit_id", "controle_de_versao", "data", "hora"])

            # Convertendo os campos de data e hora para o formato adequado
            # df['data_atual'] = pd.to_datetime(
            #     # Formato de data
            #     df['data_atual'], errors='coerce').dt.strftime('%Y-%m-%d')
            # df['hora_atual'] = pd.to_datetime(
            #     # Formato de hora
            #     df['hora_atual'], errors='coerce').dt.strftime('%H:%M:%S')

        else:
            print("Nenhum modelo encontrado.")

        # Fechando a conexão
        conn.close()

        return df  # Retorna o DataFrame

    def consultar_valores_cl(self, id_atual=None, commit_id=None, endereco=None):
        """
        Consulta os dados da tabela CLASSIFICACAO e retorna como um dicionário.
        """
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_classificacao/classificacao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = '''
            SELECT id, id_commit, controle_de_versao, data, hora, y_test,y_pred,fpr,tpr,thresholds_roc, precision, recall, thresholds,avg_precision
            FROM CLASSIFICACAO
            WHERE 1=1
        '''
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

        # Convertendo os resultados para um dicionário
        if modelos:
            colunas = ["id", "commit_id",
                       "controle_de_versao", "data", "hora", "y_test", "y_pred", "fpr", "tpr", "thresholds_roc", "precision", "recall", "thresholds", "avg_precision"]
            resultado = []
            for modelo in modelos:
                modelo_dict = {colunas[i]: modelo[i]
                               for i in range(len(colunas))}
                resultado.append(modelo_dict)
        else:
            print("Nenhum modelo encontrado.")
            resultado = []

        # Fechando a conexão
        conn.close()

        return resultado  # Retorna uma lista de dicionários

    def deletar_dados_cl(self, id_atual=None, commit_id=None, endereco=None):
        """
        Deleta registros da tabela CLASSIFICACAO com base nos critérios fornecidos.

        Parâmetros:
            id_atual (int): ID do registro a ser deletado.
            commit_id (str): Commit ID do registro a ser deletado.
            endereco (str): Endereço do controle de versão do registro a ser deletado.

        Retorna:
            int: Número de registros deletados.
        """
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_classificacao/classificacao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = 'DELETE FROM CLASSIFICACAO WHERE 1=1'
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

        # Executando a consulta
        cursor.execute(query, params)
        registros_deletados = cursor.rowcount  # Obtendo o número de registros deletados

        # Salvando as mudanças e fechando a conexão
        conn.commit()
        conn.close()

        print('Registro deletado {registros_deletados}')


# --------------------------------------Regression-----------------------------------------------------------------------------------------
    def consultar_metricas_re(self, id_atual=None, commit_id=None, endereco=None):
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_regressao/regressao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = 'SELECT dados FROM REGRESSAO     WHERE 1=1'
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

        # Convertendo os resultados para um DataFrame
        if modelos:
            # Como 'dados' é retornado como texto JSON, vamos carregar e expandir
            # Converte a string JSON em um dicionário e cria um DataFrame com esses dados
            # Convertendo JSON para dicionário
            dados_json = [json.loads(modelo[0]) for modelo in modelos]
            # Criando DataFrame com as chaves como colunas
            df = pd.DataFrame(dados_json)
            # print(df)  # Exibindo o DataFrame
        else:
            print("Nenhum modelo encontrado.")

        # Fechando a conexão
        conn.close()

        return df  # Retornando o DataFrame


    def consultar_modelos_re(self, id_atual=None, commit_id=None, endereco=None):
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_regressao/regressao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = '''
                SELECT id, id_commit, controle_de_versao, data, hora
                FROM REGRESSAO 
                WHERE 1=1
            '''
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

        # Convertendo os resultados para um DataFrame
        if modelos:
            # Criando um DataFrame a partir dos dados retornados
            df = pd.DataFrame(modelos, columns=[
                            "id", "commit_id", "controle_de_versao", "data", "hora"])

            # Convertendo os campos de data e hora para o formato adequado
            # df['data_atual'] = pd.to_datetime(
            #     # Formato de data
            #     df['data_atual'], errors='coerce').dt.strftime('%Y-%m-%d')
            # df['hora_atual'] = pd.to_datetime(
            #     # Formato de hora
            #     df['hora_atual'], errors='coerce').dt.strftime('%H:%M:%S')

        else:
            print("Nenhum modelo encontrado.")

        # Fechando a conexão
        conn.close()

        return df  # Retorna o DataFrame


    def consultar_valores_re(self, id_atual=None, commit_id=None, endereco=None):
        """
            Consulta os dados da tabela REGRESSAO e retorna como um dicionário.
            """
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_regressao/regressao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = '''
                SELECT id, id_commit, controle_de_versao, data, hora, y_test, y_pred
                FROM REGRESSAO
                WHERE 1=1
            '''
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

        # Convertendo os resultados para um dicionário
        if modelos:
            colunas = ["id", "commit_id",
                    "controle_de_versao", "data", "hora", "y_test", "y_pred"]
            resultado = []
            for modelo in modelos:
                modelo_dict = {colunas[i]: modelo[i]
                            for i in range(len(colunas))}
                resultado.append(modelo_dict)
        else:
            print("Nenhum modelo encontrado.")
            resultado = []

        # Fechando a conexão
        conn.close()

        return resultado  # Retorna uma lista de dicionários


    def deletar_dados_re(self, id_atual=None, commit_id=None, endereco=None):
        """
        Deleta registros da tabela CLASSIFICACAO com base nos critérios fornecidos.

        Parâmetros:
            id_atual (int): ID do registro a ser deletado.
            commit_id (str): Commit ID do registro a ser deletado.
            endereco (str): Endereço do controle de versão do registro a ser deletado.

        Retorna:
            int: Número de registros deletados.
        """
        # Conectando ao banco de dados SQLite
        conn = sqlite3.connect(
            '../dados/banco_de_dados_regressao/regressao.db')
        cursor = conn.cursor()

        # Montando a consulta SQL dinamicamente
        query = 'DELETE FROM REGRESSAO WHERE 1=1'
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

        # Executando a consulta
        cursor.execute(query, params)
        registros_deletados = cursor.rowcount  # Obtendo o número de registros deletados

        # Salvando as mudanças e fechando a conexão
        conn.commit()
        conn.close()

        print('Registro deletado {registros_deletados}')
