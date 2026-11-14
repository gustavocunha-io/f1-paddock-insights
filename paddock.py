from flask import Flask, render_template, request, redirect
from scraping import extrator as Extrator
from api import open_f1 as OpenF1
from api import gemini as Gemini
import markdown

app = Flask(__name__)

def obter_noticias_piloto(nome_piloto) -> list:
    try:
        noticias_list = Extrator.obter_noticias(nome_piloto)

        if noticias_list is None:
            noticias_list = []

    except Exception as exeption:
        print(f"Erro ao obter notícias: {exeption}")
        noticias_list = []

    return noticias_list

def obter_classificacao_pilotos() -> list:
    classificacao = Extrator.obter_classificacao()
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
            
    return classificacao_list

def calcular_indicadores_telemetria(piloto_json: dict, classificacao) -> dict:
    """
    Calcula os indicadores visuais para a interface gráfica Mobile-First
    (Chance de vitória percentual, Nível de alerta dinâmico e posição no grid).
    """
    nome_busca = (piloto_json.get("nome_completo") or "").lower()
    colocacao_encontrada = None
    pontos_encontrados = 0

    try:
        for p in classificacao.get_pilotos_list():
            if p.nome.lower() in nome_busca or any(parte in p.nome.lower() for parte in nome_busca.split()):
                colocacao_encontrada = p.colocacao
                pontos_encontrados = p.pontos
                break
    except Exception:
        pass

    if colocacao_encontrada == 1:
        chance_vitoria = 89
        nivel_alerta = "baixo"
        alerta_label = "ALERTA BAIXO // RITMO DE LÍDER"
    elif colocacao_encontrada and colocacao_encontrada <= 3:
        chance_vitoria = 76
        nivel_alerta = "baixo"
        alerta_label = "ALERTA BAIXO // BRIGA POR VITÓRIA"
    elif colocacao_encontrada and colocacao_encontrada <= 6:
        chance_vitoria = 60
        nivel_alerta = "medio"
        alerta_label = "ALERTA MÉDIO // ZONA DE PÓDIO"
    elif colocacao_encontrada and colocacao_encontrada <= 10:
        chance_vitoria = 42
        nivel_alerta = "medio"
        alerta_label = "ALERTA MÉDIO // DISPUTA POR PONTOS"
    elif colocacao_encontrada:
        chance_vitoria = max(10, 36 - (colocacao_encontrada * 2))
        nivel_alerta = "alto"
        alerta_label = "ALERTA ALTO // RISCO DE GRID"
    else:
        chance_vitoria = 50
        nivel_alerta = "medio"
        alerta_label = "ALERTA MÉDIO // TELEMETRIA PADRÃO"

    return {
        "posicao": colocacao_encontrada or "N/D",
        "pontos": pontos_encontrados,
        "chance_vitoria": chance_vitoria,
        "nivel_alerta": nivel_alerta,
        "alerta_label": alerta_label
    }

@app.route("/classificacao", methods=["GET"])
def exibir_classificacao():
    return render_template("classificacao.html", classificacao=obter_classificacao_pilotos())

@app.route("/dados", methods=["GET", "POST"])
def exibir_dados():
    if request.method == "GET":
        return redirect("/")

    nome_piloto: str = (request.form.get("nome-piloto") or "").strip()
    tom_analise: str = (request.form.get("analise") or "engenheiro de pista serio").strip()
    piloto_json: dict = OpenF1.obter_dados_piloto(nome_piloto) or None

    if piloto_json is not None:
        noticias_list: list = obter_noticias_piloto(nome_piloto)
        classificacao = Extrator.obter_classificacao()
        indicadores = calcular_indicadores_telemetria(piloto_json, classificacao)

        prompt = Gemini.gerar_prompt(piloto_json, classificacao, tom_analise, noticias_list)
        texto_gemini = Gemini.obter_reposta_gemini(prompt)
        texto_html = markdown.markdown(texto_gemini)

        return render_template(
            "exibir.html",
            piloto=piloto_json,
            analise=texto_html,
            tom=tom_analise,
            noticias=noticias_list,
            indicadores=indicadores
        )
    else:
        return render_template(
            "exibir.html",
            piloto=None,
            erro=f"O piloto '{nome_piloto}' não foi encontrado nos registros oficiais da F1. Tente buscar pelo sobrenome (ex: Verstappen, Hamilton, Norris, Leclerc).",
            termo_busca=nome_piloto
        )

@app.route("/", methods=["GET", "POST"])
def paddock():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
