# News-Portals Keyword Scraper

## Descrição
Ferramenta de web scraping desenvolvida em Python para extrair as últimas notícias dos portais G1 e UOL, contando a quantidade de ocorrências de uma palavra-chave no corpo de cada artigo. O sistema é orientado a objetos, permitindo fácil expansão para novos portais no futuro.

## Funcionalidades Principais

### Extração de Notícias
- Extrai títulos, links e horários de publicação das notícias do G1 ou UOL.
- Suporta múltiplas páginas de notícias recentes.
- Conta a ocorrência de uma palavra-chave no texto completo de cada artigo.
- Armazena os dados extraídos em um arquivo CSV estruturado.

### Suporte a Múltiplos Portais
- Arquitetura baseada em herança e polimorfismo.
- Facilmente extensível com novos scrapers seguindo a interface `NewsScraper`.

## Requisitos Técnicos
- Python 3.x
- Bibliotecas:
  - `requests`
  - `beautifulsoup4`
  - `fake_useragent`

Instalação das dependências:
```bash
pip install requests beautifulsoup4 fake-useragent
```

## Como Utilizar
1. Execute o script principal:
   ```bash
   python main.py
   ```

2. Insira a palavra-chave que deseja buscar nos artigos.

3. Escolha o portal de notícias:
   - `1` para G1
   - `2` para UOL

4. O sistema buscará as notícias mais recentes, acessará os artigos e verificará a ocorrência da palavra-chave em cada um deles.

5. Os resultados serão salvos em um arquivo CSV, nomeado conforme o portal (`g1_keyword_noticias.csv` ou `uol_keyword_noticias.csv`).

## Exemplo de Saída no Terminal
```plaintext
Digite a keyword que deseja analisar: educação
Você deseja analisar qual desses portais?
1 - G1
2 - UOL
Coletado: Governo anuncia novo plano educacional - Keyword: 4
Página atual: 1
Coletado: Enem 2025 terá mudanças importantes - Keyword: 2
Página atual: 1
Coleta finalizada (10 notícias salvas)
Keyword total: 15
```

## Exemplo de Conteúdo do Arquivo CSV
```csv
data_coleta,titulo,link,horario,keyword_count,keyword_used
2025-04-22 12:45:01,Governo anuncia novo plano educacional,https://g1.globo.com/educacao/noticia/...,10:25,4,educação
2025-04-22 12:46:33,Enem 2025 terá mudanças importantes,https://g1.globo.com/educacao/noticia/...,09:58,2,educação
```

## Licença
MIT License - Disponível para uso e modificação. Consulte o arquivo LICENSE para detalhes.

--------------------------------------

# News-Portals Keyword Scraper

## Description
A Python-based web scraping tool that extracts the latest news articles from G1 and UOL news portals, counting how many times a specific keyword appears in the body of each article. The system is object-oriented, making it easy to extend to new news portals in the future.

## Main Features

### News Extraction
- Extracts titles, links, and publication times from G1 or UOL articles.
- Supports multiple pages of recent news.
- Counts the number of times a keyword appears in the full text of each article.
- Stores the extracted data in a structured CSV file.

### Multi-Portal Support
- Architecture based on inheritance and polymorphism.
- Easily extendable by implementing new scrapers using the `NewsScraper` interface.

## Technical Requirements
- Python 3.x
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `fake_useragent`

Install the dependencies:
```bash
pip install requests beautifulsoup4 fake-useragent
```

## How to Use
1. Run the main script:
   ```bash
   python main.py
   ```

2. Enter the keyword you want to search for in the articles.

3. Choose the news portal:
   - `1` for G1
   - `2` for UOL

4. The system will automatically fetch the latest articles, access each one, and count how many times the keyword appears.

5. Results will be saved in a CSV file named according to the chosen portal (`g1_keyword_noticias.csv` or `uol_keyword_noticias.csv`).

## Example Output in Terminal
```plaintext
Enter the keyword you want to analyze: education
Which portal do you want to analyze?
1 - G1
2 - UOL
Collected: Government announces new education plan - Keyword: 4
Current page: 1
Collected: ENEM 2025 will have important changes - Keyword: 2
Current page: 1
Scraping finished (10 news articles saved)
Total keyword count: 15
```

## Example CSV Output
```csv
data_coleta,titulo,link,horario,keyword_count,keyword_used
2025-04-22 12:45:01,Government announces new education plan,https://g1.globo.com/education/news/...,10:25,4,education
2025-04-22 12:46:33,ENEM 2025 will have important changes,https://g1.globo.com/education/news/...,09:58,2,education
```

## License
MIT License – Free to use and modify. See the LICENSE file for details.