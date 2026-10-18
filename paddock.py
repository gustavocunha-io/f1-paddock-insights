from flask import Flask, render_template, request
from scraping.extrator import *
from open_f1 import *
import json

app = Flask(__name__)

@app.route("/noticias", methods=["POST"])
def exibir_noticias():
    try:
        nome_piloto = request.form.get("nome-piloto")
        noticias_list = obter_noticias(nome_piloto)

        if noticias_list is None:
            noticias_list = []

    except Exception as exeption:
        print(f"Erro: {exeption}")
        noticias_list = []

    return render_template("noticias.html", noticias=noticias_list)

@app.route("/classificacao", methods=["GET"])
def exibir_classificacao():
    classificacao = obter_classificacao_pilotos()
    classificacao_list = []

    for piloto in classificacao.get_pilotos_list():
        piloto_dict = {
            "posicao": piloto.colocacao,
            "nome": piloto.nome,
            "pais": piloto.pais,
            "equipe": piloto.equipe,
            "pontos": piloto.pontos
        }

        if piloto_dict:
            classificacao_list.append(piloto_dict)

    return render_template("classificacao.html", classificacao=classificacao_list)

@app.route("/exibir", methods=["POST"])
def exibir_dados():
    nome_piloto = request.form.get("nome-piloto")
    tom_analise = request.form.get("analise")
    piloto_json = obter_dados_piloto(nome_piloto) if nome_piloto and tom_analise else None

    return render_template("exibir.html", piloto=piloto_json)

@app.route("/", methods=["GET", "POST"])
def paddock():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)