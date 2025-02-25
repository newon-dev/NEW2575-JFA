import requests
import json

# URL do servidor que está rodando o Flask
url = 'http://localhost:8080/modificar_baias'  # Atualize conforme a URL e porta do seu servidor

# Dados a serem enviados no corpo da requisição
dados = {
    'tagAntiga': 'Victor',
    'tagNova': 'Funcionou'
}

# Cabeçalhos para indicar que o corpo é em JSON
headers = {'Content-Type': 'application/json'}

# Enviando a requisição POST
response = requests.post(url, data=json.dumps(dados), headers=headers)

# Verificando a resposta
if response.status_code == 200:
    print("Resposta do servidor:", response.json())
else:
    print(f"Erro {response.status_code}: {response.json()}")
