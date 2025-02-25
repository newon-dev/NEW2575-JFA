import requests
import json

# URL do seu endpoint
url = 'http://127.0.0.1:8080/modificar_antenas'

# Dados para enviar no corpo da requisição
dados = {
    "id": 1,
    "nome": "teste ponte 2",
    "ip": "10.0.0.10"
}

# Cabeçalhos da requisição
headers = {
    'Content-Type': 'application/json'
}

# Enviar a requisição POST com os dados e cabeçalhos
response = requests.post(url, data=json.dumps(dados), headers=headers)

# Verificar a resposta do servidor
if response.status_code == 200:
    print('Requisição bem-sucedida!')
    print(response.json())  # Exibe o conteúdo da resposta em formato JSON
else:
    print(f'Erro: {response.status_code}')
    print(response.text)  # Exibe a resposta de erro do servidor
