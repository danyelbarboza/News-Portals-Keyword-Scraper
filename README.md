# News Portals Keyword Scraper

## Descrição
Ferramenta de web scraping desenvolvida em Python para monitorar e analisar a ocorrência de palavras-chave em artigos de notícias de diversos portais brasileiros. O sistema é modular, orientado a objetos e permite fácil expansão para novos portais.

## Portais Suportados
1.  **G1** - Notícias gerais
2.  **Exame** - Notícias econômicas e financeiras
3.  **CartaCapital** - Notícias políticas e análises
4.  **MoneyTimes** - Mercado financeiro e investimentos
5.  **Suno** - Notícias de investimentos e finanças pessoais

## Funcionalidades Principais

### Extração Avançada de Notícias
-   Extração completa de títulos, links e horários de publicação.
-   Suporte a múltiplas páginas com detecção automática de limite temporal.
-   Contagem precisa de ocorrências de palavras-chave no conteúdo dos artigos (para saída CSV).
-   Armazenamento em CSV com metadados completos.
-   Armazenamento em banco de dados MySQL com o artigo completo e metadados.
-   Opção para executar o scraping em todos os portais suportados de uma vez.

### Filtros Temporais Flexíveis
-   Opções de período personalizáveis:
    -   Última hora
    -   Hoje
    -   7 dias
    -   30 dias
    -   (Varia por portal)

### Arquitetura Modular
-   Design baseado em classes abstratas para fácil implementação de novos scrapers.
-   Polimorfismo para tratamento uniforme de diferentes portais.
-   Tratamento robusto de erros e exceções.

## Requisitos Técnicos

### Dependências Principais
-   Python 3.8+
-   Bibliotecas essenciais:
    -   `requests`
    -   `beautifulsoup4`
    -   `fake-useragent`
    -   `cloudscraper` (para portais com proteção anti-bot)
    -   `pymysql` (para armazenamento em banco de dados)
    -   `python-dotenv` (para gerenciamento de credenciais do banco de dados)

### Instalação
```bash
pip install requests beautifulsoup4 fake-useragent cloudscraper pymysql python-dotenv
```

## Como Utilizar

1.  Configure as variáveis de ambiente para o banco de dados em um arquivo `.env` na raiz do projeto (caso opte por salvar em banco de dados):
    ```env
    DB_HOST=seu_host
    DB_USER=seu_usuario
    DB_PASSWORD=sua_senha
    DB_NAME=seu_banco_de_dados
    ```
2.  Execute o script principal:
    ```bash
    python main.py
    ```
   
3.  Insira a palavra-chave que deseja monitorar.

4.  Selecione o portal de notícias:
    -   `1` para G1
    -   `2` para Exame
    -   `3` para CartaCapital
    -   `4` para MoneyTimes
    -   `5` para Suno
    -   `6` para Todos os portais
    -   `7` para Sair

5.  Escolha o período de análise:
    -   Opções variam por portal (ex: última hora, hoje, 7 dias, 30 dias).

6.  Escolha como deseja salvar as notícias:
    - `1` para CSV
    - `2` para Banco de dados

7.  O sistema irá:
    -   Buscar todas as notícias no período selecionado.
    -   Acessar cada artigo individualmente.
    -   Se CSV: Contar as ocorrências da palavra-chave e gerar relatório completo em CSV.
    -   Se Banco de Dados: Salvar o título, link, data da coleta, data da notícia e o conteúdo completo do artigo no banco de dados.

## Exemplo de Saída

### Terminal
```plaintext
Bem-vindo ao Keyword Monitor!
Essa ferramenta coleta notícias de portais brasileiros e conta a quantidade de ocorrências de uma palavra-chave no corpo de cada artigo.

Digite a keyword que deseja analisar: bitcoin

Você deseja analisar qual desses portais?
1 - G1
2 - Exame
3 - Carta Capital
4 - Money Times
5 - Suno
6 - Todos
7 - Sair
> 4

Você deseja analisar qual período?
1 - 1 hora
2 - Hoje
3 - 30 dias
> 2

Você deseja salvar as notícias em CSV ou em um banco de dados?
1 - CSV
2 - Banco de dados
> 1

Verificando página 1...
Verificando página 2...
- Coletado: Bitcoin atinge novo recorde histórico
- Keyword: 8
Página 1 de 2

- Coletado: ETF de Bitcoin é aprovado nos EUA
- Keyword: 12
Página 1 de 2

Coleta finalizada (2 notícias salvas em CSV)
Keyword total: 20
```

### Arquivo CSV (exemplo) `moneytimes_keyword_noticias.csv`
```csv
titulo,link,scraping_date,news_date,keyword_count,keyword_used
Bitcoin atinge novo recorde histórico,https://www.moneytimes.com.br/bitcoin...,2025-05-23 10:30:15,há 2 horas,8,bitcoin
ETF de Bitcoin é aprovado nos EUA,https://www.moneytimes.com.br/etf...,2025-05-23 10:31:22,hoje 09:45,12,bitcoin
```


### Banco de Dados (exemplo de mensagem no terminal)
```plaintext
Verificando página 1...
- Coletado: Bitcoin atinge novo recorde histórico
Página 1 de 1
- Coletado: ETF de Bitcoin é aprovado nos EUA
Página 1 de 1

Coleta finalizada: (2 notícias coletadas e 2 inseridas com sucesso.)
```


## Estrutura do Projeto
```
news-scraper/
├── main.py                 # Script principal
├── user_input.py           # Gerencia a entrada do usuário e o fluxo do programa
├── run_scrapers.py         # Orquestra a execução dos scrapers e o salvamento dos dados
├── save_csv.py             # Módulo para salvar os dados em formato CSV
├── save_database.py        # Módulo para salvar os dados no banco de dados MySQL
├── portals/
│   ├── scraper_base.py     # Classe abstrata base para os scrapers
│   ├── g1_scraper.py       # Scraper para G1
│   ├── exame_scraper.py    # Scraper para Exame
│   ├── carta_scraper.py    # Scraper para CartaCapital
│   ├── moneytimes_scraper.py # Scraper para MoneyTimes
│   └── suno_scraper.py     # Scraper para Suno
├── .env                    # Arquivo para credenciais do banco de dados (não versionado)
└── README.md               # Documentação
```

## Melhorias Implementadas
-   Filtragem temporal precisa.
-   Opção de salvar em banco de dados MySQL.
-   Opção de realizar scraping em todos os portais configurados.
-   Verificação de notícias duplicadas ao salvar no banco de dados.

## Licença
MIT License - Consulte o arquivo LICENSE para detalhes.
