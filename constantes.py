# Domínio do site escolhido.
DOMINIO:str = "https://grandepremio.com"

# URL da página de notícias da F1.
URL_F1:str = f"{DOMINIO}/br/f1/"

# URL da pagina de classificacao dos pilotos.
URL_CLASSIFICACAO:str = f"{URL_F1}classificacao/2026/pilotos/"

# Definição de um navegador real para evitar bloqueios.
HEADERS = {'User-Agent': 'Mozilla/5.0'}