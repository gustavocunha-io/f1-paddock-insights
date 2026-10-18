from flask import Flask, render_template, request
from scraping.extrator import *
from open_f1 import *
import json

app = Flask(__name__)

@app.route("/noticias", methods=["GET"])
def exibir_noticias():
    pass

@app.route("/classificacao", methods=["GET"])
def exibir_classificacao():
    classificacao = obter_classificacao_pilotos()
    classificacao_json = []

    for piloto in classificacao.get_pilotos_list():
        piloto_json = {
            "posicao": piloto.colocacao,
            "nome": piloto.nome,
            "pais": piloto.pais,
            "equipe": piloto.equipe,
            "pontos": piloto.pontos
        }

        if piloto_json:
            classificacao_json.append(piloto_json)

    return render_template(
        "classificacao.html",
        classificacao=classificacao_json
    )

@app.route("/exibir", methods=["POST"])
def exibir_dados():
    nome_piloto = request.form.get("piloto")
    tom_analise = request.form.get("analise")
    piloto_json = obter_dados_piloto(nome_piloto) if nome_piloto and tom_analise else None

    return render_template(
        "exibir.html",
        piloto=piloto_json
    )

@app.route("/", methods=["GET", "POST"])
def paddock():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)