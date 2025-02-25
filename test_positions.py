import requests
import json

# URL do servidor Flask
url = 'http://127.0.0.1:8080/modificar_posicoes'

# Dados para enviar no corpo da requisição POST
dados = {
    'id': 1,               # ID da posição
    'nome': 'Posição Teste', # Nome da posição
    'cor': '#FF5733'        # Cor da posição (em formato hexadecimal)
}

# Enviando a requisição POST
try:
    response = requests.post(url, json=dados)
    
    # Verificando o código de status da resposta
    if response.status_code == 200:
        # Se a requisição for bem-sucedida, exibe a resposta JSON
        resposta = response.json()
        if resposta.get('success') == 'true':
            print('Posição atualizada com sucesso!')
        else:
            print(f'Erro ao atualizar a posição: {resposta.get("erro")}')
    else:
        # Caso a resposta tenha um código de erro
        print(f'Erro: Código de status {response.status_code}')
        print(response.text)
except Exception as e:
    print(f'Erro ao fazer a requisição: {e}')
