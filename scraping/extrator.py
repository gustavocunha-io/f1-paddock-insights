from scraping.models.classificacao_pilotos import ClassificacaoPilotos
from scraping.models.piloto import Piloto
from bs4 import BeautifulSoup
from datetime import datetime
from constantes import *
import requests
import time
import re

def obter_conteudo_pagina(url:str, headers) -> str:
    return requests.get(url, headers=headers).text

def obter_noticias(nome_piloto:str):
    """
        Busca todas as notícias de acordo com o nome do piloto e retorna uma lista de dicionários
        que contêm dados como título e o conteúdo.
    """
    
    conteudo_pagina:str = obter_conteudo_pagina(URL_F1, HEADERS)
    soup:BeautifulSoup = BeautifulSoup(conteudo_pagina, "html.parser")
    div_noticias = soup.find(class_= re.compile(r"mt-\d+ wp-block-grande-premio-news-grid"))
    article_noticias = div_noticias.select("article a")[:10]
    noticias_piloto_list = []

    for noticia in article_noticias:
        link = noticia.get("href")

        if nome_piloto.lower() in link:
            time.sleep(2) # Evitar bloqueios por DDOS
            noticias_piloto_list.append(obter_conteudo_interno(link))

    print(len(noticias_piloto_list))

    return noticias_piloto_list

def obter_conteudo_interno(url):
    """ 
        Obtêm o conteúdo da página passada por parâmetro, realiza a raspagem e retorna um
        dicionário contendo as informações da noticia como o título e o conteúdo da mesma.
    """
    conteudo_interno_pagina:str = obter_conteudo_pagina(url, HEADERS)
    soup:BeautifulSoup = BeautifulSoup(conteudo_interno_pagina, "html.parser")

    materia = soup.find(class_="materia")
    
    cabecalho = materia.find("header")
    tag_titulo = cabecalho.find("h1")
    titulo = tag_titulo.text.strip()
    
    conteudo_bruto = soup.find("article")
    paragrafos_conteudo = conteudo_bruto.find_all(class_="wp-block-paragraph")
    conteudo_limpo = [paragrafo.get_text(strip=True) for paragrafo in paragrafos_conteudo]
    conteudo_completo = "\n\n".join(conteudo_limpo)

    return {
        "titulo": titulo,
        "conteudo": conteudo_completo
    }

def obter_classificacao_pilotos() -> list[ClassificacaoPilotos]:
    """
        Obtêm os dados da classificação dos pilotos utilizando soup com expressão regular 
        para realizar a filtragem.
    """

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