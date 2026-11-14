# 🏎️ F1 Paddock Insights

> **Sistema de Telemetria, Web Scraping e Estratégia de Corrida com Inteligência Artificial**  
> Trabalho Prático Individual da disciplina de **Web Services** &bull; Engenharia de Software  
> Autor: **Gustavo Cunha** ([@gustavocunha-io](https://github.com/gustavocunha-io))

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Showcase-e10600?style=for-the-badge&logo=github)](https://gustavocunha-io.github.io/f1-paddock-insights/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-00f0ff?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Mobile First](https://img.shields.io/badge/Design-Mobile%20First-00e676?style=for-the-badge)](https://gustavocunha-io.github.io/f1-paddock-insights/)

---

## 🌐 Site do Projeto no GitHub Pages

O site responsivo mobile-first apresentando o projeto completo, arquitetura, imagens e vídeo de demonstração está disponível em:

👉 **[https://gustavocunha-io.github.io/f1-paddock-insights/](https://gustavocunha-io.github.io/f1-paddock-insights/)**

---

## 📖 Visão Geral do Projeto

O **F1 Paddock Insights** é uma aplicação web mobile-first desenvolvida em Flask que unifica e orquestra 3 fontes distintas de dados e serviços web do automobilismo mundial em uma única interface inteligente de telemetria e estratégia:

1. **API REST Pública Oficial (OpenF1):** Extração de dados cadastrais de pilotos, número oficial no grid, código de país, cor hexadecimal da escuderia e foto oficial em alta definição.
2. **Web Scraping com BeautifulSoup (Portal Grande Prêmio):** Raspagem em tempo real de matérias e notícias dos bastidores sobre o piloto selecionado, além da extração automatizada da tabela oficial completa de classificação do campeonato mundial de pilotos.
3. **LLM Web Service (Google Gemini via `google-genai`):** Processamento inteligente de linguagem natural com engenharia de prompts dinâmicos para simular as comunicações de rádio do Pit Wall em três personalidades customizáveis (Engenheiro Sério, Narrador Emocionado ou Comentarista Corneta).

---

## 🏆 Temporada 2026 Concluída & Regra do Velocímetro

> **Atenção:** A temporada de 2026 foi finalizada e já temos um campeão mundial consagrado!

- **Campeão Mundial:** **Andrea Kimi Antonelli** (Mercedes-AMG Petronas F1 Team) com **390 pontos**.
- **Vice-campeão:** **Max Verstappen** (Red Bull Racing) com **279 pontos**.
- **Gráfico de Chance de Vitória Atualizado:**
  - **1º Colocado (Antonelli):** **100%** de chance confirmada (`CAMPEÃO CONFIRMADO // TÍTULO CONQUISTADO`).
  - **Demais Pilotos (colocação > 1):** **0%** de chance de título (`TEMPORADA CONCLUÍDA`).

---

## 🛠️ Arquitetura e Integração dos Web Services

```
+----------------------------------------------------------------------------------+
|                              CLIENTE MOBILE-FIRST                                |
|         (Navegador Smartphone / Tablet / Desktop - HTML5, CSS3 & JS)             |
+----------------------------------------------------------------------------------+
                                     │  ▲
              POST /dados (nome, tom) │  │  Renderização Jinja2 + Markdown
                                     ▼  │
+----------------------------------------------------------------------------------+
|                           BACKEND FLASK (paddock.py)                             |
|          - Router & Controller                                                   |
|          - Motor de Telemetria (calcular_indicadores_telemetria)                 |
|          - Agregador de Web Services                                             |
+----------------------------------------------------------------------------------+
            │                               │                               │
            ▼                               ▼                               ▼
+-----------------------+       +-----------------------+       +-----------------------+
|    OPENF1 REST API    |       |     WEB SCRAPING      |       |   GOOGLE GEMINI AI    |
| (api.openf1.org/v1)   |       |   (Grande Prêmio)     |       | (google-genai SDK)    |
| - Nome e país         |       | - Notícias do piloto  |       | - Prompt com dados    |
| - Escuderia e cor hex |       | - Tabela de pontos    |       | - 3 tons de rádio     |
| - Foto oficial        |       | - BeautifulSoup4 & Re |       | - Resposta Markdown   |
+-----------------------+       +-----------------------+       +-----------------------+
```

---

## 🎬 Vídeo de Demonstração

O site no GitHub Pages conta com um player de vídeo responsivo com capítulos navegáveis e modo de simulação interativa:

- **Local do arquivo de vídeo:** `docs/assets/videos/demo.mp4`
- **Poster de pré-visualização:** `docs/assets/images/demo-poster.svg`
- **Capítulos:**
  1. `00:00` - Interface Mobile-First & Painel do Paddock
  2. `00:35` - Busca & Integração com a API OpenF1
  3. `01:10` - Web Scraping de Notícias & Tabela no Grande Prêmio
  4. `01:50` - Rádio Pit Wall Descriptografado com Google Gemini
  5. `02:30` - Velocímetro: Andrea Kimi Antonelli Campeão (100% vs 0%)
  6. `03:10` - Tabela Oficial Geral de Classificação 2026

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- Python 3.10 ou superior
- Gerenciador de pacotes `pip` ou ambiente `conda`
- Chave de API do [Google AI Studio](https://aistudio.google.com/)

### 2. Clonar o repositório
```bash
git clone https://github.com/gustavocunha-io/f1-paddock-insights.git
cd f1-paddock-insights
```

### 3. Criar e ativar o ambiente virtual
```bash
# Opção A: com venv (padrão)
python -m venv venv

# No Windows:
.\venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate

# Instalar dependências:
pip install -r requirements.txt
```
```bash
# Opção B: com Conda
conda env create -f environment.yml
conda activate web_services
```

### 4. Executar a aplicação
```bash
python paddock.py
```
Acesse no seu navegador: **`http://localhost:5000`**

### 5. Inserir a(s) Chave(s) de API do Google Gemini
> **Zero dependência de arquivo `.env`:** Para segurança ao subir o código no GitHub, a chave da API é inserida diretamente no campo do formulário na tela inicial.
- Suporta **múltiplas chaves** separadas por vírgula para **rodízio automático (Round-Robin)** e fallback se uma cota esgotar.
- A chave é salva automaticamente no seu navegador (`localStorage`).

---

## ⚙️ Como Ativar o GitHub Pages no Repositório

Para publicar ou atualizar o site estático no GitHub Pages:

1. Acesse o repositório no GitHub: `https://github.com/gustavocunha-io/f1-paddock-insights`
2. Clique na aba **Settings** (Configurações)
3. No menu lateral esquerdo, clique em **Pages**
4. Em **Build and deployment**:
   - **Source:** Selecione `Deploy from a branch`
   - **Branch:** Selecione `main` e a pasta `/docs`
   - Clique em **Save**
5. Em poucos instantes o site estará no ar em:  
   `https://gustavocunha-io.github.io/f1-paddock-insights/`

---

## 📁 Estrutura de Diretórios

```
f1-paddock-insights/
├── paddock.py               # Servidor Flask e rotas da aplicação
├── constantes.py            # URLs e constantes de raspagem
├── requirements.txt         # Dependências pip
├── environment.yml          # Especificação do ambiente Conda
├── api/                     # Módulos de integração com APIs
│   ├── open_f1.py           # Cliente da OpenF1 REST API
│   └── gemini.py            # Integração com Google Gemini (google-genai)
├── scraping/                # Módulo de Web Scraping com BeautifulSoup
│   ├── extrator.py          # Extrator de notícias e tabela do Grande Prêmio
│   └── models/              # Modelos de dados (Piloto, Classificação)
├── static/                  # Estilos CSS do app Flask
├── templates/               # Templates Jinja2 (index, exibir, classificacao)
└── docs/                    # 🚀 Site de Apresentação no GitHub Pages
    ├── index.html           # Página principal responsiva mobile-first
    ├── css/
    │   └── style.css        # Folha de estilos responsiva mobile-first
    ├── js/
    │   └── main.js          # Simulador de telemetria, vídeo e drawer menu
    └── assets/
        ├── images/          # Mockups, diagramas SVG, favicon e poster
        │   ├── favicon.svg
        │   ├── architecture-diagram.svg
        │   ├── mockup-mobile-home.svg
        │   ├── mockup-telemetry-champion.svg
        │   ├── mockup-radio-gemini.svg
        │   ├── mockup-standings.svg
        │   └── demo-poster.svg
        └── videos/          # Vídeo de demonstração
            ├── demo.mp4
            └── README.md
```

---

## 👨‍💻 Autor

- **Gustavo Cunha** &bull; [GitHub](https://github.com/gustavocunha-io)
- Trabalho Prático Individual &bull; Disciplina de **Web Services**
