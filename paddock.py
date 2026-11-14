from flask import Flask, render_template, request, redirect, send_from_directory, render_template_string, session
from scraping import extrator as Extrator
from api import open_f1 as OpenF1
from api import gemini as Gemini
import markdown
import os

app = Flask(__name__)
app.secret_key = "f1_paddock_session_key_2026"

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

# Constantes do cálculo matemático de encerramento da temporada F1
CORRIDAS_RESTANTES_TEMPORADA = 3  # Corridas finais da temporada oficial (ex: Las Vegas, Catar e Abu Dhabi)
PONTOS_MAXIMOS_POR_GP = 26        # 25 pontos de vitória + 1 ponto de volta mais rápida por etapa

def calcular_indicadores_telemetria(piloto_json: dict, classificacao, corridas_restantes: int = CORRIDAS_RESTANTES_TEMPORADA) -> dict:
    """
    Calcula automaticamente os indicadores de telemetria e probabilidade matemática
    de título mundial, analisando os pontos restantes em disputa na temporada.
    
    Regra Matemática da F1:
    - Cada corrida distribui até 26 pontos máximos (25 de vitória + 1 de volta mais rápida).
    - Se a vantagem do líder (1º) sobre o vice (2º) for maior que os pontos restantes em disputa
      (corridas_restantes * 26), o líder é matematicamente campeão antecipado (100%),
      e todos os outros competidores estão matematicamente eliminados do título (0%).
    - Se a disputa ainda estiver aberta, calcula a probabilidade proporcional à pontuação.
    """
    nome_busca = (piloto_json.get("nome_completo") or "").lower()
    colocacao_encontrada = None
    pontos_encontrados = 0

    pilotos_grid = classificacao.get_pilotos_list() if classificacao else []

    try:
        for p in pilotos_grid:
            if p.nome.lower() in nome_busca or any(parte in p.nome.lower() for parte in nome_busca.split()):
                colocacao_encontrada = p.colocacao
                pontos_encontrados = p.pontos
                break
    except Exception:
        pass

    # Extrai o líder e o vice-líder para o cálculo matemático
    lider = pilotos_grid[0] if len(pilotos_grid) > 0 else None
    vice = pilotos_grid[1] if len(pilotos_grid) > 1 else None

    pontos_lider = lider.pontos if lider else 0
    pontos_vice = vice.pontos if vice else 0
    pontos_maximos_em_disputa = max(0, corridas_restantes * PONTOS_MAXIMOS_POR_GP)

    # Análise matemática: a vantagem do líder já é inalcançável?
    vantagem_lider = pontos_lider - pontos_vice
    campeao_matematico_definido = (vantagem_lider > pontos_maximos_em_disputa) and (pontos_lider > 0)

    if colocacao_encontrada == 1:
        if campeao_matematico_definido:
            chance_vitoria = 100
            nivel_alerta = "baixo"
            alerta_label = "CAMPEÃO MATEMÁTICO // TÍTULO ANTECIPADO"
            descricao_chance = (
                f"Matematicamente Campeão Mundial! Com {pontos_lider} pts contra {pontos_vice} pts do vice-líder, "
                f"a vantagem de {vantagem_lider} pts é superior aos {pontos_maximos_em_disputa} pts restantes em disputa "
                f"({corridas_restantes} GPs restantes)."
            )
        else:
            # Caso o campeonato ainda estivesse aberto matematicamente
            chance_vitoria = min(95, max(60, int(50 + (vantagem_lider / max(1, pontos_maximos_em_disputa)) * 45)))
            nivel_alerta = "baixo"
            alerta_label = "LÍDER DO MUNDIAL // DISPUTA PELO TÍTULO"
            descricao_chance = (
                f"Líder com vantagem de {vantagem_lider} pts. Ainda restam {pontos_maximos_em_disputa} pts em disputa "
                f"({corridas_restantes} corridas restantes)."
            )
    elif colocacao_encontrada and colocacao_encontrada > 1:
        # Pontuação máxima que este piloto ainda poderia somar se vencesse todas as etapas restantes
        pontos_maximos_possiveis = pontos_encontrados + pontos_maximos_em_disputa

        if campeao_matematico_definido or pontos_maximos_possiveis < pontos_lider:
            # Matematicamente eliminado da disputa pelo título mundial
            chance_vitoria = 0
            if colocacao_encontrada == 2:
                nivel_alerta = "baixo"
                alerta_label = "VICE-LÍDER // TÍTULO MATEMATICAMENTE FINALIZADO"
                descricao_chance = (
                    f"Matematicamente sem chances de título. Máximo alcançável: {pontos_maximos_possiveis} pts "
                    f"(Líder já possui {pontos_lider} pts em {corridas_restantes} corridas restantes)."
                )
            elif colocacao_encontrada <= 3:
                nivel_alerta = "medio"
                alerta_label = f"PÓDIO DO MUNDIAL ({colocacao_encontrada}º) // TÍTULO INALCANÇÁVEL"
                descricao_chance = (
                    f"Título matematicamente fora de alcance (máx. {pontos_maximos_possiveis} pts vs {pontos_lider} pts do líder). "
                    f"Disputa focada nas posições do pódio geral."
                )
            elif colocacao_encontrada <= 10:
                nivel_alerta = "medio"
                alerta_label = f"TOP {colocacao_encontrada} DO MUNDIAL // DISPUTA POR PONTOS"
                descricao_chance = (
                    f"Sem chance matemática de título mundial (máx. {pontos_maximos_possiveis} pts). Foco na zona de pontuação."
                )
            else:
                nivel_alerta = "alto"
                alerta_label = f"{colocacao_encontrada}º NO MUNDIAL // GRID GERAL"
                descricao_chance = f"Sem chance matemática de título mundial (máximo de {pontos_maximos_possiveis} pts)."
        else:
            # Ainda teria chances matemáticas de título
            deficit = pontos_lider - pontos_encontrados
            chance_vitoria = max(5, int((1 - (deficit / max(1, pontos_maximos_em_disputa))) * 40))
            nivel_alerta = "medio"
            alerta_label = f"DISPUTA MATEMÁTICA // {colocacao_encontrada}º LUGAR"
            descricao_chance = (
                f"Ainda com chances matemáticas de título! Máximo alcançável: {pontos_maximos_possiveis} pts "
                f"contra {pontos_lider} pts do líder ({corridas_restantes} GPs restantes)."
            )
    else:
        chance_vitoria = 0
        nivel_alerta = "medio"
        alerta_label = "GRID OFICIAL // TELEMETRIA PADRÃO"
        descricao_chance = "Piloto fora da zona de pontuação principal do mundial."

    return {
        "posicao": colocacao_encontrada or "N/D",
        "pontos": pontos_encontrados,
        "chance_vitoria": chance_vitoria,
        "nivel_alerta": nivel_alerta,
        "alerta_label": alerta_label,
        "descricao_chance": descricao_chance,
        "corridas_restantes": corridas_restantes,
        "pontos_em_disputa": pontos_maximos_em_disputa,
        "campeao_matematico": campeao_matematico_definido
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
    api_keys: str = (request.form.get("api-keys") or request.form.get("api-key") or "").strip()

    # Se novas chaves foram enviadas, armazena na sessão do usuário
    if api_keys:
        session["api_keys"] = api_keys
    else:
        # Se veio vazio (ex: clique no botão da classificação), resgata da sessão
        api_keys = session.get("api_keys", "")

    piloto_json: dict = OpenF1.obter_dados_piloto(nome_piloto) or None

    if piloto_json is not None:
        noticias_list: list = obter_noticias_piloto(nome_piloto)
        classificacao = Extrator.obter_classificacao()
        indicadores = calcular_indicadores_telemetria(piloto_json, classificacao)

        prompt = Gemini.gerar_prompt(piloto_json, classificacao, tom_analise, noticias_list)
        texto_gemini = Gemini.obter_reposta_gemini(prompt, chaves_input=api_keys)
        texto_html = markdown.markdown(texto_gemini)

        return render_template(
            "exibir.html",
            piloto=piloto_json,
            analise=texto_html,
            tom=tom_analise,
            noticias=noticias_list,
            indicadores=indicadores,
            api_keys=api_keys
        )
    else:
        return render_template(
            "exibir.html",
            piloto=None,
            erro=f"O piloto '{nome_piloto}' não foi encontrado nos registros oficiais da F1. Tente buscar pelo sobrenome (ex: Verstappen, Hamilton, Norris, Leclerc).",
            termo_busca=nome_piloto,
            api_keys=api_keys
        )

@app.route("/", methods=["GET", "POST"])
def paddock():
    return render_template("index.html")

@app.route("/limpar-chaves", methods=["POST"])
def limpar_chaves():
    session.pop("api_keys", None)
    Gemini.limpar_pool_chaves()
    return {"status": "ok", "mensagem": "Chaves removidas com sucesso"}

@app.route("/docs")
def exibir_docs_redirect():
    return redirect("/docs/")

@app.route("/docs/")
def exibir_docs_page():
    docs_file = os.path.join(app.root_path, "docs", "index.html")
    with open(docs_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    html_content = html_content.replace("url_for('../static'", "url_for('static'")
    return render_template_string(html_content)

@app.route("/docs/<path:filename>")
def exibir_docs_assets(filename):
    docs_dir = os.path.join(app.root_path, "docs")
    return send_from_directory(docs_dir, filename)

@app.route("/assets/<path:filename>")
def exibir_assets_fallback(filename):
    return send_from_directory(os.path.join(app.root_path, "docs", "assets"), filename)

@app.route("/js/<path:filename>")
def exibir_js_fallback(filename):
    return send_from_directory(os.path.join(app.root_path, "docs", "js"), filename)

@app.route("/css/<path:filename>")
def exibir_css_fallback(filename):
    return send_from_directory(os.path.join(app.root_path, "docs", "css"), filename)

if __name__ == "__main__":
    app.run(debug=True)
