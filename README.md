# G1 Keyword Scraper

## Descrição
Ferramenta de web scraping para extrair as últimas notícias do portal G1 e contar a quantidade de ocorrências de uma palavra-chave no **texto completo** de cada artigo. Desenvolvido em Python, utilizando as bibliotecas `requests`, `BeautifulSoup` e `csv` para processar e armazenar os dados extraídos.

## Funcionalidades Principais
### Extração de Notícias
- Extrai os títulos, links e horários de publicação das notícias do G1
- Suporta páginas de notícias atuais
- Busca e conta a ocorrência de uma palavra-chave no texto completo de cada artigo
- Armazenamento dos dados extraídos em um arquivo CSV estruturado

## Requisitos Técnicos
- Python 3.x
- Bibliotecas `requests`, `beautifulsoup4` e `csv`

Instalação das dependências:
```bash
pip install requests beautifulsoup4
```

## Como Utilizar
1. Execute o script no terminal:
   ```bash
   python g1_keyword_scraper.py
   ```

2. O script solicitará que você insira uma palavra-chave para buscar no texto dos artigos do dia.

3. O script buscará automaticamente as notícias mais recentes no G1, acessará os artigos e verificará quantas vezes a palavra-chave aparece em cada um deles.

4. As notícias e os dados relacionados (título, link, horário de publicação e contagem da palavra-chave) serão salvos em um arquivo CSV chamado `g1_keyword_noticias.csv`.

## Exemplo de Saída no Terminal
```plaintext
Coletado: Governo anuncia novo pacote de medidas econômicas - Keyword: 3
Página atual: 1
Coletado: Protestos tomam as ruas em várias cidades - Keyword: 1
Página atual: 1
Coleta finalizada (5 notícias salvas)
Keyword total: 7
```

## Exemplo de Conteúdo do Arquivo CSV
```csv
data_coleta,titulo,link,horario_g1,keyword_count,keyword_used
2025-04-22 12:30:45,Governo anuncia novo pacote de medidas econômicas,https://g1.globo.com/politica/noticia/2025/04/22/pacote-de-medidas.ghtml,12:05,3,keyword
2025-04-22 12:31:10,Protestos tomam as ruas em várias cidades,https://g1.globo.com/brasil/noticia/2025/04/22/protestos.ghtml,11:50,1,keyword
```

## Licença
MIT License - Disponível para uso e modificação. Consulte o arquivo LICENSE para detalhes.

--------------------------------------
# G1 Keyword Scraper

## Description
A web scraping tool to extract the latest news from the G1 portal and count the occurrences of a specific keyword in the **full text** of each article. Developed in Python, using the `requests`, `BeautifulSoup`, and `csv` libraries to process and store the extracted data.

## Key Features
### News Extraction
- Extracts titles, links, and publication times of G1 news articles
- Supports current news pages
- Searches and counts the occurrences of a keyword in the full text of each article
- Stores the extracted data in a structured CSV file

## Technical Requirements
- Python 3.x
- `requests`, `beautifulsoup4`, and `csv` libraries

Install the dependencies:
```bash
pip install requests beautifulsoup4
```

## How to Use
1. Run the script in the terminal:
   ```bash
   python g1_keyword_scraper.py
   ```

2. The script will ask you to input a keyword to search for in the articles' text.

3. The script will automatically fetch the latest news from G1, visit the articles, and check how many times the keyword appears in each one.

4. The news and related data (title, link, publication time, and keyword count) will be saved in a CSV file named `g1_keyword_noticias.csv`.

## Example Output in Terminal
```plaintext
Collected: Government announces new economic measures package - Keyword: 3
Current page: 1
Collected: Protests take over the streets in several cities - Keyword: 1
Current page: 1
Collection finished (5 news articles saved)
Keyword total: 7
```

## Example CSV File Content
```csv
data_collected,title,link,g1_time,keyword_count,keyword_used
2025-04-22 12:30:45,Government announces new economic measures package,https://g1.globo.com/politica/noticia/2025/04/22/pacote-de-medidas.ghtml,12:05,3,keyword
2025-04-22 12:31:10,Protests take over the streets in several cities,https://g1.globo.com/brasil/noticia/2025/04/22/protestos.ghtml,11:50,1,keyword
```

## License
MIT License - Available for use and modification. Please refer to the LICENSE file for details.
