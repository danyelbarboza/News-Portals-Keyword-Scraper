from datetime import datetime
from save_csv import SaveCSV
from save_database import Database

# Coleta as notícias e salva no csv
def run_scraper_csv(portal_scraper, period, portal_name, keyword):
    keyword_total_count = 0
    keyword_count = 0
    headers_news, last_page = portal_scraper.get_news(period) # Retorna as notícias em formato de lista e o número de páginas
    resultados = []
    data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    for item in headers_news:
        keyword_count = portal_scraper.count_keyword_in_article(item['link']) if item['link'] else None
        resultados.append({
            "titulo": item['title'],
            "link": item['link'],
            "scraping_date": data_coleta,
            "news_date": item['time'],
            "keyword_count": keyword_count
        })
        print(f"- Coletado: {item['title']}\n- Keyword: {keyword_count}")
        print(f"Página {item['current_page']} de {last_page}\n")
        keyword_total_count += keyword_count if keyword_count is not None else 0


    SaveCSV.save_to_csv(resultados, portal_name, keyword)
    print(f"\nColeta finalizada ({len(resultados)} notícias salvas em CSV)")
    print(f"Keyword total: {keyword_total_count}\n")

# Coleta as notícias e salva no banco de dados
def run_scraper_db(portal_scraper, period, portal_name):
    headers_news, last_page = portal_scraper.get_news(period) # Retorna as notícias em formato de lista e o número de páginas
    resultados = []
    db = Database()
    data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    for item in headers_news:
        full_article = portal_scraper.get_full_article(item['link']) if item['link'] else None
        resultados.append({
            "title": item['title'],
            "link": item['link'],
            "scraping_date": data_coleta,
            "news_date": item['time'],
            "article": full_article
        })
        print(f"- Coletado: {item['title']}")
        print(f"Página {item['current_page']} de {last_page}")
        
    db.insert_news(resultados, portal_name)

    