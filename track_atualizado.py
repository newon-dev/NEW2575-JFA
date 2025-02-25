import json
import logging
import time
import sys
from rich.console import Console
import threading
from rfid import RF600XML
from db import BancoDeDados
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Variáveis de ambiente
MOSTRAR_BARRA_CARREGAMENTO = True
DATABASE = "movimentacao.db"
carregando = True
console = Console()
leitoras_rfid = []
lista_de_posicoes = []

def recuperar_posicoes() -> list:
    global lista_de_posicoes
    try:
        db = BancoDeDados("movimentacao.db")
        result = db.recuperar_baias()
        if result:
            baias = []
            for baia in result: 
                baias.append({
                    'id': baia['id'],   
                    'tagx1': baia['tagx1'],
                    'tagx2': baia['tagx2'],
                    'tagy1': baia['tagy1'],
                    'tagy2': baia['tagy2'],  
                    
                })
            lista_de_posicoes = baias
            return baias
    except Exception as e:
        print(e)
        
def recuperar_leitores() -> list:
    try:
        db = BancoDeDados("movimentacao.db")
        result = db.recuperar_antenas()
        if result:
            antenas = []
            for antena in result: 
                antenas.append({
                    'id': antena[0],   
                    'nome': antena[1],
                    'ip': antena[2],
                })
            return antenas
    except Exception as e:
        print(e)
    
def recuperar_posicoes() ->list:
    db = BancoDeDados("movimentacao.db")
    result = db.recuperar_baias()   
    x_axis = []
    y_axis = []
    for item in result:
        x_axis.append({item['tagx1']: item['id']})
        x_axis.append({item['tagx2']: item['id']})
        y_axis.append({item['tagy1']: item['id']})
        y_axis.append({item['tagy2']: item['id']})
    return x_axis, y_axis

class PonteRolante:
    def __init__(self, numero):
        global leitoras_rfid
        self.numero = 0
        self.position = 0
        self.pos_x = "None"
        self.pos_y = "None"
        self.leitor_x_ip = ""
        self.leitor_y_ip = ""
        self.numero = numero
        self.leitor_rfid = [leitoras_rfid[self.numero], leitoras_rfid[self.numero + 1]]
        self.antenas = []
        self.posicao_antiga = 0
    
    def create_reader(self):
        try:
            self.antenas = [
            RF600XML(port=10001, host=self.leitor_rfid[0]['ip']),
            RF600XML(port=10001, host=self.leitor_rfid[1]['ip'])
            ]
            print(f"Antenas criadas com sucesso")
        except Exception as e:
            print("Erro ao criar instancia dos leitores")
            print(e)
   
    def atualizar_leituras(self):
                tag1 = self.antenas[1].ler_tag()
                tag0 = self.antenas[0].ler_tag()
                if tag0:
                    return tag0
                elif tag1:
                    return tag1
                else:
                    return None
   
    def verificar_posicao(self, tag, x_axis, y_axis):
        if tag:
            for baia in x_axis:
                if tag in baia:
                    primeiro_item = next(iter(baia.items()))
                    self.pos_x = primeiro_item[0]
                    break
            for baia in y_axis:
                if tag in baia:
                    primeiro_item = next(iter(baia.items()))
                    self.pos_y = primeiro_item[0]

    def calcular_id_posicao(self, x_axis, y_axis):
            for baia in x_axis:
                if(self.pos_x in baia):
                    for baia_y in y_axis:
                        if(self.pos_y in baia_y):
                            primeiro_item = next(iter(baia.items()))
                            posicao = primeiro_item[1]
                            return posicao
                        else:
                            return None
            
    def atualizar_banco_dados(self, posicao):
        try:
            if(self.posicao_antiga != posicao):
                db = BancoDeDados("movimentacao.db")
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                db.salvar_movimentacao(self.numero, posicao, timestamp )   
                return True
            else:
                return None           
        except Exception as e:
            print(e)
            return False

if __name__ == "__main__":
    leitoras_rfid = recuperar_leitores()
    ponte0 = PonteRolante(0) ## Para a ponte 2 utilizar numero 2
    ponte0.create_reader()
    x_axis, y_axis = recuperar_posicoes()
    while True:
        tag = ponte0.atualizar_leituras()
        if tag:
            ponte0.verificar_posicao(tag, x_axis, y_axis)
            posicao = ponte0.calcular_id_posicao(x_axis, y_axis)
            if posicao:
                resultado = ponte0.atualizar_banco_dados(posicao)
                print("Done")
                


        
    
    