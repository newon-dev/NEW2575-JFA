import json
import logging
import time
import sys
from rich.console import Console
from rich.spinner import Spinner
import threading
from rfid import RF600XML

"""
Arquivo:track.py
Descrição: Monitoramento de posição de ponte rolante usando RFID.
Data de criação: Fevereiro 2025
"""

__author__ = "Victor Sousa"
__email__ = "victor.sousa@newon.io"


#_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ #
#Configuração de módulos
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ __ _ _ #
#Variáveis de ambiente geral
MOSTRAR_BARRA_CARREGAMENTO = True
DATABASE = "movimentacao.db"
carregando = True
console = Console()


def carregar_mapa_posicoes(arquivo: object) -> list:
    """
    Função que recebe um arquivo .json com o mapeamento de posições e seus respectivos nomes da ponte rolante
    """
    try:
        with open(arquivo, 'r') as f:
            mapa_posicoes = json.load(f)
        logging.info("Mapa de posições carregado com sucesso.")
        return mapa_posicoes
    except FileNotFoundError:
        logging.error(f"Arquivo {arquivo} não encontrado.")
        return {}
    except json.JSONDecodeError:
        logging.error("Erro ao decodificar o arquivo JSON.")
        return {}
# VERFICADO OK
def carregando() -> None:
    """
    Exibe um spinner de loading até que exibir_carregamento seja False.
    """
    with console.status("[bold green]Lendo tags...", spinner="dots") as status:
        while True:
            if not carregando:
                break
            time.sleep(0.1)
#VERIFICADO OK
class PonteRolante:
    """
    Classe responsável pelo tracking da ponte rolante, possuí toda a lógica para rastrear a ponte.
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
        Responsável por atualizar a posição da ponte em relação ao eixo que ela pertence X ou Y
        :param: Str contendo a tag a ser definida
        """
        eixo = self.identificar_eixo(tag)
        
        if eixo == "x":
            self.tag_x = tag
        elif eixo == "y":
            self.tag_y = tag

        return True if self.calcular_posicao() else False
        


    def identificar_eixo(self, tag: str)-> str:
        """
        Identifica o eixo (x ou y) com base na tag fornecida.
        :param: Tag Str contendo a tag rfid
        :return: Retorna se a tag pertence ao eixo X ou Y
        """
        for nome_posicao, posicao_info in self.mapa_posicoes.items():
            if tag == posicao_info["x"]:
                return "x"
            elif tag == posicao_info["y"]:
                return "y"
        return None

    def calcular_posicao(self) -> str:
        """
        Calcula a posição com base nas tags lidas e no mapa de posições.
        :return: Posição: Retorna a posição conhecida da ponte no momento
        """
        if self.tag_x and self.tag_y:
            # Busca a combinação de x e y no mapa de posições
            for nome_posicao, posicao_info in self.mapa_posicoes.items():
                if posicao_info["x"] == self.tag_x and posicao_info["y"] == self.tag_y:
                    self.posicao = nome_posicao
                    self.nome_posicao = nome_posicao
                    break
            else:
                self.posicao = "Posição Desconhecida"
                self.nome_posicao = "Desconhecida"
        elif self.tag_x:
            self.posicao = f"{self.tag_x}, Y Desconhecido"
            self.nome_posicao = "Y Desconhecido"
        elif self.tag_y:
            self.posicao = f"X Desconhecido, {self.tag_y}"
            self.nome_posicao = "X Desconhecido"
        else:
            self.posicao = "Desconhecida"
            self.nome_posicao = "Desconhecida"
        #logging.info(f"Nova posição da ponte: {self.nome_posicao} (Posição: {self.posicao})")
        return True
#VERIFICADO OK
        

if __name__ == "__main__":
    mapa_posicoes = carregar_mapa_posicoes('positions.json')
    leitores = [
        RF600XML(port=10001, host="10.0.0.10"),
        RF600XML(port=10001, host="10.0.0.11")
    ] ##Conjunto de leitores das tags RFID, sendo um x,y 

    if MOSTRAR_BARRA_CARREGAMENTO:
        thread = threading.Thread(target=carregando, daemon=True)
        thread.start()

    if len(leitores) != 2:
        print("Foi informado um numero maior que dois leitores")
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
                            resultado = ponte.atualizar_posicao(tag)
                            if resultado:
                                print(ponte.ultima_posicao != ponte.nome_posicao)
                                if ponte.ultima_posicao != ponte.nome_posicao:
                                    print(f"posicao atual {ponte.nome_posicao} antiga {ponte.ultima_posicao}")
                                    ponte.ultima_posicao = ponte.nome_posicao
                                else:
                                    print("Posição se manteve igual")

                            carregando = True
                    time.sleep(0.5)  
            except KeyboardInterrupt:
                print("\nEncerrando monitoramento...")
                for leitor in leitores:
                    leitor.stop()
                    leitor.client_socket.close()
                print("Conexões fechadas com sucesso.")
#VERIFICADO OK