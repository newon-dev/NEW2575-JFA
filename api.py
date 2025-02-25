from flask import Flask, request, jsonify, Response
from db import (
    BancoDeDados,
)
from flask_cors import CORS
from db import BancoDeDados
from rfid import RF600XML
import csv
import io

app = Flask(__name__)
CORS(app)

online_antenas = [False, False]
try:
    db = BancoDeDados("movimentacao.db")
except Exception as e:
    print(e)


@app.route("/ultima_posicao", methods=["POST"])
def ultima_posicao():
    try:
        dados = request.get_json()
        numero_ponte = dados.get("ponte")

        if not numero_ponte:
            return jsonify({"erro": "Número da ponte é obrigatório."}), 400
        db = BancoDeDados("movimentacao.db")
        resultado = db.obter_ultima_posicao(numero_ponte)
        db.fechar_conexao()
        if resultado:
            x, y, horario = resultado
            resposta = {"x": x, "y": y, "horario": horario}
            return jsonify(resposta)
        else:
            return (
                jsonify(
                    {"erro": "Nenhuma movimentação encontrada para a ponte fornecida."}
                ),
                404,
            )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data or "accessCode" not in data:
            return jsonify({"erro": 'Parâmetro "accessCode" ausente no JSON.'}), 400
        access_code = data["accessCode"]
        if access_code == "1234":
            return jsonify({"return": True})
        else:
            return jsonify({"return": False})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/check_antena", methods=["GET", "POST"])
def check_antena():
    result = db.recuperar_antenas()
    if result:
        antenas = []
        for antena in result:
            ip = antena[2]
            nome = antena[1]
            print(RF600XML.ping_antenna(ip))
            if RF600XML.ping_antenna(ip):
                antenas.append({"nome": nome, "ip": ip})
        return jsonify(antenas)
    else:
        return jsonify([])


@app.route("/recuperar_antenas", methods=["GET", "POST"])
def recuperar_antenas():
    result = db.recuperar_antenas()
    if result:
        antenas = []
        for antena in result:
            antenas.append({"id": antena[0], "nome": antena[1], "ip": antena[2]})
        return jsonify(antenas)
    else:
        return jsonify([])


@app.route("/modificar_antenas", methods=["POST"])
def modificar_antenas():
    try:
        dados = request.get_json()
        if not dados or not all(key in dados for key in ["id", "nome", "ip"]):
            return (
                jsonify(
                    {"erro": 'Os parâmetros "id", "nome" e "ip" são obrigatórios.'}
                ),
                400,
            )
        id_antena = dados["id"]
        nome_antena = dados["nome"]
        ip_antena = dados["ip"]
        sucesso = db.update_antenas(id_antena, nome_antena, ip_antena)

        if sucesso:
            return jsonify({"success": "true"})
        else:
            return (
                jsonify(
                    {"success": "false", "erro": "Não foi possível atualizar a antena."}
                ),
                500,
            )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/recuperar_posicoes", methods=["GET", "POST"])
def recuperar_posicoes():
    result = db.recuperar_posicoes()
    if result:
        posicoes = []
        for posicao in result:
            posicoes.append(
                {
                    "id": posicao[0],
                    "color": posicao[1],
                    "name": posicao[2],
                    "x": posicao[3],
                    "y": posicao[4],
                }
            )
        return jsonify(posicoes)
    else:
        return jsonify([])


@app.route("/modificar_posicoes", methods=["POST"])
def modificar_posicoes():
    try:
        dados = request.get_json()
        print(dados)
        if not dados or not all(key in dados for key in ["x", "y", "cor", "nome"]):
            return (
                jsonify(
                    {"erro": 'Os parâmetros "x","y" , "nome" e "ip" são obrigatórios.'}
                ),
                400,
            )
        x = dados["x"]
        y = dados["y"]
        nome = dados["nome"]
        cor = dados["cor"]
        sucesso = db.atualizar_mapa_posicoes(cor, nome, str(x), str(y))
        if sucesso:
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 500})
    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500


@app.route("/recuperar_logs", methods=["GET", "POST"])
def obter_logs():
    result = db.obter_logs()
    if result:
        logs = []
        for posicao in result:
            logs.append(
                {
                    "id": posicao["id"],
                    "ponte": posicao["ponte"],
                    "posicao": posicao["posicao"],
                    "hora": posicao["hora"],
                }
            )
        return jsonify(logs)
    else:
        return jsonify([])


@app.route("/download_csv", methods=["GET", "POST"])
def download_logs():
    limite = request.args.get("limite", default=50, type=int)
    logs = db.baixar_csv(limite)
    if not logs:
        return "Nenhum log encontrado", 404
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "x", "y", "ponte", "hora"])
    writer.writeheader()
    writer.writerows(logs)
    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=logs_{limite}_registros.csv"
        },
    )


@app.route("/recuperar_baias", methods=["GET", "POST"])
def recuperar_baias():
    result = db.recuperar_baias()
    if result:
        baias = []
        for baia in result:
            baias.append(
                {
                    "x": baia["x"],
                    "y": baia["y"],
                    "tagx1": baia["tagx1"],
                    "tagx2": baia["tagx2"],
                    "tagy1": baia["tagy1"],
                    "tagy2": baia["tagy2"],
                    "tagy3": baia["tagy3"],
                    "tagy4": baia["tagy4"],
                }
            )
        return jsonify(baias)
    else:
        return jsonify([])


@app.route("/modificar_baias", methods=["POST"])
def modificar_baias():
    try:
        dados = request.get_json()
        if not dados or not all(key in dados for key in ["tagAntiga", "tagNova"]):
            return (
                jsonify(
                    {"erro": 'Os parâmetros "tagAntiga", "tagNova" são obrigatórios.'}
                ),
                400,
            )
        tagAntiga = dados["tagAntiga"]
        tagNova = dados["tagNova"]
        sucesso = db.atualizar_tag(tagAntiga, tagNova)

        if sucesso:
            return jsonify({"success": "true"})
        else:
            return (
                jsonify(
                    {"success": "false", "erro": "Não foi possível atualizar a antena."}
                ),
                500,
            )
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
