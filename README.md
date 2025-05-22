# News Portals Keyword Scraper

## Descrição
Ferramenta avançada de web scraping desenvolvida em Python para monitorar e analisar a ocorrência de palavras-chave em artigos de notícias de diversos portais brasileiros. O sistema é modular, orientado a objetos e permite fácil expansão para novos portais.

## Portais Suportados
1. **G1** - Notícias gerais
2. **Exame** - Notícias econômicas e financeiras
3. **CartaCapital** - Notícias políticas e análises
4. **MoneyTimes** - Mercado financeiro e investimentos
5. **Suno** - Notícias de investimentos e finanças pessoais

## Funcionalidades Principais

### Extração Avançada de Notícias
- Extração completa de títulos, links e horários de publicação
- Suporte a múltiplas páginas com detecção automática de limite temporal
- Contagem precisa de ocorrências de palavras-chave no conteúdo dos artigos
- Armazenamento em CSV com metadados completos

### Filtros Temporais Flexíveis
- Opções de período personalizáveis:
  - Última hora
  - Hoje
  - 7 dias
  - 30 dias
  - (Varia por portal)

### Arquitetura Modular
- Design baseado em classes abstratas para fácil implementação de novos scrapers
- Polimorfismo para tratamento uniforme de diferentes portais
- Tratamento robusto de erros e exceções

## Requisitos Técnicos

### Dependências Principais
- Python 3.8+
- Bibliotecas essenciais:
  - `requests`
  - `beautifulsoup4`
  - `fake-useragent`
  - `cloudscraper` (para portais com proteção anti-bot)

### Instalação
```bash
pip install requests beautifulsoup4 fake-useragent cloudscraper
```

## Como Utilizar

1. Execute o script principal:
   ```bash
   python main.py
   ```

2. Insira a palavra-chave que deseja monitorar

3. Selecione o portal de notícias:
   - `1` para G1
   - `2` para Exame
   - `3` para CartaCapital
   - `4` para MoneyTimes
   - `5` para Suno

4. Escolha o período de análise:
   - Opções variam por portal (última hora, hoje, 7 dias, 30 dias)

5. O sistema irá:
   - Buscar todas as notícias no período selecionado
   - Acessar cada artigo individualmente
   - Contar as ocorrências da palavra-chave
   - Gerar relatório completo em CSV

## Exemplo de Saída

### Terminal
```plaintext
Bem-vindo ao Keyword Monitor!
Digite a keyword que deseja analisar: bitcoin

Você deseja analisar qual desses portais?
1 - G1
2 - Exame
3 - Carta Capital
4 - Money Times
5 - Suno
> 4

Você deseja analisar qual período?
1 - 1 hora
2 - Hoje
3 - 30 dias
> 2

Verificando página 1...
Verificando página 2...
Coletado: Bitcoin atinge novo recorde histórico - Keyword: 8
Página atual: 1
Coletado: ETF de Bitcoin é aprovado nos EUA - Keyword: 12
Página atual: 1

Coleta finalizada (24 notícias salvas)
Keyword total: 87
```

### Arquivo CSV (exemplo)
```csv
data_coleta,titulo,link,horario,keyword_count,keyword_used
2025-05-22 14:30:15,Bitcoin atinge novo recorde histórico,https://www.moneytimes.com.br/bitcoin...,há 2 horas,8,bitcoin
2025-05-22 14:31:22,ETF de Bitcoin é aprovado nos EUA,https://www.moneytimes.com.br/etf...,hoje 09:45,12,bitcoin
```

## Estrutura do Projeto
```
news-scraper/
├── main.py                 # Script principal
├── scraper_base.py         # Classe abstrata base
├── g1_scraper.py           # Scraper para G1
├── exame_scraper.py        # Scraper para Exame
├── carta_scraper.py        # Scraper para CartaCapital
├── moneytimes_scraper.py   # Scraper para MoneyTimes
├── suno_scraper.py         # Scraper para Suno
└── README.md               # Documentação
```

## Melhorias Implementadas
- Suporte a 5 portais diferentes com estratégias específicas
- Mecanismos anti-bot (User-Agent aleatório, delays)
- Tratamento de diferentes formatos de data/hora
- Busca por conteúdo em múltiplos seletores CSS
- Filtragem temporal precisa

## Licença
MIT License - Consulte o arquivo LICENSE para detalhes.