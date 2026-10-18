from scraping.models.classificacao_pilotos import ClassificacaoPilotos
from scraping.models.piloto import Piloto
from bs4 import BeautifulSoup
from datetime import datetime
from constantes import *
import requests
import re

def obter_conteudo_pagina(url:str, headers) -> str:
    return requests.get(url, headers=headers).text

def obter_noticias():
    pass

# Obtêm os dados da classificação dos pilotos utilizando soup com expressão regular para realizar a filtragem.
def obter_classificacao_pilotos() -> list[ClassificacaoPilotos]:
    conteudo_pagina:str = obter_conteudo_pagina(URL_CLASSIFICACAO, HEADERS)
    soup:BeautifulSoup = BeautifulSoup(conteudo_pagina, "html.parser")
    tabela = soup.find(class_="gp-standings-page")

    ano_atual:int = datetime.now().year
    
    # Lógica para raspar e armazenar os dados dos 3 primeiros pilotos na classificação.
    div_lideres = tabela.find_all("div", style=re.compile(r"--tc:\s*#"))
    classificacao_pilotos:ClassificacaoPilotos = ClassificacaoPilotos(f"Classificação Fórmula 1 {ano_atual} - Pilotos")
   
    for dados_piloto in div_lideres:
        colocacao:int = int(dados_piloto.find("div").text.strip())
        nome:str = dados_piloto.find("div", class_=re.compile(r"text-\[\d+\.\d*px\]")).text.strip()
        div_equipe = list(dados_piloto.find("div", class_=re.compile(r"text-\[\d+\.*\d*px\] text-ms-muted mt-\[\d+\.*\d*px\]")).stripped_strings)
        pais:str = div_equipe[0]
        equipe:str = div_equipe[-1]
        pontos:int = int(list(dados_piloto.find("div", class_=re.compile(r"font-extrabold text-\[\d+\.*\d*px\] mt-\d+")))[-0].text)

        piloto = Piloto(nome, pais, equipe, pontos, colocacao)
        classificacao_pilotos.inserir_piloto(piloto)

    # Lógica para raspar e armazenar os dados dos pilotos restantes.
    div_tabela_geral = tabela.find("div", "gp-tablewrap overflow-x-auto")
    div_tabela_sem_cabecalho = div_tabela_geral.find("tbody")
    div_tabela_restante = div_tabela_sem_cabecalho.find_all("tr")

    for dados_piloto in div_tabela_restante:
        colocacao:int = int(dados_piloto.find("span", class_=re.compile(r"tabular-nums tracking-\[-.\d*\d+em\]")).text.strip())
        nome:str = dados_piloto.find("span", class_=re.compile(r"tracking-\[-.\d*\d+em\] truncate")).text.strip()
        span_pais_equipe = list(dados_piloto.find("span", class_=re.compile(r"gap-\d+\.*\d* whitespace-nowrap overflow-hidden")).stripped_strings)
        pais:str = span_pais_equipe[0]
        equipe:str = span_pais_equipe[-1]
        pontos:int = int(dados_piloto.find("b", class_=re.compile(r"text-\[\d+\d*px\] tracking-\[-.\d*\d+em\]")).text.strip())

        piloto:Piloto = Piloto(nome, pais, equipe, pontos, colocacao)
        classificacao_pilotos.inserir_piloto(piloto)
    
    return classificacao_pilotos