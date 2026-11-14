import re
from google import genai
from scraping.models.classificacao_pilotos import *
from scraping.models.piloto import Piloto

# Contador global para distribuição equitativa de requisições (Round-Robin)
_indice_rodizio: int = 0

# Pool mantido em memória durante a execução para que as chaves persistam
# mesmo após a primeira inserção ou quando o usuário analisa pilotos pela classificação
_pool_chaves_em_memoria: list[str] = []

def extrair_pool_chaves(chaves_input: str = "") -> list[str]:
    """
    Extrai a lista de chaves a partir da entrada fornecida pelo usuário.
    Se a entrada contiver novas chaves, o pool em memória é atualizado.
    Se a entrada vier vazia, reutiliza o pool ativo mantido em memória
    desde a primeira inserção (permitindo que o usuário navegue pela classificação
    ou envie campos vazios mantendo as chaves e o rodízio ativos).
    """
    global _pool_chaves_em_memoria
    if chaves_input and chaves_input.strip():
        chaves = [k.strip() for k in re.split(r'[,;\n\r\t]+', chaves_input) if k.strip()]
        if chaves:
            _pool_chaves_em_memoria = chaves
            return _pool_chaves_em_memoria

    # Reutiliza o pool previamente registrado na memória
    return _pool_chaves_em_memoria

def limpar_pool_chaves() -> None:
    """Limpa o pool de chaves em memória."""
    global _pool_chaves_em_memoria, _indice_rodizio
    _pool_chaves_em_memoria = []
    _indice_rodizio = 0

def mascarar_chave(chave: str) -> str:
    """Mascara a chave para exibição segura (ex: AIzaSy...oPnY)."""
    if len(chave) > 10:
        return f"{chave[:6]}...{chave[-4:]}"
    return "***"

def gerar_prompt(piloto_json: dict, classificacao: ClassificacaoPilotos, tom_analise: str, noticias_list: list) -> str:
    prompt = [
        f"Gere uma análise com tom \"{tom_analise}\" de acordo com os seguintes dados de piloto de Fôrmula 1:\n\n"
        f"- Nome: {piloto_json['nome_completo']}\n"\
        f"- Equipe: {piloto_json['equipe']}\n"\
        f"- Número: {piloto_json['numero']}\n"
        f"- Pais: {piloto_json['codigo_pais']}\n"\
        "\nA colocação deve ser um ponto relevante na análise. Utilize a tabela geral do campeonato abaixo onde"\
        "consta a posição desse piloto.\n\nColocação  | \t\t   Nome  \t\t |  Pontos\n"
    ]

    pilotos_list: list[Piloto] = classificacao.get_pilotos_list()

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

def obter_reposta_gemini(prompt: str, chaves_input: str = "") -> str:
    """
    Processa a requisição com a IA Google Gemini utilizando:
    - Chave inserida pelo usuário no formulário da interface.
    - Rodízio automático de chaves (Round-Robin) entre as chaves cadastradas.
    - Fallback imediato: se uma chave falhar (ex: cota esgotada), tenta a próxima do pool.
    """
    global _indice_rodizio

    if not prompt:
        return ""

    pool_chaves = extrair_pool_chaves(chaves_input)

    if not pool_chaves:
        return (
            "⚠️ **Chave de API do Google Gemini não fornecida!**\n\n"
            "Por favor, insira sua chave da API no campo de entrada da tela inicial.\n\n"
            "💡 *Dica de Rodízio:* Você pode inserir **múltiplas chaves separadas por vírgula** no input "
            "para ativar o balanceamento e evitar o esgotamento de cotas."
        )

    total_chaves = len(pool_chaves)
    start_idx = _indice_rodizio % total_chaves
    _indice_rodizio = (_indice_rodizio + 1) % total_chaves

    erros = []

    # Tentativas iterativas com rotação e fallback
    for tentativa in range(total_chaves):
        idx_atual = (start_idx + tentativa) % total_chaves
        chave_atual = pool_chaves[idx_atual]
        chave_mascarada = mascarar_chave(chave_atual)

        try:
            cliente = genai.Client(api_key=chave_atual)
            response = cliente.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            texto = response.text or ""

            # Adiciona nota informativa de rodízio quando houver pool múltiplo ou ativo
            if total_chaves > 1:
                nota_rodizio = (
                    f"\n\n---\n"
                    f"🔄 **Rodízio de Chaves Ativo:** Requisição atendida com sucesso pela chave "
                    f"**#{idx_atual + 1}** (`{chave_mascarada}`) de um total de **{total_chaves}** chaves cadastradas."
                )
                texto += nota_rodizio

            return texto

        except Exception as e:
            erros.append(f"Chave #{idx_atual + 1} ({chave_mascarada}): {e}")

    # Todas as chaves falharam
    detalhes = "\n".join(f"- {err}" for err in erros)
    return (
        f"❌ **Falha na comunicação com o Google Gemini após tentar todas as chaves ({total_chaves} chave(s)):**\n\n"
        f"{detalhes}\n\n"
        f"👉 Verifique se as chaves fornecidas no input são válidas e se possuem cota disponível."
    )
