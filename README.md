# News Portal Scraper & Sentiment Analysis

## Descrição

Ferramenta de web scraping desenvolvida em Python para monitorar, coletar e analisar notícias de diversos portais brasileiros. O sistema extrai artigos completos, realiza uma análise de sentimento sobre o conteúdo e armazena os dados consolidados em um banco de dados MySQL. A arquitetura é modular, orientada a objetos e permite fácil expansão para novos portais.

## Portais Suportados

1.  **G1** - Notícias gerais
2.  **Exame** - Notícias econômicas e financeiras
3.  **CartaCapital** - Notícias políticas e análises
4.  **MoneyTimes** - Mercado financeiro e investimentos
5.  **Suno** - Notícias de investimentos e finanças pessoais

## Funcionalidades Principais

### Extração Automatizada de Notícias

  - Coleta de títulos, links, datas de publicação e conteúdo completo dos artigos.
  - Suporte a múltiplas páginas com busca baseada em períodos de tempo definidos.
  - Verificação de notícias duplicadas para garantir que apenas novos artigos sejam inseridos no banco de dados.

### Análise de Sentimentos

  - Análise automática do sentimento de cada artigo (positivo, neutro ou negativo).
  - Utiliza o modelo pré-treinado `cardiffnlp/twitter-xlm-roberta-base-sentiment` da biblioteca `transformers` para alta acurácia na classificação.
  - Armazena o resultado da análise (sentimento e pontuação de confiança) junto com os dados da notícia.

### Armazenamento em Banco de Dados

  - Integração com MySQL para armazenamento persistente e estruturado dos dados.
  - Salva o artigo completo, metadados (título, link, data da notícia, data da coleta) e os resultados da análise de sentimento.

## Requisitos Técnicos

### Dependências Principais

  - Python 3.8+
  - Bibliotecas essenciais:
      - `requests`
      - `beautifulsoup4`
      - `cloudscraper` (para portais com proteção anti-bot)
      - `pymysql` (para conexão com o banco de dados MySQL)
      - `python-dotenv` (para gerenciamento de credenciais)
      - `transformers`
      - `torch`
      - `sentencepiece`

### Instalação

Clone o repositório e instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Como Utilizar

1.  **Configure o Ambiente**: Crie um arquivo `.env` na raiz do projeto para definir as variáveis de ambiente do seu banco de dados.

    ```env
    DB_HOST=seu_host
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=seu_banco_de_dados
    ```

2.  **Execute o Script**: Inicie o programa executando o script principal.

    ```bash
    python src/main.py
    ```

3.  **Selecione o Portal**: Escolha um dos portais listados no menu interativo.

      - `1` para G1
      - `2` para Exame
      - `3` para CartaCapital
      - `4` para MoneyTimes
      - `5` para Suno
      - `6` para Todos (em desenvolvimento)
      - `7` para Sair

4.  **Escolha o Período**: Selecione o intervalo de tempo para a busca das notícias (as opções podem variar entre os portais).

5.  **Aguarde a Coleta**: O sistema irá buscar e processar as notícias, exibindo o progresso no terminal. Ao final, os dados serão salvos no banco de dados.

## Exemplo de Saída

### Interação no Terminal

```plaintext
Bem-vindo ao Keyword Monitor!
Essa ferramenta coleta notícias de portais brasileiros e conta a quantidade de ocorrências de uma palavra-chave no corpo de cada artigo.

Você deseja analisar qual desses portais?
1 - G1
2 - Exame
3 - Carta Capital
4 - Money Times
5 - Suno
6 - Todos
7 - Sair
> 1

Você deseja analisar qual período?
1 - 1 hora
2 - Hoje 
3 - 7 dias
> 2

Verificando página 1...
Verificando página 2...
- Coletado: Nova política econômica é anunciada pelo governo e divide opiniões
Página 1 de 2
- Coletado: Mercado reage positivamente às novas medidas de incentivo
Página 1 de 2

Coleta finalizada: (2 notícias coletadas e 2 inseridas com sucesso.)
```

### Dados no Banco de Dados

As notícias são salvas em uma tabela com a seguinte estrutura: `(title, link, scraping_date, news_date, article, sentiment_analysis, confidence_score)`.

## Estrutura do Projeto

```
news-portals-keyword-scraper/
├── .gitignore
├── README.md
├── requirements.txt
└── src/
    ├── main.py                 # Script principal que inicia a aplicação
    ├── dto/                    # Módulos de Data Transfer Object (Scrapers)
    │   ├── g1_scraper.py
    │   ├── exame_scraper.py
    │   ├── carta_scraper.py
    │   ├── moneytimes_scraper.py
    │   └── suno_scraper.py
    └── service/                # Módulos de serviço
        ├── run_scrapers.py     # Orquestra a execução dos scrapers
        ├── save_database.py    # Gerencia a conexão e inserção no DB
        ├── sentiment_analysis.py # Realiza a análise de sentimento
        └── user_input.py       # Gerencia a entrada do usuário
```