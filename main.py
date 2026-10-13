from scraping.extrator import *
import requests
from flask import Flask

DOMINIO:str = "https://grandepremio.com"
URL:str = f"{DOMINIO}/br/f1/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

app = Flask(__name__)

@app.route("/classificacao")
def exibir_classificacao():
    pass

def obter_conteudo_pagina(url:str, headers):
    return requests.get(url, headers=headers).text

if __name__ == "__main__":
    conteudo_html = obter_conteudo_pagina(URL, HEADERS)
    obter_tabela_classificao(conteudo_html)