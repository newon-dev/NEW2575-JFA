import requests
import json

# URL do servidor Flask
url = "http://127.0.0.1:8080/ultima_posicao"

# Dados a serem enviados na requisição
dados = {"ponte": 1}

# Cabeçalhos (definindo que os dados são JSON)
headers = {"Content-Type": "application/json"}

# Enviar a requisição POST
response = requests.post(url, json=dados, headers=headers)

# Verificar a resposta
if response.status_code == 200:
    print("Requisição bem-sucedida:", response.json())
else:
    print(f"Erro {response.status_code}:", response.json())
