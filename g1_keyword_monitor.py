import requests
from bs4 import BeautifulSoup
import re
import csv
import time
from datetime import datetime

CSV_FILE = 'g1_keyword_noticias.csv'

keyword_to_search = input("Escreva a palavra-chave que deseja verificar se existe nas notíticias de hoje: ")

def get_todays_g1_news():
    news_list = []
    for pagina in range(1, get_pages_today_g1_news() + 1):
        res = requests.get(f"https://g1.globo.com/ultimas-noticias/index/feed/pagina-{pagina}.ghtml")
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.find_all('div', class_='feed-post-body')

        for article in articles:
            title_tag = article.find('a', class_='feed-post-link')
            title = title_tag.text.strip() if title_tag else 'Sem título'
            link = title_tag['href'] if title_tag else None
            timestamp = article.find('span', class_='feed-post-datetime')
            time_text = timestamp.text.strip() if timestamp else 'Horário não encontrado'

            news_list.append({
                'title': title,
                'link': link,
                'time': time_text,
                'current_page': pagina
            })

    return news_list

def get_pages_today_g1_news():
    paginas = 2
    while True:
        res = requests.get(f"https://g1.globo.com/ultimas-noticias/index/feed/pagina-{paginas}.ghtml")
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.find_all('div', class_='feed-post-body')
        time.sleep(random.uniform(0.1, 0.5))
        stop = False
        print(f"Verificando página {paginas - 1}...")
        for article in articles:
            timestamp = article.find('span', class_='feed-post-datetime')
            time_text = timestamp.text.strip() if timestamp else 'Horário não encontrado'

            if not any(p in time_text.lower() for p in ['minuto', 'minutos', 'hora', 'horas']):
                stop = True
                break
            
        if stop:
            break    
        paginas += 1

    return paginas

def count_keyword_in_article(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        article = soup.find('article')
        if article:
            text = article.get_text(separator=' ', strip=True)
            matches = re.findall(r'\b' + keyword_to_search + r'\b', text, flags=re.IGNORECASE)
            return len(matches)
    except:
        return None
    return None

def save_to_csv(news_data):
    fieldnames = ['data_coleta', 'titulo', 'link', 'horario_g1', 'keyword_count', 'keyword_used']
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        try:
            f.seek(0)
            if f.read(1) == '':
                writer.writeheader()
        except:
            pass

        for row in news_data:
            row['keyword_used'] = keyword_to_search
            writer.writerow(row)

keyword_total_count = 0
keyword_count = 0

def run_scraper():
    global keyword_total_count, keyword_count
    noticias = get_todays_g1_news()
    resultados = []
    data_coleta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for item in noticias:
        keyword_count = count_keyword_in_article(item['link']) if item['link'] else None
        resultados.append({
            'data_coleta': data_coleta,
            'titulo': item['title'],
            'link': item['link'],
            'horario_g1': item['time'],
            'keyword_count': keyword_count
        })
        print(f"Coletado: {item['title']} - Keyword: {keyword_count}")
        print(f"Página atual: {item['current_page']}")
        keyword_total_count += keyword_count if keyword_count is not None else 0
        time.sleep(random.uniform(0.1, 0.5))

    save_to_csv(resultados)
    print(f"Coleta finalizada ({len(resultados)} notícias salvas)")
    print(f"Keyword total: {keyword_total_count}")

run_scraper()
