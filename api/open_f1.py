import requests

URL = "https://api.openf1.org/v1/drivers"

def obter_dados_piloto(nome_piloto: str):
    termo_busca = nome_piloto.strip().upper()

    if not termo_busca:
        return None
        
    try:
        response = requests.get(URL, timeout=10)
        data = response.json()
    except Exception:
        return None

    if isinstance(data, dict) or not isinstance(data, list) or len(data) == 0:
        return None

    dados_piloto = None

    for piloto in reversed(data):
        last_name = (piloto.get("last_name") or "").upper()
        if termo_busca == last_name or termo_busca in last_name:
            dados_piloto = piloto
            break

    if not dados_piloto:
        for piloto in reversed(data):
            first_name = (piloto.get("first_name") or "").upper()
            if termo_busca == first_name or termo_busca in first_name:
                dados_piloto = piloto
                break

    if not dados_piloto:
        for piloto in reversed(data):
            full_name = (piloto.get("full_name") or "").upper()
            if termo_busca in full_name:
                dados_piloto = piloto
                break

    if not dados_piloto:
        return None

    return {
        "nome_completo": dados_piloto.get("full_name"),
        "equipe": dados_piloto.get("team_name"),
        "numero": dados_piloto.get("driver_number"),
        "codigo_pais": dados_piloto.get("country_code"),
        "foto_url": dados_piloto.get("headshot_url"),
        "cor_equipe": dados_piloto.get("team_colour"),
    }