import requests

URL = "https://api.openf1.org/v1/drivers"

def obter_dados_piloto(nome_piloto:str):
    nome_partes = nome_piloto.strip().split()
    sobrenome = nome_partes[-1]
    
    response = requests.get(URL, params={"last_name": sobrenome})
    data = response.json()

    if not data and len(nome_partes) > 0:
        nome = nome_partes[0]
        response = requests.get(URL, params={"first_name": nome})
        data = response.json()

    dados_piloto_json = data[-1]
    
    return  {
        "foto_url": dados_piloto_json["headshot_url"],
        "cor_equipe": dados_piloto_json["team_colour"],
        "equipe": dados_piloto_json["team_name"]
    }