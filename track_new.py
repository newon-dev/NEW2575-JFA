import logging
import time
import sys
from rich.console import Console
import threading
from rfid import RF600XML
from db import BancoDeDados

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MOSTRAR_BARRA_CARREGAMENTO = True
DATABASE = "movimentacao.db"
carregando = True
console = Console()

def carregar_mapa_posicoes() -> dict:
    """Carrega as informações das baias do banco de dados
    :retorna um array com as posições
    """
    try:
       db = BancoDeDados(DATABASE)
       baias = db.recuperar_baias()
       return baias

    except Exception as e:
        print(f"Erro ao acessar o banco de dados {e}")
        return None

class PonteRolante:
    """
    Classe responsável pelo rastreamento da posição da ponte rolante com base nas tags RFID lidas.
    """

    def __init__(self, mapa_posicoes):
        self.tag_x = None
        self.tag_y = None
        self.posicao = "Desconhecida"
        self.nome_posicao = "Desconhecida"
        self.mapa_posicoes = mapa_posicoes
        self.ultima_posicao = ""

    def atualizar_posicao(self, tag: str) -> None:
        """
        Atualiza a posição da ponte com base na tag lida.
        """
        eixo = self.identificar_eixo(tag)

        if eixo == "x":
            self.tag_x = tag
        elif eixo == "y":
            self.tag_y = tag

        if self.calcular_posicao():
            return True
        return False

    def identificar_eixo(self, tag: str) -> str:
        """
        Determina se a tag pertence ao eixo X ou Y.
        """
        for posicao in self.mapa_posicoes:
            if tag in (posicao["tagx1"], posicao["tagx2"]):
                return "x"
            elif tag in (posicao["tagy1"], posicao["tagy2"], posicao["tagy3"], posicao["tagy4"]):
                return "y"
        return None

    def calcular_posicao(self) -> bool:
        """
        Determina a posição da ponte verificando se está dentro do intervalo correto.
        - Se X estiver entre x1 e x2, e Y entre y1 e y2 -> posição confirmada.
        - Se a posição for a última baia, ela se estende até o infinito.
        """
        nome_posicao = "Testes"

        for posicao in self.mapa_posicoes:
            x1, x2 = posicao["tagx1"], posicao["tagx2"]
            y1, y2, y3, y4 = posicao["tagy1"], posicao["tagy2"], posicao["tagy3"], posicao["tagy3"]
            dentro_x = False
            dentro_y = False

            if x1 and not x2 and self.tag_x == x1:
                dentro_x = True

            elif x1 and x2 and (self.tag_x in (x1, x2)):
                dentro_x = True

            if y1 and y2 and (self.tag_y in (y1, y2)):
                dentro_y = True
            
            if y3 and y4 and (self.tag_y in (y3, y4)):
                dentro_y = True

            if dentro_x and dentro_y:
                self.posicao = nome_posicao
                self.nome_posicao = nome_posicao
                break
            elif dentro_x:
                self.posicao = f"{nome_posicao} (Y desconhecido)"
                self.nome_posicao = nome_posicao
            elif dentro_y:
                self.posicao = f"X desconhecido ({nome_posicao})"
                self.nome_posicao = nome_posicao
        else:
            self.posicao = "Desconhecida"
            self.nome_posicao = "Desconhecida"

        return True

    def detectar_ponte(self, tag):
        eixo = self.identificar_eixo(tag)
        if eixo == "x":
            self.tag_x = tag
        elif eixo == "y":
            self.tag_y = tag

        return self.calcular_posicao()

if __name__ == "__main__":
    mapa_posicoes = carregar_mapa_posicoes()
    leitores = [
        RF600XML(port=10001, host="10.0.0.10"),
        RF600XML(port=10001, host="10.0.0.11")
    ]
    if MOSTRAR_BARRA_CARREGAMENTO:
        thread = threading.Thread(target=lambda: console.status("[bold green]Lendo tags...", spinner="dots"), daemon=True)
        thread.start()
    if len(leitores) != 2:
        print("Foi informado um número incorreto de leitores")
        sys.exit(1)
    else:
        if mapa_posicoes:
            ponte = PonteRolante(mapa_posicoes)
            try:
                while True:
                    for i, leitor in enumerate(leitores):
                        tag = leitor.ler_tag()
                        if tag:
                            carregando = False
                            resultado = ponte.detectar_ponte(tag)
                            if resultado:
                                if ponte.ultima_posicao != ponte.nome_posicao:
                                    print(f"Posição atual: {ponte.nome_posicao} (Anterior: {ponte.ultima_posicao})")
                                    ponte.ultima_posicao = ponte.nome_posicao
                                else:
                                    print("Posição se manteve igual")

                    time.sleep(0.5)  
            except KeyboardInterrupt:
                print("\nEncerrando monitoramento...")
                for leitor in leitores:
                    leitor.stop()
                    leitor.client_socket.close()
                print("Conexões fechadas com sucesso.")

