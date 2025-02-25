import sqlite3
import random

NUMERO_DE_POSICOES = 96


class BancoDeDados:
    def __init__(self, nome_db: str):
        self.nome_db = nome_db
        self.conn = sqlite3.connect(nome_db, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        """
        Cria a tabela 'movimentacao' caso não exista.
        """
        try:
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS movimentacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ponte INT NOT NULL,
                x TEXT NOT NULL,
                y TEXT NOT NULL,
                horario TEXT NOT NULL
            )
            """
            )
            self.conn.commit()
            return True
        except Exception as e:
            return False

    def salvar_movimentacao(self, ponte, x, y, horario) -> bool:
        """
        Salva um array de dados no banco de dados.
        :param dados: Lista de arrays contendo [ponte, posicao, horario]
        """
        try:
            self.cursor.execute(
                """
            INSERT INTO movimentacao (ponte, x, y, horario)
            VALUES (?, ?, ?, ?)
            """,
                (ponte, x, y, horario),
            )
            self.conn.commit()
            print("Dados salvos com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            self.conn.rollback()
            return False

    def obter_ultima_posicao(self, ponte: int) -> list:
        """
        Retorna a última posição e horário conhecidos para a ponte especificada.
        :param id_ponte: ID da ponte rolante
        :return: Tupla (x, y, horario) ou None se não encontrado
        """
        self.cursor.execute(
            """
        SELECT x,y, horario
        FROM movimentacao
        WHERE ponte = ?
        ORDER BY id DESC
        LIMIT 1
        """,
            (ponte,),
        )
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado
        else:
            print(f"Nenhuma movimentação encontrada para a ponte com ID {ponte}.")
            return None

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()

    def criar_tabela_antenas(self):
        """
        Cria a tabela 'antenas caso não exista.
        """
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS antenas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            ip TEXT NOT NULL
        )
        """
        )
        self.conn.commit()

    def cadastrar_antena(self, nome: str, ip: str):
        """
        Cadastra uma antena no banco de dados.
        :param nome: Nome da antena.
        :param ip: IP da antena.
        """
        try:
            self.cursor.execute(
                """
            INSERT INTO antenas (nome, ip)
            VALUES (?, ?)
            """,
                (nome, ip),
            )
            self.conn.commit()
            print("Antena cadastrada com sucesso.")
        except Exception as e:
            print(f"Erro ao cadastrar antena: {e}")
            self.conn.rollback()

    def recuperar_antenas(self):
        """
        Recupera os dados das duas primeiras antenas cadastradas no banco de dados.
        :return: Lista de tuplas com (id, nome, ip) das antenas ou lista vazia se não houver antenas.
        """
        self.cursor.execute(
            """
        SELECT id, nome, ip
        FROM antenas ORDER BY ID DESC
        LIMIT 4
        """
        )
        resultado = self.cursor.fetchall()

        if resultado:
            return resultado
        else:
            return []

    def update_antenas(self, id, name, ip) -> bool:
        """
        Atualiza o nome e o IP de uma antena no banco de dados com base no ID.

        :param id: ID da antena que será atualizada.
        :param name: Novo nome a ser atribuído à antena.
        :param ip: Novo IP a ser atribuído à antena.
        :return: True se a atualização for bem-sucedida, False caso contrário.
        """
        try:
            self.cursor.execute(
                """
            UPDATE antenas
            SET nome = ?, ip = ?
            WHERE id = ?
            """,
                (name, ip, id),
            )

            self.conn.commit()

            if self.cursor.rowcount > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro ao atualizar antena: {e}")
            return False

    def criar_tabela_posicoes(self) -> bool:
        """
        Cria a tabela 'posicoes' caso não exista.
        """
        try:
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS posicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                name TEXT NOT NULL,
                x TEXT NOT NULL,
                y TEXT NOT NULL               
            )
            """
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def recuperar_posicoes(self) -> list:
        """
        Recupera os dados das duas primeiras antenas cadastradas no banco de dados.
        :return: Lista de tuplas com (id, nome, ip) das antenas ou lista vazia se não houver antenas.
        """
        self.cursor.execute(
            """
        SELECT id, color, name, x, y
        FROM posicoes ORDER BY ID ASC
        LIMIT ?
        """,
            (NUMERO_DE_POSICOES,),
        )
        resultado = self.cursor.fetchall()

        if resultado:
            return resultado
        else:
            return []

    def atualizar_mapa_posicoes(self, color: str, name: str, x: str, y: str) -> bool:
        """
        Atualiza os dados de uma posição no banco de dados com base no ID fornecido.
        :param x: Coordenada X
        :param y: Coordenada Y
        :param color: Novo valor de cor para a posição
        :param name: Novo nome para a posição
        :return: Retorna True se a atualização for bem-sucedida, False caso contrário
        """
        try:
            # Verificar se a linha existe antes de tentar atualizar
            self.cursor.execute(
                """
            SELECT * FROM posicoes WHERE x = ? AND y = ?
            """,
                (x, y),
            )

            if self.cursor.fetchone() is None:
                # Se não houver resultado, significa que a linha não existe
                print(f"Nenhuma linha encontrada para as coordenadas ({x}, {y}).")
                return False

            # Exibindo a consulta que será executada para fins de depuração
            print(
                f"Executando UPDATE para a posição ({x}, {y}) com cor '{color}' e nome '{name}'"
            )

            # Executando o UPDATE
            self.cursor.execute(
                """
            UPDATE posicoes
            SET color = ?, name = ?
            WHERE x = ? and y = ?
            """,
                (color, name, x, y),
            )

            # Comitando a transação
            self.conn.commit()

            # Verificando o número de linhas afetadas
            print(f"Número de linhas afetadas: {self.cursor.rowcount}")

            if self.cursor.rowcount > 0:
                # Se a linha foi realmente atualizada, retornamos True
                return True
            else:
                # Se nenhuma linha foi atualizada, logamos o ocorrido
                print(f"Nenhuma linha foi atualizada para a posição ({x}, {y})")
                return False
        except Exception as e:
            # Captura e exibe qualquer erro que ocorrer durante a execução da consulta
            print(f"Erro ao atualizar posição: {e}")
            return False

    def obter_logs(self) -> list:
        """
        Retorna as últimas 20 posições e horários conhecidos para as pontes.
        :return: Lista de dicionários com os dados ou uma lista vazia se não encontrar resultados.
        """
        self.cursor.execute(
            """
        SELECT id, ponte, x, y, horario
        FROM movimentacao
        ORDER BY id DESC
        LIMIT 50
        """
        )
        resultado = self.cursor.fetchall()

        if resultado:
            logs = []
            for posicao in resultado:
                logs.append(
                    {
                        "id": posicao[0],
                        "ponte": posicao[1],
                        "x": posicao[2],
                        "y": posicao[3],
                        "hora": posicao[4],
                    }
                )
            return logs
        else:
            return []

    def baixar_csv(self, limite: int = 50) -> list:
        """
        Busca dados da tabela com um limite configurável.
        Pode gerar um arquivo grande dependendo do limite.

        :param limite: O número de registros que serão retornados. O padrão é 50.
        :return: Lista de dicionários com os dados ou uma lista vazia se não encontrar resultados.
        """
        # A consulta SQL agora inclui um limite configurável
        self.cursor.execute(
            """
        SELECT id, ponte, x, y, horario
        FROM movimentacao
        ORDER BY id DESC
        LIMIT ?
        """,
            (limite,),
        )

        resultado = self.cursor.fetchall()

        if resultado:
            logs = []
            for posicao in resultado:
                logs.append(
                    {
                        "id": posicao[0],
                        "ponte": posicao[1],
                        "x": posicao[2],
                        "y": posicao[3],
                        "hora": posicao[4],
                    }
                )
            return logs
        else:
            return []

    def criar_tabela_baias(self) -> bool:
        """
        Cria a tabela 'baias' caso não exista.
        """
        try:
            self.cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS baias (
                x TEXT,
                y TEXT,
                tagx1 TEXT,
                tagx2 TEXT,
                tagy1 TEXT,
                tagy2 TEXT,
                tagy3 TEXT,
                tagy4 TEXT                                
            )
            """
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def recuperar_baias(self) -> list:
        """
        Puxa os dados da tabela baias
        :return: Lista de dicionários com os dados ou uma lista vazia se não encontrar resultados.
        """
        self.cursor.execute(
            """
        SELECT x, y, tagx1, tagx2, tagy1, tagy2, tagy3, tagy4
        FROM baias
        ORDER BY x ASC
        """
        )
        resultado = self.cursor.fetchall()
        if resultado:
            logs = []
            for posicao in resultado:
                logs.append(
                    {
                        "x": posicao[0],
                        "y": posicao[1],
                        "tagx1": posicao[2] if posicao[2] is not None else "",
                        "tagx2": posicao[3] if posicao[3] is not None else "",
                        "tagy1": posicao[4] if posicao[4] is not None else "",
                        "tagy2": posicao[5] if posicao[5] is not None else "",
                        "tagy3": posicao[6] if posicao[6] is not None else "",
                        "tagy4": posicao[7] if posicao[7] is not None else "",
                    }
                )
            return logs
        else:
            return []

    def resetar_baias(self) -> bool:
        """
        Reseta a tabela baias, criando ou atualizando entradas para cada combinação de x e y.
        """
        try:
            dados_baias = []
            for x in range(16):  # x variando de 0 a 15
                for y in range(6):  # y variando de 0 a 5
                    tagx1 = f"tagx1_{random.randint(1, 1000)}"
                    tagx2 = f"tagx2_{random.randint(1, 1000)}"
                    tagy1 = f"tagy1_{x}_{y}"
                    tagy2 = f"tagy2_{x}_{y}"
                    tagy3 = f"tagy3_{x}_{y}"
                    tagy4 = f"tagy4_{x}_{y}"
                    dados_baias.append((x, y, tagx1, tagx2, tagy1, tagy2, tagy3, tagy4))

            self.cursor.executemany(
                """
                INSERT OR REPLACE INTO baias (x, y, tagx1, tagx2, tagy1, tagy2, tagy3, tagy4)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                dados_baias,
            )
            self.conn.commit()
            print(
                f"{len(dados_baias)} entradas foram inseridas ou atualizadas na tabela baias."
            )
            return True
        except Exception as e:
            print(f"Erro ao tentar resetar a tabela baias: {e}")
            return False

    def atualizar_tag(self, valor_antigo: str, novo_valor: str) -> bool:
        """
        Atualiza todas as entradas na tabela baias onde qualquer tag (tagx1, tagx2, tagy1, tagy2) possui
        o valor antigo, e atualiza essas entradas para o novo valor.
        :param valor_antigo: O valor que as tags possuem e serão atualizadas.
        :param novo_valor: Novo valor a ser atribuído às tags selecionadas.
        :return: True se a atualização for bem-sucedida, False se ocorrer um erro.
        """
        try:
            tags = ["tagx1", "tagx2", "tagy1", "tagy2"]
            for tag in tags:
                sql = f"""
                UPDATE baias
                SET {tag} = ?
                WHERE {tag} = ?
                """
                self.cursor.execute(sql, (novo_valor, valor_antigo))
            self.conn.commit()
            print(
                f"Todas as entradas com valor '{valor_antigo}' em qualquer tag foram atualizadas para '{novo_valor}'."
            )
            return True
        except Exception as e:
            print(f"Erro ao atualizar as tags: {e}")
            return False

    def popular_grid(self) -> bool:
        """
        Popula a tabela 'posicoes' com um grid de 16 colunas de X e 6 linhas de Y.
        """
        try:
            for y in range(6):
                for x in range(16):
                    color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                    self.cursor.execute(
                        """
                    INSERT INTO posicoes (color, name, x, y) VALUES (?, ?, ?, ?)""",
                        (color, f"Cell_{x}_{y}", x, y),
                    )

            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    db = BancoDeDados("movimentacao.db")
    # db.criar_tabela()
    dados = [
        (1, "0", "0", "2025-02-04 10:00:00"),
        (1, "1", "0", "2025-02-04 10:00:00"),
        (1, "2", "0", "2025-02-04 10:00:00"),
        (1, "3", "0", "2025-02-04 10:00:00"),
        (1, "4", "0", "2025-02-04 10:00:00"),
    ]
    data = db.recuperar_baias()
    print(data)
    db.fechar_conexao()
