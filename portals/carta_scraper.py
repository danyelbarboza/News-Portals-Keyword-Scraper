import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, timedelta
import random
from portals.scraper_base import NewsScraper
from fake_useragent import UserAgent


ua = UserAgent()
headers = {"User-Agent": ua.random}


class CartaCapitalScraper(NewsScraper):
    def get_news(self, period):
        news_list = []
        for pagina in range(1, self.get_pages_news(period)):
            try:
                res = requests.get(f"https://www.cartacapital.com.br/mais-recentes/page/{pagina}", timeout = 20)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar página {pagina}: {e}")
                continue
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("a", class_="l-list__item") # Extrai as notícias
            time.sleep(random.uniform(0.3, 0.6))
            last_page = pagina
            for article in articles:
                title_tag = article.find("h2") if article.find("h2") else None
                title = title_tag.text.strip() if title_tag else "Sem título"
                link = article["href"] if article else None
                timestamp = article.find("span")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
                match = re.search(r'\d{2}\.\d{2}\.\d{4} \d{2}h\d{2}', time_text)
                date_str = match.group().replace("h", ":") 
                date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M")


                news_list.append({
                    "title": title,
                    "link": link,
                    "time": date_obj,
                    "current_page": pagina
                })


        return news_list, last_page

    # Conta o número de páginas com notícias recentes
    def get_pages_news(self, period):
        paginas = 2
        while True:
            res = requests.get(f"https://www.cartacapital.com.br/mais-recentes/page/{paginas}")
            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all("a", class_="l-list__item")
            time.sleep(random.uniform(0.1, 0.5))
            stop = False
            print(f"Verificando página {paginas - 1}...")
            for article in articles:
                timestamp = article.find("span")
                time_text = timestamp.get_text(separator=" ", strip=True) if timestamp else "Horário não encontrado"
                match = re.search(r'\d{2}\.\d{2}\.\d{4} \d{2}h\d{2}', time_text)
                date_str = match.group().replace("h", ":") 
                date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
                diference = datetime.now() - date_obj
                if period == 1:
                    if diference > timedelta(hours=1):
                        stop = True
                        break
                elif period == 2:
                    if diference > timedelta(days=1):
                        stop = True
                        break
                elif period == 3:
                    if diference > timedelta(days=7):
                        stop = True
                        break
                elif period == 4:
                    if diference > timedelta(days=30):
                        stop = True
                        break
            if stop:
                break    
            paginas += 1
        return paginas

    # Conta ocorrências da keyword no artigo. Essa função é usada quando trabalhamos com CSV
    def count_keyword_in_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find("div", class_="content-closed contentOpen")
            if full_article is None:
                return 0
            all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
            text = " ".join([p.get_text(strip=True) for p in all_paragraphs])
            matches = re.findall(fr"\b{re.escape(self.keyword)}\b", text, flags=re.IGNORECASE)
            return len(matches)
        except Exception as e:
            return e
        return None
    
    # Retorna o texto completo do artigo. Essa função é usada quando trabalhamos com MySQL
    def get_full_article(self, url):
        try:
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")


            full_article = soup.find("div", class_="content-closed contentOpen")
            all_paragraphs = full_article.find_all("p") if full_article.find("p") else None
            text = " ".join([p.get_text(strip=True) for p in all_paragraphs])
            return text
        except Exception as e:
            return e