from db import BancoDeDados
def gerar_mapa_inicial():
    """
    Gera um dicionário com as posições iniciais do mapa.
    """
    mapa = []
    for y in range(6):
        for x in range(16):
            mapa.append({
                "x": x,
                "y": y,
                "color": "white",
                "name": f"Posicao_{x}_{y}"
            })
    return mapa
if __name__ == "__main__":
    db = BancoDeDados('movimentacao.db')
    mapa_inicial = gerar_mapa_inicial()
    for posicao in mapa_inicial:
        print(db.atualizar_mapa_posicoes(posicao["color"], posicao["name"], posicao["x"], posicao["y"]))