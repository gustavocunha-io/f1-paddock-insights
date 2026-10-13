from bs4 import BeautifulSoup
from bs4.element import Tag
from scraping.modelos import *

URL_CLASSIFICACAO = ""

def obter_nome_piloto(conteudo_soup:Tag):
    tag_nome_piloto:Tag = conteudo_soup.find("span", class_="truncate")

    if tag_nome_piloto:
        return tag_nome_piloto.text.strip()
    return ""

def obter_estatisticas_tabela(conteudo_soup:Tag):
    linha_pilotos = conteudo_soup.find_all("tr")
    nomes_pilotos_list = []

    for linha in linha_pilotos:
        nome_piloto = obter_nome_piloto(linha)

        if nome_piloto:
            nomes_pilotos_list.append(nome_piloto)

    print(nomes_pilotos_list)

def obter_tabela_classificao(conteudo_html:str):

    #classificacao:Classificacao = Classificacao(titulo="Fórmula 1 - Pilotos")
    soup = BeautifulSoup(conteudo_html, 'html.parser')
    container = soup.find("div", id="gpch-1-tabs")
    tabela = container.find("table")
    obter_estatisticas_tabela(tabela)

    #print(tabela)