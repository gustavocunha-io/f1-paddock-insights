from scraping.models.classificacao_pilotos import *
from scraping.models.piloto import Piloto
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

API_KEY_GEMINI = os.getenv("API_KEY_GEMINI", "")

def gerar_prompt(piloto_json:dict, classificacao:ClassificacaoPilotos, tom_analise:str, noticias_list:list) -> str:
    prompt = [
        f"Gere uma análise com tom \"{tom_analise}\" de acordo com os seguintes dados de piloto de Fôrmula 1:\n\n"
        f"- Nome: {piloto_json["nome_completo"]}\n"\
        f"- Equipe: {piloto_json["equipe"]}\n"\
        f"- Número: {piloto_json["numero"]}\n"
        f"- Pais: {piloto_json["codigo_pais"]}\n"\
        "\nA colocação deve ser um ponto relevante na análise. Utilize a tabela geral do campeonato abaixo onde"\
        "consta a posição desse piloto.\n\nColocação  | \t\t   Nome  \t\t |  Pontos\n"
    ]

    pilotos_list:list[Piloto] = classificacao.get_pilotos_list()

    for piloto in pilotos_list:
        prompt.append(f"{piloto.colocacao:<10} | {f'{piloto.nome}':<35} |  {f'{piloto.pontos:<4}'} pts\n")

    prompt.append("\nLeve em consideração também as últimas notícias sobre o piloto abaixo se as mesmas existirem:\n\n")
    
    for noticia in noticias_list:
        prompt.append(f"- {noticia}\n\n")

    prompt.append(
        "Por fim, deve-se ser feito uma brincadeira independente da colocação do piloto no campeonato, ou seja," \
        "se o piloto estiver em uma boa, elogie-o, caso contrário, zoe-o, leve em consideração também o carro," \
        "por exemplo, pilotos que estão nas ultimas colocações pode-se dizer que estão pilotando carroças."
    )

    return "".join(prompt)

def obter_reposta_gemini(prompt) -> str:
    if prompt:
        cliente = genai.Client(api_key=API_KEY_GEMINI)
        response = cliente.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text
    return ""

# piloto_json = {
#     "nome_completo": "Verstappen",
#     "equipe": "Red Bull Racing",
#     "numero": "3",
#     "codigo_pais": "NED",
# }

# classificacao = ClassificacaoPilotos("Campeonato 2026 - F1")
# classificacao.inserir_piloto(Piloto("Verstappen", "Holanda", "Red Bull Racing", 198, 3))
# classificacao.inserir_piloto(Piloto("Kimi Antonelli", "Arábia Saudita", "Red Bull Racing", 198, 1))

# prompt = gerar_prompt(piloto_json, classificacao, "Narrador emotivo", ["Mais uma vitória", "Derrota em casa"])
# print(obter_reposta_gemini(prompt))