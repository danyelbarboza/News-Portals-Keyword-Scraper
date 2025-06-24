from datetime import datetime
from service.save_database import Database
from datetime import timedelta, datetime
from service.sentiment_analysis import SentimentAnalysis


# Coleta as notícias e salva no banco de dados
def run_scraper_db(portal_scraper, period, portal_name):
    headers_news, last_page = portal_scraper.get_news(period) # Retorna as notícias em formato de lista e o número de páginas
    resultados = []
    db = Database()
    data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    for item in headers_news:
        if portal_name == "g1":
            if item['link']:
                full_article, news_date = portal_scraper.get_full_article(item['link'])
            else:
                full_article, news_date = None, None
            if full_article is None:
                continue
            diference = datetime.now() - news_date
            if period == ['minuto', 'minutos']:
                if diference > timedelta(hours=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas']:
                if diference > timedelta(days=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias']:
                if diference > timedelta(days=7):
                    break
            
            resultados.append({
                "title": item['title'],
                "link": item['link'],
                "scraping_date": data_coleta,
                "news_date": news_date,
                "article": full_article
            })
            print(f"- Coletado: {item['title']}")
            print(f"Página {item['current_page']} de {last_page}")
        
        elif portal_name == "moneytimes":
            if item['link']:
                print(item['link'])
                full_article, news_date = portal_scraper.get_full_article(item['link'])
            else:
                full_article, news_date = None, None
            if full_article is None:
                continue
            diference = datetime.now() - news_date
            if period == ['minuto', 'minutos']:
                if diference > timedelta(hours=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas']:
                if diference > timedelta(days=1):
                    break
            elif period == ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias', 'mes', 'meses']:
                if diference > timedelta(days=30):
                    break 
            
            resultados.append({
                "title": item['title'],
                "link": item['link'],
                "scraping_date": data_coleta,
                "news_date": news_date,
                "article": full_article
            })
            print(f"- Coletado: {item['title']}")
            print(f"Página {item['current_page']} de {last_page}")
            
            
        else:
            full_article = portal_scraper.get_full_article(item['link']) if item['link'] else None
            if full_article is None:
                continue
            diference = datetime.now() - item['time']
            if period == 1:
                if diference > timedelta(hours=1):
                    break
            elif period == 2:
                if diference > timedelta(days=1):
                    break
            elif period == 3:
                if diference > timedelta(days=7):
                    break
            elif period == 4:
                if diference > timedelta(days=30):
                    break
                
            resultados.append({
                "title": item['title'],
                "link": item['link'],
                "scraping_date": data_coleta,
                "news_date": item['time'],
                "article": full_article
            })
            print(f"- Coletado: {item['title']}")
            print(f"Página {item['current_page']} de {last_page}")
            
    sentiment, score = SentimentAnalysis().analyze(resultados)    
    db.insert_news(resultados, portal_name, sentiment, score)

    