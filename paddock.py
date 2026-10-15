from scraping.extrator import *
from flask import Flask
import json

app = Flask(__name__)

@app.route("/classificacao", methods=["GET"])
def exibir_classificacao():
    classificacao = obter_classificacao_pilotos()
    classificacao_json = []

    for piloto in classificacao.get_pilotos_list():
        piloto_json = {
            "colocação": piloto.colocacao,
            "nome": piloto.nome,
            "país": piloto.pais,
            "equipe": piloto.equipe,
            "pontos": piloto.pontos
        }

        if piloto_json:
            classificacao_json.append(piloto_json)
    return json.dumps(classificacao_json, indent=4, ensure_ascii=False)
    
if __name__ == "__main__":
    app.run(debug=True)